#ai-assisted with OCA/OpenAI Model with human supervision

"""Sync shared skill folders into Codex and Claude discovery paths."""

from __future__ import annotations

import argparse
import filecmp
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

TOOL_DIRECTORIES: dict[str, str] = {
    "claude": ".claude",
    "codex": ".codex",
}
DEFAULT_TARGET_FILTER = "both"
DEFAULT_ACTION = "sync"
DEFAULT_SOURCE_DIRECTORY_NAMES = ("general-skills", "cpv-skills", "skills", "SKILLS")
VALID_SKILL_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")
AI_DISCLOSURE = "#ai-assisted with OCA/OpenAI Model with human supervision"


@dataclass(frozen=True)
class RuntimeConfig:
    action: str
    target_root: Path
    skills_dirs: tuple[Path, ...]
    target_filter: str
    remove_skill_name: str | None
    remove_from_source: bool
    dry_run: bool
    mirror_targets: tuple[str, ...]
    strict_mirror: bool


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    return run(arguments, sys.stdout, sys.stderr)


def run(argv: list[str], stdout: TextIO, stderr: TextIO) -> int:
    parser = build_parser()
    namespace = parser.parse_args(argv)

    try:
        config = build_runtime_config(namespace)
        return execute_action(config, stdout, stderr)
    except SkillSyncError as error:
        print(f"ERROR: {error}", file=stderr)
        return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skills-manager",
        description="Sync, list, or remove shared Codex and Claude skills.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  skills-manager --home --skills ./general-skills --skills ./cpv-skills
  skills-manager list --home
  skills-manager remove cpv-ops --home
  skills-manager delete cpv-ops --target codex --dry-run
""",
    )
    parser.add_argument(
        "command",
        nargs="?",
        help="sync, list, ls, remove, rm, or delete. Defaults to sync.",
    )
    parser.add_argument("skill_name", nargs="?", help="Skill name for remove/delete.")
    parser.add_argument(
        "--root",
        type=Path,
        help="Directory that should receive .claude/ and .codex/.",
    )
    parser.add_argument(
        "--home",
        action="store_true",
        help="Use the current user's home directory as --root.",
    )
    parser.add_argument(
        "--skills",
        type=Path,
        action="append",
        default=[],
        help="Source skills directory. May be repeated. Defaults to auto-detection.",
    )
    parser.add_argument(
        "--target",
        choices=("both", "all", "claude", "codex"),
        default=DEFAULT_TARGET_FILTER,
        help="Operate on both tools or only one tool.",
    )
    parser.add_argument(
        "--from-source",
        action="store_true",
        help="With remove/delete, also remove the skill from the source directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show destructive operations without deleting anything.",
    )
    parser.add_argument(
        "--mirror",
        action="append",
        default=[],
        help="Mirror skills to an rsync destination. May be repeated.",
    )
    parser.add_argument(
        "--strict-mirror",
        action="store_true",
        help="Exit non-zero if any --mirror sync fails.",
    )
    return parser


def build_runtime_config(namespace: argparse.Namespace) -> RuntimeConfig:
    action, remove_skill_name = parse_action(namespace.command, namespace.skill_name)
    target_root = resolve_target_root(namespace.root, namespace.home)
    skills_dirs = resolve_skills_directories(namespace.skills, target_root, action)

    if action == "sync" and not skills_dirs:
        raise SkillSyncError(
            "Skills directory not found. Provide --skills or create general-skills/ or cpv-skills/."
        )

    if namespace.from_source and not skills_dirs:
        raise SkillSyncError("--from-source requires a source skills directory.")

    return RuntimeConfig(
        action=action,
        target_root=target_root,
        skills_dirs=skills_dirs,
        target_filter=namespace.target,
        remove_skill_name=remove_skill_name,
        remove_from_source=namespace.from_source,
        dry_run=namespace.dry_run,
        mirror_targets=tuple(namespace.mirror),
        strict_mirror=namespace.strict_mirror,
    )


def parse_action(command: str | None, skill_name: str | None) -> tuple[str, str | None]:
    if command is None:
        return DEFAULT_ACTION, None

    if command == "sync":
        require_no_skill_name(command, skill_name)
        return "sync", None

    if command in {"list", "ls"}:
        require_no_skill_name(command, skill_name)
        return "list", None

    if command in {"remove", "rm", "delete"}:
        if skill_name is None:
            raise SkillSyncError(f"{command} requires a skill name.")
        validate_skill_name(skill_name)
        return "remove", skill_name

    raise SkillSyncError(f"Unknown command: {command}")


def require_no_skill_name(command: str, skill_name: str | None) -> None:
    if skill_name is not None:
        raise SkillSyncError(f"{command} does not accept a skill name.")


def validate_skill_name(skill_name: str) -> None:
    if VALID_SKILL_NAME.fullmatch(skill_name) is None:
        raise SkillSyncError(
            f"Invalid skill name {skill_name!r}; use lowercase letters, digits, and hyphens."
        )


def resolve_target_root(root: Path | None, use_home: bool) -> Path:
    if use_home:
        return Path.home().resolve()

    if root is not None:
        return resolve_existing_directory(root, "--root")

    git_root = find_git_root(Path.cwd())
    if git_root is not None:
        return git_root

    return Path.cwd().resolve()


def resolve_existing_directory(path: Path, label: str) -> Path:
    expanded_path = path.expanduser()
    if not expanded_path.is_dir():
        raise SkillSyncError(f"{label} directory not found: {expanded_path}")
    return expanded_path.resolve()


def find_git_root(start_dir: Path) -> Path | None:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start_dir,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    if result.returncode != 0:
        return None

    git_root = Path(result.stdout.strip())
    if not git_root.is_dir():
        return None
    return git_root.resolve()


def resolve_skills_directories(
    explicit_skills_dirs: list[Path],
    target_root: Path,
    action: str,
) -> tuple[Path, ...]:
    if explicit_skills_dirs:
        return resolve_unique_directories(explicit_skills_dirs, "--skills")

    discovered_dirs = [
        candidate.resolve()
        for candidate in candidate_skill_directories(target_root)
        if candidate.is_dir()
    ]
    if discovered_dirs:
        return unique_paths(discovered_dirs)

    if action == "list":
        return ()

    return ()


def resolve_unique_directories(paths: list[Path], label: str) -> tuple[Path, ...]:
    resolved_paths = [resolve_existing_directory(path, label) for path in paths]
    return unique_paths(resolved_paths)


def unique_paths(paths: list[Path]) -> tuple[Path, ...]:
    unique_resolved_paths: list[Path] = []
    seen_paths: set[Path] = set()
    for path in paths:
        resolved_path = path.resolve()
        if resolved_path in seen_paths:
            continue
        unique_resolved_paths.append(resolved_path)
        seen_paths.add(resolved_path)
    return tuple(unique_resolved_paths)


def candidate_skill_directories(target_root: Path) -> list[Path]:
    current_dir = Path.cwd()
    project_root = Path(__file__).resolve().parents[2]
    base_dirs = (target_root, current_dir, project_root)
    candidates: list[Path] = []

    for base_dir in base_dirs:
        for source_name in DEFAULT_SOURCE_DIRECTORY_NAMES:
            candidates.append(base_dir / source_name)

    return candidates


def execute_action(config: RuntimeConfig, stdout: TextIO, stderr: TextIO) -> int:
    if config.action == "sync":
        return sync_skills(config, stdout, stderr)

    if config.action == "list":
        list_skills(config, stdout)
        return 0

    if config.action == "remove":
        remove_skill(config, stdout)
        return 0

    raise SkillSyncError(f"Unsupported action: {config.action}")


def sync_skills(config: RuntimeConfig, stdout: TextIO, stderr: TextIO) -> int:
    assert config.skills_dirs

    prepare_source_trees(config.skills_dirs)
    source_label = format_source_dirs(config.skills_dirs)

    with tempfile.TemporaryDirectory(prefix="skills-manager-") as temp_dir:
        merged_source_dir = build_merged_skills_tree(config.skills_dirs, Path(temp_dir))

        for target_name in selected_targets(config.target_filter):
            sync_target(merged_source_dir, source_label, config.target_root, target_name, stdout)

        mirror_failures = mirror_skills(merged_source_dir, config.mirror_targets, stdout, stderr)

    print("Skills available at source:", file=stdout)
    log_source_skills(config.skills_dirs, stdout)
    print(file=stdout)

    if config.strict_mirror and mirror_failures:
        return 1
    return 0


def selected_targets(target_filter: str) -> tuple[str, ...]:
    if target_filter in {"both", "all"}:
        return tuple(TOOL_DIRECTORIES)
    return (target_filter,)


def sync_target(
    source_dir: Path,
    source_label: str,
    target_root: Path,
    target_name: str,
    stdout: TextIO,
) -> None:
    destination = target_root / TOOL_DIRECTORIES[target_name] / "skills"
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.is_dir() and directories_match(source_dir, destination):
        print(f"OK: {destination} already up to date", file=stdout)
    else:
        replace_directory(source_dir, destination)
        print(f"OK: {destination} refreshed from {source_label}", file=stdout)

    print(f"  Skills in {destination}:", file=stdout)
    log_skills(destination, stdout)
    print(file=stdout)


def directories_match(left: Path, right: Path) -> bool:
    if not right.exists():
        return False

    comparison = filecmp.dircmp(left, right)
    if comparison.left_only or comparison.right_only or comparison.funny_files:
        return False

    _, mismatches, errors = filecmp.cmpfiles(
        left,
        right,
        comparison.common_files,
        shallow=False,
    )
    if mismatches or errors:
        return False

    for common_dir in comparison.common_dirs:
        if not directories_match(left / common_dir, right / common_dir):
            return False

    return True


def replace_directory(source_dir: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)

    shutil.copytree(source_dir, destination, symlinks=True)
    prepare_skills_tree(destination)


def prepare_source_trees(source_dirs: tuple[Path, ...]) -> None:
    for source_dir in source_dirs:
        prepare_skills_tree(source_dir)


def build_merged_skills_tree(source_dirs: tuple[Path, ...], parent_dir: Path) -> Path:
    merged_dir = parent_dir / "skills"
    merged_dir.mkdir()

    for skill_dir in source_skill_directories(source_dirs):
        shutil.copytree(skill_dir, merged_dir / skill_dir.name, symlinks=True)

    prepare_skills_tree(merged_dir)
    return merged_dir


def source_skill_directories(source_dirs: tuple[Path, ...]) -> list[Path]:
    skill_dirs: list[Path] = []
    seen_skill_names: dict[str, Path] = {}

    for source_dir in source_dirs:
        for skill_dir in sorted_child_directories(source_dir):
            existing_source = seen_skill_names.get(skill_dir.name)
            if existing_source is not None:
                raise SkillSyncError(
                    f"Duplicate skill name {skill_dir.name!r} found in "
                    f"{existing_source.parent} and {source_dir}."
                )
            seen_skill_names[skill_dir.name] = skill_dir
            skill_dirs.append(skill_dir)

    return skill_dirs


def format_source_dirs(source_dirs: tuple[Path, ...]) -> str:
    return ", ".join(str(source_dir) for source_dir in source_dirs)


def mirror_skills(
    source_dir: Path,
    mirror_targets: tuple[str, ...],
    stdout: TextIO,
    stderr: TextIO,
) -> int:
    failures = 0
    for mirror_target in mirror_targets:
        command = ["rsync", "-av", "--delete", f"{source_dir}/", mirror_target]
        result = subprocess.run(
            command,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode == 0:
            print(f"OK: mirror refreshed at {mirror_target}", file=stdout)
        else:
            failures += 1
            print(f"WARN: mirror failed for {mirror_target}", file=stderr)
    return failures


def prepare_skills_tree(skills_dir: Path) -> None:
    for skill_dir in sorted_child_directories(skills_dir):
        manifest = skill_dir / "SKILL.md"
        if manifest.exists():
            continue
        manifest.write_text(placeholder_manifest(skill_dir.name), encoding="utf-8")


def placeholder_manifest(skill_name: str) -> str:
    return f"""---
name: {skill_name}
description: "Placeholder skill for {skill_name}. Replace this with complete instructions before use."
---

<!-- {AI_DISCLOSURE} -->

# SKILL: {skill_name}

## Purpose

Describe the responsibilities and workflow for the "{skill_name}" role.

## Usage

- List instructions that Codex or Claude should follow when this skill is invoked.
- Replace this placeholder text with real guidance.
"""


def list_skills(config: RuntimeConfig, stdout: TextIO) -> None:
    if not config.skills_dirs:
        print("Source skills:", file=stdout)
        print("    (source directory not found; provide --skills to include it)", file=stdout)
    else:
        print("Source skills:", file=stdout)
        log_source_skills(config.skills_dirs, stdout)
    print(file=stdout)

    for target_name in selected_targets(config.target_filter):
        target_dir = config.target_root / TOOL_DIRECTORIES[target_name] / "skills"
        print(f"{target_name.capitalize()} installed skills ({target_dir}):", file=stdout)
        log_skills(target_dir, stdout)
        print(file=stdout)


def remove_skill(config: RuntimeConfig, stdout: TextIO) -> None:
    assert config.remove_skill_name is not None

    print(f"Removing skill: {config.remove_skill_name}", file=stdout)
    if config.dry_run:
        print("Dry run: no files will be deleted.", file=stdout)
    print(file=stdout)

    for target_name in selected_targets(config.target_filter):
        target_dir = (
            config.target_root
            / TOOL_DIRECTORIES[target_name]
            / "skills"
            / config.remove_skill_name
        )
        label = f"{target_name.capitalize()} installed skills"
        remove_skill_directory(label, target_dir, config, stdout)

    if config.remove_from_source:
        assert config.skills_dirs
        for source_root in config.skills_dirs:
            source_dir = source_root / config.remove_skill_name
            remove_skill_directory(f"Source skills ({source_root})", source_dir, config, stdout)


def remove_skill_directory(
    label: str,
    skill_dir: Path,
    config: RuntimeConfig,
    stdout: TextIO,
) -> None:
    if not skill_dir.is_dir():
        print(f"- {label}: not found at {skill_dir}", file=stdout)
        return

    if config.dry_run:
        print(f"- {label}: would remove {skill_dir}", file=stdout)
        return

    shutil.rmtree(skill_dir)
    print(f"- {label}: removed {skill_dir}", file=stdout)


def log_skills(skills_dir: Path, stdout: TextIO) -> None:
    if not skills_dir.is_dir():
        print("    (directory not found)", file=stdout)
        return

    skill_dirs = sorted_child_directories(skills_dir)
    if not skill_dirs:
        print("    (no skills found)", file=stdout)
        return

    for skill_dir in skill_dirs:
        if (skill_dir / "SKILL.md").is_file():
            print(f"    - {skill_dir.name}", file=stdout)
        else:
            print(f"    - {skill_dir.name} (missing SKILL.md)", file=stdout)


def log_source_skills(source_dirs: tuple[Path, ...], stdout: TextIO) -> None:
    for source_dir in source_dirs:
        print(f"  {source_dir}:", file=stdout)
        log_skills(source_dir, stdout)


def sorted_child_directories(directory: Path) -> list[Path]:
    return sorted(
        path for path in directory.iterdir() if path.is_dir() and not path.name.startswith(".")
    )


class SkillSyncError(Exception):
    """Raised when CLI input or runtime state prevents a safe operation."""

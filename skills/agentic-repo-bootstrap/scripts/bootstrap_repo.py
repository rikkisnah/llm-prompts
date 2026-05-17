#ai-assisted with OCA/OpenAI Model with human supervision

"""Bootstrap or retrofit a repository with agentic engineering governance."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from render_templates import render_file, write_rendered_file

VALID_LANGUAGES = ("auto", "python", "go", "bash", "generic")
VALID_MODES = ("inspect", "bootstrap", "retrofit", "upgrade-strictness")
VALID_MATURITY = ("light", "standard", "strict")
VALID_RUNTIME_TYPES = ("library", "cli", "api", "webapp", "service", "docs-only")
DISCLOSURE = "#ai-assisted with OCA/OpenAI Model with human supervision"


@dataclass(frozen=True)
class RepoProfile:
    """Detected or selected target repository profile."""

    repo: Path
    mode: str
    language: str
    package_name: str
    runtime_type: str
    maturity: str
    dependency_manager: str
    deployment_docs: bool


@dataclass
class BootstrapReport:
    """Summary of repository bootstrap actions."""

    written: list[str] = field(default_factory=list)
    overwritten: list[str] = field(default_factory=list)
    symlinks: list[str] = field(default_factory=list)
    validation: list[str] = field(default_factory=list)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo = args.repo.expanduser().resolve()
    if not repo.exists():
        repo.mkdir(parents=True)
    profile = build_profile(args, repo)
    inspection = inspect_repo(profile)

    if profile.mode == "inspect":
        print(json.dumps(inspection, indent=2, sort_keys=True))
        return 0

    print(json.dumps({"inspection": inspection}, indent=2, sort_keys=True))
    report = bootstrap_repo(profile, run_validation=args.run_validation)
    print(json.dumps(report.__dict__, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Target repository path.")
    parser.add_argument("--mode", choices=VALID_MODES, default="bootstrap")
    parser.add_argument("--language", choices=VALID_LANGUAGES, default="auto")
    parser.add_argument("--package-name", default="", help="Package/module/project name.")
    parser.add_argument("--runtime-type", choices=VALID_RUNTIME_TYPES, default="library")
    parser.add_argument("--maturity", choices=VALID_MATURITY, default="standard")
    parser.add_argument("--run-validation", action="store_true", help="Run score/tests/validate after writes.")
    return parser


def build_profile(args: argparse.Namespace, repo: Path) -> RepoProfile:
    """Resolve runtime profile from arguments and repo contents."""

    language = detect_language(repo) if args.language == "auto" else args.language
    package_name = args.package_name or infer_package_name(repo)
    runtime_type = args.runtime_type
    maturity = next_maturity(repo) if args.mode == "upgrade-strictness" else args.maturity
    deployment_docs = runtime_type in {"api", "webapp", "service"}
    return RepoProfile(
        repo=repo,
        mode=args.mode,
        language=language,
        package_name=package_name,
        runtime_type=runtime_type,
        maturity=maturity,
        dependency_manager=detect_dependency_manager(repo, language),
        deployment_docs=deployment_docs,
    )


def detect_language(repo: Path) -> str:
    """Detect the dominant repository language."""

    if (repo / "go.mod").exists() or any(repo.glob("*.go")):
        return "go"
    if (repo / "pyproject.toml").exists() or any(repo.glob("*.py")) or (repo / "src").exists():
        return "python"
    if any(repo.glob("*.sh")) or (repo / "scripts").exists():
        return "bash"
    return "generic"


def infer_package_name(repo: Path) -> str:
    """Infer a package or project name from the directory."""

    return repo.name.replace("_", "-")


def detect_dependency_manager(repo: Path, language: str) -> str:
    """Detect the dependency manager for a language profile."""

    if language == "python":
        return "uv" if (repo / "uv.lock").exists() or shutil.which("uv") else "python"
    if language == "go":
        return "go modules" if (repo / "go.mod").exists() else "go modules"
    if language == "bash":
        return "none"
    return "existing project commands"


def next_maturity(repo: Path) -> str:
    """Choose the next maturity when upgrading strictness."""

    agents = repo / "AGENTS.md"
    if not agents.exists():
        return "standard"
    text = agents.read_text(encoding="utf-8").lower()
    if "maturity: strict" in text:
        return "strict"
    if "maturity: standard" in text:
        return "strict"
    return "standard"


def inspect_repo(profile: RepoProfile) -> dict[str, object]:
    """Inspect governance and tool state without writing files."""

    governance_files = [
        "README.md",
        "AGENTS.md",
        "CLAUDE.md",
        "MEMORY.md",
        "CONTEXT.md",
        "Makefile",
        "scripts/score_architecture.py",
        "tests/test_score_architecture.py",
        "docs/agent/clean-code-guide.md",
        "docs/adr/template.md",
    ]
    existing = [path for path in governance_files if (profile.repo / path).exists()]
    missing = [path for path in governance_files if path not in existing]
    return {
        "repo": str(profile.repo),
        "mode": profile.mode,
        "language": profile.language,
        "package_name": profile.package_name,
        "runtime_type": profile.runtime_type,
        "maturity": profile.maturity,
        "dependency_manager": profile.dependency_manager,
        "git_status": git_status(profile.repo),
        "existing_governance_files": existing,
        "missing_governance_files": missing,
        "tools": detect_tools(profile.language),
        "recommended_changes": missing,
    }


def git_status(repo: Path) -> str:
    """Return short git status when repo is under git."""

    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return "not a git repository or git unavailable"
    return result.stdout.strip() or "clean"


def detect_tools(language: str) -> dict[str, bool]:
    """Detect known validation tools."""

    expected = {
        "python": ("uv", "python3"),
        "go": ("go", "golangci-lint"),
        "bash": ("shellcheck", "shfmt", "bash"),
        "generic": ("make",),
    }.get(language, ("make",))
    return {tool: shutil.which(tool) is not None for tool in expected}


def bootstrap_repo(profile: RepoProfile, *, run_validation: bool) -> BootstrapReport:
    """Write governance files and optionally validate the result."""

    report = BootstrapReport()
    values = template_values(profile)
    template_root = Path(__file__).resolve().parents[1] / "assets" / "templates"
    for target_path, template_name in selected_templates(profile):
        rendered = render_file(template_root / template_name, values)
        absolute_target = profile.repo / target_path
        overwritten = write_rendered_file(absolute_target, rendered)
        (report.overwritten if overwritten else report.written).append(target_path)

    update_gitignore(profile.repo, report)
    create_claude_symlink(profile.repo, report)

    if run_validation:
        report.validation.extend(run_validation_commands(profile.repo))
    return report


def template_values(profile: RepoProfile) -> dict[str, str]:
    """Build template substitutions."""

    language_guide = f"docs/agent/{profile.language}-style-guide.md"
    return {
        "PROJECT_NAME": profile.package_name,
        "PACKAGE_NAME": profile.package_name,
        "LANGUAGE": profile.language,
        "LANGUAGE_TITLE": profile.language.title(),
        "LANGUAGE_STYLE_GUIDE": language_guide,
        "RUNTIME_TYPE": profile.runtime_type,
        "MATURITY": profile.maturity,
        "DEPENDENCY_MANAGER": profile.dependency_manager,
        "DISCLOSURE": DISCLOSURE,
        "DISCLOSURE_MD": "<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->",
    }


def selected_templates(profile: RepoProfile) -> list[tuple[str, str]]:
    """Return target paths and template names for this profile."""

    language_template = f"docs-agent-{profile.language}-style-guide.md.j2"
    makefile_template = f"Makefile.{makefile_profile(profile.language)}.j2"
    targets = [
        ("README.md", "README.md.j2"),
        ("AGENTS.md", "AGENTS.md.j2"),
        ("MEMORY.md", "MEMORY.md.j2"),
        ("CONTEXT.md", "CONTEXT.md.j2"),
        ("Makefile", makefile_template),
        ("scripts/score_architecture.py", "score_architecture.py.j2"),
        ("tests/test_score_architecture.py", "test_score_architecture.py.j2"),
        ("docs/agent/clean-code-guide.md", "docs-agent-clean-code-guide.md.j2"),
        ("docs/agent/review-guide.md", "docs-agent-review-guide.md.j2"),
        ("docs/agent/testing-guide.md", "docs-agent-testing-guide.md.j2"),
        (f"docs/agent/{profile.language}-style-guide.md", language_template),
        ("docs/adr/template.md", "docs-adr-template.md.j2"),
    ]
    if profile.runtime_type in {"library", "cli", "api", "webapp", "service"}:
        targets.append(("INSTALL.md", "INSTALL.md.j2"))
    targets.extend([("DEVELOP.md", "DEVELOP.md.j2"), ("CREATE-PR.md", "CREATE-PR.md.j2")])
    if profile.deployment_docs:
        targets.append(("DEPLOY.md", "DEPLOY.md.j2"))
    return targets


def makefile_profile(language: str) -> str:
    """Map a language to a Makefile template profile."""

    if language in {"python", "go", "bash"}:
        return "python.uv" if language == "python" else language
    return "generic"


def update_gitignore(repo: Path, report: BootstrapReport) -> None:
    """Append required local artifact ignores without hiding CONTEXT.md."""

    required_lines = [
        ".env",
        ".env.local",
        ".env.production",
        ".env.development",
        "*.log",
        "tmp/",
        ".temp/",
        ".cache/",
        ".pytest_cache/",
        ".mypy_cache/",
        ".ruff_cache/",
        "__pycache__/",
        "dist/",
        "build/",
        ".coverage",
        "htmlcov/",
        ".venv/",
        ".uv-cache/",
        "!.env.example",
        "!.env.sample",
        "!.env.template",
    ]
    path = repo / ".gitignore"
    existing = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    merged = list(existing)
    changed = False
    for line in required_lines:
        if line not in merged:
            merged.append(line)
            changed = True
    if changed:
        path.write_text("\n".join(merged).rstrip() + "\n", encoding="utf-8")
        (report.overwritten if existing else report.written).append(".gitignore")


def create_claude_symlink(repo: Path, report: BootstrapReport) -> None:
    """Create or replace CLAUDE.md as a symlink to AGENTS.md."""

    claude = repo / "CLAUDE.md"
    if claude.exists() or claude.is_symlink():
        if claude.is_dir():
            raise IsADirectoryError(f"Cannot replace directory: {claude}")
        claude.unlink()
    os.symlink("AGENTS.md", claude)
    report.symlinks.append("CLAUDE.md -> AGENTS.md")


def run_validation_commands(repo: Path) -> list[str]:
    """Run generated validation commands and summarize results."""

    summaries: list[str] = []
    commands = [
        ["make", "score"],
        ["python3", "-m", "unittest", "tests/test_score_architecture.py"],
        ["make", "validate"],
    ]
    for command in commands:
        result = subprocess.run(command, cwd=repo, check=False, capture_output=True, text=True)
        status = "passed" if result.returncode == 0 else f"failed ({result.returncode})"
        summaries.append(f"{' '.join(command)}: {status}")
    return summaries


if __name__ == "__main__":
    raise SystemExit(main())

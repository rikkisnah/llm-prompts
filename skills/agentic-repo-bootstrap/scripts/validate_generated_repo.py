#ai-assisted with OCA/OpenAI Model with human supervision

"""Validate the expected governance files in a bootstrapped repository."""

from __future__ import annotations

import argparse
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path


REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "MEMORY.md",
    "CONTEXT.md",
    "Makefile",
    "scripts/score_architecture.py",
    "tests/test_score_architecture.py",
    "docs/agent/clean-code-guide.md",
    "docs/agent/review-guide.md",
    "docs/agent/testing-guide.md",
    "docs/adr/template.md",
)


@dataclass(frozen=True)
class ValidationResult:
    """One validation check result."""

    name: str
    passed: bool
    detail: str


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--run-score", action="store_true")
    args = parser.parse_args(argv)

    results = validate_repo(args.repo.resolve(), run_score=args.run_score)
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"{status} {result.name}: {result.detail}")
    return 0 if all(result.passed for result in results) else 1


def validate_repo(repo: Path, *, run_score: bool = False) -> list[ValidationResult]:
    """Run structural validation for generated governance files."""

    results = [
        ValidationResult("repo exists", repo.is_dir(), str(repo)),
        *validate_required_files(repo),
        validate_claude_symlink(repo),
        validate_agents_line_count(repo),
    ]
    if run_score:
        results.append(validate_score_command(repo))
    return results


def validate_required_files(repo: Path) -> list[ValidationResult]:
    """Validate required file existence."""

    return [
        ValidationResult(f"file {relative_path}", (repo / relative_path).exists(), relative_path)
        for relative_path in REQUIRED_FILES
    ]


def validate_claude_symlink(repo: Path) -> ValidationResult:
    """Validate CLAUDE.md points to AGENTS.md."""

    claude = repo / "CLAUDE.md"
    passed = claude.is_symlink() and os.readlink(claude) == "AGENTS.md"
    return ValidationResult("CLAUDE.md symlink", passed, "CLAUDE.md -> AGENTS.md")


def validate_agents_line_count(repo: Path) -> ValidationResult:
    """Validate AGENTS.md stays compact."""

    agents = repo / "AGENTS.md"
    if not agents.exists():
        return ValidationResult("AGENTS.md line count", False, "missing")
    line_count = len(agents.read_text(encoding="utf-8").splitlines())
    return ValidationResult("AGENTS.md line count", line_count < 200, f"{line_count} lines")


def validate_score_command(repo: Path) -> ValidationResult:
    """Run the generated score gate."""

    result = subprocess.run(
        ["python3", "scripts/score_architecture.py", "--min-score", "10"],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )
    detail = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else result.stderr.strip()
    return ValidationResult("score gate", result.returncode == 0, detail or "no output")


if __name__ == "__main__":
    raise SystemExit(main())

#ai-assisted with OCA/OpenAI Model with human supervision

"""Detect and optionally install known validation tools for bootstrapped repos."""

from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass


KNOWN_TOOLS: dict[str, tuple[str, ...]] = {
    "python": ("uv",),
    "go": ("go", "golangci-lint"),
    "bash": ("shellcheck", "shfmt"),
    "generic": (),
}


@dataclass(frozen=True)
class ToolPlan:
    """A validation tool installation recommendation."""

    tool: str
    installed: bool
    command: tuple[str, ...] | None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=sorted(KNOWN_TOOLS), default="generic")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Install known missing tools with the detected package manager.",
    )
    args = parser.parse_args(argv)

    plans = plan_tools(args.language)
    for plan in plans:
        status = "present" if plan.installed else "missing"
        print(f"{plan.tool}: {status}")
        if not plan.installed and plan.command:
            print(f"  install: {' '.join(plan.command)}")

    if args.apply:
        for plan in plans:
            if plan.installed or plan.command is None:
                continue
            print(f"Installing {plan.tool}...")
            result = subprocess.run(plan.command, check=False)
            if result.returncode != 0:
                print(f"ERROR: failed to install {plan.tool}", file=sys.stderr)
                return result.returncode

    return 0


def plan_tools(language: str) -> list[ToolPlan]:
    """Return the known validation tool state for a language profile."""

    return [
        ToolPlan(tool=tool, installed=shutil.which(tool) is not None, command=install_command(tool))
        for tool in KNOWN_TOOLS.get(language, ())
    ]


def install_command(tool: str) -> tuple[str, ...] | None:
    """Return a conservative install command for a known tool."""

    if tool == "golangci-lint" and shutil.which("go"):
        return ("go", "install", "github.com/golangci/golangci-lint/cmd/golangci-lint@latest")
    if tool == "shfmt" and shutil.which("go"):
        return ("go", "install", "mvdan.cc/sh/v3/cmd/shfmt@latest")

    package_manager = detect_package_manager()
    if package_manager == "brew":
        return ("brew", "install", tool)
    if package_manager == "apt-get":
        package_name = "golangci-lint" if tool == "golangci-lint" else tool
        return ("sudo", "apt-get", "install", "-y", package_name)

    if tool == "uv":
        if package_manager == "brew":
            return ("brew", "install", "uv")
        return None

    return None


def detect_package_manager() -> str | None:
    """Detect a local package manager for known developer tools."""

    if shutil.which("brew"):
        return "brew"
    if platform.system().lower() == "linux" and shutil.which("apt-get"):
        return "apt-get"
    return None


if __name__ == "__main__":
    raise SystemExit(main())

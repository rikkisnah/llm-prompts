#ai-assisted with OCA/OpenAI Model with human supervision

"""Parse Python source files without writing bytecode caches."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

SOURCE_ROOTS = (Path("src"), Path("tests"))


def main() -> int:
    for source_file in iter_python_files(SOURCE_ROOTS):
        parse_source_file(source_file)
    return 0


def iter_python_files(roots: tuple[Path, ...]) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        if root.exists():
            files.extend(root.rglob("*.py"))
    return sorted(files)


def parse_source_file(source_file: Path) -> None:
    source_text = source_file.read_text(encoding="utf-8")
    ast.parse(source_text, filename=str(source_file))


if __name__ == "__main__":
    raise SystemExit(main())

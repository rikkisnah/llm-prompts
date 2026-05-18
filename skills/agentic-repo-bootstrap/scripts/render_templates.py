#ai-assisted with OCA/OpenAI Model with human supervision

"""Small dependency-free template renderer for repo bootstrap assets."""

from __future__ import annotations

from pathlib import Path
def render_text(template_text: str, values: dict[str, str]) -> str:
    """Render a template using explicit token replacement.

    This intentionally avoids a full template language so Makefile variables
    such as ``$(UV)`` and shell snippets remain untouched.
    """

    rendered_text = template_text
    for key, value in sorted(values.items(), key=lambda item: len(item[0]), reverse=True):
        rendered_text = rendered_text.replace(f"${key}", value)
    return rendered_text


def render_file(template_path: Path, values: dict[str, str]) -> str:
    """Read and render a template file."""

    return render_text(template_path.read_text(encoding="utf-8"), values)


def write_rendered_file(target_path: Path, rendered_text: str) -> bool:
    """Write rendered text and return True when an existing file was overwritten."""

    was_existing_file = target_path.exists() or target_path.is_symlink()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(rendered_text, encoding="utf-8")
    return was_existing_file

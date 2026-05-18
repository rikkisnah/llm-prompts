#ai-assisted with OCA/OpenAI Model with human supervision

from __future__ import annotations

import io
import tempfile
import unittest
from pathlib import Path

from skills_manager.cli import run


class SkillManagerCliTests(unittest.TestCase):
    def test_sync_installs_skills_for_claude_and_codex(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "target"
            source = Path(temp_dir) / "source"
            create_skill(source, "cpv-ops")
            root.mkdir()

            result = run_cli(["sync", "--root", str(root), "--skills", str(source)])

            self.assertEqual(result.exit_code, 0, result.stderr)
            self.assertTrue((root / ".claude" / "skills" / "cpv-ops" / "SKILL.md").is_file())
            self.assertTrue((root / ".codex" / "skills" / "cpv-ops" / "SKILL.md").is_file())
            self.assertIn("cpv-ops", result.stdout)

    def test_sync_merges_multiple_source_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "target"
            general_source = Path(temp_dir) / "general-skills"
            cpv_source = Path(temp_dir) / "cpv-skills"
            create_skill(general_source, "skill-authoring")
            create_skill(cpv_source, "cpv-ops")
            root.mkdir()

            result = run_cli(
                [
                    "sync",
                    "--root",
                    str(root),
                    "--skills",
                    str(general_source),
                    "--skills",
                    str(cpv_source),
                ]
            )

            self.assertEqual(result.exit_code, 0, result.stderr)
            self.assertTrue(
                (root / ".claude" / "skills" / "skill-authoring" / "SKILL.md").is_file()
            )
            self.assertTrue((root / ".claude" / "skills" / "cpv-ops" / "SKILL.md").is_file())
            self.assertTrue(
                (root / ".codex" / "skills" / "skill-authoring" / "SKILL.md").is_file()
            )
            self.assertTrue((root / ".codex" / "skills" / "cpv-ops" / "SKILL.md").is_file())

    def test_duplicate_source_skill_names_fail_fast(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "target"
            first_source = Path(temp_dir) / "first"
            second_source = Path(temp_dir) / "second"
            create_skill(first_source, "cpv-ops")
            create_skill(second_source, "cpv-ops")
            root.mkdir()

            result = run_cli(
                [
                    "sync",
                    "--root",
                    str(root),
                    "--skills",
                    str(first_source),
                    "--skills",
                    str(second_source),
                ]
            )

            self.assertEqual(result.exit_code, 2)
            self.assertIn("Duplicate skill name", result.stderr)

    def test_list_reports_source_and_installed_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "target"
            source = Path(temp_dir) / "source"
            create_skill(source, "cpv-ops")
            root.mkdir()

            sync_result = run_cli(["sync", "--root", str(root), "--skills", str(source)])
            self.assertEqual(sync_result.exit_code, 0, sync_result.stderr)

            list_result = run_cli(["list", "--root", str(root), "--skills", str(source)])

            self.assertEqual(list_result.exit_code, 0, list_result.stderr)
            self.assertIn("Source skills", list_result.stdout)
            self.assertIn("Claude installed skills", list_result.stdout)
            self.assertIn("Codex installed skills", list_result.stdout)

    def test_list_ignores_hidden_skill_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "target"
            source = Path(temp_dir) / "source"
            create_skill(source, "cpv-ops")
            hidden_dir = root / ".codex" / "skills" / ".system"
            hidden_dir.mkdir(parents=True)

            list_result = run_cli(["list", "--root", str(root), "--skills", str(source)])

            self.assertEqual(list_result.exit_code, 0, list_result.stderr)
            self.assertNotIn(".system", list_result.stdout)

    def test_remove_deletes_only_installed_skills_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "target"
            source = Path(temp_dir) / "source"
            create_skill(source, "cpv-ops")
            root.mkdir()

            sync_result = run_cli(["sync", "--root", str(root), "--skills", str(source)])
            self.assertEqual(sync_result.exit_code, 0, sync_result.stderr)

            remove_result = run_cli(["remove", "cpv-ops", "--root", str(root), "--skills", str(source)])

            self.assertEqual(remove_result.exit_code, 0, remove_result.stderr)
            self.assertFalse((root / ".claude" / "skills" / "cpv-ops").exists())
            self.assertFalse((root / ".codex" / "skills" / "cpv-ops").exists())
            self.assertTrue((source / "cpv-ops").is_dir())

    def test_remove_target_and_dry_run_are_guarded(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "target"
            source = Path(temp_dir) / "source"
            create_skill(source, "cpv-ops")
            root.mkdir()

            sync_result = run_cli(["sync", "--root", str(root), "--skills", str(source)])
            self.assertEqual(sync_result.exit_code, 0, sync_result.stderr)

            dry_run = run_cli(
                [
                    "delete",
                    "cpv-ops",
                    "--root",
                    str(root),
                    "--skills",
                    str(source),
                    "--target",
                    "codex",
                    "--dry-run",
                ]
            )

            self.assertEqual(dry_run.exit_code, 0, dry_run.stderr)
            self.assertIn("would remove", dry_run.stdout)
            self.assertTrue((root / ".codex" / "skills" / "cpv-ops").is_dir())
            self.assertTrue((root / ".claude" / "skills" / "cpv-ops").is_dir())

    def test_from_source_requires_explicit_flag(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "target"
            source = Path(temp_dir) / "source"
            create_skill(source, "cpv-ops")
            root.mkdir()

            result = run_cli(
                [
                    "delete",
                    "cpv-ops",
                    "--root",
                    str(root),
                    "--skills",
                    str(source),
                    "--from-source",
                ]
            )

            self.assertEqual(result.exit_code, 0, result.stderr)
            self.assertFalse((source / "cpv-ops").exists())

    def test_invalid_skill_name_fails_fast(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            result = run_cli(["remove", "../bad", "--root", str(root)])

            self.assertEqual(result.exit_code, 2)
            self.assertIn("Invalid skill name", result.stderr)


def create_skill(source: Path, name: str) -> None:
    skill_dir = source / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        f"""---
name: {name}
description: "Test skill"
---

# {name}
""",
        encoding="utf-8",
    )


def run_cli(arguments: list[str]) -> "CliResult":
    stdout = io.StringIO()
    stderr = io.StringIO()
    exit_code = run(arguments, stdout, stderr)
    return CliResult(exit_code=exit_code, stdout=stdout.getvalue(), stderr=stderr.getvalue())


class CliResult:
    def __init__(self, exit_code: int, stdout: str, stderr: str) -> None:
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr


if __name__ == "__main__":
    unittest.main()

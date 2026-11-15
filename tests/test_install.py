"""Installer flags, archive URLs, symlink safety, and manifest uninstall."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import install  # noqa: E402


class InstallTests(unittest.TestCase):
    def test_flags_can_precede_the_target_and_empty_argv_is_not_sys_argv(self) -> None:
        parsed = install.parse_args(["--agent", "all", "--mcp", "/tmp/premium-taste-target"])
        self.assertEqual(parsed.agent, "all")
        self.assertTrue(parsed.mcp)
        self.assertEqual(parsed.target, Path("/tmp/premium-taste-target"))
        self.assertEqual(install.parse_args([]).target, Path("."))

        sentinel = Path("/tmp/premium-taste-should-not-install")
        old = sys.argv
        sys.argv = ["install.py", str(sentinel), "--agent", "all"]
        try:
            code = install.main([])
        finally:
            sys.argv = old
        self.assertEqual(code, 1)
        self.assertFalse(sentinel.exists())

    def test_archive_url_covers_branch_tag_and_sha(self) -> None:
        repo = "https://github.com/02-OS/premium-taste.git"
        for ref in ("master", "v1.2.3", "abc1234", "0123456789abcdef"):
            url = install.archive_url(repo, ref)
            self.assertEqual(url, f"https://github.com/02-OS/premium-taste/archive/{ref}.tar.gz")
            self.assertNotIn("refs/heads", url)
        script = (ROOT / "install.sh").read_text(encoding="utf-8")
        self.assertIn("archive/${REF}.tar.gz", script)
        self.assertNotIn("refs/heads", script)
        self.assertIn('TARGET="."', script)
        self.assertIn("checkout --quiet", script)

    def test_target_inside_the_repo_is_rejected(self) -> None:
        self.assertEqual(install.main([str(ROOT / "site"), "--dry-run", "--agent", "none"]), 1)

    def test_symlink_destination_is_not_removed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            link = target / ".premium-taste"
            link.symlink_to(target / "missing-dest")
            with self.assertRaises(install.InstallError):
                install.copy_core(target, dry_run=False)
            self.assertTrue(link.is_symlink())
            self.assertFalse(link.exists())

    def test_failed_replace_restores_the_previous_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            dest = target / ".premium-taste"
            dest.mkdir()
            marker = dest / "keep.txt"
            marker.write_text("kept", encoding="utf-8")
            real = os.replace
            calls = {"n": 0}

            def flaky(src, dst):
                calls["n"] += 1
                if calls["n"] == 2:
                    raise OSError("rename failed")
                return real(src, dst)

            with mock.patch("install.os.replace", side_effect=flaky):
                with self.assertRaises(OSError):
                    install.copy_core(target, dry_run=False)
            self.assertEqual(marker.read_text(encoding="utf-8"), "kept")
            self.assertFalse((target / ".premium-taste.staging").exists())

    def test_null_mcp_servers_becomes_an_object(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            mcp_file = target / ".mcp.json"
            mcp_file.write_text('{"mcpServers": null}\n', encoding="utf-8")
            install.update_mcp_json(target, dry_run=False)
            loaded = json.loads(mcp_file.read_text(encoding="utf-8"))
            self.assertIsInstance(loaded["mcpServers"], dict)
            self.assertIn("premium-taste", loaded["mcpServers"])
            mcp_file.write_text('{"mcpServers": ["premium-taste"]}\n', encoding="utf-8")
            install.update_mcp_json(target, dry_run=False)
            loaded = json.loads(mcp_file.read_text(encoding="utf-8"))
            self.assertIsInstance(loaded["mcpServers"], dict)

    def test_uninstall_removes_only_manifest_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(install.main([str(target), "--agent", "none", "--no-agents-md"]), 0)
            extra = target / "notes.txt"
            extra.write_text("leave me", encoding="utf-8")
            manifest = json.loads((target / ".premium-taste" / ".install-manifest.json").read_text(encoding="utf-8"))
            self.assertIn("skills/critique-ui/SKILL.md", " ".join(manifest["files"]))
            self.assertEqual(install.main([str(target), "--uninstall"]), 0)
            self.assertTrue(extra.is_file())
            self.assertFalse((target / ".premium-taste" / "AGENTS.md").exists())

    def test_pages_workflow_verifies_pull_requests_and_deploys_on_push(self) -> None:
        text = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
        self.assertIn("pull_request:", text)
        self.assertIn("github.event_name == 'push'", text)
        self.assertIn("python3 -m unittest discover -s tests -v", text)
        deploy = text.split("deploy:", 1)[1]
        self.assertIn("github.event_name == 'push'", deploy)
        self.assertNotIn("pull_request", deploy)


if __name__ == "__main__":
    unittest.main()

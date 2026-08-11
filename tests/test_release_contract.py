import tempfile
import unittest
from pathlib import Path

from scripts.verify_release import REQUIRED_ROOT_FILES, scan_repository


class ReleaseContractTests(unittest.TestCase):
    def make_root(self, base: Path) -> Path:
        root = base / "repo"
        root.mkdir()
        for name in REQUIRED_ROOT_FILES:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("public release contract\n", encoding="utf-8")
        return root

    def test_clean_minimal_tree_passes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = self.make_root(Path(temp_dir))
            (root / "README.md").write_text("safe public material\n", encoding="utf-8")
            self.assertEqual([], scan_repository(root))

    def test_missing_legal_files_are_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            violations = scan_repository(root)
            self.assertTrue(any("missing required file: LICENSE" in item for item in violations))
            self.assertTrue(any("missing required file: NOTICE" in item for item in violations))

    def test_forbidden_artifacts_and_directories_are_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = self.make_root(Path(temp_dir))
            (root / "paper.pdf").write_bytes(b"%PDF synthetic")
            run_dir = root / "runs" / "private"
            run_dir.mkdir(parents=True)
            (run_dir / "record.json").write_text("{}", encoding="utf-8")
            violations = scan_repository(root)
            joined = "\n".join(violations)
            self.assertIn("forbidden extension", joined)
            self.assertIn("forbidden directory", joined)

    def test_browser_automation_and_secret_assignments_are_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = self.make_root(Path(temp_dir))
            (root / "unsafe.py").write_text(
                "Storage.get" + "Cookies()\n"
                "Browser.set" + "DownloadBehavior()\n"
                "api_" + "token = 'not-a-real-secret'\n",
                encoding="utf-8",
            )
            violations = "\n".join(scan_repository(root))
            self.assertIn("browser-session automation", violations)
            self.assertIn("download automation", violations)
            self.assertIn("secret-like assignment", violations)

    def test_private_machine_paths_are_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = self.make_root(Path(temp_dir))
            (root / "private.md").write_text(
                "Local source was under " + "E:\\cnki-writing-skill" + ".\n",
                encoding="utf-8",
            )
            violations = scan_repository(root)
            self.assertTrue(any("developer-machine absolute path" in item for item in violations))

    def test_internal_and_temporary_directories_are_skipped(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = self.make_root(Path(temp_dir))
            for directory in (".git", ".tmp", ".codex"):
                path = root / directory
                path.mkdir()
                (path / "private.pdf").write_bytes(b"ignored")
            self.assertEqual([], scan_repository(root))

    def test_non_utf8_public_text_is_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = self.make_root(Path(temp_dir))
            (root / "broken.md").write_bytes(b"\xff\xfe")
            violations = scan_repository(root)
            self.assertTrue(any("not strict UTF-8" in item for item in violations))


if __name__ == "__main__":
    unittest.main()

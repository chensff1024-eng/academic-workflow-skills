import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGER_PATH = ROOT / "scripts" / "package_skills.py"


def load_packager():
    spec = importlib.util.spec_from_file_location("package_skills", PACKAGER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class PackagingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packager = load_packager()

    def test_readme_cross_links_series_and_rights_boundary(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("cnki-literature-review", readme)
        self.assertIn("world-history-submission-strategy", readme)
        self.assertIn("unofficial", readme.casefold())
        self.assertIn("does not automate", readme.casefold())

    def test_skill_contracts_have_frontmatter_and_evals(self):
        for name in self.packager.SKILL_NAMES:
            skill_root = ROOT / "skills" / name
            contract = (skill_root / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(contract.startswith("---\nname: "))
            self.assertIn("\ndescription: ", contract)
            self.assertTrue((skill_root / "evals" / "evals.json").is_file())

    def test_package_inventory_and_hash_are_deterministic(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir)
            first = self.packager.package_skills(ROOT, output)
            second = self.packager.package_skills(ROOT, output)
            self.assertEqual(first, second)
            self.assertEqual(set(self.packager.SKILL_NAMES), {item["skill"] for item in first})
            for item in first:
                archive = Path(item["archive"])
                self.assertEqual(64, len(item["sha256"]))
                with zipfile.ZipFile(archive) as package:
                    names = package.namelist()
                prefix = item["skill"] + "/"
                self.assertIn(prefix + "SKILL.md", names)
                self.assertTrue(any(name.startswith(prefix + "references/") for name in names))
                self.assertTrue(any(name.startswith(prefix + "scripts/") for name in names))
                self.assertTrue(any(name.startswith(prefix + "examples/") for name in names))
                self.assertTrue(any(name.startswith(prefix + "evals/") for name in names))
                self.assertFalse(any("__pycache__" in name or name.endswith(".pyc") for name in names))

    def test_packaging_stops_when_release_verifier_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            fake_root = Path(temp_dir) / "repo"
            fake_root.mkdir()
            with self.assertRaisesRegex(ValueError, "release verification failed"):
                self.packager.package_skills(fake_root, Path(temp_dir) / "dist")

    def test_packaging_cli_runs_from_repository_root(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(PACKAGER_PATH),
                    "--output-dir",
                    temp_dir,
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertEqual(2, completed.stdout.count("PACKAGE_OK"))


if __name__ == "__main__":
    unittest.main()

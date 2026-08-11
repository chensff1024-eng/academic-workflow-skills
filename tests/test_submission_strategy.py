import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "world-history-submission-strategy"
QUERY_PATH = SKILL_ROOT / "scripts" / "query_matrix.py"
MATRIX_PATH = SKILL_ROOT / "references" / "journal-matrix.json"


def load_query_module():
    spec = importlib.util.spec_from_file_location("query_matrix", QUERY_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class SubmissionStrategyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.query = load_query_module()
        cls.matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))

    def test_matrix_has_dated_provenance_and_distinguishes_journal_forms(self):
        self.assertRegex(self.matrix["snapshot_date"], r"^20\d{2}-\d{2}-\d{2}$")
        self.assertIn("provenance_class", self.matrix)
        self.assertGreaterEqual(len(self.matrix["journals"]), 5)
        forms = {entry["journal_form"] for entry in self.matrix["journals"]}
        self.assertIn("specialist", forms)
        self.assertIn("general-history", forms)
        for entry in self.matrix["journals"]:
            self.assertTrue(entry["evidence_source"].startswith("https://"))
            self.assertEqual(self.matrix["snapshot_date"], entry["evidence_checked"])

    def test_query_ranks_theme_fit_deterministically(self):
        results = self.query.query_journals(self.matrix, ["世界史", "全球史", "跨国"])
        self.assertEqual("世界历史", results[0]["name"])
        self.assertGreater(results[0]["fit_score"], results[-1]["fit_score"])
        reversed_matrix = {**self.matrix, "journals": list(reversed(self.matrix["journals"]))}
        self.assertEqual(results, self.query.query_journals(reversed_matrix, ["世界史", "全球史", "跨国"]))

    def test_result_separates_fit_inference_from_dynamic_facts(self):
        result = self.query.query_journals(self.matrix, ["社会经济史"])[0]
        self.assertEqual("editorial-fit-inference", result["assessment_type"])
        self.assertIn("official-source", result["provenance_class"])
        self.assertIn("submission_instructions", result["unresolved_dynamic_facts"])
        self.assertIn("indexing_status", result["unresolved_dynamic_facts"])
        self.assertEqual("none", result["submission_action"])
        self.assertIn("使用时须复核", result["boundary"])

    def test_cli_outputs_strategy_without_submission_action(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "strategy.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(QUERY_PATH),
                    "--terms",
                    "英国史,港口,运输",
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertIn("SUBMISSION_STRATEGY_OK", completed.stdout)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("none", payload["submission_action"])
            self.assertGreaterEqual(len(payload["candidates"]), 5)
            self.assertIn("No login, upload, email, payment, or final submission", payload["boundary"])

    def test_runtime_source_has_no_web_or_submission_client(self):
        source = QUERY_PATH.read_text(encoding="utf-8")
        for forbidden in ("requests", "selenium", "playwright", "smtplib", "urllib.request"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()

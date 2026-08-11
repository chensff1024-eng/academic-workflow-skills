import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PIPELINE_PATH = ROOT / "skills" / "cnki-literature-review" / "scripts" / "literature_pipeline.py"


def load_pipeline():
    spec = importlib.util.spec_from_file_location("literature_pipeline", PIPELINE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class LiteraturePipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline = load_pipeline()

    def test_normalize_record_and_metadata_only_downgrade(self):
        normalized = self.pipeline.normalize_record(
            {
                "title": "  港口与腹地  ",
                "authors": "甲；乙",
                "year": "2024",
                "journal": "示例史学",
                "keywords": "港口; 腹地",
                "citations": "12",
                "abstract": "",
            }
        )
        self.assertEqual("港口与腹地", normalized["title"])
        self.assertEqual(["甲", "乙"], normalized["authors"])
        self.assertEqual(2024, normalized["year"])
        self.assertEqual(12, normalized["citations"])
        self.assertEqual("metadata-only", normalized["evidence_level"])

    def test_missing_title_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "title"):
            self.pipeline.normalize_record({"authors": "甲"})

    def test_ranking_is_deterministic_and_transparent(self):
        records = [
            {"title": "城市史研究", "keywords": ["城市"], "year": 2025, "citations": 50},
            {"title": "港口腹地关系", "keywords": ["港口", "腹地"], "year": 2022, "citations": 5},
            {"title": "港口贸易网络", "keywords": ["港口"], "year": 2024, "citations": 10},
        ]
        ranked = self.pipeline.rank_records(records, ["港口", "腹地"])
        self.assertEqual("港口腹地关系", ranked[0]["title"])
        self.assertEqual(["港口", "腹地"], ranked[0]["matched_terms"])
        self.assertGreater(ranked[0]["relevance_score"], ranked[1]["relevance_score"])
        self.assertEqual(ranked, self.pipeline.rank_records(list(reversed(records)), ["港口", "腹地"]))

    def test_review_packet_preserves_supplied_evidence_boundaries(self):
        records = [
            self.pipeline.normalize_record(
                {
                    "title": "有摘要研究",
                    "authors": ["甲"],
                    "year": 2023,
                    "abstract": "本文讨论港口与区域市场。",
                    "notes": "用户注记：比较交通条件。",
                }
            ),
            self.pipeline.normalize_record(
                {"title": "仅元数据研究", "authors": ["乙"], "year": 2022}
            ),
        ]
        packet = self.pipeline.render_review_packet(records, "港口史")
        self.assertIn("abstract-backed", packet)
        self.assertIn("metadata-only", packet)
        self.assertIn("本文讨论港口与区域市场。", packet)
        self.assertIn("不得据此推断论文观点", packet)
        self.assertNotIn("全文显示", packet)

    def test_runtime_source_has_no_network_or_browser_dependency(self):
        source = PIPELINE_PATH.read_text(encoding="utf-8")
        for forbidden in ("requests", "selenium", "playwright", "urllib.request", "import socket"):
            self.assertNotIn(forbidden, source)

    def test_cli_generates_markdown_from_synthetic_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            source = temp / "records.json"
            output = temp / "review.md"
            source.write_text(
                json.dumps(
                    [
                        {
                            "title": "近代港口运输研究",
                            "authors": ["示例作者"],
                            "year": 2024,
                            "keywords": ["港口", "运输"],
                            "abstract": "合成摘要：研究运输网络。",
                        }
                    ],
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(PIPELINE_PATH),
                    "--input",
                    str(source),
                    "--topic",
                    "近代港口史",
                    "--terms",
                    "港口,运输",
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
            self.assertIn("REVIEW_PACKET_OK", completed.stdout)
            rendered = output.read_text(encoding="utf-8")
            self.assertIn("近代港口史", rendered)
            self.assertIn("近代港口运输研究", rendered)
            self.assertIn("港口、运输", rendered)


if __name__ == "__main__":
    unittest.main()

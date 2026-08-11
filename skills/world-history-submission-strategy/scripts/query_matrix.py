#!/usr/bin/env python3
"""Query a dated local journal-fit matrix without performing submission actions."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


DYNAMIC_FACTS = [
    "submission_instructions",
    "submission_channel",
    "format_and_word_limits",
    "fees",
    "review_cycle",
    "indexing_status",
    "editorial_contacts",
    "generative_ai_policy",
]
SEPARATOR = re.compile(r"\s*[,;；、]\s*")


def _terms(values: list[str] | str) -> list[str]:
    candidates = values if isinstance(values, list) else SEPARATOR.split(values)
    result: list[str] = []
    for value in candidates:
        term = " ".join(str(value).strip().split()).casefold()
        if term and term not in result:
            result.append(term)
    return result


def validate_matrix(matrix: dict[str, Any]) -> None:
    for key in ("schema_version", "snapshot_date", "provenance_class", "journals"):
        if key not in matrix:
            raise ValueError(f"matrix missing {key}")
    if not isinstance(matrix["journals"], list) or not matrix["journals"]:
        raise ValueError("matrix journals must be a non-empty list")
    for entry in matrix["journals"]:
        for key in (
            "name",
            "journal_form",
            "scope_terms",
            "preferred_signals",
            "caution",
            "evidence_source",
            "evidence_checked",
        ):
            if key not in entry:
                raise ValueError(f"journal entry missing {key}")


def query_journals(matrix: dict[str, Any], terms: list[str]) -> list[dict[str, Any]]:
    """Return deterministic topic-fit inferences with dynamic facts unresolved."""

    validate_matrix(matrix)
    requested = _terms(terms)
    results: list[dict[str, Any]] = []
    for entry in matrix["journals"]:
        scope = _terms(entry["scope_terms"])
        signals = _terms(entry["preferred_signals"])
        matched_scope = [term for term in requested if any(term in item or item in term for item in scope)]
        matched_signals = [term for term in requested if any(term in item or item in term for item in signals)]
        score = len(matched_scope) * 10 + len(matched_signals) * 4
        fit_reasons = []
        if matched_scope:
            fit_reasons.append("主题范围匹配：" + "、".join(matched_scope))
        if matched_signals:
            fit_reasons.append("稿件信号匹配：" + "、".join(matched_signals))
        if not fit_reasons:
            fit_reasons.append("当前关键词未形成直接匹配，仅保留为相邻候选。")

        results.append(
            {
                "name": entry["name"],
                "journal_form": entry["journal_form"],
                "fit_score": score,
                "matched_terms": matched_scope + [term for term in matched_signals if term not in matched_scope],
                "fit_reasons": fit_reasons,
                "mismatch_risk": entry["caution"],
                "assessment_type": "editorial-fit-inference",
                "provenance_class": matrix["provenance_class"],
                "evidence_date": entry["evidence_checked"],
                "evidence_source": entry["evidence_source"],
                "unresolved_dynamic_facts": list(DYNAMIC_FACTS),
                "submission_action": "none",
                "boundary": "使用时须复核全部动态事实；本结果不登录、不上传、不发送、不付款、不提交。",
            }
        )

    return sorted(results, key=lambda item: (-item["fit_score"], item["name"]))


def default_matrix_path() -> Path:
    return Path(__file__).resolve().parents[1] / "references" / "journal-matrix.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terms", required=True, help="Comma-separated manuscript topic terms")
    parser.add_argument("--matrix", type=Path, default=default_matrix_path())
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    try:
        matrix = json.loads(args.matrix.read_text(encoding="utf-8"))
        candidates = query_journals(matrix, _terms(args.terms))
        payload = {
            "schema_version": "1.0",
            "matrix_snapshot_date": matrix["snapshot_date"],
            "query_terms": _terms(args.terms),
            "assessment_type": "editorial-fit-inference",
            "candidates": candidates,
            "submission_action": "none",
            "boundary": "No login, upload, email, payment, or final submission was performed.",
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"SUBMISSION_STRATEGY_FAILED {error}")
        return 1

    print(f"SUBMISSION_STRATEGY_OK candidates={len(candidates)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

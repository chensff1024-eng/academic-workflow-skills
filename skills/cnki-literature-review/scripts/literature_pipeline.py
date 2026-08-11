#!/usr/bin/env python3
"""Normalize user-supplied metadata and render a bounded review packet."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


SEPARATOR = re.compile(r"\s*[,;；、]\s*")


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def _split_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        candidates = value
    else:
        candidates = SEPARATOR.split(str(value))
    result: list[str] = []
    for candidate in candidates:
        cleaned = _clean_text(candidate)
        if cleaned and cleaned not in result:
            result.append(cleaned)
    return result


def _non_negative_int(value: Any, field: str) -> int:
    if value in (None, ""):
        return 0
    try:
        parsed = int(str(value).strip())
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field} must be an integer") from error
    if parsed < 0:
        raise ValueError(f"{field} must be non-negative")
    return parsed


def _year(value: Any) -> int | None:
    if value in (None, ""):
        return None
    parsed = _non_negative_int(value, "year")
    if parsed < 1000 or parsed > 9999:
        raise ValueError("year must be four digits")
    return parsed


def normalize_record(raw: dict[str, Any]) -> dict[str, Any]:
    """Normalize one bibliographic record without inventing missing fields."""

    if not isinstance(raw, dict):
        raise ValueError("record must be an object")
    title = _clean_text(raw.get("title"))
    if not title:
        raise ValueError("title is required")

    abstract = _clean_text(raw.get("abstract"))
    notes = _clean_text(raw.get("notes"))
    return {
        "title": title,
        "authors": _split_list(raw.get("authors") or raw.get("author")),
        "year": _year(raw.get("year")),
        "journal": _clean_text(raw.get("journal") or raw.get("source")),
        "keywords": _split_list(raw.get("keywords")),
        "abstract": abstract,
        "citations": _non_negative_int(raw.get("citations"), "citations"),
        "locator": _clean_text(raw.get("locator") or raw.get("doi")),
        "notes": notes,
        "evidence_level": "abstract-backed" if abstract or notes else "metadata-only",
    }


def rank_records(records: list[dict[str, Any]], topic_terms: list[str]) -> list[dict[str, Any]]:
    """Rank records using visible term matches and bounded tie-breakers."""

    terms = []
    for value in topic_terms:
        term = _clean_text(value).casefold()
        if term and term not in terms:
            terms.append(term)

    ranked: list[dict[str, Any]] = []
    for raw in records:
        record = normalize_record(raw)
        title = record["title"].casefold()
        keyword_text = " ".join(record["keywords"]).casefold()
        evidence_text = f"{record['abstract']} {record['notes']}".casefold()
        matched = [term for term in terms if term in f"{title} {keyword_text} {evidence_text}"]
        title_hits = sum(term in title for term in matched)
        keyword_hits = sum(term in keyword_text for term in matched)
        score = len(matched) * 10 + title_hits * 2 + keyword_hits
        record["matched_terms"] = matched
        record["relevance_score"] = score
        ranked.append(record)

    return sorted(
        ranked,
        key=lambda item: (
            -item["relevance_score"],
            -(item["year"] or 0),
            -min(item["citations"], 1000),
            item["title"].casefold(),
        ),
    )


def _cell(value: Any) -> str:
    return _clean_text(value).replace("|", "\\|") or "未提供"


def render_review_packet(records: list[dict[str, Any]], topic: str) -> str:
    """Render a Markdown ledger that keeps source evidence visibly bounded."""

    normalized = []
    for record in records:
        item = normalize_record(record)
        item["matched_terms"] = _split_list(record.get("matched_terms"))
        if "relevance_score" in record:
            item["relevance_score"] = record["relevance_score"]
        normalized.append(item)
    lines = [
        f"# 文献综述证据包：{_clean_text(topic)}",
        "",
        "> 本证据包只使用用户提供的书目信息、摘要与阅读注记；它不包含自动下载的全文。",
        "",
        "## 证据台账",
        "",
        "| 序号 | 题名 | 作者 | 年份 | 来源 | 证据等级 | 匹配词 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for index, record in enumerate(normalized, start=1):
        matches = record.get("matched_terms", [])
        lines.append(
            "| {index} | {title} | {authors} | {year} | {journal} | {level} | {matches} |".format(
                index=index,
                title=_cell(record["title"]),
                authors=_cell("、".join(record["authors"])),
                year=_cell(record["year"]),
                journal=_cell(record["journal"]),
                level=record["evidence_level"],
                matches=_cell("、".join(matches)),
            )
        )

    lines.extend(["", "## 可用证据与限制", ""])
    for index, record in enumerate(normalized, start=1):
        lines.append(f"### {index}. {record['title']}")
        lines.append("")
        lines.append(f"- 证据等级：`{record['evidence_level']}`")
        if record["abstract"]:
            lines.append(f"- 用户提供的摘要：{record['abstract']}")
        if record["notes"]:
            lines.append(f"- 用户注记：{record['notes']}")
        if record["evidence_level"] == "metadata-only":
            lines.append("- 限制：只有元数据，不得据此推断论文观点、方法、史料或结论。")
        if record["locator"]:
            lines.append(f"- 定位信息：{record['locator']}")
        lines.append("")

    lines.extend(
        [
            "## 综合写作框架",
            "",
            "1. 按研究问题或学术分歧分组，不按题名机械罗列。",
            "2. 每项实质判断回指 abstract-backed 记录或用户注记。",
            "3. 将 metadata-only 记录保留为待核材料，不把它写成学术结论。",
            "4. 单列证据冲突、研究空白与下一轮检索式。",
            "",
        ]
    )
    return "\n".join(lines)


def load_records(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        records = payload.get("records") if isinstance(payload, dict) else payload
    elif suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            records = list(csv.DictReader(handle))
    else:
        raise ValueError("input must be UTF-8 JSON or CSV")
    if not isinstance(records, list):
        raise ValueError("input must contain a list of records")
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--terms", default="")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    try:
        records = load_records(args.input)
        terms = _split_list(args.terms)
        ranked = rank_records(records, terms)
        rendered = render_review_packet(ranked, args.topic)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"REVIEW_PACKET_FAILED {error}")
        return 1

    print(f"REVIEW_PACKET_OK records={len(ranked)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Reject public-release trees that contain unsafe or private material."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_ROOT_FILES = (
    "README.md",
    "LICENSE",
    "NOTICE",
    "THIRD_PARTY_NOTICES.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
)

SKIPPED_DIRECTORIES = {".git", ".tmp", ".codex"}
FORBIDDEN_DIRECTORIES = {"runs", "dist-check", "__pycache__"}
FORBIDDEN_EXTENSIONS = {
    ".pdf",
    ".caj",
    ".doc",
    ".docx",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
}
TEXT_EXTENSIONS = {
    "",
    ".md",
    ".txt",
    ".py",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
    ".cfg",
}

RISK_ANCHORS = (
    ("browser-session automation", "Storage.get" + "Cookies"),
    ("download automation", "Browser.set" + "DownloadBehavior"),
    ("download automation", "Page.set" + "DownloadBehavior"),
)

SECRET_ASSIGNMENT = re.compile(
    r"(?im)^\s*(?:api[_-]?key|api[_-]?token|access[_-]?token|password|secret)\s*[:=]\s*['\"][^'\"\r\n]+['\"]"
)
WINDOWS_ABSOLUTE_PATH = re.compile(r"(?i)\b[A-Z]:[\\/](?:Users|Documents and Settings|cnki-writing-skill|submission-skill|academic-workflow-skills)(?:[\\/]|\b)")
UNIX_HOME_PATH = re.compile(r"(?:^|[\s'\"])/(?:home|Users)/[^\s'\"]+")
DIRECT_DOWNLOAD = re.compile(
    r"(?i)(?:requests\.(?:get|post)|urlopen|fetch)\s*\([^\n]{0,160}(?:download|\.pdf|\.caj)"
)


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _iter_public_files(root: Path):
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().lower()):
        relative_parts = path.relative_to(root).parts
        if any(part in SKIPPED_DIRECTORIES for part in relative_parts):
            continue
        if path.is_file():
            yield path


def scan_repository(root: Path) -> list[str]:
    """Return deterministic release violations for *root*."""

    root = root.resolve()
    violations: list[str] = []

    for name in REQUIRED_ROOT_FILES:
        if not (root / name).is_file():
            violations.append(f"missing required file: {name}")

    for path in _iter_public_files(root):
        relative = _relative(path, root)
        relative_parts = path.relative_to(root).parts

        forbidden_part = next(
            (part for part in relative_parts[:-1] if part in FORBIDDEN_DIRECTORIES),
            None,
        )
        if forbidden_part:
            violations.append(f"{relative}: forbidden directory: {forbidden_part}")

        if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
            violations.append(f"{relative}: forbidden extension: {path.suffix.lower()}")

        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="strict")
        except UnicodeDecodeError:
            violations.append(f"{relative}: not strict UTF-8")
            continue

        if text.startswith("\ufeff"):
            violations.append(f"{relative}: UTF-8 BOM is not allowed")

        for label, anchor in RISK_ANCHORS:
            if anchor in text:
                violations.append(f"{relative}: {label}")
        if SECRET_ASSIGNMENT.search(text):
            violations.append(f"{relative}: secret-like assignment")
        if WINDOWS_ABSOLUTE_PATH.search(text) or UNIX_HOME_PATH.search(text):
            violations.append(f"{relative}: developer-machine absolute path")
        if DIRECT_DOWNLOAD.search(text):
            violations.append(f"{relative}: direct document-download code")

    return sorted(set(violations))


def count_public_files(root: Path) -> int:
    return sum(1 for _ in _iter_public_files(root.resolve()))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    violations = scan_repository(args.root)
    if violations:
        for violation in violations:
            print(f"RELEASE_VIOLATION {violation}")
        print(f"RELEASE_VERIFY_FAILED violations={len(violations)}")
        return 1

    print(f"RELEASE_VERIFY_OK scanned_files={count_public_files(args.root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

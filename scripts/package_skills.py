#!/usr/bin/env python3
"""Create deterministic, independently installable Skill archives."""

from __future__ import annotations

import argparse
import hashlib
import zipfile
from pathlib import Path

try:
    from scripts.verify_release import scan_repository
except ModuleNotFoundError:
    from verify_release import scan_repository


SKILL_NAMES = ("cnki-literature-review", "world-history-submission-strategy")
LEGAL_FILES = ("LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md")
EXCLUDED_PARTS = {"__pycache__", ".tmp", ".git", ".codex"}
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def _skill_files(skill_root: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in skill_root.rglob("*")
            if path.is_file()
            and not any(part in EXCLUDED_PARTS for part in path.relative_to(skill_root).parts)
            and path.suffix.lower() != ".pyc"
        ),
        key=lambda path: path.relative_to(skill_root).as_posix(),
    )


def _write_member(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    info = zipfile.ZipInfo(name, FIXED_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package_skills(root: Path, output_dir: Path) -> list[dict[str, str]]:
    """Verify *root* and build one deterministic archive per Skill."""

    root = root.resolve()
    violations = scan_repository(root)
    if violations:
        raise ValueError("release verification failed: " + "; ".join(violations))

    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, str]] = []
    for skill_name in SKILL_NAMES:
        skill_root = root / "skills" / skill_name
        if not (skill_root / "SKILL.md").is_file():
            raise ValueError(f"missing Skill contract: {skill_name}/SKILL.md")
        archive_path = output_dir / f"{skill_name}.zip"
        with zipfile.ZipFile(archive_path, "w") as archive:
            for path in _skill_files(skill_root):
                member = f"{skill_name}/{path.relative_to(skill_root).as_posix()}"
                _write_member(archive, member, path.read_bytes())
            for legal_name in LEGAL_FILES:
                _write_member(archive, f"{skill_name}/{legal_name}", (root / legal_name).read_bytes())
        results.append(
            {
                "skill": skill_name,
                "archive": str(archive_path),
                "sha256": _sha256(archive_path),
            }
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, default=Path(".tmp/dist"))
    args = parser.parse_args()

    try:
        results = package_skills(args.root, args.output_dir)
    except (OSError, ValueError) as error:
        print(f"PACKAGE_FAILED {error}")
        return 1

    for result in results:
        print(
            f"PACKAGE_OK skill={result['skill']} archive={result['archive']} "
            f"sha256={result['sha256']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

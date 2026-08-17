#!/usr/bin/env python3
"""Build a sealed local G134 review intake from REVIEW_MANIFEST.tsv."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANIFEST = HERE / "REVIEW_MANIFEST.tsv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    with MANIFEST.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        source = ROOT / row["path"]
        actual = sha256(source)
        if actual != row["sha256"]:
            raise SystemExit(f"hash mismatch: {row['path']} {actual} != {row['sha256']}")

    intake = Path(tempfile.mkdtemp(prefix="udt_g134_area_review_", dir="/tmp"))
    for row in rows:
        source = ROOT / row["path"]
        target = intake / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    manifest_target = intake / "REVIEW_MANIFEST.tsv"
    shutil.copy2(MANIFEST, manifest_target)
    scope = {
        "review": "G134 full-metric area history reframe",
        "manifest_listed_payload_files": len(rows),
        "file_count_including_manifest": len(rows) + 1,
        "total_intake_files_including_scope": len(rows) + 2,
        "manifest_sha256": sha256(MANIFEST),
        "restrictions": [
            "read-only",
            "no repository access outside intake",
            "no edits",
            "no continued research",
            "no protected packages",
            "no internet required",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(intake)
    print(f"manifest_sha256={scope['manifest_sha256']}")
    print(f"payload_files={len(rows)} intake_files={scope['total_intake_files_including_scope']}")


if __name__ == "__main__":
    main()

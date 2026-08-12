#!/usr/bin/env python3
"""Build a sealed read-only review intake from the exact package and source manifest."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_one(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_pair_first_review_", dir="/tmp"))
    package_dst = intake / HERE.name
    package_dst.mkdir()

    copied = []
    for src in sorted(HERE.iterdir()):
        if src.is_file() and src.name != "build_review_intake.py":
            dst = package_dst / src.name
            copy_one(src, dst)
            copied.append({"path": str(dst.relative_to(intake)), "sha256": sha(dst), "kind": "package"})

    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8") as f:
        source_rows = list(csv.DictReader(f, delimiter="\t"))
    for row in source_rows:
        src = ROOT / row["path"]
        if sha(src) != row["sha256"]:
            raise SystemExit(f"source hash mismatch: {row['path']}")
        dst = intake / "sources" / row["path"]
        copy_one(src, dst)
        copied.append({"path": str(dst.relative_to(intake)), "sha256": sha(dst), "kind": "source"})

    request = package_dst / "ADVERSARIAL_REVIEW_REQUEST.md"
    (intake / "REVIEW_SCOPE.json").write_text(
        json.dumps({"schema": "udt-pair-first-sealed-review-v1", "files": copied}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    copied.append({"path": "REVIEW_SCOPE.json", "sha256": sha(intake / "REVIEW_SCOPE.json"), "kind": "scope"})

    # Files are immutable to the review process. Directories remain traversable.
    for path in intake.rglob("*"):
        if path.is_file():
            os.chmod(path, 0o444)
        elif path.is_dir():
            os.chmod(path, 0o555)
    os.chmod(intake, 0o555)

    print(str(intake))
    print(str(request.relative_to(intake)))
    print(len(copied))


if __name__ == "__main__":
    main()

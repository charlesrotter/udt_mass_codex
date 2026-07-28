#!/usr/bin/env python3
"""Freeze exact source blobs from the preregistered base."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "73833fa4e75152e51d24f8056b6856dd835785f7"
TREE = "f6bc54423c4ce5426e48a4c5ae82c6ba7e555202"


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main() -> None:
    if git("rev-parse", f"{BASE}^{{tree}}").decode().strip() != TREE:
        raise SystemExit("base tree mismatch")
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    rows = []
    for source in sources:
        path = source["path"]
        payload = git("show", f"{BASE}:{path}")
        rows.append({
            "path": path,
            "git_blob": git("rev-parse", f"{BASE}:{path}").decode().strip(),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "bytes": str(len(payload)),
            "role": source["role"],
        })
    with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    print(f"sources={len(rows)}")


if __name__ == "__main__":
    main()

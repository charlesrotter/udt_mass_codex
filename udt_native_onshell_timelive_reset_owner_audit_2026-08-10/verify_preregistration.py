#!/usr/bin/env python3
"""Fail closed if the G57 preregistration or frozen source universe changes."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    snap = json.loads((HERE / "PREREG_SNAPSHOT.json").read_text(encoding="utf-8"))
    assert snap["candidate_count"] == 36
    assert snap["axis_count"] == 8
    assert snap["falsification_count"] == 15
    for name, expected in snap["files"].items():
        assert sha(HERE / name) == expected, name
    assert sha(HERE / "SOURCE_MANIFEST.tsv") == snap["source_manifest_sha256"]
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 36
    assert len({row["candidate_id"] for row in rows}) == 36
    for row in rows:
        path = ROOT / row["path"]
        assert path.is_file(), row["path"]
        assert sha(path) == row["sha256"], row["path"]
        blob = subprocess.check_output(["git", "rev-parse", row["source_ref"]], cwd=ROOT, text=True).strip()
        assert blob == row["git_blob"], row["path"]
    print("PASS: preregistration immutable; 36 exact candidate sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Replay every initial/refined source from its immutable Git reference."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def load(name: str):
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    initial = load("SOURCE_MANIFEST.tsv")
    refinement = load("SOURCE_MANIFEST_REFINEMENT.tsv")
    combined = load("SOURCE_MANIFEST_CONSOLIDATED.tsv")
    assert len(initial) == 44
    assert len(refinement) == 28
    assert len(combined) == len({row["path"] for row in combined}) == 72
    assert {row["path"] for row in combined} == {row["path"] for row in initial + refinement}
    assert not any("kernel_plane_global_curvature" in row["path"] for row in combined)
    for row in combined:
        data = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        assert hashlib.sha256(data).hexdigest() == row["sha256"], row["path"]
        assert len(data) == int(row["size"]), row["path"]
        blob = subprocess.check_output(["git", "rev-parse", row["source_ref"]], cwd=ROOT, text=True).strip()
        assert blob == row["git_blob"], row["path"]
    print("PASS: 72/72 immutable source refs; protected atlas absent")


if __name__ == "__main__":
    main()

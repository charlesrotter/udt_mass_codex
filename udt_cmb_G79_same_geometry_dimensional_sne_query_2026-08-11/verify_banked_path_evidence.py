#!/usr/bin/env python3
"""Fail closed unless the sealed G79 path field is tracked byte-identically."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RELATIVE = f"{HERE.name}/PATH_EVIDENCE.npz"
EXPECTED = "3f61f35f57b06f4407a7c9b98a75e37c929a6ce71fe180f7fe93d2e3ba765cd7"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", RELATIVE],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert tracked.returncode == 0 and tracked.stdout.strip() == RELATIVE
    path = HERE / "PATH_EVIDENCE.npz"
    assert path.stat().st_size == 120575
    assert digest(path) == EXPECTED
    with (HERE / "REVIEW_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    row = next(item for item in rows if item["path"] == RELATIVE)
    assert row["sha256"] == EXPECTED and row["role"] == "G79_package"
    print("PASS: G79 PATH_EVIDENCE.npz is tracked and byte-identical to the sealed review row")


if __name__ == "__main__":
    main()

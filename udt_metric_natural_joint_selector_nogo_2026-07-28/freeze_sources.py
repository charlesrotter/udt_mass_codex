#!/usr/bin/env python3
"""Freeze the preregistered source paths from the exact base commit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "e7ea5936eaecbab626db0f30e12a8be4630b5dd7"
TREE = "cad25e08302b9e6ed3809b1774d0d82af1848a2a"


def git(*args: str, binary: bool = False):
    result = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=not binary, check=False)
    if result.returncode:
        error = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise RuntimeError(error)
    return result.stdout


def main() -> None:
    if git("rev-parse", f"{BASE}^{{tree}}").strip() != TREE:
        raise AssertionError("F01 base tree mismatch")
    paths = [line for line in (HERE / "SOURCE_PATHS.txt").read_text().splitlines() if line]
    if len(paths) != 13 or len(paths) != len(set(paths)):
        raise AssertionError("source path census mismatch")
    rows = []
    for index, path in enumerate(paths, 1):
        blob = git("rev-parse", f"{BASE}:{path}").strip()
        content = git("cat-file", "blob", blob, binary=True)
        rows.append({
            "source_id": f"S{index:02d}", "path": path, "git_blob": blob,
            "size_bytes": len(content), "sha256": hashlib.sha256(content).hexdigest(),
            "read_from": "FIXED_GIT_BASE_BLOB",
        })
    with (HERE / "SOURCE_MANIFEST.tsv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    print(f"sources_frozen={len(rows)} base={BASE} tree={TREE}")


if __name__ == "__main__":
    main()

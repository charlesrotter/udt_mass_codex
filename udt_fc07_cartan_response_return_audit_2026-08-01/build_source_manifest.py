#!/usr/bin/env python3
"""Freeze the preregistered FC07 Cartan/response source scope at HEAD."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "45ebc7ee6ab5f216198835eaef4cfcb498e1147d"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=True
    ).stdout.strip()


def main() -> int:
    head = BASE
    assert git("merge-base", "--is-ancestor", head, "HEAD") == ""
    rows = []
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = row["path"]
            entry = git("ls-tree", head, "--", path).split()
            assert len(entry) >= 3 and entry[1] == "blob", path
            blob = entry[2]
            payload = subprocess.run(
                ["git", "show", f"{head}:{path}"], cwd=ROOT, capture_output=True, check=True
            ).stdout
            assert hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest() == blob
            rows.append(
                {
                    "path": path,
                    "role": row["role"],
                    "base_commit": head,
                    "git_blob": blob,
                    "sha256": hashlib.sha256(payload).hexdigest(),
                    "bytes": str(len(payload)),
                }
            )
    target = HERE / "SOURCE_MANIFEST.tsv"
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"PASS source freeze base={head} files={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

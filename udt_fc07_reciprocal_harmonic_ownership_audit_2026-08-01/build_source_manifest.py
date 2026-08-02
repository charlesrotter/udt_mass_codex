#!/usr/bin/env python3
"""Freeze the preregistered FC07 harmonic-ownership source scope."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "37df6a1"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=True
    ).stdout.strip()


def main() -> int:
    base = git("rev-parse", BASE)
    assert git("merge-base", "--is-ancestor", base, "HEAD") == ""
    rows: list[dict[str, str]] = []
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = row["path"]
            entry = git("ls-tree", base, "--", path).split()
            assert len(entry) >= 3 and entry[1] == "blob", path
            blob = entry[2]
            payload = subprocess.run(
                ["git", "show", f"{base}:{path}"],
                cwd=ROOT,
                capture_output=True,
                check=True,
            ).stdout
            framed = b"blob " + str(len(payload)).encode() + b"\0" + payload
            assert hashlib.sha1(framed).hexdigest() == blob
            rows.append(
                {
                    "path": path,
                    "role": row["role"],
                    "base_commit": base,
                    "git_blob": blob,
                    "sha256": hashlib.sha256(payload).hexdigest(),
                    "bytes": str(len(payload)),
                }
            )
    target = HERE / "SOURCE_MANIFEST.tsv"
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"PASS source freeze base={base} files={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

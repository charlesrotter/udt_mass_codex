#!/usr/bin/env python3
"""Freeze load-bearing sources from the preregistration commit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "3e3eecc"


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main() -> None:
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        scope = list(csv.DictReader(handle, delimiter="\t"))
    rows: list[dict[str, object]] = []
    identities: list[str] = []
    for item in scope:
        path = item["path"]
        data = git("show", f"{BASE}:{path}")
        blob = git("rev-parse", f"{BASE}:{path}").decode().strip()
        sha = hashlib.sha256(data).hexdigest()
        if blob != item["git_blob"] or sha != item["sha256"]:
            raise AssertionError(f"source scope mismatch: {path}")
        row = {"path": path, "role": item["role"], "blob": blob, "sha256": sha, "bytes": len(data)}
        rows.append(row)
        identities.append(f"{path}\t{blob}\t{sha}\t{len(data)}")
    with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    identity_sha = hashlib.sha256(("\n".join(identities) + "\n").encode()).hexdigest()
    print(f"base={BASE}")
    print(f"sources={len(rows)}")
    print(f"identity_sha256={identity_sha}")


if __name__ == "__main__":
    main()


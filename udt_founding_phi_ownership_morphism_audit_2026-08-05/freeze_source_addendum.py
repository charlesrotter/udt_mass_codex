#!/usr/bin/env python3
"""Freeze the preregistered four-file direct-founding source addendum."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()


def main() -> None:
    paths = [
        line.strip()
        for line in (HERE / "SOURCE_ADDENDUM_PATHS.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(paths) != 4 or len(paths) != len(set(paths)):
        raise SystemExit("addendum must contain exactly four unique paths")
    rows = []
    for relative in paths:
        target = ROOT / relative
        if not target.is_file():
            raise SystemExit(f"missing addendum source: {relative}")
        data = target.read_bytes()
        rows.append(
            {
                "path": relative,
                "git_blob": git("hash-object", "--", relative),
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
                "last_commit": git("log", "-1", "--format=%H", "--", relative),
            }
        )
    manifest = HERE / "SOURCE_ADDENDUM_MANIFEST.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["path", "git_blob", "sha256", "bytes", "last_commit"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    result = {
        "schema": "udt.founding_phi_ownership.source_addendum.v1",
        "base_source_count": 31,
        "addendum_source_count": 4,
        "effective_source_count": 35,
        "correction_commit_parent": git("rev-parse", "HEAD"),
        "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
    }
    (HERE / "SOURCE_ADDENDUM_FREEZE.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

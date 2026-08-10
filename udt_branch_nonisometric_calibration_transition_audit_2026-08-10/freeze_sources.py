#!/usr/bin/env python3
"""Freeze the exact preregistered source scope at the source-freeze commit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT = HERE / "SOURCE_MANIFEST.tsv"


def main() -> None:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(rows) == len({row["path"] for row in rows}) == 44

    rendered = []
    for row in rows:
        path = row["path"]
        data = subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)
        rendered.append(
            {
                "source_id": row["source_id"],
                "path": path,
                "source_ref": f"{commit}:{path}",
                "git_blob": subprocess.check_output(
                    ["git", "rev-parse", f"{commit}:{path}"], cwd=ROOT, text=True
                ).strip(),
                "sha256": hashlib.sha256(data).hexdigest(),
                "size": str(len(data)),
                "role": row["role"],
            }
        )

    with OUTPUT.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=rendered[0].keys(), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rendered)
    print(f"PASS: froze {len(rendered)} sources at {commit}")


if __name__ == "__main__":
    main()

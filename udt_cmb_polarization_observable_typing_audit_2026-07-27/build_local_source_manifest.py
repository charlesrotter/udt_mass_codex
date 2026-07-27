#!/usr/bin/env python3
"""Freeze the preregistered local source paths by Git blob and SHA-256."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def blob(path: Path) -> str:
    result = subprocess.run(
        ["git", "hash-object", str(path)], cwd=ROOT, check=True, text=True,
        stdout=subprocess.PIPE,
    )
    return result.stdout.strip()


def main() -> int:
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        sources = [row for row in csv.DictReader(handle, delimiter="\t") if row["source_type"] == "LOCAL"]
    assert len(sources) == 10
    fields = ("source_id", "path", "git_blob", "sha256")
    writer = csv.DictWriter(__import__("sys").stdout, delimiter="\t", fieldnames=fields)
    writer.writeheader()
    for row in sources:
        path = ROOT / row["path_or_query"]
        assert path.is_file()
        writer.writerow({
            "source_id": row["source_id"], "path": row["path_or_query"],
            "git_blob": blob(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

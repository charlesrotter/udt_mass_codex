#!/usr/bin/env python3
"""Build frozen Git-blob and SHA-256 identities for the source scope."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> None:
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    fields = ["source_id", "path", "role", "git_blob", "sha256", "size_bytes"]
    with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            path = ROOT / row["path"]
            data = path.read_bytes()
            blob = subprocess.run(
                ["git", "rev-parse", f"HEAD:{row['path']}"], cwd=ROOT,
                check=True, text=True, capture_output=True,
            ).stdout.strip()
            writer.writerow({
                **row,
                "git_blob": blob,
                "sha256": hashlib.sha256(data).hexdigest(),
                "size_bytes": len(data),
            })


if __name__ == "__main__":
    main()

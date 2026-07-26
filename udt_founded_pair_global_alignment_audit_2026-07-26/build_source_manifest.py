#!/usr/bin/env python3
"""Build exact identities for every registered source."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> None:
    output: list[dict[str, str]] = []
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = ROOT / row["path"]
            if not path.is_file():
                raise AssertionError(f"missing source: {row['path']}")
            blob = subprocess.run(
                ["git", "hash-object", row["path"]],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            ).stdout.strip()
            output.append(
                {
                    "path": row["path"],
                    "registered_use": row["registered_use"],
                    "git_blob": blob,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "bytes": str(path.stat().st_size),
                }
            )
    with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["path", "registered_use", "git_blob", "sha256", "bytes"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(output)


if __name__ == "__main__":
    main()


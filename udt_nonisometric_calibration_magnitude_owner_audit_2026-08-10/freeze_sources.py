#!/usr/bin/env python3
"""Freeze exact committed inputs for the preregistered magnitude-owner audit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> None:
    base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    output = []
    for row in rows:
        source_ref = f"{base}:{row['path']}"
        data = subprocess.check_output(["git", "show", source_ref], cwd=ROOT)
        blob = subprocess.check_output(["git", "rev-parse", source_ref], cwd=ROOT, text=True).strip()
        output.append(
            {
                **row,
                "source_ref": source_ref,
                "git_blob": blob,
                "sha256": hashlib.sha256(data).hexdigest(),
                "size": len(data),
            }
        )
    fields = ["source_id", "path", "source_ref", "git_blob", "sha256", "size", "role"]
    with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)
    print(f"PASS: frozen_sources={len(output)} base={base}")


if __name__ == "__main__":
    main()

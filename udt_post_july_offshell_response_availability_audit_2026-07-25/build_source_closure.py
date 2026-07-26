#!/usr/bin/env python3
"""Build a deterministic hash census for the primary evidence cited by each family."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    with (PKG / "CANDIDATE_RESPONSE_GATE_MATRIX.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    output = PKG / "FAMILY_SOURCE_CLOSURE.tsv"
    fields = ["candidate_id", "source_path", "citation", "git_blob", "sha256", "tracked"]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            citation = row["load_bearing_evidence"]
            source_path = citation.split(":", 1)[0]
            source = ROOT / source_path
            blob = subprocess.run(
                ["git", "rev-parse", f"HEAD:{source_path}"], cwd=ROOT,
                check=True, text=True, capture_output=True,
            ).stdout.strip()
            writer.writerow({
                "candidate_id": row["candidate_id"],
                "source_path": source_path,
                "citation": citation,
                "git_blob": blob,
                "sha256": sha256(source),
                "tracked": "YES",
            })


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Freeze SHA-256 hashes of the tracked G293 source spine."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--scope", type=Path, default=Path(__file__).resolve().parent / "SOURCE_SCOPE.tsv")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "SOURCE_MANIFEST.tsv")
    args = parser.parse_args()

    rows = []
    with args.scope.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            source = row["source"]
            if source.startswith("https://"):
                rows.append({"source": source, "sha256": "EXTERNAL_REFERENCE", "bytes": "NA"})
                continue
            path = args.repo / source
            if not path.is_file():
                raise FileNotFoundError(path)
            rows.append({"source": source, "sha256": sha256(path), "bytes": str(path.stat().st_size)})

    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "sha256", "bytes"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"frozen_sources={len(rows)}")


if __name__ == "__main__":
    main()

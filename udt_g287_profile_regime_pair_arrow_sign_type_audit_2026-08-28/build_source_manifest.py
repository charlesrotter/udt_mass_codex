#!/usr/bin/env python3
"""Build the exact G287 source manifest from the frozen source-scope table."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=PACKAGE / "SOURCE_MANIFEST.tsv")
    args = parser.parse_args()
    with (PACKAGE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    lines = ["path\tbytes\tsha256"]
    for row in rows:
        path = ROOT / row["path"]
        payload = path.read_bytes()
        lines.append(f"{row['path']}\t{len(payload)}\t{hashlib.sha256(payload).hexdigest()}")
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {len(rows)} source rows to {args.output}")


if __name__ == "__main__":
    main()

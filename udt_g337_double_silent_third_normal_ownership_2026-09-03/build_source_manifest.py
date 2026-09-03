#!/usr/bin/env python3
"""Build the frozen G337 source manifest from the preregistration commit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "96135e03"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "SOURCE_MANIFEST.tsv")
    args = parser.parse_args()
    rows = list(csv.DictReader(
        (HERE / "SOURCE_SCOPE.tsv").open(encoding="utf-8"), delimiter="\t"
    ))
    output = ["source_id\tpath\tbytes\tsha256"]
    for row in rows:
        relative = Path(row["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise AssertionError(f"unsafe source path: {relative}")
        result = subprocess.run(
            ["git", "show", f"{PREREG_COMMIT}:{relative.as_posix()}"],
            cwd=ROOT, capture_output=True, check=False,
        )
        if result.returncode:
            raise AssertionError(f"source absent at preregistration: {relative}")
        payload = result.stdout
        output.append(
            f"{row['source_id']}\t{relative.as_posix()}\t{len(payload)}\t"
            f"{hashlib.sha256(payload).hexdigest()}"
        )
    args.output.write_text("\n".join(output) + "\n", encoding="utf-8")
    print(f"G337 source manifest: {len(rows)} frozen sources at {PREREG_COMMIT}")


if __name__ == "__main__":
    main()

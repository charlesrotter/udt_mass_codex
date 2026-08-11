#!/usr/bin/env python3
"""Build the current post-review package manifest without self-reference."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "POSTREVIEW_MANIFEST.tsv"
EXCLUDE = {OUT.name, "POSTREVIEW_VERIFICATION_RESULT.json"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    paths = sorted(
        (path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDE),
        key=lambda path: str(path.relative_to(ROOT)),
    )
    with OUT.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256"))
        writer.writerows((str(path.relative_to(ROOT)), digest(path)) for path in paths)
    print(f"postreview_manifest_rows={len(paths)}")


if __name__ == "__main__":
    main()

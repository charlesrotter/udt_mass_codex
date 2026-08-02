#!/usr/bin/env python3
"""Build source and final package SHA-256 manifests."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
EXCLUDE = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-only", action="store_true")
    args = parser.parse_args()
    source = PACKAGE / "SOURCE_MANIFEST.tsv"
    (PACKAGE / "SOURCE_MANIFEST.sha256").write_text(
        f"{digest(source)}  SOURCE_MANIFEST.tsv\n", encoding="utf-8"
    )
    if args.source_only:
        print("PASS source manifest hash")
        return 0
    paths = sorted(path for path in PACKAGE.iterdir() if path.is_file() and path.name not in EXCLUDE)
    (PACKAGE / "PACKAGE_MANIFEST.sha256").write_text(
        "\n".join(f"{digest(path)}  {path.name}" for path in paths) + "\n", encoding="utf-8"
    )
    print(f"PASS package manifest files={len(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

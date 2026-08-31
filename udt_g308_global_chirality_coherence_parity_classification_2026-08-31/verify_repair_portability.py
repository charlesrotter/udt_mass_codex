#!/usr/bin/env python3
"""Verify G308 source resolution in repository and sealed layouts."""

from __future__ import annotations

import csv
import json
import tempfile
from pathlib import Path

import verify_package as package


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "PORTABILITY_VERIFICATION_RESULT.json"


def write_dummy(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("g308-portability\n", encoding="utf-8")


def rejects(root: Path, relative: Path) -> bool:
    try:
        package.resolve_source(root, relative)
    except AssertionError:
        return True
    return False


def main() -> None:
    relative = Path("source_package") / "evidence.txt"
    with tempfile.TemporaryDirectory(prefix="g308_portability_") as temporary:
        base = Path(temporary)

        repository_root = base / "repository"
        repository_path = repository_root / relative
        write_dummy(repository_path)
        repository_layout_verified = package.resolve_source(repository_root, relative) == repository_path

        sealed_root = base / "sealed"
        sealed_path = sealed_root / "frozen_sources" / relative
        write_dummy(sealed_path)
        sealed_layout_verified = package.resolve_source(sealed_root, relative) == sealed_path

        missing_root = base / "missing"
        missing_layout_rejected = rejects(missing_root, relative)

        ambiguous_root = base / "ambiguous"
        write_dummy(ambiguous_root / relative)
        write_dummy(ambiguous_root / "frozen_sources" / relative)
        ambiguous_layout_rejected = rejects(ambiguous_root, relative)

    source_rows = 0
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            relative_source = Path(row["path"])
            resolved = package.resolve_source(ROOT, relative_source)
            assert package.digest(resolved) == row["sha256"], relative_source
            source_rows += 1

    assert source_rows == 9
    assert repository_layout_verified
    assert sealed_layout_verified
    assert missing_layout_rejected
    assert ambiguous_layout_rejected
    result = {
        "status": "PASS",
        "source_rows_verified": source_rows,
        "repository_layout_verified": repository_layout_verified,
        "sealed_layout_verified": sealed_layout_verified,
        "missing_layout_rejected": missing_layout_rejected,
        "ambiguous_layout_rejected": ambiguous_layout_rejected,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Verify frozen sources in either repository or sealed-intake layout."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    package = args.package.resolve()
    container = package.parent
    repo_root = container
    sealed_root = container / "sources"

    with (package / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(rows) == 10
    assert len({row["path"] for row in rows}) == 10

    if all((sealed_root / row["path"]).is_file() for row in rows):
        source_root = sealed_root
        layout = "sealed"
    elif all((repo_root / row["path"]).is_file() for row in rows):
        source_root = repo_root
        layout = "repository"
    else:
        raise AssertionError("neither repository nor sealed source layout is complete")

    for row in rows:
        path = source_root / row["path"]
        assert digest(path) == row["sha256"], row["path"]
        assert "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" not in row["path"]
        assert "udt_native_onshell_timelive_reset_owner_audit_2026-08-10" not in row["path"]
    print(f"PASS layout={layout} sources={len(rows)}")


if __name__ == "__main__":
    main()

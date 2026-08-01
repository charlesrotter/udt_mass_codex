#!/usr/bin/env python3
"""Freeze the additions-only source universe for the premise audit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
PARENT = ROOT / "udt_whole_configuration_reciprocity_audit_2026-08-01"
BASE = "9d17940c5ab490b281b7818b46918ed378c96bf1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"{BASE}:{path}"], cwd=ROOT, text=True
    ).strip()


def main() -> None:
    with (PARENT / "SOURCE_INVENTORY.tsv").open(newline="", encoding="utf-8") as handle:
        parent_rows = list(csv.DictReader(handle, delimiter="\t"))
    parent_paths = {row["path"] for row in parent_rows}
    if len(parent_paths) != 1384:
        raise RuntimeError(f"expected 1384 parent sources, got {len(parent_paths)}")

    prefix = "udt_whole_configuration_reciprocity_audit_2026-08-01/"
    tracked = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASE], cwd=ROOT, text=True
    ).splitlines()
    package_paths = sorted(path for path in tracked if path.startswith(prefix))
    if len(package_paths) != 40:
        raise RuntimeError(f"expected 40 complete parent-package paths, got {len(package_paths)}")

    paths = sorted(parent_paths | set(package_paths))
    if len(paths) != 1424:
        raise RuntimeError(f"expected 1424-path union, got {len(paths)}")

    rows = []
    for path in paths:
        file_path = ROOT / path
        if not file_path.is_file():
            raise RuntimeError(f"missing source: {path}")
        layer = "PARENT_1384_SOURCE_UNIVERSE" if path in parent_paths else "WHOLE_RECIPROCITY_PARENT_PACKAGE"
        rows.append(
            {
                "path": path,
                "git_blob": git_blob(path),
                "sha256": sha256(file_path),
                "bytes": file_path.stat().st_size,
                "layer": layer,
            }
        )

    with (PKG / "SOURCE_INVENTORY.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["path", "git_blob", "sha256", "bytes", "layer"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    (PKG / "SOURCE_PATHS.txt").write_text("\n".join(paths) + "\n", encoding="utf-8")
    (PKG / "SOURCE_MANIFEST.sha256").write_text(
        "\n".join(f'{row["sha256"]}  {row["path"]}' for row in rows) + "\n",
        encoding="utf-8",
    )
    with (PKG / "SOURCE_PACKAGE_SCOPE.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["layer", "paths", "rule"], delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(
            [
                {"layer": "PARENT_1384_SOURCE_UNIVERSE", "paths": 1384, "rule": "exact parent frozen inventory"},
                {"layer": "WHOLE_RECIPROCITY_PARENT_PACKAGE", "paths": 40, "rule": "complete tracked package at base"},
                {"layer": "UNION", "paths": 1424, "rule": "sorted unique additions-only union"},
            ]
        )
    print("PASS premise-audit preregistration build: sources=1424 parent=1384 package=40")


if __name__ == "__main__":
    main()

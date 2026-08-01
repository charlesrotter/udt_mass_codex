#!/usr/bin/env python3
"""Freeze the additions-only source universe for the cross-family atlas."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
PARENT = ROOT / "udt_global_local_self_consistency_premise_audit_2026-08-01"
PARENT_PACKAGE = "udt_global_local_self_consistency_premise_audit_2026-08-01"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob(path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"HEAD:{path}"], cwd=ROOT, text=True).strip()


def main() -> None:
    with (PARENT / "SOURCE_INVENTORY.tsv").open(newline="", encoding="utf-8") as handle:
        inherited = list(csv.DictReader(handle, delimiter="\t"))
    if len(inherited) != 1424:
        raise RuntimeError("parent source count changed")

    parent_paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", "HEAD", PARENT_PACKAGE], cwd=ROOT, text=True
    ).splitlines()
    if len(parent_paths) != 42:
        raise RuntimeError(f"parent package count changed: {len(parent_paths)}")

    layers = {row["path"]: "PARENT_PREMISE_AUDIT_SOURCE_UNIVERSE" for row in inherited}
    if set(parent_paths) & set(layers):
        raise RuntimeError("unexpected source-layer overlap")
    layers.update({path: "GLOBAL_LOCAL_PREMISE_PARENT_PACKAGE" for path in parent_paths})
    if len(layers) != 1466:
        raise RuntimeError("union count changed")

    rows = []
    for rel in sorted(layers):
        path = ROOT / rel
        if not path.is_file():
            raise RuntimeError(f"missing source: {rel}")
        rows.append({
            "path": rel,
            "git_blob": blob(rel),
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
            "layer": layers[rel],
        })

    with (PKG / "SOURCE_INVENTORY.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (PKG / "SOURCE_PATHS.txt").write_text("\n".join(row["path"] for row in rows) + "\n", encoding="utf-8")
    (PKG / "SOURCE_MANIFEST.sha256").write_text(
        "\n".join(f"{row['sha256']}  ../{row['path']}" for row in rows) + "\n", encoding="utf-8"
    )
    print(f"PASS preregistration build: sources={len(rows)} parent={len(inherited)} package={len(parent_paths)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Freeze the exact preregistered source universe."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent
BASE = "9fe5202e86627aa47a5200ea776dcb468a6531f6"
PARENT = "udt_bootstrap_closure_ownership_audit_2026-08-01"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tree() -> dict[str, tuple[str, int]]:
    out = subprocess.check_output(["git", "ls-tree", "-rl", BASE], cwd=ROOT, text=True)
    result = {}
    for line in out.splitlines():
        meta, path = line.split("\t", 1)
        _mode, kind, blob, size = meta.split()
        if kind == "blob":
            result[path] = (blob, int(size))
    return result


def main() -> None:
    base_tree = tree()
    paths = set((ROOT / PARENT / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines())
    parent_source_count = len(paths)
    parent_package = {p for p in base_tree if p.startswith(PARENT + "/")}
    paths.update(parent_package)

    with (PKG / "SOURCE_PACKAGE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        scopes = list(csv.DictReader(handle, delimiter="\t"))
    package_counts = {}
    for row in scopes:
        prefix = row["package_path"].rstrip("/") + "/"
        found = {p for p in base_tree if p.startswith(prefix)}
        if not found:
            raise RuntimeError(f"empty package scope: {row['package_path']}")
        package_counts[row["scope_id"]] = len(found)
        paths.update(found)

    direct_files = [p for p in (PKG / "SOURCE_FILE_SCOPE.txt").read_text(encoding="utf-8").splitlines() if p]
    for path in direct_files:
        if path not in base_tree:
            raise RuntimeError(f"missing direct source: {path}")
        paths.add(path)

    sorted_paths = sorted(paths)
    inventory = []
    for path in sorted_paths:
        blob, size = base_tree[path]
        data = subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)
        if len(data) != size:
            raise RuntimeError(f"size mismatch: {path}")
        inventory.append({"path": path, "sha256": sha256(data), "bytes": size, "blob": blob, "base": BASE})

    with (PKG / "SOURCE_INVENTORY.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(inventory[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(inventory)
    (PKG / "SOURCE_PATHS.txt").write_text("".join(f"{p}\n" for p in sorted_paths), encoding="utf-8")
    (PKG / "SOURCE_MANIFEST.sha256").write_text(
        "".join(f"{row['sha256']}  ../{row['path']}\n" for row in inventory), encoding="utf-8"
    )
    snapshot = {
        "base": BASE,
        "parent_source_paths": parent_source_count,
        "parent_package_paths": len(parent_package),
        "package_scopes": len(scopes),
        "package_counts": package_counts,
        "direct_files": len(direct_files),
        "source_union": len(sorted_paths),
        "premises": 15,
        "interpretations": 10,
    }
    (PKG / "PREREG_SNAPSHOT.json").write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"PASS prereg build: parent={parent_source_count} parent_package={len(parent_package)} "
        f"packages={len(scopes)} direct={len(direct_files)} union={len(sorted_paths)}"
    )


if __name__ == "__main__":
    main()


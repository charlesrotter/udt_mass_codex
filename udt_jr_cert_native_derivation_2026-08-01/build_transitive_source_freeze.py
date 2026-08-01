#!/usr/bin/env python3
"""Build the append-only transitive evidence freeze at the exact preregistered base."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "686336343878e8a9e39a4b72df08d23754243631"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tracked_under(directory: str) -> list[str]:
    output = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASE, "--", directory],
        cwd=ROOT,
        text=True,
    )
    return [line for line in output.splitlines() if line]


def git_blob(path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{BASE}:{path}"], cwd=ROOT, text=True).strip()


with (HERE / "TRANSITIVE_PACKAGE_SCOPE.tsv").open(encoding="utf-8", newline="") as handle:
    packages = list(csv.DictReader(handle, delimiter="\t"))

original = {
    line.strip()
    for line in (HERE / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
if len(original) != 172:
    raise SystemExit(f"original freeze changed: expected 172, got {len(original)}")

package_counts: dict[str, int] = {}
all_transitive: set[str] = set()
for row in packages:
    directory = row["package_path"]
    paths = tracked_under(directory)
    if not paths:
        raise SystemExit(f"empty or missing package at base: {directory}")
    package_counts[directory] = len(paths)
    all_transitive.update(paths)

additions = sorted(all_transitive - original)
overlap = sorted(all_transitive & original)
inventory = []
for rel in additions:
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f"working-tree path missing: {rel}")
    inventory.append(
        {"path": rel, "sha256": digest(path), "bytes": path.stat().st_size, "blob": git_blob(rel), "base": BASE}
    )

(HERE / "TRANSITIVE_SOURCE_PATHS.txt").write_text(
    "".join(f"{row['path']}\n" for row in inventory), encoding="utf-8"
)
with (HERE / "TRANSITIVE_SOURCE_INVENTORY.tsv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=["path", "sha256", "bytes", "blob", "base"],
        delimiter="\t",
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(inventory)
(HERE / "TRANSITIVE_SOURCE_MANIFEST.sha256").write_text(
    "".join(f"{row['sha256']}  ../{row['path']}\n" for row in inventory), encoding="utf-8"
)

combined = sorted(original | set(additions))
(HERE / "COMBINED_SOURCE_PATHS.txt").write_text("".join(f"{path}\n" for path in combined), encoding="utf-8")
snapshot = {
    "base": BASE,
    "package_count": len(packages),
    "package_file_counts": package_counts,
    "scoped_package_union": len(all_transitive),
    "overlap_with_original_count": len(overlap),
    "overlap_with_original_paths": overlap,
    "transitive_additions": len(additions),
    "original_sources": len(original),
    "combined_sources": len(combined),
    "package_scope_sha256": digest(HERE / "TRANSITIVE_PACKAGE_SCOPE.tsv"),
    "transitive_paths_sha256": digest(HERE / "TRANSITIVE_SOURCE_PATHS.txt"),
    "transitive_inventory_sha256": digest(HERE / "TRANSITIVE_SOURCE_INVENTORY.tsv"),
    "transitive_manifest_sha256": digest(HERE / "TRANSITIVE_SOURCE_MANIFEST.sha256"),
    "combined_paths_sha256": digest(HERE / "COMBINED_SOURCE_PATHS.txt"),
}
(HERE / "TRANSITIVE_FREEZE_SNAPSHOT.json").write_text(
    json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(
    "PASS transitive freeze: "
    f"packages={len(packages)} package_union={len(all_transitive)} "
    f"overlap={len(overlap)} additions={len(additions)} combined={len(combined)}"
)

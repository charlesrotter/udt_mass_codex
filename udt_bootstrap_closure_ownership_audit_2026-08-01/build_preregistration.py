#!/usr/bin/env python3
"""Build the exact preregistered source freeze without inspecting semantic outcomes."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "df2b35fcb6fc709e1ad0639b9f46222d64ee99cd"
PARENT = "udt_jr_cert_native_derivation_2026-08-01"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tracked_under(path: str) -> list[str]:
    output = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASE, "--", path], cwd=ROOT, text=True
    )
    return [line for line in output.splitlines() if line]


def blob(path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{BASE}:{path}"], cwd=ROOT, text=True).strip()


parent_sources = {
    line for line in (ROOT / PARENT / "COMBINED_SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines() if line
}
if len(parent_sources) != 586:
    raise SystemExit(f"unexpected parent source count {len(parent_sources)}")
parent_package = set(tracked_under(PARENT))

with (HERE / "SOURCE_PACKAGE_SCOPE.tsv").open(encoding="utf-8", newline="") as handle:
    packages = list(csv.DictReader(handle, delimiter="\t"))
if len(packages) != 17:
    raise SystemExit(f"unexpected package scope {len(packages)}")

package_paths: set[str] = set()
package_counts: dict[str, int] = {}
for row in packages:
    paths = tracked_under(row["package_path"])
    if not paths:
        raise SystemExit(f"empty package {row['package_path']}")
    package_counts[row["package_path"]] = len(paths)
    package_paths.update(paths)

paths = sorted(parent_sources | parent_package | package_paths)
inventory = []
for rel in paths:
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f"missing working path {rel}")
    inventory.append(
        {"path": rel, "sha256": digest(path), "bytes": path.stat().st_size, "blob": blob(rel), "base": BASE}
    )

(HERE / "SOURCE_PATHS.txt").write_text("".join(f"{row['path']}\n" for row in inventory), encoding="utf-8")
with (HERE / "SOURCE_INVENTORY.tsv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(
        handle, fieldnames=["path", "sha256", "bytes", "blob", "base"], delimiter="\t", lineterminator="\n"
    )
    writer.writeheader()
    writer.writerows(inventory)
(HERE / "SOURCE_MANIFEST.sha256").write_text(
    "".join(f"{row['sha256']}  ../{row['path']}\n" for row in inventory), encoding="utf-8"
)

def row_count(name: str, key: str) -> int:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return sum(1 for row in csv.DictReader(handle, delimiter="\t") if row.get(key))


snapshot = {
    "base": BASE,
    "parent_sources": len(parent_sources),
    "parent_package_files": len(parent_package),
    "scoped_packages": len(packages),
    "scoped_package_file_union": len(package_paths),
    "package_file_counts": package_counts,
    "source_union": len(paths),
    "premise_rows": row_count("PREMISE_LEDGER.tsv", "premise_id"),
    "output_candidates": row_count("OUTPUT_CANDIDATES.tsv", "candidate_id"),
    "return_candidates": row_count("RETURN_CANDIDATES.tsv", "candidate_id"),
    "source_paths_sha256": digest(HERE / "SOURCE_PATHS.txt"),
    "source_inventory_sha256": digest(HERE / "SOURCE_INVENTORY.tsv"),
    "source_manifest_sha256": digest(HERE / "SOURCE_MANIFEST.sha256"),
    "package_scope_sha256": digest(HERE / "SOURCE_PACKAGE_SCOPE.tsv"),
}
(HERE / "PREREG_SNAPSHOT.json").write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(
    "PASS prereg build: "
    f"parent={len(parent_sources)} parent_package={len(parent_package)} "
    f"packages={len(packages)} union={len(paths)} outputs={snapshot['output_candidates']} "
    f"returns={snapshot['return_candidates']}"
)

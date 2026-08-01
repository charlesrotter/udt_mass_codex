#!/usr/bin/env python3
"""Build the exact 140-path preregistration freeze from the reviewed parent audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_stability_foundations_audit_2026-08-01"
BASE = "089e2044be1b2e801f9b4f07e83efb5296dc1375"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob(path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{BASE}:{path}"], cwd=ROOT, text=True).strip()


direct = [line.strip() for line in (PARENT / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
package_names = [line.split("  ", 1)[1] for line in (PARENT / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines() if line.strip()]
package = [f"udt_stability_foundations_audit_2026-08-01/{name}" for name in package_names]
package.append("udt_stability_foundations_audit_2026-08-01/PACKAGE_MANIFEST.sha256")
with (PARENT / "TRANSITIVE_PREMISE_FREEZE.tsv").open(encoding="utf-8", newline="") as handle:
    transitive = [row["path"] for row in csv.DictReader(handle, delimiter="\t")]

paths = sorted(set(direct + package + transitive))
if len(direct) != 94 or len(package) != 42 or len(transitive) != 4 or len(paths) != 140:
    raise SystemExit(f"unexpected census direct={len(direct)} package={len(package)} transitive={len(transitive)} union={len(paths)}")

inventory = []
for rel in paths:
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f"missing {rel}")
    inventory.append({"path": rel, "sha256": digest(path), "bytes": path.stat().st_size, "blob": git_blob(rel), "base": BASE})

(HERE / "SOURCE_PATHS.txt").write_text("".join(f"{row['path']}\n" for row in inventory), encoding="utf-8")
with (HERE / "SOURCE_INVENTORY.tsv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=["path", "sha256", "bytes", "blob", "base"], delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(inventory)
(HERE / "SOURCE_MANIFEST.sha256").write_text("".join(f"{row['sha256']}  ../{row['path']}\n" for row in inventory), encoding="utf-8")

premise_rows = sum(1 for _ in (HERE / "PREMISE_LEDGER.tsv").open(encoding="utf-8")) - 1
route_rows = sum(1 for _ in (HERE / "ROUTE_CANDIDATES.tsv").open(encoding="utf-8")) - 1
snapshot = {
    "base": BASE,
    "direct_parent_sources": len(direct),
    "parent_package_files": len(package),
    "transitive_parent_sources": len(transitive),
    "source_union": len(paths),
    "premise_rows": premise_rows,
    "route_rows": route_rows,
    "source_paths_sha256": digest(HERE / "SOURCE_PATHS.txt"),
    "source_inventory_sha256": digest(HERE / "SOURCE_INVENTORY.tsv"),
    "source_manifest_sha256": digest(HERE / "SOURCE_MANIFEST.sha256"),
}
(HERE / "PREREG_SNAPSHOT.json").write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"PASS prereg build: sources={len(paths)} premises={premise_rows} routes={route_rows}")

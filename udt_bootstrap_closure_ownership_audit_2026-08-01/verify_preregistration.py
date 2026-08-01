#!/usr/bin/env python3
"""Read-only fail-closed verification of the closure-ownership preregistration."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "df2b35fcb6fc709e1ad0639b9f46222d64ee99cd"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


sources = read_tsv("SOURCE_INVENTORY.tsv")
premises = read_tsv("PREMISE_LEDGER.tsv")
outputs = read_tsv("OUTPUT_CANDIDATES.tsv")
returns = read_tsv("RETURN_CANDIDATES.tsv")
packages = read_tsv("SOURCE_PACKAGE_SCOPE.tsv")
snapshot = json.loads((HERE / "PREREG_SNAPSHOT.json").read_text(encoding="utf-8"))

assert len(sources) == len({row["path"] for row in sources}) == snapshot["source_union"]
assert [row["premise_id"] for row in premises] == [f"BCO-P{i:02d}" for i in range(1, 19)]
assert [row["candidate_id"] for row in outputs] == [f"O{i:02d}" for i in range(1, 12)]
assert [row["candidate_id"] for row in returns] == [f"R{i:02d}" for i in range(1, 9)]
assert len(packages) == 17
assert all(row["base"] == BASE for row in sources)
assert all(
    (ROOT / row["path"]).is_file()
    and digest(ROOT / row["path"]) == row["sha256"]
    and (ROOT / row["path"]).stat().st_size == int(row["bytes"])
    and subprocess.check_output(["git", "rev-parse", f"{BASE}:{row['path']}"], cwd=ROOT, text=True).strip()
    == row["blob"]
    for row in sources
)
assert snapshot["base"] == BASE and snapshot["parent_sources"] == 586
assert snapshot["premise_rows"] == 18 and snapshot["output_candidates"] == 11
assert snapshot["return_candidates"] == 8 and snapshot["scoped_packages"] == 17
assert snapshot["source_paths_sha256"] == digest(HERE / "SOURCE_PATHS.txt")
assert snapshot["source_inventory_sha256"] == digest(HERE / "SOURCE_INVENTORY.tsv")
assert snapshot["source_manifest_sha256"] == digest(HERE / "SOURCE_MANIFEST.sha256")
assert snapshot["package_scope_sha256"] == digest(HERE / "SOURCE_PACKAGE_SCOPE.tsv")
assert "No outcome authorizes" in (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
print(
    "PASS closure-ownership preregistration: "
    f"sources={len(sources)} premises={len(premises)} outputs={len(outputs)} returns={len(returns)}"
)

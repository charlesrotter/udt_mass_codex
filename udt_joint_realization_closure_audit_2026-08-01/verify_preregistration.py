#!/usr/bin/env python3
"""Read-only verification of the frozen joint-realization preregistration."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "089e2044be1b2e801f9b4f07e83efb5296dc1375"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


with (HERE / "SOURCE_INVENTORY.tsv").open(encoding="utf-8", newline="") as handle:
    sources = list(csv.DictReader(handle, delimiter="\t"))
with (HERE / "PREMISE_LEDGER.tsv").open(encoding="utf-8", newline="") as handle:
    premises = list(csv.DictReader(handle, delimiter="\t"))
with (HERE / "ROUTE_CANDIDATES.tsv").open(encoding="utf-8", newline="") as handle:
    routes = list(csv.DictReader(handle, delimiter="\t"))
snapshot = json.loads((HERE / "PREREG_SNAPSHOT.json").read_text(encoding="utf-8"))

assert len(sources) == len({row["path"] for row in sources}) == 140
assert len(premises) == 17 and [row["premise_id"] for row in premises] == [f"JR-P{i:02d}" for i in range(1, 18)]
assert len(routes) == 8 and [row["route_id"] for row in routes] == [f"J{i:02d}" for i in range(1, 9)]
assert all(row["base"] == BASE for row in sources)
assert all((ROOT / row["path"]).is_file() and digest(ROOT / row["path"]) == row["sha256"] and (ROOT / row["path"]).stat().st_size == int(row["bytes"]) for row in sources)
assert snapshot["base"] == BASE and snapshot["source_union"] == 140 and snapshot["premise_rows"] == 17 and snapshot["route_rows"] == 8
assert snapshot["source_paths_sha256"] == digest(HERE / "SOURCE_PATHS.txt")
assert snapshot["source_inventory_sha256"] == digest(HERE / "SOURCE_INVENTORY.tsv")
assert snapshot["source_manifest_sha256"] == digest(HERE / "SOURCE_MANIFEST.sha256")
print("PASS preregistration: 140 sources; 17 premises; 8 routes; base=" + BASE)

#!/usr/bin/env python3
"""Read-only fail-closed verifier for the JR_CERT_NATIVE preregistration."""

from __future__ import annotations

import csv
import hashlib
import json
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


with (HERE / "SOURCE_INVENTORY.tsv").open(encoding="utf-8", newline="") as handle:
    sources = list(csv.DictReader(handle, delimiter="\t"))
with (HERE / "PREMISE_LEDGER.tsv").open(encoding="utf-8", newline="") as handle:
    premises = [row for row in csv.DictReader(handle, delimiter="\t") if row.get("premise_id")]
with (HERE / "ROUTE_CANDIDATES.tsv").open(encoding="utf-8", newline="") as handle:
    routes = [row for row in csv.DictReader(handle, delimiter="\t") if row.get("route_id")]
snapshot = json.loads((HERE / "PREREG_SNAPSHOT.json").read_text(encoding="utf-8"))

assert len(sources) == len({row["path"] for row in sources}) == 172
assert len(premises) == 20 and [row["premise_id"] for row in premises] == [f"JRC-P{i:02d}" for i in range(1, 21)]
assert len(routes) == 14
assert [row["route_id"] for row in routes] == [f"E{i:02d}" for i in range(1, 9)] + [f"B{i:02d}" for i in range(1, 7)]
assert all(row["base"] == BASE for row in sources)
assert all((ROOT / row["path"]).is_file() and digest(ROOT / row["path"]) == row["sha256"] and (ROOT / row["path"]).stat().st_size == int(row["bytes"]) for row in sources)
assert snapshot["base"] == BASE and snapshot["source_union"] == 172 and snapshot["premise_rows"] == 20 and snapshot["route_rows"] == 14
assert snapshot["source_paths_sha256"] == digest(HERE / "SOURCE_PATHS.txt")
assert snapshot["source_inventory_sha256"] == digest(HERE / "SOURCE_INVENTORY.tsv")
assert snapshot["source_manifest_sha256"] == digest(HERE / "SOURCE_MANIFEST.sha256")
assert "Stage 3" in (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
print("PASS preregistration: 172 sources; 20 premises; 14 routes; base=" + BASE)

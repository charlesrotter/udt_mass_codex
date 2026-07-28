#!/usr/bin/env python3
"""Generate the exact preregistered P02 Cartesian stratum universe."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    contract = json.loads((ROOT / "SAMPLING_CONTRACT.json").read_text())
    order = contract["axis_order"]
    axes = contract["axes"]
    rows = []
    for index, values in enumerate(itertools.product(*(axes[name] for name in order))):
        row = {"stratum_id": f"P02S{index:05d}"}
        row.update(dict(zip(order, values)))
        rows.append(row)
    if len(rows) != contract["strata"] or len({row["stratum_id"] for row in rows}) != len(rows):
        raise AssertionError("stratum universe count or identity failure")
    output = ROOT / "STRATUM_UNIVERSE.tsv"
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["stratum_id", *order], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    result = {
        "schema": "udt-full-local-jet-strata-p02-universe-1.0",
        "strata": len(rows),
        "attempts": len(rows) * contract["replicates_per_stratum"],
        "stratum_tsv_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "first_id": rows[0]["stratum_id"],
        "last_id": rows[-1]["stratum_id"],
    }
    (ROOT / "STRATUM_UNIVERSE_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

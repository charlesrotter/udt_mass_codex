#!/usr/bin/env python3
"""Independent replay of the random-only R3 block atlas."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import healpy as hp
import numpy as np

import run_r1_ingestion_nulls as r1


ROOT = Path(__file__).resolve().parent


def main() -> int:
    result = json.loads((ROOT / "R3_BLOCK_RESULT.json").read_text())
    atlas_path = ROOT / "R3_BLOCK_ATLAS.tsv"
    assert hashlib.sha256(atlas_path.read_bytes()).hexdigest() == result["atlas_sha256"]
    with atlas_path.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    actual = defaultdict(list)
    for row in rows:
        actual[(row["sample"], row["cap"], int(row["nside"]))].append(
            (int(row["nested_pixel"]), int(row["full_random_rows"]))
        )
    entries = [entry for entry in r1.read_manifest() if entry.kind == "random"]
    for entry in entries:
        data = r1.read_numeric_columns(entry.path, ["RA", "DEC", "Z"], entry.rows)
        valid = r1.assign_shells(data["Z"], entry.sample) >= 0
        theta = np.pi / 2.0 - np.deg2rad(data["DEC"][valid])
        phi = np.mod(np.deg2rad(data["RA"][valid]), 2.0 * np.pi)
        for nside in (4, 8, 16):
            assigned = hp.ang2pix(nside, theta, phi, nest=True)
            unique, counts = np.unique(assigned, return_counts=True)
            expected = list(zip(unique.tolist(), counts.tolist()))
            assert actual[(entry.sample, entry.cap, nside)] == expected
    assert len(rows) == result["atlas_rows"]
    assert result["galaxy_catalog_read"] is False and result["r2_curve_or_descriptor_read"] is False
    print(f"PASS: independently replayed {len(rows)} random-only block rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

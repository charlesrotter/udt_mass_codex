#!/usr/bin/env python3
"""Build the fixed R3 spatial block atlas from official random catalogs only."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import healpy as hp
import numpy as np

import run_r1_ingestion_nulls as r1


ROOT = Path(__file__).resolve().parent
ATLAS = ROOT / "R3_BLOCK_ATLAS.tsv"
RESULT = ROOT / "R3_BLOCK_RESULT.json"
NSIDES = (4, 8, 16)


def pixels(ra, dec, nside):
    return hp.ang2pix(
        nside,
        np.deg2rad(90.0 - np.asarray(dec, dtype=np.float64)),
        np.deg2rad(np.mod(np.asarray(ra, dtype=np.float64), 360.0)),
        nest=True,
    )


def main() -> int:
    if ATLAS.exists() or RESULT.exists():
        raise FileExistsError("R3 block outputs already exist")
    entries = [entry for entry in r1.read_manifest() if entry.kind == "random"]
    rows = []
    summaries = []
    for entry in entries:
        data = r1.read_numeric_columns(entry.path, ["RA", "DEC", "Z"], entry.rows)
        valid = r1.assign_shells(data["Z"], entry.sample) >= 0
        assert np.all(np.isfinite(data["RA"][valid])) and np.all(np.isfinite(data["DEC"][valid]))
        assert np.all((data["DEC"][valid] >= -90.0) & (data["DEC"][valid] <= 90.0))
        selected = int(np.count_nonzero(valid))
        for nside in NSIDES:
            pix = pixels(data["RA"][valid], data["DEC"][valid], nside)
            unique, counts = np.unique(pix, return_counts=True)
            assert np.sum(counts) == selected and np.all(counts > 0)
            total = float(selected)
            for order, (pixel, count) in enumerate(zip(unique, counts)):
                rows.append({
                    "sample": entry.sample,
                    "cap": entry.cap,
                    "nside": nside,
                    "block_order": order,
                    "nested_pixel": int(pixel),
                    "full_random_rows": int(count),
                    "full_random_fraction": float(count / total),
                    "source_sha256": entry.sha256,
                })
            summaries.append({
                "sample": entry.sample,
                "cap": entry.cap,
                "nside": nside,
                "source_rows": entry.rows,
                "envelope_rows": selected,
                "occupied_blocks": int(len(unique)),
                "count_min": int(np.min(counts)),
                "count_median": float(np.median(counts)),
                "count_max": int(np.max(counts)),
                "count_cv": float(np.std(counts) / np.mean(counts)),
            })

    fields = (
        "sample", "cap", "nside", "block_order", "nested_pixel", "full_random_rows",
        "full_random_fraction", "source_sha256",
    )
    with ATLAS.open("x", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    result = {
        "status": "OBSERVED__RANDOM_ONLY_BLOCK_GEOMETRY_FROZEN",
        "healpy": hp.__version__,
        "nest": True,
        "nsides": list(NSIDES),
        "atlas_rows": len(rows),
        "atlas_sha256": hashlib.sha256(ATLAS.read_bytes()).hexdigest(),
        "summaries": summaries,
        "galaxy_catalog_read": False,
        "r2_curve_or_descriptor_read": False,
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"PASS: froze {len(rows)} random-only R3 block rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

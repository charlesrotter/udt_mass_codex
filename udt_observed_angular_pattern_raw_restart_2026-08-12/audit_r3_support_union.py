#!/usr/bin/env python3
"""Outcome-free census of R3 selected-data versus selected-random block support."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import run_r1_ingestion_nulls as r1
import run_r2_central_pattern as r2
import run_r3_covariance_atlas as r3


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "R3_SUPPORT_CENSUS_RESULT.json"


def main() -> int:
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    entries = r1.read_manifest()
    data_entries = {(e.sample, e.cap): e for e in entries if e.kind == "data"}
    random_entries = {(e.sample, e.cap): e for e in entries if e.kind == "random"}
    blocks = r3.load_block_pixels()
    rows = []
    for sample in ("CMASS", "LOWZ"):
        for cap in ("North", "South"):
            de, re = data_entries[(sample, cap)], random_entries[(sample, cap)]
            data = r1.read_numeric_columns(de.path, ["RA", "DEC", "Z"], de.rows)
            random = r1.read_numeric_columns(re.path, ["RA", "DEC", "Z"], re.rows)
            data_sid = r1.assign_shells(data["Z"], sample)
            random_sid = r1.assign_shells(random["Z"], sample)
            hashes = r1.splitmix64(np.arange(re.rows, dtype=np.uint64), int(re.sha256[:16], 16))
            fine_pixels, fine_to_parent = r3.parent_maps(sample, cap, blocks)
            for group in r2.groups(sample):
                lo, hi = int(group["members"][0]), int(group["members"][-1])
                di = np.flatnonzero((data_sid >= lo) & (data_sid <= hi))
                candidates = np.flatnonzero((random_sid >= lo) & (random_sid <= hi))
                need = r3.RATIO * len(di)
                local = np.argpartition(hashes[candidates], need - 1)[:need]
                local = local[np.lexsort((candidates[local], hashes[candidates][local]))]
                ri = candidates[local]
                dp = r3.patch_labels(data["RA"][di], data["DEC"][di], fine_pixels)
                rp = r3.patch_labels(random["RA"][ri], random["DEC"][ri], fine_pixels)
                for nside in r3.NSIDES:
                    size = len(blocks[(sample, cap, nside)])
                    dparent = fine_to_parent[nside][dp]
                    rparent = fine_to_parent[nside][rp]
                    nd = np.bincount(dparent, minlength=size)
                    nr = np.bincount(rparent, minlength=size)
                    missing = (nd > 0) & (nr == 0)
                    rows.append({
                        "sample": sample,
                        "cap": cap,
                        "factor": int(group["factor"]),
                        "group": int(group["group"]),
                        "nside": nside,
                        "data_only_blocks": int(np.count_nonzero(missing)),
                        "data_in_data_only_blocks": int(np.sum(nd[missing])),
                        "union_active_blocks": int(np.count_nonzero((nd > 0) | (nr > 0))),
                        "random_active_blocks": int(np.count_nonzero(nr > 0)),
                    })
    affected = [row for row in rows if row["data_only_blocks"]]
    by_nside = {}
    for nside in r3.NSIDES:
        subset = [row for row in rows if row["nside"] == nside]
        hit = [row for row in subset if row["data_only_blocks"]]
        by_nside[str(nside)] = {
            "selection_count": len(subset),
            "affected_selection_count": len(hit),
            "total_data_only_blocks": sum(row["data_only_blocks"] for row in hit),
            "total_data_in_data_only_blocks": sum(row["data_in_data_only_blocks"] for row in hit),
            "max_data_only_blocks_per_selection": max((row["data_only_blocks"] for row in hit), default=0),
            "max_data_objects_per_selection": max((row["data_in_data_only_blocks"] for row in hit), default=0),
        }
    result = {
        "status": "GEOMETRY_SUPPORT_AUDIT_ONLY__NO_PAIR_COUNTS_OR_COVARIANCE_READ",
        "selection_resolution_records": len(rows),
        "affected_records": len(affected),
        "by_nside": by_nside,
        "affected": affected,
    }
    assert len(rows) == 194 * 3 and len(affected) == 17
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS: R3 support-union census (582 records, 17 data-only records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

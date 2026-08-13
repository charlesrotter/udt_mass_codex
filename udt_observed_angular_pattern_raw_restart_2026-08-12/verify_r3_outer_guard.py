#!/usr/bin/env python3
"""Exact no-covariance catch-proof for the R3 TreeCorr outer guard."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import treecorr

import run_r1_ingestion_nulls as r1
import run_r2_central_pattern as r2
import run_r3_covariance_atlas as r3


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "R3_OUTER_GUARD_RESULT.json"


def unguarded_count(catalog):
    corr = treecorr.NNCorrelation(
        min_sep=0.25, max_sep=30.0, nbins=119, sep_units="degrees",
        bin_type="Linear", bin_slop=0.0, angle_slop=0.0, brute=False,
    )
    corr.process(catalog, metric="Arc", num_threads=8, corr_only=False)
    return np.rint(np.asarray(corr.npairs)).astype(np.int64), np.asarray(corr.weight)


def main() -> int:
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    sample, cap = "CMASS", "North"
    group = list(r2.groups(sample))[17]
    entry = next(
        item for item in r1.read_manifest()
        if item.kind == "data" and item.sample == sample and item.cap == cap
    )
    data = r1.read_numeric_columns(entry.path, ["RA", "DEC", "Z"], entry.rows)
    shell = r1.assign_shells(data["Z"], sample)
    lo, hi = int(group["members"][0]), int(group["members"][-1])
    index = np.flatnonzero((shell >= lo) & (shell <= hi))
    fine, _ = r3.parent_maps(sample, cap, r3.load_block_pixels())
    patch = r3.patch_labels(data["RA"][index], data["DEC"][index], fine)
    catalog = treecorr.Catalog(
        ra=data["RA"][index], dec=data["DEC"][index],
        ra_units="degrees", dec_units="degrees", w=np.ones(len(index)),
        patch=patch, npatch=len(fine),
    )
    expected = r3.load_r2_components()[(sample, cap, 1, 17, "DD", "W0_UNIT")]

    old_count, old_weight = unguarded_count(catalog)
    old_diff = np.flatnonzero(old_count != expected["count"])
    assert old_diff.tolist() == [118]
    assert int(old_count[118] - expected["count"][118]) == -1
    assert float(old_weight[118] - expected["weight"][118]) == -1.0

    guarded = r3.tree_count(catalog)
    new_count, new_weight = r3.correlation_arrays(guarded)
    assert np.array_equal(new_count, expected["count"])
    assert np.array_equal(new_weight, expected["weight"])
    assert len(guarded.npairs) == 120
    relation = guarded.results[(423, 476)]
    assert int(round(relation.npairs[118])) >= 1

    result = {
        "status": "PASS",
        "selection": "CMASS_North_f1_g17",
        "n_data": len(index),
        "unguarded_differing_bins": old_diff.tolist(),
        "unguarded_bin118_count_difference": int(old_count[118] - expected["count"][118]),
        "guarded_analysis_counts_exact": True,
        "guarded_analysis_weights_exact": True,
        "analysis_bin_count": r3.NBIN,
        "tree_bin_count": r3.TREE_NBIN,
        "discarded_guard_interval_deg": [30.0, r3.TREE_MAX_SEP],
        "guard_bin_pair_count": int(round(guarded.npairs[119])),
        "trigger_relation_bin118_pair_count": int(round(relation.npairs[118])),
        "covariance_read": False,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS: R3 outer guard restores exact 119-bin trigger component")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

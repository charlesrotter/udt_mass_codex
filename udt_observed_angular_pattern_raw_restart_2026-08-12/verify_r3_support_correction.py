#!/usr/bin/env python3
"""Synthetic exact replay of an R3 data-only active block."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import treecorr

import run_r3_covariance_atlas as r3


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "R3_SUPPORT_CORRECTION_RESULT.json"


def catalog(ra, dec, weight, patch=None, npatch=None):
    kwargs = {} if patch is None else {"patch": patch, "npatch": npatch}
    return treecorr.Catalog(
        ra=ra, dec=dec, ra_units="degrees", dec_units="degrees", w=weight, **kwargs
    )


def main() -> int:
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    rng = np.random.default_rng(31082026)
    full_ra = rng.uniform(8.0, 70.0, 700)
    full_dec = rng.uniform(-16.0, 16.0, 700)
    fine_pix = r3.pixel_ids(full_ra, full_dec, 16)
    fine_pixels = np.unique(fine_pix)
    target_pixel = int(fine_pixels[len(fine_pixels) // 2])
    target_full = np.flatnonzero(fine_pix == target_pixel)
    selected_random = fine_pix != target_pixel
    random_ra, random_dec = full_ra[selected_random], full_dec[selected_random]
    extra = target_full[:1]
    chosen = np.concatenate((np.arange(0, 350, 4), extra))
    data_ra, data_dec = full_ra[chosen], full_dec[chosen]
    data_w = 0.8 + (np.arange(len(chosen)) % 13) / 17.0

    dpatch = np.searchsorted(fine_pixels, r3.pixel_ids(data_ra, data_dec, 16)).astype(np.int32)
    rpatch = np.searchsorted(fine_pixels, r3.pixel_ids(random_ra, random_dec, 16)).astype(np.int32)
    target = int(np.searchsorted(fine_pixels, target_pixel))
    assert np.count_nonzero(dpatch == target) > 0 and np.count_nonzero(rpatch == target) == 0
    active = (np.bincount(dpatch, minlength=len(fine_pixels)) > 0) | (
        np.bincount(rpatch, minlength=len(fine_pixels)) > 0
    )
    assert active[target]

    maps, sizes = {}, {}
    for nside in r3.NSIDES:
        parent = fine_pixels // ((16 // nside) ** 2)
        unique = np.unique(parent)
        maps[nside] = np.searchsorted(unique, parent).astype(np.int32)
        sizes[nside] = len(unique)
    D = catalog(data_ra, data_dec, data_w, dpatch, len(fine_pixels))
    R = catalog(random_ra, random_dec, np.ones(len(random_ra)), rpatch, len(fine_pixels))
    correlations = {"DD": r3.tree_count(D), "DR": r3.tree_count(D, R), "RR": r3.tree_count(R)}
    removals = {
        name: r3.aggregate_removals(corr, maps, sizes, chunk_size=19)[16]
        for name, corr in correlations.items()
    }
    keep_d, keep_r = dpatch != target, rpatch != target
    D2 = catalog(data_ra[keep_d], data_dec[keep_d], data_w[keep_d])
    R2 = catalog(random_ra[keep_r], random_dec[keep_r], np.ones(np.count_nonzero(keep_r)))
    rerun = {"DD": r3.tree_count(D2), "DR": r3.tree_count(D2, R2), "RR": r3.tree_count(R2)}
    records = {}
    for name in r3.COMPONENTS:
        full_c, full_w = r3.correlation_arrays(correlations[name])
        got_c = full_c - removals[name]["count"][target]
        got_w = full_w - removals[name]["weight"][target]
        want_c, want_w = r3.correlation_arrays(rerun[name])
        assert np.array_equal(got_c, want_c)
        assert np.allclose(got_w, want_w, rtol=5e-12, atol=1e-10)
        records[name] = {
            "removed_integer_pairs": int(np.sum(removals[name]["count"][target])),
            "removed_weight": float(np.sum(removals[name]["weight"][target])),
        }
    assert records["DD"]["removed_integer_pairs"] > 0
    assert records["DR"]["removed_integer_pairs"] > 0
    assert records["RR"]["removed_integer_pairs"] == 0
    result = {
        "status": "PASS",
        "seed": 31082026,
        "target_full_footprint_pixel": target_pixel,
        "target_selected_data_count": int(np.count_nonzero(dpatch == target)),
        "target_selected_random_count": 0,
        "active_union_includes_target": True,
        "exact_rerun_components": records,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS: exact data-only block deletion replay")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

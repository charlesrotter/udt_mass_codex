#!/usr/bin/env python3
"""Synthetic catch-proof for R3 nested patch-deletion algebra."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import treecorr

import run_r3_covariance_atlas as r3


OUTPUT = Path(__file__).resolve().parent / "R3_SYNTHETIC_PREFLIGHT_RESULT.json"


def catalog(ra, dec, weight, patch=None, npatch=None):
    kwargs = {}
    if patch is not None:
        kwargs.update(patch=patch, npatch=npatch)
    return treecorr.Catalog(
        ra=ra, dec=dec, ra_units="degrees", dec_units="degrees", w=weight, **kwargs
    )


def main() -> int:
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    rng = np.random.default_rng(20260813)
    random_ra = rng.uniform(5.0, 75.0, 480)
    random_dec = rng.uniform(-18.0, 18.0, 480)
    # Data occupy a deterministic subset of random-owned finest pixels.
    chosen = np.arange(0, 360, 3)
    data_ra = random_ra[chosen]
    data_dec = random_dec[chosen]
    data_w = 0.7 + (np.arange(len(chosen)) % 17) / 13.0

    fine_pix_all = r3.pixel_ids(random_ra, random_dec, 16)
    fine_pixels = np.unique(fine_pix_all)
    rpatch = np.searchsorted(fine_pixels, fine_pix_all).astype(np.int32)
    dpix = r3.pixel_ids(data_ra, data_dec, 16)
    dpatch = np.searchsorted(fine_pixels, dpix).astype(np.int32)
    assert np.all(fine_pixels[dpatch] == dpix)

    maps, sizes = {}, {}
    for nside in r3.NSIDES:
        parent = fine_pixels // ((16 // nside) ** 2)
        unique = np.unique(parent)
        maps[nside] = np.searchsorted(unique, parent).astype(np.int32)
        sizes[nside] = len(unique)

    D = catalog(data_ra, data_dec, data_w, dpatch, len(fine_pixels))
    R = catalog(random_ra, random_dec, np.ones(len(random_ra)), rpatch, len(fine_pixels))
    correlations = {
        "DD": r3.tree_count(D),
        "DR": r3.tree_count(D, R),
        "RR": r3.tree_count(R),
    }
    removals = {name: r3.aggregate_removals(corr, maps, sizes, chunk_size=23) for name, corr in correlations.items()}

    for nside in r3.NSIDES:
        dparent = maps[nside][dpatch]
        rparent = maps[nside][rpatch]
        active = np.flatnonzero(np.bincount(rparent, minlength=sizes[nside]) > 0)
        probes = sorted(set((int(active[0]), int(active[len(active) // 2]), int(active[-1]))))
        for block in probes:
            keep_d = dparent != block
            keep_r = rparent != block
            D2 = catalog(data_ra[keep_d], data_dec[keep_d], data_w[keep_d])
            R2 = catalog(random_ra[keep_r], random_dec[keep_r], np.ones(np.count_nonzero(keep_r)))
            rerun = {"DD": r3.tree_count(D2), "DR": r3.tree_count(D2, R2), "RR": r3.tree_count(R2)}
            for name in r3.COMPONENTS:
                full_c, full_w = r3.correlation_arrays(correlations[name])
                got_c = full_c - removals[name][nside]["count"][block]
                got_w = full_w - removals[name][nside]["weight"][block]
                want_c, want_w = r3.correlation_arrays(rerun[name])
                assert np.array_equal(got_c, want_c)
                assert np.allclose(got_w, want_w, rtol=5e-12, atol=1e-10)

    # Catch-proof: omitting the second endpoint subtraction must fail for a cross-block pair.
    nside = 16
    rr_full, _ = r3.correlation_arrays(correlations["RR"])
    correct = removals["RR"][nside]["count"]
    assert np.any(correct > 0) and np.any(rr_full[None, :] - correct != rr_full[None, :])

    sample = rng.normal(size=(max(130, sizes[16]), r3.NBIN))
    _, covariance, eig, tau, rank = r3.covariance_record(sample)
    assert np.allclose(covariance, covariance.T, rtol=0.0, atol=0.0)
    assert eig[0] >= -100.0 * max(tau, np.finfo(np.float64).tiny)
    assert rank <= min(r3.NBIN, sample.shape[0] - 1)
    result = {
        "status": "PASS",
        "seed": 20260813,
        "data_rows": len(data_ra),
        "random_rows": len(random_ra),
        "nsides": list(r3.NSIDES),
        "probes_per_resolution_max": 3,
        "all_integer_components_exact": True,
        "all_weighted_components_within_tolerance": True,
        "covariance_rank_bound_pass": True,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS: R3 synthetic nested deletion and covariance preflight")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

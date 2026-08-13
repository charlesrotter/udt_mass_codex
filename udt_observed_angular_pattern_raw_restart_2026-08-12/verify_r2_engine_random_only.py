#!/usr/bin/env python3
"""Independent random-only Corrfunc/TreeCorr/brute anchor for R2."""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import treecorr
from Corrfunc.mocks.DDtheta_mocks import DDtheta_mocks

import run_r1_ingestion_nulls as r1


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "R2_PREENGINE_RESULT.json"
EDGES = np.arange(0.25, 30.0001, 0.25, dtype=np.float64)
NPSEUDO = 33_107


def corrfunc_count(auto, ra1, dec1, w1, ra2=None, dec2=None, w2=None):
    result = DDtheta_mocks(
        1 if auto else 0, 8, EDGES, ra1, dec1, weights1=w1, RA2=ra2, DEC2=dec2,
        weights2=w2, weight_type="pair_product", link_in_dec=True, link_in_ra=True,
        output_thetaavg=False, fast_acos=False, isa="fastest",
    )
    factor = 2 if auto else 1
    return result["npairs"].astype(np.int64) // factor, result["npairs"] * result["weightavg"] / factor


def treecorr_count(auto, ra1, dec1, w1, ra2=None, dec2=None, w2=None):
    config = dict(
        min_sep=0.25, max_sep=30.0, nbins=119, sep_units="degrees", bin_type="Linear",
        bin_slop=0.0, angle_slop=0.0, brute=False,
    )
    cat1 = treecorr.Catalog(ra=ra1, dec=dec1, ra_units="degrees", dec_units="degrees", w=w1)
    nn = treecorr.NNCorrelation(**config)
    if auto:
        nn.process(cat1, metric="Arc", num_threads=8, corr_only=False)
    else:
        cat2 = treecorr.Catalog(ra=ra2, dec=dec2, ra_units="degrees", dec_units="degrees", w=w2)
        nn.process(cat1, cat2, metric="Arc", num_threads=8, corr_only=False)
    return nn.npairs.astype(np.int64), nn.weight.astype(np.float64)


def direct_count(auto, ra1, dec1, w1, ra2=None, dec2=None, w2=None):
    rb, db, wb = (ra1, dec1, w1) if auto else (ra2, dec2, w2)
    cosine = (
        np.sin(np.deg2rad(dec1))[:, None] * np.sin(np.deg2rad(db))[None, :]
        + np.cos(np.deg2rad(dec1))[:, None] * np.cos(np.deg2rad(db))[None, :]
        * np.cos(np.deg2rad(ra1)[:, None] - np.deg2rad(rb)[None, :])
    )
    theta = np.rad2deg(np.arccos(np.clip(cosine, -1.0, 1.0)))
    pair_weight = w1[:, None] * wb[None, :]
    if auto:
        upper = np.triu_indices(len(ra1), 1)
        theta, pair_weight = theta[upper], pair_weight[upper]
    else:
        theta, pair_weight = theta.ravel(), pair_weight.ravel()
    return np.histogram(theta, bins=EDGES)[0], np.histogram(theta, bins=EDGES, weights=pair_weight)[0]


def main() -> int:
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    entries = r1.read_manifest()
    entry = next(e for e in entries if e.sample == "CMASS" and e.cap == "North" and e.kind == "random")
    columns = r1.read_numeric_columns(entry.path, ["RA", "DEC", "Z"], entry.rows)
    shell = r1.assign_shells(columns["Z"], "CMASS")
    candidates = np.flatnonzero(shell == 35)
    hashes = r1.splitmix64(np.arange(entry.rows, dtype=np.uint64), int(entry.sha256[:16], 16))
    needed = 6 * NPSEUDO
    local = np.argpartition(hashes[candidates], needed - 1)[:needed]
    local = local[np.lexsort((candidates[local], hashes[candidates][local]))]
    chosen = candidates[local]
    data_index, random_index = chosen[:NPSEUDO], chosen[NPSEUDO:]
    wd = 0.5 + ((hashes[data_index] >> np.uint64(11)).astype(np.float64) / 2**53)
    wr = 0.5 + ((hashes[random_index] >> np.uint64(11)).astype(np.float64) / 2**53)

    cases = (
        ("DD", True, data_index, None, wd, None),
        ("DR", False, data_index, random_index, wd, wr),
        ("RR", True, random_index, None, wr, None),
    )
    records = []
    for name, auto, ia, ib, wa, wb in cases:
        args = (
            columns["RA"][ia], columns["DEC"][ia], wa,
            None if ib is None else columns["RA"][ib],
            None if ib is None else columns["DEC"][ib], wb,
        )
        tick = time.monotonic()
        cc, cw = corrfunc_count(auto, *args)
        split = time.monotonic()
        tc, tw = treecorr_count(auto, *args)
        done = time.monotonic()
        records.append({
            "component": name,
            "corrfunc_seconds": split - tick,
            "treecorr_seconds": done - split,
            "integer_counts_exact": bool(np.array_equal(cc, tc)),
            "max_weight_abs_difference": float(np.max(np.abs(cw - tw))),
            "max_weight_relative_difference": float(np.max(np.abs(cw - tw) / np.maximum(np.abs(tw), 1.0))),
        })

    # A genuinely different direct calculation on compact prefixes.
    compact_records = []
    compact_cases = (
        ("DD", True, data_index[:257], None, wd[:257], None),
        ("DR", False, data_index[:257], random_index[:521], wd[:257], wr[:521]),
        ("RR", True, random_index[:521], None, wr[:521], None),
    )
    for name, auto, ia, ib, wa, wb in compact_cases:
        args = (
            columns["RA"][ia], columns["DEC"][ia], wa,
            None if ib is None else columns["RA"][ib],
            None if ib is None else columns["DEC"][ib], wb,
        )
        cc, cw = corrfunc_count(auto, *args)
        dc, dw = direct_count(auto, *args)
        compact_records.append({
            "component": name,
            "integer_counts_exact": bool(np.array_equal(cc, dc)),
            "max_weight_abs_difference": float(np.max(np.abs(cw - dw))),
            "max_weight_relative_difference": float(np.max(np.abs(cw - dw) / np.maximum(np.abs(dw), 1.0))),
        })

    result = {
        "status": "PASS",
        "galaxy_catalog_read": False,
        "source": str(entry.path),
        "source_sha256": entry.sha256,
        "shell_id": 35,
        "pseudo_data_count": NPSEUDO,
        "pseudo_random_count": 5 * NPSEUDO,
        "corrfunc": "2.5.3",
        "treecorr": treecorr.__version__,
        "large_random_only": records,
        "compact_direct": compact_records,
    }
    assert all(x["integer_counts_exact"] for x in records + compact_records)
    assert max(x["max_weight_relative_difference"] for x in records) <= 5e-9
    assert max(x["max_weight_relative_difference"] for x in compact_records) <= 5e-12
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS: R2 random-only Corrfunc/TreeCorr/direct engine anchor")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

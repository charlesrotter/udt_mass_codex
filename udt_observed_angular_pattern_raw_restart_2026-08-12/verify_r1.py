#!/usr/bin/env python3
"""Independent finite-output verification for R1."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
EDGES_DEG = np.arange(0.25, 30.0001, 0.25, dtype=np.float64)
EDGES_CHORD = 2.0 * np.sin(np.deg2rad(EDGES_DEG) / 2.0)


def rows(name: str):
    with (ROOT / name).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def brute(a: np.ndarray, b: np.ndarray | None = None) -> np.ndarray:
    if b is None:
        dist = np.linalg.norm(a[:, None, :] - a[None, :, :], axis=2)
        dist = dist[np.triu_indices(a.shape[0], 1)]
    else:
        dist = np.linalg.norm(a[:, None, :] - b[None, :, :], axis=2).ravel()
    return np.histogram(dist, bins=EDGES_CHORD)[0].astype(np.int64)


def main() -> int:
    result = json.loads((ROOT / "R1_RESULT.json").read_text())
    assert result["galaxy_pair_counts_computed"] is False
    assert result["fine_shells"] == 110
    assert result["angular_bin_count"] == 119

    files = rows("R1_FILE_INGESTION_SUMMARY.tsv")
    ingest = rows("R1_INGESTION_ATLAS.tsv")
    null = rows("R1_RANDOM_NULL_ATLAS.tsv")
    summaries = rows("R1_RANDOM_NULL_SUMMARY.tsv")
    anchors = rows("R1_ENGINE_ANCHOR.tsv")
    assert len(files) == 8 and len(ingest) == 110
    assert all(int(row["rows_manifest"]) == int(row["rows_read"]) for row in files)
    assert all(int(row["all_allowed_finite"]) == 1 for row in files)
    sampled = [row for row in ingest if row["r1_status"] == "SAMPLED"]
    assert len(null) == len(sampled) * 2 * 119
    assert len(summaries) == len(sampled) * 3

    # Recompute every Landy--Szalay output from frozen raw counts and sample sizes.
    nlookup = {
        (row["sample"], row["cap"], row["shell_id"], row["replicate"]): row
        for row in summaries if row["replicate"] in {"0", "1"}
    }
    for row in null:
        key = (row["sample"], row["cap"], row["shell_id"], row["replicate"])
        summary = nlookup[key]
        nd, nr = int(summary["n_pseudo_data"]), int(summary["n_pseudo_random"])
        dd, dr, rr = int(row["dd_raw"]), int(row["dr_raw"]), int(row["rr_raw"])
        ddn = dd / (nd * (nd - 1) / 2.0)
        drn = dr / (nd * nr)
        rrn = rr / (nr * (nr - 1) / 2.0)
        w = (ddn - 2.0 * drn + rrn) / rrn
        sigma = np.sqrt(1.0 / max(dd, 1) + 4.0 / max(dr, 1) + 1.0 / rr)
        assert np.isclose(float(row["dd_norm"]), ddn, rtol=2e-15, atol=0.0)
        assert np.isclose(float(row["dr_norm"]), drn, rtol=2e-15, atol=0.0)
        assert np.isclose(float(row["rr_norm"]), rrn, rtol=2e-15, atol=0.0)
        assert np.isclose(float(row["w_null"]), w, rtol=2e-14, atol=1e-18)
        assert np.isclose(float(row["sigma_proxy"]), sigma, rtol=2e-15, atol=0.0)

    # Independent brute-force replay on compact actual-catalog coordinate anchors.
    bundle = np.load(ROOT / "R1_ENGINE_ANCHOR_INPUTS.npz")
    amap = {(r["sample"], r["cap"], r["family"]): r for r in anchors}
    for sample in ("CMASS", "LOWZ"):
        for cap in ("North", "South"):
            label = f"{sample}_{cap}"
            d, r = bundle[f"{label}_data"], bundle[f"{label}_random"]
            for family, counts in (("DD", brute(d)), ("DR", brute(d, r)), ("RR", brute(r))):
                recorded = amap[(sample, cap, family)]
                fast_saved = np.asarray([int(x) for x in recorded["fast_counts_csv"].split(",")])
                brute_saved = np.asarray([int(x) for x in recorded["brute_counts_csv"].split(",")])
                assert np.array_equal(counts, fast_saved)
                assert np.array_equal(counts, brute_saved)
                assert int(recorded["max_abs_count_difference"]) == 0
                assert int(recorded["all_bins_exact"]) == 1

    assert bool(result["independent_actual_catalog_pair_anchors_pass"])
    print(
        "PASS: R1 independent verification "
        f"({len(ingest)} shells, {len(null)} null-bin rows, {len(anchors)} actual-catalog anchors)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

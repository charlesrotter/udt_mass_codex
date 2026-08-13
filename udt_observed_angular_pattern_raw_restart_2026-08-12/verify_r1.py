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
    curves: dict[tuple[str, str, str, str], list[tuple[int, float, float]]] = {}
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
        bin_id = int(round((float(row["theta_lo_deg"]) - 0.25) / 0.25))
        curves.setdefault(key, []).append((bin_id, w, sigma))

    # Reconstruct every per-replicate and between-replicate summary and guard independently.
    summary_lookup = {
        (row["sample"], row["cap"], row["shell_id"], row["replicate"]): row
        for row in summaries
    }
    for key, values in curves.items():
        values.sort()
        assert [item[0] for item in values] == list(range(119))
        w = np.asarray([item[1] for item in values])
        sigma = np.asarray([item[2] for item in values])
        z = w / sigma
        recorded = summary_lookup[key]
        checks = {
            "max_abs_w": np.max(np.abs(w)),
            "rms_w": np.sqrt(np.mean(w * w)),
            "max_abs_z_proxy": np.max(np.abs(z)),
            "rms_z_proxy": np.sqrt(np.mean(z * z)),
        }
        for field, value in checks.items():
            assert np.isclose(float(recorded[field]), value, rtol=2e-14, atol=1e-18)
        guard = int(checks["max_abs_z_proxy"] <= 12.0 and checks["rms_z_proxy"] <= 3.0)
        assert int(recorded["within_registered_guard"]) == guard

    shell_keys = sorted({key[:3] for key in curves})
    for shell_key in shell_keys:
        v0 = sorted(curves[shell_key + ("0",)])
        v1 = sorted(curves[shell_key + ("1",)])
        w0, s0 = np.asarray([x[1] for x in v0]), np.asarray([x[2] for x in v0])
        w1, s1 = np.asarray([x[1] for x in v1]), np.asarray([x[2] for x in v1])
        dw = w0 - w1
        dz = dw / np.sqrt(s0 * s0 + s1 * s1)
        recorded = summary_lookup[shell_key + ("DIFFERENCE_0_MINUS_1",)]
        checks = {
            "max_abs_w": np.max(np.abs(dw)),
            "rms_w": np.sqrt(np.mean(dw * dw)),
            "max_abs_z_proxy": np.max(np.abs(dz)),
            "rms_z_proxy": np.sqrt(np.mean(dz * dz)),
        }
        for field, value in checks.items():
            assert np.isclose(float(recorded[field]), value, rtol=2e-14, atol=1e-18)
        guard = int(checks["max_abs_z_proxy"] <= 12.0 and checks["rms_z_proxy"] <= 3.0)
        assert int(recorded["within_registered_guard"]) == guard

    assert all(int(row["within_registered_guard"]) == 1 for row in summaries)
    assert bool(result["registered_guards_pass"])

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

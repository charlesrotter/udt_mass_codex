#!/usr/bin/env python3
"""FD1 Phase II: preregistered Planck TT basin readout of the frozen Phase-I atlas."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
ATLAS = ROOT / "phase1_atlas_g240.json"
OUTPUT = ROOT / "phase2_comparison.json"

# Planck Collaboration, 2018 Results I, A&A 641 A1 (2020), Table 5.
# These values enter only after Phase I was committed at e7268d61.
PEAKS = np.array([220.6, 538.1, 809.8, 1147.8, 1446.8, 1779.0, 2075.0])
PEAK_SIGMA = np.array([0.6, 1.3, 1.0, 2.3, 1.6, 3.0, 8.0])
TROUGHS = np.array([416.3, 675.5, 1001.1, 1290.0, 1623.8, 1919.0, 2241.0])
HISTORICAL_RA2_MAX_FRACTIONAL_RESIDUAL = 0.031
KEYS: dict[str, bool] = {}


def key(name: str, condition: bool) -> None:
    KEYS[name] = bool(condition)
    print(f"KEY {name}: {KEYS[name]}")


def identity(row: dict[str, object]) -> tuple[object, ...]:
    return row["n_label"], row["q_ratio"], row["wall"], row["hbar"]


def affine_fit(frequencies: np.ndarray) -> tuple[float, float, np.ndarray]:
    design = np.column_stack((frequencies, np.ones_like(frequencies)))
    scale, offset = np.linalg.lstsq(design, PEAKS, rcond=None)[0]
    return float(scale), float(offset), scale * frequencies + offset


def one_scale_fit(frequencies: np.ndarray) -> tuple[float, np.ndarray]:
    scale = float(np.dot(frequencies, PEAKS) / np.dot(frequencies, frequencies))
    return scale, scale * frequencies


def compare_row(row: dict[str, object]) -> dict[str, object]:
    common = {
        "n_label": row["n_label"],
        "n": row["n"],
        "q_ratio": row["q_ratio"],
        "q": row["q"],
        "qcrit": row["qcrit"],
        "hbar": row["hbar"],
        "wall": row["wall"],
    }
    if float(row["hbar"]) == 0.0:
        return {**common, "classification": "MU_OFF_LIMIT_POINT_CONTINUUM"}

    wm = np.asarray(row["omega_mminus"][:7], dtype=float)
    w0 = np.asarray(row["omega_m0"][:7], dtype=float)
    wp = np.asarray(row["omega_mplus"][:7], dtype=float)
    scale, offset, ell0 = affine_fit(w0)
    ellm = scale * wm + offset
    ellp = scale * wp + offset
    residual = ell0 - PEAKS
    fractional = residual / PEAKS
    one_scale, ell0_one_scale = one_scale_fit(w0)
    one_scale_fractional = (ell0_one_scale - PEAKS) / PEAKS

    # Peaks 2..7 have a published trough on each side.  Peak 1 is an edge case.
    left = TROUGHS[:6]
    right = TROUGHS[1:7]
    basin = np.minimum(PEAKS[1:] - left, right - PEAKS[1:])
    centered_displacement = np.maximum(np.abs(ellp[1:] - ell0[1:]), np.abs(ellm[1:] - ell0[1:]))
    half_split = 0.5 * np.abs(ellp[1:] - ellm[1:])
    centered_margin = basin - centered_displacement
    split_margin = basin - half_split
    absolute_margin = np.minimum.reduce((ellm[1:] - left, ellp[1:] - left, right - ellm[1:], right - ellp[1:]))

    centered_contained = bool(np.all(centered_margin >= 0.0))
    splitting_small = bool(np.all(split_margin >= 0.0))
    absolute_contained = bool(np.all(absolute_margin >= 0.0))
    if centered_contained:
        morphology = "FULL_CENTERED_MULTIPLET_CONTAINMENT"
    elif splitting_small:
        morphology = "SPLITTING_ONLY"
    else:
        morphology = "BASIN_MISMATCH"

    return {
        **common,
        "classification": morphology,
        "affine_scale": scale,
        "affine_offset": offset,
        "m0_prediction": ell0.tolist(),
        "mminus_prediction": ellm.tolist(),
        "mplus_prediction": ellp.tolist(),
        "m0_residual": residual.tolist(),
        "m0_fractional_residual": fractional.tolist(),
        "m0_max_abs_fractional_residual": float(np.max(np.abs(fractional))),
        "m0_rms_fractional_residual": float(np.sqrt(np.mean(fractional**2))),
        "historical_ra2_line_met": bool(np.max(np.abs(fractional)) <= HISTORICAL_RA2_MAX_FRACTIONAL_RESIDUAL),
        "one_scale": one_scale,
        "one_scale_prediction": ell0_one_scale.tolist(),
        "one_scale_max_abs_fractional_residual": float(np.max(np.abs(one_scale_fractional))),
        "basin_peak_indices": [2, 3, 4, 5, 6, 7],
        "basin_clearance": basin.tolist(),
        "centered_displacement": centered_displacement.tolist(),
        "half_split": half_split.tolist(),
        "centered_margin": centered_margin.tolist(),
        "split_margin": split_margin.tolist(),
        "absolute_trough_margin": absolute_margin.tolist(),
        "centered_contained": centered_contained,
        "splitting_small": splitting_small,
        "absolute_contained_diagnostic": absolute_contained,
    }


def consecutive_intervals(rows: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    by_family: dict[tuple[float, str], dict[float, dict[str, bool]]] = defaultdict(lambda: defaultdict(dict))
    for row in rows:
        if float(row["hbar"]) == 0.0:
            continue
        by_family[(float(row["q_ratio"]), str(row["wall"]))][float(row["hbar"])][str(row["n_label"])] = bool(row[field])
    intervals = []
    for (q_ratio, wall), hmap in sorted(by_family.items()):
        states = [(hbar, len(nstates) == 3 and all(nstates.values())) for hbar, nstates in sorted(hmap.items())]
        runs: list[list[float]] = []
        current: list[float] = []
        for hbar, state in states:
            if state:
                current.append(hbar)
            elif current:
                runs.append(current)
                current = []
        if current:
            runs.append(current)
        for run in runs:
            if len(run) >= 2:
                intervals.append({
                    "q_ratio": q_ratio,
                    "wall": wall,
                    "hbar_first_grid": run[0],
                    "hbar_last_grid": run[-1],
                    "grid_points": run,
                    "all_three_sne_n_samples": True,
                    "field": field,
                })
    return intervals


def main() -> None:
    atlas = json.loads(ATLAS.read_text(encoding="utf-8"))
    key("FD1_P2_K1_phase1_frozen_blind", atlas["observational_width_values_loaded"] is False and all(atlas["keys"].values()))
    rows = [compare_row(row) for row in atlas["rows"]]
    live = [row for row in rows if float(row["hbar"]) > 0.0]
    key("FD1_P2_K2_row_count", len(rows) == 462 and len(live) == 420 and len({identity(row) for row in rows}) == 462)
    key("FD1_P2_K3_positive_affine_scale", all(float(row["affine_scale"]) > 0.0 for row in live))
    key("FD1_P2_K4_finite_readout", all(np.isfinite(float(row["m0_max_abs_fractional_residual"])) for row in live))
    key("FD1_P2_K5_edge_peak_excluded", all(row["basin_peak_indices"] == [2, 3, 4, 5, 6, 7] for row in live))

    morphology_intervals = consecutive_intervals(live, "centered_contained")
    historical_line_intervals = consecutive_intervals(live, "historical_ra2_line_met")
    joint_rows = []
    for row in live:
        row["joint_centered_and_historical_line"] = bool(row["centered_contained"] and row["historical_ra2_line_met"])
        joint_rows.append(row)
    joint_intervals = consecutive_intervals(joint_rows, "joint_centered_and_historical_line")
    split_rows = []
    for row in live:
        row["splitting_only_boolean"] = bool(row["splitting_small"] and not row["centered_contained"])
        split_rows.append(row)
    splitting_only_intervals = consecutive_intervals(split_rows, "splitting_only_boolean")

    key("FD1_P2_K6_morphology_exhaustive", all(row["classification"] in {
        "FULL_CENTERED_MULTIPLET_CONTAINMENT", "SPLITTING_ONLY", "BASIN_MISMATCH"
    } for row in live))
    key("FD1_P2_K7_anti_split_only", all(
        row["classification"] != "FULL_CENTERED_MULTIPLET_CONTAINMENT" or row["centered_contained"]
        for row in live
    ))

    count_by_class: dict[str, int] = defaultdict(int)
    count_by_wall: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in live:
        count_by_class[str(row["classification"])] += 1
        count_by_wall[str(row["wall"])][str(row["classification"])] += 1

    if joint_intervals:
        landed = "FD1-OPEN-COMPATIBILITY-WINDOW"
    elif morphology_intervals and splitting_only_intervals:
        landed = "FD1-MIXED"
    elif morphology_intervals:
        landed = "FD1-OPEN-COMPATIBILITY-WINDOW_WITH_SHAPE_THRESHOLD_UNGRADED"
    elif splitting_only_intervals:
        landed = "FD1-SPLITTING-ONLY-WINDOW"
    else:
        landed = "FD1-NO-BACKGROUND-WINDOW-IN-SLICE"

    payload = {
        "phase": "FD1_PHASE2_ATTRIBUTED_READOUT",
        "source": {
            "citation": "Planck Collaboration, Planck 2018 Results I, A&A 641 A1 (2020), Table 5",
            "doi": "https://doi.org/10.1051/0004-6361/201833880",
            "peaks": PEAKS.tolist(),
            "peak_sigma": PEAK_SIGMA.tolist(),
            "troughs": TROUGHS.tolist(),
        },
        "phase1_commit": "e7268d61",
        "phase1_atlas_sha256": hashlib.sha256(ATLAS.read_bytes()).hexdigest(),
        "keys": KEYS,
        "summary": {
            "landed_classification": landed,
            "class_counts": dict(count_by_class),
            "class_counts_by_wall": {wall: dict(counts) for wall, counts in count_by_wall.items()},
            "morphology_intervals": morphology_intervals,
            "historical_ra2_line_intervals": historical_line_intervals,
            "joint_intervals": joint_intervals,
            "splitting_only_intervals": splitting_only_intervals,
            "minimum_centered_margin": min(min(row["centered_margin"]) for row in live),
            "maximum_centered_margin": max(min(row["centered_margin"]) for row in live),
            "minimum_m0_max_abs_fractional_residual": min(row["m0_max_abs_fractional_residual"] for row in live),
            "maximum_m0_max_abs_fractional_residual": max(row["m0_max_abs_fractional_residual"] for row in live),
            "historical_line_is_report_only_not_merit_filter": True,
        },
        "rows": rows,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"WROTE {OUTPUT}")
    print(f"TOTAL KEYS {sum(KEYS.values())}/{len(KEYS)}")
    if not all(KEYS.values()):
        raise SystemExit(f"failed keys: {[name for name, passed in KEYS.items() if not passed]}")


if __name__ == "__main__":
    main()

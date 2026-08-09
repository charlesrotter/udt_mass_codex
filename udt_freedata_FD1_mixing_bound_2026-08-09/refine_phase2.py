#!/usr/bin/env python3
"""Refine and convergence-check the eight frozen FD1 Phase-II transition brackets."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

import derive_phase1 as p1
import derive_phase2 as p2


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "phase2_transition_refinement.json"
INV_N_VALUES = p1.INV_N_VALUES
BRACKETS = (
    (0.75, "D", "entry", 0.001, 0.002),
    (0.75, "D", "exit", 0.02, 0.05),
    (0.75, "N", "entry", 0.002, 0.005),
    (0.75, "N", "exit", 0.02, 0.05),
    (0.95, "D", "entry", 0.1, 0.2),
    (0.95, "D", "exit", 0.5, 1.0),
    (0.95, "N", "entry", 0.1, 0.2),
    (0.95, "N", "exit", 0.5, 1.0),
)
KEYS: dict[str, bool] = {}


def key(name: str, condition: bool) -> None:
    KEYS[name] = bool(condition)
    print(f"KEY {name}: {KEYS[name]}")


def spectral_row(inv_n: float, q_ratio: float, wall: str, hbar: float, grid: int, cutoff_factor: float) -> dict[str, object]:
    n = 1.0 / inv_n
    q = p1.q_value(n, q_ratio)
    umin = p1.family_umin(n, q) * cutoff_factor
    geometry = p1.make_x_geometry(n, q, hbar, umin, grid)
    modes: dict[int, np.ndarray] = {}
    residuals: dict[int, float] = {}
    for m in (-1, 0, 1):
        solved = p1.solve_modes(geometry, m, wall)
        frequencies = np.asarray(solved["omega"][:p1.NMODES])
        modes[m] = frequencies
        residuals[m] = float(max(solved["raw_backward_residuals"][:p1.NMODES]))
    mean_pair = 0.5 * (modes[1] + modes[-1])
    return {
        "n_label": f"inv_n={inv_n:.4f}",
        "n": n,
        "q_ratio": q_ratio,
        "q": q,
        "qcrit": (2.0 - n) / 2.0,
        "hbar": hbar,
        "wall": wall,
        "omega_mminus": modes[-1].tolist(),
        "omega_m0": modes[0].tolist(),
        "omega_mplus": modes[1].tolist(),
        "eta_split": (np.abs(modes[1] - modes[-1]) / mean_pair).tolist(),
        "full_displacement": (
            np.maximum(np.abs(modes[1] - modes[0]), np.abs(modes[-1] - modes[0])) / modes[0]
        ).tolist(),
        "umin": umin,
        "grid": grid,
        "cutoff_factor": cutoff_factor,
        "max_raw_backward_residual": {str(m): value for m, value in residuals.items()},
    }


def evaluate(q_ratio: float, wall: str, hbar: float, grid: int, cutoff_factor: float = 1.0) -> dict[str, object]:
    spectral_rows = [spectral_row(inv_n, q_ratio, wall, hbar, grid, cutoff_factor) for inv_n in INV_N_VALUES]
    rows = [p2.compare_row(row) for row in spectral_rows]
    shape_margins = [p2.HISTORICAL_RA2_MAX_FRACTIONAL_RESIDUAL - row["m0_max_abs_fractional_residual"] for row in rows]
    centered_margins = [
        min(np.asarray(row["centered_margin"]) / np.asarray(row["basin_clearance"]))
        for row in rows
    ]
    shape_margin = float(min(shape_margins))
    centered_margin = float(min(centered_margins))
    joint_margin = min(shape_margin, centered_margin)
    return {
        "q_ratio": q_ratio,
        "wall": wall,
        "hbar": hbar,
        "grid": grid,
        "cutoff_factor": cutoff_factor,
        "inside": bool(shape_margin >= 0.0 and centered_margin >= 0.0),
        "shape_margin": shape_margin,
        "normalized_centered_margin": centered_margin,
        "joint_margin": joint_margin,
        "controlling_condition": "HISTORICAL_SHAPE_LINE" if shape_margin <= centered_margin else "CENTERED_MULTIPLET",
        "maximum_raw_backward_residual": max(
            value for row in spectral_rows for value in row["max_raw_backward_residual"].values()
        ),
        "rows": rows,
    }


def bisect(q_ratio: float, wall: str, low: float, high: float, grid: int) -> dict[str, object]:
    cache: dict[float, dict[str, object]] = {}

    def sample(hbar: float) -> dict[str, object]:
        if hbar not in cache:
            cache[hbar] = evaluate(q_ratio, wall, hbar, grid)
        return cache[hbar]

    left, right = low, high
    left_state, right_state = bool(sample(left)["inside"]), bool(sample(right)["inside"])
    if left_state == right_state:
        raise RuntimeError(f"unbracketed transition q={q_ratio} wall={wall} {low}-{high}")
    for _ in range(8):
        middle = math.sqrt(left * right)
        middle_state = bool(sample(middle)["inside"])
        if middle_state == left_state:
            left = middle
        else:
            right = middle
    boundary = math.sqrt(left * right)
    return {
        "grid": grid,
        "boundary_estimate": boundary,
        "left": sample(left),
        "right": sample(right),
        "samples": [cache[hbar] for hbar in sorted(cache)],
    }


def main() -> None:
    transitions = []
    orientations_ok = True
    residual_ok = True
    boundary_convergence = []
    for q_ratio, wall, edge, low, high in BRACKETS:
        coarse = bisect(q_ratio, wall, low, high, 180)
        primary = bisect(q_ratio, wall, low, high, 240)
        log_drift = abs(math.log(coarse["boundary_estimate"] / primary["boundary_estimate"]))
        boundary_convergence.append(log_drift)
        endpoint_variants = []
        expected = {
            low: bool(primary["samples"][0]["inside"]),
            high: bool(primary["samples"][-1]["inside"]),
        }
        for grid, factor in ((320, 1.0), (240, 0.1), (240, 0.01)):
            for hbar in (low, high):
                result = evaluate(q_ratio, wall, hbar, grid, factor)
                orientations_ok &= bool(result["inside"]) == expected[hbar]
                residual_ok &= float(result["maximum_raw_backward_residual"]) < 1.0e-8
                endpoint_variants.append(result)
        transitions.append({
            "q_ratio": q_ratio,
            "wall": wall,
            "edge": edge,
            "original_bracket": [low, high],
            "coarse_bisection": coarse,
            "primary_bisection": primary,
            "boundary_log_drift_g180_g240": log_drift,
            "endpoint_variants": endpoint_variants,
        })
        print(
            f"TRANSITION q={q_ratio:.2f} wall={wall} {edge} "
            f"g180={coarse['boundary_estimate']:.8g} g240={primary['boundary_estimate']:.8g} "
            f"logdrift={log_drift:.3e}"
        )

    key("FD1_R1_transition_count", len(transitions) == 8)
    key("FD1_R2_boundary_grid_convergence", max(boundary_convergence) < 0.10)
    key("FD1_R3_endpoint_orientation", orientations_ok)
    key("FD1_R4_raw_backward_residual", residual_ok)
    key("FD1_R5_no_new_family", {(item[0], item[1], item[2]) for item in BRACKETS} == {
        (transition["q_ratio"], transition["wall"], transition["edge"]) for transition in transitions
    })
    payload = {
        "phase": "FD1_PHASE2_TRANSITION_REFINEMENT",
        "keys": KEYS,
        "summary": {
            "transition_count": len(transitions),
            "maximum_boundary_log_drift_g180_g240": max(boundary_convergence),
            "endpoint_orientation_preserved": orientations_ok,
            "all_raw_backward_residuals_below_1e-8": residual_ok,
            "historical_ra2_line_is_report_only": True,
        },
        "transitions": transitions,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"WROTE {OUTPUT}")
    print(f"TOTAL KEYS {sum(KEYS.values())}/{len(KEYS)}")
    if not all(KEYS.values()):
        raise SystemExit(f"failed keys: {[name for name, passed in KEYS.items() if not passed]}")


if __name__ == "__main__":
    main()

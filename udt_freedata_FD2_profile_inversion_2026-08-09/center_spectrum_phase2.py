#!/usr/bin/env python3
"""Attributed Planck readout of the frozen regular-center spectrum correction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
PHASE1 = ROOT / "center_spectrum_phase1.json"
OUTPUT = ROOT / "center_spectrum_phase2.json"
EXPECTED_PHASE1_HASH = "8fe6c747b5f2629e6fbd4ddb44bd40452d39052a71adc1aa46cfbad1771ae567"

# Planck Collaboration, 2018 Results I, A&A 641 A1 (2020), Table 5.
PEAKS = np.asarray([220.6, 538.1, 809.8, 1147.8, 1446.8, 1779.0, 2075.0])
SIGMA = np.asarray([0.6, 1.3, 1.0, 2.3, 1.6, 3.0, 8.0])
TROUGHS = np.asarray([416.3, 675.5, 1001.1, 1290.0, 1623.8, 1919.0, 2241.0])
HISTORICAL_LINE = 0.031


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def affine_fit(frequencies: np.ndarray) -> tuple[float, float, np.ndarray]:
    design = np.column_stack((frequencies, np.ones_like(frequencies)))
    scale, offset = np.linalg.lstsq(design, PEAKS, rcond=None)[0]
    return float(scale), float(offset), scale * frequencies + offset


def one_scale_fit(frequencies: np.ndarray) -> tuple[float, np.ndarray]:
    scale = float(np.dot(frequencies, PEAKS) / np.dot(frequencies, frequencies))
    return scale, scale * frequencies


def compare(row: dict[str, object], convention: str) -> dict[str, object]:
    wm = np.asarray(row["modes"]["-1"]["positive_omega"][:7], dtype=float)
    wp = np.asarray(row["modes"]["1"]["positive_omega"][:7], dtype=float)
    w0_positive = np.asarray(row["modes"]["0"]["positive_omega"][:7], dtype=float)
    if convention == "POSITIVE_ONLY":
        w0 = w0_positive
    elif convention == "ZERO_INCLUDED":
        if row["wall"] != "N" or not row["modes"]["0"]["exact_zero_mode"]:
            raise ValueError("zero-included convention requires the exact Neumann m=0 zero mode")
        w0 = np.r_[0.0, w0_positive[:6]]
    else:
        raise ValueError(convention)

    scale, offset, ell0 = affine_fit(w0)
    ellm = scale * wm + offset
    ellp = scale * wp + offset
    residual = ell0 - PEAKS
    fractional = residual / PEAKS
    one_scale, ell0_one = one_scale_fit(w0)
    one_fractional = (ell0_one - PEAKS) / PEAKS

    left = TROUGHS[:6]
    right = TROUGHS[1:]
    basin = np.minimum(PEAKS[1:] - left, right - PEAKS[1:])
    displacement = np.maximum(np.abs(ellm[1:] - ell0[1:]), np.abs(ellp[1:] - ell0[1:]))
    half_split = 0.5 * np.abs(ellp[1:] - ellm[1:])
    centered_margin = basin - displacement
    split_margin = basin - half_split
    actual_margin = np.minimum.reduce(
        (ellm[1:] - left, ellp[1:] - left, right - ellm[1:], right - ellp[1:])
    )
    centered = bool(np.all(centered_margin >= 0.0))
    splitting_small = bool(np.all(split_margin >= 0.0))
    actual = bool(np.all(actual_margin >= 0.0))
    if centered:
        morphology = "FULL_CENTERED_MULTIPLET_CONTAINMENT"
    elif splitting_small:
        morphology = "SPLITTING_ONLY"
    else:
        morphology = "BASIN_MISMATCH"
    max_fractional = float(np.max(np.abs(fractional)))
    return {
        "q_ratio": row["q_ratio"],
        "wall": row["wall"],
        "hbar": row["hbar"],
        "inv_n": row["inv_n"],
        "n": row["n"],
        "neumann_mode_convention": convention,
        "knob_count_continuous": 2,
        "omega_m0_compared": w0.tolist(),
        "omega_mminus_compared": wm.tolist(),
        "omega_mplus_compared": wp.tolist(),
        "affine_scale": scale,
        "affine_offset": offset,
        "m0_prediction": ell0.tolist(),
        "mminus_prediction": ellm.tolist(),
        "mplus_prediction": ellp.tolist(),
        "m0_residual": residual.tolist(),
        "m0_fractional_residual": fractional.tolist(),
        "m0_max_abs_fractional_residual": max_fractional,
        "m0_rms_fractional_residual": float(np.sqrt(np.mean(fractional**2))),
        "historical_ra2_line_met": bool(max_fractional <= HISTORICAL_LINE),
        "one_scale": one_scale,
        "one_scale_prediction": ell0_one.tolist(),
        "one_scale_max_abs_fractional_residual": float(np.max(np.abs(one_fractional))),
        "centered_displacement": displacement.tolist(),
        "half_split": half_split.tolist(),
        "centered_margin": centered_margin.tolist(),
        "split_margin": split_margin.tolist(),
        "actual_trough_margin": actual_margin.tolist(),
        "centered_contained": centered,
        "splitting_small": splitting_small,
        "actual_trough_contained": actual,
        "morphology": morphology,
        "central_n_witness": bool(centered and actual and max_fractional <= HISTORICAL_LINE),
        "pairing_caveat": (
            "same positive-root index carried only to reproduce the frozen FD1 diagnostic; "
            "the metric has not derived that m=0 and |m|=1 rows form an observational multiplet"
        ),
    }


def main() -> None:
    if sha256(PHASE1) != EXPECTED_PHASE1_HASH:
        raise SystemExit("frozen Phase-I hash mismatch")
    phase1 = json.loads(PHASE1.read_text(encoding="utf-8"))
    if not all(phase1["gates"].values()):
        raise SystemExit("Phase I gates are not all green")
    rows = []
    for row in phase1["rows"]:
        rows.append(compare(row, "POSITIVE_ONLY"))
        if row["wall"] == "N":
            rows.append(compare(row, "ZERO_INCLUDED"))

    gates = {
        "row_count": len(rows) == 6,
        "both_neumann_conventions": sum(row["neumann_mode_convention"] == "ZERO_INCLUDED" for row in rows) == 2,
        "no_component_removed": all(
            len(row[field]) == 7
            for row in rows
            for field in ("omega_m0_compared", "omega_mminus_compared", "omega_mplus_compared")
        ),
        "positive_affine_orientation": all(row["affine_scale"] > 0.0 for row in rows),
        "finite": all(
            np.all(np.isfinite(np.asarray(row[field], dtype=float)))
            for row in rows
            for field in ("m0_prediction", "mminus_prediction", "mplus_prediction")
        ),
        "morphology_exhaustive": all(
            row["morphology"] in {
                "FULL_CENTERED_MULTIPLET_CONTAINMENT", "SPLITTING_ONLY", "BASIN_MISMATCH"
            }
            for row in rows
        ),
    }
    survivors = [row for row in rows if row["central_n_witness"]]
    counts = {name: sum(row["morphology"] == name for row in rows) for name in {
        "FULL_CENTERED_MULTIPLET_CONTAINMENT", "SPLITTING_ONLY", "BASIN_MISMATCH"
    }}
    summary = {
        "comparison_row_count": len(rows),
        "morphology_counts": counts,
        "central_n_witness_count": len(survivors),
        "central_n_witness_identities": [
            [row["q_ratio"], row["wall"], row["hbar"], row["neumann_mode_convention"]]
            for row in survivors
        ],
        "minimum_m0_max_abs_fractional_residual": min(row["m0_max_abs_fractional_residual"] for row in rows),
        "maximum_m0_max_abs_fractional_residual": max(row["m0_max_abs_fractional_residual"] for row in rows),
        "minimum_one_scale_max_abs_fractional_residual": min(row["one_scale_max_abs_fractional_residual"] for row in rows),
        "inherited_four_witnesses_sustain_central_n": bool(survivors),
    }
    payload = {
        "phase": "UPSTREAM_CENTER_SPECTRUM_CORRECTION_PHASE2_ATTRIBUTED_READOUT",
        "source": {
            "citation": "Planck Collaboration, Planck 2018 Results I, A&A 641 A1 (2020), Table 5",
            "doi": "https://doi.org/10.1051/0004-6361/201833880",
            "peaks": PEAKS.tolist(),
            "sigma": SIGMA.tolist(),
            "troughs": TROUGHS.tolist(),
        },
        "phase1_sha256": sha256(PHASE1),
        "gates": gates,
        "summary": summary,
        "rows": rows,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(json.dumps(gates, indent=2, sort_keys=True))
    print(f"WROTE {OUTPUT}")
    if not all(gates.values()):
        raise SystemExit(f"failed gates: {[name for name, passed in gates.items() if not passed]}")


if __name__ == "__main__":
    main()

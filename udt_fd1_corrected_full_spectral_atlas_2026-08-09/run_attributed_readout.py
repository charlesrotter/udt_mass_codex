#!/usr/bin/env python3
"""Attributed full-atlas readout; historical pairing remains explicitly nonphysical."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
ATLAS = ROOT / "corrected_full_atlas_certified.json"
REFERENCE = REPO / "udt_freedata_FD2_profile_inversion_2026-08-09" / "center_spectrum_phase2.json"
OUTPUT = ROOT / "attributed_readout.json"
EXPECTED_ATLAS = "042138fb73cc9f3bef4faf97fc0357f2a2f079daced5e39d6532c4a6f770dfbb"
EXPECTED_REFERENCE = "a1d8c66091f2e7bf831ed54e28c2b68db9d5870ff73ddcd114b2bcc1cdba7722"
PEAKS = np.asarray([220.6, 538.1, 809.8, 1147.8, 1446.8, 1779.0, 2075.0])
SIGMA = np.asarray([0.6, 1.3, 1.0, 2.3, 1.6, 3.0, 8.0])
TROUGHS = np.asarray([416.3, 675.5, 1001.1, 1290.0, 1623.8, 1919.0, 2241.0])
HISTORICAL_LINE = 0.031


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def affine(frequencies: np.ndarray) -> dict[str, object]:
    design = np.column_stack((frequencies, np.ones_like(frequencies)))
    scale, offset = np.linalg.lstsq(design, PEAKS, rcond=None)[0]
    predicted = scale * frequencies + offset
    fractional = (predicted - PEAKS) / PEAKS
    one_scale = float(np.dot(frequencies, PEAKS) / np.dot(frequencies, frequencies))
    one_predicted = one_scale * frequencies
    return {
        "scale": float(scale),
        "offset": float(offset),
        "prediction": predicted.tolist(),
        "fractional_residual": fractional.tolist(),
        "max_abs_fractional_residual": float(np.max(np.abs(fractional))),
        "rms_fractional_residual": float(np.sqrt(np.mean(fractional**2))),
        "historical_3p1_line_met": bool(np.max(np.abs(fractional)) <= HISTORICAL_LINE),
        "one_scale": one_scale,
        "one_scale_prediction": one_predicted.tolist(),
        "one_scale_max_abs_fractional_residual": float(np.max(np.abs((one_predicted - PEAKS) / PEAKS))),
    }


def one_readout(row: dict[str, object], convention: str) -> dict[str, object]:
    positive = {
        "mminus": np.asarray(row["omega_mminus"], dtype=float),
        "m0": np.asarray(row["omega_m0"], dtype=float),
        "mplus": np.asarray(row["omega_mplus"], dtype=float),
    }
    compared = {name: values[:7] for name, values in positive.items()}
    if convention == "ZERO_INCLUDED":
        if row["wall"] != "N" or not row["neumann_m0_exact_zero_mode"]:
            raise ValueError("zero convention without exact Neumann zero")
        compared["m0"] = np.r_[0.0, positive["m0"][:6]]
    elif convention != "POSITIVE_ONLY":
        raise ValueError(convention)
    standalone = {name: affine(values) for name, values in compared.items()}

    m0_fit = standalone["m0"]
    scale, offset = float(m0_fit["scale"]), float(m0_fit["offset"])
    ell0 = np.asarray(m0_fit["prediction"])
    ellm = scale * compared["mminus"] + offset
    ellp = scale * compared["mplus"] + offset
    left, right = TROUGHS[:6], TROUGHS[1:]
    basin = np.minimum(PEAKS[1:] - left, right - PEAKS[1:])
    displacement = np.maximum(np.abs(ellm[1:] - ell0[1:]), np.abs(ellp[1:] - ell0[1:]))
    half_split = 0.5 * np.abs(ellp[1:] - ellm[1:])
    centered_margin = basin - displacement
    split_margin = basin - half_split
    actual_margin = np.minimum.reduce((ellm[1:] - left, ellp[1:] - left, right - ellm[1:], right - ellp[1:]))
    centered, split, actual = bool(np.all(centered_margin >= 0)), bool(np.all(split_margin >= 0)), bool(np.all(actual_margin >= 0))
    morphology = "FULL_CENTERED_MULTIPLET_CONTAINMENT" if centered else ("SPLITTING_ONLY" if split else "BASIN_MISMATCH")

    crowding: dict[str, list[int]] = {}
    all_positive = np.concatenate(tuple(positive.values()))
    for name, fit in standalone.items():
        projected = float(fit["scale"]) * all_positive + float(fit["offset"])
        crowding[name] = [int(np.count_nonzero((projected >= lo) & (projected <= hi))) for lo, hi in zip(left, right)]
    return {
        "inv_n": row["inv_n"], "n": row["n"], "q_ratio": row["q_ratio"], "q": row["q"],
        "hbar": row["hbar"], "wall": row["wall"], "neumann_mode_convention": convention,
        "standalone_families": standalone,
        "historical_pairing_diagnostic": {
            "m0_prediction": ell0.tolist(), "mminus_prediction": ellm.tolist(), "mplus_prediction": ellp.tolist(),
            "centered_margin": centered_margin.tolist(), "split_margin": split_margin.tolist(),
            "actual_trough_margin": actual_margin.tolist(), "centered_contained": centered,
            "splitting_small": split, "actual_trough_contained": actual, "morphology": morphology,
            "pairing_caveat": "same positive-root index is historical provenance only; no physical multiplet is derived",
        },
        "all_24_positive_line_crowding_by_anchor": crowding,
    }


def reference_difference(rows: list[dict[str, object]]) -> float:
    reference = json.loads(REFERENCE.read_text())
    maximum = 0.0
    for old in reference["rows"]:
        current = next(
            row for row in rows
            if float(row["inv_n"]) == float(old["inv_n"])
            and float(row["q_ratio"]) == float(old["q_ratio"])
            and float(row["hbar"]) == float(old["hbar"])
            and row["wall"] == old["wall"]
            and row["neumann_mode_convention"] == old["neumann_mode_convention"]
        )
        history = current["historical_pairing_diagnostic"]
        m0 = current["standalone_families"]["m0"]
        pairs = (
            (np.asarray(history["m0_prediction"]), np.asarray(old["m0_prediction"])),
            (np.asarray(history["mminus_prediction"]), np.asarray(old["mminus_prediction"])),
            (np.asarray(history["mplus_prediction"]), np.asarray(old["mplus_prediction"])),
            (np.asarray(m0["fractional_residual"]), np.asarray(old["m0_fractional_residual"])),
        )
        for new, prior in pairs:
            maximum = max(maximum, float(np.max(np.abs(new - prior) / np.maximum(1.0, np.abs(prior)))))
        if history["morphology"] != old["morphology"]:
            return float("inf")
    return maximum


def extrema(values: list[float]) -> dict[str, float]:
    array = np.asarray(values, dtype=float)
    return {
        "minimum": float(np.min(array)),
        "median": float(np.median(array)),
        "p95": float(np.quantile(array, 0.95)),
        "maximum": float(np.max(array)),
    }


def main() -> None:
    if digest(ATLAS) != EXPECTED_ATLAS or digest(REFERENCE) != EXPECTED_REFERENCE:
        raise SystemExit("frozen input hash mismatch")
    atlas = json.loads(ATLAS.read_text())
    spectral = [row for row in atlas["rows"] if float(row["hbar"]) > 0.0]
    rows: list[dict[str, object]] = []
    for row in spectral:
        rows.append(one_readout(row, "POSITIVE_ONLY"))
        if row["wall"] == "N":
            rows.append(one_readout(row, "ZERO_INCLUDED"))

    morphology = Counter(row["historical_pairing_diagnostic"]["morphology"] for row in rows)
    residuals: dict[str, list[float]] = defaultdict(list)
    line_met: dict[str, int] = Counter()
    crowd_values: dict[str, list[int]] = defaultdict(list)
    for row in rows:
        for family, fit in row["standalone_families"].items():
            residuals[family].append(float(fit["max_abs_fractional_residual"]))
            line_met[family] += int(fit["historical_3p1_line_met"])
        for anchor, counts in row["all_24_positive_line_crowding_by_anchor"].items():
            crowd_values[anchor].extend(counts)
    old_difference = reference_difference(rows)
    caveat_ok = all(
        "no physical multiplet" in row["historical_pairing_diagnostic"]["pairing_caveat"] for row in rows
    )
    gates = {
        "AR1_atlas_and_reference_hashes": True,
        "AR2_420_spectral_and_630_convention_rows": len(spectral) == 420 and len(rows) == 630,
        "AR3_both_neumann_conventions": sum(row["neumann_mode_convention"] == "ZERO_INCLUDED" for row in rows) == 210,
        "AR4_all_three_families": all(set(row["standalone_families"]) == {"mminus", "m0", "mplus"} for row in rows),
        "AR5_positive_finite_affine": all(
            float(fit["scale"]) > 0.0 and np.all(np.isfinite(np.asarray(fit["prediction"])))
            for row in rows for fit in row["standalone_families"].values()
        ),
        "AR6_pairing_caveat_carried": caveat_ok,
        "AR7_earlier_six_rows_reproduced": old_difference < 2.0e-9,
        "AR8_all_24_lines_counted": all(len(counts) == 6 for row in rows for counts in row["all_24_positive_line_crowding_by_anchor"].values()),
    }
    summary = {
        "spectral_identities": len(spectral),
        "convention_rows": len(rows),
        "historical_pairing_morphology_counts": dict(morphology),
        "standalone_max_abs_fractional_residual": {name: extrema(values) for name, values in residuals.items()},
        "standalone_historical_3p1_line_counts": dict(line_met),
        "line_crowding_counts_per_trough_basin": {name: extrema(values) for name, values in crowd_values.items()},
        "earlier_six_row_max_relative_difference": old_difference,
        "historical_pairing_is_not_physical_multiplet": True,
    }
    payload = {
        "phase": "ATTRIBUTED_FULL_CORRECTED_ATLAS_READOUT",
        "source": {
            "citation": "Planck Collaboration, Planck 2018 Results I, A&A 641 A1 (2020), Table 5",
            "doi": "https://doi.org/10.1051/0004-6361/201833880",
            "peaks": PEAKS.tolist(), "sigma": SIGMA.tolist(), "troughs": TROUGHS.tolist(),
        },
        "phase1_commit": "2ef02737",
        "atlas_sha256": EXPECTED_ATLAS,
        "gates": gates,
        "summary": summary,
        "rows": rows,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(json.dumps(gates, indent=2, sort_keys=True))
    print(f"WROTE {OUTPUT} SHA256 {digest(OUTPUT)}")
    if not all(gates.values()):
        raise SystemExit("attributed readout gate failed")


if __name__ == "__main__":
    main()

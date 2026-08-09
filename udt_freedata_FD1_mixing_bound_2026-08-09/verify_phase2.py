#!/usr/bin/env python3
"""Independent FD1 Phase-II existence audit after the boundary-location gate failed."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import numpy as np

import verify_phase1 as alt


ROOT = Path(__file__).resolve().parent
ATLAS = ROOT / "phase1_atlas_g240.json"
FAILED_BOUNDARY = ROOT / "phase2_transition_refinement_failed_boundary.json"
OUT = ROOT / "phase2_independent_verification.json"
PEAKS = np.array([220.6, 538.1, 809.8, 1147.8, 1446.8, 1779.0, 2075.0])
TROUGHS = np.array([416.3, 675.5, 1001.1, 1290.0, 1623.8, 1919.0, 2241.0])
INV_N_VALUES = (0.9658, 0.9470, 0.9284)
INSIDE = ((0.75, "D", 0.01), (0.75, "N", 0.01), (0.95, "D", 0.5), (0.95, "N", 0.5))
OUTSIDE = (
    (0.75, "D", 0.001), (0.75, "D", 0.05),
    (0.75, "N", 0.002), (0.75, "N", 0.05),
    (0.95, "D", 0.1), (0.95, "D", 1.0),
    (0.95, "N", 0.1), (0.95, "N", 1.0),
)
KEYS: dict[str, bool] = {}


def key(name: str, condition: bool) -> None:
    KEYS[name] = bool(condition)
    print(f"KEY {name}: {KEYS[name]}")


def row_identity(row: dict[str, object]) -> tuple[object, ...]:
    return row["n_label"], row["q_ratio"], row["wall"], row["hbar"]


def compare(wminus: np.ndarray, wzero: np.ndarray, wplus: np.ndarray) -> dict[str, object]:
    design = np.column_stack(((wzero[:7]), np.ones(7)))
    scale, offset = np.linalg.lstsq(design, PEAKS, rcond=None)[0]
    ell0 = scale * wzero[:7] + offset
    ellminus = scale * wminus[:7] + offset
    ellplus = scale * wplus[:7] + offset
    max_fractional = float(np.max(np.abs((ell0 - PEAKS) / PEAKS)))
    one_scale = float(np.dot(wzero[:7], PEAKS) / np.dot(wzero[:7], wzero[:7]))
    one_scale_max = float(np.max(np.abs((one_scale * wzero[:7] - PEAKS) / PEAKS)))
    left, right = TROUGHS[:6], TROUGHS[1:]
    basin = np.minimum(PEAKS[1:] - left, right - PEAKS[1:])
    centered = np.maximum(np.abs(ellplus[1:] - ell0[1:]), np.abs(ellminus[1:] - ell0[1:]))
    centered_margin = basin - centered
    absolute_margin = np.minimum.reduce((
        ellminus[1:] - left, ellplus[1:] - left, right - ellminus[1:], right - ellplus[1:]
    ))
    return {
        "affine_offset_spent": True,
        "affine_scale": float(scale),
        "affine_offset": float(offset),
        "affine_max_abs_fractional_residual": max_fractional,
        "one_scale_max_abs_fractional_residual": one_scale_max,
        "centered_margin": centered_margin.tolist(),
        "absolute_trough_margin": absolute_margin.tolist(),
        "centered_contained": bool(np.all(centered_margin >= 0.0)),
        "absolute_contained": bool(np.all(absolute_margin >= 0.0)),
        "historical_line_met": bool(max_fractional <= 0.031),
        "inside": bool(np.all(centered_margin >= 0.0) and max_fractional <= 0.031),
    }


def independent_record(row: dict[str, object], expected_inside: bool) -> dict[str, object]:
    geometry = alt.alternate_geometry(
        float(row["n"]), float(row["q"]), float(row["hbar"]), float(row["umin"]), 300
    )
    frequencies: dict[int, np.ndarray] = {}
    residuals = []
    drifts = []
    for m, field in ((-1, "omega_mminus"), (0, "omega_m0"), (1, "omega_mplus")):
        K, M, C = alt.alternate_matrices(geometry, m, str(row["wall"]))
        solved = []
        for mode in range(7):
            reference = float(row[field][mode])
            omega, residual = alt.nonlinear_frequency(K, M, C, m, mode, reference)
            solved.append(omega)
            residuals.append(residual)
            drifts.append(abs(omega / reference - 1.0))
        frequencies[m] = np.asarray(solved)
    comparison = compare(frequencies[-1], frequencies[0], frequencies[1])
    return {
        "identity": row_identity(row),
        "expected_inside": expected_inside,
        "comparison": comparison,
        "maximum_frequency_drift_from_g240": max(drifts),
        "maximum_raw_backward_residual": max(residuals),
        "frequencies": {str(m): values.tolist() for m, values in frequencies.items()},
    }


def validate(records: list[dict[str, object]], metadata: dict[str, object]) -> bool:
    expected_count = 3 * (len(INSIDE) + len(OUTSIDE))
    identities = [tuple(record["identity"]) for record in records]
    if len(records) != expected_count or len(set(identities)) != expected_count:
        return False
    if metadata.get("boundary_gate_status") != "FAILED_PRESERVED":
        return False
    for record in records:
        comparison = record.get("comparison", {})
        if comparison.get("affine_offset_spent") is not True:
            return False
        if bool(comparison.get("inside")) != bool(record.get("expected_inside")):
            return False
        if record.get("expected_inside"):
            if comparison.get("absolute_contained") is not True:
                return False
            if float(comparison.get("one_scale_max_abs_fractional_residual", 0.0)) <= 0.20:
                return False
    return True


def main() -> None:
    atlas = json.loads(ATLAS.read_text(encoding="utf-8"))
    failed = json.loads(FAILED_BOUNDARY.read_text(encoding="utf-8"))
    atlas_rows = {row_identity(row): row for row in atlas["rows"]}
    key("FD1_IV1_failed_boundary_preserved", failed["keys"]["FD1_R2_boundary_grid_convergence"] is False)
    key("FD1_IV2_endpoint_controls_survived", failed["keys"]["FD1_R3_endpoint_orientation"] is True)

    records = []
    for expected_inside, witnesses in ((True, INSIDE), (False, OUTSIDE)):
        for q_ratio, wall, hbar in witnesses:
            for inv_n in INV_N_VALUES:
                identity = (f"inv_n={inv_n:.4f}", q_ratio, wall, hbar)
                records.append(independent_record(atlas_rows[identity], expected_inside))

    max_drift = max(record["maximum_frequency_drift_from_g240"] for record in records)
    max_residual = max(record["maximum_raw_backward_residual"] for record in records)
    inside_records = [record for record in records if record["expected_inside"]]
    outside_records = [record for record in records if not record["expected_inside"]]
    metadata = {"boundary_gate_status": "FAILED_PRESERVED", "affine_offset_caveat": True}
    key("FD1_IV3_independent_inside", len(inside_records) == 12 and all(r["comparison"]["inside"] for r in inside_records))
    key("FD1_IV4_independent_outside", len(outside_records) == 24 and not any(r["comparison"]["inside"] for r in outside_records))
    key("FD1_IV5_frequency_agreement", max_drift < 0.03)
    key("FD1_IV6_raw_backward_residual", max_residual < 1.0e-8)
    key("FD1_IV7_absolute_trough_containment", all(r["comparison"]["absolute_contained"] for r in inside_records))
    key("FD1_IV8_one_scale_mismatch_disclosed", all(
        r["comparison"]["one_scale_max_abs_fractional_residual"] > 0.20 for r in inside_records
    ))
    key("FD1_IV9_record_schema", validate(records, metadata))

    mutations = []
    duplicate = copy.deepcopy(records); duplicate.append(copy.deepcopy(duplicate[0]))
    mutations.append(("duplicate_witness", not validate(duplicate, metadata)))
    missing = copy.deepcopy(records[:-1])
    mutations.append(("missing_witness", not validate(missing, metadata)))
    no_offset = copy.deepcopy(records); no_offset[0]["comparison"]["affine_offset_spent"] = False
    mutations.append(("lost_offset_disclosure", not validate(no_offset, metadata)))
    promoted = copy.deepcopy(records); promoted[12]["comparison"]["inside"] = True
    mutations.append(("promoted_outside", not validate(promoted, metadata)))
    erased_one_scale = copy.deepcopy(records); erased_one_scale[0]["comparison"]["one_scale_max_abs_fractional_residual"] = 0.01
    mutations.append(("erased_one_scale_mismatch", not validate(erased_one_scale, metadata)))
    erased_failure = copy.deepcopy(metadata); erased_failure["boundary_gate_status"] = "PASSED"
    mutations.append(("erased_boundary_failure", not validate(records, erased_failure)))
    key("FD1_IV10_catch_proofs", all(passed for _, passed in mutations))

    payload = {
        "phase": "FD1_PHASE2_INDEPENDENT_EXISTENCE_AUDIT",
        "keys": KEYS,
        "metadata": metadata,
        "summary": {
            "inside_records": len(inside_records),
            "outside_records": len(outside_records),
            "maximum_frequency_drift_from_g240": max_drift,
            "maximum_raw_backward_residual": max_residual,
            "minimum_inside_affine_margin_to_3p1pct": min(
                0.031 - r["comparison"]["affine_max_abs_fractional_residual"] for r in inside_records
            ),
            "minimum_inside_centered_margin": min(
                min(r["comparison"]["centered_margin"]) for r in inside_records
            ),
            "minimum_inside_one_scale_mismatch": min(
                r["comparison"]["one_scale_max_abs_fractional_residual"] for r in inside_records
            ),
            "boundary_locations_certified": False,
        },
        "records": records,
        "catch_proofs": [{"name": name, "rejected": passed} for name, passed in mutations],
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"WROTE {OUT}")
    print(f"TOTAL KEYS {sum(KEYS.values())}/{len(KEYS)}")
    if not all(KEYS.values()):
        raise SystemExit(f"failed keys: {[name for name, passed in KEYS.items() if not passed]}")


if __name__ == "__main__":
    main()

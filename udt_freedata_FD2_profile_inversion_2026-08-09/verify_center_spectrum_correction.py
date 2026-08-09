#!/usr/bin/env python3
"""Independent saved-artifact verification for the center-spectrum correction."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.special import jn_zeros


ROOT = Path(__file__).resolve().parent
PHASE1 = ROOT / "center_spectrum_phase1.json"
PHASE2 = ROOT / "center_spectrum_phase2.json"
OUTPUT = ROOT / "center_spectrum_verification.json"
EXPECTED_PHASE1 = "8fe6c747b5f2629e6fbd4ddb44bd40452d39052a71adc1aa46cfbad1771ae567"
PEAKS = np.asarray([220.6, 538.1, 809.8, 1147.8, 1446.8, 1779.0, 2075.0])
TROUGHS = np.asarray([416.3, 675.5, 1001.1, 1290.0, 1623.8, 1919.0, 2241.0])


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def phase1_errors(payload: dict[str, object]) -> list[str]:
    errors = []
    if payload.get("phase") != "UPSTREAM_CENTER_SPECTRUM_CORRECTION_PHASE1_BLIND":
        errors.append("wrong phase")
    if payload.get("observational_peak_values_loaded") is not False:
        errors.append("observational disclosure")
    if not all(payload.get("gates", {}).values()):
        errors.append("failed gate")
    rows = payload.get("rows", [])
    if len(rows) != 4:
        errors.append("row count")
    identities = [(row.get("q_ratio"), row.get("wall"), row.get("hbar")) for row in rows]
    if len(set(identities)) != len(identities):
        errors.append("duplicate identity")
    zero_count = 0
    for row in rows:
        modes = row.get("modes", {})
        if set(modes) != {"-1", "0", "1"}:
            errors.append("channel set")
            continue
        for m in ("-1", "0", "1"):
            values = np.asarray(modes[m].get("positive_omega", []), dtype=float)
            if len(values) != 7 or not np.all(values > 0.0) or not np.all(np.diff(values) > 0.0):
                errors.append("positive sequence")
            collocation = modes[m].get("collocation", [])
            if len(collocation) != 7 or not all(item.get("success") for item in collocation):
                errors.append("collocation")
        exact = bool(modes["0"].get("exact_zero_mode"))
        if row.get("wall") == "N":
            zero_count += int(exact)
        elif exact:
            errors.append("Dirichlet zero claim")
    if zero_count != 2:
        errors.append("Neumann zero count")
    return errors


def independent_compare(row: dict[str, object], convention: str) -> dict[str, object]:
    wminus = np.asarray(row["modes"]["-1"]["positive_omega"], dtype=float)
    wplus = np.asarray(row["modes"]["1"]["positive_omega"], dtype=float)
    wzero = np.asarray(row["modes"]["0"]["positive_omega"], dtype=float)
    if convention == "ZERO_INCLUDED":
        wzero = np.r_[0.0, wzero[:6]]
    design = np.column_stack((wzero[:7], np.ones(7)))
    scale, offset = np.linalg.solve(design.T @ design, design.T @ PEAKS)
    e0 = scale * wzero[:7] + offset
    em = scale * wminus[:7] + offset
    ep = scale * wplus[:7] + offset
    basin = np.minimum(PEAKS[1:] - TROUGHS[:6], TROUGHS[1:] - PEAKS[1:])
    displacement = np.maximum(np.abs(em[1:] - e0[1:]), np.abs(ep[1:] - e0[1:]))
    half_split = 0.5 * np.abs(ep[1:] - em[1:])
    actual = np.minimum.reduce(
        (em[1:] - TROUGHS[:6], ep[1:] - TROUGHS[:6], TROUGHS[1:] - em[1:], TROUGHS[1:] - ep[1:])
    )
    centered = bool(np.all(basin - displacement >= 0.0))
    splitting = bool(np.all(basin - half_split >= 0.0))
    morphology = "FULL_CENTERED_MULTIPLET_CONTAINMENT" if centered else (
        "SPLITTING_ONLY" if splitting else "BASIN_MISMATCH"
    )
    return {
        "scale": float(scale),
        "offset": float(offset),
        "max_fractional": float(np.max(np.abs((e0 - PEAKS) / PEAKS))),
        "centered": centered,
        "splitting": splitting,
        "actual": bool(np.all(actual >= 0.0)),
        "morphology": morphology,
    }


def phase2_errors(phase1: dict[str, object], phase2: dict[str, object]) -> tuple[list[str], list[dict[str, object]]]:
    errors = []
    if phase2.get("phase1_sha256") != EXPECTED_PHASE1:
        errors.append("phase1 hash")
    if phase2.get("source", {}).get("peaks") != PEAKS.tolist():
        errors.append("peak target")
    rows2 = phase2.get("rows", [])
    if len(rows2) != 6:
        errors.append("phase2 row count")
    by_identity = {
        (row["q_ratio"], row["wall"], row["hbar"]): row for row in phase1["rows"]
    }
    replay = []
    for saved in rows2:
        identity = (saved["q_ratio"], saved["wall"], saved["hbar"])
        if identity not in by_identity:
            errors.append("unknown identity")
            continue
        recomputed = independent_compare(by_identity[identity], saved["neumann_mode_convention"])
        replay.append({"identity": [*identity, saved["neumann_mode_convention"]], **recomputed})
        if recomputed["morphology"] != saved["morphology"]:
            errors.append("morphology mismatch")
        if recomputed["centered"] != saved["centered_contained"]:
            errors.append("centered mismatch")
        if recomputed["actual"] != saved["actual_trough_contained"]:
            errors.append("actual mismatch")
        if abs(recomputed["max_fractional"] - saved["m0_max_abs_fractional_residual"]) > 1.0e-10:
            errors.append("fractional mismatch")
    return errors, replay


def main() -> None:
    phase1 = json.loads(PHASE1.read_text(encoding="utf-8"))
    phase2 = json.loads(PHASE2.read_text(encoding="utf-8"))
    p1_errors = phase1_errors(phase1)
    p2_errors, replay = phase2_errors(phase1, phase2)

    analytic = phase1["analytic_controls"]
    analytic_check = {
        "j0_values_match_scipy": bool(np.allclose(analytic["dirichlet_exact_j0"], jn_zeros(0, 4), rtol=0.0, atol=1e-14)),
        "j1_values_match_scipy": bool(np.allclose(analytic["neumann_positive_exact_j1"], jn_zeros(1, 4), rtol=0.0, atol=1e-14)),
    }

    catches = []
    mutation = copy.deepcopy(phase1)
    mutation["rows"].append(copy.deepcopy(mutation["rows"][0]))
    catches.append(("duplicate_phase1_identity", bool(phase1_errors(mutation))))
    mutation = copy.deepcopy(phase1)
    mutation["rows"][1]["modes"]["0"]["exact_zero_mode"] = False
    catches.append(("missing_neumann_zero", bool(phase1_errors(mutation))))
    mutation = copy.deepcopy(phase1)
    mutation["rows"][0]["modes"]["1"]["positive_omega"].pop()
    catches.append(("missing_rotating_mode", bool(phase1_errors(mutation))))
    mutation = copy.deepcopy(phase1)
    mutation["observational_peak_values_loaded"] = True
    catches.append(("phase1_observational_leak", bool(phase1_errors(mutation))))
    mutation2 = copy.deepcopy(phase2)
    mutation2["source"]["peaks"][0] += 1.0
    catches.append(("changed_peak_target", bool(phase2_errors(phase1, mutation2)[0])))
    mutation2 = copy.deepcopy(phase2)
    mutation2["rows"][0]["morphology"] = "FULL_CENTERED_MULTIPLET_CONTAINMENT"
    catches.append(("forced_survivor", bool(phase2_errors(phase1, mutation2)[0])))

    gates = {
        "phase1_hash": sha256(PHASE1) == EXPECTED_PHASE1,
        "phase1_schema": not p1_errors,
        "phase2_independent_replay": not p2_errors,
        "analytic_controls": all(analytic_check.values()),
        "all_six_splitting_only": len(replay) == 6 and all(row["morphology"] == "SPLITTING_ONLY" for row in replay),
        "zero_centered_survivors": sum(row["centered"] for row in replay) == 0,
        "zero_actual_trough_survivors": sum(row["actual"] for row in replay) == 0,
        "catch_proofs": all(passed for _, passed in catches),
    }
    payload = {
        "phase": "CENTER_SPECTRUM_CORRECTION_INDEPENDENT_SAVED_ARTIFACT_REPLAY",
        "inputs": {PHASE1.name: sha256(PHASE1), PHASE2.name: sha256(PHASE2)},
        "phase1_errors": p1_errors,
        "phase2_errors": p2_errors,
        "analytic_check": analytic_check,
        "replay": replay,
        "catch_proofs": [{"name": name, "rejected": passed} for name, passed in catches],
        "gates": gates,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(gates, indent=2, sort_keys=True))
    print(json.dumps(payload["catch_proofs"], indent=2, sort_keys=True))
    print(f"WROTE {OUTPUT}")
    if not all(gates.values()):
        raise SystemExit(f"failed gates: {[name for name, passed in gates.items() if not passed]}")


if __name__ == "__main__":
    main()

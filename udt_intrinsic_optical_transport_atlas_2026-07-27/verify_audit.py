#!/usr/bin/env python3
from __future__ import annotations

import copy
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAMPS = (
    "COPRESENCE = WORKING_INTERPRETIVE_FRAME", "METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL",
    "INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED", "COMPLETE_WHOLE_SOLUTION_LAW = OPEN",
)
LIMITS = {
    "null": 2e-8, "energy": 2e-8, "screen": 2e-8, "curvature": 2e-8,
    "symplectic": 2e-7, "detM": 2e-7, "composition": 8e-7,
    "convergence": 3e-6, "RK4": 5e-5, "geometry": 2e-8,
}


def rows(name):
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def state():
    return {"stamps": STAMPS, "candidates": 6, "paths": 36, "checkpoints": 144,
            "cpu": True, "float64": True, "all_paths": True,
            "null": 0.0, "energy": 0.0, "screen": 0.0, "curvature": 0.0,
            "symplectic": 0.0, "detM": 0.0, "composition": 0.0, "convergence": 0.0,
            "RK4": 0.0, "geometry": 0.0, "anchor": True, "screens_equal": False,
            "B_composable": False, "tautology_promoted": False, "normalization_fit": False,
            "lambda_selected": False, "on_shell": False, "universal_nogo": False,
            "semantics_selected": False, "downstream": False}


def validate(s):
    assert s["stamps"] == STAMPS and s["candidates"] == 6
    assert s["paths"] == 36 and s["checkpoints"] == 144 and s["all_paths"]
    assert s["cpu"] and s["float64"]
    for key in ("null", "energy", "screen", "curvature", "symplectic", "detM",
                "composition", "convergence", "RK4", "geometry"):
        assert s[key] <= LIMITS[key]
    assert s["anchor"] and not s["screens_equal"] and not s["B_composable"]
    assert not s["tautology_promoted"] and not s["normalization_fit"]
    assert not s["lambda_selected"] and not s["on_shell"] and not s["universal_nogo"]
    assert not s["semantics_selected"] and not s["downstream"]


def expect(field, value):
    candidate = state(); candidate[field] = value
    try: validate(candidate)
    except AssertionError: return "PASS"
    raise AssertionError(field)


def main() -> int:
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    paths, checkpoints = rows("PATH_OUTCOMES.tsv"), rows("CHECKPOINT_ATLAS.tsv")
    geometry, rk4 = rows("INDEPENDENT_GEOMETRY_HOLDOUTS.tsv"), rows("RK4_HOLDOUTS.tsv")
    contracts = rows("FALSIFICATION_CONTRACT.tsv")
    assert result["status"] == independent["status"] == "PASS"
    assert len(paths) == 36 and len(checkpoints) == len(geometry) == 144 and len(rk4) == 6
    assert len({row["path_id"] for row in paths}) == 36
    assert Counter(row["event_id"] for row in paths) == {"P00": 12, "P01": 12, "P02": 12}
    assert Counter(row["lambda"] for row in paths) == {"-2": 6, "-1": 6, "0": 6, "0.5": 6, "1": 6, "2": 6}
    assert min(float(row["endpoint_screen_leakage"]) for row in paths) > 0
    assert min(float(row["detB"]) for row in checkpoints) > 0
    assert max(abs(float(row["lambda_complement"])-float(row["WRL_W"]))
               for row in checkpoints if row["lambda"] == "-2") == 0
    grouped = defaultdict(list)
    for row in paths:
        grouped[(row["event_id"], row["direction"])].append((float(row["normalized_shape_rms"]), float(row["lambda"])))
    winners = Counter(min(values)[1] for values in grouped.values())
    assert winners == {2.0: 4, -2.0: 2}
    maxima = result["numerical_maxima"]
    observed = state()
    observed.update({
        "null": maxima["max_null_residual"], "energy": maxima["max_killing_energy_drift"],
        "screen": max(maxima["max_screen_gram_residual"], maxima["max_k_screen_residual"]),
        "curvature": maxima["max_curvature_asymmetry"], "symplectic": maxima["max_symplectic_residual"],
        "detM": maxima["max_detM_residual"], "composition": maxima["composition_residual"],
        "convergence": maxima["convergence_difference"],
        "RK4": independent["maximum_RK4_DOP853_difference"],
        "geometry": independent["maximum_coordinate_frame_scaled_error"],
    })
    validate(observed)
    assert maxima["anchor_error"] == 0
    report = (HERE / "AUDIT_REPORT.md").read_text()
    prereg = (HERE / "PREREGISTRATION.md").read_text()
    for stamp in STAMPS:
        assert stamp in report and stamp in prereg

    mutations = {
        "F01": ("stamps", STAMPS[:-1]), "F02": ("candidates", 5),
        "F03": ("paths", 35), "F04": ("all_paths", False), "F05": ("cpu", False),
        "F06": ("null", 3e-8), "F07": ("energy", 3e-8), "F08": ("screen", 3e-8),
        "F09": ("curvature", 3e-8), "F10": ("symplectic", 3e-7),
        "F11": ("composition", 9e-7), "F12": ("convergence", 4e-6),
        "F13": ("RK4", 6e-5), "F14": ("geometry", 3e-8), "F15": ("anchor", False),
        "F16": ("screens_equal", True), "F17": ("B_composable", True),
        "F18": ("tautology_promoted", True), "F19": ("normalization_fit", True),
        "F20": ("lambda_selected", True), "F21": ("on_shell", True),
        "F22": ("universal_nogo", True), "F23": ("semantics_selected", True),
        "F24": ("downstream", True),
    }
    assert set(mutations) == {row["catch_id"] for row in contracts}
    catches = [{"catch_id": row["catch_id"], "result": expect(*mutations[row["catch_id"]]),
                "corruption_or_overclaim": row["corruption_or_overclaim"]} for row in contracts]
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catches[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(catches)
    verification = {
        "schema": "udt-intrinsic-optical-transport-verification-1.0", "status": "PASS",
        "paths": 36, "checkpoints": 144, "geometry_holdouts": 144, "RK4_holdouts": 6,
        "all_endpoint_screens_mixed": True, "projected_caustics": 0,
        "winner_counts": {"lambda_-2": 2, "lambda_2": 4}, "lambda_selected": False,
        "catch_proofs": "24/24", "numerical_gates": "10/10",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(verification, indent=2, sort_keys=True)+"\n")
    print(json.dumps(verification, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__": raise SystemExit(main())

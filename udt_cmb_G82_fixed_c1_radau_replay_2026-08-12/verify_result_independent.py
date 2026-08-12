#!/usr/bin/env python3
"""Independent saved-artifact verifier for the preregistered G82 Radau replay."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G81 = ROOT / "udt_cmb_G81_nonradial_screen_covariance_2026-08-12"
EXPECTED_MAXIMUM = "G81_C1_SCREEN_COVARIANCE_SURVIVES_ONE_FIXED_NON_DOP853_RADAU_REPLAY"
EXPECTED_SCIENCE = "DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS"
EXPECTED_AUTHORITY = (
    "one-control integrator-family replay only; no selector, physical profile, endpoint, scale, Xmax, "
    "SNe/CMB observable, cmb_temp, source, action, matter, bootstrap closure, signalling law, or future signal"
)
A_ROT = np.array([[3.0 / 5.0, -4.0 / 5.0], [4.0 / 5.0, 3.0 / 5.0]])
B_ROT = np.array([[5.0 / 13.0, -12.0 / 13.0], [12.0 / 13.0, 5.0 / 13.0]])


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def relative(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left - right) / max(1.0, np.linalg.norm(left), np.linalg.norm(right)))


def validate(payload: dict, manifest: list[dict[str, str]]) -> dict:
    assert payload["schema"] == "udt-cmb-g82-fixed-c1-radau-replay-v1"
    assert payload["status"] == "PASS"
    assert payload["maximum_conclusion_if_pass"] == EXPECTED_MAXIMUM
    assert payload["scientific_maximum_unchanged"] == EXPECTED_SCIENCE
    assert payload["authority_boundary"] == EXPECTED_AUTHORITY
    assert payload["method"]["integrator"] == "Radau"
    assert payload["method"]["rtol"] == 5.0e-11
    assert payload["method"]["atol"] == 5.0e-13
    assert payload["method"]["max_step"] == 1.0 / 512.0
    assert payload["gate"] == 2.0e-4
    assert payload["changed_from_g81"] == "integrator family only: Radau instead of DOP853"
    assert all(payload["extra_gates"].values())
    control = payload["control"]
    assert control["control_id"] == "C1_FULL_ANGULAR"
    assert control["status"] == "PASS" and all(control["gates"].values())
    assert payload["coarse_fine_max_relative"] < payload["gate"]

    source_rows = {row["path"]: row for row in manifest}
    assert len(source_rows) == len(manifest) == 6
    for path, row in source_rows.items():
        assert digest(ROOT / path) == row["sha256"]

    controls = rows(HERE / "CONTROL_UNIVERSE.tsv")
    assert len(controls) == 1 and controls[0]["control_id"] == "C1_FULL_ANGULAR"
    assert controls[0]["direction_er:direction_etheta:direction_epsi".split(":")[0]] == "12/13"
    assert (controls[0]["direction_etheta"], controls[0]["direction_epsi"]) == ("3/13", "4/13")
    assert controls[0]["integrator"] == "Radau"

    old = json.loads((G81 / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))["controls"][1]
    comparison = {}
    for key in ("forward_fine_D", "reverse_fine_D", "rotated_fine_D"):
        comparison[key] = relative(np.asarray(control[key]), np.asarray(old[key]))
        assert math.isclose(
            comparison[key], payload["radau_vs_dop853_matrix_relative"][key], rel_tol=2e-12, abs_tol=2e-15
        )
        assert comparison[key] < payload["gate"]

    forward = np.asarray(control["forward_fine_D"])
    reverse = np.asarray(control["reverse_fine_D"])
    rotated = np.asarray(control["rotated_fine_D"])
    z = float(control["Z"])
    unrotated_residual = relative(reverse, z * forward.T)
    rotated_residual = relative(rotated, z * B_ROT @ forward.T @ A_ROT.T)
    area_residual = abs(math.sqrt(abs(np.linalg.det(reverse))) / math.sqrt(abs(np.linalg.det(forward))) - z)
    assert math.isclose(unrotated_residual, control["independent_unrotated_reciprocity_relative"], rel_tol=2e-12, abs_tol=2e-15)
    assert math.isclose(rotated_residual, control["independent_rotated_covariance_relative"], rel_tol=2e-12, abs_tol=2e-15)
    assert math.isclose(area_residual, control["independent_area_ratio_minus_Z"], rel_tol=2e-12, abs_tol=2e-15)
    assert max(unrotated_residual, rotated_residual, area_residual) < payload["gate"]
    assert digest(HERE / "DERIVATION_RESULT.json") == digest(HERE / "DERIVATION_STDOUT.txt")
    return {
        "source_rows": len(source_rows),
        "controls": len(controls),
        "radau_vs_dop853_max_relative": max(comparison.values()),
        "recomputed_unrotated_residual": unrotated_residual,
        "recomputed_rotated_residual": rotated_residual,
        "recomputed_area_residual": area_residual,
    }


def main() -> None:
    payload = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    manifest = rows(HERE / "SOURCE_MANIFEST.tsv")
    evidence = validate(payload, manifest)
    result = {
        "schema": "udt-cmb-g82-independent-verification-v1",
        "status": "PASS",
        **evidence,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

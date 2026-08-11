#!/usr/bin/env python3
"""Fail-closed artifact, algebra, numerical, and scope verifier for G68."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def verify_payload(payload: dict, bundle: dict, profile_rows: list[dict[str, str]], preregistration: str) -> dict[str, bool]:
    checks: dict[str, bool] = {}
    require(payload["schema"] == "UDT_CMB_G68_FINITE_PATH_JACOBI_V1", "wrong result schema")
    require(payload["profile_rows"] == len(payload["profiles"]) == len(profile_rows) == 21, "profile missing or duplicated")
    registered_ids = [row["profile_id"] for row in profile_rows]
    result_ids = [row["profile_id"] for row in payload["profiles"]]
    require(result_ids == registered_ids and len(set(result_ids)) == 21, "profile ordering/universe changed")
    require(all(row["profile_status"] == "CHOSE_CONTROL" for row in profile_rows), "control profile promoted")
    require(sum(row["family"] == "F01" for row in payload["profiles"]) == 3, "F01 count changed")
    require(sum(row["family"] == "F02" for row in payload["profiles"]) == 18, "F02 count changed")
    checks["G01_profile_universe"] = True

    require(payload["status_counts"] == {"ENDPOINT_REGULAR_NO_CAUSTIC": 21}, "outcome census changed or filtered")
    require(all(row["endpoint_reached"] and not row["turning_events"] and row["first_caustic_affine"] is None for row in payload["profiles"]), "endpoint/turning/caustic ledger inconsistent")
    checks["G05_outcome_census"] = True

    thresholds = {
        "null": 2.0e-8,
        "screen_gram": 2.0e-8,
        "screen_ray": 2.0e-8,
        "wronskian": 2.0e-7,
        "tidal_antisymmetry": 2.0e-8,
        "conserved_p_t": 2.0e-8,
        "conserved_p_psi": 2.0e-8,
    }
    for key, limit in thresholds.items():
        require(max(row["residuals"][key] for row in payload["profiles"]) <= limit, f"residual failed: {key}")
    require(min(row["residuals"]["min_A"] for row in payload["profiles"]) > 0.0, "A regularity lost")
    require(min(row["residuals"]["min_block_D"] for row in payload["profiles"]) > 0.0, "t-psi block regularity lost")
    checks["G06_G07_geometry_residuals"] = True

    require(max(row["convergence"]["production_refined_D_relative"] for row in payload["profiles"]) <= 2.0e-7, "production/refined D failed")
    require(max(row["convergence"]["refined_second_D_relative"] for row in payload["profiles"]) <= 2.0e-6, "second-method D failed")
    checks["G08_method_convergence"] = True

    for row in payload["profiles"]:
        D = np.asarray(row["endpoint_D"], dtype=float)
        require(abs(float(np.linalg.det(D)) - row["det_D"]) <= 2.0e-14, f"determinant mismatch: {row['profile_id']}")
        require(np.linalg.norm(0.5 * (D - D.T)) <= 2.0e-8, f"endpoint antisymmetry exceeds gate: {row['profile_id']}")
        require(abs(row["polar_rotation"]) <= 2.0e-8, f"endpoint rotation exceeds observed zero class: {row['profile_id']}")
    checks["finite_map_internal_algebra"] = True

    for row in payload["profiles"]:
        if row["family"] != "F01":
            continue
        A_start = 1.0 + row["lapse_a"] * 0.25**2
        exact_s = 0.75 / math.sqrt(A_start)
        exact_D = exact_s * np.eye(2)
        require(abs(row["affine_final"] - exact_s) <= 2.0e-12, f"F01 affine mismatch: {row['profile_id']}")
        require(np.linalg.norm(np.asarray(row["endpoint_D"]) - exact_D) <= 2.0e-12, f"F01 D mismatch: {row['profile_id']}")
        require(row["F01_exact_D_relative"] <= 2.0e-8, f"F01 registered exact gate failed: {row['profile_id']}")
    checks["G10_F01_exact"] = True

    reflection = payload["reflection_checks"]
    require(len(reflection) == 18, "reflection universe changed")
    require(max(row["coordinate_reflection_max_absolute"] for row in reflection.values()) <= 2.0e-8, "coordinate reflection failed")
    require(max(row["D_conjugation_relative"] for row in reflection.values()) <= 2.0e-8, "D reflection failed")
    require(all(row["negative_endpoint_reached"] for row in reflection.values()), "negative-mixing endpoint missing")
    checks["G11_reflection"] = True

    epsilon = payload["epsilon_limit_checks"]
    require(len(epsilon) == 9, "epsilon-limit universe changed")
    require(all(row["nonincrease_or_below_floor"] for row in epsilon), "epsilon limit failed")
    require(all([control["epsilon"] for control in row["controls"]] == [1.0e-2, 5.0e-3] for row in epsilon), "epsilon values changed")
    checks["epsilon_limit"] = True

    require(bundle["schema"] == "UDT_CMB_G68_GEODESIC_BUNDLE_VERIFY_V1", "wrong bundle schema")
    require(bundle["profile_rows"] == len(bundle["rows"]) == 21, "bundle universe incomplete")
    require([row["profile_id"] for row in bundle["rows"]] == registered_ids, "bundle profile ordering changed")
    require(bundle["passed"] and bundle["max_fine_reference_relative"] <= 2.0e-4, "bundle/Jacobi check failed")
    require(bundle["max_coarse_fine_relative"] < 2.0e-4, "bundle delta convergence failed")
    require("no Riemann or Jacobi integration" in bundle["method"], "bundle method is not independent of Jacobi assembly")
    checks["G09_bundle_verification"] = True

    f01 = {row["lapse_a"]: row for row in payload["profiles"] if row["family"] == "F01"}
    area_changes = []
    anisotropies = []
    for row in payload["profiles"]:
        if row["family"] != "F02":
            continue
        D = np.asarray(row["endpoint_D"])
        area_changes.append(row["det_D"] / f01[row["lapse_a"]]["det_D"] - 1.0)
        anisotropies.append((D[0, 0] - D[1, 1]) / (0.5 * (D[0, 0] + D[1, 1])))
    require(min(area_changes) < 0.0 < max(area_changes), "profile-dependent area sign census lost")
    require(max(anisotropies) > 0.0, "finite shear census lost")
    checks["profile_dependence_observed"] = True

    require("bounded slice of function space" in preregistration, "bounded-slice scope missing")
    require("not `X_max`" in preregistration and "or a physical CMB endpoint" in preregistration, "endpoint scope missing")
    require("no physical CMB profile" in payload["maximum_conclusion"], "physical profile promoted")
    require("no physical" not in payload["status_counts"], "invalid status type")
    checks["G12_G13_G14_scope"] = True
    return checks


def verify_documents(exact: str, report: str, completeness: str, lay: str) -> dict[str, bool]:
    """Fail closed if the bounded control result is semantically promoted."""
    checks: dict[str, bool] = {}
    required_exact = (
        "FINITE_PATH_CONTROL_ATLAS_REGULAR_WITH_PROFILE_DEPENDENCE",
        "LEAD_INDEPENDENTLY_REPRODUCED_PENDING_ADVERSARIAL_REVIEW",
        "not `X_max` or last scattering",
        "not a CMB prediction",
        "does not supply those objects",
    )
    require(all(token in exact for token in required_exact), "exact derivation scope/status changed")
    checks["semantic_exact_scope"] = True

    required_report = (
        "LEAD_INDEPENDENTLY_REPRODUCED_PENDING_ADVERSARIAL_REVIEW",
        "Fresh zero-context semantic review",
        "remains outstanding",
        "not a CMB prediction",
        "Do not select a control profile",
    )
    require(all(token in report for token in required_report), "audit report overstates the evidence")
    checks["semantic_report_scope"] = True

    required_completeness = (
        "no metric field equation",
        "no physical boundary completion",
        "no global topological sector classified",
        "no time-live\n   metric",
        "not enumerated",
        "**Stability:** not tested",
    )
    require(all(token in completeness for token in required_completeness), "completeness omission deleted")
    checks["semantic_completeness_scope"] = True

    require("controls, not candidate universes" in lay, "lay report promoted the control ensemble")
    require("source/state information" in lay, "lay report lost the source/state boundary")
    checks["semantic_lay_scope"] = True
    return checks


def verify_files() -> dict:
    source_rows = tsv(HERE / "SOURCE_MANIFEST.tsv")
    require(len(source_rows) == 7, "source manifest universe changed")
    for row in source_rows:
        require(sha256(ROOT / row["path"]) == row["sha256"], f"source hash changed: {row['path']}")

    profile_rows = tsv(HERE / "PROFILE_UNIVERSE.tsv")
    require(len(profile_rows) == 21 and len({row["profile_id"] for row in profile_rows}) == 21, "profile table invalid")
    require(all(row["profile_status"] == "CHOSE_CONTROL" for row in profile_rows), "control promoted")
    payload = json.loads((HERE / "FINITE_PATH_RESULT.json").read_text(encoding="utf-8"))
    bundle = json.loads((HERE / "BUNDLE_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    preregistration = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    checks = verify_payload(payload, bundle, profile_rows, preregistration)
    checks.update(
        verify_documents(
            (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8"),
            (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8"),
            (HERE / "COMPLETENESS_SCOPE.md").read_text(encoding="utf-8"),
            (HERE / "LAY_REPORT.md").read_text(encoding="utf-8"),
        )
    )
    checks["source_hashes"] = True

    atlas = tsv(HERE / "FINITE_PATH_ATLAS.tsv")
    reflection = tsv(HERE / "REFLECTION_ATLAS.tsv")
    epsilon = tsv(HERE / "EPSILON_LIMIT_ATLAS.tsv")
    require(len(atlas) == 21 and [row["profile_id"] for row in atlas] == [row["profile_id"] for row in profile_rows], "finite atlas mismatch")
    require(len(reflection) == 18 and len(epsilon) == 9, "auxiliary atlas mismatch")
    checks["rendered_atlases"] = True

    with np.load(HERE / "FINITE_PATH_SAMPLES.npz") as samples:
        require(len(samples.files) == 42, "sample key universe changed")
        for row in profile_rows:
            s = samples[row["profile_id"] + "__s"]
            state = samples[row["profile_id"] + "__state"]
            require(s.shape == (501,) and state.shape == (32, 501), f"sample shape changed: {row['profile_id']}")
            require(abs(s[0]) < 1.0e-15 and abs(state[1, -1] - 1.0) < 2.0e-10, f"sample endpoint changed: {row['profile_id']}")
    checks["raw_samples"] = True
    return {"checks": checks, "passed": len(checks), "total": len(checks)}


def main() -> None:
    result = verify_files()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(rendered, encoding="utf-8")
    (HERE / "PACKAGE_VERIFICATION_STDOUT.txt").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

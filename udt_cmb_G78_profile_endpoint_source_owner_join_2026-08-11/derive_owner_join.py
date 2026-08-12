#!/usr/bin/env python3
"""Derive the bounded G78 profile/endpoint/source ownership join."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "9a78af889321d84914ae5eb2c066da56bc957719"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_sources() -> list[dict[str, str]]:
    manifest = rows(HERE / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == 20
    assert len({row["path"] for row in manifest}) == 20
    for row in manifest:
        assert row["source_commit"] == BASE
        data = subprocess.check_output(["git", "show", f"{BASE}:{row['path']}"], cwd=ROOT)
        assert digest_bytes(data) == row["sha256"], row["path"]
    return manifest


def exact_scale_factorization() -> dict[str, object]:
    R, c_e, A, h, st = sp.symbols("R c_E A h sin_theta", positive=True, nonzero=True)
    dt_dtau = R / c_e
    original = {
        "tau_tau": -A * c_e**2 * dt_dtau**2,
        "x_x": R**2 / A,
        "theta_theta": R**2,
        "psi_psi_unit_x2": R**2,
        "tau_psi": 2 * R * c_e * h * st**2 * dt_dtau,
    }
    expected = {
        "tau_tau": -A,
        "x_x": 1 / A,
        "theta_theta": 1,
        "psi_psi_unit_x2": 1,
        "tau_psi": 2 * h * st**2,
    }
    checks = {key: sp.simplify(original[key] / R**2 - expected[key]) == 0 for key in original}
    assert all(checks.values())
    return {
        "substitution": "tau=c_E*t/R",
        "factorization": "ds^2=R^2*dSigma^2",
        "coefficient_checks": checks,
        "interpretation": "dimensionless_null_sky_relation_independent_of_constant_R_and_unit_calibration_cE",
        "non_implication": "does_not_make_UDT_scale_free_or_select_R_endpoint_or_Xmax",
    }


def exact_source_congruence() -> dict[str, object]:
    a, b, c, d, u, v, w = sp.symbols("a b c d u v w")
    D = sp.Matrix([[a, b], [c, d]])
    C_obs = sp.Matrix([[u, v], [v, w]])
    C_src = D.inv() * C_obs * D.inv().T
    residual = sp.simplify(D * C_src * D.T - C_obs)
    assert residual == sp.zeros(2)

    max_relative = 0.0
    minimum_source_eigenvalue = float("inf")
    controls = 0
    for k in range(1, 17):
        Dn = np.array([[1.0 + k / 19.0, (-1) ** k / 7.0], [k / 23.0, 0.8 + k / 31.0]])
        if abs(np.linalg.det(Dn)) < 0.1:
            continue
        B = np.array([[1.0 + k / 13.0, k / 29.0], [(-1) ** k / 11.0, 0.7 + k / 17.0]])
        Cn = B @ B.T + 0.2 * np.eye(2)
        source = np.linalg.solve(Dn, Cn) @ np.linalg.inv(Dn).T
        reconstructed = Dn @ source @ Dn.T
        relative = np.linalg.norm(reconstructed - Cn) / np.linalg.norm(Cn)
        max_relative = max(max_relative, float(relative))
        minimum_source_eigenvalue = min(minimum_source_eigenvalue, float(np.linalg.eigvalsh(source).min()))
        controls += 1
    assert controls == 16 and max_relative < 2e-15 and minimum_source_eigenvalue > 0
    return {
        "symbolic_residual_zero": True,
        "deterministic_controls": controls,
        "maximum_relative_residual": max_relative,
        "minimum_source_eigenvalue": minimum_source_eigenvalue,
        "interpretation": "invertible_geometry_transports_arbitrary_positive_definite_source_data_but_does_not_derive_it",
    }


def family_census() -> dict[str, object]:
    profiles = rows(ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/PROFILE_ATLAS.tsv")
    direct = rows(ROOT / "udt_cmb_G77_full_family_direct_christoffel_replay_2026-08-11/DIRECT_CHRISTOFFEL_ATLAS.tsv")
    assert len(profiles) == len(direct) == 591
    assert len({row["profile_id"] for row in profiles}) == 591
    assert {row["profile_id"] for row in profiles} == {row["profile_id"] for row in direct}
    nonzero = [row for row in profiles if row["shape_id"] != "ZERO"]
    zero = [row for row in profiles if row["shape_id"] == "ZERO"]
    assert len(nonzero) == 49 * 4 * 3 == 588 and len(zero) == 3
    classes: dict[str, int] = {}
    for row in direct:
        classes[row["direct_class"]] = classes.get(row["direct_class"], 0) + 1
        assert int(row["crossed_vertices"]) == 2562
        assert int(row["missing_vertices"]) == 0
        assert int(row["negative_faces"]) == 0
        assert int(row["negative_projected_face_maps"]) == 0
        assert int(row["near_area_1e2"]) == 0
        assert abs(float(row["degree"]) - 1.0) < 5e-15
    assert classes == {"STRONG_DIRECT_AGREEMENT": 590, "REGISTERED_DIRECT_AGREEMENT": 1}
    return {
        "profiles": len(profiles),
        "nonzero_profiles": len(nonzero),
        "zero_controls": len(zero),
        "direct_classes": classes,
        "sampled_degree_one": 591,
        "sampled_missing_or_orientation_defects": 0,
        "selector_rows_from_regular_topology": 0,
    }


def owner_routes() -> list[dict[str, str]]:
    return [
        {"route": "P_REGULARITY", "target": "PHYSICAL_PROFILE", "status": "OPEN_NO_OWNER", "evidence": "all_591_controls_survive_registered_center_signature_and_sampled_relation_gates", "blocker": "regularity_characterizes_the_control_family_but_supplies_no_physical_selection_rule"},
        {"route": "P_GLOBAL_RELATION", "target": "PHYSICAL_PROFILE", "status": "OPEN_NO_OWNER", "evidence": "all_591_sampled_relations_are_degree_one_orientation_preserving", "blocker": "relation_invariants_evaluate_each_supplied_profile_but_do_not_select_one"},
        {"route": "E_SCALE", "target": "PHYSICAL_ENDPOINT_OR_GLOBAL_SCALE", "status": "OPEN_NO_OWNER", "evidence": "tau_cE_t_over_R_gives_ds2_equals_R2_dSigma2", "blocker": "dimensionless_null_sky_relation_is_blind_to_constant_R_while_cE_remains_unit_calibration"},
        {"route": "E_SNE", "target": "PHYSICAL_ENDPOINT_OR_GLOBAL_SCALE", "status": "COMPATIBILITY_ANCHOR_ONLY", "evidence": "P1_is_r_of_phi_pair_with_observed_low_z_parameters", "blocker": "no_owned_map_from_P1_Rw_n_to_G75_A_q_or_control_endpoint"},
        {"route": "E_XMAX", "target": "PHYSICAL_ENDPOINT_OR_GLOBAL_SCALE", "status": "NECESSARY_REQUIREMENT_ONLY", "evidence": "finite_pair_separation_approaches_Xmax_only_at_divergent_depth", "blocker": "no_realization_identifies_control_x1_or_symbolic_R_with_Xmax"},
        {"route": "S_GEOMETRY", "target": "PHYSICAL_SOURCE_STATE", "status": "OPEN_NO_OWNER", "evidence": "invertible_response_has_exact_positive_definite_source_pullback", "blocker": "metric_transports_source_state_but_does_not_populate_shape_normalization_or_statistics"},
        {"route": "S_MULTICHANNEL", "target": "PHYSICAL_SOURCE_STATE", "status": "CONDITIONAL_IDENTIFIABILITY_ONLY", "evidence": "known_source_covariance_plus_independent_carry_separates_controls_in_G70", "blocker": "known_source_and_observable_carry_are_unowned_physical_premises"},
    ]


def dependency_edges() -> list[dict[str, str]]:
    return [
        {"source": "c_E", "target": "tau_coordinate", "relation": "calibrates_clock_to_ruler", "owner_status": "OBSERVED_FOUNDATIONAL_ANCHOR"},
        {"source": "R", "target": "metric", "relation": "overall_constant_scale_after_tau_substitution", "owner_status": "FREE_UNSELECTED"},
        {"source": "G75_profile", "target": "metric", "relation": "supplies_A_and_q_control_functions", "owner_status": "CHOSE_BOUNDED_CONTROL"},
        {"source": "observer_and_endpoint", "target": "relation_map", "relation": "supplies_query_domain_and_crossing", "owner_status": "PINNED_HISTORICAL_CONTROL"},
        {"source": "metric_plus_query", "target": "relation_map", "relation": "evaluates_null_sky_relation", "owner_status": "DERIVED_CONDITIONAL_ON_QUERY"},
        {"source": "relation_map", "target": "screen_response", "relation": "transports_source_channels", "owner_status": "DERIVED_CONDITIONAL_ON_QUERY"},
        {"source": "source_state", "target": "observed_sky", "relation": "is_pulled_back_and_transformed", "owner_status": "OPEN_NO_OWNER"},
        {"source": "SNe_P1", "target": "low_z_pair_relation", "relation": "conditional_compatibility_anchor", "owner_status": "OBSERVED_CONDITIONAL"},
        {"source": "X_max", "target": "physical_pair_realization", "relation": "necessary_asymptotic_gate", "owner_status": "WORKING_FOUNDATIONAL_FRAME"},
        {"source": "physical_query_or_global_completion", "target": "endpoint_and_profile", "relation": "missing_selection_map", "owner_status": "OPEN"},
        {"source": "native_source_law", "target": "source_state", "relation": "missing_population_map", "owner_status": "OPEN"},
    ]


def write_tsv(path: Path, data: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(data[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(data)


def main() -> None:
    manifest = verify_sources()
    family = family_census()
    scale = exact_scale_factorization()
    source = exact_source_congruence()
    routes = owner_routes()
    edges = dependency_edges()
    write_tsv(HERE / "OWNER_ROUTE_LEDGER.tsv", routes)
    write_tsv(HERE / "DEPENDENCY_GRAPH.tsv", edges)
    result = {
        "schema": "udt-cmb-g78-profile-endpoint-source-owner-join-v1",
        "status": "PASS",
        "landing": "NO_PHYSICAL_PROFILE_ENDPOINT_SCALE_OR_SOURCE_OWNER_IN_FROZEN_G78_UNIVERSE",
        "source_rows": len(manifest),
        "family": family,
        "scale_factorization": scale,
        "source_congruence": source,
        "route_status_counts": {status: sum(row["status"] == status for row in routes) for status in sorted({row["status"] for row in routes})},
        "owned_native_routes": sum(row["status"] == "OWNED_NATIVE" for row in routes),
        "next_gate": "derive_or_supply_one_complete_physical_query_global_completion_or_native_source_state_map_before_any_fit",
        "maximum_scope": "exact_twenty_source_ownership_audit_plus_frozen_591_profile_finite_mesh_census",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

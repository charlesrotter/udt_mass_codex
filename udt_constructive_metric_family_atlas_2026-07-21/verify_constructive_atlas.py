#!/usr/bin/env python3
"""Independent verifier for the constructive metric-family atlas.

This module does not import the atlas builder. One all-slot family is reconstructed
with SymPy and one curvature tensor is recomputed by a separately written contraction.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CLASSIFICATION = "CONSTRUCTIVE_ALL_SLOT_CONFIGURATION_FAMILIES_OBSERVED_IN_REGISTERED_LOCAL_REGIME"
MAXIMUM = "CONSTRUCTIVE_METRIC_CONFIGURATION_FAMILIES_CHARACTERIZED_NOT_DYNAMICAL_SOLUTIONS"
TOLERANCE = 2e-10
RANK_TOLERANCE = 1e-9
LAMBDAS = (-1.0, -0.5, 0.0, 0.5, 1.0)
POINT_IDS = tuple(f"P{i}" for i in range(8))
SOURCE_HASHES = {
    "UDT_NATIVE_ACTION_COLD_PACKET.md": "d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0",
    "udt_complete_metric_solution_space_map_2026-07-21/SHA256SUMS.txt": "1778e4dcfcf9ac0bd3574fb3ff5248f2990265fa40d0822ff964ac67c434ae38",
    "udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt": "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad",
    "udt_local_jet_atlas_p02_2026-07-21/SHA256SUMS.txt": "c56390eb26b80c54a3c3a09f4800086c8dbc00b5bfd40b2038e264e85bec8938",
    "udt_founded_constraint_atlas_p03_2026-07-21/SHA256SUMS.txt": "b0ec5cbb2be404084e1b1ed4eca98d53c9712a62cf1af0a48eb340b64467c3be",
    "udt_global_kinematic_assembly_p03g_2026-07-21/SHA256SUMS.txt": "62f9b3f33409b62fb841734e8a91e61d9b859247bf808c4a6cf3740b6a54b6c9",
    "udt_finite_cell_completion_atlas_2026-07-21/SHA256SUMS.txt": "56c5f36455ae1f89811f3b86db9455a39482510415e6a7f770d2e5ffaa4ed0c7",
}
TABLES = (
    "SOURCE_LINEAGE.tsv", "FAMILY_DEFINITIONS.tsv", "SAMPLE_POINTS.tsv", "DEPENDENCY_PROOF.tsv",
    "CONFIGURATION_OBSERVATIONS.tsv", "SECTOR_ACTIVITY.tsv", "PHI_ANGULAR_OBSERVATIONS.tsv", "SAMPLED_TANGENT_RANK.tsv",
    "DEFORMATION_INCIDENCE.tsv", "CSN_ORBIT_OBSERVATIONS.tsv", "GAUGE_ORBIT_CHECKS.tsv",
    "DEGENERACY_CLOSURE.tsv", "COVERAGE_LEDGER.tsv", "TEN_CRITERION_SCOPE.tsv",
    "ANTI_IMPOSITION_AUDIT.tsv",
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            h.update(block)
    return h.hexdigest()


def canonical_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def coefficient_exact(bank: int, field: int, term: int) -> sp.Rational:
    raw = ((bank + 2) * 11 + (field + 1) * 7 + (term + 1) * 5 + (bank + 1) * (field + term + 3)) % 19 - 9
    if raw == 0:
        raw = 1 if (bank + field + term) % 2 == 0 else -1
    denominator = 60 if term < 4 else 90 if term < 8 else 120
    return sp.Rational(raw, denominator)


def sympy_anchor() -> dict[str, np.ndarray]:
    coordinates = sp.symbols("x0:4", real=True)
    features = list(coordinates)
    features.extend(value**2 / 2 for value in coordinates)
    features.extend(coordinates[i] * coordinates[j] for i in range(4) for j in range(i + 1, 4))
    bank = 2
    deformation = sp.Rational(1, 2)
    base = tuple(sp.Rational(value) for value in ("0.08", "0.14", "-0.06", "0.12", "-0.09", "0.05", "0.11", "-0.07", "0.09", "0.04"))
    latent = []
    for field in range(10):
        polynomial = sum((coefficient_exact(bank, field, term) * feature for term, feature in enumerate(features)), sp.Integer(0))
        latent.append(base[field] + deformation * polynomial)
    a, b, c, d, e, f, a20, a30, a21, a31 = latent
    u, w, r, t = sp.exp(a), sp.exp(c), sp.exp(d), sp.exp(f)
    slots = sp.Matrix([
        -u**2, -u * b, w**2 - b**2,
        r**2, r * e, e**2 + t**2,
        a20, a30, a21, a31,
    ])
    coframe = sp.Matrix([
        [u, b, 0, 0],
        [0, w, 0, 0],
        [r * a20 + e * a30, r * a21 + e * a31, r, e],
        [t * a30, t * a31, 0, t],
    ])
    eta = sp.diag(-1, 1, 1, 1)
    metric = sp.simplify(coframe.T * eta * coframe)
    point = {coordinates[0]: sp.Rational(1, 5), coordinates[1]: sp.Rational(1, 6), coordinates[2]: -sp.Rational(1, 7), coordinates[3]: -sp.Rational(1, 8)}

    def values(vector: list[sp.Expr] | sp.Matrix) -> np.ndarray:
        return np.asarray([float(sp.N(item.subs(point), 18)) for item in list(vector)], dtype=float)

    slot_values = values(slots)
    slot_first = np.zeros((4, 10))
    slot_second = np.zeros((4, 4, 10))
    for k in range(4):
        slot_first[k] = values([sp.diff(item, coordinates[k]) for item in slots])
        for ell in range(4):
            slot_second[k, ell] = values([sp.diff(item, coordinates[k], coordinates[ell]) for item in slots])

    coframe_value = np.asarray(coframe.subs(point).evalf(18), dtype=float)
    coframe_first = np.zeros((4, 4, 4))
    coframe_second = np.zeros((4, 4, 4, 4))
    metric_value = np.asarray(metric.subs(point).evalf(18), dtype=float)
    metric_first = np.zeros((4, 4, 4))
    metric_second = np.zeros((4, 4, 4, 4))
    for k in range(4):
        coframe_first[k] = np.asarray(coframe.diff(coordinates[k]).subs(point).evalf(18), dtype=float)
        metric_first[k] = np.asarray(metric.diff(coordinates[k]).subs(point).evalf(18), dtype=float)
        for ell in range(4):
            coframe_second[k, ell] = np.asarray(coframe.diff(coordinates[k], coordinates[ell]).subs(point).evalf(18), dtype=float)
            metric_second[k, ell] = np.asarray(metric.diff(coordinates[k], coordinates[ell]).subs(point).evalf(18), dtype=float)
    latent_symbols = sp.symbols("z0:10", real=True)
    za, zb, zc, zd, ze, zf, za20, za30, za21, za31 = latent_symbols
    symbolic_slots = sp.Matrix([
        -sp.exp(2 * za), -sp.exp(za) * zb, sp.exp(2 * zc) - zb**2,
        sp.exp(2 * zd), sp.exp(zd) * ze, ze**2 + sp.exp(2 * zf),
        za20, za30, za21, za31,
    ])
    latent_jacobian = symbolic_slots.jacobian(sp.Matrix(latent_symbols))
    latent_values = {symbol: expression.subs(point) for symbol, expression in zip(latent_symbols, latent)}
    latent_jacobian_value = np.asarray(latent_jacobian.subs(latent_values).evalf(18), dtype=float)
    return {
        "slot_values": slot_values, "slot_first": slot_first, "slot_second": slot_second,
        "coframe": coframe_value, "coframe_first": coframe_first, "coframe_second": coframe_second,
        "metric": metric_value, "metric_first": metric_first, "metric_second": metric_second,
        "latent_jacobian": latent_jacobian_value,
    }


def independent_curvature(g: np.ndarray, dg: np.ndarray, ddg: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    inverse = np.linalg.inv(g)
    inverse_first = np.array([-inverse @ dg[k] @ inverse for k in range(4)])
    gamma = np.zeros((4, 4, 4))
    dgamma = np.zeros((4, 4, 4, 4))
    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                lowered = np.array([dg[mu, sigma, nu] + dg[nu, sigma, mu] - dg[sigma, mu, nu] for sigma in range(4)])
                gamma[rho, mu, nu] = 0.5 * inverse[rho] @ lowered
                for k in range(4):
                    derivative = np.array([ddg[k, mu, sigma, nu] + ddg[k, nu, sigma, mu] - ddg[k, sigma, mu, nu] for sigma in range(4)])
                    dgamma[k, rho, mu, nu] = 0.5 * (inverse_first[k, rho] @ lowered + inverse[rho] @ derivative)
    riemann_up = np.zeros((4, 4, 4, 4))
    for rho in range(4):
        for sigma in range(4):
            for mu in range(4):
                for nu in range(4):
                    riemann_up[rho, sigma, mu, nu] = (
                        dgamma[mu, rho, nu, sigma] - dgamma[nu, rho, mu, sigma]
                        + sum(gamma[rho, mu, lam] * gamma[lam, nu, sigma] - gamma[rho, nu, lam] * gamma[lam, mu, sigma] for lam in range(4))
                    )
    riemann_down = np.einsum("ar,rsuv->asuv", g, riemann_up)
    ricci = np.einsum("rsrn->sn", riemann_up)
    scalar = float(np.einsum("ab,ab", inverse, ricci))
    return riemann_down, ricci, scalar


def validate(result: dict, tables: dict[str, list[dict[str, str]]], raw: list[dict], *, rehash: bool, reconstruct: bool) -> list[str]:
    checks: list[str] = []

    def require(condition: bool, name: str) -> None:
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    require(result["schema"] == "udt-constructive-metric-family-atlas-1.0", "schema")
    require(result["status"] == "PASS" and result["classification"] == CLASSIFICATION, "classification")
    require(result["maximum_conclusion"] == MAXIMUM, "maximum")
    require(result["regular_configuration_records"] == 160 and result["unique_metric_jet_hashes"] == 129, "result_counts")
    require(result["coefficient_banks"] == 4 and result["deformation_values"] == 5 and result["sample_points"] == 8, "sample_design")
    require(result["all_ten_slots"] is True and result["all_four_coordinates_in_nonzero_deformations"] is True, "whole_local_frame")
    require(result["phi_branch"] == "C02_INDEPENDENT_SIGNED_FIELD_ONLY", "phi_scope")
    require(result["deformation_edges"] == 128 and result["gauge_checks"] == 3 and result["csn_orbit_records"] == 4, "aux_counts")
    require(result["degeneracy_closure_records"] == 20 and result["singular_closure_records_retained"] == 4, "closure_result")
    require(result["max_identity_residual"] < TOLERANCE, "identity_gate")
    require(result["dynamics_loaded"] is False and result["solutions_run"] == 0 and result["physical_evolution_claimed"] is False, "no_dynamics")
    require(result["compatibility_ranking_used"] is False and result["finite_exhaustiveness_claim"] is False and result["gpu_used"] is False, "authority_stop")
    require(result["evidence_grade"] == "VERIFIED_WITH_CAVEATS", "evidence_grade")
    require(result["sampled_tangent_rank_counts"] == {"0": 4, "1": 28, "4": 16, "5": 112}, "result_tangent_counts")
    require(result["sampled_parameter_count_per_bank"] == 5 and result["ten_amplitudes_independently_scanned"] is False, "shared_amplitude_scope")

    sources = tables["SOURCE_LINEAGE.tsv"]
    require(len(sources) == 7 and {row["path"]: row["sha256"] for row in sources} == SOURCE_HASHES, "source_registry")
    if rehash:
        require(all(digest(ROOT / path) == expected for path, expected in SOURCE_HASHES.items()), "source_rehash")

    families = tables["FAMILY_DEFINITIONS.tsv"]
    require(len(families) == 7 and sum(row["kind"] == "REGULAR_ALL_SLOT_SPLIT_COFRAME" for row in families) == 4, "families")
    points = tables["SAMPLE_POINTS.tsv"]
    require(len(points) == 8 and {row["point_id"] for row in points} == set(POINT_IDS), "points")
    dependency = tables["DEPENDENCY_PROOF.tsv"]
    require(len(dependency) == 44 and all(row["all_coordinate_coefficients_nonzero"] == "YES" for row in dependency), "dependencies")

    observations = tables["CONFIGURATION_OBSERVATIONS.tsv"]
    expected_ids = {f"B{bank}_L{index}_{point}" for bank in range(4) for index in range(5) for point in POINT_IDS}
    require(len(observations) == 160 and {row["configuration_id"] for row in observations} == expected_ids, "observation_id_census")
    require(len({row["configuration_id"] for row in observations}) == 160, "observation_unique")
    require(all(row["retained"] == "YES" and row["physical_merit"] == "NOT_EVALUATED" for row in observations), "no_merit_filter")
    require(all(row["inertia"] == "1,3,0" and int(row["latent_to_slot_rank"]) == 10 for row in observations), "regular_rank_ten")
    require(max(float(row["identity_residual"]) for row in observations) < TOLERANCE, "observation_identity")
    require(max(float(row["weyl_trace_residual"]) for row in observations) < TOLERANCE, "weyl_trace")
    require(len({row["metric_jet_sha256"] for row in observations}) == 129, "unique_metric_jets")
    require(Counter(int(row["sampled_tangent_rank"]) for row in observations) == Counter({0: 4, 1: 28, 4: 16, 5: 112}), "observation_tangent_counts")

    raw_by_id = {row["configuration_id"]: row for row in raw}
    require(len(raw) == 160 and len(raw_by_id) == 160 and set(raw_by_id) == expected_ids, "raw_census")
    observation_by_id = {row["configuration_id"]: row for row in observations}
    for config_id, row in raw_by_id.items():
        identity = {"slots": row["slot_values"], "slot_first": row["slot_first"], "slot_second": row["slot_second"], "phi": row["phi"]}
        metric = {"metric": row["metric"], "first": row["metric_first"], "second": row["metric_second"]}
        require(canonical_hash(identity) == row["configuration_sha256"] == observation_by_id[config_id]["configuration_sha256"], f"configuration_hash_{config_id}")
        require(canonical_hash(metric) == row["metric_jet_sha256"] == observation_by_id[config_id]["metric_jet_sha256"], f"metric_hash_{config_id}")
    if rehash:
        require(digest(HERE / "RAW_CONFIGURATION_JETS.jsonl") == result["raw_configuration_sha256"], "raw_file_hash")

    sectors = tables["SECTOR_ACTIVITY.tsv"]
    require(len(sectors) == 160 and {row["configuration_id"] for row in sectors} == expected_ids, "sector_census")
    nonzero_ids = {row["configuration_id"] for row in observations if float(row["deformation"]) != 0}
    zero_ids = expected_ids - nonzero_ids
    require(len(nonzero_ids) == 128 and len(zero_ids) == 32, "deformation_partition")
    sector_by_id = {row["configuration_id"]: row for row in sectors}
    active_fields = ("time_active", "depth_active", "angular2_active", "angular3_active")
    require(all(all(sector_by_id[config][field] == "YES" for field in active_fields) for config in nonzero_ids), "all_coordinate_activity")
    require(all(sector_by_id[config]["mixed_shift_values_active"] == "YES" and sector_by_id[config]["screen_offdiagonal_active"] == "YES" for config in expected_ids), "mixed_slots_live")
    require(all(sector_by_id[config]["dynamical_interpretation"] == "NONE_CONFIGURATION_ONLY" for config in expected_ids), "time_not_evolution")

    zero_rows = [observation_by_id[config] for config in zero_ids]
    nonzero_rows = [observation_by_id[config] for config in nonzero_ids]
    require(all(float(row["riemann_max_abs"]) <= RANK_TOLERANCE for row in zero_rows), "observed_flat_origins")
    require(all(int(row["ricci_rank"]) == 4 and int(row["curvature_operator_rank"]) == 6 for row in nonzero_rows), "observed_nonzero_full_ranks")
    require(all(int(row["shear_rank"]) == 2 and int(row["twist_rank"]) == 1 and float(row["mixed_curvature_max_abs"]) > RANK_TOLERANCE for row in nonzero_rows), "observed_nonzero_coupling")

    census = result["observed_census"]
    require(census["zero_deformation_records"] == 32 and census["zero_deformation_flat_curvature_records"] == 32, "census_zero")
    require(census["nonzero_deformation_records"] == 128 and census["nonzero_full_ricci_rank_records"] == 128 and census["nonzero_full_curvature_operator_rank_records"] == 128, "census_ranks")
    require(census["nonzero_shear_rank_two_records"] == 128 and census["nonzero_twist_rank_one_records"] == 128 and census["nonzero_mixed_curvature_records"] == 128, "census_coupling")
    require((census["phi_negative_records"], census["phi_near_zero_records"], census["phi_positive_records"]) == (54, 12, 94), "census_phi")
    require(
        (census["dphi_timelike_records"], census["dphi_zero_records"], census["dphi_nonzero_near_null_records"], census["dphi_spacelike_records"])
        == (18, 32, 0, 110),
        "census_dphi",
    )

    phi_rows = tables["PHI_ANGULAR_OBSERVATIONS.tsv"]
    require(len(phi_rows) == 160 and all(row["relation_inferred"] == "NONE_OBSERVATION_ONLY" for row in phi_rows), "phi_no_relation")
    tangent_rows = tables["SAMPLED_TANGENT_RANK.tsv"]
    require(len(tangent_rows) == 160 and {row["configuration_id"] for row in tangent_rows} == expected_ids, "tangent_census")
    require(Counter(int(row["sampled_tangent_rank"]) for row in tangent_rows) == Counter({0: 4, 1: 28, 4: 16, 5: 112}), "tangent_rank_distribution")
    require(all(row["abstract_latent_to_slot_rank"] == "10" and row["ten_amplitudes_independently_scanned"] == "NO" for row in tangent_rows), "tangent_scope_disclosed")
    require(all(
        row["sample_parameters"] == "lambda,x0,x1,x2,x3"
        and row["sample_parameter_count"] == "5"
        and row["interpretation"] == "CORRELATED_PATH_TANGENT_NOT_FULL_TEN_PARAMETER_SCAN"
        for row in tangent_rows
    ), "tangent_parameterization_scope")
    incidence = tables["DEFORMATION_INCIDENCE.tsv"]
    require(len(incidence) == 128 and len({row["path_id"] for row in incidence}) == 128, "incidence_count")
    require(all(row["compatibility_verdict"] == "NOT_ASSIGNED_OBSERVED_DEFORMATION_ONLY" for row in incidence), "no_compatibility_verdict")

    gauge = tables["GAUGE_ORBIT_CHECKS.tsv"]
    require(len(gauge) == 3 and all(row["counted_as_new_geometry"] == "NO" for row in gauge), "gauge_not_new")
    require(max(float(row[key]) for row in gauge for key in ("metric_tensor_residual", "curvature_tensor_residual", "scalar_residual")) < TOLERANCE, "gauge_residuals")
    csn = tables["CSN_ORBIT_OBSERVATIONS.tsv"]
    require(len(csn) == 4 and all(row["physical_representative_selected"] == "NO" for row in csn), "csn_no_selection")
    require(max(abs(float(row["determinant_ratio"]) - float(row["expected_determinant_ratio"])) for row in csn) < TOLERANCE, "csn_weight")

    closure = tables["DEGENERACY_CLOSURE.tsv"]
    require(len(closure) == 20 and len({(row["family_id"], row["parameter"]) for row in closure}) == 20, "closure_count")
    require(sum(int(row["rank"]) < 4 for row in closure) == 4 and all(row["retained"] == "YES" and row["merit"] == "NOT_EVALUATED" for row in closure), "closure_retained")
    require(any(int(row["rank"]) == 4 and row["inertia"] not in {"1,3,0", "3,1,0"} for row in closure), "other_signature_retained")

    coverage = tables["COVERAGE_LEDGER.tsv"]
    require(len(coverage) == 14 and all(row["status"] == "PASS" for row in coverage), "coverage")
    require(next(row for row in coverage if row["coverage_id"] == "C13")["required"] == "EXPLICIT_OPEN", "unbounded_remainder")
    criteria = tables["TEN_CRITERION_SCOPE.tsv"]
    require(len(criteria) == 10 and next(row for row in criteria if row["criterion"] == "FULL_EQUATIONS")["covered"] == "none solved", "equations_open")
    require(next(row for row in criteria if row["criterion"] == "STABILITY")["covered"] == "not entered", "stability_open")
    anti = tables["ANTI_IMPOSITION_AUDIT.tsv"]
    require(len(anti) == 15 and all(row["present"] == "ABSENT" for row in anti), "anti_imposition")

    if reconstruct:
        anchor = sympy_anchor()
        saved = raw_by_id["B2_L3_P3"]
        for key in ("slot_values", "slot_first", "slot_second", "coframe", "coframe_first", "coframe_second", "metric", "metric_first", "metric_second"):
            require(float(np.max(np.abs(anchor[key] - np.asarray(saved[key], dtype=float)))) < 3e-13, f"sympy_anchor_{key}")
        require(np.linalg.matrix_rank(anchor["latent_jacobian"], tol=RANK_TOLERANCE) == 10, "sympy_latent_rank")
        riemann, ricci, scalar = independent_curvature(anchor["metric"], anchor["metric_first"], anchor["metric_second"])
        require(float(np.max(np.abs(riemann - np.asarray(saved["riemann_down"])))) < 3e-13, "independent_riemann")
        require(float(np.max(np.abs(ricci - np.asarray(saved["ricci"])))) < 3e-13, "independent_ricci")
        require(abs(scalar - float(saved["observables"]["scalar_curvature"])) < 3e-13, "independent_scalar")
    return checks


def expect_failure(name: str, callback, catches: list[str]) -> None:
    try:
        callback()
    except (AssertionError, KeyError, ValueError, TypeError):
        catches.append(name)
        return
    raise AssertionError(f"mutation escaped: {name}")


def main() -> None:
    result = json.loads((HERE / "ATLAS_RESULT.json").read_text(encoding="utf-8"))
    tables = {name: tsv(HERE / name) for name in TABLES}
    raw = [json.loads(line) for line in (HERE / "RAW_CONFIGURATION_JETS.jsonl").read_text(encoding="utf-8").splitlines() if line]
    checks = validate(result, tables, raw, rehash=True, reconstruct=True)
    catches: list[str] = []

    def validate_mutated(result_value=result, table_value=tables, raw_value=raw):
        return validate(result_value, table_value, raw_value, rehash=False, reconstruct=False)

    for key, value in (
        ("classification", "PHYSICAL_SOLUTION_SELECTED"), ("maximum_conclusion", "UNIVERSE_DERIVED"),
        ("regular_configuration_records", 159), ("all_ten_slots", False),
        ("all_four_coordinates_in_nonzero_deformations", False), ("dynamics_loaded", True),
        ("solutions_run", 1), ("physical_evolution_claimed", True),
        ("compatibility_ranking_used", True), ("finite_exhaustiveness_claim", True),
        ("gpu_used", True), ("singular_closure_records_retained", 3),
        ("ten_amplitudes_independently_scanned", True),
    ):
        bad = copy.deepcopy(result); bad[key] = value
        expect_failure(f"result_{key}", lambda b=bad: validate(b, tables, raw, rehash=False, reconstruct=False), catches)

    def table_mutation(table: str, row: int, key: str, value: str, name: str) -> None:
        bad = copy.deepcopy(tables); bad[table][row][key] = value
        expect_failure(name, lambda: validate(result, bad, raw, rehash=False, reconstruct=False), catches)

    bad = copy.deepcopy(tables); bad["CONFIGURATION_OBSERVATIONS.tsv"].pop()
    expect_failure("missing_configuration", lambda: validate(result, bad, raw, rehash=False, reconstruct=False), catches)
    bad = copy.deepcopy(tables); bad["CONFIGURATION_OBSERVATIONS.tsv"][-1] = copy.deepcopy(bad["CONFIGURATION_OBSERVATIONS.tsv"][0])
    expect_failure("duplicate_configuration", lambda: validate(result, bad, raw, rehash=False, reconstruct=False), catches)
    table_mutation("CONFIGURATION_OBSERVATIONS.tsv", 0, "retained", "NO", "record_discarded")
    table_mutation("CONFIGURATION_OBSERVATIONS.tsv", 0, "physical_merit", "PREFERRED", "merit_filter")
    table_mutation("CONFIGURATION_OBSERVATIONS.tsv", 0, "latent_to_slot_rank", "9", "slot_rank_loss")
    table_mutation("CONFIGURATION_OBSERVATIONS.tsv", 0, "identity_residual", "1", "identity_failure")
    table_mutation("CONFIGURATION_OBSERVATIONS.tsv", 0, "weyl_trace_residual", "1", "weyl_trace_failure")
    table_mutation("SECTOR_ACTIVITY.tsv", 40, "time_active", "NO", "time_dropped")
    table_mutation("SECTOR_ACTIVITY.tsv", 40, "angular2_active", "NO", "angular_dropped")
    table_mutation("SECTOR_ACTIVITY.tsv", 40, "mixed_shift_values_active", "NO", "shift_dropped")
    table_mutation("SECTOR_ACTIVITY.tsv", 40, "screen_offdiagonal_active", "NO", "screen_shape_dropped")
    table_mutation("SECTOR_ACTIVITY.tsv", 40, "dynamical_interpretation", "PHYSICAL_EVOLUTION", "time_promoted")
    table_mutation("PHI_ANGULAR_OBSERVATIONS.tsv", 0, "relation_inferred", "PHI_FORCES_SHEAR", "phi_relation_invented")
    table_mutation("SAMPLED_TANGENT_RANK.tsv", 0, "ten_amplitudes_independently_scanned", "YES", "shared_lambda_hidden")
    table_mutation("SAMPLED_TANGENT_RANK.tsv", 0, "sampled_tangent_rank", "10", "sampled_rank_promoted")
    table_mutation("SAMPLED_TANGENT_RANK.tsv", 0, "sample_parameter_count", "10", "parameter_count_promoted")
    table_mutation("SAMPLED_TANGENT_RANK.tsv", 0, "sample_parameters", "a,b,c,d,e,f,A20,A30,A21,A31", "parameter_list_promoted")
    table_mutation("SAMPLED_TANGENT_RANK.tsv", 0, "interpretation", "FULL_TEN_PARAMETER_SCAN", "full_scan_interpretation_promoted")
    table_mutation("DEFORMATION_INCIDENCE.tsv", 0, "compatibility_verdict", "PREFERRED", "compatibility_ranked")
    table_mutation("GAUGE_ORBIT_CHECKS.tsv", 0, "counted_as_new_geometry", "YES", "gauge_double_count")
    table_mutation("GAUGE_ORBIT_CHECKS.tsv", 0, "scalar_residual", "1", "gauge_covariance_failure")
    table_mutation("CSN_ORBIT_OBSERVATIONS.tsv", 0, "physical_representative_selected", "YES", "csn_selected")
    table_mutation("CSN_ORBIT_OBSERVATIONS.tsv", 0, "expected_determinant_ratio", "0", "csn_weight_corrupt")
    table_mutation("DEGENERACY_CLOSURE.tsv", 2, "retained", "NO", "singular_discarded")
    table_mutation("DEGENERACY_CLOSURE.tsv", 2, "merit", "REJECTED", "singular_merit_filter")
    bad = copy.deepcopy(tables); bad["DEGENERACY_CLOSURE.tsv"].pop()
    expect_failure("closure_missing", lambda: validate(result, bad, raw, rehash=False, reconstruct=False), catches)
    bad = copy.deepcopy(tables); bad["COVERAGE_LEDGER.tsv"].pop()
    expect_failure("remainder_hidden", lambda: validate(result, bad, raw, rehash=False, reconstruct=False), catches)
    table_mutation("TEN_CRITERION_SCOPE.tsv", 2, "covered", "equations solved", "equations_promoted")
    table_mutation("TEN_CRITERION_SCOPE.tsv", 8, "covered", "stable", "stability_promoted")
    table_mutation("ANTI_IMPOSITION_AUDIT.tsv", 0, "present", "PRESENT", "target_loaded")
    table_mutation("DEPENDENCY_PROOF.tsv", 0, "all_coordinate_coefficients_nonzero", "NO", "coordinate_dependency_lost")
    bad = copy.deepcopy(tables); bad["SOURCE_LINEAGE.tsv"].pop()
    expect_failure("source_missing", lambda: validate(result, bad, raw, rehash=False, reconstruct=False), catches)

    bad_raw = list(raw[:-1])
    expect_failure("raw_missing", lambda: validate(result, tables, bad_raw, rehash=False, reconstruct=False), catches)
    bad_raw = copy.deepcopy(raw); bad_raw[0]["slot_values"][0] += 1.0
    expect_failure("raw_slot_mutation", lambda: validate(result, tables, bad_raw, rehash=False, reconstruct=False), catches)
    bad_raw = copy.deepcopy(raw); bad_raw[0]["metric_first"][0][0][0] += 1.0
    expect_failure("raw_metric_mutation", lambda: validate(result, tables, bad_raw, rehash=False, reconstruct=False), catches)

    verification = {
        "schema": "udt-constructive-metric-family-atlas-verification-1.0",
        "verdict": "PASS",
        "generator_imported": "NO",
        "independent_checks": len(checks),
        "catch_proofs": len(catches),
        "sympy_anchor": "B2_L3_P3",
        "independent_curvature_reconstruction": "PASS",
        "main_result_sha256": digest(HERE / "ATLAS_RESULT.json"),
        "raw_configuration_sha256": digest(HERE / "RAW_CONFIGURATION_JETS.jsonl"),
        "fresh_adversarial_context": "COMPLETE_VERIFIED_WITH_CAVEATS",
        "fresh_reviewer": "constructive_atlas_adversary",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "UDT_CONSTRUCTIVE_METRIC_FAMILY_ATLAS_VERIFICATION=PASS",
        f"independent_checks={len(checks)}",
        f"catch_proofs={len(catches)}",
        "generator_imported=NO",
        "sympy_anchor=B2_L3_P3",
        "independent_curvature_reconstruction=PASS",
        "records=160 unique_metric_jets=129",
        "all_ten_slots=YES all_four_coordinates=YES",
        "no_merit_filter=YES no_compatibility_ranking=YES",
        f"main_result_sha256={verification['main_result_sha256']}",
        f"raw_configuration_sha256={verification['raw_configuration_sha256']}",
        "fresh_adversarial_context=COMPLETE_VERIFIED_WITH_CAVEATS",
        "fresh_reviewer=constructive_atlas_adversary",
    ]
    (HERE / "VERIFICATION_TRANSCRIPT.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))


if __name__ == "__main__":
    main()

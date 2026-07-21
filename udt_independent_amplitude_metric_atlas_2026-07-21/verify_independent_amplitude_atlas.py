#!/usr/bin/env python3
"""Independent verifier for the eleven-control metric configuration atlas.

This script does not import the atlas builder or the preceding constructive builder. It reconstructs
the amplitude design, polynomial two-jets, one full symbolic parameter tangent, and one curvature
tensor with separately written code.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCHEMA = "udt-independent-amplitude-metric-atlas-1.0"
CLASSIFICATION = "INDEPENDENT_AMPLITUDE_CONFIGURATION_ATLAS_OBSERVED_IN_REGISTERED_LOCAL_REGIME"
MAXIMUM = "TEN_METRIC_AMPLITUDES_AND_PHI_VARIED_INDEPENDENTLY_WITHIN_REGISTERED_CONFIGURATION_DESIGN"
TOLERANCE = 2e-10
RANK_TOLERANCE = 1e-9
DIFFERENCE_STEP = 1e-6
HADAMARD_COLUMNS = (1, 2, 4, 8, 16, 3, 5, 6, 7, 9, 10)
PARAMETERS = tuple(f"alpha_{index}" for index in range(10)) + ("beta",)
BASE = (0.08, 0.14, -0.06, 0.12, -0.09, 0.05, 0.11, -0.07, 0.09, 0.04)
PHI_OFFSETS = (-0.25, 0.0, 0.25, 0.125)
POINTS = {
    "P0": (0.0, 0.0, 0.0, 0.0),
    "P1": (1 / 3, -1 / 4, 1 / 5, -1 / 6),
    "P2": (-1 / 4, 1 / 5, -1 / 6, 1 / 7),
    "P3": (1 / 5, 1 / 6, -1 / 7, -1 / 8),
    "P4": (-1 / 6, -1 / 7, 1 / 8, 1 / 9),
    "P5": (1 / 2, 0.0, -1 / 3, 1 / 4),
    "P6": (0.0, -1 / 2, 1 / 4, -1 / 3),
    "P7": (1 / 3, 1 / 3, 1 / 3, 1 / 3),
}
SCHEDULE = {0: ("P0", "P4"), 1: ("P1", "P5"), 2: ("P2", "P6"), 3: ("P3", "P7")}
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
SOURCE_HASHES = {
    "udt_constructive_metric_family_atlas_2026-07-21/SHA256SUMS.txt": "c851721f3e8e15768f8f4945151c0d78bde6f1186bbadcfce5066b939a645370",
    "udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt": "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad",
    "udt_independent_amplitude_metric_atlas_2026-07-21/PREREGISTRATION.md": "75e9b15d97b21ee4f7104b071340fd52e50044285c4dcf3415167ad54115b8d0",
    "udt_independent_amplitude_metric_atlas_2026-07-21/PREREGISTRATION_CORRECTION.md": "7042512e08b55d2305be22cf88d594b261968350ebe50c548d492a80c03a8029",
}
TABLES = (
    "SOURCE_LINEAGE.tsv",
    "AMPLITUDE_DESIGN.tsv",
    "SAMPLE_SCHEDULE.tsv",
    "PARAMETER_DEPENDENCY.tsv",
    "CONFIGURATION_OBSERVATIONS.tsv",
    "PARAMETER_TANGENT_RANKS.tsv",
    "DESIGN_FAMILY_CENSUS.tsv",
    "METRIC_AXIS_CENSUS.tsv",
    "PHI_DECOUPLING.tsv",
    "SECTOR_ACTIVITY.tsv",
    "COVERAGE_LEDGER.tsv",
    "TEN_CRITERION_SCOPE.tsv",
    "ANTI_IMPOSITION_AUDIT.tsv",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sylvester(order: int) -> np.ndarray:
    matrix = np.ones((1, 1), dtype=int)
    while matrix.shape[0] < order:
        matrix = np.block([[matrix, matrix], [matrix, -matrix]])
    return matrix


def coefficient(bank: int, field: int, term: int) -> float:
    raw = ((bank + 2) * 11 + (field + 1) * 7 + (term + 1) * 5 + (bank + 1) * (field + term + 3)) % 19 - 9
    if raw == 0:
        raw = 1 if (bank + field + term) % 2 == 0 else -1
    denominator = 60.0 if term < 4 else 90.0 if term < 8 else 120.0
    return raw / denominator


def feature_twojets(x: np.ndarray) -> list[np.ndarray]:
    features: list[np.ndarray] = []
    for coordinate in range(4):
        jet = np.zeros(21)
        jet[0] = x[coordinate]
        jet[1 + coordinate] = 1.0
        features.append(jet)
    for coordinate in range(4):
        jet = np.zeros(21)
        jet[0] = 0.5 * x[coordinate] ** 2
        jet[1 + coordinate] = x[coordinate]
        jet[5 + 4 * coordinate + coordinate] = 1.0
        features.append(jet)
    for first in range(4):
        for second in range(first + 1, 4):
            jet = np.zeros(21)
            jet[0] = x[first] * x[second]
            jet[1 + first] = x[second]
            jet[1 + second] = x[first]
            jet[5 + 4 * first + second] = 1.0
            jet[5 + 4 * second + first] = 1.0
            features.append(jet)
    return features


def polynomial_twojet(bank: int, field: int, x: np.ndarray) -> np.ndarray:
    return sum((coefficient(bank, field, term) * jet for term, jet in enumerate(feature_twojets(x))), np.zeros(21))


def latent_slot_jacobian(latent: np.ndarray) -> np.ndarray:
    a, b, c, d, e, f = latent[:6]
    u, w, r, t = np.exp(a), np.exp(c), np.exp(d), np.exp(f)
    matrix = np.zeros((10, 10))
    matrix[0, 0] = -2 * u**2
    matrix[1, 0] = -u * b
    matrix[1, 1] = -u
    matrix[2, 1] = -2 * b
    matrix[2, 2] = 2 * w**2
    matrix[3, 3] = 2 * r**2
    matrix[4, 3] = r * e
    matrix[4, 4] = r
    matrix[5, 4] = 2 * e
    matrix[5, 5] = 2 * t**2
    matrix[6:, 6:] = np.eye(4)
    return matrix


def symbolic_anchor() -> dict[str, np.ndarray]:
    x = sp.symbols("x0:4", real=True)
    alpha = sp.symbols("a0:10", real=True)
    beta = sp.symbols("beta", real=True)
    features = list(x)
    features.extend(value**2 / 2 for value in x)
    features.extend(x[first] * x[second] for first in range(4) for second in range(first + 1, 4))

    def exact_coefficient(field: int, term: int) -> sp.Rational:
        raw = ((0 + 2) * 11 + (field + 1) * 7 + (term + 1) * 5 + (0 + 1) * (field + term + 3)) % 19 - 9
        if raw == 0:
            raw = 1 if (field + term) % 2 == 0 else -1
        denominator = 60 if term < 4 else 90 if term < 8 else 120
        return sp.Rational(raw, denominator)

    polynomials = [
        sum((exact_coefficient(field, term) * feature for term, feature in enumerate(features)), sp.Integer(0))
        for field in range(11)
    ]
    latent = [sp.Rational(str(BASE[field])) + alpha[field] * polynomials[field] for field in range(10)]
    a, b, c, d, e, f, a20, a30, a21, a31 = latent
    u, w, r, t = sp.exp(a), sp.exp(c), sp.exp(d), sp.exp(f)
    slots = [
        -u**2,
        -u * b,
        w**2 - b**2,
        r**2,
        r * e,
        e**2 + t**2,
        a20,
        a30,
        a21,
        a31,
    ]
    phi = sp.Rational(-1, 4) + beta * polynomials[10]
    slot_jet = list(slots)
    slot_jet.extend(sp.diff(item, x[k]) for k in range(4) for item in slots)
    slot_jet.extend(sp.diff(item, x[k], x[ell]) for k in range(4) for ell in range(4) for item in slots)
    phi_jet = [phi]
    phi_jet.extend(sp.diff(phi, x[k]) for k in range(4))
    phi_jet.extend(sp.diff(phi, x[k], x[ell]) for k in range(4) for ell in range(4))
    substitutions = {symbol: sp.Integer(0) for symbol in (*x, *alpha, beta)}
    slot_values = np.array([float(sp.N(item.subs(substitutions), 18)) for item in slot_jet])
    phi_values = np.array([float(sp.N(item.subs(substitutions), 18)) for item in phi_jet])
    metric_tangent = np.array(
        [[float(sp.N(sp.diff(item, parameter).subs(substitutions), 18)) for parameter in alpha] for item in slot_jet]
    )
    combined = np.zeros((231, 11))
    combined[:210, :10] = metric_tangent
    combined[210:, :10] = np.array(
        [[float(sp.N(sp.diff(item, parameter).subs(substitutions), 18)) for parameter in alpha] for item in phi_jet]
    )
    combined[210:, 10] = np.array([float(sp.N(sp.diff(item, beta).subs(substitutions), 18)) for item in phi_jet])
    return {
        "slot_jet": slot_values,
        "phi_jet": phi_values,
        "metric_tangent": metric_tangent,
        "combined_tangent": combined,
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
                        dgamma[mu, rho, nu, sigma]
                        - dgamma[nu, rho, mu, sigma]
                        + sum(
                            gamma[rho, mu, lam] * gamma[lam, nu, sigma]
                            - gamma[rho, nu, lam] * gamma[lam, mu, sigma]
                            for lam in range(4)
                        )
                    )
    riemann_down = np.einsum("ar,rsuv->asuv", g, riemann_up)
    ricci = np.einsum("rsrn->sn", riemann_up)
    scalar = float(np.einsum("ab,ab", inverse, ricci))
    return riemann_down, ricci, scalar


def independent_split_ranks(slot_values: np.ndarray, slot_first: np.ndarray) -> tuple[int, int]:
    screen = np.array([[slot_values[3], slot_values[4]], [slot_values[4], slot_values[5]]])
    shifts = np.array([[slot_values[6], slot_values[8]], [slot_values[7], slot_values[9]]])
    screen_first = [
        np.array([[slot_first[k, 3], slot_first[k, 4]], [slot_first[k, 4], slot_first[k, 5]]])
        for k in range(4)
    ]
    shifts_first = [
        np.array([[slot_first[k, 6], slot_first[k, 8]], [slot_first[k, 7], slot_first[k, 9]]])
        for k in range(4)
    ]
    inverse = np.linalg.inv(screen)
    twist = np.zeros(2)
    for vertical in range(2):
        twist[vertical] = (
            shifts_first[0][vertical, 1]
            - shifts_first[1][vertical, 0]
            - sum(shifts[other, 0] * shifts_first[2 + other][vertical, 1] for other in range(2))
            + sum(shifts[other, 1] * shifts_first[2 + other][vertical, 0] for other in range(2))
        )
    shear_rows = []
    for base in range(2):
        horizontal = screen_first[base] - sum(
            shifts[vertical, base] * screen_first[2 + vertical] for vertical in range(2)
        )
        vertical_derivative = np.array(
            [[shifts_first[2 + derivative][output, base] for output in range(2)] for derivative in range(2)]
        )
        deformation = 0.5 * (horizontal - vertical_derivative @ screen - screen @ vertical_derivative.T)
        expansion = float(np.trace(inverse @ deformation))
        shear = deformation - 0.5 * expansion * screen
        shear_rows.append((shear[0, 0], shear[0, 1], shear[1, 1]))
    shear_rank = int(np.linalg.matrix_rank(np.asarray(shear_rows), tol=RANK_TOLERANCE))
    twist_rank = int(np.linalg.matrix_rank(twist.reshape(2, 1), tol=RANK_TOLERANCE))
    return shear_rank, twist_rank


def rank_text(rows: list[dict[str, str]], field: str) -> str:
    counts = Counter(int(row[field]) for row in rows)
    return ";".join(f"{rank}:{counts[rank]}" for rank in sorted(counts))


def validate(
    result: dict,
    tables: dict[str, list[dict[str, str]]],
    raw: list[dict],
    *,
    rehash: bool,
    reconstruct: bool,
) -> list[str]:
    checks: list[str] = []

    def require(condition: bool, name: str) -> None:
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    require(result["schema"] == SCHEMA and result["status"] == "PASS", "schema_status")
    require(result["classification"] == CLASSIFICATION and result["maximum_conclusion"] == MAXIMUM, "scope_classification")
    require(result["amplitude_design_rows"] == 60 and result["metric_amplitude_count"] == 10 and result["phi_amplitude_count"] == 1, "result_design_counts")
    require(result["metric_design_rank"] == 10 and result["combined_design_rank"] == 11, "result_design_ranks")
    require(result["hadamard_columns"] == list(HADAMARD_COLUMNS) and result["hadamard_rows_unique"] == 32, "corrected_hadamard_result")
    require(result["regular_configuration_records"] == 480, "result_configuration_count")
    require(result["complete_metric_tangent_rank_counts"] == {"10": 480} and result["combined_tangent_rank_counts"] == {"11": 480}, "result_tangent_counts")
    require(result["max_phi_to_metric_feedback"] == 0.0 and result["max_metric_to_phi_feedback"] == 0.0, "result_decoupling")
    require(result["dynamics_loaded"] is False and result["solutions_run"] == 0 and result["physical_evolution_claimed"] is False, "no_dynamics")
    require(result["physics_ranking_used"] is False and result["finite_exhaustiveness_claim"] is False and result["gpu_used"] is False, "authority_stop")

    lineage = {row["path"]: row["sha256"] for row in tables["SOURCE_LINEAGE.tsv"]}
    require(lineage == {key: value for key, value in SOURCE_HASHES.items() if "PREREGISTRATION" not in key}, "source_lineage")
    if rehash:
        require(all(digest(ROOT / path) == expected for path, expected in SOURCE_HASHES.items()), "source_and_prereg_rehash")

    design = tables["AMPLITUDE_DESIGN.tsv"]
    require(len(design) == 60 and len({row["design_id"] for row in design}) == 60, "design_identity_census")
    matrix = np.array([[float(row[name]) for name in PARAMETERS] for row in design])
    require(len({tuple(row) for row in matrix}) == 60, "design_vectors_unique")
    require(np.linalg.matrix_rank(matrix[:, :10]) == 10 and np.linalg.matrix_rank(matrix) == 11, "independent_design_ranks")
    require(Counter(row["family"] for row in design) == Counter({"ORIGIN": 1, "METRIC_AXIS": 20, "PHI_AXIS": 2, "ORTHOGONAL_SIGN": 32, "PHI_SWEEP": 5}), "design_families")
    require(all(np.min(matrix[:, index]) < 0 < np.max(matrix[:, index]) and np.any(matrix[:, index] == 0) for index in range(11)), "parameter_sign_zero_coverage")
    hadamard = sylvester(32)[:, HADAMARD_COLUMNS]
    require(len({tuple(row) for row in hadamard}) == 32 and np.linalg.matrix_rank(hadamard) == 11, "hadamard_unique_rank")
    require(np.array_equal(hadamard.T @ hadamard, 32 * np.eye(11, dtype=int)), "hadamard_orthogonality")

    schedule = tables["SAMPLE_SCHEDULE.tsv"]
    require(len(schedule) == 8 and {row["point_id"] for row in schedule} == set(POINTS), "schedule")
    dependency = tables["PARAMETER_DEPENDENCY.tsv"]
    require(len(dependency) == 44 and all(row["all_coordinates_present"] == "YES" for row in dependency), "dependency_census")
    require(sum(row["target"] == "METRIC_ONLY" for row in dependency) == 40 and sum(row["target"] == "PHI_ONLY" for row in dependency) == 4, "dependency_separation")

    expected_ids = {
        f"{row['design_id']}_B{bank}_{point_id}"
        for row in design
        for bank in range(4)
        for point_id in SCHEDULE[bank]
    }
    observations = tables["CONFIGURATION_OBSERVATIONS.tsv"]
    require(len(observations) == 480 and {row["configuration_id"] for row in observations} == expected_ids, "observation_census")
    require(all(row["retained"] == "YES" and row["physical_merit"] == "NOT_EVALUATED" for row in observations), "no_filter")
    require(all(row["inertia"] == "1,3,0" and int(row["latent_to_slot_rank"]) == 10 for row in observations), "regular_chart_rank")
    require(max(float(row["identity_residual"]) for row in observations) < TOLERANCE, "identity_residual")

    tangent = tables["PARAMETER_TANGENT_RANKS.tsv"]
    require(len(tangent) == 480 and {row["configuration_id"] for row in tangent} == expected_ids, "tangent_census")
    require(Counter(int(row["complete_metric_rank"]) for row in tangent) == Counter({10: 480}), "complete_metric_rank_census")
    require(Counter(int(row["combined_rank"]) for row in tangent) == Counter({11: 480}), "combined_rank_census")
    require(Counter(int(row["slot_value_rank"]) for row in tangent) == Counter({10: 420, 0: 60}), "slot_value_rank_census")
    require(all(float(row["phi_to_metric_feedback_max_abs"]) == 0.0 and float(row["metric_to_phi_feedback_max_abs"]) == 0.0 for row in tangent), "tangent_decoupling")
    require(all(float(row["difference_step"]) == DIFFERENCE_STEP and float(row["rank_threshold"]) == RANK_TOLERANCE for row in tangent), "registered_numerical_controls")

    family_census = tables["DESIGN_FAMILY_CENSUS.tsv"]
    require(len(family_census) == 5 and sum(int(row["records"]) for row in family_census) == 480, "family_census")
    require(all(row["merit_filter"] == "NONE" for row in family_census), "family_census_no_merit")
    family_reconciled = True
    for row in family_census:
        subset = [item for item in observations if item["design_family"] == row["design_family"]]
        family_reconciled &= int(row["records"]) == len(subset)
        family_reconciled &= row["ricci_rank_counts"] == rank_text(subset, "ricci_rank")
        family_reconciled &= row["curvature_operator_rank_counts"] == rank_text(subset, "curvature_operator_rank")
        family_reconciled &= row["shear_rank_counts"] == rank_text(subset, "shear_rank")
        family_reconciled &= row["twist_rank_counts"] == rank_text(subset, "twist_rank")
        family_reconciled &= int(row["mixed_curvature_active"]) == sum(
            float(item["mixed_curvature_max_abs"]) > RANK_TOLERANCE for item in subset
        )
    require(family_reconciled, "family_census_reconciled")
    axis_census = tables["METRIC_AXIS_CENSUS.tsv"]
    require(len(axis_census) == 20 and all(int(row["records"]) == 8 and row["merit_filter"] == "NONE" for row in axis_census), "axis_census")
    axis_reconciled = True
    for row in axis_census:
        subset = [item for item in observations if item["design_id"] == row["design_id"]]
        axis_reconciled &= row["ricci_rank_counts"] == rank_text(subset, "ricci_rank")
        axis_reconciled &= row["curvature_operator_rank_counts"] == rank_text(subset, "curvature_operator_rank")
        axis_reconciled &= row["shear_rank_counts"] == rank_text(subset, "shear_rank")
        axis_reconciled &= row["twist_rank_counts"] == rank_text(subset, "twist_rank")
        axis_reconciled &= int(row["mixed_curvature_active"]) == sum(
            float(item["mixed_curvature_max_abs"]) > RANK_TOLERANCE for item in subset
        )
    require(axis_reconciled, "axis_census_reconciled")

    raw_by_id = {row["configuration_id"]: row for row in raw}
    require(len(raw) == 480 and len(raw_by_id) == 480 and set(raw_by_id) == expected_ids, "raw_census")
    obs_by_id = {row["configuration_id"]: row for row in observations}
    hash_ok = True
    for config_id, row in raw_by_id.items():
        identity = {"slots": row["slot_values"], "slot_first": row["slot_first"], "slot_second": row["slot_second"], "phi": row["phi"]}
        metric = {"metric": row["metric"], "first": row["metric_first"], "second": row["metric_second"]}
        hash_ok &= canonical_hash(identity) == row["configuration_sha256"] == obs_by_id[config_id]["configuration_sha256"]
        hash_ok &= canonical_hash(metric) == row["metric_jet_sha256"] == obs_by_id[config_id]["metric_jet_sha256"]
        hash_ok &= canonical_hash(row["phi"]) == row["phi_jet_sha256"] == obs_by_id[config_id]["phi_jet_sha256"]
        hash_ok &= canonical_hash(row["parameter_tangent"]) == row["parameter_tangent_sha256"] == obs_by_id[config_id]["parameter_tangent_sha256"]
    require(hash_ok, "all_raw_hashes")
    if rehash:
        require(digest(HERE / "RAW_CONFIGURATION_JETS.jsonl") == result["raw_configuration_sha256"], "raw_file_hash")

    phi_checks = tables["PHI_DECOUPLING.tsv"]
    require(len(phi_checks) == 16 and all(row["status"] == "PASS" and int(row["unique_metric_jets"]) == 1 for row in phi_checks), "phi_decoupling_checks")
    require(Counter(int(row["unique_phi_jets"]) for row in phi_checks) == Counter({5: 8, 3: 8}), "phi_decoupling_distinct")
    sectors = tables["SECTOR_ACTIVITY.tsv"]
    require(len(sectors) == 480 and {row["configuration_id"] for row in sectors} == expected_ids, "sector_census")
    require(all(row["dynamical_interpretation"] == "NONE_CONFIGURATION_ONLY" for row in sectors), "configuration_not_evolution")
    require(len(tables["COVERAGE_LEDGER.tsv"]) == 10 and all(row["status"] == "PASS" for row in tables["COVERAGE_LEDGER.tsv"]), "coverage_ledger")
    require(len(tables["TEN_CRITERION_SCOPE.tsv"]) == 10, "ten_criterion_scope")
    expected_anti = (
        "action EOM or residual filter", "boundary seal or topology target", "particle mass stability or spectrum target",
        "GR or empirical merit target", "shared metric amplitude retained", "phi amplitude fed into metric",
        "rank-deficient record discarded", "slot-value rank promoted to complete-jet rank", "time dependence called evolution",
        "finite design called generic dense or exhaustive", "physical representative selected", "metric-phi law inferred",
        "parameter threshold assigned physical meaning", "undesired curvature class filtered", "complete solution space claimed",
    )
    anti = tables["ANTI_IMPOSITION_AUDIT.tsv"]
    require(
        len(anti) == 15
        and tuple(row["failure_mode"] for row in anti) == expected_anti
        and all(row["present"] == "ABSENT" for row in anti),
        "anti_imposition",
    )

    independently_reconciled = True
    reconstructed_census: Counter[str] = Counter()
    for config_id, saved in raw_by_id.items():
        observation = obs_by_id[config_id]
        riemann = np.asarray(saved["riemann_down"])
        ricci = np.asarray(saved["ricci"])
        curvature_matrix = np.array([[riemann[a, b, c, d] for c, d in PAIRS] for a, b in PAIRS])
        ricci_rank = int(np.linalg.matrix_rank(ricci, tol=RANK_TOLERANCE))
        curvature_rank = int(np.linalg.matrix_rank(curvature_matrix, tol=RANK_TOLERANCE))
        shear_rank, twist_rank = independent_split_ranks(
            np.asarray(saved["slot_values"]), np.asarray(saved["slot_first"])
        )
        mixed = []
        for i in range(2):
            for j in range(2):
                for a in range(2, 4):
                    for b in range(2, 4):
                        mixed.extend((riemann[i, a, j, b], riemann[i, j, a, b]))
        mixed_max = float(np.max(np.abs(mixed)))
        phi_first = np.asarray(saved["phi"]["first"])
        phi_norm = float(phi_first @ np.linalg.inv(np.asarray(saved["metric"])) @ phi_first)
        independently_reconciled &= ricci_rank == int(observation["ricci_rank"])
        independently_reconciled &= curvature_rank == int(observation["curvature_operator_rank"])
        independently_reconciled &= shear_rank == int(observation["shear_rank"])
        independently_reconciled &= twist_rank == int(observation["twist_rank"])
        independently_reconciled &= abs(mixed_max - float(observation["mixed_curvature_max_abs"])) < 2e-12
        independently_reconciled &= abs(phi_norm - float(observation["phi_gradient_norm"])) < 2e-12
        metric_zero = all(float(observation[f"alpha_{index}"]) == 0.0 for index in range(10))
        reconstructed_census["metric_zero_records" if metric_zero else "metric_nonzero_records"] += 1
        reconstructed_census["metric_zero_flat_records"] += int(
            metric_zero and float(observation["riemann_max_abs"]) <= RANK_TOLERANCE
        )
        reconstructed_census["full_ricci_rank_records"] += int(ricci_rank == 4)
        reconstructed_census["full_curvature_operator_rank_records"] += int(curvature_rank == 6)
        reconstructed_census["shear_rank_two_records"] += int(shear_rank == 2)
        reconstructed_census["twist_rank_one_records"] += int(twist_rank == 1)
        reconstructed_census["mixed_curvature_records"] += int(mixed_max > RANK_TOLERANCE)
        phi_value = float(saved["phi"]["value"])
        reconstructed_census["phi_negative_records"] += int(phi_value < -RANK_TOLERANCE)
        reconstructed_census["phi_near_zero_records"] += int(abs(phi_value) <= RANK_TOLERANCE)
        reconstructed_census["phi_positive_records"] += int(phi_value > RANK_TOLERANCE)
        phi_max = float(np.max(np.abs(phi_first)))
        reconstructed_census["dphi_timelike_records"] += int(phi_norm < -RANK_TOLERANCE)
        reconstructed_census["dphi_zero_records"] += int(phi_max <= RANK_TOLERANCE)
        reconstructed_census["dphi_nonzero_near_null_records"] += int(
            phi_max > RANK_TOLERANCE and abs(phi_norm) <= RANK_TOLERANCE
        )
        reconstructed_census["dphi_spacelike_records"] += int(phi_norm > RANK_TOLERANCE)
    require(independently_reconciled, "all_record_geometry_observations_reconciled")
    require(dict(reconstructed_census) == result["geometry_census"], "geometry_census_independently_reconstructed")

    design_by_id = {row["design_id"]: row for row in design}
    structural_ok = True
    minimum_jacobian_singular = float("inf")
    for bank in range(4):
        for point_id in SCHEDULE[bank]:
            x = np.asarray(POINTS[point_id], dtype=float)
            field_jets = [polynomial_twojet(bank, field, x) for field in range(11)]
            latent_control = np.zeros((210, 10))
            for field in range(10):
                latent_control[field * 21 : (field + 1) * 21, field] = field_jets[field]
            combined_control = np.zeros((231, 11))
            combined_control[:210, :10] = latent_control
            combined_control[210:, 10] = field_jets[10]
            structural_ok &= np.linalg.matrix_rank(latent_control, tol=RANK_TOLERANCE) == 10
            structural_ok &= np.linalg.matrix_rank(combined_control, tol=RANK_TOLERANCE) == 11
            for design_id, design_row in design_by_id.items():
                amplitudes = np.array([float(design_row[name]) for name in PARAMETERS])
                latent = np.array([BASE[field] + amplitudes[field] * field_jets[field][0] for field in range(10)])
                singular = np.linalg.svd(latent_slot_jacobian(latent), compute_uv=False)
                minimum_jacobian_singular = min(minimum_jacobian_singular, float(np.min(singular)))
    require(structural_ok and minimum_jacobian_singular > RANK_TOLERANCE, "independent_prolonged_jet_rank_proof")

    if reconstruct:
        anchor = symbolic_anchor()
        saved = raw_by_id["O00_B0_P0"]
        saved_slot = np.concatenate((np.asarray(saved["slot_values"]).reshape(-1), np.asarray(saved["slot_first"]).reshape(-1), np.asarray(saved["slot_second"]).reshape(-1)))
        saved_phi = np.concatenate(((saved["phi"]["value"],), np.asarray(saved["phi"]["first"]), np.asarray(saved["phi"]["second"]).reshape(-1)))
        require(np.max(np.abs(anchor["slot_jet"] - saved_slot)) < 2e-12 and np.max(np.abs(anchor["phi_jet"] - saved_phi)) < 2e-12, "symbolic_anchor_twojets")
        require(np.linalg.matrix_rank(anchor["metric_tangent"], tol=RANK_TOLERANCE) == 10, "symbolic_anchor_metric_rank_ten")
        require(np.linalg.matrix_rank(anchor["combined_tangent"], tol=RANK_TOLERANCE) == 11, "symbolic_anchor_combined_rank_eleven")
        require(np.linalg.matrix_rank(anchor["metric_tangent"][:10], tol=RANK_TOLERANCE) == 0, "symbolic_anchor_value_rank_zero")

        curved = raw_by_id["H17_B2_P6"]
        riemann, ricci, scalar = independent_curvature(np.asarray(curved["metric"]), np.asarray(curved["metric_first"]), np.asarray(curved["metric_second"]))
        require(np.max(np.abs(riemann - np.asarray(curved["riemann_down"]))) < 2e-10, "independent_curvature_anchor")
        require(np.max(np.abs(ricci - np.asarray(curved["ricci"]))) < 2e-10, "independent_ricci_anchor")
        require(abs(scalar - float(curved["observables"]["scalar_curvature"])) < 2e-10, "independent_scalar_anchor")
    return checks


def main() -> None:
    result = json.loads((HERE / "ATLAS_RESULT.json").read_text(encoding="utf-8"))
    tables = {name: tsv(HERE / name) for name in TABLES}
    raw = [json.loads(line) for line in (HERE / "RAW_CONFIGURATION_JETS.jsonl").read_text(encoding="utf-8").splitlines()]
    checks = validate(result, tables, raw, rehash=True, reconstruct=True)

    mutations = []

    def catch(name: str, mutator) -> None:
        changed_result = copy.deepcopy(result)
        changed_tables = copy.deepcopy(tables)
        changed_raw = copy.deepcopy(raw)
        mutator(changed_result, changed_tables, changed_raw)
        try:
            validate(changed_result, changed_tables, changed_raw, rehash=False, reconstruct=False)
        except (AssertionError, KeyError, ValueError):
            mutations.append(name)
            return
        raise AssertionError(f"uncaught_mutation_{name}")

    catch("missing_design", lambda _r, t, _w: t["AMPLITUDE_DESIGN.tsv"].pop())
    catch("duplicate_design", lambda _r, t, _w: t["AMPLITUDE_DESIGN.tsv"].__setitem__(1, copy.deepcopy(t["AMPLITUDE_DESIGN.tsv"][0])))
    catch("shared_amplitude_regression", lambda _r, t, _w: [row.__setitem__("alpha_1", row["alpha_0"]) for row in t["AMPLITUDE_DESIGN.tsv"]])
    catch("lost_metric_axis", lambda _r, t, _w: t["AMPLITUDE_DESIGN.tsv"][1].__setitem__("family", "ORIGIN"))
    catch("lost_phi_axis", lambda _r, t, _w: t["AMPLITUDE_DESIGN.tsv"][21].__setitem__("family", "ORIGIN"))
    catch("rank_promotion", lambda _r, t, _w: t["PARAMETER_TANGENT_RANKS.tsv"][0].__setitem__("complete_metric_rank", "9"))
    catch("phi_feedback", lambda _r, t, _w: t["PARAMETER_TANGENT_RANKS.tsv"][0].__setitem__("phi_to_metric_feedback_max_abs", "0.001"))
    catch("omitted_sector", lambda _r, t, _w: t["SECTOR_ACTIVITY.tsv"].pop())
    catch("changed_tolerance", lambda _r, t, _w: t["PARAMETER_TANGENT_RANKS.tsv"][0].__setitem__("rank_threshold", "1e-6"))
    catch("filtered_record", lambda _r, t, _w: t["CONFIGURATION_OBSERVATIONS.tsv"].pop())
    catch("dynamics_promotion", lambda r, _t, _w: r.__setitem__("dynamics_loaded", True))
    catch("physical_evolution_promotion", lambda r, _t, _w: r.__setitem__("physical_evolution_claimed", True))
    catch("physics_ranking_promotion", lambda r, _t, _w: r.__setitem__("physics_ranking_used", True))
    catch("solutions_promotion", lambda r, _t, _w: r.__setitem__("solutions_run", 1))
    catch("finite_exhaustiveness", lambda r, _t, _w: r.__setitem__("finite_exhaustiveness_claim", True))
    catch("geometry_census_corruption", lambda r, _t, _w: r["geometry_census"].__setitem__("twist_rank_one_records", 0))
    catch("anti_imposition_identity", lambda _r, t, _w: t["ANTI_IMPOSITION_AUDIT.tsv"][0].__setitem__("failure_mode", "changed"))

    output = {
        "schema": "udt-independent-amplitude-metric-atlas-verification-1.0",
        "status": "PASS",
        "independent_checks": len(checks),
        "catch_proofs": len(mutations),
        "catches": mutations,
        "builder_imported": False,
        "symbolic_anchor": "O00_B0_P0",
        "independent_curvature_anchor": "H17_B2_P6",
        "classification_verified": CLASSIFICATION,
        "maximum_verified": MAXIMUM,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "UDT_INDEPENDENT_AMPLITUDE_ATLAS_VERIFICATION=PASS",
        f"independent_checks={len(checks)} catch_proofs={len(mutations)}",
        "builder_imported=NO",
        "symbolic_anchor=O00_B0_P0 metric_rank=10 combined_rank=11 slot_value_rank=0",
        "structural_prolonged_jet_rank=10+1 ALL_480",
        "independent_curvature_anchor=H17_B2_P6 PASS",
        f"classification={CLASSIFICATION}",
        f"maximum={MAXIMUM}",
    ]
    (HERE / "VERIFICATION_TRANSCRIPT.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))


if __name__ == "__main__":
    main()

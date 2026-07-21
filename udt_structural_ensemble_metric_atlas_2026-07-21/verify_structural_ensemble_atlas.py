#!/usr/bin/env python3
"""Independent verifier for the structural ensemble and Mobius interaction atlas.

This verifier does not import the ensemble-atlas builder. It reconstructs the control partition,
carrier/mask design, all raw curvatures, split kinematics, Mobius terms, and sampled span ranks.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_amplitude_volume_metric_atlas_2026-07-21"
SCHEMA = "udt-structural-ensemble-metric-atlas-1.0"
CLASSIFICATION = "BOUNDED_STRUCTURAL_ENSEMBLE_CONFIGURATIONS_AND_MOBIUS_INTERACTIONS_OBSERVED"
MAXIMUM = "BOUNDED_STRUCTURAL_ENSEMBLE_AND_MOBIUS_INTERACTION_ATLAS_CHARACTERIZED"
TOLERANCE = 2e-10
RANK_TOLERANCE = 1e-9
UNCERTAINTY_LOW = RANK_TOLERANCE / 100
UNCERTAINTY_HIGH = RANK_TOLERANCE * 100
PARAMETERS = tuple(f"alpha_{index}" for index in range(10)) + ("beta",)
ENSEMBLES = (
    ("E0", "BASE_BLOCK", (0, 1, 2), 1),
    ("E1", "ANGULAR_SCREEN_BLOCK", (3, 4, 5), 2),
    ("E2", "SHIFT_CONNECTION_BLOCK", (6, 7, 8, 9), 4),
    ("E3", "PHI_FIELD", (10,), 8),
)
SCHEDULE = {0: ("P0", "P4"), 1: ("P1", "P5"), 2: ("P2", "P6"), 3: ("P3", "P7")}
POINTS = {
    "P0": (0.0, 0.0, 0.0, 0.0), "P1": (1 / 3, -1 / 4, 1 / 5, -1 / 6),
    "P2": (-1 / 4, 1 / 5, -1 / 6, 1 / 7), "P3": (1 / 5, 1 / 6, -1 / 7, -1 / 8),
    "P4": (-1 / 6, -1 / 7, 1 / 8, 1 / 9), "P5": (1 / 2, 0.0, -1 / 3, 1 / 4),
    "P6": (0.0, -1 / 2, 1 / 4, -1 / 3), "P7": (1 / 3, 1 / 3, 1 / 3, 1 / 3),
}
BASE_VALUES = (0.08, 0.14, -0.06, 0.12, -0.09, 0.05, 0.11, -0.07, 0.09, 0.04)
PHI_OFFSETS = (-0.25, 0.0, 0.25, 0.125)
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAYLOADS = (
    "slot_twojet", "metric_twojet", "riemann", "weyl", "ricci", "scalar", "shear", "twist", "phi_twojet"
)
SOURCE_HASHES = {
    "udt_amplitude_volume_metric_atlas_2026-07-21/SHA256SUMS.txt": "5182486f4a87080096532d9fe5ba999837ac79fac979c5694f216209ae41c112",
    "udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt": "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad",
    "udt_structural_ensemble_metric_atlas_2026-07-21/PREREGISTRATION.md": "bbb628becce5b16923e6c41f129e7aa549cb10d7168d4cdd0ba13a4fa6f73f07",
    "udt_structural_ensemble_metric_atlas_2026-07-21/PREREGISTRATION_IMPLEMENTATION_NOTE.md": "47521b770c2ef1f60c2018e3257a58bf08d9699e37d18bd95ec0a635f0e14f61",
}
TABLE_NAMES = (
    "SOURCE_LINEAGE.tsv", "ENSEMBLE_REGISTRY.tsv", "CARRIER_VECTOR_REGISTRY.tsv",
    "ENSEMBLE_MASK_REGISTRY.tsv", "SAMPLE_SCHEDULE.tsv", "CONFIGURATION_OBSERVATIONS.tsv",
    "RAW_SHARD_REGISTRY.tsv", "MASK_GEOMETRY_CENSUS.tsv", "MOBIUS_INTERACTIONS.tsv",
    "INTERACTION_SPAN_RANKS.tsv", "INTERACTION_ORDER_CENSUS.tsv", "NUMERIC_MARGIN_LEDGER.tsv",
    "COVERAGE_LEDGER.tsv", "TEN_CRITERION_SCOPE.tsv", "ANTI_IMPOSITION_AUDIT.tsv",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def canonical_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def replay_manifest(path: Path) -> bool:
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        expected, relative = line.split("  ", 1)
        target = path.parent / relative
        if not target.is_file() or digest(target) != expected:
            return False
    return True


def mask_names(mask: int) -> str:
    names = [name for _identity, name, _controls, bit in ENSEMBLES if mask & bit]
    return ";".join(names) if names else "EMPTY"


def mask_vector(carrier: np.ndarray, mask: int) -> np.ndarray:
    result = np.zeros(11)
    for _identity, _name, controls, bit in ENSEMBLES:
        if mask & bit:
            result[list(controls)] = carrier[list(controls)]
    return result


def jet_constant(value: float) -> tuple[float, np.ndarray, np.ndarray]:
    return float(value), np.zeros(4), np.zeros((4, 4))


def jet_add(left, right):
    return left[0] + right[0], left[1] + right[1], left[2] + right[2]


def jet_scale(scale: float, value):
    return scale * value[0], scale * value[1], scale * value[2]


def jet_mul(left, right):
    return (
        left[0] * right[0],
        left[0] * right[1] + right[0] * left[1],
        left[0] * right[2] + right[0] * left[2]
        + np.outer(left[1], right[1]) + np.outer(right[1], left[1]),
    )


def jet_exp(value):
    exponential = float(np.exp(value[0]))
    return exponential, exponential * value[1], exponential * (value[2] + np.outer(value[1], value[1]))


def coefficient(bank: int, field: int, term: int) -> float:
    raw = ((bank + 2) * 11 + (field + 1) * 7 + (term + 1) * 5 + (bank + 1) * (field + term + 3)) % 19 - 9
    if raw == 0:
        raw = 1 if (bank + field + term) % 2 == 0 else -1
    return raw / (60.0 if term < 4 else 90.0 if term < 8 else 120.0)


def feature_jets(point: np.ndarray) -> list[tuple[float, np.ndarray, np.ndarray]]:
    features = []
    for coordinate in range(4):
        first = np.zeros(4); first[coordinate] = 1.0
        features.append((float(point[coordinate]), first, np.zeros((4, 4))))
    for coordinate in range(4):
        first = np.zeros(4); first[coordinate] = point[coordinate]
        second = np.zeros((4, 4)); second[coordinate, coordinate] = 1.0
        features.append((0.5 * float(point[coordinate] ** 2), first, second))
    for first_coordinate, second_coordinate in PAIRS:
        first = np.zeros(4)
        first[first_coordinate] = point[second_coordinate]
        first[second_coordinate] = point[first_coordinate]
        second = np.zeros((4, 4))
        second[first_coordinate, second_coordinate] = 1.0
        second[second_coordinate, first_coordinate] = 1.0
        features.append((float(point[first_coordinate] * point[second_coordinate]), first, second))
    return features


def polynomial_jet(bank: int, field: int, point: np.ndarray):
    result = jet_constant(0.0)
    for term, feature in enumerate(feature_jets(point)):
        result = jet_add(result, jet_scale(coefficient(bank, field, term), feature))
    return result


def primitive_twojets(bank: int, amplitudes: np.ndarray, point: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, tuple]:
    latent = [
        jet_add(jet_constant(BASE_VALUES[field]), jet_scale(float(amplitudes[field]), polynomial_jet(bank, field, point)))
        for field in range(10)
    ]
    a, b, c, d, e, f, a20, a30, a21, a31 = latent
    u, w, r, t = jet_exp(a), jet_exp(c), jet_exp(d), jet_exp(f)
    slots = (
        jet_scale(-1.0, jet_mul(u, u)),
        jet_scale(-1.0, jet_mul(u, b)),
        jet_add(jet_mul(w, w), jet_scale(-1.0, jet_mul(b, b))),
        jet_mul(r, r),
        jet_mul(r, e),
        jet_add(jet_mul(e, e), jet_mul(t, t)),
        a20, a30, a21, a31,
    )
    values = np.asarray([slot[0] for slot in slots])
    first = np.asarray([slot[1] for slot in slots]).T
    second = np.transpose(np.asarray([slot[2] for slot in slots]), (1, 2, 0))
    phi = jet_add(jet_constant(PHI_OFFSETS[bank]), jet_scale(float(amplitudes[10]), polynomial_jet(bank, 10, point)))
    return values, first, second, phi


def metric_twojets_from_slots(values: np.ndarray, first: np.ndarray, second: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    jets = [(values[index], first[:, index], second[:, :, index]) for index in range(10)]
    h = ((jets[0], jets[1]), (jets[1], jets[2]))
    q = ((jets[3], jets[4]), (jets[4], jets[5]))
    shifts = ((jets[6], jets[8]), (jets[7], jets[9]))
    zero = jet_constant(0.0)
    metric = [[zero for _ in range(4)] for _ in range(4)]
    for i in range(2):
        for j in range(2):
            value = h[i][j]
            for a in range(2):
                for b in range(2):
                    value = jet_add(value, jet_mul(jet_mul(q[a][b], shifts[a][i]), shifts[b][j]))
            metric[i][j] = value
        for b in range(2):
            value = zero
            for a in range(2):
                value = jet_add(value, jet_mul(q[a][b], shifts[a][i]))
            metric[i][2 + b] = value
            metric[2 + b][i] = value
    for a in range(2):
        for b in range(2):
            metric[2 + a][2 + b] = q[a][b]
    g = np.asarray([[metric[mu][nu][0] for nu in range(4)] for mu in range(4)])
    dg = np.asarray([[[metric[mu][nu][1][k] for nu in range(4)] for mu in range(4)] for k in range(4)])
    ddg = np.asarray([[[[metric[mu][nu][2][k, ell] for nu in range(4)] for mu in range(4)] for ell in range(4)] for k in range(4)])
    return g, dg, ddg


def flatten_twojet(values, first, second) -> np.ndarray:
    return np.concatenate((np.asarray(values).reshape(-1), np.asarray(first).reshape(-1), np.asarray(second).reshape(-1)))


def split_kinematics(slot_values: np.ndarray, slot_first: np.ndarray) -> tuple[np.ndarray, np.ndarray, int, int]:
    screen = np.array([[slot_values[3], slot_values[4]], [slot_values[4], slot_values[5]]])
    shifts = np.array([[slot_values[6], slot_values[8]], [slot_values[7], slot_values[9]]])
    screen_first = [np.array([[slot_first[k, 3], slot_first[k, 4]], [slot_first[k, 4], slot_first[k, 5]]]) for k in range(4)]
    shifts_first = [np.array([[slot_first[k, 6], slot_first[k, 8]], [slot_first[k, 7], slot_first[k, 9]]]) for k in range(4)]
    inverse = np.linalg.inv(screen)
    twist = np.zeros(2)
    for vertical in range(2):
        twist[vertical] = (
            shifts_first[0][vertical, 1] - shifts_first[1][vertical, 0]
            - sum(shifts[other, 0] * shifts_first[2 + other][vertical, 1] for other in range(2))
            + sum(shifts[other, 1] * shifts_first[2 + other][vertical, 0] for other in range(2))
        )
    shear_rows = []
    for base in range(2):
        horizontal = screen_first[base] - sum(shifts[vertical, base] * screen_first[2 + vertical] for vertical in range(2))
        vertical_derivative = np.array([[shifts_first[2 + derivative][output, base] for output in range(2)] for derivative in range(2)])
        deformation = 0.5 * (horizontal - vertical_derivative @ screen - screen @ vertical_derivative.T)
        expansion = float(np.trace(inverse @ deformation))
        shear = deformation - 0.5 * expansion * screen
        shear_rows.append((shear[0, 0], shear[0, 1], shear[1, 1]))
    shear = np.asarray(shear_rows)
    return shear, twist, int(np.linalg.matrix_rank(shear, tol=RANK_TOLERANCE)), int(np.linalg.matrix_rank(twist.reshape(2, 1), tol=RANK_TOLERANCE))


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
    up = np.zeros((4, 4, 4, 4))
    for rho in range(4):
        for sigma in range(4):
            for mu in range(4):
                for nu in range(4):
                    up[rho, sigma, mu, nu] = (
                        dgamma[mu, rho, nu, sigma] - dgamma[nu, rho, mu, sigma]
                        + sum(gamma[rho, mu, lam] * gamma[lam, nu, sigma] - gamma[rho, nu, lam] * gamma[lam, mu, sigma] for lam in range(4))
                    )
    down = np.einsum("ar,rsuv->asuv", g, up)
    ricci = np.einsum("rsrn->sn", up)
    scalar = float(np.einsum("ab,ab", inverse, ricci))
    return down, ricci, scalar


def weyl_tensor(g: np.ndarray, riemann: np.ndarray, ricci: np.ndarray, scalar: float) -> np.ndarray:
    result = np.zeros_like(riemann)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    result[a, b, c, d] = (
                        riemann[a, b, c, d]
                        - 0.5 * (g[a, c] * ricci[b, d] - g[a, d] * ricci[b, c] - g[b, c] * ricci[a, d] + g[b, d] * ricci[a, c])
                        + scalar * (g[a, c] * g[b, d] - g[a, d] * g[b, c]) / 6.0
                    )
    return result


def reconstructed_payloads(
    slot_values: np.ndarray,
    slot_first: np.ndarray,
    slot_second: np.ndarray,
    metric: np.ndarray,
    metric_first: np.ndarray,
    metric_second: np.ndarray,
    riemann: np.ndarray,
    weyl: np.ndarray,
    ricci: np.ndarray,
    scalar: float,
    shear: np.ndarray,
    twist: np.ndarray,
    phi,
) -> dict[str, np.ndarray]:
    return {
        "slot_twojet": flatten_twojet(slot_values, slot_first, slot_second),
        "metric_twojet": flatten_twojet(metric, metric_first, metric_second),
        "riemann": np.asarray(riemann).reshape(-1),
        "weyl": np.asarray(weyl).reshape(-1),
        "ricci": np.asarray(ricci).reshape(-1),
        "scalar": np.asarray((scalar,)),
        "shear": shear.reshape(-1), "twist": twist.reshape(-1),
        "phi_twojet": flatten_twojet((phi[0],), phi[1], phi[2]),
    }


def geometry_class(ricci_rank: int, curvature_rank: int, shear_rank: int, twist_rank: int, mixed: float) -> str:
    return f"R{ricci_rank}_K{curvature_rank}_S{shear_rank}_T{twist_rank}_M{int(mixed > RANK_TOLERANCE)}"


def dphi_class(phi_first: np.ndarray, metric: np.ndarray) -> str:
    norm = float(phi_first @ np.linalg.inv(metric) @ phi_first)
    if float(np.max(np.abs(phi_first))) <= RANK_TOLERANCE:
        return "ZERO"
    if abs(norm) <= RANK_TOLERANCE:
        return "NONZERO_NEAR_NULL"
    return "TIMELIKE" if norm < 0 else "SPACELIKE"


def mobius(cube: dict[int, np.ndarray], target: int) -> np.ndarray:
    return sum(
        ((-1) ** (target.bit_count() - subset.bit_count())) * cube[subset]
        for subset in range(16) if subset & ~target == 0
    )


def numeric_status(value: float) -> str:
    return "NUMERIC_UNCERTAIN" if UNCERTAINTY_LOW <= abs(value) <= UNCERTAINTY_HIGH else "NUMERIC_CLASSIFIED"


def validate_partition(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 11
    assert [int(row["control_index"]) for row in rows] == list(range(11))
    assert Counter(row["ensemble_id"] for row in rows) == Counter({"E0": 3, "E1": 3, "E2": 4, "E3": 1})
    expected = {index: ensemble_id for ensemble_id, _name, controls, _bit in ENSEMBLES for index in controls}
    assert all(row["ensemble_id"] == expected[int(row["control_index"])] for row in rows)
    assert all(row["physical_interpretation"] == "NONE" for row in rows)


def validate_carriers(rows: list[dict[str, str]], parent_rows: dict[str, dict[str, str]]) -> None:
    assert len(rows) == 48
    assert [row["carrier_id"] for row in rows] == carrier_identities()
    for row in rows:
        parent = parent_rows[row["carrier_id"]]
        assert row["parent_row_sha256"] == canonical_hash(parent)
        assert all(float(row[name]) == float(parent[name]) for name in PARAMETERS)
        assert all(row[field] == parent[field] for field in ("design_kind", "direction_id", "radius", "halton_index"))


def validate_masks(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 16
    assert [int(row["mask_integer"]) for row in rows] == list(range(16))
    assert Counter(int(row["ensemble_order"]) for row in rows) == Counter({0: 1, 1: 4, 2: 6, 3: 4, 4: 1})
    assert all(row["selected_ensembles"] == mask_names(int(row["mask_integer"])) for row in rows)


def validate_schedule(rows: list[dict[str, str]], expected_contexts: set[tuple[str, str]]) -> None:
    assert len(rows) == 8
    assert {(row["bank"], row["point_id"]) for row in rows} == expected_contexts
    assert all(int(row["configurations"]) == 768 for row in rows)


def validate_configurations(rows: list[dict[str, str]], expected_ids: set[str]) -> None:
    identities = [row["configuration_id"] for row in rows]
    assert len(rows) == 6144 and len(set(identities)) == 6144 and set(identities) == expected_ids
    assert all(row["retained"] == "YES" and row["physical_merit"] == "NOT_EVALUATED" for row in rows)


def validate_interactions(rows: list[dict[str, str]], expected_ids: set[str]) -> None:
    identities = [row["interaction_id"] for row in rows]
    assert len(rows) == 5760 and len(set(identities)) == 5760 and set(identities) == expected_ids
    for row in rows:
        target = int(row["target_integer"])
        subsets = [subset for subset in range(16) if subset & ~target == 0]
        assert row["subsets_used"] == ";".join(f"M{subset:X}" for subset in subsets)
        assert int(row["subset_count"]) == len(subsets)
        assert row["physical_interaction_claimed"] == "NO"


def validate_authority(result: dict) -> None:
    assert result["physical_interaction_claimed"] is False
    assert result["mobius_physical_coupling_claimed"] is False
    assert result["phi_metric_source_claimed"] is False
    assert result["ensemble_ontology_claimed"] is False
    assert result["action_or_equations_loaded"] is False
    assert result["dynamics_loaded"] is False
    assert result["solutions_run"] == 0
    assert result["physics_ranking_used"] is False
    assert result["finite_exhaustiveness_claim"] is False
    assert result["gpu_used"] is False


def validate_digest(path: Path, expected: str) -> None:
    assert digest(path) == expected


def validate_interaction_norm(row: dict[str, str], payload_name: str, expected: tuple[float, float, str, str]) -> None:
    l2, maximum, active, status = expected
    assert abs(float(row[f"{payload_name}_l2"]) - l2) < 2e-11
    assert abs(float(row[f"{payload_name}_max_abs"]) - maximum) < 2e-12
    assert row[f"{payload_name}_active"] == active
    assert row[f"{payload_name}_status"] == status


def validate_span_row(row: dict[str, str], expected: tuple[int, int, int, int, float, float, float, str]) -> None:
    vectors, components, rank, maximum_rank, largest, minimum_retained, maximum_discarded, status = expected
    assert int(row["vectors"]) == vectors and int(row["components"]) == components
    assert int(row["span_rank"]) == rank and int(row["max_possible_rank"]) == maximum_rank
    assert abs(float(row["largest_singular"]) - largest) < 2e-10
    assert abs(float(row["min_retained_singular"]) - minimum_retained) < 2e-10
    assert abs(float(row["max_discarded_singular"]) - maximum_discarded) < 2e-10
    assert row["rank_status"] == status and row["physical_dof_claimed"] == "NO"


def carrier_identities() -> list[str]:
    return [f"R{direction:02d}_1" for direction in range(16)] + [f"R{direction:02d}_3" for direction in range(16)] + [f"V{index:03d}" for index in range(1, 17)]


def main() -> None:
    result = json.loads((HERE / "ATLAS_RESULT.json").read_text(encoding="utf-8"))
    tables = {name: tsv(HERE / name) for name in TABLE_NAMES}
    checks: list[str] = []

    def require(condition: bool, name: str) -> None:
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    require(result["schema"] == SCHEMA and result["status"] == "PASS", "schema_status")
    require(result["classification"] == CLASSIFICATION and result["maximum_conclusion"] == MAXIMUM, "scope_stamp")
    require(
        result["ensemble_count"] == 4 and result["control_count"] == 11 and result["carrier_vectors"] == 48
        and result["mask_count"] == 16 and result["configuration_records"] == 6144
        and result["interaction_records"] == 5760 and result["raw_shards"] == 8 and result["span_rank_rows"] == 135,
        "result_counts",
    )
    validate_authority(result)
    checks.append("authority_stop")
    require(all(digest(ROOT / path) == expected for path, expected in SOURCE_HASHES.items()), "source_and_prereg_hashes")
    require(all(replay_manifest(ROOT / path) for path in SOURCE_HASHES if path.endswith("SHA256SUMS.txt")), "parent_manifest_entries")
    lineage = {row["path"]: row["sha256"] for row in tables["SOURCE_LINEAGE.tsv"]}
    require(lineage == {path: value for path, value in SOURCE_HASHES.items() if "PREREGISTRATION" not in path}, "source_lineage")

    validate_partition(tables["ENSEMBLE_REGISTRY.tsv"])
    checks.append("control_partition")
    masks = tables["ENSEMBLE_MASK_REGISTRY.tsv"]
    validate_masks(masks)
    checks.append("mask_registry")

    parent_rows = {row["design_id"]: row for row in tsv(PARENT / "AMPLITUDE_VOLUME_DESIGN.tsv")}
    carriers = tables["CARRIER_VECTOR_REGISTRY.tsv"]
    carrier_by_id = {row["carrier_id"]: row for row in carriers}
    validate_carriers(carriers, parent_rows)
    checks.append("carrier_parent_reconciliation")

    schedule = tables["SAMPLE_SCHEDULE.tsv"]
    expected_contexts = {(f"B{bank}", point) for bank, points in SCHEDULE.items() for point in points}
    validate_schedule(schedule, expected_contexts)
    checks.append("schedule")

    observations = tables["CONFIGURATION_OBSERVATIONS.tsv"]
    obs_by_id = {row["configuration_id"]: row for row in observations}
    expected_config_ids = {
        f"{carrier}_M{mask:X}_B{bank}_{point}"
        for carrier in carrier_identities() for mask in range(16) for bank, points in SCHEDULE.items() for point in points
    }
    validate_configurations(observations, expected_config_ids)
    checks.append("configuration_census_and_no_filter")

    interaction_rows = tables["MOBIUS_INTERACTIONS.tsv"]
    interaction_by_id = {row["interaction_id"]: row for row in interaction_rows}
    expected_interaction_ids = {
        f"{carrier}_T{target:X}_B{bank}_{point}"
        for carrier in carrier_identities() for target in range(1, 16) for bank, points in SCHEDULE.items() for point in points
    }
    validate_interactions(interaction_rows, expected_interaction_ids)
    checks.append("interaction_census_subsets_and_authority")

    shards = tables["RAW_SHARD_REGISTRY.tsv"]
    shard_by_context = {(row["bank"], row["point_id"]): row for row in shards}
    require(len(shards) == 8 and set(shard_by_context) == expected_contexts and sum(int(row["records"]) for row in shards) == 6144, "shard_registry")
    require(
        all(
            (HERE / row["path"]).is_file()
            and (HERE / row["path"]).stat().st_size == int(row["bytes"])
            and digest(HERE / row["path"]) == row["sha256"]
            for row in shards
        ),
        "shard_hashes",
    )
    require(digest(HERE / "RAW_SHARD_REGISTRY.tsv") == result["raw_shard_registry_sha256"], "shard_registry_hash")

    interaction_vectors: dict[tuple[int, str], list[np.ndarray]] = defaultdict(list)
    raw_ids: set[str] = set()
    reconstructed_classes: Counter[tuple[int, str]] = Counter()
    reconstructed_active: dict[int, Counter[str]] = defaultdict(Counter)
    max_curvature_error = 0.0
    max_kinematic_error = 0.0
    max_primitive_jet_error = 0.0
    max_metric_assembly_error = 0.0
    all_raw_ok = True
    all_interactions_ok = True
    interaction_expected_norms: dict[tuple[str, str], tuple[float, float, str, str]] = {}

    for (bank_text, point_id), shard_row in sorted(shard_by_context.items()):
        bank = int(bank_text[1:])
        raw_rows = [json.loads(line) for line in (HERE / shard_row["path"]).read_text(encoding="utf-8").splitlines()]
        require(len(raw_rows) == 768, f"raw_shard_count_{bank_text}_{point_id}")
        context_payloads: dict[tuple[str, int], dict[str, np.ndarray]] = {}
        for raw in raw_rows:
            config_id = raw["configuration_id"]
            raw_ids.add(config_id)
            observation = obs_by_id[config_id]
            carrier_id, mask = raw["carrier_id"], int(raw["mask_integer"])
            carrier = carrier_by_id[carrier_id]
            carrier_vector = np.array([float(carrier[name]) for name in PARAMETERS])
            effective = mask_vector(carrier_vector, mask)
            all_raw_ok &= np.max(np.abs(effective - np.asarray(raw["effective_amplitudes"]))) < 1e-15
            all_raw_ok &= np.max(np.abs(carrier_vector - np.asarray(raw["carrier_amplitudes"]))) < 1e-15
            all_raw_ok &= raw["bank"] == bank_text and raw["point_id"] == point_id
            identity = {"slots": raw["slot_values"], "slot_first": raw["slot_first"], "slot_second": raw["slot_second"], "phi": raw["phi"]}
            metric_payload = {"metric": raw["metric"], "first": raw["metric_first"], "second": raw["metric_second"]}
            all_raw_ok &= canonical_hash(identity) == raw["configuration_sha256"] == observation["configuration_sha256"]
            all_raw_ok &= canonical_hash(metric_payload) == raw["metric_jet_sha256"] == observation["metric_jet_sha256"]

            point = np.asarray(POINTS[point_id])
            regenerated_values, regenerated_first, regenerated_second, regenerated_phi = primitive_twojets(bank, effective, point)
            primitive_error = max(
                float(np.max(np.abs(regenerated_values - np.asarray(raw["slot_values"])))),
                float(np.max(np.abs(regenerated_first - np.asarray(raw["slot_first"])))),
                float(np.max(np.abs(regenerated_second - np.asarray(raw["slot_second"])))),
                abs(regenerated_phi[0] - float(raw["phi"]["value"])),
                float(np.max(np.abs(regenerated_phi[1] - np.asarray(raw["phi"]["first"])))),
                float(np.max(np.abs(regenerated_phi[2] - np.asarray(raw["phi"]["second"])))),
            )
            max_primitive_jet_error = max(max_primitive_jet_error, primitive_error)
            assembled_metric, assembled_first, assembled_second = metric_twojets_from_slots(
                regenerated_values, regenerated_first, regenerated_second
            )
            metric_assembly_error = max(
                float(np.max(np.abs(assembled_metric - np.asarray(raw["metric"])))),
                float(np.max(np.abs(assembled_first - np.asarray(raw["metric_first"])))),
                float(np.max(np.abs(assembled_second - np.asarray(raw["metric_second"])))),
            )
            max_metric_assembly_error = max(max_metric_assembly_error, metric_assembly_error)
            all_raw_ok &= primitive_error < 2e-15 and metric_assembly_error < 2e-15

            metric = assembled_metric
            metric_first = assembled_first
            metric_second = assembled_second
            riemann, ricci, scalar = independent_curvature(metric, metric_first, metric_second)
            weyl = weyl_tensor(metric, riemann, ricci, scalar)
            curvature_error = max(
                float(np.max(np.abs(riemann - np.asarray(raw["riemann_down"])))),
                float(np.max(np.abs(ricci - np.asarray(raw["ricci"])))),
                float(np.max(np.abs(weyl - np.asarray(raw["weyl_down"])))),
                abs(scalar - float(raw["observables"]["scalar_curvature"])),
            )
            max_curvature_error = max(max_curvature_error, curvature_error)
            curvature_matrix = np.array([[riemann[a, b, c, d] for c, d in PAIRS] for a, b in PAIRS])
            ricci_singular = np.linalg.svd(ricci, compute_uv=False)
            curvature_singular = np.linalg.svd(curvature_matrix, compute_uv=False)
            ricci_rank = int(np.count_nonzero(ricci_singular > RANK_TOLERANCE))
            curvature_rank = int(np.count_nonzero(curvature_singular > RANK_TOLERANCE))
            ricci_status = "NUMERIC_UNCERTAIN" if np.any((ricci_singular >= UNCERTAINTY_LOW) & (ricci_singular <= UNCERTAINTY_HIGH)) else "NUMERIC_CLASSIFIED"
            curvature_status = "NUMERIC_UNCERTAIN" if np.any((curvature_singular >= UNCERTAINTY_LOW) & (curvature_singular <= UNCERTAINTY_HIGH)) else "NUMERIC_CLASSIFIED"
            shear, twist, shear_rank, twist_rank = split_kinematics(regenerated_values, regenerated_first)
            max_kinematic_error = max(
                max_kinematic_error,
                float(np.max(np.abs(shear.reshape(-1) - np.asarray(raw["shear_vector"])))),
                float(np.max(np.abs(twist - np.asarray(raw["twist_vector"])))),
            )
            mixed_values = []
            for i in range(2):
                for j in range(2):
                    for a in range(2, 4):
                        for b in range(2, 4):
                            mixed_values.extend((riemann[i, a, j, b], riemann[i, j, a, b]))
            mixed = float(np.max(np.abs(mixed_values)))
            class_id = geometry_class(ricci_rank, curvature_rank, shear_rank, twist_rank, mixed)
            phi_class = dphi_class(regenerated_phi[1], metric)
            all_raw_ok &= curvature_error < TOLERANCE
            all_raw_ok &= ricci_rank == int(observation["ricci_rank"])
            all_raw_ok &= curvature_rank == int(observation["curvature_operator_rank"])
            all_raw_ok &= shear_rank == int(observation["shear_rank"]) and twist_rank == int(observation["twist_rank"])
            all_raw_ok &= ricci_status == observation["ricci_rank_status"] and curvature_status == observation["curvature_rank_status"]
            all_raw_ok &= class_id == observation["geometry_class"] and phi_class == observation["dphi_class"]
            all_raw_ok &= observation["numeric_uncertain"] == ("YES" if "NUMERIC_UNCERTAIN" in (ricci_status, curvature_status) else "NO")
            reconstructed_classes[(mask, class_id)] += 1
            context_payloads[(carrier_id, mask)] = reconstructed_payloads(
                regenerated_values, regenerated_first, regenerated_second,
                metric, metric_first, metric_second, riemann, weyl, ricci, scalar,
                shear, twist, regenerated_phi,
            )

        for carrier_id in carrier_identities():
            for target in range(1, 16):
                interaction_id = f"{carrier_id}_T{target:X}_{bank_text}_{point_id}"
                saved = interaction_by_id[interaction_id]
                subsets = [subset for subset in range(16) if subset & ~target == 0]
                all_interactions_ok &= saved["subsets_used"] == ";".join(f"M{subset:X}" for subset in subsets)
                all_interactions_ok &= int(saved["subset_count"]) == len(subsets)
                for payload_name in PAYLOADS:
                    cube = {mask: context_payloads[(carrier_id, mask)][payload_name] for mask in range(16)}
                    vector = mobius(cube, target)
                    interaction_vectors[(target, payload_name)].append(vector)
                    l2, maximum = float(np.linalg.norm(vector)), float(np.max(np.abs(vector)))
                    active = maximum > RANK_TOLERANCE
                    interaction_expected_norms[(interaction_id, payload_name)] = (
                        l2, maximum, "YES" if active else "NO", numeric_status(maximum)
                    )
                    all_interactions_ok &= abs(l2 - float(saved[f"{payload_name}_l2"])) < 2e-11
                    all_interactions_ok &= abs(maximum - float(saved[f"{payload_name}_max_abs"])) < 2e-12
                    all_interactions_ok &= saved[f"{payload_name}_active"] == ("YES" if active else "NO")
                    all_interactions_ok &= saved[f"{payload_name}_status"] == numeric_status(maximum)
                    reconstructed_active[target][payload_name] += int(active)

    require(raw_ids == expected_config_ids and all_raw_ok, "all_raw_configurations_reconstructed")
    require(max_primitive_jet_error < 2e-15 and max_metric_assembly_error < 2e-15, "all_primitive_jets_and_metric_assembly")
    require(max_curvature_error < TOLERANCE and max_kinematic_error < 2e-12, "all_curvature_and_kinematics")
    require(all_interactions_ok, "all_mobius_interactions_reconstructed")

    class_table = {
        (int(row["mask_integer"]), row["geometry_class"]): int(row["records"])
        for row in tables["MASK_GEOMETRY_CENSUS.tsv"]
    }
    require(class_table == dict(reconstructed_classes) and sum(class_table.values()) == 6144, "geometry_census")
    expected_result_classes = {
        f"M{mask:X}": dict(sorted(Counter({class_id: count for (saved_mask, class_id), count in reconstructed_classes.items() if saved_mask == mask}).items()))
        for mask in range(16)
    }
    require(result["mask_geometry_class_counts"] == expected_result_classes, "result_geometry_census")
    require(result["numeric_uncertain_configurations"] == sum(row["numeric_uncertain"] == "YES" for row in observations), "uncertain_configuration_census")

    span_saved = {(int(row["target_integer"]), row["payload"]): row for row in tables["INTERACTION_SPAN_RANKS.tsv"]}
    margins_saved = {(int(row["target_integer"]), row["payload"]): row for row in tables["NUMERIC_MARGIN_LEDGER.tsv"]}
    require(len(span_saved) == 135 and len(margins_saved) == 135, "span_margin_census")
    span_ok = True
    margin_ok = True
    span_expected: dict[tuple[int, str], tuple[int, int, int, int, float, float, float, str]] = {}
    for target in range(1, 16):
        for payload_name in PAYLOADS:
            matrix = np.stack(interaction_vectors[(target, payload_name)])
            singular = np.linalg.svd(matrix, compute_uv=False)
            rank = int(np.count_nonzero(singular > RANK_TOLERANCE))
            retained = singular[singular > RANK_TOLERANCE]
            discarded = singular[singular <= RANK_TOLERANCE]
            status = "NUMERIC_UNCERTAIN" if np.any((singular >= UNCERTAINTY_LOW) & (singular <= UNCERTAINTY_HIGH)) else "NUMERIC_CLASSIFIED"
            saved = span_saved[(target, payload_name)]
            expected_span = (
                384, matrix.shape[1], rank, min(matrix.shape), float(singular[0]),
                float(np.min(retained)) if retained.size else 0.0,
                float(np.max(discarded)) if discarded.size else 0.0, status,
            )
            span_expected[(target, payload_name)] = expected_span
            try:
                validate_span_row(saved, expected_span)
            except AssertionError:
                span_ok = False
            maxima = [float(row[f"{payload_name}_max_abs"]) for row in interaction_rows if int(row["target_integer"]) == target]
            active = [value for value in maxima if value > RANK_TOLERANCE]
            inactive = [value for value in maxima if value <= RANK_TOLERANCE]
            margin = margins_saved[(target, payload_name)]
            margin_ok &= int(margin["active_rows"]) == len(active) and int(margin["inactive_rows"]) == len(inactive)
            margin_ok &= int(margin["uncertain_rows"]) == sum(UNCERTAINTY_LOW <= value <= UNCERTAINTY_HIGH for value in maxima)
            margin_ok &= abs(float(margin["min_active_max_abs"]) - (min(active) if active else 0.0)) < 2e-12
            margin_ok &= abs(float(margin["max_inactive_max_abs"]) - (max(inactive) if inactive else 0.0)) < 2e-12
    require(span_ok, "interaction_span_ranks")
    require(margin_ok, "interaction_numeric_margins")

    result_active = {
        f"M{target:X}": {payload_name: reconstructed_active[target][payload_name] for payload_name in PAYLOADS}
        for target in range(1, 16)
    }
    require(result["active_interaction_rows_by_target_and_payload"] == result_active, "result_interaction_census")
    order_saved = {(int(row["ensemble_order"]), row["payload"]): row for row in tables["INTERACTION_ORDER_CENSUS.tsv"]}
    order_ok = len(order_saved) == 36
    for order in range(1, 5):
        subset = [row for row in interaction_rows if int(row["ensemble_order"]) == order]
        for payload_name in PAYLOADS:
            row = order_saved[(order, payload_name)]
            active = sum(item[f"{payload_name}_active"] == "YES" for item in subset)
            order_ok &= int(row["interaction_rows"]) == len(subset)
            order_ok &= int(row["active_rows"]) == active and int(row["inactive_rows"]) == len(subset) - active
            order_ok &= row["physical_interpretation"] == "NONE"
    require(order_ok, "interaction_order_census")
    require(len(tables["COVERAGE_LEDGER.tsv"]) == 10 and len(tables["TEN_CRITERION_SCOPE.tsv"]) == 10, "scope_ledgers")
    require(len(tables["ANTI_IMPOSITION_AUDIT.tsv"]) == 12 and all(row["present"] == "ABSENT" for row in tables["ANTI_IMPOSITION_AUDIT.tsv"]), "anti_imposition")

    catches: list[str] = []

    def catch(name: str, operation) -> None:
        try:
            operation()
        except (AssertionError, KeyError, ValueError, IndexError, OSError):
            catches.append(name)
            return
        raise AssertionError(f"uncaught_mutation_{name}")

    catch("missing_control", lambda: validate_partition(copy.deepcopy(tables["ENSEMBLE_REGISTRY.tsv"][:-1])))
    duplicated = copy.deepcopy(tables["ENSEMBLE_REGISTRY.tsv"]); duplicated[-1] = copy.deepcopy(duplicated[0])
    catch("duplicate_shared_control", lambda: validate_partition(duplicated))
    wrong_member = copy.deepcopy(tables["ENSEMBLE_REGISTRY.tsv"]); wrong_member[0]["ensemble_id"] = "E1"
    catch("wrong_ensemble_membership", lambda: validate_partition(wrong_member))
    physicalized = copy.deepcopy(tables["ENSEMBLE_REGISTRY.tsv"]); physicalized[0]["physical_interpretation"] = "MATTER"
    catch("ensemble_physicalization", lambda: validate_partition(physicalized))
    catch("missing_carrier", lambda: validate_carriers(copy.deepcopy(carriers[:-1]), parent_rows))
    drifted_carriers = copy.deepcopy(carriers); drifted_carriers[0]["alpha_0"] = str(float(drifted_carriers[0]["alpha_0"]) + 0.1)
    catch("carrier_drift", lambda: validate_carriers(drifted_carriers, parent_rows))
    catch("missing_mask", lambda: validate_masks(copy.deepcopy(masks[:-1])))
    duplicated_masks = copy.deepcopy(masks); duplicated_masks[-1] = copy.deepcopy(duplicated_masks[0])
    catch("duplicate_mask", lambda: validate_masks(duplicated_masks))
    catch("missing_configuration", lambda: validate_configurations(copy.deepcopy(observations[:-1]), expected_config_ids))
    filtered_configurations = copy.deepcopy(observations); filtered_configurations[0]["retained"] = "NO"
    catch("filtered_configuration", lambda: validate_configurations(filtered_configurations, expected_config_ids))
    wrong_schedule = copy.deepcopy(schedule); wrong_schedule[0]["point_id"] = "P7"
    catch("wrong_schedule", lambda: validate_schedule(wrong_schedule, expected_contexts))
    catch("missing_interaction", lambda: validate_interactions(copy.deepcopy(interaction_rows[:-1]), expected_interaction_ids))
    wrong_subsets = copy.deepcopy(interaction_rows); wrong_subsets[0]["subsets_used"] = "M0"
    catch("wrong_interaction_subsets", lambda: validate_interactions(wrong_subsets, expected_interaction_ids))
    physical_interactions = copy.deepcopy(interaction_rows); physical_interactions[0]["physical_interaction_claimed"] = "YES"
    catch("physical_interaction_row_promotion", lambda: validate_interactions(physical_interactions, expected_interaction_ids))
    synthetic = {mask: np.asarray((float((mask & 1) > 0 and (mask & 2) > 0),)) for mask in range(16)}
    catch("incorrect_subset_sign", lambda: np.testing.assert_allclose(-mobius(synthetic, 3), np.asarray((1.0,)), atol=0, rtol=0))
    norm_key = (interaction_rows[0]["interaction_id"], "riemann")
    corrupted_norm = copy.deepcopy(interaction_rows[0]); corrupted_norm["riemann_l2"] = str(float(corrupted_norm["riemann_l2"]) + 1.0)
    catch("corrupted_interaction_norm", lambda: validate_interaction_norm(corrupted_norm, "riemann", interaction_expected_norms[norm_key]))
    first_span_key = next(iter(span_saved))
    incorrect_span = copy.deepcopy(span_saved[first_span_key]); incorrect_span["span_rank"] = str(int(incorrect_span["span_rank"]) + 1)
    catch("incorrect_span_rank", lambda: validate_span_row(incorrect_span, span_expected[first_span_key]))
    first_source_path = next(iter(SOURCE_HASHES))
    catch("source_manifest_drift", lambda: validate_digest(ROOT / first_source_path, "0" * 64))
    catch("shard_hash_drift", lambda: validate_digest(HERE / shards[0]["path"], "0" * 64))
    authority_mutations = (
        ("physical_interaction_promotion", "physical_interaction_claimed", True),
        ("mobius_coupling_promotion", "mobius_physical_coupling_claimed", True),
        ("phi_source_promotion", "phi_metric_source_claimed", True),
        ("ensemble_ontology_promotion", "ensemble_ontology_claimed", True),
        ("action_promotion", "action_or_equations_loaded", True),
        ("dynamics_promotion", "dynamics_loaded", True),
        ("solution_promotion", "solutions_run", 1),
        ("physics_ranking_promotion", "physics_ranking_used", True),
        ("finite_exhaustiveness", "finite_exhaustiveness_claim", True),
        ("gpu_promotion", "gpu_used", True),
    )
    for name, field, value in authority_mutations:
        mutated = copy.deepcopy(result); mutated[field] = value
        catch(name, lambda mutated=mutated: validate_authority(mutated))
    anti_mutation = copy.deepcopy(tables["ANTI_IMPOSITION_AUDIT.tsv"]); anti_mutation[0]["present"] = "PRESENT"
    catch(
        "anti_imposition_declaration_drift",
        lambda: np.testing.assert_equal([row["present"] for row in anti_mutation], ["ABSENT"] * 12),
    )

    output = {
        "schema": "udt-structural-ensemble-metric-atlas-verification-1.0",
        "status": "PASS",
        "independent_checks": len(checks),
        "catch_proofs": len(catches),
        "catches": catches,
        "ensemble_builder_imported": False,
        "all_configuration_curvatures_reconstructed": 6144,
        "all_primitive_slot_and_phi_twojets_regenerated": 6144,
        "all_metrics_reassembled_from_regenerated_slots": 6144,
        "all_mobius_interactions_reconstructed": 5760,
        "max_primitive_jet_reconstruction_error": max_primitive_jet_error,
        "max_metric_assembly_reconstruction_error": max_metric_assembly_error,
        "max_curvature_reconstruction_error": max_curvature_error,
        "max_kinematic_reconstruction_error": max_kinematic_error,
        "classification_verified": CLASSIFICATION,
        "maximum_verified": MAXIMUM,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "UDT_STRUCTURAL_ENSEMBLE_ATLAS_VERIFICATION=PASS",
        f"independent_checks={len(checks)} catch_proofs={len(catches)}",
        "ensemble_builder_imported=NO",
        "controls=11 carriers=48 masks=16 configurations=6144 interactions=5760 ALL_RECONCILED",
        f"all_6144_primitive_jets=PASS max_error={max_primitive_jet_error:.17g}",
        f"all_6144_metric_assemblies=PASS max_error={max_metric_assembly_error:.17g}",
        f"all_6144_curvatures=PASS max_error={max_curvature_error:.17g}",
        f"all_5760_mobius_terms=PASS max_kinematic_error={max_kinematic_error:.17g}",
        f"classification={CLASSIFICATION}",
        f"maximum={MAXIMUM}",
    ]
    (HERE / "VERIFICATION_TRANSCRIPT.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))


if __name__ == "__main__":
    main()

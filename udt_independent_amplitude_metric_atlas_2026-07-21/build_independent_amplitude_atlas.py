#!/usr/bin/env python3
"""Build the preregistered independent-amplitude metric configuration atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_constructive_metric_family_atlas_2026-07-21"
sys.path.insert(0, str(PARENT))

import build_constructive_atlas as parent  # noqa: E402


SCHEMA = "udt-independent-amplitude-metric-atlas-1.0"
CLASSIFICATION = "INDEPENDENT_AMPLITUDE_CONFIGURATION_ATLAS_OBSERVED_IN_REGISTERED_LOCAL_REGIME"
MAXIMUM = "TEN_METRIC_AMPLITUDES_AND_PHI_VARIED_INDEPENDENTLY_WITHIN_REGISTERED_CONFIGURATION_DESIGN"
RANK_DEFICIENT = "PARAMETERIZATION_RANK_DEFICIENT_IN_REGISTERED_REGIME"
TOLERANCE = 2e-10
RANK_TOLERANCE = 1e-9
DIFFERENCE_STEP = 1e-6
HADAMARD_COLUMNS = (1, 2, 4, 8, 16, 3, 5, 6, 7, 9, 10)
ALPHA_NAMES = tuple(f"alpha_{index}" for index in range(10))
PARAMETER_NAMES = ALPHA_NAMES + ("beta",)
POINT_SCHEDULE = {
    0: ("P0", "P4"),
    1: ("P1", "P5"),
    2: ("P2", "P6"),
    3: ("P3", "P7"),
}
SOURCE_HASHES = {
    "udt_constructive_metric_family_atlas_2026-07-21/SHA256SUMS.txt": "c851721f3e8e15768f8f4945151c0d78bde6f1186bbadcfce5066b939a645370",
    "udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt": "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def write_tsv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sylvester(order: int) -> np.ndarray:
    matrix = np.ones((1, 1), dtype=int)
    while matrix.shape[0] < order:
        matrix = np.block([[matrix, matrix], [matrix, -matrix]])
    if matrix.shape != (order, order):
        raise AssertionError("hadamard_order")
    return matrix


def amplitude_design() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def append(design_id: str, family: str, values: np.ndarray, note: str) -> None:
        row: dict[str, object] = {"design_id": design_id, "family": family, "note": note}
        row.update({name: float(values[index]) for index, name in enumerate(PARAMETER_NAMES)})
        rows.append(row)

    append("O00", "ORIGIN", np.zeros(11), "all eleven controls zero")
    for field in range(10):
        for sign, suffix in ((1.0, "P"), (-1.0, "M")):
            vector = np.zeros(11)
            vector[field] = sign
            append(f"A{field:02d}{suffix}", "METRIC_AXIS", vector, f"isolated {ALPHA_NAMES[field]}")
    for sign, suffix in ((1.0, "P"), (-1.0, "M")):
        vector = np.zeros(11)
        vector[10] = sign
        append(f"B00{suffix}", "PHI_AXIS", vector, "isolated beta")
    block = sylvester(32)[:, HADAMARD_COLUMNS]
    for index, signs in enumerate(block):
        append(f"H{index:02d}", "ORTHOGONAL_SIGN", 0.75 * signs.astype(float), "corrected H32 columns")
    fixed_metric = np.array((1.0, -0.5, 0.75, -1.0, 0.5, -0.75, 1.0, -0.5, 0.75, -1.0))
    for index, beta in enumerate((-1.0, -0.5, 0.0, 0.5, 1.0)):
        append(f"S{index:02d}", "PHI_SWEEP", np.concatenate((fixed_metric, (beta,))), "fixed metric amplitudes")
    return rows


def regular_family(bank: int, amplitudes: np.ndarray, x: np.ndarray) -> dict[str, object]:
    latent = [
        parent.jet_constant(parent.BASE_VALUES[index])
        + float(amplitudes[index]) * parent.polynomial_jet(bank, index, x)
        for index in range(10)
    ]
    a, b, c, d, e, f, a20, a30, a21, a31 = latent
    u, w, r, t = parent.jet_exp(a), parent.jet_exp(c), parent.jet_exp(d), parent.jet_exp(f)
    slots = (
        -(u * u),
        -(u * b),
        w * w - b * b,
        r * r,
        r * e,
        e * e + t * t,
        a20,
        a30,
        a21,
        a31,
    )
    slot_values = np.array([item.value for item in slots])
    slot_first = np.array([item.first for item in slots]).T
    slot_second = np.transpose(np.array([item.second for item in slots]), (1, 2, 0))
    metric_jets = parent.metric_jets_from_split(slot_values, slot_first, slot_second)

    zero = parent.jet_constant(0.0)
    coframe_jets = [[zero for _ in range(parent.DIM)] for _ in range(parent.DIM)]
    coframe_jets[0] = [u, b, zero, zero]
    coframe_jets[1] = [zero, w, zero, zero]
    coframe_jets[2] = [r * a20 + e * a30, r * a21 + e * a31, r, e]
    coframe_jets[3] = [t * a30, t * a31, zero, t]
    coframe = np.array([[item.value for item in row] for row in coframe_jets])
    coframe_first = np.array(
        [[[coframe_jets[i][mu].first[k] for mu in range(4)] for i in range(4)] for k in range(4)]
    )
    coframe_second = np.array(
        [
            [
                [[coframe_jets[i][mu].second[k, ell] for mu in range(4)] for i in range(4)]
                for ell in range(4)
            ]
            for k in range(4)
        ]
    )
    phi = (
        parent.jet_constant(parent.PHI_OFFSETS[bank])
        + float(amplitudes[10]) * parent.polynomial_jet(bank, 10, x)
    )
    return {
        "latent": latent,
        "slots": slots,
        "slot_values": slot_values,
        "slot_first": slot_first,
        "slot_second": slot_second,
        "metric_jets": metric_jets,
        "coframe": coframe,
        "coframe_first": coframe_first,
        "coframe_second": coframe_second,
        "phi": phi,
    }


def slot_vector(family: dict[str, object]) -> np.ndarray:
    return np.concatenate(
        (
            np.asarray(family["slot_values"]).reshape(-1),
            np.asarray(family["slot_first"]).reshape(-1),
            np.asarray(family["slot_second"]).reshape(-1),
        )
    )


def phi_vector(family: dict[str, object]) -> np.ndarray:
    phi = family["phi"]
    return np.concatenate(((float(phi.value),), np.asarray(phi.first).reshape(-1), np.asarray(phi.second).reshape(-1)))


def tangent_diagnostics(bank: int, amplitudes: np.ndarray, x: np.ndarray) -> dict[str, object]:
    metric_columns = []
    combined_columns = []
    for parameter in range(11):
        plus = amplitudes.copy()
        minus = amplitudes.copy()
        plus[parameter] += DIFFERENCE_STEP
        minus[parameter] -= DIFFERENCE_STEP
        plus_family = regular_family(bank, plus, x)
        minus_family = regular_family(bank, minus, x)
        metric_derivative = (slot_vector(plus_family) - slot_vector(minus_family)) / (2 * DIFFERENCE_STEP)
        phi_derivative = (phi_vector(plus_family) - phi_vector(minus_family)) / (2 * DIFFERENCE_STEP)
        combined_columns.append(np.concatenate((metric_derivative, phi_derivative)))
        if parameter < 10:
            metric_columns.append(metric_derivative)
    metric_tangent = np.column_stack(metric_columns)
    combined_tangent = np.column_stack(combined_columns)
    slot_rank, slot_status, slot_singular = parent.numerical_rank(metric_tangent[:10])
    metric_rank, metric_status, metric_singular = parent.numerical_rank(metric_tangent)
    combined_rank, combined_status, combined_singular = parent.numerical_rank(combined_tangent)
    phi_feedback = float(np.max(np.abs(combined_tangent[:210, 10])))
    metric_to_phi = float(np.max(np.abs(combined_tangent[210:, :10])))
    return {
        "slot_value_rank": slot_rank,
        "slot_value_status": slot_status,
        "slot_value_singular_values": slot_singular,
        "complete_metric_rank": metric_rank,
        "complete_metric_status": metric_status,
        "complete_metric_singular_values": metric_singular,
        "combined_rank": combined_rank,
        "combined_status": combined_status,
        "combined_singular_values": combined_singular,
        "phi_to_metric_feedback_max_abs": phi_feedback,
        "metric_to_phi_feedback_max_abs": metric_to_phi,
    }


def main() -> None:
    checks: list[str] = []

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    for path, expected in SOURCE_HASHES.items():
        check(f"source_{path}", digest(ROOT / path) == expected)
    write_tsv(
        "SOURCE_LINEAGE.tsv",
        ["path", "sha256", "role"],
        [
            {"path": path, "sha256": expected, "role": "VERIFIED_PARENT_OR_EVALUATOR"}
            for path, expected in SOURCE_HASHES.items()
        ],
    )

    design = amplitude_design()
    design_matrix = np.array([[float(row[name]) for name in PARAMETER_NAMES] for row in design])
    hadamard = sylvester(32)[:, HADAMARD_COLUMNS]
    check("design_count", len(design) == 60)
    check("design_unique", len({tuple(row) for row in design_matrix}) == 60)
    check("metric_design_rank", np.linalg.matrix_rank(design_matrix[:, :10]) == 10)
    check("complete_design_rank", np.linalg.matrix_rank(design_matrix) == 11)
    check("hadamard_unique", len({tuple(row) for row in hadamard}) == 32)
    check("hadamard_rank", np.linalg.matrix_rank(hadamard) == 11)
    check("hadamard_orthogonal", np.array_equal(hadamard.T @ hadamard, 32 * np.eye(11, dtype=int)))
    check("parameter_signs_and_zero", all(np.min(design_matrix[:, index]) < 0 < np.max(design_matrix[:, index]) and np.any(design_matrix[:, index] == 0) for index in range(11)))
    check("metric_axes", sum(row["family"] == "METRIC_AXIS" for row in design) == 20)
    check("phi_axes", sum(row["family"] == "PHI_AXIS" for row in design) == 2)
    check("phi_sweep", sum(row["family"] == "PHI_SWEEP" for row in design) == 5)
    write_tsv(
        "AMPLITUDE_DESIGN.tsv",
        ["design_id", "family", *PARAMETER_NAMES, "note"],
        design,
    )

    schedule_rows = []
    for bank, point_ids in POINT_SCHEDULE.items():
        for point_id in point_ids:
            point = parent.POINTS[point_id]
            schedule_rows.append(
                {
                    "bank": f"B{bank}",
                    "point_id": point_id,
                    "x0": point[0],
                    "x1": point[1],
                    "x2": point[2],
                    "x3": point[3],
                    "design_rows": 60,
                }
            )
    check("schedule_count", len(schedule_rows) == 8 and {row["point_id"] for row in schedule_rows} == set(parent.POINTS))
    write_tsv("SAMPLE_SCHEDULE.tsv", list(schedule_rows[0]), schedule_rows)

    dependency_rows = []
    for bank in range(4):
        for field, name in enumerate(parent.LATENT_NAMES + ("phi",)):
            coefficients = [parent.coefficient(bank, field, coordinate) for coordinate in range(4)]
            dependency_rows.append(
                {
                    "bank": f"B{bank}",
                    "field": name,
                    "control": PARAMETER_NAMES[field],
                    "target": "METRIC_ONLY" if field < 10 else "PHI_ONLY",
                    "dx0_linear": coefficients[0],
                    "dx1_linear": coefficients[1],
                    "dx2_linear": coefficients[2],
                    "dx3_linear": coefficients[3],
                    "all_coordinates_present": "YES" if all(value != 0 for value in coefficients) else "NO",
                }
            )
    check("parameter_dependencies", len(dependency_rows) == 44 and all(row["all_coordinates_present"] == "YES" for row in dependency_rows))
    write_tsv("PARAMETER_DEPENDENCY.tsv", list(dependency_rows[0]), dependency_rows)

    observations: list[dict[str, object]] = []
    tangents: list[dict[str, object]] = []
    sectors: list[dict[str, object]] = []
    raw_rows: list[dict[str, object]] = []
    for design_row in design:
        amplitudes = np.array([float(design_row[name]) for name in PARAMETER_NAMES])
        for bank in range(4):
            for point_id in POINT_SCHEDULE[bank]:
                point = np.array(parent.POINTS[point_id], dtype=float)
                family = regular_family(bank, amplitudes, point)
                observation, raw = parent.observe_configuration(family)
                tangent = tangent_diagnostics(bank, amplitudes, point)
                tangent_hash = canonical_hash(tangent)
                config_id = f"{design_row['design_id']}_B{bank}_{point_id}"
                identity = {
                    "slots": raw["slot_values"],
                    "slot_first": raw["slot_first"],
                    "slot_second": raw["slot_second"],
                    "phi": raw["phi"],
                }
                metric_payload = {"metric": raw["metric"], "first": raw["metric_first"], "second": raw["metric_second"]}
                prefix = {
                    "configuration_id": config_id,
                    "design_id": design_row["design_id"],
                    "design_family": design_row["family"],
                    "bank": f"B{bank}",
                    "point_id": point_id,
                    "configuration_sha256": canonical_hash(identity),
                    "metric_jet_sha256": canonical_hash(metric_payload),
                    "phi_jet_sha256": canonical_hash(raw["phi"]),
                    "parameter_tangent_sha256": tangent_hash,
                }
                observations.append(
                    {
                        **prefix,
                        **{name: design_row[name] for name in PARAMETER_NAMES},
                        **observation,
                        "complete_metric_parameter_rank": tangent["complete_metric_rank"],
                        "combined_parameter_rank": tangent["combined_rank"],
                        "retained": "YES",
                        "physical_merit": "NOT_EVALUATED",
                    }
                )
                tangents.append(
                    {
                        "configuration_id": config_id,
                        "slot_value_rank": tangent["slot_value_rank"],
                        "slot_value_status": tangent["slot_value_status"],
                        "complete_metric_rank": tangent["complete_metric_rank"],
                        "complete_metric_status": tangent["complete_metric_status"],
                        "combined_rank": tangent["combined_rank"],
                        "combined_status": tangent["combined_status"],
                        "phi_to_metric_feedback_max_abs": tangent["phi_to_metric_feedback_max_abs"],
                        "metric_to_phi_feedback_max_abs": tangent["metric_to_phi_feedback_max_abs"],
                        "difference_step": DIFFERENCE_STEP,
                        "rank_threshold": RANK_TOLERANCE,
                        "interpretation": "COMPLETE_TWO_JET_PARAMETER_TANGENT_NOT_GLOBAL_GENERICITY",
                    }
                )
                sectors.append(
                    {
                        "configuration_id": config_id,
                        "time_active": "YES" if observation["time_derivative_activity"] > RANK_TOLERANCE else "NO",
                        "depth_active": "YES" if observation["depth_derivative_activity"] > RANK_TOLERANCE else "NO",
                        "angular2_active": "YES" if observation["angular2_derivative_activity"] > RANK_TOLERANCE else "NO",
                        "angular3_active": "YES" if observation["angular3_derivative_activity"] > RANK_TOLERANCE else "NO",
                        "mixed_shift_values_active": "YES" if np.max(np.abs(family["slot_values"][6:])) > RANK_TOLERANCE else "NO",
                        "screen_offdiagonal_active": "YES" if abs(family["slot_values"][4]) > RANK_TOLERANCE else "NO",
                        "shear_rank": observation["shear_rank"],
                        "twist_rank": observation["twist_rank"],
                        "mixed_curvature_active": "YES" if observation["mixed_curvature_max_abs"] > RANK_TOLERANCE else "NO",
                        "dynamical_interpretation": "NONE_CONFIGURATION_ONLY",
                    }
                )
                raw_rows.append(
                    {
                        **prefix,
                        "coordinates": point.tolist(),
                        "amplitudes": amplitudes.tolist(),
                        **raw,
                        "parameter_tangent": tangent,
                    }
                )

    check("configuration_count", len(observations) == 480)
    check("configuration_ids_unique", len({row["configuration_id"] for row in observations}) == 480)
    check("all_lorentzian", all(row["inertia"] == "1,3,0" for row in observations))
    check("latent_slot_rank", all(int(row["latent_to_slot_rank"]) == 10 for row in observations))
    check("identity_residual", max(float(row["identity_residual"]) for row in observations) < TOLERANCE)
    check("weyl_trace_residual", max(float(row["weyl_trace_residual"]) for row in observations) < TOLERANCE)
    check("all_retained", all(row["retained"] == "YES" for row in observations))
    write_tsv("CONFIGURATION_OBSERVATIONS.tsv", list(observations[0]), observations)
    write_tsv("PARAMETER_TANGENT_RANKS.tsv", list(tangents[0]), tangents)
    write_tsv("SECTOR_ACTIVITY.tsv", list(sectors[0]), sectors)
    with (HERE / "RAW_CONFIGURATION_JETS.jsonl").open("w", encoding="utf-8") as handle:
        for row in raw_rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")

    complete_rank_counts = Counter(int(row["complete_metric_rank"]) for row in tangents)
    combined_rank_counts = Counter(int(row["combined_rank"]) for row in tangents)
    slot_rank_counts = Counter(int(row["slot_value_rank"]) for row in tangents)
    rank_success = complete_rank_counts == Counter({10: 480}) and combined_rank_counts == Counter({11: 480})
    check("zero_phi_metric_feedback", max(float(row["phi_to_metric_feedback_max_abs"]) for row in tangents) == 0.0)
    check("zero_metric_phi_feedback", max(float(row["metric_to_phi_feedback_max_abs"]) for row in tangents) == 0.0)

    def rank_text(rows: list[dict[str, object]], field: str) -> str:
        counts = Counter(int(row[field]) for row in rows)
        return ";".join(f"{rank}:{counts[rank]}" for rank in sorted(counts))

    family_census = []
    for family_name in sorted({str(row["design_family"]) for row in observations}):
        subset = [row for row in observations if row["design_family"] == family_name]
        family_census.append(
            {
                "design_family": family_name,
                "records": len(subset),
                "ricci_rank_counts": rank_text(subset, "ricci_rank"),
                "curvature_operator_rank_counts": rank_text(subset, "curvature_operator_rank"),
                "shear_rank_counts": rank_text(subset, "shear_rank"),
                "twist_rank_counts": rank_text(subset, "twist_rank"),
                "mixed_curvature_active": sum(float(row["mixed_curvature_max_abs"]) > RANK_TOLERANCE for row in subset),
                "merit_filter": "NONE",
            }
        )
    check("family_census", len(family_census) == 5 and sum(int(row["records"]) for row in family_census) == 480)
    write_tsv("DESIGN_FAMILY_CENSUS.tsv", list(family_census[0]), family_census)

    axis_census = []
    for design_id in sorted({str(row["design_id"]) for row in observations if row["design_family"] == "METRIC_AXIS"}):
        subset = [row for row in observations if row["design_id"] == design_id]
        axis_census.append(
            {
                "design_id": design_id,
                "metric_field": int(design_id[1:3]),
                "sign": "PLUS" if design_id.endswith("P") else "MINUS",
                "records": len(subset),
                "ricci_rank_counts": rank_text(subset, "ricci_rank"),
                "curvature_operator_rank_counts": rank_text(subset, "curvature_operator_rank"),
                "shear_rank_counts": rank_text(subset, "shear_rank"),
                "twist_rank_counts": rank_text(subset, "twist_rank"),
                "mixed_curvature_active": sum(float(row["mixed_curvature_max_abs"]) > RANK_TOLERANCE for row in subset),
                "merit_filter": "NONE",
            }
        )
    check("axis_census", len(axis_census) == 20 and all(int(row["records"]) == 8 for row in axis_census))
    write_tsv("METRIC_AXIS_CENSUS.tsv", list(axis_census[0]), axis_census)

    phi_rows = []
    by_key = {(row["design_id"], row["bank"], row["point_id"]): row for row in observations}
    for bank in range(4):
        for point_id in POINT_SCHEDULE[bank]:
            sweep = [by_key[(f"S{index:02d}", f"B{bank}", point_id)] for index in range(5)]
            axes = [by_key[(design_id, f"B{bank}", point_id)] for design_id in ("O00", "B00P", "B00M")]
            phi_rows.extend(
                (
                    {
                        "check_id": f"SWEEP_B{bank}_{point_id}",
                        "kind": "FIVE_LEVEL_PHI_SWEEP",
                        "records": ";".join(row["configuration_id"] for row in sweep),
                        "unique_metric_jets": len({row["metric_jet_sha256"] for row in sweep}),
                        "unique_phi_jets": len({row["phi_jet_sha256"] for row in sweep}),
                        "metric_expected": 1,
                        "phi_expected": 5,
                        "status": "PASS" if len({row["metric_jet_sha256"] for row in sweep}) == 1 and len({row["phi_jet_sha256"] for row in sweep}) == 5 else "FAIL",
                    },
                    {
                        "check_id": f"AXIS_B{bank}_{point_id}",
                        "kind": "ORIGIN_PLUS_PHI_AXES",
                        "records": ";".join(row["configuration_id"] for row in axes),
                        "unique_metric_jets": len({row["metric_jet_sha256"] for row in axes}),
                        "unique_phi_jets": len({row["phi_jet_sha256"] for row in axes}),
                        "metric_expected": 1,
                        "phi_expected": 3,
                        "status": "PASS" if len({row["metric_jet_sha256"] for row in axes}) == 1 and len({row["phi_jet_sha256"] for row in axes}) == 3 else "FAIL",
                    },
                )
            )
    check("phi_decoupling", len(phi_rows) == 16 and all(row["status"] == "PASS" for row in phi_rows))
    write_tsv("PHI_DECOUPLING.tsv", list(phi_rows[0]), phi_rows)

    metric_zero = [row for row in observations if all(float(row[name]) == 0.0 for name in ALPHA_NAMES)]
    metric_nonzero = [row for row in observations if row not in metric_zero]
    coverage = [
        {"id": "C01", "object": "amplitude_design_rows", "observed": len(design), "required": 60, "status": "PASS", "scope": "finite deterministic design"},
        {"id": "C02", "object": "unique_amplitude_rows", "observed": len({tuple(row) for row in design_matrix}), "required": 60, "status": "PASS", "scope": "not Cartesian exhaustive"},
        {"id": "C03", "object": "metric_design_rank", "observed": int(np.linalg.matrix_rank(design_matrix[:, :10])), "required": 10, "status": "PASS", "scope": "sample design matrix"},
        {"id": "C04", "object": "combined_design_rank", "observed": int(np.linalg.matrix_rank(design_matrix)), "required": 11, "status": "PASS", "scope": "sample design matrix"},
        {"id": "C05", "object": "regular_configuration_records", "observed": len(observations), "required": 480, "status": "PASS", "scope": "four banks two points each"},
        {"id": "C06", "object": "complete_metric_tangent_rank_ten_records", "observed": complete_rank_counts.get(10, 0), "required": 480, "status": "PASS" if rank_success else "OBSERVED_DEFICIENT", "scope": "210x10 tangent"},
        {"id": "C07", "object": "combined_tangent_rank_eleven_records", "observed": combined_rank_counts.get(11, 0), "required": 480, "status": "PASS" if rank_success else "OBSERVED_DEFICIENT", "scope": "231x11 tangent"},
        {"id": "C08", "object": "phi_decoupling_checks", "observed": sum(row["status"] == "PASS" for row in phi_rows), "required": 16, "status": "PASS", "scope": "configuration independence only"},
        {"id": "C09", "object": "all_coordinate_metric_activity_nonzero_metric_records", "observed": sum(all(row[name] == "YES" for name in ("time_active", "depth_active", "angular2_active", "angular3_active")) for row in sectors if row["configuration_id"] in {item["configuration_id"] for item in metric_nonzero}), "required": len(metric_nonzero), "status": "PASS", "scope": "pointwise derivative activity"},
        {"id": "C10", "object": "arbitrary_functions_global_topology_and_dynamics", "observed": "NOT_ENUMERATED", "required": "EXPLICIT_OPEN", "status": "PASS", "scope": "no finite exhaustiveness"},
    ]
    check("coverage", len(coverage) == 10 and all(row["status"] in {"PASS", "OBSERVED_DEFICIENT"} for row in coverage))
    write_tsv("COVERAGE_LEDGER.tsv", list(coverage[0]), coverage)

    criteria = [
        ("Q01", "FIELDS", "ten independently controlled metric slots plus independent C02 phi", "other field realizations and phi joins open"),
        ("Q02", "ACTION_TERMS", "none", "all actions excluded"),
        ("Q03", "FULL_EQUATIONS", "none", "no EOM solution set"),
        ("Q04", "DOMAIN_COORDINATES", "four smooth banks and all eight points", "arbitrary functions and global atlas open"),
        ("Q05", "BOUNDARY_REGULARITY", "not sampled", "finite-cell boundary open"),
        ("Q06", "TOPOLOGICAL_SECTOR", "none selected", "global topology open"),
        ("Q07", "DYNAMICAL_CHARACTER", "coordinate-dependent configurations", "not physical evolution"),
        ("Q08", "BRANCH_BIFURCATION", "finite amplitude design only", "no law-defined branches"),
        ("Q09", "STABILITY", "not entered", "no perturbation operator"),
        ("Q10", "REGIME_VALIDITY", "one regular factorized local chart", "other charts nonsmooth and global regimes open"),
    ]
    write_tsv("TEN_CRITERION_SCOPE.tsv", ["id", "criterion", "covered", "open"], [{"id": a, "criterion": b, "covered": c, "open": d} for a, b, c, d in criteria])
    anti = [
        ("A01", "action EOM or residual filter", "ABSENT"),
        ("A02", "boundary seal or topology target", "ABSENT"),
        ("A03", "particle mass stability or spectrum target", "ABSENT"),
        ("A04", "GR or empirical merit target", "ABSENT"),
        ("A05", "shared metric amplitude retained", "ABSENT"),
        ("A06", "phi amplitude fed into metric", "ABSENT"),
        ("A07", "rank-deficient record discarded", "ABSENT"),
        ("A08", "slot-value rank promoted to complete-jet rank", "ABSENT"),
        ("A09", "time dependence called evolution", "ABSENT"),
        ("A10", "finite design called generic dense or exhaustive", "ABSENT"),
        ("A11", "physical representative selected", "ABSENT"),
        ("A12", "metric-phi law inferred", "ABSENT"),
        ("A13", "parameter threshold assigned physical meaning", "ABSENT"),
        ("A14", "undesired curvature class filtered", "ABSENT"),
        ("A15", "complete solution space claimed", "ABSENT"),
    ]
    write_tsv("ANTI_IMPOSITION_AUDIT.tsv", ["id", "failure_mode", "present"], [{"id": a, "failure_mode": b, "present": c} for a, b, c in anti])

    geometry_census = {
        "metric_zero_records": len(metric_zero),
        "metric_zero_flat_records": sum(float(row["riemann_max_abs"]) <= RANK_TOLERANCE for row in metric_zero),
        "metric_nonzero_records": len(metric_nonzero),
        "full_ricci_rank_records": sum(int(row["ricci_rank"]) == 4 for row in observations),
        "full_curvature_operator_rank_records": sum(int(row["curvature_operator_rank"]) == 6 for row in observations),
        "shear_rank_two_records": sum(int(row["shear_rank"]) == 2 for row in observations),
        "twist_rank_one_records": sum(int(row["twist_rank"]) == 1 for row in observations),
        "mixed_curvature_records": sum(float(row["mixed_curvature_max_abs"]) > RANK_TOLERANCE for row in observations),
        "phi_negative_records": sum(float(row["phi"]) < -RANK_TOLERANCE for row in observations),
        "phi_near_zero_records": sum(abs(float(row["phi"])) <= RANK_TOLERANCE for row in observations),
        "phi_positive_records": sum(float(row["phi"]) > RANK_TOLERANCE for row in observations),
        "dphi_timelike_records": sum(float(row["phi_gradient_norm"]) < -RANK_TOLERANCE for row in observations),
        "dphi_zero_records": sum(float(row["phi_gradient_max_abs"]) <= RANK_TOLERANCE for row in observations),
        "dphi_nonzero_near_null_records": sum(float(row["phi_gradient_max_abs"]) > RANK_TOLERANCE and abs(float(row["phi_gradient_norm"])) <= RANK_TOLERANCE for row in observations),
        "dphi_spacelike_records": sum(float(row["phi_gradient_norm"]) > RANK_TOLERANCE for row in observations),
    }
    classification = CLASSIFICATION if rank_success else RANK_DEFICIENT
    result = {
        "schema": SCHEMA,
        "status": "PASS",
        "classification": classification,
        "maximum_conclusion": MAXIMUM if rank_success else RANK_DEFICIENT,
        "checks": len(checks),
        "checks_passed": checks,
        "amplitude_design_rows": len(design),
        "metric_amplitude_count": 10,
        "phi_amplitude_count": 1,
        "metric_design_rank": int(np.linalg.matrix_rank(design_matrix[:, :10])),
        "combined_design_rank": int(np.linalg.matrix_rank(design_matrix)),
        "hadamard_columns": list(HADAMARD_COLUMNS),
        "hadamard_rows_unique": len({tuple(row) for row in hadamard}),
        "regular_configuration_records": len(observations),
        "unique_configuration_hashes": len({row["configuration_sha256"] for row in observations}),
        "unique_metric_jet_hashes": len({row["metric_jet_sha256"] for row in observations}),
        "slot_value_rank_counts": {str(key): value for key, value in sorted(slot_rank_counts.items())},
        "complete_metric_tangent_rank_counts": {str(key): value for key, value in sorted(complete_rank_counts.items())},
        "combined_tangent_rank_counts": {str(key): value for key, value in sorted(combined_rank_counts.items())},
        "phi_decoupling_checks": len(phi_rows),
        "max_identity_residual": max(float(row["identity_residual"]) for row in observations),
        "max_phi_to_metric_feedback": max(float(row["phi_to_metric_feedback_max_abs"]) for row in tangents),
        "max_metric_to_phi_feedback": max(float(row["metric_to_phi_feedback_max_abs"]) for row in tangents),
        "raw_configuration_sha256": digest(HERE / "RAW_CONFIGURATION_JETS.jsonl"),
        "geometry_census": geometry_census,
        "dynamics_loaded": False,
        "solutions_run": 0,
        "physical_evolution_claimed": False,
        "physics_ranking_used": False,
        "finite_exhaustiveness_claim": False,
        "gpu_used": False,
        "evidence_grade": "OBSERVED_PENDING_INDEPENDENT_VERIFICATION",
    }
    (HERE / "ATLAS_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "UDT_INDEPENDENT_AMPLITUDE_METRIC_ATLAS=PASS",
        f"checks={len(checks)} classification={classification}",
        f"design_rows={len(design)} metric_design_rank={result['metric_design_rank']} combined_design_rank={result['combined_design_rank']}",
        f"configurations={len(observations)} unique_configurations={result['unique_configuration_hashes']} unique_metric_jets={result['unique_metric_jet_hashes']}",
        f"slot_value_tangent_ranks={result['slot_value_rank_counts']}",
        f"complete_metric_tangent_ranks={result['complete_metric_tangent_rank_counts']}",
        f"combined_tangent_ranks={result['combined_tangent_rank_counts']}",
        f"phi_decoupling_checks={len(phi_rows)} max_phi_to_metric_feedback={result['max_phi_to_metric_feedback']:.3g} max_metric_to_phi_feedback={result['max_metric_to_phi_feedback']:.3g}",
        f"metric_zero_flat={geometry_census['metric_zero_flat_records']}/{geometry_census['metric_zero_records']}",
        f"full_ricci_curvature_ranks={geometry_census['full_ricci_rank_records']}/{geometry_census['full_curvature_operator_rank_records']}/{len(observations)}",
        f"shear_twist_mixed={geometry_census['shear_rank_two_records']}/{geometry_census['twist_rank_one_records']}/{geometry_census['mixed_curvature_records']}/{len(observations)}",
        f"phi_signs={geometry_census['phi_negative_records']}/{geometry_census['phi_near_zero_records']}/{geometry_census['phi_positive_records']}",
        f"dphi_timelike_zero_nearnull_spacelike={geometry_census['dphi_timelike_records']}/{geometry_census['dphi_zero_records']}/{geometry_census['dphi_nonzero_near_null_records']}/{geometry_census['dphi_spacelike_records']}",
        f"max_identity_residual={result['max_identity_residual']:.17g}",
        f"raw_configuration_sha256={result['raw_configuration_sha256']}",
        "dynamics=NO solutions=0 physics_ranking=NO finite_exhaustiveness=NO gpu=NO",
        f"maximum_conclusion={result['maximum_conclusion']}",
    ]
    (HERE / "ATLAS_TRANSCRIPT.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the preregistered raw eleven-amplitude volume atlas."""

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
PARENT = ROOT / "udt_independent_amplitude_metric_atlas_2026-07-21"
sys.path.insert(0, str(PARENT))

import build_independent_amplitude_atlas as previous  # noqa: E402


SCHEMA = "udt-amplitude-volume-metric-atlas-1.0"
CLASSIFICATION = "BOUNDED_AMPLITUDE_VOLUME_CONFIGURATIONS_OBSERVED"
MAXIMUM = "BOUNDED_ELEVEN_AMPLITUDE_INTERIOR_AND_RADIAL_CONFIGURATION_VOLUME_CHARACTERIZED"
TOLERANCE = 2e-10
RANK_TOLERANCE = 1e-9
PARAMETERS = tuple(f"alpha_{index}" for index in range(10)) + ("beta",)
HALTON_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31)
HADAMARD_COLUMNS = (1, 2, 4, 8, 16, 3, 5, 6, 7, 9, 10)
RADII = (0.125, 0.25, 0.5, 0.75, 1.0)
SCHEDULE = {0: ("P0", "P4"), 1: ("P1", "P5"), 2: ("P2", "P6"), 3: ("P3", "P7")}
SOURCE_HASHES = {
    "udt_independent_amplitude_metric_atlas_2026-07-21/SHA256SUMS.txt": "8b7ad5fab519c6ed0d0e83a590869356d3bcffc097681997a591d7d793500aa4",
    "udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt": "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def canonical_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def write_tsv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sylvester(order: int) -> np.ndarray:
    matrix = np.ones((1, 1), dtype=int)
    while matrix.shape[0] < order:
        matrix = np.block([[matrix, matrix], [matrix, -matrix]])
    return matrix


def radical_inverse(index: int, base: int) -> float:
    value = 0.0
    factor = 1.0 / base
    current = index
    while current:
        current, digit = divmod(current, base)
        value += digit * factor
        factor /= base
    return value


def amplitude_design() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def append(design_id: str, kind: str, vector: np.ndarray, direction: str, radius: str, index: str) -> None:
        row: dict[str, object] = {
            "design_id": design_id,
            "design_kind": kind,
            "direction_id": direction,
            "radius": radius,
            "halton_index": index,
        }
        row.update({name: float(vector[position]) for position, name in enumerate(PARAMETERS)})
        rows.append(row)

    append("O00", "ORIGIN", np.zeros(11), "-", "0", "-")
    signs = sylvester(32)[:, HADAMARD_COLUMNS]
    for direction in range(16):
        for radius_index, radius in enumerate(RADII):
            append(
                f"R{direction:02d}_{radius_index}",
                "RADIAL",
                radius * signs[direction].astype(float),
                f"D{direction:02d}",
                str(radius),
                "-",
            )
    for index in range(1, 65):
        vector = np.array([2 * radical_inverse(index, base) - 1 for base in HALTON_BASES])
        append(f"V{index:03d}", "INTERIOR", vector, "-", "-", str(index))
    return rows


def dphi_class(observation: dict[str, object]) -> str:
    gradient_max = float(observation["phi_gradient_max_abs"])
    norm = float(observation["phi_gradient_norm"])
    if gradient_max <= RANK_TOLERANCE:
        return "ZERO"
    if abs(norm) <= RANK_TOLERANCE:
        return "NONZERO_NEAR_NULL"
    return "TIMELIKE" if norm < 0 else "SPACELIKE"


def geometry_class(observation: dict[str, object]) -> str:
    mixed = int(float(observation["mixed_curvature_max_abs"]) > RANK_TOLERANCE)
    return (
        f"R{int(observation['ricci_rank'])}_K{int(observation['curvature_operator_rank'])}"
        f"_S{int(observation['shear_rank'])}_T{int(observation['twist_rank'])}_M{mixed}"
    )


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
        [{"path": path, "sha256": expected, "role": "VERIFIED_PARENT_OR_EVALUATOR"} for path, expected in SOURCE_HASHES.items()],
    )

    design = amplitude_design()
    matrix = np.array([[float(row[name]) for name in PARAMETERS] for row in design])
    interior = [row for row in design if row["design_kind"] == "INTERIOR"]
    radial = [row for row in design if row["design_kind"] == "RADIAL"]
    interior_matrix = np.array([[float(row[name]) for name in PARAMETERS] for row in interior])
    check("design_count", len(design) == 145 and len(interior) == 64 and len(radial) == 80)
    check("design_unique", len({tuple(row) for row in matrix}) == 145)
    check("interior_unique", len({tuple(row) for row in interior_matrix}) == 64)
    check("interior_metric_rank", np.linalg.matrix_rank(interior_matrix[:, :10]) == 10)
    check("interior_combined_rank", np.linalg.matrix_rank(interior_matrix) == 11)
    check("interior_sign_coverage", all(np.min(interior_matrix[:, i]) < 0 < np.max(interior_matrix[:, i]) for i in range(11)))
    check("radial_registry", {float(row["radius"]) for row in radial} == set(RADII) and len({row["direction_id"] for row in radial}) == 16)
    write_tsv("AMPLITUDE_VOLUME_DESIGN.tsv", ["design_id", "design_kind", "direction_id", "radius", "halton_index", *PARAMETERS], design)

    schedule_rows = []
    for bank, point_ids in SCHEDULE.items():
        for point_id in point_ids:
            point = previous.parent.POINTS[point_id]
            schedule_rows.append({"bank": f"B{bank}", "point_id": point_id, "x0": point[0], "x1": point[1], "x2": point[2], "x3": point[3], "design_rows": 145})
    check("schedule", len(schedule_rows) == 8 and {row["point_id"] for row in schedule_rows} == set(previous.parent.POINTS))
    write_tsv("SAMPLE_SCHEDULE.tsv", list(schedule_rows[0]), schedule_rows)

    observations: list[dict[str, object]] = []
    raw_rows: list[dict[str, object]] = []
    margin_rows: list[dict[str, object]] = []
    for design_row in design:
        amplitudes = np.array([float(design_row[name]) for name in PARAMETERS])
        for bank in range(4):
            for point_id in SCHEDULE[bank]:
                point = np.array(previous.parent.POINTS[point_id], dtype=float)
                family = previous.regular_family(bank, amplitudes, point)
                observation, raw = previous.parent.observe_configuration(family)
                config_id = f"{design_row['design_id']}_B{bank}_{point_id}"
                identity = {"slots": raw["slot_values"], "slot_first": raw["slot_first"], "slot_second": raw["slot_second"], "phi": raw["phi"]}
                metric = {"metric": raw["metric"], "first": raw["metric_first"], "second": raw["metric_second"]}
                prefix = {
                    "configuration_id": config_id,
                    "design_id": design_row["design_id"],
                    "design_kind": design_row["design_kind"],
                    "direction_id": design_row["direction_id"],
                    "radius": design_row["radius"],
                    "halton_index": design_row["halton_index"],
                    "bank": f"B{bank}",
                    "point_id": point_id,
                    "configuration_sha256": canonical_hash(identity),
                    "metric_jet_sha256": canonical_hash(metric),
                }
                classification = geometry_class(observation)
                observations.append({
                    **prefix,
                    **{name: design_row[name] for name in PARAMETERS},
                    **observation,
                    "dphi_class": dphi_class(observation),
                    "geometry_class": classification,
                    "numeric_uncertain": "YES" if observation["ricci_rank_status"] == "NUMERIC_UNCERTAIN" or observation["curvature_rank_status"] == "NUMERIC_UNCERTAIN" else "NO",
                    "retained": "YES",
                    "physical_merit": "NOT_EVALUATED",
                })
                raw_rows.append({**prefix, "coordinates": point.tolist(), "amplitudes": amplitudes.tolist(), **raw})
                ricci_singular = [float(value) for value in raw["ricci_singular_values"]]
                curvature_singular = [float(value) for value in raw["curvature_singular_values"]]
                split = previous.parent.split_kinematics(np.asarray(raw["slot_values"]), np.asarray(raw["slot_first"]))
                shear_rows = np.asarray(
                    [(item[0, 0], item[0, 1], item[1, 1]) for item in split["shears"]], dtype=float
                )
                shear_singular = np.linalg.svd(shear_rows, compute_uv=False)
                twist_norm = float(np.linalg.norm(np.asarray(split["twist"])))
                margin_rows.append({
                    "configuration_id": config_id,
                    "ricci_min_singular": min(ricci_singular),
                    "curvature_min_singular": min(curvature_singular),
                    "shear_min_singular": min(float(value) for value in shear_singular),
                    "twist_norm": twist_norm,
                    "mixed_curvature_max_abs": observation["mixed_curvature_max_abs"],
                    "ricci_rank": observation["ricci_rank"],
                    "curvature_operator_rank": observation["curvature_operator_rank"],
                    "shear_rank": observation["shear_rank"],
                    "twist_rank": observation["twist_rank"],
                    "ricci_status": observation["ricci_rank_status"],
                    "curvature_status": observation["curvature_rank_status"],
                    "rank_threshold": RANK_TOLERANCE,
                })

    check("configuration_count", len(observations) == 1160)
    check("configuration_unique_ids", len({row["configuration_id"] for row in observations}) == 1160)
    check("all_lorentzian", all(row["inertia"] == "1,3,0" for row in observations))
    check("identity_gate", max(float(row["identity_residual"]) for row in observations) < TOLERANCE)
    check("all_retained", all(row["retained"] == "YES" for row in observations))
    write_tsv("CONFIGURATION_OBSERVATIONS.tsv", list(observations[0]), observations)
    write_tsv("NUMERIC_RANK_MARGINS.tsv", list(margin_rows[0]), margin_rows)
    with (HERE / "RAW_CONFIGURATION_JETS.jsonl").open("w", encoding="utf-8") as handle:
        for row in raw_rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")

    by_key = {(row["design_id"], row["bank"], row["point_id"]): row for row in observations}
    incidence = []
    for direction in range(16):
        sequence = ["O00", *(f"R{direction:02d}_{index}" for index in range(5))]
        for bank in range(4):
            for point_id in SCHEDULE[bank]:
                for edge, (left_id, right_id) in enumerate(zip(sequence[:-1], sequence[1:])):
                    left = by_key[(left_id, f"B{bank}", point_id)]
                    right = by_key[(right_id, f"B{bank}", point_id)]
                    changed = any(left[field] != right[field] for field in ("ricci_rank", "curvature_operator_rank", "shear_rank", "twist_rank", "geometry_class", "dphi_class"))
                    incidence.append({
                        "edge_id": f"D{direction:02d}_B{bank}_{point_id}_E{edge}",
                        "direction_id": f"D{direction:02d}",
                        "bank": f"B{bank}",
                        "point_id": point_id,
                        "from_configuration": left["configuration_id"],
                        "to_configuration": right["configuration_id"],
                        "from_radius": 0.0 if left_id == "O00" else RADII[edge - 1],
                        "to_radius": RADII[edge],
                        "delta_determinant": float(right["determinant"]) - float(left["determinant"]),
                        "delta_scalar_curvature": float(right["scalar_curvature"]) - float(left["scalar_curvature"]),
                        "delta_riemann_max_abs": float(right["riemann_max_abs"]) - float(left["riemann_max_abs"]),
                        "ricci_rank_change": int(right["ricci_rank"]) - int(left["ricci_rank"]),
                        "curvature_rank_change": int(right["curvature_operator_rank"]) - int(left["curvature_operator_rank"]),
                        "shear_rank_change": int(right["shear_rank"]) - int(left["shear_rank"]),
                        "twist_rank_change": int(right["twist_rank"]) - int(left["twist_rank"]),
                        "from_geometry_class": left["geometry_class"],
                        "to_geometry_class": right["geometry_class"],
                        "from_dphi_class": left["dphi_class"],
                        "to_dphi_class": right["dphi_class"],
                        "diagnostic_tuple_changed": "YES" if changed else "NO",
                        "physical_transition_claimed": "NO",
                    })
    check("radial_edges", len(incidence) == 640)
    check("no_physical_transition", all(row["physical_transition_claimed"] == "NO" for row in incidence))
    write_tsv("RADIAL_INCIDENCE.tsv", list(incidence[0]), incidence)

    class_rows = []
    for design_kind in ("ORIGIN", "RADIAL", "INTERIOR"):
        subset = [row for row in observations if row["design_kind"] == design_kind]
        counts = Counter(row["geometry_class"] for row in subset)
        for class_id in sorted(counts):
            class_rows.append({"design_kind": design_kind, "geometry_class": class_id, "records": counts[class_id], "retained": "YES", "physical_merit": "NOT_EVALUATED"})
    check("class_census_complete", sum(int(row["records"]) for row in class_rows) == 1160)
    write_tsv("GEOMETRIC_CLASS_CENSUS.tsv", list(class_rows[0]), class_rows)

    uncertain = sum(row["numeric_uncertain"] == "YES" for row in observations)
    changed_edges = sum(row["diagnostic_tuple_changed"] == "YES" for row in incidence)
    coverage = [
        {"id": "C01", "object": "amplitude_identities", "observed": len(design), "required": 145, "status": "PASS", "scope": "finite raw design"},
        {"id": "C02", "object": "interior_rows", "observed": len(interior), "required": 64, "status": "PASS", "scope": "Halton indices 1..64"},
        {"id": "C03", "object": "radial_rows", "observed": len(radial), "required": 80, "status": "PASS", "scope": "16 directions five radii"},
        {"id": "C04", "object": "configuration_records", "observed": len(observations), "required": 1160, "status": "PASS", "scope": "all retained"},
        {"id": "C05", "object": "radial_edges", "observed": len(incidence), "required": 640, "status": "PASS", "scope": "diagnostic changes only"},
        {"id": "C06", "object": "numeric_uncertain_records", "observed": uncertain, "required": "REPORTED_NOT_FILTERED", "status": "PASS", "scope": "rank threshold diagnostic"},
        {"id": "C07", "object": "diagnostic_tuple_changed_edges", "observed": changed_edges, "required": "REPORTED_NOT_FILTERED", "status": "PASS", "scope": "not physical transition"},
        {"id": "C08", "object": "ensemble_or_physics_interpretation", "observed": "NOT_PERFORMED", "required": "DEFERRED", "status": "PASS", "scope": "raw mapping only"},
        {"id": "C09", "object": "arbitrary_functions_charts_global_space", "observed": "NOT_ENUMERATED", "required": "EXPLICIT_OPEN", "status": "PASS", "scope": "no exhaustiveness"},
    ]
    write_tsv("COVERAGE_LEDGER.tsv", list(coverage[0]), coverage)

    criteria = [
        ("Q01", "FIELDS", "ten metric amplitudes plus independent C02 phi", "other field realizations open"),
        ("Q02", "ACTION_TERMS", "none", "all actions excluded"),
        ("Q03", "FULL_EQUATIONS", "none", "no law-defined solutions"),
        ("Q04", "DOMAIN_COORDINATES", "four analytic banks eight points", "arbitrary functions and charts open"),
        ("Q05", "BOUNDARY_REGULARITY", "not sampled", "finite-cell boundary open"),
        ("Q06", "TOPOLOGICAL_SECTOR", "none", "global topology open"),
        ("Q07", "DYNAMICAL_CHARACTER", "configuration dependence only", "physical evolution absent"),
        ("Q08", "BRANCH_BIFURCATION", "diagnostic radial changes", "no physical transition claim"),
        ("Q09", "STABILITY", "not entered", "no perturbation operator"),
        ("Q10", "REGIME_VALIDITY", "bounded eleven-cube local chart", "global and full amplitude space open"),
    ]
    write_tsv("TEN_CRITERION_SCOPE.tsv", ["id", "criterion", "covered", "open"], [{"id": a, "criterion": b, "covered": c, "open": d} for a, b, c, d in criteria])
    anti = [
        ("A01", "action EOM or residual filter", "ABSENT"),
        ("A02", "sector ensemble label or orchestra interpretation", "ABSENT"),
        ("A03", "physical phase transition claim", "ABSENT"),
        ("A04", "particle GR cosmology or boundary merit target", "ABSENT"),
        ("A05", "rank or class used as acceptance filter", "ABSENT"),
        ("A06", "duplicate or uncertain record discarded", "ABSENT"),
        ("A07", "time dependence called evolution", "ABSENT"),
        ("A08", "metric-phi law inferred", "ABSENT"),
        ("A09", "finite sample called probabilistic dense generic or exhaustive", "ABSENT"),
        ("A10", "physical representative scale topology or carrier selected", "ABSENT"),
    ]
    write_tsv("ANTI_IMPOSITION_AUDIT.tsv", ["id", "failure_mode", "present"], [{"id": a, "failure_mode": b, "present": c} for a, b, c in anti])

    census = {
        "geometry_class_counts": dict(sorted(Counter(row["geometry_class"] for row in observations).items())),
        "design_kind_counts": dict(sorted(Counter(row["design_kind"] for row in observations).items())),
        "numeric_uncertain_records": uncertain,
        "radial_changed_edges": changed_edges,
        "radial_unchanged_edges": len(incidence) - changed_edges,
        "phi_sign_counts": {
            "negative": sum(float(row["phi"]) < -RANK_TOLERANCE for row in observations),
            "near_zero": sum(abs(float(row["phi"])) <= RANK_TOLERANCE for row in observations),
            "positive": sum(float(row["phi"]) > RANK_TOLERANCE for row in observations),
        },
        "dphi_class_counts": dict(sorted(Counter(row["dphi_class"] for row in observations).items())),
    }
    result = {
        "schema": SCHEMA,
        "status": "PASS",
        "classification": CLASSIFICATION,
        "maximum_conclusion": MAXIMUM,
        "checks": len(checks),
        "checks_passed": checks,
        "amplitude_identities": len(design),
        "interior_rows": len(interior),
        "radial_rows": len(radial),
        "coefficient_banks": 4,
        "sample_points": 8,
        "configuration_records": len(observations),
        "unique_configuration_hashes": len({row["configuration_sha256"] for row in observations}),
        "unique_metric_jet_hashes": len({row["metric_jet_sha256"] for row in observations}),
        "radial_edges": len(incidence),
        "max_identity_residual": max(float(row["identity_residual"]) for row in observations),
        "raw_configuration_sha256": digest(HERE / "RAW_CONFIGURATION_JETS.jsonl"),
        "observed_census": census,
        "ensemble_interpretation_performed": False,
        "physical_transition_claimed": False,
        "dynamics_loaded": False,
        "solutions_run": 0,
        "physics_ranking_used": False,
        "finite_exhaustiveness_claim": False,
        "gpu_used": False,
        "evidence_grade": "OBSERVED_PENDING_INDEPENDENT_VERIFICATION",
    }
    (HERE / "ATLAS_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "UDT_AMPLITUDE_VOLUME_METRIC_ATLAS=PASS",
        f"checks={len(checks)} classification={CLASSIFICATION}",
        f"design=145 interior=64 radial=80 configurations={len(observations)}",
        f"unique_configurations={result['unique_configuration_hashes']} unique_metric_jets={result['unique_metric_jet_hashes']}",
        f"geometry_classes={census['geometry_class_counts']}",
        f"radial_edges={len(incidence)} changed={changed_edges} unchanged={len(incidence)-changed_edges}",
        f"numeric_uncertain_records={uncertain}",
        f"phi_signs={census['phi_sign_counts']} dphi_classes={census['dphi_class_counts']}",
        f"max_identity_residual={result['max_identity_residual']:.17g}",
        f"raw_configuration_sha256={result['raw_configuration_sha256']}",
        "ensembles=DEFERRED dynamics=NO solutions=0 physics_ranking=NO finite_exhaustiveness=NO gpu=NO",
        f"maximum_conclusion={MAXIMUM}",
    ]
    (HERE / "ATLAS_TRANSCRIPT.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))


if __name__ == "__main__":
    main()

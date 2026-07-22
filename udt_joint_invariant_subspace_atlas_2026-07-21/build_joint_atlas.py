#!/usr/bin/env python3
"""Build the preregistered metric/phi joint invariant-subspace atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from collections import Counter
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_structural_ensemble_metric_atlas_2026-07-21"
EVALUATOR = ROOT / "udt_canonical_geometry_evaluator_p01_2026-07-21"
sys.path.insert(0, str(EVALUATOR))
sys.path.insert(0, str(HERE))

from canonical_geometry_evaluator import Jet2, MetricJets, evaluate_metric_jets  # noqa: E402
from invariant_subspace_core import (  # noqa: E402
    FAMILY_REGISTRY,
    PAIRS,
    bivector_eigenplanes,
    classify_family,
    family_operators,
    intrinsic_objects,
    nonlinear_transform_jets,
    nonlinear_transforms,
    relmax,
)


SCHEMA = "udt-joint-invariant-subspace-atlas-1.0"
MAXIMUM = "BOUNDED_POINTWISE_JOINT_INVARIANT_SUBSPACE_ATLAS_CHARACTERIZED"
SOURCE_HASHES = {
    "udt_structural_ensemble_metric_atlas_2026-07-21/SHA256SUMS.txt": "3d569ed31506f5f7ce44beac30e8419571f734b3973dcc34d6c474bf78636757",
    "udt_chart_coframe_invariance_atlas_2026-07-21/SHA256SUMS.txt": "082c41bea96e99611d3fc89a135692058e346665b4b1520d7f6d790788a0cf09",
    "udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt": "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad",
}
PREREG_HASHES = {
    "PREREGISTRATION.md": "411545435b04aae96d315ce26ba4994b054176dd26177f89229324a40cf1a6c0",
    "PREREGISTRATION_CORRECTION.md": "b600d8c2e2525b5b8eeac0cc954a33ec6f5a9b1ea38d9669476e1f7a8ec6cfc9",
}
COMPARISON_FIELDS = (
    "algebra_dimension", "commutant_dimension", "commutant_center_dimension",
    "selfadjoint_center_dimension", "central_block_ranks", "central_rank2_split_count",
    "central_block_status", "gradient_orbit_dimension", "gradient_orbit_metric_rank",
    "gradient_orbit_signature", "reducibility_class",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def check_sources() -> list[dict[str, object]]:
    rows = []
    for relative, expected in SOURCE_HASHES.items():
        path = ROOT / relative
        actual = digest(path)
        if actual != expected:
            raise AssertionError(f"source manifest {relative}: {actual}")
        rows.append({"path": relative, "sha256": actual, "role": "IMMUTABLE_SOURCE"})
    for relative, expected in PREREG_HASHES.items():
        path = HERE / relative
        actual = digest(path)
        if actual != expected:
            raise AssertionError(f"preregistration {relative}: {actual}")
        rows.append({"path": relative, "sha256": actual, "role": "PREREGISTRATION"})
    return rows


def operator_adjoint_residuals(objects: dict[str, object]) -> tuple[float, float]:
    metric = np.asarray(objects["metric"])
    self_residual = max(
        relmax(np.asarray(objects[name]).T @ metric, metric @ np.asarray(objects[name]))
        for name in ("R", "H", "D")
    )
    skew_residual = max(
        relmax(operator.T @ metric, -metric @ operator)
        for name in ("RG", "WG") for operator in objects[name]
    )
    return self_residual, skew_residual


def family_rows(configuration_id: str, objects: dict[str, object]) -> list[dict[str, object]]:
    rows = []
    for family_id, keys in FAMILY_REGISTRY:
        classification = classify_family(family_operators(objects, keys), np.asarray(objects["gradient"]), np.asarray(objects["metric"]))
        rows.append({"configuration_id": configuration_id, "family_id": family_id, "operator_keys": ";".join(keys), **classification})
    return rows


def bivector_rows(configuration_id: str, objects: dict[str, object]) -> tuple[dict[str, object], list[dict[str, object]]]:
    summary: dict[str, object] = {}
    rows: list[dict[str, object]] = []
    for name, key in (("RIEMANN", "riemann_down"), ("WEYL", "weyl_down")):
        current, candidates = bivector_eigenplanes(name, np.asarray(objects[key]), np.asarray(objects["inverse"]), np.asarray(objects["metric"]))
        for field, value in current.items():
            summary[f"{name.lower()}_{field}"] = value
        for index, candidate in enumerate(candidates):
            rows.append({"configuration_id": configuration_id, "candidate_id": f"{name}_E{index:02d}", **candidate})
    return summary, rows


def expected_generator_residual(original_geometry, original_objects, transformed_objects, transform) -> float:
    j = np.asarray(transform["J"], dtype=float)
    inverse_j = np.linalg.inv(j)
    maximum = 0.0
    weyl_up = np.einsum("ar,rsuv->asuv", np.asarray(original_objects["inverse"]), np.asarray(original_objects["weyl_down"]))
    for destination_index, (a, b) in enumerate(PAIRS):
        expected_r = np.zeros((4, 4))
        expected_w = np.zeros((4, 4))
        for mu in range(4):
            for nu in range(4):
                expected_r += j[mu, a] * j[nu, b] * inverse_j @ original_geometry.riemann_up[:, :, mu, nu] @ j
                expected_w += j[mu, a] * j[nu, b] * inverse_j @ weyl_up[:, :, mu, nu] @ j
        maximum = max(
            maximum,
            relmax(transformed_objects["RG"][destination_index], expected_r),
            relmax(transformed_objects["WG"][destination_index], expected_w),
        )
    return maximum


def covariance_residual(original_geometry, original_objects, transformed_objects, transform) -> dict[str, float]:
    j = np.asarray(transform["J"], dtype=float)
    inverse_j = np.linalg.inv(j)
    residuals = {
        "metric": relmax(transformed_objects["metric"], j.T @ original_objects["metric"] @ j),
        "gradient": relmax(transformed_objects["gradient"], inverse_j @ original_objects["gradient"]),
        "ricci_operator": relmax(transformed_objects["R"], inverse_j @ original_objects["R"] @ j),
        "hessian_operator": relmax(transformed_objects["H"], inverse_j @ original_objects["H"] @ j),
        "phi_dyad": relmax(transformed_objects["D"], inverse_j @ original_objects["D"] @ j),
        "curvature_generators": expected_generator_residual(original_geometry, original_objects, transformed_objects, transform),
    }
    residuals["maximum"] = max(residuals.values())
    return residuals


def main() -> None:
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    jordan_metric=np.array(((0.0,1.0,0.0,0.0),(1.0,0.0,0.0,0.0),(0.0,0.0,1.0,0.0),(0.0,0.0,0.0,1.0)))
    jordan=np.zeros((4,4));jordan[0,1]=1.0
    jordan_result=classify_family([jordan],np.zeros(4),jordan_metric)
    if jordan_result["numeric_status"]!="NUMERIC_UNCERTAIN" or jordan_result["central_block_status"]!="NUMERIC_UNCERTAIN_CENTRAL_BLOCKS":
        raise AssertionError("defective Jordan primary did not fail closed")
    source_rows = check_sources()
    transforms = nonlinear_transforms()
    family_atlas: list[dict[str, object]] = []
    configuration_atlas: list[dict[str, object]] = []
    eigenplane_atlas: list[dict[str, object]] = []
    nonlinear_configurations: list[dict[str, object]] = []
    nonlinear_families: list[dict[str, object]] = []
    margin_rows: list[dict[str, object]] = []
    maximum_parent_residual = 0.0
    maximum_selfadjoint_residual = 0.0
    maximum_skew_residual = 0.0
    maximum_nonlinear_covariance = 0.0
    nonlinear_discordances = 0
    nonlinear_uncertain_comparisons = 0
    seen_configurations: set[str] = set()

    shards = tsv(PARENT / "RAW_SHARD_REGISTRY.tsv")
    for shard_index, shard in enumerate(shards, start=1):
        shard_path = PARENT / shard["path"]
        if digest(shard_path) != shard["sha256"]:
            raise AssertionError(f"raw shard {shard['path']}")
        with shard_path.open(encoding="utf-8") as handle:
            raw_rows = [json.loads(line) for line in handle]
        if len(raw_rows) != int(shard["records"]):
            raise AssertionError("shard record count")
        for raw in raw_rows:
            configuration_id = raw["configuration_id"]
            if configuration_id in seen_configurations:
                raise AssertionError("duplicate configuration")
            seen_configurations.add(configuration_id)
            metric = np.asarray(raw["metric"], dtype=float)
            metric_first = np.asarray(raw["metric_first"], dtype=float)
            metric_second = np.asarray(raw["metric_second"], dtype=float)
            phi = raw["phi"]
            phi_first = np.asarray(phi["first"], dtype=float)
            phi_second = np.asarray(phi["second"], dtype=float)
            geometry = evaluate_metric_jets(MetricJets(metric, metric_first, metric_second))
            objects = intrinsic_objects(geometry, phi_first, phi_second)
            parent_residual = max(
                relmax(geometry.riemann_down, np.asarray(raw["riemann_down"])),
                relmax(geometry.ricci, np.asarray(raw["ricci"])),
                relmax(objects["weyl_down"], np.asarray(raw["weyl_down"])),
            )
            maximum_parent_residual = max(maximum_parent_residual, parent_residual)
            self_residual, skew_residual = operator_adjoint_residuals(objects)
            maximum_selfadjoint_residual = max(maximum_selfadjoint_residual, self_residual)
            maximum_skew_residual = max(maximum_skew_residual, skew_residual)
            current_family_rows = family_rows(configuration_id, objects)
            family_atlas.extend(current_family_rows)
            family_lookup = {row["family_id"]: row for row in current_family_rows}
            bivector_summary, bivector_candidates = bivector_rows(configuration_id, objects)
            eigenplane_atlas.extend(bivector_candidates)
            gradient_norm = float(phi_first @ geometry.inverse @ phi_first)
            if float(np.linalg.norm(phi_first)) <= 1.0e-12:
                gradient_class = "ZERO"
            elif abs(gradient_norm) <= 1.0e-9:
                gradient_class = "NULL"
            elif gradient_norm < 0:
                gradient_class = "TIMELIKE"
            else:
                gradient_class = "SPACELIKE"
            configuration_atlas.append({
                "configuration_id": configuration_id,
                "carrier_id": raw["carrier_id"],
                "mask_id": raw["mask_id"],
                "bank": raw["bank"],
                "point_id": raw["point_id"],
                "gradient_norm": gradient_norm,
                "gradient_class": gradient_class,
                "parent_tensor_residual": parent_residual,
                "selfadjoint_operator_residual": self_residual,
                "skew_operator_residual": skew_residual,
                **bivector_summary,
                "retained": "YES",
                "physical_merit": "NOT_EVALUATED",
            })
            for row in current_family_rows:
                if row["numeric_status"] == "NUMERIC_UNCERTAIN":
                    margin_rows.append({
                        "configuration_id": configuration_id, "probe": "ORIGINAL", "object": row["family_id"],
                        "status": row["numeric_status"], "detail": row["central_block_status"],
                    })
            for tensor in ("riemann", "weyl"):
                if bivector_summary[f"{tensor}_numeric_status"] == "NUMERIC_UNCERTAIN":
                    margin_rows.append({
                        "configuration_id": configuration_id, "probe": "ORIGINAL", "object": tensor.upper(),
                        "status": "NUMERIC_UNCERTAIN", "detail": "BIVECTOR_SPECTRUM_OR_PLANE_MARGIN",
                    })

            for transform in transforms:
                transformed = nonlinear_transform_jets(
                    metric, metric_first, metric_second, float(phi["value"]), phi_first, phi_second, transform, Jet2
                )
                transformed_geometry = evaluate_metric_jets(MetricJets(*transformed[:3]))
                transformed_objects = intrinsic_objects(transformed_geometry, transformed[4], transformed[5])
                covariance = covariance_residual(geometry, objects, transformed_objects, transform)
                maximum_nonlinear_covariance = max(maximum_nonlinear_covariance, covariance["maximum"])
                transformed_summary, _ = bivector_rows(configuration_id, transformed_objects)
                nonlinear_configurations.append({
                    "configuration_id": configuration_id,
                    "transform_id": transform["id"],
                    **{f"covariance_{name}": value for name, value in covariance.items()},
                    **transformed_summary,
                    "riemann_summary_agreement": "YES" if all(
                        transformed_summary[f"riemann_{field}"] == bivector_summary[f"riemann_{field}"]
                        for field in (
                            "isolated_real_simple_eigenplanes", "nondegenerate_simple_eigenplanes",
                            "complementary_split_count", "repeated_eigenvalue_multiplicity", "complex_isolated_count",
                        )
                    ) else "NO",
                    "weyl_summary_agreement": "YES" if all(
                        transformed_summary[f"weyl_{field}"] == bivector_summary[f"weyl_{field}"]
                        for field in (
                            "isolated_real_simple_eigenplanes", "nondegenerate_simple_eigenplanes",
                            "complementary_split_count", "repeated_eigenvalue_multiplicity", "complex_isolated_count",
                        )
                    ) else "NO",
                    "retained": "YES",
                })
                transformed_family_rows = family_rows(configuration_id, transformed_objects)
                for transformed_row in transformed_family_rows:
                    original_row = family_lookup[transformed_row["family_id"]]
                    uncertain = "NUMERIC_UNCERTAIN" in (original_row["numeric_status"], transformed_row["numeric_status"])
                    agreement = all(str(original_row[field]) == str(transformed_row[field]) for field in COMPARISON_FIELDS)
                    if uncertain:
                        status = "NUMERIC_UNCERTAIN_RETAINED"
                        nonlinear_uncertain_comparisons += 1
                    elif agreement:
                        status = "AGREE"
                    else:
                        status = "DISCORDANT"
                        nonlinear_discordances += 1
                    nonlinear_families.append({
                        "configuration_id": configuration_id,
                        "transform_id": transform["id"],
                        "family_id": transformed_row["family_id"],
                        "comparison_status": status,
                        **{f"original_{field}": original_row[field] for field in COMPARISON_FIELDS},
                        **{f"transformed_{field}": transformed_row[field] for field in COMPARISON_FIELDS},
                        "original_numeric_status": original_row["numeric_status"],
                        "transformed_numeric_status": transformed_row["numeric_status"],
                    })
                    if uncertain:
                        margin_rows.append({
                            "configuration_id": configuration_id, "probe": transform["id"],
                            "object": transformed_row["family_id"], "status": status,
                            "detail": transformed_row["central_block_status"],
                        })
        print(f"shard={shard_index}/{len(shards)} path={shard['path']} configurations={len(seen_configurations)}", flush=True)

    if len(seen_configurations) != 6144:
        raise AssertionError(f"configuration count {len(seen_configurations)}")
    if len(family_atlas) != 55296 or len(nonlinear_configurations) != 12288 or len(nonlinear_families) != 110592:
        raise AssertionError("atlas row counts")

    write_tsv("SOURCE_LINEAGE.tsv", ["path", "sha256", "role"], source_rows)
    write_tsv("OPERATOR_FAMILY_REGISTRY.tsv", ["family_id", "operator_keys", "scope"], [
        {"family_id": family_id, "operator_keys": ";".join(keys), "scope": "REGISTERED_NAMED_POINTWISE_FAMILY"}
        for family_id, keys in FAMILY_REGISTRY
    ])
    write_tsv("NONLINEAR_TRANSFORM_REGISTRY.tsv", ["transform_id", "jacobian_json", "second_jet_json", "third_jet_json", "scope"], [
        {
            "transform_id": transform["id"],
            "jacobian_json": json.dumps(np.asarray(transform["J"]).tolist(), separators=(",", ":")),
            "second_jet_json": json.dumps(np.asarray(transform["K"]).tolist(), separators=(",", ":")),
            "third_jet_json": json.dumps(np.asarray(transform["L"]).tolist(), separators=(",", ":")),
            "scope": "NONLINEAR_COORDINATE_THREE_JET_AT_POINT",
        }
        for transform in transforms
    ])
    write_tsv("CONFIGURATION_SUBSPACE_CENSUS.tsv", list(configuration_atlas[0]), configuration_atlas)
    write_tsv("FAMILY_SUBSPACE_ATLAS.tsv", list(family_atlas[0]), family_atlas)
    eigen_fields = list(eigenplane_atlas[0]) if eigenplane_atlas else [
        "configuration_id", "candidate_id", "tensor", "eigenvalue_real", "eigenvalue_gap",
        "simplicity_residual", "plane_signature", "metric_margin", "projector_json", "numeric_status",
    ]
    write_tsv("BIVECTOR_EIGENPLANE_ATLAS.tsv", eigen_fields, eigenplane_atlas)
    write_tsv("NONLINEAR_CONFIGURATION_ATLAS.tsv", list(nonlinear_configurations[0]), nonlinear_configurations)
    write_tsv("NONLINEAR_FAMILY_COMPARISON.tsv", list(nonlinear_families[0]), nonlinear_families)
    write_tsv("NUMERIC_MARGIN_LEDGER.tsv", ["configuration_id", "probe", "object", "status", "detail"], margin_rows)

    family_census = Counter(
        (row["family_id"], row["reducibility_class"], row["central_block_status"], row["gradient_orbit_dimension"], row["gradient_orbit_signature"], row["numeric_status"])
        for row in family_atlas
    )
    write_tsv("FAMILY_CLASS_CENSUS.tsv", [
        "family_id", "reducibility_class", "central_block_status", "gradient_orbit_dimension",
        "gradient_orbit_signature", "numeric_status", "configurations",
    ], [
        {
            "family_id": key[0], "reducibility_class": key[1], "central_block_status": key[2],
            "gradient_orbit_dimension": key[3], "gradient_orbit_signature": key[4],
            "numeric_status": key[5], "configurations": count,
        }
        for key, count in sorted(family_census.items())
    ])
    family_lookup_all = {(row["configuration_id"], row["family_id"]): row for row in family_atlas}
    escalation_census = Counter()
    for row in family_atlas:
        if row["central_rank2_split_count"] != 1:
            continue
        configuration_id = row["configuration_id"]
        escalation_census[(
            row["family_id"],
            family_lookup_all[(configuration_id, "F08_FULL_RIEMANN_JOINT")]["reducibility_class"],
            family_lookup_all[(configuration_id, "F09_FULL_WEYL_JOINT")]["reducibility_class"],
        )] += 1
    write_tsv("UNIQUE_SPLIT_ESCALATION_CENSUS.tsv", [
        "source_family", "full_riemann_joint_class", "full_weyl_joint_class", "configurations",
    ], [
        {
            "source_family": key[0], "full_riemann_joint_class": key[1],
            "full_weyl_joint_class": key[2], "configurations": count,
        }
        for key, count in sorted(escalation_census.items())
    ])
    bivector_census = Counter(
        (tensor, row[f"{tensor}_isolated_real_simple_eigenplanes"], row[f"{tensor}_nondegenerate_simple_eigenplanes"],
         row[f"{tensor}_complementary_split_count"], row[f"{tensor}_repeated_eigenvalue_multiplicity"],
         row[f"{tensor}_complex_isolated_count"], row[f"{tensor}_numeric_status"])
        for row in configuration_atlas for tensor in ("riemann", "weyl")
    )
    write_tsv("BIVECTOR_CLASS_CENSUS.tsv", [
        "tensor", "isolated_real_simple_eigenplanes", "nondegenerate_simple_eigenplanes",
        "complementary_split_count", "repeated_eigenvalue_multiplicity", "complex_isolated_count",
        "numeric_status", "configurations",
    ], [
        {
            "tensor": key[0], "isolated_real_simple_eigenplanes": key[1],
            "nondegenerate_simple_eigenplanes": key[2], "complementary_split_count": key[3],
            "repeated_eigenvalue_multiplicity": key[4], "complex_isolated_count": key[5],
            "numeric_status": key[6], "configurations": count,
        }
        for key, count in sorted(bivector_census.items())
    ])
    write_tsv("COVERAGE_LEDGER.tsv", ["id", "object", "observed", "required", "status"], [
        {"id": "C01", "object": "parent configurations", "observed": len(configuration_atlas), "required": 6144, "status": "PASS"},
        {"id": "C02", "object": "family classifications", "observed": len(family_atlas), "required": 55296, "status": "PASS"},
        {"id": "C03", "object": "nonlinear configurations", "observed": len(nonlinear_configurations), "required": 12288, "status": "PASS"},
        {"id": "C04", "object": "nonlinear family comparisons", "observed": len(nonlinear_families), "required": 110592, "status": "PASS"},
        {"id": "C05", "object": "discarded configurations", "observed": 0, "required": 0, "status": "PASS"},
    ])
    write_tsv("PREMISE_STATUS_LEDGER.tsv", ["id", "premise", "status", "scope"], [
        {"id": "P01", "premise": "4D Lorentzian metric plus scalar phi two-jet", "status": "CONDITIONAL", "scope": "immutable parent realization"},
        {"id": "P02", "premise": "nine named operator families", "status": "FREE_AND_EXPLORED", "scope": "preregistered named bounded registry; other subsets open"},
        {"id": "P03", "premise": "two nonlinear coordinate three-jets", "status": "FREE_AND_EXPLORED", "scope": "finite probes not full group"},
        {"id": "P04", "premise": "rank tolerance 1e-9", "status": "PINNED_BY_HABIT", "scope": "all margins retained"},
        {"id": "P05", "premise": "eigen cluster tolerance 1e-8", "status": "PINNED_BY_HABIT", "scope": "degeneracies retained"},
        {"id": "P06", "premise": "supplied 2+2 split", "status": "ABSENT", "scope": "never loaded"},
        {"id": "P07", "premise": "action source carrier boundary scale", "status": "OPEN", "scope": "never loaded"},
    ])
    write_tsv("ANTI_IMPOSITION_AUDIT.tsv", ["id", "question", "result"], [
        {"id": "A01", "question": "Was any supplied 2+2 projector loaded?", "result": "NO"},
        {"id": "A02", "question": "Was any plane ranked by physical resemblance?", "result": "NO"},
        {"id": "A03", "question": "Were null degenerate complex repeated or uncertain rows filtered?", "result": "NO"},
        {"id": "A04", "question": "Was any action source carrier boundary or scale loaded?", "result": "NO"},
        {"id": "A05", "question": "Is the map exhaustive beyond the registered pointwise objects?", "result": "NO"},
    ])

    unique_central_rows = sum(row["central_rank2_split_count"] == 1 and row["numeric_status"] == "NUMERIC_CLASSIFIED" for row in family_atlas)
    multiple_central_rows = sum(row["central_rank2_split_count"] > 1 and row["numeric_status"] == "NUMERIC_CLASSIFIED" for row in family_atlas)
    gradient_plane_rows = sum(row["gradient_orbit_dimension"] == 2 and row["numeric_status"] == "NUMERIC_CLASSIFIED" for row in family_atlas)
    nondegenerate_gradient_plane_rows = sum(
        row["gradient_orbit_dimension"] == 2 and row["gradient_orbit_metric_rank"] == 2 and row["numeric_status"] == "NUMERIC_CLASSIFIED"
        for row in family_atlas
    )
    exact_bivector_split_rows = sum(
        row[f"{tensor}_complementary_split_count"] == 1 and row[f"{tensor}_numeric_status"] == "NUMERIC_CLASSIFIED"
        for row in configuration_atlas for tensor in ("riemann", "weyl")
    )
    result = {
        "schema": SCHEMA,
        "status": "PASS" if maximum_nonlinear_covariance <= 1.0e-9 and nonlinear_discordances == 0 else "VERIFICATION_REQUIRED",
        "maximum_conclusion": MAXIMUM,
        "configurations": len(configuration_atlas),
        "family_rows": len(family_atlas),
        "nonlinear_configuration_rows": len(nonlinear_configurations),
        "nonlinear_family_rows": len(nonlinear_families),
        "bivector_eigenplane_rows": len(eigenplane_atlas),
        "numeric_margin_rows": len(margin_rows),
        "unique_central_2plus2_rows": unique_central_rows,
        "multiple_central_2plus2_rows": multiple_central_rows,
        "gradient_generated_plane_rows": gradient_plane_rows,
        "nondegenerate_gradient_generated_plane_rows": nondegenerate_gradient_plane_rows,
        "unique_bivector_complementary_split_rows": exact_bivector_split_rows,
        "nonlinear_classification_discordances": nonlinear_discordances,
        "nonlinear_uncertain_comparisons": nonlinear_uncertain_comparisons,
        "max_parent_tensor_residual": maximum_parent_residual,
        "max_selfadjoint_operator_residual": maximum_selfadjoint_residual,
        "max_skew_operator_residual": maximum_skew_residual,
        "max_nonlinear_covariance_residual": maximum_nonlinear_covariance,
        "discarded_rows": 0,
        "supplied_split_loaded": False,
        "physical_split_selected": False,
        "action_or_equation_loaded": False,
        "full_group_claimed": False,
        "global_distribution_claimed": False,
        "gpu_used": False,
    }
    (HERE / "ATLAS_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        f"UDT_JOINT_INVARIANT_SUBSPACE_ATLAS={result['status']}",
        f"configurations={len(configuration_atlas)} families={len(family_atlas)} nonlinear_configs={len(nonlinear_configurations)} nonlinear_families={len(nonlinear_families)}",
        f"unique_central_2plus2={unique_central_rows} multiple_central_2plus2={multiple_central_rows}",
        f"gradient_planes={gradient_plane_rows} nondegenerate_gradient_planes={nondegenerate_gradient_plane_rows}",
        f"unique_bivector_splits={exact_bivector_split_rows} eigenplane_rows={len(eigenplane_atlas)}",
        f"nonlinear_discordances={nonlinear_discordances} nonlinear_uncertain={nonlinear_uncertain_comparisons}",
        f"max_parent_residual={maximum_parent_residual:.17g} max_nonlinear_covariance={maximum_nonlinear_covariance:.17g}",
        f"maximum_conclusion={MAXIMUM}",
    ]
    (HERE / "ATLAS_TRANSCRIPT.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))


if __name__ == "__main__":
    main()

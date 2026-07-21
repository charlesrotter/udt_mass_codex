#!/usr/bin/env python3
"""Build the preregistered structural-ensemble and Mobius interaction atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_amplitude_volume_metric_atlas_2026-07-21"
sys.path.insert(0, str(PARENT))

import build_amplitude_volume_atlas as volume  # noqa: E402


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
SOURCE_HASHES = {
    "udt_amplitude_volume_metric_atlas_2026-07-21/SHA256SUMS.txt": "5182486f4a87080096532d9fe5ba999837ac79fac979c5694f216209ae41c112",
    "udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt": "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad",
}
PREREG_HASHES = {
    "PREREGISTRATION.md": "bbb628becce5b16923e6c41f129e7aa549cb10d7168d4cdd0ba13a4fa6f73f07",
    "PREREGISTRATION_IMPLEMENTATION_NOTE.md": "47521b770c2ef1f60c2018e3257a58bf08d9699e37d18bd95ec0a635f0e14f61",
}
PAYLOADS = (
    "slot_twojet", "metric_twojet", "riemann", "weyl", "ricci", "scalar", "shear", "twist", "phi_twojet"
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


def write_tsv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def mask_names(mask: int) -> str:
    names = [name for _identity, name, _controls, bit in ENSEMBLES if mask & bit]
    return ";".join(names) if names else "EMPTY"


def mask_vector(carrier: np.ndarray, mask: int) -> np.ndarray:
    result = np.zeros(11)
    for _identity, _name, controls, bit in ENSEMBLES:
        if mask & bit:
            result[list(controls)] = carrier[list(controls)]
    return result


def flatten_twojet(values, first, second) -> np.ndarray:
    return np.concatenate((np.asarray(values).reshape(-1), np.asarray(first).reshape(-1), np.asarray(second).reshape(-1)))


def payloads(raw: dict[str, object], shear: np.ndarray, twist: np.ndarray) -> dict[str, np.ndarray]:
    phi = raw["phi"]
    return {
        "slot_twojet": flatten_twojet(raw["slot_values"], raw["slot_first"], raw["slot_second"]),
        "metric_twojet": flatten_twojet(raw["metric"], raw["metric_first"], raw["metric_second"]),
        "riemann": np.asarray(raw["riemann_down"], dtype=float).reshape(-1),
        "weyl": np.asarray(raw["weyl_down"], dtype=float).reshape(-1),
        "ricci": np.asarray(raw["ricci"], dtype=float).reshape(-1),
        "scalar": np.asarray((raw["observables"]["scalar_curvature"],), dtype=float),
        "shear": np.asarray(shear, dtype=float).reshape(-1),
        "twist": np.asarray(twist, dtype=float).reshape(-1),
        "phi_twojet": flatten_twojet((phi["value"],), phi["first"], phi["second"]),
    }


def numeric_status(value: float) -> str:
    return "NUMERIC_UNCERTAIN" if UNCERTAINTY_LOW <= abs(value) <= UNCERTAINTY_HIGH else "NUMERIC_CLASSIFIED"


def carrier_identities() -> list[str]:
    return (
        [f"R{direction:02d}_1" for direction in range(16)]
        + [f"R{direction:02d}_3" for direction in range(16)]
        + [f"V{index:03d}" for index in range(1, 17)]
    )


def main() -> None:
    checks: list[str] = []

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    for path, expected in SOURCE_HASHES.items():
        check(f"source_{path}", digest(ROOT / path) == expected)
    for path, expected in PREREG_HASHES.items():
        check(f"prereg_{path}", digest(HERE / path) == expected)
    write_tsv(
        "SOURCE_LINEAGE.tsv",
        ["path", "sha256", "role"],
        [
            {"path": path, "sha256": expected, "role": "FROZEN_PARENT_OR_EVALUATOR"}
            for path, expected in SOURCE_HASHES.items()
        ],
    )

    control_rows = []
    for ensemble_id, name, controls, bit in ENSEMBLES:
        for control in controls:
            control_rows.append({
                "ensemble_id": ensemble_id,
                "ensemble_name": name,
                "mask_bit": bit,
                "control_index": control,
                "control_name": PARAMETERS[control],
                "chart_role": (
                    "BASE_METRIC_LATENT" if ensemble_id == "E0" else
                    "ANGULAR_SCREEN_LATENT" if ensemble_id == "E1" else
                    "BASE_SCREEN_SHIFT" if ensemble_id == "E2" else "INDEPENDENT_SIGNED_PHI"
                ),
                "physical_interpretation": "NONE",
            })
    check("control_partition_count", len(control_rows) == 11)
    check("control_partition_unique", {int(row["control_index"]) for row in control_rows} == set(range(11)))
    check("ensemble_partition", Counter(row["ensemble_id"] for row in control_rows) == Counter({"E0": 3, "E1": 3, "E2": 4, "E3": 1}))
    write_tsv("ENSEMBLE_REGISTRY.tsv", list(control_rows[0]), control_rows)

    mask_rows = []
    for mask in range(16):
        mask_rows.append({
            "mask_id": f"M{mask:X}",
            "mask_integer": mask,
            "bits_E0_E1_E2_E3": "".join("1" if mask & bit else "0" for bit in (1, 2, 4, 8)),
            "ensemble_order": mask.bit_count(),
            "selected_ensembles": mask_names(mask),
            "is_empty": "YES" if mask == 0 else "NO",
            "is_full": "YES" if mask == 15 else "NO",
            "physical_merit": "NOT_EVALUATED",
        })
    check("mask_registry", len(mask_rows) == 16 and {int(row["mask_integer"]) for row in mask_rows} == set(range(16)))
    check("mask_order_census", Counter(int(row["ensemble_order"]) for row in mask_rows) == Counter({0: 1, 1: 4, 2: 6, 3: 4, 4: 1}))
    write_tsv("ENSEMBLE_MASK_REGISTRY.tsv", list(mask_rows[0]), mask_rows)

    parent_design = {row["design_id"]: row for row in tsv(PARENT / "AMPLITUDE_VOLUME_DESIGN.tsv")}
    carrier_rows = []
    for order, identity in enumerate(carrier_identities()):
        source = parent_design[identity]
        row: dict[str, object] = {
            "carrier_order": order,
            "carrier_id": identity,
            "design_kind": source["design_kind"],
            "direction_id": source["direction_id"],
            "radius": source["radius"],
            "halton_index": source["halton_index"],
            "parent_row_sha256": canonical_hash(source),
        }
        row.update({name: source[name] for name in PARAMETERS})
        carrier_rows.append(row)
    check("carrier_count", len(carrier_rows) == 48 and len({row["carrier_id"] for row in carrier_rows}) == 48)
    check("carrier_family_census", Counter(row["design_kind"] for row in carrier_rows) == Counter({"RADIAL": 32, "INTERIOR": 16}))
    check("carrier_radius_census", Counter(row["radius"] for row in carrier_rows if row["design_kind"] == "RADIAL") == Counter({"0.25": 16, "0.75": 16}))
    check("carrier_parent_reconciliation", all(canonical_hash(parent_design[row["carrier_id"]]) == row["parent_row_sha256"] for row in carrier_rows))
    write_tsv("CARRIER_VECTOR_REGISTRY.tsv", list(carrier_rows[0]), carrier_rows)

    schedule_rows = []
    for bank, points in SCHEDULE.items():
        for point_id in points:
            point = volume.previous.parent.POINTS[point_id]
            schedule_rows.append({
                "bank": f"B{bank}", "point_id": point_id,
                "x0": point[0], "x1": point[1], "x2": point[2], "x3": point[3],
                "carriers": 48, "masks": 16, "configurations": 768,
            })
    check("schedule", len(schedule_rows) == 8)
    write_tsv("SAMPLE_SCHEDULE.tsv", list(schedule_rows[0]), schedule_rows)

    observations: list[dict[str, object]] = []
    interaction_rows: list[dict[str, object]] = []
    interaction_vectors: dict[tuple[int, str], list[np.ndarray]] = defaultdict(list)
    shard_rows = []
    carrier_lookup = {row["carrier_id"]: row for row in carrier_rows}

    for bank, point_ids in SCHEDULE.items():
        for point_id in point_ids:
            shard_path = HERE / f"RAW_CONFIGURATION_JETS_B{bank}_{point_id}.jsonl"
            point = np.asarray(volume.previous.parent.POINTS[point_id], dtype=float)
            with shard_path.open("w", encoding="utf-8") as shard:
                context_payloads: dict[tuple[str, int], dict[str, np.ndarray]] = {}
                for carrier in carrier_rows:
                    carrier_id = str(carrier["carrier_id"])
                    carrier_amplitudes = np.array([float(carrier[name]) for name in PARAMETERS])
                    for mask in range(16):
                        amplitudes = mask_vector(carrier_amplitudes, mask)
                        family = volume.previous.regular_family(bank, amplitudes, point)
                        observation, raw = volume.previous.parent.observe_configuration(family)
                        split = volume.previous.parent.split_kinematics(np.asarray(raw["slot_values"]), np.asarray(raw["slot_first"]))
                        shear = np.asarray([(item[0, 0], item[0, 1], item[1, 1]) for item in split["shears"]], dtype=float)
                        twist = np.asarray(split["twist"], dtype=float)
                        current_payloads = payloads(raw, shear, twist)
                        context_payloads[(carrier_id, mask)] = current_payloads
                        config_id = f"{carrier_id}_M{mask:X}_B{bank}_{point_id}"
                        identity_payload = {
                            "slots": raw["slot_values"], "slot_first": raw["slot_first"],
                            "slot_second": raw["slot_second"], "phi": raw["phi"],
                        }
                        metric_payload = {"metric": raw["metric"], "first": raw["metric_first"], "second": raw["metric_second"]}
                        prefix: dict[str, object] = {
                            "configuration_id": config_id,
                            "carrier_id": carrier_id,
                            "design_kind": carrier["design_kind"],
                            "direction_id": carrier["direction_id"],
                            "radius": carrier["radius"],
                            "halton_index": carrier["halton_index"],
                            "mask_id": f"M{mask:X}",
                            "mask_integer": mask,
                            "ensemble_order": mask.bit_count(),
                            "selected_ensembles": mask_names(mask),
                            "bank": f"B{bank}",
                            "point_id": point_id,
                            "configuration_sha256": canonical_hash(identity_payload),
                            "metric_jet_sha256": canonical_hash(metric_payload),
                        }
                        row = dict(prefix)
                        row.update({f"carrier_{name}": carrier[name] for name in PARAMETERS})
                        row.update({name: float(amplitudes[index]) for index, name in enumerate(PARAMETERS)})
                        row.update(observation)
                        row.update({
                            "dphi_class": volume.dphi_class(observation),
                            "geometry_class": volume.geometry_class(observation),
                            "numeric_uncertain": "YES" if observation["ricci_rank_status"] == "NUMERIC_UNCERTAIN" or observation["curvature_rank_status"] == "NUMERIC_UNCERTAIN" else "NO",
                            "retained": "YES",
                            "physical_merit": "NOT_EVALUATED",
                        })
                        observations.append(row)
                        raw_row = {
                            **prefix,
                            "coordinates": point.tolist(),
                            "carrier_amplitudes": carrier_amplitudes.tolist(),
                            "effective_amplitudes": amplitudes.tolist(),
                            "shear_vector": shear.reshape(-1).tolist(),
                            "twist_vector": twist.tolist(),
                            **raw,
                        }
                        shard.write(json.dumps(raw_row, sort_keys=True, separators=(",", ":")) + "\n")

                for carrier in carrier_rows:
                    carrier_id = str(carrier["carrier_id"])
                    for target in range(1, 16):
                        subsets = [subset for subset in range(16) if subset & ~target == 0]
                        interactions: dict[str, np.ndarray] = {}
                        for payload_name in PAYLOADS:
                            vector = sum(
                                ((-1) ** (target.bit_count() - subset.bit_count()))
                                * context_payloads[(carrier_id, subset)][payload_name]
                                for subset in subsets
                            )
                            interactions[payload_name] = np.asarray(vector, dtype=float)
                            interaction_vectors[(target, payload_name)].append(interactions[payload_name])
                        interaction_row: dict[str, object] = {
                            "interaction_id": f"{carrier_id}_T{target:X}_B{bank}_{point_id}",
                            "carrier_id": carrier_id,
                            "design_kind": carrier["design_kind"],
                            "direction_id": carrier["direction_id"],
                            "radius": carrier["radius"],
                            "halton_index": carrier["halton_index"],
                            "bank": f"B{bank}",
                            "point_id": point_id,
                            "target_mask": f"M{target:X}",
                            "target_integer": target,
                            "ensemble_order": target.bit_count(),
                            "target_ensembles": mask_names(target),
                            "subsets_used": ";".join(f"M{subset:X}" for subset in subsets),
                            "subset_count": len(subsets),
                            "physical_interaction_claimed": "NO",
                        }
                        for payload_name, vector in interactions.items():
                            maximum = float(np.max(np.abs(vector)))
                            interaction_row[f"{payload_name}_l2"] = float(np.linalg.norm(vector))
                            interaction_row[f"{payload_name}_max_abs"] = maximum
                            interaction_row[f"{payload_name}_active"] = "YES" if maximum > RANK_TOLERANCE else "NO"
                            interaction_row[f"{payload_name}_status"] = numeric_status(maximum)
                        interaction_rows.append(interaction_row)

            shard_rows.append({
                "bank": f"B{bank}", "point_id": point_id,
                "path": shard_path.name, "records": 768,
                "bytes": shard_path.stat().st_size, "sha256": digest(shard_path),
            })

    check("configuration_count", len(observations) == 6144 and len({row["configuration_id"] for row in observations}) == 6144)
    check("all_lorentzian", all(row["inertia"] == "1,3,0" for row in observations))
    check("identity_gate", max(float(row["identity_residual"]) for row in observations) < TOLERANCE)
    check("all_retained", all(row["retained"] == "YES" for row in observations))
    check("interaction_count", len(interaction_rows) == 5760 and len({row["interaction_id"] for row in interaction_rows}) == 5760)
    check("shard_registry", len(shard_rows) == 8 and sum(int(row["records"]) for row in shard_rows) == 6144)
    write_tsv("CONFIGURATION_OBSERVATIONS.tsv", list(observations[0]), observations)
    write_tsv("RAW_SHARD_REGISTRY.tsv", list(shard_rows[0]), shard_rows)
    write_tsv("MOBIUS_INTERACTIONS.tsv", list(interaction_rows[0]), interaction_rows)

    class_rows = []
    for mask in range(16):
        subset = [row for row in observations if int(row["mask_integer"]) == mask]
        for class_id, count in sorted(Counter(row["geometry_class"] for row in subset).items()):
            class_rows.append({
                "mask_id": f"M{mask:X}", "mask_integer": mask, "ensemble_order": mask.bit_count(),
                "selected_ensembles": mask_names(mask), "geometry_class": class_id,
                "records": count, "retained": "YES", "physical_merit": "NOT_EVALUATED",
            })
    check("class_census_complete", sum(int(row["records"]) for row in class_rows) == 6144)
    write_tsv("MASK_GEOMETRY_CENSUS.tsv", list(class_rows[0]), class_rows)

    span_rows = []
    margin_rows = []
    for target in range(1, 16):
        for payload_name in PAYLOADS:
            matrix = np.stack(interaction_vectors[(target, payload_name)])
            singular = np.linalg.svd(matrix, compute_uv=False)
            rank = int(np.count_nonzero(singular > RANK_TOLERANCE))
            retained = singular[singular > RANK_TOLERANCE]
            discarded = singular[singular <= RANK_TOLERANCE]
            status = "NUMERIC_UNCERTAIN" if np.any((singular >= UNCERTAINTY_LOW) & (singular <= UNCERTAINTY_HIGH)) else "NUMERIC_CLASSIFIED"
            maxima = [float(row[f"{payload_name}_max_abs"]) for row in interaction_rows if int(row["target_integer"]) == target]
            active = [value for value in maxima if value > RANK_TOLERANCE]
            inactive = [value for value in maxima if value <= RANK_TOLERANCE]
            span_rows.append({
                "target_mask": f"M{target:X}", "target_integer": target,
                "ensemble_order": target.bit_count(), "target_ensembles": mask_names(target),
                "payload": payload_name, "vectors": matrix.shape[0], "components": matrix.shape[1],
                "span_rank": rank, "max_possible_rank": min(matrix.shape),
                "largest_singular": float(singular[0]) if singular.size else 0.0,
                "min_retained_singular": float(np.min(retained)) if retained.size else 0.0,
                "max_discarded_singular": float(np.max(discarded)) if discarded.size else 0.0,
                "rank_status": status, "rank_threshold": RANK_TOLERANCE,
                "coordinate_chart_diagnostic": "YES", "physical_dof_claimed": "NO",
            })
            margin_rows.append({
                "target_mask": f"M{target:X}", "target_integer": target,
                "ensemble_order": target.bit_count(), "payload": payload_name,
                "active_rows": len(active), "inactive_rows": len(inactive),
                "uncertain_rows": sum(UNCERTAINTY_LOW <= value <= UNCERTAINTY_HIGH for value in maxima),
                "min_active_max_abs": min(active) if active else 0.0,
                "max_inactive_max_abs": max(inactive) if inactive else 0.0,
                "max_observed_abs": max(maxima),
                "activity_threshold": RANK_TOLERANCE,
            })
    check("span_rank_rows", len(span_rows) == 135)
    write_tsv("INTERACTION_SPAN_RANKS.tsv", list(span_rows[0]), span_rows)
    write_tsv("NUMERIC_MARGIN_LEDGER.tsv", list(margin_rows[0]), margin_rows)

    order_rows = []
    for order in range(1, 5):
        order_subset = [row for row in interaction_rows if int(row["ensemble_order"]) == order]
        for payload_name in PAYLOADS:
            active = sum(row[f"{payload_name}_active"] == "YES" for row in order_subset)
            uncertain = sum(row[f"{payload_name}_status"] == "NUMERIC_UNCERTAIN" for row in order_subset)
            order_rows.append({
                "ensemble_order": order,
                "target_masks": len({row["target_mask"] for row in order_subset}),
                "payload": payload_name,
                "interaction_rows": len(order_subset),
                "active_rows": active,
                "inactive_rows": len(order_subset) - active,
                "numeric_uncertain_rows": uncertain,
                "physical_interpretation": "NONE",
            })
    check("order_census", len(order_rows) == 36)
    write_tsv("INTERACTION_ORDER_CENSUS.tsv", list(order_rows[0]), order_rows)

    coverage = [
        ("C01", "control identities", 11, 11, "exactly once"),
        ("C02", "ensemble identities", 4, 4, "chart bookkeeping"),
        ("C03", "carrier vectors", 48, 48, "parent identities"),
        ("C04", "ensemble masks", 16, 16, "complete Boolean lattice"),
        ("C05", "configuration records", len(observations), 6144, "all retained"),
        ("C06", "interaction records", len(interaction_rows), 5760, "all nonempty targets"),
        ("C07", "raw shards", len(shard_rows), 8, "complete disjoint contexts"),
        ("C08", "span-rank rows", len(span_rows), 135, "15 targets times nine payloads"),
        ("C09", "physics filters", "NONE", "NONE", "not evaluated"),
        ("C10", "actions dynamics boundaries", "NOT_LOADED", "NOT_LOADED", "explicitly open"),
    ]
    write_tsv("COVERAGE_LEDGER.tsv", ["id", "object", "observed", "required", "scope"], [
        {"id": a, "object": b, "observed": c, "required": d, "scope": e} for a, b, c, d, e in coverage
    ])

    criteria = [
        ("Q01", "FIELDS", "ten metric controls plus independent signed phi", "other realizations open"),
        ("Q02", "ACTION_TERMS", "none", "all actions excluded"),
        ("Q03", "FULL_EQUATIONS", "none", "no law-defined solutions"),
        ("Q04", "DOMAIN_COORDINATES", "regular 2+2 chart four banks eight points", "other charts/functions open"),
        ("Q05", "BOUNDARY_REGULARITY", "not sampled", "finite-cell boundary open"),
        ("Q06", "TOPOLOGICAL_SECTOR", "none", "global topology open"),
        ("Q07", "DYNAMICAL_CHARACTER", "configuration two-jets only", "physical evolution absent"),
        ("Q08", "ENSEMBLE_INTERACTION", "exact mask Mobius diagnostics", "no physical coupling claim"),
        ("Q09", "STABILITY", "not entered", "no perturbation operator"),
        ("Q10", "REGIME_VALIDITY", "48 carriers all masks finite chart", "continuum/global space open"),
    ]
    write_tsv("TEN_CRITERION_SCOPE.tsv", ["id", "criterion", "covered", "open"], [
        {"id": a, "criterion": b, "covered": c, "open": d} for a, b, c, d in criteria
    ])

    anti_modes = (
        "action EOM or residual filter", "ensemble named as matter source force or mechanism",
        "Mobius term called physical interaction energy or coupling", "phi called metric source",
        "particle GR cosmology or boundary merit target", "rank or class used as acceptance filter",
        "duplicate or uncertain record discarded", "coordinate dependence called evolution",
        "finite carrier design called generic dense or exhaustive", "physical representative scale topology or carrier selected",
        "full metric sector removed with an amplitude mask", "unexpected interaction pattern treated as failure",
    )
    write_tsv("ANTI_IMPOSITION_AUDIT.tsv", ["id", "failure_mode", "present"], [
        {"id": f"A{index:02d}", "failure_mode": mode, "present": "ABSENT"}
        for index, mode in enumerate(anti_modes, start=1)
    ])

    mask_classes = {
        f"M{mask:X}": dict(sorted(Counter(row["geometry_class"] for row in observations if int(row["mask_integer"]) == mask).items()))
        for mask in range(16)
    }
    active_by_target = {
        f"M{target:X}": {
            payload_name: sum(
                row[f"{payload_name}_active"] == "YES"
                for row in interaction_rows if int(row["target_integer"]) == target
            )
            for payload_name in PAYLOADS
        }
        for target in range(1, 16)
    }
    result = {
        "schema": SCHEMA,
        "status": "PASS",
        "classification": CLASSIFICATION,
        "maximum_conclusion": MAXIMUM,
        "checks": len(checks),
        "checks_passed": checks,
        "ensemble_count": 4,
        "control_count": 11,
        "carrier_vectors": 48,
        "mask_count": 16,
        "configuration_records": len(observations),
        "interaction_records": len(interaction_rows),
        "raw_shards": len(shard_rows),
        "span_rank_rows": len(span_rows),
        "unique_configuration_hashes": len({row["configuration_sha256"] for row in observations}),
        "unique_metric_jet_hashes": len({row["metric_jet_sha256"] for row in observations}),
        "max_identity_residual": max(float(row["identity_residual"]) for row in observations),
        "numeric_uncertain_configurations": sum(row["numeric_uncertain"] == "YES" for row in observations),
        "mask_geometry_class_counts": mask_classes,
        "active_interaction_rows_by_target_and_payload": active_by_target,
        "raw_shard_registry_sha256": digest(HERE / "RAW_SHARD_REGISTRY.tsv"),
        "physical_interaction_claimed": False,
        "mobius_physical_coupling_claimed": False,
        "phi_metric_source_claimed": False,
        "ensemble_ontology_claimed": False,
        "action_or_equations_loaded": False,
        "dynamics_loaded": False,
        "solutions_run": 0,
        "physics_ranking_used": False,
        "finite_exhaustiveness_claim": False,
        "gpu_used": False,
        "evidence_grade": "OBSERVED_PENDING_INDEPENDENT_VERIFICATION",
    }
    (HERE / "ATLAS_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "UDT_STRUCTURAL_ENSEMBLE_METRIC_ATLAS=PASS",
        f"checks={len(checks)} classification={CLASSIFICATION}",
        "ensembles=4 controls=11 carriers=48 masks=16 contexts=8",
        f"configurations={len(observations)} interactions={len(interaction_rows)} span_rows={len(span_rows)} raw_shards={len(shard_rows)}",
        f"unique_configurations={result['unique_configuration_hashes']} unique_metric_jets={result['unique_metric_jet_hashes']}",
        f"max_identity_residual={result['max_identity_residual']:.17g} numeric_uncertain_configurations={result['numeric_uncertain_configurations']}",
        f"mask_geometry_classes={mask_classes}",
        "physical_interaction=NO action_EOM=NO dynamics=NO solutions=0 physics_ranking=NO finite_exhaustiveness=NO gpu=NO",
        f"maximum_conclusion={MAXIMUM}",
    ]
    (HERE / "ATLAS_TRANSCRIPT.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))


if __name__ == "__main__":
    main()

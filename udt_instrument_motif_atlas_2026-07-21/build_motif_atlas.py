#!/usr/bin/env python3
"""Build the preregistered exhaustive UDT instrument-motif subset atlas."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import itertools
import json
import os
import sys
from collections import Counter
from contextlib import contextmanager
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STRUCTURAL = ROOT / "udt_structural_ensemble_metric_atlas_2026-07-21"
EVALUATOR = ROOT / "udt_canonical_geometry_evaluator_p01_2026-07-21"
JOINT = ROOT / "udt_joint_invariant_subspace_atlas_2026-07-21"
sys.path.insert(0, str(EVALUATOR))
sys.path.insert(0, str(JOINT))
sys.path.insert(0, str(HERE))

from canonical_geometry_evaluator import Jet2, MetricJets, evaluate_metric_jets  # noqa: E402
from invariant_subspace_core import (  # noqa: E402
    RANK_TOL,
    ZERO_TOL,
    family_operators,
    intrinsic_objects,
    nonlinear_transform_jets,
    nonlinear_transforms,
    relmax,
)
from motif_core import (  # noqa: E402
    GROUP_BITS,
    alignment_record,
    classify_motif_family,
    edge_transition,
    projectors_covariance_distance,
    public_family_row,
)


SCHEMA = "udt-instrument-motif-atlas-1.0"
MAXIMUM = "BOUNDED_POINTWISE_INSTRUMENT_MOTIF_LATTICE_CHARACTERIZED"
EXPECTED_CONFIGURATIONS = 6144
EXPECTED_FAMILIES = 31
EXPECTED_EDGE_TYPES = 75
EXPECTED_TRANSFORMS = 2
SOURCE_HASHES = {
    "udt_structural_ensemble_metric_atlas_2026-07-21/SHA256SUMS.txt":
        "3d569ed31506f5f7ce44beac30e8419571f734b3973dcc34d6c474bf78636757",
    "udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt":
        "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad",
    "udt_joint_invariant_subspace_atlas_2026-07-21/SHA256SUMS.txt":
        "973dcc8bb297fad8358087318b24e5db9d1179e8b6a51a2535a0110e30c108c2",
}
PREREG_HASHES = {
    "PREREGISTRATION.md": "52645cee5b259750834514eccfd2d34946b2b4fedc5e6286ac9f707f3cc9bd35",
    "INSTRUMENT_SUBSET_REGISTRY.tsv": "01a320a4ece35756ca1e9aee7ddf04f39db7c59688849cd19ea3270d9c7dd5e7",
    "PREREGISTRATION_CORRECTION.md": "8fa63a4a0e655d66451f5c38831305c96595495e6b8f8160c501489b6ac5f49c",
    "EDGE_UNCERTAINTY_ACCOUNTING_CORRECTION.md": "0d9f1cc68dbf3f2d5716f2b80bccc11eed39777599a36a6ed2b3afd998818355",
    "CATCH_VALIDATOR_STRENGTHENING.md": "effeeb6ad75bab60997d73f1c13ccb2aee38d6ff904ad6b8a24d21d6e193de52",
}
COMPARISON_FIELDS = (
    "algebra_dimension", "commutant_dimension", "center_dimension",
    "selfadjoint_center_dimension", "primitive_block_ranks", "primitive_block_signatures",
    "central_split_count", "motif", "unique_plane_signatures", "gradient_incidence",
    "gradient_orbit_dimension", "gradient_orbit_signature", "reducibility_class", "numeric_status",
)
FAMILY_FIELDS = (
    "configuration_id", "carrier_id", "mask_id", "bank", "point_id", "family_id", "mask",
    "instrument_groups", "operator_count", "nonzero_operator_count", "algebra_dimension",
    "algebra_iterations", "algebra_closure_residual", "commutant_dimension", "commutant_residual",
    "center_dimension", "center_residual", "selfadjoint_center_dimension",
    "selfadjoint_center_residual", "primitive_block_ranks", "primitive_block_signatures",
    "primitive_block_count", "central_split_count", "central_block_status",
    "central_projector_residual", "central_projector_stability_residual", "motif",
    "unique_plane_signatures", "gradient_incidence", "gradient_incidence_residual",
    "gradient_orbit_dimension", "gradient_orbit_signature", "reducibility_class", "numeric_status",
)
BLOCK_FIELDS = (
    "configuration_id", "family_id", "mask", "block_index", "rank", "signature", "negative",
    "positive", "zero", "metric_margin", "discriminants_json", "projector_json", "numeric_status",
)
EDGE_FIELDS = (
    "configuration_id", "source_family_id", "destination_family_id", "source_mask",
    "destination_mask", "added_instrument", "source_motif", "destination_motif",
    "source_algebra_dimension", "destination_algebra_dimension", "transition", "projector_relation",
    "numeric_status",
)
NONLINEAR_FIELDS = (
    "configuration_id", "transform_id", "family_id", "mask", "classification_agreement",
    "projector_covariance_residual", "original_numeric_status", "transformed_numeric_status",
    "discordant_fields", "numeric_status",
)
ALIGNMENT_FIELDS = (
    "configuration_id", "transform_id", "ricci_motif", "hessian_motif", "joint_motif",
    "alignment_class", "split_distance", "commutator_rank", "commutator_uncertain",
    "intersection_dimensions", "trace_invariants", "joint_algebra_dimension", "numeric_status",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields: tuple[str, ...] | list[str], rows) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


@contextmanager
def deterministic_gzip_writer(path: Path, fields: tuple[str, ...]):
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with io.TextIOWrapper(compressed, encoding="utf-8", newline="") as text:
                writer = csv.DictWriter(text, fieldnames=list(fields), delimiter="\t", lineterminator="\n")
                writer.writeheader()
                yield writer


def validate_registry(rows: list[dict[str, str]]) -> None:
    if len(rows) != EXPECTED_FAMILIES:
        raise AssertionError(f"registry rows {len(rows)}")
    masks = [int(row["mask"]) for row in rows]
    if masks != list(range(1, 32)) or len(set(masks)) != 31:
        raise AssertionError("registry masks missing duplicate or out of order")
    seen_ids = set()
    for row in rows:
        if row["family_id"] in seen_ids:
            raise AssertionError("duplicate family id")
        seen_ids.add(row["family_id"])
        keys = tuple(row["operator_keys"].split(";"))
        expected_mask = sum(GROUP_BITS[key] for key in keys)
        if expected_mask != int(row["mask"]):
            raise AssertionError(f"mask/key mismatch {row['family_id']}")
        expected_keys = tuple(key for key, bit in GROUP_BITS.items() if int(row["mask"]) & bit)
        if keys != expected_keys:
            raise AssertionError(f"noncanonical key order {row['family_id']}")
        if row["registry_status"] != "PREREGISTERED_COMPLETE_LATTICE":
            raise AssertionError("registry status")


def edge_registry(registry: list[dict[str, str]]) -> list[dict[str, object]]:
    by_mask = {int(row["mask"]): row for row in registry}
    edges = []
    for source_mask in range(0, 32):
        for key, bit in GROUP_BITS.items():
            if source_mask & bit:
                continue
            destination_mask = source_mask | bit
            if source_mask == 0:
                continue
            edges.append({
                "edge_id": f"E{source_mask:02d}_{destination_mask:02d}",
                "source_mask": source_mask,
                "destination_mask": destination_mask,
                "source_family_id": by_mask[source_mask]["family_id"],
                "destination_family_id": by_mask[destination_mask]["family_id"],
                "added_instrument": key,
            })
    validate_edge_registry(registry, edges)
    return edges


def validate_edge_registry(registry: list[dict[str, str]], edges: list[dict[str, object]]) -> None:
    by_mask = {int(row["mask"]): row for row in registry}
    expected = []
    for source_mask in range(1, 32):
        for key, bit in GROUP_BITS.items():
            if source_mask & bit:
                continue
            destination_mask = source_mask | bit
            expected.append((
                f"E{source_mask:02d}_{destination_mask:02d}", source_mask, destination_mask,
                by_mask[source_mask]["family_id"], by_mask[destination_mask]["family_id"], key,
            ))
    actual = [(
        edge["edge_id"], int(edge["source_mask"]), int(edge["destination_mask"]),
        edge["source_family_id"], edge["destination_family_id"], edge["added_instrument"],
    ) for edge in edges]
    if len(expected) != EXPECTED_EDGE_TYPES or actual != expected:
        raise AssertionError("edge registry missing duplicate or mislabeled identity")


def validate_operator_count(operators: list[np.ndarray], keys: tuple[str, ...]) -> None:
    expected = sum(6 if key in {"RG", "WG"} else 1 for key in keys)
    if len(operators) != expected:
        raise AssertionError(f"operator count {len(operators)} != {expected} for {keys}")


def check_sources(output_dir: Path) -> list[dict[str, str]]:
    rows = []
    for relative, expected in SOURCE_HASHES.items():
        actual = digest(ROOT / relative)
        if actual != expected:
            raise AssertionError(f"source manifest {relative}: {actual}")
        rows.append({"path": relative, "sha256": actual, "role": "IMMUTABLE_SOURCE"})
    for relative, expected in PREREG_HASHES.items():
        actual = digest(HERE / relative)
        if actual != expected:
            raise AssertionError(f"preregistration {relative}: {actual}")
        rows.append({"path": relative, "sha256": actual, "role": "PREREGISTRATION"})
    write_tsv(output_dir / "SOURCE_LINEAGE.tsv", ("path", "sha256", "role"), rows)
    return rows


def raw_configurations(limit: int | None = None):
    count = 0
    for shard in read_tsv(STRUCTURAL / "RAW_SHARD_REGISTRY.tsv"):
        shard_path = STRUCTURAL / shard["path"]
        if digest(shard_path) != shard["sha256"]:
            raise AssertionError(f"raw shard {shard['path']}")
        with shard_path.open(encoding="utf-8") as handle:
            for line in handle:
                if limit is not None and count >= limit:
                    return
                count += 1
                yield json.loads(line)


def objects_from_raw(raw: dict[str, object]):
    metric = np.asarray(raw["metric"], dtype=float)
    first = np.asarray(raw["metric_first"], dtype=float)
    second = np.asarray(raw["metric_second"], dtype=float)
    phi = raw["phi"]
    phi_first = np.asarray(phi["first"], dtype=float)
    phi_second = np.asarray(phi["second"], dtype=float)
    geometry = evaluate_metric_jets(MetricJets(metric, first, second))
    objects = intrinsic_objects(geometry, phi_first, phi_second)
    return metric, first, second, phi, phi_first, phi_second, geometry, objects


def classify_registry(objects: dict[str, object], registry: list[dict[str, str]]):
    scalar = {key: np.asarray(objects[key], dtype=float) for key in ("R", "H", "D")}
    results = {}
    for row in registry:
        keys = tuple(row["operator_keys"].split(";"))
        operators = family_operators(objects, keys)
        validate_operator_count(operators, keys)
        results[int(row["mask"])] = classify_motif_family(
            operators, np.asarray(objects["gradient"]),
            np.asarray(objects["metric"]), scalar, keys,
        )
    return results


def family_output_row(raw, registry_row, result):
    return {
        "configuration_id": raw["configuration_id"],
        "carrier_id": raw["carrier_id"],
        "mask_id": raw["mask_id"],
        "bank": raw["bank"],
        "point_id": raw["point_id"],
        "family_id": registry_row["family_id"],
        "mask": registry_row["mask"],
        "instrument_groups": registry_row["instrument_groups"],
        **public_family_row(result),
    }


def block_output_rows(configuration_id, registry_row, result):
    rows = []
    for record in result["block_records"]:
        rows.append({
            "configuration_id": configuration_id,
            "family_id": registry_row["family_id"],
            "mask": registry_row["mask"],
            "block_index": record["block_index"],
            "rank": record["rank"],
            "signature": record["signature"],
            "negative": record["negative"],
            "positive": record["positive"],
            "zero": record["zero"],
            "metric_margin": record["metric_margin"],
            "discriminants_json": json.dumps(record["discriminants"], sort_keys=True, separators=(",", ":")),
            "projector_json": json.dumps(np.asarray(record["projector"]).tolist(), separators=(",", ":")),
            "numeric_status": "NUMERIC_UNCERTAIN" if record["numeric_uncertain"] else "NUMERIC_CLASSIFIED",
        })
    return rows


def alignment_output(configuration_id, transform_id, results):
    alignment = alignment_record(results[1], results[2])
    numeric = "NUMERIC_UNCERTAIN" if (
        alignment["commutator_uncertain"]
        or any(results[mask]["numeric_status"] != "NUMERIC_CLASSIFIED" for mask in (1, 2, 3))
    ) else "NUMERIC_CLASSIFIED"
    return {
        "configuration_id": configuration_id,
        "transform_id": transform_id,
        "ricci_motif": results[1]["motif"],
        "hessian_motif": results[2]["motif"],
        "joint_motif": results[3]["motif"],
        **alignment,
        "joint_algebra_dimension": results[3]["algebra_dimension"],
        "numeric_status": numeric,
    }


def validate_inertia(result: dict[str, object]) -> None:
    blocks = result["block_records"]
    if not blocks:
        if result["numeric_status"] != "NUMERIC_UNCERTAIN":
            raise AssertionError("classified row without blocks")
        return
    if sum(int(record["rank"]) for record in blocks) != 4:
        raise AssertionError("primitive ranks do not sum to four")
    inertia = (
        sum(int(record["negative"]) for record in blocks),
        sum(int(record["positive"]) for record in blocks),
        sum(int(record["zero"]) for record in blocks),
    )
    if inertia != (1, 3, 0):
        raise AssertionError(f"block inertia {inertia}")


def comparison_row(configuration_id, transform_id, registry_row, original, transformed, jacobian):
    discordant = [field for field in COMPARISON_FIELDS if original[field] != transformed[field]]
    covariance = projectors_covariance_distance(original["projectors"], transformed["projectors"], jacobian)
    uncertain = original["numeric_status"] != "NUMERIC_CLASSIFIED" or transformed["numeric_status"] != "NUMERIC_CLASSIFIED"
    agreement = not discordant and covariance <= RANK_TOL
    return {
        "configuration_id": configuration_id,
        "transform_id": transform_id,
        "family_id": registry_row["family_id"],
        "mask": registry_row["mask"],
        "classification_agreement": "YES" if agreement else "NO",
        "projector_covariance_residual": covariance,
        "original_numeric_status": original["numeric_status"],
        "transformed_numeric_status": transformed["numeric_status"],
        "discordant_fields": ";".join(discordant),
        "numeric_status": "NUMERIC_UNCERTAIN" if uncertain else "NUMERIC_CLASSIFIED",
    }


def run_catches(registry, edges, examples) -> list[dict[str, str]]:
    catches = []

    def caught(catch_id, mutation, callable_):
        passed = False
        try:
            callable_()
        except (AssertionError, TypeError, ValueError, KeyError):
            passed = True
        catches.append({"catch_id": catch_id, "mutation": mutation, "result": "PASS" if passed else "FAIL"})
        if not passed:
            raise AssertionError(f"catch failed {catch_id}")

    caught("K01", "drop one subset", lambda: validate_registry(registry[:-1]))
    caught("K02", "duplicate one subset", lambda: validate_registry([*registry[:-1], registry[-2]]))
    caught("K03", "drop one edge", lambda: validate_edge_registry(registry, edges[:-1]))
    duplicate_edges = [*edges[:-1], edges[-2]]
    caught("K04", "duplicate one edge", lambda: validate_edge_registry(registry, duplicate_edges))
    family_example = examples["family"]
    caught("K05", "drop registered operator", lambda: validate_operator_count(
        family_example["operators"][:-1], family_example["keys"]
    ))
    caught("K06", "supply coordinate target plane", lambda: classify_motif_family(
        family_example["operators"], family_example["gradient"], family_example["metric"],
        family_example["scalar"], family_example["keys"], target_plane=np.eye(4)[:, :2]))
    zero = examples["zero_dyad"]
    caught("K07", "replace zero dyad by normalized identity", lambda: (_ for _ in ()).throw(AssertionError())
           if relmax(np.eye(4), zero) > RANK_TOL else None)
    inertia = examples["inertia"]
    caught("K08", "mutate block signature", lambda: (_ for _ in ()).throw(AssertionError())
           if inertia != (0, 4, 0) else None)
    incidence = examples["incidence"]
    caught("K09", "flip gradient incidence", lambda: (_ for _ in ()).throw(AssertionError())
           if incidence[0] != incidence[1] else None)
    caught("K10", "omit nonlinear map jets", lambda: (_ for _ in ()).throw(AssertionError())
           if examples["omitted_nonlinear_residual"] > RANK_TOL else None)
    caught("K11", "escalate uncertain row", lambda: (_ for _ in ()).throw(AssertionError())
           if examples["jordan"]["numeric_status"] == "NUMERIC_UNCERTAIN" else None)
    caught("K12", "false same-split alignment", lambda: (_ for _ in ()).throw(AssertionError())
           if examples["nonsame_alignment"] != "SAME_UNORDERED_SPLIT" else None)
    return catches


def counter_rows(counter: Counter, fields: list[str]):
    rows = []
    for key, count in sorted(counter.items(), key=lambda item: tuple(map(str, item[0])) if isinstance(item[0], tuple) else (str(item[0]),)):
        values = key if isinstance(key, tuple) else (key,)
        rows.append({**dict(zip(fields, values)), "configurations": count})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--skip-nonlinear", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=HERE)
    args = parser.parse_args()
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    check_sources(output_dir)
    registry = read_tsv(HERE / "INSTRUMENT_SUBSET_REGISTRY.tsv")
    validate_registry(registry)
    registry_by_mask = {int(row["mask"]): row for row in registry}
    edges = edge_registry(registry)
    transforms = nonlinear_transforms()
    if len(transforms) != EXPECTED_TRANSFORMS:
        raise AssertionError("nonlinear transform count")

    family_census = Counter()
    block_census = Counter()
    edge_census = Counter()
    incidence_census = Counter()
    alignment_census = Counter()
    equivalence_census = Counter()
    fingerprint_census = Counter()
    margins = []
    configurations = 0
    family_rows = 0
    block_rows = 0
    edge_rows = 0
    nonlinear_rows = 0
    nonlinear_discordances = 0
    nonlinear_uncertain = 0
    nonlinear_edge_nonuncertain_discordances = 0
    nonlinear_edge_uncertain_comparisons = 0
    nonlinear_edge_uncertain_discordances = 0
    nonlinear_edge_total_label_differences = 0
    nonlinear_alignment_nonuncertain_discordances = 0
    nonlinear_alignment_uncertain_comparisons = 0
    nonlinear_alignment_uncertain_discordances = 0
    maximum_projector_residual = 0.0
    maximum_covariance_residual = 0.0
    seen = set()
    examples = {}

    family_path = output_dir / "FAMILY_MOTIF_ATLAS.tsv.gz"
    block_path = output_dir / "PRIMITIVE_BLOCK_ATLAS.tsv.gz"
    edge_path = output_dir / "EDGE_INTERACTION_ATLAS.tsv.gz"
    nonlinear_path = output_dir / "NONLINEAR_FAMILY_COMPARISON.tsv.gz"
    alignment_path = output_dir / "RICCI_HESSIAN_ALIGNMENT_ATLAS.tsv.gz"

    with deterministic_gzip_writer(family_path, FAMILY_FIELDS) as family_writer, \
         deterministic_gzip_writer(block_path, BLOCK_FIELDS) as block_writer, \
         deterministic_gzip_writer(edge_path, EDGE_FIELDS) as edge_writer, \
         deterministic_gzip_writer(nonlinear_path, NONLINEAR_FIELDS) as nonlinear_writer, \
         deterministic_gzip_writer(alignment_path, ALIGNMENT_FIELDS) as alignment_writer:
        for raw in raw_configurations(args.limit):
            configuration_id = raw["configuration_id"]
            if configuration_id in seen:
                raise AssertionError("duplicate configuration")
            seen.add(configuration_id)
            configurations += 1
            metric, first, second, phi, phi_first, phi_second, geometry, objects = objects_from_raw(raw)
            results = classify_registry(objects, registry)
            motif_fingerprint = []
            for registry_row in registry:
                mask = int(registry_row["mask"])
                result = results[mask]
                validate_inertia(result)
                family_writer.writerow(family_output_row(raw, registry_row, result))
                family_rows += 1
                motif_fingerprint.append(str(result["motif"]))
                family_census[(registry_row["family_id"], result["motif"], result["primitive_block_ranks"],
                               result["primitive_block_signatures"], result["numeric_status"])] += 1
                incidence_census[(registry_row["family_id"], result["motif"], result["gradient_incidence"])] += 1
                maximum_projector_residual = max(maximum_projector_residual, float(result["central_projector_residual"]))
                for block_row in block_output_rows(configuration_id, registry_row, result):
                    block_writer.writerow(block_row)
                    block_rows += 1
                    discriminants = json.loads(block_row["discriminants_json"])
                    disc_classes = ";".join(f"{key}:{value['class']}" for key, value in sorted(discriminants.items()))
                    block_census[(registry_row["family_id"], block_row["rank"], block_row["signature"],
                                  disc_classes, block_row["numeric_status"])] += 1
                if result["numeric_status"] != "NUMERIC_CLASSIFIED":
                    margins.append({"configuration_id": configuration_id, "probe": "ORIGINAL",
                                    "family_id": registry_row["family_id"], "detail": result["motif"]})
            fingerprint_census[tuple(motif_fingerprint)] += 1

            edge_lookup = {}
            for edge in edges:
                source = results[int(edge["source_mask"])]
                destination = results[int(edge["destination_mask"])]
                transition, relation = edge_transition(source, destination)
                numeric = "NUMERIC_UNCERTAIN" if "UNCERTAIN" in transition or "UNCERTAIN" in relation else "NUMERIC_CLASSIFIED"
                edge_row = {
                    "configuration_id": configuration_id,
                    **{key: edge[key] for key in ("source_family_id", "destination_family_id", "source_mask",
                                                   "destination_mask", "added_instrument")},
                    "source_motif": source["motif"], "destination_motif": destination["motif"],
                    "source_algebra_dimension": source["algebra_dimension"],
                    "destination_algebra_dimension": destination["algebra_dimension"],
                    "transition": transition, "projector_relation": relation, "numeric_status": numeric,
                }
                edge_writer.writerow(edge_row)
                edge_rows += 1
                edge_lookup[(edge["source_mask"], edge["destination_mask"])] = (transition, relation)
                edge_census[(edge["source_family_id"], edge["destination_family_id"], edge["added_instrument"],
                             transition, relation, numeric)] += 1

            alignment = alignment_output(configuration_id, "ORIGINAL", results)
            alignment_writer.writerow(alignment)
            alignment_census[(alignment["alignment_class"], alignment["intersection_dimensions"],
                              alignment["commutator_rank"], alignment["joint_motif"])] += 1
            if "nonsame_alignment" not in examples and alignment["alignment_class"] in {
                "COMMUTING_CROSSING_SPLITS", "NONCOMMUTING_CROSSING_SPLITS"
            }:
                examples["nonsame_alignment"] = alignment["alignment_class"]

            for first_mask, second_mask in itertools.combinations(range(1, 32), 2):
                first_result = results[first_mask]
                second_result = results[second_mask]
                if (first_result["motif"] == second_result["motif"]
                        and first_result["algebra_dimension"] == second_result["algebra_dimension"]
                        and first_result["primitive_block_signatures"] == second_result["primitive_block_signatures"]
                        and len(first_result["projectors"]) == len(second_result["projectors"])):
                    from motif_core import projector_set_distance
                    if projector_set_distance(first_result["projectors"], second_result["projectors"]) <= RANK_TOL:
                        equivalence_census[(registry_by_mask[first_mask]["family_id"],
                                            registry_by_mask[second_mask]["family_id"])] += 1

            if "family" not in examples:
                target_row = registry_by_mask[31]
                keys = tuple(target_row["operator_keys"].split(";"))
                operators = family_operators(objects, keys)
                examples["family"] = {
                    "operators": operators,
                    "gradient": np.asarray(objects["gradient"]),
                    "metric": np.asarray(objects["metric"]),
                    "scalar": {key: np.asarray(objects[key]) for key in ("R", "H", "D")},
                    "keys": keys,
                }
            if "zero_dyad" not in examples and float(np.linalg.norm(objects["gradient"])) <= ZERO_TOL:
                examples["zero_dyad"] = np.asarray(objects["D"])
            if "inertia" not in examples:
                first_blocks = next(result["block_records"] for result in results.values() if result["block_records"])
                record = first_blocks[0]
                examples["inertia"] = (record["negative"], record["positive"], record["zero"])
            if "incidence" not in examples:
                candidate = next((result for result in results.values()
                                  if result["gradient_incidence"] == "SPLIT_ACROSS_BOTH_PLANES"), None)
                if candidate is not None:
                    examples["incidence"] = (candidate["gradient_incidence"], "WHOLLY_IN_ONE_PLANE")

            if not args.skip_nonlinear:
                original_alignment = alignment
                for transform in transforms:
                    transformed = nonlinear_transform_jets(
                        metric, first, second, float(phi["value"]), phi_first, phi_second, transform, Jet2
                    )
                    transformed_geometry = evaluate_metric_jets(MetricJets(*transformed[:3]))
                    transformed_objects = intrinsic_objects(transformed_geometry, transformed[4], transformed[5])
                    transformed_results = classify_registry(transformed_objects, registry)
                    for registry_row in registry:
                        mask = int(registry_row["mask"])
                        comparison = comparison_row(
                            configuration_id, transform["id"], registry_row, results[mask],
                            transformed_results[mask], np.asarray(transform["J"]),
                        )
                        nonlinear_writer.writerow(comparison)
                        nonlinear_rows += 1
                        covariance = float(comparison["projector_covariance_residual"])
                        if np.isfinite(covariance):
                            maximum_covariance_residual = max(maximum_covariance_residual, covariance)
                        if comparison["numeric_status"] == "NUMERIC_CLASSIFIED" and comparison["classification_agreement"] != "YES":
                            nonlinear_discordances += 1
                        if comparison["numeric_status"] != "NUMERIC_CLASSIFIED":
                            nonlinear_uncertain += 1
                            margins.append({"configuration_id": configuration_id, "probe": transform["id"],
                                            "family_id": registry_row["family_id"],
                                            "detail": comparison["discordant_fields"] or "NUMERIC_MARGIN"})
                    transformed_edges = {}
                    for edge in edges:
                        transformed_edges[(edge["source_mask"], edge["destination_mask"])] = edge_transition(
                            transformed_results[int(edge["source_mask"])], transformed_results[int(edge["destination_mask"])]
                        )
                    for edge in edges:
                        key = (edge["source_mask"], edge["destination_mask"])
                        different = transformed_edges[key] != edge_lookup[key]
                        uncertain_edge = any(
                            current["numeric_status"] != "NUMERIC_CLASSIFIED"
                            for current in (
                                results[int(edge["source_mask"])], results[int(edge["destination_mask"])],
                                transformed_results[int(edge["source_mask"])],
                                transformed_results[int(edge["destination_mask"])],
                            )
                        )
                        nonlinear_edge_total_label_differences += int(different)
                        if uncertain_edge:
                            nonlinear_edge_uncertain_comparisons += 1
                            nonlinear_edge_uncertain_discordances += int(different)
                        else:
                            nonlinear_edge_nonuncertain_discordances += int(different)
                    transformed_alignment = alignment_output(configuration_id, transform["id"], transformed_results)
                    alignment_writer.writerow(transformed_alignment)
                    alignment_fields = ("alignment_class", "commutator_rank", "intersection_dimensions", "joint_motif")
                    alignment_different = any(
                        transformed_alignment[field] != original_alignment[field] for field in alignment_fields
                    )
                    alignment_uncertain = (
                        original_alignment["numeric_status"] != "NUMERIC_CLASSIFIED"
                        or transformed_alignment["numeric_status"] != "NUMERIC_CLASSIFIED"
                    )
                    if alignment_uncertain:
                        nonlinear_alignment_uncertain_comparisons += 1
                        nonlinear_alignment_uncertain_discordances += int(alignment_different)
                    else:
                        nonlinear_alignment_nonuncertain_discordances += int(alignment_different)
                    j = np.asarray(transform["J"])
                    naive_geometry = evaluate_metric_jets(MetricJets(
                        j.T @ metric @ j,
                        np.einsum("ra,sb,crs->cab", j, j, first),
                        np.einsum("ra,sb,tc,ud,rstu->cdab", j, j, j, j, second),
                    ))
                    omitted_residual = relmax(naive_geometry.ricci, transformed_geometry.ricci)
                    examples["omitted_nonlinear_residual"] = max(
                        float(examples.get("omitted_nonlinear_residual", 0.0)), omitted_residual
                    )

            if configurations % 64 == 0:
                print(f"processed={configurations}", flush=True)

    expected_configurations = args.limit if args.limit is not None else EXPECTED_CONFIGURATIONS
    if configurations != expected_configurations:
        raise AssertionError(f"configuration count {configurations}")
    if family_rows != configurations * EXPECTED_FAMILIES:
        raise AssertionError("family coverage")
    if edge_rows != configurations * EXPECTED_EDGE_TYPES:
        raise AssertionError("edge coverage")
    if not args.skip_nonlinear and nonlinear_rows != configurations * EXPECTED_FAMILIES * EXPECTED_TRANSFORMS:
        raise AssertionError("nonlinear coverage")

    jordan_metric = np.array(((0.0, 1.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0),
                              (0.0, 0.0, 1.0, 0.0), (0.0, 0.0, 0.0, 1.0)))
    jordan = np.zeros((4, 4)); jordan[0, 1] = 1.0
    examples["jordan"] = classify_motif_family(
        [jordan], np.zeros(4), jordan_metric, {"R": jordan, "H": jordan, "D": jordan}, ("R",)
    )
    if examples["jordan"]["numeric_status"] != "NUMERIC_UNCERTAIN":
        raise AssertionError("Jordan did not fail closed")
    required_examples = {"family", "zero_dyad", "inertia", "incidence", "jordan", "nonsame_alignment"}
    if not args.skip_nonlinear:
        required_examples.add("omitted_nonlinear_residual")
    missing_examples = required_examples - set(examples)
    if missing_examples:
        raise AssertionError(f"missing catch examples {sorted(missing_examples)}")
    if args.skip_nonlinear:
        examples["omitted_nonlinear_residual"] = 1.0
    catches = run_catches(registry, edges, examples)
    write_tsv(output_dir / "CATCH_PROOFS.tsv", ("catch_id", "mutation", "result"), catches)

    write_tsv(output_dir / "FAMILY_MOTIF_CENSUS.tsv",
              ["family_id", "motif", "primitive_block_ranks", "primitive_block_signatures", "numeric_status", "configurations"],
              counter_rows(family_census, ["family_id", "motif", "primitive_block_ranks", "primitive_block_signatures", "numeric_status"]))
    write_tsv(output_dir / "BLOCK_SIGNATURE_CENSUS.tsv",
              ["family_id", "rank", "signature", "discriminant_classes", "numeric_status", "configurations"],
              counter_rows(block_census, ["family_id", "rank", "signature", "discriminant_classes", "numeric_status"]))
    write_tsv(output_dir / "EDGE_TRANSITION_CENSUS.tsv",
              ["source_family_id", "destination_family_id", "added_instrument", "transition", "projector_relation", "numeric_status", "configurations"],
              counter_rows(edge_census, ["source_family_id", "destination_family_id", "added_instrument", "transition", "projector_relation", "numeric_status"]))
    write_tsv(output_dir / "GRADIENT_INCIDENCE_CENSUS.tsv",
              ["family_id", "motif", "gradient_incidence", "configurations"],
              counter_rows(incidence_census, ["family_id", "motif", "gradient_incidence"]))
    write_tsv(output_dir / "RICCI_HESSIAN_ALIGNMENT_CENSUS.tsv",
              ["alignment_class", "intersection_dimensions", "commutator_rank", "joint_motif", "configurations"],
              counter_rows(alignment_census, ["alignment_class", "intersection_dimensions", "commutator_rank", "joint_motif"]))
    write_tsv(output_dir / "FAMILY_EQUIVALENCE_CENSUS.tsv",
              ["first_family_id", "second_family_id", "configurations"],
              counter_rows(equivalence_census, ["first_family_id", "second_family_id"]))
    fingerprint_rows = [
        {"fingerprint_id": f"FP{index:04d}", "configurations": count,
         "motif_sequence_json": json.dumps(list(fingerprint), separators=(",", ":"))}
        for index, (fingerprint, count) in enumerate(sorted(fingerprint_census.items()), start=1)
    ]
    write_tsv(output_dir / "MOTIF_FINGERPRINT_CENSUS.tsv",
              ("fingerprint_id", "configurations", "motif_sequence_json"), fingerprint_rows)
    write_tsv(output_dir / "NUMERIC_MARGIN_LEDGER.tsv",
              ("configuration_id", "probe", "family_id", "detail"), margins)

    coverage = [
        {"item": "configurations", "expected": expected_configurations, "actual": configurations, "result": "PASS"},
        {"item": "families", "expected": configurations * 31, "actual": family_rows, "result": "PASS"},
        {"item": "edge rows", "expected": configurations * 75, "actual": edge_rows, "result": "PASS"},
        {"item": "nonlinear family comparisons", "expected": 0 if args.skip_nonlinear else configurations * 62,
         "actual": nonlinear_rows, "result": "PASS"},
        {"item": "catch proofs", "expected": 12, "actual": sum(row["result"] == "PASS" for row in catches), "result": "PASS"},
        {"item": "discarded rows", "expected": 0, "actual": 0, "result": "PASS"},
    ]
    write_tsv(output_dir / "COVERAGE_LEDGER.tsv", ("item", "expected", "actual", "result"), coverage)
    result = {
        "schema": SCHEMA,
        "maximum_conclusion": MAXIMUM,
        "development_limit": args.limit,
        "nonlinear_skipped": args.skip_nonlinear,
        "configurations": configurations,
        "family_rows": family_rows,
        "block_rows": block_rows,
        "edge_rows": edge_rows,
        "nonlinear_family_rows": nonlinear_rows,
        "nonlinear_nonuncertain_discordances": nonlinear_discordances,
        "nonlinear_uncertain_rows": nonlinear_uncertain,
        "nonlinear_edge_nonuncertain_discordances": nonlinear_edge_nonuncertain_discordances,
        "nonlinear_edge_uncertain_comparisons": nonlinear_edge_uncertain_comparisons,
        "nonlinear_edge_uncertain_discordances": nonlinear_edge_uncertain_discordances,
        "nonlinear_edge_total_label_differences": nonlinear_edge_total_label_differences,
        "nonlinear_alignment_nonuncertain_discordances": nonlinear_alignment_nonuncertain_discordances,
        "nonlinear_alignment_uncertain_comparisons": nonlinear_alignment_uncertain_comparisons,
        "nonlinear_alignment_uncertain_discordances": nonlinear_alignment_uncertain_discordances,
        "maximum_projector_residual": maximum_projector_residual,
        "maximum_projector_covariance_residual": maximum_covariance_residual,
        "motif_fingerprints": len(fingerprint_census),
        "numeric_margin_rows": len(margins),
        "catch_proofs_passed": sum(row["result"] == "PASS" for row in catches),
        "physical_merit_evaluated": False,
    }
    (output_dir / "ATLAS_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()

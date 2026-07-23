#!/usr/bin/env python3
"""Build the preregistered complete temporal-soldering atlas."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import itertools
import json
import math
import multiprocessing as mp
import os
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "d7a2469ae3a76a099e78656c9357710bf8645843"
MOTIF = ROOT / "udt_motif_hopf_correspondence_audit_2026-07-22"
GLOBAL = ROOT / "udt_global_metric_assembly_atlas_2026-07-22"
CHART = ROOT / "udt_chart_coframe_invariance_atlas_2026-07-21"
COCYCLE = ROOT / "udt_global_coframe_cocycle_audit_2026-07-20"
SEAL = ROOT / "udt_complete_seal_fixed_set_selector_audit_2026-07-21"
sys.path.insert(0, str(MOTIF))
sys.path.insert(0, str(GLOBAL))

import build_correspondence_atlas as prior  # noqa: E402
import build_global_assembly_atlas as assembly  # noqa: E402
from motif_core import signature_record  # noqa: E402


SCHEMA = "udt-temporal-soldering-atlas-1.0"
PATH_NODES = 17
H_STEPS = prior.H_STEPS
SOURCE_PATTERNS = (
    "udt_structural_ensemble_metric_atlas_2026-07-21/RAW_CONFIGURATION_JETS_B*.jsonl",
    "udt_structural_ensemble_metric_atlas_2026-07-21/RAW_SHARD_REGISTRY.tsv",
    "udt_structural_ensemble_metric_atlas_2026-07-21/ENSEMBLE_REGISTRY.tsv",
    "udt_structural_ensemble_metric_atlas_2026-07-21/ENSEMBLE_MASK_REGISTRY.tsv",
    "udt_structural_ensemble_metric_atlas_2026-07-21/CARRIER_VECTOR_REGISTRY.tsv",
    "udt_joint_invariant_subspace_atlas_2026-07-21/FAMILY_SUBSPACE_ATLAS.tsv",
    "udt_joint_invariant_subspace_atlas_2026-07-21/FAMILY_CLASS_CENSUS.tsv",
    "udt_joint_invariant_subspace_atlas_2026-07-21/UNIQUE_SPLIT_ESCALATION_CENSUS.tsv",
    "udt_joint_invariant_subspace_atlas_2026-07-21/BIVECTOR_CLASS_CENSUS.tsv",
    "udt_instrument_motif_atlas_2026-07-21/FAMILY_MOTIF_ATLAS.tsv.gz",
    "udt_instrument_motif_atlas_2026-07-21/FAMILY_MOTIF_CENSUS.tsv",
    "udt_instrument_motif_atlas_2026-07-21/MOTIF_FINGERPRINT_CENSUS.tsv",
    "udt_instrument_motif_atlas_2026-07-21/BLOCK_SIGNATURE_CENSUS.tsv",
    "udt_instrument_motif_atlas_2026-07-21/FAMILY_EQUIVALENCE_CENSUS.tsv",
    "udt_instrument_motif_atlas_2026-07-21/GRADIENT_INCIDENCE_CENSUS.tsv",
    "udt_instrument_motif_atlas_2026-07-21/RICCI_HESSIAN_ALIGNMENT_CENSUS.tsv",
    "udt_instrument_motif_atlas_2026-07-21/EDGE_TRANSITION_CENSUS.tsv",
    "udt_instrument_motif_atlas_2026-07-21/EDGE_INTERACTION_ATLAS.tsv.gz",
    "udt_global_metric_assembly_atlas_2026-07-22/PATH_ASSEMBLY_CENSUS.tsv.gz",
    "udt_global_metric_assembly_atlas_2026-07-22/DENSE_TRANSPORT_ATLAS.tsv",
    "udt_global_metric_assembly_atlas_2026-07-22/NUMERIC_MARGIN_LEDGER.tsv",
    "udt_global_metric_assembly_atlas_2026-07-22/BUNDLE_HOLONOMY_ATLAS.tsv",
    "udt_chart_coframe_invariance_atlas_2026-07-21/INVARIANCE_CENSUS.tsv",
    "udt_chart_coframe_invariance_atlas_2026-07-21/TRANSFORMED_SPAN_RANKS.tsv",
    "udt_chart_coframe_invariance_atlas_2026-07-21/CONFIGURATION_ORBIT_SHARDS.tsv",
    "udt_chart_coframe_invariance_atlas_2026-07-21/TRANSFORMATION_REGISTRY.tsv",
    "udt_global_coframe_cocycle_audit_2026-07-20/COCYCLE_CLASSIFICATION.tsv",
    "udt_global_kinematic_assembly_p03g_2026-07-21/GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv",
    "udt_complete_seal_fixed_set_selector_audit_2026-07-21/INTERPRETATION_SELECTOR.tsv",
    "udt_motif_hopf_correspondence_audit_2026-07-22/COHERENT_IDENTITY_REGISTRY.tsv",
    "udt_motif_hopf_correspondence_audit_2026-07-22/PATH_FAMILY_ATLAS.tsv.gz",
    "udt_motif_hopf_correspondence_audit_2026-07-22/PATH_CONTINUATION_SUMMARY.tsv.gz",
    "udt_motif_hopf_correspondence_audit_2026-07-22/PATH_MOTIF_PERSISTENCE.tsv",
    "udt_motif_hopf_correspondence_audit_2026-07-22/DISTRIBUTION_ATLAS.tsv.gz",
    "udt_motif_hopf_correspondence_audit_2026-07-22/DISTRIBUTION_CENSUS.tsv",
    "udt_motif_hopf_correspondence_audit_2026-07-22/FAMILY_TRANSITION_CENSUS.tsv",
    "udt_motif_hopf_correspondence_audit_2026-07-22/MIDPOINT_MOTIF_CENSUS.tsv",
)

PATH_FIELDS = (
    "identity_id", "family_id", "bank", "carrier_id", "mask_id", "motif_word",
    "stable_projector_path", "node_rows", "node_signature_word", "local_temporal_class",
    "negative_line_nodes", "lorentz_subspace_dimension", "presentation_status",
    "continuity_status", "orientation_status", "global_status",
)
COMPLEMENT_FIELDS = (
    "identity_id", "family_id", "path_node", "t", "motif", "timelike_projector_index",
    "timelike_signature", "orthogonal_complement_signature", "projector_match_status",
    "max_projector_match_distance", "derivative_convergence_residual",
    "frobenius_obstruction_h", "frobenius_obstruction_h2", "frobenius_class",
    "orientation_status", "slicing_status",
)
LINE_FIELDS = (
    "identity_id", "family_id", "motif", "nodes", "local_line_status",
    "all_node_complement_status", "integrable_nodes", "nonintegrable_nodes", "uncertain_nodes",
    "highest_unconditional_completion_rung", "conditional_next_rung", "global_line_status",
    "time_orientation_status", "lapse_status", "shift_status", "connector_status",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def canonical_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def iter_tsv(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        yield from csv.DictReader(handle, delimiter="\t")


def read_tsv(path: Path) -> list[dict[str, str]]:
    return list(iter_tsv(path))


def write_tsv(path: Path, fields, rows) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class DeterministicGzipWriter:
    def __init__(self, path: Path, fields):
        self.raw = path.open("wb")
        self.compressed = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.text = io.TextIOWrapper(self.compressed, encoding="utf-8", newline="")
        self.writer = csv.DictWriter(self.text, fieldnames=list(fields), delimiter="\t", lineterminator="\n")
        self.writer.writeheader()

    def writerows(self, rows) -> None:
        self.writer.writerows(rows)

    def close(self) -> None:
        self.text.flush()
        self.text.close()
        self.raw.close()


def source_paths() -> list[Path]:
    result = []
    for pattern in SOURCE_PATTERNS:
        matches = sorted(ROOT.glob(pattern))
        if not matches:
            raise AssertionError(f"missing frozen source pattern {pattern}")
        result.extend(matches)
    paths = sorted(set(result))
    if len(paths) != len(result):
        raise AssertionError("duplicate frozen source expansion")
    return paths


def frozen_source_rows() -> list[dict[str, object]]:
    rows = []
    for path in source_paths():
        relative = path.relative_to(ROOT).as_posix()
        blob = subprocess.check_output(["git", "rev-parse", f"{BASE}:{relative}"], cwd=ROOT, text=True).strip()
        base_bytes = int(subprocess.check_output(["git", "cat-file", "-s", blob], cwd=ROOT, text=True).strip())
        actual = digest(path)
        working_blob = subprocess.check_output(["git", "hash-object", relative], cwd=ROOT, text=True).strip()
        if working_blob != blob or path.stat().st_size != base_bytes:
            raise AssertionError(f"frozen source differs from base: {relative}")
        rows.append({"path": relative, "base_blob": blob, "sha256": actual, "bytes": base_bytes})
    return rows


def node_temporal_class(rows: list[dict[str, str]]) -> str:
    if any(row["numeric_status"] != "NUMERIC_CLASSIFIED" for row in rows):
        return "TRANSITION_OR_NUMERICALLY_UNCERTAIN"
    motifs = {row["motif"] for row in rows}
    if len(motifs) != 1:
        return "TRANSITION_OR_NUMERICALLY_UNCERTAIN"
    signatures = {(row["primitive_block_ranks"], row["primitive_block_signatures"]) for row in rows}
    if len(signatures) != 1:
        return "TRANSITION_OR_NUMERICALLY_UNCERTAIN"
    ranks, signature = next(iter(signatures))
    motif = next(iter(motifs))
    if motif == "FOUR_LINES" and ranks == "1;1;1;1" and signature == "N0_P1_Z0;N0_P1_Z0;N0_P1_Z0;N1_P0_Z0":
        return "UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE"
    if motif == "LINE_PLUS_THREE" and ranks == "1;3" and signature == "N0_P3_Z0;N1_P0_Z0":
        return "UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE"
    if motif == "LINE_PLUS_THREE" and ranks == "1;3" and signature == "N0_P1_Z0;N1_P2_Z0":
        return "RANK_ONE_LINE_SPACELIKE__LORENTZ_COMPLEMENT"
    if motif == "TWO_PLUS_TWO_LINES" and ranks == "1;1;2" and signature == "N0_P1_Z0;N0_P1_Z0;N1_P1_Z0":
        return "LORENTZ_TWO_PLANE_ONLY"
    if motif in {"FULL_IRREDUCIBLE_4", "SCALAR_4_AMBIGUITY"} and ranks == "4" and signature == "N1_P3_Z0":
        return "NO_PROPER_INTRINSIC_TEMPORAL_SUBSPACE"
    if any("N1_" in row["primitive_block_signatures"] for row in rows):
        return "LORENTZ_SUBSPACE_DIMENSION_GE_2_ONLY"
    return "SIGNATURE_OR_PROJECTOR_DATA_MISSING"


def build_path_atlas():
    summary = {(r["identity_id"], r["family_id"]): r for r in iter_tsv(MOTIF / "PATH_CONTINUATION_SUMMARY.tsv.gz")}
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in iter_tsv(MOTIF / "PATH_FAMILY_ATLAS.tsv.gz"):
        grouped[(row["identity_id"], row["family_id"])].append(row)
    if len(grouped) != 95_232 or set(grouped) != set(summary):
        raise AssertionError("path universe/parent overlap mismatch")

    assembly_keys = {(r["identity_id"], r["family_id"]) for r in iter_tsv(GLOBAL / "PATH_ASSEMBLY_CENSUS.tsv.gz")}
    if assembly_keys != set(grouped):
        raise AssertionError("assembly projection overlap mismatch")

    paths = []
    eligible: dict[str, list[str]] = defaultdict(list)
    for key in sorted(grouped):
        rows = sorted(grouped[key], key=lambda row: int(row["path_node"]))
        if len(rows) != PATH_NODES or [int(r["path_node"]) for r in rows] != list(range(PATH_NODES)):
            raise AssertionError(f"node coverage mismatch {key}")
        parent = summary[key]
        temporal = node_temporal_class(rows)
        if parent["stable_projector_path"] != "YES":
            temporal = "TRANSITION_OR_NUMERICALLY_UNCERTAIN"
        if temporal == "UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE":
            eligible[key[0]].append(key[1])
        signature_word = ";".join(f"{r['primitive_block_ranks']}:{r['primitive_block_signatures']}" for r in rows)
        negative_nodes = sum("N1_P0_Z0" in r["primitive_block_signatures"].split(";") for r in rows)
        lorentz_dim = {
            "UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE": "1",
            "RANK_ONE_LINE_SPACELIKE__LORENTZ_COMPLEMENT": "3",
            "LORENTZ_TWO_PLANE_ONLY": "2",
            "LORENTZ_SUBSPACE_DIMENSION_GE_2_ONLY": ">=2",
            "NO_PROPER_INTRINSIC_TEMPORAL_SUBSPACE": "4_UNDISTINGUISHED",
            "TRANSITION_OR_NUMERICALLY_UNCERTAIN": "UNRESOLVED",
            "SIGNATURE_OR_PROJECTOR_DATA_MISSING": "MISSING",
        }[temporal]
        paths.append({
            "identity_id": key[0], "family_id": key[1], "bank": rows[0]["bank"],
            "carrier_id": rows[0]["carrier_id"], "mask_id": rows[0]["mask_id"],
            "motif_word": parent["distinct_motifs"], "stable_projector_path": parent["stable_projector_path"],
            "node_rows": PATH_NODES, "node_signature_word": canonical_hash(signature_word),
            "local_temporal_class": temporal, "negative_line_nodes": negative_nodes,
            "lorentz_subspace_dimension": lorentz_dim,
            "presentation_status": "INSTRUMENT_FAMILY_PRESENTATION__NOT_PHYSICAL_UNIVERSE",
            "continuity_status": (
                "SAMPLED_PERSISTENT_17_NODES__CONTINUOUS_INTERVAL_NOT_CERTIFIED"
                if temporal == "UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE"
                else "NO_UNIQUE_SAMPLED_LINE"
            ),
            "orientation_status": "PROJECTOR_IMAGE_UNORIENTED",
            "global_status": "GLOBAL_LINE_BUNDLE_NOT_ESTABLISHED",
        })
    return paths, dict(eligible)


IDENTITY_BY_ID = {str(row["identity_id"]): row for row in prior.identities()}
FAMILY_BY_ID = {str(row["family_id"]): row for row in prior.FAMILIES}


def classify_selected(identity, families, point):
    amplitudes = np.asarray(identity["amplitudes"], dtype=float)
    analytic = prior.volume.previous.regular_family(int(identity["bank"]), amplitudes, np.asarray(point, dtype=float))
    geometry = prior.evaluate_metric_jets(analytic["metric_jets"])
    phi = analytic["phi"]
    objects = prior.intrinsic_objects(geometry, np.asarray(phi.first), np.asarray(phi.second))
    scalar = {key: objects[key] for key in ("R", "H", "D")}
    results = {}
    for family in families:
        keys = tuple(family["keys"])
        result = prior.classify_motif_family(
            prior.family_operators(objects, keys), objects["gradient"], objects["metric"], scalar, keys
        )
        result["projector_validation_residual"] = prior.projector_validation(result, objects, keys)
        results[str(family["family_id"])] = result
    return geometry, results


def line_index(result) -> int:
    labels = prior.block_labels(result)
    matches = [index for index, label in enumerate(labels) if label == (1, "N1_P0_Z0")]
    if len(matches) != 1:
        raise RuntimeError(f"expected one timelike line, found {matches}")
    return matches[0]


def complement_worker(task):
    identity_id, family_ids = task
    identity = IDENTITY_BY_ID[identity_id]
    families = [FAMILY_BY_ID[value] for value in family_ids]
    start = np.asarray(identity["start_point"], dtype=float)
    end = np.asarray(identity["end_point"], dtype=float)
    output = []
    for node in range(PATH_NODES):
        t = node / (PATH_NODES - 1)
        point = (1.0 - t) * start + t * end
        geometry, centers = classify_selected(identity, families, point)
        stencil = {}
        for step in H_STEPS:
            for axis in range(4):
                for sign in (-1, 1):
                    neighbor = point.copy()
                    neighbor[axis] += sign * step
                    _neighbor_geometry, results = classify_selected(identity, families, neighbor)
                    stencil[(step, axis, sign)] = results
        for family in families:
            family_id = str(family["family_id"])
            center = centers[family_id]
            index = line_index(center)
            projectors = [np.asarray(value, dtype=float) for value in center["projectors"]]
            derivatives = {}
            max_match = 0.0
            for step in H_STEPS:
                derivative = np.zeros((4, 4, 4))
                for axis in range(4):
                    minus, _permutation, distance_minus = prior.matched_projectors(center, stencil[(step, axis, -1)][family_id])
                    plus, _permutation, distance_plus = prior.matched_projectors(center, stencil[(step, axis, 1)][family_id])
                    if minus is None or plus is None:
                        raise RuntimeError(f"projector match failed {identity_id} {family_id} node {node}")
                    max_match = max(max_match, distance_minus, distance_plus)
                    derivative[axis] = -(plus[index] - minus[index]) / (2.0 * step)
                derivatives[step] = derivative
            complement = np.eye(4) - projectors[index]
            metric = np.asarray(geometry.metric, dtype=float)
            complement_signature = signature_record(complement, metric)["signature"]
            convergence = float(np.linalg.norm(derivatives[H_STEPS[0]] - derivatives[H_STEPS[1]]) / max(np.linalg.norm(derivatives[H_STEPS[1]]), 1.0))
            obstruction_h = prior.frobenius_obstruction(complement, derivatives[H_STEPS[0]], np.asarray(geometry.christoffel))
            obstruction_h2 = prior.frobenius_obstruction(complement, derivatives[H_STEPS[1]], np.asarray(geometry.christoffel))
            frobenius = prior.obstruction_class(obstruction_h2, convergence)
            output.append({
                "identity_id": identity_id, "family_id": family_id, "path_node": node, "t": f"{t:.17g}",
                "motif": center["motif"], "timelike_projector_index": index,
                "timelike_signature": "N1_P0_Z0", "orthogonal_complement_signature": complement_signature,
                "projector_match_status": "ALL_16_STENCIL_MATCHES", "max_projector_match_distance": f"{max_match:.17g}",
                "derivative_convergence_residual": f"{convergence:.17g}",
                "frobenius_obstruction_h": f"{obstruction_h:.17g}",
                "frobenius_obstruction_h2": f"{obstruction_h2:.17g}", "frobenius_class": frobenius,
                "orientation_status": "PROJECTOR_IMAGE_UNORIENTED",
                "slicing_status": (
                    "LOCAL_ORTHOGONAL_FOLIATION_SAMPLED_AT_NODE__NO_TIME_ORIENTATION"
                    if frobenius == "NUMERICALLY_INTEGRABLE_LOCAL" else
                    "LOCAL_ORTHOGONAL_FOLIATION_NOT_CERTIFIED"
                ),
            })
    return output


def build_complements(eligible, jobs: int):
    tasks = [(identity_id, sorted(families)) for identity_id, families in sorted(eligible.items())]
    rows = []
    if jobs == 1:
        iterator = map(complement_worker, tasks)
    else:
        pool = mp.Pool(processes=jobs)
        iterator = pool.imap(complement_worker, tasks, chunksize=1)
    try:
        for result in iterator:
            rows.extend(result)
    finally:
        if jobs != 1:
            pool.close()
            pool.join()
    rows.sort(key=lambda row: (row["identity_id"], row["family_id"], int(row["path_node"])))
    if len(rows) != 1_775 * PATH_NODES:
        raise AssertionError(f"complement coverage {len(rows)}")
    return rows


def build_line_summary(path_rows, complement_rows):
    path_by_key = {(r["identity_id"], r["family_id"]): r for r in path_rows}
    grouped = defaultdict(list)
    for row in complement_rows:
        grouped[(row["identity_id"], row["family_id"])].append(row)
    rows = []
    for key in sorted(grouped):
        nodes = grouped[key]
        if len(nodes) != PATH_NODES:
            raise AssertionError(f"line node coverage {key}")
        census = Counter(row["frobenius_class"] for row in nodes)
        integrable = census["NUMERICALLY_INTEGRABLE_LOCAL"]
        nonintegrable = census["NUMERICALLY_NONINTEGRABLE_LOCAL"]
        uncertain = PATH_NODES - integrable - nonintegrable
        if integrable == PATH_NODES:
            status = "ALL_17_NODES_SAMPLED_INTEGRABLE"
            conditional = "LOCAL_HYPERSURFACE_ORTHOGONAL_THREADING_IF_CONTINUITY_AND_ORIENTATION_SUPPLIED"
        elif nonintegrable:
            status = "NONINTEGRABILITY_OBSERVED_AT_ONE_OR_MORE_NODES"
            conditional = "NONE"
        else:
            status = "NUMERICALLY_UNCERTAIN_AT_ONE_OR_MORE_NODES"
            conditional = "NONE"
        rows.append({
            "identity_id": key[0], "family_id": key[1], "motif": path_by_key[key]["motif_word"],
            "nodes": PATH_NODES, "local_line_status": "UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE_AT_ALL_17_NODES",
            "all_node_complement_status": status, "integrable_nodes": integrable,
            "nonintegrable_nodes": nonintegrable, "uncertain_nodes": uncertain,
            "highest_unconditional_completion_rung": "1_LOCAL_UNORIENTED_LINE",
            "conditional_next_rung": conditional,
            "global_line_status": "OPEN__NO_PROJECTOR_LINE_COCYCLE_OR_COMPLETE_METRIC_GLUE",
            "time_orientation_status": "OPEN__NO_SIGN_SECTION",
            "lapse_status": "OPEN__NO_SELECTED_TIME_FUNCTION_OR_NORMALIZATION",
            "shift_status": "OPEN__NO_SELECTED_SLICING_OR_THREAD_CONGRUENCE",
            "connector_status": "OPEN__LINE_IS_NOT_FULL_OPTICAL_CONNECTOR",
        })
    return rows


def build_class_census(path_rows):
    class_groups = defaultdict(list)
    for row in path_rows:
        class_groups[row["local_temporal_class"]].append(row)
    rows = []
    for classification in sorted(class_groups):
        values = class_groups[classification]
        rows.append({
            "local_temporal_class": classification,
            "path_presentations": len(values),
            "unique_analytic_identities": len({r["identity_id"] for r in values}),
            "fraction_of_95232": f"{len(values) / 95232:.17g}",
            "physical_universe_count": "NOT_INFERRED",
        })
    return rows


def build_chart_census(path_rows):
    transformations = read_tsv(CHART / "TRANSFORMATION_REGISTRY.tsv")
    class_counts = Counter(row["local_temporal_class"] for row in path_rows)
    rows = []
    for transform in transformations:
        determinant = float(transform["determinant"])
        if abs(determinant) <= 1.0e-12:
            raise AssertionError(f"singular registered transformation {transform['transform_id']}")
        for classification in sorted(class_counts):
            rows.append({
                "transform_id": transform["transform_id"], "kind": transform["kind"],
                "local_temporal_class": classification, "path_presentations": class_counts[classification],
                "node_presentations": class_counts[classification] * PATH_NODES,
                "invariance_basis": (
                    "P_PRIME=J_INV_P_J__G_PRIME=J_TRANSPOSE_G_J__RESTRICTION_CONGRUENCE"
                    if transform["kind"] == "COORDINATE" else
                    "INTERNAL_COFRAME_GAUGE__COORDINATE_METRIC_AND_PROJECTOR_IMAGE_UNCHANGED"
                ),
                "status": "EXACT_CLASS_INVARIANCE_FOR_ALL_RETAINED_PRESENTATIONS",
            })
    return rows


def build_completion_ladder(line_rows):
    all_integrable = sum(r["all_node_complement_status"] == "ALL_17_NODES_SAMPLED_INTEGRABLE" for r in line_rows)
    nonintegrable = sum("NONINTEGRABILITY" in r["all_node_complement_status"] for r in line_rows)
    uncertain = len(line_rows) - all_integrable - nonintegrable
    return [
        {"rung": 1, "name": "LOCAL_UNORIENTED_LINE", "unconditional_paths": len(line_rows), "status": "OBSERVED_AT_ALL_17_SAMPLED_NODES"},
        {"rung": 2, "name": "LOCAL_CONTINUOUS_LINE_BUNDLE_ON_OPEN_PATH", "unconditional_paths": 0, "status": "OPEN__17_NODE_PERSISTENCE_IS_NOT_INTERVAL_CERTIFICATION"},
        {"rung": 3, "name": "LOCAL_TIME_ORIENTATION_SUPPLIED", "unconditional_paths": 0, "status": "OPEN__NO_SIGN_SECTION"},
        {"rung": 4, "name": "LOCAL_HYPERSURFACE_ORTHOGONAL_THREADING", "unconditional_paths": 0, "status": f"CONDITIONAL__{all_integrable}_ALL_NODE_INTEGRABLE__{nonintegrable}_NONINTEGRABLE__{uncertain}_UNCERTAIN"},
        {"rung": 5, "name": "GLOBAL_LINE_BUNDLE", "unconditional_paths": 0, "status": "OPEN__NO_PROJECTOR_LINE_TRANSITION_COCYCLE"},
        {"rung": 6, "name": "GLOBAL_TIME_ORIENTED_THREADING", "unconditional_paths": 0, "status": "OPEN__GLOBAL_LINE_AND_ORIENTATION_ABSENT"},
        {"rung": 7, "name": "FULL_OPTICAL_CONNECTOR", "unconditional_paths": 0, "status": "OPEN__TIME_FUNCTION_SCALE_CURVE_AND_ENDPOINT_SOLDERING_ABSENT"},
    ]


def selector_rows():
    return [
        {"selector": "COMPLETE_METRIC_PLUS_REGISTERED_NATIVE_INSTRUMENTS", "line_selection": "SELECTS_ON_1775_OF_95232_PATH_PRESENTATIONS", "orientation": "SILENT", "slicing": "CONSTRAINS_NOT_SELECTS", "global_glue": "OPEN", "reason": "a simple negative invariant block occurs only on the registered subset"},
        {"selector": "RECIPROCITY", "line_selection": "CONSTRAINS_NOT_SELECTS", "orientation": "SILENT", "slicing": "SILENT", "global_glue": "CONSTRAINS_NOT_SELECTS", "reason": "ratio and transition parity do not identify a negative projector image"},
        {"selector": "COMMON_SCALE_NEUTRALITY", "line_selection": "SILENT", "orientation": "SILENT", "slicing": "SILENT", "global_glue": "SILENT", "reason": "positive common scale preserves signature and projector images"},
        {"selector": "FINITE_CELL", "line_selection": "SILENT", "orientation": "SILENT", "slicing": "SILENT", "global_glue": "CONSTRAINS_NOT_SELECTS", "reason": "finite domain does not choose boundary/cap/quotient or line transition functions"},
        {"selector": "STATIC_SEAL", "line_selection": "CONDITIONAL_BASE_CONTROL_ONLY", "orientation": "NO_SELECTION", "slicing": "CONSTRAINS_NOT_SELECTS", "global_glue": "CONSTRAINS_NOT_SELECTS", "reason": "all four existing lifts fix an already conditional base timelike line; no lift is selected"},
        {"selector": "BOOTSTRAP", "line_selection": "OPEN", "orientation": "OPEN", "slicing": "OPEN", "global_glue": "OPEN", "reason": "current bootstrap is on-shell admissibility without an off-shell ranking functional"},
    ]


def reconstruction_rows():
    return [
        {"object": "LOCAL_NULL_CONE", "requires": "LORENTZIAN_METRIC_REPRESENTATIVE", "status": "CONDITIONAL_METRIC_READOUT_AVAILABLE", "not_supplied": "PREFERRED_OBSERVER_OR_CLOCK"},
        {"object": "UNIT_TIMELIKE_VECTOR_UP_TO_SIGN", "requires": "UNIQUE_NEGATIVE_LINE_AND_METRIC_NORMALIZATION", "status": "AVAILABLE_ON_1775_PATH_PRESENTATIONS_AT_SAMPLED_NODES", "not_supplied": "TIME_ORIENTATION"},
        {"object": "SPATIAL_PROJECTOR", "requires": "TIMELIKE_LINE_PROJECTOR", "status": "I_MINUS_P_TIME_AVAILABLE_ON_1775_PATH_PRESENTATIONS", "not_supplied": "GLOBAL_SLICING"},
        {"object": "LOCAL_ORTHOGONAL_SLICES", "requires": "FROBENIUS_INTEGRABLE_SPATIAL_PROJECTOR", "status": "SAMPLED_CONDITIONAL_SUBSET_ONLY", "not_supplied": "CONTINUOUS_CERTIFICATION_AND_TIME_ORIENTATION"},
        {"object": "LAPSE", "requires": "SELECTED_TIME_FUNCTION_AND_NORMALIZATION", "status": "OPEN", "not_supplied": "TIME_FUNCTION"},
        {"object": "SHIFT", "requires": "SELECTED_SLICING_AND_THREAD_CONGRUENCE", "status": "OPEN", "not_supplied": "SLICING_AND_CONGRUENCE"},
        {"object": "FULL_OPTICAL_CONNECTOR", "requires": "GLOBAL_THREADING_SCALE_CURVE_AND_ENDPOINT_SOLDERING", "status": "OPEN", "not_supplied": "ALL_LISTED_JOIN_DATA"},
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=max(1, min(12, os.cpu_count() or 1)))
    args = parser.parse_args()
    source_rows = frozen_source_rows()
    path_rows, eligible = build_path_atlas()
    complement_rows = build_complements(eligible, args.jobs)
    line_rows = build_line_summary(path_rows, complement_rows)
    class_rows = build_class_census(path_rows)
    chart_rows = build_chart_census(path_rows)

    writer = DeterministicGzipWriter(HERE / "PATH_TEMPORAL_CLASSIFICATION.tsv.gz", PATH_FIELDS)
    writer.writerows(path_rows)
    writer.close()
    writer = DeterministicGzipWriter(HERE / "ORTHOGONAL_COMPLEMENT_ATLAS.tsv.gz", COMPLEMENT_FIELDS)
    writer.writerows(complement_rows)
    writer.close()
    write_tsv(HERE / "LINE_COMPLETION_ATLAS.tsv", LINE_FIELDS, line_rows)
    write_tsv(HERE / "TEMPORAL_CLASS_CENSUS.tsv", tuple(class_rows[0]), class_rows)
    write_tsv(HERE / "CHART_COFRAME_TEMPORAL_INVARIANCE.tsv", tuple(chart_rows[0]), chart_rows)
    write_tsv(HERE / "COMPLETION_LADDER.tsv", ("rung", "name", "unconditional_paths", "status"), build_completion_ladder(line_rows))
    write_tsv(HERE / "SELECTOR_STATUS.tsv", ("selector", "line_selection", "orientation", "slicing", "global_glue", "reason"), selector_rows())
    write_tsv(HERE / "INVARIANT_RECONSTRUCTION_LEDGER.tsv", ("object", "requires", "status", "not_supplied"), reconstruction_rows())
    write_tsv(HERE / "FROZEN_SOURCE_LEDGER.tsv", ("path", "base_blob", "sha256", "bytes"), source_rows)

    frobenius = Counter(row["frobenius_class"] for row in complement_rows)
    line_status = Counter(row["all_node_complement_status"] for row in line_rows)
    result = {
        "schema": SCHEMA,
        "base": BASE,
        "frozen_source_files": len(source_rows),
        "path_presentations": len(path_rows),
        "path_nodes": len(path_rows) * PATH_NODES,
        "unique_analytic_identities": len({row["identity_id"] for row in path_rows}),
        "local_temporal_class_census": dict(sorted(Counter(row["local_temporal_class"] for row in path_rows).items())),
        "unique_line_path_presentations": len(line_rows),
        "unique_line_analytic_identities": len({row["identity_id"] for row in line_rows}),
        "orthogonal_complement_node_rows": len(complement_rows),
        "frobenius_node_census": dict(sorted(frobenius.items())),
        "line_path_completion_census": dict(sorted(line_status.items())),
        "registered_transformations": len(read_tsv(CHART / "TRANSFORMATION_REGISTRY.tsv")),
        "path_transform_presentations": len(path_rows) * len(read_tsv(CHART / "TRANSFORMATION_REGISTRY.tsv")),
        "highest_unconditional_completion_rung": 1,
        "global_line_bundles_derived": 0,
        "time_orientations_derived": 0,
        "lapses_derived": 0,
        "shifts_derived": 0,
        "full_optical_connectors_derived": 0,
        "cpu_only": True,
        "gpu_runs": 0,
        "actions_loaded": 0,
        "carriers_loaded": 0,
        "sne_fits": 0,
        "maximum_conclusion": "BOUNDED_REGISTERED_TEMPORAL_SOLDERING_ATLAS_CHARACTERIZED__GLOBAL_THREADING_AND_FULL_CONNECTOR_OPEN",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

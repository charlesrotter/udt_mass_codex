#!/usr/bin/env python3
"""Build the preregistered UDT global metric-assembly atlas."""

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
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PRIOR_DIR = ROOT / "udt_motif_hopf_correspondence_audit_2026-07-22"
sys.path.insert(0, str(PRIOR_DIR))

import build_correspondence_atlas as prior  # noqa: E402
from motif_core import projector_set_distance, signature_record  # noqa: E402


SCHEMA = "udt-global-metric-assembly-atlas-1.0"
SOURCE_HASHES = {
    "udt_motif_hopf_correspondence_audit_2026-07-22/SHA256SUMS.txt": "b9dca9e1baca68b82118e1a008829196d9bb834dae69cfa5d82f0ae771902164",
    "udt_instrument_motif_atlas_2026-07-21/SHA256SUMS.txt": "97dac2c32317deb603a054cffd3d2162f537d8bc7806d2276fa7e8544dd22ed5",
    "udt_global_coframe_cocycle_audit_2026-07-20/SHA256SUMS.txt": "1297e8f6773f863f426d66f6c4915741a742c1ee13230abf2b066421de49b04b",
    "complete_coframe_seal_involution_2026-07-20/SHA256SUMS.txt": "87d43cb281d236111a8baec4fe7da5686a8043931e6ba0a2715228f7d61f483e",
    "angular_toric_closure_selector_2026-07-19/SHA256SUMS.txt": "64d664a76a28c170cdc293626cd6a5011755ee4eeaa414a303ace7b6eec9ec50",
    "boundary_bootstrap_representative_selector_audit_2026-07-19/SHA256SUMS.txt": "6cd896586dda87b8e9794818c34ccb392a2f5a004e7d88ba8e288db57e50c6c3",
    "scale_breaking_closure_census_2026-07-20/SHA256SUMS.txt": "53996dfcc0fb9cef29422ff94908fe71aaed32703d49e70e2d6d7f01aa19fe84",
    "matter_bootstrap_dimensional_inventory_2026-07-20/SHA256SUMS.txt": "716c2ad9c071a49f75b4c340d6d980d75cfc0a48b0923c39e0cf3d100759ae77",
}

DERIVATIVE_STEP = 1.0e-5
TRANSPORT_NODES = (33, 65, 129)
TRANSPORT_PASS = 2.0e-7
TRANSPORT_REFINEMENT_PASS = 5.0e-6
FOLLOW_NODES = 9
H_STEPS = prior.H_STEPS

IDENTITIES = prior.identities()
IDENTITY_BY_ID = {str(row["identity_id"]): row for row in IDENTITIES}
FAMILY_BY_ID = {str(row["family_id"]): row for row in prior.FAMILIES}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def relmax(first: np.ndarray, second: np.ndarray) -> float:
    left = np.asarray(first, dtype=float)
    right = np.asarray(second, dtype=float)
    return float(np.max(np.abs(left - right)) / max(1.0, float(np.max(np.abs(left))), float(np.max(np.abs(right)))))


def read_tsv(path: Path) -> list[dict[str, str]]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def iter_tsv(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        yield from csv.DictReader(handle, delimiter="\t")


def write_tsv(path: Path, rows: list[dict[str, object]], fields: tuple[str, ...] | None = None) -> None:
    if fields is None:
        if not rows:
            raise ValueError(f"fields required for empty table {path}")
        fields = tuple(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class DeterministicGzipWriter:
    def __init__(self, path: Path, fields: tuple[str, ...]):
        self.raw = path.open("wb")
        self.compressed = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.text = io.TextIOWrapper(self.compressed, encoding="utf-8", newline="")
        self.writer = csv.DictWriter(self.text, fieldnames=list(fields), delimiter="\t", lineterminator="\n")
        self.writer.writeheader()

    def writerows(self, rows):
        self.writer.writerows(rows)

    def close(self):
        self.text.flush()
        self.text.close()
        self.raw.close()


def verify_sources() -> None:
    for source, expected in SOURCE_HASHES.items():
        actual = digest(ROOT / source)
        if actual != expected:
            raise AssertionError(f"frozen source mismatch {source}: {actual} != {expected}")


def point_on_path(identity: dict[str, object], t: float) -> np.ndarray:
    start = np.asarray(identity["start_point"], dtype=float)
    end = np.asarray(identity["end_point"], dtype=float)
    return (1.0 - t) * start + t * end


def classify_specific(identity: dict[str, object], family: dict[str, object], point: np.ndarray):
    amplitudes = np.asarray(identity["amplitudes"], dtype=float)
    analytic = prior.volume.previous.regular_family(int(identity["bank"]), amplitudes, np.asarray(point, dtype=float))
    geometry = prior.evaluate_metric_jets(analytic["metric_jets"])
    phi = analytic["phi"]
    objects = prior.intrinsic_objects(geometry, np.asarray(phi.first), np.asarray(phi.second))
    scalar = {key: objects[key] for key in ("R", "H", "D")}
    result = prior.classify_motif_family(
        prior.family_operators(objects, tuple(family["keys"])),
        objects["gradient"],
        objects["metric"],
        scalar,
        tuple(family["keys"]),
    )
    result["projector_validation_residual"] = prior.projector_validation(result, objects, tuple(family["keys"]))
    return geometry, result


def endpoint_derivative(identity, family, t: float, center: dict[str, object]):
    eps = DERIVATIVE_STEP
    center_projectors = [np.asarray(value, dtype=float) for value in center["projectors"]]
    if t <= eps:
        samples = []
        for offset in (eps, 2.0 * eps):
            _geometry, result = classify_specific(identity, family, point_on_path(identity, t + offset))
            matched, _permutation, _distance = prior.matched_projectors(center, result)
            if matched is None:
                raise RuntimeError("forward projector derivative match failed")
            samples.append(matched)
        derivatives = [
            (-3.0 * center_projectors[index] + 4.0 * samples[0][index] - samples[1][index]) / (2.0 * eps)
            for index in range(len(center_projectors))
        ]
    elif t >= 1.0 - eps:
        samples = []
        for offset in (eps, 2.0 * eps):
            _geometry, result = classify_specific(identity, family, point_on_path(identity, t - offset))
            matched, _permutation, _distance = prior.matched_projectors(center, result)
            if matched is None:
                raise RuntimeError("backward projector derivative match failed")
            samples.append(matched)
        derivatives = [
            (3.0 * center_projectors[index] - 4.0 * samples[0][index] + samples[1][index]) / (2.0 * eps)
            for index in range(len(center_projectors))
        ]
    else:
        _minus_geometry, minus = classify_specific(identity, family, point_on_path(identity, t - eps))
        _plus_geometry, plus = classify_specific(identity, family, point_on_path(identity, t + eps))
        minus_projectors, _minus_permutation, _minus_distance = prior.matched_projectors(center, minus)
        plus_projectors, _plus_permutation, _plus_distance = prior.matched_projectors(center, plus)
        if minus_projectors is None or plus_projectors is None:
            raise RuntimeError("centered projector derivative match failed")
        derivatives = [
            (plus_projectors[index] - minus_projectors[index]) / (2.0 * eps)
            for index in range(len(center_projectors))
        ]
    return derivatives


def transport_generator(identity, family, t: float):
    geometry, result = classify_specific(identity, family, point_on_path(identity, t))
    if result["numeric_status"] != "NUMERIC_CLASSIFIED":
        raise RuntimeError("uncertain projector classification in dense anchor")
    projectors = [np.asarray(value, dtype=float) for value in result["projectors"]]
    partials = endpoint_derivative(identity, family, t, result)
    tangent = np.asarray(identity["end_point"], dtype=float) - np.asarray(identity["start_point"], dtype=float)
    gamma = np.asarray(geometry.christoffel, dtype=float)
    gamma_t = np.einsum("r,mrn->mn", tangent, gamma)
    covariant = [partial + gamma_t @ projector - projector @ gamma_t for partial, projector in zip(partials, projectors)]
    kato = sum((derivative @ projector for derivative, projector in zip(covariant, projectors)), np.zeros((4, 4)))
    metric = np.asarray(geometry.metric, dtype=float)
    skew = relmax(kato.T @ metric + metric @ kato, np.zeros((4, 4)))
    commutator = max(
        (relmax(kato @ projector - projector @ kato, derivative) for derivative, projector in zip(covariant, projectors)),
        default=0.0,
    )
    return kato - gamma_t, metric, projectors, skew, commutator


def integrate_transport(identity, family, nodes: int):
    steps = nodes - 1
    h = 1.0 / steps
    matrix = np.eye(4)
    cache: dict[float, tuple[np.ndarray, np.ndarray, list[np.ndarray], float, float]] = {}

    def evaluate(t: float):
        key = round(float(t), 14)
        if key not in cache:
            cache[key] = transport_generator(identity, family, float(t))
        return cache[key]

    for index in range(steps):
        t = index * h
        m1 = evaluate(t)[0]
        m2 = evaluate(t + 0.5 * h)[0]
        m4 = evaluate(t + h)[0]
        k1 = m1 @ matrix
        k2 = m2 @ (matrix + 0.5 * h * k1)
        k3 = m2 @ (matrix + 0.5 * h * k2)
        k4 = m4 @ (matrix + h * k3)
        matrix = matrix + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    _m0, metric0, projectors0, _skew0, _comm0 = evaluate(0.0)
    _m1, metric1, projectors1, _skew1, _comm1 = evaluate(1.0)
    inverse = np.linalg.inv(matrix)
    transported = [matrix @ projector @ inverse for projector in projectors0]
    intertwining = projector_set_distance(transported, projectors1)
    isometry = relmax(matrix.T @ metric1 @ matrix, metric0)
    max_skew = max(value[3] for value in cache.values())
    max_commutator = max(value[4] for value in cache.values())
    return {
        "matrix": matrix,
        "intertwining_residual": intertwining,
        "metric_isometry_residual": isometry,
        "max_kato_metric_skew_residual": max_skew,
        "max_kato_commutator_residual": max_commutator,
        "sample_count": len(cache),
    }


def transport_worker(task: tuple[str, str, str]):
    identity_id, family_id, motif = task
    identity = IDENTITY_BY_ID[identity_id]
    family = FAMILY_BY_ID[family_id]
    try:
        solutions = {nodes: integrate_transport(identity, family, nodes) for nodes in TRANSPORT_NODES}
        fine = solutions[129]
        refinement_33_65 = relmax(solutions[33]["matrix"], solutions[65]["matrix"])
        refinement_65_129 = relmax(solutions[65]["matrix"], fine["matrix"])
        max_transport = max(
            fine["intertwining_residual"],
            fine["metric_isometry_residual"],
            fine["max_kato_metric_skew_residual"],
            fine["max_kato_commutator_residual"],
        )
        passed = max_transport <= TRANSPORT_PASS and refinement_65_129 <= TRANSPORT_REFINEMENT_PASS
        status = "DENSE_TRANSPORT_PASS" if passed else "DENSE_TRANSPORT_NUMERIC_MARGIN_RETAINED"
        error = "-"
    except Exception as exc:  # retained fail-closed evidence
        solutions = {}
        fine = {
            "matrix": np.full((4, 4), np.nan),
            "intertwining_residual": math.nan,
            "metric_isometry_residual": math.nan,
            "max_kato_metric_skew_residual": math.nan,
            "max_kato_commutator_residual": math.nan,
            "sample_count": 0,
        }
        refinement_33_65 = math.nan
        refinement_65_129 = math.nan
        status = "DENSE_TRANSPORT_FAILED_RETAINED"
        error = f"{type(exc).__name__}:{exc}"
    return {
        "identity_id": identity_id,
        "family_id": family_id,
        "motif": motif,
        "selection_sha256": hashlib.sha256(f"{identity_id}\t{family_id}".encode()).hexdigest(),
        "nodes_33_samples": solutions.get(33, {}).get("sample_count", 0),
        "nodes_65_samples": solutions.get(65, {}).get("sample_count", 0),
        "nodes_129_samples": fine["sample_count"],
        "intertwining_residual_129": f"{fine['intertwining_residual']:.17g}",
        "metric_isometry_residual_129": f"{fine['metric_isometry_residual']:.17g}",
        "kato_metric_skew_residual_129": f"{fine['max_kato_metric_skew_residual']:.17g}",
        "kato_commutator_residual_129": f"{fine['max_kato_commutator_residual']:.17g}",
        "refinement_33_65": f"{refinement_33_65:.17g}",
        "refinement_65_129": f"{refinement_65_129:.17g}",
        "transport_matrix_sha256": canonical_hash(np.asarray(fine["matrix"]).tolist()),
        "transport_status": status,
        "error": error,
    }


def derivative_projectors_at_point(identity, family, point, center):
    center_projectors = [np.asarray(value, dtype=float) for value in center["projectors"]]
    derivatives_by_step = {}
    max_match = 0.0
    for step in H_STEPS:
        derivatives = [np.zeros((4, 4, 4)) for _ in center_projectors]
        for axis in range(4):
            neighbor_results = []
            for sign in (-1, 1):
                neighbor = np.asarray(point, dtype=float).copy()
                neighbor[axis] += sign * step
                _geometry, result = classify_specific(identity, family, neighbor)
                matched, _permutation, distance = prior.matched_projectors(center, result)
                if matched is None:
                    raise RuntimeError("stencil projector match failed")
                max_match = max(max_match, distance)
                neighbor_results.append(matched)
            minus, plus = neighbor_results
            for index in range(len(center_projectors)):
                derivatives[index][axis] = (plus[index] - minus[index]) / (2.0 * step)
        derivatives_by_step[step] = derivatives
    return derivatives_by_step, max_match


def candidate_node(identity, family, t: float):
    point = point_on_path(identity, t)
    geometry, center = classify_specific(identity, family, point)
    base = {
        "identity_id": identity["identity_id"],
        "family_id": family["family_id"],
        "path_node": int(round(t * (FOLLOW_NODES - 1))),
        "t": f"{t:.17g}",
        "motif": center["motif"],
        "numeric_status": center["numeric_status"],
    }
    if center["numeric_status"] != "NUMERIC_CLASSIFIED" or center["motif"] != "TWO_PLUS_TWO_LINES":
        return {
            **base,
            "lorentz_class": "NOT_AVAILABLE",
            "transverse_class": "NOT_AVAILABLE",
            "lorentz_obstruction": "nan",
            "transverse_obstruction": "nan",
            "max_derivative_convergence": "nan",
            "max_projector_match_distance": "nan",
            "node_status": "MOTIF_CHANGE_OR_NUMERIC_UNCERTAIN_RETAINED",
        }
    splits = prior.complementary_rank_two_splits([np.asarray(value) for value in center["projectors"]])
    if len(splits) != 1:
        return {
            **base,
            "lorentz_class": "NOT_AVAILABLE",
            "transverse_class": "NOT_AVAILABLE",
            "lorentz_obstruction": "nan",
            "transverse_obstruction": "nan",
            "max_derivative_convergence": "nan",
            "max_projector_match_distance": "nan",
            "node_status": "UNIQUE_SPLIT_LOST_RETAINED",
        }
    derivatives, max_match = derivative_projectors_at_point(identity, family, point, center)
    projectors = [np.asarray(value, dtype=float) for value in center["projectors"]]
    gamma = np.asarray(geometry.christoffel, dtype=float)
    side_records = []
    for side in splits[0]:
        members = [index for index, primitive in enumerate(projectors) if prior.relmax(side @ primitive, primitive) <= 1.0e-8]
        partial_h = sum((derivatives[H_STEPS[0]][index] for index in members), np.zeros((4, 4, 4)))
        partial_h2 = sum((derivatives[H_STEPS[1]][index] for index in members), np.zeros((4, 4, 4)))
        convergence = float(np.linalg.norm(partial_h - partial_h2) / max(np.linalg.norm(partial_h2), 1.0))
        obstruction = prior.frobenius_obstruction(np.asarray(side), partial_h2, gamma)
        classification = prior.obstruction_class(obstruction, convergence)
        signature = signature_record(np.asarray(side), np.asarray(geometry.metric))["signature"]
        side_records.append({
            "signature": signature,
            "obstruction": obstruction,
            "convergence": convergence,
            "classification": classification,
        })
    lorentz = next((row for row in side_records if row["signature"] == "N1_P1_Z0"), None)
    transverse = next((row for row in side_records if row["signature"] == "N0_P2_Z0"), None)
    if lorentz is None or transverse is None:
        return {
            **base,
            "lorentz_class": "NOT_AVAILABLE",
            "transverse_class": "NOT_AVAILABLE",
            "lorentz_obstruction": "nan",
            "transverse_obstruction": "nan",
            "max_derivative_convergence": f"{max(row['convergence'] for row in side_records):.17g}",
            "max_projector_match_distance": f"{max_match:.17g}",
            "node_status": "SPLIT_SIGNATURE_MISMATCH_RETAINED",
        }
    both_integrable = all(row["classification"] == "NUMERICALLY_INTEGRABLE_LOCAL" for row in (lorentz, transverse))
    any_nonintegrable = any(row["classification"] == "NUMERICALLY_NONINTEGRABLE_LOCAL" for row in (lorentz, transverse))
    if both_integrable:
        status = "BOTH_SIDES_SAMPLED_INTEGRABLE"
    elif any_nonintegrable:
        status = "NONINTEGRABILITY_OBSERVED"
    else:
        status = "NUMERIC_UNCERTAIN_RETAINED"
    return {
        **base,
        "lorentz_class": lorentz["classification"],
        "transverse_class": transverse["classification"],
        "lorentz_obstruction": f"{lorentz['obstruction']:.17g}",
        "transverse_obstruction": f"{transverse['obstruction']:.17g}",
        "max_derivative_convergence": f"{max(lorentz['convergence'], transverse['convergence']):.17g}",
        "max_projector_match_distance": f"{max_match:.17g}",
        "node_status": status,
    }


def candidate_worker(task: tuple[str, str]):
    identity_id, family_id = task
    identity = IDENTITY_BY_ID[identity_id]
    family = FAMILY_BY_ID[family_id]
    rows = []
    try:
        for node in range(FOLLOW_NODES):
            rows.append(candidate_node(identity, family, node / (FOLLOW_NODES - 1)))
    except Exception as exc:
        rows.append({
            "identity_id": identity_id,
            "family_id": family_id,
            "path_node": -1,
            "t": "nan",
            "motif": "UNRESOLVED",
            "numeric_status": "FAILED_RETAINED",
            "lorentz_class": "NOT_AVAILABLE",
            "transverse_class": "NOT_AVAILABLE",
            "lorentz_obstruction": "nan",
            "transverse_obstruction": "nan",
            "max_derivative_convergence": "nan",
            "max_projector_match_distance": "nan",
            "node_status": f"EXECUTION_FAILURE_RETAINED:{type(exc).__name__}:{exc}",
        })
    statuses = [row["node_status"] for row in rows]
    if len(rows) == FOLLOW_NODES and all(status == "BOTH_SIDES_SAMPLED_INTEGRABLE" for status in statuses):
        path_status = "SAMPLED_ALL_9_NODES_INTEGRABLE_CANDIDATE"
    elif any(status == "NONINTEGRABILITY_OBSERVED" for status in statuses):
        path_status = "DEVELOPS_SAMPLED_NONINTEGRABILITY"
    elif any("MOTIF_CHANGE" in status or "UNIQUE_SPLIT_LOST" in status or "SIGNATURE" in status for status in statuses):
        path_status = "DEVELOPS_SPLIT_OR_MOTIF_CHANGE"
    elif any("FAILURE" in status for status in statuses):
        path_status = "EXECUTION_FAILURE_RETAINED"
    else:
        path_status = "NUMERIC_UNCERTAIN_RETAINED"
    finite_obstructions = [
        float(row[key])
        for row in rows
        for key in ("lorentz_obstruction", "transverse_obstruction")
        if row[key] != "nan"
    ]
    finite_convergence = [float(row["max_derivative_convergence"]) for row in rows if row["max_derivative_convergence"] != "nan"]
    summary = {
        "identity_id": identity_id,
        "family_id": family_id,
        "nodes_expected": FOLLOW_NODES,
        "nodes_recorded": len(rows),
        "integrable_nodes": sum(status == "BOTH_SIDES_SAMPLED_INTEGRABLE" for status in statuses),
        "nonintegrable_nodes": sum(status == "NONINTEGRABILITY_OBSERVED" for status in statuses),
        "uncertain_or_changed_nodes": sum(status not in {"BOTH_SIDES_SAMPLED_INTEGRABLE", "NONINTEGRABILITY_OBSERVED"} for status in statuses),
        "max_obstruction": f"{max(finite_obstructions, default=math.nan):.17g}",
        "max_derivative_convergence": f"{max(finite_convergence, default=math.nan):.17g}",
        "path_status": path_status,
    }
    return rows, summary


def exact_transport_control() -> dict[str, object]:
    s, a, b = sp.symbols("s a b", real=True)
    eta = sp.diag(-1, 1, 1, 1)
    generator = sp.Matrix([
        [0, a, 0, 0],
        [a, 0, 0, 0],
        [0, 0, 0, -b],
        [0, 0, b, 0],
    ])
    transform = sp.Matrix([
        [sp.cosh(a * s), sp.sinh(a * s), 0, 0],
        [sp.sinh(a * s), sp.cosh(a * s), 0, 0],
        [0, 0, sp.cos(b * s), -sp.sin(b * s)],
        [0, 0, sp.sin(b * s), sp.cos(b * s)],
    ])
    elementary = []
    for index in range(4):
        value = sp.zeros(4)
        value[index, index] = 1
        elementary.append(value)
    projectors = [sp.simplify(transform * value * transform.inv()) for value in elementary]
    derivatives = [value.diff(s) for value in projectors]
    kato = sp.simplify(sum((derivatives[index] * projectors[index] for index in range(4)), sp.zeros(4)))
    commutator_residuals = [sp.simplify(kato * projectors[index] - projectors[index] * kato - derivatives[index]) for index in range(4)]
    isometry = sp.simplify(transform.T * eta * transform - eta)
    skew = sp.simplify(kato.T * eta + eta * kato)

    phi, A, Ap, omega, omegap = sp.symbols("phi A Ap Omega Omega_p", positive=True, finite=True)
    gamma_phi = sp.diag(0, Ap / A, omegap / omega - 1, omegap / omega + 1)
    coordinate_projectors = elementary
    toric_covariant = [sp.simplify(gamma_phi * value - value * gamma_phi) for value in coordinate_projectors]
    f = sp.simplify(sp.exp(-2 * phi) / (sp.exp(-2 * phi) + sp.exp(2 * phi)))
    result = {
        "schema": "udt-global-assembly-exact-controls-1.0",
        "lorentz_generator_metric_skew": skew == sp.zeros(4),
        "transport_intertwining_identities": all(value == sp.zeros(4) for value in commutator_residuals),
        "transport_solution_metric_isometry": isometry == sp.zeros(4),
        "kato_equals_generator_for_four_lines": sp.simplify(kato - generator) == sp.zeros(4),
        "toric_depth_projectors_covariantly_constant": all(value == sp.zeros(4) for value in toric_covariant),
        "toric_depth_kato_generator": "ZERO",
        "toric_connection_fraction": str(f),
        "toric_connection_common_scale_dependence": "NONE",
        "finite_endpoint_q": "f(phi_minus)-f(phi_plus)",
        "full_range_conditional_q": str(sp.limit(f, phi, -sp.oo) - sp.limit(f, phi, sp.oo)),
    }
    if not all(bool(value) for key, value in result.items() if isinstance(value, bool)):
        raise AssertionError(f"exact control failed {result}")
    return result


def completion_registry() -> list[dict[str, str]]:
    return [
        {"completion_id": "FC01_BOUNDARY_BOUNDARY", "base_completion": "FINITE_INTERVAL", "orbit_completion": "NO_CAP_TWO_PHYSICAL_BOUNDARIES", "regularity": "REGULAR_WITH_BOUNDARY_IF_BOUNDARY_DATA_SUPPLIED", "topology_family": "I_X_ORBIT", "infinite_family_rule": "arbitrary compatible boundary geometries", "selection_status": "REGISTERED_ALTERNATIVE"},
        {"completion_id": "FC02_ONE_CAP_BOUNDARY", "base_completion": "FINITE_INTERVAL", "orbit_completion": "ONE_PRIMITIVE_CAP_ONE_PHYSICAL_BOUNDARY", "regularity": "REGULAR_IF_PRIMITIVE_CAP_JETS_HOLD", "topology_family": "SOLID_TORUS_WITH_BOUNDARY", "infinite_family_rule": "all primitive meridians and compatible profiles", "selection_status": "REGISTERED_ALTERNATIVE"},
        {"completion_id": "FC03_TWO_CAP_P0", "base_completion": "FINITE_INTERVAL", "orbit_completion": "TWO_PRIMITIVE_SAME_DEPENDENT_CYCLES", "regularity": "REGULAR_CAPS", "topology_family": "S2_X_S1_STANDARD_OR_GENERAL_P0", "infinite_family_rule": "all primitive determinant-zero ordered pairs", "selection_status": "REGISTERED_ALTERNATIVE"},
        {"completion_id": "FC04_TWO_CAP_P1", "base_completion": "FINITE_INTERVAL", "orbit_completion": "TWO_PRIMITIVE_DETERMINANT_ONE_CYCLES", "regularity": "REGULAR_CAPS", "topology_family": "S3", "infinite_family_rule": "all ordered unimodular primitive pairs", "selection_status": "UNIQUE_ONLY_INSIDE_SUPPLIED_OPPOSITE_EIGENCIRCLE_PREMISES"},
        {"completion_id": "FC05_TWO_CAP_P_GT1", "base_completion": "FINITE_INTERVAL", "orbit_completion": "TWO_PRIMITIVE_GENERAL_CYCLES", "regularity": "REGULAR_CAPS", "topology_family": "LENS_L_P_Q", "infinite_family_rule": "all primitive pairs with determinant magnitude greater than one", "selection_status": "REGISTERED_ALTERNATIVE"},
        {"completion_id": "FC06_NONPRIMITIVE_CAP", "base_completion": "FINITE_INTERVAL", "orbit_completion": "ONE_OR_TWO_NONPRIMITIVE_COLLAPSES", "regularity": "ORBIFOLD_OR_SINGULAR", "topology_family": "SINGULAR_TORIC_COMPLETION", "infinite_family_rule": "all nonprimitive cap vectors", "selection_status": "RETAINED_MATHEMATICAL_BRANCH"},
        {"completion_id": "FC07_PERIODIC_TORUS_BUNDLE", "base_completion": "S1", "orbit_completion": "NO_CAP_GL2Z_MAPPING_TORUS", "regularity": "REGULAR_IF_ENDPOINT_JETS_MATCH_MONODROMY", "topology_family": "TORUS_BUNDLE_OVER_S1", "infinite_family_rule": "all GL(2,Z) monodromies", "selection_status": "REGISTERED_GLOBAL_ALTERNATIVE_NOT_CURRENT_PHYSICAL_CELL_WITHOUT_EXTRA_JOIN"},
        {"completion_id": "FC08_MIRROR_DOUBLE", "base_completion": "DOUBLED_INTERVAL", "orbit_completion": "MIRROR_SEAL_WITH_REGISTERED_ANGULAR_LIFT", "regularity": "DEPENDS_ON_FIXED_SET_AND_JETS", "topology_family": "DOUBLE_OR_REFLECTION_QUOTIENT", "infinite_family_rule": "reciprocal F_b and angular +I,-I,axis-reflection/exchange lifts", "selection_status": "MULTIPLE_REGISTERED_LIFTS"},
        {"completion_id": "FC09_NONORIENTABLE_GLUE", "base_completion": "S1_OR_QUOTIENT_INTERVAL", "orbit_completion": "ORIENTATION_REVERSING_BUNDLE_GLUE", "regularity": "REGULAR_BUNDLE_POSSIBLE", "topology_family": "NONORIENTABLE_ORIENTATION_TWISTED", "infinite_family_rule": "all determinant-minus-one monodromies and line sign holonomies", "selection_status": "REGISTERED_ALTERNATIVE_UNLESS_ORIENTATION_ADDED"},
        {"completion_id": "FC10_STRATIFIED_PROJECTOR", "base_completion": "FINITE_OR_PERIODIC", "orbit_completion": "PROJECTOR_RANK_MERGER_OR_SPLIT", "regularity": "METRIC_MAY_BE_REGULAR_PROJECTOR_FINE_SPLIT_FAILS", "topology_family": "STRATIFIED_DISTRIBUTION", "infinite_family_rule": "all retained motif transitions and degeneracies", "selection_status": "RETAINED_NOT_FILTERED"},
        {"completion_id": "FC11_NONINTEGRABLE_DISTRIBUTION", "base_completion": "FINITE_OR_PERIODIC", "orbit_completion": "ANHOLONOMIC_NO_ORBIT_SURFACE", "regularity": "REGULAR_DISTRIBUTION", "topology_family": "NONINTEGRABLE_PLANE_FIELD", "infinite_family_rule": "all nonzero Frobenius branches", "selection_status": "RETAINED_NOT_TORIC_ORBIT"},
        {"completion_id": "FC12_RECIPROCAL_TORIC_DIAGONAL", "base_completion": "FINITE_INTERVAL_OPEN_OR_CAP", "orbit_completion": "GLOBAL_FIXED_INTEGRAL_T2_BASIS_WITH_RECIPROCAL_WEIGHTS", "regularity": "PROFILE_AND_ENDPOINT_DEPENDENT", "topology_family": "BOUNDARY_P0_S3_LENS_OR_OTHER_PER_CAP_DATA", "infinite_family_rule": "arbitrary positive A,Omega plus every disclosed endpoint class", "selection_status": "CONDITIONAL_CONTROL_NOT_SELECTED"},
    ]


def canonical_primitive_vectors(bound: int = 3):
    values = []
    for a, b in itertools.product(range(-bound, bound + 1), repeat=2):
        if a == 0 and b == 0:
            continue
        if math.gcd(abs(a), abs(b)) != 1:
            continue
        if a < 0 or (a == 0 and b < 0):
            continue
        values.append((a, b))
    return sorted(values)


def extended_gcd(a: int, b: int):
    if b == 0:
        return (abs(a), 1 if a >= 0 else -1, 0)
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def cap_pair_witnesses() -> list[dict[str, object]]:
    vectors = canonical_primitive_vectors(3)
    rows = []
    for first, second in itertools.product(vectors, repeat=2):
        a, b = first
        c, d = second
        signed = a * d - b * c
        p = abs(signed)
        g, x, y = extended_gcd(a, b)
        if g != 1:
            raise AssertionError("primitive bezout")
        # u=(-y,x) gives det(v_minus,u)=1; alpha is the first coordinate of v_plus.
        alpha = x * c + y * d
        q = alpha % p if p > 1 else 0
        if p == 0:
            topology = "P0_DEPENDENT_CYCLES"
        elif p == 1:
            topology = "S3_DETERMINANT_ONE"
        else:
            topology = "LENS_L_P_Q_CONVENTION"
        rows.append({
            "v_minus": f"({a},{b})",
            "v_plus": f"({c},{d})",
            "signed_determinant": signed,
            "p_abs_determinant": p,
            "q_representative_convention": q if p > 1 else "-",
            "topology_class": topology,
            "cap_regularity": "BOTH_PRIMITIVE_BOUNDED_WITNESS",
            "coverage_status": "BOUNDED_ARITHMETIC_WITNESS_NOT_INFINITE_FAMILY_EXHAUSTION",
        })
    return rows


def abelian_coker(matrix: np.ndarray) -> str:
    value = np.asarray(matrix, dtype=int)
    rank = int(np.linalg.matrix_rank(value.astype(float)))
    if rank == 0:
        return "Z^2"
    gcd_entries = 0
    for item in value.flat:
        gcd_entries = math.gcd(gcd_entries, abs(int(item)))
    if rank == 1:
        torsion = f"+Z/{gcd_entries}" if gcd_entries > 1 else ""
        return f"Z{torsion}"
    determinant = abs(int(round(np.linalg.det(value))))
    d1 = max(1, gcd_entries)
    d2 = determinant // d1
    factors = []
    if d1 > 1:
        factors.append(f"Z/{d1}")
    if d2 > 1:
        factors.append(f"Z/{d2}")
    return "+".join(factors) if factors else "0"


def monodromy_registry() -> list[dict[str, object]]:
    witnesses = {
        "M_IDENTITY": [[1, 0], [0, 1]],
        "M_MINUS_IDENTITY": [[-1, 0], [0, -1]],
        "M_ORDER4_ROTATION": [[0, -1], [1, 0]],
        "M_ORDER6_ELLIPTIC": [[0, -1], [1, 1]],
        "M_PARABOLIC": [[1, 1], [0, 1]],
        "M_HYPERBOLIC": [[2, 1], [1, 1]],
        "M_EXCHANGE": [[0, 1], [1, 0]],
        "M_ORIENTATION_REVERSING_GLIDE": [[1, 1], [0, -1]],
    }
    rows = []
    for name, values in witnesses.items():
        matrix = np.asarray(values, dtype=int)
        det = int(round(np.linalg.det(matrix)))
        trace = int(np.trace(matrix))
        if det == -1:
            kind = "ORIENTATION_REVERSING"
        elif matrix.tolist() == [[1, 0], [0, 1]]:
            kind = "IDENTITY"
        elif abs(trace) < 2:
            kind = "FINITE_ELLIPTIC"
        elif abs(trace) == 2:
            kind = "PARABOLIC_OR_MINUS_PARABOLIC"
        else:
            kind = "HYPERBOLIC"
        coker = abelian_coker(matrix - np.eye(2, dtype=int))
        rows.append({
            "monodromy_id": name,
            "matrix": json.dumps(values, separators=(",", ":")),
            "determinant": det,
            "trace": trace,
            "monodromy_class": kind,
            "fiber_coker_M_minus_I": coker,
            "mapping_torus_H1": f"Z+({coker})",
            "coverage_status": "PARAMETRIC_GL2Z_FAMILY_WITH_CLASS_WITNESS",
        })
    return rows


def motif_completion_rows(motif_counts: Counter, completion_rows, follow_census: Counter):
    motifs = [
        "SCALAR_4_AMBIGUITY",
        "FULL_IRREDUCIBLE_4",
        "TWO_PLUS_TWO_LINES",
        "FOUR_LINES",
        "LINE_PLUS_THREE",
        "TRANSITION_OR_UNCERTAIN",
        "RECIPROCAL_TORIC_CONTROL",
    ]
    rows = []
    toric_ids = {"FC02_ONE_CAP_BOUNDARY", "FC03_TWO_CAP_P0", "FC04_TWO_CAP_P1", "FC05_TWO_CAP_P_GT1", "FC06_NONPRIMITIVE_CAP", "FC07_PERIODIC_TORUS_BUNDLE", "FC12_RECIPROCAL_TORIC_DIAGONAL"}
    for motif in motifs:
        for completion in completion_rows:
            completion_id = completion["completion_id"]
            if motif in {"SCALAR_4_AMBIGUITY", "FULL_IRREDUCIBLE_4"}:
                compatibility = "WHOLE_TANGENT_GEOMETRY_CAN_EXIST__NO_PROPER_PROJECTOR_BUNDLE"
                toric_gate = "NO_INTRINSIC_TWO_LINE_TORIC_DISTRIBUTION"
            elif motif == "LINE_PLUS_THREE":
                compatibility = "LINE_AND_COMPLEMENT_BUNDLE_POSSIBLE_WITH_GLOBAL_GLUE"
                toric_gate = "NO_INTRINSIC_TWO_TRANSVERSE_LINE_PAIR"
            elif motif == "FOUR_LINES":
                compatibility = "FOUR_LINE_BUNDLE_POSSIBLE_WITH_PERMUTATION_AND_SIGN_GLUE"
                toric_gate = "ALL_FROZEN_MIDPOINT_COMPLEMENTARY_RANK2_SIDES_NONINTEGRABLE"
            elif motif == "TWO_PLUS_TWO_LINES":
                compatibility = "L2_PLUS_TWO_LINE_BUNDLE_POSSIBLE_WHERE_SPLIT_PERSISTS"
                if completion_id in toric_ids:
                    toric_gate = "REQUIRES_ALL_NODE_INTEGRABLE_TWO_LINE_COMPLEMENT_PLUS_ORIENTATION_COMMUTATION_PERIODICITY_GLOBAL_GLUE"
                else:
                    toric_gate = "NO_TORIC_REQUIREMENT_FOR_RETAINED_BOUNDARY_OR_ANHOLONOMIC_COMPLETION"
            elif motif == "TRANSITION_OR_UNCERTAIN":
                compatibility = "STRATIFIED_ONLY_UNLESS_COARSE_PROJECTOR_SURVIVES"
                toric_gate = "FINE_BUNDLE_NOT_DEFINED_ACROSS_TRANSITION"
            else:
                compatibility = "EXACT_WITHIN_CONDITIONAL_RECIPROCAL_TORIC_CLASS"
                toric_gate = "GLOBAL_PERIODS_CAPS_ACTION_AND_ORIENTATION_STILL_REQUIRED"
            rows.append({
                "motif": motif,
                "frozen_stable_path_count": motif_counts.get(motif, 0) if motif != "TRANSITION_OR_UNCERTAIN" else 95_232 - sum(motif_counts.values()),
                "completion_id": completion_id,
                "local_to_global_compatibility": compatibility,
                "toric_orbit_gate": toric_gate,
                "sampled_all_node_integrable_candidates": follow_census.get("SAMPLED_ALL_9_NODES_INTEGRABLE_CANDIDATE", 0) if motif == "TWO_PLUS_TWO_LINES" else 0,
                "global_selection": "NOT_SELECTED_BY_LOCAL_MOTIF",
            })
    return rows


def holonomy_registry(completions, monodromies, exact):
    rows = []
    for completion in completions:
        cid = completion["completion_id"]
        projector = "OPEN_PATH_TRANSPORT_ONLY"
        levi = "PROFILE_DEPENDENT_NOT_COMPUTED_WITHOUT_COMPLETE_METRIC"
        lattice = "NONE_OR_OPEN"
        principal = "NOT_DEFINED_WITHOUT_FREE_ACTION"
        if cid == "FC01_BOUNDARY_BOUNDARY":
            lattice = "BOUNDARY_T2_BASIS_IF_SUPPLIED_NO_CLOSED_MONODROMY"
        elif cid == "FC02_ONE_CAP_BOUNDARY":
            lattice = "ONE_PRIMITIVE_MERIDIAN_CYCLE"
        elif cid in {"FC03_TWO_CAP_P0", "FC04_TWO_CAP_P1", "FC05_TWO_CAP_P_GT1"}:
            lattice = "CAP_PAIR_DETERMINANT_P_AND_Q_CONVENTION"
            projector = "INTERVAL_TRANSPORT_PLUS_CAP_EXTENSION_REQUIRED"
        elif cid == "FC06_NONPRIMITIVE_CAP":
            lattice = "NONPRIMITIVE_ISOTROPY_OR_SINGULAR_STABILIZER"
        elif cid == "FC07_PERIODIC_TORUS_BUNDLE":
            projector = "CLOSED_ONLY_AFTER_ENDPOINT_GL2Z_GLUE"
            lattice = "GENERAL_GL2Z_MONODROMY"
        elif cid == "FC08_MIRROR_DOUBLE":
            projector = "Z2_GRADED_RECIPROCAL_GLUE_WITH_EVEN_REVERSAL_PARITY_ON_CLOSED_COCYCLE"
            lattice = "ANGULAR_LIFT_DEPENDENT"
        elif cid == "FC09_NONORIENTABLE_GLUE":
            projector = "W1_NONZERO_SIGN_OR_PERMUTATION_HOLONOMY_ALLOWED"
            lattice = "DET_MINUS_ONE_GL2Z"
        elif cid == "FC10_STRATIFIED_PROJECTOR":
            projector = "FINE_HOLONOMY_UNDEFINED_COARSE_STRATIFIED_TRANSPORT_ONLY"
        elif cid == "FC11_NONINTEGRABLE_DISTRIBUTION":
            projector = "DISTRIBUTION_TRANSPORT_DEFINED_NO_LEAF_ORBIT_HOLONOMY"
        elif cid == "FC12_RECIPROCAL_TORIC_DIAGONAL":
            projector = "DEPTH_PATH_KATO_ZERO_IN_COORDINATE_PROJECTOR_FRAME"
            lattice = "SUPPLIED_INTEGRAL_T2_BASIS_AND_CAP_OR_GLUE_DATA"
            principal = "A=f dxi1+(1-f)dxi2; Q_FINITE=f_minus-f_plus; UNIT_ONLY_WITH_FULL_GLOBAL_PREMISES"
        rows.append({
            "completion_id": cid,
            "projector_kato_transport": projector,
            "levi_civita_tangent_holonomy": levi,
            "torus_lattice_or_cap_data": lattice,
            "principal_circle_characteristic_data": principal,
            "conflation_guard": "FOUR_NOTIONS_DISTINCT",
        })
    for row in monodromies:
        rows.append({
            "completion_id": f"FC07::{row['monodromy_id']}",
            "projector_kato_transport": "CLOSED_ONLY_AFTER_THIS_EXPLICIT_GLUE",
            "levi_civita_tangent_holonomy": "NOT_FIXED_BY_LATTICE_MONODROMY",
            "torus_lattice_or_cap_data": f"M={row['matrix']};H1={row['mapping_torus_H1']}",
            "principal_circle_characteristic_data": "NOT_AUTOMATICALLY_DEFINED",
            "conflation_guard": "FOUR_NOTIONS_DISTINCT",
        })
    return rows


def selector_matrix(completions):
    selectors = [
        ("RECIPROCITY", "reciprocal exponential comparison and Z2-graded transition algebra", "udt_global_coframe_cocycle_audit_2026-07-20/AUDIT_REPORT.md"),
        ("CSN", "positive common scale is calibration before material scale selection", "UDT_NATIVE_ACTION_DERIVATION_DISPATCH.md"),
        ("FINITE_CELL", "finite mirrored physical cell/no spatial infinity; boundary completion not specified", "angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md"),
        ("STATIC_SEAL", "static phi parity/value only; complete coframe lift and polarization open", "complete_coframe_seal_involution_2026-07-20/AUDIT_REPORT.md"),
        ("BOOTSTRAP", "on-shell admissibility without off-shell ranking functional", "boundary_bootstrap_representative_selector_audit_2026-07-19/AUDIT_REPORT.md"),
        ("SCALE_MATTER_INVENTORY", "no native dimensional matter object/action coefficient/source/boundary charge", "matter_bootstrap_dimensional_inventory_2026-07-20/AUDIT_REPORT.md"),
        ("DENSITY_BOOTSTRAP", "density may be a derived fixed-point output only after native mass and proper volume exist; it is not presently an independent selecting input", "matter_bootstrap_dimensional_inventory_2026-07-20/AUDIT_REPORT.md"),
    ]
    rows = []
    for selector_id, consequence, citation in selectors:
        for completion in completions:
            cid = completion["completion_id"]
            if selector_id == "FINITE_CELL" and cid == "FC07_PERIODIC_TORUS_BUNDLE":
                verdict = "NOT_CURRENT_PHYSICAL_CELL_WITHOUT_EXTRA_QUOTIENT_JOIN"
            elif selector_id == "FINITE_CELL" and cid == "FC06_NONPRIMITIVE_CAP":
                verdict = "DOES_NOT_LICENSE_SINGULAR_PHYSICAL_METRIC"
            elif selector_id == "STATIC_SEAL" and cid == "FC08_MIRROR_DOUBLE":
                verdict = "REQUIRES_A_SEAL_BUT_LEAVES_MULTIPLE_ANGULAR_LIFTS"
            elif selector_id == "RECIPROCITY" and cid == "FC08_MIRROR_DOUBLE":
                verdict = "CONSTRAINS_TRANSITION_PARITY_BUT_DOES_NOT_SELECT_LIFT_OR_COVER"
            elif selector_id == "RECIPROCITY" and cid == "FC12_RECIPROCAL_TORIC_DIAGONAL":
                verdict = "COMPATIBLE_RATIO_STRUCTURE_NOT_GLOBAL_SELECTION"
            elif selector_id == "CSN" and cid == "FC12_RECIPROCAL_TORIC_DIAGONAL":
                verdict = "REMOVES_COMMON_OMEGA_FROM_NORMALIZED_CONNECTION_NOT_PERIODS_CAPS_OR_ACTION"
            else:
                verdict = "NO_UNIQUE_BRANCH_DECISION"
            rows.append({
                "selector_id": selector_id,
                "completion_id": cid,
                "exact_registered_consequence": consequence,
                "branch_verdict": verdict,
                "source": citation,
                "selection_power": "NONSELECTING_IN_CURRENT_REGISTRY",
            })
    return rows


def build_path_census(summary_rows, candidate_keys):
    fields = (
        "identity_id", "family_id", "distinct_motifs", "stable_projector_path", "motif_transitions",
        "matched_edges", "unmatched_edges", "frozen_holonomy_status", "local_distribution_track",
        "continuous_transport_track", "global_completion_status",
    )
    writer = DeterministicGzipWriter(HERE / "PATH_ASSEMBLY_CENSUS.tsv.gz", fields)
    motif_counts = Counter()
    transitions = 0
    try:
        rows = []
        for record in summary_rows:
            motif = record["distinct_motifs"]
            stable = record["stable_projector_path"] == "YES"
            key = (record["identity_id"], record["family_id"])
            if stable:
                motif_counts[motif] += 1
            else:
                transitions += 1
            if stable and motif == "TWO_PLUS_TWO_LINES":
                local_track = "MIDPOINT_INTEGRABLE_CANDIDATE" if key in candidate_keys else "MIDPOINT_NONINTEGRABLE_TWO_PLANE_SPLIT"
            elif stable and motif == "FOUR_LINES":
                local_track = "ALL_MIDPOINT_COMPLEMENTARY_RANK2_SIDES_NONINTEGRABLE"
            elif stable and motif == "LINE_PLUS_THREE":
                local_track = "RANK3_HYPERSURFACE_TRACK"
            elif stable and motif in {"SCALAR_4_AMBIGUITY", "FULL_IRREDUCIBLE_4"}:
                local_track = "NO_PROPER_INTRINSIC_PROJECTOR_SPLIT"
            else:
                local_track = "TRANSITION_OR_NUMERIC_TRACK_RETAINED"
            rows.append({
                "identity_id": record["identity_id"],
                "family_id": record["family_id"],
                "distinct_motifs": motif,
                "stable_projector_path": record["stable_projector_path"],
                "motif_transitions": record["motif_transitions"],
                "matched_edges": record["matched_edges"],
                "unmatched_edges": record["unmatched_edges"],
                "frozen_holonomy_status": record["holonomy_status"],
                "local_distribution_track": local_track,
                "continuous_transport_track": "DENSE_ANCHOR_BY_POPULATED_STRATUM" if stable else "FINE_TRANSPORT_NOT_CLAIMED",
                "global_completion_status": "REQUIRES_EXPLICIT_GLOBAL_DATA",
            })
            if len(rows) >= 4096:
                writer.writerows(rows)
                rows = []
        if rows:
            writer.writerows(rows)
    finally:
        writer.close()
    return motif_counts, transitions


def density_bootstrap_ledger():
    return [
        {
            "route_id": "D01_OBSERVED_DENSITY_INPUT",
            "density_role": "externally supplied observational anchor",
            "mass_status": "not derived by this route",
            "volume_status": "may use a chosen observational volume",
            "circularity_status": "NONCIRCULAR_BUT_EXTERNAL",
            "selection_authority": "COMPARISON_OR_CALIBRATION_ONLY",
            "missing_object": "native mass and volume from the same UDT solution",
        },
        {
            "route_id": "D02_CONDITIONAL_CARRIER_READOUT",
            "density_role": "mass divided by volume after adopting a conditional carrier/action/readout",
            "mass_status": "CONDITIONAL",
            "volume_status": "completion-dependent",
            "circularity_status": "TYPE_CORRECT_ONLY_IF_ALL_PREMISES_TRAVEL",
            "selection_authority": "CONDITIONAL_BRANCH_DIAGNOSTIC_NOT_FOUNDATION_SELECTOR",
            "missing_object": "native carrier/action/source/boundary charge",
        },
        {
            "route_id": "D03_NATIVE_SIMULTANEOUS_FIXED_POINT",
            "density_role": "rho_solution=M_native[g,fields]/V_proper[g] solved with geometry boundary and bootstrap",
            "mass_status": "OPEN_NATIVE_OBJECT_REQUIRED",
            "volume_status": "GLOBAL_COMPLETION_DEPENDENT_BUT_GEOMETRICALLY_DEFINABLE",
            "circularity_status": "DESIRED_NONCIRCULAR_SIMULTANEOUS_CLOSURE",
            "selection_authority": "POTENTIAL_FUTURE_EIGENVALUE_OR_BRANCH_SELECTOR",
            "missing_object": "off-shell native mass functional plus varied global closure and response map",
        },
        {
            "route_id": "D04_DIMENSIONLESS_COMPACTNESS_LOOP",
            "density_role": "G rho Xmax^2/c^2 equivalent to G M/(c^2 Xmax) for rho=M/V with V proportional to Xmax^3",
            "mass_status": "symbolic unknown",
            "volume_status": "homogeneous finite-cell scaling",
            "circularity_status": "RANK_ONE_IF_NO_INDEPENDENT_DIMENSIONAL_DATUM",
            "selection_authority": "CAN_SELECT_AT_MOST_DIMENSIONLESS_BRANCH_OR_COMPACTNESS",
            "missing_object": "independent scale-breaking datum or process",
        },
        {
            "route_id": "D05_ASSEMBLY_ATLAS_CONTRIBUTION",
            "density_role": "provides alternative proper-volume and boundary geometries for a later simultaneous solve",
            "mass_status": "NOT_SUPPLIED_BY_GEOMETRY_ATLAS",
            "volume_status": "branch-dependent candidate object",
            "circularity_status": "NO_DENSITY_FED_BACK_IN_CURRENT_ATLAS",
            "selection_authority": "NONE_UNTIL_NATIVE_MASS_BOOTSTRAP_EXISTS",
            "missing_object": "join from completion-specific volume/boundary to native matter functional",
        },
    ]


def build(workers: int):
    verify_sources()
    summary_rows = list(iter_tsv(PRIOR_DIR / "PATH_CONTINUATION_SUMMARY.tsv.gz"))
    if len(summary_rows) != 95_232:
        raise AssertionError(f"path summaries {len(summary_rows)}")
    keys = [(row["identity_id"], row["family_id"]) for row in summary_rows]
    if len(set(keys)) != 95_232:
        raise AssertionError("duplicate frozen path identity")

    distribution_groups = defaultdict(list)
    for row in iter_tsv(PRIOR_DIR / "DISTRIBUTION_ATLAS.tsv.gz"):
        if row["motif"] == "TWO_PLUS_TWO_LINES" and row["distribution_kind"] == "COMPLEMENTARY_RANK2":
            distribution_groups[(row["identity_id"], row["family_id"])].append(row["frobenius_class"])
    candidate_keys = sorted(
        key for key, classes in distribution_groups.items()
        if len(classes) == 2 and all(value == "NUMERICALLY_INTEGRABLE_LOCAL" for value in classes)
    )
    if len(candidate_keys) != 1_536:
        raise AssertionError(f"candidate identity set {len(candidate_keys)}")

    motif_counts, transitions = build_path_census(summary_rows, set(candidate_keys))

    strata = defaultdict(list)
    for row in summary_rows:
        if row["stable_projector_path"] == "YES":
            strata[(row["distinct_motifs"], row["family_id"])].append((row["identity_id"], row["family_id"], row["distinct_motifs"]))
    anchor_tasks = []
    for stratum in sorted(strata):
        anchor_tasks.append(min(strata[stratum], key=lambda item: hashlib.sha256(f"{item[0]}\t{item[1]}".encode()).hexdigest()))
    if len(anchor_tasks) != 83:
        raise AssertionError(f"populated stable strata {len(anchor_tasks)}")

    context = mp.get_context("fork")
    with context.Pool(processes=workers) as pool:
        transport_rows = list(pool.imap(transport_worker, anchor_tasks, chunksize=1))
    transport_rows.sort(key=lambda row: (row["motif"], row["family_id"], row["identity_id"]))
    write_tsv(HERE / "DENSE_TRANSPORT_ATLAS.tsv", transport_rows)

    candidate_fields = (
        "identity_id", "family_id", "path_node", "t", "motif", "numeric_status", "lorentz_class",
        "transverse_class", "lorentz_obstruction", "transverse_obstruction", "max_derivative_convergence",
        "max_projector_match_distance", "node_status",
    )
    node_writer = DeterministicGzipWriter(HERE / "FINITE_CELL_DISTRIBUTION_FOLLOW.tsv.gz", candidate_fields)
    candidate_summaries = []
    try:
        with context.Pool(processes=workers) as pool:
            for node_rows, path_summary in pool.imap(candidate_worker, candidate_keys, chunksize=1):
                node_writer.writerows(node_rows)
                candidate_summaries.append(path_summary)
    finally:
        node_writer.close()
    candidate_summaries.sort(key=lambda row: (row["identity_id"], row["family_id"]))
    write_tsv(HERE / "FINITE_CELL_DISTRIBUTION_SUMMARY.tsv", candidate_summaries)
    follow_census = Counter(row["path_status"] for row in candidate_summaries)
    mask_registry = {row["mask_id"]: row for row in read_tsv(ROOT / "udt_structural_ensemble_metric_atlas_2026-07-21/ENSEMBLE_MASK_REGISTRY.tsv")}
    candidate_provenance = defaultdict(lambda: {"candidate_rows": 0, "identities": set()})
    for row in candidate_summaries:
        mask_id = row["identity_id"].rsplit("_", 1)[-1]
        key = (mask_id, row["family_id"])
        candidate_provenance[key]["candidate_rows"] += 1
        candidate_provenance[key]["identities"].add(row["identity_id"])
    provenance_rows = []
    for (mask_id, family_id), values in sorted(candidate_provenance.items()):
        provenance_rows.append({
            "structural_mask": mask_id,
            "selected_ensembles": mask_registry[mask_id]["selected_ensembles"],
            "instrument_family": family_id,
            "candidate_rows": values["candidate_rows"],
            "unique_analytic_identities": len(values["identities"]),
            "interpretation_guard": "ACTIVE_STRUCTURAL_ENSEMBLE_PROVENANCE_NOT_INDEPENDENT_PHYSICAL_BRANCH_COUNT",
        })
    write_tsv(HERE / "CANDIDATE_PROVENANCE_CENSUS.tsv", provenance_rows)

    exact = exact_transport_control()
    (HERE / "EXACT_TRANSPORT_CONTROL.json").write_text(json.dumps(exact, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    completions = completion_registry()
    write_tsv(HERE / "COMPLETION_CLASS_REGISTRY.tsv", completions)
    cap_rows = cap_pair_witnesses()
    write_tsv(HERE / "CAP_PAIR_WITNESSES.tsv", cap_rows)
    monodromies = monodromy_registry()
    write_tsv(HERE / "TORUS_MONODROMY_REGISTRY.tsv", monodromies)
    assembly_rows = motif_completion_rows(motif_counts, completions, follow_census)
    write_tsv(HERE / "MOTIF_COMPLETION_ATLAS.tsv", assembly_rows)
    holonomy_rows = holonomy_registry(completions, monodromies, exact)
    write_tsv(HERE / "BUNDLE_HOLONOMY_ATLAS.tsv", holonomy_rows)
    selector_rows = selector_matrix(completions)
    write_tsv(HERE / "SELECTOR_MATRIX.tsv", selector_rows)
    density_rows = density_bootstrap_ledger()
    write_tsv(HERE / "DENSITY_BOOTSTRAP_CIRCULARITY_LEDGER.tsv", density_rows)

    transport_census = Counter(row["transport_status"] for row in transport_rows)
    cap_census = Counter(row["topology_class"] for row in cap_rows)
    monodromy_census = Counter(row["monodromy_class"] for row in monodromies)
    selected = []
    stage_gates = [
        {"stage": "1_CONTINUOUS_TRANSPORT", "activation_requirement": "exact identity plus all populated-stratum dense anchors accounted", "status": "COMPLETE_WITH_NUMERIC_MARGINS_RETAINED", "downstream_authority": "PROJECTOR_TRANSPORT_ONLY_NOT_PHYSICAL_TIME"},
        {"stage": "2_FINITE_CELL_PATH_FOLLOW", "activation_requirement": "exact 1536 midpoint candidate set followed at nine nodes", "status": "COMPLETE_WITH_ALL_BRANCHES_RETAINED", "downstream_authority": "SAMPLED_LOCAL_DISTRIBUTION_ONLY"},
        {"stage": "3_COMPLETION_TAXONOMY", "activation_requirement": "all registered parametric completion families represented", "status": "COMPLETE_FOR_REGISTERED_TAXONOMY", "downstream_authority": "NO_ARBITRARY_FOUR_MANIFOLD_COMPLETENESS_CLAIM"},
        {"stage": "4_BUNDLE_HOLONOMY", "activation_requirement": "four distinct holonomy notions and explicit gluing gates", "status": "COMPLETE_FOR_REGISTERED_BRANCH_DATA", "downstream_authority": "NO_OPEN_PATH_HOLONOMY_PROMOTION"},
        {"stage": "5_UDT_SELECTOR", "activation_requirement": "exact registered premises leave one quotient class", "status": "NO_UNIQUE_QUOTIENT_SELECTED", "downstream_authority": "GLOBAL_QUOTIENT_SELECTION_OPEN"},
        {"stage": "6_DEFORMATION_DYNAMICS", "activation_requirement": "one quotient plus section/action/boundary selected natively", "status": "NOT_ACTIVATED__GLOBAL_QUOTIENT_NOT_SELECTED", "downstream_authority": "NO_CARRIER_OR_REDUCED_ACTION_DERIVATION"},
        {"stage": "7_TIME_LIVE", "activation_requirement": "native nonlinear evolution law constraints and boundary flux", "status": "NOT_ACTIVATED__NATIVE_DYNAMICS_UNDEFINED", "downstream_authority": "NO_CPU_TIME_EVOLUTION_AND_NO_GPU_WORK"},
    ]
    write_tsv(HERE / "STAGE_GATE_LEDGER.tsv", stage_gates)

    result = {
        "schema": SCHEMA,
        "frozen_path_identities": len(summary_rows),
        "unique_frozen_path_identities": len(set(keys)),
        "stable_path_count": sum(motif_counts.values()),
        "transition_or_unstable_path_count": transitions,
        "stable_motif_census": dict(sorted(motif_counts.items())),
        "populated_motif_family_strata": len(anchor_tasks),
        "dense_transport_anchor_count": len(transport_rows),
        "dense_transport_status_census": dict(sorted(transport_census.items())),
        "midpoint_integrable_candidate_identities": len(candidate_keys),
        "midpoint_integrable_unique_analytic_identities": len({identity_id for identity_id, _family_id in candidate_keys}),
        "midpoint_integrable_structural_mask_census": dict(sorted(Counter(identity_id.rsplit("_", 1)[-1] for identity_id, _family_id in candidate_keys).items())),
        "midpoint_integrable_instrument_family_census": dict(sorted(Counter(family_id for _identity_id, family_id in candidate_keys).items())),
        "finite_cell_follow_nodes_per_candidate": FOLLOW_NODES,
        "finite_cell_follow_status_census": dict(sorted(follow_census.items())),
        "completion_class_count": len(completions),
        "motif_completion_cross_rows": len(assembly_rows),
        "bounded_cap_pair_witness_count": len(cap_rows),
        "bounded_cap_pair_topology_census": dict(sorted(cap_census.items())),
        "monodromy_witness_count": len(monodromies),
        "monodromy_class_census": dict(sorted(monodromy_census.items())),
        "holonomy_registry_rows": len(holonomy_rows),
        "selector_matrix_rows": len(selector_rows),
        "density_bootstrap_routes": len(density_rows),
        "selected_global_quotient_classes": selected,
        "stage_6_status": "NOT_ACTIVATED__GLOBAL_QUOTIENT_NOT_SELECTED",
        "stage_7_status": "NOT_ACTIVATED__NATIVE_DYNAMICS_UNDEFINED",
        "cpu_time_live_runs": 0,
        "gpu_runs": 0,
        "maximum_conclusion": "BOUNDED_REGISTERED_GLOBAL_METRIC_ASSEMBLY_ATLAS_CHARACTERIZED__GLOBAL_QUOTIENT_SELECTION_OPEN",
    }
    (HERE / "ATLAS_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=min(12, os.cpu_count() or 1))
    args = parser.parse_args()
    build(max(1, args.workers))


if __name__ == "__main__":
    main()

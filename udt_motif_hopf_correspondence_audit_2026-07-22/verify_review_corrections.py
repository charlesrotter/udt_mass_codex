#!/usr/bin/env python3
"""Independent correction verifier for the fresh adversarial-review findings.

This verifier imports the frozen, nonproduction motif implementation and the already frozen
analytic-Jet reconstruction. It does not import the production correspondence builder or toric
derivation. It writes only the correction result and exercised mutation-catch ledger.
"""

from __future__ import annotations

import ast
import copy
import csv
import hashlib
import importlib.util
import itertools
import json
import math
import os
from collections import Counter
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import verify_correspondence_independent as reconstructed  # noqa: E402


COMPARE = reconstructed.COMPARE
COVARIANCE_TOLERANCE = 1.0e-8
SEED_TOLERANCE = 1.0e-12
MAXIMUM = (
    "OBSERVED_BOUNDED_REGISTERED-CHART_SAMPLED_MOTIF_AND_FROBENIUS_CENSUS"
    "+EXACT_CONDITIONAL_RECIPROCAL-TORIC/HOPF-SEED_COMPATIBILITY_WITNESS"
)
DIRECT_SOURCES = {
    "udt_amplitude_volume_metric_atlas_2026-07-21/SHA256SUMS.txt":
        "5182486f4a87080096532d9fe5ba999837ac79fac979c5694f216209ae41c112",
    "udt_joint_invariant_subspace_atlas_2026-07-21/SHA256SUMS.txt":
        "973dcc8bb297fad8358087318b24e5db9d1179e8b6a51a2535a0110e30c108c2",
}
HOPF_SEED_SHA256 = "7a9dcf021a23cd663bb484e435ee716084e38999f0629b294790aca77e15b748"
MAP_INTERPRETATION = "ZERO_CONSTANT_CUBIC_GLOBAL_POLYNOMIAL_FROM_REGISTERED_JETS"
SAMPLED_STATUS = "17_NODE_SAMPLED_MATCH_NOT_CONTINUOUS_BUNDLE_THEOREM"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def family_results(objects: dict[str, object], metric: np.ndarray) -> dict[int, dict[str, object]]:
    scalar = {key: objects[key] for key in ("R", "H", "D")}
    return {
        mask: reconstructed.independent.classify(
            reconstructed.independent.operators(objects, keys),
            objects["gradient"], metric, scalar, keys,
        )
        for _family_id, mask, keys in reconstructed.FAMILIES
    }


def labels(result: dict[str, object]) -> list[tuple[int, str]]:
    return [(int(item["rank"]), str(item["signature"])) for item in result["blocks"]]


def assignment(
    first: dict[str, object],
    second: dict[str, object],
    first_projectors: list[np.ndarray] | None = None,
    second_projectors: list[np.ndarray] | None = None,
) -> tuple[int, ...] | None:
    first_labels = labels(first)
    second_labels = labels(second)
    if Counter(first_labels) != Counter(second_labels):
        return None
    left = first_projectors or [np.asarray(item) for item in first["projectors"]]
    right = second_projectors or [np.asarray(item) for item in second["projectors"]]
    best: tuple[int, ...] | None = None
    best_distance = math.inf
    for permutation in itertools.permutations(range(len(right))):
        if any(first_labels[index] != second_labels[permutation[index]] for index in range(len(left))):
            continue
        distance = max(
            (reconstructed.independent.relmax(left[index], right[permutation[index]])
             for index in range(len(left))),
            default=0.0,
        )
        if distance < best_distance:
            best = tuple(permutation)
            best_distance = distance
    return best


def polynomial_map_value(
    jacobian: np.ndarray,
    jacobian_first: np.ndarray,
    jacobian_second: np.ndarray,
    point: np.ndarray,
) -> np.ndarray:
    return (
        jacobian @ point
        + 0.5 * np.einsum("mab,a,b->m", jacobian_first, point, point)
        + (1.0 / 6.0) * np.einsum("mabc,a,b,c->m", jacobian_second, point, point, point)
    )


def polynomial_map_local_jets(
    jacobian: np.ndarray,
    jacobian_first: np.ndarray,
    jacobian_second: np.ndarray,
    point: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    local_jacobian = (
        jacobian
        + np.einsum("mab,b->ma", jacobian_first, point)
        + 0.5 * np.einsum("mabc,b,c->ma", jacobian_second, point, point)
    )
    local_first = jacobian_first + np.einsum("mabc,c->mab", jacobian_second, point)
    return local_jacobian, local_first, jacobian_second


def invert_polynomial_map(
    jacobian: np.ndarray,
    jacobian_first: np.ndarray,
    jacobian_second: np.ndarray,
    target: np.ndarray,
) -> tuple[np.ndarray, float]:
    point = np.linalg.solve(jacobian, target)
    for _iteration in range(30):
        local_jacobian, _local_first, _local_second = polynomial_map_local_jets(
            jacobian, jacobian_first, jacobian_second, point
        )
        residual = polynomial_map_value(
            jacobian, jacobian_first, jacobian_second, point
        ) - target
        step = np.linalg.solve(local_jacobian, residual)
        point -= step
        if float(np.max(np.abs(step))) < 1.0e-14:
            break
    residual = float(np.max(np.abs(
        polynomial_map_value(jacobian, jacobian_first, jacobian_second, point) - target
    )))
    if residual > 1.0e-11:
        raise AssertionError(f"polynomial map inversion {residual}")
    return point, residual


def covariance_audit() -> dict[str, object]:
    lookup = reconstructed.identity_data()
    identities = sorted(
        lookup,
        key=lambda value: hashlib.sha256(
            ("MOTIF_HOPF_INDEPENDENT_V1|" + value).encode()
        ).hexdigest(),
    )[:64]
    transforms = reconstructed.independent.transforms()
    comparisons = 0
    nonuncertain_discordances = 0
    maximum_object_residual = 0.0
    maximum_projector_residual = 0.0
    maximum_inverse_map_residual = 0.0
    minimum_absolute_jacobian_determinant = math.inf
    point_status_census: Counter[str] = Counter()
    edge_comparisons = 0
    edge_discordances = 0
    edge_total = 0
    edge_skips: Counter[str] = Counter()

    for identity_id in identities:
        bank, amplitudes = lookup[identity_id]
        original_nodes: list[dict[int, dict[str, object]]] = []
        transformed_nodes: dict[str, list[dict[int, dict[str, object]]]] = {
            transform_id: [] for transform_id, *_rest in transforms
        }
        point_maps: dict[str, list[dict[int, tuple[int, ...] | None]]] = {
            transform_id: [] for transform_id, *_rest in transforms
        }

        for point in reconstructed.path_points(bank):
            g, dg, ddg, phi_first, phi_second = reconstructed.metric_phi_jets(
                bank, amplitudes, point
            )
            objects, _geometry = reconstructed.independent.objects(
                g, dg, ddg, phi_first, phi_second
            )
            originals = family_results(objects, g)
            original_nodes.append(originals)

            for transform_id, registered_jacobian, registered_first, registered_second in transforms:
                mapped_point, inverse_residual = invert_polynomial_map(
                    registered_jacobian, registered_first, registered_second, point
                )
                jacobian, jacobian_first, jacobian_second = polynomial_map_local_jets(
                    registered_jacobian, registered_first, registered_second, mapped_point
                )
                determinant = abs(float(np.linalg.det(jacobian)))
                minimum_absolute_jacobian_determinant = min(
                    minimum_absolute_jacobian_determinant, determinant
                )
                maximum_inverse_map_residual = max(
                    maximum_inverse_map_residual, inverse_residual
                )
                transformed = reconstructed.independent.transform_jets(
                    g, dg, ddg, 0.0, phi_first, phi_second,
                    jacobian, jacobian_first, jacobian_second,
                )
                transformed_objects, _transformed_geometry = reconstructed.independent.objects(
                    transformed[0], transformed[1], transformed[2],
                    transformed[4], transformed[5],
                )
                transformed_results = family_results(transformed_objects, transformed[0])
                transformed_nodes[transform_id].append(transformed_results)
                inverse = np.linalg.inv(jacobian)
                maximum_object_residual = max(
                    maximum_object_residual,
                    reconstructed.independent.relmax(transformed_objects["metric"], jacobian.T @ g @ jacobian),
                    reconstructed.independent.relmax(transformed_objects["gradient"], inverse @ objects["gradient"]),
                    reconstructed.independent.relmax(transformed_objects["R"], inverse @ objects["R"] @ jacobian),
                    reconstructed.independent.relmax(transformed_objects["H"], inverse @ objects["H"] @ jacobian),
                    reconstructed.independent.relmax(transformed_objects["D"], inverse @ objects["D"] @ jacobian),
                )
                current_maps: dict[int, tuple[int, ...] | None] = {}
                for _family_id, mask, _keys in reconstructed.FAMILIES:
                    original = originals[mask]
                    current = transformed_results[mask]
                    comparisons += 1
                    discordant = [field for field in COMPARE if original[field] != current[field]]
                    both_classified = (
                        original["numeric_status"] == "NUMERIC_CLASSIFIED"
                        and current["numeric_status"] == "NUMERIC_CLASSIFIED"
                    )
                    if both_classified:
                        point_status_census["BOTH_CLASSIFIED"] += 1
                    elif (
                        original["numeric_status"] == "NUMERIC_CLASSIFIED"
                    ) != (
                        current["numeric_status"] == "NUMERIC_CLASSIFIED"
                    ):
                        point_status_census["ONE_SIDED_UNCERTAIN"] += 1
                    else:
                        point_status_census["BOTH_UNCERTAIN"] += 1
                    if both_classified and discordant:
                        nonuncertain_discordances += 1
                    predicted = [inverse @ np.asarray(item) @ jacobian for item in original["projectors"]]
                    if both_classified and not discordant:
                        residual = reconstructed.independent.set_distance(
                            predicted,
                            [np.asarray(item) for item in current["projectors"]],
                        )
                        maximum_projector_residual = max(maximum_projector_residual, residual)
                    current_maps[mask] = assignment(original, current, predicted)
                point_maps[transform_id].append(current_maps)

        # Compare the actual minimum-distance edge assignment with the assignment predicted by
        # pointwise tensor covariance. This is the preregistered path-matching covariance gate.
        for transform_id, *_rest in transforms:
            current_nodes = transformed_nodes[transform_id]
            maps = point_maps[transform_id]
            for node in range(16):
                for _family_id, mask, _keys in reconstructed.FAMILIES:
                    left = original_nodes[node][mask]
                    right = original_nodes[node + 1][mask]
                    transformed_left = current_nodes[node][mask]
                    transformed_right = current_nodes[node + 1][mask]
                    original_edge = assignment(left, right)
                    transformed_edge = assignment(transformed_left, transformed_right)
                    left_map = maps[node][mask]
                    right_map = maps[node + 1][mask]
                    edge_total += 1
                    if None in (original_edge, transformed_edge, left_map, right_map):
                        reasons = []
                        if original_edge is None:
                            reasons.append("ORIGINAL_EDGE_UNMATCHED")
                        if transformed_edge is None:
                            reasons.append("TRANSFORMED_EDGE_UNMATCHED")
                        if left_map is None:
                            reasons.append("LEFT_POINT_COVARIANCE_MAP_UNMATCHED")
                        if right_map is None:
                            reasons.append("RIGHT_POINT_COVARIANCE_MAP_UNMATCHED")
                        edge_skips["+".join(reasons)] += 1
                        continue
                    predicted = [None] * len(left_map)
                    for original_left, transformed_left_index in enumerate(left_map):
                        original_right = original_edge[original_left]
                        predicted[transformed_left_index] = right_map[original_right]
                    edge_comparisons += 1
                    if tuple(predicted) != transformed_edge:
                        edge_discordances += 1

    return {
        "coordinate_map_interpretation": MAP_INTERPRETATION,
        "coordinate_map_evidence_status": "CONFIRMATORY_POST_SECOND_REVIEW_REPAIR",
        "blind_identities": len(identities),
        "stored_nonlinear_transforms": len(transforms),
        "all_family_node_comparisons": comparisons,
        "nonuncertain_classification_discordances": nonuncertain_discordances,
        "maximum_intrinsic_object_covariance_residual": maximum_object_residual,
        "maximum_projector_set_covariance_residual": maximum_projector_residual,
        "maximum_inverse_map_residual": maximum_inverse_map_residual,
        "minimum_absolute_jacobian_determinant": minimum_absolute_jacobian_determinant,
        "point_status_census": dict(sorted(point_status_census.items())),
        "uncertainty_bearing_point_comparisons": (
            point_status_census["ONE_SIDED_UNCERTAIN"]
            + point_status_census["BOTH_UNCERTAIN"]
        ),
        "possible_edge_transport_comparisons": edge_total,
        "matched_edge_transport_comparisons": edge_comparisons,
        "skipped_edge_transport_comparisons": sum(edge_skips.values()),
        "skipped_edge_reason_census": dict(sorted(edge_skips.items())),
        "matched_edge_transport_discordances": edge_discordances,
    }


def symbolic_toric_audit() -> dict[str, object]:
    time, phi, xi1, xi2 = sp.symbols("t phi xi1 xi2", real=True)
    coordinates = (time, phi, xi1, xi2)
    radial = sp.Function("A", positive=True)(phi)
    common = sp.Function("Omega", positive=True)(phi)
    metric = sp.diag(
        -1,
        radial**2,
        common**2 * sp.exp(-2 * phi),
        common**2 * sp.exp(2 * phi),
    )
    inverse = sp.simplify(metric.inv())
    gamma = [[[
        sp.simplify(sum(
            inverse[upper, lower] * (
                sp.diff(metric[lower, right], coordinates[left])
                + sp.diff(metric[lower, left], coordinates[right])
                - sp.diff(metric[left, right], coordinates[lower])
            )
            for lower in range(4)
        ) / 2)
        for right in range(4)] for left in range(4)] for upper in range(4)]
    hessian = sp.Matrix(
        4, 4,
        lambda upper, lower: sp.simplify(
            -sum(inverse[upper, index] * gamma[1][index][lower] for index in range(4))
        ),
    )
    dyad = sp.zeros(4)
    dyad[1, 1] = inverse[1, 1]
    expected_hessian = sp.diag(
        0,
        -sp.diff(radial, phi) / radial**3,
        (sp.diff(common, phi) / common - 1) / radial**2,
        (sp.diff(common, phi) / common + 1) / radial**2,
    )
    expected_dyad = sp.diag(0, radial**-2, 0, 0)
    hessian_residual = sp.simplify(hessian - expected_hessian)
    dyad_residual = sp.simplify(dyad - expected_dyad)
    angular_gap = sp.simplify(hessian[3, 3] - hessian[2, 2])

    diagonal_generator = sp.Matrix((0, 0, 1, 1))
    generator_flat = metric * diagonal_generator
    generator_norm = sp.simplify((diagonal_generator.T * metric * diagonal_generator)[0])
    connection = [sp.simplify(value / generator_norm) for value in generator_flat]
    weight = sp.simplify(connection[2])
    expected_weight = sp.simplify(1 / (1 + sp.exp(4 * phi)))
    connection_residual = sp.simplify((weight - expected_weight).rewrite(sp.exp))
    quotient = sp.Matrix((
        sp.sech(2 * phi) * sp.cos(xi1 - xi2),
        sp.sech(2 * phi) * sp.sin(xi1 - xi2),
        -sp.tanh(2 * phi),
    ))
    quotient_norm_residual = sp.simplify((quotient.dot(quotient) - 1).rewrite(sp.exp))
    unit_limit = sp.simplify(
        sp.limit(weight, phi, -sp.oo) - sp.limit(weight, phi, sp.oo)
    )
    if hessian_residual != sp.zeros(4) or dyad_residual != sp.zeros(4):
        raise AssertionError("symbolic metric derivation")
    if sp.simplify(angular_gap - 2 / radial**2) != 0:
        raise AssertionError("symbolic angular gap")
    if connection_residual != 0 or quotient_norm_residual != 0 or unit_limit != 1:
        raise AssertionError("symbolic connection/quotient")
    return {
        "christoffels_derived_from_metric": True,
        "mixed_hessian_derived_from_metric": True,
        "gradient_dyad_derived_from_metric": True,
        "angular_gap": str(angular_gap),
        "diagonal_connection_weight": str(weight),
        "connection_common_scale_cancelled": not weight.has(common),
        "quotient_norm_exact": quotient_norm_residual == 0,
        "conditional_full_range_unit_limit": str(unit_limit),
    }


def direct_hopf_seed_audit() -> dict[str, object]:
    source = ROOT / "hopfion_arc_scripts_2026-07-05/fs_hopfion.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    if not any(isinstance(node, ast.FunctionDef) and node.name == "hopf_seed" for node in tree.body):
        raise AssertionError("hopf_seed function absent")
    specification = importlib.util.spec_from_file_location("frozen_hopf_seed_module", source)
    if specification is None or specification.loader is None:
        raise AssertionError("hopf_seed import specification")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    import torch

    if module.dev != "cpu":
        raise AssertionError("CPU-only seed replay")
    generator = np.random.default_rng(20260722)
    phi = generator.uniform(-2.0, 2.0, 1000)
    xi1 = generator.uniform(-math.pi, math.pi, 1000)
    xi2 = generator.uniform(-math.pi, math.pi, 1000)
    eta = np.arctan(np.exp(2 * phi))
    s1 = np.cos(eta) * np.cos(xi1)
    s2 = np.cos(eta) * np.sin(xi1)
    s3 = np.sin(eta) * np.cos(xi2)
    s4 = np.sin(eta) * np.sin(xi2)
    scale = 1.7
    denominator = 1 + s4
    x = scale * s1 / denominator
    y = scale * s2 / denominator
    z = scale * s3 / denominator
    with torch.no_grad():
        actual = module.hopf_seed(
            torch.as_tensor(x, dtype=torch.float64),
            torch.as_tensor(y, dtype=torch.float64),
            torch.as_tensor(z, dtype=torch.float64),
            scale,
        ).cpu().numpy()
    delta = xi1 - xi2
    expected = np.asarray((
        np.cosh(2 * phi) ** -1 * np.cos(delta),
        np.cosh(2 * phi) ** -1 * np.sin(delta),
        -np.tanh(2 * phi),
    ))
    residual = float(np.max(np.abs(actual - expected)))
    return {
        "source_path": str(source.relative_to(ROOT)),
        "source_sha256": digest(source),
        "function_executed": "hopf_seed",
        "device": module.dev,
        "dtype": "float64",
        "sample_points": 1000,
        "sample_seed": 20260722,
        "maximum_absolute_residual": residual,
    }


def validate_source_lineage(rows: list[dict[str, str]]) -> None:
    if len(rows) != 10 or len({row["path"] for row in rows}) != 10:
        raise AssertionError("complete source lineage")
    indexed = {row["path"]: row["sha256"] for row in rows}
    for relative, expected in DIRECT_SOURCES.items():
        if indexed.get(relative) != expected:
            raise AssertionError(f"direct source lineage {relative}")
        if digest(ROOT / relative) != expected:
            raise AssertionError(f"direct source manifest identity {relative}")
        package = ROOT / Path(relative).parent
        for line in (package / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            wanted, name = line.split(maxsplit=1)
            if digest(package / name.strip()) != wanted:
                raise AssertionError(f"direct source manifest content {relative}:{name}")


def validate_result(result: dict[str, object], lineage: list[dict[str, str]]) -> None:
    covariance = result["covariance"]
    symbolic = result["symbolic_toric"]
    seed = result["direct_hopf_seed"]
    provenance = result["construction_provenance"]
    if covariance["blind_identities"] != 64 or covariance["stored_nonlinear_transforms"] != 2:
        raise AssertionError("covariance anchor coverage")
    if covariance["all_family_node_comparisons"] != 64 * 17 * 31 * 2:
        raise AssertionError("covariance family/node coverage")
    point_status = covariance["point_status_census"]
    if set(point_status) != {"BOTH_CLASSIFIED", "ONE_SIDED_UNCERTAIN", "BOTH_UNCERTAIN"}:
        raise AssertionError("point status classes")
    if sum(point_status.values()) != covariance["all_family_node_comparisons"]:
        raise AssertionError("point status completeness")
    if covariance["uncertainty_bearing_point_comparisons"] != (
        point_status["ONE_SIDED_UNCERTAIN"] + point_status["BOTH_UNCERTAIN"]
    ):
        raise AssertionError("uncertainty accounting")
    if covariance["nonuncertain_classification_discordances"] != 0:
        raise AssertionError("coordinate classification discordance")
    if covariance["coordinate_map_interpretation"] != MAP_INTERPRETATION:
        raise AssertionError("node-dependent nonlinear coordinate map")
    if covariance["coordinate_map_evidence_status"] != "CONFIRMATORY_POST_SECOND_REVIEW_REPAIR":
        raise AssertionError("coordinate map evidence provenance")
    if covariance["maximum_inverse_map_residual"] > 1.0e-11:
        raise AssertionError("coordinate map inverse residual")
    if covariance["minimum_absolute_jacobian_determinant"] <= 1.0e-6:
        raise AssertionError("coordinate map Jacobian degeneracy")
    if covariance["maximum_intrinsic_object_covariance_residual"] > COVARIANCE_TOLERANCE:
        raise AssertionError("intrinsic object covariance residual")
    if covariance["maximum_projector_set_covariance_residual"] > COVARIANCE_TOLERANCE:
        raise AssertionError("projector covariance residual")
    if covariance["possible_edge_transport_comparisons"] != 64 * 16 * 31 * 2:
        raise AssertionError("possible edge coverage")
    if covariance["matched_edge_transport_comparisons"] <= 0:
        raise AssertionError("missing matched edge coverage")
    if covariance["matched_edge_transport_comparisons"] + covariance["skipped_edge_transport_comparisons"] != covariance["possible_edge_transport_comparisons"]:
        raise AssertionError("edge comparison accounting")
    if sum(covariance["skipped_edge_reason_census"].values()) != covariance["skipped_edge_transport_comparisons"]:
        raise AssertionError("skipped edge reason accounting")
    if covariance["matched_edge_transport_discordances"] != 0:
        raise AssertionError("path matching covariance")
    if result["frobenius_certification_scope"] != "REGISTERED_CHART_ONLY":
        raise AssertionError("Frobenius scope promotion")
    required_symbolic = (
        "christoffels_derived_from_metric", "mixed_hessian_derived_from_metric",
        "gradient_dyad_derived_from_metric", "connection_common_scale_cancelled",
        "quotient_norm_exact",
    )
    if not all(symbolic[key] is True for key in required_symbolic):
        raise AssertionError("symbolic toric derivation")
    if symbolic["angular_gap"] != "2/A(phi)**2":
        raise AssertionError("symbolic angular gap")
    if symbolic["diagonal_connection_weight"] != "exp(-2*phi)/(2*cosh(2*phi))":
        raise AssertionError("symbolic connection weight")
    if symbolic["conditional_full_range_unit_limit"] != "1":
        raise AssertionError("symbolic unit limit")
    if seed["function_executed"] != "hopf_seed" or seed["device"] != "cpu":
        raise AssertionError("direct seed execution")
    if seed["source_sha256"] != HOPF_SEED_SHA256:
        raise AssertionError("direct seed source identity")
    if seed["dtype"] != "float64" or seed["sample_points"] != 1000 or seed["sample_seed"] != 20260722:
        raise AssertionError("direct seed sample contract")
    if seed["maximum_absolute_residual"] > SEED_TOLERANCE:
        raise AssertionError("direct seed residual")
    if provenance != {
        "supplied_equal_weight_circle_action": True,
        "imported_s2_matter_carrier": False,
        "imported_l2_l4_action_functional": False,
    }:
        raise AssertionError("construction provenance")
    if result["overall_correspondence_status"] != "LEAD":
        raise AssertionError("correspondence promotion")
    if result["sampled_path_status"] != SAMPLED_STATUS:
        raise AssertionError("sampled path promotion")
    if result["maximum_conclusion"] != MAXIMUM:
        raise AssertionError("maximum conclusion")
    validate_source_lineage(lineage)


def mutation_catches(
    result: dict[str, object], lineage: list[dict[str, str]]
) -> list[dict[str, str]]:
    mutations = []

    def add(name: str, mutate) -> None:
        candidate = copy.deepcopy(result)
        candidate_lineage = copy.deepcopy(lineage)
        mutate(candidate, candidate_lineage)
        try:
            validate_result(candidate, candidate_lineage)
        except AssertionError:
            mutations.append({"catch_id": name, "result": "MUTATION_REJECTED"})
            return
        raise AssertionError(f"mutation survived {name}")

    add("K01_MISSING_COVARIANCE_COMPARISON", lambda item, _rows: item["covariance"].__setitem__(
        "all_family_node_comparisons", item["covariance"]["all_family_node_comparisons"] - 1
    ))
    add("K02_DUPLICATE_COVARIANCE_COMPARISON", lambda item, _rows: item["covariance"].__setitem__(
        "all_family_node_comparisons", item["covariance"]["all_family_node_comparisons"] + 1
    ))
    add("K03_PROJECTOR_COVARIANCE_FAILURE", lambda item, _rows: item["covariance"].__setitem__(
        "maximum_projector_set_covariance_residual", 1.0e-3
    ))
    add("K04_CLASSIFICATION_DISCORDANCE", lambda item, _rows: item["covariance"].__setitem__(
        "nonuncertain_classification_discordances", 1
    ))
    add("K05_PATH_MATCHING_DISCORDANCE", lambda item, _rows: item["covariance"].__setitem__(
        "matched_edge_transport_discordances", 1
    ))
    add("K06_FROBENIUS_SCOPE_PROMOTION", lambda item, _rows: item.__setitem__(
        "frobenius_certification_scope", "CHART_INDEPENDENT"
    ))
    add("K07_CIRCULAR_TORIC_FORMULA", lambda item, _rows: item["symbolic_toric"].__setitem__(
        "christoffels_derived_from_metric", False
    ))
    add("K08_SEED_BEHAVIOR_MISMATCH", lambda item, _rows: item["direct_hopf_seed"].__setitem__(
        "maximum_absolute_residual", 1.0e-4
    ))
    add("K09_OMITTED_SUPPLIED_CIRCLE_ACTION", lambda item, _rows: item["construction_provenance"].__setitem__(
        "supplied_equal_weight_circle_action", False
    ))
    add("K10_IMPORTED_S2_CARRIER", lambda item, _rows: item["construction_provenance"].__setitem__(
        "imported_s2_matter_carrier", True
    ))
    add("K11_IMPORTED_L2_L4_ACTION", lambda item, _rows: item["construction_provenance"].__setitem__(
        "imported_l2_l4_action_functional", True
    ))
    add("K12_NATIVE_EMERGENCE_PROMOTION", lambda item, _rows: item.__setitem__(
        "overall_correspondence_status", "NATIVE_CARRIER_DERIVED"
    ))
    add("K13_MISSING_DIRECT_SOURCE_LINEAGE", lambda _item, rows: rows.__setitem__(
        slice(None), [row for row in rows if row["path"] not in DIRECT_SOURCES]
    ))
    add("K14_MISSING_EDGE_COMPARISONS", lambda item, _rows: item["covariance"].__setitem__(
        "matched_edge_transport_comparisons", 0
    ))
    add("K15_INTRINSIC_COVARIANCE_FAILURE", lambda item, _rows: item["covariance"].__setitem__(
        "maximum_intrinsic_object_covariance_residual", 1.0e9
    ))
    add("K16_CONTINUOUS_BUNDLE_PROMOTION", lambda item, _rows: item.__setitem__(
        "sampled_path_status", "CONTINUOUS_BUNDLE_THEOREM"
    ))
    add("K17_SYMBOLIC_ANGULAR_GAP_MUTATION", lambda item, _rows: item["symbolic_toric"].__setitem__(
        "angular_gap", "nonsense"
    ))
    add("K18_HOPF_SEED_SOURCE_MUTATION", lambda item, _rows: item["direct_hopf_seed"].__setitem__(
        "source_sha256", "0" * 64
    ))
    add("K19_HOPF_SEED_SAMPLE_COUNT_MUTATION", lambda item, _rows: item["direct_hopf_seed"].__setitem__(
        "sample_points", 1
    ))
    add("K20_UNCERTAINTY_ACCOUNTING_LOSS", lambda item, _rows: item["covariance"].__setitem__(
        "uncertainty_bearing_point_comparisons", 0
    ))
    add("K21_SKIPPED_EDGE_ACCOUNTING_LOSS", lambda item, _rows: item["covariance"].__setitem__(
        "skipped_edge_transport_comparisons", 0
    ))
    add("K22_FIXED_JACOBIAN_SUBSTITUTION", lambda item, _rows: item["covariance"].__setitem__(
        "coordinate_map_interpretation", "FIXED_JACOBIAN"
    ))
    add("K23_SYMBOLIC_CONNECTION_MUTATION", lambda item, _rows: item["symbolic_toric"].__setitem__(
        "diagonal_connection_weight", "nonsense"
    ))
    return mutations


def main() -> None:
    covariance = covariance_audit()
    symbolic = symbolic_toric_audit()
    seed = direct_hopf_seed_audit()
    result = {
        "schema": "udt-motif-hopf-review-correction-1.0",
        "status": "PASS_WITH_REGISTERED_SCOPE",
        "covariance": covariance,
        "frobenius_certification_scope": "REGISTERED_CHART_ONLY",
        "symbolic_toric": symbolic,
        "direct_hopf_seed": seed,
        "construction_provenance": {
            "supplied_equal_weight_circle_action": True,
            "imported_s2_matter_carrier": False,
            "imported_l2_l4_action_functional": False,
        },
        "sampled_path_status": SAMPLED_STATUS,
        "overall_correspondence_status": "LEAD",
        "maximum_conclusion": MAXIMUM,
    }
    lineage = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    validate_result(result, lineage)
    catches = mutation_catches(result, lineage)
    result["exercised_mutation_catches"] = len(catches)
    with (HERE / "REVIEW_CORRECTION_CATCH_PROOFS.tsv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(
            handle, fieldnames=("catch_id", "result"), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(catches)
    (HERE / "REVIEW_CORRECTION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

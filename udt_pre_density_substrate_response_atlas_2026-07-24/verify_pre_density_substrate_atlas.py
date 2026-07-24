#!/usr/bin/env python3
"""Independent verifier for the pre-density substrate-response atlas.

This implementation uses only the Python standard library, does not import
the production module, and recomputes the numeric load-bearing quantities.
"""

from __future__ import annotations

import cmath
import copy
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent


class VerificationError(RuntimeError):
    pass


def read_tsv(name: str) -> list[dict[str, str]]:
    with (OUT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with (OUT / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fieldnames})


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def identity(rows: list[dict[str, str]], key: str, expected: int, label: str) -> None:
    values = [row[key] for row in rows]
    if len(values) != expected:
        raise VerificationError(f"{label}: expected {expected}, found {len(values)}")
    if len(set(values)) != expected:
        raise VerificationError(f"{label}: duplicate identity")


def matrix_transpose_vector(
    matrix: tuple[tuple[int, int], tuple[int, int]],
    vector: tuple[int, int],
) -> tuple[int, int]:
    return (
        matrix[0][0] * vector[0] + matrix[1][0] * vector[1],
        matrix[0][1] * vector[0] + matrix[1][1] * vector[1],
    )


def determinant3(matrix: list[list[float]]) -> float:
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return (
        a * (e * i - f * h)
        - b * (d * i - f * g)
        + c * (d * h - e * g)
    )


def inverse3(matrix: list[list[float]]) -> list[list[float]]:
    det = determinant3(matrix)
    if abs(det) < 1e-14:
        raise VerificationError("singular independent metric witness")
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    cofactors = [
        [e * i - f * h, -(d * i - f * g), d * h - e * g],
        [-(b * i - c * h), a * i - c * g, -(a * h - b * g)],
        [b * f - c * e, -(a * f - c * d), a * e - b * d],
    ]
    return [[cofactors[col][row] / det for col in range(3)] for row in range(3)]


def five_point_derivative(function: Callable[[float], float], value: float) -> float:
    step = 1e-3
    return (
        function(value - 2 * step)
        - 8 * function(value - step)
        + 8 * function(value + step)
        - function(value + 2 * step)
    ) / (12 * step)


def finite_variation(function: Callable[[float], float]) -> float:
    step = 1e-3
    return (
        function(-2 * step)
        - 8 * function(-step)
        + 8 * function(step)
        - function(2 * step)
    ) / (12 * step)


def parse_directions(value: str) -> list[tuple[int, int]]:
    result = []
    for item in value.split(";"):
        first, second = item.strip("()").split(",")
        result.append((int(first), int(second)))
    return sorted(result)


def brute_shortest(
    matrix: tuple[tuple[float, float], tuple[float, float]]
) -> tuple[float, list[tuple[int, int]], float]:
    """Independent fixed-box enumeration with an exterior lower-bound proof."""

    bound = 12
    tolerance = 1e-11
    best = math.inf
    directions: list[tuple[int, int]] = []
    for first in range(-bound, bound + 1):
        for second in range(-bound, bound + 1):
            if first == 0 and second == 0:
                continue
            if math.gcd(abs(first), abs(second)) != 1:
                continue
            if first < 0 or (first == 0 and second < 0):
                continue
            value = (
                matrix[0][0] * first * first
                + 2 * matrix[0][1] * first * second
                + matrix[1][1] * second * second
            )
            if value < best - tolerance:
                best = value
                directions = [(first, second)]
            elif abs(value - best) <= tolerance:
                directions.append((first, second))
    trace = matrix[0][0] + matrix[1][1]
    discriminant = math.sqrt(
        (matrix[0][0] - matrix[1][1]) ** 2 + 4 * matrix[0][1] ** 2
    )
    lambda_min = (trace - discriminant) / 2
    outside_lower_bound = lambda_min * (bound + 1) ** 2
    if outside_lower_bound <= best:
        raise VerificationError("independent lattice search not certified")
    return best, sorted(set(directions)), outside_lower_bound


def inverse2(
    matrix: tuple[tuple[float, float], tuple[float, float]]
) -> tuple[tuple[float, float], tuple[float, float]]:
    determinant = (
        matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    )
    return (
        (matrix[1][1] / determinant, -matrix[0][1] / determinant),
        (-matrix[1][0] / determinant, matrix[0][0] / determinant),
    )


def transpose2(
    matrix: tuple[tuple[float, float], tuple[float, float]]
) -> tuple[tuple[float, float], tuple[float, float]]:
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


def multiply2(
    left: tuple[tuple[float, float], tuple[float, float]],
    right: tuple[tuple[float, float], tuple[float, float]],
) -> tuple[tuple[float, float], tuple[float, float]]:
    return tuple(
        tuple(
            sum(left[row][middle] * right[middle][column] for middle in range(2))
            for column in range(2)
        )
        for row in range(2)
    )


def load_state() -> dict[str, object]:
    names = {
        "axes": "SUBSTRATE_AXIS_REGISTRY.tsv",
        "groups": "TRANSFORMATION_GROUP_REGISTRY.tsv",
        "completion_registry": "COMPLETION_TEST_REGISTRY.tsv",
        "probes": "CONDITIONAL_PROBE_REGISTRY.tsv",
        "samples": "SAMPLE_GRID.tsv",
        "sources": "SOURCE_MANIFEST.tsv",
        "source_verification": "SOURCE_VERIFICATION.tsv",
        "local": "LOCAL_OBJECT_ATLAS.tsv",
        "laws": "TRANSFORMATION_LAW_ATLAS.tsv",
        "monodromy": "MONODROMY_GRID.tsv",
        "shape": "SHAPE_GRID.tsv",
        "selectors": "TORUS_LATTICE_SELECTOR_ATLAS.tsv",
        "selector_covariance": "DUAL_SELECTOR_COVARIANCE.tsv",
        "compatibility": "GROUP_COMPATIBILITY_ATLAS.tsv",
        "global": "GLOBAL_DESCENT_ATLAS.tsv",
        "coverage": "COMPLETION_COVERAGE.tsv",
        "response": "CONDITIONAL_RESPONSE_ATLAS.tsv",
    }
    state = {key: read_tsv(name) for key, name in names.items()}
    with (OUT / "RESULTS.json").open(encoding="utf-8") as handle:
        state["results"] = json.load(handle)
    return state


def verify_state(state: dict[str, object]) -> dict[str, object]:
    axes = state["axes"]
    groups = state["groups"]
    completion_registry = state["completion_registry"]
    probes = state["probes"]
    samples = state["samples"]
    sources = state["sources"]
    source_verification = state["source_verification"]
    local = state["local"]
    laws = state["laws"]
    monodromy = state["monodromy"]
    shape = state["shape"]
    selectors = state["selectors"]
    selector_covariance = state["selector_covariance"]
    compatibility = state["compatibility"]
    global_rows = state["global"]
    coverage = state["coverage"]
    response = state["response"]
    results = state["results"]

    identity(axes, "axis_id", 20, "axes")
    identity(groups, "group_id", 10, "groups")
    identity(completion_registry, "completion_id", 12, "completion_registry")
    identity(probes, "probe_id", 10, "probes")
    identity(samples, "sample_id", 12, "samples")
    identity(sources, "source_id", 20, "sources")
    identity(source_verification, "source_id", 20, "source_verification")
    identity(local, "object_id", 15, "local")
    identity(laws, "group_id", 10, "laws")
    identity(monodromy, "sample_id", 6, "monodromy")
    if len(shape) != 25:
        raise VerificationError("shape grid count")
    if len(selectors) != 25:
        raise VerificationError("selector grid count")
    identity(selector_covariance, "sample_id", 6, "selector_covariance")
    identity(compatibility, "test_id", 12, "compatibility")
    identity(global_rows, "completion_id", 12, "global")
    identity(coverage, "completion_id", 12, "coverage")
    identity(response, "probe_id", 10, "response")

    if any(row["axis"].lower() == "density" for row in axes):
        raise VerificationError("density relabeled as primary axis")
    primary_headers = set()
    for key in ("axes", "local", "laws", "global", "response"):
        primary_headers.update(state[key][0].keys())
    if "density" in {header.lower() for header in primary_headers}:
        raise VerificationError("density output field")

    source_by_id = {row["source_id"]: row for row in source_verification}
    for row in sources:
        actual = file_hash(ROOT / row["path"])
        if actual != row["sha256"]:
            raise VerificationError(f"source changed: {row['source_id']}")
        checked = source_by_id[row["source_id"]]
        if checked["actual_sha256"] != actual or checked["status"] != "PASS":
            raise VerificationError(f"source verification row: {row['source_id']}")

    shape_max = 0.0
    isotropic = 0
    for row in shape:
        phi = float(row["phi"])
        shear = float(row["shear"])
        h11 = math.exp(-2 * phi)
        h12 = shear * math.exp(-phi)
        h22 = shear * shear + math.exp(2 * phi)
        det = h11 * h22 - h12 * h12
        x = h11 - h22
        y = 2 * h12
        anisotropy = math.hypot(x, y)
        trace = h11 + h22
        disc = math.sqrt(max(trace * trace - 4 * det, 0.0))
        expected = {
            "determinant": det,
            "anisotropy_norm": anisotropy,
            "eigenvalue_min": (trace - disc) / 2,
            "eigenvalue_max": (trace + disc) / 2,
        }
        for key, value in expected.items():
            shape_max = max(shape_max, abs(float(row[key]) - value))
        if anisotropy < 1e-14:
            isotropic += 1
            if row["stratum"] != "ISOTROPIC" or row["eigenaxis_alpha_mod_pi"] != "UNDEFINED":
                raise VerificationError("isotropic row corrupted")
        else:
            alpha = 0.5 * math.atan2(y, x)
            shape_max = max(
                shape_max, abs(float(row["eigenaxis_alpha_mod_pi"]) - alpha)
            )
            if row["stratum"] != "ANISOTROPIC":
                raise VerificationError("anisotropic row corrupted")
    if shape_max >= 1e-11 or isotropic != 1:
        raise VerificationError("shape grid residual or isotropic count")

    selector_by_point = {(row["phi"], row["shear"]): row for row in selectors}
    if len(selector_by_point) != 25:
        raise VerificationError("duplicate selector grid point")
    selector_residual_max = 0.0
    selector_unique = 0
    selector_ties = 0
    for phi_value in (-1.0, -0.5, 0.0, 0.5, 1.0):
        for shear_value in (-1.0, -0.5, 0.0, 0.5, 1.0):
            key = (f"{phi_value:.1f}", f"{shear_value:.1f}")
            if key not in selector_by_point:
                raise VerificationError(f"missing selector point {key}")
            row = selector_by_point[key]
            h11 = math.exp(-2 * phi_value)
            h12 = shear_value * math.exp(-phi_value)
            h22 = shear_value * shear_value + math.exp(2 * phi_value)
            h = ((h11, h12), (h12, h22))
            hinv = inverse2(h)
            cycle_value, cycles, _ = brute_shortest(h)
            dual_value, duals, _ = brute_shortest(hinv)
            if parse_directions(row["shortest_cycles_mod_sign"]) != cycles:
                raise VerificationError(f"cycle selector {key}")
            if parse_directions(row["shortest_dual_characters_mod_sign"]) != duals:
                raise VerificationError(f"dual selector {key}")
            selector_residual_max = max(
                selector_residual_max,
                abs(float(row["cycle_norm_squared"]) - cycle_value),
                abs(float(row["dual_norm_squared"]) - dual_value),
            )
            unique = len(duals) == 1
            if int(row["cycle_multiplicity"]) != len(cycles):
                raise VerificationError(f"cycle multiplicity {key}")
            if int(row["dual_multiplicity"]) != len(duals):
                raise VerificationError(f"dual multiplicity {key}")
            if row["unique_dual_U1_reduction"] != ("YES" if unique else "NO_TIE"):
                raise VerificationError(f"dual uniqueness {key}")
            if row["classification"] != (
                "UNIQUE_METRIC_LATTICE_CHARACTER" if unique else "SYSTOLIC_TIE_WALL"
            ):
                raise VerificationError(f"selector classification {key}")
            selector_unique += int(unique)
            selector_ties += int(not unique)
    if selector_residual_max >= 1e-11:
        raise VerificationError("selector norm residual")
    if (selector_unique, selector_ties) != (22, 3):
        raise VerificationError("selector unique/tie counts")

    matrices_float = {
        "M01": ((1.0, 0.0), (0.0, 1.0)),
        "M02": ((0.0, 1.0), (1.0, 0.0)),
        "M03": ((1.0, 1.0), (0.0, 1.0)),
        "M04": ((0.0, -1.0), (1.0, 0.0)),
        "M05": ((-1.0, 0.0), (0.0, -1.0)),
        "M06": ((1.0, 0.0), (1.0, 1.0)),
    }
    base_phi, base_shear = 0.5, 0.5
    base_h = (
        (math.exp(-2 * base_phi), base_shear * math.exp(-base_phi)),
        (
            base_shear * math.exp(-base_phi),
            base_shear * base_shear + math.exp(2 * base_phi),
        ),
    )
    _, base_duals, _ = brute_shortest(inverse2(base_h))
    if len(base_duals) != 1:
        raise VerificationError("independent covariance base tie")
    covariance_by_id = {row["sample_id"]: row for row in selector_covariance}
    for sample_id, matrix in matrices_float.items():
        matrix_inverse = inverse2(matrix)
        transformed_h = multiply2(
            transpose2(matrix_inverse), multiply2(base_h, matrix_inverse)
        )
        _, observed, _ = brute_shortest(inverse2(transformed_h))
        base_dual = base_duals[0]
        predicted_float = (
            transpose2(matrix_inverse)[0][0] * base_dual[0]
            + transpose2(matrix_inverse)[0][1] * base_dual[1],
            transpose2(matrix_inverse)[1][0] * base_dual[0]
            + transpose2(matrix_inverse)[1][1] * base_dual[1],
        )
        predicted = (int(round(predicted_float[0])), int(round(predicted_float[1])))
        if predicted[0] < 0 or (predicted[0] == 0 and predicted[1] < 0):
            predicted = (-predicted[0], -predicted[1])
        if observed != [predicted]:
            raise VerificationError(f"independent selector covariance {sample_id}")
        row = covariance_by_id[sample_id]
        expected_text = f"({predicted[0]},{predicted[1]})"
        if (
            row["predicted_transformed_dual_mod_sign"] != expected_text
            or row["observed_transformed_dual_mod_sign"] != expected_text
            or row["status"] != "PASS"
        ):
            raise VerificationError(f"selector covariance row {sample_id}")

    matrices = {
        "M01": ((1, 0), (0, 1)),
        "M02": ((0, 1), (1, 0)),
        "M03": ((1, 1), (0, 1)),
        "M04": ((0, -1), (1, 0)),
        "M05": ((-1, 0), (0, -1)),
        "M06": ((1, 0), (1, 1)),
    }
    class_counts = {
        "PRESERVED": 0,
        "REVERSED_OR_CONJUGATED": 0,
        "MIXED_WITH_OTHER_CHARACTER": 0,
    }
    for row in monodromy:
        transformed = matrix_transpose_vector(matrices[row["sample_id"]], (1, -1))
        expected_vector = f"({transformed[0]},{transformed[1]})"
        if transformed == (1, -1):
            expected_class = "PRESERVED"
        elif transformed == (-1, 1):
            expected_class = "REVERSED_OR_CONJUGATED"
        else:
            expected_class = "MIXED_WITH_OTHER_CHARACTER"
        if (
            row["w_transformed"] != expected_vector
            or row["relative_character_status"] != expected_class
        ):
            raise VerificationError(f"monodromy row {row['sample_id']}")
        class_counts[expected_class] += 1
    if class_counts != {
        "PRESERVED": 1,
        "REVERSED_OR_CONJUGATED": 2,
        "MIXED_WITH_OTHER_CHARACTER": 3,
    }:
        raise VerificationError("monodromy class counts")

    compatibility_by_id = {row["test_id"]: row for row in compatibility}
    translation_change = abs(cmath.exp(1j * math.pi / 3) - 1)
    if translation_change <= 0.9:
        raise VerificationError("nontrivial translation witness")
    if (
        compatibility_by_id["GC01"]["result"]
        != "NO_EQUIVARIANT_IDENTIFICATION_WITHOUT_EXTRA_MAP"
        or compatibility_by_id["GC07"]["result"]
        != "FAILS_TORUS_TRANSLATION_EQUIVARIANCE"
        or compatibility_by_id["GC09"]["result"]
        != "JOINT_T2_METRIC_CONNECTION_OBJECT_DERIVED"
        or compatibility_by_id["GC10"]["result"]
        != "CANONICAL_INTEGRAL_U1_CHARACTER_SET_AVAILABLE"
        or compatibility_by_id["GC12"]["result"]
        != "BRANCHWISE_CANONICAL_METRIC_LATTICE_U1_REDUCTION_AVAILABLE__PHYSICAL_SELECTION_AND_PHASE_SECTION_OPEN"
    ):
        raise VerificationError("group compatibility ruling")

    registered_completions = [row["completion_id"] for row in completion_registry]
    if [row["completion_id"] for row in global_rows] != registered_completions:
        raise VerificationError("global completion order/coverage")
    if [row["completion_id"] for row in coverage] != registered_completions:
        raise VerificationError("completion coverage order")
    if any(
        row["registered"] != "YES"
        or row["classified_once"] != "YES"
        or row["preferred_or_filtered"] != "NO"
        for row in coverage
    ):
        raise VerificationError("completion preferred, missing, or repeated")
    if any("SECTION_DERIVED" in row["rank_one_selector"] for row in global_rows):
        raise VerificationError("phase section promoted")
    if next(
        row
        for row in global_rows
        if row["completion_id"] == "FC11_NONINTEGRABLE_DISTRIBUTION"
    )["joint_t2_object"] != "NO_GLOBAL_TORIC_BUNDLE":
        raise VerificationError("anholonomic torus bundle promotion")

    response_by_id = {row["probe_id"]: row for row in response}
    if "parallel_section_conditions_not_ordinary_section_existence" not in response_by_id["CP06"]["scope"]:
        raise VerificationError("parallel versus ordinary section conflated")
    if response_by_id["CP09"]["status"] != "CONDITIONAL_REFERENCE_ONLY":
        raise VerificationError("conditional carrier promoted")
    if response_by_id["CP10"]["status"] != "PASS":
        raise VerificationError("matter-solve guard")

    conformal_max = 0.0
    for aval in (-0.5, 0.0, 0.5):
        for xval in (-1.0, -0.5, 0.0, 0.5, 1.0):
            for yval in (-1.0, -0.5, 0.0, 0.5, 1.0):
                flux_x = lambda z: math.exp(aval * z) * (2 * z + yval)
                flux_y = lambda z: math.exp(aval * xval) * (xval + 4 * z)
                numeric = -(
                    five_point_derivative(flux_x, xval)
                    + five_point_derivative(flux_y, yval)
                )
                exact = -math.exp(aval * xval) * (
                    6 + aval * (2 * xval + yval)
                )
                conformal_max = max(conformal_max, abs(numeric - exact))
    if conformal_max >= 1e-11:
        raise VerificationError("independent conformal response residual")

    amat = [
        [1.1, -0.3, 0.2],
        [-0.3, 0.7, 0.4],
        [0.2, 0.4, 1.6],
    ]
    fmat = [
        [0.0, 0.8, -0.5],
        [-0.8, 0.0, 1.2],
        [0.5, -1.2, 0.0],
    ]
    kmats = [
        [[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 0.0]],
        [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
    ]

    def metric(epsilon: float, kmat: list[list[float]]) -> list[list[float]]:
        return [
            [
                (1.0 if row == col else 0.0) + epsilon * kmat[row][col]
                for col in range(3)
            ]
            for row in range(3)
        ]

    def l2_value(epsilon: float, kmat: list[list[float]]) -> float:
        h = metric(epsilon, kmat)
        hinv = inverse3(h)
        return math.sqrt(determinant3(h)) * sum(
            hinv[i][j] * amat[j][i] for i in range(3) for j in range(3)
        )

    def l4_value(epsilon: float, kmat: list[list[float]]) -> float:
        h = metric(epsilon, kmat)
        hinv = inverse3(h)
        total = 0.0
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for ell in range(3):
                        total += (
                            hinv[i][k]
                            * hinv[j][ell]
                            * fmat[i][j]
                            * fmat[k][ell]
                        )
        return math.sqrt(determinant3(h)) * total

    anisotropy_max = 0.0
    for kmat in kmats:
        l2_numeric = finite_variation(lambda eps: l2_value(eps, kmat))
        l2_expected = -sum(
            kmat[i][j] * amat[j][i] for i in range(3) for j in range(3)
        )
        cmat = [
            [
                sum(fmat[i][j] * fmat[k][j] for j in range(3))
                for k in range(3)
            ]
            for i in range(3)
        ]
        l4_numeric = finite_variation(lambda eps: l4_value(eps, kmat))
        l4_expected = -2 * sum(
            kmat[i][k] * cmat[k][i] for i in range(3) for k in range(3)
        )
        anisotropy_max = max(
            anisotropy_max,
            abs(l2_numeric - l2_expected),
            abs(l4_numeric - l4_expected),
        )
    if anisotropy_max >= 1e-9:
        raise VerificationError("independent anisotropy response residual")

    if (
        results["join_ruling"]
        != "BRANCHWISE_CANONICAL_METRIC_LATTICE_U1_REDUCTION_AVAILABLE__PHYSICAL_SELECTION_AND_PHASE_SECTION_OPEN"
    ):
        raise VerificationError("JSON join ruling")
    if results["density_to_geometry"] != "OPEN_NOT_SAMPLED":
        raise VerificationError("JSON pre-density scope")
    if results["matter_solve_launched"] or results["gpu_used"]:
        raise VerificationError("unauthorized solve or GPU")
    if results["monodromy_class_counts"] != class_counts:
        raise VerificationError("JSON monodromy counts")
    if (
        results["dual_selector_unique_count"] != selector_unique
        or results["dual_selector_tie_count"] != selector_ties
        or results["dual_selector_covariance_count"] != len(selector_covariance)
    ):
        raise VerificationError("JSON selector counts")
    if results["diagonal_dual_selector_exact"] != {
        "phi_negative": "(1,0)_mod_sign",
        "phi_zero": "(1,0)_and_(0,1)_tie",
        "phi_positive": "(0,1)_mod_sign",
        "reason": "H_inverse=diag(exp(2phi),exp(-2phi))",
    }:
        raise VerificationError("diagonal reciprocal selector ruling")

    return {
        "shape_residual_max": shape_max,
        "shape_isotropic_count": isotropic,
        "selector_residual_max": selector_residual_max,
        "selector_unique_count": selector_unique,
        "selector_tie_count": selector_ties,
        "selector_covariance_count": len(selector_covariance),
        "translation_non_equivariance_witness": translation_change,
        "monodromy_class_counts": class_counts,
        "conformal_five_point_residual_max": conformal_max,
        "anisotropy_five_point_residual_max": anisotropy_max,
        "source_count": len(sources),
        "completion_count": len(global_rows),
        "conditional_probe_count": len(response),
        "join_ruling": results["join_ruling"],
    }


def expect_failure(
    pristine: dict[str, object],
    catch_id: str,
    mutation: str,
    mutate: Callable[[dict[str, object]], None],
) -> dict[str, object]:
    candidate = copy.deepcopy(pristine)
    mutate(candidate)
    try:
        verify_state(candidate)
    except VerificationError as exc:
        return {
            "catch_id": catch_id,
            "mutation": mutation,
            "expected": "REJECT",
            "observed": "REJECT",
            "status": "PASS",
            "caught_reason": str(exc),
        }
    return {
        "catch_id": catch_id,
        "mutation": mutation,
        "expected": "REJECT",
        "observed": "ACCEPT",
        "status": "FAIL",
        "caught_reason": "mutation escaped verifier",
    }


def main() -> None:
    state = load_state()
    independent = verify_state(state)

    def set_field(
        collection: str, identity_key: str, identity_value: str, field: str, value: str
    ) -> Callable[[dict[str, object]], None]:
        def mutation(candidate: dict[str, object]) -> None:
            row = next(
                item
                for item in candidate[collection]
                if item[identity_key] == identity_value
            )
            row[field] = value

        return mutation

    catches = [
        expect_failure(
            state,
            "C01",
            "remove_registered_axis",
            lambda candidate: candidate["axes"].pop(),
        ),
        expect_failure(
            state,
            "C02",
            "duplicate_registered_axis",
            lambda candidate: candidate["axes"].append(copy.deepcopy(candidate["axes"][0])),
        ),
        expect_failure(
            state,
            "C03",
            "remove_completion",
            lambda candidate: candidate["global"].pop(),
        ),
        expect_failure(
            state,
            "C04",
            "assert_unregistered_group_join",
            set_field(
                "compatibility",
                "test_id",
                "GC12",
                "result",
                "COMMON_BUNDLE_DERIVED",
            ),
        ),
        expect_failure(
            state,
            "C05",
            "relabel_axis_as_density",
            set_field("axes", "axis_id", "A01", "axis", "density"),
        ),
        expect_failure(
            state,
            "C06",
            "conflate_parallel_and_ordinary_section",
            set_field("response", "probe_id", "CP06", "scope", "no_section_exists"),
        ),
        expect_failure(
            state,
            "C07",
            "promote_conditional_carrier",
            set_field("response", "probe_id", "CP09", "status", "DERIVED_NATIVE"),
        ),
        expect_failure(
            state,
            "C08",
            "prefer_completion_after_outcome",
            set_field(
                "coverage",
                "completion_id",
                "FC04_TWO_CAP_P1",
                "preferred_or_filtered",
                "YES",
            ),
        ),
        expect_failure(
            state,
            "C09",
            "corrupt_mixed_monodromy",
            set_field(
                "monodromy",
                "sample_id",
                "M03",
                "relative_character_status",
                "PRESERVED",
            ),
        ),
        expect_failure(
            state,
            "C10",
            "corrupt_source_hash",
            set_field(
                "sources",
                "source_id",
                "S20",
                "sha256",
                "0" * 64,
            ),
        ),
        expect_failure(
            state,
            "C11",
            "erase_isotropic_degeneracy",
            lambda candidate: next(
                row
                for row in candidate["shape"]
                if row["phi"] == "0.0" and row["shear"] == "0.0"
            ).__setitem__("stratum", "ANISOTROPIC"),
        ),
        expect_failure(
            state,
            "C12",
            "claim_matter_solve",
            lambda candidate: candidate["results"].__setitem__(
                "matter_solve_launched", True
            ),
        ),
        expect_failure(
            state,
            "C13",
            "corrupt_metric_lattice_character",
            lambda candidate: next(
                row
                for row in candidate["selectors"]
                if row["phi"] == "-0.5" and row["shear"] == "-1.0"
            ).__setitem__("shortest_dual_characters_mod_sign", "(0,1)"),
        ),
        expect_failure(
            state,
            "C14",
            "promote_systolic_tie_to_unique",
            lambda candidate: next(
                row
                for row in candidate["selectors"]
                if row["phi"] == "0.0" and row["shear"] == "0.0"
            ).__setitem__("unique_dual_U1_reduction", "YES"),
        ),
        expect_failure(
            state,
            "C15",
            "remove_selector_covariance_case",
            lambda candidate: candidate["selector_covariance"].pop(),
        ),
        expect_failure(
            state,
            "C16",
            "promote_character_connection_to_phase_section",
            set_field(
                "global",
                "completion_id",
                "FC04_TWO_CAP_P1",
                "rank_one_selector",
                "PHASE_SECTION_DERIVED",
            ),
        ),
    ]
    if any(row["status"] != "PASS" for row in catches):
        raise VerificationError("catch proof failure")

    write_tsv(
        "CATCH_PROOF_RESULTS.tsv",
        [
            "catch_id",
            "mutation",
            "expected",
            "observed",
            "status",
            "caught_reason",
        ],
        catches,
    )
    result = {
        "schema": "udt_pre_density_substrate_response_independent_v1",
        "implementation": "python_standard_library_no_production_import",
        "independent": independent,
        "catch_proof_count": len(catches),
        "catch_proof_pass_count": sum(row["status"] == "PASS" for row in catches),
        "overall": "PASS",
    }
    (OUT / "INDEPENDENT_RESULTS.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print("INDEPENDENT_PRE_DENSITY_ATLAS_VERIFICATION")
    print(f"sources={independent['source_count']}")
    print(f"completions={independent['completion_count']}")
    print(f"shape_residual_max={independent['shape_residual_max']:.17g}")
    print(
        "dual_selector="
        f"unique={independent['selector_unique_count']} "
        f"ties={independent['selector_tie_count']} "
        f"covariance={independent['selector_covariance_count']}"
    )
    print(f"selector_residual_max={independent['selector_residual_max']:.17g}")
    print(
        "conformal_five_point_residual_max="
        f"{independent['conformal_five_point_residual_max']:.17g}"
    )
    print(
        "anisotropy_five_point_residual_max="
        f"{independent['anisotropy_five_point_residual_max']:.17g}"
    )
    print(f"catch_proofs={len(catches)}/{len(catches)}")
    print(f"join={independent['join_ruling']}")
    print("INDEPENDENT_PASS")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent exact verifier for the native coframe-composition audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANIFEST = HERE / "SOURCE_MANIFEST.sha256"
ADJACENCY_BUILDER = (
    ROOT
    / "udt_configuration_space_adjacency_atlas_2026-07-22"
    / "build_configuration_adjacency_atlas.py"
)
ATLAS_BUILDER = (
    ROOT
    / "udt_bank_simplex_interior_atlas_2026-07-23"
    / "build_bank_simplex_atlas.py"
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source_records() -> list[tuple[str, str]]:
    output = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        expected, raw_path = line.split("  ", 1)
        output.append((expected, raw_path))
    return output


def validate_sources(records: list[tuple[str, str]]) -> None:
    if len(records) != 18:
        raise AssertionError("source-count mismatch")
    if len({path for _, path in records}) != len(records):
        raise AssertionError("duplicate source path")
    for expected, raw_path in records:
        path = ROOT / raw_path
        if not path.is_file() or digest(path) != expected:
            raise AssertionError(f"source mismatch: {raw_path}")


def load_module(path: Path, name: str):
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def independent_source_behavior() -> dict[str, object]:
    """Different-anchor cofield and full-matrix reconstruction."""

    source = load_module(ADJACENCY_BUILDER, "independent_behavior_source")
    atlas = load_module(ATLAS_BUILDER, "independent_behavior_atlas")
    amplitudes = np.asarray(
        [((-1.0) ** index) * (index + 2) / 37.0 for index in range(11)]
    )
    anchors = ((0.29, 0.55, 0.30, 0.20), (0.73, 0.25, 0.75, 0.58))
    max_feature_residual = 0.0
    max_scalar_residual = 0.0
    chart_checks = 0
    matrix_checks = 0

    for u, r, v, t in anchors:
        weights = np.asarray(
            [
                (1.0 - t) * (1.0 - r),
                (1.0 - t) * r * (1.0 - v),
                (1.0 - t) * r * v,
                t,
            ]
        )
        bank_coordinates = [
            source.float_bank_coordinate(bank, u) for bank in range(4)
        ]
        for chart in atlas.CHARTS:
            observed_features, observed_gradient = atlas.float_basis_simplex(
                chart,
                np.asarray([u]),
                np.asarray([r]),
                np.asarray([v]),
                np.asarray([t]),
            )
            if chart.startswith("J1"):
                coordinates = tuple(
                    sum(
                        weights[bank] * bank_coordinates[bank][axis]
                        for bank in range(4)
                    )
                    for axis in range(4)
                )
                coefficients = tuple(
                    tuple(
                        sum(
                            weights[bank]
                            * float(source.COEFFICIENTS[bank][field][term])
                            for bank in range(4)
                        )
                        for term in range(14)
                    )
                    for field in range(11)
                )
                expected_features = np.asarray(
                    [
                        source.float_field_value(coefficients[field], coordinates)
                        for field in range(10)
                    ]
                )
                expected_gradient = np.asarray(
                    source.float_field_gradient(coefficients[10], coordinates)
                )
            else:
                endpoint_features = []
                endpoint_gradients = []
                for bank in range(4):
                    endpoint_features.append(
                        [
                            source.float_field_value(
                                tuple(map(float, source.COEFFICIENTS[bank][field])),
                                bank_coordinates[bank],
                            )
                            for field in range(10)
                        ]
                    )
                    endpoint_gradients.append(
                        source.float_field_gradient(
                            tuple(map(float, source.COEFFICIENTS[bank][10])),
                            bank_coordinates[bank],
                        )
                    )
                expected_features = weights @ np.asarray(endpoint_features)
                expected_gradient = weights @ np.asarray(endpoint_gradients)
            feature_residual = max(
                float(np.max(np.abs(observed_features[0] - expected_features))),
                float(np.max(np.abs(observed_gradient[0] - expected_gradient))),
            )
            if feature_residual > 2.0e-15:
                raise AssertionError(f"independent feature residual {feature_residual}")
            max_feature_residual = max(max_feature_residual, feature_residual)
            chart_checks += 1

            latent = np.asarray(
                [
                    float(source.BASE_VALUES[field])
                    + amplitudes[field] * expected_features[field]
                    for field in range(10)
                ]
            )
            gradient = amplitudes[10] * expected_gradient
            a, b, c, d, e, f, a20, a30, a21, a31 = latent
            su, sw, sr, st = math.exp(a), math.exp(c), math.exp(d), math.exp(f)
            coframe = np.asarray(
                [
                    [su, b, 0.0, 0.0],
                    [0.0, sw, 0.0, 0.0],
                    [sr * a20 + e * a30, sr * a21 + e * a31, sr, e],
                    [st * a30, st * a31, 0.0, st],
                ]
            )
            metric = coframe.T @ np.diag([-1.0, 1.0, 1.0, 1.0]) @ coframe
            direct_scalar = float(gradient @ np.linalg.solve(metric, gradient))
            observed_scalar = float(
                atlas.float_scalar_simplex(
                    chart,
                    amplitudes,
                    np.asarray([u]),
                    np.asarray([r]),
                    np.asarray([v]),
                    np.asarray([t]),
                )[0]
            )
            scalar_residual = abs(direct_scalar - observed_scalar)
            if scalar_residual > 2.0e-14:
                raise AssertionError(f"independent scalar residual {scalar_residual}")
            max_scalar_residual = max(max_scalar_residual, scalar_residual)
            matrix_checks += 1

    return {
        "anchors": len(anchors),
        "chart_checks": chart_checks,
        "matrix_checks": matrix_checks,
        "fields_per_coframe": 10,
        "max_feature_residual": max_feature_residual,
        "max_scalar_residual": max_scalar_residual,
    }


def independent_algebra() -> dict[str, object]:
    eta = sp.diag(-1, 1, 1, 1)
    gauge = sp.diag(1, -1, -1, 1)
    gauge_metric = gauge.T * eta * gauge
    midpoint = (sp.eye(4) + gauge) / 2

    if gauge_metric != eta:
        raise AssertionError("gauge preservation failed")
    if (gauge.det(), gauge[0, 0], midpoint.det(), midpoint.rank()) != (1, 1, 0, 2):
        raise AssertionError("gauge midpoint tuple failed")

    # Independent Sylvester-signature route for the metric-average catch.
    g0 = sp.diag(-1, 1, 1, 1)
    g1 = sp.Matrix(
        [
            [-1, 2, 0, 0],
            [2, -3, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    eigen0 = sorted(float(value) for value in g0.eigenvals())
    eigen1 = sorted(float(value) for value in g1.eigenvals())
    if sum(value < 0 for value in eigen0) != 1:
        raise AssertionError("g0 signature failed")
    if sum(value < 0 for value in eigen1) != 1:
        raise AssertionError("g1 signature failed")
    if ((g0 + g1) / 2).rank() != 3:
        raise AssertionError("metric midpoint did not lose rank")
    relative = g0.inv() * g1
    relative_eigenvalues = relative.eigenvals()
    negative_eigenspace_dimension = len((relative + sp.eye(4)).nullspace())
    if relative_eigenvalues != {-1: 2, 1: 2}:
        raise AssertionError("relative spectrum failed")
    if negative_eigenspace_dimension != 1:
        raise AssertionError("negative Jordan-block count failed")

    x, y = sp.symbols("x y", real=True)
    k = sp.Matrix([[0, 1], [1, 0]])
    p = lambda z: sp.diag(sp.exp(-z), sp.exp(z))
    if sp.simplify(p(x) * p(y) - p(x + y)) != sp.zeros(2):
        raise AssertionError("one-parameter group failed")
    if sp.simplify(p(x).T * k * p(x) - k) != sp.zeros(2):
        raise AssertionError("pairing failed")

    def chart_frame(a_block, d_block, shift):
        return a_block.row_join(sp.zeros(2)).col_join(
            (d_block * shift).row_join(d_block)
        )

    group_anchors = 0
    anchor_data = (
        (
            sp.Matrix([[2, 1], [0, 3]]),
            sp.Matrix([[5, -1], [0, 7]]),
            sp.Matrix([[1, 2], [3, 4]]),
            sp.Matrix([[11, -2], [0, 13]]),
            sp.Matrix([[17, 3], [0, 19]]),
            sp.Matrix([[-1, 2], [0, 5]]),
        ),
        (
            sp.Matrix([[1, -3], [0, 2]]),
            sp.Matrix([[4, 5], [0, 6]]),
            sp.Matrix([[0, 1], [-2, 3]]),
            sp.Matrix([[3, 4], [0, 5]]),
            sp.Matrix([[7, -2], [0, 8]]),
            sp.Matrix([[6, 0], [1, -4]]),
        ),
    )
    for a1, d1, s1, a2, d2, s2 in anchor_data:
        e1 = chart_frame(a1, d1, s1)
        e2 = chart_frame(a2, d2, s2)
        product = chart_frame(
            a1 * a2,
            d1 * d2,
            d2.inv() * s1 * a2 + s2,
        )
        if e1 * e2 != product:
            raise AssertionError("independent chart-group product failed")
        inverse = chart_frame(
            a1.inv(),
            d1.inv(),
            -d1 * s1 * a1.inv(),
        )
        if e1 * inverse != sp.eye(4):
            raise AssertionError("independent chart-group inverse failed")
        if 23 * sp.eye(4) * e1 != e1 * (23 * sp.eye(4)):
            raise AssertionError("independent central-scale check failed")
        group_anchors += 1
    shear_frame = sp.eye(4)
    shear_frame[0, 1] = 1
    second_gauge = sp.diag(1, -1, -1, 1)
    direct_metric = shear_frame.T * eta * shear_frame
    gauged_second_metric = (
        (shear_frame * second_gauge).T
        * eta
        * (shear_frame * second_gauge)
    )
    group_gauge_residual = gauged_second_metric - direct_metric
    if group_gauge_residual == sp.zeros(4):
        raise AssertionError("chart-group gauge descent catch failed")

    w0, w1, w2, w3 = sp.symbols("w0 w1 w2 w3")
    base = w0 * w1 * w2
    volume = base * w3
    weights = (w0, w1, w2, w3)
    edge_checks = 0
    for first in range(4):
        for second in range(first + 1, 4):
            zeroed = {
                weight: 0
                for index, weight in enumerate(weights)
                if index not in (first, second)
            }
            if base.subs(zeroed) != 0 or volume.subs(zeroed) != 0:
                raise AssertionError("edge bubble failed")
            edge_checks += 1
    face_checks = 0
    for weight in weights:
        if volume.subs(weight, 0) != 0:
            raise AssertionError("face bubble failed")
        face_checks += 1

    # Recompute the causal flip by solving from the inverse frame rather than
    # importing the production norm.
    q = sp.symbols("q", positive=True)
    frame = sp.diag(1 / q, q, 1, 1)
    inverse_frame = frame.inv()
    inverse_metric = inverse_frame * eta * inverse_frame.T
    covector = sp.Matrix([1, 1, 0, 0])
    norm = sp.factor((covector.T * inverse_metric * covector)[0])
    if norm.subs(q, 2) != sp.Rational(-15, 4):
        raise AssertionError("positive reciprocal deformation sign failed")
    if norm.subs(q, sp.Rational(1, 2)) != sp.Rational(15, 4):
        raise AssertionError("negative reciprocal deformation sign failed")

    lam = sp.symbols("lambda")
    toy_difference = sp.factor(lam**2 - lam)
    if toy_difference.subs(lam, 0) != 0 or toy_difference.subs(lam, 1) != 0:
        raise AssertionError("toy endpoints failed")
    if toy_difference.subs(lam, sp.Rational(1, 2)) == 0:
        raise AssertionError("toy interior failed")

    return {
        "gauge_midpoint_rank": midpoint.rank(),
        "gauge_midpoint_determinant": str(midpoint.det()),
        "metric_midpoint_rank": ((g0 + g1) / 2).rank(),
        "metric_midpoint_determinant": str(((g0 + g1) / 2).det()),
        "relative_eigenvalue_multiplicities": {"-1": 2, "1": 2},
        "relative_negative_eigenspace_dimension": negative_eigenspace_dimension,
        "edge_checks": edge_checks,
        "face_checks": face_checks,
        "triangular_group_anchors": group_anchors,
        "triangular_group_gauge_residual": str(group_gauge_residual.tolist()),
        "reciprocal_norm": str(norm),
        "reciprocal_norm_q2": str(norm.subs(q, 2)),
        "reciprocal_norm_qhalf": str(norm.subs(q, sp.Rational(1, 2))),
        "toy_difference": str(toy_difference),
    }


def validate_package(
    result: dict[str, object],
    premises: list[dict[str, str]],
    candidates: list[dict[str, str]],
    requirements: list[dict[str, str]],
) -> None:
    if result["schema"] != "udt-native-coframe-composition-audit-v1":
        raise AssertionError("schema mismatch")
    if result["maximum_conclusion"] != (
        "CURRENT_UDT_PREMISES_SUPPLY_CONDITIONAL_RECIPROCAL_ONE_PARAMETER_"
        "COMPOSITION_BUT_NOT_A_WEIGHTED_MULTI_CONFIGURATION_MEAN_OR_NATIVE_"
        "COMPLETE_COFRAME_COMPOSITION"
    ):
        raise AssertionError("maximum conclusion mismatch")
    if len(premises) != 8 or len(candidates) != 10 or len(requirements) != 11:
        raise AssertionError("table row-count mismatch")
    if len({row["premise"] for row in premises}) != 8:
        raise AssertionError("premise identity mismatch")
    if len({row["candidate"] for row in candidates}) != 10:
        raise AssertionError("candidate identity mismatch")
    if len({row["requirement"] for row in requirements}) != 11:
        raise AssertionError("requirement identity mismatch")
    if any(row["multi_input_composition"] == "YES" for row in premises):
        raise AssertionError("unsupported complete premise map")

    by_premise = {row["premise"]: row for row in premises}
    if by_premise["positional_comparison_composition"]["ruling"] != "PARTIAL_NATIVE_LAW":
        raise AssertionError("reciprocal partial law lost")
    if by_premise["current_bootstrap"]["ruling"] != "FILTER_NOT_MAP":
        raise AssertionError("bootstrap type conflated")

    by_candidate = {row["candidate"]: row for row in candidates}
    if by_candidate["J1_GENERATOR_COEFFICIENT_BARYCENTRIC"]["status"] != (
        "CHOSE_ANALYTIC_CONFIGURATION_CHART"
    ):
        raise AssertionError("J1 was promoted")
    if by_candidate["J2_EVALUATED_COFIELD_BARYCENTRIC"]["status"] != (
        "CHOSE_LOCAL_COFIELD_CHART"
    ):
        raise AssertionError("J2 was promoted")
    if by_candidate["RECIPROCAL_LOGARITHMIC_MEAN"]["status"] != (
        "DERIVED_ALGEBRAIC_IDENTITY_GIVEN_CHOSEN_WEIGHTS_AND_ALIGNED_LOG_COORDINATE"
    ):
        raise AssertionError("reciprocal scope changed")
    triangular = by_candidate["COMPLETE_TRIANGULAR_COFRAME_GROUP"]
    if triangular["status"] != (
        "DERIVED_CHART_GROUP_CLOSURE; CHOSE_AS_PHYSICAL_COMPOSITION"
    ):
        raise AssertionError("triangular chart group scope changed")
    required_physical_composition_data = (
        "type-correct relative base/internal identification",
        "selected representative section or genuinely local-Lorentz-equivariant quotient operation",
        "selected weighted multi-input rule",
        "compatible phi/dphi rule",
    )
    if any(
        component not in triangular["extra_structure"]
        for component in required_physical_composition_data
    ):
        raise AssertionError(
            "triangular chart group lost a required physical-composition datum"
        )
    for candidate in (
        "RELATIVE_FRAME_LOG_OR_GEODESIC",
        "QUOTIENT_FRECHET_OR_KARCHER_BARYCENTER",
        "ACTION_OR_BOOTSTRAP_SELECTED_PATH",
    ):
        if not by_candidate[candidate]["extra_structure"]:
            raise AssertionError(f"extra structure omitted for {candidate}")

    rulings = result["rulings"]
    if rulings["J1"].startswith("DERIVED") or rulings["J2"].startswith("DERIVED"):
        raise AssertionError("chart promoted in result")
    if "NOT_COMPOSITION_INVARIANT" not in rulings["bank_simplex_pocket"]:
        raise AssertionError("pocket privileged")
    if rulings["reciprocal_depth_composition"] != (
        "DERIVED_CONDITIONAL_PAIRWISE_ONE_PARAMETER_RECIPROCAL_SUBGROUP"
    ):
        raise AssertionError("pairwise reciprocal scope changed")
    if "NOT_SELECTED_BY_CURRENT_UDT_PREMISES" not in rulings[
        "reciprocal_weighted_mean"
    ]:
        raise AssertionError("weighted reciprocal mean promoted")
    if result["counts"]["candidate_complete_native_laws"] != 0:
        raise AssertionError("complete native law count promoted")
    if result["counts"]["partial_native_reciprocal_laws"] != 1:
        raise AssertionError("partial native law count changed")

    algebra = result["algebra"]
    gauge = algebra["lorentz_gauge"]
    if gauge["matrix"] != (
        "[[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], "
        "[0, 0, 0, 1]]"
    ):
        raise AssertionError("saved Lorentz gauge changed")
    if gauge["affine_midpoint_determinant"] != "0":
        raise AssertionError("saved coframe midpoint determinant changed")
    if gauge["affine_midpoint_rank"] != 2:
        raise AssertionError("saved coframe midpoint rank changed")
    if algebra["metric_affine"]["midpoint_determinant"] != "0":
        raise AssertionError("saved metric midpoint determinant changed")
    relative = algebra["relative_metric_log_obstruction"]
    if relative["eigenvalue_multiplicities"] != {"-1": 2, "1": 2}:
        raise AssertionError("saved relative spectrum changed")
    if relative["negative_eigenspace_dimension"] != 1:
        raise AssertionError("saved relative Jordan structure changed")
    if relative["real_logarithm"] != "DOES_NOT_EXIST":
        raise AssertionError("saved relative-log obstruction changed")
    bubbles = algebra["bubbles"]
    if bubbles["base_edge_preserving"] != "w0*w1*w2":
        raise AssertionError("saved edge bubble changed")
    if bubbles["volume_face_preserving"] != "w0*w1*w2*w3":
        raise AssertionError("saved face bubble changed")
    if (bubbles["edge_checks"], bubbles["face_checks"]) != (6, 4):
        raise AssertionError("saved bubble coverage changed")
    if (bubbles["delta_plus_log2"], bubbles["delta_minus_log2"]) != (
        "-15/4",
        "15/4",
    ):
        raise AssertionError("saved reciprocal sign flip changed")
    if algebra["toy_chart_difference"]["difference"] != "lambda*(lambda - 1)":
        raise AssertionError("saved J1/J2 difference changed")
    chart_group = algebra["complete_triangular_chart_group"]
    if (
        chart_group["closure_residual"],
        chart_group["inverse_residual"],
        chart_group["common_scale"],
    ) != ("ZERO_4X4", "ZERO_4X4", "CENTRAL"):
        raise AssertionError("saved chart-group algebra changed")
    if chart_group["physical_scope"] != "CHOSEN_COORDINATE_INTERNAL_TRIVIALIZATION":
        raise AssertionError("saved chart-group physical scope changed")
    if chart_group["independent_gauge_descent"] != "FAILS_WITHOUT_SELECTED_SECTION":
        raise AssertionError("saved chart-group gauge scope changed")
    if chart_group["independent_second_input_gauge_metric_residual"] != (
        "[[0, 2, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]"
    ):
        raise AssertionError("saved chart-group gauge residual changed")
    if any("triangular_group" not in row for row in requirements):
        raise AssertionError("triangular requirement column missing")
    behavioral = result["source_behavioral_reconstruction"]
    if (
        behavioral["anchors"],
        behavioral["chart_checks"],
        behavioral["coframe_checks"],
        behavioral["fields_per_coframe"],
    ) != (3, 6, 6, 10):
        raise AssertionError("source behavioral coverage changed")
    if behavioral["chart_differences"] < 1:
        raise AssertionError("source behavioral chart distinction lost")
    if behavioral["max_scalar_residual"] > 2.0e-14:
        raise AssertionError("source behavioral scalar residual changed")
    if behavioral["transitive_source_sha256"] != (
        "121148082560c9ee17efeac7db942d00130e528db8d6a6155f8df85cefc92ec4"
    ):
        raise AssertionError("transitive behavioral source changed")


def expect_failure(name: str, callback) -> dict[str, str]:
    try:
        callback()
    except (AssertionError, KeyError, ValueError) as exc:
        return {
            "catch_id": name,
            "result": "PASS",
            "caught": type(exc).__name__,
            "scope": "RECORD_INTEGRITY_MUTATION",
        }
    raise AssertionError(f"mutation was not caught: {name}")


def catch_proofs(
    result: dict[str, object],
    premises: list[dict[str, str]],
    candidates: list[dict[str, str]],
    requirements: list[dict[str, str]],
) -> list[dict[str, str]]:
    catches = []

    def mutate_and_validate(mutator):
        r = copy.deepcopy(result)
        p = copy.deepcopy(premises)
        c = copy.deepcopy(candidates)
        q = copy.deepcopy(requirements)
        mutator(r, p, c, q)
        validate_package(r, p, c, q)

    catches.append(
        expect_failure(
            "M01_NON_LORENTZ_GAUGE",
            lambda: mutate_and_validate(
                lambda r, p, c, q: r["algebra"]["lorentz_gauge"].__setitem__(
                    "matrix",
                    "[[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], "
                    "[0, 0, 0, 2]]",
                )
            ),
        )
    )
    catches.append(
        expect_failure(
            "M02_NONSINGULAR_MIDPOINT_CLAIM",
            lambda: mutate_and_validate(
                lambda r, p, c, q: r["algebra"]["lorentz_gauge"].__setitem__(
                    "affine_midpoint_determinant", "1"
                )
            ),
        )
    )
    catches.append(
        expect_failure(
            "M03_BUBBLE_NOT_EDGE_ZERO",
            lambda: mutate_and_validate(
                lambda r, p, c, q: r["algebra"]["bubbles"].__setitem__(
                    "base_edge_preserving", "w0*w1"
                )
            ),
        )
    )
    catches.append(
        expect_failure(
            "M04_J1_PROMOTED",
            lambda: mutate_and_validate(
                lambda r, p, c, q: c.__setitem__(
                    next(i for i, row in enumerate(c) if row["candidate"].startswith("J1_")),
                    {
                        **next(row for row in c if row["candidate"].startswith("J1_")),
                        "status": "DERIVED",
                    },
                )
            ),
        )
    )
    catches.append(
        expect_failure(
            "M05_J2_PROMOTED",
            lambda: mutate_and_validate(
                lambda r, p, c, q: r["rulings"].__setitem__("J2", "DERIVED_NATIVE")
            ),
        )
    )
    catches.append(
        expect_failure(
            "M06_MISSING_EXTRA_STRUCTURE",
            lambda: mutate_and_validate(
                lambda r, p, c, q: next(
                    row for row in c if row["candidate"] == "RELATIVE_FRAME_LOG_OR_GEODESIC"
                ).__setitem__("extra_structure", "")
            ),
        )
    )
    catches.append(
        expect_failure(
            "M07_SOURCE_HASH_MUTATION",
            lambda: validate_sources(
                [("0" * 64, source_records()[0][1])] + source_records()[1:]
            ),
        )
    )
    catches.append(
        expect_failure(
            "M08_MAXIMUM_CONCLUSION_OVERCLAIM",
            lambda: mutate_and_validate(
                lambda r, p, c, q: r.__setitem__(
                    "maximum_conclusion", "NATIVE_COMPLETE_COFRAME_LAW_DERIVED"
                )
            ),
        )
    )
    catches.append(
        expect_failure(
            "M09_MISSING_CANDIDATE",
            lambda: mutate_and_validate(lambda r, p, c, q: c.pop()),
        )
    )
    catches.append(
        expect_failure(
            "M10_BOOTSTRAP_PROMOTED_TO_MAP",
            lambda: mutate_and_validate(
                lambda r, p, c, q: next(
                    row for row in p if row["premise"] == "current_bootstrap"
                ).__setitem__("ruling", "PARTIAL_NATIVE_LAW")
            ),
        )
    )
    catches.append(
        expect_failure(
            "M11_RECIPROCAL_SCOPE_PROMOTED",
            lambda: mutate_and_validate(
                lambda r, p, c, q: next(
                    row for row in c if row["candidate"] == "RECIPROCAL_LOGARITHMIC_MEAN"
                ).__setitem__("status", "DERIVED_COMPLETE_COFRAME")
            ),
        )
    )
    catches.append(
        expect_failure(
            "M12_DUPLICATE_REQUIREMENT",
            lambda: mutate_and_validate(lambda r, p, c, q: q.append(copy.deepcopy(q[0]))),
        )
    )
    catches.append(
        expect_failure(
            "M13_FALSE_GLOBAL_REAL_LOG",
            lambda: mutate_and_validate(
                lambda r, p, c, q: r["algebra"][
                    "relative_metric_log_obstruction"
                ].__setitem__("real_logarithm", "EXISTS_GLOBALLY")
            ),
        )
    )
    catches.append(
        expect_failure(
            "M14_TRIANGULAR_GROUP_PROMOTED_NATIVE",
            lambda: mutate_and_validate(
                lambda r, p, c, q: next(
                    row
                    for row in c
                    if row["candidate"] == "COMPLETE_TRIANGULAR_COFRAME_GROUP"
                ).__setitem__("status", "DERIVED_NATIVE_PHYSICAL_COMPOSITION")
            ),
        )
    )
    catches.append(
        expect_failure(
            "M15_TRIANGULAR_GROUP_FALSE_GAUGE_DESCENT",
            lambda: mutate_and_validate(
                lambda r, p, c, q: r["algebra"][
                    "complete_triangular_chart_group"
                ].__setitem__("independent_gauge_descent", "PASS")
            ),
        )
    )
    catches.append(
        expect_failure(
            "M16_BEHAVIORAL_SOURCE_RESULT_MUTATION",
            lambda: mutate_and_validate(
                lambda r, p, c, q: r["source_behavioral_reconstruction"].__setitem__(
                    "coframe_checks", 0
                )
            ),
        )
    )
    return catches


def main() -> None:
    records = source_records()
    validate_sources(records)
    result = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    premises = read_tsv("PREMISE_TYPE_LEDGER.tsv")
    candidates = read_tsv("CANDIDATE_OPERATION_CENSUS.tsv")
    requirements = read_tsv("J1_J2_REQUIREMENT_MATRIX.tsv")
    validate_package(result, premises, candidates, requirements)
    algebra = independent_algebra()
    source_behavior = independent_source_behavior()
    catches = catch_proofs(result, premises, candidates, requirements)
    if any(row["result"] != "PASS" for row in catches):
        raise AssertionError("catch proof failure")

    with (HERE / "CATCH_PROOFS.tsv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("catch_id", "result", "caught", "scope"),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(catches)

    output = {
        "schema": "udt-native-coframe-composition-independent-v1",
        "status": "PASS",
        "sources_checked": len(records),
        "premise_rows": len(premises),
        "candidate_rows": len(candidates),
        "requirement_rows": len(requirements),
        "catch_proofs": {"passed": len(catches), "total": len(catches)},
        "catch_proof_scope": (
            "RECORD_INTEGRITY_MUTATIONS; LOAD_BEARING_ALGEBRA_AND_SOURCE_"
            "BEHAVIOR_RECOMPUTED_SEPARATELY"
        ),
        "independent_algebra": algebra,
        "independent_source_behavior": source_behavior,
        "result_sha256": digest(HERE / "RESULT.json"),
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

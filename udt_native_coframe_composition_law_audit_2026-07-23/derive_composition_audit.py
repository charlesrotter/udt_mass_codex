#!/usr/bin/env python3
"""Exact algebra for the preregistered native coframe-composition audit."""

from __future__ import annotations

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
ATLAS_BUILDER = (
    ROOT
    / "udt_bank_simplex_interior_atlas_2026-07-23"
    / "build_bank_simplex_atlas.py"
)
ADJACENCY_BUILDER = (
    ROOT
    / "udt_configuration_space_adjacency_atlas_2026-07-22"
    / "build_configuration_adjacency_atlas.py"
)
SOURCE_MANIFEST = HERE / "SOURCE_MANIFEST.sha256"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def verify_sources() -> int:
    checked = 0
    for line in SOURCE_MANIFEST.read_text(encoding="utf-8").splitlines():
        expected, raw_path = line.split("  ", 1)
        path = ROOT / raw_path
        if not path.is_file() or digest(path) != expected:
            raise AssertionError(f"source mismatch: {raw_path}")
        checked += 1
    return checked


def write_tsv(name: str, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise AssertionError(f"no rows for {name}")
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def load_module(path: Path, name: str):
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def source_behavioral_reconstruction() -> dict[str, object]:
    """Reconstruct J1/J2 behavior from the transitive source, not tokens."""

    source = load_module(ADJACENCY_BUILDER, "composition_behavior_source")
    atlas = load_module(ATLAS_BUILDER, "composition_behavior_atlas")

    amplitudes = tuple(
        (1.0 if index % 2 == 0 else -1.0) * (index + 1) / 40.0
        for index in range(11)
    )
    anchors = (
        (0.17, 0.35, 0.20, 0.25),
        (0.53, 0.70, 0.60, 0.40),
        (0.89, 0.45, 0.80, 0.65),
    )

    def direct_fields(chart: str, u: float, r: float, v: float, t: float):
        weights = (
            (1.0 - t) * (1.0 - r),
            (1.0 - t) * r * (1.0 - v),
            (1.0 - t) * r * v,
            t,
        )
        bank_coordinates = [
            source.float_bank_coordinate(bank, u) for bank in range(4)
        ]
        if chart.startswith("J1"):
            coordinates = tuple(
                sum(weights[bank] * bank_coordinates[bank][axis] for bank in range(4))
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
            latent = tuple(
                float(source.BASE_VALUES[field])
                + amplitudes[field]
                * source.float_field_value(coefficients[field], coordinates)
                for field in range(10)
            )
            gradient = tuple(
                amplitudes[10] * item
                for item in source.float_field_gradient(
                    coefficients[10], coordinates
                )
            )
        else:
            endpoints = [
                source.float_endpoint(bank, amplitudes, u) for bank in range(4)
            ]
            latent = tuple(
                sum(weights[bank] * endpoints[bank][0][field] for bank in range(4))
                for field in range(10)
            )
            gradient = tuple(
                sum(weights[bank] * endpoints[bank][1][axis] for bank in range(4))
                for axis in range(4)
            )
        return latent, gradient

    def direct_scalar(latent, gradient):
        a, b, c, d, e, f, a20, a30, a21, a31 = latent
        first = gradient[0] - a20 * gradient[2] - a30 * gradient[3]
        second = gradient[1] - a21 * gradient[2] - a31 * gradient[3]
        return (
            -(first / math.exp(a)) ** 2
            + ((second - b * first / math.exp(a)) / math.exp(c)) ** 2
            + (gradient[2] / math.exp(d)) ** 2
            + ((gradient[3] - e * gradient[2] / math.exp(d)) / math.exp(f))
            ** 2
        )

    chart_checks = 0
    chart_differences = 0
    max_residual = 0.0
    coframe_checks = 0
    for u, r, v, t in anchors:
        chart_values = {}
        for chart in atlas.CHARTS:
            latent, gradient = direct_fields(chart, u, r, v, t)
            direct = direct_scalar(latent, gradient)
            observed = float(
                atlas.float_scalar_simplex(
                    chart,
                    amplitudes,
                    np.asarray([u]),
                    np.asarray([r]),
                    np.asarray([v]),
                    np.asarray([t]),
                )[0]
            )
            residual = abs(direct - observed)
            if residual > 2.0e-14:
                raise AssertionError(f"{chart} behavioral residual {residual}")
            max_residual = max(max_residual, residual)
            chart_checks += 1
            chart_values[chart] = observed

            a, b, c, d, e, f, a20, a30, a21, a31 = latent
            scale_u, scale_w = math.exp(a), math.exp(c)
            scale_r, scale_t = math.exp(d), math.exp(f)
            direct_coframe = np.asarray(
                [
                    [scale_u, b, 0.0, 0.0],
                    [0.0, scale_w, 0.0, 0.0],
                    [
                        scale_r * a20 + e * a30,
                        scale_r * a21 + e * a31,
                        scale_r,
                        e,
                    ],
                    [scale_t * a30, scale_t * a31, 0.0, scale_t],
                ]
            )
            abase = np.asarray([[scale_u, b], [0.0, scale_w]])
            dscreen = np.asarray([[scale_r, e], [0.0, scale_t]])
            shift = np.asarray([[a20, a21], [a30, a31]])
            block_coframe = np.block(
                [
                    [abase, np.zeros((2, 2))],
                    [dscreen @ shift, dscreen],
                ]
            )
            if not np.array_equal(direct_coframe, block_coframe):
                raise AssertionError("ten-field coframe block reconstruction failed")
            eta = np.diag([-1.0, 1.0, 1.0, 1.0])
            metric = direct_coframe.T @ eta @ direct_coframe
            expected_det = -math.exp(2.0 * (a + c + d + f))
            if abs(np.linalg.det(metric) - expected_det) > 2.0e-12:
                raise AssertionError("ten-field coframe determinant failed")
            coframe_checks += 1
        if abs(chart_values[atlas.CHARTS[0]] - chart_values[atlas.CHARTS[1]]) > 1e-12:
            chart_differences += 1
    if chart_differences == 0:
        raise AssertionError("behavioral J1/J2 anchors did not distinguish charts")

    return {
        "anchors": len(anchors),
        "chart_checks": chart_checks,
        "chart_differences": chart_differences,
        "coframe_checks": coframe_checks,
        "max_scalar_residual": max_residual,
        "fields_per_coframe": 10,
        "transitive_source_sha256": digest(ADJACENCY_BUILDER),
    }


def exact_algebra() -> dict[str, object]:
    eta = sp.diag(-1, 1, 1, 1)

    # Proper, orthochronous Lorentz gauge refactorization of the same metric.
    lorentz = sp.diag(1, -1, -1, 1)
    affine_midpoint = (sp.eye(4) + lorentz) / 2
    if sp.simplify(lorentz.T * eta * lorentz - eta) != sp.zeros(4):
        raise AssertionError("registered gauge matrix is not Lorentz")
    if lorentz.det() != 1 or lorentz[0, 0] != 1:
        raise AssertionError("registered gauge matrix is not proper orthochronous")
    if affine_midpoint.det() != 0 or affine_midpoint.rank() != 2:
        raise AssertionError("affine coframe midpoint catch did not trigger")

    # Even direct metric averaging can leave the Lorentzian domain.
    g0 = sp.diag(-1, 1, 1, 1)
    g1 = sp.Matrix(
        [
            [-1, 2, 0, 0],
            [2, -3, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    metric_midpoint = (g0 + g1) / 2
    if g0.det() >= 0 or g1.det() >= 0:
        raise AssertionError("metric endpoints are not Lorentzian")
    if g0[0, 0] >= 0 or g1[0, 0] >= 0:
        raise AssertionError("common coordinate time is not timelike")
    if metric_midpoint.det() != 0:
        raise AssertionError("affine metric midpoint catch did not trigger")
    relative_metric_map = g0.inv() * g1
    relative_eigenvalues = relative_metric_map.eigenvals()
    negative_eigenspace_dimension = len(
        (relative_metric_map + sp.eye(4)).nullspace()
    )
    if relative_eigenvalues != {-1: 2, 1: 2}:
        raise AssertionError("relative metric spectrum changed")
    if negative_eigenspace_dimension != 1:
        raise AssertionError("negative relative eigenspace is not one size-two block")

    # Exact reciprocal one-parameter subgroup and dual pairing.
    x, y = sp.symbols("x y", real=True)
    pairing = sp.Matrix([[0, 1], [1, 0]])

    def reciprocal(depth: sp.Expr) -> sp.Matrix:
        return sp.diag(sp.exp(-depth), sp.exp(depth))

    px = reciprocal(x)
    py = reciprocal(y)
    if sp.simplify(px * py - reciprocal(x + y)) != sp.zeros(2):
        raise AssertionError("reciprocal composition failed")
    if sp.simplify(px.T * pairing * px - pairing) != sp.zeros(2):
        raise AssertionError("reciprocal dual pairing failed")
    if px.det() != 1:
        raise AssertionError("reciprocal determinant failed")

    # The ten-field triangular coframe chart is closed as a matrix group once
    # coordinate and internal indices are identified by a chosen
    # trivialization. This is a chart-level positive result, not yet a
    # physical operation on metric equivalence classes.
    u1, w1c, b1, r1, t1, e1 = sp.symbols(
        "u1 w1c b1 r1 t1 e1", nonzero=True
    )
    u2, w2c, b2, r2, t2, e2 = sp.symbols(
        "u2 w2c b2 r2 t2 e2", nonzero=True
    )
    s111, s112, s121, s122 = sp.symbols("s111 s112 s121 s122")
    s211, s212, s221, s222 = sp.symbols("s211 s212 s221 s222")
    a1_block = sp.Matrix([[u1, b1], [0, w1c]])
    a2_block = sp.Matrix([[u2, b2], [0, w2c]])
    d1_block = sp.Matrix([[r1, e1], [0, t1]])
    d2_block = sp.Matrix([[r2, e2], [0, t2]])
    s1_block = sp.Matrix([[s111, s112], [s121, s122]])
    s2_block = sp.Matrix([[s211, s212], [s221, s222]])

    def chart_coframe(
        abase: sp.Matrix, dscreen: sp.Matrix, shift: sp.Matrix
    ) -> sp.Matrix:
        return abase.row_join(sp.zeros(2)).col_join(
            (dscreen * shift).row_join(dscreen)
        )

    e1_chart = chart_coframe(a1_block, d1_block, s1_block)
    e2_chart = chart_coframe(a2_block, d2_block, s2_block)
    product_a = a1_block * a2_block
    product_d = d1_block * d2_block
    product_s = d2_block.inv() * s1_block * a2_block + s2_block
    product_reconstructed = chart_coframe(product_a, product_d, product_s)
    if sp.simplify(e1_chart * e2_chart - product_reconstructed) != sp.zeros(4):
        raise AssertionError("complete triangular coframe chart is not closed")
    inverse_s = -d1_block * s1_block * a1_block.inv()
    inverse_reconstructed = chart_coframe(
        a1_block.inv(), d1_block.inv(), inverse_s
    )
    if sp.simplify(e1_chart * inverse_reconstructed - sp.eye(4)) != sp.zeros(4):
        raise AssertionError("complete triangular coframe inverse failed")
    omega = sp.symbols("Omega", positive=True)
    central_scale = omega * sp.eye(4)
    if (
        sp.simplify(central_scale * e1_chart - e1_chart * central_scale)
        != sp.zeros(4)
    ):
        raise AssertionError("common scale is not central in chart group")
    shear_frame = sp.eye(4)
    shear_frame[0, 1] = 1
    ungauged_product_metric = shear_frame.T * eta * shear_frame
    second_gauge_product_metric = (
        (shear_frame * lorentz).T * eta * (shear_frame * lorentz)
    )
    independent_gauge_residual = sp.simplify(
        second_gauge_product_metric - ungauged_product_metric
    )
    if independent_gauge_residual == sp.zeros(4):
        raise AssertionError("chart group product unexpectedly descended through gauge")

    # CSN quotient: common shifts change kappa but not reciprocal depth.
    a, c, sigma = sp.symbols("a c sigma", real=True)
    phi = (c - a) / 2
    kappa = (c + a) / 2
    if sp.simplify(((c + sigma) - (a + sigma)) / 2 - phi) != 0:
        raise AssertionError("CSN changed reciprocal depth")
    if sp.simplify(((c + sigma) + (a + sigma)) / 2 - kappa) != sigma:
        raise AssertionError("CSN common-scale shift not recovered")

    # J1/J2 disagree already in a one-field exact toy realization.
    lam = sp.symbols("lambda", real=True)
    j1_toy = sp.expand(lam * lam)
    j2_toy = lam
    if j1_toy.subs(lam, 0) != j2_toy.subs(lam, 0):
        raise AssertionError("toy joins disagree at first endpoint")
    if j1_toy.subs(lam, 1) != j2_toy.subs(lam, 1):
        raise AssertionError("toy joins disagree at second endpoint")
    if sp.simplify(j1_toy - j2_toy) == 0:
        raise AssertionError("toy joins did not disagree in the interior")

    # Simplex bubbles: one preserves every edge; one preserves every face.
    w0, w1, w2, w3 = sp.symbols("w0 w1 w2 w3", nonnegative=True)
    base_bubble = w0 * w1 * w2
    volume_bubble = w0 * w1 * w2 * w3
    vertices = (
        {w0: 1, w1: 0, w2: 0, w3: 0},
        {w0: 0, w1: 1, w2: 0, w3: 0},
        {w0: 0, w1: 0, w2: 1, w3: 0},
        {w0: 0, w1: 0, w2: 0, w3: 1},
    )
    for vertex in vertices:
        if base_bubble.subs(vertex) != 0 or volume_bubble.subs(vertex) != 0:
            raise AssertionError("bubble does not vanish at a vertex")
    edge_checks = 0
    weights = (w0, w1, w2, w3)
    for first in range(4):
        for second in range(first + 1, 4):
            substitution = {
                weight: 0
                for index, weight in enumerate(weights)
                if index not in (first, second)
            }
            if sp.simplify(base_bubble.subs(substitution)) != 0:
                raise AssertionError("base bubble does not vanish on an edge")
            if sp.simplify(volume_bubble.subs(substitution)) != 0:
                raise AssertionError("volume bubble does not vanish on an edge")
            edge_checks += 1
    face_checks = 0
    for weight in weights:
        if sp.simplify(volume_bubble.subs(weight, 0)) != 0:
            raise AssertionError("volume bubble does not vanish on a face")
        face_checks += 1
    base_barycenter = {w0: sp.Rational(1, 3), w1: sp.Rational(1, 3), w2: sp.Rational(1, 3), w3: 0}
    if base_bubble.subs(base_barycenter) != sp.Rational(1, 27):
        raise AssertionError("base bubble is not active at the base barycenter")

    # Reciprocal bubble counterfamily. It preserves all edge data and coframe
    # determinant but freely changes the interior causal sign.
    delta = sp.symbols("delta", real=True)
    reciprocal_coframe = sp.diag(sp.exp(-delta), sp.exp(delta), 1, 1)
    reciprocal_metric = sp.simplify(reciprocal_coframe.T * eta * reciprocal_coframe)
    covector = sp.Matrix([1, 1, 0, 0])
    scalar_norm = sp.simplify((covector.T * reciprocal_metric.inv() * covector)[0])
    expected_norm = -sp.exp(2 * delta) + sp.exp(-2 * delta)
    if sp.simplify(scalar_norm - expected_norm) != 0:
        raise AssertionError("reciprocal bubble norm formula failed")
    if reciprocal_coframe.det() != 1 or reciprocal_metric.det() != -1:
        raise AssertionError("reciprocal bubble changed determinant")
    negative_value = sp.expand_func(scalar_norm.subs(delta, sp.log(2))).simplify()
    positive_value = sp.expand_func(scalar_norm.subs(delta, -sp.log(2))).simplify()
    if negative_value != sp.Rational(-15, 4) or positive_value != sp.Rational(15, 4):
        raise AssertionError("reciprocal bubble did not flip causal sign")

    return {
        "lorentz_gauge": {
            "matrix": str(lorentz.tolist()),
            "determinant": str(lorentz.det()),
            "time_entry": str(lorentz[0, 0]),
            "metric_residual": str(lorentz.T * eta * lorentz - eta),
            "affine_midpoint_rank": affine_midpoint.rank(),
            "affine_midpoint_determinant": str(affine_midpoint.det()),
        },
        "metric_affine": {
            "endpoint_determinants": [str(g0.det()), str(g1.det())],
            "common_time_entries": [str(g0[0, 0]), str(g1[0, 0])],
            "midpoint_determinant": str(metric_midpoint.det()),
        },
        "relative_metric_log_obstruction": {
            "relative_map": str(relative_metric_map.tolist()),
            "eigenvalue_multiplicities": {"-1": 2, "1": 2},
            "negative_eigenspace_dimension": negative_eigenspace_dimension,
            "negative_jordan_blocks": "one size-two block",
            "real_logarithm": "DOES_NOT_EXIST",
            "reason": (
                "a real invertible matrix has a real logarithm only when "
                "negative-real Jordan blocks of each size occur in pairs"
            ),
        },
        "reciprocal_subgroup": {
            "composition": "P(x)P(y)=P(x+y)",
            "pairing_preserved": True,
            "determinant": "1",
            "csn_invariant_depth": "(c-a)/2",
            "csn_variant_common_scale": "(c+a)/2 -> (c+a)/2+sigma",
        },
        "complete_triangular_chart_group": {
            "coframe_form": "E(A,D,S)=[[A,0],[D*S,D]]",
            "product_A": "A1*A2",
            "product_D": "D1*D2",
            "product_S": "D2^-1*S1*A2+S2",
            "inverse_A": "A^-1",
            "inverse_D": "D^-1",
            "inverse_S": "-D*S*A^-1",
            "closure_residual": "ZERO_4X4",
            "inverse_residual": "ZERO_4X4",
            "common_scale": "CENTRAL",
            "physical_scope": "CHOSEN_COORDINATE_INTERNAL_TRIVIALIZATION",
            "independent_second_input_gauge_metric_residual": str(
                independent_gauge_residual.tolist()
            ),
            "independent_gauge_descent": "FAILS_WITHOUT_SELECTED_SECTION",
        },
        "toy_chart_difference": {
            "J1": str(j1_toy),
            "J2": str(j2_toy),
            "difference": str(sp.factor(j1_toy - j2_toy)),
            "endpoint_agreement": True,
        },
        "bubbles": {
            "base_edge_preserving": str(base_bubble),
            "volume_face_preserving": str(volume_bubble),
            "vertex_checks": len(vertices),
            "edge_checks": edge_checks,
            "face_checks": face_checks,
            "base_barycenter_value": "1/27",
            "coframe_determinant": "1",
            "metric_determinant": "-1",
            "scalar_norm": str(scalar_norm),
            "delta_plus_log2": str(negative_value),
            "delta_minus_log2": str(positive_value),
        },
    }


def premise_rows() -> list[dict[str, str]]:
    return [
        {
            "premise": "metric_from_complete_coframe",
            "mathematical_type": "UNARY_ALGEBRAIC_CONSTRUCTION",
            "exact_scope": "g=eta_ab e^a tensor e^b for one supplied coframe",
            "multi_input_composition": "NO",
            "ruling": "CONSTRAINS_OUTPUT_NOT_JOIN",
        },
        {
            "premise": "positional_comparison_composition",
            "mathematical_type": "ONE_PARAMETER_GROUP_LAW",
            "exact_scope": "P(Delta1+Delta2)=P(Delta1)P(Delta2)",
            "multi_input_composition": "RECIPROCAL_DEPTH_SUBGROUP_ONLY",
            "ruling": "PARTIAL_NATIVE_LAW",
        },
        {
            "premise": "dual_reciprocity",
            "mathematical_type": "GROUP_ACTION_AND_PAIRING_PRESERVATION",
            "exact_scope": "P^T K P=K and det(P)=1 in reciprocal pair",
            "multi_input_composition": "NO_COMPLETE_COFRAME_MAP",
            "ruling": "CONSTRAINS_RECIPROCAL_FACTOR",
        },
        {
            "premise": "common_scale_neutrality",
            "mathematical_type": "POSITIVE_SCALE_EQUIVALENCE_RELATION",
            "exact_scope": "g equivalent to Omega^2 g",
            "multi_input_composition": "NO",
            "ruling": "QUOTIENT_NOT_CONNECTION_OR_BARYCENTER",
        },
        {
            "premise": "finite_cell_seal",
            "mathematical_type": "CONDITIONAL_LOCAL_INVOLUTION_AND_GLUE",
            "exact_scope": "seal-local reciprocal parity/sign with incomplete lift",
            "multi_input_composition": "NO",
            "ruling": "BOUNDARY_COMPATIBILITY_ONLY",
        },
        {
            "premise": "reciprocal_cocycle",
            "mathematical_type": "TRANSITION_FUNCTION_COMPATIBILITY",
            "exact_scope": "Z2-graded products on an already supplied cover",
            "multi_input_composition": "NO",
            "ruling": "GLUES_CHARTS_DOES_NOT_AVERAGE_CONFIGURATIONS",
        },
        {
            "premise": "cartan_geometry",
            "mathematical_type": "CONNECTION_DERIVED_FROM_ONE_SUPPLIED_GEOMETRY",
            "exact_scope": "transport and curvature after coframe choice",
            "multi_input_composition": "NO_CONFIGURATION_SPACE_CONNECTION",
            "ruling": "DIAGNOSTIC_NOT_SELECTOR",
        },
        {
            "premise": "current_bootstrap",
            "mathematical_type": "ON_SHELL_ADMISSIBILITY_PREDICATE",
            "exact_scope": "tests completed solutions without a varied functional or section",
            "multi_input_composition": "NO",
            "ruling": "FILTER_NOT_MAP",
        },
    ]


def candidate_rows() -> list[dict[str, str]]:
    return [
        {
            "candidate": "RECIPROCAL_LOGARITHMIC_MEAN",
            "domain": "aligned positive determinant-one reciprocal subgroup",
            "formula_or_operation": "P_bar=exp(sum_i w_i log(P_i))=P(sum_i w_i phi_i)",
            "extra_structure": "common event/domain; chosen sign/unit of phi; supplied weights",
            "status": "DERIVED_ALGEBRAIC_IDENTITY_GIVEN_CHOSEN_WEIGHTS_AND_ALIGNED_LOG_COORDINATE",
            "complete_coframe_ruling": "DOES_NOT_COMPOSE_ANGULAR_SHIFT_SCALAR_OR_COMMON_SCALE_SECTORS",
        },
        {
            "candidate": "J1_GENERATOR_COEFFICIENT_BARYCENTRIC",
            "domain": "frozen polynomial generators plus marked coordinate chords",
            "formula_or_operation": "mix coordinates and coefficient tensors then evaluate",
            "extra_structure": "generator basis; polynomial family; marked points; common chart",
            "status": "CHOSE_ANALYTIC_CONFIGURATION_CHART",
            "complete_coframe_ruling": "NOT_SELECTED_BY_REGISTERED_PREMISES",
        },
        {
            "candidate": "J2_EVALUATED_COFIELD_BARYCENTRIC",
            "domain": "ten latent triangular-coframe fields plus four dphi components",
            "formula_or_operation": "evaluate endpoints then linearly mix latent fields and covector components",
            "extra_structure": "triangular gauge; common coordinates; field parameterization",
            "status": "CHOSE_LOCAL_COFIELD_CHART",
            "complete_coframe_ruling": "NOT_GLOBAL_SCALAR_INTEGRABILITY_OR_GAUGE_INDEPENDENT",
        },
        {
            "candidate": "COMPLETE_TRIANGULAR_COFRAME_GROUP",
            "domain": "registered ten-field exponential triangular coframe chart",
            "formula_or_operation": "E1*E2 with semidirect shift law; weighted option exp(sum_i w_i log(E_i))",
            "extra_structure": "type-correct relative base/internal identification; selected representative section or genuinely local-Lorentz-equivariant quotient operation; selected weighted multi-input rule; compatible phi/dphi rule",
            "status": "DERIVED_CHART_GROUP_CLOSURE; CHOSE_AS_PHYSICAL_COMPOSITION",
            "complete_coframe_ruling": "DOES_NOT_DESCEND_THROUGH_UNSELECTED_LOCAL_LORENTZ_AND_CHART_REPRESENTATIVES",
        },
        {
            "candidate": "RAW_AFFINE_COFRAME_MEAN",
            "domain": "coframe matrices in one chosen trivialization",
            "formula_or_operation": "sum_i w_i E_i",
            "extra_structure": "relative gauge/trivialization identification",
            "status": "REFUTED_AS_REPRESENTATIVE_INDEPENDENT",
            "complete_coframe_ruling": "SAME_METRIC_GAUGES_CAN_HAVE_SINGULAR_MIDPOINT",
        },
        {
            "candidate": "AFFINE_METRIC_MEAN",
            "domain": "metric components in one chart",
            "formula_or_operation": "sum_i w_i g_i",
            "extra_structure": "point/chart identification and a Lorentzian-domain prescription",
            "status": "REFUTED_AS_UNCONDITIONALLY_LORENTZIAN",
            "complete_coframe_ruling": "LORENTZIAN_ENDPOINTS_CAN_HAVE_DEGENERATE_MIDPOINT",
        },
        {
            "candidate": "RELATIVE_FRAME_LOG_OR_GEODESIC",
            "domain": "identified frame bundle or metric configuration space",
            "formula_or_operation": "choose base; log relative maps; exponentiate weighted tangent",
            "extra_structure": "relative transport; connection; log branch; base/symmetrization",
            "status": "OPEN_EXTRA_STRUCTURE_AND_NOT_GLOBAL",
            "complete_coframe_ruling": "SOME_LORENTZIAN_PAIRS_HAVE_NO_REAL_RELATIVE_LOG",
        },
        {
            "candidate": "QUOTIENT_FRECHET_OR_KARCHER_BARYCENTER",
            "domain": "physical configuration quotient",
            "formula_or_operation": "minimize weighted squared distance",
            "extra_structure": "native distance/connection; measure; existence and uniqueness branch",
            "status": "OPEN_EXTRA_STRUCTURE",
            "complete_coframe_ruling": "NOT_CURRENTLY_SUPPLIED",
        },
        {
            "candidate": "COCYCLE_OR_SEAM_GLUE",
            "domain": "overlapping charts on one supplied bundle",
            "formula_or_operation": "identify representatives by transition functions",
            "extra_structure": "cover; incidence; complete lift",
            "status": "DERIVED_PARTIAL_GLUE_NOT_COMPOSITION",
            "complete_coframe_ruling": "CATEGORY_ERROR_AS_BARYCENTER",
        },
        {
            "candidate": "ACTION_OR_BOOTSTRAP_SELECTED_PATH",
            "domain": "off_shell configuration histories",
            "formula_or_operation": "extremize functional or solve operational closure equation",
            "extra_structure": "native functional/EOM; variation domain; boundary data",
            "status": "OPEN_NOT_SUPPLIED",
            "complete_coframe_ruling": "CURRENT_BOOTSTRAP_IS_ONLY_ON_SHELL_FILTER",
        },
    ]


def requirement_rows() -> list[dict[str, str]]:
    return [
        {
            "requirement": "R1_DOMAIN_OUTPUT",
            "J1": "PASS_BOUNDED_ANALYTIC_FAMILY",
            "J2": "PASS_LOCAL_COFIELD_ONLY",
            "reciprocal_mean": "PASS_RECIPROCAL_SUBGROUP_ONLY",
            "triangular_group": "PASS_IN_CHOSEN_COMPLETE_COFRAME_CHART",
            "native_complete_status": "OPEN",
        },
        {
            "requirement": "R2_VERTEX_RECOVERY",
            "J1": "PASS",
            "J2": "PASS",
            "reciprocal_mean": "PASS",
            "triangular_group": "PASS_FOR_IDENTITY_BASED_LOG_MEAN",
            "native_complete_status": "CONSTRAINT_ONLY",
        },
        {
            "requirement": "R3_RELABELING_NATURALITY",
            "J1": "PASS_WITH_MATCHED_GENERATOR_RELABELING",
            "J2": "PASS",
            "reciprocal_mean": "PASS",
            "triangular_group": "BINARY_PRODUCT_ORDERED; LOG_MEAN_SYMMETRIC_IN_CHART",
            "native_complete_status": "CONSTRAINT_ONLY",
        },
        {
            "requirement": "R4_COMMON_COVARIANCE",
            "J1": "NOT_DERIVED_OUTSIDE_FROZEN_GENERATOR_CHART",
            "J2": "NOT_DERIVED_OUTSIDE_TRIANGULAR_LATENT_CHART",
            "reciprocal_mean": "PASS_FOR_ALIGNED_RECIPROCAL_ACTION",
            "triangular_group": "FAILS_OR_UNDEFINED_OUTSIDE_CHOSEN_SOLDERING_AND_SECTION",
            "native_complete_status": "OPEN",
        },
        {
            "requirement": "R5_REPRESENTATIVE_INDEPENDENCE",
            "J1": "FAIL_OR_UNDEFINED_WITHOUT_RELATIVE_GAUGE",
            "J2": "FAIL_OR_UNDEFINED_WITHOUT_RELATIVE_GAUGE",
            "reciprocal_mean": "PASS_FOR_INDEPENDENT_CSN_SHIFTS_OF_DIAGONAL_PAIR",
            "triangular_group": "FAIL_OR_UNDEFINED_UNDER_INDEPENDENT_LOCAL_LORENTZ_GAUGES",
            "native_complete_status": "OPEN_FOR_FULL_COFRAME",
        },
        {
            "requirement": "R6_CSN_COMPATIBILITY",
            "J1": "NOT_ESTABLISHED_FOR_COMPLETE_GENERATOR",
            "J2": "PASS_RECIPROCAL_DEPTH_QUOTIENT; COMMON_REPRESENTATIVE_CHOSEN",
            "reciprocal_mean": "PASS",
            "triangular_group": "CENTRAL_COMMON_SCALE; QUOTIENT_COMPATIBLE_IN_CHART",
            "native_complete_status": "PARTIAL_ONLY",
        },
        {
            "requirement": "R7_RECIPROCITY_COMPATIBILITY",
            "J1": "NOT_DERIVED_FOR_COMPLETE_FIELDS",
            "J2": "PASS_ONLY_FOR_LINEAR_LOG_DEPTH_SUBSECTOR",
            "reciprocal_mean": "PASS",
            "triangular_group": "CONTAINS_RECIPROCAL_SUBGROUP; FULL_EXTENSION_NOT_DERIVED",
            "native_complete_status": "PARTIAL_ONLY",
        },
        {
            "requirement": "R8_FACE_EDGE_CONSISTENCY",
            "J1": "PASS_WITHIN_ITS_OWN_RULE",
            "J2": "PASS_WITHIN_ITS_OWN_RULE",
            "reciprocal_mean": "PASS",
            "triangular_group": "PASS_FOR_ONE_FIXED_GROUP_MEAN_RULE",
            "native_complete_status": "DOES_NOT_ENSURE_UNIQUENESS",
        },
        {
            "requirement": "R9_SCALAR_INTEGRITY",
            "J1": "PASS_WITHIN_FROZEN_POLYNOMIAL_FAMILY",
            "J2": "NOT_ASSERTED_BEYOND_LOCAL_COVECTOR",
            "reciprocal_mean": "NO_COMPLETE_SCALAR_RULE",
            "triangular_group": "NO_PHI_OR_DPHI_COMPOSITION",
            "native_complete_status": "OPEN",
        },
        {
            "requirement": "R10_FINITE_CELL_COMPATIBILITY",
            "J1": "NO_GLOBAL_CELL_OR_SEAL_ACTION_LOADED",
            "J2": "NO_GLOBAL_CELL_OR_SEAL_ACTION_LOADED",
            "reciprocal_mean": "SEAL_LOCAL_RECIPROCAL_PARITY_ONLY",
            "triangular_group": "NO_SELECTED_GLOBAL_REFERENCE_OR_COMPLETE_SEAL_LIFT",
            "native_complete_status": "OPEN",
        },
        {
            "requirement": "R11_OPERATIONAL_BOOTSTRAP",
            "J1": "ABSENT",
            "J2": "ABSENT",
            "reciprocal_mean": "ABSENT",
            "triangular_group": "ABSENT",
            "native_complete_status": "OPEN",
        },
    ]


def main() -> None:
    source_count = verify_sources()
    algebra = exact_algebra()
    source_behavior = source_behavioral_reconstruction()
    premises = premise_rows()
    candidates = candidate_rows()
    requirements = requirement_rows()

    write_tsv("PREMISE_TYPE_LEDGER.tsv", premises)
    write_tsv("CANDIDATE_OPERATION_CENSUS.tsv", candidates)
    write_tsv("J1_J2_REQUIREMENT_MATRIX.tsv", requirements)

    result = {
        "schema": "udt-native-coframe-composition-audit-v1",
        "source_count": source_count,
        "algebra": algebra,
        "source_behavioral_reconstruction": source_behavior,
        "counts": {
            "premises_typed": len(premises),
            "candidate_operations": len(candidates),
            "requirements": len(requirements),
            "premises_with_complete_multi_input_map": sum(
                row["multi_input_composition"] == "YES" for row in premises
            ),
            "partial_native_reciprocal_laws": sum(
                row["ruling"] == "PARTIAL_NATIVE_LAW" for row in premises
            ),
            "candidate_complete_native_laws": sum(
                row["complete_coframe_ruling"] == "SELECTED_NATIVE_COMPLETE_LAW"
                for row in candidates
            ),
        },
        "rulings": {
            "reciprocal_depth_composition": "DERIVED_CONDITIONAL_PAIRWISE_ONE_PARAMETER_RECIPROCAL_SUBGROUP",
            "reciprocal_weighted_mean": "DERIVED_ALGEBRAIC_IDENTITY_GIVEN_CHOSEN_WEIGHTS_AND_ALIGNED_LOG_COORDINATE; NOT_SELECTED_BY_CURRENT_UDT_PREMISES",
            "native_complete_coframe_composition": "OPEN_NOT_SUPPLIED_BY_CURRENT_REGISTERED_PREMISES",
            "J1": "CHOSE_ANALYTIC_CONFIGURATION_CHART",
            "J2": "CHOSE_LOCAL_COFIELD_CHART",
            "triangular_complete_chart_group": "DERIVED_ALGEBRAIC_CLOSURE_IN_CHOSEN_TRIVIALIZATION_NOT_NATIVE_PHYSICAL_COMPOSITION",
            "bank_simplex_pocket": "OBSERVED_BOUNDED_J1_CHART_NOT_COMPOSITION_INVARIANT",
            "invariant_remainder": [
                "ENDPOINT_AND_REGISTERED_EDGE_CLASSES",
                "LORENTZIAN_NONDEGENERACY_WITHIN_EXPONENTIAL_TRIANGULAR_CHARTS",
                "AT_LEAST_ONE_ZERO_ON_ANY_SUPPLIED_CONTINUOUS_OPPOSITE_SIGN_JOIN",
            ],
            "join_dependent": [
                "BASE_INTERIOR_POCKET",
                "TRANSITION_MULTIPLICITY",
                "NEGATIVE_COMPONENT_COUNT",
                "INTERFACE_LOCATION_AND_SHAPE",
            ],
            "smallest_missing_object": "TYPE_CORRECT_RELATIVE_BASE_INTERNAL_IDENTIFICATION_PLUS_EITHER_A_SELECTED_REPRESENTATIVE_SECTION_OR_LOCAL_LORENTZ_EQUIVARIANT_QUOTIENT_OPERATION_PLUS_A_SELECTED_WEIGHTED_MULTI_INPUT_RULE_AND_COMPATIBLE_PHI_DPHI_RULE",
        },
        "maximum_conclusion": "CURRENT_UDT_PREMISES_SUPPLY_CONDITIONAL_RECIPROCAL_ONE_PARAMETER_COMPOSITION_BUT_NOT_A_WEIGHTED_MULTI_CONFIGURATION_MEAN_OR_NATIVE_COMPLETE_COFRAME_COMPOSITION",
    }
    (HERE / "RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

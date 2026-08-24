#!/usr/bin/env python3
"""Exact production algebra for the G244 metric-native observer-sky query."""

from __future__ import annotations

import argparse
import json
import random
from fractions import Fraction
from pathlib import Path

import sympy as sp


PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "DERIVATION_RESULT.json"
LANDING = (
    "METRIC_NATIVE_OBSERVER_SKY_AREA_SHAPE_QUERY_DERIVED_CONDITIONALLY"
    "__NO_FITTED_ANGULAR_COEFFICIENT"
    "__CATALOG_IDENTIFICATION_AND_HISTORY_OPEN"
)


def fraction_payload(value: Fraction | sp.Rational) -> dict[str, object]:
    value = Fraction(int(value.p), int(value.q)) if isinstance(value, sp.Rational) else value
    return {
        "exact": f"{value.numerator}/{value.denominator}",
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": float(value),
    }


def normalize(values: list[sp.Rational]) -> list[sp.Rational]:
    total = sum(values, sp.Rational(0))
    if total <= 0:
        raise ValueError("normalization requires positive mass")
    return [sp.cancel(value / total) for value in values]


def bilinear(left: list[sp.Rational], kernel: sp.Matrix, right: list[sp.Rational]) -> sp.Rational:
    return sp.cancel((sp.Matrix(1, len(left), left) * kernel * sp.Matrix(right))[0])


def exact_orthogonal(rng: random.Random, allow_reflection: bool = True) -> sp.Matrix:
    triples = ((3, 4, 5), (5, 12, 13), (7, 24, 25), (8, 15, 17), (20, 21, 29))
    x, y, z = rng.choice(triples)
    if rng.randrange(2):
        x = -x
    if rng.randrange(2):
        y = -y
    q = sp.Matrix([[sp.Rational(x, z), -sp.Rational(y, z)],
                   [sp.Rational(y, z), sp.Rational(x, z)]])
    if allow_reflection and rng.randrange(2):
        q = q * sp.diag(1, -1)
    return q


def random_invertible_2(rng: random.Random) -> sp.Matrix:
    while True:
        matrix = sp.Matrix([[rng.randint(-7, 7), rng.randint(-7, 7)],
                            [rng.randint(-7, 7), rng.randint(-7, 7)]])
        if matrix.det() != 0:
            return matrix


def symmetric_2(rng: random.Random) -> sp.Matrix:
    a, b, c = (rng.randint(-4, 4) for _ in range(3))
    return sp.Matrix([[a, b], [b, c]])


def phase_upper(symmetric: sp.Matrix) -> sp.Matrix:
    identity = sp.eye(2)
    zero = sp.zeros(2)
    return identity.row_join(symmetric).col_join(zero.row_join(identity))


def phase_lower(symmetric: sp.Matrix) -> sp.Matrix:
    identity = sp.eye(2)
    zero = sp.zeros(2)
    return identity.row_join(zero).col_join(symmetric.row_join(identity))


def compute() -> dict[str, object]:
    a, b, c, d = sp.symbols("a b c d", real=True)
    symbolic_d = sp.Matrix([[a, b], [c, d]])
    symbolic_h = symbolic_d.T * symbolic_d
    determinant_identity = sp.expand(symbolic_h.det() - symbolic_d.det() ** 2)
    x = a * a + c * c
    z = b * b + d * d
    y = a * b + c * d
    shear_nonnegative_identity = sp.expand(
        symbolic_h.trace() ** 2
        - 4 * symbolic_h.det()
        - ((x - z) ** 2 + 4 * y ** 2)
    )
    if determinant_identity != 0 or shear_nonnegative_identity != 0:
        raise AssertionError("symbolic Gram identities failed")

    rng = random.Random(244001)
    matrix_cases = 1024
    gauge_assertions = 0
    positive_shear_cases = 0
    reflection_parity_flips = 0
    for _ in range(matrix_cases):
        matrix_d = random_invertible_2(rng)
        h = matrix_d.T * matrix_d
        det_d = sp.Rational(matrix_d.det())
        area = abs(det_d)
        shape = h / area
        shear_power = sp.cancel(h.trace() ** 2 / (4 * h.det()) - 1)
        if h.det() != det_d ** 2 or shape.det() != 1 or shear_power < 0:
            raise AssertionError("area/shape decomposition failed")
        if shear_power > 0:
            positive_shear_cases += 1

        q_source = exact_orthogonal(rng)
        q_observer = exact_orthogonal(rng)
        transformed = q_source.T * matrix_d * q_observer
        transformed_h = transformed.T * transformed
        if transformed_h != q_observer.T * h * q_observer:
            raise AssertionError("endpoint screen covariance failed")
        if abs(transformed.det()) != area:
            raise AssertionError("area gauge invariance failed")
        transformed_shear = sp.cancel(
            transformed_h.trace() ** 2 / (4 * transformed_h.det()) - 1
        )
        if transformed_shear != shear_power:
            raise AssertionError("shear gauge invariance failed")
        expected_parity = sp.sign(q_source.det()) * sp.sign(q_observer.det()) * sp.sign(det_d)
        if sp.sign(transformed.det()) != expected_parity:
            raise AssertionError("orientation-line parity law failed")
        if sp.sign(transformed.det()) != sp.sign(det_d):
            reflection_parity_flips += 1

        scale = sp.Rational(rng.randint(1, 9), rng.randint(1, 9))
        scaled = scale * matrix_d
        scaled_h = scaled.T * scaled
        if abs(scaled.det()) != scale ** 2 * area:
            raise AssertionError("area scale weight failed")
        if scaled_h / abs(scaled.det()) != shape:
            raise AssertionError("shape scale invariance failed")
        if sp.cancel(scaled_h.trace() ** 2 / (4 * scaled_h.det()) - 1) != shear_power:
            raise AssertionError("shear scale invariance failed")
        gauge_assertions += 12

    if positive_shear_cases == 0 or reflection_parity_flips == 0:
        raise AssertionError("matrix census missed required strata")

    conformal_cases = 0
    for _ in range(64):
        q = exact_orthogonal(rng)
        scale = sp.Rational(rng.randint(1, 12), rng.randint(1, 12))
        matrix_d = scale * q
        h = matrix_d.T * matrix_d
        area = abs(matrix_d.det())
        if h / area != sp.eye(2):
            raise AssertionError("conformal response did not give unit shape")
        if sp.cancel(h.trace() ** 2 / (4 * h.det()) - 1) != 0:
            raise AssertionError("conformal response has spurious shear")
        conformal_cases += 1

    omega = sp.zeros(2).row_join(sp.eye(2)).col_join((-sp.eye(2)).row_join(sp.zeros(2)))
    phase_cases = 1024
    nonmultiplicative_position_cases = 0
    for _ in range(phase_cases):
        m10 = phase_upper(symmetric_2(rng)) * phase_lower(symmetric_2(rng))
        m21 = phase_lower(symmetric_2(rng)) * phase_upper(symmetric_2(rng))
        m20 = m21 * m10
        for phase in (m10, m21, m20):
            if phase.T * omega * phase != omega:
                raise AssertionError("phase is not symplectic")
        a21, b21, d10 = m21[:2, :2], m21[:2, 2:], m10[2:, 2:]
        b10 = m10[:2, 2:]
        b20 = m20[:2, 2:]
        if b20 != a21 * b10 + b21 * d10:
            raise AssertionError("full-phase position block formula failed")
        if b20 != b21 * b10:
            nonmultiplicative_position_cases += 1
    if nonmultiplicative_position_cases == 0:
        raise AssertionError("phase census missed position-block nonmultiplicativity")

    q_reference = normalize([sp.Rational(1), sp.Rational(2), sp.Rational(3), sp.Rational(4)])
    area_response = [sp.Rational(1), sp.Rational(2), sp.Rational(1), sp.Rational(3)]
    finite_cell_jacobi_maps = [sp.diag(area, 1) for area in area_response]
    if [abs(matrix.det()) for matrix in finite_cell_jacobi_maps] != area_response:
        raise AssertionError("finite-cell area response is not a Jacobi determinant readout")
    p_area = normalize([q * response for q, response in zip(q_reference, area_response)])
    kernel = sp.Matrix([
        [0, 1, 0, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 1, 0],
    ])
    dd = bilinear(p_area, kernel, p_area)
    dr = bilinear(p_area, kernel, q_reference)
    rr = bilinear(q_reference, kernel, q_reference)
    w_area = sp.cancel((dd - 2 * dr + rr) / rr)
    mismatch = [p - q for p, q in zip(p_area, q_reference)]
    if w_area != bilinear(mismatch, kernel, mismatch) / rr or w_area != sp.Rational(-1, 6):
        raise AssertionError("area-query witness failed")

    constant_area = [sp.Rational(7)] * 4
    p_constant = normalize([q * response for q, response in zip(q_reference, constant_area)])
    w_constant = sp.cancel(
        (bilinear(p_constant, kernel, p_constant)
         - 2 * bilinear(p_constant, kernel, q_reference) + rr) / rr
    )
    if p_constant != q_reference or w_constant != 0:
        raise AssertionError("constant area did not cancel")

    singular_d = sp.diag(1, 0)
    singular_h = singular_d.T * singular_d
    caustic_phase = sp.eye(4)
    if singular_h.det() != 0 or caustic_phase.det() != 1:
        raise AssertionError("caustic boundary control failed")

    return {
        "audit": "G244_METRIC_NATIVE_OBSERVER_SKY_RESPONSE_QUERY",
        "classification": LANDING,
        "preregistration_commits": ["8d1eb059", "cf301bc9"],
        "metric_status": "DERIVED_CONDITIONAL_EVALUATOR_ON_SUPPLIED_REGULAR_NULL_SHEET",
        "query_status": "CHOSE_GEOMETRIC_AREA_REFERENCE_PROJECTION_NOT_DETECTOR_LAW",
        "catalog_identification": "OPEN_REQUIRES_SOURCE_INCIDENCE_AND_DETECTOR_TRANSFER_CONTRACT",
        "direct_reciprocal_redshift": "UNCHANGED_PHI_EQUALS_LOG1PZ",
        "observational_outcomes": "CLOSED_AND_UNREAD",
        "fitted_angular_coefficients": 0,
        "screen_outputs": {
            "response_tensor": "H=D^dagger D",
            "area": "A=sqrt(det H)=abs(det D)",
            "shape": "C=H/A with det C=1",
            "shear_power": "tr(H)^2/(4 det(H))-1",
            "parity": "orientation-line-valued; scalar only after compatible orientations",
        },
        "symbolic_checks": {
            "det_H_minus_det_D_squared": str(determinant_identity),
            "shear_sum_of_squares_remainder": str(shear_nonnegative_identity),
        },
        "matrix_census": {
            "cases": matrix_cases,
            "assertions": gauge_assertions,
            "positive_shear_cases": positive_shear_cases,
            "reflection_parity_flip_cases": reflection_parity_flips,
            "conformal_cases": conformal_cases,
        },
        "phase_census": {
            "cases": phase_cases,
            "nonmultiplicative_position_cases": nonmultiplicative_position_cases,
            "composition": "M20=M21*M10; B20=A21*B10+B21*D10",
        },
        "area_query_witness": {
            "status": "EXACT_FINITE_OPERATOR_WITNESS_NOT_A_METRIC_HISTORY_OR_FIT",
            "reference": [fraction_payload(value) for value in q_reference],
            "area_response": [fraction_payload(value) for value in area_response],
            "jacobi_maps": [
                [[str(matrix[i, j]) for j in range(2)] for i in range(2)]
                for matrix in finite_cell_jacobi_maps
            ],
            "projected_w": fraction_payload(w_area),
            "constant_area_w": fraction_payload(w_constant),
        },
        "caustic_boundary": {
            "det_position_block": str(singular_d.det()),
            "det_full_phase": str(caustic_phase.det()),
            "position_inverse_used": False,
            "regular_shape_scope_exited": True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = compute()
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUTPUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()

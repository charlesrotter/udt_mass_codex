#!/usr/bin/env python3
"""Exact curvature-invariant Killing certificates for the preregistered screen ensemble."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import subprocess
import traceback
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
POINT_DIR = HERE / "invariant_points"
X, Y, Z = sp.symbols("X Y Z")
DX = (X, Y, Z)
POINTS = {
    "p1": (sp.Rational(1, 5), sp.Rational(1, 7), sp.Rational(1, 11)),
    "p2": (sp.Rational(1, 3), sp.Rational(-1, 5), sp.Rational(1, 7)),
}


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def verify_sources() -> int:
    rows = read_tsv("SOURCE_MANIFEST.tsv")
    assert len(rows) == len({row["path"] for row in rows}) == 48
    for row in rows:
        content = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        assert len(content) == int(row["bytes"])
        assert sha256_bytes(content) == row["sha256"]
    assert sha256_bytes((HERE / "SOURCE_MANIFEST.tsv").read_bytes()) == (
        HERE / "SOURCE_MANIFEST.sha256"
    ).read_text(encoding="utf-8").strip()
    return len(rows)


def trunc(expression: sp.Expr, degree: int) -> sp.Expr:
    expression = sp.expand(expression)
    if expression == 0:
        return sp.S.Zero
    polynomial = sp.Poly(expression, *DX)
    return sp.Add(*(
        coefficient * X**powers[0] * Y**powers[1] * Z**powers[2]
        for powers, coefficient in polynomial.terms()
        if sum(powers) <= degree
    ))


def matrix_trunc(matrix: sp.Matrix, degree: int) -> sp.Matrix:
    return matrix.applyfunc(lambda value: trunc(value, degree))


def matrix_product(left: sp.Matrix, right: sp.Matrix, degree: int) -> sp.Matrix:
    assert left.cols == right.rows
    return sp.Matrix(
        left.rows,
        right.cols,
        lambda i, j: trunc(sum(left[i, k] * right[k, j] for k in range(left.cols)), degree),
    )


def scalar_inverse(expression: sp.Expr, degree: int) -> sp.Expr:
    constant = expression.subs({X: 0, Y: 0, Z: 0})
    assert constant != 0
    relative = trunc((expression - constant) / constant, degree)
    result = sp.S.One
    power = sp.S.One
    sign = -1
    for _ in range(1, degree + 1):
        power = trunc(power * relative, degree)
        result = trunc(result + sign * power, degree)
        sign *= -1
    inverse = trunc(result / constant, degree)
    assert trunc(expression * inverse, degree) == 1
    return inverse


def scalar_power(expression: sp.Expr, exponent: int, degree: int) -> sp.Expr:
    if exponent == 0:
        return sp.S.One
    base = expression if exponent > 0 else scalar_inverse(expression, degree)
    result = sp.S.One
    for _ in range(abs(exponent)):
        result = trunc(result * base, degree)
    return result


def formal_inverse(metric: sp.Matrix, degree: int) -> sp.Matrix:
    zero = {X: 0, Y: 0, Z: 0}
    g0_inverse = metric.subs(zero).inv()
    perturbation = metric - metric.subs(zero)
    relative = matrix_product(g0_inverse, perturbation, degree)
    series = sp.eye(metric.rows)
    power = sp.eye(metric.rows)
    sign = -1
    for _ in range(1, degree + 1):
        power = matrix_product(power, relative, degree)
        series = matrix_trunc(series + sign * power, degree)
        sign *= -1
    inverse = matrix_product(series, g0_inverse, degree)
    assert matrix_product(inverse, metric, degree) == sp.eye(metric.rows)
    return inverse


def coordinate_derivative(expression: sp.Expr, coordinate: int) -> sp.Expr:
    if coordinate == 0:
        return sp.S.Zero
    return sp.diff(expression, DX[coordinate - 1])


def quaternion_and_coframe(point: tuple[sp.Rational, ...]):
    sx, sy, sz = (point[0] + X, point[1] + Y, point[2] + Z)
    radius_squared = sx*sx + sy*sy + sz*sz
    denominator_inverse = scalar_inverse(1 + radius_squared, 4)
    q = (
        trunc((1 - radius_squared) * denominator_inverse, 4),
        trunc(2*sx * denominator_inverse, 4),
        trunc(2*sy * denominator_inverse, 4),
        trunc(2*sz * denominator_inverse, 4),
    )
    differentials = [sp.Matrix([sp.diff(component, coordinate) for coordinate in DX]) for component in q]
    q0, q1, q2, q3 = q
    dq0, dq1, dq2, dq3 = differentials
    sigma1 = (q0*dq1 - q1*dq0 - q2*dq3 + q3*dq2).applyfunc(lambda value: trunc(value, 3))
    sigma2 = (q0*dq2 - q2*dq0 - q3*dq1 + q1*dq3).applyfunc(lambda value: trunc(value, 3))
    sigma3 = (q0*dq3 - q3*dq0 - q1*dq2 + q2*dq1).applyfunc(lambda value: trunc(value, 3))
    return q, (sigma1, sigma2, sigma3)


def profile_values(row: dict[str, str], point: tuple[sp.Rational, ...]):
    q, sigmas = quaternion_and_coframe(point)
    q0, q1, q2, q3 = q
    primary_u = trunc(3 + q0*q0 + 2*q1*q1 + 4*q2*q2 + 8*q3*q3, 3)
    u = primary_u if row["u_profile"] == "U" else sp.Integer(4)
    v0 = trunc(q0*q0 + 3*q1*q1 + 7*q2*q2 + 9*q3*q3, 3)
    r0 = trunc(2*q0*q0 + 5*q1*q1 + 11*q2*q2 + 13*q3*q3, 3)
    b0 = trunc(
        q0*q1 + 2*q0*q2 + 3*q0*q3 + 5*q1*q2 + 7*q1*q3 + 11*q2*q3,
        3,
    )
    epsilon = sp.Rational(1, 10)
    v_profiles = {
        "ONE": sp.S.One,
        "TWO": sp.Integer(2),
        "U": u,
        "V_EPS": trunc(1 + epsilon*v0, 3),
        "ZERO": sp.S.Zero,
    }
    r_profiles = {
        "ONE": sp.S.One,
        "R_EPS": trunc(1 + epsilon*r0, 3),
    }
    b_profiles = {
        "ZERO": sp.S.Zero,
        "B_EPS": trunc(epsilon*b0, 3),
    }
    return u, v_profiles[row["V_profile"]], r_profiles[row["r_profile"]], b_profiles[row["b_profile"]], sigmas


def metric_jet(row: dict[str, str], point: tuple[sp.Rational, ...]) -> sp.Matrix:
    u, area, shear_r, shear_b, (sigma1, sigma2, sigma3) = profile_values(row, point)
    assert area.subs({X: 0, Y: 0, Z: 0}) != 0
    lam = int(row["lambda"])
    a_value = int(row["a"])
    tau = sp.Matrix([1, *(a_value * sigma3)])
    s1 = sp.Matrix([0, *sigma1])
    s2 = sp.Matrix([0, *sigma2])
    s3 = sp.Matrix([0, *sigma3])
    inverse_u = scalar_inverse(u, 3)
    trace_factor = trunc(scalar_power(u, lam, 3) * area, 3)
    r_squared = trunc(shear_r * shear_r, 3)
    rb = trunc(shear_r * shear_b, 3)
    b_squared_plus_r_inverse_squared = trunc(
        shear_b*shear_b + scalar_power(shear_r, -2, 3),
        3,
    )
    metric = matrix_trunc(-inverse_u * (tau * tau.T), 3)
    metric += matrix_trunc(u * (s3 * s3.T), 3)
    metric += matrix_trunc(trace_factor * r_squared * (s1 * s1.T), 3)
    metric += matrix_trunc(trace_factor * rb * (s1 * s2.T + s2 * s1.T), 3)
    metric += matrix_trunc(trace_factor * b_squared_plus_r_inverse_squared * (s2 * s2.T), 3)
    metric = matrix_trunc(metric, 3)
    assert metric == metric.T
    return metric


def invariant_jet(row: dict[str, str], point: tuple[sp.Rational, ...]) -> dict[str, object]:
    metric = metric_jet(row, point)
    inverse = formal_inverse(metric, 3)
    gamma = [[[sp.S.Zero for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for upper, lower1, lower2 in itertools.product(range(4), repeat=3):
        total = sp.S.Zero
        for index in range(4):
            bracket = (
                coordinate_derivative(metric[index, lower2], lower1)
                + coordinate_derivative(metric[index, lower1], lower2)
                - coordinate_derivative(metric[lower1, lower2], index)
            )
            total += inverse[upper, index] * bracket
        gamma[upper][lower1][lower2] = trunc(total / 2, 2)
    for upper, lower1, lower2 in itertools.product(range(4), repeat=3):
        assert trunc(gamma[upper][lower1][lower2] - gamma[upper][lower2][lower1], 2) == 0

    ricci = sp.zeros(4)
    for first, second in itertools.product(range(4), repeat=2):
        total = sp.S.Zero
        for index in range(4):
            total += coordinate_derivative(gamma[index][first][second], index)
            total -= coordinate_derivative(gamma[index][first][index], second)
            for other in range(4):
                total += gamma[index][first][second] * gamma[other][index][other]
                total -= gamma[other][first][index] * gamma[index][second][other]
        ricci[first, second] = trunc(total, 1)
    assert matrix_trunc(ricci - ricci.T, 1) == sp.zeros(4)
    mixed_ricci = matrix_product(inverse, ricci, 1)
    squared = matrix_product(mixed_ricci, mixed_ricci, 1)
    cubed = matrix_product(squared, mixed_ricci, 1)
    invariants = [
        trunc(sp.trace(mixed_ricci), 1),
        trunc(sp.trace(squared), 1),
        trunc(sp.trace(cubed), 1),
    ]
    jacobian = sp.Matrix([
        [sp.expand(value).coeff(variable) for variable in DX]
        for value in invariants
    ])
    determinant = sp.factor(jacobian.det())
    zero = {X: 0, Y: 0, Z: 0}
    metric_at_point = metric.subs(zero)
    return {
        "invariants_at_point": [str(value.subs(zero)) for value in invariants],
        "jacobian": [[str(jacobian[i, j]) for j in range(3)] for i in range(3)],
        "jacobian_determinant": str(determinant),
        "jacobian_nonzero": determinant != 0,
        "metric_determinant_at_point": str(sp.factor(metric_at_point.det())),
    }


def candidate_rows() -> list[dict[str, str]]:
    rows = read_tsv("CANDIDATE_UNIVERSE.tsv")
    assert [row["candidate_id"] for row in rows] == [f"C{i:02d}" for i in range(1, 19)]
    return rows


def compute(candidate_id: str, point_id: str) -> int:
    source_count = verify_sources()
    rows = {row["candidate_id"]: row for row in candidate_rows()}
    assert candidate_id in rows and candidate_id != "C18"
    assert point_id in POINTS
    result = invariant_jet(rows[candidate_id], POINTS[point_id])
    result.update({
        "schema": "udt-general-screen-invariant-point-1.0",
        "candidate_id": candidate_id,
        "point_id": point_id,
        "point": [str(value) for value in POINTS[point_id]],
        "frozen_sources": source_count,
        "sympy_version": sp.__version__,
    })
    POINT_DIR.mkdir(exist_ok=True)
    destination = POINT_DIR / f"{candidate_id}_{point_id}.json"
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "candidate_id": candidate_id,
        "point_id": point_id,
        "jacobian_nonzero": result["jacobian_nonzero"],
        "output": str(destination.relative_to(ROOT)),
    }, sort_keys=True))
    return 0


def assemble() -> int:
    source_count = verify_sources()
    rows = candidate_rows()
    point_results = []
    candidate_results = []
    for row in rows:
        candidate_id = row["candidate_id"]
        if candidate_id == "C18":
            candidate_results.append({
                "candidate_id": candidate_id,
                "point_certificates": [],
                "jacobian_nonzero_at_any_registered_point": False,
                "curvature_status": "SKIPPED_METRIC_DEGENERATE",
            })
            continue
        local = []
        for point_id in POINTS:
            path = POINT_DIR / f"{candidate_id}_{point_id}.json"
            assert path.is_file(), path
            result = json.loads(path.read_text(encoding="utf-8"))
            assert result["candidate_id"] == candidate_id and result["point_id"] == point_id
            local.append(result)
            point_results.append(result)
        any_nonzero = any(result["jacobian_nonzero"] for result in local)
        if candidate_id == "C14":
            status = "SYMMETRY_ENHANCED_BY_EXACT_GLOBAL_CONTROL"
        elif any_nonzero:
            status = "UNIQUE_KILLING_LINE_CERTIFIED_DENSE_OPEN"
        else:
            status = "INCONCLUSIVE_AT_REGISTERED_POINTS"
        candidate_results.append({
            "candidate_id": candidate_id,
            "point_certificates": [result["point_id"] for result in local],
            "jacobian_nonzero_at_any_registered_point": any_nonzero,
            "curvature_status": status,
        })
    outcome = {
        "schema": "udt-general-screen-invariant-certificate-1.0",
        "status": "PASS_EXACT_POINT_ENSEMBLE",
        "sympy_version": sp.__version__,
        "frozen_sources": source_count,
        "candidate_count": len(rows),
        "nondegenerate_candidate_count": 17,
        "exact_point_certificate_count": len(point_results),
        "candidate_results": candidate_results,
        "universal_full_screen_claimed": False,
        "on_shell_claimed": False,
        "screen_selected": False,
    }
    (HERE / "INVARIANT_CERTIFICATE.json").write_text(
        json.dumps(outcome, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": outcome["status"],
        "candidate_count": len(rows),
        "point_certificates": len(point_results),
    }, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate")
    parser.add_argument("--point", choices=tuple(POINTS))
    parser.add_argument("--assemble", action="store_true")
    arguments = parser.parse_args()
    if arguments.assemble:
        assert arguments.candidate is None and arguments.point is None
        return assemble()
    assert arguments.candidate and arguments.point
    return compute(arguments.candidate, arguments.point)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        (HERE / "INVARIANT_DERIVATION_ERROR.txt").write_text(traceback.format_exc(), encoding="utf-8")
        raise

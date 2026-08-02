#!/usr/bin/env python3
"""Exact curvature-invariant certificate for the preregistered twisted-S3 candidates."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
import subprocess
import traceback
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
X, Y, Z = sp.symbols("X Y Z")
DX = (X, Y, Z)
x, y, z = sp.symbols("x y z")
XYZ = (x, y, z)


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def verify_sources() -> int:
    rows = table("SOURCE_MANIFEST.tsv")
    assert len(rows) == len({row["path"] for row in rows}) == 21
    for row in rows:
        content = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        assert len(content) == int(row["bytes"])
        assert sha256_bytes(content) == row["sha256"]
    return len(rows)


def multiindices(max_degree: int):
    for total in range(max_degree + 1):
        for i in range(total + 1):
            for j in range(total - i + 1):
                yield i, j, total - i - j


def trunc(expression, degree: int):
    expression = sp.expand(expression)
    if expression == 0:
        return sp.S.Zero
    poly = sp.Poly(expression, *DX)
    kept = []
    for powers, coefficient in poly.terms():
        if sum(powers) <= degree:
            kept.append(coefficient * X**powers[0] * Y**powers[1] * Z**powers[2])
    return sp.Add(*kept)


def matrix_trunc(matrix: sp.Matrix, degree: int) -> sp.Matrix:
    return matrix.applyfunc(lambda value: trunc(value, degree))


def matrix_product(left: sp.Matrix, right: sp.Matrix, degree: int) -> sp.Matrix:
    assert left.cols == right.rows
    return sp.Matrix(
        left.rows,
        right.cols,
        lambda i, j: trunc(sum(left[i, k] * right[k, j] for k in range(left.cols)), degree),
    )


def formal_inverse(metric: sp.Matrix, degree: int) -> sp.Matrix:
    zero = {X: 0, Y: 0, Z: 0}
    g0 = metric.subs(zero)
    g0_inverse = g0.inv()
    perturbation = metric - g0
    a_matrix = matrix_product(g0_inverse, perturbation, degree)
    series = sp.eye(metric.rows)
    power = sp.eye(metric.rows)
    sign = -1
    for _ in range(1, degree + 1):
        power = matrix_product(power, a_matrix, degree)
        series = matrix_trunc(series + sign * power, degree)
        sign *= -1
    inverse = matrix_product(series, g0_inverse, degree)
    identity = matrix_product(inverse, metric, degree)
    assert identity == sp.eye(metric.rows)
    return inverse


def scalar_inverse(expression, degree: int):
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


def scalar_power(expression, exponent: int, degree: int):
    if exponent == 0:
        return sp.S.One
    base = expression if exponent > 0 else scalar_inverse(expression, degree)
    result = sp.S.One
    for _ in range(abs(exponent)):
        result = trunc(result * base, degree)
    return result


def coordinate_derivative(expression, coordinate: int):
    if coordinate == 0:
        return sp.S.Zero
    return sp.diff(expression, DX[coordinate - 1])


def metric_jet(profile: str, lam: int, a_value: int, point: tuple[sp.Rational, ...]) -> sp.Matrix:
    shifted = (point[0] + X, point[1] + Y, point[2] + Z)
    sx, sy, sz = shifted
    radius_squared = sx*sx + sy*sy + sz*sz
    denominator = 1 + radius_squared
    denominator_inverse = scalar_inverse(denominator, 4)
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
    if profile == "primary":
        u = trunc(3 + q0*q0 + 2*q1*q1 + 4*q2*q2 + 8*q3*q3, 3)
    elif profile == "constant":
        u = sp.Integer(4)
    elif profile == "repeated":
        u = trunc(3 + q0*q0 + q1*q1 + 4*q2*q2 + 8*q3*q3, 3)
    else:
        raise AssertionError(profile)
    tau = sp.Matrix([1, *(a_value * sigma3)])
    s1 = sp.Matrix([0, *sigma1])
    s2 = sp.Matrix([0, *sigma2])
    s3 = sp.Matrix([0, *sigma3])
    inverse_u = scalar_inverse(u, 3)
    transverse = scalar_power(u, lam, 3)
    metric = matrix_trunc(-inverse_u * (tau * tau.T), 3)
    metric += matrix_trunc(u * (s3 * s3.T), 3)
    metric += matrix_trunc(transverse * (s1 * s1.T + s2 * s2.T), 3)
    metric = matrix_trunc(metric, 3)
    assert metric == metric.T
    return metric


def invariant_jet(profile: str, lam: int, a_value: int, point: tuple[sp.Rational, ...]):
    metric = metric_jet(profile, lam, a_value, point)
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
    jacobian = sp.Matrix([[sp.expand(value).coeff(variable) for variable in DX] for value in invariants])
    determinant = sp.factor(jacobian.det())
    return {
        "invariants_at_point": [str(value.subs({X: 0, Y: 0, Z: 0})) for value in invariants],
        "jacobian": [[str(value) for value in jacobian.row(row)] for row in range(3)],
        "jacobian_determinant": str(determinant),
        "jacobian_nonzero": determinant != 0,
    }


def parse_point(raw: str) -> tuple[sp.Rational, ...]:
    return tuple(sp.Rational(value) for value in raw.strip("()").split(","))


def candidate_parameters(row: dict[str, str]):
    if row["candidate_id"] == "C06":
        profile = "constant"
    elif row["candidate_id"] == "C07":
        profile = "repeated"
    else:
        profile = "primary"
    return profile, int(row["lambda"]), int(row["a_over_R"]), parse_point(row["chart_point"])


def main() -> int:
    source_count = verify_sources()
    candidates = table("CANDIDATE_UNIVERSE.tsv")
    assert [row["candidate_id"] for row in candidates] == [f"C{i:02d}" for i in range(1, 10)]
    assert len(table("GEOMETRIC_GATES.tsv")) == 13
    assert len(table("FALSIFICATION_CONTRACT.tsv")) == 20
    results = []
    for row in candidates:
        profile, lam, a_value, point = candidate_parameters(row)
        result = invariant_jet(profile, lam, a_value, point)
        result.update({
            "candidate_id": row["candidate_id"],
            "profile_class": profile,
            "lambda": lam,
            "a_over_R": a_value,
            "chart_point": row["chart_point"],
            "all_gate_eligible": row["candidate_id"] in {"C01", "C02", "C03", "C04", "C05"},
        })
        results.append(result)
        print(json.dumps(result, sort_keys=True), flush=True)
    eligible_nonzero = [row["candidate_id"] for row in results if row["all_gate_eligible"] and row["jacobian_nonzero"]]
    outcome = {
        "schema": "udt-twisted-s3-all-gate-invariant-certificate-1.0",
        "sympy_version": sp.__version__,
        "frozen_sources": source_count,
        "candidates": len(results),
        "eligible_exact_nonzero_candidates": eligible_nonzero,
        "exact_nonzero_witness_exists": bool(eligible_nonzero),
        "invariant_route_result": "ONE_DIMENSIONAL_FULL_KILLING_ALGEBRA_DERIVED_FOR_EXPLICIT_WITNESS" if eligible_nonzero else "INCONCLUSIVE_NO_REGISTERED_NONZERO_CERTIFICATE",
        "universal_family_claimed": False,
        "on_shell_claimed": False,
        "lambda_selected": False,
        "physics_promoted": False,
        "candidate_results": results,
    }
    (HERE / "INVARIANT_CERTIFICATE.json").write_text(
        json.dumps(outcome, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({key: value for key, value in outcome.items() if key != "candidate_results"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        (HERE / "DERIVATION_ERROR.txt").write_text(traceback.format_exc(), encoding="utf-8")
        raise

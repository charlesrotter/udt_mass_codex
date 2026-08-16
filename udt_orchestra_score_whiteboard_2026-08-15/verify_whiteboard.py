#!/usr/bin/env python3
"""Exact finite-dimensional checks for the orchestra-score whiteboard."""

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent


def manifest_check():
    rows = []
    for line in (HERE / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]:
        if not line.strip():
            continue
        path, expected, _role = line.split("\t")
        payload = (ROOT / path).read_bytes()
        actual = hashlib.sha256(payload).hexdigest()
        rows.append({"path": path, "match": actual == expected})
    return rows


def representation_checks():
    a, b, c, d = sp.symbols("a b c d", real=True)
    screen = sp.Matrix([[a, b], [c, d]])
    quarter_turn = sp.Matrix([[0, -1], [1, 0]])
    reflection = sp.diag(1, -1)

    so2_equations = list(screen * quarter_turn - quarter_turn * screen)
    o2_equations = so2_equations + list(screen * reflection - reflection * screen)
    so2_solution = sp.solve(so2_equations, [a, b, c, d], dict=True)
    o2_solution = sp.solve(o2_equations, [a, b, c, d], dict=True)

    # Off-block invariant intertwiners from/to a screen with a trivial base action.
    x0, x1, x2, x3 = sp.symbols("x0 x1 x2 x3", real=True)
    lower = sp.Matrix([[x0, x1], [x2, x3]])
    lower_solution = sp.solve(
        list(quarter_turn * lower - lower) + list(reflection * lower - lower),
        [x0, x1, x2, x3],
        dict=True,
    )
    upper_solution = sp.solve(
        list(lower * quarter_turn - lower) + list(lower * reflection - lower),
        [x0, x1, x2, x3],
        dict=True,
    )

    alpha, weight, depth, center = sp.symbols(
        "alpha weight depth center", positive=True, real=True
    )
    coeff_a = alpha * sp.exp(-2 * weight * center)
    coeff_b = alpha * sp.exp(2 * weight * center)
    lhs = coeff_a * sp.exp(2 * weight * depth) + coeff_b * sp.exp(
        -2 * weight * depth
    )
    rhs = 2 * alpha * sp.cosh(2 * weight * (depth - center))

    return {
        "so2_centralizer_solution": [str(item) for item in so2_solution],
        "o2_centralizer_solution": [str(item) for item in o2_solution],
        "o2_lower_intertwiner_solution": [str(item) for item in lower_solution],
        "o2_upper_intertwiner_solution": [str(item) for item in upper_solution],
        "paired_weight_identity_zero": sp.simplify(
            lhs - sp.expand_func(rhs.rewrite(sp.exp))
        )
        == 0,
    }


def carried_derivative_check():
    # A nontrivial rational witness for the exact gauge-carry identity.
    h = sp.Matrix(
        [[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 3]]
    )
    dh = sp.Matrix(
        [[0, 2, 0, 0], [0, 0, 0, 0], [0, 0, 1, 1], [0, 0, 0, -1]]
    )
    omega = sp.Matrix(
        [[1, 0, 2, 0], [0, -1, 0, 1], [1, 0, 0, 0], [0, 1, 0, 2]]
    )
    j = sp.Matrix([[1, 0], [0, 1], [1, 2], [2, -1]])
    dj = sp.Matrix([[0, 1], [2, 0], [-1, 1], [1, 1]])

    h_inv = h.inv()
    omega_prime = h * omega * h_inv - dh * h_inv
    j_prime = h * j
    dj_prime = dh * j + h * dj
    carried_original = dj + omega * j
    carried_prime = dj_prime + omega_prime * j_prime
    return sp.simplify(carried_prime - h * carried_original) == sp.zeros(4, 2)


def main():
    manifest_rows = manifest_check()
    result = {
        "all_source_hashes_match": all(row["match"] for row in manifest_rows),
        "source_count": len(manifest_rows),
        "representation": representation_checks(),
        "carried_derivative_covariance": carried_derivative_check(),
    }
    result["all_checks_pass"] = (
        result["all_source_hashes_match"]
        and result["representation"]["paired_weight_identity_zero"]
        and result["carried_derivative_covariance"]
        and result["representation"]["o2_lower_intertwiner_solution"]
        == ["{x0: 0, x1: 0, x2: 0, x3: 0}"]
        and result["representation"]["o2_upper_intertwiner_solution"]
        == ["{x0: 0, x1: 0, x2: 0, x3: 0}"]
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

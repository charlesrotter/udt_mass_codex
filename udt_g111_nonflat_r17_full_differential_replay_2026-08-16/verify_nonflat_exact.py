#!/usr/bin/env python3
"""Independent exact Cartan/exterior-form verification of every G111 geometry component."""

from __future__ import annotations

import hashlib
import json
from itertools import product
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
SIGNATURE = (-1, 1, 1, 1)


def expression_hash(expr: sp.Expr) -> str:
    return hashlib.sha256(sp.srepr(sp.expand(expr)).encode("utf-8")).hexdigest()


def build_from_exterior_forms() -> dict[str, object]:
    phi, lam, a = sp.symbols("phi lambda_R a", real=True)
    p1, p2, p3 = sp.symbols("p1 p2 p3", real=True)
    q11, q21, q31, q22, q32, q33 = sp.symbols("q11 q21 q31 q22 q32 q33", real=True)
    u, v = sp.exp(phi), sp.exp(lam * phi)

    # Coefficients of d(theta^c) in theta^i wedge theta^j, i<j, obtained directly
    # from d sigma1=-2 sigma2^sigma3 and cyclic permutations.
    exterior: list[dict[tuple[int, int], sp.Expr]] = [dict() for _ in range(4)]
    exterior[0] = {(0, 1): p1 / u, (0, 2): p2 / v, (0, 3): p3 / v,
                   (2, 3): -2 * a / (u * v**2)}
    exterior[1] = {(1, 2): -p2 / v, (1, 3): -p3 / v,
                   (2, 3): -2 * u / v**2}
    exterior[2] = {(1, 2): lam * p1 / u, (1, 3): 2 / u,
                   (2, 3): -lam * p3 / v}
    exterior[3] = {(1, 2): -2 / u, (1, 3): lam * p1 / u,
                   (2, 3): lam * p2 / v}

    structure = [[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for output, terms in enumerate(exterior):
        for (left, right), coefficient in terms.items():
            structure[left][right][output] = -coefficient
            structure[right][left][output] = coefficient

    def inner_bracket(left: int, right: int, output: int) -> sp.Expr:
        return SIGNATURE[output] * structure[left][right][output]

    gamma = [[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for direction, vector, output in product(range(4), repeat=3):
        lower = (
            inner_bracket(direction, vector, output)
            - inner_bracket(vector, output, direction)
            + inner_bracket(output, direction, vector)
        ) / 2
        gamma[direction][vector][output] = sp.expand(SIGNATURE[output] * lower)

    q12, q13, q23 = q21 + 2 * p3, q31 - 2 * p2, q32 + 2 * p1
    derivative_data = (
        (0, 0, 0, 0),
        (p1 / u, q11 / u, q12 / u, q13 / u),
        (p2 / v, q21 / v, q22 / v, q23 / v),
        (p3 / v, q31 / v, q32 / v, q33 / v),
    )
    variables = (phi, p1, p2, p3)

    def directional(expr: sp.Expr, direction: int) -> sp.Expr:
        return sum(
            derivative_data[direction][index] * sp.diff(expr, variable)
            for index, variable in enumerate(variables)
        )

    riemann_up = [[[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for left, right, vector, output in product(range(4), repeat=4):
        value = directional(gamma[right][vector][output], left)
        value -= directional(gamma[left][vector][output], right)
        value += sum(gamma[right][vector][middle] * gamma[left][middle][output] for middle in range(4))
        value -= sum(gamma[left][vector][middle] * gamma[right][middle][output] for middle in range(4))
        value -= sum(structure[left][right][middle] * gamma[middle][vector][output] for middle in range(4))
        riemann_up[left][right][vector][output] = sp.expand(value)
    riemann = [[[[SIGNATURE[output] * riemann_up[i][j][k][output] for output in range(4)]
                 for k in range(4)] for j in range(4)] for i in range(4)]
    return {"brackets": structure, "connection": gamma, "riemann": riemann}


def flattened(groups: dict[str, object], name: str) -> list[sp.Expr]:
    data = groups[name]
    if name == "riemann":
        return [data[i][j][k][l] for i, j, k, l in product(range(4), repeat=4)]
    return [data[i][j][k] for i, j, k in product(range(4), repeat=3)]


def main() -> None:
    saved = json.loads((HERE / "EXACT_COMPONENT_HASHES.json").read_text())
    geometry = build_from_exterior_forms()
    comparisons: dict[str, dict[str, object]] = {}
    for name in ("brackets", "connection", "riemann"):
        hashes = [expression_hash(expr) for expr in flattened(geometry, name)]
        expected = saved["groups"][name]["hashes"]
        comparisons[name] = {
            "component_count": len(hashes),
            "expected_count": saved["groups"][name]["component_count"],
            "all_component_hashes_equal": hashes == expected,
            "mismatch_indices": [index for index, pair in enumerate(zip(hashes, expected)) if pair[0] != pair[1]],
        }
    checks = {
        "64_bracket_components_exact": comparisons["brackets"]["component_count"] == 64 and comparisons["brackets"]["all_component_hashes_equal"],
        "64_connection_components_exact": comparisons["connection"]["component_count"] == 64 and comparisons["connection"]["all_component_hashes_equal"],
        "256_riemann_components_exact": comparisons["riemann"]["component_count"] == 256 and comparisons["riemann"]["all_component_hashes_equal"],
        "independent_exterior_form_route": True,
        "does_not_import_production": True,
    }
    result = {
        "schema": "UDT_G111_INDEPENDENT_EXACT_CARTAN_V1",
        "method": "direct exterior derivatives of the R17 coframe plus exact Cartan/Koszul curvature; no production import",
        "comparisons": comparisons,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }
    (HERE / "INDEPENDENT_EXACT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()

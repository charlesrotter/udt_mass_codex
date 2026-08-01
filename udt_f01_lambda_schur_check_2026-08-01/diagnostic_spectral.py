#!/usr/bin/env python3
"""High-precision spectral diagnostic; corroboration only, never certification."""

from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

import mpmath as mp
import sympy as sp


OUT = Path(__file__).resolve().parent
mp.mp.dps = 100


def root_equation(s: mp.mpf) -> mp.mpf:
    u = 2 * s - 1
    return (
        u * mp.log((u * u + 1) / 2)
        - 2 * u
        + 2 * mp.atan(u)
        - 2
        + mp.pi / 2
    ) / s


def poly_eval(coeff: list[mp.mpf], x: mp.mpf) -> mp.mpf:
    value = mp.mpf("0")
    for c in reversed(coeff):
        value = value * x + c
    return value


def derivative(coeff: list[mp.mpf]) -> list[mp.mpf]:
    return [mp.mpf(k) * coeff[k] for k in range(1, len(coeff))] or [mp.mpf("0")]


def multiply(a: list[mp.mpf], b: list[mp.mpf]) -> list[mp.mpf]:
    result = [mp.mpf("0")] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            result[i + j] += ai * bj
    return result


def p_basis(k: int, right: str) -> tuple[list[mp.mpf], list[mp.mpf]]:
    monomial = [mp.mpf("0")] * k + [mp.mpf("1")]
    factor = [mp.mpf("1"), mp.mpf("1")] if right == "FREE" else [mp.mpf("1"), mp.mpf("0"), mp.mpf("-1")]
    coeff = multiply(factor, monomial)
    return coeff, derivative(coeff)


def fprime_basis(k: int, trace: str) -> list[mp.mpf]:
    if trace == "FREE":
        return [mp.mpf("0")] * k + [mp.mpf("1")]
    # derivative of (1-x^2)x^k; its integral is exactly zero.
    monomial = [mp.mpf("0")] * k + [mp.mpf("1")]
    return derivative(multiply([mp.mpf("1"), mp.mpf("0"), mp.mpf("-1")], monomial))


def inertia(values: mp.matrix) -> tuple[int, int, int]:
    scale = max(abs(v) for v in values)
    tol = scale * mp.mpf("1e-70")
    neg = sum(1 for v in values if v < -tol)
    zero = sum(1 for v in values if abs(v) <= tol)
    pos = len(values) - neg - zero
    return neg, zero, pos


def assemble(s: mp.mpf, n: int, right: str, ftrace: str) -> dict[str, object]:
    # Registered P1 representative used only after the sign-invariant positive
    # scaling is separated analytically: a_F=2, a_F'=2, g_p=g_f=1.
    a = mp.mpf("2")
    ap = mp.mpf("2")
    e0 = s * s / (a * a)
    c = mp.sqrt(e0)
    qn = max(80, 6 * n)
    nodes, weights = mp.gauss_quadrature(qn, "legendre")
    pbasis = [p_basis(k, right) for k in range(n)]
    fbasis = [fprime_basis(k, ftrace) for k in range(n)]
    dim_field = 2 * n
    matrix = mp.matrix(dim_field + 1, dim_field + 1)

    def component(index: int, x: mp.mpf) -> tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
        if index < n:
            p, dp = pbasis[index]
            return poly_eval(p, x), poly_eval(dp, x), mp.mpf("0"), mp.mpf("0")
        if index < dim_field:
            return mp.mpf("0"), mp.mpf("0"), poly_eval(fbasis[index - n], x), mp.mpf("0")
        return mp.mpf("0"), mp.mpf("0"), mp.mpf("0"), mp.mpf("1")

    for qindex in range(qn):
        x = nodes[qindex]
        weight = weights[qindex]
        w = (s * s / 2) * x * x + (s * s - s) * x + 1 + s * s / 2 - s
        wp = s * s * x + s * s - s
        pbar = mp.log(w) / a
        pbarp = wp / (a * w)
        fbarp = c / w
        lt = pbarp * pbarp / 2 + fbarp * fbarp / 2
        comps = [component(i, x) for i in range(dim_field + 1)]
        for i in range(dim_field + 1):
            pi, dpi, fi, mui = comps[i]
            for j in range(i, dim_field + 1):
                pj, dpj, fj, muj = comps[j]
                value = (
                    w * (dpi * dpj + fi * fj)
                    + a * w * (pi * (pbarp * dpj + fbarp * fj) + pj * (pbarp * dpi + fbarp * fi))
                    + a * a * lt * w * pi * pj
                    + ap
                    * (
                        mui * (pj * w * lt * (1 + a * pbar) + pbar * w * (pbarp * dpj + fbarp * fj))
                        + muj * (pi * w * lt * (1 + a * pbar) + pbar * w * (pbarp * dpi + fbarp * fi))
                    )
                    + ap * ap * pbar * pbar * w * lt * mui * muj
                )
                matrix[i, j] += weight * value
                if i != j:
                    matrix[j, i] += weight * value

    field = matrix[:dim_field, :dim_field]
    cross = matrix[:dim_field, dim_field]
    diagonal = matrix[dim_field, dim_field]
    solution = mp.lu_solve(field, cross)
    schur = diagonal - (cross.T * solution)[0]
    field_eigs = mp.eigsy(field, eigvals_only=True)
    joint_eigs = mp.eigsy(matrix, eigvals_only=True)
    return {
        "n": n,
        "right_trace": right,
        "fh_trace": ftrace,
        "quadrature_nodes": qn,
        "schur": mp.nstr(schur, 80),
        "field_inertia": list(inertia(field_eigs)),
        "joint_inertia": list(inertia(joint_eigs)),
        "field_smallest": mp.nstr(field_eigs[0], 40),
        "joint_smallest_two": [mp.nstr(joint_eigs[k], 40) for k in range(min(2, len(joint_eigs)))],
        "linear_solve_residual_max": mp.nstr(max(abs(v) for v in field * solution - cross), 20),
        "mu_one_minimizer_coefficients": [mp.nstr(-v, 50) for v in solution],
        "mu_one_diagonal": mp.nstr(diagonal, 50),
    }


def main() -> None:
    root = mp.findroot(root_equation, (mp.mpf("1.6"), mp.mpf("1.8")))
    rows = []
    for n in (4, 6, 8, 10, 12, 16):
        for right in ("DIRICHLET", "FREE"):
            for ftrace in ("FREE", "ODD_ZERO"):
                rows.append(assemble(root, n, right, ftrace))
                print(json.dumps(rows[-1], sort_keys=True), flush=True)
    result = {
        "status": "CORROBORATION_ONLY",
        "root": mp.nstr(root, 90),
        "root_residual": mp.nstr(root_equation(root), 30),
        "precision_decimal_digits": mp.mp.dps,
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "mpmath": mp.__version__,
        "rows": rows,
        "conclusion_ceiling": "spectral diagnostic only; no sign certification without independent interval/error enclosure",
    }
    (OUT / "DIAGNOSTIC_SPECTRAL.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

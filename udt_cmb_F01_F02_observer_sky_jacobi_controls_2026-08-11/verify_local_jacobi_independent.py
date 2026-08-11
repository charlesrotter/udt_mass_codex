#!/usr/bin/env python3
"""Independent exact check using the lowered-metric Riemann formula.

This script does not import the production derivation.  In particular, it does not differentiate
second-kind Christoffel symbols; it constructs the fully lowered Riemann tensor directly from
second metric derivatives and quadratic connection terms.  F01 is rebuilt as its own metric.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent


def lowered_riemann(g: sp.Matrix, coords: tuple[sp.Symbol, ...]):
    gi = sp.simplify(g.inv())
    dim = len(coords)
    Gamma = [[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                Gamma[a][b][c] = sp.Rational(1, 2) * sum(
                    gi[a, e]
                    * (
                        sp.diff(g[e, c], coords[b])
                        + sp.diff(g[e, b], coords[c])
                        - sp.diff(g[b, c], coords[e])
                    )
                    for e in range(dim)
                )

    # R_abcd = g_ae R^e_bcd for the convention declared in PREREGISTRATION.md.
    def R(a: int, b: int, c: int, d: int) -> sp.Expr:
        second = sp.Rational(1, 2) * (
            sp.diff(g[a, d], coords[b], coords[c])
            + sp.diff(g[b, c], coords[a], coords[d])
            - sp.diff(g[a, c], coords[b], coords[d])
            - sp.diff(g[b, d], coords[a], coords[c])
        )
        quadratic = sum(
            g[e, f]
            * (
                Gamma[e][b][c] * Gamma[f][a][d]
                - Gamma[e][b][d] * Gamma[f][a][c]
            )
            for e in range(dim)
            for f in range(dim)
        )
        return sp.factor(second + quadratic)

    return R


def screen_tidal(g: sp.Matrix, coords, frame, theta_value) -> sp.Matrix:
    u, n, e_th, e_ps = frame
    k = u + n
    R = lowered_riemann(g, coords)
    out = sp.zeros(2)
    for aa, ea in enumerate((e_th, e_ps)):
        for bb, eb in enumerate((e_th, e_ps)):
            value = sp.S.Zero
            for a in range(4):
                if ea[a] == 0:
                    continue
                for b in range(4):
                    if k[b] == 0:
                        continue
                    for c in range(4):
                        if eb[c] == 0:
                            continue
                        for d in range(4):
                            if k[d] == 0:
                                continue
                            value += ea[a] * k[b] * eb[c] * k[d] * R(a, b, c, d)
            out[aa, bb] = sp.factor(value.subs(coords[2], theta_value))
    return out


def main() -> None:
    t, r, th, ps = sp.symbols("t r theta psi", real=True)
    coords = (t, r, th, ps)
    A = sp.Function("A")(r)
    h = sp.Function("h")(r)
    st = sp.sin(th)

    g2 = sp.zeros(4)
    g2[0, 0] = -A
    g2[1, 1] = 1 / A
    g2[2, 2] = r**2
    g2[3, 3] = r**2 * st**2
    g2[0, 3] = g2[3, 0] = h * st**2
    D = A * r**2 + h**2 * st**2
    frame2 = (
        sp.Matrix([1 / sp.sqrt(A), 0, 0, 0]),
        sp.Matrix([0, sp.sqrt(A), 0, 0]),
        sp.Matrix([0, 0, 1 / r, 0]),
        sp.Matrix(
            [h * st / (sp.sqrt(A) * sp.sqrt(D)), 0, 0, sp.sqrt(A) / (st * sp.sqrt(D))]
        ),
    )
    exact2 = screen_tidal(g2, coords, frame2, sp.pi / 2)

    # Rebuild F01 independently rather than obtaining it by a substitution in F02.
    g1 = sp.diag(-A, 1 / A, r**2, r**2 * st**2)
    frame1 = (
        sp.Matrix([1 / sp.sqrt(A), 0, 0, 0]),
        sp.Matrix([0, sp.sqrt(A), 0, 0]),
        sp.Matrix([0, 0, 1 / r, 0]),
        sp.Matrix([0, 0, 0, 1 / (r * st)]),
    )
    exact1 = screen_tidal(g1, coords, frame1, sp.pi / 2)

    A0, A1, A2, h0, h1, h2 = sp.symbols("A0 A1 A2 h0 h1 h2", real=True)
    jets = {
        A: A0,
        sp.diff(A, r): A1,
        sp.diff(A, (r, 2)): A2,
        h: h0,
        sp.diff(h, r): h1,
        sp.diff(h, (r, 2)): h2,
    }
    exact2 = exact2.applyfunc(lambda x: sp.factor(x.subs(jets)))
    exact1 = exact1.applyfunc(lambda x: sp.factor(x.subs(jets)))

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    locals_map = {"A0": A0, "A1": A1, "A2": A2, "h0": h0, "h1": h1, "h2": h2, "r": r}
    prod2 = sp.Matrix(
        [[sp.sympify(x, locals=locals_map) for x in row] for row in production["F02_tidal_matrix_equator"]]
    )
    prod1 = sp.Matrix(
        [[sp.sympify(x, locals=locals_map) for x in row] for row in production["F01_induced_limit"]]
    )

    checks = {
        "independent_F02_exact_match": all(
            sp.factor(exact2[i, j] - prod2[i, j]) == 0 for i in range(2) for j in range(2)
        ),
        "independent_F01_exact_match": all(
            sp.factor(exact1[i, j] - prod1[i, j]) == 0 for i in range(2) for j in range(2)
        ),
        "standalone_F01_zero": exact1 == sp.zeros(2),
        "F02_screen_symmetry": sp.factor(exact2[0, 1] - exact2[1, 0]) == 0,
        "F02_h_zero_limit": exact2.subs({h0: 0, h1: 0, h2: 0}) == exact1,
    }

    samples = [
        {r: sp.Rational(13, 10), A0: sp.Rational(9, 10), A1: sp.Rational(-1, 10), A2: sp.Rational(3, 50), h0: sp.Rational(1, 5), h1: sp.Rational(3, 10), h2: sp.Rational(-1, 20)},
        {r: sp.Rational(4, 5), A0: sp.Rational(6, 5), A1: sp.Rational(1, 20), A2: sp.Rational(-1, 10), h0: sp.Rational(-1, 8), h1: sp.Rational(1, 7), h2: sp.Rational(1, 9)},
        {r: sp.Rational(3, 2), A0: sp.Rational(1, 1), A1: 0, A2: 0, h0: sp.Rational(3, 20), h1: sp.Rational(1, 5), h2: sp.Rational(2, 15)},
    ]
    sample_values = []
    for sample in samples:
        lhs = exact2.subs(sample)
        rhs = prod2.subs(sample)
        sample_values.append(
            {
                "exact_match": lhs == rhs,
                "tidal": [[str(sp.factor(lhs[i, j])) for j in range(2)] for i in range(2)],
            }
        )
    checks["three_exact_rational_controls"] = all(x["exact_match"] for x in sample_values)

    result = {
        "method": "direct fully-lowered Riemann from metric second derivatives; standalone F01 rebuild",
        "checks": checks,
        "independent_F02": [[str(x) for x in row] for row in exact2.tolist()],
        "independent_F01": [[str(x) for x in row] for row in exact1.tolist()],
        "samples": sample_values,
        "passed": sum(bool(v) for v in checks.values()),
        "total": len(checks),
    }
    (ROOT / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

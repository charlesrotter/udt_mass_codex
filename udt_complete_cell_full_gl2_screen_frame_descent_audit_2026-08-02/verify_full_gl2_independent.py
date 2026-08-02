#!/usr/bin/env python3
"""Independent exterior-form verification of the full-screen curvature result.

Unlike production's direct frame-commutator curvature, this script solves the
Cartan torsion/metric system as a linear system and computes Omega=domega+omega^2.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ETA = (-1, 1, 1, 1)
PAIRS = tuple((i, j) for i in range(4) for j in range(i + 1, 4))


def add(*forms):
    result = {}
    for form in forms:
        for key, value in form.items():
            result[key] = sp.expand(result.get(key, 0) + value)
    return {key: value for key, value in result.items() if value != 0}


def scale(value, form):
    return {key: sp.expand(value * coefficient) for key, coefficient in form.items()}


def wedge(left, right):
    result = {}
    for a, ca in left.items():
        for b, cb in right.items():
            if set(a) & set(b):
                continue
            sign = (-1) ** sum(i > j for i in a for j in b)
            key = tuple(sorted(a + b))
            result[key] = sp.expand(result.get(key, 0) + sign * ca * cb)
    return {key: value for key, value in result.items() if value != 0}


def main() -> int:
    p1, p2, p3, t0, t1 = sp.symbols("p1 p2 p3 t0 t1", real=True)
    a, r, h1, h2, u, v = sp.symbols("a r h1 h2 u v", real=True)
    sigma2, sigma3 = sp.symbols("sigma2 sigma3", real=True)
    coeffs = (p1, p2, p3, t0, t1, a, r, h1, h2, u, v)
    p = (p1, p2, p3)
    e = tuple({(i,): sp.Integer(1)} for i in range(4))
    dphi = add(scale(p1, e[1]), scale(p2, e[2]), scale(p3, e[3]))
    de = (
        add(scale(-1, wedge(dphi, e[0])), scale(t0, wedge(e[2], e[3]))),
        add(wedge(dphi, e[1]), scale(t1, wedge(e[2], e[3]))),
        add(scale(a+h1, wedge(e[1], e[2])), scale(h2-r, wedge(e[1], e[3])), scale(u, wedge(e[2], e[3]))),
        add(scale(h2+r, wedge(e[1], e[2])), scale(a-h1, wedge(e[1], e[3])), scale(v, wedge(e[2], e[3]))),
    )
    structure = {}
    for upper, form in enumerate(de):
        for (i, j), value in form.items():
            structure[(upper, i, j)] = -value
            structure[(upper, j, i)] = value
    derivatives = {(i, q): sp.Symbol(f"E{i}_{q}", real=True) for i in (1, 2, 3) for q in coeffs}
    sigma = (2*a, sigma2, sigma3)
    substitutions = {}
    for i in (1, 2, 3):
        substitutions[derivatives[(i, t1)]] = t1*(p[i-1]-sigma[i-1])
        substitutions[derivatives[(i, t0)]] = -t0*(p[i-1]+sigma[i-1])

    def E(i, expression):
        if i == 0:
            return sp.Integer(0)
        return sp.expand(sum(sp.diff(expression, q)*derivatives[(i, q)] for q in coeffs).subs(substitutions))

    # Solve the connection from metric compatibility plus torsion, without the
    # production Koszul formula.
    unknowns = {}
    variables = []
    for direction in range(4):
        for lower_a, lower_b in PAIRS:
            symbol = sp.Symbol(f"w{lower_a}{lower_b}_{direction}")
            unknowns[(lower_a, lower_b, direction)] = symbol
            variables.append(symbol)

    def omega_upper(a0, b0, direction):
        if a0 == b0:
            return sp.Integer(0)
        if a0 < b0:
            lower = unknowns[(a0, b0, direction)]
        else:
            lower = -unknowns[(b0, a0, direction)]
        return ETA[a0] * lower

    equations = []
    for upper in range(4):
        for i, j in PAIRS:
            equations.append(sp.Eq(
                omega_upper(upper, j, i) - omega_upper(upper, i, j),
                structure.get((upper, i, j), 0),
            ))
    solution_set = sp.linsolve([eq.lhs-eq.rhs for eq in equations], variables)
    solutions = list(solution_set)
    assert len(solutions) == 1 and len(solutions[0]) == len(variables)
    assert not any(value.free_symbols & set(variables) for value in solutions[0])
    solved = dict(zip(variables, solutions[0]))

    omega = {}
    for upper in range(4):
        for incoming in range(4):
            omega[(upper, incoming)] = {
                (direction,): sp.factor(omega_upper(upper, incoming, direction).subs(solved))
                for direction in range(4)
                if sp.factor(omega_upper(upper, incoming, direction).subs(solved)) != 0
            }

    def d_basis(index):
        return de[index]

    def exterior(form):
        pieces = []
        for (basis,), coefficient in form.items():
            df = add(*(scale(E(i, coefficient), e[i]) for i in (1, 2, 3)))
            pieces.append(wedge(df, e[basis]))
            pieces.append(scale(coefficient, d_basis(basis)))
        return add(*pieces)

    curvature_forms = {}
    for upper in range(4):
        for incoming in range(4):
            curvature_forms[(upper, incoming)] = add(
                exterior(omega[(upper, incoming)]),
                *(wedge(omega[(upper, middle)], omega[(middle, incoming)]) for middle in range(4)),
            )

    with (HERE / "FULL_CURVATURE_CENSUS.tsv").open(newline="", encoding="utf-8") as handle:
        expected_rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(expected_rows) == 36
    matched = 0
    for row in expected_rows:
        a0, b0 = map(int, row["curvature_pair"].removeprefix("Omega"))
        i, j = map(int, row["two_form_leg"])
        actual = sp.factor(ETA[a0] * curvature_forms[(a0, b0)].get((i, j), 0))
        expected = sp.sympify(row["expression"], locals={str(q): q for q in coeffs} | {
            str(value): value for value in derivatives.values()
        } | {"sigma2": sigma2, "sigma3": sigma3})
        assert sp.simplify(actual-expected) == 0, (row["curvature_pair"], row["two_form_leg"])
        matched += 1

    def r_upper(upper, incoming, left, right):
        if left == right:
            return sp.Integer(0)
        leg = (left, right) if left < right else (right, left)
        sign = 1 if left < right else -1
        return sign * curvature_forms[(upper, incoming)].get(leg, 0)

    ricci = sp.Matrix(4, 4, lambda incoming, right: sp.factor(sum(
        r_upper(upper, incoming, upper, right) for upper in range(4)
    )))
    independent_scalar = sp.factor(sum(ETA[index] * ricci[index, index] for index in range(4)))
    production_result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    expected_scalar = sp.sympify(production_result["scalar_curvature"], locals={str(q): q for q in coeffs} | {
        str(value): value for value in derivatives.values()
    } | {"sigma2": sigma2, "sigma3": sigma3})
    assert sp.simplify(independent_scalar - expected_scalar) == 0

    # Five independent closure equations make the first Bianchi forms vanish.
    closure_subs = {
        derivatives[(1, p2)]: derivatives[(2, p1)]-a*p2-h1*p2-h2*p3+p1*p2-p3*r,
        derivatives[(1, p3)]: derivatives[(3, p1)]-a*p3+h1*p3-h2*p2+p1*p3+p2*r,
        derivatives[(2, p3)]: derivatives[(3, p2)]-p1*t1-p2*u-p3*v,
        derivatives[(1, u)]: derivatives[(2, h2)]-derivatives[(2, r)]-derivatives[(3, a)]-derivatives[(3, h1)]-a*p3-a*u-h1*p3+h1*u+h2*p2+h2*v-p2*r-r*v,
        derivatives[(1, v)]: derivatives[(2, a)]-derivatives[(2, h1)]-derivatives[(3, h2)]-derivatives[(3, r)]+a*p2-a*v-h1*p2-h1*v-h2*p3+h2*u-p3*r+r*u,
    }
    bianchi_checked = 0
    for upper in range(4):
        total = add(*(wedge(curvature_forms[(upper, incoming)], e[incoming]) for incoming in range(4)))
        for expression in total.values():
            assert sp.simplify(sp.expand(expression).subs(closure_subs)) == 0
            bianchi_checked += 1

    # Independent finite transformations and countertransformations.
    beta, g = sp.symbols("beta g", real=True)
    B = sp.Matrix([[sp.cosh(beta), sp.sinh(beta)], [sp.sinh(beta), sp.cosh(beta)]])
    q = sp.Matrix([t0, t1])
    eta2 = sp.diag(-1, 1)
    q2 = sp.expand((q.T*eta2*q)[0])
    assert sp.simplify((B*q).T*eta2*(B*q))[0] == q2
    assert sp.simplify((t1-g)**2-t0**2-q2) != 0
    assert sp.simplify(t1**2-(t0-g)**2-q2) != 0

    result = {
        "schema": "udt-complete-cell-full-gl2-independent-1.0",
        "status": "PASS_VERIFIED_WITH_CAVEATS_NO_FRESH_BLIND_REVIEW",
        "method": "LINEAR_CARTAN_CONNECTION_PLUS_EXTERIOR_CURVATURE",
        "connection_unknowns_solved": len(variables),
        "curvature_rows_matched": matched,
        "scalar_curvature_matched_by_ricci_contraction": True,
        "independent_closure_equations": len(closure_subs),
        "bianchi_components_checked": bianchi_checked,
        "pair_boost_q_squared_invariant": True,
        "pair_screen_spatial_mix_changes_q_squared": True,
        "pair_screen_lorentz_mix_changes_q_squared": True,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

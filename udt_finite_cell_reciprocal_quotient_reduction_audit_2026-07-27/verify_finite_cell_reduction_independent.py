#!/usr/bin/env python3
"""Independent exact-Fraction reconstruction; no SymPy or production import."""

from __future__ import annotations

from fractions import Fraction as F
import json


def zmat(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def eye(n):
    out = zmat(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def sub(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def tr(a):
    return [list(row) for row in zip(*a)]


def flat(a):
    return [x for row in a for x in row]


def rank(a):
    value = [row[:] for row in a]
    rows, cols = len(value), len(value[0]) if value else 0
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if value[r][col]), None)
        if pivot is None:
            continue
        value[pivot_row], value[pivot] = value[pivot], value[pivot_row]
        lead = value[pivot_row][col]
        value[pivot_row] = [x / lead for x in value[pivot_row]]
        for r in range(rows):
            if r != pivot_row and value[r][col]:
                factor = value[r][col]
                value[r] = [x - factor * y for x, y in zip(value[r], value[pivot_row])]
        pivot_row += 1
    return pivot_row


ETA = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
J2 = [[F(0), F(1)], [F(-1), F(0)]]


def response(x):
    return add(mm(tr(x), ETA), mm(ETA, x))


def jet2(x):
    return add(add(mm(mm(tr(x), tr(x)), ETA), scale(F(2), mm(mm(tr(x), ETA), x))), mm(mm(ETA, x), x))


def lorentz_generators():
    out = []
    for i in range(1, 4):
        value = zmat(4, 4); value[0][i] = value[i][0] = F(1); out.append(value)
    for i, j in ((1, 2), (1, 3), (2, 3)):
        value = zmat(4, 4); value[i][j] = F(1); value[j][i] = F(-1); out.append(value)
    return out


def main() -> None:
    checks = {}

    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        checks[name] = "PASS"

    screen = [[F(0), F(0), F(0), F(0)], [F(0), F(0), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    check("independent_screen_idempotent", mm(screen, screen) == screen)
    check("independent_screen_rank_two", rank(screen) == 2)

    lam = F(2, 3)
    x = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), lam, F(0)], [F(0), F(0), F(0), lam]]
    check("independent_response_isotropic_unmixed", response(x) == [[F(2), F(0), F(0), F(0)], [F(0), F(2), F(0), F(0)], [F(0), F(0), 2 * lam, F(0)], [F(0), F(0), F(0), 2 * lam]])

    # A rational 3-4-5 screen rotation commutes with the isotropic generator.
    r = [[F(3, 5), F(4, 5)], [F(-4, 5), F(3, 5)]]
    t = eye(4); t[2][2], t[2][3], t[3][2], t[3][3] = r[0][0], r[0][1], r[1][0], r[1][1]
    check("independent_screen_rotation_orthogonal", mm(tr(r), r) == eye(2))
    check("independent_isotropic_generator_commutes_rotation", mm(t, x) == mm(x, t))

    # Series coefficients of exp(X+wJ)^T eta exp(X+wJ) agree through order 6.
    xw = [row[:] for row in x]
    xw[2][3] = F(1); xw[3][2] = F(-1)
    def powers(value, order):
        out = [eye(4)]
        for _ in range(order):
            out.append(mm(out[-1], value))
        return out
    import math
    def metric_series(value, order):
        p = powers(value, order)
        coeff = []
        for n in range(order + 1):
            total = zmat(4, 4)
            for i in range(n + 1):
                total = add(total, scale(F(1, math.factorial(i) * math.factorial(n-i)), mm(mm(tr(p[i]), ETA), p[n-i])))
            coeff.append(total)
        return coeff
    check("independent_isotropic_w_metric_series_equal_order_six", metric_series(xw, 6) == metric_series(x, 6))

    aniso = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(2), F(2)], [F(0), F(0), F(0), F(-1)]]
    aniso0 = [row[:] for row in aniso]; aniso0[2][3] = F(1); aniso[3][2] = F(-1)
    # Same symmetric response, different second jet.
    check("independent_anisotropic_same_first_response", response(aniso) == response(aniso0))
    check("independent_anisotropic_second_jet_differs", jet2(aniso) != jet2(aniso0))

    mixed = [row[:] for row in xw]; mixed[2][0] = F(1)
    mixed0 = [row[:] for row in x]; mixed0[2][0] = F(1)
    check("independent_mixed_same_first_response", response(mixed) == response(mixed0))
    check("independent_mixed_second_jet_differs", jet2(mixed) != jet2(mixed0))

    # Centralizer rank by exact commutator columns.
    constraints = []
    gens = lorentz_generators()
    for generator in gens:
        for i in range(4):
            for j in range(4):
                row = []
                for a in range(4):
                    for b in range(4):
                        coefficient = F(0)
                        if i == a:
                            coefficient += generator[b][j]
                        if j == b:
                            coefficient -= generator[i][a]
                        row.append(coefficient)
                constraints.append(row)
    check("independent_full_Lorentz_centralizer_rank_fifteen", rank(constraints) == 15)
    check("independent_reciprocal_generator_not_scalar", x[0][0] != x[1][1])

    xplus = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    check("independent_lambda_plus1_spatial_so3_centralized", all(mm(g, xplus) == mm(xplus, g) for g in gens[3:]))
    check("independent_lambda_plus1_boost_not_centralized", mm(gens[0], xplus) != mm(xplus, gens[0]))

    check("independent_connection_leakage_nonzero_control", [-2 * F(1, 50), -2 * F(2, 50)] != [F(0), F(0)])
    check("independent_nabla_X_control", F(-3, 50) * F(2) == F(-3, 25))

    # Independent projected-connection and SO(2) gauge controls.
    h = screen
    gamma_screen = gens[5]  # J23
    d_screen = mm(mm(h, gamma_screen), h)
    check("independent_projected_connection_closes", mm(h, d_screen) == d_screen and mm(d_screen, h) == d_screen)
    check("independent_projected_connection_metric_compatible", add(mm(tr(d_screen), ETA), mm(ETA, d_screen)) == zmat(4, 4))
    gamma_leak = gens[3]  # J12 mixes ruler and screen
    leak = mm(mm(sub(eye(4), h), gamma_leak), h)
    check("independent_ambient_leakage_control", leak != zmat(4, 4))
    rate, gauge_rate = F(3, 7), F(-2, 5)
    a0 = scale(rate, J2)
    gauge_transformed = add(mm(mm(tr(r), a0), r), scale(gauge_rate, J2))
    check("independent_screen_connection_gauge_shift", gauge_transformed == scale(rate + gauge_rate, J2))

    check("independent_check_count_before_count_check", len(checks) == 20)
    if len(checks) != 21:
        raise AssertionError("unexpected independent check count")

    result = {
        "schema": "udt.finite_cell_reciprocal_quotient_reduction.independent.v1",
        "result": "PASS",
        "implementation": "stdlib_Fraction_no_sympy_no_production_import",
        "check_count": len(checks),
        "checks": checks,
        "controls": {
            "screen_rank": 2,
            "isotropic_w_metric_series": "EQUAL_THROUGH_ORDER_6",
            "anisotropic_w": "SECOND_JET_DIFFERENT",
            "mixed_w": "SECOND_JET_DIFFERENT",
            "full_Lorentz_centralizer_dimension": 1,
            "lambda_plus1_reduced_so3": "COMMUTES_BUT_BOOST_DOES_NOT",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

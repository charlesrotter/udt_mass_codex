#!/usr/bin/env python3
"""Independent exact-Fraction verification of finite quotient-lift controls.

This module does not import SymPy, the production derivation, or its output.
"""

from __future__ import annotations

from fractions import Fraction as F
import json
import math


def zmat(rows: int, cols: int):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def eye(n: int):
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
        pivot = next((r for r in range(pivot_row, rows) if value[r][col] != 0), None)
        if pivot is None:
            continue
        value[pivot_row], value[pivot] = value[pivot], value[pivot_row]
        lead = value[pivot_row][col]
        value[pivot_row] = [x / lead for x in value[pivot_row]]
        for r in range(rows):
            if r != pivot_row and value[r][col] != 0:
                factor = value[r][col]
                value[r] = [x - factor * y for x, y in zip(value[r], value[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


ETA = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
H = [[F(-1), F(0)], [F(0), F(1)]]
J = [[F(0), F(1)], [F(-1), F(0)]]


def block_x(c, k):
    out = zmat(4, 4)
    for i in range(2):
        for j in range(2):
            out[i][j] = H[i][j]
            out[i + 2][j] = c[i][j]
            out[i + 2][j + 2] = k[i][j]
    return out


def response(x):
    return add(mm(mm(tr(x), ETA), eye(4)), mm(ETA, x))


def jet2(x):
    return add(add(mm(mm(mm(tr(x), tr(x)), ETA), eye(4)), scale(F(2), mm(mm(tr(x), ETA), x))), mm(mm(ETA, x), x))


def exp_series(x, order):
    coeffs = [eye(4)]
    power = eye(4)
    for n in range(1, order + 1):
        power = mm(power, x)
        coeffs.append(scale(F(1, math.factorial(n)), power))
    return coeffs


def metric_series(x, order):
    e = exp_series(x, order)
    coeffs = []
    for n in range(order + 1):
        total = zmat(4, 4)
        for i in range(n + 1):
            total = add(total, mm(mm(tr(e[i]), ETA), e[n - i]))
        coeffs.append(total)
    return coeffs


def rrot(t):
    den = F(1) + t * t
    return [[(F(1) - t * t) / den, -F(2) * t / den], [F(2) * t / den, (F(1) - t * t) / den]]


def bdiag(a, b):
    out = zmat(len(a) + len(b), len(a[0]) + len(b[0]))
    for i in range(len(a)):
        for j in range(len(a[0])):
            out[i][j] = a[i][j]
    for i in range(len(b)):
        for j in range(len(b[0])):
            out[i + len(a)][j + len(a[0])] = b[i][j]
    return out


def main() -> None:
    checks = {}

    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        checks[name] = "PASS"

    # Eight independent quotient constraints set the base block and upper right.
    quotient_rows = zmat(8, 16)
    row = 0
    for i in range(2):
        for j in range(4):
            quotient_rows[row][4 * i + j] = F(1)
            row += 1
    check("independent_quotient_constraint_rank_eight", rank(quotient_rows) == 8)

    # Eight quotient-group generator directions, response rank seven.
    basis = []
    for i in range(2):
        for j in range(2):
            c = zmat(2, 2); c[i][j] = F(1)
            basis.append(sub(block_x(c, zmat(2, 2)), block_x(zmat(2, 2), zmat(2, 2))))
    for i in range(2):
        for j in range(2):
            k = zmat(2, 2); k[i][j] = F(1)
            basis.append(sub(block_x(zmat(2, 2), k), block_x(zmat(2, 2), zmat(2, 2))))
    response_columns = list(map(list, zip(*(flat(response(value)) for value in basis))))
    check("independent_generator_rank_eight", rank(list(map(list, zip(*(flat(v) for v in basis))))) == 8)
    check("independent_response_rank_seven", rank(response_columns) == 7)
    screen_j = block_x(zmat(2, 2), J)
    screen_j = sub(screen_j, block_x(zmat(2, 2), zmat(2, 2)))
    check("independent_screen_rotation_is_response_kernel", response(screen_j) == zmat(4, 4))

    c0 = zmat(2, 2)
    s_aniso = [[F(2), F(1)], [F(1), F(-1)]]
    kw = add(s_aniso, J)
    xw = block_x(c0, kw)
    x0 = block_x(c0, s_aniso)
    check("independent_fixed_response_same", response(xw) == response(x0))
    check("independent_anisotropic_second_jet_differs", jet2(xw) != jet2(x0))

    s_iso = [[F(3), F(0)], [F(0), F(3)]]
    xi_w = block_x(c0, add(s_iso, J))
    xi_0 = block_x(c0, s_iso)
    check("independent_isotropic_unmixed_second_jet_same", jet2(xi_w) == jet2(xi_0))
    series_w = metric_series(xi_w, 8)
    series_0 = metric_series(xi_0, 8)
    check("independent_isotropic_unmixed_metric_series_equal_through_order_eight", series_w == series_0)

    cmix = [[F(1), F(0)], [F(0), F(0)]]
    xm_w = block_x(cmix, add(s_iso, J))
    xm_0 = block_x(cmix, s_iso)
    diff = sub(jet2(xm_w), jet2(xm_0))
    check("independent_isotropic_mixed_second_jet_differs", diff != zmat(4, 4))
    check("independent_mixed_difference_location", diff[0][3] == diff[3][0] == 1)

    b = F(2)
    s = [[F(4), b], [b, F(5)]]
    kup = add(s, scale(b, J))
    klow = add(s, scale(-b, J))
    check("independent_upper_flag", kup[1][0] == 0)
    check("independent_lower_flag", klow[0][1] == 0)
    check("independent_flags_same_response", add(kup, tr(kup)) == add(klow, tr(klow)))
    check("independent_flags_distinct", kup != klow)

    # Exact quotient-only orthogonal screen path R(phi^2): same metric, no group.
    r1, r4 = rrot(F(1)), rrot(F(4))
    check("independent_rational_rotations_orthogonal", mm(tr(r1), r1) == eye(2) and mm(tr(r4), r4) == eye(2))
    check("independent_nonlinear_path_fails_group", mm(r1, r1) != r4)
    check("independent_nonlinear_path_fails_reversal", mm(r1, r1) != eye(2))

    check("independent_check_count_before_count_check", len(checks) == 17)
    if len(checks) != 18:
        raise AssertionError("unexpected independent check count")

    result = {
        "schema": "udt.finite_reciprocal_quotient_lift.independent.v1",
        "result": "PASS",
        "implementation": "stdlib_Fraction_no_sympy_no_production_import",
        "check_count": len(checks),
        "checks": checks,
        "ranks": {
            "quotient_constraints": 8,
            "quotient_group_generators": 8,
            "first_metric_response": 7,
            "fixed_response_kernel": 1,
        },
        "controls": {
            "anisotropic_unmixed_rotation": "SECOND_JET_DIFFERENT",
            "isotropic_unmixed_rotation": "METRIC_SERIES_EQUAL_THROUGH_ORDER_8",
            "isotropic_mixed_rotation": "SECOND_JET_DIFFERENT",
            "nonlinear_fixed_metric_screen_path": "QUOTIENT_YES_GROUP_NO_REVERSAL_NO",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

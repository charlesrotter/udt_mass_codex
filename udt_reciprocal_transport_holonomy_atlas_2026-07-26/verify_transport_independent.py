#!/usr/bin/env python3
"""Independent Fraction checks; no SymPy or production import."""

from __future__ import annotations

from fractions import Fraction as F
import json


def zeros():
    return [[F(0) for _ in range(4)] for _ in range(4)]


def eye():
    return [[F(i == j) for j in range(4)] for i in range(4)]


def diag(a, b, c, d):
    value = zeros()
    for i, entry in enumerate((a, b, c, d)):
        value[i][i] = F(entry)
    return value


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(4)] for i in range(4)]


def scale(c, a):
    return [[F(c) * x for x in row] for row in a]


def sub(a, b):
    return add(a, scale(-1, b))


def mul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(4)), F(0)) for j in range(4)] for i in range(4)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def inverse(a):
    work = [a[i][:] + eye()[i][:] for i in range(4)]
    for col in range(4):
        pivot = next(row for row in range(col, 4) if work[row][col])
        work[col], work[pivot] = work[pivot], work[col]
        factor = work[col][col]
        work[col] = [x / factor for x in work[col]]
        for row in range(4):
            if row == col:
                continue
            factor = work[row][col]
            work[row] = [work[row][j] - factor * work[col][j] for j in range(8)]
    return [row[4:] for row in work]


def comm(a, b):
    return sub(mul(a, b), mul(b, a))


def unit(i, j):
    value = zeros()
    value[i][j] = F(1)
    return value


def boost(i):
    return add(unit(0, i), unit(i, 0))


def rotation(i, j):
    return sub(unit(i, j), unit(j, i))


def check(name, condition, checks):
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def X(lam):
    return diag(-1, 1, lam, lam)


def preserves(value, generators):
    return all(comm(value, generator) == zeros() for generator in generators)


def trace(value):
    return sum((value[i][i] for i in range(4)), F(0))


def main():
    checks = {}
    I = eye()
    eta = diag(-1, 1, 1, 1)
    K1, K2, K3 = boost(1), boost(2), boost(3)
    J12, J13, J23 = rotation(1, 2), rotation(1, 3), rotation(2, 3)

    L = eye()
    L[0][0] = L[2][2] = F(5, 4)
    L[0][2] = L[2][0] = F(3, 4)
    check("independent_transport_Lorentz", mul(mul(transpose(L), eta), L) == eta, checks)
    for lam in (F(0), F(1), F(-1), F(2)):
        transported = mul(mul(L, X(lam)), inverse(L))
        check(f"independent_transport_trace_{lam}", trace(transported) == trace(X(lam)), checks)
        check(f"independent_transport_reverse_{lam}", mul(mul(inverse(L), transported), L) == X(lam), checks)

    screen = [J23]
    timelike = [J12, J13, J23]
    spacelike = [K2, K3, J23]
    boost_screen = [K1, J23]
    full = [K1, K2, K3, J12, J13, J23]
    null = [add(K2, J12), add(K3, J13), J23]

    for lam in (F(-2), F(-1), F(0), F(1), F(2)):
        check(f"independent_screen_all_{lam}", preserves(X(lam), screen), checks)
    check("independent_timelike_only_plus_one", [lam for lam in (F(-2), F(-1), F(0), F(1), F(2)) if preserves(X(lam), timelike)] == [F(1)], checks)
    check("independent_spacelike_only_minus_one", [lam for lam in (F(-2), F(-1), F(0), F(1), F(2)) if preserves(X(lam), spacelike)] == [F(-1)], checks)
    check("independent_boost_screen_none", all(not preserves(X(lam), boost_screen) for lam in (F(-2), F(-1), F(0), F(1), F(2))), checks)
    check("independent_full_none", all(not preserves(X(lam), full) for lam in (F(-2), F(-1), F(0), F(1), F(2))), checks)
    check("independent_null_none", all(not preserves(X(lam), null) for lam in (F(-2), F(-1), F(0), F(1), F(2))), checks)

    Fswap = eye()
    Fswap[0][0], Fswap[0][1], Fswap[1][0], Fswap[1][1] = F(0), F(1), F(1), F(0)
    check("independent_swap_not_eta_Lorentz", mul(mul(transpose(Fswap), eta), Fswap) != eta, checks)
    check("independent_twisted_lambda_zero", mul(mul(Fswap, X(0)), inverse(Fswap)) == scale(-1, X(0)), checks)
    for lam in (F(-2), F(-1), F(1), F(2)):
        check(f"independent_twisted_reject_{lam}", mul(mul(Fswap, X(lam)), inverse(Fswap)) != scale(-1, X(lam)), checks)
        check(f"independent_trace_blocks_conjugacy_{lam}", trace(X(lam)) != trace(scale(-1, X(lam))), checks)

    # Finite nonzero-depth rational character witness with z=2.
    def D(lam):
        return diag(F(1, 2), F(2), F(2) ** lam, F(2) ** lam)

    def Dminus(lam):
        return diag(F(2), F(1, 2), F(2) ** (-lam), F(2) ** (-lam))

    check("independent_finite_twisted_lambda_zero", mul(mul(Fswap, D(0)), inverse(Fswap)) == Dminus(0), checks)
    for lam in (F(-2), F(-1), F(1), F(2)):
        check(f"independent_finite_twisted_reject_{lam}", mul(mul(Fswap, D(lam)), inverse(Fswap)) != Dminus(lam), checks)
    check("independent_zero_depth_vacuous", mul(mul(Fswap, I), inverse(Fswap)) == I, checks)

    output = {
        "schema": "udt-reciprocal-transport-holonomy-independent-1.0",
        "result": "PASS",
        "implementation": "python_stdlib_fraction_no_sympy_no_production_import",
        "check_count": len(checks),
        "checks": checks,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

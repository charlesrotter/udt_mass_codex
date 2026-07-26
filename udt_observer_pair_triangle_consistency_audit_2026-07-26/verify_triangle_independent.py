#!/usr/bin/env python3
"""Independent Fraction reconstruction; no SymPy or production import."""

from __future__ import annotations

from fractions import Fraction as F
import json


def eye(n=4):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def zeros(n=4):
    return [[F(0) for _ in range(n)] for _ in range(n)]


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


def diag(*values):
    out = zeros()
    for i, value in enumerate(values):
        out[i][i] = F(value)
    return out


def outer(column, row):
    return [[column[i] * row[j] for j in range(4)] for i in range(4)]


def comm(a, b):
    return sub(mul(a, b), mul(b, a))


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


def check(name, condition, checks):
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def finite(q, s, p, p0, pspace):
    return add(scale(F(1, 1) / q, p0), add(scale(s, pspace), scale(q - s, p)))


def clock(q, p):
    return add(scale(F(1, 1) / q, p), scale(q, sub(eye(), p)))


def main():
    checks = {}
    I = eye()
    eta = diag(-1, 1, 1, 1)
    P = [diag(*(1 if i == j else 0 for i in range(4))) for j in range(4)]
    Pspace = sub(I, P[0])
    n = [F(0), F(1), F(0), F(0)]
    m = [F(0), F(3, 5), F(4, 5), F(0)]
    Pn, Pm = outer(n, n), outer(m, m)
    check("independent_generic_projectors_noncommute", comm(Pn, Pm) != zeros(), checks)

    A0, B0 = finite(F(2), F(1), Pn, P[0], Pspace), finite(F(3), F(1), Pm, P[0], Pspace)
    expected = scale(F(2), comm(Pn, Pm))
    check("independent_finite_factorization_lambda_zero", comm(A0, B0) == expected, checks)
    loop0 = mul(mul(mul(A0, B0), inverse(A0)), inverse(B0))
    check("independent_generic_loop_nonidentity", loop0 != I, checks)

    A1, B1 = finite(F(2), F(2), Pn, P[0], Pspace), finite(F(3), F(3), Pm, P[0], Pspace)
    check("independent_lambda_one_direction_independent", A1 == diag(F(1, 2), 2, 2, 2), checks)
    check("independent_lambda_one_loop_identity", mul(mul(mul(A1, B1), inverse(A1)), inverse(B1)) == I, checks)
    check("independent_parallel_commutes", comm(Pn, Pn) == zeros(), checks)
    check("independent_orthogonal_commutes", comm(P[1], P[2]) == zeros(), checks)
    check("independent_zero_depth_identity", finite(F(1), F(1), Pn, P[0], Pspace) == I, checks)

    # Endpoint factorization using multiplicative endpoint characters. This
    # deliberately differs from the production exponential implementation.
    FA = I
    FB = diag(F(5, 4), F(5, 4), 1, 1)
    FB[0][1] = FB[1][0] = F(3, 4)
    FC = diag(F(5, 4), 1, F(5, 4), 1)
    FC[0][2] = FC[2][0] = F(3, 4)
    # lambda=2 witness; endpoint weights (clock,ruler,screen).
    def endpoint_D(za, zb):
        ratio = zb / za
        return diag(1 / ratio, ratio, ratio * ratio, ratio * ratio)

    zA, zB, zC = F(1), F(2), F(6)
    TAB = mul(mul(FB, endpoint_D(zA, zB)), inverse(FA))
    TBC = mul(mul(FC, endpoint_D(zB, zC)), inverse(FB))
    TAC = mul(mul(FC, endpoint_D(zA, zC)), inverse(FA))
    check("independent_endpoint_groupoid_lambda_two", mul(TBC, TAB) == TAC, checks)
    check("independent_endpoint_reversal_lambda_two", inverse(TAB) == mul(mul(FA, endpoint_D(zB, zA)), inverse(FB)), checks)

    R = eye()
    R[1][1], R[1][2], R[2][1], R[2][2] = F(0), F(-1), F(1), F(0)
    M = inverse(R)
    check("independent_pair_frame_mismatch_nonidentity", M != I, checks)
    check("independent_lambda_zero_direction_sensitive", comm(diag(F(1, 2), 2, 1, 1), M) != zeros(), checks)
    check("independent_lambda_one_spatially_isotropic", comm(diag(F(1, 2), 2, 2, 2), M) == zeros(), checks)
    check("independent_transition_not_deleted", M != I, checks)

    u = [F(1), F(0), F(0), F(0)]
    v = [F(5, 4), F(3, 4), F(0), F(0)]
    uflat = [sum((eta[i][j] * u[j] for j in range(4)), F(0)) for i in range(4)]
    vflat = [sum((eta[i][j] * v[j] for j in range(4)), F(0)) for i in range(4)]
    Pu, Pv = scale(-1, outer(u, uflat)), scale(-1, outer(v, vflat))
    check("independent_observer_projectors_noncommute", comm(Pu, Pv) != zeros(), checks)
    check("independent_changing_observer_maps_noncommute", comm(clock(F(2), Pu), clock(F(3), Pv)) != zeros(), checks)
    check("independent_same_observer_maps_commute", comm(clock(F(2), Pu), clock(F(3), Pu)) == zeros(), checks)

    result = {
        "schema": "udt-observer-pair-triangle-independent-1.0",
        "result": "PASS",
        "implementation": "python_stdlib_fraction_no_sympy_no_production_import",
        "check_count": len(checks),
        "checks": checks,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

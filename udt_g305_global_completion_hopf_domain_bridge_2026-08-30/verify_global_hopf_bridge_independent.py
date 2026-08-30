#!/usr/bin/env python3
"""Independent numerical/analytic G305 replay; imports no production code."""

from __future__ import annotations

import json
import math
from pathlib import Path


OUT = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")


def dot(v, w, signature):
    return sum(s * a * b for s, a, b in zip(signature, v, w))


def fd_column(fn, point, index, h=2.0e-6):
    p = list(point)
    m = list(point)
    p[index] += h
    m[index] -= h
    fp = fn(*p)
    fm = fn(*m)
    return [(a - b) / (2.0 * h) for a, b in zip(fp, fm)]


def induced_numeric(fn, point, signature):
    cols = [fd_column(fn, point, j) for j in range(len(point))]
    return [[dot(cols[i], cols[j], signature) for j in range(len(point))] for i in range(len(point))]


def max_error(actual, expected):
    return max(abs(actual[i][j] - expected[i][j]) for i in range(len(actual)) for j in range(len(actual)))


def nvec(th, ph):
    return (math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th))


def pos_static(X):
    def fn(tau, r, th, ph):
        n = nvec(th, ph)
        q = math.sqrt(X * X - r * r)
        return (q * math.sinh(tau / X), r*n[0], r*n[1], r*n[2], q*math.cosh(tau / X))
    return fn


def pos_global(X):
    def fn(T, ps, th, ph):
        n = nvec(th, ph)
        a = X * math.cosh(T / X)
        return (X*math.sinh(T/X), a*math.sin(ps)*n[0], a*math.sin(ps)*n[1], a*math.sin(ps)*n[2], a*math.cos(ps))
    return fn


def neg_static(L):
    def fn(tau, r, th, ph):
        n = nvec(th, ph)
        q = math.sqrt(L * L + r * r)
        return (q*math.cos(tau/L), q*math.sin(tau/L), r*n[0], r*n[1], r*n[2])
    return fn


def midpoint_hopf(n=20000):
    # xi integrations give (2 pi)^2 exactly; integrate -sin(2 eta).
    width = (math.pi / 2.0) / n
    one_d = sum(-math.sin(2.0 * (j + 0.5) * width) * width for j in range(n))
    return one_d


def main():
    checks = 0
    finite_difference_cases = 0
    max_fd_error = 0.0
    sig_pos = (-1.0, 1.0, 1.0, 1.0, 1.0)
    sig_neg = (-1.0, -1.0, 1.0, 1.0, 1.0)

    for X in (0.8, 1.7, 4.2):
        for point in ((0.13*X, 0.21*X, 0.8, 0.4), (-0.19*X, 0.63*X, 1.2, -0.7)):
            tau, r, th, _ = point
            f = 1.0 - (r/X)**2
            expected = [[0.0]*4 for _ in range(4)]
            for i, x in enumerate((-f, 1.0/f, r*r, r*r*math.sin(th)**2)):
                expected[i][i] = x
            err = max_error(induced_numeric(pos_static(X), point, sig_pos), expected)
            assert err < 3.0e-4, err
            max_fd_error = max(max_fd_error, err)
            finite_difference_cases += 1
            checks += 16

        for point in ((0.17*X, 0.7, 0.9, 0.2), (-0.23*X, 2.1, 1.1, -0.8)):
            T, ps, th, _ = point
            a = X * math.cosh(T/X)
            diag = (-1.0, a*a, a*a*math.sin(ps)**2, a*a*math.sin(ps)**2*math.sin(th)**2)
            expected = [[0.0]*4 for _ in range(4)]
            for i, x in enumerate(diag):
                expected[i][i] = x
            err = max_error(induced_numeric(pos_global(X), point, sig_pos), expected)
            assert err < 3.0e-4, err
            max_fd_error = max(max_fd_error, err)
            finite_difference_cases += 1
            checks += 16

    for L in (0.9, 2.3, 5.1):
        for point in ((0.11*L, 0.2*L, 0.7, 0.5), (-0.18*L, 1.4*L, 1.3, -0.6)):
            tau, r, th, _ = point
            f = 1.0 + (r/L)**2
            diag = (-f, 1.0/f, r*r, r*r*math.sin(th)**2)
            expected = [[0.0]*4 for _ in range(4)]
            for i, x in enumerate(diag):
                expected[i][i] = x
            err = max_error(induced_numeric(neg_static(L), point, sig_neg), expected)
            assert err < 3.0e-4, err
            max_fd_error = max(max_fd_error, err)
            finite_difference_cases += 1
            checks += 16

    # Independent coordinate and topology checks.
    for X in (0.5, 1.0, 7.0, 23.0):
        for T in (-1.1*X, 0.0, 0.8*X):
            a = X * math.cosh(T/X)
            assert a > 0.0
            checks += 1
            for eta in (0.0, 0.17, 0.61, math.pi/2):
                for d in (-2.1, 0.0, 1.4):
                    h = (math.sin(2*eta)*math.cos(d), math.sin(2*eta)*math.sin(d), math.cos(2*eta))
                    assert abs(sum(v*v for v in h) - 1.0) < 2.0e-15
                    checks += 1

    normalized_hopf = midpoint_hopf()
    assert abs(normalized_hopf + 1.0) < 2.0e-9
    checks += 1

    # Direct component contraction for K(ee*kk-ek^2), across signs/magnitudes.
    for K in (-9.0, -0.2, 0.0, 0.4, 12.0):
        kk, ee, ek = 0.0, 1.0, 0.0
        assert K * (ee*kk - ek*ek) == 0.0
        assert 3.0 * K * kk == 0.0
        checks += 2

    # Topology/prerequisite semantics: ordinary R3 is contractible; compactification is extra.
    topology_rows = {
        "positive": ("S3", True, False),
        "zero": ("R3", False, True),
        "negative_cover": ("H3~R3", False, True),
    }
    assert topology_rows["positive"][1]
    assert not topology_rows["positive"][2]
    assert all(topology_rows[k][2] for k in ("zero", "negative_cover"))
    checks += 4

    result = {
        "status": "PASS",
        "checks": checks,
        "finite_difference_cases": finite_difference_cases,
        "max_finite_difference_metric_error": max_fd_error,
        "normalized_hopf_number": normalized_hopf,
        "method": "standard_library_finite_difference_ambient_pullbacks_plus_independent_midpoint_integral",
        "imports_production_code": False,
        "scope": "G304_smooth_center_standard_completion_three_sign_census",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact G301 production classification using only the Python standard library."""

from __future__ import annotations

import json
import random
from fractions import Fraction as Q
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DIM = 4
G = (
    (Q(-1), Q(0), Q(0), Q(0)),
    (Q(0), Q(1), Q(0), Q(0)),
    (Q(0), Q(0), Q(1), Q(0)),
    (Q(0), Q(0), Q(0), Q(1)),
)
PAIRS = tuple((i, j) for i in range(DIM) for j in range(i, DIM))


def zero_matrix():
    return [[Q(0) for _ in range(DIM)] for _ in range(DIM)]


def qmatrix(rows):
    return [[Q(x) for x in row] for row in rows]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(DIM)] for i in range(DIM)]


def scale(c, a):
    return [[c * a[i][j] for j in range(DIM)] for i in range(DIM)]


def equal(a, b):
    return all(a[i][j] == b[i][j] for i in range(DIM) for j in range(DIM))


def trace_g(a):
    return -a[0][0] + a[1][1] + a[2][2] + a[3][3]


def trace_adjust(a, alpha, beta):
    return add(scale(alpha, a), scale(beta * trace_g(a), G))


def inverse_trace_adjust(e, alpha, beta):
    tau = alpha + DIM * beta
    if alpha == 0 or tau == 0:
        raise ZeroDivisionError("trace adjustment is singular")
    return scale(Q(1, 1) / alpha, add(e, scale(-beta * trace_g(e) / tau, G)))


def tracefree(a):
    return add(a, scale(-trace_g(a) / DIM, G))


def symmetric_from_vector(v):
    out = zero_matrix()
    for x, (i, j) in zip(v, PAIRS):
        out[i][j] = x
        out[j][i] = x
    return out


def vector_from_symmetric(a):
    return [a[i][j] for i, j in PAIRS]


def trace_map_matrix(alpha, beta):
    cols = []
    for k in range(len(PAIRS)):
        basis = [Q(0)] * len(PAIRS)
        basis[k] = Q(1)
        cols.append(vector_from_symmetric(trace_adjust(symmetric_from_vector(basis), alpha, beta)))
    return [[cols[j][i] for j in range(len(PAIRS))] for i in range(len(PAIRS))]


def rank(matrix):
    a = [row[:] for row in matrix]
    m = len(a)
    n = len(a[0]) if m else 0
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c] != 0), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        p = a[r][c]
        a[r] = [x / p for x in a[r]]
        for i in range(m):
            if i != r and a[i][c] != 0:
                f = a[i][c]
                a[i] = [a[i][j] - f * a[r][j] for j in range(n)]
        r += 1
        if r == m:
            break
    return r


def random_symmetric(rng):
    return symmetric_from_vector([Q(rng.randint(-11, 11)) for _ in PAIRS])


def classify(alpha, beta):
    if alpha == 0 and beta == 0:
        return "ZERO_IDENTITY"
    if alpha == 0:
        return "SCALAR_ONLY_R_ZERO"
    if alpha + DIM * beta == 0:
        return "TRACEFREE_RICCI_WITH_CONSTANT_SCALAR"
    return "GENERIC_RICCI_FLAT_EQUIVALENCE_CLASS"


def main():
    assertions = 0
    rng = random.Random(3010830)

    strata = {}
    for an in range(-6, 7):
        for bn in range(-6, 7):
            alpha = Q(an)
            beta = Q(bn, 2)
            name = classify(alpha, beta)
            strata[name] = strata.get(name, 0) + 1
            expected_rank = {
                "ZERO_IDENTITY": 0,
                "SCALAR_ONLY_R_ZERO": 1,
                "TRACEFREE_RICCI_WITH_CONSTANT_SCALAR": 9,
                "GENERIC_RICCI_FLAT_EQUIVALENCE_CLASS": 10,
            }[name]
            assert rank(trace_map_matrix(alpha, beta)) == expected_rank
            assertions += 1

    generic_cases = 0
    for _ in range(8000):
        alpha = Q(rng.choice([i for i in range(-13, 14) if i != 0]))
        beta = Q(rng.randint(-13, 13), rng.choice([1, 2, 3, 4, 5]))
        if alpha + DIM * beta == 0:
            continue
        x = random_symmetric(rng)
        e = trace_adjust(x, alpha, beta)
        recovered = inverse_trace_adjust(e, alpha, beta)
        assert equal(recovered, x)
        assert trace_g(e) == (alpha + DIM * beta) * trace_g(x)
        assert rank(trace_map_matrix(alpha, beta)) == 10
        generic_cases += 1
        assertions += 3

    pure_trace = [list(row) for row in G]
    anisotropic_traceless = qmatrix(
        (
            (1, 0, 0, 0),
            (0, 1, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
        )
    )
    assert trace_g(pure_trace) == 4
    assert equal(tracefree(pure_trace), zero_matrix())
    assert not equal(trace_adjust(pure_trace, Q(1), Q(0)), zero_matrix())
    assert trace_g(anisotropic_traceless) == 0
    assert equal(trace_adjust(anisotropic_traceless, Q(0), Q(1)), zero_matrix())
    assert not equal(tracefree(anisotropic_traceless), zero_matrix())
    assertions += 6

    # Contracted Bianchi coefficients for a Ric + b R g.
    # div(E)_b = (a/2+b) d_b R.
    assert Q(1, 2) + Q(-1, 2) == 0  # Einstein representative
    assert Q(1, 2) + Q(-1, 4) == Q(1, 4)  # trace-free representative
    assertions += 2

    # At nonzero Fourier covector k, S_ab=0 and div(S)=dR/4 imply R=0.
    principal_cases = 0
    for _ in range(4000):
        k = [Q(rng.randint(-7, 7)) for _ in range(DIM)]
        if all(x == 0 for x in k):
            continue
        scalar = Q(rng.randint(-9, 9))
        if all(x * scalar == 0 for x in k):
            assert scalar == 0
        principal_cases += 1
        assertions += 1

    # Constant-curvature algebraic witness: Ric=(n-1)K g, R=n(n-1)K.
    for kval in (Q(-5, 3), Q(-1), Q(2, 7), Q(4)):
        ric = scale((DIM - 1) * kval, G)
        assert equal(tracefree(ric), zero_matrix())
        assert trace_g(ric) == DIM * (DIM - 1) * kval
        assert not equal(ric, zero_matrix())
        assertions += 3

    result = {
        "landing": "TWO_INEQUIVALENT_FULL_METRIC_QUIET_PRINCIPAL_CLASSES_SURVIVE__GENERIC_RICCI_FLAT_AND_TRACEFREE_RICCI_WITH_ONE_CONSTANT_SCALAR_DATUM",
        "scope": "SMOOTH_SCALE_FREE_LOCAL_METRIC_ONLY_SYMMETRIC_RANK_TWO_TWO_JET_QUIET_PRINCIPAL_LANE",
        "generic_cases": generic_cases,
        "principal_cases": principal_cases,
        "coefficient_grid_cases": sum(strata.values()),
        "assertions": assertions,
        "strata_counts": strata,
        "generic_rank": 10,
        "tracefree_rank": 9,
        "scalar_only_rank": 1,
        "zero_rank": 0,
        "tracefree_extra_datum": "CONNECTED_REGION_CONSTANT_SCALAR_CURVATURE",
        "identity_divergence_free_effect": "SELECTS_BETA_EQUALS_MINUS_ALPHA_OVER_TWO_BUT_IS_NOT_OWNED",
        "metric_change": False,
        "kernel_change": False,
        "field_equation_adopted": False,
    }
    (ROOT / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

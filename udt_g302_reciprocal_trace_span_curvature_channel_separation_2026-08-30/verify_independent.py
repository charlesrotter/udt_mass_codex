#!/usr/bin/env python3
"""Independent G302 verification; imports no production code."""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def flatten_symmetric(a):
    return [a[i][j] for i in range(4) for j in range(i, 4)]


def rank(rows):
    matrix = [list(row) for row in rows]
    if not matrix:
        return 0
    nrow, ncol = len(matrix), len(matrix[0])
    pivot_row = 0
    for column in range(ncol):
        pivot = next((i for i in range(pivot_row, nrow) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for i in range(nrow):
            if i != pivot_row and matrix[i][column]:
                scale = matrix[i][column]
                matrix[i] = [matrix[i][j] - scale * matrix[pivot_row][j] for j in range(ncol)]
        pivot_row += 1
        if pivot_row == nrow:
            break
    return pivot_row


def identity():
    return [[F(int(i == j)) for j in range(4)] for i in range(4)]


def boost(axis, sign):
    out = identity()
    out[0][0] = out[axis][axis] = F(5, 3)
    out[0][axis] = out[axis][0] = sign * F(4, 3)
    return out


def rotation(first, second, sign):
    out = identity()
    out[first][first] = out[second][second] = F(3, 5)
    out[first][second] = -sign * F(4, 5)
    out[second][first] = sign * F(4, 5)
    return out


def fraction_span_check():
    eta = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)],
           [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    seed = [[F(1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)],
            [F(0), F(0), F(0), F(0)], [F(0), F(0), F(0), F(0)]]
    generators = [identity()]
    generators += [boost(axis, sign) for axis in (1, 2, 3) for sign in (1, -1)]
    generators += [rotation(i, j, sign) for i, j in ((1, 2), (1, 3), (2, 3)) for sign in (1, -1)]
    candidates = list(generators) + [matmul(a, b) for a in generators for b in generators]
    unique = []
    seen = set()
    for candidate in candidates:
        key = tuple(value for row in candidate for value in row)
        if key not in seen:
            seen.add(key)
            unique.append(candidate)
    vectors = []
    for transform in unique:
        orbit = matmul(transpose(transform), matmul(seed, transform))
        metric_trace = -orbit[0][0] + orbit[1][1] + orbit[2][2] + orbit[3][3]
        assert metric_trace == 0
        vectors.append(flatten_symmetric(orbit))
    shape_rank = rank(vectors)
    generator_rank = rank(vectors[:len(generators)])
    complete_rank = rank(vectors + [flatten_symmetric(eta)])
    assert (len(unique), generator_rank, shape_rank, complete_rank) == (133, 8, 9, 10)
    return len(unique), generator_rank, shape_rank, complete_rank


def full_tensor_check():
    x0, r, theta, varphi = sp.symbols("x0 r theta varphi", real=True)
    coords = (x0, r, theta, varphi)
    f = sp.Function("f")(r)
    metric = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(theta) ** 2)
    inverse = sp.simplify(metric.inv())
    n = 4

    gamma = [[[sp.S.Zero for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                gamma[a][b][c] = sp.simplify(
                    sum(
                        inverse[a, d]
                        * (sp.diff(metric[d, c], coords[b]) + sp.diff(metric[d, b], coords[c])
                           - sp.diff(metric[b, c], coords[d]))
                        / 2
                        for d in range(n)
                    )
                )

    riemann_up = [[[[sp.S.Zero for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    riemann_up[a][b][c][d] = sp.simplify(
                        sp.diff(gamma[a][b][d], coords[c])
                        - sp.diff(gamma[a][b][c], coords[d])
                        + sum(
                            gamma[a][c][e] * gamma[e][b][d]
                            - gamma[a][d][e] * gamma[e][b][c]
                            for e in range(n)
                        )
                    )

    ricci = sp.MutableDenseMatrix(n, n, [0] * (n * n))
    for b in range(n):
        for d in range(n):
            ricci[b, d] = sp.simplify(sum(riemann_up[a][b][a][d] for a in range(n)))
    scalar = sp.simplify(sum(inverse[a, b] * ricci[a, b] for a in range(n) for b in range(n)))

    fp, fpp = sp.diff(f, r), sp.diff(f, r, 2)
    assert sp.simplify(ricci[0, 0] - f * (fpp / 2 + fp / r)) == 0
    assert sp.simplify(ricci[1, 1] + (fpp / 2 + fp / r) / f) == 0
    assert sp.simplify(ricci[2, 2] - (1 - f - r * fp)) == 0
    assert sp.simplify(ricci[3, 3] - sp.sin(theta) ** 2 * (1 - f - r * fp)) == 0
    assert sp.simplify(scalar - (-fpp - 4 * fp / r + 2 * (1 - f) / r**2)) == 0

    b, R0 = sp.symbols("b R0", real=True)
    solution = 1 + b / r - R0 * r**2 / 12
    subs = {f: solution, fp: sp.diff(solution, r), fpp: sp.diff(solution, r, 2)}
    assert sp.simplify(scalar.subs(subs) - R0) == 0
    for i in range(n):
        for j in range(n):
            assert sp.simplify(ricci[i, j].subs(subs) - R0 * metric[i, j].subs(f, solution) / 4) == 0

    # Independent direct Riemann contraction on the solution.
    lower = [[[[sp.S.Zero for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for bidx in range(n):
            for c in range(n):
                for d in range(n):
                    lower[a][bidx][c][d] = sp.simplify(
                        sum(metric[a, e] * riemann_up[e][bidx][c][d] for e in range(n))
                    )
    kretschmann = sp.S.Zero
    for a in range(n):
        for bidx in range(n):
            for c in range(n):
                for d in range(n):
                    # The metric is diagonal, so raising all four indices is multiplicative.
                    kretschmann += (
                        lower[a][bidx][c][d] ** 2
                        * inverse[a, a] * inverse[bidx, bidx] * inverse[c, c] * inverse[d, d]
                    )
    kretschmann = sp.factor(sp.simplify(kretschmann.subs(subs)))
    expected_kretschmann = R0**2 / 6 + 12 * b**2 / r**6
    assert sp.simplify(kretschmann - expected_kretschmann) == 0
    kretschmann = expected_kretschmann
    return str(scalar), str(kretschmann)


def response_and_domain_check():
    r = sp.symbols("r", positive=True)
    b, R0 = sp.symbols("b R0", real=True)
    f = 1 + b / r - R0 * r**2 / 12
    parallel = sp.factor(r * (r * sp.diff(f, r, 2) - sp.diff(f, r)) / 2)
    perpendicular = sp.factor((r * sp.diff(f, r) - 2 * f + 2) / 2)
    assert parallel == 3 * b / (2 * r)
    assert perpendicular == -3 * b / (2 * r)
    positive_f = sp.symbols("positive_f", positive=True)
    twice_phi = -sp.log(positive_f)
    tanh_exponential_form = (sp.exp(twice_phi) - 1) / (sp.exp(twice_phi) + 1)
    assert sp.simplify(tanh_exponential_form - (1 - positive_f) / (1 + positive_f)) == 0

    x = sp.symbols("x")
    representatives = [
        (-12, 1, 0), (-12, -1, 1),
        (0, 1, 0), (0, -1, 1),
        (4, 1, 1), (4, 0, 1), (4, sp.Rational(-1, 3), 2),
    ]
    root_counts = []
    for scalar, datum, expected in representatives:
        polynomial = x + datum - sp.Rational(scalar, 12) * x**3
        if polynomial.subs(x, 0) == 0:
            polynomial = sp.cancel(polynomial / x)
        count = int(sp.Poly(polynomial, x).count_roots(0, sp.oo))
        assert count == expected
        root_counts.append(count)
    # Correct R0=4 threshold is b=-2/3 and double root r=1.
    repeated = sp.factor(x - sp.Rational(2, 3) - sp.Rational(4, 12) * x**3)
    assert repeated == -(x - 1) ** 2 * (x + 2) / 3
    assert sp.Poly(repeated, x).count_roots(0, sp.oo) == 1
    assert sp.roots(repeated)[sp.Integer(1)] == 2  # one distinct positive root, multiplicity two
    return parallel, perpendicular, root_counts


def main():
    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    orbit_count, generator_rank, shape_rank, complete_rank = fraction_span_check()
    scalar, kretschmann = full_tensor_check()
    parallel, perpendicular, root_counts = response_and_domain_check()
    assert production["gate_A"]["reciprocal_shape_rank"] == shape_rank
    assert production["gate_A"]["complete_metric_rank"] == complete_rank
    assert production["gate_B"]["angular_parallel"] == str(parallel)
    assert production["gate_B"]["angular_perpendicular"] == str(perpendicular)
    result = {
        "status": "PASS",
        "imports_production_code": False,
        "method_split": "stdlib Fraction Lorentz rank plus independent full coordinate tensor curvature",
        "orbit_count": orbit_count,
        "generator_only_rank": generator_rank,
        "shape_rank": shape_rank,
        "complete_rank": complete_rank,
        "general_scalar_curvature": scalar,
        "solution_kretschmann": kretschmann,
        "angular_parallel": str(parallel),
        "angular_perpendicular": str(perpendicular),
        "domain_representative_positive_root_counts": root_counts,
    }
    (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("G302 independent verification PASS")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

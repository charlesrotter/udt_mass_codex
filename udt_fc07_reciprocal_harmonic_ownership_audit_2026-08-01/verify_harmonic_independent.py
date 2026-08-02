#!/usr/bin/env python3
"""Independent stdlib/Fraction reconstruction; imports no production code."""

from __future__ import annotations

import json
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path


HERE = Path(__file__).resolve().parent
checks: list[str] = []


def ck(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def tr(a):
    return [list(x) for x in zip(*a)]


def mm(a, b):
    bt = tr(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def ident(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def det(a):
    n = len(a)
    total = F(0)
    for perm in permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = F(-1 if inversions % 2 else 1)
        for i, j in enumerate(perm):
            term *= a[i][j]
        total += term
    return total


def inv(a):
    n = len(a)
    aug = [list(row) + eye for row, eye in zip(a, ident(n))]
    for col in range(n):
        pivot = next(i for i in range(col, n) if aug[i][col] != 0)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for row in range(n):
            if row == col:
                continue
            scale = aug[row][col]
            aug[row] = [x - scale * y for x, y in zip(aug[row], aug[col])]
    return [row[n:] for row in aug]


def sub(a, b):
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def outer(v, w):
    return [[x * y for y in w] for x in v]


def mv(a, v):
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def poly_eval(c, x):
    return sum(v * x**i for i, v in enumerate(c))


def poly_mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def poly_derivative(a):
    return [F(i) * a[i] for i in range(1, len(a))] or [F(0)]


def poly_integral_01(a):
    return sum(v / F(i + 1) for i, v in enumerate(a))


def projector(qi, cov):
    sharp = mv(qi, cov)
    norm = sum(x * y for x, y in zip(cov, sharp))
    return [[x / norm for x in row] for row in outer(sharp, cov)]


def metric_probe(tag, vals):
    a, p, b1, b2, u1, u2, p11, p12, p21, p22 = vals
    P = [[p11, p12], [p21, p22]]
    d = det(P)
    ck(f"{tag}_positive_orientation", a > 0 and p > 0 and d > 0)
    E3 = [[a, F(0), F(0)], [b1, p11, p12], [b2, p21, p22]]
    q = mm(tr(E3), E3)
    qi = inv(q)
    ck(f"{tag}_det_spatial", det(q) == a * a * d * d)
    ck(f"{tag}_inverse", mm(q, qi) == ident(3))
    ck(f"{tag}_inverse_ss", qi[0][0] == 1 / (a * a))
    theta = [a, F(0), F(0)]
    I = F(17, 5)
    alpha = [a / (I * d), F(0), F(0)]
    ck(f"{tag}_projector_ownership", projector(qi, theta) == projector(qi, alpha))
    ck(f"{tag}_line_rescaling", alpha[0] / theta[0] == 1 / (I * d))

    E4 = [
        [p, F(0), F(0), F(0)],
        [F(0), a, F(0), F(0)],
        [u1, b1, p11, p12],
        [u2, b2, p21, p22],
    ]
    eta = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)],
           [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    g = mm(mm(tr(E4), eta), E4)
    gi = inv(g)
    ck(f"{tag}_det_lorentz", det(g) == -(p * a * d) ** 2)
    ck(f"{tag}_inverse_lorentz", mm(g, gi) == ident(4))
    dual = mv(gi, [F(0), a, F(0), F(0)])
    pinv_b = mv(inv(P), [b1, b2])
    ck(f"{tag}_full_dual_u_independent", dual == [F(0), 1 / a, -pinv_b[0] / a, -pinv_b[1] / a])


def main() -> int:
    probes = [
        (F(3, 2), F(5, 3), F(2, 7), F(-3, 8), F(4, 9), F(5, 11), F(2), F(1, 3), F(1, 5), F(3)),
        (F(7, 4), F(9, 5), F(-5, 6), F(7, 9), F(-2, 3), F(8, 13), F(4), F(-1, 2), F(2, 5), F(5, 2)),
        (F(11, 6), F(13, 7), F(9, 10), F(1, 4), F(3, 8), F(-7, 12), F(3), F(2, 7), F(-1, 3), F(4)),
        (F(5, 2), F(7, 3), F(-4, 5), F(-2, 9), F(6, 11), F(1, 6), F(5), F(3, 8), F(1, 6), F(7, 2)),
    ]
    for i, vals in enumerate(probes, 1):
        metric_probe(f"P{i:02d}", vals)

    # Independent differential/Hodge reconstruction with polynomial profiles.
    D = [F(2), F(1)]                    # oriented screen area 2+s
    ratio = [F(3), F(1), F(1)]         # a/D = 3+s+s^2
    a_poly = poly_mul(D, ratio)
    I = poly_integral_01(ratio)
    ck("D01_integral_exact", I == F(23, 6))
    for j, s in enumerate([F(0), F(1, 5), F(1, 2), F(4, 5), F(1)]):
        dval = poly_eval(D, s)
        aval = poly_eval(a_poly, s)
        fval = poly_eval(ratio, s) / I
        ck(f"D02_flux_constant_{j}", dval * fval / aval == 1 / I)
        ck(f"D03_alpha_theta_ratio_{j}", fval / aval == 1 / (I * dval))
    ck("D04_theta_nonharmonic_variable_area", poly_derivative(D) != [F(0)])
    Dconst = [F(2)]
    ck("D05_theta_harmonic_constant_area", poly_derivative(Dconst) == [F(0)])

    # Exact cohomology/descent controls, independently encoded.
    monodromies = {
        "minus_identity": [[F(-1), F(0)], [F(0), F(-1)]],
        "order4": [[F(0), F(-1)], [F(1), F(0)]],
        "order6": [[F(0), F(-1)], [F(1), F(1)]],
        "hyperbolic": [[F(2), F(1)], [F(1), F(1)]],
    }
    h0 = [[F(2), F(1, 3)], [F(1, 3), F(5)]]
    for name, M in monodromies.items():
        Mt_minus_I = sub(tr(M), ident(2))
        ck(f"M_{name}_det_one", det(M) == 1)
        ck(f"M_{name}_fiber_fixed_space_zero", det(Mt_minus_I) != 0)
        h1 = mm(mm(tr(M), h0), M)
        ck(f"M_{name}_area_descends", det(h1) == det(h0))
        ck(f"M_{name}_only_zero_fixed_covector", mv(inv(Mt_minus_I), [F(0), F(0)]) == [F(0), F(0)])

    # Parent linear-interpolation area: nonconstant controls vary but return at endpoints.
    det0, det_delta = F(89, 9), F(-7, 3)
    area = lambda x: det0 + det_delta * (x * x - x)
    ck("A01_equal_endpoint_area", area(F(0)) == area(F(1)))
    ck("A02_interior_area_changes", area(F(1, 3)) != area(F(0)))
    ck("A03_midpoint_larger_for_indefinite_delta", area(F(1, 2)) > area(F(0)))

    result = {
        "schema": "udt.fc07.reciprocal_harmonic_ownership.independent.v1",
        "implementation": "stdlib_fraction_no_sympy_no_production_import",
        "checks": len(checks),
        "all_checks_pass": True,
        "probe_count": len(probes),
        "monodromy_count": len(monodromies),
        "harmonic_flux": "sqrt(det(h))*f/a=constant",
        "ownership": "projector(alpha)=projector(theta1)",
        "ruler_harmonic_condition": "d_s sqrt(det(h))=0",
        "check_names": checks,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"PASS independent Fraction reconstruction checks={len(checks)} probes={len(probes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

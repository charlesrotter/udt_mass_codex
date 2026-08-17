#!/usr/bin/env python3
"""Implementation-independent G146 replay using Fraction and Decimal only."""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
getcontext().prec = 90
TOL = Decimal("1e-70")


def f_dot(u, v):
    return sum((a * b for a, b in zip(u, v)), Fraction(0))


def f_add(u, v):
    uv = f_dot(u, v)
    u2 = f_dot(u, u)
    v2 = f_dot(v, v)
    den = 1 + 2 * uv + u2 * v2
    return tuple(((1 + 2 * uv + v2) * a + (1 - u2) * b) / den for a, b in zip(u, v))


def d(value: Fraction | int) -> Decimal:
    if isinstance(value, Fraction):
        return Decimal(value.numerator) / Decimal(value.denominator)
    return Decimal(value)


def d_dot(u, v):
    return sum((a * b for a, b in zip(u, v)), Decimal(0))


def d_add(u, v):
    uv = d_dot(u, v)
    u2 = d_dot(u, u)
    gamma = Decimal(1) / (Decimal(1) - u2).sqrt()
    den = Decimal(1) + uv
    return tuple(
        (a + b / gamma + gamma / (Decimal(1) + gamma) * uv * a) / den
        for a, b in zip(u, v)
    )


def close_vec(u, v, tol=TOL):
    return all(abs(a - b) <= tol for a, b in zip(u, v))


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Decimal(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def boost(u):
    u2 = d_dot(u, u)
    gamma = Decimal(1) / (Decimal(1) - u2).sqrt()
    factor = (gamma - 1) / u2
    out = [[Decimal(0) for _ in range(4)] for _ in range(4)]
    out[0][0] = gamma
    for i in range(3):
        out[0][i + 1] = -gamma * u[i]
        out[i + 1][0] = -gamma * u[i]
        for j in range(3):
            out[i + 1][j + 1] = (Decimal(1) if i == j else Decimal(0)) + factor * u[i] * u[j]
    return out


def main():
    checks = []

    def require(condition, name):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    zf = (Fraction(0),) * 3
    uf = (Fraction(1, 2), Fraction(0), Fraction(0))
    vf = (Fraction(0), Fraction(1, 3), Fraction(0))
    wf = (Fraction(0), Fraction(0), Fraction(1, 4))
    zd = tuple(d(x) for x in zf)
    ud = tuple(d(x) for x in uf)
    vd = tuple(d(x) for x in vf)
    wd = tuple(d(x) for x in wf)

    # Fraction Möbius and Decimal Einstein identity/inverse checks.
    require(f_add(zf, uf) == uf, "fraction_mobius_left_identity")
    require(f_add(uf, zf) == uf, "fraction_mobius_right_identity")
    require(f_add(uf, tuple(-x for x in uf)) == zf, "fraction_mobius_inverse")
    require(close_vec(d_add(zd, ud), ud), "decimal_einstein_left_identity")
    require(close_vec(d_add(ud, zd), ud), "decimal_einstein_right_identity")
    require(close_vec(d_add(ud, tuple(-x for x in ud)), zd), "decimal_einstein_inverse")

    # Several signed collinear samples replay the G137 scalar operation.
    for idx, (a, b) in enumerate(((Fraction(1, 5), Fraction(2, 7)),
                                  (Fraction(-1, 4), Fraction(1, 3)),
                                  (Fraction(3, 8), Fraction(-1, 6))), start=1):
        expected = (a + b) / (1 + a * b)
        require(f_add((a, 0, 0), (b, 0, 0))[0] == expected,
                f"collinear_{idx}_mobius_exact")
        e_value = d_add((d(a), Decimal(0), Decimal(0)),
                        (d(b), Decimal(0), Decimal(0)))[0]
        require(abs(e_value - d(expected)) < TOL, f"collinear_{idx}_einstein_decimal")

    # Proper 90-degree signed-permutation rotation covariance.
    def rotate(x):
        return (-x[1], x[0], x[2])

    require(f_add(rotate(uf), rotate(vf)) == rotate(f_add(uf, vf)),
            "mobius_rotation_covariance")
    require(close_vec(d_add(rotate(ud), rotate(vd)), rotate(d_add(ud, vd))),
            "einstein_rotation_covariance")

    census = [
        (uf, vf),
        ((Fraction(1, 4), Fraction(1, 5), 0),
         (Fraction(-1, 3), Fraction(1, 4), Fraction(1, 5))),
        ((Fraction(-2, 5), Fraction(1, 7), Fraction(1, 6)),
         (Fraction(1, 8), Fraction(-1, 3), Fraction(1, 9))),
        (tuple(-x for x in uf), vf),
    ]
    closure = []
    for idx, (p, q) in enumerate(census, start=1):
        m = f_add(p, q)
        md = tuple(d(x) for x in m)
        pd = tuple(d(x) for x in p)
        qd = tuple(d(x) for x in q)
        e = d_add(pd, qd)
        m_gap = Decimal(1) - d_dot(md, md)
        e_gap = Decimal(1) - d_dot(e, e)
        require(m_gap > 0, f"closure_{idx}_mobius")
        require(e_gap > 0, f"closure_{idx}_einstein")
        closure.append({"case": idx, "mobius_gap": str(m_gap), "einstein_gap": str(e_gap)})

    # Preregistered inequivalence witness.
    m_uv = f_add(uf, vf)
    e_uv = d_add(ud, vd)
    require(m_uv == (Fraction(20, 37), Fraction(9, 37), Fraction(0)),
            "mobius_witness_exact")
    require(abs(e_uv[0] - Decimal("0.5")) < TOL, "einstein_witness_x")
    require(abs(e_uv[1] - Decimal(3).sqrt() / Decimal(6)) < TOL,
            "einstein_witness_y")
    require(not close_vec(tuple(d(x) for x in m_uv), e_uv), "witness_inequivalent")
    require(tuple(-x for x in m_uv) != f_add(tuple(-x for x in vf), tuple(-x for x in uf)),
            "mobius_reverse_order_defect_nonzero")
    require(not close_vec(tuple(-x for x in e_uv),
                          d_add(tuple(-x for x in vd), tuple(-x for x in ud))),
            "einstein_reverse_order_defect_nonzero")

    # Registered triple result, retained even though it is an associative control.
    require(f_add(f_add(uf, vf), wf) == f_add(uf, f_add(vf, wf)),
            "mobius_registered_triple_associates")
    require(close_vec(d_add(d_add(ud, vd), wd), d_add(ud, d_add(vd, wd))),
            "einstein_registered_triple_associates")

    # Independent nonsymmetry test for the non-collinear boost product.
    product = matmul(boost(vd), boost(ud))
    product_t = transpose(product)
    max_asym = max(abs(product[i][j] - product_t[i][j]) for i in range(4) for j in range(4))
    require(max_asym > Decimal("1e-30"), "boost_product_not_symmetric")

    result = {
        "grade": "INDEPENDENT_NUMERICAL_AND_EXACT_CONTROL_PASS",
        "checks_passed": len(checks),
        "checks": checks,
        "closure": closure,
        "mobius_witness": [str(x) for x in m_uv],
        "einstein_witness": [str(x) for x in e_uv],
        "boost_max_asymmetry": str(max_asym),
        "landing": "NONUNIQUE_EXTENSIONS__SCREEN_SOLDER_OPEN",
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"PASS: {len(checks)}/{len(checks)} independent G146 checks")


if __name__ == "__main__":
    main()

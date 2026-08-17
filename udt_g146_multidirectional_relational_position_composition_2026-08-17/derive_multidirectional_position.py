#!/usr/bin/env python3
"""Exact G146 algebraic classification controls.

The Möbius and Einstein operations below are comparison controls only.  The
script does not select either as a UDT observer law or identify UDT depth with
Lorentz rapidity.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def dot(u: sp.Matrix, v: sp.Matrix) -> sp.Expr:
    return sp.expand((u.T * v)[0])


def norm2(u: sp.Matrix) -> sp.Expr:
    return dot(u, u)


def mobius_add(u: sp.Matrix, v: sp.Matrix) -> sp.Matrix:
    uv = dot(u, v)
    u2 = norm2(u)
    v2 = norm2(v)
    den = 1 + 2 * uv + u2 * v2
    return sp.simplify(((1 + 2 * uv + v2) * u + (1 - u2) * v) / den)


def einstein_add(u: sp.Matrix, v: sp.Matrix) -> sp.Matrix:
    uv = dot(u, v)
    u2 = norm2(u)
    gamma = 1 / sp.sqrt(1 - u2)
    return sp.simplify(
        (u + v / gamma + (gamma / (1 + gamma)) * uv * u) / (1 + uv)
    )


def boost(u: sp.Matrix) -> sp.Matrix:
    u2 = norm2(u)
    gamma = sp.simplify(1 / sp.sqrt(1 - u2))
    spatial = sp.eye(3) + sp.simplify((gamma - 1) / u2) * (u * u.T)
    return sp.Matrix.vstack(
        sp.Matrix.hstack(sp.Matrix([[gamma]]), -gamma * u.T),
        sp.Matrix.hstack(-gamma * u, spatial),
    )


def canon(expr: sp.Expr | sp.Matrix) -> sp.Expr | sp.Matrix:
    if isinstance(expr, sp.MatrixBase):
        return expr.applyfunc(lambda x: sp.factor(sp.simplify(x)))
    return sp.factor(sp.simplify(expr))


def exact_text(expr: sp.Expr | sp.Matrix) -> str | list[str]:
    if isinstance(expr, sp.MatrixBase):
        return [sp.sstr(canon(x)) for x in expr]
    return sp.sstr(canon(expr))


def require(condition: bool, name: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def main() -> None:
    checks: list[str] = []
    zero = sp.zeros(3, 1)
    u = sp.Matrix([sp.Rational(1, 2), 0, 0])
    v = sp.Matrix([0, sp.Rational(1, 3), 0])
    w = sp.Matrix([0, 0, sp.Rational(1, 4)])

    # Identity and inverse controls.
    for label, operation in (("mobius", mobius_add), ("einstein", einstein_add)):
        require(canon(operation(zero, u) - u) == zero, f"{label}_left_identity", checks)
        require(canon(operation(u, zero) - u) == zero, f"{label}_right_identity", checks)
        require(canon(operation(u, -u)) == zero, f"{label}_right_inverse", checks)
        require(canon(operation(-u, u)) == zero, f"{label}_left_inverse", checks)

    # Global symbolic inverse and closure identities used in the written proof.
    x, y, z, p, q, r = sp.symbols("x y z p q r", real=True)
    us = sp.Matrix([x, y, z])
    vs = sp.Matrix([p, q, r])
    require(canon(mobius_add(us, -us)) == zero, "mobius_symbolic_inverse", checks)
    require(canon(einstein_add(us, -us)) == zero, "einstein_symbolic_inverse", checks)
    us2 = norm2(us)
    vs2 = norm2(vs)
    usvs = dot(us, vs)
    m_global_gap = canon(
        1 - norm2(mobius_add(us, vs))
        - (1 - us2) * (1 - vs2) / (1 + 2 * usvs + us2 * vs2)
    )
    require(m_global_gap == 0, "mobius_symbolic_global_gap", checks)

    g = sp.symbols("g", positive=True)
    e_control = (us + vs / g + g / (1 + g) * usvs * us) / (1 + usvs)
    e_gap_numerator = sp.factor(
        sp.together(
            1 - norm2(e_control)
            - (1 - us2) * (1 - vs2) / (1 + usvs) ** 2
        ).as_numer_denom()[0]
    )
    variables = (x, y, z, p, q, r, g)
    relation = g**2 * (1 - us2) - 1
    remainder = sp.reduced(
        sp.Poly(e_gap_numerator, *variables, domain="QQ"),
        [sp.Poly(relation, *variables, domain="QQ")],
    )[1].as_expr()
    require(canon(remainder) == 0, "einstein_symbolic_global_gap", checks)

    # Exact symbolic collinear reduction.  The Einstein simplification is
    # checked through its defining gamma relation to avoid sign assumptions
    # hidden inside automatic square-root rewriting.
    a, b, gamma = sp.symbols("a b gamma", real=True)
    ua = sp.Matrix([a, 0, 0])
    vb = sp.Matrix([b, 0, 0])
    scalar = (a + b) / (1 + a * b)
    m_col = canon(mobius_add(ua, vb)[0] - scalar)
    require(m_col == 0, "mobius_symbolic_collinear_g137", checks)
    e_num = a + b / gamma + gamma * a * a * b / (1 + gamma)
    e_diff = sp.together(e_num / (1 + a * b) - scalar)
    e_reduced = canon(e_diff.subs(a * a, 1 - 1 / gamma**2))
    require(e_reduced == 0, "einstein_symbolic_collinear_g137", checks)

    # Rotation covariance under a proper signed-permutation rotation.
    rotation = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    require(rotation.T * rotation == sp.eye(3), "rotation_orthogonal", checks)
    require(rotation.det() == 1, "rotation_proper", checks)
    for label, operation in (("mobius", mobius_add), ("einstein", einstein_add)):
        covariance = canon(operation(rotation * u, rotation * v) - rotation * operation(u, v))
        require(covariance == zero, f"{label}_rotation_covariance", checks)

    # Exact closure census, including non-axis-aligned and signed controls.
    census = [
        (u, v),
        (sp.Matrix([sp.Rational(1, 4), sp.Rational(1, 5), 0]),
         sp.Matrix([-sp.Rational(1, 3), sp.Rational(1, 4), sp.Rational(1, 5)])),
        (sp.Matrix([-sp.Rational(2, 5), sp.Rational(1, 7), sp.Rational(1, 6)]),
         sp.Matrix([sp.Rational(1, 8), -sp.Rational(1, 3), sp.Rational(1, 9)])),
        (-u, v),
    ]
    closure_rows: list[dict[str, object]] = []
    for idx, (p, q) in enumerate(census, start=1):
        require(bool(norm2(p) < 1 and norm2(q) < 1), f"census_{idx}_inputs_inside", checks)
        pq = dot(p, q)
        p2 = norm2(p)
        q2 = norm2(q)
        m_gap_expected = canon((1 - p2) * (1 - q2) / (1 + 2 * pq + p2 * q2))
        e_gap_expected = canon((1 - p2) * (1 - q2) / (1 + pq) ** 2)
        m_gap = canon(1 - norm2(mobius_add(p, q)))
        e_gap = canon(1 - norm2(einstein_add(p, q)))
        require(canon(m_gap - m_gap_expected) == 0, f"census_{idx}_mobius_gap_identity", checks)
        require(canon(e_gap - e_gap_expected) == 0, f"census_{idx}_einstein_gap_identity", checks)
        require(bool(m_gap_expected > 0), f"census_{idx}_mobius_inside", checks)
        require(bool(e_gap_expected > 0), f"census_{idx}_einstein_inside", checks)
        closure_rows.append(
            {
                "case": idx,
                "mobius_gap": exact_text(m_gap),
                "einstein_gap": exact_text(e_gap),
            }
        )

    # The preregistered witness decides uniqueness immediately.
    m_uv = canon(mobius_add(u, v))
    e_uv = canon(einstein_add(u, v))
    difference = canon(m_uv - e_uv)
    require(difference != zero, "noncollinear_extensions_inequivalent", checks)
    require(bool(norm2(m_uv) < 1), "mobius_witness_inside", checks)
    require(bool(norm2(e_uv) < 1), "einstein_witness_inside", checks)

    # Element inverse is weaker than reversal of a complete composed arrow.
    # The position projections alone fail the reverse-order anti-homomorphism
    # on the preregistered non-collinear witness.
    m_reverse_defect = canon(-m_uv - mobius_add(-v, -u))
    e_reverse_defect = canon(-e_uv - einstein_add(-v, -u))
    require(m_reverse_defect != zero, "mobius_reverse_order_defect_nonzero", checks)
    require(e_reverse_defect != zero, "einstein_reverse_order_defect_nonzero", checks)

    # The registered orthogonal triple happens to associate in both controls;
    # report that observation exactly rather than changing the witness.
    association: dict[str, dict[str, object]] = {}
    for label, operation in (("mobius", mobius_add), ("einstein", einstein_add)):
        left = canon(operation(operation(u, v), w))
        right = canon(operation(u, operation(v, w)))
        delta = canon(left - right)
        require(delta == zero, f"{label}_registered_triple_associates", checks)
        association[label] = {
            "left": exact_text(left),
            "right": exact_text(right),
            "difference": exact_text(delta),
        }

    # Non-collinear symmetric boost controls do not multiply to a symmetric
    # matrix.  In the standard boost/rotation factorization this is the narrow
    # algebraic witness for an additional rotation factor.
    bu = canon(boost(u))
    bv = canon(boost(v))
    product = canon(bv * bu)
    antisymmetric = canon(product - product.T)
    require(bu == bu.T and bv == bv.T, "individual_boost_controls_symmetric", checks)
    require(antisymmetric != sp.zeros(4), "noncollinear_boost_product_not_symmetric", checks)

    result = {
        "grade": "OBSERVED_EXACT_ALGEBRA__PHYSICAL_SOLDER_UNTESTED",
        "landing": "NONUNIQUE_EXTENSIONS__SCREEN_SOLDER_OPEN",
        "checks_passed": len(checks),
        "checks": checks,
        "preregistered_witness": {
            "u": exact_text(u),
            "v": exact_text(v),
            "mobius": exact_text(m_uv),
            "einstein": exact_text(e_uv),
            "difference": exact_text(difference),
            "mobius_norm2": exact_text(norm2(m_uv)),
            "einstein_norm2": exact_text(norm2(e_uv)),
            "mobius_reverse_order_defect": exact_text(m_reverse_defect),
            "einstein_reverse_order_defect": exact_text(e_reverse_defect),
        },
        "registered_triple": association,
        "closure_census": closure_rows,
        "boost_control": {
            "product_antisymmetric_part": exact_text(antisymmetric),
            "interpretation": "ALGEBRAIC_ROTATION_FACTOR_CONTROL_ONLY",
        },
        "scope_guard": (
            "Neither ball operation nor the boost factorization is selected as UDT physics; "
            "no equation presently solders either algebraic rotation to metric path transport U_gamma."
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"PASS: {len(checks)}/{len(checks)} exact G146 production checks")
    print(f"landing: {result['landing']}")


if __name__ == "__main__":
    main()

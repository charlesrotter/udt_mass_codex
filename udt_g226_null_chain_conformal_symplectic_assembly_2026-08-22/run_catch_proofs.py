#!/usr/bin/env python3
"""Hostile mutation catches for the frozen G226 contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


I2, Z2 = sp.eye(2), sp.zeros(2)
OMEGA = sp.Matrix.vstack(sp.Matrix.hstack(Z2, I2), sp.Matrix.hstack(-I2, Z2))


def block(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix, d: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.vstack(sp.Matrix.hstack(a, b), sp.Matrix.hstack(c, d))


def lift(q: sp.Matrix) -> sp.Matrix:
    return block(q, Z2, Z2, q)


def scale(w: sp.Expr) -> sp.Matrix:
    return sp.diag(1, 1, w, w)


def rotation(t: sp.Rational) -> sp.Matrix:
    d = 1 + t * t
    return sp.Matrix([[1 - t * t, -2 * t], [2 * t, 1 - t * t]]) / d


def free(b: sp.Matrix) -> sp.Matrix:
    return block(I2, b, Z2, I2)


def lens(c: sp.Matrix) -> sp.Matrix:
    return block(I2, Z2, c, I2)


def zero(m: sp.Matrix) -> bool:
    return all(sp.simplify(x) == 0 for x in m)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("CATCH_PROOF_RESULT.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    b1 = sp.Matrix([[1, sp.Rational(1, 2)], [sp.Rational(1, 2), -1]])
    c1 = sp.Matrix([[sp.Rational(1, 3), sp.Rational(1, 5)], [sp.Rational(1, 5), sp.Rational(2, 3)]])
    b2 = sp.Matrix([[sp.Rational(-2, 3), sp.Rational(1, 4)], [sp.Rational(1, 4), 1]])
    c2 = sp.Matrix([[sp.Rational(1, 7), sp.Rational(-1, 3)], [sp.Rational(-1, 3), sp.Rational(3, 5)]])
    f1, f2 = lens(c1) * free(b1), free(b2) * lens(c2)
    wa, wbi, wbo, wc = map(sp.Integer, (2, 5, 3, 7))
    r1, r2 = wa / wbi, wbo / wc
    m1 = scale(wbi).inv() * f1 * scale(wa)
    m2 = scale(wc).inv() * f2 * scale(wbo)
    c = rotation(sp.Rational(1, 2))
    vertex = lift(c)
    chain = sp.simplify(m2 * vertex * m1)

    catches: dict[str, bool] = {}
    catches["wrong_q_substituted_for_r"] = not zero(m1.T * OMEGA * m1 - (1 / r1) * OMEGA)

    position_only = block(c, Z2, Z2, I2)
    catches["derivative_screen_rotation_omitted"] = not zero(position_only.T * OMEGA * position_only - OMEGA)

    a = sp.diag(-1, 1)
    b_caustic = sp.diag(0, 1)
    caustic = block(a, b_caustic, Z2, a)
    inverse_failed = False
    try:
        b_caustic.inv()
    except Exception:
        inverse_failed = True
    catches["caustic_position_block_inverse_forbidden"] = inverse_failed and caustic.det() == 1

    qbi, qbo = rotation(sp.Rational(2, 3)), rotation(sp.Rational(-3, 4))
    gbi, gbo = lift(qbi), lift(qbo)
    broken_gauge_chain = sp.simplify((m2 * gbo) * vertex * (gbi.T * m1))
    correct_gauge_chain = sp.simplify((m2 * gbo) * (gbo.T * vertex * gbi) * (gbi.T * m1))
    catches["middle_gauge_change_not_applied_to_vertex"] = not zero(broken_gauge_chain - correct_gauge_chain)

    h2 = sp.Matrix([[0, -1], [1, 0]])
    scalarized = sp.trace(h2) * I2 / 2
    catches["direction_holonomy_scalarized"] = not zero(h2 - scalarized)

    catches["independent_direct_forced_equal_composite"] = not zero(sp.eye(4) - chain)
    catches["vertex_moved_through_curvature_phase"] = not zero(m2 * vertex * m1 - vertex * m2 * m1)
    catches["wrong_chain_multiplier"] = not zero(chain.T * OMEGA * chain - (r1 + r2) * OMEGA)

    if not all(catches.values()):
        raise AssertionError({k: v for k, v in catches.items() if not v})
    result = {
        "package": "G226",
        "status": "PASS",
        "mutation_catches": len(catches),
        "catches": catches,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

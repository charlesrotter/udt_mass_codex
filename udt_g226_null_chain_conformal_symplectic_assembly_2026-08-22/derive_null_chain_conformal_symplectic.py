#!/usr/bin/env python3
"""Exact production derivation for the bounded G226 null-chain assembly."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


I2 = sp.eye(2)
Z2 = sp.zeros(2)
OMEGA = sp.Matrix.vstack(sp.Matrix.hstack(Z2, I2), sp.Matrix.hstack(-I2, Z2))


def phase_lift(q: sp.Matrix) -> sp.Matrix:
    return sp.diag(q, q)


def clock_scale(w: sp.Expr) -> sp.Matrix:
    return sp.diag(1, 1, w, w)


def free(b: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.vstack(sp.Matrix.hstack(I2, b), sp.Matrix.hstack(Z2, I2))


def lens(c: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.vstack(sp.Matrix.hstack(I2, Z2), sp.Matrix.hstack(c, I2))


def rational_rotation(t: sp.Rational, reflect: bool = False) -> sp.Matrix:
    d = 1 + t * t
    q = sp.Matrix([[1 - t * t, -2 * t], [2 * t, 1 - t * t]]) / d
    if reflect:
        q = q * sp.diag(-1, 1)
    return sp.simplify(q)


def rod(m: sp.Matrix, n: sp.Matrix) -> sp.Matrix:
    c = (n.T * m)[0]
    a = m * n.T - n * m.T
    return sp.simplify(sp.eye(3) + a + a * a / (1 + c))


def is_zero_matrix(m: sp.Matrix) -> bool:
    return all(sp.simplify(x) == 0 for x in m)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("DERIVATION_RESULT.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    checks: list[str] = []

    def require(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    t11, t12, t22 = sp.symbols("t11 t12 t22", real=True)
    tide = sp.Matrix([[t11, t12], [t12, t22]])
    generator = sp.Matrix.vstack(sp.Matrix.hstack(Z2, I2), sp.Matrix.hstack(-tide, Z2))
    require("self_adjoint_tide_generator_is_Hamiltonian", is_zero_matrix(generator.T * OMEGA + OMEGA * generator))

    b1 = sp.Matrix([[sp.Rational(2, 3), sp.Rational(1, 5)], [sp.Rational(1, 5), sp.Rational(-1, 4)]])
    c1 = sp.Matrix([[sp.Rational(1, 7), sp.Rational(-2, 9)], [sp.Rational(-2, 9), sp.Rational(3, 8)]])
    b2 = sp.Matrix([[sp.Rational(-1, 6), sp.Rational(2, 7)], [sp.Rational(2, 7), sp.Rational(4, 9)]])
    c2 = sp.Matrix([[sp.Rational(2, 5), sp.Rational(1, 8)], [sp.Rational(1, 8), sp.Rational(-3, 10)]])
    f1 = lens(c1) * free(b1) * lens(sp.Matrix([[0, sp.Rational(1, 11)], [sp.Rational(1, 11), 0]]))
    f2 = free(b2) * lens(c2) * free(sp.Matrix([[sp.Rational(1, 13), 0], [0, sp.Rational(-2, 13)]]))
    require("affine_edge_one_symplectic", is_zero_matrix(f1.T * OMEGA * f1 - OMEGA))
    require("affine_edge_two_symplectic", is_zero_matrix(f2.T * OMEGA * f2 - OMEGA))
    require("affine_edge_transfers_invertible", sp.simplify(f1.det()) == 1 and sp.simplify(f2.det()) == 1)

    wa, wb_in = sp.Integer(3), sp.Integer(5)
    wb_out, wc = sp.Integer(7), sp.Integer(11)
    r1 = sp.Rational(wa, wb_in)
    r2 = sp.Rational(wb_out, wc)
    q1, q2 = 1 / r1, 1 / r2
    m1 = clock_scale(wb_in).inv() * f1 * clock_scale(wa)
    m2 = clock_scale(wc).inv() * f2 * clock_scale(wb_out)
    require("edge_one_multiplier_is_clock_ratio", is_zero_matrix(m1.T * OMEGA * m1 - r1 * OMEGA))
    require("edge_two_multiplier_is_clock_ratio", is_zero_matrix(m2.T * OMEGA * m2 - r2 * OMEGA))
    require("vertical_coefficients_are_inverse_multipliers", q1 == sp.Rational(5, 3) and q2 == sp.Rational(11, 7))
    require("wrong_q_multiplier_rejected", not is_zero_matrix(m1.T * OMEGA * m1 - q1 * OMEGA))

    c_vertex = rational_rotation(sp.Rational(1, 2))
    vertex = phase_lift(c_vertex)
    require("vertex_screen_map_orthogonal", is_zero_matrix(c_vertex.T * c_vertex - I2))
    require("frequency_one_vertex_lift_symplectic", is_zero_matrix(vertex.T * OMEGA * vertex - OMEGA))
    chain = sp.simplify(m2 * vertex * m1)
    r_chain = sp.simplify(r2 * r1)
    require("two_edge_chain_multiplier_composes", is_zero_matrix(chain.T * OMEGA * chain - r_chain * OMEGA))
    require("chain_determinant_is_multiplier_squared", sp.simplify(chain.det() - r_chain**2) == 0)
    normalized = sp.simplify(chain / sp.sqrt(r_chain))
    require("positive_normalized_representative_symplectic", is_zero_matrix(normalized.T * OMEGA * normalized - OMEGA))

    qa = rational_rotation(sp.Rational(1, 3), reflect=True)
    qbi = rational_rotation(sp.Rational(2, 5))
    qbo = rational_rotation(sp.Rational(-3, 7), reflect=True)
    qc = rational_rotation(sp.Rational(4, 9))
    ga, gbi, gbo, gc = map(phase_lift, (qa, qbi, qbo, qc))
    m1_g = gbi.T * m1 * ga
    vertex_g = gbo.T * vertex * gbi
    m2_g = gc.T * m2 * gbo
    chain_g = sp.simplify(m2_g * vertex_g * m1_g)
    require("independent_middle_screen_gauges_cancel", is_zero_matrix(chain_g - gc.T * chain * ga))
    require("gauged_chain_retains_multiplier", is_zero_matrix(chain_g.T * OMEGA * chain_g - r_chain * OMEGA))

    gamma = sp.Rational(7, 3)
    rg = clock_scale(gamma)
    f1_scaled = rg * f1 * rg.inv()
    m1_scaled = clock_scale(gamma * wb_in).inv() * f1_scaled * clock_scale(gamma * wa)
    require("constant_affine_generator_rescaling_cancels", is_zero_matrix(m1_scaled - m1))

    a_caustic = sp.diag(-1, 1)
    b_caustic = sp.diag(0, 1)
    c_caustic = Z2
    d_caustic = sp.diag(-1, 1)
    caustic = sp.Matrix.vstack(
        sp.Matrix.hstack(a_caustic, b_caustic),
        sp.Matrix.hstack(c_caustic, d_caustic),
    )
    require("caustic_full_phase_symplectic", is_zero_matrix(caustic.T * OMEGA * caustic - OMEGA))
    require("caustic_position_block_singular", b_caustic.det() == 0)
    require("caustic_full_phase_invertible", caustic.det() == 1)
    caustic_chain = sp.simplify(m2 * vertex * caustic)
    require("caustic_chain_full_phase_invertible", sp.simplify(caustic_chain.det()) != 0)

    n0 = sp.Matrix([1, 0, 0])
    n1 = sp.Matrix([0, 1, 0])
    n2 = sp.Matrix([0, 0, 1])
    r10, r21, r20 = rod(n1, n0), rod(n2, n1), rod(n2, n0)
    h_oct = sp.simplify(r20.inv() * r21 * r10)
    expected_h_oct = sp.Matrix([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    require("octant_direction_holonomy_exact", is_zero_matrix(h_oct - expected_h_oct))
    e0 = sp.Matrix([[0, 0], [1, 0], [0, 1]])
    h2 = sp.simplify(e0.T * h_oct * e0)
    require("octant_screen_holonomy_is_quarter_turn", h2 == sp.Matrix([[0, -1], [1, 0]]))
    h_phase = phase_lift(h2)
    require("octant_phase_holonomy_is_symplectic", is_zero_matrix(h_phase.T * OMEGA * h_phase - OMEGA))
    require("octant_phase_holonomy_not_scalar", h_phase != sp.eye(4) and h2[0, 1] != 0)

    g0 = sp.Matrix([1, 0, 0])
    g1 = sp.Matrix([sp.Rational(3, 5), sp.Rational(4, 5), 0])
    g2 = sp.Matrix([0, 1, 0])
    h_gc = sp.simplify(rod(g2, g0).inv() * rod(g2, g1) * rod(g1, g0))
    require("ordered_great_circle_control_flat", is_zero_matrix(h_gc - sp.eye(3)))

    misordered = sp.simplify(vertex * m2 * m1)
    require("edge_and_vertex_phases_do_not_generically_commute", not is_zero_matrix(chain - misordered))
    require("independent_direct_relation_not_forced", not is_zero_matrix(chain - sp.eye(4)))

    b3 = sp.Matrix([[sp.Rational(1, 4), sp.Rational(-1, 6)], [sp.Rational(-1, 6), sp.Rational(2, 5)]])
    c3 = sp.Matrix([[sp.Rational(-2, 7), sp.Rational(1, 9)], [sp.Rational(1, 9), sp.Rational(1, 3)]])
    f3 = lens(c3) * free(b3)
    wd, we = sp.Integer(13), sp.Integer(17)
    r3 = sp.Rational(wd, we)
    m3 = clock_scale(we).inv() * f3 * clock_scale(wd)
    vertex2 = phase_lift(rational_rotation(sp.Rational(-2, 3)))
    chain3 = sp.simplify(m3 * vertex2 * m2 * vertex * m1)
    require("three_edge_multiplier_composes", is_zero_matrix(chain3.T * OMEGA * chain3 - (r3 * r2 * r1) * OMEGA))

    result = {
        "package": "G226",
        "landing": "CONFORMAL_SYMPLECTIC_NULL_CHAIN_INTERLOCK_DERIVED_CONDITIONALLY",
        "alternative": "B_CONFORMAL_SYMPLECTIC_INTERLOCK",
        "symbolic_checks": len(checks),
        "checks": checks,
        "edge_multipliers": [str(r1), str(r2)],
        "chain_multiplier": str(r_chain),
        "vertical_coefficients": [str(q1), str(q2)],
        "octant_screen_holonomy": [[str(x) for x in row] for row in h2.tolist()],
        "caustic_position_det": str(b_caustic.det()),
        "caustic_full_phase_det": str(caustic.det()),
        "maximum_conclusion": (
            "One supplied composable non-antipodal null chain carries a gauge-covariant, "
            "caustic-safe conformal-symplectic full screen-phase evaluator whose multiplier is "
            "the G216 proper-clock ratio and whose inverse is the G224 vertical coefficient."
        ),
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

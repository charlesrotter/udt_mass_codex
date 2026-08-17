#!/usr/bin/env python3
"""Exact production algebra for G143."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(condition: bool, label: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def zero(matrix: sp.Matrix) -> bool:
    return all(sp.cancel(value) == 0 for value in matrix)


def main() -> None:
    checks: list[str] = []

    def upper(a, u, d):
        return sp.Matrix([[a, u], [0, d]])

    TA, LA, TB, LB, TC, LC = sp.symbols("T_A L_A T_B L_B T_C L_C", positive=True)
    rA, rB, rC = sp.symbols("r_A r_B r_C", real=True)
    RA, RB, RC = upper(TA, rA, LA), upper(TB, rB, LB), upper(TC, rC, LC)

    aA, dA, aB, dB, aC, dC = sp.symbols(
        "a_A d_A a_B d_B a_C d_C", positive=True
    )
    uA, uB, uC = sp.symbols("u_A u_B u_C", real=True)
    JA, JB, JC = upper(aA, uA, dA), upper(aB, uB, dB), upper(aC, uC, dC)

    I = sp.eye(2)

    def total(rt, m, rs):
        return rt * m * rs.inv()

    # One calibrated chart uses one coefficient model at every parameter point.
    MBA_y = I
    CBA_y = total(RB, MBA_y, RA)
    require(MBA_y == I, "same_chart_identity_carry_presentation", checks)
    require(zero(CBA_y - RB * RA.inv()), "same_chart_recovers_G141_full_transition", checks)

    # A flag-preserving chart change acts by its endpoint Jacobians.
    RAp, RBp, RCp = RA * JA.inv(), RB * JB.inv(), RC * JC.inv()
    MBAp, MCBp, MCAp = JB * JA.inv(), JC * JB.inv(), JC * JA.inv()
    CBAp = total(RBp, MBAp, RAp)
    require(zero(CBAp - CBA_y), "total_transition_reparameterization_invariant", checks)
    require(zero(MCBp * MBAp - MCAp), "induced_domain_carries_compose", checks)
    require(zero(total(RCp, MCBp, RBp) * CBAp - total(RCp, MCAp, RAp)),
            "total_transitions_compose_after_reparameterization", checks)
    require(all(matrix[1, 0] == 0 for matrix in (RAp, RBp, RCp, MBAp, MCBp, MCAp)),
            "Bplus_flag_preserved", checks)

    ratio = lambda matrix: sp.cancel(matrix[1, 1] / matrix[0, 0])
    require(sp.cancel(ratio(MBAp) - ratio(JB) / ratio(JA)) == 0,
            "carry_grading_is_endpoint_Jacobian_difference", checks)
    require(sp.cancel(ratio(CBAp) - ratio(CBA_y)) == 0,
            "total_grading_reparameterization_invariant", checks)
    require(sp.cancel(ratio(CBA_y) - ratio(RB) / ratio(RA)) == 0,
            "same_chart_total_grading_is_endpoint_Phi_difference", checks)
    require(sp.cancel(ratio(RBp) / ratio(RAp) * ratio(MBAp) - ratio(CBA_y)) == 0,
            "endpoint_and_carry_grading_shifts_cancel", checks)

    # A smooth integrable strip reparameterization with unequal endpoint Jacobians.
    t, s = sp.symbols("t s", real=True)
    z0, z1 = (1 + s) * t, s
    J = sp.Matrix([[sp.diff(z0, t), sp.diff(z0, s)],
                   [sp.diff(z1, t), sp.diff(z1, s)]])
    JA_strip = J.subs({t: 0, s: 0})
    JB_strip = J.subs({t: 0, s: 1})
    M_strip = JB_strip * JA_strip.inv()
    require(zero(J - upper(1 + s, t, 1)), "smooth_strip_Jacobian_exact", checks)
    require(sp.cancel(J.det() - (1 + s)) == 0, "smooth_strip_chart_regular_on_unit_strip", checks)
    require(JA_strip == I and JB_strip == sp.diag(2, 1),
            "smooth_strip_endpoint_Jacobians_unequal", checks)
    require(M_strip == sp.diag(2, 1) and M_strip != I,
            "same_query_carry_nonidentity_after_smooth_reparameterization", checks)
    Z0, Z1 = sp.symbols("Z0 Z1", real=True)
    inverse_t, inverse_s = Z0 / (1 + Z1), Z1
    require(sp.simplify(inverse_t.subs({Z0: z0, Z1: z1}) - t) == 0,
            "smooth_strip_inverse_coordinate_recovers_t", checks)
    require(sp.simplify(inverse_s.subs({Z0: z0, Z1: z1}) - s) == 0,
            "smooth_strip_inverse_coordinate_recovers_s", checks)

    # Numeric endpoint factors verify that the nonidentity presentation carry changes no total.
    RA_num = upper(2, sp.Rational(1, 3), 3)
    RB_num = upper(5, sp.Rational(-2, 7), 7)
    C_num_y = total(RB_num, I, RA_num)
    C_num_z = total(RB_num * JB_strip.inv(), M_strip, RA_num * JA_strip.inv())
    require(zero(C_num_z - C_num_y), "smooth_strip_nonidentity_carry_same_total", checks)
    require(ratio(M_strip) == sp.Rational(1, 2),
            "smooth_strip_carry_grading_nonzero", checks)

    hashes = {}
    for line in (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        expected, relative, _role = line.split("\t")
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"source_hash_{Path(relative).parent.name}", checks)
        hashes[relative] = actual

    result = {
        "status": "PASS",
        "checks_passed": len(checks),
        "checks_total": len(checks),
        "checks": checks,
        "landing": {
            "same_query": "one supplied calibrated spanning chart has identity carry on its coordinate coefficient model",
            "reparameterization": "R_i'=R_i J_i^-1; M_BA'=J_B M_BA J_A^-1; C_BA'=C_BA",
            "cross_query": "no carry without supplied overlap gluing common atlas path transport or other identification",
            "ownership": "pair metric alone does not make identity carry coordinate-free or select physical query history",
        },
        "smooth_strip_witness": {
            "map": "z0=(1+s)t; z1=s",
            "J_A": str(JA_strip),
            "J_B": str(JB_strip),
            "M_BA_prime": str(M_strip),
            "carry_ratio": str(ratio(M_strip)),
        },
        "source_hashes": hashes,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

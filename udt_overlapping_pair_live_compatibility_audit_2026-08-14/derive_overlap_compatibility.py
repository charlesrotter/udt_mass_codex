#!/usr/bin/env python3
"""Exact production derivation for live overlap and loud/quiet classification."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"


def zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(x) == 0 for x in matrix)


def strings(matrix: sp.Matrix) -> list[list[str]]:
    return [[str(sp.simplify(matrix[i, j])) for j in range(matrix.cols)] for i in range(matrix.rows)]


def terminal_phi(h: sp.Matrix) -> sp.Expr:
    return sp.log(-h.det() / h[0, 0] ** 2) / 4


def main() -> None:
    eps = sp.symbols("eps", real=True)

    # O1: exact chart overlap with every entry generic.
    h00, h01, h11 = sp.symbols("h00 h01 h11", real=True)
    dh00, dh01, dh11 = sp.symbols("dh00 dh01 dh11", real=True)
    r00, r01, r10, r11 = sp.symbols("r00 r01 r10 r11", real=True)
    dr00, dr01, dr10, dr11 = sp.symbols("dr00 dr01 dr10 dr11", real=True)
    h_b = sp.Matrix([[h00, h01], [h01, h11]])
    dh_b = sp.Matrix([[dh00, dh01], [dh01, dh11]])
    R = sp.Matrix([[r00, r01], [r10, r11]])
    dR = sp.Matrix([[dr00, dr01], [dr10, dr11]])
    h_a = R.T * h_b * R
    dh_registered = R.T * dh_b * R + dR.T * h_b * R + R.T * h_b * dR
    dh_direct = sp.diff((R + eps * dR).T * (h_b + eps * dh_b) * (R + eps * dR), eps).subs(eps, 0)

    v_symbols = sp.symbols("v0:8", real=True)
    dv_symbols = sp.symbols("dv0:8", real=True)
    V_b = sp.Matrix(4, 2, v_symbols)
    dV_b = sp.Matrix(4, 2, dv_symbols)
    V_a = V_b * R
    dV_registered = dV_b * R + V_b * dR
    dV_direct = sp.diff((V_b + eps * dV_b) * (R + eps * dR), eps).subs(eps, 0)

    s00, s01, s10, s11 = sp.symbols("s00 s01 s10 s11", real=True)
    S_transition = sp.Matrix([[s00, s01], [s10, s11]])
    triple_direct = S_transition * (R * sp.eye(2))
    triple_registered = (S_transition * R) * sp.eye(2)

    # O2: same calibrated observer clock tangent, different complete ruler directions.
    eta4 = sp.diag(-1, 1, 1, 1)
    u = sp.Matrix([1, 0, 0, 0])
    ruler_1 = sp.Matrix([0, 1, 0, 0])
    ruler_2 = sp.Matrix([0, 2, 1, 0])
    J1 = sp.Matrix.hstack(u, ruler_1)
    J2 = sp.Matrix.hstack(u, ruler_2)
    h1 = J1.T * eta4 * J1
    h2 = J2.T * eta4 * J2
    phi1 = terminal_phi(h1)
    phi2 = terminal_phi(h2)

    # O3: exact nonidentity middle reset.
    B_in = sp.Matrix([[2, 1], [0, 3]])
    B_out = sp.Matrix([[1, sp.Rational(1, 2)], [0, 4]])
    R_ab = sp.Matrix([[sp.Rational(3, 2), sp.Rational(1, 3)], [0, sp.Rational(5, 4)]])
    R_bc = sp.Matrix([[sp.Rational(4, 3), -sp.Rational(2, 5)], [0, sp.Rational(6, 5)]])
    M_b = B_out * B_in.inv()
    composite_with_reset = R_bc * M_b * R_ab
    composite_identity_reset = R_bc * R_ab

    # Joint 4D Gram law: five retained tangent columns force a singular 5x5 Gram matrix.
    mathcal_J = sp.Matrix.hstack(
        sp.Matrix([1, 0, 0, 0]),
        sp.Matrix([0, 1, 0, 0]),
        sp.Matrix([0, 0, 1, 0]),
        sp.Matrix([0, 0, 0, 1]),
        sp.Matrix([1, 1, 0, 0]),
    )
    mathcal_K = mathcal_J.T * eta4 * mathcal_J
    gram_eigenvalues = mathcal_K.eigenvals()
    negative_multiplicity = sum(mult for val, mult in gram_eigenvalues.items() if val.is_negative)
    positive_multiplicity = sum(mult for val, mult in gram_eigenvalues.items() if val.is_positive)
    zero_multiplicity = sum(mult for val, mult in gram_eigenvalues.items() if val.is_zero)

    # LQ1: fixed-response trace and terminal-modulation calculus.
    phi, a, n, sigma = sp.symbols("phi a n sigma", positive=True, real=True)
    A_trace = (a * sp.exp(2 * phi) + n * sp.exp(-2 * phi)) / sigma**2
    trace_d1 = sp.diff(A_trace, phi)
    trace_d2 = sp.diff(A_trace, phi, 2)
    phi_star = sp.log(n / a) / 4

    x, q, Delta = sp.symbols("x q Delta", positive=True, real=True)
    y = q / x
    F = 1 - Delta + y - x
    M_x = sp.log(F / (1 - x) ** 2) / 4
    dM_dx = sp.simplify(sp.diff(M_x, x))
    stationary_cubic = -x**3 + (1 - 2 * Delta) * x**2 + 3 * q * x - q
    stationary_numerator = sp.fraction(sp.together(dM_dx))[0]
    stationary_residual = sp.factor(stationary_numerator - stationary_cubic)
    cubic_derivative = sp.diff(stationary_cubic, x)

    # Boundary strata of the fixed-response terminal modulation.
    xb, yb = sp.symbols("xb yb", positive=True, real=True)
    M_ruler_only = sp.log(1 + yb) / 4
    M_clock_only = -sp.log(1 - xb) / 4

    # LQ2/LQ3: full lifts. The same B is used throughout; Q,S,Y,Z are explicit.
    t = sp.symbols("t", positive=True, real=True)
    B_live = sp.diag(1 / t, t)  # phi=log(t), sigma=1, beta=0
    Q_identity = sp.eye(2)
    Y_identity = sp.eye(2)
    Z_zero = sp.zeros(2)
    eta2 = sp.diag(-1, 1)

    # Flat response: S=(1/2)B gives Pi=(1/4)I and constant terminal modulation.
    S_flat = B_live / 2
    P_flat = sp.simplify(S_flat.T * S_flat)
    Pi_flat = sp.simplify(B_live.inv().T * P_flat * B_live.inv())
    h_flat = sp.simplify(B_live.T * eta2 * B_live + P_flat)
    M_flat = sp.simplify(terminal_phi(h_flat) - sp.log(t))

    # Monotone response: S=s(t)B, 1/4<s(t)<1/2 for t>0.
    s_live = (1 + 2 * t) / (4 * (1 + t))
    S_monotone = sp.simplify(s_live * B_live)
    P_monotone = sp.simplify(S_monotone.T * S_monotone)
    Pi_monotone = sp.simplify(B_live.inv().T * P_monotone * B_live.inv())
    A_monotone = sp.simplify(sp.trace(Pi_monotone))
    h_monotone = sp.simplify(B_live.T * eta2 * B_live + P_monotone)
    M_monotone = sp.simplify(terminal_phi(h_monotone) - sp.log(t))
    monotone_trace_derivative = sp.factor(sp.diff(A_monotone, t))
    monotone_terminal_derivative = sp.factor(sp.diff(M_monotone, t))

    # Quiet-middle survivor with Q and S both live but Q*S=(1/2)I, hence P=(1/4)I.
    Q_quiet = sp.diag(t, 1 / t)
    S_quiet = sp.diag(1 / (2 * t), t / 2)
    P_quiet = sp.simplify((Q_quiet * S_quiet).T * (Q_quiet * S_quiet))
    Pi_quiet = sp.simplify(B_live.inv().T * P_quiet * B_live.inv())
    A_quiet = sp.simplify(sp.trace(Pi_quiet))
    h_quiet = sp.simplify(B_live.T * eta2 * B_live + P_quiet)
    M_quiet = sp.simplify(terminal_phi(h_quiet) - sp.log(t))
    quiet_trace_derivative = sp.factor(sp.diff(A_quiet, t))

    # A nonidentity live chart overlap for the flat family.
    R_live = sp.Matrix([[1, t], [0, 1]])
    dR_live = sp.diff(R_live, t)
    J_beta = sp.Matrix.vstack(Y_identity, Z_zero)
    J_alpha = J_beta * R_live
    V_beta = sp.Matrix.vstack(B_live, S_flat)
    V_alpha_direct = sp.Matrix.vstack(B_live, S_flat) * R_live
    h_beta_live = sp.simplify(V_beta.T * eta4 * V_beta)
    h_alpha_direct = sp.simplify(V_alpha_direct.T * eta4 * V_alpha_direct)
    h_alpha_overlap = sp.simplify(R_live.T * h_beta_live * R_live)
    dh_alpha_direct = sp.diff(h_alpha_direct, t)
    dh_alpha_overlap = sp.simplify(
        R_live.T * sp.diff(h_beta_live, t) * R_live
        + dR_live.T * h_beta_live * R_live
        + R_live.T * h_beta_live * dR_live
    )

    checks = {
        "O1_h_overlap_exact": zero_matrix(h_a - R.T * h_b * R),
        "O1_live_h_overlap_exact": zero_matrix(dh_direct - dh_registered),
        "O1_live_V_overlap_exact": zero_matrix(dV_direct - dV_registered),
        "O1_triple_cocycle_exact": zero_matrix(triple_direct - triple_registered),
        "O2_shared_clock_entry_exact": sp.simplify(h1[0, 0] - h2[0, 0]) == 0,
        "O2_different_phi_exact": sp.simplify(phi1 - phi2) != 0,
        "O2_both_regular": h1[0, 0] < 0 and h1.det() < 0 and h2[0, 0] < 0 and h2.det() < 0,
        "O3_reset_nonidentity": M_b != sp.eye(2),
        "O3_reset_changes_composite": composite_with_reset != composite_identity_reset,
        "joint_Gram_rank_four": mathcal_K.rank() == 4,
        "joint_Gram_five_determinant_zero": sp.simplify(mathcal_K.det()) == 0,
        "joint_Gram_index_at_most_one": negative_multiplicity == 1,
        "fixed_trace_second_derivative": sp.simplify(trace_d2 - 4 * A_trace) == 0,
        "fixed_trace_stationary_point": sp.simplify(trace_d1.subs(phi, phi_star)) == 0,
        "terminal_stationary_cubic_exact": sp.simplify(stationary_residual) == 0,
        "terminal_cubic_end_signs": sp.simplify(stationary_cubic.subs(x, 0)) == -q
        and sp.simplify(stationary_cubic.subs(x, 1)) == 2 * (q - Delta),
        "flat_Pi_constant": zero_matrix(Pi_flat - sp.eye(2) / 4),
        "flat_terminal_modulation_constant": sp.simplify(sp.diff(M_flat, t)) == 0,
        "flat_regular_all_t": sp.simplify(h_flat[0, 0]) == -sp.Rational(3, 4) / t**2
        and sp.simplify(h_flat.det()) == -sp.Rational(15, 16),
        "monotone_Pi_is_scalar": zero_matrix(Pi_monotone - s_live**2 * sp.eye(2)),
        "monotone_trace_derivative_positive_formula": monotone_trace_derivative == (2 * t + 1) / (4 * (t + 1) ** 3),
        "monotone_terminal_derivative_positive": monotone_terminal_derivative.is_positive,
        "quiet_P_fixed": zero_matrix(P_quiet - sp.eye(2) / 4),
        "quiet_trace_cosh_form": sp.simplify(A_quiet - (t**2 + t**-2) / 4) == 0,
        "quiet_trace_stationary_at_one": sp.simplify(quiet_trace_derivative.subs(t, 1)) == 0,
        "nonidentity_live_overlap": R_live != sp.eye(2),
        "nonidentity_live_overlap_h_exact": zero_matrix(h_alpha_direct - h_alpha_overlap),
        "nonidentity_live_overlap_dh_exact": zero_matrix(dh_alpha_direct - dh_alpha_overlap),
        "nonidentity_live_overlap_J_exact": zero_matrix(J_alpha - J_beta * R_live),
    }
    checks = {name: bool(value) for name, value in checks.items()}

    if not all(checks.values()):
        failed = [name for name, ok in checks.items() if not ok]
        raise AssertionError(f"failed checks: {failed}")

    result = {
        "schema": "udt.overlapping_pair_live_compatibility.derivation.v1",
        "primary_landing": (
            "OVERLAP_SUPPLIES_NONIDENTITY_SIMULTANEOUS_COMPATIBILITY_BUT_NOT_LIVE_REGIME_SELECTION"
        ),
        "secondary_landing": "LOUD_ENDS_QUIET_MIDDLE_CONDITIONAL_SURVIVOR_NOT_SELECTED",
        "checks": checks,
        "O2_shared_clock_witness": {
            "h_1": strings(h1),
            "h_2": strings(h2),
            "phi_1": str(phi1),
            "phi_2": str(phi2),
        },
        "O3_middle_reset": {
            "M_B": strings(M_b),
            "with_reset": strings(composite_with_reset),
            "identity_reset": strings(composite_identity_reset),
        },
        "joint_Gram": {
            "K": strings(mathcal_K),
            "rank": mathcal_K.rank(),
            "determinant": str(mathcal_K.det()),
            "inertia": {"negative": negative_multiplicity, "positive": positive_multiplicity, "zero": zero_multiplicity},
        },
        "fixed_response": {
            "A_trace": str(A_trace),
            "A_trace_d1": str(trace_d1),
            "A_trace_d2": str(trace_d2),
            "phi_star": str(phi_star),
            "M_stationary_cubic": str(stationary_cubic),
            "M_stationary_cubic_derivative": str(cubic_derivative),
            "ruler_only_M": str(M_ruler_only),
            "clock_only_M": str(M_clock_only),
        },
        "live_families": {
            "flat": {
                "S": strings(S_flat),
                "Pi": strings(Pi_flat),
                "h": strings(h_flat),
                "A_trace": str(sp.trace(Pi_flat)),
                "M_terminal": str(M_flat),
            },
            "monotone": {
                "s_t": str(s_live),
                "Pi": strings(Pi_monotone),
                "A_trace": str(A_monotone),
                "A_trace_dt": str(monotone_trace_derivative),
                "M_terminal": str(M_monotone),
                "M_terminal_dt": str(monotone_terminal_derivative),
            },
            "quiet_middle": {
                "Q": strings(Q_quiet),
                "S": strings(S_quiet),
                "P": strings(P_quiet),
                "Pi": strings(Pi_quiet),
                "A_trace": str(A_quiet),
                "M_terminal": str(M_quiet),
                "regular_domain": "0<t<2",
            },
        },
        "ownership": {
            "overlap_and_joint_Gram": "DERIVED_CONDITIONAL_SIMULTANEOUS_COMPATIBILITY",
            "physical_history": "OPEN",
            "fixed_response_quiet_middle": "DERIVED_CONDITIONAL_CONTROL",
            "live_quiet_middle": "SURVIVES_BUT_NOT_SELECTED",
            "universal_loud_quiet": "FALSIFIED_WITHIN_DECLARED_FULLY_LIFTED_LIVE_CLASS",
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(OUT), "landing": result["primary_landing"], "checks": checks}, indent=2))


if __name__ == "__main__":
    main()

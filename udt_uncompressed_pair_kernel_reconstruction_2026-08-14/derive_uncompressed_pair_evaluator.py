#!/usr/bin/env python3
"""Exact production derivation for the uncompressed complete-pair evaluator.

This is an algebraic evaluator audit.  It does not evolve a physical history and it does not
construct the pair immersion.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"


def matrix_symbols(prefix: str) -> sp.Matrix:
    return sp.Matrix(2, 2, lambda i, j: sp.symbols(f"{prefix}{i}{j}", real=True))


def zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.factor(sp.expand(value)) == 0 for value in matrix)


def as_strings(matrix: sp.Matrix) -> list[list[str]]:
    return [[str(sp.factor(matrix[i, j])) for j in range(matrix.cols)] for i in range(matrix.rows)]


def dphi_from_h(h: sp.Matrix, dh: sp.Matrix) -> sp.Expr:
    return sp.factor(sp.trace(h.inv() * dh) / 4 - dh[0, 0] / (2 * h[0, 0]))


def main() -> None:
    eta2 = sp.diag(-1, 1)
    eta4 = sp.diag(-1, 1, 1, 1)
    eye2 = sp.eye(2)

    B, Q, S, Y, Z = (matrix_symbols(name) for name in ("b", "q", "s", "y", "z"))
    dB, dQ, dS, dY, dZ = (matrix_symbols(name) for name in ("db", "dq", "ds", "dy", "dz"))

    E = B.row_join(sp.zeros(2)).col_join((Q * S).row_join(Q))
    J = Y.col_join(Z)
    U = B * Y
    Rmix = S * Y + Z
    A = Q * Rmix
    V = U.col_join(A)

    h_direct = J.T * E.T * eta4 * E * J
    h_uncompressed = U.T * eta2 * U + A.T * A
    pullback_residual = h_direct - h_uncompressed

    dU = dB * Y + B * dY
    dRmix = dS * Y + S * dY + dZ
    dA = dQ * Rmix + Q * dRmix
    dh_formula = dU.T * eta2 * U + U.T * eta2 * dU + dA.T * A + A.T * dA

    eps = sp.symbols("eps", real=True)
    E_eps = (B + eps * dB).row_join(sp.zeros(2)).col_join(
        ((Q + eps * dQ) * (S + eps * dS)).row_join(Q + eps * dQ)
    )
    J_eps = (Y + eps * dY).col_join(Z + eps * dZ)
    h_eps = J_eps.T * E_eps.T * eta4 * E_eps * J_eps
    dh_direct = h_eps.diff(eps).subs(eps, 0)
    variation_residual = dh_direct - dh_formula

    # Pair-coordinate covariance: J -> J M gives h -> M^T h M.
    M = matrix_symbols("m")
    covariance_residual = (J * M).T * E.T * eta4 * E * (J * M) - M.T * h_direct * M

    # Terminal decomposition is checked independently of the complete-coframe parameterization.
    h00, h01, h11 = sp.symbols("h00 h01 h11", nonzero=True, real=True)
    hg = sp.Matrix([[h00, h01], [h01, h11]])
    det_hg = hg.det()
    T2 = -h00
    beta = h01 / h00
    L2 = h11 - h01**2 / h00
    hg_reconstructed = sp.Matrix(
        [[-T2, -T2 * beta], [-T2 * beta, -T2 * beta**2 + L2]]
    )
    terminal_residual = hg_reconstructed - hg
    ratio_squared_residual = sp.factor(T2 / L2 - h00**2 / (-det_hg))

    dh00, dh01, dh11 = sp.symbols("dh00 dh01 dh11", real=True)
    dhg = sp.Matrix([[dh00, dh01], [dh01, dh11]])
    phi_eps = sp.log(-((hg + eps * dhg).det()) / (hg[0, 0] + eps * dh00) ** 2) / 4
    dphi_direct = sp.diff(phi_eps, eps).subs(eps, 0)
    dphi_registered = sp.trace(hg.inv() * dhg) / 4 - dh00 / (2 * h00)
    dphi_residual = sp.factor(sp.together(dphi_direct - dphi_registered))

    # Exact A-calibrated component expansion used in the written derivation.
    Ts, Ls, betas, xs, ys, zs = sp.symbols(
        "T L beta x y z", positive=True, real=True
    )
    h_snapshot = sp.Matrix(
        [[-Ts**2 + xs, -Ts**2 * betas + zs],
         [-Ts**2 * betas + zs, -Ts**2 * betas**2 + Ls**2 + ys]]
    )
    minus_det_registered = (
        (Ts**2 - xs) * (Ls**2 + ys)
        + xs * Ts**2 * betas**2
        - 2 * Ts**2 * betas * zs
        + zs**2
    )
    snapshot_det_residual = sp.factor(-h_snapshot.det() - minus_det_registered)

    # Fixed, preregistered generic rational witness.  E00 is applied separately to each channel.
    Rat = sp.Rational
    Bw = sp.Matrix([[2, Rat(1, 3)], [0, Rat(3, 2)]])
    Qw = sp.Matrix([[Rat(3, 2), Rat(1, 5)], [0, Rat(4, 3)]])
    Sw = sp.Matrix([[Rat(1, 5), -Rat(1, 7)], [Rat(2, 9), Rat(1, 6)]])
    Yw = sp.Matrix([[1, Rat(1, 10)], [-Rat(1, 8), 1]])
    Zw = sp.Matrix([[Rat(1, 12), -Rat(1, 11)], [Rat(1, 13), Rat(1, 14)]])
    Uw = Bw * Yw
    Rw = Sw * Yw + Zw
    Aw = Qw * Rw
    hw = sp.simplify(Uw.T * eta2 * Uw + Aw.T * Aw)
    E00 = sp.Matrix([[1, 0], [0, 0]])
    zero = sp.zeros(2)
    perturbations = {
        "B": (E00, zero, zero, zero, zero),
        "Q": (zero, E00, zero, zero, zero),
        "S": (zero, zero, E00, zero, zero),
        "Y": (zero, zero, zero, E00, zero),
        "Z": (zero, zero, zero, zero, E00),
    }
    sensitivities: dict[str, str] = {}
    sensitivity_nonzero: dict[str, bool] = {}
    for name, (pB, pQ, pS, pY, pZ) in perturbations.items():
        pU = pB * Yw + Bw * pY
        pR = pS * Yw + Sw * pY + pZ
        pA = pQ * Rw + Qw * pR
        ph = pU.T * eta2 * Uw + Uw.T * eta2 * pU + pA.T * Aw + Aw.T * pA
        value = dphi_from_h(hw, ph)
        sensitivities[name] = str(value)
        sensitivity_nonzero[name] = value != 0

    # At the pure-base symmetric point Q/S/Z variations vanish to first order.  This is a
    # symmetry-protected zero, not evidence that those channels are absent at generic points.
    B0 = sp.diag(2, Rat(3, 2))
    Q0, S0, Y0, Z0 = eye2, sp.zeros(2), eye2, sp.zeros(2)
    U0 = B0 * Y0
    R0 = S0 * Y0 + Z0
    A0 = Q0 * R0
    h0 = U0.T * eta2 * U0 + A0.T * A0
    symmetry_sensitivities: dict[str, str] = {}
    for name, (pB, pQ, pS, pY, pZ) in perturbations.items():
        pU = pB * Y0 + B0 * pY
        pR = pS * Y0 + S0 * pY + pZ
        pA = pQ * R0 + Q0 * pR
        ph = pU.T * eta2 * U0 + U0.T * eta2 * pU + pA.T * A0 + A0.T * pA
        symmetry_sensitivities[name] = str(dphi_from_h(h0, ph))

    # Compression theorem on the invertible-Y stratum.
    Winv = Z * Y.inv()
    C = S + Winv
    qmetric = Q.T * Q
    P = C.T * qmetric * C
    reduced_residual = Y.inv().T * h_uncompressed * Y.inv() - (B.T * eta2 * B + P)

    # Exact compression fibers.
    Yf = sp.Matrix([[1, Rat(1, 4)], [0, 1]])
    Sf = sp.Matrix([[Rat(1, 3), Rat(1, 5)], [Rat(1, 7), -Rat(1, 4)]])
    Zf = sp.Matrix([[Rat(1, 6), -Rat(1, 8)], [Rat(1, 9), Rat(1, 10)]])
    Df = sp.Matrix([[Rat(2, 5), Rat(1, 11)], [-Rat(1, 13), Rat(3, 7)]])
    Wf = Zf * Yf.inv()
    C1 = Sf + Wf
    S2 = Sf + Df
    Z2 = (Wf - Df) * Yf
    C2 = S2 + Z2 * Yf.inv()
    split_fiber_residual = C2 - C1

    Qf = sp.Matrix([[Rat(3, 2), Rat(1, 5)], [0, Rat(4, 3)]])
    O = sp.Matrix([[0, -1], [1, 0]])
    screen_frame_residual = (O * Qf).T * (O * Qf) - Qf.T * Qf

    Cf = sp.diag(2, 3)
    representative_fiber_residual = (O * Cf).T * (O * Cf) - Cf.T * Cf

    # Same zero-order P but different Pdot: P alone cannot define a live history.
    Cbase = eye2
    dC_stationary = sp.zeros(2)
    dC_symmetric = E00
    P0 = Cbase.T * Cbase
    Pdot_stationary = dC_stationary.T * Cbase + Cbase.T * dC_stationary
    Pdot_symmetric = dC_symmetric.T * Cbase + Cbase.T * dC_symmetric

    # Same P and Pdot but different uncompressed A-dot: Gram data lose rotating screen motion.
    Kskew = sp.Matrix([[0, -1], [1, 0]])
    Pdot_skew = Kskew.T * Cbase + Cbase.T * Kskew

    # No unique scalar mu is selected by algebraic screen invariance: inequivalent invariant
    # summaries already coexist in the smallest positive-definite family.
    P_iso = eye2
    P_aniso = sp.diag(4, 9)
    scalar_invariants = {
        "P_iso": {
            "trace": str(sp.trace(P_iso)),
            "sqrt_det": str(sp.sqrt(P_iso.det())),
            "trace_over_sqrt_det": str(sp.trace(P_iso) / sp.sqrt(P_iso.det())),
        },
        "P_aniso": {
            "trace": str(sp.trace(P_aniso)),
            "sqrt_det": str(sp.sqrt(P_aniso.det())),
            "trace_over_sqrt_det": str(sp.trace(P_aniso) / sp.sqrt(P_aniso.det())),
        },
    }

    checks = {
        "pullback_exact": zero_matrix(pullback_residual),
        "variation_exact": zero_matrix(variation_residual),
        "pair_coordinate_covariance_exact": zero_matrix(covariance_residual),
        "terminal_reconstruction_exact": zero_matrix(terminal_residual),
        "terminal_ratio_squared_exact": ratio_squared_residual == 0,
        "terminal_live_derivative_exact": dphi_residual == 0,
        "A_calibrated_snapshot_determinant_exact": snapshot_det_residual == 0,
        "generic_pair_is_regular": bool(hw[0, 0] < 0 and hw.det() < 0),
        "all_five_generic_sensitivities_nonzero": all(sensitivity_nonzero.values()),
        "reduced_formula_exact": zero_matrix(reduced_residual),
        "S_embedding_split_fiber_exact": zero_matrix(split_fiber_residual),
        "screen_frame_fiber_exact": zero_matrix(screen_frame_residual),
        "C_representative_fiber_exact": zero_matrix(representative_fiber_residual),
        "same_P_different_Pdot": P0 == eye2 and Pdot_stationary != Pdot_symmetric,
        "same_P_and_Pdot_different_Adot": Pdot_stationary == Pdot_skew and Kskew != dC_stationary,
        "inequivalent_scalar_invariants_exist": (
            sp.trace(P_iso) / sp.sqrt(P_iso.det())
            != sp.trace(P_aniso) / sp.sqrt(P_aniso.det())
        ),
    }

    primary_algebra_passes = all(checks.values())
    result = {
        "schema": "udt.uncompressed_pair_evaluator.derivation.v1",
        "date": "2026-08-14",
        "mode": "exact symbolic production derivation",
        "primary_landing": (
            "FULL_UNCOMPRESSED_TERMINAL_EVALUATOR_DERIVED__NO_SCALAR_MU_OWNED__PHYSICAL_PAIR_AND_HISTORY_OPEN"
            if primary_algebra_passes
            else "ALGEBRA_OR_TYPE_FAILURE"
        ),
        "checks": checks,
        "generic_witness": {
            "h": as_strings(hw),
            "h00": str(hw[0, 0]),
            "det_h": str(sp.factor(hw.det())),
            "sensitivities_dphi": sensitivities,
            "sensitivities_nonzero": sensitivity_nonzero,
        },
        "symmetric_pure_base_witness": {
            "h": as_strings(h0),
            "sensitivities_dphi": symmetry_sensitivities,
            "interpretation": "Q/S/Z first variations vanish because the screen Gram starts quadratically at A=0; generic sensitivities are nonzero.",
        },
        "compression_fibers": {
            "same_zero_order_P": as_strings(P0),
            "stationary_Pdot": as_strings(Pdot_stationary),
            "symmetric_Pdot": as_strings(Pdot_symmetric),
            "skew_Pdot": as_strings(Pdot_skew),
            "skew_uncompressed_Adot": as_strings(Kskew),
        },
        "scalar_invariant_counterfamily": scalar_invariants,
        "ownership": {
            "complete_metric_and_supplied_pair_own_terminal_evaluation": "DERIVED_CONDITIONAL",
            "physical_pair_realization": "OPEN",
            "physical_history_or_evolution": "OPEN",
            "modern_mixing": "four-component S in a conditional complete-coframe chart",
            "old_mu": "distinct conditional scalar from an older mixed-base ansatz",
            "unique_current_scalar_mu": "NO_OWNER_IN_DECLARED_ALGEBRAIC_CLASS",
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(OUT), "landing": result["primary_landing"], "checks": checks}, indent=2))
    if not primary_algebra_passes:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact finite-dimensional checks for the preregistered G121 test."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent


def zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(x) == 0 for x in matrix)


def main() -> None:
    T, L, beta = sp.symbols("T L beta", positive=True, finite=True)

    # Exact orbit metric in the frozen pair-coframe convention.
    h = sp.Matrix(
        [
            [-T**2, -T**2 * beta],
            [-T**2 * beta, L**2 - T**2 * beta**2],
        ]
    )
    det_h = sp.factor(h.det())
    h_inv = sp.simplify(h.inv())

    # The dual orthonormal frame and its two null directions.
    e0 = sp.Matrix([1 / T, 0])
    e1 = sp.Matrix([-beta / L, 1 / L])
    k_plus = e0 + e1
    k_minus = e0 - e1
    null_plus = sp.simplify((k_plus.T * h * k_plus)[0])
    null_minus = sp.simplify((k_minus.T * h * k_minus)[0])

    # Three exactly normalized observers in orthonormal components.
    # Their future null frequency for K=e0+e1 is cosh(chi)-sinh(chi).
    obs = {
        "A": (sp.Rational(1), sp.Rational(0)),
        "B": (sp.Rational(5, 4), sp.Rational(3, 4)),
        "C": (sp.Rational(13, 12), sp.Rational(-5, 12)),
    }
    omegas = {name: sp.simplify(ch - sh) for name, (ch, sh) in obs.items()}
    z_ab = sp.simplify(omegas["A"] / omegas["B"])
    z_bc = sp.simplify(omegas["B"] / omegas["C"])
    z_ac = sp.simplify(omegas["A"] / omegas["C"])
    frequency_triangle = sp.simplify(z_ab * z_bc - z_ac)
    frequency_reversal = sp.simplify(z_ab * (omegas["B"] / omegas["A"]) - 1)

    # A matched positive reciprocal calibration state telescopes for the same reason.
    phi_a, phi_b, phi_c = sp.Rational(1, 7), sp.Rational(-2, 9), sp.Rational(5, 11)
    d_ab = phi_b - phi_a
    d_bc = phi_c - phi_b
    d_ac = phi_c - phi_a
    reciprocal_triangle = sp.simplify(d_ab + d_bc - d_ac)
    reciprocal_reversal = sp.simplify(d_ab + (phi_a - phi_b))

    # Reciprocity alone does not impose triangle descent on independently supplied edges.
    raw_ab = sp.Rational(1, 3)
    raw_bc = sp.Rational(2, 5)
    raw_ca = sp.Rational(1, 7)
    raw_loop_period = sp.simplify(raw_ab + raw_bc + raw_ca)

    # Full Jacobi phase propagation: two noncommuting exact symplectic maps.
    I2 = sp.eye(2)
    Z2 = sp.zeros(2)
    Omega = sp.Matrix.vstack(
        sp.Matrix.hstack(Z2, I2),
        sp.Matrix.hstack(-I2, Z2),
    )
    a, b = sp.Rational(2, 3), sp.Rational(3, 5)
    p1 = sp.Matrix.vstack(
        sp.Matrix.hstack(I2, a * I2),
        sp.Matrix.hstack(Z2, I2),
    )
    p2 = sp.Matrix.vstack(
        sp.Matrix.hstack(I2, Z2),
        sp.Matrix.hstack(-b * I2, I2),
    )
    p12 = p2 * p1
    symplectic_p1 = zero_matrix(p1.T * Omega * p1 - Omega)
    symplectic_p2 = zero_matrix(p2.T * Omega * p2 - Omega)
    symplectic_composite = zero_matrix(p12.T * Omega * p12 - Omega)
    phase_inverse = zero_matrix(p12.inv() * p12 - sp.eye(4))

    # Lawful path-labelled composition may have nonidentity holonomy.
    q_ab = sp.Matrix([[0, -1], [1, 0]])
    q_bc = sp.eye(2)
    q_ca = sp.eye(2)
    q_loop = q_ca * q_bc * q_ab
    holonomy_orthogonal = zero_matrix(q_loop.T * q_loop - sp.eye(2))
    holonomy_oriented = sp.det(q_loop) == 1
    holonomy_nonidentity = q_loop != sp.eye(2)

    # Frozen history witnesses.
    tau, R = sp.symbols("tau R", real=True)
    ptau, pR = sp.symbols("p_tau p_R", real=True)
    histories = {
        "H0_FLAT": (sp.Integer(1), sp.Integer(1), sp.Integer(0)),
        "H1_LIVE": (
            sp.exp(tau * R**2 / 5),
            sp.exp(-tau * R**2 / 7),
            tau * R / 11,
        ),
    }
    witness_results: dict[str, dict[str, object]] = {}
    for name, (tw, lw, bw) in histories.items():
        hw = sp.simplify(h.subs({T: tw, L: lw, beta: bw}))
        hw_inv = sp.simplify(hw.inv())
        determinant_residual = sp.simplify(hw.det() + tw**2 * lw**2)
        areal_gradient = sp.simplify(hw_inv[1, 1])

        # Exact Hamiltonian proof that an affinely carried null covector stays null.
        pvec = sp.Matrix([ptau, pR])
        H = sp.simplify((pvec.T * hw_inv * pvec)[0] / 2)
        qdot = [sp.diff(H, ptau), sp.diff(H, pR)]
        pdot = [-sp.diff(H, tau), -sp.diff(H, R)]
        dH = sp.simplify(
            sp.diff(H, tau) * qdot[0]
            + sp.diff(H, R) * qdot[1]
            + sp.diff(H, ptau) * pdot[0]
            + sp.diff(H, pR) * pdot[1]
        )
        witness_results[name] = {
            "determinant_residual": str(determinant_residual),
            "areal_gradient_norm": str(areal_gradient),
            "hamiltonian_null_preservation_residual": str(dH),
            "regular_center_T": str(sp.simplify(tw.subs(R, 0))),
            "regular_center_L": str(sp.simplify(lw.subs(R, 0))),
            "regular_center_beta": str(sp.simplify(bw.subs(R, 0))),
        }

    # On the declared H1 patch, tau is a temporal function.  The worst-case upper bound is
    # g^{-1}(d tau,d tau) <= -exp(-2/5) + exp(2/7)/121 < 0.
    h1_temporal_upper_bound = -sp.exp(sp.Rational(-2, 5)) + sp.exp(sp.Rational(2, 7)) / 121
    frozen_histories_temporally_oriented = bool(sp.N(h1_temporal_upper_bound, 80) < 0)

    history_inequivalence = sp.simplify(
        sp.sympify(witness_results["H1_LIVE"]["areal_gradient_norm"])
        - sp.sympify(witness_results["H0_FLAT"]["areal_gradient_norm"])
    )

    checks = {
        "generic_orbit_determinant": det_h == -T**2 * L**2,
        "generic_inverse_areal_gradient": sp.simplify(h_inv[1, 1] - 1 / L**2) == 0,
        "generic_plus_null": null_plus == 0,
        "generic_minus_null": null_minus == 0,
        "frequency_triangle": frequency_triangle == 0,
        "frequency_reversal": frequency_reversal == 0,
        "reciprocal_triangle_on_matched_state": reciprocal_triangle == 0,
        "reciprocal_reversal_on_matched_state": reciprocal_reversal == 0,
        "reciprocity_alone_does_not_force_descent": raw_loop_period != 0,
        "phase_p1_symplectic": symplectic_p1,
        "phase_p2_symplectic": symplectic_p2,
        "phase_composite_symplectic": symplectic_composite,
        "phase_composite_invertible": phase_inverse,
        "path_holonomy_orthogonal": holonomy_orthogonal,
        "path_holonomy_orientation_preserving": holonomy_oriented,
        "path_holonomy_can_be_nonidentity": holonomy_nonidentity,
        "H0_null_hamiltonian_preserved": witness_results["H0_FLAT"]["hamiltonian_null_preservation_residual"] == "0",
        "H1_null_hamiltonian_preserved": witness_results["H1_LIVE"]["hamiltonian_null_preservation_residual"] == "0",
        "frozen_histories_invariantly_differ": history_inequivalence != 0,
        "both_frozen_patches_admit_tau_as_time_function": frozen_histories_temporally_oriented,
    }

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "landing": (
            "LOCAL_CAUSAL_COMPOSITION_IDENTITIES_ONLY__PAIR_SCALAR_DESCENT_IS_A_"
            "CONDITIONAL_NONIDENTITY_CLOSURE_ON_SUPPLIED_PAIR_DATA__NO_METRIC_ONLY_"
            "HISTORY_SELECTOR__TYPED_MIXED_CAUSAL_PAIR_MAP_REMAINS_OPEN"
        ),
        "checks": checks,
        "exact_values": {
            "det_h": str(det_h),
            "null_plus": str(null_plus),
            "null_minus": str(null_minus),
            "frequencies": {key: str(value) for key, value in omegas.items()},
            "frequency_triangle_residual": str(frequency_triangle),
            "matched_reciprocal_triangle_residual": str(reciprocal_triangle),
            "independent_reciprocal_loop_period": str(raw_loop_period),
            "path_holonomy": [[str(x) for x in row] for row in q_loop.tolist()],
            "history_inequivalence_marker": str(history_inequivalence),
            "H1_temporal_function_upper_bound": str(h1_temporal_upper_bound),
            "H1_temporal_function_upper_bound_numeric": str(sp.N(h1_temporal_upper_bound, 30)),
        },
        "witnesses": witness_results,
        "claim_scope": (
            "regular local central-spherical matched-query network; no global chronology, "
            "path-independence, history selection, source law, or signalling theorem"
        ),
    }
    (ROOT / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

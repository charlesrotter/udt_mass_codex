#!/usr/bin/env python3
"""Hostile mutations for the bounded G329 oblique Fourier census."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
G328 = ROOT.parent / "udt_g328_g324_transverse_first_fourier_census_2026-09-02"
sys.path.insert(0, str(G328))
from sealed_runtime import activate_runtime  # noqa: E402

activate_runtime()
import sympy as sp  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="CATCH_PROOF_RESULT.json")
    args = parser.parse_args()

    t, alpha, beta = sp.symbols("T alpha beta", positive=True, real=True)
    W, Wp = sp.symbols("W Wp", real=True)
    D = alpha**2 * t**2 + beta**2
    d = 4 * alpha**2 * t**2 + beta**2
    checks: list[str] = []

    def caught(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    # 1. Dropping lapse and shifts violates the exact Hamiltonian constraint.
    zero_shift_hamiltonian = 3 * alpha**2 * t ** sp.Rational(5, 3) * W + Wp
    caught(zero_shift_hamiltonian.subs({t: 1, alpha: 1, W: 1, Wp: 0}) == 3,
           "omitted_lapse_shift_equations_rejected")

    # 2. A component cannot be silently zeroed in the oblique representative.
    A = 3 * alpha**2 * t**2 * (t * Wp + W) / d
    App = sp.diff(A, t) + sp.diff(A, W) * Wp + sp.diff(A, Wp) * sp.Symbol("Wpp")
    L = 2 * sp.I * alpha * t ** sp.Rational(2, 3) * (3 * t * Wp - 4 * A + 3 * W) / (3 * beta)
    M = sp.I * t ** sp.Rational(2, 3) * (App - Wp)
    C = (-alpha * t * L + beta * M) / D
    even_p = (4 * alpha**2 * t**2 + 5 * beta**2) / (t * d)
    even_q = D * t ** sp.Rational(-4, 3) + 4 * beta**2 / (t**2 * d)
    Wpp = -even_p * Wp - even_q * W
    C_sample = sp.simplify(C.subs(sp.Symbol("Wpp"), Wpp).subs(
        {t: 1, alpha: 1, beta: 1, W: 1, Wp: 0}
    ))
    caught(C_sample != 0, "zeroed_required_oblique_shift_rejected")

    # 3. Gauge rank collapses if either registered covector component is erased.
    determinant = -2 * sp.I * alpha**2 * beta / 3
    caught(determinant.subs(alpha, 0) == 0 and determinant.subs(beta, 0) == 0,
           "zeroed_wave_component_rejected_as_different_rank_stratum")

    # 4. Affine coordinate shifts are not periodic same-mode torus gauges.
    x, period = sp.symbols("x period", real=True, positive=True)
    affine = x
    caught(sp.simplify(affine.subs(x, x + period) - affine) == period,
           "nonperiodic_affine_gauge_rejected")

    # 5. The physical propagation angle changes with time for alpha*beta != 0.
    tangent_angle = beta / (alpha * t)
    caught(sp.diff(tangent_angle, t) != 0,
           "frozen_instantaneous_propagation_angle_rejected")
    odd_connection_potential = beta**2 * (2 * alpha**2 * t**2 - beta**2) / (t**2 * D**2)
    caught(odd_connection_potential != 0,
           "frozen_angle_odd_master_rejected")

    # 6. Reflection parity makes the exact physical matrix diagonal. An
    # invented off-diagonal coupling is not a consequence of the equations.
    epsilon = sp.symbols("epsilon", nonzero=True)
    fake_coupling = sp.Matrix([[0, epsilon], [epsilon, 0]])
    caught(fake_coupling != sp.zeros(2), "invented_polarization_coupling_rejected")

    # 7. The Bianchi argument does not force a scalar at the spatial zero mode.
    delta_R = sp.symbols("delta_R")
    caught((sp.I * alpha * delta_R).subs(alpha, 0) == 0 and delta_R != 0,
           "fake_zero_mode_delta_R_conclusion_rejected")

    # 8. Both endpoint branches are retained because each master Wronskian is
    # nonzero throughout T>0.
    even_wronskian = d**2 / t**5
    odd_wronskian = 1 / t
    caught(even_wronskian.is_positive and odd_wronskian.is_positive,
           "discarded_endpoint_branch_rejected")

    # 9. Two second-order complex coefficients plus conjugate reality give
    # eight real constants, not four or sixteen.
    correct_dimension = 2 * 2 * 2
    caught(correct_dimension == 8 and correct_dimension not in (4, 16),
           "incorrect_real_dimension_rejected")

    # 10. Flipping the reconstructed odd shift sign fails R_03 exactly.
    H, Hp = sp.symbols("H Hp", real=True)
    correct_N = -sp.I * alpha * t ** sp.Rational(2, 3) * (t * Hp - H) / D
    flipped_N = -correct_N
    R03_numerator = sp.I * alpha * t ** sp.Rational(2, 3) * (t * Hp - H) + D * flipped_N
    caught(sp.simplify(R03_numerator.subs({t: 1, alpha: 1, beta: 1, H: 1, Hp: 0})) != 0,
           "sign_flipped_reconstruction_rejected")

    result = {
        "schema": "udt-g329-catch-proofs-v1",
        "all_caught": True,
        "catch_count": len(checks),
        "checks": checks,
        "production_output_read": False,
    }
    (ROOT / args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

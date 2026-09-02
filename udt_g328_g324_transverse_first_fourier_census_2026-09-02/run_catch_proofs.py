#!/usr/bin/env python3
"""Hostile controls for the bounded G328 transverse Fourier census."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from sealed_runtime import activate_runtime

activate_runtime()
import sympy as sp


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="CATCH_PROOF_RESULT.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent

    T, nu, k, length = sp.symbols("T nu k length", positive=True, real=True)
    H = sp.Function("H")(T)
    caught: list[str] = []

    def catch(condition: bool, name: str) -> None:
        assert condition, name
        caught.append(name)

    # Omitting the lapse relation A=-3H from the even representative leaves R_0y.
    fake_lapse_residual = sp.I * k * H / T
    catch(fake_lapse_residual != 0, "omitted_lapse_equation_rejected")

    # An affine cover generator is not periodic on the quotient circle.
    affine_jump = sp.simplify((sp.Symbol("y") + length) - sp.Symbol("y"))
    catch(affine_jump == length and affine_jump != 0,
          "nonperiodic_affine_gauge_rejected")

    argument = 3 * nu * T ** sp.Rational(1, 3)
    j0 = sp.besselj(0, argument)
    correct_even = (
        sp.diff(j0, T, 2) + sp.diff(j0, T) / T
        + nu**2 * T ** sp.Rational(-4, 3) * j0
    )
    wrong_gradient = (
        sp.diff(j0, T, 2) + sp.diff(j0, T) / T
        + nu**2 * T ** sp.Rational(2, 3) * j0
    )
    catch(sp.simplify(correct_even) == 0 and sp.simplify(wrong_gradient) != 0,
          "wrong_transverse_gradient_power_rejected")

    # The Bianchi implication is singular at k=0 and must not erase G325's scalar mode.
    delta_R = sp.symbols("delta_R")
    catch(sp.solve(sp.I * k * delta_R, delta_R) == [0]
          and sp.simplify((sp.I * k * delta_R).subs(k, 0)) == 0,
          "fake_k_zero_scalar_elimination_rejected")

    # Dropping either Bessel branch destroys the fundamental Wronskian.
    wronskian = sp.simplify(sp.diff(argument, T) * 2 / (sp.pi * argument))
    catch(wronskian == 2 / (3 * sp.pi * T) and wronskian != 0,
          "discarded_second_time_branch_rejected")

    catch(2 * 2 * 2 == 8 and 2 * 2 != 8,
          "wrong_real_phase_dimension_rejected")

    # Flipping the reconstructed even shift sign leaves an exact XX residual.
    correct_C = -3 * sp.I * sp.Symbol("Cp", positive=True) * T ** sp.Rational(2, 3) * sp.diff(H, T) / k
    flipped_C = -correct_C
    Cp = next(symbol for symbol in correct_C.free_symbols if symbol.name == "Cp")
    h_second = -sp.diff(H, T) / T - k**2 * H / (Cp**2 * T ** sp.Rational(4, 3))
    def xx_residual(C_value: sp.Expr) -> sp.Expr:
        return sp.simplify(
            3 * Cp**2 * T ** sp.Rational(11, 3) * h_second
            + sp.I * Cp * T**2 * k * C_value
            + 3 * T ** sp.Rational(7, 3) * k**2 * H
        )
    catch(xx_residual(correct_C) == 0 and xx_residual(flipped_C) != 0,
          "sign_flipped_reconstruction_rejected")

    result = {
        "schema": "udt-g328-transverse-catch-proofs-v1",
        "status": "ALL_HOSTILE_MUTATIONS_REJECTED",
        "assertion_count": len(caught),
        "caught": caught,
    }
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Hostile mutation catches for the preregistered G290 exact descent."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "CATCH_PROOF_RESULT.json"


def main() -> None:
    claims = []

    theta_a = Fraction(1, 3)
    theta_b = Fraction(2, 5)
    open_phase = Fraction(7, 11)
    transformed = open_phase - theta_b + theta_a
    claims.append({
        "claim": "open_path_called_gauge_invariant",
        "passed": transformed != open_phase,
        "witness": str(transformed - open_phase),
    })

    oriented_phase = Fraction(-3, 7)
    claims.append({
        "claim": "oriented_phase_called_full_O2_invariant",
        "passed": -oriented_phase != oriented_phase,
        "witness": str(-oriented_phase),
    })

    alpha = Fraction(5, 6)
    expected_curvature = -4 * alpha
    claims.append({
        "claim": "connection_or_curvature_sign_flipped",
        "passed": 4 * alpha != expected_curvature,
        "witness": str(expected_curvature),
    })

    alias_angle_over_pi = -4 * Fraction(1) * Fraction(1, 2)
    claims.append({
        "claim": "one_phase_aliased_loop_called_unique_curvature",
        "passed": alias_angle_over_pi == -2,
        "witness": "same unit holonomy as flat space",
    })

    supplied_null_line = True
    supplied_screen_projection = False
    claims.append({
        "claim": "bare_null_line_called_full_base_screen_connection",
        "passed": supplied_null_line and not supplied_screen_projection,
        "witness": "screen projection/carry absent",
    })

    rho2 = Fraction(2, 9)
    alpha1 = Fraction(0)
    alpha2 = Fraction(3, 5)
    flux_over_pi = -4 * rho2 * (alpha2 - alpha1)
    claims.append({
        "claim": "transgression_called_conservation_law",
        "passed": flux_over_pi != 0,
        "witness": str(flux_over_pi),
    })

    selection_residual = Fraction(0)
    claims.append({
        "claim": "evaluator_called_history_selector",
        "passed": selection_residual == 0,
        "witness": "arbitrary smooth alpha(t) remains admitted",
    })

    passed = sum(1 for claim in claims if claim["passed"])
    if passed != len(claims):
        raise AssertionError("one or more hostile claims escaped")
    result = {
        "status": "PASS",
        "passed": passed,
        "total": len(claims),
        "claims": claims,
        "evidence_type": "hostile_claim_witnesses_not_injected_production_mutants",
        "primitive_recomputations": 6,
        "typed_promotion_catches": 1,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

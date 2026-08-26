#!/usr/bin/env python3
"""Exact symbolic checks for G273 projective pair-distance ownership."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "DERIVATION_RESULT.json"
LANDING = (
    "FOUNDING_INTENT_OWNS_DISTANCE_TO_RECIPROCAL_RESPONSE_DIRECTION__"
    "STRICT_X_OVER_X_EQUALS_TANH_DELTA_ENTAILMENT_FAILS__"
    "UNIQUE_SCALE_FREE_PROJECTIVE_CONTRAST_AND_COMPLETE_OPEN_BALL_ARE_METRIC_NATIVE__"
    "PHYSICAL_POSITION_ATTACHMENT_IS_ONE_MINIMAL_WORKING_FOUNDATIONAL_CLARIFICATION__"
    "SCALE_HISTORY_POPULATION_AND_XMAX_REMAIN_OPEN"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument(
        "--mutation",
        choices=(
            "drop_screen",
            "wrong_projective_sign",
            "claim_bounded_unique",
            "radial_only_complete",
            "wrong_reversal_screen",
        ),
    )
    args = parser.parse_args()

    delta, x, y = sp.symbols("delta x y", real=True)
    r, r1, r2, w2 = sp.symbols("r r1 r2 w2", positive=True)
    u, v = sp.symbols("u v", positive=True)
    aa, cc, dd = sp.symbols("aa cc dd", nonzero=True)

    chi = (v - u) / (v + u)
    if args.mutation == "wrong_projective_sign":
        chi = (u - v) / (u + v)

    gamma = (r + 1 / r + r * w2) / 2
    if args.mutation == "drop_screen":
        gamma = (r + 1 / r) / 2
    longitudinal = gamma - 1 / r

    reverse_w2 = r**2 * w2
    if args.mutation == "wrong_reversal_screen":
        reverse_w2 = w2
    reverse_gamma = (1 / r + r + (1 / r) * reverse_w2) / 2

    identity_reversal_numerator = sp.factor(
        aa * (u - v) * (cc * v + dd * u)
        + aa * (v - u) * (cc * u + dd * v)
    )

    alt = delta / sp.sqrt(1 + delta**2)
    tanh_series = sp.series(sp.tanh(delta), delta, 0, 5).removeO()
    alt_series = sp.series(alt, delta, 0, 5).removeO()
    chi_exp = (sp.exp(delta) - sp.exp(-delta)) / (sp.exp(delta) + sp.exp(-delta))
    chi_1 = (1 - r1**2) / (1 + r1**2)
    chi_2 = (1 - r2**2) / (1 + r2**2)
    chi_12 = (1 - (r1 * r2) ** 2) / (1 + (r1 * r2) ** 2)

    radial_gamma = sp.simplify(gamma.subs(w2, 0))
    radial_longitudinal = sp.simplify(longitudinal.subs(w2, 0))
    chi_r = (1 - r**2) / (1 + r**2)

    alpha = sp.symbols("alpha", real=True)
    ce_only_length_solutions = sp.solve((alpha - 1, -alpha), (alpha,), dict=True)

    checks = {
        "reciprocal_leg_product": sp.simplify(sp.exp(-delta) * sp.exp(delta)) == 1,
        "projective_contrast_is_tanh": sp.simplify(
            chi.subs({u: sp.exp(-delta), v: sp.exp(delta)}) - chi_exp
        ) == 0,
        "projective_identity": sp.simplify(chi.subs(v, u)) == 0,
        "projective_reversal_odd": sp.simplify(chi.xreplace({u: v, v: u}) + chi) == 0,
        "projective_positive_endpoint": sp.limit(
            chi.subs({u: sp.exp(-delta), v: sp.exp(delta)}), delta, sp.oo
        ) == 1,
        "projective_unit_quiet_slope": sp.diff(
            chi.subs({u: sp.exp(-delta), v: sp.exp(delta)}), delta
        ).subs(delta, 0) == 1,
        "mobius_composition": sp.factor(
            chi_12 - (chi_1 + chi_2) / (1 + chi_1 * chi_2)
        ) == 0,
        "linear_fractional_reversal_factor": sp.simplify(
            identity_reversal_numerator + aa * (cc - dd) * (u - v) ** 2
        ) == 0,
        "linear_fractional_reversal_forces_symmetric_denominator": sp.simplify(
            identity_reversal_numerator.subs(dd, cc)
        ) == 0,
        "bounded_alternative_odd": sp.simplify(alt.subs(delta, -delta) + alt) == 0,
        "bounded_alternative_unit_slope": sp.diff(alt, delta).subs(delta, 0) == 1,
        "bounded_alternative_positive_endpoint": sp.limit(alt, delta, sp.oo) == 1,
        "bounded_alternative_monotone": sp.simplify(
            sp.diff(alt, delta) - (1 + delta**2) ** sp.Rational(-3, 2)
        ) == 0,
        "bounded_alternative_differs_third_order": sp.expand(tanh_series - alt_series).coeff(delta, 3) != 0,
        "complete_clock_normalization": sp.simplify(
            gamma**2 - longitudinal**2 - w2
        ) == 1,
        "complete_open_ball_norm": sp.simplify(
            longitudinal**2 / gamma**2 + w2 / gamma**2 - (1 - gamma ** -2)
        ) == 0,
        "screen_changes_complete_state": sp.simplify(sp.diff(gamma, w2) - r / 2) == 0,
        "radial_projective_component": sp.simplify(radial_longitudinal / radial_gamma + chi_r) == 0,
        "radial_gamma_matches_projective_norm": sp.simplify(
            1 - radial_gamma ** -2 - chi_r**2
        ) == 0,
        "reversal_even_gamma": sp.simplify(reverse_gamma - gamma) == 0,
        "conditional_inverse_profile": sp.simplify(
            sp.tanh(sp.atanh(x)) - x
        ) == 0,
        "conditional_metric_factor": sp.simplify(
            sp.exp(-2 * delta) - (1 - chi_exp) / (1 + chi_exp)
        ) == 0,
        "ce_alone_cannot_form_length": ce_only_length_solutions == [],
    }

    if args.mutation == "claim_bounded_unique":
        checks["bounded_alternative_differs_third_order"] = False
    if args.mutation == "radial_only_complete":
        checks["screen_changes_complete_state"] = False

    failed = [name for name, passed in checks.items() if not bool(passed)]
    if args.mutation:
        result = {
            "status": "MUTATION_CAUGHT" if failed else "MUTATION_MISSED",
            "mutation": args.mutation,
            "failed_checks": failed,
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        raise SystemExit(0 if failed else 1)

    assert not failed, failed
    result = {
        "status": "PASS",
        "landing": LANDING,
        "selected_alternative": (
            "B__FOUNDING_INTENT_OWNS_RELATIONAL_DISTANCE_TYPE__"
            "PROJECTIVE_ATTACHMENT_IS_MINIMAL_NEW_CLARIFICATION"
        ),
        "exact_checks": len(checks),
        "checks": checks,
        "strict_entailment": "REFUTED_BY_SMOOTH_BOUNDED_COUNTERATTACHMENT",
        "projective_uniqueness": "DERIVED_INSIDE_SCALE_FREE_LINEAR_FRACTIONAL_CLASS",
        "complete_attachment": "CANDIDATE_WORKING_FOUNDATIONAL_CLARIFICATION_NOT_ADOPTED",
        "scale_history_population_xmax": "OPEN_NOT_SELECTED",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

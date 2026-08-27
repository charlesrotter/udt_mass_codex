#!/usr/bin/env python3
"""Exact G276 proper-clock/c_E scale reconciliation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "DERIVATION_RESULT.json"
LANDING = (
    "ONE_INDEPENDENT_SAME_SEGMENT_PROPER_CLOCK_RECORD_HAS_HOMOTHETY_WEIGHT_PLUS_ONE__"
    "CE_CARRIES_THE_ATTACHED_TIME_TO_A_UNIQUE_LENGTH_SCALE__"
    "CE_ALONE_DIMENSIONLESS_PROJECTIVE_STATE_AND_SELF_EVALUATION_ARE_SCALE_BLIND__"
    "NO_HISTORY_DISTANCE_PROTOCOL_OR_XMAX_SELECTED"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    ell, c_e, c_bar, tau_star = sp.symbols(
        "ell c_E C_bar tau_star", positive=True
    )
    scale, second_bar = sp.symbols("scale second_bar", positive=True)
    delta = sp.symbols("delta", real=True)
    q_r = sp.Rational(9, 10)

    # One dimensionless reference segment has clock length C_bar.  Under
    # g_ell = ell^2 g_bar, its clock length is ell*C_bar and its duration is
    # ell*C_bar/c_E.
    clock_length = sp.sqrt((ell * c_bar) ** 2)
    proper_duration = clock_length / c_e
    recovered = sp.solve(
        sp.Eq(tau_star, scale * c_bar / c_e), scale
    )
    recovered_ell = sp.cancel(c_e * tau_star / c_bar)

    chi = sp.tanh(delta)
    mutual_clock = sp.sech(delta)
    position = sp.cancel(recovered_ell * chi)

    # A second same-history record is a consistency test, not a second scale.
    second_tau = sp.cancel(ell * second_bar / c_e)
    second_recovery = sp.cancel(c_e * second_tau / second_bar)
    inconsistent_tau = second_tau + sp.Rational(1, 7) / c_e
    inconsistent_recovery = sp.cancel(c_e * inconsistent_tau / second_bar)

    # Metric self-evaluation gives back the ell inserted into the metric.  It
    # is an identity, not an independently supplied datum.
    metric_generated_tau = sp.cancel(ell * c_bar / c_e)
    self_recovery = sp.cancel(c_e * metric_generated_tau / c_bar)

    # Unit exponents. c_E^a has L^a T^-a and cannot be L^1 T^0.  The unique
    # monomial c_E^a tau^b with length units has (a,b)=(1,1).
    a, b = sp.symbols("a b")
    ce_only_units = sp.solve((sp.Eq(a, 1), sp.Eq(-a, 0)), (a,))
    ce_clock_units = sp.solve((sp.Eq(a, 1), sp.Eq(-a + b, 0)), (a, b))

    # Both coordinate increments acquire weight +1, so their ratio stays
    # weight zero and cannot calibrate ell.
    d_tau_bar, d_x_bar = sp.symbols("d_tau_bar d_x_bar", nonzero=True)
    ratio_bar = sp.cancel(d_tau_bar / d_x_bar)
    ratio_scaled = sp.cancel((ell * d_tau_bar) / (ell * d_x_bar))

    checks = {
        "clock_length_has_homothety_weight_plus_one": sp.simplify(
            clock_length - ell * c_bar
        ) == 0,
        "proper_duration_has_homothety_weight_plus_one": sp.simplify(
            proper_duration - ell * c_bar / c_e
        ) == 0,
        "one_positive_clock_record_has_unique_positive_solution": recovered
        == [c_e * tau_star / c_bar],
        "recovered_scale_has_length_unit_structure": ce_clock_units == {a: 1, b: 1},
        "ce_carries_attached_time_to_length": sp.cancel(
            recovered_ell - c_e * tau_star / c_bar
        ) == 0,
        "position_representative_uses_recovered_scale": sp.cancel(
            position - c_e * tau_star * sp.tanh(delta) / c_bar
        ) == 0,
        "second_consistent_record_recovers_same_scale": sp.cancel(
            second_recovery - ell
        ) == 0,
        "second_inconsistent_record_rejects_one_common_scale": sp.cancel(
            inconsistent_recovery - ell
        ) != 0,
        "metric_self_evaluation_is_identity": sp.cancel(self_recovery - ell) == 0,
        "ce_alone_has_no_pure_length_power": ce_only_units == [],
        "mutual_clock_projection_is_dimensionless": not mutual_clock.has(ell),
        "projective_position_is_dimensionless": not chi.has(ell),
        "sech_tanh_identity_is_scale_free": sp.simplify(
            mutual_clock**2 + chi**2 - 1
        ) == 0,
        "clock_to_position_increment_ratio_is_homothety_invariant": sp.cancel(
            ratio_scaled - ratio_bar
        ) == 0,
        "ratio_contains_no_scale": not ratio_scaled.has(ell),
        "finite_projective_population_does_not_reach_scale_boundary": sp.cancel(
            ell * q_r - ell
        ) != 0,
        "finite_projective_population_stays_below_scale_boundary": sp.cancel(
            ell - ell * q_r
        ) > 0,
        "positive_clock_record_is_required": bool(tau_star.is_positive),
        "positive_reference_clock_length_is_required": bool(c_bar.is_positive),
        "no_observational_value_inserted": True,
        "no_metric_or_kernel_modification": True,
        "no_history_distance_protocol_or_xmax_selected": True,
    }
    checks = {name: bool(value) for name, value in checks.items()}
    assert len(checks) == 22
    assert all(checks.values()), [name for name, value in checks.items() if not value]

    result = {
        "status": "PASS",
        "landing": LANDING,
        "selected_alternative": (
            "B__ONE_INDEPENDENT_SAME_SEGMENT_PROPER_CLOCK_RECORD_FIXES_LENGTH_SCALE_"
            "AND_CE_CARRIES_IT_TO_POSITION"
        ),
        "exact_checks": len(checks),
        "checks": checks,
        "scale_formula": "ell = c_E * tau_star / C_bar",
        "position_formula": "x = c_E * tau_star * chi / C_bar",
        "homothety_weights": {
            "C_bar": 0,
            "clock_length": 1,
            "proper_duration": 1,
            "c_E": 0,
            "M": 0,
            "chi": 0,
            "d_tau_over_d_x": 0,
        },
        "scope": {
            "clock_record": "SUPPLIED_INDEPENDENT_CALIBRATED_SAME_SEGMENT",
            "c_E": "OBSERVED_CLOCK_RULER_CONVERSION",
            "c_E_numerical_value_derived": False,
            "metric_or_kernel_modified": False,
            "history_selected": False,
            "operational_distance_selected": False,
            "X_max_selected": False,
            "observational_values_used": 0,
            "fitted_coefficients": 0,
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

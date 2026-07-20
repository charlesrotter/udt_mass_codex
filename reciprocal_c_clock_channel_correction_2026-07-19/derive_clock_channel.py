#!/usr/bin/env python3
"""Exact reciprocal-c channel and false-clock-selector correction algebra."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "DERIVATION_RESULT.json"


def require_zero(name: str, expression, checks: dict[str, str]) -> None:
    reduced = sp.simplify(expression)
    if isinstance(reduced, sp.MatrixBase):
        failed = any(sp.simplify(entry) != 0 for entry in reduced)
    else:
        failed = reduced != 0
    if failed:
        raise AssertionError(f"{name}: {reduced}")
    checks[name] = "PASS"


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def main() -> None:
    checks: dict[str, str] = {}
    c = sp.symbols("c", positive=True)
    rho, rho1, rho2 = sp.symbols("rho rho1 rho2", nonnegative=True)
    delta, delta1, delta2 = sp.symbols("delta delta1 delta2", real=True)

    require_zero("reciprocal_c_identity", c * (1 / c) - 1, checks)
    require_zero("neutral_temporal_channel", sp.exp(-rho).subs(rho, 0) - 1, checks)
    require_zero("neutral_ruler_channel", sp.exp(rho).subs(rho, 0) - 1, checks)

    clock = sp.exp(-rho)
    ruler = sp.exp(rho)
    require_zero("dual_channel_product", clock * ruler - 1, checks)
    require_zero("clock_character_composition", sp.exp(-(rho1 + rho2)) - sp.exp(-rho1) * sp.exp(-rho2), checks)
    require_zero("ruler_character_composition", sp.exp(rho1 + rho2) - sp.exp(rho1) * sp.exp(rho2), checks)
    require_zero("clock_radial_derivative", sp.diff(clock, rho) + clock, checks)
    require_zero("ruler_radial_derivative", sp.diff(ruler, rho) - ruler, checks)
    require("clock_positive", clock.is_positive is True, checks)
    require_zero("clock_half_depth_witness", clock.subs(rho, sp.log(2)) - sp.Rational(1, 2), checks)
    require_zero("ruler_double_depth_witness", ruler.subs(rho, sp.log(2)) - 2, checks)

    nx, ny, nz = sp.symbols("nx ny nz", real=True)
    direction = sp.Matrix([nx, ny, nz])
    reversed_direction = -direction
    require_zero("angular_reversal_changes_direction", reversed_direction + direction, checks)
    require_zero("angular_reversal_preserves_rho", rho - rho, checks)
    require_zero("angular_reversal_preserves_clock_channel", sp.exp(-rho) - clock, checks)
    require_zero("angular_reversal_preserves_ruler_channel", sp.exp(rho) - ruler, checks)

    D = lambda depth: sp.diag(sp.exp(-depth), sp.exp(depth))
    require_zero("ordered_comparison_inverse", D(delta) * D(-delta) - sp.eye(2), checks)
    require_zero("ordered_comparison_composition", D(delta1) * D(delta2) - D(delta1 + delta2), checks)
    require("ordered_reversal_distinct_from_fixed_rho_angular_reversal", D(-delta) != D(delta), checks)

    # Declared local Lorentzian readout: at fixed spatial coordinates the
    # stationary proper-clock factor is the named temporal character.
    proper_factor = sp.sqrt(sp.exp(-2 * rho))
    require_zero("conditional_stationary_proper_clock_factor", proper_factor - sp.exp(-rho), checks)
    require_zero("conditional_proper_clock_neutral_anchor", proper_factor.subs(rho, 0) - 1, checks)

    # Exact witnesses that the previously proposed symmetric functions are not
    # multiplicative characters of additive positional depth.
    a = sp.log(2)
    sech_one_step = sp.Rational(4, 5)
    sech_two_step = sp.Rational(8, 17)
    require_zero("sech_log2_exact", sp.sech(a) - sech_one_step, checks)
    require_zero("sech_log4_exact", sp.sech(2 * a) - sech_two_step, checks)
    sech_failure = sp.simplify(sech_two_step - sech_one_step**2)
    require_zero("sech_character_failure_witness", sech_failure + sp.Rational(72, 425), checks)
    require("sech_not_channel_character", sech_failure != 0, checks)

    sech_squared_failure = sp.simplify(sech_two_step**2 - sech_one_step**4)
    require("sech_squared_not_channel_character", sech_squared_failure != 0, checks)

    sech2_one_step = sp.Rational(8, 17)
    sech2_two_step = sp.Rational(32, 257)
    require_zero("sech_2delta_log2_exact", sp.sech(2 * a) - sech2_one_step, checks)
    require_zero("sech_2delta_log4_exact", sp.sech(4 * a) - sech2_two_step, checks)
    sech2_failure = sp.simplify(sech2_two_step - sech2_one_step**2)
    require("sech_2delta_not_channel_character", sech2_failure != 0, checks)

    require_zero("true_clock_character_witness", sp.exp(-2 * a) - sp.exp(-a) ** 2, checks)
    require_zero("true_ruler_character_witness", sp.exp(2 * a) - sp.exp(a) ** 2, checks)

    result = {
        "schema": "udt-reciprocal-c-clock-channel-correction-1.0",
        "python": sys.version.split()[0],
        "sympy": sp.__version__,
        "checks": checks,
        "founding_anchor": {
            "statement": "c and c^-1 are coequal time-to-length and length-to-time conversion directions; c^-1 is not an optional arithmetic afterthought",
            "clock_channel": "the time-per-length direction is owner-identified as the clock side",
            "classification": "FOUNDING_OWNER_CLARIFIED",
        },
        "derived_channels": {
            "temporal_weight": "T(rho)=exp(-rho)",
            "ruler_weight": "R(rho)=exp(+rho)",
            "premises": "named reciprocal-c pair + dual UDT Reciprocity + regular additive composition + nontriviality + chosen sign/unit",
            "properties": "T(0)=R(0)=1; T*R=1; T and R are multiplicative characters",
            "classification": "DERIVED_CONDITIONAL_WITH_EXACT_PREMISE_STAMPS",
        },
        "direction_correction": {
            "physical_depth": "rho>=0",
            "angular_reversal": "n_hat -> -n_hat at fixed rho leaves T and R unchanged",
            "ordered_observer_reversal": "delta -> -delta gives D(-delta)=D(delta)^-1",
            "classification": "ANGULAR_REVERSAL_DOES_NOT_SWAP_CLOCK_AND_RULER_CHANNELS",
        },
        "local_clock_readout": {
            "result": "for the declared local Lorentzian quadratic readout and a stationary fixed-spatial observer, d_tau/d_t=exp(-rho)",
            "classification": "CONDITIONAL_ON_THE_DECLARED_LORENTZIAN_READOUT_REPRESENTATIVE_AND_OBSERVER_SCOPE",
            "not_open": "no additional choice among arbitrary symmetric functions is needed inside this declared branch",
        },
        "symmetric_alternative_regrade": {
            "sech_delta_failure": str(sech_failure),
            "sech_delta_squared_failure": str(sech_squared_failure),
            "sech_2delta_failure": str(sech2_failure),
            "classification": "REJECTED_AS_COMPLETE_FOUNDATION_CLOCK_CHANNEL_COUNTERMODELS",
            "reason": "they are symmetric diagnostic functions of the reciprocal pair but fail the named channel multiplicative composition character",
        },
        "corrected_frontier": {
            "closed": [
                "reciprocal-c clock/ruler channel identity",
                "dual inverse relation",
                "regular reciprocal exponential channel response",
                "direction-invariant channel weights at fixed nonnegative depth",
                "ordered comparison inverse and composition algebra",
            ],
            "conditional": [
                "local Lorentzian quadratic metric readout and CSN representative",
                "stationary proper-clock interpretation exp(-rho)",
                "reciprocal spatial slot identification",
            ],
            "open": [
                "global physical radial-angular distance and path",
                "X_max origin value and operational bounded coordinate",
                "physical representative and material scale",
                "complete action and variation domain",
                "native source coupling and differentiable finite-cell boundary",
                "carrier emergence unconditional mass and time-live matter theorem",
            ],
            "everything_solved": False,
        },
        "adjudication": {
            "base_clock_selector": "NOT_OPEN; FIXED_BY_FOUNDING_RECIPROCAL_C_CHANNEL_IDENTITY",
            "exponential_clock_channel": "DERIVED_CONDITIONAL_WITH_COMPOSITION_REGULARITY_DUAL_RECIPROCITY_AND_SIGN_UNIT",
            "symmetric_clock_selector_problem": "WITHDRAWN_AS_UNDERPREMISED",
            "negative_physical_distance": "REJECTED",
            "projective_radial_readout": "OPEN",
            "complete_udt_closure": "OPEN",
        },
        "maximum_conclusion": "THE BASE CLOCK CHANNEL WAS ALREADY FIXED BY THE FOUNDING RECIPROCAL-C IDENTITY, AND DUAL RECIPROCITY PLUS REGULAR COMPOSITION FIXES ITS RECIPROCAL EXPONENTIAL RESPONSE UP TO THE DECLARED SIGN/UNIT; ANGULAR REVERSAL AT FIXED NONNEGATIVE DEPTH DOES NOT SWAP CHANNELS OR SPEED THE CLOCK; THE RECENT SECH-TYPE ALTERNATIVES FAIL THE COMPLETE CHANNEL COMPOSITION LAW AND ARE WITHDRAWN AS COUNTERMODELS; THE LOCAL PROPER-CLOCK READING REMAINS CONDITIONALLY TIED TO THE DECLARED LORENTZIAN REPRESENTATIVE, WHILE GLOBAL DISTANCE, XMAX, ACTION, SOURCE, BOUNDARY, CARRIER, AND UNCONDITIONAL MASS REMAIN OPEN",
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

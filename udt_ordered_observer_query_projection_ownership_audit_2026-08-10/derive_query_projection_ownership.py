#!/usr/bin/env python3
"""Exact algebra and ledgers for the ordered-query projection ownership audit."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(condition: bool, name: str, checks: dict[str, bool]) -> None:
    checks[name] = bool(condition)
    if not condition:
        raise AssertionError(name)


def write_tsv(name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    checks: dict[str, bool] = {}

    a, b = sp.symbols("a b", real=True)
    dk1, dk2, dp1, dp2 = sp.symbols("dk1 dk2 dp1 dp2", real=True)
    q = lambda dk, dp: a * dk + b * dp
    require(sp.expand(q(dk1 + dk2, dp1 + dp2) - q(dk1, dp1) - q(dk2, dp2)) == 0,
            "linear_density_characters_add", checks)

    exchange_defect = sp.expand(q(dk1, -dp1) + q(dk1, dp1))
    require(exchange_defect == 2 * a * dk1, "exchange_oddness_defect", checks)
    exchange_solution = sp.solve(
        [sp.diff(exchange_defect, dk1), q(0, 1) - 1], [a, b], dict=True
    )
    require(exchange_solution == [{a: 0, b: 1}], "exchange_and_normalization_select_phi", checks)
    require(sp.simplify(q(dk1, dp1).subs(exchange_solution[0]) - dp1) == 0,
            "selected_character_is_Delta_phi", checks)

    b1 = dk1 - dp1
    b2 = 2 * dk1
    require(sp.simplify(b2 / 2 - b1 - dp1) == 0, "reciprocal_root_reconstructs_phi", checks)
    require(sp.simplify(b2 / 2 - dk1) == 0, "area_density_reconstructs_kappa", checks)
    require(sp.simplify(b1.subs({dk1: 0, dp1: 1}) + 1) == 0,
            "clock_density_has_opposite_pure_depth_sign", checks)
    require(sp.simplify(b2.subs({dk1: 0, dp1: 1})) == 0,
            "area_density_vanishes_on_pure_reciprocal", checks)

    bp, bq, br = sp.symbols("beta_p beta_q beta_r", real=True)
    f = lambda x: x + x**3
    cob_pq = f(bq) - f(bp)
    cob_qr = f(br) - f(bq)
    cob_pr = f(br) - f(bp)
    require(sp.expand(cob_pq + cob_qr - cob_pr) == 0,
            "arbitrary_beta_endpoint_coboundary_telescopes", checks)
    c = sp.symbols("c", real=True)
    extended = dp1 + c * cob_pq
    require(sp.simplify(extended.subs({bp: 0, bq: 0}) - dp1) == 0,
            "broader_coboundary_family_preserves_pair_pure_reduction", checks)
    require(sp.diff(extended, c) == cob_pq, "broader_coboundary_family_is_nontrivial", checks)

    theta, m = sp.symbols("theta m", real=True)
    cover_character = m * theta
    periodic_defect = sp.expand(cover_character.subs(theta, theta + 2 * sp.pi) - cover_character)
    require(periodic_defect == 2 * sp.pi * m, "SO2_cover_character_period_defect", checks)
    require(sp.solve(periodic_defect, m) == [0], "SO2_has_no_nontrivial_continuous_real_character", checks)

    lam, dphi, ang1, ang2 = sp.symbols("lambda dphi ang1 ang2", real=True)
    rot = lambda x: sp.Matrix([[sp.cos(x), -sp.sin(x)], [sp.sin(x), sp.cos(x)]])
    rep1 = sp.exp(lam * dp1) * rot(ang1)
    rep2 = sp.exp(lam * dp2) * rot(ang2)
    rep12 = sp.exp(lam * (dp1 + dp2)) * rot(ang1 + ang2)
    require(sp.simplify(sp.trigsimp(rep2 * rep1 - rep12)) == sp.zeros(2),
            "screen_representation_reconstructed_and_composes", checks)

    h1 = sp.diag(sp.Rational(-3, 16), 4)
    det1 = h1.det()
    phi1 = sp.log((-det1) / h1[0, 0] ** 2) / 4
    require(sp.simplify(phi1 - sp.log(sp.Rational(64, 3)) / 4) == 0,
            "mixing_witness_one_modulates_phi", checks)
    h2 = sp.Matrix([[sp.Rational(-3, 16), sp.Rational(1, 12)],
                    [sp.Rational(1, 12), sp.Rational(37, 9)]])
    det2 = h2.det()
    phi2 = sp.log((-det2) / h2[0, 0] ** 2) / 4
    beta2 = sp.cancel(h2[0, 1] / h2[0, 0])
    require(det2 == sp.Rational(-7, 9), "mixing_witness_two_determinant", checks)
    require(sp.simplify(phi2 - sp.log(sp.Rational(1792, 81)) / 4) == 0,
            "mixing_witness_two_modulates_phi", checks)
    require(beta2 == sp.Rational(-4, 9), "mixing_witness_two_retains_shift", checks)

    founding = (ROOT / "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md").read_text(
        encoding="utf-8"
    )
    for name, token in (
        ("source_has_time_length_pair", "dimension-matched temporal/radial coframe pair"),
        ("source_has_inverse_pairing", "u(\\Delta)v(\\Delta)=1"),
        ("source_has_composition", "P(\\Delta_1+\\Delta_2)=P(\\Delta_1)P(\\Delta_2)"),
        ("source_marks_sign_unit_chosen", "Sign and unit of $\\phi$"),
        ("source_does_not_claim_profile", "does not yet derive a unique action, the profile $\\phi(r)$"),
    ):
        require(token in founding, name, checks)

    classifications = [
        ("Q01", "CONDITIONAL_COMPLETE_QUERY_OUTPUT_NOT_FOUNDING_OWNED", "full panel needs supplied pair map path and screen typing"),
        ("Q02", "REALIZED_FOUNDING_PROJECTION_CONDITIONAL_UNIQUE_WITHIN_DENSITY_CHARACTER_CLASS", "after a complete calibrated query supplies the pair relation exchange oddness and normalization uniquely give Delta_phi"),
        ("Q03", "DERIVED_GEOMETRIC_CHARACTER_NOT_FOUNDING_RECIPROCAL_OUTPUT", "common scale is real state but exchange even"),
        ("Q04", "DERIVED_CLOCK_DENSITY_NOT_FOUNDING_RECIPROCAL_OUTPUT", "contains common scale and has opposite pure-depth sign"),
        ("Q05", "DERIVED_AREA_DENSITY_NOT_FOUNDING_RECIPROCAL_OUTPUT", "measures common scale and vanishes on pure reciprocal depth"),
        ("Q06", "CONDITIONAL_QUERY_STATE_NOT_CHARACTER", "shift needs event pairing and ruler evolution"),
        ("Q07", "CONDITIONAL_PATH_INSTRUMENT_NOT_REAL_SCALAR", "normal carry needs a path and endpoint screen fibers"),
        ("Q08", "DERIVED_REPRESENTATION_NOT_INDEPENDENT_QUERY", "reconstructed from Delta_phi U variance and lambda"),
        ("Q09", "CHARACTER_FAMILY_REDUCED_TO_Q02_BY_FOUNDING_GATES", "continuous density characters are linear and gates set a=0 b=1"),
        ("Q10", "MATHEMATICALLY_SURVIVES_BROADER_GROUPOID_BUT_UNOWNED", "arbitrary endpoint scalar requires a new measurement function"),
        ("Q11", "UNSELECTED_MICROPHONE_FAMILIES", "free coefficient and path or endpoint choice remain ownerless"),
        ("Q12", "OPEN_NO_PHYSICAL_REGIME_MAP", "no derived regime labels thresholds or switch"),
        ("Q13", "OPEN_LARGER_OWNER_NOT_DERIVED", "on-shell or bootstrap selection cannot be assumed"),
        ("Q14", "OPEN_OUTSIDE_AUDIT", "native source and coupling are absent"),
    ]
    write_tsv(
        "QUERY_PROJECTION_CLASSIFICATION.tsv",
        ["query_id", "disposition", "reason"],
        [{"query_id": qid, "disposition": disposition, "reason": reason}
         for qid, disposition, reason in classifications],
    )

    ownership = [
        ("M01", "kappa", "pair_metric_state", "DERIVED_CONDITIONAL", "pair_area or common-scale instrument", "NOT_FOUNDING_RECIPROCAL_OUTPUT"),
        ("M02", "phi", "reciprocal_density_state", "DERIVED_ON_SUPPLIED_PAIR_METRIC", "terminal reciprocal c_E instrument", "FOUNDING_PROJECTION_REALIZATION_CONDITIONAL"),
        ("M03", "beta", "event_pairing_shift_state", "DERIVED_ON_SUPPLIED_PAIR_METRIC", "paired events and ruler evolution", "CONDITIONAL_ENRICHED_QUERY"),
        ("M04", "U_gamma", "normal_isometry_arrow", "DERIVED_AFTER_PATH", "path plus endpoint screen frames", "CONDITIONAL_PATH_QUERY"),
        ("M05", "Delta_kappa_Delta_phi_U", "typed_arrow_shadow", "DERIVED_CONDITIONAL", "common matched pair query", "NOT_ONE_FOUNDING_SCALAR"),
        ("M06", "regime_dependent_projection", "measurement_policy", "OPEN", "physical regime map and selector", "NOT_DERIVED"),
    ]
    write_tsv(
        "MEASUREMENT_OWNERSHIP_ATLAS.tsv",
        ["measurement_id", "object", "type", "geometric_status", "required_instrument", "founding_ownership"],
        [dict(zip(
            ["measurement_id", "object", "type", "geometric_status", "required_instrument", "founding_ownership"],
            row,
        )) for row in ownership],
    )

    signatures = [
        ("F01", "supplied_ordered_signed_depth_delta", "reciprocal_operator_D_delta", "FOUNDING_DERIVED_ABSTRACT"),
        ("F02", "reciprocal_clock_ruler_channel_labels", "inverse_channel_weights", "FOUNDING_DERIVED"),
        ("F03", "matched_abstract_depths", "composition_reversal_identity", "FOUNDING_DERIVED"),
        ("F04", "c_E_time_length_conversion", "terminal_clock_ruler_unit_calibration", "OBSERVED_CALIBRATION_NOT_SELECTOR"),
        ("F05", "complete_declared_enriched_query", "metric_constructed_pair_geometry_after_query", "CONDITIONAL_QUERY_ENRICHMENT"),
    ]
    write_tsv(
        "FOUNDING_SIGNATURE_RESULT.tsv",
        ["signature_id", "input", "output", "ruling"],
        [dict(zip(["signature_id", "input", "output", "ruling"], row)) for row in signatures],
    )

    result = {
        "schema_version": 1,
        "status": "PASS",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "founding_query_output": "Delta_phi_AS_CONDITIONAL_REALIZATION_OF_FOUNDING_PROJECTION_WITHIN_CONTINUOUS_REAL_TWO_DENSITY_CHARACTER_CLASS",
        "uniqueness_scope": "UNIQUE_ONLY_WITHIN_FOUNDED_DENSITY_CHARACTERS_NOT_ALL_COMPLETE_STATE_COBBOUNDARIES",
        "complete_panel": "CONDITIONAL_GEOMETRIC_STATE_AND_TYPED_QUERY_FAMILY_NOT_FOUNDING_SINGLE_OUTPUT",
        "kappa_status": "RETAINED_COMPLETE_STATE_NOT_DELETED_BY_RECIPROCAL_PROJECTION",
        "beta_status": "CONDITIONAL_QUERY_STATE_NOT_STANDALONE_CHARACTER",
        "angular_status": "CONDITIONAL_PATH_INSTRUMENT_WITH_ZERO_CONTINUOUS_REAL_SO2_CHARACTER",
        "phi_orchestra": "UPSTREAM_COMPLETE_PAIR_METRIC_MODULATION_RETAINED",
        "physical_regime_policy": None,
        "conductor_owner": None,
        "maximum_ruling": "FOUNDED_PROJECTION_ONLY_REALIZATION_CONDITIONAL__Delta_phi_UNIQUE_WITHIN_DECLARED_CHARACTER_CLASS_AFTER_COMPLETE_CALIBRATED_QUERY_SUPPLIES_PAIR_RELATION__MULTICHANNEL_MEASUREMENT_AND_REGIME_POLICY_OPEN",
    }
    assert result["passed"] == result["total"]
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

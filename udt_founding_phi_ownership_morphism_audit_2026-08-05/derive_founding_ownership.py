#!/usr/bin/env python3
"""Exact primary algebra for the preregistered founding ownership routes."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
MAXIMUM_CONCLUSION = (
    "DERIVED_FOUNDING_OBJECT_IS_A_RELATIONAL_RECIPROCAL_CHARACTER_ON_SUPPLIED_DEPTH__"
    "DERIVED_POINTWISE_PHI_IS_A_PRESENTATION_POTENTIAL_ON_THE_SUPPLIED_FACTORIZED_ARCHITECTURE__"
    "CONDITIONAL_STATIONARY_KILLING_AND_SUPPLIED_QUERY_REALIZATIONS__"
    "NO_UNIVERSAL_FOUNDED_PHI_OWNERSHIP_MORPHISM_IN_FROZEN_NATIVE_SOURCES"
)


def d(z: sp.Rational) -> sp.Matrix:
    return sp.diag(1 / z, z)


def matrix_json(value: sp.Matrix) -> list[list[str]]:
    return [[str(value[i, j]) for j in range(value.cols)] for i in range(value.rows)]


def record(checks: dict[str, bool], name: str, condition: object) -> None:
    value = bool(condition)
    checks[name] = value
    if not value:
        raise AssertionError(name)


def write_tsv(path: Path, rows: list[tuple[str, str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["route_id", "classification", "exact_reason"])
        writer.writerows(rows)


def main() -> None:
    checks: dict[str, bool] = {}
    eta = sp.diag(-1, 1)
    pairing = sp.Matrix([[0, 1], [1, 0]])

    # Founded reciprocal character on an already supplied positive depth ratio.
    z1, z2 = sp.Rational(2), sp.Rational(5)
    record(checks, "character_composes", d(z2) * d(z1) == d(z1 * z2))
    record(checks, "character_reverses", d(1 / z1) == d(z1).inv())
    record(checks, "character_preserves_founding_pairing", d(z1).T * pairing * d(z1) == pairing)
    record(checks, "character_determinant_one", d(z1).det() == 1)
    record(checks, "nonzero_character_not_eta_isometry", d(z1).T * eta * d(z1) != eta)

    # Continuous additive comparison fixes an exponential only after the relative depth coordinate
    # and its normalization are supplied. Two distinct slopes obey the same group laws.
    x, y = sp.symbols("x y", positive=True)
    for power in (1, 2):
        char_x = sp.diag(x ** (-power), x**power)
        char_y = sp.diag(y ** (-power), y**power)
        char_xy = sp.diag((x * y) ** (-power), (x * y) ** power)
        record(checks, f"normalization_family_composes_{power}", char_y * char_x == char_xy)
        record(checks, f"normalization_family_reverses_{power}", char_x.subs(x, 1 / x) == char_x.inv())
    record(
        checks,
        "depth_normalization_not_selected",
        sp.diag(x**-1, x) != sp.diag(x**-2, x**2),
    )
    c = sp.symbols("c", positive=True)
    record(checks, "c_not_in_character_parameter", c not in d(z1).free_symbols)

    # Exact local factorization countermodel: two different phi/depth coordinates give the same
    # complete coframe when the reference presentation changes.
    z, h = sp.Rational(3), sp.Rational(7)
    reference = sp.Matrix([[2, 1], [1, 3]])
    theta = d(z) * reference
    shifted_reference = d(h).inv() * reference
    shifted_theta = d(z * h) * shifted_reference
    record(checks, "complete_coframe_unchanged_under_depth_shift", theta == shifted_theta)
    record(checks, "pointwise_depth_representative_changes", z * h != z)

    # Two endpoints: relative potential depth itself changes under independent reference shifts,
    # while the complete physical transition remains fixed.
    zp, zq = sp.Rational(2), sp.Rational(11)
    hp, hq = sp.Rational(3), sp.Rational(5)
    ref_p = sp.Matrix([[2, 0], [1, 1]])
    ref_q = sp.Matrix([[1, 2], [0, 3]])
    theta_p, theta_q = d(zp) * ref_p, d(zq) * ref_q
    physical_arrow = theta_q * theta_p.inv()
    depth_before = zq / zp
    depth_after = (zq * hq) / (zp * hp)
    ref_p_after, ref_q_after = d(hp).inv() * ref_p, d(hq).inv() * ref_q
    theta_p_after = d(zp * hp) * ref_p_after
    theta_q_after = d(zq * hq) * ref_q_after
    physical_arrow_after = theta_q_after * theta_p_after.inv()
    record(checks, "relative_potential_depth_changes", depth_before != depth_after)
    record(checks, "endpoint_complete_coframes_unchanged", theta_p == theta_p_after and theta_q == theta_q_after)
    record(checks, "complete_physical_arrow_unchanged", physical_arrow == physical_arrow_after)

    # The presentation orbit is transitive on the positive scalar representative. It is an exact
    # physical-presentation class, but cannot by itself return a named scalar clock weight.
    target_depth = sp.Rational(13, 4)
    chosen_ratio = target_depth / depth_before
    record(checks, "orbit_reaches_arbitrary_positive_depth", depth_before * chosen_ratio == target_depth)
    record(checks, "orbit_contains_distinct_depths", target_depth != depth_before)

    # Endpoint composition is exact for every supplied potential and leaves an additive constant.
    za, zb, zc = sp.Rational(2), sp.Rational(7), sp.Rational(19)
    record(checks, "endpoint_potential_composes", (zc / zb) * (zb / za) == zc / za)
    record(checks, "endpoint_common_scale_cancels", ((5 * zc) / (5 * zb)) == zc / zb)

    # A nonnegative symmetric distance magnitude cannot itself be the reversal-odd signed depth.
    magnitude_ab = abs(sp.Rational(9) - sp.Rational(2))
    magnitude_ba = abs(sp.Rational(2) - sp.Rational(9))
    record(checks, "distance_magnitude_is_symmetric", magnitude_ab == magnitude_ba and magnitude_ab > 0)
    record(checks, "distance_magnitude_not_signed_depth", magnitude_ba != -magnitude_ab)

    # Stationary branch-local Killing/lapse readout: N(q)/N(p) is the lapse ratio, while the
    # source-consistent signed depth has exp(delta_K)=N(p)/N(q).  Keep the inverse channels explicit.
    na, nb, nc, scale = map(sp.Rational, (2, 3, 11, 7))
    lab, lbc, lac = nb / na, nc / nb, nc / na
    dab, dbc, dac = na / nb, nb / nc, na / nc
    record(checks, "stationary_killing_lapse_ratio_composes", lbc * lab == lac)
    record(checks, "stationary_depth_ratio_composes", dbc * dab == dac)
    record(checks, "stationary_depth_is_inverse_lapse", dab == 1 / lab)
    record(checks, "stationary_depth_ratio_reverses", (nb / na) == 1 / dab)
    record(checks, "stationary_depth_normalization_cancels", (scale * na) / (scale * nb) == dab)
    record(checks, "different_stationary_branch_changes_depth", sp.Rational(5, 2) != dab)

    # Levi-Civita transport is eta-isometric; the unbalanced physical-metric reciprocal scaling is
    # not. Therefore transport cannot silently manufacture nonzero depth.
    boost = sp.Matrix([[sp.Rational(5, 4), sp.Rational(3, 4)], [sp.Rational(3, 4), sp.Rational(5, 4)]])
    record(checks, "metric_transport_control_is_eta_isometry", boost.T * eta * boost == eta)
    record(checks, "reciprocal_dilation_differs_from_metric_transport", d(z1).T * eta * d(z1) != eta)

    # The working global/local relation is not a function when one complete geometry admits two
    # depth presentations. This is a type countermodel, not a physical solution claim.
    relation = {"G0": {"depth_a", "depth_b"}}
    record(checks, "working_relation_can_be_multivalued", len(relation["G0"]) == 2)
    record(checks, "multivalued_relation_not_ownership_function", len(relation["G0"]) != 1)

    routes = [
        ("M01", "FOUNDING_DERIVED_ABSTRACT_GIVEN_SUPPLIED_DEPTH", "the character is exact but the observer-pair depth value is an input"),
        ("M02", "CONDITIONAL_TYPED_PATH_COCYCLE__NATIVE_DEPTH_OPEN", "path composition is exact only after an additive depth cocycle is supplied"),
        ("M03", "CONDITIONAL_BRANCH_LOCAL_KILLING_DEPTH__NO_UNIVERSAL_EXTRACTION", "stationary intrinsic Killing norm ratios own depth on that branch; factorization defeats universal extraction"),
        ("M04", "CONDITIONAL_EXTRA_REFERENCE", "a fixed physical reference removes shifts but is not founded"),
        ("M05", "DERIVED_CHARACTER_ON_SUPPLIED_PAIR__NO_REPRESENTATIVE_SELECTION", "pair orientation types the action while every positive depth remains admissible"),
        ("M06", "CONDITIONAL_OPERATIONAL_INPUT__NOT_METRIC_DERIVED", "a measured or declared pair depth completes the arrow but is additional physical data"),
        ("M07", "DERIVED_PRESENTATION_ORBIT__INSUFFICIENT_FOR_SCALAR_READOUT", "the invariant orbit contains arbitrary positive scalar representatives"),
        ("M08", "NOT_DERIVED_EXTRA_NORMALIZATION", "no founded seam endpoint or zero fixes the representative"),
        ("M09", "DERIVED_CALIBRATION_AND_CHARACTER__DEPTH_UNIT_AND_ASSIGNMENT_OPEN", "c dimension-matches clock and ruler but the founding record chooses the sign and unit of phi"),
        ("M10", "WORKING_RELATION_NONFUNCTIONAL__NO_OWNERSHIP_SELECTION", "mutual admissibility is a relation and can remain multivalued without a return law"),
    ]
    record(checks, "route_count_10", len(routes) == 10)
    record(checks, "route_ids_complete", [row[0] for row in routes] == [f"M{i:02d}" for i in range(1, 11)])
    write_tsv(HERE / "ROUTE_OUTCOMES.tsv", routes)

    witnesses = {
        "depth_before": str(depth_before),
        "depth_after": str(depth_after),
        "target_depth_in_same_orbit": str(target_depth),
        "physical_arrow": matrix_json(physical_arrow),
        "physical_arrow_after": matrix_json(physical_arrow_after),
        "stationary_killing_lapse_ratios": {"ab": str(lab), "bc": str(lbc), "ac": str(lac)},
        "stationary_depth_ratios": {"ab": str(dab), "bc": str(dbc), "ac": str(dac)},
        "factorization_theta": matrix_json(theta),
        "factorization_theta_shifted": matrix_json(shifted_theta),
        "normalization_family_powers": [1, 2],
    }
    (HERE / "WITNESSES.json").write_text(json.dumps(witnesses, indent=2, sort_keys=True) + "\n")
    result = {
        "schema": "udt.founding_phi_ownership.primary.v1",
        "status": "PASS",
        "sympy": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "route_count": len(routes),
        "maximum_conclusion": MAXIMUM_CONCLUSION,
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

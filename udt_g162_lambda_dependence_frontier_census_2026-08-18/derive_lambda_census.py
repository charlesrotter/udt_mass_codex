#!/usr/bin/env python3
"""Exact G162 residual-Lorentz dependency census."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE_SNAPSHOT = "ee261b38"
OUTCOME_CLASS = (
    "SECOND_REPAIR_SCALAR_KERNEL_DESCENDS_TO_QUOTIENT__CANONICAL_ENDPOINT_CARRY_EXACT__"
    "JOINED_ROUTE_FRAME_CHANNEL_RETAINS_LAMBDA__HISTORY_GAP_UNCHANGED"
)
LANDING = (
    "BOUNDED_SCALAR_RECIPROCAL_KERNEL_IS_RESIDUAL_LORENTZ_INVARIANT__"
    "UNIQUE_POSITIVE_ENDPOINT_ROOTS_GIVE_EXACT_FLAT_CALIBRATION_CARRY__"
    "GENERAL_COMPATIBLE_CARRY_FACTORS_AS_RB_INVERSE_LAMBDA_RA__JOINED_C_"
    "AND_GAMMA_RETAIN_SUPPLIED_ROUTE_FRAME_RAPIDITY__NORMAL_HOLONOMY_"
    "JACOBI_AND_EXTRINSIC_CHANNELS_REMAIN_SEPARATELY_TYPED__RAPIDITY_"
    "SELECTION_RETIRED_AS_SCALAR_KERNEL_GATE_ONLY__PHYSICAL_HISTORY_QUERY_"
    "PATH_CARRY_XMAX_AND_COMPLETION_OPEN"
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_manifest() -> int:
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == 13
    assert [row["source_id"] for row in rows] == [f"S{i:02d}" for i in range(1, 14)]
    for row in rows:
        payload = subprocess.run(
            ["git", "show", f"{SOURCE_SNAPSHOT}:{row['path']}"], cwd=ROOT,
            check=True, stdout=subprocess.PIPE,
        ).stdout
        assert len(payload) == int(row["bytes"]), row["source_id"]
        assert hashlib.sha256(payload).hexdigest() == row["sha256"], row["source_id"]
    return len(rows)


def assert_zero(value: sp.Matrix | sp.Expr) -> None:
    if isinstance(value, sp.MatrixBase):
        assert all(sp.simplify(entry) == 0 for entry in value)
    else:
        assert sp.simplify(value) == 0


def root(t: sp.Expr, ell: sp.Expr, beta: sp.Expr) -> sp.Matrix:
    return sp.Matrix([[t, t * beta], [0, ell]])


def root_from_metric(h: sp.Matrix) -> sp.Matrix:
    t = sp.sqrt(-h[0, 0])
    beta = sp.cancel(h[0, 1] / h[0, 0])
    ell = sp.sqrt(sp.simplify(h[1, 1] - h[0, 1] ** 2 / h[0, 0]))
    return root(t, ell, beta)


def boost(a: sp.Expr) -> sp.Matrix:
    """SO+(1,1) boost parameterized by a positive scale a=exp(theta)."""
    return sp.Matrix([[(a + 1 / a) / 2, (a - 1 / a) / 2],
                      [(a - 1 / a) / 2, (a + 1 / a) / 2]])


def terminal(h: sp.Matrix) -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    minus_det = -h.det()
    kappa = sp.log(minus_det) / 4
    phi = sp.log(minus_det / h[0, 0] ** 2) / 4
    beta = sp.cancel(h[0, 1] / h[0, 0])
    ceff = sp.cancel(-h[0, 0] / sp.sqrt(minus_det))
    position = sp.tanh(phi)
    return kappa, phi, beta, ceff, position


def census_rows() -> list[dict[str, str]]:
    q = "QUOTIENT_OWNED__LAMBDA_INVARIANT"
    s = "CANONICAL_ENDPOINT_SECTION__LAMBDA_SET_TO_IDENTITY_BY_REBUILD"
    r = "SUPPLIED_ROUTE_FRAME_CHANNEL__LAMBDA_SENSITIVE"
    g = "REPRESENTATIVE_COFRAME_GAUGE_CHANNEL__NOT_A_QUOTIENT_OBSERVABLE"
    x = "INDEPENDENT_PATH_OR_EXTRINSIC_CHANNEL__NOT_REDUCIBLE_TO_TANGENT_LAMBDA"
    o = "HISTORY_VALUE_OR_EVOLUTION_OPEN__CENSUS_DOES_NOT_SELECT"
    return [
        {"id": "D01", "object": "complete_pair_metric_h", "class": q,
         "reason": "M^T h_B M=h_A cancels every Lambda in SOplus(1,1)", "source": "S01,S09,S11"},
        {"id": "D02", "object": "pair_first_jet_h_doth", "class": q,
         "reason": "differentiate the exact metric identity for arbitrary live Lambda", "source": "S01,S09,S10,S11"},
        {"id": "D03", "object": "terminal_T_L_beta", "class": q,
         "reason": "unique calibrated functions of h", "source": "S01,S09,S11,S12"},
        {"id": "D04", "object": "terminal_kappa_phi_and_rates", "class": q,
         "reason": "functions of h,doth in the supplied calibrated chart", "source": "S01,S09,S10"},
        {"id": "D05", "object": "conditional_pair_c_eff_over_c_E", "class": q,
         "reason": "equals exp(-2 phi_pair) from h", "source": "S01,S09"},
        {"id": "D06", "object": "working_pair_position_chi_tanh_phi", "class": q,
         "reason": "depends on terminal phi and supplied Xmax only", "source": "S02,S04"},
        {"id": "D07", "object": "pair_position_differential_and_metric_frame_response", "class": q,
         "reason": "depends on quotient history derivatives, not vertical rapidity", "source": "S04,S05"},
        {"id": "D08", "object": "pair_volume_density_and_positive_half_density", "class": q,
         "reason": "sqrt(-det h)=TL and fourth-root sqrt(TL) both factor through h", "source": "S06"},
        {"id": "D09", "object": "joined_sigma_and_raw_carry_determinant_grading", "class": q,
         "reason": "C=Lambda makes joined sigma zero; half log det M=kappa_A-kappa_B", "source": "S06,S10"},
        {"id": "D10", "object": "canonical_endpoint_calibration_carry_Mcal", "class": s,
         "reason": "R_B^-1 R_A is exact and composable but has joined Lambda=I", "source": "S07,S11"},
        {"id": "D11", "object": "general_compatible_pair_carry_M", "class": r,
         "reason": "M=R_B^-1 Lambda R_A retains supplied rapidity", "source": "S10,S11"},
        {"id": "D12", "object": "supplied_carry_right_rate_K_BA", "class": r,
         "reason": "K=dot M M^-1 retains supplied endpoint and Lambda-rate data", "source": "S10"},
        {"id": "D13", "object": "metric_symmetric_skew_rate_split_S_h_A_h", "class": g,
         "reason": "presentation split; only the complete carried first jet is covariant", "source": "S10"},
        {"id": "D14", "object": "joined_transition_C", "class": r,
         "reason": "C=R_B M R_A^-1=Lambda is endpoint-gauge invariant", "source": "S10"},
        {"id": "D15", "object": "joined_rate_Gamma", "class": r,
         "reason": "Gamma=dot Lambda Lambda^-1 retains rapidity rate", "source": "S10"},
        {"id": "D16", "object": "three_observer_defect_F_and_rate_K_F", "class": r,
         "reason": "finite and first-order route closure retain supplied carry data", "source": "S10"},
        {"id": "D17", "object": "complete_coframe_score_components", "class": g,
         "reason": "upstream representative data transform inhomogeneously; only h,doth descend", "source": "S08,S09"},
        {"id": "D18", "object": "normal_and_screen_holonomy_Ugamma", "class": x,
         "reason": "separate path-labelled SO(2) channel, not tangent SOplus(1,1)", "source": "S13"},
        {"id": "D19", "object": "Jacobi_and_ambient_transport", "class": x,
         "reason": "query/congruence/path-labelled channels", "source": "S03,S12"},
        {"id": "D20", "object": "II_CII_and_conditional_eigenflag", "class": x,
         "reason": "immersion-owned extrinsic data; flag covariant but not scalar-kernel input", "source": "S11,S12"},
        {"id": "D21", "object": "physical_selection_or_evolution_of_B_Q_S_Y_Z_kappa_histories", "class": o,
         "reason": "supplied kappa is D04; census selects no physical values or evolution", "source": "S01,S05,S08"},
        {"id": "D22", "object": "physical_query_path_carry_Xmax_and_completion", "class": o,
         "reason": "not owned by residual-Lorentz factorization", "source": "S02,S05,S10,S11,S12"},
    ]


def exact_checks() -> dict[str, object]:
    checks: list[str] = []
    eta = sp.diag(-1, 1)
    ta, la, ba, tb, lb, bb = sp.symbols("ta la ba tb lb bb", positive=True)
    z = sp.symbols("z", positive=True)
    ra, rb = root(ta, la, ba), root(tb, lb, bb)
    ha, hb = ra.T * eta * ra, rb.T * eta * rb
    lam = boost(z)
    assert_zero(lam.T * eta * lam - eta)
    assert_zero(lam.det() - 1)
    checks.append("residual_factor_is_proper_orthochronous_lorentz")

    m = rb.inv() * lam * ra
    assert_zero(m.T * hb * m - ha)
    assert_zero(rb * m * ra.inv() - lam)
    checks.append("general_compatible_carry_factorization_and_joined_transition")

    # Reverse direction: compatibility forces the joined factor into O(1,1).
    m_reverse = sp.Matrix([[2, 1], [1, 1]])
    h_reverse = m_reverse.T * eta * m_reverse
    r_reverse = root_from_metric(h_reverse)
    assert_zero(r_reverse.T * eta * r_reverse - h_reverse)
    lam_reverse = m_reverse * r_reverse.inv()
    assert_zero(lam_reverse.T * eta * lam_reverse - eta)
    assert_zero(m_reverse - lam_reverse * r_reverse)
    checks.append("compatible_carry_implies_joined_lorentz_factor_reverse_direction")

    mcal = rb.inv() * ra
    assert_zero(mcal.T * hb * mcal - ha)
    assert_zero(rb * mcal * ra.inv() - sp.eye(2))
    checks.append("canonical_endpoint_section_is_metric_compatible_and_joined_identity")

    tc, lc, bc = sp.symbols("tc lc bc", positive=True)
    rc = root(tc, lc, bc)
    m_ba_cal, m_cb_cal = rb.inv() * ra, rc.inv() * rb
    assert_zero(m_cb_cal * m_ba_cal - rc.inv() * ra)
    checks.append("canonical_endpoint_section_three_observer_composition")

    z1, z2 = sp.symbols("z1 z2", positive=True)
    lam_ba, lam_cb = boost(z1), boost(z2)
    m_ba = rb.inv() * lam_ba * ra
    m_cb = rc.inv() * lam_cb * rb
    m_ca = m_cb * m_ba
    assert_zero(rc * m_ca * ra.inv() - lam_cb * lam_ba)
    checks.append("general_joined_transition_three_observer_composition")

    # All terminal scalar objects see the same endpoint metric for every Lambda.
    carried = m.T * hb * m
    assert_zero(carried - ha)
    for left, right in zip(terminal(carried), terminal(ha)):
        assert_zero(left - right)
    checks.append("terminal_kappa_phi_beta_ceff_and_position_lambda_invariant")

    assert_zero(m.det() - ra.det() / rb.det())
    assert_zero(sp.sqrt(-ha.det()) - ta * la)
    assert_zero((-ha.det()) ** sp.Rational(1, 4) - sp.sqrt(ta * la))
    checks.append("half_density_and_determinant_scale_character_lambda_invariant")

    # Live first jet: an arbitrary varying Lambda cancels pointwise and after differentiation.
    u = sp.symbols("u", real=True)
    ra_live = root(2 + u, 3 + u**2, 1 + u / 5)
    rb_live = root(4 + u**2, 5 + u, 2 - u / 7)
    lam_live = boost(sp.exp(u / 9))
    ha_live, hb_live = ra_live.T * eta * ra_live, rb_live.T * eta * rb_live
    m_live = rb_live.inv() * lam_live * ra_live
    carried_live = m_live.T * hb_live * m_live
    assert_zero(carried_live - ha_live)
    assert_zero(sp.diff(carried_live, u) - sp.diff(ha_live, u))
    checks.append("pair_metric_and_first_jet_lambda_invariant_for_live_sweep")

    # The K self-adjoint/skew split is a presentation split; only its symmetric part reaches hdot.
    k00, k01, k10, k11 = sp.symbols("k00 k01 k10 k11", real=True)
    kval = sp.Matrix([[k00, k01], [k10, k11]])
    kdag = ha.inv() * kval.T * ha
    sh, ah = (kval + kdag) / 2, (kval - kdag) / 2
    assert_zero(kval.T * ha + ha * kval - 2 * ha * sh)
    assert_zero(ah.T * ha + ha * ah)
    checks.append("metric_self_adjoint_skew_rate_split_typed_exactly")

    c_live = rb_live * m_live * ra_live.inv()
    gamma_live = sp.diff(c_live, u) * c_live.inv()
    assert_zero(c_live - lam_live)
    assert gamma_live != sp.zeros(2)
    c_cal_live = rb_live * (rb_live.inv() * ra_live) * ra_live.inv()
    assert_zero(c_cal_live - sp.eye(2))
    assert_zero(sp.diff(c_cal_live, u))
    checks.append("joined_C_and_Gamma_retain_live_rapidity_while_section_is_flat")

    # Flat overlap counterexample: endpoint rebuilding cannot recover an actual boost.
    witness = boost(sp.Rational(2))
    assert_zero(witness.T * eta * witness - eta)
    assert witness != sp.eye(2)
    assert sp.eye(2).T * eta * sp.eye(2) == eta
    checks.append("equal_endpoint_metrics_do_not_determine_actual_overlap_boost")

    # Extrinsic spectral data are tangent-frame covariant, not scalar-kernel inputs.
    cii = sp.diag(1, 4)
    cii_recharted = witness.inv() * cii * witness
    assert_zero(cii_recharted.trace() - cii.trace())
    assert_zero(cii_recharted.det() - cii.det())
    assert cii_recharted != cii
    checks.append("extrinsic_CII_is_conjugacy_covariant_not_tangent_scalar")

    rows = census_rows()
    assert len(rows) == 22
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["class"]] = counts.get(row["class"], 0) + 1
    assert counts == {
        "QUOTIENT_OWNED__LAMBDA_INVARIANT": 9,
        "CANONICAL_ENDPOINT_SECTION__LAMBDA_SET_TO_IDENTITY_BY_REBUILD": 1,
        "SUPPLIED_ROUTE_FRAME_CHANNEL__LAMBDA_SENSITIVE": 5,
        "REPRESENTATIVE_COFRAME_GAUGE_CHANNEL__NOT_A_QUOTIENT_OBSERVABLE": 2,
        "INDEPENDENT_PATH_OR_EXTRINSIC_CHANNEL__NOT_REDUCIBLE_TO_TANGENT_LAMBDA": 3,
        "HISTORY_VALUE_OR_EVOLUTION_OPEN__CENSUS_DOES_NOT_SELECT": 2,
    }
    checks.append("twenty_two_object_dependency_census_matches_repaired_inventory")

    assert len(checks) == 14
    return {
        "exact_checks": len(checks),
        "exact_check_names": checks,
        "census_rows": len(rows),
        "class_counts": counts,
        "scalar_kernel_lambda_invariant": True,
        "canonical_endpoint_section_exact_and_composable": True,
        "canonical_endpoint_section_is_physical_overlap_or_path": False,
        "joined_C_Gamma_lambda_sensitive": True,
        "all_active_objects_lambda_invariant": False,
        "normal_jacobi_extrinsic_channels_reduced_to_tangent_lambda": False,
        "rapidity_selection_remains_scalar_kernel_gate": False,
        "physical_history_derived": False,
        "physical_query_path_carry_derived": False,
    }


def write_census(rows: list[dict[str, str]]) -> None:
    with (HERE / "DEPENDENCY_CENSUS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("id", "object", "class", "reason", "source"),
                                delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = census_rows()
    write_census(rows)
    result = {
        "status": "PASS",
        "registered_outcome_class": OUTCOME_CLASS,
        "landing": LANDING,
        "source_count": verify_manifest(),
        **exact_checks(),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

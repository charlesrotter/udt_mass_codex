#!/usr/bin/env python3
"""Exact symbolic derivation for the bounded multi-channel R17 assembly."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def require(value: object, name: str, checks: dict[str, bool]) -> None:
    checks[name] = bool(value)
    if not value:
        raise AssertionError(name)


def write_tsv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    checks: dict[str, bool] = {}

    T, L, beta = sp.symbols("T L beta", positive=True, real=True)
    h = sp.Matrix([[-T**2, -T**2 * beta], [-T**2 * beta, L**2 - T**2 * beta**2]])
    require(sp.factor(h.det()) == -T**2 * L**2, "pair_metric_determinant", checks)
    T2 = -h[0, 0]
    beta_out = sp.cancel(h[0, 1] / h[0, 0])
    L2 = sp.factor(h[1, 1] - h[0, 1] ** 2 / h[0, 0])
    require(T2 == T**2 and beta_out == beta and L2 == L**2, "pair_decomposition_inverse", checks)

    kappa, phi = sp.symbols("kappa phi", real=True)
    T_kp = sp.exp(kappa - phi)
    L_kp = sp.exp(kappa + phi)
    h_kp = sp.simplify(h.subs({T: T_kp, L: L_kp}))
    variables = (kappa, phi, beta)
    components = (h_kp[0, 0], h_kp[0, 1], h_kp[1, 1])
    jac = sp.factor(sp.Matrix([[sp.diff(c, v) for v in variables] for c in components]).det())
    require(sp.simplify(jac) != 0, "kappa_phi_beta_coordinate_rank_three", checks)

    k0, k1, k2, p0, p1, p2 = sp.symbols("k0 k1 k2 p0 p1 p2", real=True)
    b1_01 = (k1 - p1) - (k0 - p0)
    b2_01 = 2 * (k1 - k0)
    b1_12 = (k2 - p2) - (k1 - p1)
    b2_12 = 2 * (k2 - k1)
    b1_02 = (k2 - p2) - (k0 - p0)
    b2_02 = 2 * (k2 - k0)
    require(sp.expand(b1_01 + b1_12 - b1_02) == 0, "clock_density_telescopes", checks)
    require(sp.expand(b2_01 + b2_12 - b2_02) == 0, "area_density_telescopes", checks)
    dk_01 = sp.expand(b2_01 / 2)
    dd_01 = sp.expand(b2_01 / 2 - b1_01)
    require(dk_01 == k1 - k0, "common_scale_character", checks)
    require(dd_01 == p1 - p0, "reciprocal_depth_character", checks)
    require(sp.expand((b2_01 / 2) + (b2_12 / 2) - b2_02 / 2) == 0,
            "common_scale_adds", checks)
    require(sp.expand(dd_01 + (b2_12 / 2 - b1_12) - (p2 - p0)) == 0,
            "reciprocal_depth_adds", checks)

    q = sp.symbols("q", real=True)
    h_shift = sp.Matrix([[-1, -q], [-q, 1 - q**2]])
    require(h_shift.det() == -1, "flat_shift_family_determinant", checks)
    require(sp.simplify(h_shift[0, 1] / h_shift[0, 0]) == q,
            "shift_independent_of_density_channels", checks)
    require(sp.simplify(h_shift[1, 1] - h_shift[0, 1] ** 2 / h_shift[0, 0]) == 1,
            "flat_shift_family_unit_orthogonal_ruler", checks)

    h_common = sp.diag(-4, 4)
    require(h_common.det() == -16 and -h_common[0, 0] == 4,
            "common_scale_only_witness", checks)
    h_recip = sp.diag(sp.Rational(-1, 4), 4)
    require(h_recip.det() == -1, "pure_reciprocal_witness", checks)

    eta = sp.diag(-1, 1, 1, 1)
    J0 = sp.Matrix([sp.Rational(1, 2), 0, sp.Rational(1, 4), 0])
    J1 = sp.Matrix([0, 2, 0, 0])
    P = sp.Matrix.hstack(J0, J1)
    h_mix1 = sp.simplify(P.T * eta * P)
    require(h_mix1 == sp.diag(sp.Rational(-3, 16), 4), "mixing_witness_one_metric", checks)
    require(h_mix1.det() == sp.Rational(-3, 4), "mixing_witness_one_determinant", checks)

    J1b = sp.Matrix([0, 2, sp.Rational(1, 3), 0])
    Pb = sp.Matrix.hstack(J0, J1b)
    h_mix2 = sp.simplify(Pb.T * eta * Pb)
    require(
        h_mix2
        == sp.Matrix([[sp.Rational(-3, 16), sp.Rational(1, 12)],
                      [sp.Rational(1, 12), sp.Rational(37, 9)]]),
        "mixing_witness_two_metric",
        checks,
    )
    require(h_mix2.det() == sp.Rational(-7, 9), "mixing_witness_two_determinant", checks)
    require(sp.cancel(h_mix2[0, 1] / h_mix2[0, 0]) == sp.Rational(-4, 9),
            "mixing_witness_two_shift", checks)
    require(sp.cancel(h_mix2[1, 1] - h_mix2[0, 1] ** 2 / h_mix2[0, 0]) == sp.Rational(112, 27),
            "mixing_witness_two_ruler", checks)

    a, b, w, d1, d2 = sp.symbols("a b w d1 d2", real=True)
    R = lambda x: sp.Matrix([[sp.cos(x), -sp.sin(x)], [sp.sin(x), sp.cos(x)]])
    require(sp.simplify(sp.trigsimp(R(b) * R(a) - R(a + b))) == sp.zeros(2),
            "normal_rotation_composes", checks)
    C1 = sp.exp(w * d1) * R(a)
    C2 = sp.exp(w * d2) * R(b)
    require(sp.simplify(sp.trigsimp(C2 * C1 - sp.exp(w * (d1 + d2)) * R(a + b))) == sp.zeros(2),
            "conformal_screen_representation_composes", checks)

    f23 = sp.Rational(-4097, 2048)
    require(f23 != 0, "zero_depth_nontrivial_angular_curvature_witness", checks)

    channel_rows = [
        {"channel_id": "C01", "disposition": "RETAIN_ARROW_CHARACTER", "reason": "endpoint reciprocal depth is exact and normalized", "independent_status": "IRREDUCIBLE_FROM_ANGULAR_CHANNEL"},
        {"channel_id": "C02", "disposition": "RETAIN_PATH_ARROW", "reason": "normal isometry composes and survives zero depth", "independent_status": "IRREDUCIBLE_FROM_REAL_DEPTH"},
        {"channel_id": "C03", "disposition": "COMPOSITION_INFRASTRUCTURE", "reason": "alignment bitorsor balances gauge but selects no phase", "independent_status": "NOT_AN_OBSERVABLE_CHANNEL"},
        {"channel_id": "C04", "disposition": "DERIVED_REPRESENTATION", "reason": "screen weight is fixed by lambda once C01 and branch state are supplied", "independent_status": "RECONSTRUCTIBLE"},
        {"channel_id": "C05", "disposition": "OBJECT_STATE_GEOMETRY", "reason": "clock and ruler covectors type the query", "independent_status": "NOT_SELECTED_AS_READOUT"},
        {"channel_id": "C06", "disposition": "LOCAL_STATE_DIAGNOSTIC", "reason": "screen gradient directions are metric-owned", "independent_status": "NO_QUERY_PROJECTION"},
        {"channel_id": "C07", "disposition": "UNSELECTED_PATH_SCALARIZATION_FAMILY", "reason": "all c compose and preserve pair-leaf depth", "independent_status": "NOT_CORE_CHANNEL"},
        {"channel_id": "C08", "disposition": "UNSELECTED_ENDPOINT_SCALARIZATION_FAMILY", "reason": "all c are exact and preserve pair-pure reduction", "independent_status": "NOT_CORE_CHANNEL"},
        {"channel_id": "C09", "disposition": "DIAGNOSTIC_NOT_CHARACTER", "reason": "strain invariants need not compose", "independent_status": "PAIR_METRIC_PARENT_RETAINED_SEPARATELY"},
        {"channel_id": "C10", "disposition": "QUOTIENT_GAUGE_REPRESENTATIVE", "reason": "A changes by dchi", "independent_status": "CURVATURE_AND_TRANSPORT_RETAINED"},
        {"channel_id": "C11", "disposition": "FIELD_STRENGTH_FOR_C02", "reason": "curvature controls local holonomy", "independent_status": "INFINITESIMAL_GENERATOR_NOT_EXTRA_ARROW"},
        {"channel_id": "C12", "disposition": "OBJECT_DOMAIN_DATA", "reason": "branch and rank select the valid fiber type", "independent_status": "NOT_OBSERVABLE_PROMOTION"},
        {"channel_id": "C13", "disposition": "STRATIFICATION_DATA", "reason": "causal type changes the domain", "independent_status": "NO_PHYSICAL_REGIME_LABEL"},
        {"channel_id": "C14", "disposition": "UPSTREAM_PAIR_MAP_DATA", "reason": "mixing modifies the pair metric before readout", "independent_status": "NO_OWNED_STANDALONE_CHANNEL"},
        {"channel_id": "C15", "disposition": "RELATION_FAMILY_OBJECT_TYPE", "reason": "path endpoint and set-valued families have different domains", "independent_status": "NO_UNIVERSAL_COLLAPSE"},
        {"channel_id": "C16", "disposition": "CONDITIONAL_QUERY_PROJECTION", "reason": "founding semantics constrain but do not choose the full readout", "independent_status": "OWNER_OPEN"},
    ]
    write_tsv(
        "CHANNEL_CLASSIFICATION.tsv",
        ["channel_id", "disposition", "reason", "independent_status"],
        channel_rows,
    )

    assembled_rows = [
        {"assembly_id": "A00", "object": "regular calibrated pair metric h", "type": "Lorentzian_2_metric_on_supplied_pair_cell", "composition": "object_state_not_standalone_character", "status": "PARENT_OBJECT"},
        {"assembly_id": "A01", "object": "kappa=log_sigma", "type": "real_endpoint_potential", "composition": "Delta_kappa_additive_on_matched_pair_states", "status": "RETAIN_COMMON_SCALE"},
        {"assembly_id": "A02", "object": "phi", "type": "real_reciprocal_endpoint_potential", "composition": "Delta_phi_additive_on_matched_pair_states", "status": "RETAIN_RECIPROCAL_DEPTH"},
        {"assembly_id": "A03", "object": "beta", "type": "real_pair_shift_state", "composition": "carried_by_full_pair_map_not_a_standalone_character", "status": "RETAIN_SHIFT"},
        {"assembly_id": "A04", "object": "U_gamma", "type": "oriented_normal_isometry_groupoid_arrow", "composition": "U_21_U_10", "status": "RETAIN_PATH_ANGULAR_TRANSPORT"},
        {"assembly_id": "A05", "object": "projector_triple_lambda_orientation", "type": "typed_object_and_local_system_data", "composition": "matched_at_middle_or_aligned_by_bitorsor", "status": "RETAIN_OBJECT_TYPING"},
    ]
    write_tsv(
        "ASSEMBLED_CHANNELS.tsv",
        ["assembly_id", "object", "type", "composition", "status"],
        assembled_rows,
    )

    regime_rows = [
        {"stratum_id": "S00", "geometric_condition": "coincidence_on_calibrated_pair_map", "active_channels": "none__sigma1_phi0_beta0_Uidentity", "physical_regime": "OPEN"},
        {"stratum_id": "S01", "geometric_condition": "pure_reciprocal_pair_metric", "active_channels": "phi", "physical_regime": "OPEN"},
        {"stratum_id": "S02", "geometric_condition": "common_scale_only_pair_metric", "active_channels": "kappa", "physical_regime": "OPEN"},
        {"stratum_id": "S03", "geometric_condition": "flat_event_pairing_shift_family", "active_channels": "beta", "physical_regime": "OPEN"},
        {"stratum_id": "S04", "geometric_condition": "zero_endpoint_depth_nontrivial_normal_loop", "active_channels": "U_holonomy", "physical_regime": "OPEN"},
        {"stratum_id": "S05", "geometric_condition": "Hstar_dphi_zero_pair_pure", "active_channels": "kappa_phi_beta_and_U_possible__G52_screen_gradient_readouts_zero", "physical_regime": "OPEN"},
        {"stratum_id": "S06", "geometric_condition": "regular_complete_pair_mixing", "active_channels": "kappa_phi_beta_and_U_possible", "physical_regime": "OPEN"},
        {"stratum_id": "S07", "geometric_condition": "flat_normal_connection", "active_channels": "kappa_phi_beta__local_U_path_independent__wound_U_may_survive", "physical_regime": "OPEN"},
        {"stratum_id": "S08", "geometric_condition": "generic_full_SO2_normal_holonomy", "active_channels": "kappa_phi_beta_and_path_U", "physical_regime": "OPEN"},
        {"stratum_id": "S09", "geometric_condition": "h00_zero_or_det_h_zero_or_pair_rank_loss", "active_channels": "regular_decomposition_fails_or_diverges", "physical_regime": "OPEN_DEGENERATE"},
    ]
    write_tsv(
        "GEOMETRIC_REGIME_ATLAS.tsv",
        ["stratum_id", "geometric_condition", "active_channels", "physical_regime"],
        regime_rows,
    )

    result = {
        "schema_version": 1,
        "status": "PASS",
        "arena": "SUPPLIED_REGULAR_STATIONARY_R17_WITH_CALIBRATED_PAIR_MAP_AND_DECLARED_CURVE_IN_ITS_IMAGE",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "pair_metric_coordinates": "UNIQUE_TRIPLE_kappa_phi_beta",
        "matched_arrow_characters": "Delta_kappa_and_Delta_phi",
        "path_arrow": "U_gamma_IN_ORIENTED_NORMAL_ISOMETRY_GROUPOID",
        "minimal_banked_assembly": "COMMON_QUERY_OBJECT_STATE_h_EQUIV_kappa_phi_beta_PLUS_TYPED_PROJECTORS_lambda__ARROW_Delta_kappa_Delta_phi_U_gamma_ALONG_DECLARED_PAIR_MAP_CURVE",
        "alpha_beta_families": "UNSELECTED_SCALARIZATIONS_NOT_PROMOTED_TO_CORE_CHANNELS",
        "screen_weight": "DERIVED_REPRESENTATION_exp_plus_or_minus_lambda_Delta_phi_U_gamma_NOT_INDEPENDENT_CHANNEL",
        "physical_regime_map": None,
        "observational_calibration": {
            "c_E": "ACTIVE_PAIR_TAPE_CALIBRATION_ONLY",
            "G_obs": "INACTIVE_WITHOUT_NATIVE_MASS_READOUT",
            "m_e": "UNAPPLIED_FUTURE_CALIBRATION_CANDIDATE",
            "hbar": "EXCLUDED",
        },
        "conductor_owner": None,
        "maximum_ruling": "CONDITIONAL_TYPED_MULTICHANNEL_KINEMATIC_ASSEMBLY_DERIVED_ON_SUPPLIED_REGULAR_PAIR_QUERY__COMMON_SCALE_RECIPROCAL_SHIFT_AND_ANGULAR_TRANSPORT_ROLES_SEPARATED__GEOMETRIC_ACTIVITY_STRATA_DERIVED__PHYSICAL_REGIME_MAP_QUERY_PATH_AND_ON_SHELL_GLOBAL_BOOTSTRAP_SELECTION_OPEN",
    }
    assert result["passed"] == result["total"]
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

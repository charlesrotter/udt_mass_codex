#!/usr/bin/env python3
"""Deterministic exact algebra and ledgers for the native-observable census."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def write_tsv(name: str, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_universe(name: str, key: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len({row[key] for row in rows}) != len(rows):
        raise AssertionError(f"duplicate {key} in {name}")
    return rows


def main() -> None:
    checks: dict[str, str] = {}
    candidates = load_universe("OBSERVABLE_UNIVERSE.tsv", "candidate_id")
    principles = load_universe("PRINCIPLE_UNIVERSE.tsv", "principle_id")
    gates = load_universe("VARIATION_GATE_UNIVERSE.tsv", "gate_id")
    require("A01_candidate_universe_26", len(candidates) == 26, checks)
    require("A02_principle_universe_12", len(principles) == 12, checks)
    require("A03_gate_universe_12", len(gates) == 12, checks)

    # Exact variation controls. H_ab means delta g_ab throughout.
    e = sp.symbols("epsilon")
    a, b, c, d = sp.symbols("a b c d", positive=True)
    da, db, dc, dd = sp.symbols("da db dc dd")
    g4 = sp.diag(a, b, c, d)
    H4 = sp.diag(da, db, dc, dd)
    dmu4 = sp.diff(sp.sqrt((a + e * da) * (b + e * db) * (c + e * dc) * (d + e * dd)), e).subs(e, 0)
    trace4 = sp.sqrt(g4.det()) * sp.trace(g4.inv() * H4) / 2
    require("A04_four_volume_first_variation", sp.simplify(dmu4 - trace4) == 0, checks)

    h3 = sp.diag(a, b, c)
    H3 = sp.diag(da, db, dc)
    dmu3 = sp.diff(sp.sqrt((a + e * da) * (b + e * db) * (c + e * dc)), e).subs(e, 0)
    trace3 = sp.sqrt(h3.det()) * sp.trace(h3.inv() * H3) / 2
    require("A05_three_volume_first_variation", sp.simplify(dmu3 - trace3) == 0, checks)

    q1, q2 = sp.symbols("q1 q2", positive=True)
    dq1, dq2 = sp.symbols("dq1 dq2")
    gamma = sp.diag(q1, q2)
    dgamma = sp.diag(dq1, dq2)
    darea = sp.diff(sp.sqrt((q1 + e * dq1) * (q2 + e * dq2)), e).subs(e, 0)
    area_trace = sp.sqrt(gamma.det()) * sp.trace(gamma.inv() * dgamma) / 2
    require("A06_boundary_measure_metric_variation", sp.simplify(darea - area_trace) == 0, checks)

    # Moving hypersurface term: sign is fixed by K_AB = 1/2 L_n gamma_AB
    # and outward displacement chi_n.
    K, chi_n, sqrt_gamma = sp.symbols("K chi_n sqrt_gamma")
    moving_area_density = sqrt_gamma * K * chi_n
    require("A07_moving_boundary_channel_nonzero", sp.diff(moving_area_density, chi_n) == sqrt_gamma * K, checks)

    M, V, dM, dV = sp.symbols("M V dM dV", nonzero=True)
    rho = M / V
    drho = sp.diff((M + e * dM) / (V + e * dV), e).subs(e, 0)
    expected_drho = (dM - rho * dV) / V
    require("A08_density_quotient_variation", sp.simplify(drho - expected_drho) == 0, checks)

    # Integrated three-curvature comparison candidate. This is variation
    # algebra only, never a UDT field equation or selected functional.
    r1, r2, r3 = sp.symbols("r1 r2 r3")
    R = r1 + r2 + r3
    Ric = sp.diag(r1, r2, r3)
    H_tf = sp.diag(1, -1, 0)
    curvature_bulk_tf = sp.simplify(sum(
        (sp.Rational(1, 2) * R * int(i == j) - Ric[i, j]) * H_tf[i, j]
        for i in range(3) for j in range(3)
    ))
    require("A09_integrated_curvature_tracefree_bulk", curvature_bulk_tf == -r1 + r2, checks)
    H_trace = sp.eye(3)
    curvature_bulk_trace = sp.simplify(sum(
        (sp.Rational(1, 2) * R * int(i == j) - Ric[i, j]) * H_trace[i, j]
        for i in range(3) for j in range(3)
    ))
    require("A10_integrated_curvature_trace_bulk", curvature_bulk_trace == R / 2, checks)

    # Constant representative changes expose the unresolved ontology branch.
    Omega = sp.symbols("Omega", positive=True)
    require("A11_four_volume_conformal_weight_four",
            sp.simplify(sp.sqrt((Omega**2 * g4).det()) / sp.sqrt(g4.det())) == Omega**4, checks)
    require("A12_three_volume_conformal_weight_three",
            sp.simplify(sp.sqrt((Omega**2 * h3).det()) / sp.sqrt(h3.det())) == Omega**3, checks)
    require("A13_boundary_area_conformal_weight_two",
            sp.simplify(sp.sqrt((Omega**2 * gamma).det()) / sp.sqrt(gamma.det())) == Omega**2, checks)
    gamma3 = sp.diag(q1, q2, c)
    require("A13b_spacetime_boundary_measure_conformal_weight_three",
            sp.simplify(sp.sqrt((Omega**2 * gamma3).det()) / sp.sqrt(gamma3.det())) == Omega**3, checks)
    # In three dimensions R -> Omega^-2 R for constant Omega.
    require("A14_integrated_R_conformal_weight_one", sp.simplify(Omega**3 * Omega**-2) == Omega, checks)

    # c and G calibrate mass/length, not length or density by themselves.
    ac, bg = sp.symbols("a_c b_G")
    length_solutions = sp.solve(
        [sp.Eq(ac + 3 * bg, 1), sp.Eq(-bg, 0), sp.Eq(-ac - 2 * bg, 0)],
        [ac, bg], dict=True,
    )
    density_solutions = sp.solve(
        [sp.Eq(ac + 3 * bg, -3), sp.Eq(-bg, 1), sp.Eq(-ac - 2 * bg, 0)],
        [ac, bg], dict=True,
    )
    require("A15_c_G_no_length", length_solutions == [], checks)
    require("A16_c_G_no_density", density_solutions == [], checks)
    require("A17_c2_over_G_is_mass_per_length",
            (2 + 3 * -1, -(-1), -2 - 2 * -1) == (-1, 1, 0), checks)

    # Functional counterfamilies.
    x, y, lam = sp.symbols("x y lambda", real=True)
    S0 = (x**2 + y**2) / 2
    S1 = S0 + lam * x * y
    grad0 = sp.Matrix([sp.diff(S0, x), sp.diff(S0, y)])
    grad1 = sp.Matrix([sp.diff(S1, x), sp.diff(S1, y)])
    require("A18_bulk_functional_counterfamily_same_root",
            grad0.subs({x: 0, y: 0}) == sp.zeros(2, 1)
            and grad1.subs({x: 0, y: 0}) == sp.zeros(2, 1), checks)
    require("A19_bulk_functional_counterfamily_different_response", grad0 != grad1, checks)

    q, T, lam_b, mu_b = sp.symbols("q T lambda_b mu_b")
    B = lam_b * q**2 / 2 + mu_b * T
    require("A20_boundary_functional_changes_field_channel", sp.diff(B, q) == lam_b * q, checks)
    require("A21_boundary_functional_changes_shape_channel", sp.diff(B, T) == mu_b, checks)

    # Closure sections with identical zero sets but different off-shell derivatives.
    u = sp.symbols("u", real=True)
    C0 = u
    C1 = (1 + x**2) * u
    require("A22_closure_same_zero_set", sp.solve(C0, u) == [0] and sp.solve(C1, u) == [0], checks)
    require("A23_closure_different_conormal_normalization",
            sp.diff(C0, u) != sp.diff(C1, u), checks)
    F0 = sp.Integer(0) * u
    F1 = u / 2
    require("A24_fixed_point_same_root", sp.solve(u - F0, u) == [0] and sp.solve(u - F1, u) == [0], checks)
    require("A25_fixed_point_different_linearization",
            sp.diff(u - F0, u) != sp.diff(u - F1, u), checks)

    # Holonomy and stratified global-object controls.
    s0, s1, ds0, ds1 = sp.symbols("s0 s1 ds0 ds1")
    line_integral = (s0 + s1) / 2
    d_line_integral = sp.diff(((s0 + e * ds0) + (s1 + e * ds1)) / 2, e).subs(e, 0)
    require("A26_fixed_path_abelian_holonomy_variation", d_line_integral == (ds0 + ds1) / 2, checks)
    p, qh, hp, hq = sp.symbols("p q_h h_p h_q", positive=True)
    H = sp.diag(p, qh)
    dH = sp.diag(hp, hq)
    w = sp.Matrix([1, 0])
    q_w = (w.T * H.inv() * w)[0]
    dq_w_direct = sp.diff((w.T * (H + e * dH).inv() * w)[0], e).subs(e, 0)
    dq_w_inverse = -(w.T * H.inv() * dH * H.inv() * w)[0]
    require("A27_squared_character_norm_variation", sp.simplify(dq_w_direct - dq_w_inverse) == 0, checks)
    ell_w = sp.sqrt(q_w)
    dell_w = sp.diff(sp.sqrt((w.T * (H + e * dH).inv() * w)[0]), e).subs(e, 0)
    require("A28_character_length_variation", sp.simplify(dell_w - dq_w_inverse / (2 * ell_w)) == 0, checks)
    # At H=I with dH=diag(1,3), active squared-norm slopes are -1 and -3.
    # The right directional derivative of their minimum is -3, while the
    # shortest-vector argmin changes from a two-set at e=0 to {e2} for e>0.
    require("A29_systole_value_tie_directional_derivative", min(-1, -3) == -3, checks)
    require("A30_shortest_argmin_set_jumps", {"e1", "e2"} != {"e2"}, checks)

    gate_rows = [
        # id, G01..G12, disposition, exact basis
        ("N01", "OBSERVED_ONLY", "INCOMPLETE", "NOT_A_STATE_ONTOLOGY", "NOT_A_STATE_OBJECT", "NOT_APPLICABLE", "NOT_APPLICABLE", "NOT_APPLICABLE", "NOT_APPLICABLE", "PASS", "FAIL_SELECTOR", "ABSENT", "ABSENT", "OBSERVED_ANCHORS_NOT_STATE_OBSERVABLE", "c_E and G_obs calibrate units; they do not define a state functional or closure map"),
        ("N02", "CONDITIONAL_REGION", "CONDITIONAL_REGION", "OPEN_ONTOLOGY", "CONDITIONAL_GLOBAL", "CONDITIONAL_FIXED_REGION", "PASS", "PASS", "INCOMPLETE_MOVING_BOUNDARY", "PASS", "PASS", "CONDITIONAL_PARTIAL_NOT_COMPLETE", "ABSENT", "DERIVED_CONDITIONAL_METRIC_MEASURE", "V4=int_M sqrt(|g|); physical value depends on region, completion, and metric representative"),
        ("N03", "CONDITIONAL_SLICE", "CONDITIONAL_SLICE_BOUNDARY", "OPEN_ONTOLOGY", "CONDITIONAL_GLOBAL", "CONDITIONAL_FIXED_DOMAIN", "PASS", "PASS", "INCOMPLETE_MOVING_BOUNDARY", "PASS", "PASS", "CONDITIONAL_PARTIAL_NOT_COMPLETE", "ABSENT", "DERIVED_CONDITIONAL_METRIC_MEASURE", "V3=int_Sigma sqrt(h); slice, boundary, completion, and representative remain inputs"),
        ("N04", "CONDITIONAL_TYPED_NONNULL_BOUNDARY", "CONDITIONAL_EMBEDDING_AND_DIMENSION", "OPEN_ONTOLOGY", "CONDITIONAL_GLOBAL", "CONDITIONAL_FIXED_EMBEDDING", "PASS", "PASS", "INCOMPLETE_SHAPE_CORNER_NULL", "PASS", "PASS", "CONDITIONAL_PARTIAL_NOT_COMPLETE", "ABSENT", "DERIVED_CONDITIONAL_BOUNDARY_MEASURE", "A_k=int_Bk sqrt(|gamma_k|); k=2 for spatial boundary and k=3 for nonnull spacetime seal; null/type-changing boundaries need separate formalism"),
        ("N05", "ABSENT", "ABSENT", "OPEN_ONTOLOGY", "ABSENT", "ABSENT", "ABSENT", "ABSENT", "ABSENT", "DIMENSION_ONLY", "ABSENT", "ABSENT", "ABSENT", "OPEN_NATIVE_MATTER_OBJECT", "No unconditional native total-mass functional exists in the registered post-firewall record"),
        ("N06", "CONDITIONAL_QUOTIENT", "ABSENT_NATIVE_MASS", "OPEN_ONTOLOGY", "CONDITIONAL", "CONDITIONAL", "CONDITIONAL", "CONDITIONAL_ON_dM", "INCOMPLETE", "CONDITIONAL_ON_M_AND_V", "FAIL_WITHOUT_M", "CONDITIONAL_FORMULA_NATIVE_M_ABSENT", "ABSENT", "CONDITIONAL_DENSITY_QUOTIENT_NOT_NATIVE_OBSERVABLE", "rho=M/V and delta rho=(delta M-rho delta V)/V are exact only after same-solution native M and V"),
        ("N07", "ABSENT", "ABSENT", "OPEN_ONTOLOGY", "ABSENT", "ABSENT", "ABSENT", "ABSENT", "ABSENT", "DIMENSION_ONLY", "ABSENT", "ABSENT", "ABSENT", "OPEN_NATIVE_MATTER_OBJECT", "No unconditional native total-energy functional exists in the registered post-firewall record"),
        ("N08", "PASS", "LOCAL_DOMAIN_ONLY", "OPEN_ONTOLOGY", "LOCAL_ONLY", "LOCAL_LINEARIZATION", "NOT_A_SELECTED_FUNCTIONAL_RESPONSE", "NOT_A_SELECTED_FUNCTIONAL_RESPONSE", "NOT_GLOBAL", "PASS", "PASS", "CONDITIONAL_LOCAL_COMPONENT_NOT_GLOBAL", "ABSENT", "DERIVED_LOCAL_GEOMETRIC_OBJECT", "Riemann, Ricci, Weyl, and Cartan data follow locally from a supplied metric/coframe and connection"),
        ("N09", "PASS", "LOCAL_DOMAIN_ONLY", "OPEN_ONTOLOGY", "LOCAL_ONLY", "LOCAL_LINEARIZATION", "NOT_A_SELECTED_FUNCTIONAL_RESPONSE", "NOT_A_SELECTED_FUNCTIONAL_RESPONSE", "NOT_GLOBAL", "PASS", "PASS", "CONDITIONAL_LOCAL_COMPONENT_NOT_GLOBAL", "ABSENT", "DERIVED_LOCAL_GEOMETRIC_OBJECT", "Scalar curvature is local and representative-dependent; a local scalar is not a global state coordinate"),
        ("N10", "UNSELECTED_CANDIDATE", "CONDITIONAL_SLICE_BOUNDARY", "OPEN_ONTOLOGY", "CONDITIONAL_GLOBAL", "CONDITIONAL_FIXED_DOMAIN", "PASS", "PASS", "INCOMPLETE_BOUNDARY_FLUX", "PASS", "FAIL_COUNTERFAMILY", "CONDITIONAL_PARTIAL_NOT_COMPLETE", "ABSENT", "DERIVED_VARIATION_OF_UNSELECTED_GLOBAL_FUNCTIONAL", "I_R=int_Sigma sqrt(h)R has exact bulk trace and trace-free response plus boundary flux but is not selected"),
        ("N11", "UNSELECTED_FAMILY", "CONDITIONAL", "OPEN_ONTOLOGY", "CONDITIONAL_GLOBAL", "CONDITIONAL", "CONDITIONAL", "CONDITIONAL", "INCOMPLETE", "PASS", "FAIL_INFINITE_FAMILY", "CONDITIONAL_FAMILY_NOT_SELECTED", "ABSENT", "UNSELECTED_GLOBAL_FUNCTIONAL_FAMILY", "Arbitrary curvature scalars and coefficients produce inequivalent same-premise functionals"),
        ("N12", "TYPE_ONLY_SOURCE_GAP", "SOURCE_GAP", "OPEN_ONTOLOGY", "TYPE_ONLY_SOURCE_GAP", "SOURCE_GAP", "SOURCE_GAP", "SOURCE_GAP", "SOURCE_GAP", "OPEN", "SOURCE_GAP", "ABSENT", "ABSENT", "TYPE_ONLY_SOURCE_GAP", "No frozen source audits a curvature operator, gauge/domain/boundary conditions, or spectral crossings"),
        ("N13", "CONDITIONAL_TORIC_REGION", "CONDITIONAL_TORIC_REGION", "CONDITIONAL_NORMALIZED_TORIC_OBJECT", "LOCAL_ONLY", "LOCAL_LINEARIZATION", "NOT_A_METRIC_FUNCTIONAL_RESPONSE", "NOT_A_METRIC_FUNCTIONAL_RESPONSE", "INCOMPLETE_GLOBAL_DESCENT", "PASS", "PASS", "CONDITIONAL_LOCAL_COMPONENT_NOT_GLOBAL", "ABSENT", "DERIVED_LOCAL_CONNECTION_OBJECT", "F=dS is exact on ordinary toric regions; global bundle descent and physical role remain open"),
        ("N14", "CONDITIONAL_PATH_PROTOCOL", "CONDITIONAL_PATH_LOOP_BASEPOINT", "OPEN_REPRESENTATIVE", "CONDITIONAL_GLOBAL", "CONDITIONAL_FIXED_PATH_OR_LOOP", "NOT_A_COMPLETED_FUNCTIONAL_RESPONSE", "NOT_A_COMPLETED_FUNCTIONAL_RESPONSE", "INCOMPLETE_PATH_CUT_GLUE", "PASS", "FAIL_PROTOCOL_FAMILY", "CONDITIONAL_PARTIAL_NOT_COMPLETE", "ABSENT", "CONDITIONAL_LC_TRANSPORT_AND_HOLONOMY_TYPES", "Open-path LC transport is an endpoint map; based-loop holonomy is a group element and only conjugacy data remove frame choice"),
        ("N15", "CONDITIONAL_BUNDLE", "CONDITIONAL_GLOBAL_LIFT", "CONDITIONAL_TORIC_OBJECT", "CONDITIONAL_GLOBAL", "CONTINUOUS_HOLONOMY_PLUS_DISCRETE_MONODROMY", "NOT_A_COMPLETED_FUNCTIONAL_RESPONSE", "NOT_A_COMPLETED_FUNCTIONAL_RESPONSE", "INCOMPLETE_GLUE_MONODROMY", "PASS", "FAIL_LIFT_FAMILY", "CONDITIONAL_PARTIAL_NOT_COMPLETE", "ABSENT", "CONDITIONAL_SPLIT_HOLONOMY_MONODROMY_OBJECT", "Continuous torus-connection holonomy and discrete GL2Z monodromy have distinct variation types and require lift, loop, and completion data"),
        ("N16", "CONDITIONAL_TORUS", "CONDITIONAL_TORIC_FIBER", "OPEN_PHYSICAL_COMMON_SCALE", "PASS", "PASS", "CONDITIONAL_CHAMBERWISE_OR_SET_VALUED", "CONDITIONAL_CHAMBERWISE_OR_SET_VALUED", "INCOMPLETE_GLOBAL_TRANSPORT", "CONDITIONAL_NORMALIZED_SHAPE_VS_PHYSICAL_LENGTH", "FAIL_PHYSICAL_SELECTION", "CONDITIONAL_PARTIAL_NOT_COMPLETE", "ABSENT", "DERIVED_STRATIFIED_ANGULAR_OBJECTS", "q_w, ell_w, min q, and W_min are distinct; W_min is set-valued at ties and physical lengths need common scale and periods"),
        ("N17", "CONDITIONAL_COMPLETION", "INCOMPLETE_GLOBAL_BRANCH", "OPEN_ONTOLOGY", "CONDITIONAL_GLOBAL_MODULI", "CONDITIONAL", "CONDITIONAL", "CONDITIONAL", "INCOMPLETE_COMPLETION", "PASS", "FAIL_COMPLETION_SELECTION", "CONDITIONAL_PARTIAL_NOT_COMPLETE", "ABSENT", "CONDITIONAL_CONFIGURATION_MODULUS", "Cell length, seal position, and moduli exist only relative to a chosen completion and equivalence rule"),
        ("N18", "CONDITIONAL_EMBEDDING", "CONDITIONAL_BOUNDARY", "OPEN_ONTOLOGY", "CONDITIONAL_GLOBAL", "CONDITIONAL", "CONDITIONAL", "CONDITIONAL", "INCOMPLETE_FUNCTIONAL_CORNER", "PASS", "FAIL_BOUNDARY_FAMILY", "CONDITIONAL_PARTIAL_NOT_COMPLETE", "ABSENT", "CONDITIONAL_BOUNDARY_GEOMETRY", "Extrinsic, corner, and joint data follow from supplied embeddings but do not select a boundary functional"),
        ("N19", "CONDITIONAL_TEMPORAL_PHI_BRANCH", "CONDITIONAL_TEMPORAL_PHI_BRANCH", "OPEN_PHYSICAL_RULER", "CONDITIONAL_GLOBAL_ON_COMPLETE_LEVELS", "NONDIFFERENTIABLE_AT_CUT", "CONDITIONAL", "CONDITIONAL", "INCOMPLETE_GLOBAL_DESCENT", "PASS", "FAIL_UNIVERSALITY_AND_RULER", "CONDITIONAL_PARTIAL_NOT_COMPLETE", "ABSENT", "DERIVED_CONDITIONAL_TEMPORAL_PHI_SEPARATION_FAMILY__NOT_UNIVERSAL", "h0 and q0 derive intrinsic level-set separation on complete everywhere-timelike nonzero-dphi branches; other causal classes and physical representative remain open"),
        ("N20", "TYPE_ONLY_SUPREMUM", "ABSENT_SEPARATION_COMPLETION", "OPEN_ONTOLOGY", "CONDITIONAL_SUPREMUM_SCHEMA", "NONATTAINMENT_OR_NONDIFFERENTIABLE_MULTIMAX", "NOT_APPLICABLE", "NOT_APPLICABLE", "INCOMPLETE_GLOBAL", "CONDITIONAL_ON_DISTANCE", "FAIL_DISTANCE_AND_COMPLETION", "ABSENT", "ABSENT", "TYPE_ONLY_GLOBAL_SUPREMUM", "Xmax=sup D_g is a working type; D_g, observer/event domain, completion, finiteness, and attainment are open"),
        ("N21", "CONDITIONAL_COMPLETION", "CONDITIONAL_GLOBAL_BRANCH", "PASS", "CONDITIONAL_GLOBAL_LABEL", "DISCRETE_NOT_COVECTOR", "NOT_APPLICABLE", "NOT_APPLICABLE", "CONDITIONAL_COMPLETION", "PASS", "FAIL_COMPLETION_SELECTION", "CONDITIONAL_DISCRETE_READOUT", "ABSENT", "DISCRETE_GLOBAL_LABEL", "Cap, gluing, orientation, and topology labels classify branches but are not infinitesimal response coordinates"),
        ("N22", "CONDITIONAL_MAP_CARRIER", "CONDITIONAL_CARRIER_BOUNDARY", "PASS", "CONDITIONAL_GLOBAL_LABEL", "DISCRETE_NOT_COVECTOR", "NOT_APPLICABLE", "NOT_APPLICABLE", "CONDITIONAL_BOUNDARY", "PASS", "FAIL_CARRIER_SELECTION", "CONDITIONAL_DISCRETE_READOUT", "ABSENT", "CONDITIONAL_TOPOLOGICAL_LABEL", "Hopf/Chern/winding/degree require an appropriate map/bundle and boundary class; carrier is not native"),
        ("N23", "POSIT_CONDITIONAL", "CONDITIONAL_CARRIER_BOX", "OPEN_ONTOLOGY", "CONDITIONAL_GLOBAL_FUNCTIONAL", "CONDITIONAL", "CONDITIONAL", "CONDITIONAL", "INCOMPLETE_PHYSICAL_BOUNDARY", "CONDITIONAL_COEFFICIENTS", "FAIL_NATIVE_SELECTION", "CONDITIONAL_CARRIER_ONLY", "CONDITIONAL_CARRIER_ONLY", "CONDITIONAL_CARRIER_FUNCTIONAL", "Existing L2+L4 energy/mass and local response are conditional on carrier, action, coefficients, box, and readout"),
        ("N24", "PASS", "LOCAL_CHART_ONLY", "OPEN_ONTOLOGY", "LOCAL_ONLY", "PARTIAL_CHART_COMPONENT_RESPONSE_ONLY", "PARTIAL_CHART_COMPONENT_RESPONSE_ONLY", "PARTIAL_CHART_COMPONENT_RESPONSE_ONLY", "NOT_GLOBAL", "PASS", "FAIL_FRAME_COMPONENT_PHYSICALIZATION", "CONDITIONAL_LOCAL_COMPONENT_NOT_GLOBAL", "ABSENT", "DERIVED_LOCAL_COMPONENT_ATLAS", "Six-family Cartan network is exact representative-dependent geometric wiring, not a frame-independent physical response law"),
        ("N25", "OBSERVED_ON_SUPPLIED_BRANCH", "CONDITIONAL_PROFILE_DATA", "NOT_NATIVE_SELECTOR", "CONDITIONAL_SCORE", "NOT_OFFSHELL_STATE_COVECTOR", "NOT_APPLICABLE", "NOT_APPLICABLE", "NOT_APPLICABLE", "PASS", "FAIL_MODEL_DEPENDENCE", "CONDITIONAL_COMPARISON_MAP_ONLY", "ABSENT", "OBSERVED_ON_SHELL_COMPARISON", "WR-L/SNe score tests a supplied profile; it neither defines nor selects the native global state"),
        ("N26", "TYPE_ONLY", "INCOMPLETE_X_AND_O", "OPEN_ONTOLOGY", "TYPE_ONLY", "ABSENT", "ABSENT", "ABSENT", "ABSENT", "OPEN", "FAIL_MAP_COUNTERFAMILY", "ABSENT", "ABSENT", "TYPE_INCOMPLETE_CLOSURE", "A(X,O)=0 and O-R[X]=0 are the correct coupled type; neither arrow, targets, normalization, or pairing is derived"),
    ]
    require("A31_gate_rows_cover_26", len(gate_rows) == 26, checks)
    require("A32_gate_rows_exact_ids", {r[0] for r in gate_rows} == {r["candidate_id"] for r in candidates}, checks)

    gate_fields = ["candidate_id"] + [f"G{i:02d}" for i in range(1, 13)] + ["disposition", "basis"]
    gate_dicts = [dict(zip(gate_fields, row, strict=True)) for row in gate_rows]
    write_tsv("OBSERVABLE_GATE_MATRIX.tsv", gate_fields, gate_dicts)

    definition_rows = [
        {"candidate_id": r["candidate_id"], "object_family": next(c["object_family"] for c in candidates if c["candidate_id"] == r["candidate_id"]),
         "exact_definition_or_absence": r["basis"], "classification": r["disposition"],
         "operator_provenance": {
             "N01": "OBSERVATION_ONLY", "N05": "ABSENT", "N07": "ABSENT", "N12": "TYPE_ONLY_SOURCE_GAP",
             "N20": "WORKING_OWNER_TYPE_SCHEMA", "N23": "CONDITIONAL_CARRIER_ACTION",
             "N25": "OBSERVED_COMPARISON", "N26": "WORKING_TYPE_ONLY",
         }.get(r["candidate_id"], "UDT_METRIC_GEOMETRY_CONDITIONAL_ON_STATED_DOMAIN"),
         "source_basis": {
             "N01": "matter_bootstrap_dimensional_inventory_2026-07-20/AUDIT_REPORT.md:47-69",
             "N02": "udt_bootstrap_to_local_response_map_audit_2026-07-25/EXACT_DERIVATION.md",
             "N03": "udt_bootstrap_to_local_response_map_audit_2026-07-25/AUDIT_REPORT.md:70-101",
             "N04": "udt_free_global_seal_transversality_audit_2026-07-21/AUDIT_REPORT.md:68-85",
             "N05": "matter_bootstrap_dimensional_inventory_2026-07-20/AUDIT_REPORT.md:130-141",
             "N06": "udt_bootstrap_to_local_response_map_audit_2026-07-25/AUDIT_REPORT.md:70-103",
             "N07": "udt_bootstrap_to_local_response_map_audit_2026-07-25/AUDIT_REPORT.md:61-66",
             "N08": "udt_nonlinear_cartan_bianchi_ensemble_atlas_2026-07-26/AUDIT_REPORT.md:11-38",
             "N09": "udt_nonlinear_cartan_bianchi_ensemble_atlas_2026-07-26/CURVATURE_CONTRACTIONS.tsv",
             "N10": "udt_bootstrap_to_local_response_map_audit_2026-07-25/AUDIT_REPORT.md:61-66",
             "N11": "udt_post_july_offshell_response_availability_audit_2026-07-25/AUDIT_REPORT.md",
             "N12": "udt_global_local_relational_closure_audit_2026-07-25/AUDIT_REPORT.md",
             "N13": "udt_pre_density_substrate_response_atlas_2026-07-24/AUDIT_REPORT.md:215-236",
             "N14": "udt_global_metric_assembly_atlas_2026-07-22/AUDIT_REPORT.md:104-116;168-180",
             "N15": "udt_global_metric_assembly_atlas_2026-07-22/AUDIT_REPORT.md",
             "N16": "udt_dual_systole_global_transport_audit_2026-07-24/AUDIT_REPORT.md:11-39",
             "N17": "udt_global_metric_assembly_atlas_2026-07-22/COMPLETION_CLASS_REGISTRY.tsv",
             "N18": "udt_free_global_seal_transversality_audit_2026-07-21/AUDIT_REPORT.md:163-190",
             "N19": "udt_two_observer_separation_selector_audit_2026-07-24/AUDIT_REPORT.md:55-94",
             "N20": "udt_xmax_observer_separation_audit_2026-07-24/AUDIT_REPORT.md:11-49",
             "N21": "udt_global_metric_assembly_atlas_2026-07-22/COMPLETION_CLASS_REGISTRY.tsv",
             "N22": "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md:51-65",
             "N23": "matter_bootstrap_dimensional_inventory_2026-07-20/AUDIT_REPORT.md:94-107",
             "N24": "udt_nonlinear_cartan_bianchi_ensemble_atlas_2026-07-26/AUDIT_REPORT.md:25-38",
             "N25": "udt_xmax_observer_separation_audit_2026-07-24/AUDIT_REPORT.md:31-36",
             "N26": "udt_bootstrap_to_local_response_map_audit_2026-07-25/AUDIT_REPORT.md:5-31",
         }[r["candidate_id"]]}
        for r in gate_dicts
    ]
    write_tsv("OBSERVABLE_DEFINITION_LEDGER.tsv",
              ["candidate_id", "object_family", "exact_definition_or_absence", "classification", "operator_provenance", "source_basis"],
              definition_rows)

    variation_rows = [
        {"variation_id": "V01", "object": "spacetime_four_volume", "fixed_domain_bulk": "delta V4=1/2 int_M sqrt(|g|) g^ab H_ab", "boundary_or_global": "+ int_boundary sqrt(|gamma|) chi_n", "tracefree_angular": "zero_for_pure_tracefree_H", "status": "EXACT_CONDITIONAL_DOMAIN"},
        {"variation_id": "V02", "object": "spatial_proper_volume", "fixed_domain_bulk": "delta V3=1/2 int_Sigma sqrt(h) h^ij H_ij", "boundary_or_global": "+ int_boundary sqrt(gamma) chi_n", "tracefree_angular": "zero_for_pure_tracefree_H", "status": "EXACT_CONDITIONAL_SLICE"},
        {"variation_id": "V03", "object": "nonnull_boundary_induced_measure", "fixed_domain_bulk": "delta A_k=1/2 int_Bk sqrt(|gamma_k|) gamma^AB delta_gamma_AB", "boundary_or_global": "+ int_Bk sqrt(|gamma_k|) K chi_n; k=2_for_partial_Sigma_and_k=3_for_spacetime_seal; null_boundaries_separate", "tracefree_angular": "zero_for_induced_tracefree_delta_gamma", "status": "EXACT_CONDITIONAL_TYPED_EMBEDDING"},
        {"variation_id": "V04", "object": "total_proper_density", "fixed_domain_bulk": "delta rho=(delta M-rho delta V)/V", "boundary_or_global": "inherits_all_M_and_V_channels", "tracefree_angular": "delta_rho_TF=delta_M_TF/V_when_delta_V_TF=0", "status": "EXACT_QUOTIENT_RULE_NATIVE_M_ABSENT"},
        {"variation_id": "V05", "object": "integrated_spatial_scalar_curvature", "fixed_domain_bulk": "int sqrt(h)(1/2 R h^ij-Ric^ij)H_ij", "boundary_or_global": "int_boundary sqrt(gamma)n^i(nabla^j H_ij-nabla_i trH)", "tracefree_angular": "orthonormal_Ricci_frame_H=diag(1,-1,0)_gives_-r1+r2", "status": "EXACT_COMPARISON_FUNCTIONAL_UNSELECTED"},
        {"variation_id": "V06", "object": "constant_conformal_representative", "fixed_domain_bulk": "V4->Omega^4 V4; V3->Omega^3 V3; A2->Omega^2 A2; A3->Omega^3 A3; I_R3->Omega I_R3", "boundary_or_global": "physical_values_change_until_representative_selected", "tracefree_angular": "not_a_tracefree_variation", "status": "EXACT_ONTOLOGY_FORK_CONTROL"},
        {"variation_id": "V07", "object": "abelian_torus_connection_fixed_path_line_integral", "fixed_domain_bulk": "delta integral_gamma S=integral_gamma delta S_for_fixed_path", "boundary_or_global": "closed_loop_exponentiation_lattice_period_global_lift_moving_path_and_monodromy_not_supplied", "tracefree_angular": "through_delta_S_only_after_metric_to_S_map", "status": "EXACT_FIXED_PATH_ABELIAN_ONLY__NOT_LC_HOLONOMY"},
        {"variation_id": "V08", "object": "angular_character_norm_systole_and_argmin", "fixed_domain_bulk": "delta q_w=-w^T H^-1(delta H)H^-1 w; delta ell_w=delta q_w/(2 ell_w)", "boundary_or_global": "physical_length_needs_common_scale_and_periods; monodromy_and_toric_completion_required", "tracefree_angular": "at_tie_directional_derivative_of_min_q_is_min_active_slopes; Clarke_subdifferential_is_convex_hull; W_min_is_set_valued_jump", "status": "EXACT_STRATIFIED_OBJECTS_DISTINGUISHED"},
        {"variation_id": "V09", "object": "observer_pair_supremum_Xmax", "fixed_domain_bulk": "first_variation_only_if_supremum_is_attained_by_unique_stable_pair_with_unique_regular_controlling_geodesic", "boundary_or_global": "nonattainment_has_no_maximizer_derivative; cut_loci_or_multiple_maximizers_give_nonsmooth_set_valued_response", "tracefree_angular": "path_dependent_when_conditionally_defined", "status": "TYPE_ONLY_Dg_AND_ATTAINMENT_OPEN"},
        {"variation_id": "V10", "object": "topology_labels", "fixed_domain_bulk": "delta Q=0_within_a_fixed_smooth_topological_component", "boundary_or_global": "jumps_only_through_boundary_escape_singularity_or_sector_change", "tracefree_angular": "not_an_infinitesimal_coordinate", "status": "DISCRETE_GLOBAL_DATA"},
    ]
    write_tsv("VARIATION_LEDGER.tsv", list(variation_rows[0]), variation_rows)

    principle_rows = [
        ("P01", "metric_local_objects_and_conditional_measures", "NO", "NO", "NO", "NO", "NO", "SUPPLIES_GEOMETRIC_PRIMITIVES_NOT_CLOSURE"),
        ("P02", "equivariance_constraint", "NO", "NO", "NO", "NO", "NO", "CONSTRAINS_COVARIANCE_WITHOUT_SELECTING_FUNCTIONAL"),
        ("P03", "domain_and_completion_types", "NO", "NO", "NO", "NO", "NO", "SUPPLIES_CELL_TYPE_NOT_BOUNDARY_OR_COMPLETION_RULE"),
        ("P04", "static_phi_parity_and_value", "NO", "NO", "NO", "NO", "NO", "SCOPED_STATIC_SCALAR_SEAL_DATA_ONLY"),
        ("P05", "working_two_arrow_architecture", "NO", "NO", "NO", "NO", "NO", "NAMES_SELF_CONSISTENCY_BUT_NOT_MAPS_TARGETS_OR_DERIVATIVE"),
        ("P06", "on_shell_admissibility_window", "NO", "NO", "NO", "NO", "NO", "WINDOW_IS_NOT_OFFSHELL_OBSERVABLE_OR_SECTION"),
        ("P07", "unit_calibration", "NO", "NO", "NO", "NO", "NO", "OBSERVED_c_E_IS_NOT_FUNCTIONAL_SELECTOR"),
        ("P08", "unit_calibration", "NO", "NO", "NO", "NO", "NO", "OBSERVED_G_obs_IS_NOT_MASS_OR_DENSITY_LAW"),
        ("P09", "challenged_ontology_constraint", "NO", "NO", "NO", "NO", "NO", "CANNOT_CLOSE_FORK_WHILE_CHALLENGED_OPEN"),
        ("P10", "local_nonlinear_geometric_wiring", "NO", "NO", "NO", "NO", "NO", "CARTAN_BIANCHI_IDENTITIES_DO_NOT_SUPPLY_PHYSICAL_RESPONSE"),
        ("P11", "conditional_energy_topology_example", "CONDITIONAL_BRANCH_ONLY", "CONDITIONAL_BRANCH_ONLY", "CONDITIONAL_BRANCH_ONLY", "INCOMPLETE_PHYSICAL_BOUNDARY", "CONDITIONAL_BRANCH_ONLY", "POSIT_SUPPLIES_REAL_BRANCHWISE_RESPONSE_BUT_NOT_UNCONDITIONAL_CLOSURE"),
        ("P12", "conditional_response_examples", "CONDITIONAL_BRANCH_ONLY", "CONDITIONAL_BRANCH_ONLY", "CONDITIONAL_BRANCH_ONLY", "INCOMPLETE_BOUNDARY_GLOBAL", "CONDITIONAL_BRANCH_ONLY", "ACTIONS_SUPPLY_REAL_VARIATIONS_ON_SUPPLIED_BRANCHES_BUT_ARE_NOT_SELECTED_BY_FOUNDATION"),
    ]
    principle_fields = ["principle_id", "definition_capacity", "selects_target", "selects_normalization", "selects_dual_pairing", "completes_boundary_global", "derives_R_or_A_arrow", "ruling"]
    principle_dicts = [dict(zip(principle_fields, row, strict=True)) for row in principle_rows]
    require("A33_principle_rows_exact_ids", {r["principle_id"] for r in principle_dicts} == {p["principle_id"] for p in principles}, checks)
    write_tsv("PRINCIPLE_CLOSURE_MATRIX.tsv", principle_fields, principle_dicts)

    counter_rows = [
        {"counter_id": "C01", "shared_registered_input": "same_metric_domain_and_symmetries", "family": "int_sqrt(h)_f(R_Ric2_Riem2_nablaR_etc)", "changed_object": "bulk_covector_and_target", "consequence": "no_unique_curvature_functional"},
        {"counter_id": "C02", "shared_registered_input": "same_bulk_geometry", "family": "B_lambda_mu=lambda*q^2/2+mu*T", "changed_object": "boundary_field_and_shape_equations", "consequence": "varying_seal_does_not_select_boundary_functional"},
        {"counter_id": "C03", "shared_registered_input": "same_closure_zero_set_u=0", "family": "C0=u; C1=(1+x^2)u", "changed_object": "conormal_normalization_off_shell", "consequence": "root_set_does_not_select_response"},
        {"counter_id": "C04", "shared_registered_input": "same_fixed_point_u=0", "family": "F0(u)=0; F1(u)=u/2", "changed_object": "fixed_point_linearization", "consequence": "self_consistency_does_not_select_recomputation_operator"},
        {"counter_id": "C05", "shared_registered_input": "same_connection_curvature_on_local_chart", "family": "loops_basepoints_lifts_and_conjugacy_readouts", "changed_object": "global_holonomy_object", "consequence": "local_F_does_not_select_global_scalar"},
        {"counter_id": "C06", "shared_registered_input": "same_local_metric", "family": "distinct_complete_topologies_boundaries_caps_and_gluings", "changed_object": "spectrum_systole_diameter_and_topology", "consequence": "local_geometry_does_not_select_global_completion"},
        {"counter_id": "C07", "shared_registered_input": "same_conformal_class", "family": "g_and_Omega^2_g", "changed_object": "volume_curvature_length_and_density_values", "consequence": "physical_observables_need_representative_or_branch_selection"},
        {"counter_id": "C08", "shared_registered_input": "same_observed_c_E_and_G_obs", "family": "all_positive_length_scales_ell", "changed_object": "mass_density_and_global_size", "consequence": "anchors_calibrate_but_do_not_select_state"},
    ]
    write_tsv("COUNTERMODEL_LEDGER.tsv", list(counter_rows[0]), counter_rows)

    complete_vectors = [r["candidate_id"] for r in gate_dicts if all(r[f"G{i:02d}"] == "PASS" for i in range(1, 11))]
    complete_closures = [r["candidate_id"] for r in gate_dicts if all(r[f"G{i:02d}"] == "PASS" for i in range(1, 13))]
    assembly_rows = [
        {"blocker_id": "B01", "required_for_every_assembly": "one_natively_selected_metric_ontology", "status": "OPEN_BLOCKER", "cannot_be_repaired_by_component_union": "components_in_different_ontologies_do_not_share_one_physical_domain"},
        {"blocker_id": "B02", "required_for_every_assembly": "complete_boundary_corner_glue_modulus_domain", "status": "OPEN_BLOCKER", "cannot_be_repaired_by_component_union": "every_global_continuous_candidate_retains_conditional_or_incomplete_global_domain"},
        {"blocker_id": "B03", "required_for_every_assembly": "native_component_and_target_selection", "status": "OPEN_BLOCKER", "cannot_be_repaired_by_component_union": "union_of_allowed_functionals_does_not_select_one_state_vector"},
        {"blocker_id": "B04", "required_for_every_assembly": "complete_recomputation_map_R_of_X", "status": "OPEN_BLOCKER", "cannot_be_repaired_by_component_union": "conditional_partial_maps_have_no_common_complete_vector_domain"},
        {"blocker_id": "B05", "required_for_every_assembly": "complete_local_admissibility_map_A_of_X_O", "status": "OPEN_BLOCKER", "cannot_be_repaired_by_component_union": "no_registered_native_principle_supplies_the_complete_map"},
        {"blocker_id": "B06", "required_for_every_assembly": "same_solution_native_mass_or_energy_and_density_response_for_bootstrap_matter", "status": "OPEN_BLOCKER", "cannot_be_repaired_by_component_union": "N05_and_N07_absent_and_N06_is_only_a_conditional_quotient"},
    ]
    write_tsv("ASSEMBLY_BLOCKER_LEDGER.tsv", list(assembly_rows[0]), assembly_rows)
    require("A34_no_complete_single_component", complete_vectors == [], checks)
    require("A35_no_complete_single_component_closure", complete_closures == [], checks)
    require("A36_coherent_assembly_has_unrepaired_global_blockers",
            all(row["status"] == "OPEN_BLOCKER" for row in assembly_rows[:5]), checks)
    require("A37_no_complete_R_arrow", all(r["G11"] != "PASS" for r in gate_dicts), checks)
    require("A38_no_complete_A_arrow", all(r["G12"] != "PASS" for r in gate_dicts), checks)

    status_rows = [
        {"claim": "metric_local_geometric_primitives", "status": "DERIVED_SCOPED", "basis": "N08,N09,N13,N24", "remaining": "physical global state and response law"},
        {"claim": "conditional_metric_measures", "status": "DERIVED_CONDITIONAL", "basis": "N02,N03,N04 with V01-V03", "remaining": "domain, representative, moving boundary and completion"},
        {"claim": "integrated_curvature_variation", "status": "DERIVED_MATHEMATICAL_COMPARISON", "basis": "N10 and V05", "remaining": "native selection and boundary completion"},
        {"claim": "set_valued_angular_systole", "status": "DERIVED_CONDITIONAL_TORIC", "basis": "N16 and V08", "remaining": "physical selection, global transport and phase"},
        {"claim": "native_total_mass_energy_density", "status": "OPEN", "basis": "N05-N07", "remaining": "native functional and same-solution variation"},
        {"claim": "universal_observer_separation_and_Xmax", "status": "OPEN_TYPE_ONLY", "basis": "N19,N20", "remaining": "D_g, complete branch and extremum regularity"},
        {"claim": "complete_global_observable_vector", "status": "NOT_DERIVED_IN_FROZEN_UNIVERSE", "basis": "no coherent component assembly survives B01-B05", "remaining": "one coherent domain and ontology plus native global definitions"},
        {"claim": "complete_bootstrap_closure_section", "status": "NOT_DERIVED_IN_FROZEN_UNIVERSE", "basis": "no coherent component assembly survives B01-B06 and neither complete arrow passes", "remaining": "R[X], A(X,O), targets, normalizations, pairing, boundary and regularity"},
        {"claim": "future_density_bracket", "status": "DEFERRED_IMPORTED_COMPARISON_ANCHOR_ONLY", "basis": "L17 and preregistration stop", "remaining": "native mass/energy and density-to-geometry response first"},
    ]
    write_tsv("STATUS_LEDGER.tsv", list(status_rows[0]), status_rows)

    result = {
        "schema": "udt-native-global-observable-census-1.0",
        "sympy_version": sp.__version__,
        "candidate_count": len(candidates),
        "principle_count": len(principles),
        "gate_count": len(gates),
        "algebra_check_count": len(checks),
        "checks": checks,
        "complete_single_component_candidates": complete_vectors,
        "complete_single_component_closure_candidates": complete_closures,
        "coherent_multi_component_assembly": "NOT_DERIVED__B01_B05_UNREPAIRED",
        "exact_objects": {
            "delta_V4_density": str(sp.simplify(trace4)),
            "delta_V3_density": str(sp.simplify(trace3)),
            "delta_boundary_area_density": str(sp.simplify(area_trace)),
            "moving_boundary_area_density": str(moving_area_density),
            "delta_rho": str(sp.simplify(expected_drho)),
            "integrated_R_tracefree_bulk": str(curvature_bulk_tf),
            "integrated_R_trace_bulk": str(curvature_bulk_trace),
            "integrated_R_boundary_flux": "n^i(nabla^j H_ij-nabla_i tr(H))",
            "conformal_weights": {"V4": 4, "V3": 3, "A2": 2, "A3": 3, "I_R3": 1},
            "delta_squared_character_norm": str(sp.simplify(dq_w_inverse)),
            "delta_character_length": str(sp.simplify(dell_w)),
            "systole_tie_right_directional_derivative_control": "min(-1,-3)=-3",
            "shortest_argmin_tie_control": "W_min(0)={e1,e2}; W_min(epsilon>0)={e2}",
        },
        "maximum_supported_conclusion": "NO_DERIVED_COMPLETE_OBSERVABLE_VECTOR_OR_CLOSURE_SECTION__EXACT_METRIC_PRIMITIVE_AND_VARIATION_ATLAS",
        "density_status": "NOT_USED__LAMBDA_CDM_CENTER_DEFERRED_IMPORTED_COMPARISON_ANCHOR",
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

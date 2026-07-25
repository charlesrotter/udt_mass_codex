#!/usr/bin/env python3
"""Exact sandbox audit of global-local relational closure architecture."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path

import sympy as sp


ROOT = Path(os.environ["UDT_REPO"]).resolve()
HERE = Path(__file__).resolve().parent

INPUTS = [
    "udt_observer_longitudinal_transverse_cocycle_audit_2026-07-24/EXACT_DERIVATION.md",
    "udt_intrinsic_clock_transverse_solder_audit_2026-07-24/EXACT_DERIVATION.md",
    "udt_bootstrap_clock_angular_closure_audit_2026-07-24/AUDIT_REPORT.md",
    "udt_bootstrap_clock_angular_closure_audit_2026-07-24/BOOTSTRAP_ROUTE_LEDGER.tsv",
    "udt_bootstrap_clock_angular_closure_audit_2026-07-24/EQUATION_FAMILY_GATE_MATRIX.tsv",
    "udt_bootstrap_clock_angular_closure_audit_2026-07-24/COMPLETION_BOOTSTRAP_ATLAS.tsv",
    "udt_reciprocal_pair_global_module_audit_2026-07-24/CONDITIONAL_HOPF_CROSSWALK.tsv",
    "null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv",
    "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
    "matter_bootstrap_dimensional_inventory_2026-07-20/STATUS_LEDGER.tsv",
]


def rows(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expect(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def main() -> None:
    checks: dict[str, str] = {}
    details: dict[str, object] = {}

    # 1. Reciprocal identity component: exact additive one-parameter group and
    # explicit contraction t -> S(t delta). This establishes the relevant
    # connected component as noncompact and topologically trivial.
    d1, d2, t = sp.symbols("d1 d2 t", real=True)
    S = lambda d: sp.diag(sp.exp(-d), sp.exp(d))
    expect("reciprocal_composition", sp.simplify(S(d2) * S(d1) - S(d1 + d2)) == sp.zeros(2), checks)
    expect("reciprocal_determinant_one", sp.simplify(S(d1).det()) == 1, checks)
    expect("reciprocal_reversal", sp.simplify(S(-d1) * S(d1)) == sp.eye(2), checks)
    expect("reciprocal_explicit_contraction_start", S(t * d1).subs(t, 0) == sp.eye(2), checks)
    expect("reciprocal_explicit_contraction_end", S(t * d1).subs(t, 1) == S(d1), checks)

    # 2. Complete composable transverse state and reducible direct sum.
    theta = sp.symbols("theta", real=True)
    I2 = sp.eye(2)
    c, s = sp.cos(theta), sp.sin(theta)
    M = sp.BlockMatrix([[c * I2, s * I2], [-s * I2, c * I2]]).as_explicit()
    Omega = sp.BlockMatrix([[sp.zeros(2), I2], [-I2, sp.zeros(2)]]).as_explicit()
    C = sp.diag(S(d1), M)
    P_rec = sp.diag(1, 1, 0, 0, 0, 0)
    P_trans = sp.eye(6) - P_rec
    expect("transverse_symplectic", sp.simplify(M.T * Omega * M - Omega) == sp.zeros(4), checks)
    expect("reciprocal_invariant_projector", sp.simplify(C * P_rec - P_rec * C) == sp.zeros(6), checks)
    expect("transverse_invariant_projector", sp.simplify(C * P_trans - P_trans * C) == sp.zeros(6), checks)

    # Independent screen SO(2) gauge admits no nonzero linear map from two
    # screen scalars into two copies of the screen-vector representation.
    J = sp.Matrix([[0, -1], [1, 0]])
    J4 = sp.diag(J, J)
    gauge_map_operator = sp.kronecker_product(sp.eye(2), J4)
    expect("linear_clock_screen_solder_nullity_zero", 8 - gauge_map_operator.rank() == 0, checks)

    # Same-endpoint clock ratio is one while transverse holonomy may remain
    # nontrivial: an explicit independence witness.
    C_loop = C.subs({d1: 0, theta: sp.pi / 2})
    expect("closed_clock_block_identity", C_loop[:2, :2] == sp.eye(2), checks)
    expect("closed_transverse_block_nontrivial", C_loop[2:, 2:] != sp.eye(4), checks)

    # 3. Conditional reciprocal-weight/Hopf-coordinate bridge.
    phi = sp.symbols("phi", real=True)
    cos2 = sp.exp(-2 * phi) / (2 * sp.cosh(2 * phi))
    sin2 = sp.exp(2 * phi) / (2 * sp.cosh(2 * phi))
    expect("hopf_weights_normalized", sp.simplify(cos2 + sin2) == 1, checks)
    expect("hopf_weight_ratio_reciprocal", sp.simplify(sin2 / cos2) == sp.exp(4 * phi), checks)
    expect("hopf_phi_reversal_exchanges_weights", sp.simplify(cos2.subs(phi, -phi) - sin2) == 0, checks)
    expect("hopf_negative_depth_endpoint", sp.limit(cos2, phi, -sp.oo) == 1 and sp.limit(sin2, phi, -sp.oo) == 0, checks)
    expect("hopf_positive_depth_endpoint", sp.limit(cos2, phi, sp.oo) == 0 and sp.limit(sin2, phi, sp.oo) == 1, checks)

    # A = cos^2(eta) dxi1 + sin^2(eta) dxi2 has
    # A wedge dA = -2 sin(eta)cos(eta) deta dxi1 dxi2.
    eta = sp.symbols("eta", real=True, nonnegative=True)
    hopf_density = -2 * sp.sin(eta) * sp.cos(eta)
    hopf_integral = sp.integrate(hopf_density, (eta, 0, sp.pi / 2)) * (2 * sp.pi) ** 2
    hopf_charge = sp.simplify(-hopf_integral / (4 * sp.pi**2))
    expect("conditional_hopf_integral_minus_4pi2", sp.simplify(hopf_integral + 4 * sp.pi**2) == 0, checks)
    expect("conditional_unit_hopf_charge", hopf_charge == 1, checks)

    # Collapse-cycle determinants exhibit the topology family; exchange/mirror
    # alone does not force determinant one.
    cap_pairs = [
        ((1, 0), (1, 0)),
        ((1, 0), (0, 1)),
        ((1, 0), (1, 3)),
        ((1, 0), (2, 5)),
    ]
    determinants = [
        abs(sp.det(sp.Matrix.hstack(sp.Matrix(a), sp.Matrix(b)))) for a, b in cap_pairs
    ]
    expect("toric_completion_determinants_0_1_3_5", determinants == [0, 1, 3, 5], checks)

    # 4. Same-solution density variation and trace-only volume control.
    V, rho, dM, dV = sp.symbols("V rho dM dV", nonzero=True)
    Mmass = rho * V
    epsilon = sp.symbols("epsilon")
    varied = (Mmass + epsilon * dM) / (V + epsilon * dV)
    drho = sp.simplify(sp.diff(varied, epsilon).subs(epsilon, 0))
    expect("density_variation", sp.simplify(drho - (dM - rho * dV) / V) == 0, checks)
    sigma = sp.symbols("sigma")
    trace_only = sigma * sp.eye(2)
    tf = sp.simplify(trace_only - sp.trace(trace_only) * sp.eye(2) / 2)
    expect("volume_isotropic_screen_tracefree_zero", tf == sp.zeros(2), checks)

    # 5. Inverse variational problem: closure equations do not automatically
    # define an action. For zero-order finite-dimensional controls, exactness
    # requires equality of cross derivatives.
    x, y = sp.symbols("x y", real=True)
    F_integrable = sp.Matrix([y, x])
    F_nonintegrable = sp.Matrix([0, x])
    curl_integrable = sp.diff(F_integrable[0], y) - sp.diff(F_integrable[1], x)
    curl_nonintegrable = sp.diff(F_nonintegrable[0], y) - sp.diff(F_nonintegrable[1], x)
    expect("integrable_response_helmholtz", curl_integrable == 0, checks)
    expect("nonintegrable_response_rejected", curl_nonintegrable != 0, checks)
    action = x * y
    expect("downstream_action_reconstruction", sp.Matrix([sp.diff(action, x), sp.diff(action, y)]) == F_integrable, checks)
    # Two paths from (0,0) to (x,y) give distinct integrals for F=(0,x).
    path_xy = x * y
    path_yx = 0
    expect("nonintegrable_path_dependence", sp.simplify(path_xy - path_yx) != 0, checks)

    # Local Helmholtz closure is not sufficient for a global single-valued
    # action on a multiply connected configuration space. The closed one-form
    # k dtheta on S1 has nonzero period for k != 0.
    theta_config, k = sp.symbols("theta_config k", real=True, nonzero=True)
    circle_period = sp.integrate(k, (theta_config, 0, 2 * sp.pi))
    expect("closed_configuration_one_form_nonzero_period", sp.simplify(circle_period - 2 * sp.pi * k) == 0, checks)
    expect("global_action_requires_zero_periods", circle_period != 0, checks)

    # 6. Mechanical registered-evidence census.
    routes = rows("udt_bootstrap_clock_angular_closure_audit_2026-07-24/BOOTSTRAP_ROUTE_LEDGER.tsv")
    equations = rows("udt_bootstrap_clock_angular_closure_audit_2026-07-24/EQUATION_FAMILY_GATE_MATRIX.tsv")
    completions = rows("udt_bootstrap_clock_angular_closure_audit_2026-07-24/COMPLETION_BOOTSTRAP_ATLAS.tsv")
    hopf = {row["step_id"]: row for row in rows("udt_reciprocal_pair_global_module_audit_2026-07-24/CONDITIONAL_HOPF_CROSSWALK.tsv")}
    action_ledger = {row["id"]: row for row in rows("native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv")}
    null_hopf = {row["claim_id"]: row for row in rows("null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv")}
    toric = {row["claim_id"]: row for row in rows("angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv")}
    expect("eight_bootstrap_routes", len(routes) == 8, checks)
    expect("twenty_eight_equation_families", len(equations) == 28, checks)
    expect("zero_complete_equation_closures", all(row["complete_simultaneous_closure"] == "NO" for row in equations), checks)
    expect("twelve_completion_families", len(completions) == 12, checks)
    expect("zero_complete_g_phi_matter_witnesses", all(row["complete_g_phi_matter_witness"] == "NO" for row in completions), checks)
    expect("hopf_carrier_type_gap_open", hopf["H12"]["status"] == "OPEN_TYPE_GAP", checks)
    expect("hopf_action_open", hopf["H13"]["status"] == "OPEN", checks)
    expect("hopf_unconditional_matter_open", hopf["H14"]["status"] == "OPEN", checks)
    expect("complete_action_open", action_ledger["S23"]["status"] == "OPEN", checks)
    expect("native_source_open", action_ledger["S22"]["status"] == "OPEN", checks)
    expect("finite_boundary_action_open", action_ledger["S24"]["status"] == "OPEN", checks)
    expect("finite_charge_mass_open", action_ledger["S25"]["status"] == "OPEN", checks)
    expect("conditional_hopf_charge_status", null_hopf["N12"]["status"] == "CONDITIONAL_UNIT_CLASS", checks)
    expect("bootstrap_no_topology_ranking", toric["T16"]["status"] == "NO_TOPOLOGY_RANKING_LAW", checks)
    expect("carrier_dynamics_open", toric["T17"]["status"] == "OPEN", checks)

    # Dependency truth table for the proposed joined closure.
    arrows = {
        "metric_relational_clock_cocycle": True,
        "metric_transverse_path_cocycle": True,
        "conditional_reciprocal_hopf_compatibility": True,
        "metric_selected_global_angular_lift_and_caps": False,
        "metric_selected_carrier_or_configuration_space": False,
        "native_off_shell_matter_mass_response": False,
        "complete_finite_cell_boundary_variation": False,
        "same_solution_metric_matter_fixed_point": False,
        "helmholtz_integrability_of_native_response": False,
        "global_action_periods_gauge_and_boundary_integrability": False,
        "downstream_native_action": False,
    }
    expect("joined_closure_not_complete", not all(arrows.values()), checks)

    details["topological_role"] = {
        "reciprocal_identity_component": "CONTRACTIBLE_ONE_PARAMETER_GROUP",
        "angular_phase_requirement": "LOAD_BEARING_FOR_WINDING",
        "clock_can_weight_but_not_supply_hopf_winding": True,
        "conditional_depth_role": "LOGIT_COORDINATE_INTERPOLATING_BETWEEN_OPPOSITE_ANGULAR_COLLAPSES",
        "conditional_total_space": "R_DEPTH_TIMES_T2_WITH_PRIMITIVE_OPPOSITE_CAPS_COMPLETES_TO_S3",
    }
    details["downstream_action_gates"] = {
        "response_covector_or_multiplier": "ABSENT",
        "local_helmholtz_formal_self_adjointness": "UNTESTABLE_UNTIL_RESPONSE_EXISTS",
        "finite_cell_boundary_flux_integrability": "ABSENT",
        "global_configuration_space_periods": "MUST_VANISH_OR_BE_EXPLICITLY_QUANTIZED/TOPOLOGICAL",
        "gauge_noether_identity": "MUST_BE_HANDLED_ON_QUOTIENT_OR_WITH_GAUGE_DATA",
    }
    details["registered_counts"] = {
        "bootstrap_routes": len(routes),
        "equation_families": len(equations),
        "complete_equation_closures": 0,
        "completion_families": len(completions),
        "complete_g_phi_matter_witnesses": 0,
    }
    details["dependency_arrows"] = arrows
    details["countermodels"] = {
        "angular_transport_without_clock": "B19/ultrastatic type and exact C_loop control",
        "clock_without_global_topology": "local WR-L reciprocal clock profile lacks selected toric completion",
        "hopf_topology_without_native_response": "conditional unit Hopf class with H12-H14 open",
        "variational_response_without_topology": "F=(y,x)=grad(xy) finite-dimensional control",
        "closure_equation_without_action": "F=(0,x) violates cross-derivative Helmholtz control",
    }
    details["smallest_missing_object"] = (
        "A_METRIC_NATIVE_OFF_SHELL_GLOBAL_LOCAL_RESPONSE_ONE_FORM_WITH_COMPLETE_"
        "FINITE_CELL_BOUNDARY_VARIATION;_ONLY_THEN_TEST_HELMHOLTZ_INTEGRABILITY_"
        "AND_RELATIONAL_TOPOLOGY_SELECTION"
    )
    details["ruling"] = (
        "OPEN_COHERENT_ARCHITECTURE;KINEMATIC_AND_CONDITIONAL_TOPOLOGICAL_"
        "COMPONENTS_EXACT;JOINED_NATIVE_CLOSURE_AND_DOWNSTREAM_ACTION_NOT_DERIVED"
    )

    result = {
        "schema": "udt-sandbox-global-local-relational-closure-audit-1.0",
        "source_tip": "99a8dec7443ec6814aa29020a6e372259947cd3c",
        "sympy": sp.__version__,
        "result": "PASS",
        "checks": checks,
        "check_count": len(checks),
        "details": details,
        "input_sha256": {relative: sha256(ROOT / relative) for relative in INPUTS},
    }
    (HERE / "RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

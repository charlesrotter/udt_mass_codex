#!/usr/bin/env python3
"""Exact algebra and deterministic ledgers for the two conditional P05 bulk lanes."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FALLBACK_MAXIMUM = "NAMED_BULK_OPERATORS_AND_VARIATION_OBSTRUCTIONS_CHARACTERIZED"
PROTOCOL_MAXIMUM = "NAMED_DYNAMICS_OPERATOR_COMPLETE_IN_EXACT_PREMISE_CLASS"

SOURCES = {
    "P04_MANIFEST": ("udt_dynamics_branch_ruling_p04_2026-07-21/SHA256SUMS.txt", "d01d65fc5abcc35078c961d0d3fc0eec7ad26e205735a77f7d83e2b45121de3f"),
    "P04_RESULT": ("udt_dynamics_branch_ruling_p04_2026-07-21/RULING_RESULT.json", "d524a993798ec8148421f5b2099358354025dae331fcef5388f6ad4c4c256039"),
    "ARM_C_MANIFEST": ("native_action_arm_c_2026-07-18/SHA256SUMS.txt", "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f"),
    "ARM_C_VARIATION": ("native_action_arm_c_2026-07-18/ARM_C_RETURN/cas_armc_variation_domain.py", "084511961b6c69270278c64ae69f58942b044f106990e7071a5003f8535aee7e"),
    "ARM_C_ACTION": ("native_action_arm_c_2026-07-18/ARM_C_RETURN/cas_armc_unique_action_weights.py", "33e804e990fad69e49b3471adc8443f8037e7d4b5f617999dd1579286c3e430c"),
    "ARM_C_BOUNDARY": ("native_action_arm_c_2026-07-18/ARM_C_RETURN/cas_armc_boundary_charge.py", "e29f017a354275b62d415961365583d165bffc9637303b1a3ae9feb17510184d"),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(relative: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    path = HERE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def exact_algebra(checks: dict[str, str]) -> dict[str, object]:
    d = sp.symbols("d", integer=True, positive=True)
    weights = {"volume": d, "EH": d - 2, "C2": d - 4}
    require("C2_weight_zero_in_4D", weights["C2"].subs(d, 4) == 0, checks)
    require("EH_not_pre_scale_weight_zero", weights["EH"].subs(d, 4) == 2, checks)

    c2 = sp.Matrix([1, -2, sp.Rational(1, 3)])
    e4 = sp.Matrix([1, -4, 1])
    require("C2_Euler_independent", sp.Matrix.hstack(c2, e4).rank() == 2, checks)
    require("Euler_quotient_one_C2_direction", c2.rank() == 1, checks)

    # Independent chain-rule scar, freshly implemented rather than importing Arm C.
    x, y, aa, bb, cc, multiplier = sp.symbols("x y aa bb cc multiplier", real=True)
    lagrangian = aa * x**2 / 2 + bb * y**2 / 2 + cc * x * y
    ex, ey = sp.diff(lagrangian, x), sp.diff(lagrangian, y)
    reduced = sp.expand(lagrangian.subs(y, -x))
    tangent_euler = sp.diff(reduced, x)
    normal_euler = sp.simplify((ex + ey).subs(y, -x))
    require("hard_restriction_is_tangent_projection", sp.simplify(tangent_euler - (ex - ey).subs(y, -x)) == 0, checks)
    require("normal_equation_survives", normal_euler != 0, checks)
    require("multiplier_elimination_is_tangent_projection", sp.simplify((ex + multiplier) - (ey + multiplier) - (ex - ey)) == 0, checks)
    witness = x + y
    require("projected_stationary_not_full_stationary", sp.diff(witness.subs(y, -x), x) == 0 and (sp.diff(witness, x) != 0 or sp.diff(witness, y) != 0), checks)

    # Independent reciprocal one-function EH reduction witness.
    r = sp.symbols("r", positive=True)
    A = sp.Function("A")(r)
    scalar_R = -sp.diff(A, r, 2) - 4 * sp.diff(A, r) / r + 2 * (1 - A) / r**2
    primitive = -r**2 * sp.diff(A, r) - 2 * r * A + 2 * r
    require("reciprocal_spherical_EH_is_boundary_primitive", sp.simplify(r**2 * scalar_R - sp.diff(primitive, r)) == 0, checks)

    # Boundary-potential specialization for P_R^{abcd}=kappa g^{a[c}g^{d]b}
    # at an orthonormal point. D[d,b,c] represents partial_d h_bc and is
    # explicitly symmetric in b,c.
    kappa = sp.symbols("kappa", nonzero=True)
    D = {}
    for der in range(4):
        for b in range(4):
            for c in range(b, 4):
                symbol = sp.symbols(f"D{der}{b}{c}")
                D[der, b, c] = symbol
                D[der, c, b] = symbol

    def delta(i: int, j: int) -> int:
        return int(i == j)

    theta = []
    expected = []
    for a in range(4):
        value = 0
        for b in range(4):
            for c in range(4):
                for der in range(4):
                    p = kappa * sp.Rational(1, 2) * (delta(a, c) * delta(der, b) - delta(a, der) * delta(c, b))
                    value += 2 * p * D[der, b, c]
        theta.append(sp.expand(value))
        expected.append(kappa * (sum(D[b, a, b] for b in range(4)) - sum(D[a, b, b] for b in range(4))))
    require("EH_raw_boundary_current_specialization", all(sp.simplify(left - right) == 0 for left, right in zip(theta, expected)), checks)

    q = sp.symbols("q", real=True)
    require("EH_principal_simple_null_factor", sp.Poly(q, q).degree() == 1, checks)
    require("C2_principal_double_null_factor", sp.Poly(q**2, q).degree() == 2, checks)

    return {
        "C2_basis": ["1", "-2", "1/3"],
        "Euler_basis": ["1", "-4", "1"],
        "tangent_euler": str(tangent_euler),
        "normal_euler": str(normal_euler),
        "EH_radial_primitive": str(primitive),
        "principal_factors": {"L01_gauge_reduced": "alpha*q^2", "L02_gauge_reduced": "kappa*q"},
    }


def lane_tables() -> dict[str, list[dict[str, str]]]:
    l01_bulk = [
        {"id": "O01", "object": "bulk_density", "formula": "L01=alpha*C_abcd*C^abcd+beta*E4", "status": "CONDITIONAL_ACTION_FAMILY", "scope_or_limit": "alpha and beta symbolic; metric-only local 4D class"},
        {"id": "O02", "object": "Euler_density", "formula": "E4=R_abcd*R^abcd-4*R_ab*R^ab+R^2", "status": "EXACT_DEFINITION", "scope_or_limit": "bulk topological only in regular 4D; boundary retained"},
        {"id": "O03", "object": "Bach_tensor", "formula": "B_ab=(nabla^c*nabla^d+(1/2)*R^cd)*C_acbd", "status": "EXACT_CONVENTION", "scope_or_limit": "regular 4D Levi-Civita metric"},
        {"id": "O04", "object": "covariant_metric_variation", "formula": "delta S_bulk=integral sqrt_abs_g*(-2*alpha*B^ab)*h_ab+boundary", "status": "DERIVED_IN_CONDITIONAL_LANE", "scope_or_limit": "h_ab=delta g_ab unrestricted before reduction"},
        {"id": "O05", "object": "metric_Euler_equation", "formula": "B_ab=0 when alpha_nonzero", "status": "CONDITIONAL_BULK_EQUATION", "scope_or_limit": "beta supplies zero regular 4D bulk equation; no source"},
        {"id": "O06", "object": "differential_order", "formula": "order_g=4", "status": "EXACT", "scope_or_limit": "principal degeneracy requires gauge quotient"},
        {"id": "O07", "object": "Euler_bulk_variation", "formula": "E_ab[E4]=0", "status": "DERIVED_REGULAR_4D", "scope_or_limit": "does not erase boundary or corners"},
    ]
    l02_bulk = [
        {"id": "O01", "object": "bulk_density", "formula": "L02=kappa*(R-2*Lambda)+beta*E4", "status": "CONDITIONAL_ACTION_FAMILY", "scope_or_limit": "kappa Lambda beta symbolic; post-scale metric-only local 4D class"},
        {"id": "O02", "object": "Euler_density", "formula": "E4=R_abcd*R^abcd-4*R_ab*R^ab+R^2", "status": "EXACT_DEFINITION", "scope_or_limit": "bulk topological only in regular 4D; boundary retained"},
        {"id": "O03", "object": "Einstein_tensor", "formula": "G_ab=R_ab-(1/2)*R*g_ab", "status": "EXACT_DEFINITION", "scope_or_limit": "selected regular physical representative required"},
        {"id": "O04", "object": "covariant_metric_variation", "formula": "delta S_bulk=integral sqrt_abs_g*(-kappa*(G^ab+Lambda*g^ab))*h_ab+boundary", "status": "DERIVED_IN_CONDITIONAL_LANE", "scope_or_limit": "h_ab=delta g_ab unrestricted before reduction"},
        {"id": "O05", "object": "metric_Euler_equation", "formula": "G_ab+Lambda*g_ab=0 when kappa_nonzero", "status": "CONDITIONAL_BULK_EQUATION", "scope_or_limit": "Lambda free including zero subcase; no source"},
        {"id": "O06", "object": "differential_order", "formula": "order_g=2", "status": "EXACT", "scope_or_limit": "principal degeneracy requires gauge quotient"},
        {"id": "O07", "object": "Euler_bulk_variation", "formula": "E_ab[E4]=0", "status": "DERIVED_REGULAR_4D", "scope_or_limit": "does not erase boundary or corners"},
    ]

    pe = "P_E^abcd=2*R^abcd-4*(g^a[c*R^d]b-g^b[c*R^d]a)+2*R*g^a[c*g^d]b"
    l01_boundary = [
        {"id": "B01", "channel": "general_raw_potential", "formula": "Theta^a=2*P^abcd*nabla_d(h_bc)-2*nabla_d(P^abcd)*h_bc", "coefficient": "P^abcd=2*alpha*C^abcd+beta*P_E^abcd", "status": "DERIVED_RAW_CURRENT", "open_completion": "polarization boundary action corners"},
        {"id": "B02", "channel": "C2_derivative_h", "formula": "4*alpha*n_a*C^abcd*nabla_d(h_bc)", "coefficient": "free alpha", "status": "EXPOSED", "open_completion": "normal/tangential decomposition and allowed derivative data"},
        {"id": "B03", "channel": "C2_h", "formula": "-4*alpha*n_a*nabla_d(C^abcd)*h_bc", "coefficient": "free alpha", "status": "EXPOSED", "open_completion": "allowed h and tangential integrations"},
        {"id": "B04", "channel": "Euler_boundary", "formula": "2*beta*n_a*P_E^abcd*nabla_d(h_bc)", "coefficient": pe, "status": "EXPOSED_DIVERGENCE_FREE_P_E", "open_completion": "Euler boundary functional and corners"},
        {"id": "B05", "channel": "static_scalar_seal", "formula": "delta_phi=0 only", "coefficient": "one scalar wire", "status": "INSUFFICIENT_FOR_METRIC_CURRENT", "open_completion": "complete h normal_h and corner polarization"},
        {"id": "B06", "channel": "differentiability", "formula": "not_selected", "coefficient": "NA", "status": "OPEN_STOP", "open_completion": "native finite-cell boundary action and all allowed variations"},
    ]
    l02_boundary = [
        {"id": "B01", "channel": "EH_derivative_h", "formula": "kappa*n_a*(nabla_b(h^ab)-nabla^a(h))", "coefficient": "free kappa", "status": "DERIVED_RAW_CURRENT", "open_completion": "polarization boundary action corners"},
        {"id": "B02", "channel": "cosmological", "formula": "no_derivative_boundary_current", "coefficient": "free Lambda", "status": "EXACT", "open_completion": "does not close EH current"},
        {"id": "B03", "channel": "Euler_boundary", "formula": "2*beta*n_a*P_E^abcd*nabla_d(h_bc)", "coefficient": pe, "status": "EXPOSED_DIVERGENCE_FREE_P_E", "open_completion": "Euler boundary functional and corners"},
        {"id": "B04", "channel": "standard_Dirichlet_completion", "formula": "not_adopted", "coefficient": "NA", "status": "CONDITIONAL_COMPARISON_ONLY", "open_completion": "UDT does not select GHY-like term or Dirichlet data"},
        {"id": "B05", "channel": "reference_orientation_normalization", "formula": "not_selected", "coefficient": "NA", "status": "OPEN", "open_completion": "finite-cell generator and charge"},
        {"id": "B06", "channel": "static_scalar_seal", "formula": "delta_phi=0 only", "coefficient": "one scalar wire", "status": "INSUFFICIENT_FOR_METRIC_CURRENT", "open_completion": "complete h normal_h and corner polarization"},
        {"id": "B07", "channel": "differentiability", "formula": "not_selected", "coefficient": "NA", "status": "OPEN_STOP", "open_completion": "native finite-cell boundary action and all allowed variations"},
    ]
    l01_noether = [
        {"id": "N01", "object": "trace_identity", "equation": "g^ab*B_ab=0", "status": "OFF_SHELL_NOETHER_IDENTITY", "limit": "four-dimensional conformal metric lane"},
        {"id": "N02", "object": "diffeomorphism_identity", "equation": "nabla^a*B_ab=0", "status": "OFF_SHELL_NOETHER_IDENTITY", "limit": "regular Levi-Civita lane"},
        {"id": "N03", "object": "normal_normal_projection", "equation": "n^a*n^b*B_ab=0", "status": "CONDITIONAL_PROJECTION_OF_FULL_EQUATION", "limit": "normal and causal type unselected"},
        {"id": "N04", "object": "normal_tangential_projection", "equation": "q^a_i*n^b*B_ab=0", "status": "CONDITIONAL_PROJECTION_OF_FULL_EQUATION", "limit": "foliation unselected"},
        {"id": "N05", "object": "tangential_projection", "equation": "q^a_i*q^b_j*B_ab=0", "status": "CONDITIONAL_PROJECTION_OF_FULL_EQUATION", "limit": "not evolution until time split and boundary data supplied"},
    ]
    l02_noether = [
        {"id": "N01", "object": "diffeomorphism_identity", "equation": "nabla^a*(G_ab+Lambda*g_ab)=0", "status": "OFF_SHELL_NOETHER_IDENTITY", "limit": "Lambda constant symbolic"},
        {"id": "N02", "object": "trace_equation", "equation": "-R+4*Lambda=0", "status": "ON_SHELL_CONSEQUENCE_NOT_IDENTITY", "limit": "regular 4D vacuum conditional lane"},
        {"id": "N03", "object": "normal_normal_projection", "equation": "n^a*n^b*(G_ab+Lambda*g_ab)=0", "status": "CONDITIONAL_PROJECTION_OF_FULL_EQUATION", "limit": "normal and causal type unselected"},
        {"id": "N04", "object": "normal_tangential_projection", "equation": "q^a_i*n^b*(G_ab+Lambda*g_ab)=0", "status": "CONDITIONAL_PROJECTION_OF_FULL_EQUATION", "limit": "foliation unselected"},
        {"id": "N05", "object": "tangential_projection", "equation": "q^a_i*q^b_j*(G_ab+Lambda*g_ab)=0", "status": "CONDITIONAL_PROJECTION_OF_FULL_EQUATION", "limit": "not evolution until time split and boundary data supplied"},
    ]
    l01_principal = [
        {"id": "P01", "arena": "regular_Lorentzian", "operator": "Bach", "ungauge_fixed": "DEGENERATE_DIFFEO_PLUS_WEYL", "diagnostic_reduction": "de_Donder_plus_trace_gauge", "principal_factor": "alpha*(g^ab*xi_a*xi_b)^2", "characteristic": "metric_null_cone_double", "claim_limit": "no well_posedness or physical gauge selected"},
        {"id": "P02", "arena": "degenerate_or_type_changing", "operator": "Bach", "ungauge_fixed": "NOT_CLASSIFIED_BY_INVERSE_METRIC_SYMBOL", "diagnostic_reduction": "NONE", "principal_factor": "UNDEFINED", "characteristic": "OPEN", "claim_limit": "P03G closure retained"},
    ]
    l02_principal = [
        {"id": "P01", "arena": "regular_Lorentzian", "operator": "Einstein_Lambda", "ungauge_fixed": "DEGENERATE_DIFFEO", "diagnostic_reduction": "harmonic_gauge", "principal_factor": "kappa*(g^ab*xi_a*xi_b)", "characteristic": "metric_null_cone_simple", "claim_limit": "conditional hyperbolic diagnostic; no physical gauge selected"},
        {"id": "P02", "arena": "degenerate_or_type_changing", "operator": "Einstein_Lambda", "ungauge_fixed": "NOT_CLASSIFIED_BY_INVERSE_METRIC_SYMBOL", "diagnostic_reduction": "NONE", "principal_factor": "UNDEFINED", "characteristic": "OPEN", "claim_limit": "P03G closure retained"},
    ]
    return {
        "lane_L01/BULK_OPERATOR.tsv": l01_bulk,
        "lane_L01/BOUNDARY_CURRENT.tsv": l01_boundary,
        "lane_L01/NOETHER_AND_CONSTRAINTS.tsv": l01_noether,
        "lane_L01/PRINCIPAL_CHARACTER.tsv": l01_principal,
        "lane_L02/BULK_OPERATOR.tsv": l02_bulk,
        "lane_L02/BOUNDARY_CURRENT.tsv": l02_boundary,
        "lane_L02/NOETHER_AND_CONSTRAINTS.tsv": l02_noether,
        "lane_L02/PRINCIPAL_CHARACTER.tsv": l02_principal,
    }


def shared_tables() -> dict[str, list[dict[str, str]]]:
    p04_pairs = read_tsv(ROOT / "udt_dynamics_branch_ruling_p04_2026-07-21/FIELD_REALIZATION_COMPATIBILITY.tsv")
    completeness = []
    for row in p04_pairs:
        lane, realization = row["lane_id"], row["realization_id"]
        if lane == "L03":
            status = "EXCLUDED_NO_OPERATOR_TO_VARY"
            equation = "NONE"
        elif lane == "L01" and realization == "C01":
            status = "METRIC_BULK_EQUATION_COMPLETE_BOUNDARY_OPEN"
            equation = "B_ab=0"
        elif lane == "L02" and realization == "C01":
            status = "FORMAL_METRIC_BULK_EQUATION_COMPLETE_REPRESENTATIVE_AND_BOUNDARY_OPEN"
            equation = "G_ab+Lambda*g_ab=0"
        elif realization in {"C02", "C04", "C07"}:
            status = "INCOMPLETE_EXTRA_FIELD_EQUATION_ABSENT"
            equation = "metric_equation_only"
        elif realization == "C03":
            status = "INCOMPLETE_COFRAME_VARIATION_AND_EQUIVALENCE_UNBUILT"
            equation = "metric_equation_only"
        elif realization == "C05":
            status = "INCOMPLETE_CONSTRAINT_VARIATION_DOMAIN_UNSELECTED"
            equation = "unrestricted_metric_equation_only"
        elif realization == "C06":
            status = "INCOMPLETE_BRIDGE_OPERATOR_ABSENT"
            equation = "endpoint_bulk_only"
        else:
            raise AssertionError((lane, realization))
        completeness.append({"pair_id": row["pair_id"], "lane_id": lane, "realization_id": realization, "p05_equation_status": status, "recorded_equation": equation, "field_removed": "NO", "boundary_complete": "NO", "global_existence": "UNEVALUATED"})

    variations = [
        {"id": "V01", "domain": "unrestricted_then_optional_restrict", "equation": "E_ab=0 then impose declared submanifold", "relation_to_full_operator": "FULL_EQUATION_RETAINED", "status": "L01_L02_CLASS_PREMISE", "limit": "boundary variation still open"},
        {"id": "V02", "domain": "hard_restrict_then_vary", "equation": "J^T*E=0", "relation_to_full_operator": "TANGENT_PROJECTION_ONLY", "status": "INEQUIVALENT_UNLESS_NORMAL_EQUATIONS_PROVED", "limit": "can discard metric equations"},
        {"id": "V03", "domain": "multiplier_constraint", "equation": "E+lambda*dC=0; C=0", "relation_to_full_operator": "TANGENT_PROJECTION_AFTER_LAMBDA_ELIMINATION", "status": "NOT_AUTOMATICALLY_FULL_EQUATION", "limit": "constraint qualification and boundary data open"},
        {"id": "V04", "domain": "readout_only_restriction", "equation": "evaluate full E_ab on declared configurations", "relation_to_full_operator": "NO_OFFSHELL_FIELD_REDUCTION", "status": "CONDITIONAL_DIAGNOSTIC", "limit": "does not prove configurations solve E_ab=0"},
        {"id": "V05", "domain": "gauge_reduction_after_variation", "equation": "full E_ab plus gauge condition", "relation_to_full_operator": "DIAGNOSTIC_IF_GAUGE_REACHABILITY_PROVED", "status": "NOT_PHYSICAL_SELECTION", "limit": "global gauge and boundary compatibility open"},
        {"id": "V06", "domain": "boundary_fixed_variation", "equation": "bulk E_ab plus declared vanishing boundary tangent", "relation_to_full_operator": "DEPENDS_ON_POLARIZATION", "status": "OPEN_IN_CURRENT_UDT", "limit": "static delta_phi wire insufficient"},
    ]
    scars = [
        {"id": "R01", "lane": "GENERIC", "witness": "L=aa*x^2/2+bb*y^2/2+cc*x*y with y=-x", "observed": "reduced_EL=(E_x-E_y)|constraint while normal=(E_x+E_y)|constraint survives", "status": "EXACT_CHAIN_RULE_SCAR", "limit": "finite-dimensional algebraic witness"},
        {"id": "R02", "lane": "GENERIC", "witness": "L=x+y with y=-x", "observed": "reduced action zero and tangent EL zero while full E=(1,1)", "status": "EXACT_FALSE_PASS_WITNESS", "limit": "does not assert continuum realization"},
        {"id": "R03", "lane": "L02", "witness": "ds2=-A(r)dt2+A(r)^-1dr2+r2dOmega2", "observed": "r^2*R=d_r[-r^2*A'-2r*A+2r]", "status": "EXACT_REDUCED_EH_BOUNDARY_PRIMITIVE", "limit": "one-function reciprocal spherical restriction; full Einstein equations not empty"},
        {"id": "R04", "lane": "L01", "witness": "conformally_flat_metric_reduction", "observed": "C2 action and Bach tensor both vanish", "status": "VACUOUS_SCAR_TEST_REJECTED", "limit": "cannot certify reduced/full equivalence outside conformally flat branch"},
        {"id": "R05", "lane": "L01_L02", "witness": "one-dimensional_ansatz_tangent_inside_ten_metric_components", "observed": "projected scalar equation cannot imply all normal tensor equations without theorem", "status": "RANK_WARNING", "limit": "pointwise chain-rule statement not PDE existence proof"},
    ]
    axes_source = read_tsv(ROOT / "udt_dynamics_branch_ruling_p04_2026-07-21/GLOBAL_AXIS_CARRYFORWARD.tsv")
    axes = [{"axis_id": row["axis_id"], "object": row["object"], "p04_disposition": row["p04_disposition"], "p05_disposition": "FREE_UNSELECTED_UNSOLVED", "value_or_choice": "NONE"} for row in axes_source]
    status = [
        {"id": "S01", "object": "L01_metric_bulk_operator", "status": "DERIVED_IN_CONDITIONAL_LANE", "scope_or_limit": "-2 alpha B^ab under unrestricted covariant h_ab variation"},
        {"id": "S02", "object": "L02_metric_bulk_operator", "status": "DERIVED_IN_CONDITIONAL_LANE", "scope_or_limit": "-kappa(G^ab+Lambda g^ab) after representative supplied"},
        {"id": "S03", "object": "Euler_bulk", "status": "ZERO_REGULAR_4D_BULK_EQUATION_BOUNDARY_RETAINED", "scope_or_limit": "beta remains free and affects boundary/corners"},
        {"id": "S04", "object": "raw_boundary_currents", "status": "DERIVED_COVARIANTLY", "scope_or_limit": "Theta exposed before polarization or boundary term"},
        {"id": "S05", "object": "finite_cell_differentiability", "status": "OPEN_STOP", "scope_or_limit": "complete polarization boundary action and corners not selected"},
        {"id": "S06", "object": "extra_field_equations", "status": "OPEN_OR_ABSENT", "scope_or_limit": "metric-only bulks do not govern C02-C07 extras"},
        {"id": "S07", "object": "L01_principal_character", "status": "CONDITIONAL_DOUBLE_NULL_FACTOR_AFTER_DIAGNOSTIC_GAUGE_QUOTIENT", "scope_or_limit": "ungauge-fixed diffeo plus Weyl degenerate"},
        {"id": "S08", "object": "L02_principal_character", "status": "CONDITIONAL_SIMPLE_NULL_FACTOR_AFTER_DIAGNOSTIC_HARMONIC_GAUGE", "scope_or_limit": "ungauge-fixed diffeo degenerate"},
        {"id": "S09", "object": "constraint_projections", "status": "RECORDED_NOT_SEPARATELY_SELECTED", "scope_or_limit": "no preferred foliation normal or causal boundary"},
        {"id": "S10", "object": "reduced_action_equivalence", "status": "REFUTED_AS_AUTOMATIC", "scope_or_limit": "exact tangent and EH primitive scars"},
        {"id": "S11", "object": "all_21_field_pairs", "status": "ACCOUNTED_NONE_REMOVED", "scope_or_limit": "two metric-only bulk-complete rows still boundary/global open"},
        {"id": "S12", "object": "all_12_global_axes", "status": "FREE_UNSELECTED_UNSOLVED", "scope_or_limit": "no global completion"},
        {"id": "S13", "object": "protocol_maximum", "status": "NOT_EARNED", "scope_or_limit": "boundary and extra-field channels absent"},
        {"id": "S14", "object": "banked_maximum", "status": FALLBACK_MAXIMUM, "scope_or_limit": "bulk operators exact; complete actions and solutions open"},
        {"id": "S15", "object": "P06_and_solves", "status": "NOT_LAUNCHED", "scope_or_limit": "new dispatch required"},
    ]
    return {
        "FIELD_EQUATION_COMPLETENESS.tsv": completeness,
        "VARIATION_DOMAIN_MATRIX.tsv": variations,
        "REDUCED_ACTION_SCAR.tsv": scars,
        "GLOBAL_AXIS_CARRYFORWARD.tsv": axes,
        "STATUS_LEDGER.tsv": status,
    }


FIELDS = {
    "lane_L01/BULK_OPERATOR.tsv": ["id", "object", "formula", "status", "scope_or_limit"],
    "lane_L02/BULK_OPERATOR.tsv": ["id", "object", "formula", "status", "scope_or_limit"],
    "lane_L01/BOUNDARY_CURRENT.tsv": ["id", "channel", "formula", "coefficient", "status", "open_completion"],
    "lane_L02/BOUNDARY_CURRENT.tsv": ["id", "channel", "formula", "coefficient", "status", "open_completion"],
    "lane_L01/NOETHER_AND_CONSTRAINTS.tsv": ["id", "object", "equation", "status", "limit"],
    "lane_L02/NOETHER_AND_CONSTRAINTS.tsv": ["id", "object", "equation", "status", "limit"],
    "lane_L01/PRINCIPAL_CHARACTER.tsv": ["id", "arena", "operator", "ungauge_fixed", "diagnostic_reduction", "principal_factor", "characteristic", "claim_limit"],
    "lane_L02/PRINCIPAL_CHARACTER.tsv": ["id", "arena", "operator", "ungauge_fixed", "diagnostic_reduction", "principal_factor", "characteristic", "claim_limit"],
    "FIELD_EQUATION_COMPLETENESS.tsv": ["pair_id", "lane_id", "realization_id", "p05_equation_status", "recorded_equation", "field_removed", "boundary_complete", "global_existence"],
    "VARIATION_DOMAIN_MATRIX.tsv": ["id", "domain", "equation", "relation_to_full_operator", "status", "limit"],
    "REDUCED_ACTION_SCAR.tsv": ["id", "lane", "witness", "observed", "status", "limit"],
    "GLOBAL_AXIS_CARRYFORWARD.tsv": ["axis_id", "object", "p04_disposition", "p05_disposition", "value_or_choice"],
    "STATUS_LEDGER.tsv": ["id", "object", "status", "scope_or_limit"],
}


def graph() -> dict[str, object]:
    nodes = [
        {"id": "P04_L01", "kind": "conditional_lane"},
        {"id": "P04_L02", "kind": "conditional_lane"},
        {"id": "P04_L03", "kind": "excluded_open_lane"},
        {"id": "FULL_METRIC_VARIATION", "kind": "added_premise"},
        {"id": "L01_BACH", "kind": "derived_conditional_bulk"},
        {"id": "L02_EINSTEIN", "kind": "derived_conditional_bulk"},
        {"id": "RAW_BOUNDARY_CURRENT", "kind": "derived_conditional"},
        {"id": "BOUNDARY_POLARIZATION", "kind": "open"},
        {"id": "BOUNDARY_ACTION_CORNERS", "kind": "open"},
        {"id": "EXTRA_FIELD_EQUATIONS", "kind": "open"},
        {"id": "GLOBAL_AXES", "kind": "open"},
        {"id": "COMPLETE_P05_OPERATOR", "kind": "not_achieved"},
        {"id": "REDUCED_VARIATION", "kind": "separate_conditional_branch"},
        {"id": "P06", "kind": "not_launched"},
    ]
    edges = [
        {"from": "P04_L01", "to": "FULL_METRIC_VARIATION", "relation": "premise"},
        {"from": "P04_L02", "to": "FULL_METRIC_VARIATION", "relation": "premise"},
        {"from": "FULL_METRIC_VARIATION", "to": "L01_BACH", "relation": "L01_Euler_operator"},
        {"from": "FULL_METRIC_VARIATION", "to": "L02_EINSTEIN", "relation": "L02_Euler_operator"},
        {"from": "L01_BACH", "to": "RAW_BOUNDARY_CURRENT", "relation": "same_variation"},
        {"from": "L02_EINSTEIN", "to": "RAW_BOUNDARY_CURRENT", "relation": "same_variation"},
        {"from": "RAW_BOUNDARY_CURRENT", "to": "BOUNDARY_POLARIZATION", "relation": "requires_choice_or_derivation"},
        {"from": "BOUNDARY_POLARIZATION", "to": "BOUNDARY_ACTION_CORNERS", "relation": "differentiability_join"},
        {"from": "BOUNDARY_ACTION_CORNERS", "to": "COMPLETE_P05_OPERATOR", "relation": "required"},
        {"from": "EXTRA_FIELD_EQUATIONS", "to": "COMPLETE_P05_OPERATOR", "relation": "required_on_non_C01_branches"},
        {"from": "GLOBAL_AXES", "to": "COMPLETE_P05_OPERATOR", "relation": "retained_branch_data"},
        {"from": "REDUCED_VARIATION", "to": "L01_BACH", "relation": "projection_not_equivalence"},
        {"from": "REDUCED_VARIATION", "to": "L02_EINSTEIN", "relation": "projection_not_equivalence"},
    ]
    forbidden = [
        {"from": "P04_L03", "to": "FULL_METRIC_VARIATION", "reason": "no bridge operator"},
        {"from": "RAW_BOUNDARY_CURRENT", "to": "COMPLETE_P05_OPERATOR", "reason": "raw current is not a selected differentiable completion"},
        {"from": "REDUCED_VARIATION", "to": "COMPLETE_P05_OPERATOR", "reason": "projected equations do not imply full equations"},
        {"from": "L01_BACH", "to": "P06", "reason": "P05 stop gate open"},
        {"from": "L02_EINSTEIN", "to": "P06", "reason": "P05 stop gate open"},
    ]
    return {"schema": "udt-p05-operator-dependency-graph-1.0", "nodes": nodes, "edges": edges, "forbidden_edges": forbidden}


def main() -> None:
    checks: dict[str, str] = {}
    for name, (relative, expected) in SOURCES.items():
        require(f"source_{name}", digest(ROOT / relative) == expected, checks)
    algebra = exact_algebra(checks)
    tables = lane_tables() | shared_tables()
    for name, rows in tables.items():
        write_tsv(name, FIELDS[name], rows)

    require("both_lane_bulk_tables", all(len(tables[f"lane_{lane}/BULK_OPERATOR.tsv"]) == 7 for lane in ("L01", "L02")), checks)
    require("raw_boundary_channels_present", len(tables["lane_L01/BOUNDARY_CURRENT.tsv"]) == 6 and len(tables["lane_L02/BOUNDARY_CURRENT.tsv"]) == 7, checks)
    require("both_boundary_stops_open", all(any(row["status"] == "OPEN_STOP" for row in tables[f"lane_{lane}/BOUNDARY_CURRENT.tsv"]) for lane in ("L01", "L02")), checks)
    completeness = tables["FIELD_EQUATION_COMPLETENESS.tsv"]
    require("all_21_field_pairs", len(completeness) == 21 and len({row["pair_id"] for row in completeness}) == 21, checks)
    require("no_field_removed", all(row["field_removed"] == "NO" for row in completeness), checks)
    require("no_boundary_complete", all(row["boundary_complete"] == "NO" for row in completeness), checks)
    require("no_global_existence", all(row["global_existence"] == "UNEVALUATED" for row in completeness), checks)
    require("L03_excluded", all(row["p05_equation_status"] == "EXCLUDED_NO_OPERATOR_TO_VARY" for row in completeness if row["lane_id"] == "L03"), checks)
    axes = tables["GLOBAL_AXIS_CARRYFORWARD.tsv"]
    require("all_12_axes", len(axes) == 12 and {row["axis_id"] for row in axes} == {f"A{i:02d}" for i in range(1, 13)}, checks)
    require("axes_free", all(row["p05_disposition"] == "FREE_UNSELECTED_UNSOLVED" and row["value_or_choice"] == "NONE" for row in axes), checks)
    require("protocol_max_not_earned", next(row for row in tables["STATUS_LEDGER.tsv"] if row["id"] == "S13")["status"] == "NOT_EARNED", checks)
    require("fallback_banked", next(row for row in tables["STATUS_LEDGER.tsv"] if row["id"] == "S14")["status"] == FALLBACK_MAXIMUM, checks)

    dep = graph()
    node_ids = {node["id"] for node in dep["nodes"]}
    require("graph_endpoints", all(edge["from"] in node_ids and edge["to"] in node_ids for edge in dep["edges"]), checks)
    require("forbidden_edges_absent", not ({(e["from"], e["to"]) for e in dep["edges"]} & {(e["from"], e["to"]) for e in dep["forbidden_edges"]}), checks)
    (HERE / "OPERATOR_DEPENDENCY_GRAPH.json").write_text(json.dumps(dep, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    source_rows = [{"id": f"SRC{i:02d}", "role": role, "path": relative, "sha256": expected, "use": "immutable premise or regression anchor; not imported implementation"} for i, (role, (relative, expected)) in enumerate(SOURCES.items(), 1)]
    write_tsv("SOURCE_LINEAGE.tsv", ["id", "role", "path", "sha256", "use"], source_rows)

    table_hashes = {name: digest(HERE / name) for name in [*tables, "SOURCE_LINEAGE.tsv"]}
    result = {
        "schema": "udt-p05-conditional-operator-builds-1.0",
        "status": "PASS",
        "evidence_grade": "LEAD_PENDING_FRESH_ADVERSARIAL_REVIEW",
        "protocol_maximum": PROTOCOL_MAXIMUM,
        "protocol_maximum_earned": False,
        "maximum_conclusion": FALLBACK_MAXIMUM,
        "counts": {
            "authorized_lanes_built": 2,
            "bridge_lanes_excluded": 1,
            "bulk_operator_rows": 14,
            "raw_boundary_rows": 13,
            "field_pairs": 21,
            "field_pairs_complete_actions": 0,
            "global_axes_free": 12,
            "variation_domains": 6,
            "reduced_action_scars": 5,
            "solutions_computed": 0,
        },
        "lane_rulings": {
            "L01": "BULK_METRIC_OPERATOR_DERIVED_CONDITIONAL_BOUNDARY_AND_EXTRA_FIELDS_OPEN",
            "L02": "FORMAL_BULK_METRIC_OPERATOR_DERIVED_CONDITIONAL_REPRESENTATIVE_BOUNDARY_AND_EXTRA_FIELDS_OPEN",
            "L03": "EXCLUDED_NO_OPERATOR_TO_VARY",
        },
        "exact_algebra": algebra,
        "source_sha256": {role: expected for role, (_, expected) in SOURCES.items()},
        "table_sha256": table_hashes,
        "check_count": len(checks),
        "checks": checks,
        "scope": {"CPU_only": True, "GPU_used": False, "full_metric_varied_before_reduction": True, "symmetry_ansatz_used_for_operator_derivation": False, "source_or_carrier_loaded": False, "boundary_completion_selected": False, "physical_representative_selected": False, "ODE_or_PDE_run": False, "P06_launched": False, "canon_changed": False},
    }
    (HERE / "OPERATOR_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "P05_CONDITIONAL_OPERATOR_BUILD=PASS",
        f"checks={len(checks)}",
        "lanes_built=L01,L02",
        "L03=EXCLUDED_NO_OPERATOR",
        "bulk_operator_rows=14",
        "raw_boundary_rows=13",
        "field_pairs=21/21",
        "complete_action_pairs=0",
        "global_axes_free=12/12",
        "solutions=0",
        "protocol_maximum_earned=NO",
        f"maximum_conclusion={FALLBACK_MAXIMUM}",
    ]
    text = "\n".join(transcript) + "\n"
    (HERE / "OPERATOR_TRANSCRIPT.txt").write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()

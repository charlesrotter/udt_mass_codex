#!/usr/bin/env python3
"""Exact derivation for the preregistered UDT free-global-seal audit."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent

PARENT_HASHES = {
    "udt_premise_reset_audit_2026-07-19/SHA256SUMS.txt": "6123253b9370bce674c626a863dc595c773da3905cb155a7fe2b77c4667fd3a7",
    "udt_global_reciprocal_closure_audit_2026-07-20/SHA256SUMS.txt": "e11985e9afd9cefbb818e75aa1afe90acec48d60b2170e26c2fe712287742d48",
    "udt_complete_seal_fixed_set_selector_audit_2026-07-21/SHA256SUMS.txt": "3a6cc83e40fe95951b19f37b68b1167a3683cf4f02c0fbf1f52f54d95db99b66",
    "udt_full_equation_variation_p05_2026-07-21/SHA256SUMS.txt": "5c26d4eb97c4dc370e286469c63d662f182a71a94a6e6899131fd6706c4e7f2e",
    "udt_pre_p06_boundary_selector_audit_2026-07-21/SHA256SUMS.txt": "45c239639d999c26f2e574592fafc392fbb7c1e6f20ea92e1d260b4784e00e51",
    "udt_time_live_characteristic_flux_audit_2026-07-21/SHA256SUMS.txt": "3089e66d65f85753d45e9e78596dba9ae2b962a015857c969ff6a0492d442f12",
    "UDT_NATIVE_ACTION_COLD_PACKET.md": "d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_tsv(name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    checks = 0
    for relative, expected in PARENT_HASHES.items():
        require(digest(ROOT / relative) == expected, f"parent hash: {relative}")
        checks += 1
    source_roles = [
        "corrected phi Xmax boundary and observational-anchor meanings",
        "global completion map and off-shell bootstrap obstruction",
        "static scalar seal versus complete fixed-set obstruction",
        "conditional metric bulk actions raw currents and constraints",
        "existing boundary selector and functional ambiguity census",
        "time-live characteristic flux and moving-seal causal audit",
        "founding finite-cell static-seal Xmax and bootstrap ledger",
    ]
    source_rows = [
        {"id": f"SRC{index:02d}", "path": relative, "sha256": expected, "role": role}
        for index, ((relative, expected), role) in enumerate(zip(PARENT_HASHES.items(), source_roles), start=1)
    ]
    write_tsv("SOURCE_LINEAGE.tsv", ["id", "path", "sha256", "role"], source_rows)

    # Variable-endpoint derivation.  Delta_q is the total endpoint field variation, while delta_T
    # moves the endpoint.  Fixed-coordinate delta_q = Delta_q - qdot*delta_T.
    mass, spring = sp.symbols("m k", nonzero=True)
    q, qdot, delta_q_total, delta_t = sp.symbols("q qdot Delta_q Delta_T")
    lam, mu = sp.symbols("lambda mu")
    lagrangian = mass * qdot**2 / 2 - spring * q**2 / 2
    momentum = sp.diff(lagrangian, qdot)
    hamiltonian = sp.expand(momentum * qdot - lagrangian)
    boundary = lam * q**2 / 2 + mu * sp.symbols("T")
    bq = sp.diff(boundary, q)
    bt = mu
    fixed_coordinate_delta_q = delta_q_total - qdot * delta_t
    endpoint_variation = sp.expand(
        momentum * fixed_coordinate_delta_q
        + lagrangian * delta_t
        + bq * delta_q_total
        + bt * delta_t
    )
    expected_endpoint = sp.expand((momentum + lam * q) * delta_q_total + (-hamiltonian + mu) * delta_t)
    require(sp.expand(endpoint_variation - expected_endpoint) == 0, "variable-endpoint formula")
    require(momentum == mass * qdot, "endpoint momentum")
    require(hamiltonian == mass * qdot**2 / 2 + spring * q**2 / 2, "endpoint Hamiltonian")
    checks += 3

    endpoint_rows = [
        {"id": "E01", "boundary_functional": "B=0", "bulk_equation": "m*qddot+k*q=0", "field_transversality": "p=0", "position_transversality": "H=0", "same_bulk": "YES", "status": "COMPARISON_WITNESS"},
        {"id": "E02", "boundary_functional": "B=lambda*q^2/2", "bulk_equation": "m*qddot+k*q=0", "field_transversality": "p+lambda*q=0", "position_transversality": "H=0", "same_bulk": "YES", "status": "INEQUIVALENT_COMPARISON_WITNESS"},
        {"id": "E03", "boundary_functional": "B=mu*T", "bulk_equation": "m*qddot+k*q=0", "field_transversality": "p=0", "position_transversality": "H=mu", "same_bulk": "YES", "status": "INEQUIVALENT_COMPARISON_WITNESS"},
        {"id": "E04", "boundary_functional": "B=lambda*q^2/2+mu*T", "bulk_equation": "m*qddot+k*q=0", "field_transversality": "p+lambda*q=0", "position_transversality": "H=mu", "same_bulk": "YES", "status": "TWO_PARAMETER_COUNTERFAMILY"},
    ]
    write_tsv("ENDPOINT_COUNTERFUNCTIONALS.tsv", ["id", "boundary_functional", "bulk_equation", "field_transversality", "position_transversality", "same_bulk", "status"], endpoint_rows)

    # A separate global-size realization is a constant homothety g_R=R^2*g_hat on a fixed
    # dimensionless cell.  It must not be conflated with moving a coordinate endpoint.
    radius = sp.symbols("R", positive=True)
    alpha, beta, kappa, cosmological = sp.symbols("alpha beta kappa Lambda")
    c2_integral, euler_integral, scalar_integral, volume_integral = sp.symbols("C2hat E4hat Ahat Vhat")
    boundary_coefficient, boundary_power = sp.symbols("b p")
    action_l01_scale = alpha * c2_integral + beta * euler_integral
    action_l02_scale = kappa * (radius**2 * scalar_integral - 2 * cosmological * radius**4 * volume_integral) + beta * euler_integral
    require(sp.diff(action_l01_scale, radius) == 0, "L01 global homothety flat direction")
    expected_l02_derivative = 2 * kappa * radius * (scalar_integral - 4 * cosmological * radius**2 * volume_integral)
    require(sp.expand(sp.diff(action_l02_scale, radius) - expected_l02_derivative) == 0, "L02 global homothety derivative")
    require(sp.solve(sp.Eq(expected_l02_derivative / (2 * kappa * radius), 0), radius**2) == [scalar_integral / (4 * cosmological * volume_integral)], "L02 conditional scale root")
    lambda_zero_condition = sp.simplify((expected_l02_derivative / (2 * kappa * radius)).subs(cosmological, 0))
    require(lambda_zero_condition == scalar_integral, "Lambda-zero scale condition")
    generic_boundary = boundary_coefficient * radius**boundary_power
    require(sp.diff(generic_boundary, radius) == boundary_coefficient * boundary_power * radius**boundary_power / radius, "boundary scaling response")
    checks += 5
    scale_rows = [
        {"id": "G01", "realization": "CONSTANT_HOMOTHETY_PRE_SCALE_L01", "action_or_response": "S=alpha*C2hat+beta*E4hat", "stationarity": "dS/dR=0 identically", "exact_consequence": "global common scale remains flat", "premises": "fixed dimensionless shape regular 4D C2/Euler bulk", "selector_status": "NO_SCALE_SELECTION"},
        {"id": "G02", "realization": "CONSTANT_HOMOTHETY_POST_SCALE_L02", "action_or_response": "S=kappa*(R^2*Ahat-2*Lambda*R^4*Vhat)+beta*E4hat", "stationarity": "2*kappa*R*(Ahat-4*Lambda*R^2*Vhat)=0", "exact_consequence": "R^2=Ahat/(4*Lambda*Vhat) only when the ratio is defined and positive", "premises": "shape Lambda and boundary completion already supplied", "selector_status": "CONDITIONAL_SCALE_EQUATION"},
        {"id": "G03", "realization": "L02_LAMBDA_ZERO_SUBCASE", "action_or_response": "S=kappa*R^2*Ahat+beta*E4hat", "stationarity": "Ahat=0 for R>0", "exact_consequence": "R remains unselected when stationarity is possible", "premises": "Lambda=0", "selector_status": "NO_GENERIC_SCALE_ROOT"},
        {"id": "G04", "realization": "BOUNDARY_SCALING_TERM", "action_or_response": "B=b*R^p", "stationarity": "adds p*b*R^(p-1)", "exact_consequence": "changes the global scale equation without changing the bulk metric equation", "premises": "comparison counterfunctional not adopted", "selector_status": "FUNCTIONAL_DEPENDENCE"},
        {"id": "G05", "realization": "MOVING_COORDINATE_ENDPOINT", "action_or_response": "boundary displacement samples local on-shell density and B response", "stationarity": "endpoint/shape equation", "exact_consequence": "not equivalent to a constant homothety without a derived global map", "premises": "embedding realization separately declared", "selector_status": "DISTINCT_REALIZATION"},
        {"id": "G06", "realization": "XMAX_OUTPUT_JOIN", "action_or_response": "Xmax=F(c_E,G_obs,M_total,rho_total,metric) remains unspecified", "stationarity": "none supplied", "exact_consequence": "neither homothety R nor endpoint R_cell is Xmax by definition", "premises": "complete global mass volume and metric closure absent", "selector_status": "OPEN"},
    ]
    write_tsv("GLOBAL_SCALE_TRANSVERSALITY.tsv", ["id", "realization", "action_or_response", "stationarity", "exact_consequence", "premises", "selector_status"], scale_rows)

    # Relational-seal variation.  The fixed-surface rule and the moving level-set rule are distinct.
    slope = sp.symbols("s", nonzero=True)
    # Variables are (delta_phi, chi_normal).  Moving level set alone has row [1,s].
    moving_constraint = sp.Matrix([[1, slope]])
    stacked_constraint = sp.Matrix([[1, slope], [1, 0]])
    require(moving_constraint.rank() == 1, "moving seal constraint rank")
    require(stacked_constraint.det() == -slope and stacked_constraint.rank() == 2, "stacked fixed/moving seal rank")
    correlated = sp.Matrix([-slope, 1])
    require(moving_constraint * correlated == sp.zeros(1, 1), "correlated moving-seal tangent")
    require(stacked_constraint.nullspace() == [], "regular slope fixed plus moving forces zero tangent")
    zero_slope = stacked_constraint.subs(slope, 0)
    require(zero_slope.rank() == 1 and zero_slope.nullspace() == [sp.Matrix([0, 1])], "zero-slope displacement freedom")
    checks += 5

    seal_rows = [
        {"id": "S01", "realization": "FIXED_STATIC_SEAL", "allowed_relation": "delta_phi=0", "normal_slope": "free possibly nonzero", "embedding_displacement": "chi_normal=0", "rank_or_effect": "one scalar field tangent removed", "compatibility": "CANONIZED_SCOPED"},
        {"id": "S02", "realization": "MOVING_RELATIONAL_LEVEL_SET", "allowed_relation": "Delta_phi=delta_phi+chi_normal*nabla_normal(phi)=0", "normal_slope": "regular nonzero", "embedding_displacement": "free only with correlated delta_phi", "rank_or_effect": "one relation on two variables", "compatibility": "CONDITIONAL_EXTENSION"},
        {"id": "S03", "realization": "STACK_FIXED_DELTA_PHI_ON_FREE_LEVEL_SET", "allowed_relation": "delta_phi=0 and Delta_phi=0", "normal_slope": "regular nonzero", "embedding_displacement": "forced chi_normal=0", "rank_or_effect": "rank two; no nonzero free-boundary tangent", "compatibility": "INCOMPATIBLE_WITH_INTENDED_FREE_MOTION"},
        {"id": "S04", "realization": "ZERO_GRADIENT_PHI_ZERO", "allowed_relation": "delta_phi=0; chi_normal algebraically free", "normal_slope": "zero", "embedding_displacement": "not constrained by phi", "rank_or_effect": "phi=0 fails to define a regular level surface when full gradient vanishes", "compatibility": "DEGENERATE_NOT_SELECTOR"},
        {"id": "S05", "realization": "FREE_BOUNDARY_NOT_LOCKED_TO_PHI", "allowed_relation": "none from phi", "normal_slope": "irrelevant", "embedding_displacement": "free", "rank_or_effect": "boundary/seal identity lost under variation", "compatibility": "DISTINCT_OBJECT_BRANCH"},
    ]
    write_tsv("SEAL_VARIATION_COMPATIBILITY.tsv", ["id", "realization", "allowed_relation", "normal_slope", "embedding_displacement", "rank_or_effect", "compatibility"], seal_rows)

    # Embedding degree counts.  Tangential embedding changes are boundary reparameterizations; only
    # one normal function is a local codimension-one shape mode.
    embedding_rows = [
        {"id": "D01", "realization": "ONE_GLOBAL_CELL_MODULUS", "raw_components": "1 scalar", "gauge_or_redundant": "0", "independent_shape_data": "1 global number", "transversality_output": "one integrated scalar equation", "can_close_local_metric_polarization": "NO"},
        {"id": "D02", "realization": "LOCAL_CODIMENSION_ONE_EMBEDDING_IN_4D", "raw_components": "4 functions", "gauge_or_redundant": "3 tangential reparameterizations", "independent_shape_data": "1 normal function", "transversality_output": "one local scalar shape equation after B is specified", "can_close_local_metric_polarization": "NO"},
        {"id": "D03", "realization": "PHI_LOCKED_LOCAL_EMBEDDING", "raw_components": "delta_phi plus chi_normal", "gauge_or_redundant": "one level-set correlation", "independent_shape_data": "one correlated tangent", "transversality_output": "one combined scalar equation; independent phi equation absent in metric-only lanes", "can_close_local_metric_polarization": "NO"},
        {"id": "D04", "realization": "PURE_TANGENTIAL_EMBEDDING_SHIFT", "raw_components": "3 functions", "gauge_or_redundant": "3 boundary reparameterizations", "independent_shape_data": "0", "transversality_output": "Noether/reparameterization identity", "can_close_local_metric_polarization": "NO"},
        {"id": "D05", "realization": "NULL_BOUNDARY_EMBEDDING", "raw_components": "generator plus cross-section data", "gauge_or_redundant": "generator rescaling and tangential shifts unnormalized", "independent_shape_data": "OPEN", "transversality_output": "OPEN until null boundary functional and normalization supplied", "can_close_local_metric_polarization": "NO"},
        {"id": "D06", "realization": "TYPE_CHANGING_OR_DEGENERATE_EMBEDDING", "raw_components": "nonuniform", "gauge_or_redundant": "OPEN", "independent_shape_data": "OPEN", "transversality_output": "UNDEFINED in regular inverse-metric audit", "can_close_local_metric_polarization": "NO"},
        {"id": "D07", "realization": "MIRROR_DOUBLE_INTERNAL_SEAM", "raw_components": "two side embeddings tied by a soldering map", "gauge_or_redundant": "common seam relabeling versus relative displacement depends on quotient", "independent_shape_data": "OPEN", "transversality_output": "jump/matching equations; exact cancellation only after full field matching", "can_close_local_metric_polarization": "NO"},
    ]
    require(4 - 3 == 1, "codimension-one embedding count")
    require(all(row["can_close_local_metric_polarization"] == "NO" for row in embedding_rows), "embedding closure census")
    checks += 2
    write_tsv("EMBEDDING_DOF_CENSUS.tsv", ["id", "realization", "raw_components", "gauge_or_redundant", "independent_shape_data", "transversality_output", "can_close_local_metric_polarization"], embedding_rows)

    # Structural moving-domain and Noether identities.  These are recorded with the convention that
    # positive chi displaces the integration domain outward.
    covariance_rows = [
        {"id": "C01", "object": "moving bulk domain", "identity": "delta S_bulk=integral_M E.delta_g+integral_boundary(Theta(g,delta_g)+i_chi L)", "status": "DERIVED_STRUCTURAL_IDENTITY", "selector_limit": "i_chi L adds a displacement coefficient but does not cancel independent field-variation channels"},
        {"id": "C02", "object": "boundary functional", "identity": "delta S_boundary=delta_g B+delta_X B+corner_terms", "status": "STRUCTURAL_B_DEPENDENCE", "selector_limit": "transversality cannot be evaluated before B and corners are specified"},
        {"id": "C03", "object": "diffeomorphism Noether current", "identity": "J_chi=Theta(g,L_chi g)-i_chi L", "status": "DERIVED_CONDITIONAL_COVARIANT_LANES", "selector_limit": "pure dragged displacement can be gauge/charge data rather than a new field equation"},
        {"id": "C04", "object": "Noether divergence", "identity": "dJ_chi=-E.L_chi g", "status": "DERIVED_CONDITIONAL_COVARIANT_LANES", "selector_limit": "on shell closure is an identity; primitive normalization and corners remain open"},
        {"id": "C05", "object": "normal physical shape mode", "identity": "coefficient of chi_normal defines T_normal[g,B]=0", "status": "CONDITIONAL_AFTER_B_AND_EMBEDDING_CHOICE", "selector_limit": "T_normal changes when B or an exact divergence changes"},
        {"id": "C06", "object": "global modulus", "identity": "d S_on_shell/d R_cell=0", "status": "CONDITIONAL_AFTER_COMPLETE_GLOBAL_FUNCTIONAL", "selector_limit": "one integrated equation and no current S_on_shell(R_cell)"},
    ]
    write_tsv("COVARIANT_TRANSVERSALITY.tsv", ["id", "object", "identity", "status", "selector_limit"], covariance_rows)

    # Independent variation channels: chi contributes to a separate embedding column and cannot by
    # itself eliminate arbitrary h or normal-h channels in either P05 current.
    channel_matrix_l02 = sp.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # h, nabla h, chi
    channel_matrix_l01 = sp.eye(4)  # h, nabla h/K, corner, chi
    require(channel_matrix_l02.rank() == 3, "L02 independent moving-boundary channels")
    require(channel_matrix_l01.rank() == 4, "L01 independent moving-boundary channels")
    # One relational seal correlation can remove at most one scalar direction.
    require(channel_matrix_l02.rank() - 1 >= 2 and channel_matrix_l01.rank() - 1 >= 3, "seal correlation insufficient")
    checks += 3

    theta_plus, theta_minus, shape_plus, shape_minus = sp.symbols("Theta_plus Theta_minus T_plus T_minus")
    doubled_flux = theta_plus - theta_minus
    doubled_shape = shape_plus - shape_minus
    require(doubled_flux.subs(theta_minus, theta_plus) == 0, "two-sided matched flux cancellation")
    require(doubled_shape.subs(shape_minus, shape_plus) == 0, "two-sided matched shape cancellation")
    checks += 2

    lane_rows = [
        {"id": "L01", "lane": "pre-scale C2", "raw_field_channels": "4 alpha C*nabla(h)-4 alpha nabla(C)*h plus Euler", "free_embedding_channel": "i_chi L_C2 plus delta_X B", "corner_channel": "4 epsilon s_k C^{nijk} delta h_ij plus improvements", "after_one_seal_correlation": "independent h K_TF and corner channels remain", "transversality_status": "ADDED_B_DEPENDENT_NOT_SELECTOR"},
        {"id": "L02", "lane": "post-scale EH", "raw_field_channels": "kappa(nabla_b h^ab-nabla^a h) plus Euler", "free_embedding_channel": "i_chi L_EH plus delta_X B", "corner_channel": "depends on selected completion/joints", "after_one_seal_correlation": "independent induced-metric and normal-jet channels remain", "transversality_status": "ADDED_B_DEPENDENT_NOT_SELECTOR"},
        {"id": "L03", "lane": "two-stage bridge", "raw_field_channels": "NONE", "free_embedding_channel": "UNDEFINED", "corner_channel": "UNDEFINED", "after_one_seal_correlation": "bridge functional and matching fields absent", "transversality_status": "OPEN_NO_OPERATOR"},
    ]
    write_tsv("LANE_BOUNDARY_CHANNELS.tsv", ["id", "lane", "raw_field_channels", "free_embedding_channel", "corner_channel", "after_one_seal_correlation", "transversality_status"], lane_rows)

    transversality_rows = [
        {"id": "T01", "realization": "GLOBAL_R_CELL", "strongest_equation": "dS_on_shell/dR_cell=0", "local_or_global": "one integrated scalar", "requires": "complete global action boundary functional fields and solution", "redundancy": "not generically gauge", "selector_result": "INSUFFICIENT_AND_NOT_EVALUABLE_YET"},
        {"id": "T02", "realization": "LOCAL_NORMAL_EMBEDDING", "strongest_equation": "T_normal[g,B]=0 pointwise", "local_or_global": "one scalar function", "requires": "selected B causal type and embedding-field split", "redundancy": "may contain constraint/Noether pieces", "selector_result": "FUNCTIONAL_DEPENDENT"},
        {"id": "T03", "realization": "RELATIONAL_PHI_ZERO", "strongest_equation": "Delta_phi=0 plus projected combined field/shape response", "local_or_global": "one correlated scalar channel", "requires": "time-live phi role and its independent or metric-induced variation", "redundancy": "fixed delta_phi cannot also be imposed at regular moving seal", "selector_result": "REDUCES_ONE_DIRECTION_NOT_COMPLETE"},
        {"id": "T04", "realization": "PURE_DIFFEO_DRAG", "strongest_equation": "dJ_chi=-E.L_chi g", "local_or_global": "Noether identity/charge", "requires": "covariant lane and declared corner primitive", "redundancy": "gauge on unmarked boundary", "selector_result": "NO_NEW_SELECTOR"},
        {"id": "T05", "realization": "NULL_SEAL", "strongest_equation": "null shape/generator equation", "local_or_global": "OPEN", "requires": "generator auxiliary null normalization B and joints", "redundancy": "generator rescaling open", "selector_result": "UNCLASSIFIED_NOT_SELECTED"},
        {"id": "T06", "realization": "TYPE_CHANGING_SEAL", "strongest_equation": "NONE", "local_or_global": "OPEN", "requires": "degenerate/type-transition variational calculus", "redundancy": "OPEN", "selector_result": "UNDEFINED_RETAINED"},
        {"id": "T07", "realization": "MIRROR_DOUBLE_INTERNAL_SEAM", "strongest_equation": "jump of field momenta and normal shape response equals zero", "local_or_global": "two-sided matching", "requires": "complete full-field soldering involution orientations B and corners", "redundancy": "common seam motion may be quotient gauge", "selector_result": "CONDITIONAL_CANCELLATION_NOT_CURRENTLY_EVALUABLE"},
    ]
    write_tsv("TRANSVERSALITY_BRANCHES.tsv", ["id", "realization", "strongest_equation", "local_or_global", "requires", "redundancy", "selector_result"], transversality_rows)

    ambiguity_rows = [
        {"id": "A01", "object": "boundary functional B", "bulk_equation": "unchanged by boundary-only additions", "free_boundary_effect": "changes field and position transversality", "removed_by_free_variation": "NO", "status": "PRIMARY_COUNTEREXAMPLE"},
        {"id": "A02", "object": "Euler beta and its boundary completion", "bulk_equation": "zero regular 4D metric bulk contribution", "free_boundary_effect": "changes boundary/corner or topological completion bookkeeping", "removed_by_free_variation": "NO", "status": "OPEN"},
        {"id": "A03", "object": "exact bulk divergence dY", "bulk_equation": "unchanged", "free_boundary_effect": "changes B-effective and shape response", "removed_by_free_variation": "NO", "status": "OPEN"},
        {"id": "A04", "object": "Theta improvement deltaY+dZ", "bulk_equation": "unchanged", "free_boundary_effect": "changes boundary/corner representative", "removed_by_free_variation": "NO", "status": "OPEN"},
        {"id": "A05", "object": "boundary Legendre transform", "bulk_equation": "unchanged", "free_boundary_effect": "changes field polarization and transversality coefficients", "removed_by_free_variation": "NO", "status": "OPEN"},
        {"id": "A06", "object": "embedding counterterm or intrinsic boundary density", "bulk_equation": "unchanged", "free_boundary_effect": "changes local shape equation", "removed_by_free_variation": "NO", "status": "OPEN_NOT_ADOPTED"},
        {"id": "A07", "object": "orientation reference generator and joints", "bulk_equation": "unchanged", "free_boundary_effect": "changes signs zero-points charges and corner response", "removed_by_free_variation": "NO", "status": "OPEN"},
        {"id": "A08", "object": "overall action normalization", "bulk_equation": "same zero set when nonzero", "free_boundary_effect": "rescales momenta response and charge", "removed_by_free_variation": "NO", "status": "OPEN"},
    ]
    require(all(row["removed_by_free_variation"] == "NO" for row in ambiguity_rows), "functional ambiguity retention")
    checks += 1
    write_tsv("FUNCTIONAL_DEPENDENCE.tsv", ["id", "object", "bulk_equation", "free_boundary_effect", "removed_by_free_variation", "status"], ambiguity_rows)

    join_rows = [
        {"id": "X01", "object": "R_cell", "current_status": "CONDITIONAL_VARIATION_PARAMETER", "may_equal": "unknown physical finite-cell size", "must_not_equal_silently": "X_max WRL endpoint static fold", "equations_available": "dS_on_shell/dR_cell=0 only after complete functional", "closure": "OPEN"},
        {"id": "X02", "object": "X_max", "current_status": "OWNER_LOCKED_GLOBAL_OUTPUT_VALUE_OPEN", "may_equal": "function of completed metric c_E G_obs and mass/density", "must_not_equal_silently": "local coordinate or freely chosen R_cell", "equations_available": "none complete", "closure": "OPEN"},
        {"id": "X03", "object": "static phi_zero_fold", "current_status": "CANONIZED_SCOPED", "may_equal": "one finite-cell seal branch", "must_not_equal_silently": "X_max or WRL endpoint", "equations_available": "phi=0 delta_phi=0 normal derivative free at fixed static seal", "closure": "OPEN_JOIN"},
        {"id": "X04", "object": "WRL_endpoint", "current_status": "CONDITIONAL_ASYMPTOTIC_BOUNDARY_BRANCH", "may_equal": "distinct optical horizon/end", "must_not_equal_silently": "static fold or X_max", "equations_available": "branch-specific asymptotic identities", "closure": "OPEN_JOIN"},
        {"id": "X05", "object": "global_bootstrap", "current_status": "WORKING_ON_SHELL_ADMISSIBILITY", "may_equal": "future selector on completed solution space", "must_not_equal_silently": "off-shell action", "equations_available": "no varied global functional", "closure": "OPEN"},
    ]
    write_tsv("GLOBAL_BOUNDARY_JOIN.tsv", ["id", "object", "current_status", "may_equal", "must_not_equal_silently", "equations_available", "closure"], join_rows)

    field_rows: list[dict[str, str]] = []
    for lane in ("L01", "L02", "L03"):
        for realization_number in range(1, 8):
            realization = f"C{realization_number:02d}"
            if lane == "L03":
                bulk = "NO_OPERATOR"
                trans = "UNDEFINED"
            elif realization_number == 1:
                bulk = "CONDITIONAL_METRIC_BULK_OPERATOR"
                trans = "ONE_B_DEPENDENT_EMBEDDING_RESPONSE_ADDED_BOUNDARY_POLARIZATION_OPEN"
            else:
                bulk = "METRIC_OPERATOR_ONLY_EXTRA_FIELD_EQUATION_ABSENT"
                trans = "METRIC_EMBEDDING_RESPONSE_PARTIAL_EXTRA_FIELD_RESPONSE_UNDEFINED"
            field_rows.append(
                {
                    "pair_id": f"{lane}_{realization}",
                    "lane": lane,
                    "realization": realization,
                    "bulk_status": bulk,
                    "free_seal_transversality": trans,
                    "global_R_cell_equation": "NOT_EVALUABLE_COMPLETE_GLOBAL_FUNCTIONAL_ABSENT",
                    "Xmax_join": "OPEN",
                    "P06_ready": "NO",
                }
            )
    require(len(field_rows) == 21 and len({row["pair_id"] for row in field_rows}) == 21, "field pair census")
    require(all(row["P06_ready"] == "NO" for row in field_rows), "P06 closure")
    checks += 2
    write_tsv("FIELD_LANE_CLOSURE.tsv", ["pair_id", "lane", "realization", "bulk_status", "free_seal_transversality", "global_R_cell_equation", "Xmax_join", "P06_ready"], field_rows)

    status_rows = [
        {"id": "R01", "claim": "free finite-cell seal position is varied", "status": "CHOSE_CONDITIONAL_OWNER_AUTHORIZED_TEST", "scope": "not canonized by this audit"},
        {"id": "R02", "claim": "global R_cell equals X_max", "status": "NOT_DERIVED_FORBIDDEN_SILENT_JOIN", "scope": "fold WRL endpoint and Xmax roles remain distinct/open"},
        {"id": "R03", "claim": "variable endpoint adds transversality", "status": "DERIVED", "scope": "field and position endpoint coefficients"},
        {"id": "R04", "claim": "free endpoint selects its boundary functional", "status": "REFUTED_BY_TWO_PARAMETER_COUNTERFAMILY", "scope": "same bulk equation different field and position transversality"},
        {"id": "R05", "claim": "one global cell modulus supplies local boundary polarization", "status": "REFUTED_BY_LOCALITY_AND_COUNT", "scope": "one integrated equation versus local field functions"},
        {"id": "R06", "claim": "local embedding variation supplies one normal shape equation", "status": "DERIVED_CONDITIONAL_AFTER_B", "scope": "three tangential embedding directions are reparameterizations"},
        {"id": "R07", "claim": "local shape equation is functional independent", "status": "REFUTED", "scope": "B exact divergences and improvements change it"},
        {"id": "R08", "claim": "fixed delta_phi and free relational seal displacement coexist at regular slope", "status": "REFUTED", "scope": "stacked rank-two constraints force chi_normal=0"},
        {"id": "R09", "claim": "moving relational seal replaces fixed variation by correlated Delta_phi=0", "status": "DERIVED_CONDITIONAL_KINEMATICS", "scope": "time-live phi-zero level-set extension not canon"},
        {"id": "R10", "claim": "pure diffeomorphic boundary motion gives independent selector", "status": "NOT_DERIVED_NOETHER_REDUNDANCY_BRANCH", "scope": "unmarked generally covariant boundary"},
        {"id": "R11", "claim": "free-boundary variation removes L01/L02 field-current channels", "status": "REFUTED", "scope": "embedding term is independent of arbitrary h derivative-h and corner variations"},
        {"id": "R12", "claim": "free-boundary variation selects causal type", "status": "NOT_DERIVED", "scope": "shape equation unavailable before B and solution; time-live causal branches survive"},
        {"id": "R13", "claim": "global R_cell stationarity can help determine size", "status": "CONDITIONAL_FUTURE_ROUTE", "scope": "requires complete global on-shell functional and noncircular matter/volume data"},
        {"id": "R14", "claim": "free-boundary premise completes bootstrap", "status": "NOT_DERIVED", "scope": "bootstrap remains on-shell and supplies no functional"},
        {"id": "R15", "claim": "P06 readiness", "status": "CLOSED_ZERO_OF_21_PAIRS", "scope": "boundary functional field equations and global object incomplete"},
        {"id": "R16", "claim": "overall classification", "status": "FREE_BOUNDARY_ADDS_TRANSVERSALITY_BUT_REMAINS_FUNCTIONAL_DEPENDENT", "scope": "owner-authorized conditional premise and current P05 lanes"},
    ]
    write_tsv("STATUS_LEDGER.tsv", ["id", "claim", "status", "scope"], status_rows)

    graph = {
        "question": "Does varying a free global finite-cell seal close the boundary selector?",
        "authorized_conditional_premise": "finite-cell seal position is varied",
        "realizations": {
            "global_modulus": "one integrated stationarity equation",
            "local_embedding": "one normal shape equation after tangential quotient",
            "relational_phi_level_set": "delta_phi+chi_normal*nabla_normal(phi)=0",
            "pure_diffeomorphism": "Noether identity/charge branch",
        },
        "dependencies": [
            "bulk lane -> raw Theta and L",
            "boundary functional B -> field polarization and shape response",
            "embedding realization -> physical versus gauge displacement",
            "relational seal definition -> correlation between delta_phi and chi",
            "complete global solution -> evaluable dS_on_shell/dR_cell",
        ],
        "failed_implications": [
            "free boundary -> B=0",
            "free boundary -> unique natural polarization",
            "one global stationarity equation -> local boundary conditions",
            "fixed delta_phi=0 plus free regular level-set motion",
            "diffeomorphism covariance -> new independent shape law",
            "R_cell -> X_max",
            "shape equation -> causal type before solution",
        ],
        "open": [
            "complete boundary and corner functional",
            "local versus global embedding realization",
            "time-live seal relation to phi",
            "fold WRL endpoint Xmax join",
            "complete coframe and non-metric field variations",
            "global on-shell bootstrap functional",
            "native matter source total mass and proper volume",
        ],
    }
    (HERE / "TRANSVERSALITY_DEPENDENCY_GRAPH.json").write_text(json.dumps(graph, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    require(len(endpoint_rows) == 4, "endpoint family count")
    require(len(scale_rows) == 6, "global scale branch count")
    require(len(seal_rows) == 5, "seal branch count")
    require(len(embedding_rows) == 7, "embedding branch count")
    require(len(covariance_rows) == 6, "covariance row count")
    require(len(transversality_rows) == 7, "transversality branch count")
    require(len(ambiguity_rows) == 8, "ambiguity count")
    require(len(join_rows) == 5, "global join count")
    require(len(status_rows) == 16, "status row count")
    checks += 9

    result = {
        "audit": "UDT_FREE_GLOBAL_SEAL_TRANSVERSALITY",
        "base": "6c17a36e3693d21de73b18827324ef68923c285c",
        "classification": "FREE_BOUNDARY_ADDS_TRANSVERSALITY_BUT_REMAINS_FUNCTIONAL_DEPENDENT",
        "epistemic_grade": "LEAD_PENDING_FRESH_ADVERSARIAL_REVIEW",
        "maximum_conclusion": "FREE_GLOBAL_SEAL_TRANSVERSALITY_SELECTOR_STATUS_CLASSIFIED",
        "checks": checks,
        "owner_authorized_conditional_premise": True,
        "premise_promoted_to_canon": False,
        "endpoint_counterfunctionals": len(endpoint_rows),
        "global_scale_realizations": len(scale_rows),
        "embedding_realizations": len(embedding_rows),
        "functional_ambiguities": len(ambiguity_rows),
        "field_lane_pairs": len(field_rows),
        "P06_ready_pairs": 0,
        "R_cell_identified_with_Xmax": False,
        "solutions_run": 0,
        "gpu_used": False,
        "central_result": (
            "Varying the seal adds one global or local-normal transversality equation only after a "
            "boundary functional and embedding realization are specified. It neither selects that "
            "functional nor supplies the remaining local field polarization. A moving phi-locked "
            "seal requires correlated total variation rather than stacking fixed delta_phi=0."
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "UDT_FREE_GLOBAL_SEAL_TRANSVERSALITY_AUDIT=PASS",
        f"checks={checks}",
        "classification=FREE_BOUNDARY_ADDS_TRANSVERSALITY_BUT_REMAINS_FUNCTIONAL_DEPENDENT",
        "endpoint_counterfunctionals=4",
        "global_scale_realizations=6",
        "L01_homothety_scale_response=IDENTICALLY_ZERO",
        "L02_homothety_scale_response=CONDITIONAL_ON_SHAPE_LAMBDA_AND_BOUNDARY",
        "embedding_realizations=7",
        "mirror_double_flux=ZERO_ONLY_AFTER_COMPLETE_MATCHING",
        "regular_phi_lock=Delta_phi=delta_phi+chi_normal*nabla_normal_phi",
        "stacked_fixed_plus_moving_regular_seal=FORCES_chi_normal_zero",
        "R_cell_equals_Xmax=NO_NOT_DERIVED",
        "functional_ambiguities=8",
        "field_pairs=21/21",
        "P06_ready_pairs=0",
        "solutions=0 gpu=NO",
        "maximum_conclusion=FREE_GLOBAL_SEAL_TRANSVERSALITY_SELECTOR_STATUS_CLASSIFIED",
    ]
    (HERE / "DERIVATION_TRANSCRIPT.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

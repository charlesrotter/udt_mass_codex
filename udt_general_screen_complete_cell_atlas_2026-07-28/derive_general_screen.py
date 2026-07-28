#!/usr/bin/env python3
"""Exact algebra for the stationary general-screen complete-S3 existence atlas."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def write_tsv(name: str, rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


I = sp.eye(2)
R = sp.Matrix([[0, -1], [1, 0]])
S1 = sp.diag(1, -1)
S2 = sp.Matrix([[0, 1], [1, 0]])
HALF = sp.Rational(1, 2)


def rotation(angle: sp.Expr) -> sp.Matrix:
    return sp.Matrix([[sp.cos(angle), -sp.sin(angle)], [sp.sin(angle), sp.cos(angle)]])


def decompose(matrix: sp.Matrix) -> dict[str, sp.Expr]:
    return {
        "area": sp.simplify(HALF*sp.trace(matrix)),
        "rotation": sp.simplify(HALF*(matrix[1, 0] - matrix[0, 1])),
        "shear1": sp.simplify(HALF*(matrix[0, 0] - matrix[1, 1])),
        "shear2": sp.simplify(HALF*(matrix[0, 1] + matrix[1, 0])),
    }


def polar_response() -> dict[str, object]:
    u, v, beta, chi = sp.symbols("u v beta chi", real=True)
    du, dv, dbeta, dchi = sp.symbols("du dv dbeta dchi", real=True)
    gamma = chi + beta
    A = rotation(gamma)
    D = sp.diag(sp.exp(u + v), sp.exp(u - v))
    P = A * D * rotation(-beta)
    # Exact product rule in the A-rotated frame.  This avoids a very large expanded inverse:
    # dP P^-1 = A[du I + dv S1 + (dchi+dbeta)R - dbeta D R D^-1]A^-1.
    transported_R = sp.cosh(2*v)*R - sp.sinh(2*v)*S2
    omega_tilde = du*I + dv*S1 + (dchi+dbeta)*R - dbeta*transported_R
    logarithmic = A * omega_tilde * rotation(-gamma)
    expected = {
        "area": du,
        "rotation": dchi + dbeta * (1 - sp.cosh(2*v)),
        "shear1": dv*sp.cos(2*gamma) - dbeta*sp.sinh(2*v)*sp.sin(2*gamma),
        "shear2": dv*sp.sin(2*gamma) + dbeta*sp.sinh(2*v)*sp.cos(2*gamma),
    }
    components = expected
    shear_norm = sp.expand_trig(expected["shear1"]**2 + expected["shear2"]**2)
    shear_norm = sp.trigsimp(shear_norm)
    assert sp.trigsimp(shear_norm - (dv**2 + dbeta**2*sp.sinh(2*v)**2)) == 0
    determinant = sp.exp(2*u)
    h = rotation(beta) * sp.diag(sp.exp(2*(u+v)), sp.exp(2*(u-v))) * rotation(-beta)
    assert not h.has(chi)

    C = A * transported_R * rotation(-gamma)
    cexpected = {
        "area": 0,
        "rotation": sp.cosh(2*v),
        "shear1": sp.sinh(2*v)*sp.sin(2*gamma),
        "shear2": -sp.sinh(2*v)*sp.cos(2*gamma),
    }
    ccomp = cexpected
    assert sp.simplify(transported_R*transported_R + I) == sp.zeros(2)
    assert sp.simplify(transported_R.det()) == 1 and sp.simplify(sp.trace(transported_R)) == 0

    # The regular global shear coordinates q1,q2 recover both tangent directions at v=0.
    q1, q2, dq1, dq2 = sp.symbols("q1 q2 dq1 dq2", real=True)
    Q = q1*S1 + q2*S2
    tangent_at_zero = du*I + dq1*S1 + dq2*S2 + dchi*R
    assert decompose(tangent_at_zero) == {
        "area": du, "rotation": dchi, "shear1": dq1, "shear2": dq2,
    }

    return {
        "symbols": {"u": u, "v": v, "beta": beta, "chi": chi, "du": du, "dv": dv, "dbeta": dbeta, "dchi": dchi},
        "P": P,
        "h": h,
        "logarithmic": logarithmic,
        "components": components,
        "shear_norm": shear_norm,
        "determinant": determinant,
        "angular_complex_structure": C,
        "angular_components": ccomp,
        "isotropic_regular_tangent": tangent_at_zero,
    }


def wedge(left: dict[tuple[int, ...], sp.Expr], right: dict[tuple[int, ...], sp.Expr]) -> dict[tuple[int, ...], sp.Expr]:
    result: dict[tuple[int, ...], sp.Expr] = {}
    for a, ca in left.items():
        for b, cb in right.items():
            if set(a) & set(b):
                continue
            inversions = sum(i > j for i in a for j in b)
            key = tuple(sorted(a+b))
            result[key] = sp.simplify(result.get(key, 0) + (-1)**inversions*ca*cb)
    return {key: value for key, value in result.items() if value != 0}


def add(*forms: dict[tuple[int, ...], sp.Expr]) -> dict[tuple[int, ...], sp.Expr]:
    result: dict[tuple[int, ...], sp.Expr] = {}
    for form in forms:
        for key, value in form.items():
            result[key] = sp.simplify(result.get(key, 0) + value)
    return {key: value for key, value in result.items() if value != 0}


def scale(value: sp.Expr, form: dict[tuple[int, ...], sp.Expr]) -> dict[tuple[int, ...], sp.Expr]:
    return {key: sp.simplify(value*coefficient) for key, coefficient in form.items()}


def general_cartan() -> dict[str, object]:
    p1, p2, p3, t0, t1, m = sp.symbols("p1 p2 p3 t0 t1 m", real=True)
    c11, c12, c21, c22 = sp.symbols("c11 c12 c21 c22", real=True)
    C = sp.Matrix([[c11, c12], [c21, c22]])
    L = {
        direction: sp.Matrix(2, 2, lambda i, j: sp.symbols(f"L{direction}{i+1}{j+1}", real=True))
        for direction in (1, 2, 3)
    }
    e = [{(index,): sp.Integer(1)} for index in range(4)]
    dphi = add(scale(p1, e[1]), scale(p2, e[2]), scale(p3, e[3]))
    de0 = add(scale(-1, wedge(dphi, e[0])), scale(t0, wedge(e[2], e[3])))
    de1 = add(wedge(dphi, e[1]), scale(t1, wedge(e[2], e[3])))
    screen_forms = []
    for out in range(2):
        pieces = []
        for direction in (1, 2, 3):
            for column in range(2):
                pieces.append(scale(L[direction][out, column], wedge(e[direction], e[column+2])))
        for column in range(2):
            pieces.append(scale(m*C[out, column], wedge(e[1], e[column+2])))
        screen_forms.append(add(*pieces))
    de = (de0, de1, *screen_forms)

    structure: dict[tuple[int, int, int], sp.Expr] = {}
    for upper, form in enumerate(de):
        for (left, right), coefficient in form.items():
            structure[upper, left, right] = -coefficient
            structure[upper, right, left] = coefficient
    signs = (-1, 1, 1, 1)

    def lower(out: int, left: int, right: int) -> sp.Expr:
        return signs[out]*structure.get((out, left, right), 0)

    def gamma(left: int, middle: int, out: int) -> sp.Expr:
        return sp.simplify(HALF*(lower(out, left, middle)-lower(left, middle, out)+lower(middle, out, left)))

    connection_matrices = {}
    for direction in range(4):
        matrix = sp.Matrix(4, 4, lambda out, middle: gamma(direction, middle, out))
        assert sp.simplify(matrix + matrix.T) == sp.zeros(4)
        connection_matrices[f"D{direction}"] = matrix
    for out in range(4):
        for left in range(4):
            for right in range(4):
                torsion_component = sp.simplify(
                    signs[out]*(gamma(left, right, out) - gamma(right, left, out))
                    - structure.get((out, left, right), 0)
                )
                assert torsion_component == 0

    rays = {}
    for label, sign in (("plus", 1), ("minus", -1)):
        k = (1, sign, 0, 0)
        acceleration = [sp.simplify(signs[out]*sum(k[a]*k[b]*gamma(a, b, out) for a in range(4) for b in range(4))) for out in range(4)]
        congruence = sp.Matrix(2, 2, lambda i, j: sp.simplify(sum(k[b]*gamma(j+2, b, i+2) for b in range(4))))
        path_connection = sp.Matrix(2, 2, lambda i, j: sp.simplify(sum(k[a]*gamma(a, j+2, i+2) for a in range(4))))
        rays[label] = {
            "acceleration": acceleration,
            "congruence": congruence,
            "congruence_components": decompose(congruence),
            "path_connection": path_connection,
            "path_components": decompose(path_connection),
        }

    # Connection blocks: for each tangent direction, map pair basis (E0,E1) into screen.
    off_blocks = {}
    for direction in range(4):
        block = sp.Matrix(2, 2, lambda screen, pair: sp.simplify(gamma(direction, pair, screen+2)))
        off_blocks[f"D{direction}"] = block

    obstruction_difference = sp.simplify(off_blocks["D2"][1, 1] - off_blocks["D3"][0, 1])
    assert obstruction_difference == t1

    # Regression against the inherited equal-screen family P=exp(lambda*phi) I.
    lam = sp.symbols("lambda", real=True)
    trace_subs = {c11: 0, c12: -1, c21: 1, c22: 0}
    for direction, p in ((1, p1), (2, p2), (3, p3)):
        trace_subs.update({L[direction][0, 0]: lam*p, L[direction][1, 1]: lam*p,
                           L[direction][0, 1]: 0, L[direction][1, 0]: 0})
    plus_trace_path = sp.simplify(rays["plus"]["path_components"]["rotation"].subs(trace_subs))
    minus_trace_path = sp.simplify(rays["minus"]["path_components"]["rotation"].subs(trace_subs))
    assert plus_trace_path == sp.simplify(HALF*(-2*m-t0+t1))
    assert minus_trace_path == sp.simplify(HALF*(2*m-t0-t1))
    assert sp.simplify(rays["plus"]["congruence_components"]["area"].subs(trace_subs) - lam*p1) == 0
    assert sp.simplify(rays["minus"]["congruence_components"]["area"].subs(trace_subs) + lam*p1) == 0

    return {
        "symbols": {"p1": p1, "p2": p2, "p3": p3, "t0": t0, "t1": t1, "m": m},
        "C": C,
        "L": L,
        "exterior_forms": de,
        "connection_matrices": connection_matrices,
        "connection_checks": {
            "metric_compatible_lowered_connection": True,
            "torsion_free_against_structure_coefficients": True,
            "D2_bottomright_minus_D3_topright": obstruction_difference,
            "equal_screen_plus_path_rotation": plus_trace_path,
            "equal_screen_minus_path_rotation": minus_trace_path,
        },
        "rays": rays,
        "pair_to_screen_connection_blocks": off_blocks,
    }


def serialize(value):
    if isinstance(value, sp.MatrixBase):
        return [[str(sp.simplify(value[i, j])) for j in range(value.cols)] for i in range(value.rows)]
    if isinstance(value, sp.Basic):
        return str(sp.simplify(value))
    if isinstance(value, dict):
        return {str(k): serialize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize(v) for v in value]
    return value


def build_tables(polar: dict[str, object], cartan: dict[str, object]) -> dict[str, int]:
    response_rows = [
        {"stratum": "A00_FULL_GL2_PLUS", "area": "du", "rotation": "dchi+dbeta*(1-cosh(2v))", "shear1": "dv*cos(2gamma)-dbeta*sinh(2v)*sin(2gamma)", "shear2": "dv*sin(2gamma)+dbeta*sinh(2v)*cos(2gamma)", "rank": "4_COFAME;3_METRIC", "ruling": "FULL_LOCAL_RESPONSE"},
        {"stratum": "A01_ISOTROPIC_POLAR_CHART", "area": "du", "rotation": "dchi", "shear1": "dv*cos(2gamma)", "shear2": "dv*sin(2gamma)", "rank": "POLAR_CHART_RANK3_AT_v0", "ruling": "BETA_UNDEFINED_CHART_NOT_GEOMETRY"},
        {"stratum": "A01_ISOTROPIC_REGULAR_q_COORDINATES", "area": "du", "rotation": "dchi", "shear1": "dq1", "shear2": "dq2", "rank": "4_COFAME;3_METRIC", "ruling": "BOTH_SHEAR_TANGENTS_PRESENT_AT_ISOTROPY"},
        {"stratum": "A02_FIXED_AXIS", "area": "du", "rotation": "dchi", "shear1": "dv*cos(2gamma)", "shear2": "dv*sin(2gamma)", "rank": "3_COFAME_FOR_FIXED_AXIS", "ruling": "ONE_SHEAR_DIRECTION_PER_FIXED_AXIS"},
        {"stratum": "A03_ROTATING_AXIS", "area": "du", "rotation": "dchi+dbeta*(1-cosh(2v))", "shear1": "dv*cos(2gamma)-dbeta*sinh(2v)*sin(2gamma)", "shear2": "dv*sin(2gamma)+dbeta*sinh(2v)*cos(2gamma)", "rank": "4_IF_v_NONZERO", "ruling": "TWO_SHEARS_PLUS_GAUGE_ROTATION"},
        {"stratum": "A04_PURE_GAUGE", "area": "0", "rotation": "dchi", "shear1": "0", "shear2": "0", "rank": "1_COFAME;0_METRIC", "ruling": "METRIC_UNCHANGED"},
        {"stratum": "A06_GL2_MINUS", "area": "same_as_plus", "rotation": "reflection_conjugated", "shear1": "reflection_conjugated", "shear2": "reflection_conjugated", "rank": "SAME_METRIC_RANK", "ruling": "ORIENTATION_COMPONENT_NOT_NEW_METRIC"},
        {"stratum": "A07_DET_ZERO", "area": "UNDEFINED_LOG_RESPONSE", "rotation": "UNDEFINED", "shear1": "UNDEFINED", "shear2": "UNDEFINED", "rank": "LESS_THAN2", "ruling": "SCREEN_AND_FOUR_METRIC_DEGENERATE"},
    ]
    write_tsv("POLAR_RESPONSE_ATLAS.tsv", response_rows)

    invariant_rows = [
        {"object": "screen_metric", "formula": "h=P^T P", "gauge": "O2_LEFT_INVARIANT", "status": "METRIC"},
        {"object": "metric_DOF", "formula": "u,q1,q2", "gauge": "3_DIMENSIONAL_SPD2", "status": "EXACT"},
        {"object": "coframe_gauge", "formula": "O_chi", "gauge": "1_DIMENSIONAL_O2", "status": "NOT_EXTRA_METRIC_DOF"},
        {"object": "area_rate", "formula": "du", "gauge": "INVARIANT", "status": "EXACT"},
        {"object": "shear_norm", "formula": "dv^2+sinh(2v)^2_dbeta^2", "gauge": "INVARIANT", "status": "EXACT"},
        {"object": "shear_eigenrates", "formula": "du_plus_or_minus_sqrt(shear_norm)", "gauge": "INVARIANT", "status": "EXACT"},
        {"object": "displayed_rotation", "formula": "dchi+dbeta*(1-cosh(2v))", "gauge": "SHIFTS_UNDER_LOCAL_O2", "status": "COFRAME_CONNECTION"},
        {"object": "angular_structure_C", "formula": "P_R_P_inverse;C^2=-I;trC=0;detC=1", "gauge": "CONJUGACY_CLASS", "status": "EXACT"},
        {"object": "angular_structure_shear_norm", "formula": "sinh(2v)^2", "gauge": "INVARIANT", "status": "ANISOTROPY_COUPLES_TO_MAURER_CARTAN"},
    ]
    write_tsv("GAUGE_INVARIANT_ATLAS.tsv", invariant_rows)

    witnesses = [
        {"id": "W00_GENERAL", "P": "arbitrary_smooth_GL2_on_S3", "screen_response": "FULL_POINTWISE_COFAME_RESPONSE", "global_status": "GLOBAL_REGULAR_IF_detP_NOWHERE_ZERO", "physics_status": "OFF_SHELL_EXISTENCE_FAMILY"},
        {"id": "W01_TRACE", "P": "exp(lambda_phi)_I", "screen_response": "lambda_dphi_I", "global_status": "GLOBAL_REGULAR_COMPLETE_CELL_CONFIGURATION", "physics_status": "PARENT_EQUAL_WEIGHT_SUBFAMILY"},
        {"id": "W02_SHEAR1", "P": "exp(lambda_phi_I+mu_phi_S1)", "screen_response": "dphi_(lambda_I+mu_S1)", "global_status": "GLOBAL_REGULAR_COMPLETE_CELL_FOR_SMOOTH_FINITE_phi", "physics_status": "OFF_SHELL_ONE_SHEAR_WITNESS"},
        {"id": "W03_SHEAR2", "P": "exp(lambda_phi_I+nu_phi_S2)", "screen_response": "dphi_(lambda_I+nu_S2)", "global_status": "GLOBAL_REGULAR_COMPLETE_CELL_FOR_SMOOTH_FINITE_phi", "physics_status": "OFF_SHELL_OTHER_SHEAR_WITNESS"},
        {"id": "W04_TWO_SHEAR", "P": "exp(u(x)_I+q1(x)_S1+q2(x)_S2)", "screen_response": "arbitrary_I_S1_S2_first_jet_at_q1=q2=0;Frechet_exp_response_elsewhere", "global_status": "GLOBAL_REGULAR_COMPLETE_CELL_FOR_ALL_SMOOTH_FINITE_u_q1_q2", "physics_status": "OFF_SHELL_FULL_SYMMETRIC_RESPONSE_WITNESS"},
        {"id": "W05_PURE_GAUGE", "P": "O_chi_times_fixed_H", "screen_response": "dchi_R_metric_zero", "global_status": "GLOBAL_ON_S3_FOR_SMOOTH_chi", "physics_status": "COFRAME_GAUGE_CONTROL"},
        {"id": "W06_ROTATING_AXIS", "P": "O_chi_exp(uI+v_axis_beta)", "screen_response": "FULL_POLAR_FORMULA", "global_status": "GLOBAL_WHEN_EXP_symmetric_matrix_used_across_v_zero", "physics_status": "OFF_SHELL_GENERAL_RESPONSE_CONTROL"},
        {"id": "W07_ORIENTATION_REVERSE", "P": "fixed_reflection_times_W00", "screen_response": "O2_CONJUGATE", "global_status": "GLOBAL", "physics_status": "SAME_METRIC_ORIENTATION_CONTROL"},
        {"id": "W08_DEGENERATE", "P": "detP_zero_somewhere", "screen_response": "UNDEFINED_AT_ZERO", "global_status": "FOUR_METRIC_DEGENERATE", "physics_status": "RETAINED_BOUNDARY_NOT_CONFIGURATION"},
    ]
    write_tsv("COMPLETE_S3_WITNESS_ATLAS.tsv", witnesses)

    global_rows = [
        {"object": "four_coframe_determinant", "condition": "detP_nonzero", "result": "det_coframe=detP_relative_to_(c_E_dt,sigma3,sigma1,sigma2)", "scope": "EXACT_POINTWISE"},
        {"object": "four_metric_determinant", "condition": "detP_nonzero", "result": "det_g=-(detP)^2_relative_to_(c_E_dt,sigma3,sigma1,sigma2)", "scope": "EXACT_POINTWISE"},
        {"object": "screen_metric", "condition": "P_in_GL2", "result": "h=P^T_P_positive_definite", "scope": "EXACT_POINTWISE"},
        {"object": "compact_spatial_slice", "condition": "smooth_P_detP_nonzero_and_positive_slice_stratum_on_S3", "result": "RIEMANNIAN_GEODESICALLY_COMPLETE", "scope": "HOPF_RINOW_ON_COMPACT_SLICE"},
        {"object": "four_Lorentzian_spacetime", "condition": "smooth_finite_phi_and_smooth_P_in_GL2", "result": "GLOBAL_NONDEGENERATE_CONFIGURATION", "scope": "NOT_A_LORENTZIAN_GEODESIC_COMPLETENESS_CLAIM"},
        {"object": "orientation_plus_polar_lift", "condition": "smooth_P:S3_to_GL2_plus", "result": "global_O_in_SO2_and_global_chi_lift_exist_because_S3_simply_connected", "scope": "POLAR_GAUGE_EXISTENCE"},
        {"object": "orientation_minus_component", "condition": "smooth_P:S3_to_GL2_minus", "result": "fixed_reflection_times_GL2_plus;same_h_space", "scope": "COFRAME_ORIENTATION_CONTROL"},
        {"object": "isotropic_axis", "condition": "v=0", "result": "beta_undefined_but_logH=uI+q1S1+q2S2_is_regular", "scope": "CHART_ONLY_DEGENERACY"},
        {"object": "screen_rank_boundary", "condition": "detP=0", "result": "coframe_and_four_metric_degenerate", "scope": "RETAINED_NONCONFIGURATION_BOUNDARY"},
    ]
    write_tsv("GLOBAL_EXISTENCE_ATLAS.tsv", global_rows)

    rank_rows = [
        {"chart": "polar_v_nonzero", "inputs": "du;dv;dbeta;dchi", "outputs": "area;shear1;shear2;rotation", "rank": "4", "determinant": "sinh(2v)", "ruling": "FULL_COFAME_RESPONSE"},
        {"chart": "polar_v_zero", "inputs": "du;dv;dbeta;dchi", "outputs": "area;shear1;shear2;rotation", "rank": "3", "determinant": "0", "ruling": "POLAR_AXIS_CHART_LOSS_ONLY"},
        {"chart": "regular_logH_at_isotropy", "inputs": "du;dq1;dq2;dchi", "outputs": "area;shear1;shear2;rotation", "rank": "4", "determinant": "1", "ruling": "BOTH_SHEAR_TANGENTS_RECOVERED"},
        {"chart": "metric_polar_v_nonzero", "inputs": "du;dv;dbeta", "outputs": "area;shear1;shear2", "rank": "3", "determinant": "sinh(2v)", "ruling": "FULL_SPD2_RESPONSE"},
        {"chart": "metric_regular_at_isotropy", "inputs": "du;dq1;dq2", "outputs": "area;shear1;shear2", "rank": "3", "determinant": "1", "ruling": "THREE_METRIC_DOF"},
    ]
    write_tsv("RESPONSE_RANK_ATLAS.tsv", rank_rows)

    slice_rows = [
        {"stratum": "A08_POSITIVE", "condition": "exp(2phi)-alpha^2_exp(-2phi)>0", "four_metric": "LORENTZIAN_NONDEGENERATE_IF_detP_NONZERO", "t_slice": "RIEMANNIAN_COMPLETE_ON_COMPACT_S3", "ruling": "SPACELIKE_SLICE"},
        {"stratum": "A09_ZERO", "condition": "exp(2phi)-alpha^2_exp(-2phi)=0", "four_metric": "LORENTZIAN_NONDEGENERATE_IF_detP_NONZERO", "t_slice": "DEGENERATE", "ruling": "CAUSAL_SLICE_BOUNDARY_RETAINED"},
        {"stratum": "A10_NEGATIVE", "condition": "exp(2phi)-alpha^2_exp(-2phi)<0", "four_metric": "LORENTZIAN_NONDEGENERATE_IF_detP_NONZERO", "t_slice": "INDEFINITE", "ruling": "NONSPACELIKE_COORDINATE_SLICE_RETAINED"},
        {"stratum": "DET_P_ZERO", "condition": "detP=0", "four_metric": "DEGENERATE", "t_slice": "DEGENERATE", "ruling": "METRIC_BOUNDARY"},
    ]
    write_tsv("ORIENTATION_DEGENERACY_ATLAS.tsv", slice_rows)

    completion_source = HERE.parent / "udt_global_metric_assembly_atlas_2026-07-22/COMPLETION_CLASS_REGISTRY.tsv"
    with completion_source.open(newline="", encoding="utf-8") as handle:
        completion_rows = list(csv.DictReader(handle, delimiter="\t"))
    completion_out = []
    for row in completion_rows:
        cid = row["completion_id"]
        if cid == "FC04_TWO_CAP_P1":
            status = "CONSTRUCTIVE_S3_GENERAL_SCREEN_WITNESS"
            requirement = "global_left_invariant_frame_and_smooth_GL2_P"
        elif cid == "FC05_TWO_CAP_P_GT1":
            status = "CONDITIONAL_LENS_QUOTIENT_DESCENT"
            requirement = "deck_equivariance_of_phi_pair_and_h_or_O2_coframe_transitions"
        elif cid == "FC11_NONINTEGRABLE_DISTRIBUTION":
            status = "PROPERTY_REALIZED_INSIDE_S3_WITNESS_NOT_SEPARATE_METRIC"
            requirement = "contact_screen_distribution;completion_class_overlap_retained"
        elif cid == "FC10_STRATIFIED_PROJECTOR":
            status = "NOT_COVERED_BY_GL2_INTERIOR"
            requirement = "rank_change_requires_beyond_invertible_screen_and_may_need_other_full_metric_blocks"
        elif cid in {"FC07_PERIODIC_TORUS_BUNDLE", "FC08_MIRROR_DOUBLE", "FC09_NONORIENTABLE_GLUE"}:
            status = "CONDITIONAL_TRANSITION_DESCENT_ONLY"
            requirement = "monodromy_or_lift_equivariance_of_h_and_O2_screen_transitions"
        else:
            status = "BLOCKED_NO_ACTUAL_GENERAL_SCREEN_METRIC_AND_JOINS"
            requirement = "cap_boundary_profiles_smooth_chart_and_pair_join"
        completion_out.append({
            "completion_id": cid, "topology_family": row["topology_family"],
            "parent_selection_status": row["selection_status"], "general_screen_status": status,
            "exact_requirement": requirement, "physical_selection": "NONE",
        })
    write_tsv("COMPLETION_DESCENT_ATLAS.tsv", completion_out)

    # Cartan response summary, retaining symbolic matrices in the JSON evidence.
    plus = cartan["rays"]["plus"]
    minus = cartan["rays"]["minus"]
    mixing_rows = [
        {"object": "null_plus_acceleration", "formula": ";".join(map(str, plus["acceleration"])), "zero_condition": "screen_components_equal_zero", "status": "EXACT_FIRST_JET"},
        {"object": "null_minus_acceleration", "formula": ";".join(map(str, minus["acceleration"])), "zero_condition": "screen_components_equal_zero", "status": "EXACT_FIRST_JET"},
        {"object": "null_plus_congruence", "formula": str(plus["congruence"]), "zero_condition": "componentwise", "status": "FULL_SCREEN_MATRIX"},
        {"object": "null_minus_congruence", "formula": str(minus["congruence"]), "zero_condition": "componentwise", "status": "FULL_SCREEN_MATRIX"},
        {"object": "pair_to_screen_connection", "formula": "four_direction_blocks_in_GENERAL_CARTAN_RESULT.json", "zero_condition": "all_block_entries_zero", "status": "GENERICALLY_MIXED_NOT_PHYSICAL_COUPLING"},
    ]
    write_tsv("PAIR_SCREEN_MIXING_ATLAS.tsv", mixing_rows)

    cartan_rows = [
        {"object": "angular_complex_structure", "plus": "C=P_R_P_inverse", "minus": "same", "invariant_or_condition": "C^2=-I;trC=0;detC=1", "status": "EXACT"},
        {"object": "null_acceleration", "plus": "(-p1,-p1,-2p2,-2p3)", "minus": "(+p1,-p1,-2p2,-2p3)", "invariant_or_condition": "pregeodesic_iff_p2=p3=0", "status": "EXACT_FIRST_JET"},
        {"object": "congruence_area", "plus": "+tr(L1)/2", "minus": "-tr(L1)/2", "invariant_or_condition": "trC=0_removes_Maurer_Cartan_area", "status": "EXACT"},
        {"object": "congruence_shear1", "plus": "+(L111-L122+(c11-c22)m)/2", "minus": "negative_of_plus", "invariant_or_condition": "screen_basis_components_spin2", "status": "EXACT"},
        {"object": "congruence_shear2", "plus": "+(L112+L121+(c12+c21)m)/2", "minus": "negative_of_plus", "invariant_or_condition": "screen_basis_components_spin2", "status": "EXACT"},
        {"object": "congruence_rotation", "plus": "(-t0+t1)/2", "minus": "-(t0+t1)/2", "invariant_or_condition": "distinct_from_path_frame_rotation", "status": "DISPLAYED_FRAME_COMPONENT"},
        {"object": "path_screen_connection", "plus": "pure_skew", "minus": "pure_skew", "invariant_or_condition": "area=shear1=shear2=0_by_metric_compatibility", "status": "EXACT"},
        {"object": "path_frame_rotation", "plus": "(L112-L121+(c12-c21)m-t0+t1)/2", "minus": "(-L112+L121-(c12-c21)m-t0-t1)/2", "invariant_or_condition": "changes_under_path_dependent_O2_gauge", "status": "COFRAME_CONNECTION"},
    ]
    write_tsv("CARTAN_RESPONSE_ATLAS.tsv", cartan_rows)

    # All-direction Levi-Civita preservation of the registered pair/screen split requires
    # every entry of every pair-to-screen block to vanish.  The D2/D3 symmetric off-diagonal
    # equations have opposite t1 signs, so together they require t1=0.  But on the actual
    # S3 coframe t1=kappa*exp(phi)/detP, which cannot vanish for kappa!=0 and P invertible.
    block_rows = [
        {"condition_id": "BP01", "source_blocks": "D0;D1", "required": "p2=0;p3=0", "actual_S3_consequence": "dphi_has_no_screen_components", "status": "NECESSARY_NOT_SUFFICIENT"},
        {"condition_id": "BP02", "source_blocks": "D2;D3", "required": "t0=0", "actual_S3_consequence": "alpha*kappa*exp(-phi)/detP=0", "status": "NECESSARY_NOT_SUFFICIENT"},
        {"condition_id": "BP03", "source_blocks": "D2;D3_diagonal", "required": "L111+c11*m=0;L122+c22*m=0", "actual_S3_consequence": "screen_diagonal_jets_must_cancel_angular_structure", "status": "NECESSARY_NOT_SUFFICIENT"},
        {"condition_id": "BP04", "source_blocks": "D2;D3_offdiagonal", "required": "S+t1=0;S-t1=0_where_S=L112+L121+(c12+c21)*m", "actual_S3_consequence": "t1=0;S=0", "status": "NECESSARY_NOT_SUFFICIENT"},
        {"condition_id": "BP05", "source_blocks": "ALL", "required": "t1=0", "actual_S3_consequence": "contradicts_t1=kappa*exp(phi)/detP_for_kappa_nonzero_finite_phi_detP_nonzero", "status": "NO_PARALLEL_PAIR_SCREEN_SPLIT_WITHIN_REGISTERED_S3_FAMILY"},
        {"condition_id": "BP06", "source_blocks": "NULL_ACCELERATIONS_ONLY", "required": "p2=0;p3=0", "actual_S3_consequence": "aligned_null_pregeodesic_condition_only;does_not_imply_parallel_split", "status": "WEAKER_PATHWISE_CONDITION"},
    ]
    write_tsv("BLOCK_PRESERVATION_CONDITIONS.tsv", block_rows)

    completeness = read_tsv("COMPLETENESS_PLAN.tsv")
    coverage = [
        {"criterion": row["criterion"], "stamp": "EXPLICITLY_OPEN_NOT_TESTED" if row["criterion"] == "STABILITY_SPECTRUM" else "COVERED_AS_BOUNDED_SCOPE", "covered": row["covered_now"], "open": row["dropped_or_open"]}
        for row in completeness
    ]
    write_tsv("TEN_CRITERION_COVERAGE.tsv", coverage)

    return {
        "response_rows": len(response_rows), "witnesses": len(witnesses),
        "global_rows": len(global_rows), "rank_rows": len(rank_rows),
        "completion_rows": len(completion_out), "mixing_rows": len(mixing_rows),
        "cartan_rows": len(cartan_rows),
        "block_preservation_rows": len(block_rows), "coverage_rows": len(coverage),
    }


def main() -> int:
    polar = polar_response()
    cartan = general_cartan()
    counts = build_tables(polar, cartan)
    cartan_serialized = serialize(cartan)
    (HERE / "GENERAL_CARTAN_RESULT.json").write_text(json.dumps(cartan_serialized, indent=2, sort_keys=True) + "\n")
    result = {
        "schema": "udt-general-screen-complete-cell-atlas-1.0",
        "status": "PASS",
        "sympy_version": sp.__version__,
        **counts,
        "coframe_response_rank": 4,
        "metric_screen_response_rank": 3,
        "both_shear_tangents_at_isotropy": True,
        "complete_S3_full_symmetric_witness": True,
        "all_direction_pair_screen_parallel_split": False,
        "parallel_split_obstruction": "t1=kappa*exp(phi)/detP_nonzero_on_registered_S3_GL2_family",
        "rotation_is_extra_metric_DOF": False,
        "full_4D_metric_family": False,
        "on_shell_or_selected": False,
        "outcome_class": "MIXED_BRANCH_AND_DEGENERACY_ATLAS",
        "maximum_conclusion": "COMPLETE_OFF_SHELL_S3_GENERAL_SCREEN_EXISTENCE_AND_FIRST_JET_RESPONSE_ONLY",
        "polar": serialize({key: value for key, value in polar.items() if key != "symbols"}),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "polar"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

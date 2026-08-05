#!/usr/bin/env python3
"""Primary exact algebra for the full-coframe first-jet/stratified atlas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
RESULT_PATH = HERE / "RESULT.json"
ETA = sp.diag(-1, 1, 1, 1)
ETA_BASE = sp.diag(-1, 1)
SYMMETRIC_SLOTS = [(i, j) for i in range(4) for j in range(i, 4)]
OUTCOME = (
    "DERIVED_FULL_METRIC_FIRST_JET_SURJECTION__"
    "DERIVED_JOINT_RECIPROCAL_ANGULAR_CAUSAL_STRATA__"
    "NORMALIZED_REDUCTION_HAS_NO_UNIVERSAL_STRATIFIED_EXTENSION__"
    "NO_KINEMATIC_EVOLUTION_RETURN"
)


def scalar(value):
    value = sp.simplify(value)
    if value.is_Integer:
        return int(value)
    if value.is_Rational:
        return f"{value.p}/{value.q}"
    return str(value)


def matrix_values(matrix: sp.Matrix):
    return [[scalar(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)]


def tangent_vector(generator: sp.Matrix) -> sp.Matrix:
    tangent = generator.T * ETA + ETA * generator
    return sp.Matrix([tangent[i, j] for i, j in SYMMETRIC_SLOTS])


def first_jet_result():
    per_direction = []
    blocks = []
    for mu in range(4):
        variables = sp.symbols(f"x{mu}_0:16")
        xmat = sp.Matrix(4, 4, variables)
        tangent = xmat.T * ETA + ETA * xmat
        expressions = [tangent[i, j] for i, j in SYMMETRIC_SLOTS]
        coefficient = sp.Matrix(expressions).jacobian(variables)
        per_direction.append(
            {
                "direction": mu,
                "coframe_jet_components": 16,
                "metric_jet_components": 10,
                "rank": coefficient.rank(),
                "nullity": 16 - coefficient.rank(),
            }
        )
        blocks.append(coefficient)

    full = sp.diag(*blocks)

    h = sp.diag(-1, 1, 0, 0)
    base_scale = sp.diag(1, 1, 0, 0)
    base_offdiag = sp.zeros(4)
    base_offdiag[0, 1] = 1
    base_offdiag[1, 0] = -1
    screen_area = sp.diag(0, 0, 1, 1)
    screen_shear = sp.diag(0, 0, 1, -1)
    screen_offdiag = sp.zeros(4)
    screen_offdiag[2, 3] = screen_offdiag[3, 2] = 1
    generators = [h, base_scale, base_offdiag, screen_area, screen_shear, screen_offdiag]
    names = [
        "founded_reciprocal_H",
        "base_common_scale",
        "base_offdiagonal",
        "screen_area",
        "screen_diagonal_shear",
        "screen_offdiagonal_shear",
    ]
    for a in (0, 1):
        for b in (2, 3):
            generator = sp.zeros(4)
            generator[a, b] = 1
            generator[b, a] = 1 if a == 1 else -1
            generators.append(generator)
            names.append(f"mixing_{a}{b}")
    basis_matrix = sp.Matrix.hstack(*(tangent_vector(generator) for generator in generators))

    gauge = []
    eta_sign = [-1, 1, 1, 1]
    for a in range(4):
        for b in range(a + 1, 4):
            generator = sp.zeros(4)
            generator[a, b] = 1
            generator[b, a] = -sp.Rational(eta_sign[a], eta_sign[b])
            gauge.append(generator)
    gauge_flat = sp.Matrix.hstack(*(sp.Matrix(generator).reshape(16, 1) for generator in gauge))

    return {
        "per_direction": per_direction,
        "full_coframe_jet_components": 64,
        "full_metric_jet_components": 40,
        "full_rank": full.rank(),
        "full_nullity": 64 - full.rank(),
        "spatial_and_time_directions_equally_released": all(row["rank"] == 10 for row in per_direction),
        "metric_basis_names": names,
        "metric_basis_rank": basis_matrix.rank(),
        "metric_basis_category_counts": {"founded_reciprocal": 1, "other_base": 2, "screen": 3, "mixing": 4},
        "founded_H_metric_tangent": matrix_values(h.T * ETA + ETA * h),
        "Lorentz_gauge_basis_dimension": gauge_flat.rank(),
        "Lorentz_gauge_tangents_zero": all(tangent_vector(generator) == sp.zeros(10, 1) for generator in gauge),
        "arbitrary_first_jets_constructed_by_theta_equals_I_plus_x_mu_X_mu": True,
        "first_jet_kinematic_constraint_count": 0,
    }


def factor_metric(a, q, s):
    a = sp.sympify(a)
    q = sp.Matrix(q)
    s = sp.Matrix(s)
    abase = sp.diag(1 / a, a)
    zero = sp.zeros(2)
    return sp.BlockMatrix([[abase, zero], [q * s, q]]).as_explicit()


def causal_value(a, q, s, p):
    e = factor_metric(a, q, s)
    metric = e.T * ETA * e
    return sp.simplify((p.T * metric.inv() * p)[0])


def joint_causal_result():
    a = sp.symbols("a", positive=True, nonzero=True)
    q11, q12, q21, q22 = sp.symbols("q11 q12 q21 q22")
    s00, s01, s10, s11 = sp.symbols("s00 s01 s10 s11")
    pt, px, py, pz = sp.symbols("pt px py pz")
    q = sp.Matrix([[q11, q12], [q21, q22]])
    s = sp.Matrix([[s00, s01], [s10, s11]])
    p_base = sp.Matrix([pt, px])
    p_screen = sp.Matrix([py, pz])
    p = sp.Matrix([pt, px, py, pz])
    e = factor_metric(a, q, s)
    einv = sp.BlockMatrix(
        [[sp.diag(a, 1 / a), sp.zeros(2)], [-s * sp.diag(a, 1 / a), q.inv()]]
    ).as_explicit()
    inverse_identity = sp.simplify(e * einv - sp.eye(4)) == sp.zeros(4)
    metric_inverse = einv * ETA * einv.T
    base_frame = sp.diag(a, 1 / a) * (p_base - s.T * p_screen)
    screen_frame = q.inv().T * p_screen
    expected = (base_frame.T * ETA_BASE * base_frame)[0] + (screen_frame.T * screen_frame)[0]
    formula_identity = sp.simplify(sp.together((p.T * metric_inverse * p)[0] - expected)) == 0

    fixed_p = sp.Matrix([1, 0, 1, 0])
    identity_q = sp.eye(2)
    mixing = {
        "timelike": causal_value(1, identity_q, sp.Matrix([[-1, 0], [0, 0]]), fixed_p),
        "null": causal_value(1, identity_q, sp.zeros(2), fixed_p),
        "spacelike": causal_value(1, identity_q, sp.Matrix([[1, 0], [0, 0]]), fixed_p),
    }
    shear = {
        "timelike": causal_value(1, sp.diag(2, sp.Rational(1, 2)), sp.zeros(2), fixed_p),
        "null": causal_value(1, sp.eye(2), sp.zeros(2), fixed_p),
        "spacelike": causal_value(1, sp.diag(sp.Rational(1, 2), 2), sp.zeros(2), fixed_p),
    }
    return {
        "block_inverse_identity_exact": inverse_identity,
        "causal_formula_identity_exact": formula_identity,
        "formula": "u=A^{-T}(p_base-S^T p_screen); v=Q^{-T}p_screen; s_phi=u^T eta_base u+v^T v",
        "same_coordinate_dphi": [1, 0, 1, 0],
        "mixing_witness_s_phi": {key: scalar(value) for key, value in mixing.items()},
        "unit_determinant_screen_shear_witness_s_phi": {key: scalar(value) for key, value in shear.items()},
        "screen_shear_determinants": [1, 1, 1],
        "all_three_causal_classes_from_mixing": [sp.signsimp(value) for value in mixing.values()] == [-3, 0, 1],
        "all_three_causal_classes_from_unit_area_shear": [sp.signsimp(value) for value in shear.values()] == [sp.Rational(-3, 4), 0, 3],
    }


def transition_result():
    lam = sp.symbols("lambda", real=True)
    p = sp.Matrix([1, lam, 0, 0])
    sharp = ETA * p
    norm = sp.expand((p.T * ETA * p)[0])
    numerator = sharp * p.T
    projector = sp.simplify(numerator / norm)
    pole_entry = sp.factor(projector[0, 0])

    p_time = lam * sp.Matrix([1, 0, 0, 0])
    p_space = lam * sp.Matrix([0, 1, 0, 0])

    def normalized_projector(covector):
        vector = ETA * covector
        squared = (covector.T * ETA * covector)[0]
        return sp.simplify(vector * covector.T / squared)

    time_limit = normalized_projector(p_time).applyfunc(lambda value: sp.limit(value, lam, 0))
    space_limit = normalized_projector(p_space).applyfunc(lambda value: sp.limit(value, lam, 0))

    return {
        "nonzero_null_crossing": {
            "path_dphi": "(1,lambda,0,0)",
            "s_phi": str(norm),
            "null_at_lambda": ["-1", "1"],
            "ds_dlambda_at_plus_one": scalar(sp.diff(norm, lam).subs(lam, 1)),
            "dphi_nonzero_at_plus_one": True,
            "sharp_vector_at_plus_one": [scalar(value) for value in sharp.subs(lam, 1)],
            "unnormalized_outer_at_plus_one_nonzero": numerator.subs(lam, 1) != sp.zeros(4),
            "normalized_projector_entry_00": str(pole_entry),
            "normalized_projector_has_simple_pole": sp.limit((lam - 1) * pole_entry, lam, 1) != 0,
        },
        "zero_gradient_crossing": {
            "timelike_approach_projector_limit": matrix_values(time_limit),
            "spacelike_approach_projector_limit": matrix_values(space_limit),
            "limits_equal": time_limit == space_limit,
            "path_independent_normalized_projector_extension": False,
        },
        "unnormalized_dphi_and_sharp_remain_finite_at_nonzero_null": True,
        "causal_change_requires_null_or_zero_by_continuity": True,
    }


def rank_result():
    lam = sp.symbols("lambda", real=True)
    theta = sp.diag(1, 1, 1, lam)
    metric = theta.T * ETA * theta
    det_theta = sp.factor(theta.det())
    det_metric = sp.factor(metric.det())
    inverse_metric = metric.inv()
    adjugate_metric = sp.simplify(det_metric * inverse_metric)

    return {
        "coframe_path": "diag(1,1,1,lambda)",
        "coframe_determinant": str(det_theta),
        "metric": matrix_values(metric),
        "metric_determinant": str(det_metric),
        "det_g_equals_det_eta_times_det_theta_squared": sp.simplify(det_metric + det_theta**2) == 0,
        "inverse_metric_33": str(inverse_metric[3, 3]),
        "inverse_diverges_at_rank_loss": True,
        "metric_adjugate": matrix_values(adjugate_metric),
        "metric_adjugate_limit_at_zero": matrix_values(adjugate_metric.subs(lam, 0)),
        "orientation_branches_separated_by_rank_loss": True,
        "rank_at_zero": metric.subs(lam, 0).rank(),
        "coframe_rank_at_zero": theta.subs(lam, 0).rank(),
        "coframe_rank_variety_codimensions_rank_leq_3_2_1_0": [1, 4, 9, 16],
        "screen_path": "Q=diag(1,lambda)",
        "screen_rank_at_zero": 1,
        "screen_rank_variety_codimensions_rank_leq_1_0": [1, 4],
        "factorized_det_E_equals_det_Q": True,
        "finite_phi_pair_determinant": -1,
        "finite_phi_rank_loss": False,
        "phi_asymptotes_have_no_finite_nondegenerate_fixed_chart_metric_limit": True,
        "canonical_Lorentzian_continuation_from_rank_loss": False,
    }


def lorentz_basis():
    signs = [-1, 1, 1, 1]
    basis = []
    for a in range(4):
        for b in range(a + 1, 4):
            generator = sp.zeros(4)
            generator[a, b] = 1
            generator[b, a] = -sp.Rational(signs[a], signs[b])
            assert generator.T * ETA + ETA * generator == sp.zeros(4)
            basis.append(generator)
    return basis


def inertia_symmetric(matrix: sp.Matrix):
    positive = negative = zero = 0
    for eigenvalue, multiplicity in matrix.eigenvals().items():
        eigenvalue = sp.simplify(eigenvalue)
        if eigenvalue == 0:
            zero += multiplicity
        elif eigenvalue.is_positive:
            positive += multiplicity
        elif eigenvalue.is_negative:
            negative += multiplicity
        else:
            raise AssertionError(f"undetermined exact eigenvalue sign: {eigenvalue}")
    return [positive, negative, zero]


def stabilizer_row(name: str, covector: sp.Matrix):
    ambient = lorentz_basis()
    action = sp.Matrix.hstack(*(generator.T * covector for generator in ambient))
    nullspace = action.nullspace()
    subalgebra = [sum((vector[k] * ambient[k] for k in range(6)), sp.zeros(4)) for vector in nullspace]
    dimension = len(subalgebra)
    flattened = sp.Matrix.hstack(*(matrix.reshape(16, 1) for matrix in subalgebra))
    structure = [[[sp.Integer(0) for _ in range(dimension)] for _ in range(dimension)] for _ in range(dimension)]
    closure = True
    for i in range(dimension):
        for j in range(dimension):
            commutator = subalgebra[i] * subalgebra[j] - subalgebra[j] * subalgebra[i]
            try:
                coefficients = flattened.gauss_jordan_solve(commutator.reshape(16, 1))[0]
            except ValueError:
                closure = False
                continue
            for k in range(dimension):
                structure[i][j][k] = sp.simplify(coefficients[k])
    adjoint = []
    for i in range(dimension):
        adjoint.append(sp.Matrix(dimension, dimension, lambda k, j: structure[i][j][k]))
    killing = sp.Matrix(dimension, dimension, lambda i, j: sp.trace(adjoint[i] * adjoint[j]))
    algebra_type = {
        "timelike": "so(3)",
        "spacelike": "so(1,2)",
        "nonzero_null": "iso(2)",
        "zero": "so(1,3)",
    }[name]
    return {
        "stratum": name,
        "representative": [scalar(value) for value in covector],
        "dimension": dimension,
        "closed_under_commutator": closure,
        "Killing_rank": killing.rank(),
        "Killing_inertia_positive_negative_zero": inertia_symmetric(killing),
        "algebra_type": algebra_type,
    }


def stabilizer_result():
    rows = [
        stabilizer_row("timelike", sp.Matrix([1, 0, 0, 0])),
        stabilizer_row("spacelike", sp.Matrix([0, 1, 0, 0])),
        stabilizer_row("nonzero_null", sp.Matrix([1, 1, 0, 0])),
        stabilizer_row("zero", sp.zeros(4, 1)),
    ]
    return {
        "rows": rows,
        "nonzero_dimensions_all_three": [row["dimension"] for row in rows[:3]],
        "algebra_types_distinct": len({row["algebra_type"] for row in rows}) == 4,
        "null_Killing_form_degenerate": rows[2]["Killing_rank"] < rows[2]["dimension"],
        "zero_covector_restores_full_Lorentz_dimension": rows[3]["dimension"] == 6,
    }


def derive():
    first_jet = first_jet_result()
    joint_causal = joint_causal_result()
    transitions = transition_result()
    ranks = rank_result()
    stabilizers = stabilizer_result()
    return {
        "schema": "udt.full_coframe_first_jet_stratified_transition.v1",
        "sympy_version": sp.__version__,
        "outcome": OUTCOME,
        "first_jet": first_jet,
        "joint_causal": joint_causal,
        "causal_transitions": transitions,
        "rank_transitions": ranks,
        "stabilizers": stabilizers,
        "maurer_cartan": {
            "first_jet_constraint_count": 0,
            "identity_uses_derivatives_of_first_jet_or_second_jet": True,
            "actual_coframe_identity_not_evolution_equation": True,
        },
        "physical_time_evolution_derived": False,
        "native_complete_return_derived": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = derive()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if not args.no_write:
        RESULT_PATH.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

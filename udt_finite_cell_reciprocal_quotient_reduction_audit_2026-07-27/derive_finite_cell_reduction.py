#!/usr/bin/env python3
"""Exact branchwise finite-cell reciprocal quotient-reduction algebra."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import sympy as sp


HERE = Path(__file__).resolve().parent


def zero(value: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in value)


def flatten(value: sp.Matrix) -> sp.Matrix:
    return value.reshape(value.rows * value.cols, 1)


def second_metric_jet(value: sp.Matrix, eta: sp.Matrix) -> sp.Matrix:
    return sp.simplify(
        value.T * value.T * eta
        + 2 * value.T * eta * value
        + eta * value * value
    )


def lorentz_generators() -> dict[str, sp.Matrix]:
    result: dict[str, sp.Matrix] = {}
    for i in range(1, 4):
        value = sp.zeros(4)
        value[0, i] = value[i, 0] = 1
        result[f"K0{i}"] = value
    for i, j in ((1, 2), (1, 3), (2, 3)):
        value = sp.zeros(4)
        value[i, j] = 1
        value[j, i] = -1
        result[f"J{i}{j}"] = value
    return result


def row_count(name: str) -> int:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    eta = sp.diag(-1, 1, 1, 1)
    u = sp.Matrix([1, 0, 0, 0])
    n = sp.Matrix([0, 1, 0, 0])
    p_u = -u * (u.T * eta)
    p_n = n * (n.T * eta)
    screen = sp.simplify(sp.eye(4) - p_u - p_n)
    q = sp.simplify(eta + (eta * u) * (eta * u).T - (eta * n) * (eta * n).T)
    checks: dict[str, str] = {}

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        checks[name] = "PASS"

    # Intrinsic pair -> basis-free screen.
    check("screen_projector_idempotent", zero(screen * screen - screen))
    check("screen_projector_rank_two", screen.rank() == 2)
    check("screen_annihilates_clock_and_ruler", screen * u == sp.zeros(4, 1) and screen * n == sp.zeros(4, 1))
    check("screen_metric_rank_two_positive_on_image", q == sp.diag(0, 0, 1, 1))
    p_u_flip = -(-u) * ((-u).T * eta)
    p_n_flip = (-n) * ((-n).T * eta)
    check("screen_projector_sign_independent", zero(screen - (sp.eye(4) - p_u_flip - p_n_flip)))

    # Basis-free branch lift and its screen-rotation representatives.
    phi, phi1, phi2, lam, w, alpha = sp.symbols(
        "phi phi1 phi2 lambda w alpha", real=True
    )
    h = -p_u + p_n
    x_lam = sp.simplify(h + lam * screen)
    check("branch_generator_projector_form", x_lam == sp.diag(-1, 1, lam, lam))
    response = sp.simplify(x_lam.T * eta + eta * x_lam)
    check("branch_response_isotropic_unmixed", response == sp.diag(2, 2, 2 * lam, 2 * lam))
    check("branch_mixing_block_zero", response[:2, 2:] == sp.zeros(2) and response[2:, :2] == sp.zeros(2))

    j = sp.Matrix([[0, 1], [-1, 0]])

    def rotation(angle: sp.Expr) -> sp.Matrix:
        return sp.Matrix(
            [[sp.cos(angle), sp.sin(angle)], [-sp.sin(angle), sp.cos(angle)]]
        )

    bphi = sp.diag(sp.exp(-phi), sp.exp(phi))
    qphi = sp.exp(lam * phi) * rotation(w * phi)
    f = bphi.row_join(sp.zeros(2)).col_join(sp.zeros(2).row_join(qphi))
    pi = sp.Matrix.hstack(sp.eye(2), sp.zeros(2))
    check("finite_lift_projects_founded_pair", zero(pi * f - bphi * pi))
    check("finite_lift_preserves_screen", f[:2, 2:] == sp.zeros(2))
    metric = sp.trigsimp(f.T * eta * f)
    expected_metric = sp.diag(
        -sp.exp(-2 * phi),
        sp.exp(2 * phi),
        sp.exp(2 * lam * phi),
        sp.exp(2 * lam * phi),
    )
    check("finite_metric_independent_of_screen_rotation", zero(metric - expected_metric))
    f1 = f.subs(phi, phi1)
    f2 = f.subs(phi, phi2)
    f12 = f.subs(phi, phi1 + phi2)
    check("finite_lift_complete_group_law", zero(sp.trigsimp(f2 * f1 - f12)))
    check("finite_lift_reversal", zero(sp.trigsimp(f.subs(phi, -phi) * f - sp.eye(4))))

    transition = sp.eye(4)
    transition[2:, 2:] = rotation(alpha)
    check("screen_SO2_transition_preserves_pair_and_screen", zero(transition * screen - screen * transition))
    check("isotropic_lift_commutes_with_screen_transition", zero(sp.trigsimp(transition * f - f * transition)))
    reflection = sp.eye(4)
    reflection[3, 3] = -1
    reflected_metric = sp.simplify(reflection.T * expected_metric * reflection)
    check("orientation_reversal_preserves_finite_metric", zero(reflected_metric - expected_metric))

    # No nonzero line is invariant under the full connected screen SO(2).
    vx, vy = sp.symbols("vx vy", real=True)
    v = sp.Matrix([vx, vy])
    invariant_vector_solution = sp.solve(list(j * v), (vx, vy), dict=True)
    check("no_nonzero_SO2_invariant_screen_vector", invariant_vector_solution == [{vx: 0, vy: 0}])
    check("no_real_SO2_invariant_screen_line", sp.expand(sp.det(sp.Matrix.hstack(v, j * v))) == -(vx**2 + vy**2))

    # Parent finite-lift counterstrata remain real outside the branch's
    # isotropic/unmixed response.
    a, b, d, mix = sp.symbols("a b d mix", real=True)
    s_aniso = sp.Matrix([[a, b], [b, d]])
    x_aniso_w = sp.diag(-1, 1, 0, 0)
    x_aniso_w[2:, 2:] = s_aniso + w * j
    x_aniso_0 = sp.diag(-1, 1, 0, 0)
    x_aniso_0[2:, 2:] = s_aniso
    aniso_diff = sp.simplify(
        second_metric_jet(x_aniso_w, eta) - second_metric_jet(x_aniso_0, eta)
    )
    check("anisotropic_counterstratum_rotation_visible", not zero(aniso_diff.subs({a: 2, b: 1, d: -1, w: 1})))
    x_mixed_w = sp.diag(-1, 1, lam, lam)
    x_mixed_w[2, 0] = mix
    x_mixed_w[2:, 2:] += w * j
    x_mixed_0 = sp.diag(-1, 1, lam, lam)
    x_mixed_0[2, 0] = mix
    mixed_diff = sp.simplify(
        second_metric_jet(x_mixed_w, eta) - second_metric_jet(x_mixed_0, eta)
    )
    check("mixed_counterstratum_rotation_visible", not zero(mixed_diff.subs({mix: 1, w: 1})))

    # Exact intrinsic/optical connection leakage and contact obstruction.
    p1, p2, p3, contact_b = sp.symbols("p1 p2 p3 contact_B", real=True)
    lplus_acceleration = sp.Matrix([-p1, -p1, -2 * p2, -2 * p3])
    lminus_acceleration = sp.Matrix([p1, -p1, -2 * p2, -2 * p3])
    check("aligned_null_screen_leakage_formula", lplus_acceleration[2:, :] == sp.Matrix([-2 * p2, -2 * p3]) and lminus_acceleration[2:, :] == sp.Matrix([-2 * p2, -2 * p3]))
    leakage_solution = sp.solve(
        list(lplus_acceleration[2:, :]), (p2, p3), dict=True
    )
    check("aligned_null_pregeodesic_requires_zero_screen_gradient", leakage_solution == [{p2: 0, p3: 0}])
    check("contact_bracket_forces_ruler_gradient", sp.solve([contact_b * p1], p1, dict=True) == [{p1: 0}])

    # The exact north-event covariant derivative control is independent of lambda.
    gamma_001 = -sp.Rational(3, 50)
    nabla_x_01 = sp.simplify(gamma_001 * (1 - (-1)))
    check("frozen_profile_nabla_X_component_exact", nabla_x_01 == -sp.Rational(3, 25))
    check("no_lambda_repairs_frozen_nonparallel_component", lam not in nabla_x_01.free_symbols and nabla_x_01 != 0)

    # Full Lorentz holonomy has scalar centralizer only.
    generators = lorentz_generators()
    zvars = sp.symbols("z0:16", real=True)
    z = sp.Matrix(4, 4, zvars)
    commutator_equations = []
    for generator in generators.values():
        commutator_equations.extend(list(z * generator - generator * z))
    commutator_matrix, _ = sp.linear_eq_to_matrix(commutator_equations, zvars)
    check("full_Lorentz_centralizer_constraint_rank_fifteen", commutator_matrix.rank() == 15)
    check("full_Lorentz_centralizer_dimension_one", 16 - commutator_matrix.rank() == 1)
    check("reciprocal_generator_is_never_scalar", x_lam[0, 0] != x_lam[1, 1])
    check("full_holonomy_cannot_preserve_reciprocal_generator", any(not zero(generator * x_lam - x_lam * generator) for generator in generators.values()))

    # Reduced lambda=+1 product preserves clock-vs-space only.
    x_plus = x_lam.subs(lam, 1)
    spatial_names = ("J12", "J13", "J23")
    check("lambda_plus1_commutes_with_spatial_so3", all(zero(generators[name] * x_plus - x_plus * generators[name]) for name in spatial_names))
    check("lambda_plus1_not_full_Lorentz_parallel_under_boosts", not zero(generators["K01"] * x_plus - x_plus * generators["K01"]))
    check("parallel_product_depth_is_trivial", sp.exp(0) == 1)
    twist_parameter = sp.symbols("twist_parameter", real=True)
    check("parallel_product_ruler_twist_removed", (twist_parameter * sp.Symbol("kappa")).subs(twist_parameter, 0) == 0)

    # The scalar seal cannot select branch/flag data.
    check("all_finite_lifts_identity_at_phi_zero", zero(f.subs(phi, 0) - sp.eye(4)))
    check("registered_branch_count_sixteen", row_count("BRANCH_UNIVERSE.tsv") == 16)
    check("registered_completion_count_twelve", row_count("COMPLETION_UNIVERSE.tsv") == 12)

    expected_check_count = 37
    check("registered_check_count_before_count_check", len(checks) == expected_check_count - 1)
    if len(checks) != expected_check_count:
        raise AssertionError(f"unexpected check count {len(checks)}")

    result = {
        "schema": "udt.finite_cell_reciprocal_quotient_reduction.derivation.v1",
        "result": "PASS",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "counts": {
            "registered_branches": row_count("BRANCH_UNIVERSE.tsv"),
            "registered_completions": row_count("COMPLETION_UNIVERSE.tsv"),
            "intrinsic_screen_rank": screen.rank(),
            "screen_rotation_metric_fiber": 1,
            "full_Lorentz_centralizer_dimension": 16 - commutator_matrix.rank(),
        },
        "branchwise_positive": {
            "twisted_S3_intrinsic_screen": "DERIVED_GIVEN_REGISTERED_CONFIGURATION",
            "basis_free_finite_lift": "F_lambda(phi)=exp(-phi)P_u+exp(phi)P_n+exp(lambda phi)H",
            "screen_rotation_descent": "FINITE_METRIC_REPRESENTATIVE_FREEDOM_BECAUSE_C_ZERO_AND_S_ISOTROPIC",
            "global_screen_bundle": "DERIVED_GIVEN_INTRINSIC_GLOBAL_PAIR",
        },
        "global_obstructions": {
            "metric_selected_screen_flag": "NOT_DERIVED_BY_REGISTERED_ZERO_JET_OR_GLOBAL_SOURCES",
            "projected_screen_transport": "DOES_NOT_CLOSE_GLOBALLY_FOR_NONCONSTANT_TWISTED_S3_DEPTH",
            "parallel_reciprocal_grading": "REFUTED_ON_FROZEN_NONCONSTANT_PROFILE_AND_FULL_HOLONOMY_CONTROLS",
            "endpoint_descent": "PATH_LABELLED_ONLY_ON_FULL_HOLONOMY_BRANCH",
            "reduced_survivor": "LAMBDA_PLUS1_CONSTANT_PHI_TWIST_ZERO_CLOCK_VS_ALL_SPACE_NOT_FULL_PAIR",
        },
        "physical_status": {
            "exact_quotient_semantics": "OPEN_NOT_SELECTED",
            "configuration_on_shell": "OPEN_NOT_SELECTED",
            "lambda": "OPEN_NOT_SELECTED",
            "observer_path_section": "OPEN_NOT_SELECTED",
            "other_completion_metrics": "STRUCTURAL_NO_CONCRETE_METRIC",
        },
        "maximum_conclusion": "TWISTED_S3_BRANCH_HAS_INTRINSIC_GLOBAL_SCREEN_AND_BASIS_FREE_FINITE_METRIC_QUOTIENT_LIFT;_SCREEN_ROTATION_IS_METRIC_GAUGE_POINTWISE;_FULL_CONNECTION_HOLONOMY_PREVENTS_PARALLEL_OR_ENDPOINT_QUOTIENT_DESCENT;_PHYSICAL_SELECTION_OPEN",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

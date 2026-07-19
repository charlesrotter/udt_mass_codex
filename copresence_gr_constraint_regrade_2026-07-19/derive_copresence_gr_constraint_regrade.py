#!/usr/bin/env python3
"""Exact CPU anchors for the co-presence regrade of GR-origin constraints."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
RESULT = HERE / "DERIVATION_RESULT.json"
OUTCOME = "PRIOR_ALGEBRA_SURVIVES_CONSTRAINT_ROLES_RECLASSIFIED_NO_NATIVE_GR_CONSTRAINT_SELECTED"


def require(name: str, condition: bool, checks: dict[str, bool]) -> None:
    checks[name] = bool(condition)
    if not condition:
        raise AssertionError(name)


def main() -> None:
    checks: dict[str, bool] = {}

    # Predicate, multiplier, and restricted-domain roles are not interchangeable.
    x, y, eta = sp.symbols("x y eta", real=True)
    base = x**2 + y**2
    constraint = x + y - 1
    metric_root = sp.solve([sp.diff(base, x), sp.diff(base, y)], [x, y], dict=True)[0]
    augmented = base + eta * constraint
    multiplier_root = sp.solve(
        [sp.diff(augmented, x), sp.diff(augmented, y), sp.diff(augmented, eta)],
        [x, y, eta],
        dict=True,
    )[0]
    restricted = sp.expand(base.subs(y, 1 - x))
    restricted_root = sp.solve(sp.Eq(sp.diff(restricted, x), 0), x)[0]
    require("unrestricted_root_exact", metric_root == {x: 0, y: 0}, checks)
    require("after_solution_predicate_not_automatically_satisfied", constraint.subs(metric_root) == -1, checks)
    require(
        "varied_multiplier_root_exact",
        multiplier_root == {x: sp.Rational(1, 2), y: sp.Rational(1, 2), eta: -1},
        checks,
    )
    require("restricted_tangent_root_exact", restricted_root == sp.Rational(1, 2), checks)
    require(
        "multiplier_reaction_nonzero",
        sp.Matrix([eta * sp.diff(constraint, x), eta * sp.diff(constraint, y)]).subs(multiplier_root)
        == sp.Matrix([-1, -1]),
        checks,
    )

    # An aligned constraint can be redundant at one root without proving off-shell equivalence.
    aligned_base = (x - 1) ** 2 + (y - 2) ** 2
    aligned_constraint = x + y - 3
    aligned_augmented = aligned_base + eta * aligned_constraint
    aligned_root = sp.solve(
        [
            sp.diff(aligned_augmented, x),
            sp.diff(aligned_augmented, y),
            sp.diff(aligned_augmented, eta),
        ],
        [x, y, eta],
        dict=True,
    )[0]
    require("aligned_constraint_root_exact", aligned_root == {x: 1, y: 2, eta: 0}, checks)

    # A finite penalty does not exactly enforce a hard constraint.
    alpha = sp.symbols("alpha", positive=True, finite=True)
    penalty = base + alpha * constraint**2 / 2
    penalty_root = sp.solve([sp.diff(penalty, x), sp.diff(penalty, y)], [x, y], dict=True)[0]
    penalty_residual = sp.simplify(constraint.subs(penalty_root))
    require("finite_penalty_root_exact", penalty_root == {x: alpha / (2 * (alpha + 1)), y: alpha / (2 * (alpha + 1))}, checks)
    require("finite_penalty_constraint_residual_nonzero", penalty_residual == -1 / (alpha + 1), checks)

    # A Noether identity relates equations; it is not an additional independent equation.
    u, v = sp.symbols("u v", real=True)
    gauge_action = (u - v) ** 2
    e_u = sp.diff(gauge_action, u)
    e_v = sp.diff(gauge_action, v)
    require("finite_noether_identity", sp.simplify(e_u + e_v) == 0, checks)
    require("noether_equations_not_each_identity", e_u != 0 and e_v != 0, checks)

    # A foliation projection can vanish in one slicing and not another.
    rapidity = sp.symbols("zeta", real=True)
    minkowski = sp.diag(-1, 1)
    normal = sp.Matrix([sp.cosh(rapidity), sp.sinh(rapidity)])
    tangent = sp.Matrix([sp.sinh(rapidity), sp.cosh(rapidity)])
    require("boosted_normal_unit_timelike", sp.simplify((normal.T * minkowski * normal)[0] + 1) == 0, checks)
    require("boosted_tangent_unit_spacelike", sp.simplify((tangent.T * minkowski * tangent)[0] - 1) == 0, checks)
    require("boosted_frame_orthogonal", sp.simplify((normal.T * minkowski * tangent)[0]) == 0, checks)

    tensor = sp.Matrix([[0, 0], [0, 1]])
    h_projection = sp.simplify((normal.T * tensor * normal)[0])
    m_projection = sp.simplify((normal.T * tensor * tangent)[0])
    require("normal_projection_slice_dependent", h_projection == sp.sinh(rapidity) ** 2, checks)
    require("normal_projection_vanishes_in_reference_slice", h_projection.subs(rapidity, 0) == 0, checks)
    require("normal_projection_nonzero_in_boosted_slice", sp.simplify(h_projection.subs(rapidity, 1)) != 0, checks)
    require(
        "momentum_projection_slice_dependent",
        sp.simplify(m_projection - sp.sinh(rapidity) * sp.cosh(rapidity)) == 0,
        checks,
    )
    zero_tensor = sp.zeros(2)
    require(
        "complete_tensor_zero_implies_all_projections_zero",
        sp.simplify((normal.T * zero_tensor * normal)[0]) == 0
        and sp.simplify((normal.T * zero_tensor * tangent)[0]) == 0,
        checks,
    )

    # Constraint propagation depends on the local equations, not whole-history co-membership.
    time = sp.symbols("t", real=True)
    u0, v0, a, b = sp.symbols("u0 v0 a b", real=True)
    propagated_u = u0 + a * time
    propagated_v = v0 + a * time
    propagated_constraint = sp.expand(propagated_u - propagated_v)
    require("paired_dynamics_propagates_constraint", propagated_constraint == u0 - v0, checks)
    require(
        "zero_initial_constraint_propagates_under_paired_dynamics",
        sp.simplify(propagated_constraint.subs(v0, u0)) == 0,
        checks,
    )

    unpaired_u = u0 + a * time
    unpaired_v = v0 + b * time
    unpaired_constraint = sp.expand(unpaired_u - unpaired_v)
    require("unpaired_dynamics_constraint_drift", sp.diff(unpaired_constraint, time) == a - b, checks)
    require(
        "zero_initial_constraint_not_sufficient_without_propagation_law",
        sp.simplify(unpaired_constraint.subs(v0, u0)) == time * (a - b),
        checks,
    )
    history_coefficients = sp.Poly(unpaired_constraint, time).all_coeffs()
    require("whole_history_admissibility_requires_two_conditions", history_coefficients == [a - b, u0 - v0], checks)
    require(
        "same_copresence_domain_allows_distinct_constraint_propagation",
        sp.simplify(unpaired_constraint - propagated_constraint) == time * (a - b),
        checks,
    )
    require(
        "same_background_allows_distinct_parent_tensor_projections",
        tensor != zero_tensor and h_projection != 0,
        checks,
    )

    # Lapse-like canonical multiplier: formal role only, not a UDT field adoption.
    q, p, lapse, qdot = sp.symbols("q p N qdot", real=True)
    hamiltonian_constraint = (p**2 + q**2 - 1) / 2
    canonical_lagrangian = p * qdot - lapse * hamiltonian_constraint
    require("lapse_variation_imposes_constraint", sp.diff(canonical_lagrangian, lapse) == -hamiltonian_constraint, checks)
    require("lapse_adds_q_reaction", sp.diff(canonical_lagrangian, q) == -lapse * q, checks)
    require("lapse_adds_p_reaction", sp.diff(canonical_lagrangian, p) == qdot - lapse * p, checks)

    # Finite-boundary contribution from a multiplier term.
    qprime, multiplier = sp.symbols("qprime lambda", real=True)
    boundary_lagrangian = qprime**2 / 2 + multiplier * qprime
    boundary_momentum = sp.diff(boundary_lagrangian, qprime)
    require("multiplier_changes_boundary_momentum", boundary_momentum == qprime + multiplier, checks)

    role_counts = {
        "RETAINED": 11,
        "RECLASSIFIED_CONDITIONAL": 4,
        "OPEN": 7,
        "REJECTED_AS_INFERENCE": 5,
    }
    payload = {
        "schema": "udt-copresence-gr-constraint-regrade-v1",
        "date": "2026-07-19",
        "outcome": OUTCOME,
        "versions": {"python": platform.python_version(), "sympy": sp.__version__},
        "scope": "constraint-role and provenance regrade; no concrete GR constraint adopted",
        "exact_checks": {"passed": sum(checks.values()), "total": len(checks), "checks": checks},
        "derived": {
            "metric_only_root": [str(metric_root[x]), str(metric_root[y])],
            "metric_only_predicate_residual": str(constraint.subs(metric_root)),
            "multiplier_root": [str(multiplier_root[x]), str(multiplier_root[y]), str(multiplier_root[eta])],
            "restricted_root": str(restricted_root),
            "finite_penalty_residual": str(penalty_residual),
            "noether_identity": str(sp.simplify(e_u + e_v)),
            "boosted_hamiltonian_like_projection": str(h_projection),
            "boosted_momentum_like_projection": str(m_projection),
            "propagated_constraint": str(propagated_constraint),
            "unpropagated_constraint": str(unpaired_constraint),
            "whole_history_coefficients": [str(item) for item in history_coefficients],
            "lapse_multiplier_equation": str(sp.diff(canonical_lagrangian, lapse)),
            "boundary_momentum": str(boundary_momentum),
        },
        "classification": {
            "prior_gr_constraint_algebra": "RETAINED",
            "prior_paired_top_level": "RETAINED_BOTH_CONDITIONALLY_ADMISSIBLE",
            "bootstrap_whole_solution_role": "RETAINED_AND_CLARIFIED_ON_SHELL_ADMISSIBILITY",
            "hamiltonian_momentum_constraints": "PARENT_EQUATION_AND_FOLIATION_CONDITIONAL_NOT_NATIVE",
            "lapse": "FORMAL_MULTIPLIER_EXAMPLE_NOT_NATIVE_ONTOLOGY",
            "shift": "OPEN_NATIVE_ONTOLOGY_AND_DETAILED_ROLE_NOT_DERIVED_HERE",
            "constraint_propagation": "OPEN_REQUIRES_LOCAL_DYNAMICS_AND_DATA",
            "copresence_as_propagation_mechanism": "REJECTED_AS_INFERENCE",
            "field_census_selection": "OPEN_NOT_SELECTED",
            "action_selection": "OPEN_NOT_SELECTED",
            "physical_calibration": "OPEN_REQUIRES_REPRESENTATIVE_AND_MATERIAL_RULES",
            "same_copresence_countermodels": "DERIVED_NONSELECTION_OF_CONSTRAINT_LAW",
        },
        "role_counts": role_counts,
        "maximum_conclusion": "RECLASSIFICATION_OVERLAY_ONLY",
    }
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"outcome={OUTCOME}")
    print(f"exact_checks={sum(checks.values())}/{len(checks)}")
    print(f"result_sha256={hashlib.sha256(RESULT.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()

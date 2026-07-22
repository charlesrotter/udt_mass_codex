#!/usr/bin/env python3
"""Exact controls for the reciprocal-subbundle ownership audit.

This is a finite-dimensional configuration/selection audit.  It does not
define a UDT action, equation of motion, or physical time evolution.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def orthogonal_projector(g: sp.Matrix, columns: sp.Matrix) -> sp.Matrix:
    gram = columns.T * g * columns
    return sp.simplify(columns * gram.inv() * columns.T * g)


def algebra_basis(generators: list[sp.Matrix]) -> list[sp.Matrix]:
    """Close a rational matrix set under multiplication."""
    size = generators[0].rows
    basis: list[sp.Matrix] = []

    def add(candidate: sp.Matrix) -> bool:
        vectors = [item.reshape(size * size, 1) for item in basis]
        before = sp.Matrix.hstack(*vectors).rank() if vectors else 0
        after_vectors = vectors + [candidate.reshape(size * size, 1)]
        after = sp.Matrix.hstack(*after_vectors).rank()
        if after > before:
            basis.append(candidate)
            return True
        return False

    add(sp.eye(size))
    for generator in generators:
        add(generator)
    changed = True
    while changed:
        changed = False
        snapshot = list(basis)
        for left in snapshot:
            for right in snapshot:
                if add(sp.simplify(left * right)):
                    changed = True
    return basis


def commutant_solution(generators: list[sp.Matrix]) -> tuple[sp.FiniteSet, tuple[sp.Symbol, ...]]:
    variables = sp.symbols("x0:16")
    matrix = sp.Matrix(4, 4, variables)
    equations = []
    for generator in generators:
        equations.extend(list(matrix * generator - generator * matrix))
    return sp.linsolve(equations, variables), variables


def main() -> None:
    q = sp.diag(-1, 1, 1, 1)
    e0, e1, e2, e3 = [sp.eye(4)[:, index] for index in range(4)]
    seal = sp.diag(1, -1, 1, 1)

    # An exact proper, orthochronous boost tangent to the seal.
    gamma = sp.Rational(5, 3)
    gamma_v = sp.Rational(4, 3)
    boost_02 = sp.Matrix(
        [
            [gamma, 0, gamma_v, 0],
            [0, 1, 0, 0],
            [gamma_v, 0, gamma, 0],
            [0, 0, 0, 1],
        ]
    )

    # Two reciprocal-plane solderings at the same admitted symmetric seal data.
    solder_0 = sp.Matrix.hstack(e0, e1)
    solder_1 = boost_02 * solder_0
    eta_2 = sp.diag(-1, 1)
    seal_2 = sp.diag(1, -1)
    projector_0 = orthogonal_projector(q, solder_0)
    projector_1 = orthogonal_projector(q, solder_1)

    # Connected stabilizer of the seal normal inside its Lorentzian tangent 3-plane.
    boost_generator_02 = sp.zeros(4)
    boost_generator_02[0, 2] = boost_generator_02[2, 0] = 1
    boost_generator_03 = sp.zeros(4)
    boost_generator_03[0, 3] = boost_generator_03[3, 0] = 1
    rotation_generator_23 = sp.zeros(4)
    rotation_generator_23[2, 3] = -1
    rotation_generator_23[3, 2] = 1
    stabilizer_generators = [boost_generator_02, boost_generator_03, rotation_generator_23]
    stabilizer_solution, stabilizer_variables = commutant_solution(stabilizer_generators)
    solution_tuple = next(iter(stabilizer_solution))
    stabilizer_matrix = sp.Matrix(4, 4, solution_tuple)
    free_symbols = sorted(
        set().union(*(value.free_symbols for value in solution_tuple)), key=lambda item: item.name
    )
    stabilizer_projector_ranks = sorted(
        {
            int(stabilizer_matrix.subs(dict(zip(free_symbols, values))).rank())
            for values in ((0, 0), (0, 1), (1, 0), (1, 1))
            if zero_matrix(
                stabilizer_matrix.subs(dict(zip(free_symbols, values))) ** 2
                - stabilizer_matrix.subs(dict(zip(free_symbols, values)))
            )
        }
    )

    # Timelike dphi leaves the complete spatial rotation group; it marks no spatial partner.
    rotation_generator_12 = sp.zeros(4)
    rotation_generator_12[1, 2] = -1
    rotation_generator_12[2, 1] = 1
    rotation_generator_13 = sp.zeros(4)
    rotation_generator_13[1, 3] = -1
    rotation_generator_13[3, 1] = 1
    timelike_solution, _ = commutant_solution(
        [rotation_generator_12, rotation_generator_13, rotation_generator_23]
    )
    timelike_matrix = sp.Matrix(4, 4, next(iter(timelike_solution)))
    timelike_free = sorted(
        set().union(*(value.free_symbols for value in timelike_matrix)), key=lambda item: item.name
    )
    timelike_projector_ranks = sorted(
        {
            int(timelike_matrix.subs(dict(zip(timelike_free, values))).rank())
            for values in ((0, 0), (0, 1), (1, 0), (1, 1))
            if zero_matrix(
                timelike_matrix.subs(dict(zip(timelike_free, values))) ** 2
                - timelike_matrix.subs(dict(zip(timelike_free, values)))
            )
        }
    )

    # Null dphi: use a null basis and the full connected little algebra (two null rotations + SO(2)).
    null_metric = sp.Matrix(
        [[0, -1, 0, 0], [-1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    )
    null_rotation_1 = sp.Matrix(
        [[0, 0, 1, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
    )
    null_rotation_2 = sp.Matrix(
        [[0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0]]
    )
    null_screen_rotation = sp.Matrix(
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, -1], [0, 0, 1, 0]]
    )
    null_generators = [null_rotation_1, null_rotation_2, null_screen_rotation]
    null_solution, _ = commutant_solution(null_generators)
    null_matrix = sp.Matrix(4, 4, next(iter(null_solution)))
    null_a, null_b = sorted(
        set().union(*(value.free_symbols for value in null_matrix)), key=lambda item: item.name
    )
    null_idempotent_solutions = sp.solve(
        list(null_matrix**2 - null_matrix), [null_a, null_b], dict=True
    )
    null_projector_ranks = sorted(
        {int(null_matrix.subs(solution).rank()) for solution in null_idempotent_solutions}
    )

    # Simple curvature endomorphism: three distinct Lorentzian rank-two spectral pairings survive.
    simple_ricci = sp.diag(1, 2, 3, 4)
    ricci_planes = [
        sp.diag(1, 1, 0, 0),
        sp.diag(1, 0, 1, 0),
        sp.diag(1, 0, 0, 1),
    ]

    # Exact full-algebra and flat controls for the registered holonomy dichotomy.
    distinct_diagonal = sp.diag(1, 2, 3, 4)
    dense = sp.ones(4)
    full_basis = algebra_basis([distinct_diagonal, dense])
    full_commutant, _ = commutant_solution([distinct_diagonal, dense])

    # Complete registered angular seal-lift alternatives.
    identity_2 = sp.eye(2)
    minus_identity_2 = -sp.eye(2)
    reflection_2 = sp.diag(1, -1)
    m00, m01, m10, m11 = sp.symbols("m00 m01 m10 m11")
    m = sp.Matrix([[m00, m01], [m10, m11]])

    def anticommutant_dimension(lift: sp.Matrix) -> int:
        equations = list(lift * m * lift + m)
        coefficient, _rhs = sp.linear_eq_to_matrix(equations, [m00, m01, m10, m11])
        return 4 - coefficient.rank()

    hodge_2 = sp.Matrix([[0, -1], [1, 0]])
    complementary = hodge_2 * reflection_2

    # Abstract reciprocal representation remains exact independently of a soldering.
    phi = sp.symbols("phi", real=True)
    reciprocal_character = sp.diag(sp.exp(-phi), sp.exp(phi))
    dual_pairing = sp.Matrix([[0, 1], [1, 0]])

    omega = sp.symbols("omega", positive=True)
    projector_csn = orthogonal_projector(omega**2 * q, solder_0)

    checks = {
        "abstract_reciprocal_pairing_preserved": zero_matrix(
            reciprocal_character.T * dual_pairing * reciprocal_character - dual_pairing
        ),
        "boost_preserves_metric": zero_matrix(boost_02.T * q * boost_02 - q),
        "boost_is_proper": sp.simplify(boost_02.det() - 1) == 0,
        "boost_is_orthochronous": bool(boost_02[0, 0] > 0),
        "boost_preserves_seal": zero_matrix(boost_02 * seal - seal * boost_02),
        "boost_preserves_normal_and_static_dphi_direction": boost_02 * e1 == e1,
        "soldering_0_induced_lorentz_pair": zero_matrix(solder_0.T * q * solder_0 - eta_2),
        "soldering_1_induced_lorentz_pair": zero_matrix(solder_1.T * q * solder_1 - eta_2),
        "soldering_0_seal_intertwining": zero_matrix(seal * solder_0 - solder_0 * seal_2),
        "soldering_1_seal_intertwining": zero_matrix(seal * solder_1 - solder_1 * seal_2),
        "projector_0_valid": zero_matrix(projector_0**2 - projector_0)
        and projector_0.rank() == 2
        and zero_matrix(projector_0.T * q - q * projector_0),
        "projector_1_valid": zero_matrix(projector_1**2 - projector_1)
        and projector_1.rank() == 2
        and zero_matrix(projector_1.T * q - q * projector_1),
        "projectors_distinct": not zero_matrix(projector_1 - projector_0),
        "stabilizer_maps_projectors": zero_matrix(
            projector_1 - boost_02 * projector_0 * boost_02.inv()
        ),
        "no_rank_two_stabilizer_invariant_projector": stabilizer_projector_ranks == [0, 1, 3, 4],
        "timelike_dphi_has_no_rank_two_stabilizer_invariant_projector": timelike_projector_ranks
        == [0, 1, 3, 4],
        "null_dphi_little_group_preserves_no_rank_two_projector": null_projector_ranks == [0, 4]
        and all(zero_matrix(generator.T * null_metric + null_metric * generator) for generator in null_generators),
        "csn_does_not_select_projector": zero_matrix(projector_csn - projector_0),
        "simple_ricci_retains_three_lorentzian_pairings": len(ricci_planes) == 3
        and all(
            projector.rank() == 2
            and zero_matrix(projector * simple_ricci - simple_ricci * projector)
            for projector in ricci_planes
        ),
        "full_generator_algebra_is_M4": len(full_basis) == 16,
        "full_generator_commutant_is_scalar": str(full_commutant)
        == "{(x15, 0, 0, 0, 0, x15, 0, 0, 0, 0, x15, 0, 0, 0, 0, x15)}",
        "flat_control_preserves_multiple_planes": zero_matrix(sp.zeros(4) * projector_0)
        and zero_matrix(sp.zeros(4) * projector_1),
        "identity_angular_lift_has_no_anticommutant": anticommutant_dimension(identity_2) == 0,
        "minus_identity_angular_lift_has_no_anticommutant": anticommutant_dimension(minus_identity_2)
        == 0,
        "reflection_angular_lift_has_anticommutant": anticommutant_dimension(reflection_2) == 2,
        "reflection_metric_complement_exists": zero_matrix(complementary**2 - identity_2)
        and sp.trace(complementary) == 0
        and zero_matrix(complementary.T - complementary)
        and zero_matrix(reflection_2 * complementary * reflection_2 + complementary),
        "orientation_hodge_is_not_real_involution": zero_matrix(hodge_2**2 + identity_2),
    }

    if not all(checks.values()):
        failed = [name for name, value in checks.items() if not value]
        raise AssertionError(f"failed exact checks: {failed}")

    result = {
        "schema": "udt-reciprocal-subbundle-ownership-algebra-1.0",
        "status": "PASS",
        "sympy_version": sp.__version__,
        "checks": checks,
        "counts": {
            "exact_checks": len(checks),
            "boundary_soldering_witnesses": 2,
            "stabilizer_invariant_projector_ranks": stabilizer_projector_ranks,
            "timelike_dphi_invariant_projector_ranks": timelike_projector_ranks,
            "null_dphi_invariant_projector_ranks": null_projector_ranks,
            "simple_ricci_lorentzian_rank_two_pairings": len(ricci_planes),
            "full_algebra_dimension": len(full_basis),
            "angular_lift_anticommutant_dimensions": {
                "PLUS_IDENTITY": anticommutant_dimension(identity_2),
                "MINUS_IDENTITY": anticommutant_dimension(minus_identity_2),
                "AXIS_REFLECTION": anticommutant_dimension(reflection_2),
            },
        },
        "exact_matrices": {
            "metric": str(q.tolist()),
            "seal": str(seal.tolist()),
            "tangent_boost": str(boost_02.tolist()),
            "projector_0": str(projector_0.tolist()),
            "projector_1": str(projector_1.tolist()),
            "stabilizer_commutant": str(stabilizer_matrix.tolist()),
            "timelike_dphi_commutant": str(timelike_matrix.tolist()),
            "null_dphi_commutant": str(null_matrix.tolist()),
            "reflection_complement": str(complementary.tolist()),
        },
        "scope": "FINITE_DIMENSIONAL_BOUNDARY_AND_POINTWISE_CONTROLS_ONLY",
        "maximum_conclusion": "CURRENT_REGISTERED_DATA_DO_NOT_SELECT_A_UNIVERSAL_RECIPROCAL_SUBBUNDLE",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

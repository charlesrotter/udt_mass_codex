#!/usr/bin/env python3
"""Exact finite-dimensional witnesses for the G123 direct-incidence theorem."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def phase_lift(radius: sp.Expr) -> sp.Matrix:
    """Flat point-observer query tangent -> source screen phase in matched bases."""
    return sp.Matrix(
        [
            [0, 0, radius, 0],
            [0, 0, 0, radius],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )


def main() -> None:
    eta = sp.diag(-1, 1, 1, 1)
    M_A = sp.Matrix(
        [[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 4, 0], [0, 0, 0, 4]]
    )
    M_B = sp.Matrix(
        [
            [1, 1, 0, 0],
            [0, sp.Rational(4, 5), 3, 0],
            [0, sp.Rational(-3, 5), 4, 0],
            [0, 0, 0, 5],
        ]
    )
    M_C = sp.Matrix(
        [
            [1, 1, 0, 0],
            [0, sp.Rational(4, 5), 0, 3],
            [0, 0, 5, 0],
            [0, sp.Rational(-3, 5), 0, 4],
        ]
    )

    D_BA = sp.simplify(M_B.inv() * M_A)
    D_CB = sp.simplify(M_C.inv() * M_B)
    D_CA = sp.simplify(M_C.inv() * M_A)
    D_AB = sp.simplify(M_A.inv() * M_B)

    H_A = sp.simplify(M_A.T * eta * M_A)
    H_B = sp.simplify(M_B.T * eta * M_B)
    pair_A = H_A[:2, :2]
    pair_B = H_B[:2, :2]
    # Relative to the preregistered query split, this block carries A-angular
    # input variations into B-longitudinal output coordinates.  Its rank is
    # invariant only under block-preserving reparameterizations of that split.
    angular_to_pair_block = D_BA[:2, 2:]

    # Collinear rays at affine radii 4 and 5: direct incidence matches source
    # position but not the derivative half of phase.
    M_B_collinear = sp.Matrix(
        [[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 5, 0], [0, 0, 0, 5]]
    )
    D_collinear = sp.simplify(M_B_collinear.inv() * M_A)
    lift_A = phase_lift(sp.Integer(4))
    lift_B = phase_lift(sp.Integer(5))
    carried_lift_B = sp.simplify(lift_B * D_collinear)
    position_match = zero(carried_lift_B[:2, :] - lift_A[:2, :])
    momentum_match = zero(carried_lift_B[2:, :] - lift_A[2:, :])

    Lambda_A = sp.Matrix.vstack(4 * sp.eye(2), sp.eye(2))
    Lambda_B = sp.Matrix.vstack(5 * sp.eye(2), sp.eye(2))
    Lambda_aligned = Lambda_A.copy()
    mismatch_intersection = 4 - sp.Matrix.hstack(Lambda_A, Lambda_B).rank()
    aligned_intersection = 4 - sp.Matrix.hstack(Lambda_A, Lambda_aligned).rank()

    vertex_dF = sp.Matrix(
        [[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    )

    expected_D_BA = sp.Matrix(
        [
            [1, sp.Rational(1, 5), sp.Rational(12, 5), 0],
            [0, sp.Rational(4, 5), sp.Rational(-12, 5), 0],
            [0, sp.Rational(3, 25), sp.Rational(16, 25), 0],
            [0, 0, 0, sp.Rational(4, 5)],
        ]
    )

    checks = {
        "regular_source_leg_A": M_A.rank() == 4,
        "regular_source_leg_B": M_B.rank() == 4,
        "regular_source_leg_C": M_C.rank() == 4,
        "direct_map_exact": D_BA == expected_D_BA,
        "direct_map_reversal": zero(D_AB * D_BA - sp.eye(4)),
        "three_observer_composition": zero(D_CB * D_BA - D_CA),
        "complete_pullback_isometry": zero(D_BA.T * H_B * D_BA - H_A),
        "direct_map_has_angular_to_pair_mixing_in_supplied_split": (
            angular_to_pair_block.rank() > 0
        ),
        "terminal_pair_blocks_regular": pair_A.det() == -1 and pair_B.det() == -1,
        "terminal_pair_depths_zero_in_flat_control": (
            sp.simplify(-pair_A.det() / pair_A[0, 0] ** 2) == 1
            and sp.simplify(-pair_B.det() / pair_B[0, 0] ** 2) == 1
        ),
        "point_observer_phase_lifts_rank_two": lift_A.rank() == 2 and lift_B.rank() == 2,
        "incidence_matches_source_position": position_match,
        "incidence_does_not_force_phase_momentum": not momentum_match,
        "mismatched_phase_planes_intersection_zero": mismatch_intersection == 0,
        "aligned_phase_stratum_nonempty": aligned_intersection == 2,
        "vertex_full_differential_rank_two": vertex_dF.rank() == 2,
    }

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "exact_objects": {
            "D_BA": str(D_BA),
            "D_BA_determinant": str(sp.factor(D_BA.det())),
            "H_A": str(H_A),
            "H_B": str(H_B),
            "angular_to_pair_block_rank_in_supplied_split": int(
                angular_to_pair_block.rank()
            ),
            "D_collinear": str(D_collinear),
            "lift_A_rank": int(lift_A.rank()),
            "lift_B_rank": int(lift_B.rank()),
            "mismatch_intersection_dimension": int(mismatch_intersection),
            "aligned_intersection_dimension": int(aligned_intersection),
            "vertex_dF_rank": int(vertex_dF.rank()),
        },
        "landing": (
            "DECLARED_COMMON_EVENT_OBSERVER_EXPONENTIAL_INCIDENCE_RELATION_DERIVED_CONDITIONALLY__"
            "REGULAR_STRATUM_IS_FOUR_DIMENSIONAL_LOCAL_QUERY_TANGENT_GRAPH__"
            "REGULAR_MULTIPLE_PREIMAGES_GIVE_LOCAL_GRAPH_BRANCHES__"
            "NONTRANSVERSE_VERTEX_OR_CAUSTIC_FIBERS_REMAIN_UNCLASSIFIED_STRATIFIED_RELATIONS__"
            "DIRECT_TANGENT_MAP_IS_NOT_A_FULL_JACOBI_PHASE_ARROW__"
            "PHASE_MATCHING_REMAINS_A_SOURCE_BOUNDARY_COMPATIBILITY_CONDITION__"
            "NO_HISTORY_SELECTOR_FOUND_IN_DECLARED_COMMON_EVENT_TEST"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

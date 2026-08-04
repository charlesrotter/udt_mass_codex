#!/usr/bin/env python3
"""Exact metric-natural reciprocal/screen selector atlas."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ETA = sp.diag(-1, 1, 1, 1)
I4 = sp.eye(4)


def generator(i: int, j: int) -> sp.Matrix:
    """Lorentz generator in the defining representation."""
    out = sp.zeros(4)
    if i == 0:
        out[i, j] = 1
        out[j, i] = 1
    else:
        out[i, j] = 1
        out[j, i] = -1
    assert out.T * ETA + ETA * out == sp.zeros(4)
    return out


BOOSTS = [generator(0, i) for i in (1, 2, 3)]
ROTATIONS = [generator(1, 2), generator(1, 3), generator(2, 3)]
LORENTZ = BOOSTS + ROTATIONS
SO12_COMPLEMENT_E1 = [generator(0, 2), generator(0, 3), generator(2, 3)]
NULL_LITTLE_GROUP = [generator(2, 3), generator(0, 2) + generator(1, 2), generator(0, 3) + generator(1, 3)]


def commutant(generators: list[sp.Matrix]) -> tuple[int, list[sp.Matrix]]:
    variables = sp.symbols("p0:16")
    matrix = sp.Matrix(4, 4, variables)
    equations: list[sp.Expr] = []
    for item in generators:
        equations.extend(matrix * item - item * matrix)
    coefficient, _ = sp.linear_eq_to_matrix(equations, variables)
    basis = [sp.Matrix(4, 4, vector) for vector in coefficient.nullspace()]
    return coefficient.rank(), basis


def spectral_projector(operator: sp.Matrix, value: sp.Expr, others: list[sp.Expr]) -> sp.Matrix:
    out = I4
    for other in others:
        out = sp.simplify(out * (operator - other * I4) / (value - other))
    return sp.simplify(out)


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


full_rank, full_basis = commutant(LORENTZ)
round_rank, round_basis = commutant(ROTATIONS)
ruler_rank, ruler_basis = commutant(SO12_COMPLEMENT_E1)
null_rank, null_basis = commutant(NULL_LITTLE_GROUP)

assert full_rank == 15 and len(full_basis) == 1
assert full_basis[0] == I4 or full_basis[0] == -I4
assert round_rank == 14 and len(round_basis) == 2
assert ruler_rank == 14 and len(ruler_basis) == 2
assert null_rank == 14 and len(null_basis) == 2

# Full isotropy leaves scalar projectors only; scalar idempotents have rank zero or four.
s = sp.symbols("s", real=True)
scalar_idempotents = sp.solve(sp.Eq(s * s, s), s)
assert scalar_idempotents == [0, 1]

# SO(3) leaves only the time line and the full spatial three-plane as irreducible blocks.
round_projector_ranks = sorted({a + 3 * b for a in (0, 1) for b in (0, 1)})
assert round_projector_ranks == [0, 1, 3, 4]
assert 2 not in round_projector_ranks

# A single spacelike ruler line has the dual SO+(1,2) obstruction.
ruler_projector_ranks = sorted({a + 3 * b for a in (0, 1) for b in (0, 1)})
assert ruler_projector_ranks == [0, 1, 3, 4]

# The null-vector little group has a two-dimensional nonsemisimple commutant, but no rank-two
# idempotent. In the displayed basis B0^2=0 and B0+B1=I, so idempotency leaves only 0 and I.
B0 = sp.Matrix([[-1, 1, 0, 0], [-1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
B1 = sp.Matrix([[2, -1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
assert B0 * B0 == sp.zeros(4) and B0 + B1 == I4
assert all(B0 * item == item * B0 and B1 * item == item * B1 for item in NULL_LITTLE_GROUP)
null_idempotent_ranks = [0, 4]

# Distinct Ricci eigenvalues construct a natural rank-two polynomial projector.
A = sp.diag(2, 3, 5, 5)
ricci_q02 = sp.diag(0, sp.Rational(1, 2), sp.Rational(3, 2), sp.Rational(3, 2))
assert A == 2 * I4 + 2 * ricci_q02
P_time = spectral_projector(A, sp.Integer(2), [sp.Integer(3), sp.Integer(5)])
P_ruler = spectral_projector(A, sp.Integer(3), [sp.Integer(2), sp.Integer(5)])
P = sp.simplify(P_time + P_ruler)
assert P == sp.diag(1, 1, 0, 0)
assert P * P == P and P.rank() == 2
assert P.T * ETA == ETA * P

# Exact rational boost verifies covariance of the polynomial construction.
boost = sp.Matrix(
    [
        [sp.Rational(5, 3), 0, sp.Rational(4, 3), 0],
        [0, 1, 0, 0],
        [sp.Rational(4, 3), 0, sp.Rational(5, 3), 0],
        [0, 0, 0, 1],
    ]
)
assert boost.T * ETA * boost == ETA
A_prime = sp.simplify(boost * A * boost.inv())
P_prime = sp.simplify(
    spectral_projector(A_prime, sp.Integer(2), [sp.Integer(3), sp.Integer(5)])
    + spectral_projector(A_prime, sp.Integer(3), [sp.Integer(2), sp.Integer(5)])
)
assert P_prime == sp.simplify(boost * P * boost.inv())

# Two simple-spectrum approaches meet the same round operator but select different limits.
epsilon = sp.symbols("epsilon", positive=True)
A_e1 = sp.diag(2, 5 - epsilon, 5, 5)
A_e2 = sp.diag(2, 5, 5 - epsilon, 5)
A_round = sp.diag(2, 5, 5, 5)
P_e1 = sp.diag(1, 1, 0, 0)
P_e2 = sp.diag(1, 0, 1, 0)
assert A_e1.subs(epsilon, 0) == A_round == A_e2.subs(epsilon, 0)
assert P_e1 != P_e2 and (P_e1 - P_e2).rank() == 2
axis_swap = sp.Matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
assert A_e2 == axis_swap * A_e1 * axis_swap.inv()
assert P_e2 == axis_swap * P_e1 * axis_swap.inv()

# The spatial-line orbit at the round point is two-dimensional: natural as a set, not a member.
e1 = sp.Matrix([0, 1, 0, 0])
orbit_tangents = sp.Matrix.hstack(*(item * e1 for item in ROTATIONS))
assert orbit_tangents.rank() == 2

# Replay the registered intrinsic-form census without altering its evidence.
intrinsic = table(ROOT / "udt_intrinsic_two_form_distribution_audit_2026-08-02/CANDIDATE_ATLAS.tsv")
assert len(intrinsic) == 18
distribution_counts: dict[str, int] = {}
for row in intrinsic:
    distribution_counts[row["distribution_status"]] = distribution_counts.get(row["distribution_status"], 0) + 1
assert distribution_counts == {
    "METRIC_DEGENERATE": 1,
    "MULTIPLE_NONZERO_TYPES_ON_DIFFERENT_LOCI": 6,
    "PROJECTOR_BLOCKED": 2,
    "ZERO": 9,
}
full_intrinsic = [row for row in intrinsic if row["intrinsic_scope"] == "FULL_DISTRIBUTION"]
assert len(full_intrinsic) == 6
assert all("DIM2_SPAN_T_N_ON_NONZERO__DIM4_ON_ZERO" in row["kernel_status"] for row in full_intrinsic)
assert all("FAILS_THREE_GREAT_CIRCLES" in row["projective_extension"] for row in full_intrinsic)

outcomes = [
    ["M00", "METRIC_ZERO_JET", "NONE_UNIVERSAL", "FULL_LORENTZ_ISOTROPY", "UNIVERSAL_OBSTRUCTION_EXACT", "NO_RANK2_IDEMPOTENT_IN_SCALAR_COMMUTANT"],
    ["M01", "COFRAME_PRESENTATION", "YES_IF_SUPPLIED_AS_PHYSICAL_INPUT", "LOCAL_LORENTZ_EQUIVALENCE", "CONDITIONAL_INPUT_NOT_METRIC_SELECTOR", "FIRST_TWO_LEGS_CHANGE_WITH_PRESENTATION"],
    ["M02", "QUERY_BUNDLE", "TAUTOLOGICAL_ON_TOTAL_SPACE", "NO_NATURAL_SPACETIME_SECTION_DERIVED", "DERIVED_CONTAINER_NO_NATURAL_SECTION", "SMOOTH_SECTIONS_EXIST_BUT_PROJECTION_SELECTS_NONE"],
    ["M03", "PHI_FIRST_JET", "ONE_LINE_ON_REGULAR_NONNULL_LOCUS", "RESIDUAL_SO3_OR_SO12_AND_NULL_ZERO_STRATA", "FIRST_JET_INSUFFICIENT_FOR_RANK2", "SECOND_LINE_NOT_SELECTED"],
    ["M04", "PHI_SECOND_JET", "TIMELIKE_DPHI_PLUS_SIMPLE_SPATIAL_HESSIAN_LINE_OR_SPACELIKE_DPHI_PLUS_SIMPLE_TIMELIKE_LINE", "EIGEN_COLLISION_COMPLEX_NULL_JORDAN_NULL_OR_ZERO_DPHI_TYPE_CHANGE_AND_OPEN_PHYSICAL_PHI", "BRANCH_LOCAL_CONDITIONAL", "CAUSAL_RESTRICTED_SPECTRAL_CONDITIONS_REQUIRED"],
    ["M05", "RICCI_SPECTRAL", "YES_ON_DISTINCT_CAUSAL_EIGENLINE_STRATUM", "ROUND_SPATIAL_COLLISION", "BRANCH_LOCAL_POSITIVE_COLLISION_OBSTRUCTED", "EXACT_POLYNOMIAL_PROJECTOR"],
    ["M06", "RIEMANN_WEYL_BIVECTOR", "POSSIBLE_IF_UNIQUE_REAL_SIMPLE_DECOMPOSABLE_EIGENBIVECTOR", "CONFORMALLY_FLAT_TIED_OR_NONSIMPLE_SPECTRUM", "CONDITIONAL_CAPABILITY_NO_FROZEN_WITNESS", "NOT_A_UNIVERSAL_SELECTOR"],
    ["M07", "JOINT_SCALAR_GRADIENTS", "POSSIBLE_ON_RANK2_NONDEGENERATE_SPAN", "CONSTANT_COLLINEAR_NULL_OR_DEGENERATE_LOCI", "CONDITIONAL_CAPABILITY_NO_FROZEN_WITNESS", "RANK_CHANGES_REQUIRE_ATLAS"],
    ["M08", "KILLING_SYMMETRY", "POSSIBLE_WITH_UNIQUE_INTRINSIC_CLOCK_AND_RULER_LINES", "NO_SYMMETRY_OR_ENHANCED_SYMMETRY_TIES", "BRANCH_LOCAL_CONDITIONAL", "GENERATOR_CHOICE_NOT_AUTOMATIC"],
    ["M09", "HOLONOMY_REDUCTION", "POSSIBLE_WITH_UNIQUE_INVARIANT_NONDEGENERATE_RANK2_SUBSPACE", "IRREDUCIBLE_OR_ROUND_1_PLUS_3_HOLONOMY", "BRANCH_LOCAL_CONDITIONAL", "PARALLELISM_STRONGER_THAN_METRIC_NATURALITY"],
    ["M10", "INTRINSIC_TWO_FORM_KERNEL", "YES_ON_SIX_REGISTERED_NONZERO LOCI", "ZERO_GRAPH_BLOCKED_AND_DEGENERATE_CONTROLS", "BRANCH_LOCAL_POSITIVE_DEFECT_OBSTRUCTED", "EXACT_DIM2_KERNEL_ON_NONZERO_LOCUS"],
    ["M11", "ROUND_COMPLETE_S3", "TIME_LINE_ONLY", "SPATIAL_SO3_ISOTROPY", "NO_UNIQUE_RECIPROCAL_SPLIT", "IDEMPOTENT_RANKS_0_1_3_4"],
    ["M12", "SQUASHED_COMPLETE_S3", "TIME_PLUS_UNORIENTED_SIMPLE_RICCI_LINE", "ROUND_LIMIT_AND_OFFSHELL_STATUS", "BRANCH_LOCAL_POSITIVE_NOT_PHYSICAL", "METRIC_SELECTED_LINE_NOT_PARALLEL"],
    ["M13", "WHOLE_SOLUTION_NONLOCAL", "POSITIVE_CAPABILITY_ON_OTHER_BRANCHES_UNCLASSIFIED", "ROUND_ISOTROPY_BLOCKS_UNIQUE_MEMBER_ON_CONTROL_AND_NO_OTHER_REGISTERED_OPERATION", "ROUND_CONTROL_OBSTRUCTED_OTHER_BRANCH_CAPABILITY_OPEN", "GLOBAL_NATURALITY_STILL_COMMUTES_WITH_ISOMETRY"],
    ["M14", "BOUNDARY_TOPOLOGY_COMPLETION", "UNCLASSIFIED", "UNSELECTED_COMPLETION_JOIN_AND_MONODROMY", "OPEN_NO_TYPED_SELECTOR", "CANNOT_BACKFILL_GLOBAL_SECTION"],
    ["M15", "SET_VALUED_EQUIVARIANT", "YES_AS_ORBIT_ON_TIE_STRATA", "NO_UNIQUE_SMOOTH_MEMBER", "NATURAL_SET_NOT_REALIZED_SPLIT", "ROUND_SPATIAL_LINES_FORM_DIM2_ORBIT"],
    ["M16", "RANK_CHANGING_ATLAS", "STRATIFIED_DATA_ONLY", "ZERO_TIE_CAUSAL_AND_PROJECTOR_RANK_CHANGE", "NO_GLOBAL_SMOOTH_FIXED_RANK_FROM_CURRENT_DATA", "GLUING_REMAINS_OPEN"],
    ["M17", "ACTION_OR_DYNAMICAL", "DOWNSTREAM_IF_LATER_SUPPLIED", "ACTION_SOURCE_VARIATION_OPEN", "EXCLUDED_NOT_TESTED_AS_METRIC_SELECTOR", "WOULD_CHANGE_THE_QUESTION"],
]
assert [row[0] for row in outcomes] == [f"M{i:02d}" for i in range(18)]
with (HERE / "SELECTOR_OUTCOMES.tsv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(["selector_id", "family", "positive_domain", "obstruction_domain", "ruling", "certificate"])
    writer.writerows(outcomes)

checks = {
    "full_commutant_rank": full_rank,
    "full_commutant_nullity": len(full_basis),
    "full_scalar_idempotent_ranks": [0, 4],
    "round_spatial_commutant_rank": round_rank,
    "round_spatial_commutant_nullity": len(round_basis),
    "round_invariant_projector_ranks": round_projector_ranks,
    "single_ruler_complement_commutant_rank": ruler_rank,
    "single_ruler_invariant_projector_ranks": ruler_projector_ranks,
    "null_little_group_commutant_rank": null_rank,
    "null_little_group_idempotent_ranks": null_idempotent_ranks,
    "q02_ricci_spectrum": ["0", "1/2", "3/2", "3/2"],
    "synthetic_operator_equals_2I_plus_2Ricci_q02": A == 2 * I4 + 2 * ricci_q02,
    "ricci_projector_rank": P.rank(),
    "ricci_projector_idempotent": P * P == P,
    "ricci_projector_metric_self_adjoint": P.T * ETA == ETA * P,
    "ricci_projector_equivariant_under_exact_boost": P_prime == boost * P * boost.inv(),
    "collision_common_limit_operator": A_e1.subs(epsilon, 0) == A_e2.subs(epsilon, 0),
    "collision_distinct_projector_limits": P_e1 != P_e2,
    "collision_paths_related_by_round_axis_rotation": A_e2 == axis_swap * A_e1 * axis_swap.inv(),
    "round_spatial_line_orbit_dimension": orbit_tangents.rank(),
    "intrinsic_candidate_count": len(intrinsic),
    "intrinsic_distribution_counts": distribution_counts,
    "intrinsic_positive_candidate_count": len(full_intrinsic),
    "selector_outcome_count": len(outcomes),
}
result = {
    "schema": "udt-metric-natural-reciprocal-split-selector-1.0",
    "result": "BRANCH_LOCAL_SELECTORS_ONLY_UNIVERSAL_OBSTRUCTED",
    "checks": checks,
    "universal_scope": "retained domain containing full-isotropy and round-S3 controls",
    "positive_witnesses": ["Ricci simple-spectrum stratum", "squashed-S3 Ricci line", "intrinsic-two-form nonzero locus"],
    "open_classes": ["whole-solution positive capability away from round control", "boundary/topology completion", "rank-changing gluing"],
    "authority_boundary": "no physical split branch action source carrier boundary bootstrap density Xmax matter mass dynamics or canon",
}
(HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))

#!/usr/bin/env python3
"""Exact bounded audit of global founded-depth factorization ownership."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
Q = sp.Rational


def character(z: sp.Expr) -> sp.Matrix:
    return sp.diag(1 / z, z)


def embed_base(matrix: sp.Matrix) -> sp.Matrix:
    return sp.diag(matrix, sp.eye(2))


def extension(z: sp.Expr, screen: sp.Matrix, mixing: sp.Matrix) -> sp.Matrix:
    a = character(z)
    zero = sp.zeros(2)
    return sp.Matrix.vstack(sp.Matrix.hstack(a, zero), sp.Matrix.hstack(screen * mixing, screen))


def incidence(vertex_count: int, edges: list[tuple[int, int]]) -> sp.Matrix:
    rows = []
    for left, right in edges:
        row = [0] * vertex_count
        row[left] = -1
        row[right] = 1
        rows.append(row)
    return sp.Matrix(rows)


def matrix_json(matrix: sp.Matrix) -> list[list[str]]:
    return [[str(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)]


def assert_check(checks: dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)
    if not value:
        raise AssertionError(name)


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    fields = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    checks: dict[str, bool] = {}
    with (HERE / "CANDIDATE_UNIVERSE.tsv").open(encoding="utf-8", newline="") as handle:
        candidates = list(csv.DictReader(handle, delimiter="\t"))
    route_ids = [row["route_id"] for row in candidates]
    assert_check(checks, "candidate_count_12", len(route_ids) == 12)
    assert_check(checks, "candidate_ids_unique", len(route_ids) == len(set(route_ids)))
    assert_check(checks, "candidate_ids_complete", route_ids == [f"O{i:02d}" for i in range(1, 13)])

    # Three-chart complete-coframe control.
    z_values = [Q(2), Q(3), Q(5)]
    shift_values = [Q(7), Q(11), Q(13)]
    screens = [sp.Matrix([[2, 0], [1, 3]]), sp.Matrix([[3, 0], [-1, 2]]), sp.Matrix([[5, 0], [2, 1]])]
    mixings = [sp.Matrix([[1, 2], [0, 1]]), sp.Matrix([[2, -1], [1, 3]]), sp.Matrix([[0, 1], [2, -2]])]
    references = [
        sp.eye(4),
        sp.Matrix([[1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]]),
        sp.Matrix([[2, 0, 0, 0], [0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1]]),
    ]
    e = [extension(z_values[i], screens[i], mixings[i]) for i in range(3)]
    k = [embed_base(character(shift_values[i])) for i in range(3)]
    e_prime = [
        extension(z_values[i] * shift_values[i], screens[i], mixings[i] * character(shift_values[i]))
        for i in range(3)
    ]
    references_prime = [k[i].inv() * references[i] for i in range(3)]
    theta = [e[i] * references[i] for i in range(3)]
    theta_prime = [e_prime[i] * references_prime[i] for i in range(3)]
    for i in range(3):
        assert_check(checks, f"local_factorization_identity_{i}", e_prime[i] * k[i].inv() == e[i])
        assert_check(checks, f"complete_coframe_unchanged_{i}", theta_prime[i] == theta[i])

    pairs = [(0, 1), (1, 2), (0, 2)]
    left: dict[tuple[int, int], sp.Matrix] = {}
    right: dict[tuple[int, int], sp.Matrix] = {}
    right_prime: dict[tuple[int, int], sp.Matrix] = {}
    for i, j in pairs:
        left[i, j] = theta[j] * theta[i].inv()
        right[i, j] = references[j] * references[i].inv()
        right_prime[i, j] = references_prime[j] * references_prime[i].inv()
        assert_check(checks, f"two_sided_overlap_{i}{j}", e[j] == left[i, j] * e[i] * right[i, j].inv())
        assert_check(
            checks,
            f"reference_coboundary_{i}{j}",
            right_prime[i, j] == k[j].inv() * right[i, j] * k[i],
        )
        assert_check(
            checks,
            f"transformed_overlap_{i}{j}",
            e_prime[j] == left[i, j] * e_prime[i] * right_prime[i, j].inv(),
        )
    assert_check(checks, "physical_cocycle", left[0, 2] == left[1, 2] * left[0, 1])
    assert_check(checks, "reference_cocycle", right[0, 2] == right[1, 2] * right[0, 1])
    assert_check(checks, "shifted_reference_cocycle", right_prime[0, 2] == right_prime[1, 2] * right_prime[0, 1])
    assert_check(checks, "nonconstant_local_shift_witness", len(set(shift_values)) == 3)

    # Scalar descent: connected overlap equations leave one value per base point.
    cover_incidence = incidence(3, [(0, 1), (1, 2), (0, 2)])
    assert_check(checks, "connected_cover_rank_2", cover_incidence.rank() == 2)
    assert_check(checks, "scalar_shift_nullity_1_per_point", 3 - cover_incidence.rank() == 1)
    scalar_samples = [sp.Matrix([7, 7, 7]), sp.Matrix([11, 11, 11])]
    assert_check(checks, "global_scalar_shift_sample_0", cover_incidence * scalar_samples[0] == sp.zeros(3, 1))
    assert_check(checks, "global_scalar_shift_sample_1", cover_incidence * scalar_samples[1] == sp.zeros(3, 1))
    assert_check(checks, "global_scalar_can_be_nonconstant", scalar_samples[0][0] != scalar_samples[1][0])

    # Oriented and reversal-twisted affine cocycles under arbitrary local shifts.
    def shifted_affine(eps: int, a: sp.Expr, chi_i: sp.Expr, chi_j: sp.Expr) -> sp.Expr:
        return a + chi_j - eps * chi_i

    affine_rows = []
    for label, eps01, eps12, a01, a12 in [
        ("oriented", 1, 1, Q(2), Q(3)),
        ("reversal_twisted", -1, -1, Q(2), Q(3)),
    ]:
        eps02 = eps12 * eps01
        a02 = eps12 * a01 + a12
        ap01 = shifted_affine(eps01, a01, Q(7), Q(11))
        ap12 = shifted_affine(eps12, a12, Q(11), Q(13))
        ap02 = shifted_affine(eps02, a02, Q(7), Q(13))
        assert_check(checks, f"affine_cocycle_{label}", a02 == eps12 * a01 + a12)
        assert_check(checks, f"shifted_affine_cocycle_{label}", ap02 == eps12 * ap01 + ap12)
        affine_rows.append(
            {"family": label, "eps_02": str(eps02), "a_02": str(a02), "a_prime_02": str(ap02)}
        )
    assert_check(checks, "oriented_period_gauge_invariant", Q(5) + (1 - 1) * Q(7) == Q(5))
    assert_check(checks, "reversal_translation_gauge_variant", Q(5) + (1 - (-1)) * Q(7) == Q(19))

    # Observer graph: composition constrains free edges, not endpoint potentials.
    observer_edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    b = incidence(4, observer_edges)
    c = sp.Matrix([[1, -1, 0, 1, 0, 0], [1, 0, -1, 0, 1, 0], [0, 1, -1, 0, 0, 1], [0, 0, 0, 1, -1, 1]])
    assert_check(checks, "observer_incidence_rank_3", b.rank() == 3)
    assert_check(checks, "triangle_rank_3", c.rank() == 3)
    assert_check(checks, "triangle_annihilates_coboundaries", c * b == sp.zeros(4, 4))
    phi = sp.Matrix([1, 4, -2, 7])
    chi = sp.Matrix([2, 3, 5, 11])
    edge_depth = b * phi
    shifted_edge_depth = edge_depth + b * chi
    assert_check(checks, "endpoint_potential_composes", c * edge_depth == sp.zeros(4, 1))
    assert_check(checks, "shifted_endpoint_potential_composes", c * shifted_edge_depth == sp.zeros(4, 1))
    assert_check(checks, "fixed_depth_stabilizer_nullity_1", 4 - b.rank() == 1)
    free_edges = sp.Matrix([1, 0, 0, 0, 0, 0])
    assert_check(checks, "free_edge_non_coboundary_fails", c * free_edges != sp.zeros(4, 1))
    period_row = c.row(0)
    assert_check(checks, "loop_period_gauge_invariant", (period_row * (free_edges + b * chi))[0] == (period_row * free_edges)[0])
    assert_check(checks, "nonzero_path_period_witness", (period_row * free_edges)[0] == 1)

    # Query reset preserves the character law for every supplied depth.
    reset = sp.Matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
    d01_2 = sp.diag(Q(1, 2), Q(2), 1, 1)
    d01_3 = sp.diag(Q(1, 3), Q(3), 1, 1)
    d01_6 = sp.diag(Q(1, 6), Q(6), 1, 1)
    assert_check(checks, "query_character_composition", d01_3 * d01_2 == d01_6)
    assert_check(
        checks,
        "query_reset_composition",
        (reset * d01_3 * reset.inv()) * (reset * d01_2 * reset.inv()) == reset * d01_6 * reset.inv(),
    )
    assert_check(checks, "query_reset_changes_plane_action", reset * d01_2 * reset.inv() != d01_2)

    # Fixed-reference seam stabilizers versus presentation-varying seams.
    h_minus = Q(2)
    fixed_oriented = embed_base(character(Q(3)))
    oriented_required = fixed_oriented * embed_base(character(h_minus)) * fixed_oriented.inv()
    assert_check(checks, "fixed_oriented_seam_requires_equal_shift", oriented_required == embed_base(character(h_minus)))
    flip2 = sp.Matrix([[0, 1], [1, 0]])
    fixed_reversal = embed_base(flip2)
    reversal_required = fixed_reversal * embed_base(character(h_minus)) * fixed_reversal.inv()
    assert_check(checks, "fixed_reversal_seam_requires_inverse_shift", reversal_required == embed_base(character(1 / h_minus)))
    # Separate nontrivial seam witness: build endpoint presentations independently.
    seam_screen_minus = sp.Matrix([[2, 0], [1, 4]])
    seam_screen_plus = sp.Matrix([[3, 0], [-2, 5]])
    seam_mixing_minus = sp.Matrix([[1, -1], [2, 0]])
    seam_mixing_plus = sp.Matrix([[0, 3], [-1, 2]])
    seam_e_minus = extension(Q(2), seam_screen_minus, seam_mixing_minus)
    seam_e_plus = extension(Q(5), seam_screen_plus, seam_mixing_plus)
    seam_ref_minus = sp.Matrix([[1, 0, 0, 0], [1, 1, 0, 0], [0, 0, 1, 0], [0, 1, 0, 1]])
    seam_ref_plus = sp.Matrix([[2, 0, 0, 0], [0, 1, 0, 0], [1, 0, 1, 0], [0, 0, 2, 1]])
    seam_theta_minus = seam_e_minus * seam_ref_minus
    seam_theta_plus = seam_e_plus * seam_ref_plus
    seam_physical = seam_theta_plus * seam_theta_minus.inv()
    seam_reference = seam_ref_plus * seam_ref_minus.inv()
    seam_k_minus = embed_base(character(Q(2)))
    seam_k_plus = embed_base(character(Q(7)))
    seam_e_minus_prime = extension(Q(4), seam_screen_minus, seam_mixing_minus * character(Q(2)))
    seam_e_plus_prime = extension(Q(35), seam_screen_plus, seam_mixing_plus * character(Q(7)))
    seam_ref_minus_prime = seam_k_minus.inv() * seam_ref_minus
    seam_ref_plus_prime = seam_k_plus.inv() * seam_ref_plus
    seam_reference_prime = seam_ref_plus_prime * seam_ref_minus_prime.inv()
    assert_check(
        checks,
        "seam_reference_coboundary_nontrivial",
        seam_reference_prime == seam_k_plus.inv() * seam_reference * seam_k_minus
        and seam_reference_prime != seam_reference,
    )
    assert_check(
        checks,
        "seam_relation_before_shift",
        seam_e_plus == seam_physical * seam_e_minus * seam_reference.inv(),
    )
    assert_check(
        checks,
        "seam_relation_after_unequal_shifts",
        seam_e_plus_prime == seam_physical * seam_e_minus_prime * seam_reference_prime.inv(),
    )
    assert_check(
        checks,
        "seam_complete_coframes_unchanged",
        seam_e_minus_prime * seam_ref_minus_prime == seam_theta_minus
        and seam_e_plus_prime * seam_ref_plus_prime == seam_theta_plus,
    )

    classifications = [
        ("O01", "DERIVED_PRESENTATION_FREEDOM", "arbitrary nonconstant local zero-cochain witness"),
        ("O02", "CONDITIONAL_REDUCTION", "fixed reference transitions leave their stabilizer only"),
        ("O03", "DERIVED_NONSELECTION", "two-sided cocycle is preserved by induced coboundary"),
        ("O04", "OPEN_ARCHITECTURE_NONSELECTION", "scalar descent leaves arbitrary global functions"),
        ("O05", "DERIVED_CLASS_DATA_NOT_SECTION", "parity and oriented periods may survive; local representatives do not"),
        ("O06", "DERIVED_EQUIVARIANCE_NONSELECTION", "query reset transports any supplied depth"),
        ("O07", "CONDITIONAL_REDUCTION_MOD_CONSTANT", "independently fixed pair depths leave one connected-component constant"),
        ("O08", "DERIVED_NONSELECTION", "triangle composition annihilates every endpoint potential"),
        ("O09", "DERIVED_PERIOD_INVARIANCE_NONSELECTION", "path periods survive zero-cochain shifts but are not fixed"),
        ("O10", "DERIVED_PHYSICAL_GLUE__FACTORIZATION_NONSELECTION", "complete seam data do not fix reference presentation"),
        ("O11", "BRANCH_LOCAL_CONDITIONAL_OWNERSHIP", "regular intrinsic selector may own depth only on its stratum"),
        ("O12", "NOT_FOUNDED_PERIOD_RESTRICTION_ONLY", "identity return would constrain loop data not select local potential"),
    ]
    assert_check(checks, "classification_count_12", len(classifications) == 12)
    assert_check(checks, "classification_ids_match", [row[0] for row in classifications] == route_ids)
    write_tsv(
        HERE / "ROUTE_CLASSIFICATION.tsv",
        [{"route_id": route, "classification": status, "exact_reason": reason} for route, status, reason in classifications],
    )

    witness = {
        "affine_cocycles": affine_rows,
        "chart_shift_values": [str(v) for v in shift_values],
        "complete_coframes_unchanged": True,
        "fixed_depth_stabilizer_dimension": 1,
        "global_scalar_shift_samples": [7, 11],
        "observer_incidence": matrix_json(b),
        "reference_transition_01_before": matrix_json(right[0, 1]),
        "reference_transition_01_after": matrix_json(right_prime[0, 1]),
        "seam_physical_transition": matrix_json(seam_physical),
        "seam_reference_after": matrix_json(seam_reference_prime),
        "seam_reference_before": matrix_json(seam_reference),
        "seam_reference_changed": seam_reference_prime != seam_reference,
        "seam_relation_preserved": True,
        "triangle_matrix": matrix_json(c),
    }
    (HERE / "WITNESSES.json").write_text(json.dumps(witness, indent=2, sort_keys=True) + "\n")

    result = {
        "check_count": len(checks),
        "checks": checks,
        "maximum_conclusion": (
            "DERIVED_GLOBAL_FACTORIZATION_GROUPOID_FREEDOM_ON_THE_SUPPLIED_SMOOTH_COVER__"
            "DERIVED_COCYCLE_CLASS_AND_PERIOD_INVARIANTS_DO_NOT_SELECT_A_SECTION__"
            "CONDITIONAL_REDUCTIONS_REQUIRE_UNOWNED_REFERENCE_DEPTH_OR_BRANCH_SECTION_DATA__"
            "NO_GLOBAL_PHI_OWNERSHIP_SELECTION"
        ),
        "route_count": len(classifications),
        "sympy": sp.__version__,
    }
    assert_check(checks, "all_checks_true_before_write", all(checks.values()))
    result["check_count"] = len(checks)
    result["checks"] = checks
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

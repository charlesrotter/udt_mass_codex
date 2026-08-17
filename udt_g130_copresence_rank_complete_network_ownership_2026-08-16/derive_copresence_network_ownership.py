#!/usr/bin/env python3
"""Exact G130 production derivation."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

EXPECTED_SOURCE_PATHS = {
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_MAP.md",
    "copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md",
    "copresence_causal_accessibility_selector_2026-07-19/STATUS_LEDGER.tsv",
    "udt_founding_phi_ownership_morphism_audit_2026-08-05/AUDIT_REPORT.md",
    "udt_g121_copresent_reciprocal_causal_history_consistency_2026-08-16/AUDIT_REPORT.md",
    "udt_g123_direct_copresent_incidence_relation_2026-08-16/AUDIT_REPORT.md",
    "udt_g129_copresent_relational_network_faithfulness_2026-08-16/AUDIT_REPORT.md",
}


def source_hashes_match() -> bool:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    paths = [row["path"] for row in rows]
    return (
        len(rows) == 9
        and len(set(paths)) == 9
        and set(paths) == EXPECTED_SOURCE_PATHS
        and all(
        hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"]
        for row in rows
        )
    )


def design_row(v: tuple[int, int, int, int], w: tuple[int, int, int, int]) -> list[int]:
    """Coefficients of v^T g w in the ten-component symmetric basis."""
    out: list[int] = []
    for i in range(4):
        out.append(v[i] * w[i])
    for i, j in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)):
        out.append(v[i] * w[j] + v[j] * w[i])
    return out


def restriction_matrix(rulers: list[tuple[int, int, int]]) -> sp.Matrix:
    clock = (1, 0, 0, 0)
    rows: list[list[int]] = []
    for xyz in rulers:
        ruler = (0, *xyz)
        rows.extend(
            [design_row(clock, clock), design_row(clock, ruler), design_row(ruler, ruler)]
        )
    return sp.Matrix(rows)


def scalar_curvature(metric: sp.Matrix, coords: tuple[sp.Symbol, ...]) -> sp.Expr:
    n = len(coords)
    inverse = sp.simplify(metric.inv())
    gamma = [[[
        sp.simplify(
            sp.Rational(1, 2)
            * sum(
                inverse[k, ell]
                * (
                    sp.diff(metric[ell, j], coords[i])
                    + sp.diff(metric[ell, i], coords[j])
                    - sp.diff(metric[i, j], coords[ell])
                )
                for ell in range(n)
            )
        )
        for j in range(n)] for i in range(n)] for k in range(n)]
    ricci = sp.MutableDenseMatrix.zeros(n, n)
    for i in range(n):
        for j in range(n):
            ricci[i, j] = sp.simplify(
                sum(
                    sp.diff(gamma[k][i][j], coords[k])
                    - sp.diff(gamma[k][i][k], coords[j])
                    + sum(
                        gamma[k][k][ell] * gamma[ell][i][j]
                        - gamma[k][j][ell] * gamma[ell][i][k]
                        for ell in range(n)
                    )
                    for k in range(n)
                )
            )
    return sp.simplify(sum(inverse[i, j] * ricci[i, j] for i in range(n) for j in range(n)))


def main() -> None:
    founding_results = (ROOT / "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md").read_text()
    founding_map = (ROOT / "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_MAP.md").read_text()
    copresence = (
        ROOT / "copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md"
    ).read_text()

    axial = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    complete = axial + [(1, 1, 0), (1, 0, 1), (0, 1, 1)]
    one_rank = restriction_matrix(axial[:1]).rank()
    axial_rank = restriction_matrix(axial).rank()
    complete_matrix = restriction_matrix(complete)
    complete_rank = complete_matrix.rank()

    # Universal conditional law does not imply totality of the comparison domain.
    candidates = ("q0", "q1")
    comparison_exists = {"q0": True, "q1": False}
    reciprocity_holds = {"q0": True, "q1": False}
    conditional_law = all(
        (not comparison_exists[q]) or reciprocity_holds[q] for q in candidates
    )
    domain_totality = all(comparison_exists[q] for q in candidates)

    potential_a = (sp.Rational(0), sp.Rational(1, 3), sp.Rational(2, 5))
    potential_b = (sp.Rational(0), sp.Rational(2, 3), sp.Rational(-1, 7))

    def edges(potential: tuple[sp.Rational, ...]) -> dict[tuple[int, int], sp.Rational]:
        return {
            (i, j): potential[j] - potential[i]
            for i in range(len(potential)) for j in range(len(potential))
        }

    edges_a = edges(potential_a)
    edges_b = edges(potential_b)

    def edge_laws(edge: dict[tuple[int, int], sp.Rational]) -> bool:
        return all(
            edge[i, j] == -edge[j, i]
            and edge[i, j] + edge[j, k] == edge[i, k]
            for i in range(3) for j in range(3) for k in range(3)
        )

    t, r, theta, psi = sp.symbols("t r theta psi", real=True)
    s = sp.symbols("s", positive=True)
    coords = (t, r, theta, psi)
    g_s = sp.diag(-s, 1 / s, r**2, r**2 * sp.sin(theta) ** 2)
    scalar_s = scalar_curvature(g_s, coords)
    expected_scalar = 2 * (1 - s) / r**2

    # Exact repaired countermodel: both members realize nonzero reciprocal depth.
    # s=exp(-2 phi), hence s=1/4 has phi=+log(2) and s=4 has phi=-log(2).
    scalar_positive = sp.simplify(scalar_s.subs({s: sp.Rational(1, 4), r: 1}))
    scalar_negative = sp.simplify(scalar_s.subs({s: 4, r: 1}))
    g0 = g_s.subs({s: sp.Rational(1, 4), r: 1, theta: sp.pi / 2})
    g1 = g_s.subs({s: 4, r: 1, theta: sp.pi / 2})
    h0 = sp.Matrix([[g0[0, 0], g0[0, 1]], [g0[1, 0], g0[1, 1]]])
    h1 = sp.Matrix([[g1[0, 0], g1[0, 1]], [g1[1, 0], g1[1, 1]]])

    unknown = sp.symbols("y0:10")
    fixed_metric_components = sp.Matrix(
        [sp.Rational(-4), 3, 5, 7, 1, -2, 3, 4, -1, 2]
    )
    fixed_observations = complete_matrix * fixed_metric_components
    reconstructed = sp.linsolve(
        (complete_matrix, fixed_observations), *list(unknown)
    )
    expected_solution = sp.FiniteSet(tuple(fixed_metric_components))
    left_inverse = sp.simplify(
        (complete_matrix.T * complete_matrix).inv() * complete_matrix.T
    )

    source_rows = [
        {
            "claim_id": "E01",
            "object": "copresence",
            "owned_content": "events are co-members conditional on one supplied candidate solution",
            "not_owned": "clock-ruler query plane or numerical relation value",
            "status": "WORKING_DOMAIN_MEMBERSHIP_ONLY",
        },
        {
            "claim_id": "E02",
            "object": "reciprocity",
            "owned_content": "every supplied positional comparison obeys the same reciprocal law",
            "not_owned": "existence or totality of all rank-needed comparisons",
            "status": "UNIVERSAL_CONDITIONAL_LAW_SCHEMA",
        },
        {
            "claim_id": "E03",
            "object": "ordered_depth",
            "owned_content": "D(delta) after delta is supplied",
            "not_owned": "realized delta field or complete pair values",
            "status": "SUPPLIED_INPUT",
        },
        {
            "claim_id": "E04",
            "object": "all_plane_completion",
            "owned_content": "rank-ten coverage if all admissible planes are declared",
            "not_owned": "direct founding entailment of that declared family",
            "status": "CONDITIONAL_METRIC_NATURAL_COMPLETION",
        },
        {
            "claim_id": "E05",
            "object": "relation_first_history",
            "owned_content": "rank-complete compatible pair values are equivalent to one metric",
            "not_owned": "which numerical values Nature realizes",
            "status": "DERIVED_REPRESENTATION_EQUIVALENCE",
        },
    ]
    with (HERE / "SOURCE_ENTAILMENT.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=source_rows[0].keys(), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(source_rows)

    checks = {
        "source_hashes_match": source_hashes_match(),
        "lexical_anchor_founding_relative_depth_is_input": "at relative depth" in founding_results,
        "lexical_anchor_founding_profile_explicitly_open": "does not yet derive a unique action, the profile" in founding_results,
        "lexical_anchor_every_comparison_wording_present": "respected by every positional comparison" in founding_map,
        "lexical_anchor_copresence_is_event_domain_membership": "p,q\\in M_S=\\operatorname{dom}(S)" in copresence,
        "conditional_law_does_not_imply_domain_totality": conditional_law and not domain_totality,
        "composition_allows_distinct_complete_depth_networks": (
            edge_laws(edges_a) and edge_laws(edges_b) and edges_a != edges_b
        ),
        "one_plane_rank_three": one_rank == 3,
        "axial_rank_seven": axial_rank == 7,
        "all_plane_family_contains_rank_ten_witness": complete_rank == 10,
        "rank_ten_fixed_values_reconstruct_metric_and_left_inverse": (
            reconstructed == expected_solution
            and sp.simplify(left_inverse * complete_matrix) == sp.eye(10)
        ),
        "countermodels_same_domain_and_exact_lorentz_signature": (
            g0[0, 0] < 0 and all(g0[i, i] > 0 for i in range(1, 4))
            and g1[0, 0] < 0 and all(g1[i, i] > 0 for i in range(1, 4))
        ),
        "countermodels_both_reciprocal_clock_ruler_determinant": h0.det() == -1 and h1.det() == -1,
        "countermodel_pair_values_differ": h0 != h1,
        "scalar_curvature_formula": sp.simplify(scalar_s - expected_scalar) == 0,
        "positive_depth_member_scalar_three_halves": scalar_positive == sp.Rational(3, 2),
        "negative_depth_member_scalar_minus_six": scalar_negative == -6,
        "two_nontrivial_foundational_members_are_nonisometric": scalar_positive != scalar_negative,
    }
    checks = {name: bool(value) for name, value in checks.items()}
    if not all(checks.values()):
        failed = [name for name, value in checks.items() if not value]
        raise SystemExit(f"failed checks: {failed}")

    result = {
        "status": "PASS",
        "landing": "COPRESENCE_DENOTES_EVENT_COMEMBERSHIP_IN_SUPPLIED_S__RECIPROCITY_OWNS_LAW_SCHEMA__RANK_COMPLETE_NETWORK_VALUES_OPEN",
        "checks": checks,
        "production_check_count": len(checks),
        "one_plane_rank": one_rank,
        "axial_rank": axial_rank,
        "rank_complete_witness": complete_rank,
        "scalar_curvature_family": str(scalar_s),
        "registered_scalar_s_quarter_at_r1": str(scalar_positive),
        "registered_scalar_s_four_at_r1": str(scalar_negative),
        "maximum_conclusion": (
            "Co-presence denotes event co-membership conditional on supplied S, and Reciprocity owns the common law "
            "schema on supplied comparisons. Declaring all admissible clock-ruler planes makes the "
            "query domain rank complete, and compatible rank-complete pair values are equivalent to "
            "one Lorentz metric. The active founding sources do not supply those numerical values: "
            "two nontrivial nonisometric reciprocal metrics satisfy the same conditional membership and law statements."
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

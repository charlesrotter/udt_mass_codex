#!/usr/bin/env python3
"""Exact G235 production derivation. Writes only registered package outputs."""

from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent


def bilinear_row(u: sp.Matrix, v: sp.Matrix) -> list[sp.Expr]:
    """Coefficients of u^T g v in the symmetric 4x4 component basis."""
    return [
        u[0] * v[0],
        u[0] * v[1] + u[1] * v[0],
        u[0] * v[2] + u[2] * v[0],
        u[0] * v[3] + u[3] * v[0],
        u[1] * v[1],
        u[1] * v[2] + u[2] * v[1],
        u[1] * v[3] + u[3] * v[1],
        u[2] * v[2],
        u[2] * v[3] + u[3] * v[2],
        u[3] * v[3],
    ]


def compute() -> tuple[dict[str, object], str]:
    e0 = sp.Matrix([1, 0, 0, 0])
    e1 = sp.Matrix([0, 1, 0, 0])
    e2 = sp.Matrix([0, 0, 1, 0])
    e3 = sp.Matrix([0, 0, 0, 1])
    rulers = [e1, e2, e3, e1 + e2, e1 + e3, e2 + e3]
    design = sp.Matrix(
        [row for v in rulers for row in (bilinear_row(e0, e0), bilinear_row(e0, v), bilinear_row(v, v))]
    )

    T, L, beta = sp.symbols("T L beta", positive=True, real=True)
    h = sp.Matrix(
        [
            [-T**2, -T**2 * beta],
            [-T**2 * beta, L**2 - T**2 * beta**2],
        ]
    )
    m = T * L
    J = sp.diag(1, m)
    h_s = sp.simplify(J.inv().T * h * J.inv())
    reconstructed_h = sp.simplify(J.T * h_s * J)

    p0, p1, p2 = sp.symbols("p0 p1 p2", real=True)
    edge = lambda a, b: sp.expand(b - a)
    triangle = sp.simplify(edge(p0, p1) + edge(p1, p2) - edge(p0, p2))
    reversal = sp.simplify(edge(p0, p1) + edge(p1, p0))

    s, b = sp.symbols("s b", real=True)
    phi = s**3 + 2 * s**4 + b * s**5
    phi_0 = phi.subs(b, 0)
    phi_7 = phi.subs(b, 7)
    jet_differences = [sp.diff(phi_7 - phi_0, s, order).subs(s, 0) for order in range(6)]
    invariant_separator = sp.simplify(sp.Rational(240) * 7 / sp.Integer(3) ** 5)

    sa, sb, sc = sp.symbols("sa sb sc", real=True)

    def primary_network_evidence(b_value: int) -> dict[str, bool]:
        profile = phi.subs(b, b_value)
        radius = 3 * (1 + s)
        clock_sq = sp.exp(-2 * profile)
        spatial = sp.diag(sp.exp(2 * profile), radius**2, radius**2)
        pair_checks = []
        clock_entries = []
        for ruler in rulers:
            spatial_ruler = ruler[1:, :]
            ruler_sq = sp.expand((spatial_ruler.T * spatial * spatial_ruler)[0])
            pair_h00 = -clock_sq
            clock_entries.append(pair_h00)
            m_sq = sp.expand(clock_sq * ruler_sq)
            completed_spatial = sp.simplify(ruler_sq / m_sq)
            pair_checks.extend(
                [
                    sp.simplify((-clock_sq) * completed_spatial + 1) == 0,
                    sp.simplify(completed_spatial - sp.exp(2 * profile)) == 0,
                ]
            )
        pa, pb, pc = (sp.expand(profile.subs(s, node)) for node in (sa, sb, sc))
        edge_closure = sp.simplify((pb - pa) + (pc - pb) - (pc - pa)) == 0
        common_clock = all(sp.simplify(entry - clock_entries[0]) == 0 for entry in clock_entries[1:])
        return {
            "six_pair_completions": all(pair_checks),
            "six_constructed_h00_entries_match": common_clock,
            "edge_closure": edge_closure,
            "network_pass": all(pair_checks) and common_clock and edge_closure and design.rank() == 10,
        }

    seed_evidence = primary_network_evidence(0)
    control_evidence = primary_network_evidence(7)
    seed_network_passes = seed_evidence["network_pass"]
    control_network_passes = control_evidence["network_pass"]
    candidate_rejects_control = seed_network_passes and not control_network_passes
    five_ruler_design = sp.Matrix(
        [row for v in rulers[:5] for row in (bilinear_row(e0, e0), bilinear_row(e0, v), bilinear_row(v, v))]
    )
    corrupted_edge_defect = sp.simplify(edge(p0, p1) + edge(p1, p2) - (edge(p0, p2) + 1))

    theta, radius_symbol = sp.symbols("theta radius_symbol", real=True, positive=True)
    screen_north = sp.diag(radius_symbol**2, radius_symbol**2 * sp.sin(theta) ** 2)
    north_to_south = sp.diag(1, -1)
    screen_south = sp.simplify(north_to_south.T * screen_north * north_to_south)
    screen_recovered = sp.simplify(north_to_south.inv().T * screen_south * north_to_south.inv())

    checks = {
        "six_plane_design_rank_ten": design.rank() == 10,
        "six_plane_design_kernel_zero": len(design.nullspace()) == 0,
        "common_clock_entry_independent_of_ruler": (
            seed_evidence["six_constructed_h00_entries_match"]
            and control_evidence["six_constructed_h00_entries_match"]
        ),
        "generic_pair_determinant": sp.simplify(h.det() + T**2 * L**2) == 0,
        "completed_pair_determinant_minus_one": sp.simplify(h_s.det() + 1) == 0,
        "completed_tuple_reconstructs_full_pullback": reconstructed_h == h,
        "completed_depth_depends_only_on_common_clock": sp.simplify(h_s[0, 0] + T**2) == 0,
        "matched_depth_triangle_telescopes": triangle == 0,
        "matched_depth_reversal": reversal == 0,
        "twins_share_profile_jets_zero_through_four": all(value == 0 for value in jet_differences[:5]),
        "twins_differ_at_profile_fifth_jet": jet_differences[5] == 840,
        "g233_invariant_separator_is_560_over_81": invariant_separator == sp.Rational(560, 81),
        "seed_network_passes_structural_condition": seed_network_passes,
        "b7_network_passes_structural_condition": control_network_passes,
        "five_ruler_mutation_drops_rank": five_ruler_design.rank() < 10,
        "corrupted_edge_mutation_breaks_composition": corrupted_edge_defect != 0,
        "two_chart_screen_overlap_recovers_metric": screen_south == screen_north
        and screen_recovered == screen_north,
        "candidate_rejects_preregistered_b7_control": candidate_rejects_control,
    }

    landing = (
        "RANK_COMPLETE_MATCHED_COMPLETION_IS_RECONSTRUCTIVE_NOT_SELECTIVE"
        "__EXISTENCE_CONDITION_ACCEPTS_G233_INVARIANT_TWINS"
        "__NO_CANDIDATE"
    )
    result = {
        "landing": landing,
        "all_positive_checks_pass": all(value for key, value in checks.items() if key != "candidate_rejects_preregistered_b7_control"),
        "candidate_nonidentity_gate_passes": checks["candidate_rejects_preregistered_b7_control"],
        "design_shape": list(design.shape),
        "design_rank": design.rank(),
        "profile_jet_differences_orders_0_to_5": [str(value) for value in jet_differences],
        "g233_invariant_separator": str(invariant_separator),
        "profile_network_evidence": {"0": seed_evidence, "7": control_evidence},
        "checks": checks,
        "maximum_conclusion": (
            "Existence of one smooth compatible rank-complete matched-incidence network of typed "
            "G176-completed pairs is reconstructive, not a nonidentity metric/profile selector, "
            "on the declared regular covered arena."
        ),
    }
    atlas_buffer = io.StringIO()
    writer = csv.writer(atlas_buffer, delimiter="\t", lineterminator="\n")
    writer.writerow(
        [
            "member",
            "b",
            "shared_jets_0_to_4",
            "invariant_separator_from_seed",
            "rank",
            "completion",
            "matched_composition",
            "candidate_verdict",
        ]
    )
    writer.writerow(["seed", "0", "YES", "0", "10", "PASS", "PASS", "ACCEPTED"])
    writer.writerow(["control", "7", "YES", "560/81", "10", "PASS", "PASS", "ACCEPTED_NOT_REJECTED"])
    return result, atlas_buffer.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-write",
        action="store_true",
        help="recompute and print the result without changing frozen package artifacts",
    )
    args = parser.parse_args()
    result, atlas = compute()
    if not args.no_write:
        (ROOT / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        (ROOT / "NETWORK_TWIN_ATLAS.tsv").write_text(atlas, encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

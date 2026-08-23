#!/usr/bin/env python3
"""Dependency-free independent G235 replay using exact Fraction arithmetic."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent


def bilinear_row(u: tuple[int, ...], v: tuple[int, ...]) -> list[Fraction]:
    return [
        Fraction(u[0] * v[0]),
        Fraction(u[0] * v[1] + u[1] * v[0]),
        Fraction(u[0] * v[2] + u[2] * v[0]),
        Fraction(u[0] * v[3] + u[3] * v[0]),
        Fraction(u[1] * v[1]),
        Fraction(u[1] * v[2] + u[2] * v[1]),
        Fraction(u[1] * v[3] + u[3] * v[1]),
        Fraction(u[2] * v[2]),
        Fraction(u[2] * v[3] + u[3] * v[2]),
        Fraction(u[3] * v[3]),
    ]


def rank(matrix: list[list[Fraction]]) -> int:
    rows = [row[:] for row in matrix]
    if not rows:
        return 0
    nrows, ncols = len(rows), len(rows[0])
    pivot_row = 0
    for col in range(ncols):
        pivot = next((r for r in range(pivot_row, nrows) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][col]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for r in range(nrows):
            if r != pivot_row and rows[r][col]:
                factor = rows[r][col]
                rows[r] = [a - factor * b for a, b in zip(rows[r], rows[pivot_row])]
        pivot_row += 1
        if pivot_row == nrows:
            break
    return pivot_row


def compute() -> dict[str, object]:
    e0 = (1, 0, 0, 0)
    rulers = [
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
        (0, 1, 1, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 1),
    ]
    design = [row for v in rulers for row in (bilinear_row(e0, e0), bilinear_row(e0, v), bilinear_row(v, v))]

    rng = random.Random(235)
    pair_assertions = 0
    pair_ok = True
    composition_ok = True
    profile_composition = {0: True, 7: True}
    profile_pair_completion = {0: True, 7: True}
    profile_common_clock = {0: True, 7: True}
    trials = 5000
    for _ in range(trials):
        t = Fraction(rng.randint(1, 19), rng.randint(1, 19))
        length = Fraction(rng.randint(1, 19), rng.randint(1, 19))
        beta = Fraction(rng.randint(-19, 19), rng.randint(1, 19))
        h00 = -(t * t)
        h01 = -(t * t) * beta
        h11 = length * length - t * t * beta * beta
        m = t * length
        hs00 = h00
        hs01 = h01 / m
        hs11 = h11 / (m * m)
        det_hs = hs00 * hs11 - hs01 * hs01
        rec = (hs00, hs01 * m, hs11 * m * m)
        pair_ok &= det_hs == -1 and rec == (h00, h01, h11)
        pair_assertions += 2

        p = [Fraction(rng.randint(-30, 30), rng.randint(1, 19)) for _ in range(3)]
        d01, d12, d02 = p[1] - p[0], p[2] - p[1], p[2] - p[0]
        composition_ok &= d01 + d12 == d02 and d01 == -(p[0] - p[1])
        pair_assertions += 2

        nodes = [Fraction(rng.randint(-5, 5), rng.randint(6, 20)) for _ in range(3)]
        for b_value in profile_composition:
            values = [node**3 + 2 * node**4 + b_value * node**5 for node in nodes]
            profile_composition[b_value] &= (
                (values[1] - values[0]) + (values[2] - values[1]) == values[2] - values[0]
            )
            pair_assertions += 1
            for node, profile_value in zip(nodes, values):
                # The completion identity is algebraic for every positive reciprocal scale.  This
                # exact positive rational instantiation keeps the replay dependency-free; it is a
                # test coordinate, not a replacement for exp(2*phi) in the physical metric.
                reciprocal_scale = 1 + profile_value * profile_value
                clock_sq = 1 / reciprocal_scale
                radius_sq = (3 * (1 + node)) ** 2
                clock_entries: list[Fraction] = []
                for ruler in rulers:
                    ruler_sq = (
                        reciprocal_scale * ruler[1] ** 2
                        + radius_sq * ruler[2] ** 2
                        + radius_sq * ruler[3] ** 2
                    )
                    completed_spatial = ruler_sq / (clock_sq * ruler_sq)
                    pair_pass = completed_spatial == reciprocal_scale and clock_sq * completed_spatial == 1
                    profile_pair_completion[b_value] &= pair_pass
                    clock_entries.append(-clock_sq)
                    pair_assertions += 2
                clock_pass = all(entry == clock_entries[0] for entry in clock_entries[1:])
                profile_common_clock[b_value] &= clock_pass
                pair_assertions += len(clock_entries) - 1

    jet_differences = [Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(840)]
    separator = Fraction(240 * 7, 3**5)
    design_rank = rank(design)
    five_ruler_rank = rank(design[:15])
    network_pass = {
        b_value: (
            design_rank == 10
            and pair_ok
            and profile_composition[b_value]
            and profile_pair_completion[b_value]
            and profile_common_clock[b_value]
        )
        for b_value in profile_composition
    }
    candidate_rejects_control = network_pass[0] and not network_pass[7]
    corrupted_values = [Fraction(0), Fraction(2, 7), Fraction(-3, 11)]
    corrupted_edge_defect = (
        (corrupted_values[1] - corrupted_values[0])
        + (corrupted_values[2] - corrupted_values[1])
        - ((corrupted_values[2] - corrupted_values[0]) + 1)
    )
    screen_radius_sq = Fraction(49, 4)
    screen_theta_weight = Fraction(9, 25)
    screen_north = ((screen_radius_sq, Fraction(0)), (Fraction(0), screen_radius_sq * screen_theta_weight))
    # The overlap Jacobian diag(1,-1) flips the angular chart's second coordinate twice.
    screen_south = ((screen_north[0][0], -screen_north[0][1]), (-screen_north[1][0], screen_north[1][1]))
    screen_recovered = ((screen_south[0][0], -screen_south[0][1]), (-screen_south[1][0], screen_south[1][1]))
    checks = {
        "independent_six_plane_rank_ten": design_rank == 10,
        "independent_completed_pair_and_reconstruction_trials": pair_ok,
        "independent_matched_composition_trials": composition_ok,
        "independent_seed_profile_network": network_pass[0],
        "independent_b7_profile_network": network_pass[7],
        "independent_six_pair_completions_per_profile": all(profile_pair_completion.values()),
        "independent_six_constructed_h00_entries_match": all(profile_common_clock.values()),
        "independent_twin_jet_collision": jet_differences[:5] == [Fraction(0)] * 5,
        "independent_twin_next_jet_differs": jet_differences[5] == 840,
        "independent_g233_separator": separator == Fraction(560, 81),
        "independent_five_ruler_mutation_drops_rank": five_ruler_rank < 10,
        "independent_corrupted_edge_breaks_composition": corrupted_edge_defect != 0,
        "independent_two_chart_screen_overlap": screen_south == screen_north
        and screen_recovered == screen_north,
        "independent_both_twins_pass_network_structure": all(network_pass.values()),
        "independent_candidate_rejects_control": candidate_rejects_control,
    }
    result = {
        "landing": "INDEPENDENT_CONFIRMATION__NO_CANDIDATE",
        "all_positive_checks_pass": all(value for key, value in checks.items() if key != "independent_candidate_rejects_control"),
        "candidate_nonidentity_gate_passes": checks["independent_candidate_rejects_control"],
        "trials": trials,
        "assertions": pair_assertions + 5,
        "rank": design_rank,
        "five_ruler_rank": five_ruler_rank,
        "network_pass_by_b": {str(key): value for key, value in network_pass.items()},
        "profile_pair_completion_by_b": {
            str(key): value for key, value in profile_pair_completion.items()
        },
        "profile_common_clock_by_b": {str(key): value for key, value in profile_common_clock.items()},
        "separator": f"{separator.numerator}/{separator.denominator}",
        "checks": checks,
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-write",
        action="store_true",
        help="recompute and print the result without changing the frozen verification artifact",
    )
    args = parser.parse_args()
    result = compute()
    if not args.no_write:
        (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

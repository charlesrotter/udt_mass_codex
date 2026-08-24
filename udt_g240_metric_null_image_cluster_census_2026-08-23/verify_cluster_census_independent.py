#!/usr/bin/env python3
"""Independent exact enumeration for G240; imports no production code."""

from __future__ import annotations

import argparse
import itertools
import json
import random
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "INDEPENDENT_VERIFICATION.json"


def count_images(images: list[int], cells: int) -> list[int]:
    return [sum(image == cell for image in images) for cell in range(cells)]


def three_point_count_distribution(mean: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    """Distribution on 0,1,2 matching Poisson first two factorial moments exactly."""
    p2 = mean * mean / 2
    p1 = mean - mean * mean
    p0 = 1 - p1 - p2
    assert p0 >= 0 and p1 >= 0 and p2 >= 0
    return p0, p1, p2


def enumerate_first_second(parents: list[tuple[Fraction, list[int]]], cells: int):
    distributions = [three_point_count_distribution(mean) for mean, _ in parents]
    first = [Fraction(0) for _ in range(cells)]
    second = [[Fraction(0) for _ in range(cells)] for _ in range(cells)]
    probability_total = Fraction(0)
    for counts in itertools.product(range(3), repeat=len(parents)):
        probability = Fraction(1)
        observed = [0] * cells
        for parent_index, count in enumerate(counts):
            probability *= distributions[parent_index][count]
            image_counts = count_images(parents[parent_index][1], cells)
            for cell in range(cells):
                observed[cell] += count * image_counts[cell]
        probability_total += probability
        for i in range(cells):
            first[i] += probability * observed[i]
            for j in range(cells):
                ordered_distinct = observed[i] * observed[j] - (observed[i] if i == j else 0)
                second[i][j] += probability * ordered_distinct
    assert probability_total == 1
    return first, second


def direct_formula(parents: list[tuple[Fraction, list[int]]], cells: int):
    first = [Fraction(0) for _ in range(cells)]
    sibling = [[Fraction(0) for _ in range(cells)] for _ in range(cells)]
    for mean, images in parents:
        c = count_images(images, cells)
        for i in range(cells):
            first[i] += mean * c[i]
            for j in range(cells):
                sibling[i][j] += mean * (c[i] * c[j] - (c[i] if i == j else 0))
    second = [[first[i] * first[j] + sibling[i][j] for j in range(cells)] for i in range(cells)]
    return first, sibling, second


def normalized_gamma(first: list[Fraction], sibling: list[list[Fraction]]):
    n = sum(first, Fraction(0))
    s = sum((sum(row, Fraction(0)) for row in sibling), Fraction(0))
    denominator = n * n + s
    p = [value / n for value in first]
    return [
        [sibling[i][j] / denominator - (s / denominator) * p[i] * p[j] for j in range(len(first))]
        for i in range(len(first))
    ]


def permute_sky(parents: list[tuple[Fraction, list[int]]], permutation: list[int]):
    return [(mean, [permutation[image] for image in images]) for mean, images in parents]


def permute_vector(vector: list[Fraction], permutation: list[int]):
    result = [Fraction(0)] * len(vector)
    for old, new in enumerate(permutation):
        result[new] = vector[old]
    return result


def permute_matrix(matrix: list[list[Fraction]], permutation: list[int]):
    result = [[Fraction(0) for _ in permutation] for _ in permutation]
    for i in range(len(permutation)):
        for j in range(len(permutation)):
            result[permutation[i]][permutation[j]] = matrix[i][j]
    return result


def build_result() -> dict[str, Any]:
    rng = random.Random(240)
    means = [Fraction(1, 4), Fraction(1, 3), Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)]
    cases = 2003
    multi_image_cases = 0
    one_image_cases = 0
    covariance_cases = 0
    for _ in range(cases):
        cells = rng.randint(2, 4)
        parent_count = rng.randint(1, 4)
        parents: list[tuple[Fraction, list[int]]] = []
        all_single = True
        for _parent in range(parent_count):
            image_count = rng.randint(1, 4)
            all_single = all_single and image_count == 1
            parents.append((rng.choice(means), [rng.randrange(cells) for _ in range(image_count)]))

        enumerated_first, enumerated_second = enumerate_first_second(parents, cells)
        formula_first, sibling, formula_second = direct_formula(parents, cells)
        assert enumerated_first == formula_first
        assert enumerated_second == formula_second
        expected_s = sum(mean * len(images) * (len(images) - 1) for mean, images in parents)
        actual_s = sum((sum(row, Fraction(0)) for row in sibling), Fraction(0))
        assert actual_s == expected_s
        if all_single:
            one_image_cases += 1
            assert actual_s == 0
        else:
            multi_image_cases += 1
            assert actual_s > 0

        branch_reordered = [(mean, list(reversed(images))) for mean, images in reversed(parents)]
        reordered_first, reordered_sibling, reordered_second = direct_formula(branch_reordered, cells)
        assert reordered_first == formula_first
        assert reordered_sibling == sibling
        assert reordered_second == formula_second

        permutation = list(range(cells))
        rng.shuffle(permutation)
        sky_first, sky_sibling, _ = direct_formula(permute_sky(parents, permutation), cells)
        assert sky_first == permute_vector(formula_first, permutation)
        assert sky_sibling == permute_matrix(sibling, permutation)
        covariance_cases += 1

        gamma = normalized_gamma(formula_first, sibling)
        assert sum((sum(row, Fraction(0)) for row in gamma), Fraction(0)) == 0

    g239 = [(Fraction(1), [0, 1])]
    first, sibling, _ = direct_formula(g239, 2)
    gamma = normalized_gamma(first, sibling)
    assert gamma == [
        [Fraction(-1, 12), Fraction(1, 12)],
        [Fraction(1, 12), Fraction(-1, 12)],
    ]

    return {
        "audit": "G240_INDEPENDENT_EXACT_CONFIGURATION_ENUMERATION",
        "status": "PASS",
        "implementation": "independent_fraction_enumeration_of_matching_first_two_poisson_factorial_moments",
        "seed": 240,
        "cases": cases,
        "one_image_cases": one_image_cases,
        "multi_image_cases": multi_image_cases,
        "covariance_cases": covariance_cases,
        "configuration_states_per_case_max": 81,
        "g239_gamma": [["-1/12", "1/12"], ["1/12", "-1/12"]],
        "branch_relabeling_invariant": True,
        "source_reordering_invariant": True,
        "sky_permutation_covariant": True,
        "normalization_exact": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = build_result()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        print(payload, end="")
    else:
        OUTPUT.write_text(payload, encoding="utf-8")
        print(payload, end="")


if __name__ == "__main__":
    main()

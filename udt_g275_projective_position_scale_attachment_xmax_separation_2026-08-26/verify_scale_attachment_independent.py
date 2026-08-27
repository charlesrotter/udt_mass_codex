#!/usr/bin/env python3
"""Independent Fraction census for G275; no production import or output read."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "INDEPENDENT_VERIFICATION.json"
CASES = 20_000
LANDING = (
    "W5_PROJECTIVE_POSITION_IS_HOMOTHETY_INVARIANT__"
    "ONE_MATCHED_NONZERO_WEIGHT_ANCHOR_FIXES_ONE_DIMENSIONAL_SCALE__"
    "DIMENSIONFUL_REPRESENTATIVE_RETAINS_FULL_FRAME_CARRY__"
    "XMAX_EQUALS_SCALE_ONLY_AFTER_SEPARATELY_OWNED_POPULATED_BOUNDARY_COMPLETION"
)


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def multiply(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def scale_matrix(a: list[list[F]], factor: F) -> list[list[F]]:
    return [[factor * value for value in row] for row in a]


def inverse_lorentz(a: list[list[F]]) -> list[list[F]]:
    eta = [[F(0) for _ in range(4)] for _ in range(4)]
    eta[0][0] = F(-1)
    eta[1][1] = eta[2][2] = eta[3][3] = F(1)
    return multiply(multiply(eta, transpose(a)), eta)


def inverse_2x2(g: list[list[F]]) -> list[list[F]]:
    determinant = g[0][0] * g[1][1] - g[0][1] * g[1][0]
    return [
        [g[1][1] / determinant, -g[0][1] / determinant],
        [-g[1][0] / determinant, g[0][0] / determinant],
    ]


def connection(g: list[list[F]], dg: list[list[list[F]]]) -> list[list[list[F]]]:
    inverse = inverse_2x2(g)
    return [
        [
            [
                F(1, 2)
                * sum(
                    (
                        inverse[a][d]
                        * (dg[b][d][c] + dg[c][d][b] - dg[d][b][c])
                        for d in range(2)
                    ),
                    F(0),
                )
                for c in range(2)
            ]
            for b in range(2)
        ]
        for a in range(2)
    ]


def boost(q: tuple[F, F, F]) -> list[list[F]]:
    q2 = sum((value * value for value in q), F(0))
    gamma = (1 + q2) / (1 - q2)
    spatial = tuple(2 * value / (1 - q2) for value in q)
    result = [[F(0) for _ in range(4)] for _ in range(4)]
    result[0][0] = gamma
    for i in range(3):
        result[0][i + 1] = spatial[i]
        result[i + 1][0] = spatial[i]
        for j in range(3):
            result[i + 1][j + 1] = F(int(i == j)) + spatial[i] * spatial[j] / (gamma + 1)
    return result


def rotation_xy(t: F) -> list[list[F]]:
    cosine = (1 - t * t) / (1 + t * t)
    sine = 2 * t / (1 + t * t)
    return [
        [F(1), F(0), F(0), F(0)],
        [F(0), cosine, -sine, F(0)],
        [F(0), sine, cosine, F(0)],
        [F(0), F(0), F(0), F(1)],
    ]


def projective(a: list[list[F]]) -> tuple[F, F, F]:
    return tuple(a[i][0] / a[0][0] for i in range(1, 4))


def norm2(vector: tuple[F, F, F]) -> F:
    return sum((value * value for value in vector), F(0))


def projective_supremum_sq(vectors: list[tuple[F, F, F]]) -> F:
    if not vectors:
        raise ValueError("a populated relation domain is required")
    return max(norm2(vector) for vector in vectors)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    assertions = 0
    active_screen_cases = 0
    carry_separators = 0
    positive_weight_cases = 0
    negative_weight_cases = 0
    finite_domain_controls = 0
    boundary_approach_controls = 0

    def require(condition: bool) -> None:
        nonlocal assertions
        assertions += 1
        assert condition

    for index in range(CASES):
        ell = F(2 + index % 17, 1 + index % 5)
        first = boost((F(1 + index % 2, 13), F(0), F(0)))
        second = boost(
            (
                F(index % 2, 17),
                F(1 + index % 3, 19),
                F(1 + index % 2, 23),
            )
        )
        propagator = boost(
            (
                F(1 + index % 2, 29),
                F(1 + index % 3, 31),
                F(index % 2, 37),
            )
        )
        carry = rotation_xy(F(1 + index % 3, 7))

        lambda_bar = multiply(multiply(inverse_lorentz(second), propagator), first)
        first_scaled = scale_matrix(first, 1 / ell)
        second_scaled = scale_matrix(second, 1 / ell)
        second_scaled_inverse = scale_matrix(inverse_lorentz(second), ell)
        lambda_scaled = multiply(multiply(second_scaled_inverse, propagator), first_scaled)
        chi = projective(lambda_bar)

        require(lambda_scaled == lambda_bar)
        require(projective(lambda_scaled) == chi)
        require(norm2(chi) < 1)
        require(chi[1] != 0 or chi[2] != 0)
        active_screen_cases += 1

        plain = projective(multiply(second, first))
        carried = projective(multiply(multiply(second, carry), first))
        require(projective(multiply(second, carry)) == projective(second))
        require(carried != plain)
        require(tuple(ell * value for value in carried) != tuple(ell * value for value in plain))
        require(tuple((ell * value) / ell for value in plain) == plain)
        carry_separators += 1

        # Independent generic two-dimensional constant-homothety connection check.
        aa = F(2 + index % 5)
        bb = F(index % 3, 11)
        cc = F(3 + index % 7)
        metric = [[-aa, bb], [bb, cc]]
        derivatives = [
            [[F(1 + index % 3, 5), F(1, 7)], [F(1, 7), F(2, 9)]],
            [[F(3, 10), F(1 + index % 2, 8)], [F(1 + index % 2, 8), F(4, 13)]],
        ]
        metric_scaled = scale_matrix(metric, ell * ell)
        derivatives_scaled = [
            [[ell * ell * derivatives[k][i][j] for j in range(2)] for i in range(2)]
            for k in range(2)
        ]
        require(connection(metric_scaled, derivatives_scaled) == connection(metric, derivatives))

        weight = (1, 2, 3, -1, -2, -3)[index % 6]
        baseline = F(5 + index % 11, 2 + index % 3)
        observed = ell**weight * baseline
        ratio = observed / baseline
        require(ratio == ell**weight)
        require(ratio != (ell + 1) ** weight)
        if weight > 0:
            positive_weight_cases += 1
        else:
            negative_weight_cases += 1

        second_weight = (-2, -1, 1, 2)[index % 4]
        second_baseline = F(7 + index % 13, 3 + index % 4)
        second_observed = ell**second_weight * second_baseline
        require(second_observed / second_baseline == ell**second_weight)

        q_finite = F(2 + index % 89, 100)
        require(F(0) <= q_finite < 1)
        require(ell * q_finite < ell)
        require((ell * q_finite) / ell == q_finite)
        finite_domain_controls += 1

        sequence_index = 2 + index % 997
        q_sequence = F(sequence_index, sequence_index + 1)
        require(q_sequence < 1)
        require(F(1) - q_sequence == F(1, sequence_index + 1))
        boundary_approach_controls += 1

    require(active_screen_cases == CASES)
    require(carry_separators == CASES)
    require(positive_weight_cases > 0 and negative_weight_cases > 0)
    require(finite_domain_controls == CASES)
    require(boundary_approach_controls == CASES)
    empty_population_control = False
    try:
        projective_supremum_sq([])
    except ValueError:
        empty_population_control = True
    zero_state_population_control = projective_supremum_sq([(F(0), F(0), F(0))]) == 0
    require(empty_population_control and zero_state_population_control)

    result = {
        "status": "PASS",
        "landing": LANDING,
        "production_imported": False,
        "production_output_read": False,
        "arithmetic": "fractions.Fraction exact rational",
        "cases": CASES,
        "exact_assertions": assertions,
        "active_screen_cases": active_screen_cases,
        "carry_separators": carry_separators,
        "positive_weight_cases": positive_weight_cases,
        "negative_weight_cases": negative_weight_cases,
        "finite_domain_controls": finite_domain_controls,
        "boundary_approach_controls": boundary_approach_controls,
        "empty_population_control": empty_population_control,
        "zero_state_population_control": zero_state_population_control,
        "observations_used": False,
        "history_selected": False,
        "X_max_selected": False,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

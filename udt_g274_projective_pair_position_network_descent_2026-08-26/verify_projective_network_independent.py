#!/usr/bin/env python3
"""Independent exact-rational G274 verifier; imports no production function."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "INDEPENDENT_VERIFICATION.json"
CASES = 20_000
LANDING = (
    "FULL_PATH_LABELLED_FRAME_MORPHISMS_DESCEND_EXACTLY__"
    "PROJECTIVE_OPEN_BALL_VECTOR_IS_A_VALID_PAIR_COORDINATE_BUT_NOT_A_"
    "STANDALONE_NONRADIAL_COMPOSITION_LAW__SCREEN_FRAME_CARRY_IS_REQUIRED__"
    "RADIAL_MOBIUS_STRATUM_CLOSES__SCALE_HISTORY_BRANCH_POPULATION_AND_XMAX_REMAIN_OPEN"
)


def eye(n: int) -> list[list[F]]:
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def multiply(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def equal(a: list[list[F]], b: list[list[F]]) -> bool:
    return a == b


def boost(q: tuple[F, F, F]) -> list[list[F]]:
    q2 = sum((x * x for x in q), F(0))
    gamma = (1 + q2) / (1 - q2)
    s = tuple(2 * x / (1 - q2) for x in q)
    result = [[F(0) for _ in range(4)] for _ in range(4)]
    result[0][0] = gamma
    for i in range(3):
        result[0][i + 1] = s[i]
        result[i + 1][0] = s[i]
        for j in range(3):
            result[i + 1][j + 1] = F(int(i == j)) + s[i] * s[j] / (gamma + 1)
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


def norm2(v: tuple[F, F, F]) -> F:
    return sum((x * x for x in v), F(0))


def lorentz_ok(a: list[list[F]]) -> bool:
    eta = [[F(0) for _ in range(4)] for _ in range(4)]
    eta[0][0] = F(-1)
    eta[1][1] = eta[2][2] = eta[3][3] = F(1)
    return multiply(multiply(transpose(a), eta), a) == eta


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    assertions = 0
    active_screen = 0
    separators = 0
    collinear_controls = 0
    overlap_controls = 0

    def require(condition: bool) -> None:
        nonlocal assertions
        assertions += 1
        assert condition

    for index in range(CASES):
        q1 = (F(1 + index % 3, 13), F(0), F(0))
        q2 = (
            F((index * 5) % 3, 17),
            F(1 + (index * 7) % 3, 19),
            F(1 + (index * 11) % 3, 23),
        )
        q3 = (
            F(1 + (index * 13) % 2, 29),
            F(1 + (index * 17) % 2, 31),
            F((index * 19) % 2, 37),
        )
        first = boost(q1)
        second = boost(q2)
        third = boost(q3)
        carry = rotation_xy(F(1 + index % 3, 7))
        second_with_carry = multiply(second, carry)

        require(lorentz_ok(first))
        require(lorentz_ok(second))
        require(lorentz_ok(carry))
        require(projective(second_with_carry) == projective(second))

        plain = multiply(second, first)
        carried = multiply(second_with_carry, first)
        v_plain = projective(plain)
        v_carried = projective(carried)
        require(lorentz_ok(plain))
        require(norm2(v_plain) < 1)
        require(norm2(v_carried) < 1)
        require(v_plain != v_carried)
        separators += 1

        v_second = projective(second)
        require(v_second[1] != 0 and v_second[2] != 0)
        active_screen += 1

        left_grouping = multiply(third, multiply(second, first))
        right_grouping = multiply(multiply(third, second), first)
        require(left_grouping == right_grouping)

        # Exact radial Möbius control from rational Cayley parameters.
        radial_first = boost((q1[0], F(0), F(0)))
        radial_second = boost((F(1 + index % 2, 11), F(0), F(0)))
        z1 = projective(radial_first)[0]
        z2 = projective(radial_second)[0]
        radial_total = projective(multiply(radial_second, radial_first))[0]
        require(radial_total == (z2 + z1) / (1 + z2 * z1))
        collinear_controls += 1

        # Independent overlap covariance with a changed middle frame.
        middle_change = rotation_xy(F(1 + index % 2, 5))
        middle_inverse = transpose(middle_change)
        first_prime = multiply(middle_change, first)
        second_prime = multiply(second, middle_inverse)
        require(multiply(second_prime, first_prime) == plain)
        overlap_controls += 1

    require(active_screen * 10 >= 9 * CASES)
    require(separators == CASES)
    require(collinear_controls == CASES)
    require(overlap_controls == CASES)

    result = {
        "status": "PASS",
        "landing": LANDING,
        "production_imported": False,
        "arithmetic": "fractions.Fraction exact rational",
        "cases": CASES,
        "exact_assertions": assertions,
        "active_screen_cases": active_screen,
        "vector_only_separators": separators,
        "collinear_mobius_controls": collinear_controls,
        "overlap_covariance_controls": overlap_controls,
        "physical_position_attachment": "CANDIDATE_NOT_ADOPTED",
        "observations_used": False,
        "scale_selected": False,
        "history_selected": False,
        "branch_population_selected": False,
        "X_max_used": False,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

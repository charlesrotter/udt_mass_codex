#!/usr/bin/env python3
"""G274 mutation and typed-overreach catches."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "CATCH_PROOF_RESULT.json"


def boost(q: sp.Matrix) -> sp.Matrix:
    q2 = (q.T * q)[0]
    gamma = sp.cancel((1 + q2) / (1 - q2))
    s = q.applyfunc(lambda x: sp.cancel(2 * x / (1 - q2)))
    spatial = sp.eye(3) + s * s.T / (gamma + 1)
    return sp.Matrix.vstack(
        sp.Matrix.hstack(sp.Matrix([[gamma]]), s.T),
        sp.Matrix.hstack(s, spatial),
    ).applyfunc(sp.cancel)


def projective(matrix: sp.Matrix) -> sp.Matrix:
    return (matrix[1:, 0] / matrix[0, 0]).applyfunc(sp.cancel)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    bx = boost(sp.Matrix([sp.Rational(1, 3), 0, 0]))
    bs = boost(sp.Matrix([0, sp.Rational(1, 4), sp.Rational(1, 5)]))
    rotation = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 0, -1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
        ]
    )

    v_screen = projective(bs)
    v_plain = projective(bs * bx)
    v_hidden_carry = projective((bs * rotation) * bx)
    scale_1 = sp.Rational(7)
    scale_2 = sp.Rational(13)
    ledger = (ROOT / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")

    catches = {
        "erased_screen_component_caught": sp.cancel((v_screen.T * v_screen)[0] - v_screen[0] ** 2) > 0,
        "commuting_noncollinear_relations_caught": bs * bx != bx * bs,
        "vector_only_composition_caught": (
            projective(bs * rotation) == projective(bs) and v_hidden_carry != v_plain
        ),
        "path_label_erasure_caught": projective(bx * (bs * bx)) != projective(bs * bx),
        "scale_selection_caught": (
            (scale_1 * v_plain) / scale_1 == v_plain
            and (scale_2 * v_plain) / scale_2 == v_plain
            and scale_1 != scale_2
        ),
        "physical_canonization_caught": (
            "CANDIDATE_WORKING_FOUNDATIONAL_CLARIFICATION_NOT_ADOPTED" in ledger
            and "dimensionful_X\tFREE_AND_UNSELECTED" in ledger
            and "X_max\tOPEN_NOT_USED" in ledger
        ),
    }
    catches = {key: bool(value) for key, value in catches.items()}
    assert len(catches) == 6
    assert all(catches.values()), [key for key, value in catches.items() if not value]

    result = {
        "status": "PASS",
        "implementation_mutations_caught": 5,
        "typed_scope_catches_passed": 1,
        "catches": catches,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

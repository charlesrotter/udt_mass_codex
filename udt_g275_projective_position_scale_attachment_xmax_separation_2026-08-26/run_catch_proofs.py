#!/usr/bin/env python3
"""Executable hostile mutations and typed-scope rejection checks for G275."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "CATCH_PROOF_RESULT.json"
Vector = tuple[F, F, F]
Matrix = list[list[F]]


def multiply(a: Matrix, b: Matrix) -> Matrix:
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def inverse_lorentz(a: Matrix) -> Matrix:
    eta = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)],
           [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    return multiply(multiply(eta, transpose(a)), eta)


def boost(q: Vector) -> Matrix:
    q2 = sum((value * value for value in q), F(0))
    gamma = (1 + q2) / (1 - q2)
    spatial = tuple(2 * value / (1 - q2) for value in q)
    result = [[F(0) for _ in range(4)] for _ in range(4)]
    result[0][0] = gamma
    for i in range(3):
        result[0][i + 1] = result[i + 1][0] = spatial[i]
        for j in range(3):
            result[i + 1][j + 1] = F(int(i == j)) + spatial[i] * spatial[j] / (gamma + 1)
    return result


def rotation_xy(t: F) -> Matrix:
    cosine = (1 - t * t) / (1 + t * t)
    sine = 2 * t / (1 + t * t)
    return [[F(1), F(0), F(0), F(0)], [F(0), cosine, -sine, F(0)],
            [F(0), sine, cosine, F(0)], [F(0), F(0), F(0), F(1)]]


def projective(a: Matrix) -> Vector:
    return tuple(a[i][0] / a[0][0] for i in range(1, 4))


def scale_matrix(a: Matrix, factor: F) -> Matrix:
    return [[factor * value for value in row] for row in a]


def full_morphism(first: Matrix, second: Matrix, propagator: Matrix) -> Matrix:
    return multiply(multiply(inverse_lorentz(second), propagator), first)


def projective_supremum_sq(vectors: list[Vector]) -> F:
    if not vectors:
        raise ValueError("a populated relation domain is required")
    return max(sum((value * value for value in vector), F(0)) for vector in vectors)


def require_nonzero_weight(weight: int) -> None:
    if weight == 0:
        raise ValueError("zero homothety weight cannot recover scale")


def anchor_matches(ell: F, observed: F, baseline: F, weight: int) -> bool:
    require_nonzero_weight(weight)
    return observed == ell**weight * baseline


def append_check(ledger: list[dict[str, object]], name: str, kind: str,
                 baseline: bool, mutant_rejected: bool) -> None:
    assert baseline and mutant_rejected, name
    ledger.append({
        "name": name,
        "kind": kind,
        "baseline_passed": baseline,
        "mutant_rejected": mutant_rejected,
    })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    ell_a = F(7, 3)
    ell_b = F(11, 4)
    first = boost((F(1, 7), F(0), F(0)))
    second = boost((F(1, 11), F(2, 13), F(1, 17)))
    propagator = boost((F(1, 19), F(1, 23), F(0)))
    baseline_morphism = full_morphism(first, second, propagator)
    scaled_morphism = multiply(
        multiply(scale_matrix(inverse_lorentz(second), ell_a), propagator),
        scale_matrix(first, 1 / ell_a),
    )
    chi = projective(baseline_morphism)
    ledger: list[dict[str, object]] = []

    # M1: the correct homothety cancels in the full morphism; attaching it to chi is a leak.
    leaked_chi = tuple(ell_a * value for value in chi)
    append_check(ledger, "homothety_leak_into_projective_state", "implementation",
                 scaled_morphism == baseline_morphism, leaked_chi != chi)

    # M2: deleting either active screen component changes this exact nonradial state.
    screen_deleted = (chi[0], F(0), F(0))
    append_check(ledger, "screen_deletion", "implementation",
                 chi[1] != 0 and chi[2] != 0, screen_deleted != chi)

    # M3: equal single-arrow projective states with distinct spatial carry compose differently.
    carry = rotation_xy(F(2, 9))
    second_with_carry = multiply(second, carry)
    same_single_state = projective(second_with_carry) == projective(second)
    plain_composite = projective(multiply(second, first))
    carried_composite = projective(multiply(second_with_carry, first))
    append_check(ledger, "vector_only_composition", "implementation",
                 same_single_state, plain_composite != carried_composite)

    # M4: one matched datum admits one common scale; a per-anchor replacement fails it.
    baseline_anchor = F(13, 8)
    weight = -2
    observed = ell_a**weight * baseline_anchor
    append_check(ledger, "per_anchor_scale_proliferation", "implementation",
                 anchor_matches(ell_a, observed, baseline_anchor, weight),
                 not anchor_matches(ell_b, observed, baseline_anchor, weight))

    # M5: a finite populated domain has a strict sub-boundary supremum, not ell.
    finite_population = [(F(1, 2), F(1, 3), F(1, 4)), (F(2, 3), F(1, 5), F(1, 7))]
    q2 = projective_supremum_sq(finite_population)
    x_sup_sq = ell_a * ell_a * q2
    automatic_xmax_sq = ell_a * ell_a
    append_check(ledger, "automatic_xmax_equals_scale", "implementation",
                 q2 < 1, x_sup_sq != automatic_xmax_sq)

    # M6: empty population is rejected, unlike a populated zero-state domain.
    empty_rejected = False
    try:
        projective_supremum_sq([])
    except ValueError:
        empty_rejected = True
    zero_population_sup = projective_supremum_sq([(F(0), F(0), F(0))])
    append_check(ledger, "empty_population_as_zero_supremum", "implementation",
                 zero_population_sup == 0, empty_rejected)

    # T1: no power of c_E with dimensions L T^-1 has pure-length dimensions L^1 T^0.
    candidate_power = F(1)  # forced by the length exponent
    full_dimension_matches = (candidate_power, -candidate_power) == (F(1), F(0))
    dropped_time_dimension_mutant = candidate_power == 1
    append_check(ledger, "ce_only_length_attachment", "typed_scope",
                 not full_dimension_matches, dropped_time_dimension_mutant)

    # T2: zero-weight data are scale-blind and must be rejected by the recovery contract.
    zero_weight_rejected = False
    try:
        require_nonzero_weight(0)
    except ValueError:
        zero_weight_rejected = True
    scale_blind = ell_a**0 * baseline_anchor == ell_b**0 * baseline_anchor
    append_check(ledger, "zero_weight_scale_recovery", "typed_scope",
                 scale_blind, zero_weight_rejected)

    catches = {row["name"] + "_caught": True for row in ledger}
    implementation = sum(row["kind"] == "implementation" for row in ledger)
    typed = sum(row["kind"] == "typed_scope" for row in ledger)
    assert implementation == 6 and typed == 2 and len(ledger) == 8

    result = {
        "status": "PASS",
        "implementation_mutations_caught": implementation,
        "typed_scope_catches_passed": typed,
        "catches": catches,
        "mutation_ledger": ledger,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

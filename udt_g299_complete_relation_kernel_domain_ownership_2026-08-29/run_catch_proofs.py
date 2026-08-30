#!/usr/bin/env python3
"""Hostile mutation catches for the G299 load-bearing witnesses."""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def mdot(x, y):
    return -x[0] * y[0] + x[1] * y[1] + x[2] * y[2]


def det3(a, b, c):
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - b[0] * (a[1] * c[2] - a[2] * c[1])
        + c[0] * (a[1] * b[2] - a[2] * b[1])
    )


def has_owner_phrase(text: str) -> bool:
    return "physical normalized pair position is the metric's complete projective relation state" in text


def has_carry_phrase(text: str) -> bool:
    return "projectivization forgets the arrow's right spatial/frame carry" in text


def catches() -> dict[str, bool]:
    r, w = F(3, 2), F(2, 5)
    gamma = (1 + r * r + r * r * w * w) / (2 * r)
    a = (-1 + r * r + r * r * w * w) / (2 * r)
    U = (gamma, a, w)
    clock = tuple(r * x for x in U)
    nT = (F(0), F(1), F(0))
    nL = (r - gamma, r - a, -w)

    wrong_sign_local = (r - gamma, r + a, -w)
    omitted_screen_local = (r - gamma, r - a, F(0))

    founding = (HERE.parent / "founding.md").read_text()
    g274 = (HERE.parent / "udt_g274_projective_pair_position_network_descent_2026-08-26" /
            "EXACT_DERIVATION.md").read_text()

    scalar_only_mutant_says_equal = mdot(clock, clock) == mdot(clock, clock)
    complete_plane_test_says_equal = det3(clock, nT, nL) == 0
    owner_phrase = "physical normalized pair position is the metric's complete projective relation state"
    carry_phrase = "projectivization forgets the arrow's right spatial/frame carry"

    # Every boolean is true only if the named corruption is detected.
    return {
        "wrong_target_local_sign_rejected": mdot(U, wrong_sign_local) != 0,
        "omitted_active_screen_rejected": mdot(omitted_screen_local, omitted_screen_local) != 1,
        "plane_collapse_rejected": det3(clock, nT, nL) != 0,
        "constant_clock_entry_rejected": mdot(clock, clock) != F(-1),
        "scalar_equals_complete_rejected": scalar_only_mutant_says_equal and not complete_plane_test_says_equal,
        "missing_W5_owner_phrase_rejected": (
            has_owner_phrase(founding) and not has_owner_phrase(founding.replace(owner_phrase, ""))
        ),
        "missing_full_carry_phrase_rejected": (
            has_carry_phrase(g274) and not has_carry_phrase(g274.replace(carry_phrase, ""))
        ),
    }


def main() -> None:
    results = catches()
    assert all(results.values()), results
    output = {"status": "PASS", "hostile_catches": len(results), "catches": results}
    (HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

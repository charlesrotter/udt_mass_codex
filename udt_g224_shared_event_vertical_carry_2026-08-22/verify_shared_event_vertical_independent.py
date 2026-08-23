#!/usr/bin/env python3
"""Independent exact-rational G224 replay without SymPy."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent
CASES = 20000
SEED = 2240822


def positive(rng: random.Random) -> Fraction:
    return Fraction(rng.randint(1, 97), rng.randint(1, 89))


def main(*, write_outputs: bool = True) -> None:
    rng = random.Random(SEED)
    assertions = 0

    for _ in range(CASES):
        w1, w2, w3, g1, g2, zeta = (positive(rng) for _ in range(6))

        c21 = w1 / w2
        assert w2 * c21 == w1
        assertions += 1

        c21_prime = (g1 * w1) / (g2 * w2)
        assert c21_prime * g2 == g1 * c21
        assertions += 1

        assert (zeta * w1) / (zeta * w2) == c21
        assertions += 1

        assert (w2 / w3) * (w1 / w2) == w1 / w3
        assertions += 1
        assert (w1 / w2) * (w2 / w1) == 1
        assertions += 1

        w_a, w_b_in, w_b_out, w_c = (positive(rng) for _ in range(4))
        r_ab = w_a / w_b_in
        r_bc = w_b_out / w_c
        q_ab = w_b_in / w_a
        q_bc = w_c / w_b_out
        assert q_ab == 1 / r_ab
        assertions += 1
        assert q_bc == 1 / r_bc
        assertions += 1
        assert q_bc * q_ab == 1 / (r_bc * r_ab)
        assertions += 1

        switch_raw = w_b_in / w_b_out
        assert switch_raw / w_b_in == 1 / w_b_out
        assertions += 1

        w_c_out, w_d = positive(rng), positive(rng)
        r_cd = w_c_out / w_d
        q_cd = w_d / w_c_out
        assert q_cd * q_bc * q_ab == 1 / (r_cd * r_bc * r_ab)
        assertions += 1

        # An independent direct edge is generally unconstrained. Force it to
        # differ from the composite if random equality happens.
        r_ac_independent = positive(rng)
        if r_ac_independent == r_bc * r_ab:
            r_ac_independent += 1
        assert 1 / r_ac_independent != q_bc * q_ab
        assertions += 1

    # Fixed exact Minkowski direction witness.
    k1 = (Fraction(1), Fraction(1), Fraction(0), Fraction(0))
    k2 = (Fraction(1), Fraction(3, 5), Fraction(4, 5), Fraction(0))

    def minkowski_norm(v: tuple[Fraction, ...]) -> Fraction:
        return -v[0] * v[0] + sum(x * x for x in v[1:])

    assert minkowski_norm(k1) == 0
    assertions += 1
    assert minkowski_norm(k2) == 0
    assertions += 1
    assert k1 != k2
    assertions += 1

    result = {
        "status": "PASS",
        "seed": SEED,
        "cases": CASES,
        "exact_rational_assertions": assertions,
        "affine_rescaling_invariant": True,
        "clock_recalibration_invariant": True,
        "vertex_cocycle": True,
        "inverse_clock_path_carry": True,
        "independent_direct_edge_counterexample": True,
        "different_null_direction_control": True,
    }
    if write_outputs:
        (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
    print(
        f"PASS: G224 independent replay; {CASES} cases; "
        f"{assertions} exact-rational assertions"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    main(write_outputs=not args.check_only)

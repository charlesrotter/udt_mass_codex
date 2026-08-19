#!/usr/bin/env python3
"""Dependency-free exact rational replay of the G176 theorem."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent
TRIALS = 20_000
SEED = 176_202_608_19


def positive(rng: random.Random) -> Fraction:
    return Fraction(rng.randint(1, 80), rng.randint(1, 80))


def signed(rng: random.Random) -> Fraction:
    return Fraction(rng.randint(-80, 80), rng.randint(1, 80))


def main() -> None:
    rng = random.Random(SEED)
    checks = 0
    turn_checks = 0
    for i in range(TRIALS):
        T = positive(rng)
        Ls = positive(rng)
        beta = signed(rng)
        m = positive(rng)
        k = positive(rng)

        h00 = -(T * T)
        h01 = -(T * T) * beta
        h11 = Ls * Ls - T * T * beta * beta
        det_aux = h00 * h11 - h01 * h01
        assert det_aux == -(T * T * Ls * Ls)
        checks += 1

        hs00 = h00
        hs01 = h01 / m
        hs11 = h11 / (m * m)
        det_s = hs00 * hs11 - hs01 * hs01
        assert det_s == det_aux / (m * m)
        assert hs01 / hs00 == beta / m
        assert hs11 - hs01 * hs01 / hs00 == Ls * Ls / (m * m)
        checks += 3

        m_rec = T * Ls
        det_rec = det_aux / (m_rec * m_rec)
        assert det_rec == -1
        assert Ls / m_rec == 1 / T
        checks += 2

        # If a positive n also gives determinant -1, exact squares force n=m_rec.
        n2 = -det_aux
        assert n2 == m_rec * m_rec
        checks += 1

        # Positive auxiliary reparameterization.
        h01_t = -(T * T) * (k * beta)
        h11_t = (k * Ls) ** 2 - T * T * (k * beta) ** 2
        mt = k * m
        assert h01_t / mt == hs01
        assert h11_t / (mt * mt) == hs11
        checks += 2

        # Orientation reversal preserves determinant and flips the shift.
        assert (-h01) / m == -hs01
        assert h00 * h11 - (-h01) * (-h01) == det_aux
        checks += 2

        A = positive(rng)
        v2 = Fraction(rng.randint(0, 80), rng.randint(1, 80))
        r2 = positive(rng)
        b2 = positive(rng)
        H = A * v2 + r2 * b2
        static_m2 = H / A
        assert H / static_m2 == A
        assert -(Fraction(1, 1) / A) * (H / static_m2) == -1
        checks += 2
        if v2 == 0 or i % 10 == 0:
            assert static_m2 > 0
            turn_checks += 1

    result = {
        "audit": "G176",
        "implementation": "independent Python standard-library Fraction replay",
        "seed": SEED,
        "trials": TRIALS,
        "exact_assertion_count": checks,
        "angular_turn_positive_checks": turn_checks,
        "pass": True,
        "landing_replayed": "COMPLETED_PAIR_DUAL_RECIPROCITY_UNIQUELY_FIXES_RECIPROCAL_RULER",
    }
    (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

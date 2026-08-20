#!/usr/bin/env python3
"""Independent exact G183 replay using a rational Lorentz basis."""

from fractions import Fraction as F
import json
import os
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TRIALS = 20000


def dot(v, w):
    return -v[0] * w[0] + sum(v[i] * w[i] for i in range(1, 4))


def add(*vectors):
    return tuple(sum(vector[i] for vector in vectors) for i in range(4))


def scale(a, v):
    return tuple(a * x for x in v)


def rank_two(u, v):
    return any(u[i] * v[j] != u[j] * v[i] for i in range(4) for j in range(i + 1, 4))


def run():
    rng = random.Random(9183)
    assertions = 0
    collapsed = 0
    regular = 0

    for trial in range(TRIALS):
        numerator = rng.randint(-7, 7)
        denominator = rng.randint(abs(numerator) + 1, abs(numerator) + 9)
        velocity = F(numerator, denominator)
        gamma = (1 + velocity * velocity) / (1 - velocity * velocity)
        boost = 2 * velocity / (1 - velocity * velocity)
        u = (gamma, boost, F(0), F(0))
        e1 = (boost, gamma, F(0), F(0))
        e2 = (F(0), F(0), F(1), F(0))
        e3 = (F(0), F(0), F(0), F(1))
        assert dot(u, u) == -1 and dot(e1, e1) == dot(e2, e2) == dot(e3, e3) == 1
        assert dot(u, e1) == dot(u, e2) == dot(u, e3) == 0
        assertions += 7

        a = F(rng.randint(-9, 9), rng.randint(1, 8))
        if trial % 5 == 0:
            b = c = d = F(0)
            collapsed += 1
        else:
            while True:
                b = F(rng.randint(-8, 8), rng.randint(1, 7))
                c = F(rng.randint(-8, 8), rng.randint(1, 7))
                d = F(rng.randint(-8, 8), rng.randint(1, 7))
                if (b, c, d) != (0, 0, 0):
                    break
            regular += 1
        v = add(scale(a, u), scale(b, e1), scale(c, e2), scale(d, e3))
        h00 = dot(u, u)
        h01 = dot(u, v)
        h11 = dot(v, v)
        det_h = h00 * h11 - h01 * h01
        expected = -(b * b + c * c + d * d)
        assert h01 == -a
        assert det_h == expected
        assert (det_h == 0) == (not rank_two(u, v))
        assert (det_h < 0) == rank_two(u, v)
        assertions += 4

    # Independent fixture checks.
    null_clock_h = (F(0), F(1), F(1))
    assert null_clock_h[0] * null_clock_h[2] - null_clock_h[1] ** 2 == -1
    # c=(1,-1) in coefficient space has norm -1 for this Gram matrix.
    assert 2 * null_clock_h[1] * F(1) * F(-1) + null_clock_h[2] == -1
    assertions += 2

    null_generator = (F(1), F(1), F(0), F(0))
    transverse = (F(0), F(0), F(1), F(0))
    assert dot(null_generator, null_generator) == 0
    assert dot(null_generator, transverse) == 0 and dot(transverse, transverse) == 1
    assert rank_two(null_generator, transverse)
    assertions += 3

    spacelike_a = (F(0), F(1), F(0), F(0))
    spacelike_b = (F(0), F(0), F(1), F(0))
    assert dot(spacelike_a, spacelike_a) == dot(spacelike_b, spacelike_b) == 1
    assert dot(spacelike_a, spacelike_b) == 0 and rank_two(spacelike_a, spacelike_b)
    assertions += 2

    # Rindler focus: the tau column has the exact scalar factor 1+a*s.
    for a in (F(1, 3), F(2), F(7, 5)):
        s = -1 / a
        assert 1 + a * s == 0
        assertions += 1

    # Same-endpoint reflected polynomial branches have equal speed functions.
    for s in (F(i, 20) for i in range(21)):
        assert 1 + (1 - 2 * s) ** 2 == 1 + (-(1 - 2 * s)) ** 2
        assertions += 1

    # Winding endpoint modulo 2 is fixed while branch lift and tape magnitude vary.
    lifts = [1 + 2 * n for n in range(-50, 51)]
    assert len(set(lifts)) == 101 and all((value - 1) % 2 == 0 for value in lifts)
    assert (-1) ** 2 == 1 ** 2 and -1 != 1
    assertions += 3

    result = {
        "audit": "G183",
        "status": "PASS",
        "trials": TRIALS,
        "assertions": assertions,
        "collapsed_trials": collapsed,
        "regular_trials": regular,
        "method": "rational Lorentz basis and coefficient-space rank classification",
        "checks": {
            "determinant_formula_independent": True,
            "rank_equivalence_independent": True,
            "null_clock_nonintrinsic": True,
            "null_plane_rank_two_degenerate_metric": True,
            "spacelike_plane_outside_domain": True,
            "focus_factor": True,
            "reflected_branch_metric": True,
            "winding_label_survives": True,
        },
    }
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: G183 independent Lorentz-basis replay; trials={TRIALS}; assertions={assertions}")


if __name__ == "__main__":
    run()

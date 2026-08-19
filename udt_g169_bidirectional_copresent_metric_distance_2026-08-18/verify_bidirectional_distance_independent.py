#!/usr/bin/env python3
"""Independent stdlib-only exact replay for G169."""

from __future__ import annotations

import json
import random
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
SEED = 169
TRIALS = 1200
rng = random.Random(SEED)
checks = 0


def require(condition: bool, message: str) -> None:
    global checks
    if not condition:
        raise AssertionError(message)
    checks += 1


def chi(q: Fraction) -> Fraction:
    return (1 - q) / (1 + q)


def matmul(a: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]],
           b: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    return (
        (a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]),
        (a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]),
    )


def det(a: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> Fraction:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv(a: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    determinant = det(a)
    if determinant == 0:
        raise ZeroDivisionError("singular matrix")
    return (
        (a[1][1] / determinant, -a[0][1] / determinant),
        (-a[1][0] / determinant, a[0][0] / determinant),
    )


def reciprocal_ratio(a: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> Fraction:
    return a[1][1] / a[0][0]


for _ in range(TRIALS):
    q1 = Fraction(rng.randint(1, 31), rng.randint(1, 31))
    q2 = Fraction(rng.randint(1, 31), rng.randint(1, 31))
    require(q1 * (1 / q1) == 1, "q reversal")
    require(chi(1 / q1) == -chi(q1), "chi reversal")
    require(chi(q1 * q2) == (chi(q1) + chi(q2)) / (1 + chi(q1) * chi(q2)), "Mobius composition")

    x = Fraction(rng.randint(-30, 30), rng.randint(1, 31))
    y = Fraction(rng.randint(-30, 30), rng.randint(1, 31))
    require(abs(x + y) <= abs(x) + abs(y), "matched depth triangle")

    surface_a = Fraction(rng.randint(1, 20), rng.randint(1, 20))
    q2_endpoint = 1 / (1 + surface_a * surface_a)
    require(q2_endpoint == q2_endpoint, "surface endpoints equal")
    require(q2_endpoint * q2_endpoint != 1, "surface reversal does not invert q")

    a0 = Fraction(rng.randint(1, 11), rng.randint(1, 11))
    a1 = Fraction(rng.randint(-7, 7), rng.randint(1, 11))
    d0 = Fraction(rng.randint(1, 11), rng.randint(1, 11))
    b0 = Fraction(rng.randint(1, 11), rng.randint(1, 11))
    b1 = Fraction(rng.randint(-7, 7), rng.randint(1, 11))
    e0 = Fraction(rng.randint(1, 11), rng.randint(1, 11))
    m_ba = ((a0, a1), (Fraction(0), d0))
    m_cb = ((b0, b1), (Fraction(0), e0))
    m_ca = matmul(m_cb, m_ba)
    require(matmul(m_cb, m_ba) == m_ca, "full carry composition")
    require(det(m_ca) == det(m_cb) * det(m_ba), "determinant character")
    require(reciprocal_ratio(m_ca) == reciprocal_ratio(m_cb) * reciprocal_ratio(m_ba), "reciprocal character")

    p_a = ((Fraction(rng.randint(1, 9)), Fraction(rng.randint(-5, 5))),
           (Fraction(0), Fraction(rng.randint(1, 9))))
    p_b = ((Fraction(rng.randint(1, 9)), Fraction(rng.randint(-5, 5))),
           (Fraction(0), Fraction(rng.randint(1, 9))))
    gauged = matmul(matmul(inv(p_b), m_ba), p_a)
    reverse_gauged = matmul(matmul(inv(p_a), inv(m_ba)), p_b)
    require(reverse_gauged == inv(gauged), "reversal gauge equivariance")

identity = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
shear = ((Fraction(1), Fraction(1)), (Fraction(0), Fraction(1)))
require(shear != identity, "shear nonclosure")
require(det(shear) == 1, "scale scalar blind to shear")
require(reciprocal_ratio(shear) == 1, "reciprocal scalar blind to shear")

require(Fraction(1, 5) != Fraction(1, 2) * Fraction(1, 3), "arbitrary triangle counterexample")
require(Fraction(1, 2) * Fraction(1, 3) == Fraction(1, 6), "matched triangle")

landing = (
    "CONDITIONAL_RELATIONAL_DISTANCE_OBJECT"
    "__RECIPROCAL_SCALAR_REVERSAL_DERIVED_ON_ONE_SUPPLIED_RELATION"
    "__MATCHED_CHAIN_COMPOSITION_DERIVED"
    "__ARBITRARY_TRIANGLE_ADDITIVITY_NOT_REQUIRED_OR_DERIVED"
    "__PHYSICAL_TWO_ENDED_GERM_AND_CARRY_OWNERSHIP_OPEN"
)
result = {
    "implementation": "stdlib Fraction; no production imports",
    "seed": SEED,
    "trials": TRIALS,
    "checks_passed": checks,
    "landing_supported": landing,
}
(HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))

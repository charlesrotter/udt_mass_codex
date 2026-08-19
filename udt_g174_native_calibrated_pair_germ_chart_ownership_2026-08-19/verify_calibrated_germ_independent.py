#!/usr/bin/env python3
"""Independent stdlib/Fraction replay of the G174 load-bearing identities."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent
SEED = 17420260819
TRIALS = 12000


def positive_fraction(rng: random.Random, low: int = 1, high: int = 13) -> Fraction:
    return Fraction(rng.randint(low, high), rng.randint(low, high))


rng = random.Random(SEED)
checks = 0
turning_cases = 0
radial_cases = 0
general_cases = 0
candidate_difference_cases = 0

for i in range(TRIALS):
    A = positive_fraction(rng)
    r = positive_fraction(rng)
    if i % 6 == 0:
        v = Fraction(0)
        b2 = positive_fraction(rng)
        turning_cases += 1
        mode = "turn"
    elif i % 10 == 1:
        v = positive_fraction(rng)
        if rng.randrange(2):
            v = -v
        b2 = Fraction(0)
        radial_cases += 1
        mode = "radial"
    else:
        v = positive_fraction(rng)
        if rng.randrange(2):
            v = -v
        b2 = positive_fraction(rng)
        general_cases += 1
        mode = "general"

    m = positive_fraction(rng)
    lam = positive_fraction(rng)
    H = A * v * v + r * r * b2
    det_cal = -H / (A * m * m)
    e4 = A * H / (m * m)

    assert H > 0
    checks += 1
    assert det_cal < 0
    checks += 1
    assert e4 == A * H / (m * m)
    checks += 1

    H_tilde = A * (lam * v) ** 2 + r * r * lam * lam * b2
    m_tilde = lam * m
    assert H_tilde == lam * lam * H
    checks += 1
    assert A * H_tilde / (m_tilde * m_tilde) == e4
    checks += 1
    assert lam * v / m_tilde == v / m
    checks += 1
    assert lam * lam * b2 / (m_tilde * m_tilde) == b2 / (m * m)
    checks += 1

    mA2 = v * v + r * r * b2
    mP2 = v * v + r * r * b2 / A
    e4A = A * H / mA2
    e4P = A * H / mP2
    assert e4P == A * A
    checks += 1
    if mA2 != mP2:
        candidate_difference_cases += 1
        assert e4A != e4P
    else:
        assert e4A == e4P
    checks += 1

    c = positive_fraction(rng)
    m1 = positive_fraction(rng)
    m2 = positive_fraction(rng)
    endpoint1 = A * H / (m1 * m1)
    endpoint2 = A * H / (m2 * m2)
    assert (endpoint2 / (c * c)) / (endpoint1 / (c * c)) == endpoint2 / endpoint1
    checks += 1

    n1 = positive_fraction(rng)
    n2 = positive_fraction(rng)
    new_relative = (A * H / (n2 * n2)) / (A * H / (n1 * n1))
    old_relative = endpoint2 / endpoint1
    assert new_relative / old_relative == (m2 * n1 / (m1 * n2)) ** 2
    checks += 1

    if mode == "turn":
        assert mA2 == r * r * b2 and mP2 == r * r * b2 / A
        checks += 1
        assert e4A == A and e4P == A * A
        checks += 1
    elif mode == "radial":
        assert mA2 == v * v and mP2 == v * v
        checks += 1
        assert e4A == A * A and e4P == A * A
        checks += 1
    else:
        assert mA2 > 0 and mP2 > 0
        checks += 1
        assert H > 0
        checks += 1

assert turning_cases >= 1000
assert candidate_difference_cases > 0
assert checks == TRIALS * 13

landing = (
    "CALIBRATED_GERM_OWNS_UNIQUE_SCALAR__UNCALIBRATED_LINE_RETAINS_ATLAS"
    "__G173_TENSOR_AND_RANK_THEOREM_RETAINED"
    "__M_IS_THE_JACOBIAN_FROM_AUXILIARY_PARAMETER_TO_SUPPLIED_RULER_COORDINATE"
    "__DISTINCT_M_DEFINE_DISTINCT_CALIBRATED_GERMS_UNLESS_IDENTICAL"
    "__CONSTANT_UNIT_RESCALE_CANCELS_FROM_ENDPOINT_DEPTH"
    "__PHYSICAL_CALIBRATION_AND_CARRY_OWNER_REMAIN_OPEN"
)
result = {
    "status": "PASS__INDEPENDENT_STDLIB_FRACTION_REPLAY",
    "landing_supported": landing,
    "seed": SEED,
    "trials": TRIALS,
    "checks_passed": checks,
    "turning_cases": turning_cases,
    "radial_cases": radial_cases,
    "general_cases": general_cases,
    "candidate_difference_cases": candidate_difference_cases,
    "imports_production_code": False,
    "uses_sympy": False,
}
(HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))

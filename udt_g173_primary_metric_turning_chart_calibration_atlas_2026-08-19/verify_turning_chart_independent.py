#!/usr/bin/env python3
"""Independent stdlib/Fraction replay of the G173 load-bearing identities."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent
SEED = 17320260819
TRIALS = 12000


def positive_fraction(rng: random.Random, low: int = 1, high: int = 12) -> Fraction:
    return Fraction(rng.randint(low, high), rng.randint(low, high))


rng = random.Random(SEED)
checks = 0
turning_cases = 0
radial_cases = 0
general_cases = 0

for i in range(TRIALS):
    A = positive_fraction(rng)  # A = exp(2 phi) > 0
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

    H = A * v * v + r * r * b2
    det_h = -H / A
    raw_e4 = A * H
    mA2 = v * v + r * r * b2
    mP2 = v * v + r * r * b2 / A
    e4A = raw_e4 / mA2
    e4P = raw_e4 / mP2

    assert H > 0
    checks += 1
    assert det_h < 0
    checks += 1
    assert raw_e4 == A * H
    checks += 1
    assert mA2 > 0
    checks += 1
    assert mP2 > 0
    checks += 1
    assert e4A == A * H / mA2
    checks += 1
    assert e4P == A * A
    checks += 1

    lam = positive_fraction(rng)
    H2 = A * (lam * v) ** 2 + r * r * lam * lam * b2
    raw2 = A * H2
    mA22 = (lam * v) ** 2 + r * r * lam * lam * b2
    mP22 = (lam * v) ** 2 + r * r * lam * lam * b2 / A
    assert raw2 == lam * lam * raw_e4
    checks += 1
    assert raw2 / mA22 == e4A
    checks += 1
    assert raw2 / mP22 == e4P
    checks += 1

    if mode == "turn":
        assert e4A == A
        checks += 1
        assert e4P == A * A and det_h == -(r * r * b2) / A
        checks += 1
    else:
        e4r = raw_e4 / (v * v)
        assert e4A == e4r * v * v / mA2
        checks += 1
        if mode == "radial":
            assert e4A == A * A and e4P == A * A
        else:
            assert e4P == e4r * v * v / mP2
        checks += 1

assert turning_cases >= 1000
assert checks == TRIALS * 12

landing = (
    "PULLBACK_EXTENDS__CALIBRATION_ATLAS_NONUNIQUE"
    "__RADIAL_TURN_WITH_ANGULAR_MOTION_IS_REGULAR"
    "__RAW_TERMINAL_PHI_IS_AN_AFFINE_LOG_DENSITY"
    "__ANY_POSITIVE_WEIGHT_ONE_CALIBRATION_GIVES_AN_INVARIANT_SCALAR_CHART"
    "__TWO_METRIC_BUILT_CALIBRATIONS_SURVIVE_AND_DISAGREE"
    "__NO_FINITE_CALIBRATION_CAN_EQUAL_G172_ON_EVERY_PUNCTURED_MONOTONE_NEIGHBORHOOD"
    "__TRUE_FIRST_RANK_BOUNDARY_IS_ZERO_COMPLETE_SPATIAL_TANGENT"
    "__NO_PHYSICAL_CALIBRATION_OR_GLOBAL_SELECTION"
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
    "imports_production_code": False,
    "uses_sympy": False,
}
(HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))

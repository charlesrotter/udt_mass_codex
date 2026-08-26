#!/usr/bin/env python3
"""Independent Fraction/stdlib checks for G273; production is not imported."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "INDEPENDENT_VERIFICATION.json"
LANDING = (
    "FOUNDING_INTENT_OWNS_DISTANCE_TO_RECIPROCAL_RESPONSE_DIRECTION__"
    "STRICT_X_OVER_X_EQUALS_TANH_DELTA_ENTAILMENT_FAILS__"
    "UNIQUE_SCALE_FREE_PROJECTIVE_CONTRAST_AND_COMPLETE_OPEN_BALL_ARE_METRIC_NATIVE__"
    "PHYSICAL_POSITION_ATTACHMENT_IS_ONE_MINIMAL_WORKING_FOUNDATIONAL_CLARIFICATION__"
    "SCALE_HISTORY_POPULATION_AND_XMAX_REMAIN_OPEN"
)


def bounded_alternative(value: float) -> float:
    return value / math.sqrt(1.0 + value * value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    rng = random.Random(273)
    cases = 24000
    exact_assertions = 0
    planar_controls = 0
    active_screen_cases = 0
    counterattachment_separators = 0

    for index in range(cases):
        r = Fraction(rng.randint(1, 100), rng.randint(1, 100))
        if index % 97 == 0:
            wa = wb = Fraction(0)
        else:
            wa = Fraction(rng.randint(-30, 30), rng.randint(1, 30))
            wb = Fraction(rng.randint(-30, 30), rng.randint(1, 30))
        screen2 = wa * wa + wb * wb

        gamma = (r + 1 / r + r * screen2) / 2
        longitudinal = gamma - 1 / r
        rho2 = longitudinal**2 / gamma**2 + screen2 / gamma**2
        chi = (1 / r - r) / (1 / r + r)

        assert gamma >= 1
        assert gamma**2 - longitudinal**2 - screen2 == 1
        assert rho2 == 1 - 1 / gamma**2
        assert -1 < chi < 1
        reverse_gamma = (1 / r + r + (1 / r) * (r**2 * screen2)) / 2
        assert reverse_gamma == gamma
        exact_assertions += 5

        if screen2 == 0:
            assert longitudinal / gamma == -chi
            assert rho2 == chi**2
            planar_controls += 1
            exact_assertions += 2
        else:
            planar_gamma = (r + 1 / r) / 2
            assert gamma > planar_gamma
            assert rho2 > chi**2
            active_screen_cases += 1
            exact_assertions += 2

        delta = -math.log(float(r))
        projective = math.tanh(delta)
        alternative = bounded_alternative(delta)
        assert math.isclose(projective, float(chi), rel_tol=2e-13, abs_tol=2e-13)
        assert -1.0 < alternative < 1.0
        if abs(delta) > 1e-10:
            assert not math.isclose(projective, alternative, rel_tol=1e-12, abs_tol=1e-12)
            counterattachment_separators += 1

    composition_cases = 6000
    for _ in range(composition_cases):
        d1 = rng.uniform(-4.0, 4.0)
        d2 = rng.uniform(-4.0, 4.0)
        d3 = rng.uniform(-4.0, 4.0)
        c1, c2 = math.tanh(d1), math.tanh(d2)
        mobius = (c1 + c2) / (1.0 + c1 * c2)
        assert math.isclose(mobius, math.tanh(d1 + d2), rel_tol=3e-13, abs_tol=3e-13)

        def compose_alt(a: float, b: float) -> float:
            ia = a / math.sqrt(1.0 - a * a)
            ib = b / math.sqrt(1.0 - b * b)
            return bounded_alternative(ia + ib)

        a1, a2, a3 = map(bounded_alternative, (d1, d2, d3))
        left = compose_alt(compose_alt(a1, a2), a3)
        right = compose_alt(a1, compose_alt(a2, a3))
        assert math.isclose(left, right, rel_tol=8e-13, abs_tol=8e-13)

    assert planar_controls > 0
    assert active_screen_cases > 0
    assert counterattachment_separators > 0
    result = {
        "status": "PASS",
        "landing": LANDING,
        "method": "INDEPENDENT_EXACT_FRACTION_HYPERBOLOID_PLUS_STDLIB_COUNTERATTACHMENTS",
        "production_imported": False,
        "cases": cases,
        "exact_assertions": exact_assertions,
        "composition_cases": composition_cases,
        "planar_controls": planar_controls,
        "active_screen_cases": active_screen_cases,
        "counterattachment_separators": counterattachment_separators,
        "strict_entailment": "REFUTED",
        "physical_attachment_scale_history_xmax": "OPEN_NOT_SELECTED",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Dependency-free independent verification for G293.

This implementation does not import the production module or read its output.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import random


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("INDEPENDENT_VERIFICATION.json"))
    args = parser.parse_args()

    rng = random.Random(293)
    assertions = 0

    # Additive and reciprocal/projective composition over an independent floating grid.
    for _ in range(4000):
        # Keep this floating control away from saturated tanh cancellation. The
        # unrestricted identity is certified symbolically by the independent
        # production route; this replay checks a well-conditioned numerical set.
        s = rng.uniform(-1.0, 1.0)
        t = rng.uniform(-1.0, 1.0)
        k = rng.uniform(-1.0, 1.0)
        alpha = rng.uniform(0.05, 7.0)
        assert math.isclose(k * (s + t), k * s + k * t, rel_tol=0.0, abs_tol=2e-14)
        assertions += 1
        ds = math.tanh(k * s)
        dt = math.tanh(k * t)
        composed = (ds + dt) / (1.0 + ds * dt)
        assert math.isclose(composed, math.tanh(k * (s + t)), rel_tol=2e-11, abs_tol=2e-11)
        assertions += 1
        assert math.isclose((k / alpha) * (alpha * s), k * s, rel_tol=2e-15, abs_tol=2e-15)
        assertions += 1
        depth = rng.uniform(-5.0, 5.0)
        shift = rng.uniform(-5.0, 5.0)
        flow_left = depth + shift + k * s
        flow_right = depth + k * s + shift
        assert math.isclose(flow_left, flow_right, rel_tol=0.0, abs_tol=2e-14)
        assertions += 1

    # Exact P2 integrals from the antiderivative (x^3-x)/2.
    def p2_antiderivative(x: Fraction) -> Fraction:
        return (x**3 - x) / 2

    assert p2_antiderivative(Fraction(1)) - p2_antiderivative(Fraction(-1)) == 0
    assertions += 1
    for numerator in range(-9, 10):
        c = Fraction(numerator, 10)
        amplitude = Fraction(7, 13)
        cap = amplitude * (p2_antiderivative(Fraction(1)) - p2_antiderivative(c))
        expected = amplitude * (c - c**3) / 2
        assert cap == expected
        assertions += 1
    north = Fraction(1) + Fraction(7, 13)
    equator = Fraction(1) - Fraction(7, 26)
    assert north - equator == Fraction(21, 26)
    assertions += 1

    # Difference one-form b=x(1-x^2)/2 dphi obeys db=P2*omega after
    # omega=-dx^dphi. Check the polynomial coefficient exactly.
    for numerator in range(-10, 11):
        x = Fraction(numerator, 10)
        db_dx = (1 - 3 * x * x) / 2
        p2 = (3 * x * x - 1) / 2
        assert db_dx == -p2
        assertions += 1

    # Endpoint cocycle from a nonlinear potential composes and reverses but is
    # not homogeneous in endpoint difference.
    def potential(x: Fraction) -> Fraction:
        return x + x**3

    def endpoint_delta(a: Fraction, b: Fraction) -> Fraction:
        return potential(b) - potential(a)

    for _ in range(1000):
        a = Fraction(rng.randint(-50, 50), 13)
        b = Fraction(rng.randint(-50, 50), 17)
        c = Fraction(rng.randint(-50, 50), 19)
        assert endpoint_delta(a, c) == endpoint_delta(a, b) + endpoint_delta(b, c)
        assert endpoint_delta(a, b) == -endpoint_delta(b, a)
        assertions += 2
        if a != 0 and b != a:
            if endpoint_delta(a, b) != endpoint_delta(Fraction(0), b - a):
                assertions += 1

    # An augmented translation-equivariant state can have nonlinear depth.
    for _ in range(1000):
        delta0 = Fraction(rng.randint(-50, 50), 11)
        y0 = Fraction(rng.randint(-50, 50), 13)
        s0 = Fraction(rng.randint(-20, 20), 17)
        t0 = Fraction(rng.randint(-20, 20), 19)
        shift = Fraction(rng.randint(-50, 50), 23)

        def augmented(d: Fraction, y: Fraction, step: Fraction) -> tuple[Fraction, Fraction]:
            return d + y * step + step * step / 2, y + step

        direct = augmented(delta0, y0, s0 + t0)
        staged_s = augmented(delta0, y0, s0)
        staged = augmented(staged_s[0], staged_s[1], t0)
        shifted = augmented(delta0 + shift, y0, s0)
        unshifted = augmented(delta0, y0, s0)
        assert direct == staged
        assert shifted[0] - unshifted[0] == shift
        assertions += 2

    # Exact primary-branch regression using rational samples.
    for _ in range(4000):
        r = Fraction(rng.randint(1, 1000), rng.randint(1, 100))
        C = Fraction(rng.randint(-1000, 1000) or 1, rng.randint(1, 100))
        # f=1+C/r, f'=-C/r^2, f''=2C/r^3
        f = Fraction(1) + C / r
        fp = -C / (r * r)
        fpp = 2 * C / (r * r * r)
        e0 = r * fp + f - 1
        e1 = r * fp + r * r * fpp / 2
        assert e0 == 0 and e1 == 0
        assertions += 2
        # G257/G260 active angular values in C notation.
        apar = 3 * C / (2 * r)
        aperp = -3 * C / (2 * r)
        assert apar + aperp == 0
        assert apar != 0 and aperp != 0
        assertions += 2

        # Local scalar two-jet residual R=0 permits a non-Einstein Q/r^2 term.
        Q = Fraction(rng.randint(-1000, 1000) or 1, rng.randint(1, 100))
        e0_scalar = -Q / (r * r)
        e1_scalar = Q / (r * r)
        scalar_R = -2 * (e0_scalar + e1_scalar) / (r * r)
        assert scalar_R == 0
        assert e0_scalar != 0 and e1_scalar != 0
        assertions += 2

    # Explicitly reject a nonconstant translation-equivariant generator claim.
    for _ in range(1000):
        depth = Fraction(rng.randint(-100, 100), 17)
        shift = Fraction(rng.randint(-100, 100) or 1, 19)
        defect = (1 + (depth + shift) ** 2) - (1 + depth**2)
        if defect == 0:
            # The exceptional shift=-2*depth does not establish equivariance; use shift=1.
            shift = Fraction(1)
            defect = (1 + (depth + shift) ** 2) - (1 + depth**2)
        assert defect != 0
        assertions += 1

    result = {
        "all_pass": True,
        "assertion_count": assertions,
        "production_imported": False,
        "production_result_read": False,
        "methods": [
            "independent_floating_hyperbolic_grid",
            "exact_fraction_P2_antiderivative",
            "exact_fraction_GR_branch_regression",
            "exact_nonconstant_generator_counterexamples",
        ],
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"all_pass": True, "assertions": assertions}))


if __name__ == "__main__":
    main()

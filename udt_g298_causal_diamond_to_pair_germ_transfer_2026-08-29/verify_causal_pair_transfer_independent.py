#!/usr/bin/env python3
"""Independent exact-rational G298 verification; reads no production code or result."""

from fractions import Fraction
import json
from pathlib import Path
import random
import sys


OUT = Path(__file__).resolve().parent / "INDEPENDENT_VERIFICATION.json"


def lorentz(v, w):
    total = -(v[0] * w[0])
    for j in range(1, 4):
        total += v[j] * w[j]
    return total


def times(c, v):
    return tuple(c * q for q in v)


def determinant3(a, b, c):
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - b[0] * (a[1] * c[2] - a[2] * c[1])
        + c[0] * (a[1] * b[2] - a[2] * b[1])
    )


def main():
    rng = random.Random(298)
    assertions = 0
    trials = 20000

    for _ in range(trials):
        rn = rng.randint(1, 29)
        rd = rng.randint(1, 29)
        r = Fraction(rn, rd)
        wx = Fraction(rng.randint(-12, 12), rng.randint(1, 13))
        wy = Fraction(rng.randint(-12, 12), rng.randint(1, 13))
        wnorm = wx * wx + wy * wy

        G = (r + 1 / r + r * wnorm) / 2
        longitudinal = G - 1 / r
        target_clock = (G, longitudinal, wx, wy)
        transported_source_ruler = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
        normalized_ray = (Fraction(1), Fraction(1), Fraction(0), Fraction(0))
        target_rate_clock = times(r, target_clock)

        assert lorentz(target_clock, target_clock) == -1
        assert lorentz(normalized_ray, normalized_ray) == 0
        assert -lorentz(normalized_ray, target_clock) == 1 / r
        assertions += 3

        q00 = lorentz(target_rate_clock, target_rate_clock)
        q01 = lorentz(target_rate_clock, transported_source_ruler)
        q11 = lorentz(transported_source_ruler, transported_source_ruler)
        determinant = q00 * q11 - q01 * q01

        assert q00 == -(r * r)
        assert q01 == r * longitudinal
        assert q11 == 1
        assert determinant == -(r * r) * (1 + longitudinal * longitudinal)
        assert determinant < 0
        assertions += 5

        local_target_ruler = tuple(r * normalized_ray[j] - target_clock[j] for j in range(4))
        assert lorentz(local_target_ruler, local_target_ruler) == 1
        assert lorentz(local_target_ruler, target_clock) == 0
        assert lorentz(target_rate_clock, local_target_ruler) == 0
        assertions += 3


        if wx != 0:
            # Algebraic projection witness only: the transported-source and target-local ruler
            # planes are not related by a pair-domain basis change because, together with the
            # common clock, they span rank three. This does not certify equal completeness.
            separator = determinant3(
                target_rate_clock[:3], transported_source_ruler[:3], local_target_ruler[:3]
            )
            assert separator == -(r * r) * wx
            assert separator != 0
            assertions += 2

        # W1 reads T^2=-q00=r^2, so the exponential depth variable is exactly r.
        assert -q00 == r * r
        assert q11 - q01 * q01 / q00 == 1 + longitudinal * longitudinal
        assert -determinant == r * r * (1 + longitudinal * longitudinal)
        assertions += 3

        # Affine rescaling is independently checked on the normalized ray and ratio.
        c = Fraction(rng.randint(1, 19), rng.randint(1, 19))
        scaled_ray = times(c, normalized_ray)
        recovered = times(1 / c, scaled_ray)
        assert recovered == normalized_ray
        assert (c * Fraction(1)) / (c / r) == r
        assertions += 2

    # Branch equivariance and active-screen non-collapse are separate exact controls.
    plus = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
    minus = (Fraction(0), Fraction(-1), Fraction(0), Fraction(0))
    branch_set = {plus, minus}
    image_set = {(v[0], -v[1], v[2], v[3]) for v in branch_set}
    assert image_set == branch_set
    assertions += 1

    r = Fraction(2)
    G0 = (r + 1 / r) / 2
    G1 = (r + 1 / r + r) / 2
    a0 = G0 - 1 / r
    a1 = G1 - 1 / r
    assert r * a0 != r * a1
    ray = (Fraction(1), Fraction(1), Fraction(0), Fraction(0))
    clock0 = (G0, a0, Fraction(0), Fraction(0))
    clock1 = (G1, a1, Fraction(1), Fraction(0))
    ruler0 = tuple(r * ray[j] - clock0[j] for j in range(4))
    ruler1 = tuple(r * ray[j] - clock1[j] for j in range(4))
    local0 = (lorentz(times(r, clock0), times(r, clock0)), lorentz(times(r, clock0), ruler0), lorentz(ruler0, ruler0))
    local1 = (lorentz(times(r, clock1), times(r, clock1)), lorentz(times(r, clock1), ruler1), lorentz(ruler1, ruler1))
    assert local0 == local1 == (-r * r, Fraction(0), Fraction(1))
    assertions += 2

    result = {
        "status": "PASS",
        "implementation_independence": "imports no production module and reads no production result",
        "trials": trials,
        "assertions": assertions,
        "branch_equivariance": "PASS",
        "active_screen_noncollapse": "PASS",
        "inequivalent_natural_plane_separator": "PASS",
        "verification_boundary": "algebraic projection witness only; does not certify equal completeness or physical ownership",
    }
    if "--no-write" not in sys.argv:
        OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Dependency-free exact-rational G212 reconstruction checks."""

from __future__ import annotations

import json
import os
import random
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "INDEPENDENT_VERIFICATION.json"
SEED = 212_20260822
TRIALS = 10_000


def main() -> None:
    rng = random.Random(SEED)
    assertions = 0

    for _ in range(TRIALS):
        # Independent pair-potential closure.
        p = [Fraction(rng.randint(-10_000, 10_000), rng.randint(1, 97)) for _ in range(5)]
        for i in range(5):
            for j in range(i + 1, 5):
                dij = p[j] - p[i]
                assert dij == -(p[i] - p[j])
                assertions += 1
        for i in range(5):
            for j in range(i + 1, 5):
                for k in range(j + 1, 5):
                    assert (p[j] - p[i]) + (p[k] - p[j]) == p[k] - p[i]
                    assertions += 1

        # Independent exact inversion of two generic completed clocks.
        while True:
            x = Fraction(rng.randint(1, 30), rng.randint(1, 30))
            y = Fraction(rng.randint(1, 30), rng.randint(1, 30))
            s1 = Fraction(rng.randint(0, 20), rng.randint(1, 20))
            s2 = Fraction(rng.randint(0, 20), rng.randint(1, 20))
            # Choose clocks in the regular stratum: R_i=C_i*x-S_i*y is positive.
            c1 = s1 * y / x + Fraction(rng.randint(1, 20), rng.randint(1, 20))
            c2 = s2 * y / x + Fraction(rng.randint(1, 20), rng.randint(1, 20))
            determinant = c2 * s1 - c1 * s2
            if determinant != 0:
                break
        r1 = c1 * x - s1 * y
        r2 = c2 * x - s2 * y
        assert r1 > 0
        assert r2 > 0
        assertions += 2
        x_reconstructed = (-s2 * r1 + s1 * r2) / determinant
        y_reconstructed = (-c2 * r1 + c1 * r2) / determinant
        assert x_reconstructed == x
        assert y_reconstructed == y
        assertions += 2

        # Independent constant-curvature substitution in the primary spherical frame.
        curvature = Fraction(rng.randint(-40, 40), rng.randint(1, 40))
        radius = Fraction(rng.randint(1, 40), rng.randint(1, 40))
        f = 1 - curvature * radius * radius
        first = -2 * curvature * radius
        second = -2 * curvature
        k_tr = -second / 2
        k_mixed = -first / (2 * radius)
        k_angular = (1 - f) / (radius * radius)
        assert k_tr == curvature
        assert k_mixed == curvature
        assert k_angular == curvature
        scalar = -second - 4 * first / radius + 2 * (1 - f) / (radius * radius)
        kretschmann = second * second + 4 * (first / radius) ** 2 + 4 * ((1 - f) / (radius * radius)) ** 2
        assert scalar == 12 * curvature
        assert kretschmann == 24 * curvature * curvature
        assertions += 5

    result = {
        "status": "PASS",
        "method": "dependency_free_fraction_pair_potentials_tomography_and_space_form_substitution",
        "seed": SEED,
        "trials": TRIALS,
        "assertions": assertions,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

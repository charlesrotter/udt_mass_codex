#!/usr/bin/env python3
"""Implementation-independent exact-rational verification for G297."""

from fractions import Fraction
import json
import random
from pathlib import Path


def main():
    rng = random.Random(2970829)
    assertions = 0
    cases = 0

    for _ in range(5000):
        q = Fraction(rng.randint(2, 1000), rng.randint(1, 999))
        if q == 1:
            q += Fraction(1, 997)
        gamma = (q * q + 1) / (2 * q)
        radar = 2 * q / (q * q + 1)
        assert radar * gamma == 1
        assert radar != q
        assert q != 1 / q
        assertions += 3
        cases += 1

    for _ in range(5000):
        p = Fraction(rng.randint(2, 1000), rng.randint(1, 999))
        if p == 1:
            p += Fraction(1, 991)
        ab = p
        ba = 1 / p
        mutual = 2 / (p + 1 / p)
        assert ab * ba == 1
        assert ab != mutual
        assert ba != mutual
        assertions += 3
        cases += 1

    for _ in range(5000):
        r = Fraction(rng.randint(1, 1000), rng.randint(1, 1000))
        w2 = Fraction(rng.randint(1, 1000), rng.randint(1, 1000))
        gamma = (r + 1 / r) / 2 + r * w2 / 2
        planar = 2 / (r + 1 / r)
        mutual = 1 / gamma
        assert 0 < mutual < planar <= 1
        reverse_gamma = (1 / r + r) / 2 + (1 / r) * (r * r * w2) / 2
        assert reverse_gamma == gamma
        assertions += 2
        cases += 1

    for _ in range(5000):
        T = Fraction(rng.randint(1, 1000), rng.randint(1, 1000))
        L = Fraction(rng.randint(1, 1000), rng.randint(1, 1000))
        beta = Fraction(rng.randint(-1000, 1000), rng.randint(1, 1000))
        h00 = -T * T
        h01 = -T * T * beta
        h11 = L * L - T * T * beta * beta
        determinant = h00 * h11 - h01 * h01
        density = T * L
        assert determinant == -(density * density)
        assert T * (L / density) == 1
        assertions += 2
        cases += 1

    saved_path = Path(__file__).with_name("DERIVATION_RESULT.json")
    saved = json.loads(saved_path.read_text(encoding="utf-8"))
    assert saved["all_pass"] is True
    assert saved["check_count"] >= 80
    assertions += 2

    result = {
        "all_pass": True,
        "cases": cases,
        "assertions": assertions,
        "method": "independent exact-rational randomized reconstruction; no production import",
    }
    Path(__file__).with_name("INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

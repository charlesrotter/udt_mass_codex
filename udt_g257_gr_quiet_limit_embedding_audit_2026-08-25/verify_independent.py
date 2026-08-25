#!/usr/bin/env python3
"""Independent exact-Fraction verification for G257; imports no production code/result."""

from __future__ import annotations

import json
import random
from fractions import Fraction as F
from pathlib import Path


OUT = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")


def main() -> None:
    rng = random.Random(257)
    assertions = 0
    cases = 0

    for _ in range(512):
        r = F(rng.randint(3, 100), rng.randint(1, 9))
        c = F(rng.randint(-9, 9), rng.randint(1, 9))
        if c == 0 or 1 + c / r <= 0:
            continue
        f = 1 + c / r
        fp = -c / r**2
        fpp = 2 * c / r**3
        e0 = r * fp + f - 1
        e1 = r * fp + r**2 * fpp / 2
        assert e0 == 0
        assert e1 == 0
        assertions += 2

        u = -c / r
        p = -u / (2 * (1 - u))
        zeta = u * (2 - u) / (2 * (1 - u) ** 2)
        e0_phi = f * (1 - 2 * p) - 1
        e1_phi = f * (2 * p**2 - 2 * p - zeta)
        a_parallel = f * (2 * p**2 + p - zeta)
        a_perp = 1 - f * (1 + p)
        assert e0_phi == 0
        assert e1_phi == 0
        assert a_parallel == -3 * u / 2
        assert a_perp == 3 * u / 2
        assert a_parallel + a_perp == 0
        assertions += 5
        cases += 1

    pair_cases = 0
    for _ in range(512):
        r_s = F(rng.randint(1, 8), rng.randint(1, 5))
        r_a = r_s + F(rng.randint(1, 30), rng.randint(1, 5))
        r_b = r_s + F(rng.randint(1, 30), rng.randint(1, 5))
        f_a = 1 - r_s / r_a
        f_b = 1 - r_s / r_b
        q_ab = f_b / f_a
        q_ba = f_a / f_b
        chi_ab = (f_a - f_b) / (f_a + f_b)
        chi_ba = (f_b - f_a) / (f_b + f_a)
        assert q_ab * q_ba == 1
        assert chi_ba == -chi_ab
        assertions += 2

        r_c = r_s + F(rng.randint(1, 30), rng.randint(1, 5))
        f_c = 1 - r_s / r_c
        q_bc = f_c / f_b
        q_ac = f_c / f_a
        assert q_ab * q_bc == q_ac
        assertions += 1
        pair_cases += 1

    result = {
        "status": "PASS",
        "method": "independent exact rational substitution and pair composition",
        "production_imported": False,
        "production_result_read": False,
        "vacuum_angular_cases": cases,
        "pair_composition_cases": pair_cases,
        "assertions": assertions,
        "verified": [
            "general f=1+C/r family zeros both independent vacuum components",
            "native phi-jet residuals vanish on the same family",
            "A_parallel=-3u/2 and A_perp=+3u/2",
            "q reversal and three-endpoint composition",
        ],
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

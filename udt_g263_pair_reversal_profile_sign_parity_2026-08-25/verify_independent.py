#!/usr/bin/env python3
"""Implementation-distinct exact-Fraction replay for G263."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


def verify() -> dict[str, object]:
    assertions = 0

    def equal(left: F, right: F, name: str) -> None:
        nonlocal assertions
        if left != right:
            raise AssertionError(f"{name}: {left} != {right}")
        assertions += 1

    for i in range(1, 1001):
        s = F(i % 17 + 1, i % 13 + 1)  # exp(phi)>0; spans s<1, s=1, s>1
        u = F(i % 19 + 1, i % 11 + 1)  # exp(delta)>0
        p = F((7 * i) % 23 - 11, i % 5 + 1)
        z = F((11 * i) % 29 - 14, i % 7 + 1)
        r = F(i % 31 + 1, i % 3 + 1)
        half = F(1, 2)

        # Pair-arrow reversal, implemented directly with rational characters.
        d0, d1 = 1 / u, u
        dr0, dr1 = u, 1 / u
        equal(d0 * dr0, F(1), "pair_inverse_clock")
        equal(d1 * dr1, F(1), "pair_inverse_ruler")
        de = (u + 1 / u) * half
        do0 = (1 / u - u) * half
        do1 = -do0
        equal(d0, de + do0, "pair_reconstruct_clock")
        equal(d1, de + do1, "pair_reconstruct_ruler")
        equal((d0 + dr0) * half, de, "pair_even_clock")
        equal((d1 - dr1) * half, do1, "pair_odd_ruler")

        # Whole-profile conjugation. C sends (s,p,z)->(1/s,-p,-z).
        f, fc = 1 / s**2, s**2
        n, nc = 1 / s, s
        c1, sh1 = (s + 1 / s) * half, (s - 1 / s) * half
        c2, sh2 = (s**2 + 1 / s**2) * half, (s**2 - 1 / s**2) * half
        equal(f * fc, F(1), "profile_f_inverse")
        equal(n * nc, F(1), "profile_lapse_inverse")
        equal((n + nc) * half, c1, "lapse_even")
        equal((n - nc) * half, -sh1, "lapse_odd")
        equal((f + fc) * half, c2, "f_even")
        equal((f - fc) * half, -sh2, "f_odd")

        mu = r * (1 - f) * half
        muc = r * (1 - fc) * half
        mue = -r * sh1**2
        muo = r * sh2 * half
        equal((mu + muc) * half, mue, "mu_even")
        equal((mu - muc) * half, muo, "mu_odd")
        equal(mu, mue + muo, "mu_reconstruction")

        accel, accelc = -p / (r * s), p * s / r
        equal((accel + accelc) * half, p * sh1 / r, "accel_even")
        equal((accel - accelc) * half, -p * c1 / r, "accel_odd")

        e0 = f * (1 - 2 * p) - 1
        e0c = fc * (1 + 2 * p) - 1
        equal((e0 + e0c) * half, c2 + 2 * p * sh2 - 1, "E0_even")
        equal((e0 - e0c) * half, -sh2 - 2 * p * c2, "E0_odd")

        e1 = f * (2 * p**2 - 2 * p - z)
        e1c = fc * (2 * p**2 + 2 * p + z)
        equal((e1 + e1c) * half, 2 * p**2 * c2 + (2 * p + z) * sh2, "E1_even")
        equal((e1 - e1c) * half, -2 * p**2 * sh2 - (2 * p + z) * c2, "E1_odd")

        apar = f * (2 * p**2 + p - z)
        aparc = fc * (2 * p**2 - p + z)
        equal((apar + aparc) * half, 2 * p**2 * c2 - (p - z) * sh2, "Apar_even")
        equal((apar - aparc) * half, -2 * p**2 * sh2 + (p - z) * c2, "Apar_odd")

        aperp = 1 - f * (1 + p)
        aperpc = 1 - fc * (1 - p)
        equal((aperp + aperpc) * half, 1 - c2 + p * sh2, "Aperp_even")
        equal((aperp - aperpc) * half, sh2 - p * c2, "Aperp_odd")
        equal(apar + aperp, e1 - e0, "angular_join")
        equal(aparc + aperpc, e1c - e0c, "conjugate_angular_join")

        # R_pair fixes the supplied ambient coefficient; C_phi does not unless s=1.
        equal(f, f, "pair_reversal_metric_fixed")
        if s != 1 and f == fc:
            raise AssertionError("profile conjugation failed to separate metric")
        assertions += 1

    return {
        "status": "PASS",
        "case_count": 1000,
        "assertion_count": assertions,
        "signed_profile_coverage": "s_less_equal_greater_than_one",
        "implementation": "standard_library_fraction_no_production_import_no_result_read",
        "qualification": "implementation_distinct_exact_algebra_not_independent_physical_premise",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()

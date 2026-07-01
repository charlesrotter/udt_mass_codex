"""Candidate audit for the angular-source coupling eta.

The attractive value eta=1/18 can be written as

    eta = 1 / (2 N^2),  N = 2 ell + 1 = 3.

This script compares simple angular normalization candidates and their
consequences for the admissibility cap and ell=1 endpoint exponent.

No candidate is promoted here. The output is an audit target list.
"""

from __future__ import annotations

import math


def p_soft(source: float):
    disc = 1.0 - 8.0 * source
    if disc < 0.0:
        return None
    return 0.5 * (1.0 - math.sqrt(disc))


def main() -> None:
    n = 3
    candidates = {
        "1/(2N^2), N=3": 1.0 / (2.0 * n * n),
        "1/(N^2), N=3": 1.0 / (n * n),
        "1/(4N), N=3": 1.0 / (4.0 * n),
        "1/(8N), N=3": 1.0 / (8.0 * n),
        "critical ell1 1/16": 1.0 / 16.0,
        "1/(4pi)": 1.0 / (4.0 * math.pi),
        "1/(2pi^2)": 1.0 / (2.0 * math.pi * math.pi),
    }

    print("Eta candidate audit")
    print("lambda_cap=1/(8 eta); ell1 lambda=2; ell2 lambda=6")
    print()
    for name, eta in candidates.items():
        cap = 1.0 / (8.0 * eta)
        p_ell1 = p_soft(eta * 2.0)
        p_ell2 = p_soft(eta * 6.0)
        ell1_status = "allowed" if eta * 2.0 < 1.0 / 8.0 else "edge/excluded"
        ell2_status = "allowed" if eta * 6.0 < 1.0 / 8.0 else "edge/excluded"
        print(name)
        print(f"  eta={eta:.10g} lambda_cap={cap:.8g}")
        print(f"  ell1: {ell1_status:13s} p={p_ell1}")
        print(f"  ell2: {ell2_status:13s} p={p_ell2}")
        print()

    print("verdict:")
    print("  eta=1/(2N^2) with N=3 uniquely gives 1/18 in this list")
    print("  and cleanly admits ell=1 while excluding ell=2")
    print("  but deriving N=3 and the 1/2 factor at the source-action level")
    print("  remains required")


if __name__ == "__main__":
    main()


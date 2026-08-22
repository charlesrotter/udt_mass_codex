#!/usr/bin/env python3
"""High-precision boundary diagnostics for the G208 witness and sharp bound."""

from __future__ import annotations

import json
import os
from pathlib import Path

import mpmath as mp


OUT = Path(__file__).with_name("BOUNDARY_DIAGNOSTICS.json")


def phi(r: mp.mpf, n: int, a: mp.mpf, r0: mp.mpf) -> mp.mpf:
    x = r / r0
    return a * x**2 * (x**2 - 1) ** n / (2**n)


def diagnose() -> dict[str, object]:
    # The s=50 subtraction cancels roughly 174 decimal digits.
    mp.mp.dps = 240
    profiles = []
    for n, a_text in ((3, "1"), (3, "10"), (5, "1"), (7, "0.5")):
        a = mp.mpf(a_text)
        r0 = mp.mpf(1)
        integrand = lambda r: mp.exp(-2 * phi(r, n, a, r0))
        cutoff = mp.mpf(3)
        finite_segment = mp.quad(integrand, [r0, cutoff])
        # For x>=sqrt(2), phi >= a*x^(2n+2)/2^(2n).
        power = 2 * n + 2
        decay = a / (2 ** (2 * n - 1))
        lower = cutoff / r0
        tail_upper = (
            r0
            * mp.gammainc(mp.mpf(1) / power, decay * lower**power, mp.inf)
            / (power * decay ** (mp.mpf(1) / power))
        )
        finite_upper = finite_segment + tail_upper
        if not (finite_upper > 0 and mp.isfinite(finite_upper)):
            raise AssertionError("finite optical witness upper bound")
        center_ratio = 4 * a * (-1) ** n / (2**n * r0**2)
        numerical_ratio = 4 * phi(mp.mpf("1e-20"), n, a, r0) / mp.mpf("1e-40")
        if abs(numerical_ratio - center_ratio) > mp.mpf("1e-35"):
            raise AssertionError("smooth center coefficient")
        profiles.append(
            {
                "n": n,
                "a": a_text,
                "integral_f_finite_segment": mp.nstr(finite_segment, 80),
                "analytic_tail_upper": mp.nstr(tail_upper, 80),
                "spiral_optical_length_upper": mp.nstr(mp.sqrt(2) * finite_upper, 80),
                "center_sigma_over_r2": mp.nstr(center_ratio, 60),
            }
        )

    bound_checks = []
    for s_text in ("1e-40", "0.1", "1", "10", "50"):
        s = mp.mpf(s_text)
        C = mp.cosh(2 * s)
        S = mp.sinh(2 * s)
        schur = C - S * S / C
        target = 1 / C
        rel = abs(schur - target) / target
        if rel > mp.mpf("1e-100"):
            raise AssertionError("high-precision Schur cancellation")
        bound_checks.append(
            {
                "s": s_text,
                "sqrt_cosh_2s": mp.nstr(mp.sqrt(C), 70),
                "relative_schur_error": mp.nstr(rel, 10),
            }
        )

    return {
        "status": "PASS",
        "precision_digits": mp.mp.dps,
        "profile_count": len(profiles),
        "profiles": profiles,
        "bound_checks": bound_checks,
        "claim": "the preregistered center-regular sigma=4phi spiral has finite optical length",
    }


def main() -> None:
    result = diagnose()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()

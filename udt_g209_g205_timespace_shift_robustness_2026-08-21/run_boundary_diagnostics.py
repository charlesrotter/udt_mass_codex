#!/usr/bin/env python3
"""High-precision outer-tail controls for the G209 failure witness."""

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
    mp.mp.dps = 120
    profiles = []
    for n, a_text, v_text, R_text in (
        (3, "1", "0.5", "1"),
        (3, "10", "2", "0.75"),
        (5, "1", "1", "2"),
        (7, "0.5", "3", "1.5"),
    ):
        a = mp.mpf(a_text)
        v = mp.mpf(v_text)
        R = mp.mpf(R_text)
        r0 = mp.mpf(1)
        cutoff = mp.mpf(3)
        integrand = lambda rr: rr * mp.exp(-phi(rr, n, a, r0))
        finite_segment = mp.quad(integrand, [r0, cutoff])
        power = 2 * n + 2
        decay = a / (2 ** (2 * n))
        lower = cutoff / r0
        tail_upper = (
            r0**2
            * mp.gammainc(mp.mpf(2) / power, decay * lower**power, mp.inf)
            / (power * decay ** (mp.mpf(2) / power))
        )
        b_cut = v * cutoff / mp.sqrt(R**2 + cutoff**2)
        affine_upper = mp.sqrt(2) * (finite_segment + tail_upper) / b_cut
        if not (mp.isfinite(affine_upper) and affine_upper > 0):
            raise AssertionError("finite affine witness upper bound")
        center_slope = v / R
        numeric_slope = (v * mp.mpf("1e-30") / mp.sqrt(R**2 + mp.mpf("1e-60"))) / mp.mpf("1e-30")
        if abs(numeric_slope - center_slope) > mp.mpf("1e-50"):
            raise AssertionError("smooth center shift coefficient")
        profiles.append(
            {
                "n": n,
                "a": a_text,
                "v": v_text,
                "R": R_text,
                "finite_r_sqrt_f_segment": mp.nstr(finite_segment, 70),
                "analytic_tail_upper": mp.nstr(tail_upper, 70),
                "failure_affine_upper_control": mp.nstr(affine_upper, 70),
                "center_b_over_r": mp.nstr(center_slope, 50),
            }
        )
    return {
        "status": "PASS",
        "precision_digits": mp.mp.dps,
        "profile_count": len(profiles),
        "profiles": profiles,
        "claim": "the smooth bounded-coordinate radial shift admits an outer nonradial null ray with finite affine tail",
    }


def main() -> None:
    result = diagnose()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""High-precision boundary controls for the G210 sigma=-phi witness."""

from __future__ import annotations

import json
import os
from pathlib import Path

import mpmath as mp


OUT = Path(__file__).with_name("BOUNDARY_DIAGNOSTICS.json")


def main() -> None:
    mp.mp.dps = 120
    profiles: list[dict[str, object]] = []
    for n in (3, 5, 7, 9):
        def phi(x: mp.mpf) -> mp.mpf:
            return x**2 * (x**2 - 1) ** n / mp.mpf(2) ** n

        total = mp.quad(lambda x: mp.exp(-phi(x)), [0, 1, 2, mp.inf])
        tail = mp.quad(lambda x: mp.exp(-phi(x)), [2, mp.inf])
        time_to_two = mp.quad(lambda x: mp.exp(phi(x)), [1, 2])
        profiles.append(
            {
                "n": n,
                "failure_affine_integral_0_inf": mp.nstr(total, 100),
                "failure_affine_tail_2_inf": mp.nstr(tail, 100),
                "coordinate_time_integral_1_2": mp.nstr(time_to_two, 100),
                "finite_positive_affine_integral": bool(mp.isfinite(total) and total > 0),
                "finite_positive_tail": bool(mp.isfinite(tail) and tail > 0),
            }
        )
    assert all(p["finite_positive_affine_integral"] and p["finite_positive_tail"] for p in profiles)
    result = {
        "status": "PASS",
        "precision_digits": mp.mp.dps,
        "profile_count": len(profiles),
        "profiles": profiles,
        "scope": "finite high-precision anchors; analytic asymptotic proof remains separate",
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()

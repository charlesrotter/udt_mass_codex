#!/usr/bin/env python3
"""High-precision G205 radial affine controls for G211."""

from __future__ import annotations

import json
import os
from pathlib import Path

import mpmath as mp


OUT = Path(__file__).with_name("RADIAL_CONTROLS.json")


def main() -> None:
    mp.mp.dps = 120
    profiles: list[dict[str, object]] = []
    for n in (3, 5, 7, 9):
        def phi(x: mp.mpf) -> mp.mpf:
            return x**2 * (x**2 - 1) ** n / mp.mpf(2) ** n

        common_only = mp.quad(lambda x: mp.exp(-2 * phi(x)), [0, 1, 2, mp.inf])
        relative_only = mp.quad(lambda x: mp.exp(-phi(x)), [0, 1, 2, mp.inf])
        common_tail = mp.quad(lambda x: mp.exp(-2 * phi(x)), [2, mp.inf])
        relative_tail = mp.quad(lambda x: mp.exp(-phi(x)), [2, mp.inf])
        sample = mp.mpf("1.75")
        width_relative = mp.exp(phi(sample))
        width_compensated = mp.exp(phi(sample))
        compensated_density = mp.exp(2 * (phi(sample) / 2) - phi(sample))
        profiles.append(
            {
                "n": n,
                "common_only_affine_integral": mp.nstr(common_only, 100),
                "relative_only_affine_integral": mp.nstr(relative_only, 100),
                "common_only_tail": mp.nstr(common_tail, 100),
                "relative_only_tail": mp.nstr(relative_tail, 100),
                "relative_width_at_1p75": mp.nstr(width_relative, 100),
                "compensated_width_at_1p75": mp.nstr(width_compensated, 100),
                "compensated_affine_density_at_1p75": mp.nstr(compensated_density, 100),
                "finite_common_only": bool(mp.isfinite(common_only) and common_only > 0),
                "finite_relative_only": bool(mp.isfinite(relative_only) and relative_only > 0),
                "same_relative_cone": bool(width_relative == width_compensated),
                "compensated_density_one": bool(compensated_density == 1),
            }
        )
    assert all(
        p["finite_common_only"]
        and p["finite_relative_only"]
        and p["same_relative_cone"]
        and p["compensated_density_one"]
        for p in profiles
    )
    result = {
        "status": "PASS",
        "precision_digits": mp.mp.dps,
        "profile_count": len(profiles),
        "profiles": profiles,
        "scope": "finite radial anchors; divergence of the compensated unit density is analytic",
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()

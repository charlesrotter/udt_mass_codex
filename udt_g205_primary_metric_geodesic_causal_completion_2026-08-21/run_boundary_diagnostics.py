#!/usr/bin/env python3
"""High-precision finite-radius controls supporting, but not proving, G205 boundary theorems."""

from __future__ import annotations

import json
import os
from pathlib import Path

import mpmath as mp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "BOUNDARY_DIAGNOSTICS.json"


def main() -> None:
    mp.mp.dps = 80
    n = 3
    a = mp.mpf(1)
    start = mp.mpf("1.25")
    radii = [mp.mpf(value) for value in ("1.5", "1.75", "2.0")]

    def phi(r: mp.mpf) -> mp.mpf:
        return a * r**2 * (r**2 - 1) ** n / (2**n)

    def f(r: mp.mpf) -> mp.mpf:
        return mp.exp(-2 * phi(r))

    def timelike_integrand(r: mp.mpf) -> mp.mpf:
        energy = mp.mpf(2)
        angular = mp.mpf(1)
        return 1 / mp.sqrt(energy**2 - f(r) * (1 + angular**2 / r**2))

    def spacelike_e0_integrand(r: mp.mpf) -> mp.mpf:
        angular = mp.mpf(1)
        return 1 / mp.sqrt(f(r) * (1 - angular**2 / r**2))

    rows = []
    prior = None
    for radius in radii:
        row = {
            "r": mp.nstr(radius, 20),
            "phi": mp.nstr(phi(radius), 60),
            "f": mp.nstr(f(radius), 60),
            "radial_null_affine": mp.nstr(radius - start, 60),
            "timelike_affine": mp.nstr(mp.quad(timelike_integrand, [start, radius]), 60),
            "spacelike_E0_affine": mp.nstr(mp.quad(spacelike_e0_integrand, [start, radius]), 60),
            "optical_radial_length": mp.nstr(mp.quad(lambda value: 1 / f(value), [start, radius]), 60),
            "log10_spatial_integrand": mp.nstr(phi(radius) / mp.log(10), 60),
            "log10_optical_integrand": mp.nstr(2 * phi(radius) / mp.log(10), 60),
        }
        if prior is not None:
            assert mp.mpf(row["radial_null_affine"]) > mp.mpf(prior["radial_null_affine"])
            assert mp.mpf(row["timelike_affine"]) > mp.mpf(prior["timelike_affine"])
            assert mp.mpf(row["spacelike_E0_affine"]) > mp.mpf(prior["spacelike_E0_affine"])
            assert mp.mpf(row["optical_radial_length"]) > mp.mpf(prior["optical_radial_length"])
        rows.append(row)
        prior = row

    result = {
        "all_pass": True,
        "precision_digits": mp.mp.dps,
        "control": {"n": n, "a": "1", "r0": "1", "E_timelike": "2", "L": "1"},
        "rows": rows,
        "analytic_proof_controls": {
            "radial_null_affine": "r-r_start exactly",
            "nonzero_E": "radial velocity tends to abs(E)",
            "spacelike_E0": "affine integrand is at least exp(phi)",
            "optical": "radial integrand is exp(2phi)",
        },
        "scope": "finite numerical diagnostics only; analytic divergence proofs own the limits",
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""High-precision finite controls for the G207 analytic affine statements."""

from __future__ import annotations

import json
import os
from pathlib import Path

import mpmath as mp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "BOUNDARY_DIAGNOSTICS.json"


def main() -> None:
    mp.mp.dps = 100
    rc = mp.mpf("1.7")
    fc = mp.mpf("0.43")
    t0 = mp.mpf("2.3")
    angular_momentum = mp.mpf("0.91")
    exact = mp.sqrt(mp.pi) * rc * mp.sqrt(fc) * t0 / (2 * angular_momentum)
    cutoffs = [mp.mpf(v) for v in ("0.5", "1", "2", "4", "8")]
    rows = []
    previous = mp.mpf("0")
    for cutoff in cutoffs:
        partial = (
            rc
            * mp.sqrt(fc)
            * t0
            * mp.sqrt(mp.pi)
            * mp.erf(cutoff / t0)
            / (2 * angular_momentum)
        )
        tail = exact - partial
        assert partial > previous
        assert partial < exact
        assert tail > 0
        rows.append(
            {
                "t_cutoff": mp.nstr(cutoff, 20),
                "affine_partial": mp.nstr(partial, 60),
                "remaining_tail": mp.nstr(tail, 60),
            }
        )
        previous = partial

    # Finite controls for the center-regular bounded eigenvalue q=r^4 sin^2(theta)/(r0^4+r^4).
    r0 = mp.mpf("1.2")
    samples = []
    for radius in (mp.mpf("0"), mp.mpf("0.1"), mp.mpf("1"), mp.mpf("10"), mp.mpf("1e4")):
        for sine2 in (mp.mpf("0"), mp.mpf("0.25"), mp.mpf("1")):
            q = radius**4 * sine2 / (r0**4 + radius**4)
            assert 0 <= q < 1
            samples.append({"r": mp.nstr(radius, 20), "sin2": mp.nstr(sine2, 20), "q": mp.nstr(q, 60)})

    result = {
        "all_pass": True,
        "precision_digits": mp.mp.dps,
        "exact_failure_affine_future": mp.nstr(exact, 60),
        "gaussian_rows": rows,
        "bounded_screen_samples": samples,
        "scope": "finite high-precision controls only; analytic proofs own global and completeness claims",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()

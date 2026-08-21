#!/usr/bin/env python3
"""High-precision finite controls for the G206 analytic affine bounds.

The largest registered cutoff leaves a Gaussian tail below 1e-100.  We use
160 working digits so the strict partial-integral inequality is resolved
numerically rather than lost to cancellation at the originally attempted
80-digit precision.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import mpmath as mp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "BOUNDARY_DIAGNOSTICS.json"


def main() -> None:
    mp.mp.dps = 160
    epsilon = mp.mpf("0.2")
    r_start = mp.mpf("0.5")
    energy = mp.mpf("1.3")
    upper_constant = mp.e ** (4 * epsilon)

    def gaussian_weight(lam: mp.mpf) -> mp.mpf:
        return mp.e ** (-2 * (r_start + energy * lam) ** 2)

    exact_gaussian = mp.sqrt(mp.pi) * mp.erfc(mp.sqrt(2) * r_start) / (2 * mp.sqrt(2) * energy)
    cutoffs = [mp.mpf(value) for value in ("0.5", "1", "2", "4", "8")]
    rows = []
    previous = mp.mpf("0")
    previous_tail = exact_gaussian
    for cutoff in cutoffs:
        # Evaluate the strictly positive tail directly.  Computing it as
        # exact_gaussian - quadrature(partial) caused the original 80-digit
        # diagnostic to round the final tail to zero at cutoff 8.
        tail = (
            mp.sqrt(mp.pi)
            * mp.erfc(mp.sqrt(2) * (r_start + energy * cutoff))
            / (2 * mp.sqrt(2) * energy)
        )
        partial = exact_gaussian - tail
        assert tail > 0
        assert tail < previous_tail
        assert partial > previous
        assert partial < exact_gaussian
        rows.append(
            {
                "lambda_cutoff": mp.nstr(cutoff, 20),
                "failing_gaussian_partial": mp.nstr(partial, 60),
                "failing_registered_upper_partial": mp.nstr(upper_constant * partial, 60),
                "remaining_gaussian_tail": mp.nstr(tail, 80),
                "bounded_witness_affine_lower": mp.nstr(mp.e ** (-4 * epsilon) * cutoff, 60),
            }
        )
        previous = partial
        previous_tail = tail

    result = {
        "all_pass": True,
        "precision_digits": mp.mp.dps,
        "repair_note": "160 working digits avoid the preregistered cutoff-8 cancellation seen at 80 digits; theorem and witnesses unchanged",
        "epsilon": mp.nstr(epsilon, 20),
        "exact_gaussian_integral": mp.nstr(exact_gaussian, 60),
        "registered_failing_upper": mp.nstr(upper_constant * exact_gaussian, 60),
        "rows": rows,
        "scope": "finite high-precision controls only; analytic bounds own completeness classes",
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

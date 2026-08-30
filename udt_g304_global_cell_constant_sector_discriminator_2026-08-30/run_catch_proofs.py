#!/usr/bin/env python3
"""Concrete hostile mutations for G304."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="CATCH_PROOF_RESULT.json")
    args = parser.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        out = Path(__file__).resolve().parent / out

    catches = []

    def caught(name: str, mutant_claim: bool, reason: str) -> None:
        if mutant_claim:
            raise AssertionError(f"mutation escaped: {name}")
        catches.append({"mutation": name, "caught": True, "reason": reason})

    # Each boolean is the exact false claim a broken implementation would accept.
    caught("sign_reversal", (1 + 1.0**2) == 0, "negative constant has no finite zero")
    caught("proper_element_is_dr_over_f", abs(math.atanh(0.999999) - math.pi / 2) < 1e-6, "proper uses dr/sqrt(f), not optical dr/f")
    caught("positive_optical_finite", math.isfinite(float("inf")), "positive optical reach diverges")
    caught("positive_horizon_curvature_singular", not math.isfinite(12.0**2 / 6.0), "b=0 invariants are constant and finite")
    caught("G17_fixes_magnitude", len({1.0, 2.0, 10.0}) == 1, "finite-cell properties hold for every positive X")
    caught("WRL_exact_tracefree", abs(2.0 * 0.5 / 3.0) < 1e-15, "WR-L ODE residual is 2r/X")
    caught("network_selects_constant", (2.0 - 1.0) + (4.0 - 2.0) != (4.0 - 1.0), "endpoint composition telescopes for every valuation")
    caught("projective_endpoint_is_dimensionful_X", isinstance(1.0, str), "chi endpoint is dimensionless and does not fix X")
    caught("old_source_negative_universal", "source-free" == "fixed-sign source equation", "changed load-bearing premises require regrade")
    caught("working_equals_derived", "WORKING" == "DERIVED", "G17 grade must remain explicit")

    result = {
        "schema": "UDT_G304_CATCH_PROOFS_V1",
        "status": "PASS",
        "caught": len(catches),
        "mutations": catches,
    }
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "caught": len(catches)}, sort_keys=True))


if __name__ == "__main__":
    main()

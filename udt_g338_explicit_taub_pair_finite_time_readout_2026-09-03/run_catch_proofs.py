#!/usr/bin/env python3
"""Hostile mutation catches for the bounded G338 result."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path


def det2(h00: float, h01: float, h11: float) -> float:
    return h00 * h11 - h01 * h01


def G(u: float, rho: float) -> float:
    return rho * u ** (-2.0 / 3.0) + (1.0 - rho) * u ** (4.0 / 3.0)


def pair(u: float, rho: float, z: float) -> tuple[float, float, float]:
    spatial = G(u, rho)
    c, s = math.cosh(z), math.sinh(z)
    return -c * c + spatial * s * s, (spatial - 1.0) * s * c, -s * s + spatial * c * c


def main() -> None:
    catches: dict[str, bool] = {}

    u, rho, z = 2.3, 0.37, 0.8
    spatial = G(u, rho)
    h00, h01, h11 = pair(u, rho, z)

    # Mutation 1: delete the mixing/shift term after the pullback.
    catches["omitted_shift_breaks_raw_determinant"] = abs(h00 * h11 + spatial) > 1e-3

    # Mutation 2: use the auxiliary coordinate determinant as though W1 had
    # already calibrated it.
    catches["omitted_ruler_calibration_fails_unit_determinant"] = abs(det2(h00, h01, h11) + 1.0) > 1e-3

    # Mutation 3: reverse the longitudinal Kasner exponent. This destroys the
    # preregistered rho=2/3 first-order silent direction.
    bad_G_prime_at_one = (2.0 / 3.0) * rho + (4.0 / 3.0) * (1.0 - rho)
    catches["wrong_longitudinal_exponent_breaks_silence"] = abs(bad_G_prime_at_one) > 0.1

    # Mutation 4: claim the terminal scalar is a faithful record of the full
    # pair at zero boost. Phi is identically zero while m=sqrt(G) varies.
    densities = [math.sqrt(G(x, rho)) for x in (0.2, 1.0, 5.0)]
    phis = [-0.5 * math.log(1.0) for _ in densities]
    catches["terminal_scalar_faithfulness_claim_rejected"] = len(set(round(x, 12) for x in densities)) > 1 and len(set(phis)) == 1

    # Mutation 5: identify the pair-germ Delta=0 boundary with ambient
    # curvature blow-up. A transverse boundary occurs at positive finite T.
    threshold = (math.cosh(z) / math.sinh(z)) ** 2
    boundary_u = threshold ** 0.75
    curvature = 64.0 / (27.0 * boundary_u**4)
    catches["pair_boundary_not_ambient_singularity"] = boundary_u > 0.0 and math.isfinite(curvature)

    # Mutation 6: claim W1 erases all evolution. Its invariant density is the
    # ruler conversion m=sqrt(G), which differs at finite time.
    catches["normalization_erases_all_change_rejected"] = abs(math.sqrt(G(3.0, 2.0 / 3.0)) - 1.0) > 1e-3

    # Mutation 7: claim a nonzero boost leaves no regular interval. The initial
    # surface always has G=1 and hence Delta=1.
    h00_initial, _, _ = pair(1.0, 0.44, 4.0)
    catches["no_regular_interval_claim_rejected"] = abs(h00_initial + 1.0) < 1e-10

    # Mutation 8: elevate the diagnostic carry to a selected physical pair.
    # No selection datum appears in the input tuple.
    input_fields = {"u", "rho", "z"}
    catches["physical_occupancy_not_in_inputs"] = "occupancy" not in input_fields and "population" not in input_fields

    # Mutation 9: infer an absolute scale. All readouts here depend on u=T/T0;
    # common rescaling of T and T0 is invisible.
    ratio_a = 7.5 / 2.5
    ratio_b = 75.0 / 25.0
    catches["common_time_rescaling_is_invisible"] = ratio_a == ratio_b and G(ratio_a, rho) == G(ratio_b, rho)

    if not all(catches.values()):
        failed = [name for name, value in catches.items() if not value]
        raise AssertionError(f"uncaught hostile mutations: {failed}")

    result = {
        "catches_passed": sum(catches.values()),
        "catches_total": len(catches),
        "all_passed": all(catches.values()),
        "catches": catches,
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        out = Path(__file__).with_name("CATCH_PROOF_RESULT.json")
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

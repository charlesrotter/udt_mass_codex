#!/usr/bin/env python3
"""Mutation catches for the G265 landing. Writes no files."""

import json
import math


def main() -> None:
    caught = []

    f = 2.25
    optical = 1 / f
    proper = 1 / math.sqrt(f)
    caught.append(("optical_not_proper", abs(optical - proper) > 0.1))

    # Mutating the null density from 1/f to 1/sqrt(f) breaks g(k,k)=0.
    c = 3.0
    kt_mut = 1 / (c * math.sqrt(f))
    null_residual = -f * c * c * kt_mut * kt_mut + 1 / f
    caught.append(("mutated_null_density", abs(null_residual) > 0.1))

    na, nb = 1.2, 2.0
    rab, rba = nb / na, na / nb
    caught.append(("signed_arrow_not_mutual", abs(rab - rba) > 0.5))
    caught.append(("reversal_inverse", abs(rab * rba - 1.0) < 1e-15))

    delta = 0.7
    caught.append(("signed_not_even", abs(math.exp(-delta) - 1 / math.cosh(delta)) > 0.1))
    caught.append(("even_is_reversal_invariant", abs(1 / math.cosh(delta) - 1 / math.cosh(-delta)) < 1e-15))

    # The nonconstant local p=-2/9 candidate fails the all-interval equation at fourth order.
    z = 0.1
    p = -2 / 9
    x = 1 + z
    m = (1 - 2 * p) / (1 - p) * (x ** (1 - p) - 1) / (
        x ** (p / 2) * (x ** (1 - 2 * p) - 1)
    )
    even = 1 / math.cosh(p * math.log(1 / x))
    caught.append(("false_nonconstant_sech_solution", abs(m - even) > 1e-8))

    # Infinite bare c adds exactly zero to a supplied metric delay and cannot change its profile.
    metric_delay = 4.2
    bare_inverse_speed = 0.0
    caught.append(("zero_bare_term_is_nonselective", metric_delay + bare_inverse_speed == metric_delay))

    failed = [name for name, ok in caught if not ok]
    assert not failed, failed
    print(json.dumps({"status": "PASS", "catches": len(caught), "names": [n for n, _ in caught]}, indent=2))


if __name__ == "__main__":
    main()

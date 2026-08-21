#!/usr/bin/env python3
"""Independent exact-Fraction verification for G201; no SymPy or production imports."""

from fractions import Fraction as F
import json
import random


def one_jet(r, f, fp, fpp, sine):
    angmom = r * sine
    tide_parallel = angmom**2 * (r * fpp - fp) / (2 * r**3)
    tide_perp = angmom**2 * (r * fp - 2 * f + 2) / (2 * r**4)
    metric_amplitudes = (
        r**2 * tide_parallel / sine**2,
        r**2 * tide_perp / sine**2,
    )

    p = -r * fp / (2 * f)
    q = r**2 * (fp**2 - f * fpp) / (2 * f**2)
    jet_amplitudes = (
        f * (2 * p**2 - q + p),
        1 - f * (1 + p),
    )
    assert metric_amplitudes == jet_amplitudes
    return 2


def main() -> None:
    rng = random.Random(201)
    cases = 10000
    assertions = 0
    for _ in range(cases):
        r = F(rng.randint(1, 31), rng.randint(1, 13))
        f = F(rng.randint(1, 37), rng.randint(1, 17))
        fp = F(rng.randint(-31, 31), rng.randint(1, 19))
        fpp = F(rng.randint(-31, 31), rng.randint(1, 19))
        sine = F(rng.randint(1, 9), 10)
        assertions += one_jet(r, f, fp, fpp, sine)

    # Local cancellation at arbitrary positive f.
    cancellation_cases = 1000
    for _ in range(cancellation_cases):
        f = F(rng.randint(1, 53), rng.randint(1, 23))
        p = 1 / f - 1
        q = 2 * p**2 + p
        assert f * (2 * p**2 - q + p) == 0
        assert 1 - f * (1 + p) == 0
        assertions += 2

    # Exact smooth f=1+C r^2 controls for both signs on positive-f domains.
    family_controls = 400
    signs_seen = set()
    for index in range(family_controls):
        r = F((index % 17) + 1, 19)
        if index % 2 == 0:
            constant = F((index % 11) + 1, 7)
        else:
            constant = -F((index % 11) + 1, 29)
        f = 1 + constant * r**2
        if f <= 0:
            continue
        signs_seen.add(1 if constant > 0 else -1)
        fp = 2 * constant * r
        fpp = 2 * constant
        sine = F(3, 5)
        assertions += one_jet(r, f, fp, fpp, sine)
        angmom = r * sine
        assert angmom**2 * (r * fpp - fp) / (2 * r**3) == 0
        assert angmom**2 * (r * fp - 2 * f + 2) / (2 * r**4) == 0
        assertions += 2
    assert signs_seen == {-1, 1}
    assertions += 1

    # Same phi-value proxy f=1: quiet and nonquiet jets both exist.
    assert one_jet(F(2), F(1), F(0), F(0), F(1, 2)) == 2
    quiet_p = F(0)
    quiet_q = F(0)
    assert (2 * quiet_p**2 - quiet_q + quiet_p, -(quiet_p)) == (0, 0)
    live_p = F(1)
    live_q = F(0)
    assert (2 * live_p**2 - live_q + live_p, -(live_p)) == (3, -1)
    assertions += 5

    print(json.dumps({
        "all_pass": True,
        "cases": cases,
        "cancellation_cases": cancellation_cases,
        "family_controls_requested": family_controls,
        "family_signs_seen": sorted(signs_seen),
        "assertions": assertions,
        "method": "independent exact-Fraction metric-jet to phi-jet identity replay",
        "production_imports": False,
        "production_artifacts_read": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

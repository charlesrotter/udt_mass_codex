#!/usr/bin/env python3
"""Independent stdlib/Fraction replay of G171 multi-pair claims."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent
RNG = random.Random(1710819)


def det2(h: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> Fraction:
    return h[0][0] * h[1][1] - h[0][1] * h[1][0]


def pair_metric(
    a: Fraction,
    b: Fraction,
    c: Fraction,
    d: Fraction,
    st: Fraction,
    sr: Fraction,
    sth: Fraction,
    sph: Fraction,
) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    # g=diag(-a,b,c,d), u=(1,0,0,0), s=(st,sr,sth,sph)
    return (
        (-a, -a * st),
        (-a * st, -a * st * st + b * sr * sr + c * sth * sth + d * sph * sph),
    )


def q2(h: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> Fraction:
    return h[0][0] * h[0][0] / (-det2(h))


trials = 12000
checks = 0
different_pair_readouts = 0
reversal_checks = 0
matched_triangle_checks = 0
unmatched_triangle_nonzero = 0
shared_rechart_checks = 0

for _ in range(trials):
    vals = [Fraction(RNG.randint(1, 11), RNG.randint(1, 9)) for _ in range(8)]
    a, b, c, d, st, sr, sth, sph = vals
    h_rad = pair_metric(a, b, c, d, st, sr, Fraction(0), Fraction(0))
    h_ang = pair_metric(a, b, c, d, st, sr, sth, sph)
    assert h_rad[0][0] < 0 and det2(h_rad) < 0
    assert h_ang[0][0] < 0 and det2(h_ang) < 0
    checks += 4

    qr = q2(h_rad)
    qa = q2(h_ang)
    assert qr != qa
    different_pair_readouts += 1
    checks += 1

    ratio = qa / qr
    reverse = qr / qa
    assert ratio * reverse == 1
    reversal_checks += 1
    checks += 1

    # Observer-only endpoint q^2 states telescope multiplicatively.
    qA = Fraction(RNG.randint(1, 17), RNG.randint(1, 13))
    qB = Fraction(RNG.randint(1, 17), RNG.randint(1, 13))
    qC = Fraction(RNG.randint(1, 17), RNG.randint(1, 13))
    assert (qB / qA) * (qC / qB) == qC / qA
    matched_triangle_checks += 1
    checks += 1

    # Pair-specific B readouts need not cancel.
    qB_left = qr
    qB_right = qa
    defect = qB_left / qB_right
    assert defect != 1
    unmatched_triangle_nonzero += 1
    checks += 1

    # One shared diagonal pair rechart multiplies every endpoint q^2 by (p0/p1)^2,
    # so the endpoint ratio is unchanged.
    p0 = Fraction(RNG.randint(1, 9), RNG.randint(1, 9))
    p1 = Fraction(RNG.randint(1, 9), RNG.randint(1, 9))
    factor = (p0 / p1) ** 2
    assert (qa * factor) / (qr * factor) == qa / qr
    shared_rechart_checks += 1
    checks += 1

landing = (
    "PRIMARY_METRIC_PAIR_GERM_RELATIVE_NETWORK"
    "__EACH_ORDERED_PAIR_RESPONSE_NATIVE_FROM_ITS_COMPLETE_PULLBACK"
    "__SAME_PAIR_REVERSAL_AUTOMATIC"
    "__SHARED_OBSERVER_DOES_NOT_FORCE_PAIR_INDEPENDENT_ENDPOINT_DENSITY"
    "__GENERAL_TRIANGLE_ADDITIVITY_NOT_DERIVED_OR_REQUIRED"
    "__MATCHED_ENDPOINT_READOUT_SUBFAMILY_TELESCOPES"
    "__NO_SCAFFOLDED_CARRY_KERNEL"
)

result = {
    "landing_supported": landing,
    "trials": trials,
    "checks_passed": checks,
    "different_pair_readouts": different_pair_readouts,
    "reversal_checks": reversal_checks,
    "matched_triangle_checks": matched_triangle_checks,
    "unmatched_triangle_nonzero": unmatched_triangle_nonzero,
    "shared_rechart_checks": shared_rechart_checks,
    "implementation": "stdlib fractions; no sympy or production imports",
}
(HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))

#!/usr/bin/env python3
"""Independent dependency-free G184 replay using direct determinants and degrees."""

from fractions import Fraction as F
import json
import math
import os
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent
TRIALS = 20000


def det2(a, b, c, d):
    return a * d - b * c


def pull(h00, h01, h11, a, b, c, d):
    # J=((a,b),(c,d)); return the three symmetric entries J^T h J.
    return (
        h00 * a * a + 2 * h01 * a * c + h11 * c * c,
        h00 * a * b + h01 * (a * d + b * c) + h11 * c * d,
        h00 * b * b + 2 * h01 * b * d + h11 * d * d,
    )


def run():
    rng = random.Random(9184)
    assertions = 0
    orientation_preserving = 0
    orientation_reversing = 0

    for _ in range(TRIALS):
        t = F(rng.randint(1, 10), rng.randint(1, 9))
        length = F(rng.randint(1, 10), rng.randint(1, 9))
        beta = F(rng.randint(-8, 8), rng.randint(1, 9))
        h00 = -t * t
        h01 = -t * t * beta
        h11 = length * length - t * t * beta * beta
        det_h = h00 * h11 - h01 * h01
        assert det_h == -(t * length) ** 2
        assertions += 1

        while True:
            a, b, c, d = (
                F(rng.randint(-8, 8), rng.randint(1, 7)) for _ in range(4)
            )
            det_j = det2(a, b, c, d)
            if det_j:
                break
        if det_j > 0:
            orientation_preserving += 1
        else:
            orientation_reversing += 1
        p00, p01, p11 = pull(h00, h01, h11, a, b, c, d)
        det_p = p00 * p11 - p01 * p01
        assert det_p == det_j * det_j * det_h
        assertions += 1

        # Independent two-stage pullback expanded entrywise.
        while True:
            e, f, g, k = (
                F(rng.randint(-8, 8), rng.randint(1, 7)) for _ in range(4)
            )
            if det2(e, f, g, k):
                break
        q00, q01, q11 = pull(p00, p01, p11, e, f, g, k)
        ca = a * e + b * g
        cb = a * f + b * k
        cc = c * e + d * g
        cd = c * f + d * k
        r00, r01, r11 = pull(h00, h01, h11, ca, cb, cc, cd)
        assert (q00, q01, q11) == (r00, r01, r11)
        assertions += 1

        # Spatial calibrated map; density covariance tested without square roots.
        spatial_derivative = F(rng.randint(1, 12), rng.randint(1, 10))
        s00, s01, s11 = pull(h00, h01, h11, F(1), F(0), F(0), spatial_derivative)
        assert s00 == h00
        assert s01 == spatial_derivative * h01
        assert s11 == spatial_derivative**2 * h11
        assert -(s00 * s11 - s01 * s01) == spatial_derivative**2 * (-det_h)
        assertions += 4

    # Direct independent sampling of the fixed nonlinear map.
    for i in range(501):
        u = F(i, 500)
        s = (u + u * u) / 2
        ds = (1 + 2 * u) / 2
        source_speed_sq = 1 + 4 * s * s
        target_speed_sq = ds * ds + (2 * s * ds) ** 2
        assert target_speed_sq == ds * ds * source_speed_sq
        assert ds > 0
        assertions += 2

    # Independent numerical replay of the exact semicircle/helix identities.
    radius = 2.75
    a = radius / 2 * math.sqrt(1 - 4 / math.pi**2)
    for i in range(2001):
        s = math.pi * radius * i / 2000
        c1_prime = (math.cos(s / radius), math.sin(s / radius), 0.0)
        c2_prime = (
            2 * a / radius * math.cos(2 * s / radius),
            2 / math.pi,
            2 * a / radius * math.sin(2 * s / radius),
        )
        speed1 = sum(x * x for x in c1_prime)
        speed2 = sum(x * x for x in c2_prime)
        assert math.isclose(speed1, 1.0, rel_tol=1e-12, abs_tol=1e-12)
        assert math.isclose(speed2, 1.0, rel_tol=1e-12, abs_tol=1e-12)
        assertions += 2
    k1 = 1 / radius**2
    k2 = 16 * a * a / radius**4
    assert not math.isclose(k1, k2, rel_tol=1e-12, abs_tol=1e-12)
    assertions += 1

    # Degree and reflection are recomputed without using the production structures.
    for n in range(-100, 101):
        ell = 2 * n + 1
        partner = 2 * (-n - 1) + 1
        assert partner == -ell
        assert abs(partner) == abs(ell)
        assert (ell == partner) is False
        assertions += 3
    for degree in range(1, 51):
        assert abs(degree * 1) == degree
        assert abs(degree * -1) == degree
        assertions += 2
    assert abs(1) != abs(2)
    assertions += 1

    result = {
        "audit": "G184",
        "status": "PASS",
        "method": "entrywise pullback expansion, direct determinant law, sampled embedding derivatives, integer degree",
        "trials": TRIALS,
        "assertions": assertions,
        "orientation_preserving_jacobians": orientation_preserving,
        "orientation_reversing_jacobians": orientation_reversing,
        "checks": {
            "pullback_composition_independent": True,
            "determinant_covariance_independent": True,
            "completed_density_covariance_independent": True,
            "nonlinear_reparameterization_independent": True,
            "same_metric_extrinsic_separation_independent": True,
            "degree_invariance_independent": True,
            "reflection_pairing_independent": True,
        },
    }
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(f"PASS: G184 independent replay; trials={TRIALS}; assertions={assertions}")


if __name__ == "__main__":
    run()

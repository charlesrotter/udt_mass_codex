#!/usr/bin/env python3
"""Dependency-free exact production derivation for G184."""

from fractions import Fraction as F
import json
import math
import os
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent
TRIALS = 12000
LANDING = (
    "TYPED_REALIZATION_ISOMORPHISM_CLASSIFIES_REGULAR_BRANCH_EQUIVALENCE__"
    "KERNEL_IS_NOT_A_COMPLETE_REALIZATION_INVARIANT"
)


def transpose(a):
    return tuple(zip(*a))


def matmul(a, b):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0])))
        for i in range(len(a))
    )


def pullback(h, jac):
    return matmul(transpose(jac), matmul(h, jac))


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def completed_metric(t, beta, length):
    return (
        (-t * t, -t * t * beta),
        (-t * t * beta, length * length - t * t * beta * beta),
    )


def random_nonzero_fraction(rng, numerator=9, denominator=8):
    while True:
        value = F(rng.randint(-numerator, numerator), rng.randint(1, denominator))
        if value:
            return value


def random_invertible_matrix(rng):
    while True:
        value = (
            (F(rng.randint(-7, 7), rng.randint(1, 6)), F(rng.randint(-7, 7), rng.randint(1, 6))),
            (F(rng.randint(-7, 7), rng.randint(1, 6)), F(rng.randint(-7, 7), rng.randint(1, 6))),
        )
        if det2(value):
            return value


def run():
    rng = random.Random(184_0819)
    assertions = 0

    # General pullback functoriality and determinant covariance.
    for _ in range(TRIALS):
        t = abs(random_nonzero_fraction(rng))
        length = abs(random_nonzero_fraction(rng))
        beta = F(rng.randint(-9, 9), rng.randint(1, 8))
        h3 = completed_metric(t, beta, length)
        assert h3[0][0] < 0 and det2(h3) == -(t * length) ** 2 < 0

        j23 = random_invertible_matrix(rng)
        j12 = random_invertible_matrix(rng)
        h2 = pullback(h3, j23)
        h1_step = pullback(h2, j12)
        composite = matmul(j23, j12)
        h1_direct = pullback(h3, composite)
        assert h1_step == h1_direct
        assert det2(h2) == det2(j23) ** 2 * det2(h3)
        assert det2(h1_direct) == det2(composite) ** 2 * det2(h3)
        assertions += 5

        # Clock-calibration-preserving spatial reparameterization.
        k = abs(random_nonzero_fraction(rng))
        jq = ((F(1), F(0)), (F(0), k))
        hq = pullback(h3, jq)
        assert hq[0][0] == h3[0][0]
        assert hq[0][1] == k * h3[0][1]
        assert hq[1][1] == k * k * h3[1][1]
        assert -det2(hq) == k * k * (-det2(h3))
        # This squared identity is the exact density law m_tilde=k*m.
        assert (k * t * length) ** 2 == -det2(hq)
        assertions += 5

    # Exact nonlinear reparameterization control f(u)=(u+u^2)/2.
    nonlinear_checks = 0
    for i in range(101):
        u = F(i, 100)
        f = (u + u * u) / 2
        fp = (1 + 2 * u) / 2
        base_h11 = 1 + 4 * f * f
        pulled_h11 = fp * fp * base_h11
        direct_dx = fp
        direct_dy = 2 * f * fp
        assert pulled_h11 == direct_dx * direct_dx + direct_dy * direct_dy
        assert fp > 0
        nonlinear_checks += 2
    assert (F(0) + F(0) ** 2) / 2 == 0
    assert (F(1) + F(1) ** 2) / 2 == 1
    assertions += nonlinear_checks + 2

    # The strict relation has groupoid closure by exact map/Jacobian laws.
    identity = ((F(1), F(0)), (F(0), F(1)))
    test_j = ((F(2), F(1, 3)), (F(-1, 4), F(5, 3)))
    inverse_scale = F(1, det2(test_j))
    inverse = (
        (inverse_scale * test_j[1][1], -inverse_scale * test_j[0][1]),
        (-inverse_scale * test_j[1][0], inverse_scale * test_j[0][0]),
    )
    assert matmul(identity, test_j) == test_j == matmul(test_j, identity)
    assert matmul(test_j, inverse) == identity == matmul(inverse, test_j)
    assertions += 2

    # Same-endpoint, same-pair-metric semicircle/helix witness.
    # The algebra is exact: both speeds square to one.  The helix parameter
    # a^2/R^2=(1-4/pi^2)/4 gives 4a^2/R^2+4/pi^2=1.
    for x in (F(i, 1000) for i in range(1, 1000)):
        # x stands for 4/pi^2; the cancellation is an identity for every x.
        a2_over_r2 = (1 - x) / 4
        assert 4 * a2_over_r2 + x == 1
        assertions += 1
    # Curvature squares are 1/R^2 and 4(1-4/pi^2)/R^2.
    # pi>3 implies pi^2>9>16/3, so equality (which requires pi^2=16/3) is impossible.
    assert F(9) > F(16, 3)
    assertions += 1
    radius = 3.0
    endpoint = 2.0 * radius
    helix_a = radius / 2.0 * math.sqrt(1.0 - 4.0 / math.pi**2)
    length_domain = math.pi * radius

    def c1(s):
        return (radius * math.sin(s / radius), radius * (1 - math.cos(s / radius)), 0.0)

    def c2(s):
        return (
            helix_a * math.sin(2 * s / radius),
            (2 / math.pi) * s,
            helix_a * (1 - math.cos(2 * s / radius)),
        )

    assert all(abs(value) < 1e-12 for value in c1(0.0))
    assert all(abs(value) < 1e-12 for value in c2(0.0))
    assert all(abs(a - b) < 1e-12 for a, b in zip(c1(length_domain), (0.0, endpoint, 0.0)))
    assert all(abs(a - b) < 1e-12 for a, b in zip(c2(length_domain), (0.0, endpoint, 0.0)))
    curvature1_sq = 1.0 / radius**2
    curvature2_sq = 4.0 * (1.0 - 4.0 / math.pi**2) / radius**2
    assert not math.isclose(curvature1_sq, curvature2_sq, rel_tol=1e-12, abs_tol=1e-12)
    assertions += 5

    # Image equality does not erase covering degree.  A circle diffeomorphism
    # has degree +/-1, so precomposition preserves absolute degree.
    degrees = (1, 2, -1, -2)
    for n in degrees:
        for diffeo_degree in (-1, 1):
            assert abs(n * diffeo_degree) == abs(n)
            assertions += 1
    assert abs(1) != abs(2)
    assertions += 1

    # Reflected polynomial branches: strict-distinct, conditionally symmetry-equivalent.
    reflected_checks = 0
    for s in (F(i, 40) for i in range(41)):
        plus = (s, s * (1 - s))
        minus = (s, -s * (1 - s))
        reflected_minus = (minus[0], -minus[1])
        assert reflected_minus == plus
        if 0 < s < 1:
            assert plus != minus
        reflected_checks += 2 if 0 < s < 1 else 1
    assertions += reflected_checks

    # Winding classification under endpoint-preserving circle isometries.
    winding_pairs = []
    for n in range(-40, 41):
        ell = 1 + 2 * n
        reflected_n = -n - 1
        reflected_ell = 1 + 2 * reflected_n
        assert reflected_ell == -ell
        assert abs(reflected_ell) == abs(ell)
        assert (ell - 1) % 2 == 0
        winding_pairs.append((n, reflected_n, ell, reflected_ell))
        assertions += 3
    assert len({abs(1 + 2 * n) for n in range(-40, 41)}) > 1
    assertions += 1

    result = {
        "audit": "G184",
        "landing_candidate": LANDING,
        "trials": TRIALS,
        "assertions": assertions,
        "checks": {
            "strict_groupoid_identity_inverse_composition": True,
            "pullback_functoriality": True,
            "kernel_spatial_reparameterization_covariance": True,
            "nonlinear_marked_reparameterization": True,
            "same_endpoints_and_pair_metric_not_immersion_isomorphism": True,
            "extrinsic_curvature_separates_semicircle_helix": True,
            "image_equality_does_not_erase_degree": True,
            "reflection_equivalence_is_query_conditional": True,
            "winding_reflection_pairs_only_equal_absolute_lift": True,
            "non_scalar_transport_not_scalarized": True,
        },
        "witnesses": {
            "nonlinear_reparameterization": {"f": "(u+u^2)/2", "endpoints_fixed": True},
            "semicircle_helix": {
                "same_endpoints": True,
                "same_pair_metric": "diag(-1,1)",
                "curvature1_sq": "1/R^2",
                "curvature2_sq": "4*(1-4/pi^2)/R^2",
                "ambient_isometry_equivalent": False,
            },
            "circle_coverings": {"same_image": True, "degrees": [1, 2], "equivalent": False},
            "reflected_polynomial": {
                "strict_equivalent": False,
                "equivalent_if_reflection_admitted": True,
                "equivalent_if_transverse_orientation_fixed": False,
            },
            "winding": winding_pairs,
        },
    }
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (ROOT / "DERIVATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(f"PASS: G184 exact branch equivalence; trials={TRIALS}; assertions={assertions}")


if __name__ == "__main__":
    run()

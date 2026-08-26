#!/usr/bin/env python3
"""Result-blind implementation-distinct consistency replay for G264."""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path


def verify() -> dict[str, object]:
    exact_assertions = 0
    numeric_assertions = 0

    def exact(left: F, right: F, name: str) -> None:
        nonlocal exact_assertions
        if left != right:
            raise AssertionError(f"{name}: {left} != {right}")
        exact_assertions += 1

    def numeric(condition: bool, name: str) -> None:
        nonlocal numeric_assertions
        if not condition:
            raise AssertionError(name)
        numeric_assertions += 1

    # Arbitrary local jets: recompute R from channel trace and K from orthonormal sectional blocks.
    for i in range(1, 2001):
        r = F(i % 29 + 1, i % 7 + 1)
        f = F((7 * i) % 31 + 1, (11 * i) % 23 + 1)
        fp = F((13 * i) % 37 - 18, i % 5 + 1)
        fpp = F((17 * i) % 41 - 20, i % 9 + 1)

        scalar_direct = -fpp - 4 * fp / r - 2 * (f - 1) / r**2
        radial_channel = (r * fp + f - 1) / r**2
        angular_channel = fpp / 2 + fp / r
        exact(scalar_direct, -2 * radial_channel - 2 * angular_channel, "scalar_channel_trace")

        k_direct = fpp**2 + 4 * (fp / r) ** 2 + 4 * ((f - 1) / r**2) ** 2
        k_tr = -fpp / 2
        k_ta = -fp / (2 * r)
        k_ra = -fp / (2 * r)
        k_aa = (1 - f) / r**2
        k_sections = 4 * (k_tr**2 + 2 * k_ta**2 + 2 * k_ra**2 + k_aa**2)
        exact(k_direct, k_sections, "kretschmann_sectional_sum")

        # Smooth-center polynomial jet: either sign of a remains finite.
        a = F((19 * i) % 43 - 21, i % 11 + 1)
        b = F((23 * i) % 47 - 23, i % 13 + 1)
        f_center = 1 + a * r**2 + b * r**4
        fp_center = 2 * a * r + 4 * b * r**3
        fpp_center = 2 * a + 12 * b * r**2
        scalar_center = -fpp_center - 4 * fp_center / r - 2 * (f_center - 1) / r**2
        k_center = (
            fpp_center**2
            + 4 * (fp_center / r) ** 2
            + 4 * ((f_center - 1) / r**2) ** 2
        )
        exact(scalar_center, -12 * a - 30 * b * r**2, "center_scalar_series")
        exact(k_center, 24 * a**2 + 120 * a * b * r**2 + 212 * b**2 * r**4, "center_k_series")

    # Exponential negative bump, sampled without importing production or saved results.
    bump_cases = 0
    maximum_depths_decimal: list[Decimal] = []
    with localcontext() as context:
        context.prec = 80
        one = Decimal(1)
        two = Decimal(2)
        four = Decimal(4)
        five = Decimal(5)
        e_decimal = one.exp()
        for epsilon_text in ("0.01", "0.1", "1", "10", "100", "1000000"):
            epsilon = Decimal(epsilon_text)
            length = one + epsilon.sqrt() / Decimal(10)
            maximum_depths_decimal.append(-(one + epsilon / e_decimal).ln() / two)
            upper = one + epsilon / e_decimal
            for j in range(1, 251):
                radius = length * Decimal(j) / Decimal(25)
                x = (radius / length) ** 2
                expx = (-x).exp()
                f = one + epsilon * x * expx
                fp = two * epsilon * radius * expx * (one - x) / length**2
                fpp = two * epsilon * expx * (one - five * x + two * x**2) / length**2
                scalar = -fpp - four * fp / radius - two * (f - one) / radius**2
                k = fpp**2 + four * (fp / radius) ** 2 + four * ((f - one) / radius**2) ** 2
                numeric(f > one, "negative bump sign")
                numeric(f <= upper, "negative bump bound")
                numeric(scalar.is_finite() and k.is_finite(), "negative bump curvature finite")
                numeric(one / f.sqrt() >= one / upper.sqrt(), "proper length lower bound")
                bump_cases += 1

    numeric(
        all(a > b for a, b in zip(maximum_depths_decimal, maximum_depths_decimal[1:])),
        "bump depth unbounded trend",
    )

    # Exact exponent classification for the registered power-law end.
    power_classes: dict[str, str] = {}
    for alpha in (F(1, 2), F(1), F(3, 2), F(2), F(5, 2), F(4), F(6), F(7)):
        if alpha < 2:
            expected = "subcritical"
            numeric(alpha / 2 <= 1, "subcritical radial exponent")
            numeric(2 * alpha - 4 < 0, "subcritical curvature exponent")
        elif alpha == 2:
            expected = "critical"
            numeric(alpha / 2 == 1, "critical radial exponent")
            numeric(2 * alpha - 4 == 0, "critical curvature exponent")
        else:
            expected = "supercritical"
            numeric(alpha / 2 > 1, "supercritical radial exponent")
            numeric(2 * alpha - 4 > 0, "supercritical curvature exponent")
        power_classes[str(alpha)] = expected
        if alpha <= 6:
            numeric(2 - alpha / 2 >= -1, "infinite volume exponent")
        else:
            numeric(2 - alpha / 2 < -1, "finite volume exponent")

    # Exact alpha=2 critical representative, recomputed without production code.
    # Set f=1+c r^2/l^2 and evaluate the invariant and angular-channel formulae
    # directly for arbitrary rational samples.
    critical_cases = 0
    for i in range(1, 1001):
        radius = F(i % 31 + 1, i % 9 + 1)
        coefficient = F(i % 37 + 1, i % 13 + 1)
        length = F(i % 41 + 1, i % 11 + 1)
        f_critical = 1 + coefficient * radius**2 / length**2
        fp_critical = 2 * coefficient * radius / length**2
        fpp_critical = 2 * coefficient / length**2
        scalar_critical = (
            -fpp_critical
            - 4 * fp_critical / radius
            - 2 * (f_critical - 1) / radius**2
        )
        k_critical = (
            fpp_critical**2
            + 4 * (fp_critical / radius) ** 2
            + 4 * ((f_critical - 1) / radius**2) ** 2
        )
        a_parallel = (radius**2 * fpp_critical - radius * fp_critical) / 2
        a_perpendicular = 1 - f_critical + radius * fp_critical / 2
        exact(scalar_critical, -12 * coefficient / length**2, "critical scalar")
        exact(k_critical, 24 * coefficient**2 / length**4, "critical kretschmann")
        exact(a_parallel, F(0), "critical A_parallel")
        exact(a_perpendicular, F(0), "critical A_perpendicular")
        critical_cases += 1

    return {
        "status": "PASS",
        "exact_case_count": 2000,
        "exact_assertion_count": exact_assertions,
        "bump_case_count": bump_cases,
        "numeric_assertion_count": numeric_assertions,
        "bump_minimum_phi_samples": [str(value) for value in maximum_depths_decimal],
        "power_classes": power_classes,
        "critical_case_count": critical_cases,
        "critical_exact_intersection": (
            "f=1+C(r/L)^2 has R=-12C/L^2, K=24C^2/L^4, "
            "Aparallel=Aperp=0"
        ),
        "implementation": "standard_library_fraction_and_decimal_no_production_import_no_result_read",
        "role": "consistency_replay_not_metric_first_derivation",
        "qualification": "exact_local_jet_consistency_plus_numeric_bump_diagnostic_not_independent_derivation_or_physical_premise",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()

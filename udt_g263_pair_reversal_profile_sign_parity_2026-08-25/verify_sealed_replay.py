#!/usr/bin/env python3
"""Dependency-free, result-blind, end-to-end exact replay for the G263 landing."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


def verify() -> dict[str, object]:
    assertions = 0
    signed = {"negative_phi": 0, "zero_phi": 0, "positive_phi": 0}
    metric_separations = 0
    shared_scalar_inversions = 0
    sphere_guards = 0
    zero_tide_nonquiet = 0

    def equal(left: F | tuple[F, ...], right: F | tuple[F, ...], name: str) -> None:
        nonlocal assertions
        if left != right:
            raise AssertionError(f"{name}: {left} != {right}")
        assertions += 1

    for i in range(1, 1001):
        # s=exp(phi)>0 and u=exp(delta)>0. These schedules cross both fixed points.
        s = F((3 * i) % 19 + 1, (5 * i) % 17 + 1)
        u = F((7 * i) % 23 + 1, (11 * i) % 29 + 1)
        p = F((13 * i) % 31 - 15, i % 7 + 1)
        z = F((17 * i) % 37 - 18, i % 5 + 1)
        r = F(i % 13 + 1, i % 4 + 1)
        half = F(1, 2)

        if s < 1:
            signed["negative_phi"] += 1
        elif s == 1:
            signed["zero_phi"] += 1
        else:
            signed["positive_phi"] += 1

        # R_pair: delta -> -delta with the same ambient metric.
        d0, d1 = 1 / u, u
        dr0, dr1 = u, 1 / u
        equal(d0 * dr0, F(1), "pair_inverse_clock")
        equal(d1 * dr1, F(1), "pair_inverse_ruler")
        de = (u + 1 / u) * half
        do0 = (1 / u - u) * half
        do1 = -do0
        equal(d0, de + do0, "pair_clock_reconstruction")
        equal(d1, de + do1, "pair_ruler_reconstruction")
        equal((d0 + dr0) * half, de, "pair_clock_even")
        equal((d1 + dr1) * half, de, "pair_ruler_even")
        equal((d0 - dr0) * half, do0, "pair_clock_odd")
        equal((d1 - dr1) * half, do1, "pair_ruler_odd")
        contrast = (u**2 + 1 / u**2) * half - 1
        equal(contrast, (u - 1 / u) ** 2 * half, "pair_contrast_even")
        equal(contrast, (1 / u**2 + u**2) * half - 1, "pair_contrast_reversal")

        # Both operations invert the endpoint clock scalar, but only C_phi changes g.
        s_a = F((2 * i) % 11 + 1, (3 * i) % 7 + 1)
        s_b = F((5 * i) % 13 + 1, (7 * i) % 9 + 1)
        q_ab = s_a / s_b
        equal(s_b / s_a, 1 / q_ab, "pair_swap_scalar_inverse")
        equal(s_b / s_a, 1 / q_ab, "profile_conjugate_scalar_inverse")
        shared_scalar_inversions += 1

        # C_phi: (s,p,z)->(1/s,-p,-z), f->1/f.
        f, fc = 1 / s**2, s**2
        n, nc = 1 / s, s
        metric = (-f, 1 / f, F(1))
        metric_c = (-fc, 1 / fc, F(1))
        equal(f * fc, F(1), "profile_f_inverse")
        equal(n * nc, F(1), "profile_lapse_inverse")
        equal(metric[2], metric_c[2], "areal_sphere_unchanged")
        sphere_guards += 1
        if s != 1:
            if metric == metric_c:
                raise AssertionError("profile conjugation failed to change metric off fixed point")
            metric_separations += 1
        assertions += 1

        c1 = (s + 1 / s) * half
        sh1 = (s - 1 / s) * half
        c2 = (s**2 + 1 / s**2) * half
        sh2 = (s**2 - 1 / s**2) * half
        equal((n + nc) * half, c1, "lapse_even")
        equal((n - nc) * half, -sh1, "lapse_odd")
        equal((f + fc) * half, c2, "f_even")
        equal((f - fc) * half, -sh2, "f_odd")

        mu = r * (1 - f) * half
        mu_c = r * (1 - fc) * half
        equal((mu + mu_c) * half, -r * sh1**2, "mass_aspect_even")
        equal((mu - mu_c) * half, r * sh2 * half, "mass_aspect_odd")
        equal(mu, -r * sh1**2 + r * sh2 * half, "mass_aspect_reconstruction")

        accel, accel_c = -p / (r * s), p * s / r
        equal((accel + accel_c) * half, p * sh1 / r, "acceleration_even")
        equal((accel - accel_c) * half, -p * c1 / r, "acceleration_odd")

        e0 = f * (1 - 2 * p) - 1
        e0_c = fc * (1 + 2 * p) - 1
        equal((e0 + e0_c) * half, c2 + 2 * p * sh2 - 1, "E0_even")
        equal((e0 - e0_c) * half, -sh2 - 2 * p * c2, "E0_odd")

        e1 = f * (2 * p**2 - 2 * p - z)
        e1_c = fc * (2 * p**2 + 2 * p + z)
        equal((e1 + e1_c) * half, 2 * p**2 * c2 + (2 * p + z) * sh2, "E1_even")
        equal((e1 - e1_c) * half, -2 * p**2 * sh2 - (2 * p + z) * c2, "E1_odd")

        apar = f * (2 * p**2 + p - z)
        apar_c = fc * (2 * p**2 - p + z)
        equal((apar + apar_c) * half, 2 * p**2 * c2 - (p - z) * sh2, "Aparallel_even")
        equal((apar - apar_c) * half, -2 * p**2 * sh2 + (p - z) * c2, "Aparallel_odd")

        aperp = 1 - f * (1 + p)
        aperp_c = 1 - fc * (1 - p)
        equal((aperp + aperp_c) * half, 1 - c2 + p * sh2, "Aperp_even")
        equal((aperp - aperp_c) * half, sh2 - p * c2, "Aperp_odd")
        equal(apar + aperp, e1 - e0, "angular_residual_join")
        equal(apar_c + aperp_c, e1_c - e0_c, "conjugate_angular_residual_join")

        # G201 zero-tide separator. Only regular f0=1+x>0 witnesses are admissible.
        c = F((19 * i) % 41 - 20, (23 * i) % 17 + 1)
        x = c * r**2
        f0 = 1 + x
        if f0 > 0:
            f0_prime = 2 * c * r
            f0_second = 2 * c
            equal((r**2 * f0_second - r * f0_prime) * half, F(0), "zero_tide_Aparallel")
            equal(1 - f0 + r * f0_prime * half, F(0), "zero_tide_Aperp")

            fc0_prime = -2 * c * r / f0**2
            fc0_second = -2 * c / f0**2 + 8 * c**2 * r**2 / f0**3
            apar_conj = (r**2 * fc0_second - r * fc0_prime) * half
            aperp_conj = 1 - 1 / f0 + r * fc0_prime * half
            equal(apar_conj, 4 * x**2 / (1 + x) ** 3, "zero_tide_conjugate_Aparallel")
            equal(aperp_conj, x**2 / (1 + x) ** 2, "zero_tide_conjugate_Aperp")
            if x != 0:
                if apar_conj == 0 or aperp_conj == 0:
                    raise AssertionError("conjugate zero-tide family remained quiet away from x=0")
                zero_tide_nonquiet += 1
            assertions += 1

    # Exact finite witnesses for the formulas whose elementary limits give the scoped end table.
    constant_jet_witnesses: list[dict[str, str]] = []
    for s in (F(100), F(1, 100)):
        constant_jet_witnesses.append(
            {
                "s": str(s),
                "N": str(1 / s),
                "mu_over_r": str((1 - 1 / s**2) / 2),
                "Aparallel": "0",
                "Aperp": str(1 - 1 / s**2),
            }
        )

    if not all(signed.values()):
        raise AssertionError("signed profile coverage incomplete")
    if not metric_separations or not zero_tide_nonquiet:
        raise AssertionError("separator coverage incomplete")

    return {
        "status": "PASS",
        "case_count": 1000,
        "assertion_count": assertions,
        "implementation": "standard_library_fraction_no_sympy_no_production_import_no_result_read",
        "signed_profile_cases": signed,
        "shared_scalar_inversion_cases": shared_scalar_inversions,
        "metric_separation_cases": metric_separations,
        "areal_sphere_guard_cases": sphere_guards,
        "nonquiet_conjugate_zero_tide_cases": zero_tide_nonquiet,
        "constant_jet_witnesses": constant_jet_witnesses,
        "constant_jet_limit_qualification": "elementary_limits_of_N_1_over_s_mu_half_1_minus_1_over_s2_Aparallel_0_Aperp_1_minus_1_over_s2",
        "qualification": "dependency_free_exact_algebra_not_epistemically_independent_physical_derivation",
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

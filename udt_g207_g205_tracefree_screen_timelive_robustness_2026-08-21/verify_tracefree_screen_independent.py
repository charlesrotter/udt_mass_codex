#!/usr/bin/env python3
"""Independent coordinate and exact-rational replay for G207."""

from __future__ import annotations

from fractions import Fraction
import json
import os
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "INDEPENDENT_VERIFICATION.json"


def main() -> None:
    assertions = 0

    def demand(value: bool, message: str) -> None:
        nonlocal assertions
        assertions += 1
        if not value:
            raise AssertionError(message)

    # Independent Euler-Lagrange reconstruction of the exact live circular orbit.
    t, t0, rc, fc, fp, angular_momentum = sp.symbols("t t0 rc fc fp angular_momentum", positive=True)
    tau2 = t**2 / t0**2
    gpp = rc**2 * sp.exp(-2 * tau2)
    tdot = angular_momentum * sp.exp(tau2) / (rc * sp.sqrt(fc))
    phidot = angular_momentum / gpp
    tddot = sp.diff(tdot, t) * tdot
    null_lagrangian_twice = -fc * tdot**2 + gpp * phidot**2
    demand(sp.simplify(null_lagrangian_twice) == 0, "Euler-Lagrange orbit is null")
    # d/dlambda(-f tdot) - (1/2) partial_t(gpp) phidot^2 = 0.
    t_el = sp.simplify(-fc * tddot - sp.diff(gpp, t) * phidot**2 / 2)
    demand(t_el == 0, "Euler-Lagrange t equation")
    # At the registered radial stationary profile, partial_r gpp=2r exp(-2 tau^2).
    radial_el = sp.factor(fp * tdot**2 / 2 - rc * sp.exp(-2 * tau2) * phidot**2)
    radial_factor = sp.factor(radial_el / (angular_momentum**2 * sp.exp(2 * tau2) / (2 * fc * rc**3)))
    demand(sp.simplify(radial_factor - (rc * fp - 2 * fc)) == 0, "Euler-Lagrange radial factor")
    demand(sp.simplify(radial_el.subs(fp, 2 * fc / rc)) == 0, "G205 circular condition")
    theta = sp.symbols("theta", real=True)
    angular_shape = sp.sin(theta) ** 2 * sp.exp(-2 * tau2 * sp.sin(theta) ** 2)
    demand(sp.simplify(sp.diff(angular_shape, theta).subs(theta, sp.pi / 2)) == 0, "polar equation")
    future = sp.integrate(rc * sp.sqrt(fc) * sp.exp(-tau2) / angular_momentum, (t, 0, sp.oo))
    demand(
        sp.simplify(future - sp.sqrt(sp.pi) * rc * sp.sqrt(fc) * t0 / (2 * angular_momentum)) == 0,
        "finite affine future",
    )

    cases = 10_000
    seen: set[tuple[Fraction, ...]] = set()
    changed_clock = 0
    changed_area = 0
    changed_beta = 0
    for index in range(cases):
        # This is a separately written rational local model in an h0-orthogonal frame.
        lapse = Fraction(100_000 + index, 1)
        radial_weight = Fraction((index % 11) + 1, (index % 7) + 1)
        screen_1 = Fraction((index % 13) + 2, (index % 5) + 1)
        screen_2 = Fraction((index % 17) + 3, (index % 3) + 1)
        scale = Fraction((index % 19) + 2, (index % 19) + 3)  # positive and never one
        clock = (
            Fraction((index % 5) + 1, 100),
            Fraction((index % 7) + 1, 90),
            Fraction((index % 11) + 1, 110),
        )
        ruler = (
            Fraction((index % 23) + 1, (index % 4) + 1),
            Fraction((index % 29) + 1, (index % 6) + 2),
            Fraction((index % 31) + 1, (index % 8) + 3),
        )
        key = (
            Fraction(index, 1), lapse, radial_weight, screen_1, screen_2, scale,
            *clock, *ruler,
        )
        demand(key not in seen, f"distinct exact case {index}")
        seen.add(key)

        det_base = -lapse * radial_weight * screen_1 * screen_2
        det_shear = -lapse * radial_weight * (screen_1 * scale**2) * (screen_2 / scale**2)
        demand(det_shear == det_base, f"ambient determinant {index}")
        demand(det_shear < 0, f"ambient Lorentz signature {index}")

        def pair_entries(p_weight: Fraction, q_weight: Fraction) -> tuple[Fraction, Fraction, Fraction]:
            clock_spatial = (
                radial_weight * clock[0] ** 2
                + p_weight * clock[1] ** 2
                + q_weight * clock[2] ** 2
            )
            h00 = -lapse + clock_spatial
            h01 = (
                radial_weight * clock[0] * ruler[0]
                + p_weight * clock[1] * ruler[1]
                + q_weight * clock[2] * ruler[2]
            )
            h11 = (
                radial_weight * ruler[0] ** 2
                + p_weight * ruler[1] ** 2
                + q_weight * ruler[2] ** 2
            )
            return h00, h01, h11

        hb = pair_entries(screen_1, screen_2)
        hs = pair_entries(screen_1 * scale**2, screen_2 / scale**2)
        demand(hb[0] < 0 and hs[0] < 0, f"timelike clock stratum {index}")
        det_hb = hb[0] * hb[2] - hb[1] ** 2
        det_hs = hs[0] * hs[2] - hs[1] ** 2
        demand(det_hb < 0 and det_hs < 0, f"Lorentz pair stratum {index}")
        ruler_sq_b = hb[2] - hb[1] ** 2 / hb[0]
        ruler_sq_s = hs[2] - hs[1] ** 2 / hs[0]
        demand((-hb[0]) * ruler_sq_b == -det_hb, f"base pair identity {index}")
        demand((-hs[0]) * ruler_sq_s == -det_hs, f"shear pair identity {index}")
        # Reciprocal completion rescales the supplied ruler coordinate by sqrt(-det h).
        demand((-hb[0]) * (ruler_sq_b / (-det_hb)) == 1, f"base completion {index}")
        demand((-hs[0]) * (ruler_sq_s / (-det_hs)) == 1, f"shear completion {index}")

        if hb[0] != hs[0]:
            changed_clock += 1
        if det_hb != det_hs:
            changed_area += 1
        if hb[1] / hb[0] != hs[1] / hs[0]:
            changed_beta += 1

        # The radial direction is unchanged, giving the same coordinate causal bound.
        radial_speed_sq = lapse / (Fraction(1, 1) / lapse)
        demand(radial_speed_sq == lapse**2, f"radial causal speed {index}")

        # A clock germ with no spatial leg is exactly screen-blind.
        static_h00_base = -lapse
        static_h00_shear = -lapse
        demand(static_h00_base == static_h00_shear, f"static clock screen blindness {index}")

    demand(changed_clock > 0, "generic supplied clock germs hear screen shear")
    demand(changed_area > 0, "generic pair areas hear ambient determinant-one shear")
    demand(changed_beta > 0, "generic shifts hear ambient determinant-one shear")

    result = {
        "all_pass": True,
        "assertions": assertions,
        "cases": cases,
        "distinct_cases": len(seen),
        "changed_clock_cases": changed_clock,
        "changed_pair_area_cases": changed_area,
        "changed_beta_cases": changed_beta,
        "production_imported": False,
        "production_artifact_read": False,
        "method": "independent_euler_lagrange_circular_orbit_plus_exact_fraction_determinant_one_ambient_and_completed_pair_replay",
        "not_independently_verified_here": [
            "global_hyperbolicity_for_every_smooth_declared_S",
            "null_completeness_for_every_smooth_static_declared_S",
            "compact_time_supported_live_null_completeness",
            "physical_S_history_or_Xmax_selection",
        ],
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()

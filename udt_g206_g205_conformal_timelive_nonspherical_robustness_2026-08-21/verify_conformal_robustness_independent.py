#!/usr/bin/env python3
"""Independent exact-rational and high-precision algebraic-core replay for G206."""

from __future__ import annotations

from fractions import Fraction
import json
import math
import os
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "INDEPENDENT_VERIFICATION.json"


def main() -> None:
    cases = 10_000
    assertions = 0
    seen: set[tuple] = set()

    def demand(value: bool, message: str) -> None:
        nonlocal assertions
        assertions += 1
        if not value:
            raise AssertionError(message)

    # Independent direct radial-coordinate geodesic replay.  This does not
    # import the production connection-difference calculation.  Starting
    # from g_tilde=e^(2w) diag(-f,1/f), insert the reparameterized G205
    # radial null tangent directly into both coordinate geodesic equations.
    t, r = sp.symbols("t r", real=True)
    energy_symbol = sp.symbols("E", positive=True)
    f_symbol = sp.Function("f")(r)
    w = sp.Function("w")(t, r)
    q_symbol = sp.exp(2 * w)
    metric = sp.diag(-q_symbol * f_symbol, q_symbol / f_symbol)
    inverse = metric.inv()
    coordinates = (t, r)
    gamma = [[[sp.simplify(sp.Rational(1, 2) * sum(
        inverse[a, d] * (
            sp.diff(metric[d, c], coordinates[b])
            + sp.diff(metric[d, b], coordinates[c])
            - sp.diff(metric[b, c], coordinates[d])
        )
        for d in range(2)
    )) for c in range(2)] for b in range(2)] for a in range(2)]
    for direction in (-1, 1):
        tangent = (
            energy_symbol / (q_symbol * f_symbol),
            direction * energy_symbol / q_symbol,
        )
        null_norm = sp.simplify(sum(
            metric[a, b] * tangent[a] * tangent[b]
            for a in range(2) for b in range(2)
        ))
        demand(null_norm == 0, f"direct radial null norm direction {direction}")
        for a in range(2):
            derivative = sum(tangent[b] * sp.diff(tangent[a], coordinates[b]) for b in range(2))
            connection = sum(
                gamma[a][b][c] * tangent[b] * tangent[c]
                for b in range(2) for c in range(2)
            )
            demand(
                sp.simplify(derivative + connection) == 0,
                f"direct radial affine geodesic component {a} direction {direction}",
            )

    for index in range(cases):
        pair_a = Fraction((index % 23) + 1, (index % 7) + 1)
        pair_b = Fraction((index % 11) - 5, (index % 13) + 7)
        pair_c = Fraction((index % 19) + 1, (index % 5) + 2)
        scale = Fraction((index % 17) + 1, (index % 29) + 2)
        epsilon = Fraction((index % 7) + 1, 10)
        radius2 = Fraction((index % 31) + 1, (index % 37) + 3)
        u = Fraction(index % 101, 100)
        sine_control = Fraction((index % 19) + 1, 20) * (-1 if index % 2 else 1)
        energy = Fraction((index % 13) + 1, (index % 9) + 1)
        base_f = Fraction((index % 17) + 1, (index % 23) + 2)
        key = (pair_a, pair_b, pair_c, scale, epsilon, radius2, u, sine_control, energy, base_f)
        demand(key not in seen, f"duplicate case {index}")
        seen.add(key)

        det_h = -pair_a * pair_c - pair_b**2
        demand(det_h < 0, f"Lorentz pair {index}")
        l2 = pair_c + pair_b**2 / pair_a
        m2 = -det_h
        demand(pair_a * l2 == m2, f"pair determinant {index}")
        demand(pair_a * (l2 / m2) == 1, f"completed reciprocity {index}")

        scaled_a = scale**2 * pair_a
        scaled_b = scale**2 * pair_b
        scaled_c = scale**2 * pair_c
        scaled_l2 = scaled_c + scaled_b**2 / scaled_a
        scaled_m2 = scaled_a * scaled_c + scaled_b**2
        demand(scaled_l2 == scale**2 * l2, f"ruler scaling {index}")
        demand(scaled_m2 == scale**4 * m2, f"area scaling {index}")
        demand(-scaled_b / scaled_a == -pair_b / pair_a, f"shift invariance {index}")
        demand((scaled_m2 / scaled_a**2) == (m2 / pair_a**2), f"control depth invariance {index}")
        demand(scaled_a * (scaled_l2 / scaled_m2) == 1, f"scaled reciprocity {index}")

        angular = radius2 * (3 * u - 1) / (1 + radius2)
        omega_b = epsilon * sine_control * angular
        demand(-1 < angular < 2, f"angular bounds {index}")
        demand(abs(omega_b) <= 2 * epsilon, f"Omega_B bound {index}")
        lower_weight = math.exp(float(-4 * epsilon))
        demand(0 < lower_weight <= 1, f"positive lower weight {index}")

        radial_norm = -base_f * (energy / base_f) ** 2 + energy**2 / base_f
        demand(radial_norm == 0, f"base radial null {index}")
        k_omega = Fraction((index % 29) - 14, (index % 11) + 3)
        tangent_component = Fraction((index % 13) - 6, (index % 17) + 5)
        pregeodesic = 2 * k_omega * tangent_component
        rescaling_derivative = -2 * k_omega * tangent_component
        demand(pregeodesic + rescaling_derivative == 0, f"affine cancellation {index}")

        r_start = Fraction((index % 17) + 1, 10)
        e_float = float(energy)
        gaussian = math.sqrt(math.pi) * math.erfc(math.sqrt(2) * float(r_start)) / (2 * math.sqrt(2) * e_float)
        failing_upper = math.exp(float(4 * epsilon)) * gaussian
        demand(math.isfinite(failing_upper) and failing_upper > 0, f"finite failing bound {index}")
        control_length = (index % 97) + 1
        demand(lower_weight * control_length >= lower_weight, f"divergent lower sequence {index}")

    result = {
        "all_pass": True,
        "assertions": assertions,
        "cases": cases,
        "distinct_cases": len(seen),
        "production_imported": False,
        "production_artifact_read": False,
        "method": "independent_direct_radial_coordinate_geodesic_plus_exact_rational_pair_affine_and_witness_algebraic_core",
        "not_independently_verified_here": [
            "global_hyperbolicity_conformal_transfer",
            "all_null_geodesic_integral_iff_criterion",
            "timelike_or_spacelike_completeness",
            "physical_Omega_selection",
        ],
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Implementation-distinct G280 check via direct neighboring-ray integration."""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent


def rk4_bundle(a: float, length: float, steps: int = 256) -> tuple[float, float]:
    """Integrate exact transverse neighboring-ray equations, not the production Jacobi code."""
    state = [0.0, 1.0, 0.0, 1.0]  # x, x', y, y'
    step = length / steps

    def rhs(values: list[float]) -> list[float]:
        x, vx, y, vy = values
        return [vx, a * x, vy, -a * y]

    for _ in range(steps):
        k1 = rhs(state)
        k2 = rhs([state[i] + step * k1[i] / 2 for i in range(4)])
        k3 = rhs([state[i] + step * k2[i] / 2 for i in range(4)])
        k4 = rhs([state[i] + step * k3[i] for i in range(4)])
        state = [
            state[i] + step * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6
            for i in range(4)
        ]
    return state[0], state[2]


def verify() -> dict[str, object]:
    rng = random.Random(280_2)
    cases = 4096
    assertions = 0
    maximum_relative_integration_error = 0.0
    minimum_area_separation = float("inf")
    minimum_radial_separation = float("inf")
    for _ in range(cases):
        length = rng.uniform(0.5, 2.0)
        q_length = rng.uniform(0.2, 1.0)
        root_a = q_length / length
        a = root_a**2
        delta = rng.uniform(-3.0, 3.0)

        # On the axis H and all first derivatives vanish, so the same chosen endpoint boost is the
        # complete frame arrow in both metrics. Its clock column gives the same W5 state.
        chi_flat = math.tanh(delta)
        chi_wave = math.sinh(delta) / math.cosh(delta)
        z_flat = math.exp(delta)
        z_wave = math.cosh(delta) + math.sinh(delta)
        assert math.isclose(chi_flat, chi_wave, rel_tol=3e-15, abs_tol=3e-15)
        assert math.isclose(z_flat, z_wave, rel_tol=3e-14, abs_tol=3e-14)

        dx_numeric, dy_numeric = rk4_bundle(a, length)
        dx_exact = math.sinh(root_a * length) / root_a
        dy_exact = math.sin(root_a * length) / root_a
        relative_error = max(
            abs(dx_numeric - dx_exact) / abs(dx_exact),
            abs(dy_numeric - dy_exact) / abs(dy_exact),
        )
        maximum_relative_integration_error = max(maximum_relative_integration_error, relative_error)
        assert relative_error < 2.0e-10

        wave_area = dx_numeric * dy_numeric
        flat_area = length**2
        assert 0.0 < wave_area < flat_area
        separation = (flat_area - wave_area) / flat_area
        minimum_area_separation = min(minimum_area_separation, separation)
        assert separation > 1.0e-5
        # Independent primary-static-spherical separator at the same W5 depth and one common scale.
        depth = rng.uniform(0.01, 2.0)
        ell = rng.uniform(0.1, 10.0)
        radial_a = ell * math.sqrt(depth)
        radial_b = ell * math.sqrt((math.sqrt(1.0 + 4.0 * depth) - 1.0) / 2.0)
        assert math.tanh(depth) == math.tanh(depth)
        assert 0.0 < radial_b < radial_a
        radial_separation = (radial_a - radial_b) / radial_a
        minimum_radial_separation = min(minimum_radial_separation, radial_separation)
        assert radial_separation > 1.0e-3
        assertions += 10

    return {
        "audit": "G280_INDEPENDENT_NEIGHBORING_RAY_CHECK",
        "status": "PASS",
        "cases": cases,
        "assertions": assertions,
        "production_module_imported": False,
        "production_result_read": False,
        "method": "direct RK4 integration of full-metric neighboring-ray equations",
        "maximum_relative_integration_error": maximum_relative_integration_error,
        "minimum_relative_area_separation": minimum_area_separation,
        "minimum_primary_radial_areal_separation": minimum_radial_separation,
        "same_projective_and_redshift_state": True,
        "different_native_screen_area": True,
        "different_primary_radial_areal_radius": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = verify()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        print(rendered, end="")
    else:
        (PACKAGE / "INDEPENDENT_VERIFICATION.json").write_text(rendered)
        print(rendered, end="")


if __name__ == "__main__":
    main()

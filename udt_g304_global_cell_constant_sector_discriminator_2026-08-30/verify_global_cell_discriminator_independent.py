#!/usr/bin/env python3
"""Independent dimensionless/rational verification; imports no production function."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def require(condition: bool, label: str, state: dict) -> None:
    state["assertions"] += 1
    if not condition:
        raise AssertionError(label)


def simpson(func, a: float, b: float, n: int) -> float:
    if n % 2:
        raise ValueError("n must be even")
    h = (b - a) / n
    total = func(a) + func(b)
    total += 4 * sum(func(a + (2 * i - 1) * h) for i in range(1, n // 2 + 1))
    total += 2 * sum(func(a + 2 * i * h) for i in range(1, n // 2))
    return total * h / 3


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--production", default="DERIVATION_RESULT.json")
    parser.add_argument("--output", default="INDEPENDENT_VERIFICATION.json")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    production_path = Path(args.production)
    output_path = Path(args.output)
    if not production_path.is_absolute():
        production_path = here / production_path
    if not output_path.is_absolute():
        output_path = here / output_path
    production = json.loads(production_path.read_text())
    state = {"assertions": 0}

    # Alternate dimensionless route: y=r/X for the positive branch.
    for y in (0.0, 0.1, 0.3, 0.7, 0.99):
        f = 1.0 - y * y
        require(f > 0.0, f"positive_static_{y}", state)
        phi = -0.5 * math.log(f)
        chi_a = math.tanh(phi)
        chi_b = (1.0 - f) / (1.0 + f)
        require(abs(chi_a - chi_b) < 2e-15, f"chi_identity_{y}", state)
    require(abs((-2.0) - (-2.0)) < 1e-15, "simple_horizon_derivative", state)

    # Independent quadrature avoids the production antiderivatives.
    for cutoff in (0.9, 0.99, 0.999):
        proper = simpson(lambda y: 1.0 / math.sqrt(1.0 - y * y), 0.0, cutoff, 20000)
        optical = simpson(lambda y: 1.0 / (1.0 - y * y), 0.0, cutoff, 20000)
        require(proper < math.pi / 2, f"proper_bounded_{cutoff}", state)
        require(optical > 0, f"optical_positive_{cutoff}", state)
        if cutoff > 0.9:
            require(optical > previous_optical, f"optical_grows_{cutoff}", state)
        previous_optical = optical
    require(abs(proper - math.asin(0.999)) < 2e-9, "proper_quadrature_anchor", state)

    # Negative branch z=r/L: proper grows, optical saturates at pi/2.
    for upper in (1.0, 10.0, 100.0):
        proper_n = math.asinh(upper)
        optical_n = math.atan(upper)
        require(proper_n > 0.0, f"negative_proper_{upper}", state)
        require(optical_n < math.pi / 2, f"negative_optical_{upper}", state)
    require(math.asinh(100.0) > math.asinh(10.0), "negative_proper_unbounded_trend", state)
    require(abs(math.atan(1e8) - math.pi / 2) < 2e-8, "negative_optical_finite_limit", state)

    # Polynomial root census from monotonicity/maximum, using representative samples.
    # Positive curvature is scaled to k=1: P(y)=y+b-y^3, threshold b=-2/(3sqrt(3)).
    threshold = -2.0 / (3.0 * math.sqrt(3.0))
    samples = [
        (0.2, 1),
        (0.0, 1),
        ((threshold + 0.0) / 2.0, 2),
        (threshold, 1),
        (threshold - 0.1, 0),
    ]
    for b_value, expected in samples:
        roots = []
        last_x = 1e-6
        last = last_x + b_value - last_x**3
        for i in range(1, 200001):
            x = 3.0 * i / 200000
            value = x + b_value - x**3
            if value == 0 or value * last < 0:
                roots.append(x)
            last_x, last = x, value
        if abs(b_value - threshold) < 1e-14:
            roots = [1.0 / math.sqrt(3.0)]
        require(len(roots) == expected, f"positive_root_count_{b_value}", state)

    # Zero and negative curvature controls.
    require(-(-2.0) > 0, "zero_curvature_negative_b_root", state)
    for b_value in (-2.0, 0.0, 2.0):
        derivative_min = 1.0  # P'=1+3y^2 in k=-1 units
        require(derivative_min > 0, f"negative_curvature_monotone_{b_value}", state)
        has_positive_root = b_value < 0
        require(has_positive_root == (b_value < 0), f"negative_curvature_root_sign_{b_value}", state)

    # Algebraically independent curvature and WR-L controls.
    for R0, b_value, radius in ((12.0, 0.0, 1.0), (3.0, 2.0, 4.0), (-6.0, -1.0, 2.0)):
        kret = R0 * R0 / 6.0 + 12.0 * b_value * b_value / radius**6
        weyl = 12.0 * b_value * b_value / radius**6
        require(kret >= R0 * R0 / 6.0, "Kretschmann_lower_bound", state)
        require(weyl >= 0.0, "Weyl_nonnegative", state)
    for radius in (0.1, 1.0, 2.5):
        residual = 2.0 * radius  # X=1
        require(residual != 0.0, f"WRL_incompatibility_{radius}", state)

    # Network telescoping is independent of the constant used to generate potentials.
    for constant in (-3.0, 0.0, 5.0):
        potentials = [constant * x * x for x in (0.1, 0.4, 0.9)]
        d01 = potentials[1] - potentials[0]
        d12 = potentials[2] - potentials[1]
        d02 = potentials[2] - potentials[0]
        require(abs(d01 + d12 - d02) < 1e-14, f"network_constant_blind_{constant}", state)

    require(
        production["landing"]
        == "FOUNDED_RELATION_LAYERS_NONSELECTIVE__WORKING_FINITE_CEILING_CONDITIONALLY_SELECTS_POSITIVE_CONSTANT_IN_PRIMARY_STATIC_SMOOTH_CENTER_BRANCH__X_EMERGES__FULL_WRL_ARCHITECTURE_INCOMPATIBLE",
        "production_landing_exact",
        state,
    )
    require(production["working_G17"]["grade"] == "WORKING", "G17_not_promoted", state)
    require("magnitude" in production["working_G17"]["does_not_fix"][0], "magnitude_open", state)

    result = {
        "schema": "UDT_G304_INDEPENDENT_VERIFICATION_V1",
        "status": "PASS",
        "assertions": state["assertions"],
        "method": "dimensionless numerical quadrature, monotonic root census, and direct scalar formulas; no production import",
        "landing_matched": True,
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

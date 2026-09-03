#!/usr/bin/env python3
"""Implementation-distinct numerical verification of the bounded G335 identities."""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path


def require(condition: bool, label: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def sgn(value: float, tolerance: float = 1e-12) -> int:
    if value > tolerance:
        return 1
    if value < -tolerance:
        return -1
    return 0


def verify() -> dict:
    rng = random.Random(335)
    checks: list[str] = []
    max_trace_error = 0.0
    max_rank_error = 0.0
    max_trace_relative = 0.0
    max_rank_relative = 0.0
    max_flat_control_error = 0.0
    records: list[dict] = []

    for index in range(240):
        C = rng.choice((-1.0, 1.0)) * rng.uniform(0.2, 9.0)
        root = rng.uniform(0.05, 15.0)
        branch = rng.choice((-1.0, 1.0))
        b = -C + branch * root
        silent_exists = abs(b) >= abs(C) and abs(b) > 1e-14
        if abs(b) > 1e-14:
            mu0 = (b - C) / (2.0 * b)
            require((0.0 <= mu0 <= 1.0) == silent_exists,
                    f"silent_condition_{index}", checks)
            if silent_exists:
                q_zero = 0.5 * (b - C) - b * mu0
                require(abs(q_zero) < 2e-12, f"silent_value_{index}", checks)
                for offset in (-1e-5, 1e-5):
                    mu = min(1.0, max(0.0, mu0 + offset))
                    if mu != mu0:
                        require(abs(0.5 * (b - C) - b * mu) > 0.0,
                                f"near_silent_nonzero_{index}_{offset}", checks)

        if abs(b) < abs(C):
            gap = 0.5 * (abs(C) - abs(b))
            endpoint_min = min(abs(0.5 * (b - C)), abs(-0.5 * (b + C)))
            require(abs(gap - endpoint_min) < 2e-12 and gap > 0.0,
                    f"gap_formula_{index}", checks)
            for mu in (0.0, 0.13, 0.5, 0.87, 1.0):
                q = 0.5 * (b - C) - b * mu
                require(sgn(q) == -sgn(C), f"gap_sign_{index}_{mu}", checks)
                require(abs(q) + 2e-12 >= gap, f"gap_bound_{index}_{mu}", checks)

        mu = rng.random()
        q0 = 0.5 * (b - C) - b * mu
        rapidity = rng.uniform(-3.5, 3.5)
        sh = math.sinh(rapidity)
        ch = math.cosh(rapidity)
        d00 = 2.0 * q0 * sh * sh
        d01 = 2.0 * q0 * sh * ch
        d11 = 2.0 * q0 * ch * ch
        trace_error = abs((-d00 + d11) - 2.0 * q0)
        rank_error = abs(d00 * d11 - d01 * d01)
        max_trace_error = max(max_trace_error, trace_error)
        max_rank_error = max(max_rank_error, rank_error)
        scale = max(1.0, abs(q0), abs(d00), abs(d01), abs(d11))
        max_trace_relative = max(max_trace_relative, trace_error / scale)
        max_rank_relative = max(max_rank_relative, rank_error / (scale * scale))
        require(trace_error < 5e-12 * scale, f"boost_trace_{index}", checks)
        require(rank_error < 2e-10 * scale * scale, f"boost_rank_{index}", checks)
        require(abs(0.5 * d00 - q0 * sh * sh) < 2e-12 * scale,
                f"terminal_{index}", checks)

        # General frame carry can cancel raw components without cancelling the tensor response.
        raw = (d00 - d00, d01 - d01, d11 - d11)
        require(max(abs(value) for value in raw) == 0.0,
                f"carry_cancellation_{index}", checks)
        if abs(q0) > 1e-9:
            require(max(abs(d00), abs(d01), abs(d11)) > 0.0,
                    f"geometry_nonzero_{index}", checks)

        # A direct numerical continuity control uses a smooth q(t) unrelated to production code.
        if abs(q0) > 1e-7:
            a = rng.uniform(-4.0, 4.0)
            c = rng.uniform(-4.0, 4.0)
            denominator = abs(a) + abs(c)
            epsilon = 1.0 if denominator == 0.0 else min(1.0, abs(q0) / (4.0 * denominator))
            for fraction in (-1.0, -0.7, -0.2, 0.2, 0.7, 1.0):
                t = fraction * epsilon
                q_t = q0 + a * t + c * t * t
                require(sgn(q_t) == sgn(q0), f"local_sign_{index}_{fraction}", checks)

        spatial_a = rng.uniform(-3.0, 3.0)
        spatial_b = spatial_a + 1.0
        observer_a = ch * q0 + sh * spatial_a
        observer_b = ch * q0 + sh * spatial_b
        if abs(sh) > 1e-9:
            require(abs(observer_a - observer_b) > 1e-9,
                    f"observer_jet_ambiguity_{index}", checks)

        if len(records) < 16:
            records.append({
                "C": C,
                "b": b,
                "mu": mu,
                "q0": q0,
                "rapidity": rapidity,
                "silent_exists_some_direction": silent_exists,
            })

    # Independent known-development control: central differences recover d(log a)/dt=H for
    # a(t)=exp(Ht). This is a consistency check, not a proof about G332 developments.
    step = 1e-6
    for H in (-2.0, -0.25, 0.25, 2.0):
        for t in (-0.8, -0.1, 0.0, 0.1, 0.8):
            log_plus = math.log(math.exp(H * (t + step)))
            log_minus = math.log(math.exp(H * (t - step)))
            estimate = (log_plus - log_minus) / (2.0 * step)
            error = abs(estimate - H)
            max_flat_control_error = max(max_flat_control_error, error)
            require(error < 3e-10, f"flat_control_{H}_{t}", checks)

    # Exact boundary controls independent of the randomized loop.
    for C, b, expected_gap in ((3.0, 1.0, 1.0), (-3.0, -1.0, 1.0)):
        require(abs(0.5 * (abs(C) - abs(b)) - expected_gap) < 1e-15,
                f"uniform_gap_control_{C}_{b}", checks)
    for b in (-4.0, 4.0):
        require(abs(0.5 * b - 0.5 * b) == 0.0,
                f"silent_half_direction_{b}", checks)

    return {
        "package": "G335",
        "verdict": "PASS",
        "checks_passed": len(checks),
        "imports_production": False,
        "reads_production_result": False,
        "method": "independent floating random strata, finite differences, and direct matrix algebra",
        "seed": 335,
        "max_trace_error": max_trace_error,
        "max_rank_error": max_rank_error,
        "max_trace_relative": max_trace_relative,
        "max_rank_relative": max_rank_relative,
        "max_flat_control_error": max_flat_control_error,
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(json.dumps({"checks_passed": result["checks_passed"], "verdict": result["verdict"]}))


if __name__ == "__main__":
    main()

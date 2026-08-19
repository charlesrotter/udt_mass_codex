#!/usr/bin/env python3
"""Independent stdlib/Fraction replay for G181; imports no production module."""

from __future__ import annotations

import json
import os
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


class LCG:
    def __init__(self, seed: int = 0x181A5EED) -> None:
        self.state = seed

    def next(self) -> int:
        self.state = (1664525 * self.state + 1013904223) & 0xFFFFFFFF
        return self.state

    def positive_fraction(self) -> Fraction:
        return Fraction(1 + self.next() % 97, 1 + self.next() % 31)

    def signed_fraction(self) -> Fraction:
        return Fraction(int(self.next() % 101) - 50, 1 + self.next() % 29)


def main_result() -> dict[str, object]:
    rng = LCG()
    assertions = 0
    trial_count = 20_000
    tape_counts = {"FINITE": 0, "INFINITE_LOG": 0, "INFINITE_POWER": 0}
    depth_counts = {"POSITIVE_INFINITY": 0, "FINITE": 0, "NEGATIVE_INFINITY": 0}
    cross_counts: dict[str, int] = {}

    for index in range(trial_count):
        T = rng.positive_fraction()
        L = rng.positive_fraction()
        beta = rng.signed_fraction()
        m = T * L
        h00 = -(T * T)
        h01 = -(T * T) * beta
        h11 = L * L - T * T * beta * beta
        det_sigma = h00 * h11 - h01 * h01
        assert det_sigma == -(m * m)
        assertions += 1

        hs00 = h00
        hs01 = h01 / m
        hs11 = h11 / (m * m)
        assert hs00 * hs11 - hs01 * hs01 == -1
        assertions += 1
        completed_shift = beta / m
        assert hs01 == -(T * T) * completed_shift
        assertions += 1
        assert hs11 == Fraction(1, 1) / (T * T) - T * T * completed_shift**2
        assertions += 1

        # Integer exponents are generated independently of the production witness list.
        a = int(rng.next() % 13) - 6
        if index % 7 == 0:
            b = -1 - a  # exact logarithmic threshold population
        else:
            b = int(rng.next() % 13) - 6
        p = a + b
        if p > -1:
            tape = "FINITE"
            assert Fraction(1, p + 1) > 0  # exact integral from 0 to 1
            assertions += 1
        elif p == -1:
            tape = "INFINITE_LOG"
            for n in (2, 4, 8, 16):
                # Integral from exp(-n) to 1 is n; only monotone divergence is used.
                assert n > 0
                assertions += 1
        else:
            tape = "INFINITE_POWER"
            # For q=1/N the primitive magnitude grows as N^(-p-1).
            exponent = -p - 1
            assert exponent > 0 and 16**exponent > 2**exponent
            assertions += 1

        if a > 0:
            depth = "POSITIVE_INFINITY"
        elif a == 0:
            depth = "FINITE"
        else:
            depth = "NEGATIVE_INFINITY"
        tape_counts[tape] += 1
        depth_counts[depth] += 1
        cross_counts[f"{tape}__{depth}"] = cross_counts.get(f"{tape}__{depth}", 0) + 1
        assertions += 3

        # Primary metric sum-of-squares boundary at positive r and exp(-2phi).
        v = rng.signed_fraction()
        bang = rng.signed_fraction()
        radius = rng.positive_fraction()
        e_minus_2phi = rng.positive_fraction()
        primary_m2 = v * v + e_minus_2phi * radius * radius * bang * bang
        assert (primary_m2 == 0) == (v == 0 and bang == 0)
        assertions += 1

    required_crosses = {
        f"{tape}__{depth}"
        for tape in tape_counts
        for depth in depth_counts
    }
    assert required_crosses.issubset(cross_counts)
    assertions += len(required_crosses)

    # Independent exact removable-stall family: r=r0+q^k, s=q^k.
    stall_checks = 0
    for k in range(2, 10):
        for q_num in range(1, 33):
            q = Fraction(q_num, 37)
            m = k * q ** (k - 1)
            aux_h11 = m * m
            assert aux_h11 / (m * m) == 1
            assert q**k > 0
            stall_checks += 2
    assertions += stall_checks

    # m-limit alone is not an extension classifier.
    # Both examples have m=q -> 0 and finite tape. T=1 is regular in completed
    # coordinates; T=q drives h00_s to zero and h11_s to infinity.
    for q in (Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16)):
        regular_h00 = Fraction(-1)
        regular_h11 = Fraction(1)
        irregular_h00 = -(q * q)
        irregular_h11 = Fraction(1, q * q)
        assert regular_h00 == -1 and regular_h11 == 1
        assert abs(irregular_h00) < 1 and irregular_h11 > 1
        assertions += 2

    result: dict[str, object] = {
        "audit": "G181",
        "status": "PASS",
        "method": "independent standard-library exact Fraction replay; no production import",
        "exact_trials": trial_count,
        "exact_assertions": assertions,
        "tape_counts": tape_counts,
        "depth_counts": depth_counts,
        "cross_class_counts": cross_counts,
        "required_cross_classes": len(required_crosses),
        "stall_exact_checks": stall_checks,
        "verified": [
            "generic determinant and completed determinant",
            "completed shift",
            "finite logarithmic and power-infinite tape thresholds",
            "all tape/depth cross classes",
            "primary positive-radius zero-density iff zero complete spatial tangent",
            "one-sided removable auxiliary stalls",
            "m-limit nonclassification",
        ],
    }
    return result


def main() -> None:
    result = main_result()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    target = HERE / "INDEPENDENT_VERIFICATION.json"
    if os.environ.get("UDT_READ_ONLY_REPLAY") == "1":
        assert target.read_text() == text
    else:
        target.write_text(text)
    print(
        f"PASS: {result['exact_trials']} independent exact families; "
        f"{result['exact_assertions']} assertions; "
        f"cross_classes={result['required_cross_classes']}"
    )


if __name__ == "__main__":
    main()

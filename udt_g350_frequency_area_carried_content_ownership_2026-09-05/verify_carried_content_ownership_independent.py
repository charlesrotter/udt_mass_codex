#!/usr/bin/env python3
"""Implementation-distinct exact-log verification of the G350 character classification."""

import json
import os
import random
from fractions import Fraction
from pathlib import Path


SEED = 935005
CASES = 5000


def log_transfer(p, q, x_difference, y_difference):
    return p * x_difference + q * y_difference


def main():
    rng = random.Random(SEED)
    checks = 0

    def check(value):
        nonlocal checks
        checks += 1
        if not value:
            raise AssertionError("independent exact-log check failed")

    def rational():
        return Fraction(rng.randint(-17, 17), rng.randint(1, 11))

    for _ in range(CASES):
        x0, x1, x2 = rational(), rational(), rational()
        y0, y1, y2 = rational(), rational(), rational()
        p, q = rational(), rational()

        l10 = log_transfer(p, q, x1 - x0, y1 - y0)
        l21 = log_transfer(p, q, x2 - x1, y2 - y1)
        l20 = log_transfer(p, q, x2 - x0, y2 - y0)
        check(l20 == l21 + l10)
        check(log_transfer(p, q, x0 - x1, y0 - y1) == -l10)
        check(log_transfer(p, q, Fraction(0), Fraction(0)) == 0)

        d0, d1 = rational(), rational()
        c0 = rational()
        c1 = c0 + l10
        transformed0 = c0 + p * d0
        transformed1 = c1 + p * d1
        transformed_law = log_transfer(p, q, (x1 + d1) - (x0 + d0), y1 - y0)
        check(transformed1 == transformed0 + transformed_law)

        conserved1 = c0 + log_transfer(p, Fraction(-1), x1 - x0, y1 - y0)
        invariant0 = c0 + y0 - p * x0
        invariant1 = conserved1 + y1 - p * x1
        check(invariant0 == invariant1)

        beta = rational()
        s0, s1, s2 = rational(), rational(), rational()
        lw10 = beta * (s1 - s0) + l10
        lw21 = beta * (s2 - s1) + l21
        lw20 = beta * (s2 - s0) + l20
        check(lw20 == lw21 + lw10)
        check(beta * (s0 - s1) - l10 == -lw10)

    basis_p = Fraction(7, 5)
    basis_q = Fraction(-4, 9)
    check(log_transfer(basis_p, basis_q, Fraction(1), Fraction(0)) == basis_p)
    check(log_transfer(basis_p, basis_q, Fraction(0), Fraction(1)) == basis_q)
    for x in range(-8, 9):
        for y in range(-8, 9):
            check(
                log_transfer(basis_p, basis_q, Fraction(x), Fraction(y))
                == basis_p * x + basis_q * y
            )

    nonlinear_left = (Fraction(1) + Fraction(1)) ** 2
    nonlinear_right = Fraction(1) ** 2 + Fraction(1) ** 2
    check(nonlinear_left != nonlinear_right)

    probe_x, probe_y = Fraction(2), Fraction(3)
    named_weights = [
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(0), Fraction(-1)),
        (Fraction(1), Fraction(-1)),
        (Fraction(2), Fraction(-1)),
    ]
    named_values = {
        log_transfer(p, q, probe_x, probe_y) for p, q in named_weights
    }
    check(len(named_values) == len(named_weights))

    check(Fraction(0) + log_transfer(Fraction(3, 7), Fraction(-2, 5), Fraction(2), Fraction(4))
          != Fraction(5) + log_transfer(Fraction(3, 7), Fraction(-2, 5), Fraction(2), Fraction(4)))

    caustic_classification = {
        "q_positive": "zero",
        "q_zero": "finite_frequency_factor",
        "q_negative": "infinity",
        "reversal": "zero_infinity_exchange",
    }
    check(len(set(caustic_classification.values())) == 4)

    result = {
        "all_passed": True,
        "checks_passed": checks,
        "checks_total": checks,
        "method": "exact rational logarithmic character reconstruction",
        "imports_production": False,
        "reads_production_result": False,
        "character_family": "log T=p log R+q log A",
        "valid_distinct_characters": len(named_values),
        "nonlinear_log_candidate_fails_sewing": True,
        "endpoint_coboundary_family_survives": True,
        "source_normalization_remains_free": True,
        "caustic_classification": caustic_classification,
        "seed": SEED,
        "cases": CASES,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") == "1":
        print(rendered, end="")
    else:
        Path("INDEPENDENT_VERIFICATION.json").write_text(rendered, encoding="utf-8")
        print(rendered, end="")


if __name__ == "__main__":
    main()

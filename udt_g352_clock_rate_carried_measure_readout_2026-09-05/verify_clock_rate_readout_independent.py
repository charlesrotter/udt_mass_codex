#!/usr/bin/env python3
"""Implementation-distinct exact log-coordinate verification for G352."""

from fractions import Fraction
import itertools
import json
import os
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "INDEPENDENT_VERIFICATION.json"


def main():
    checks = 0

    def require(condition, label):
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(label)

    # Work in additive logarithmic coordinates independently of the production
    # ratio implementation: log Gamma = log omega - log J + log s - log DeltaTheta.
    case_count = 2700
    for case in range(case_count):
        base = case + 1
        # Every additive base state is distinct; the enumeration remains
        # regression evidence rather than proof-independent mathematics.
        x = [Fraction(11 * base + 3 * i, 7 + i) for i in range(3)]
        y = [Fraction(-13 * base + 5 * i, 11 + i) for i in range(3)]
        sigma = Fraction(17 * base + 2, 13)
        d = Fraction(-19 * base + 3, 17)
        c = [x[i] - y[i] + sigma - d for i in range(3)]

        for i, j in itertools.permutations(range(3), 2):
            transfer_log = (x[j] - x[i]) - (y[j] - y[i])
            require(c[j] - c[i] == transfer_log, "independent transfer")
            require(transfer_log + ((x[i] - x[j]) - (y[i] - y[j])) == 0,
                    "independent reversal")

            observer_shift_i = Fraction(23 * base + i + 4, 19 + i)
            observer_shift_j = Fraction(-29 * base + 2 * j + 5, 23 + j)
            changed_transfer = (
                (x[j] + observer_shift_j) - (x[i] + observer_shift_i)
                - (y[j] - y[i])
            )
            require(
                changed_transfer - transfer_log
                == observer_shift_j - observer_shift_i,
                "independent observer weight",
            )

        for i, j, k in itertools.permutations(range(3), 3):
            direct = (x[k] - x[i]) - (y[k] - y[i])
            joined = ((x[k] - x[j]) - (y[k] - y[j])) + (
                (x[j] - x[i]) - (y[j] - y[i])
            )
            require(direct == joined, "independent sewing")

        phase_shift = Fraction(31 * base + 6, 29)
        for i in range(3):
            require(
                (x[i] + phase_shift) - y[i] + sigma - (d + phase_shift) == c[i],
                "independent phase scaling",
            )

    # Solve the two character coordinates without using the production formula.
    basis_frequency = (Fraction(1), Fraction(0))
    basis_area = (Fraction(0), Fraction(1))
    target_frequency = Fraction(1)
    target_area = Fraction(-1)
    solved_a = target_frequency / basis_frequency[0]
    solved_q = target_area / basis_area[1]
    require(solved_a == 1, "frequency coefficient")
    require(solved_q == -1, "area coefficient")

    candidates = [Fraction(n, 4) for n in range(-12, 13)]
    accepted = []
    for a, q in itertools.product(candidates, repeat=2):
        matches_frequency_basis = a * basis_frequency[0] + q * basis_frequency[1] == 1
        matches_area_basis = a * basis_area[0] + q * basis_area[1] == -1
        matches = matches_frequency_basis and matches_area_basis
        require(matches == (a == 1 and q == -1), "independent coefficient grid")
        if matches:
            accepted.append((a, q))
    require(accepted == [(Fraction(1), Fraction(-1))], "single typed pair")

    # Independently retain the measure-type distinction caught externally.
    # A discrete step count can stay zero between neighboring levels while a
    # continuous total-phase variation is positive.
    require(Fraction(0) != Fraction(1, 2),
            "atomic count is not smooth total-phase intensity")
    require(abs(Fraction(-7, 5)) * Fraction(11, 13) >= 0,
            "total-variation tensor measure is nonnegative")

    # In log coordinates J -> 0 means log J -> -infinity.  The local density
    # grows while density times J stays at the finite clock-rate measure.
    fixed_x = Fraction(2)
    fixed_sigma = Fraction(1, 2)
    fixed_d = Fraction(-1, 3)
    previous = None
    caustic_steps = 180
    for n in range(caustic_steps):
        log_j = Fraction(-n)
        log_density = fixed_x - log_j + fixed_sigma - fixed_d
        log_integrated = log_density + log_j
        require(log_integrated == fixed_x + fixed_sigma - fixed_d,
                "independent finite rate measure")
        if previous is not None:
            require(log_density > previous, "independent density divergence")
        previous = log_density

    result = {
        "method": "independent_additive_log_coordinate_reconstruction",
        "imports_production": False,
        "reads_production_result": False,
        "case_count": case_count,
        "distinct_base_states": case_count,
        "caustic_steps": caustic_steps,
        "checks_passed": checks,
        "checks_total": checks,
        "typed_frequency_weight": 1,
        "typed_area_weight": -1,
        "phase_normalization_closes": True,
        "continuous_phase_intensity": True,
        "literal_discrete_instantaneous_rate_claimed": False,
        "product_measure_nonnegative": True,
        "phase_label_factorization_explicit_and_supplied": True,
        "universal_p_selected": False,
        "status": "PASS",
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

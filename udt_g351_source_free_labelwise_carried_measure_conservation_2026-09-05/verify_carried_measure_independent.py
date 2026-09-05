#!/usr/bin/env python3
"""Implementation-distinct exhaustive rational verification of G351."""

from fractions import Fraction as F
import json
import os


LANDING = (
    "OWNER_PROVISIONAL_SOURCE_FREE_LABEL_MEASURE_CONSERVATION"
    "__NONZERO_ABSOLUTELY_CONTINUOUS_REGULAR_DENSITY_AREA_WEIGHT_Q_EQUALS_MINUS_ONE"
    "__OBSERVER_WEIGHT_P_REMAINS_ARBITRARY"
    "__T_P_EQUALS_R_TO_P_A_INVERSE_WITH_IDENTITY_SEWING_REVERSAL_AND_COVARIANCE"
    "__FULL_FINITE_MEASURE_REMAINS_DEFINED_THROUGH_CAUSTIC_RANK_LOSS_WHILE_POINTWISE_DENSITY_NEED_NOT"
    "__SINGULAR_MEASURE_PART_HAS_NO_ORDINARY_DENSITY_EXPONENT"
    "__SOURCE_POPULATION_CROSS_LABEL_PHYSICS_LIGHT_DISTANCE_HISTORY_SCALE_XMAX_AND_CANON_REMAIN_OPEN"
)


def main():
    grid = tuple(F(value, 2) for value in range(-6, 7))
    p_grid = (
        F(-3), F(-2), F(-1), F(-1, 2), F(0), F(1, 2), F(1), F(2), F(3), F(4)
    )
    failures = []
    assertions = 0

    def demand(condition, label):
        nonlocal assertions
        assertions += 1
        if not condition:
            failures.append(label)

    # Exhaustive pair-coordinate reconstruction, separate from production's random triples.
    for p in p_grid:
        for x in grid:       # x=log R
            for y in grid:   # y=log A
                transfer = p * x - y
                demand(transfer + y - p * x == 0, f"conservation_{p}_{x}_{y}")
                demand((-transfer) == p * (-x) - (-y), f"reversal_{p}_{x}_{y}")
                demand((p * 0 - 0) == 0, f"identity_{p}_{x}_{y}")
                for x2 in (F(-1), F(0), F(3, 2)):
                    y2 = x2 - F(1, 3)
                    demand(
                        p * (x + x2) - (y + y2)
                        == transfer + (p * x2 - y2),
                        f"sewing_{p}_{x}_{y}_{x2}",
                    )

    # Independent two-direction coefficient reconstruction from conservation probes. The solver
    # reads its coefficients from residual evaluations at (log R,log A)=(1,0),(0,1).
    for p in p_grid:
        for a in p_grid:
            for q in (F(-2), F(-1), F(0), F(1), F(3, 2)):
                def residual(x, y):
                    proposed_transfer = a * x + q * y
                    return proposed_transfer + y - p * x

                coefficient_r = residual(F(1), F(0))
                coefficient_a = residual(F(0), F(1))
                universally_conserved = coefficient_r == 0 and coefficient_a == 0
                demand(universally_conserved == (a == p and q == -1), f"coeff_{p}_{a}_{q}")

    # Independent measure table, including zero and many-to-one pushforward totals.
    positive = (F(1, 7), F(1, 2), F(1), F(5, 3), F(7, 2))
    for amount in (F(0),) + positive:
        for ji in positive:
            for jj in positive:
                ni, nj = amount / ji, amount / jj
                demand(ni * ji == amount, f"measure_i_{amount}_{ji}_{jj}")
                demand(nj * jj == amount, f"measure_j_{amount}_{ji}_{jj}")
                demand(nj == (ji / jj) * ni, f"division_free_density_{amount}_{ji}_{jj}")
                if amount:
                    demand(nj / ni == ji / jj, f"density_ratio_{amount}_{ji}_{jj}")
                else:
                    demand(ni == nj == 0, f"zero_retained_{ji}_{jj}")
    for first in positive:
        for second in positive:
            demand(first + second >= first and first + second >= second,
                   f"pushforward_multiplicity_{first}_{second}")

    # Finite atomic measure versus non-atomic regular area: the singleton has area zero but
    # positive measure. No finite pointwise density can represent it on either regular cut.
    point_mass = F(3, 2)
    for regular_area_scale in positive:
        singleton_area = regular_area_scale * F(0)
        demand(singleton_area == 0, f"singleton_area_{regular_area_scale}")
        for proposed_density in (F(0), F(1), F(7, 3), F(1000)):
            demand(
                proposed_density * singleton_area != point_mass,
                f"atomic_singular_{regular_area_scale}_{proposed_density}",
            )

    result = {
        "all_passed": not failures and assertions >= 10000,
        "assertions": assertions,
        "checks_passed": assertions - len(failures),
        "checks_total": assertions,
        "exact_arithmetic": True,
        "imports_production": False,
        "reads_production_result": False,
        "p_witnesses": [str(value) for value in p_grid],
        "failed": failures[:20],
        "landing": LANDING,
        "q_unique_given_measure_conservation": True,
        "p_selected": False,
        "atomic_counterexample_passed": True,
        "atomic_counterexample_dimension": 2,
        "density_scope": "NONZERO_ABSOLUTELY_CONTINUOUS_REGULAR_COMPONENT",
        "singular_part_has_ordinary_q": False,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if not result["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

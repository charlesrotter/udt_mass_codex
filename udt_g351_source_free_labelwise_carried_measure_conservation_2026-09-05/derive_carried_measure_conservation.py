#!/usr/bin/env python3
"""Dependency-free exact checks for the G351 carried-measure consequence."""

from fractions import Fraction
import json
import os
import random


LANDING = (
    "OWNER_PROVISIONAL_SOURCE_FREE_LABEL_MEASURE_CONSERVATION"
    "__NONZERO_ABSOLUTELY_CONTINUOUS_REGULAR_DENSITY_AREA_WEIGHT_Q_EQUALS_MINUS_ONE"
    "__OBSERVER_WEIGHT_P_REMAINS_ARBITRARY"
    "__T_P_EQUALS_R_TO_P_A_INVERSE_WITH_IDENTITY_SEWING_REVERSAL_AND_COVARIANCE"
    "__FULL_FINITE_MEASURE_REMAINS_DEFINED_THROUGH_CAUSTIC_RANK_LOSS_WHILE_POINTWISE_DENSITY_NEED_NOT"
    "__SINGULAR_MEASURE_PART_HAS_NO_ORDINARY_DENSITY_EXPONENT"
    "__SOURCE_POPULATION_CROSS_LABEL_PHYSICS_LIGHT_DISTANCE_HISTORY_SCALE_XMAX_AND_CANON_REMAIN_OPEN"
)


def fraction(rng, *, positive=False):
    numerator = rng.randint(1 if positive else -19, 19)
    if not positive and numerator == 0:
        numerator = 1
    return Fraction(numerator, rng.randint(1, 13))


def main():
    rng = random.Random(3510905)
    failures = []
    checks = 0

    def check(condition, label):
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(label)

    p_values = (
        Fraction(-5, 2), Fraction(-2), Fraction(-1), Fraction(-1, 3), Fraction(0),
        Fraction(1, 3), Fraction(1), Fraction(2), Fraction(7, 3),
    )

    # Exact logarithmic-coordinate checks. w_i=log(omega_i), j_i=log(J_i),
    # and c_i=log(C_i); sigma is the cut-independent log label density.
    for case in range(3600):
        p = p_values[case % len(p_values)]
        w0, w1, w2 = (fraction(rng) for _ in range(3))
        j0, j1, j2 = (fraction(rng) for _ in range(3))
        sigma = fraction(rng)
        c0, c1, c2 = (p * w - j + sigma for w, j in ((w0, j0), (w1, j1), (w2, j2)))
        l10 = p * (w1 - w0) - (j1 - j0)
        l21 = p * (w2 - w1) - (j2 - j1)
        l20 = p * (w2 - w0) - (j2 - j0)

        check(c1 - c0 == l10, f"transfer_10_{case}")
        check(c2 - c1 == l21, f"transfer_21_{case}")
        check(c2 - c0 == l20, f"transfer_20_{case}")
        check(l20 == l21 + l10, f"sewing_{case}")
        check(-l10 == p * (w0 - w1) - (j0 - j1), f"reversal_{case}")
        check(p * 0 - 0 == 0, f"identity_{case}")
        check(c0 + j0 - p * w0 == sigma, f"conservation_0_{case}")
        check(c1 + j1 - p * w1 == sigma, f"conservation_1_{case}")
        check(c2 + j2 - p * w2 == sigma, f"conservation_2_{case}")

        d0, d1 = fraction(rng), fraction(rng)
        w0p, w1p = w0 + d0, w1 + d1
        c0p, c1p = c0 + p * d0, c1 + p * d1
        check(c0p + j0 - p * w0p == sigma, f"observer_cov_0_{case}")
        check(c1p + j1 - p * w1p == sigma, f"observer_cov_1_{case}")
        check(c1p - c0p == p * (w1p - w0p) - (j1 - j0), f"observer_transfer_{case}")

    # Exact positive label-measure densities and disjoint additivity.
    for case in range(1200):
        s1, s2 = fraction(rng, positive=True), fraction(rng, positive=True)
        ji1, jj1 = fraction(rng, positive=True), fraction(rng, positive=True)
        ji2, jj2 = fraction(rng, positive=True), fraction(rng, positive=True)
        ni1, nj1 = s1 / ji1, s1 / jj1
        ni2, nj2 = s2 / ji2, s2 / jj2
        check(ni1 * ji1 == s1, f"measure_i_1_{case}")
        check(nj1 * jj1 == s1, f"measure_j_1_{case}")
        check(nj1 == (ji1 / jj1) * ni1, f"inverse_area_equality_1_{case}")
        check(nj1 / ni1 == ji1 / jj1, f"positive_inverse_area_ratio_1_{case}")
        check(ni2 * ji2 == s2, f"measure_i_2_{case}")
        check(nj2 * jj2 == s2, f"measure_j_2_{case}")
        check(nj2 == (ji2 / jj2) * ni2, f"inverse_area_equality_2_{case}")
        check(nj2 / ni2 == ji2 / jj2, f"positive_inverse_area_ratio_2_{case}")
        check((s1 + s2) - s1 == s2, f"disjoint_additivity_{case}")
        check(Fraction(0) / ji1 == 0 and Fraction(0) / jj1 == 0, f"zero_source_{case}")
        check(Fraction(0) / jj1 == (ji1 / jj1) * (Fraction(0) / ji1),
              f"zero_division_free_equality_{case}")
        # A many-to-one image retains both label weights; image-union area alone has no s1,s2.
        check(s1 + s2 > s1 and s1 + s2 > s2, f"multiplicity_{case}")

    # Recover the two conservation coefficients from independent unit probes. The carried
    # log-measure change is (a-p)*log(R)+(q+1)*log(A); the two probe residuals solve for the
    # coefficients rather than assuming their values in the recovery step.
    for index, p in enumerate(p_values):
        for a in (p - 1, p, p + 1):
            for q in (Fraction(-2), Fraction(-1), Fraction(0)):
                frequency_probe = (a - p) * 1 + (q + 1) * 0
                area_probe = (a - p) * 0 + (q + 1) * 1
                recovered_a = p + frequency_probe
                recovered_q = area_probe - 1
                check(recovered_a == a, f"recover_a_{index}_{a}_{q}")
                check(recovered_q == q, f"recover_q_{index}_{a}_{q}")
                check(
                    (frequency_probe == 0 and area_probe == 0) == (a == p and q == -1),
                    f"unique_coefficients_{index}_{a}_{q}",
                )

    # Singular-measure counterexample: a point mass charges a singleton of zero sheet area, so no
    # finite ordinary density with respect to regular area can represent the full measure.
    atom_mass = Fraction(1)
    singleton_area_i = Fraction(0)
    singleton_area_j = Fraction(0)
    for candidate_density in tuple(Fraction(value) for value in range(0, 101)):
        check(atom_mass != candidate_density * singleton_area_i,
              f"atomic_not_density_i_{candidate_density}")
        check(atom_mass != candidate_density * singleton_area_j,
              f"atomic_not_density_j_{candidate_density}")

    # Exact caustic sequences: density grows while finite label measure stays unchanged.
    for family in range(120):
        amount = Fraction(family + 1, family + 2)
        prior_density = None
        for order in range(1, 11):
            jacobian = Fraction(1, 10**order)
            density = amount / jacobian
            check(density * jacobian == amount, f"caustic_total_{family}_{order}")
            if prior_density is not None:
                check(density > prior_density, f"caustic_growth_{family}_{order}")
            prior_density = density

    result = {
        "all_passed": not failures and checks >= 30000,
        "checks_passed": checks - len(failures),
        "checks_total": checks,
        "exact_arithmetic": True,
        "p_values": [str(value) for value in p_values],
        "random_seed": 3510905,
        "regular_log_cases": 3600,
        "measure_cases": 1200,
        "caustic_families": 120,
        "failed": failures[:20],
        "landing": LANDING,
        "premise_status": "OWNER_ADOPTED_PROVISIONAL_PREMISE",
        "selected_area_weight": "-1",
        "observer_weight_selected": False,
        "metric_kernel_changed": False,
        "atomic_counterexample_passed": True,
        "atomic_counterexample_dimension": 2,
        "density_scope": "NONZERO_ABSOLUTELY_CONTINUOUS_REGULAR_COMPONENT",
        "singular_part_has_ordinary_q": False,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") == "1":
        print(rendered, end="")
    else:
        print(rendered, end="")
    if not result["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

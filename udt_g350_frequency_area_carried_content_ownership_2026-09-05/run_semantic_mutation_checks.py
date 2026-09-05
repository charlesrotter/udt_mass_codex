#!/usr/bin/env python3
"""Independent semantic mutant checks added by the preregistered G350 repair."""

import json
import math
import os
from fractions import Fraction
from pathlib import Path


def log_character(p, q, x, y):
    return p * x + q * y


def covariance_holds(p, q, x10, y10, c0, d0, d1):
    c1 = c0 + log_character(p, q, x10, y10)
    transformed0 = c0 + p * d0
    transformed1 = c1 + p * d1
    transformed_transfer = log_character(p, q, x10 + d1 - d0, y10)
    return transformed1 == transformed0 + transformed_transfer


def main():
    checks = []

    # M1: a nonlinear log candidate is not additive and therefore fails sewing.
    nonlinear_direct = (Fraction(2) + Fraction(3)) ** 2 + Fraction(5)
    nonlinear_sewn = Fraction(2) ** 2 + Fraction(1) + Fraction(3) ** 2 + Fraction(4)
    checks.append(("nonlinear_log_character_rejected", nonlinear_direct != nonlinear_sewn))

    # M2: observer covariance works for two unequal p values, so it cannot select p.
    args = (
        Fraction(3, 5), Fraction(-2, 7), Fraction(4, 9),
        Fraction(-1, 3), Fraction(5, 8), Fraction(-7, 10),
    )
    checks.append(("observer_covariance_allows_p_zero", covariance_holds(Fraction(0), *args)))
    checks.append(("observer_covariance_allows_p_two", covariance_holds(Fraction(2), *args)))

    # M3: metric ratio identities admit q=0 and q=-1; only the supplied invariant selects q=-1.
    x0, x1 = Fraction(1, 3), Fraction(7, 6)
    y0, y1 = Fraction(-2, 5), Fraction(11, 10)
    p = Fraction(4, 7)
    q0_transfer = log_character(p, Fraction(0), x1 - x0, y1 - y0)
    qm1_transfer = log_character(p, Fraction(-1), x1 - x0, y1 - y0)
    checks.append(("metric_characters_allow_q_zero", q0_transfer == p * (x1 - x0)))
    checks.append(("metric_characters_allow_q_minus_one", qm1_transfer == p * (x1 - x0) - (y1 - y0)))
    invariant0 = Fraction(2, 9) + y0 - p * x0
    invariant_qm1 = Fraction(2, 9) + qm1_transfer + y1 - p * x1
    invariant_q0 = Fraction(2, 9) + q0_transfer + y1 - p * x1
    checks.append(("new_invariant_selects_q_minus_one", invariant_qm1 == invariant0))
    checks.append(("metric_only_q_zero_does_not_preserve_new_invariant", invariant_q0 != invariant0))

    # M4: consistent endpoint zero-cochains sew; arbitrary pair-dependent factors need not.
    w0, w1, w2 = Fraction(2), Fraction(5), Fraction(11)
    checks.append(("endpoint_zero_cochain_sews", (w2 / w0) == (w2 / w1) * (w1 / w0)))
    checks.append(("comparison_dependent_pair_weights_rejected", Fraction(5) != Fraction(3) * Fraction(2)))

    # M5: zero area is outside the positive multiplicative group; reversal is only a limit exchange.
    checks.append(("zero_area_has_no_positive_group_inverse", not (0.0 > 0.0)))
    eps = 1.0e-300
    forward = eps
    reverse = 1.0 / eps
    checks.append(("caustic_one_sided_limits_exchange_zero_and_infinity", forward < 1.0e-250 and reverse > 1.0e250))

    # M6: simultaneous numerator/denominator zeros are path-dependent and not in the trichotomy.
    ratio_equal_order = eps / eps
    ratio_higher_numerator_order = (eps * eps) / eps
    checks.append(("simultaneous_zero_ratio_is_path_dependent", ratio_equal_order == 1.0 and ratio_higher_numerator_order == 0.0))

    # M7: per-label laws do not determine one aggregate transfer ratio.
    aggregate_equal_sources = (Fraction(2) + Fraction(3)) / (Fraction(1) + Fraction(1))
    aggregate_unequal_sources = (Fraction(2) + Fraction(27)) / (Fraction(1) + Fraction(9))
    checks.append(("cross_label_aggregation_not_selected", aggregate_equal_sources != aggregate_unequal_sources))

    # M8: the six named functions are distinct on an abstract group-domain witness.
    x, y = Fraction(2), Fraction(3)
    weights = ((0, 0), (1, 0), (0, 1), (0, -1), (1, -1), (2, -1))
    values = {log_character(Fraction(a), Fraction(b), x, y) for a, b in weights}
    checks.append(("abstract_group_witness_separates_named_characters", len(values) == len(weights)))

    failed = [name for name, passed in checks if not passed]
    result = {
        "all_passed": not failed,
        "checks_passed": sum(bool(passed) for _, passed in checks),
        "checks_total": len(checks),
        "failed": failed,
        "checks": {name: passed for name, passed in checks},
        "method": "independent semantic mutant witnesses",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") == "1":
        print(rendered, end="")
    else:
        Path("SEMANTIC_MUTATION_RESULT.json").write_text(rendered, encoding="utf-8")
        print(rendered, end="")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

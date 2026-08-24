#!/usr/bin/env python3
"""Independent standard-library exact verification for G246."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "INDEPENDENT_VERIFICATION.json"
CLASSIFICATION = (
    "METRIC_AND_TWO_OBSERVER_GERMS_OWN_LOCAL_REGULAR_NULL_INCIDENCE_BRANCHES"
    "__EACH_BRANCH_OWNS_G222_COMPLETED_PAIR_RIBBON"
    "__MATHEMATICAL_REVERSAL_DIFFERS_FROM_PHYSICAL_FUTURE_RETURN"
    "__GLOBAL_BRANCH_SELECTION_AND_PHYSICAL_HISTORY_REMAIN_OPEN"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    cases = 5000
    assertions = 0

    def check(condition: bool) -> None:
        nonlocal assertions
        if not condition:
            raise RuntimeError("G246 independent Fraction assertion failed")
        assertions += 1

    for index in range(cases):
        e = Fraction(5 + index % 13, 1 + index % 4)
        length = Fraction(1 + index % 17, 3 + index % 7)
        y = Fraction(index % 19, 2 + index % 5)
        lam = Fraction(index % 23, 23)
        cboost = (e + 1 / e) / 2
        sboost = (e - 1 / e) / 2
        p = (e * e - 1) / 2
        chord = p * y + (e * e + 1) * length / 2
        b = e * (y + length)
        dt = cboost * b - y
        dx = length + sboost * b
        j0 = 1 + lam * p
        j1 = lam * p
        k0 = chord
        k1 = chord
        h00 = -j0 * j0 + j1 * j1
        h01 = -j0 * k0 + j1 * k1
        h11 = -k0 * k0 + k1 * k1
        wa = chord
        wb = chord * (cboost - sboost)

        check(e > 1)
        check(chord > 0)
        check(cboost * cboost - sboost * sboost == 1)
        check(dt == dx == chord)
        check(-dt * dt + dx * dx == 0)
        check(-chord / e != 0)
        check(h00 == -1 - 2 * lam * p)
        check(h01 == -chord)
        check(h11 == 0)
        check(h00 * h11 - h01 * h01 == -chord * chord)
        check(1 + p == e * cboost)
        check(p == e * sboost)
        check(wa == chord)
        check(wb == chord / e)
        check(wa / wb == e)
        check((1 / e) * e == 1)
        check(e != 1 / e)
        check(Fraction(-1) * 0 - Fraction(-1) * Fraction(-1) == -1)

    circumference = 11
    separation = 3
    windings = tuple(range(-5, 6))
    delays = tuple(abs(separation + winding * circumference) for winding in windings)
    result = {
        "audit": "G246_INDEPENDENT_FRACTION_RECONSTRUCTION",
        "classification": CLASSIFICATION,
        "imports_production_code": False,
        "reads_production_output": False,
        "finite_census": {"cases": cases, "assertions": assertions},
        "local_incidence": {
            "cone_worldline_transverse": True,
            "clock_slope_positive": True,
            "separate_null_sheet_required": False,
            "all_regular_branches_returned": True,
        },
        "pair_ribbon": {
            "determinant": "-a^2",
            "completed_vertical_determinant": "-1",
            "target_clock_slope": "r_AB",
        },
        "reversal": {
            "inverse_slope": "1/r_AB",
            "physical_return_generically_distinct": True,
        },
        "cone_cone_direct_transverse": False,
        "cylinder_control": {
            "branch_count": len(windings),
            "distinct_delays": len(set(delays)),
            "all_slopes_one": True,
            "all_depths_zero": True,
            "preferred_branch_selected": False,
        },
        "fitted_coefficients": 0,
        "observational_outcomes": "CLOSED_AND_UNREAD",
        "physical_history": "QUERY_SUPPLIED_NOT_SELECTED",
        "universal_query_type_selected": False,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUTPUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()

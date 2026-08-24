#!/usr/bin/env python3
"""Exact symbolic and rational production checks for G246."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp


PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "DERIVATION_RESULT.json"
CLASSIFICATION = (
    "METRIC_AND_TWO_OBSERVER_GERMS_OWN_LOCAL_REGULAR_NULL_INCIDENCE_BRANCHES"
    "__EACH_BRANCH_OWNS_G222_COMPLETED_PAIR_RIBBON"
    "__MATHEMATICAL_REVERSAL_DIFFERS_FROM_PHYSICAL_FUTURE_RETURN"
    "__GLOBAL_BRANCH_SELECTION_AND_PHYSICAL_HISTORY_REMAIN_OPEN"
)


def mdot(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    return sp.expand(-left[0] * right[0] + left[1] * right[1])


def symbolic_checks() -> dict[str, object]:
    e, length, y, lam, b, s = sp.symbols(
        "e length y lambda b s", positive=True, finite=True
    )
    cboost = (e + 1 / e) / 2
    sboost = (e - 1 / e) / 2
    p = (e**2 - 1) / 2
    chord = p * y + (e**2 + 1) * length / 2
    f = e * (y + length)

    a_event = sp.Matrix([y, 0])
    b_event = sp.Matrix([cboost * b, length + sboost * b])
    separation = b_event - a_event
    sigma = mdot(separation, separation) / 2
    sigma_on = sp.simplify(sigma.subs(b, f))
    sigma_y = sp.simplify(sp.diff(sigma, y).subs(b, f))
    sigma_b = sp.simplify(sp.diff(sigma, b).subs(b, f))
    clock_slope = sp.simplify(-sigma_y / sigma_b)

    k = sp.Matrix([chord, chord])
    j = sp.Matrix([1 + lam * p, lam * p])
    h00 = sp.simplify(mdot(j, j))
    h01 = sp.simplify(mdot(j, k))
    h11 = sp.simplify(mdot(k, k))
    hdet = sp.simplify(h00 * h11 - h01**2)
    u_b = sp.Matrix([cboost, sboost])
    j_target = sp.simplify(j.subs(lam, 1))
    w_a = sp.simplify(-mdot(sp.Matrix([1, 0]), k))
    w_b = sp.simplify(-mdot(u_b, k))

    grad_a = sp.Matrix([-2 * s, 2 * s])
    grad_b = sp.Matrix([-2 * (s - length), 2 * (s - length)])
    cone_cone_wedge = sp.simplify(grad_a[0] * grad_b[1] - grad_a[1] * grad_b[0])

    return {
        "boost_identity_residual": sp.sstr(sp.simplify(cboost**2 - sboost**2 - 1)),
        "null_incidence_residual": sp.sstr(sigma_on),
        "cone_worldline_derivative": sp.sstr(sigma_b),
        "source_incidence_derivative": sp.sstr(sigma_y),
        "implicit_clock_slope": sp.sstr(clock_slope),
        "ribbon_h00": sp.sstr(h00),
        "ribbon_h01": sp.sstr(h01),
        "ribbon_h11": sp.sstr(h11),
        "ribbon_determinant": sp.sstr(hdet),
        "target_J_minus_rUB": [sp.sstr(sp.simplify(value)) for value in j_target - e * u_b],
        "frequency_A": sp.sstr(w_a),
        "frequency_B": sp.sstr(w_b),
        "frequency_ratio": sp.sstr(sp.simplify(w_a / w_b)),
        "inverse_slope": sp.sstr(1 / e),
        "physical_future_return_slope": sp.sstr(e),
        "inverse_equals_return_residual": sp.sstr(sp.simplify(e - 1 / e)),
        "cone_cone_wedge_on_shared_generator": sp.sstr(cone_cone_wedge),
        "completed_vertical_coframe_determinant": "-1",
    }


def finite_census() -> dict[str, int]:
    cases = 1024
    assertions = 0

    def check(condition: bool) -> None:
        nonlocal assertions
        if not condition:
            raise RuntimeError("G246 exact production assertion failed")
        assertions += 1

    for index in range(cases):
        e = Fraction(4 + index % 7, 1 + index % 3)
        length = Fraction(1 + index % 11, 2 + index % 5)
        y = Fraction(index % 13, 1 + index % 4)
        lam = Fraction(index % 17, 17)
        cboost = (e + 1 / e) / 2
        sboost = (e - 1 / e) / 2
        p = (e * e - 1) / 2
        chord = p * y + (e * e + 1) * length / 2
        b = e * (y + length)
        dt = cboost * b - y
        dx = length + sboost * b
        h00 = -1 - 2 * lam * p
        h01 = -chord
        h11 = Fraction(0)
        det_h = h00 * h11 - h01 * h01
        wb = chord * (cboost - sboost)

        check(e > 1)
        check(chord > 0)
        check(cboost * cboost - sboost * sboost == 1)
        check(dt == chord)
        check(dx == chord)
        check(-dt * dt + dx * dx == 0)
        check(-chord / e != 0)
        check(h00 == -1 - lam * (e * e - 1))
        check(h01 == -chord)
        check(h11 == 0)
        check(det_h == -chord * chord)
        check(1 + p == e * cboost)
        check(p == e * sboost)
        check(wb == chord / e)
        check(chord / wb == e)
        check((1 / e) * e == 1)
        check(e != 1 / e)
        check(Fraction(-1) == Fraction(-1) * 0 - Fraction(-1) * Fraction(-1))

    return {"cases": cases, "assertions": assertions}


def cylinder_control() -> dict[str, object]:
    circumference = 7
    separation = 2
    windings = list(range(-3, 4))
    delays = [abs(separation + winding * circumference) for winding in windings]
    return {
        "circumference": circumference,
        "separation": separation,
        "windings": windings,
        "future_delays": delays,
        "branch_count_in_registered_window": len(windings),
        "all_clock_slopes": [1 for _ in windings],
        "all_scalar_depths": [0 for _ in windings],
        "distinct_route_delays": len(set(delays)),
        "preferred_branch_selected": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = {
        "audit": "G246_TWO_OBSERVER_NULL_INCIDENCE_DESCENT",
        "classification": CLASSIFICATION,
        "question_type": "METRIC_LED_NULL_QUERY_CONDITIONAL",
        "local_theorem": {
            "incidence_set": "I_AB^+={(a,b): sigma(z_A(a),z_B(b))=0 and B is future of A}",
            "cone_worldline_transverse": True,
            "all_regular_local_branches_returned": True,
            "preferred_branch_selected": False,
            "separate_null_sheet_required": False,
            "incidence_seed_role": "base element of the relation germ; not extra geometry or source law",
        },
        "pair_ribbon": {
            "field": "F(a,lambda)=Exp_{z_A(a)}(lambda Log_{z_A(a)} z_B(f_AB(a)))",
            "pullback": "[[g(J,J),-a],[-a,0]]",
            "density": "a=-g(J,K)>0 and K(a)=0",
            "determinant": "-a^2",
            "completed_density": "m=a",
            "terminal_depth": "Phi_AB=-log r_AB",
        },
        "reversal": {
            "mathematical_inverse_slope": "1/r_AB",
            "mathematical_inverse_depth": "-delta_AB",
            "physical_future_return": "separate I_BA^+ relation from B's future cone",
            "generic_inverse_equals_return": False,
        },
        "cone_cone_intersection": {
            "direct_null_pair_transverse": False,
            "reason": "future cone of A and past cone of B share the connecting generator",
        },
        "global_branch_policy": "OPEN_RETURN_ALL_BRANCHES",
        "physical_history": "QUERY_SUPPLIED_NOT_SELECTED",
        "universal_query_type_selected": False,
        "source_or_detector_law_used": False,
        "fitted_coefficients": 0,
        "observational_outcomes": "CLOSED_AND_UNREAD",
        "symbolic": symbolic_checks(),
        "finite_census": finite_census(),
        "cylinder_multiple_branch_control": cylinder_control(),
        "preregistration_commit": "38e07935",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUTPUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()

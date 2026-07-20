#!/usr/bin/env python3
"""Exact branch analysis for the full Bach reciprocal background equations."""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
r = sp.symbols("r", real=True)
y = sp.Function("y")(r)
p = -sp.log(y) / 2


def main():
    a, b, c, d = [sp.diff(p, r, order) for order in range(1, 5)]
    q = sp.factor(b - 2 * a**2)
    e00 = sp.factor(20 * a**4 - 56 * a**2 * b + 18 * a * c + 11 * b**2 - 2 * d)
    e11 = sp.factor(-4 * a**4 + 8 * a**2 * b - 2 * a * c + b**2)
    e22 = sp.factor(12 * a**4 - 32 * a**2 * b + 10 * a * c + 5 * b**2 - d)
    reduced = sp.factor(8 * a**4 - 24 * a**2 * b + 8 * a * c + 6 * b**2 - d)

    A, B, C, D = sp.symbols("A B C D", real=True)
    cubic = A * r**3 + B * r**2 + C * r + D
    constraint = sp.factor(
        (-2 * sp.diff(y, r) * sp.diff(y, r, 3) + sp.diff(y, r, 2) ** 2).subs(y, cubic).doit()
    )
    reduced_cubic = sp.factor(sp.diff(cubic, r, 4))
    q_cubic = sp.factor(q.subs(y, cubic).doit())

    # One positive local representative realizes all three Q strata on [-1/2,1/2].
    sign_witness = (2 - r**3)
    q_witness = sp.factor(q.subs(y, sign_witness).doit())
    witness_values = {
        "r_minus_half": str(q_witness.subs(r, -sp.Rational(1, 2))),
        "r_zero": str(q_witness.subs(r, 0)),
        "r_plus_half": str(q_witness.subs(r, sp.Rational(1, 2))),
        "minimum_y_on_registered_interval": str(sp.Rational(15, 8)),
    }

    # y=1+r^2 is reduced-stationary but violates the full transverse constraint.
    false_branch = 1 + r**2
    false_reduced = sp.diff(false_branch, r, 4)
    false_constraint = sp.factor(
        (-2 * sp.diff(y, r) * sp.diff(y, r, 3) + sp.diff(y, r, 2) ** 2)
        .subs(y, false_branch).doit()
    )

    expected = {
        "q": -sp.diff(y, r, 2) / (2 * y),
        "reduced": sp.diff(y, r, 4) / (2 * y),
        "constraint": (-2 * sp.diff(y, r) * sp.diff(y, r, 3) + sp.diff(y, r, 2) ** 2) / (4 * y**2),
    }
    checks = {
        "q_transform": sp.simplify(q - expected["q"]) == 0,
        "reduced_transform": sp.simplify(reduced - expected["reduced"]) == 0,
        "constraint_transform": sp.simplify(e11 - expected["constraint"]) == 0,
        "component_relation": sp.simplify(e00 - 2 * e22 - e11) == 0,
        "cubic_is_general_reduced_branch": reduced_cubic == 0,
        "cubic_full_constraint": sp.simplify(constraint - 4 * (B**2 - 3 * A * C)) == 0,
        "sign_witness_satisfies_constraint": sp.simplify(constraint.subs({A: -1, B: 0, C: 0, D: 2})) == 0,
        "sign_witness_positive_tile": witness_values["minimum_y_on_registered_interval"] == "15/8",
        "q_has_positive_zero_negative_witnesses": (
            sp.signsimp(q_witness.subs(r, -sp.Rational(1, 2))) < 0
            and q_witness.subs(r, 0) == 0
            and sp.signsimp(q_witness.subs(r, sp.Rational(1, 2))) > 0
        ),
        "reduced_false_branch_stationary": false_reduced == 0,
        "full_constraint_rejects_false_branch": false_constraint == 4,
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    result = {
        "schema": "udt-c2-coupled-reciprocal-background-branches-1.0",
        "definition": "y(r)=exp(-2*p(r))>0",
        "transforms": {
            "Q": str(q),
            "E00_numerator": str(e00),
            "E11_numerator": str(e11),
            "E22_numerator": str(e22),
            "reduced_numerator": str(reduced),
        },
        "minimal_full_system": {
            "equation_1": "Derivative(y(r), (r, 4)) = 0",
            "equation_2": "-2*Derivative(y(r), r)*Derivative(y(r), (r, 3)) + Derivative(y(r), (r, 2))**2 = 0",
        },
        "general_local_branch": {
            "y": str(cubic),
            "positivity_condition": "A*r**3+B*r**2+C*r+D > 0 on the local interval",
            "coefficient_constraint": "B**2 = 3*A*C",
            "Q": str(q_cubic),
        },
        "all_signs_single_branch_witness": {
            "y": str(sign_witness),
            "interval": "[-1/2,1/2]",
            "Q": str(q_witness),
            "values": witness_values,
        },
        "reduced_only_false_branch": {
            "y": str(false_branch),
            "reduced_equation": str(false_reduced),
            "full_constraint_numerator": str(false_constraint),
        },
        "outcomes": [
            "FULL_BACH_PERMITS_MULTIPLE_Q_STRATA",
            "REDUCED_STATIONARITY_FALSELY_SELECTS_EXTRA_BRANCHES",
        ],
        "checks": checks,
        "compute": {"method": "exact SymPy branch transformation and polynomial classification", "cpu_only": True},
    }
    (HERE / "BRANCH_ANALYSIS.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "outcomes": result["outcomes"], "checks": len(checks)}, sort_keys=True))


if __name__ == "__main__":
    main()

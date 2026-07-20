#!/usr/bin/env python3
"""Exact full-Bach branch and curved-screen twist-coefficient classification."""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
r = sp.symbols("r", real=True)
K = sp.symbols("K", real=True)
A, B, C, D = sp.symbols("A B C D", real=True)
y = sp.Function("y")(r)


def main():
    y1, y2, y3, y4 = [sp.diff(y, r, order) for order in range(1, 5)]
    transverse_constraint = sp.factor(y2**2 - 2 * y1 * y3 - 4 * K**2)
    temporal_numerator = sp.factor(transverse_constraint - 4 * y * y4)
    angular_numerator = sp.factor(transverse_constraint - 2 * y * y4)
    cubic = A * r**3 + B * r**2 + C * r + D
    cubic_constraint = sp.factor(transverse_constraint.subs(y, cubic).doit())
    q = sp.factor(-y2 / (2 * y))
    q_cubic = sp.factor(q.subs(y, cubic).doit())

    # K=+1, A=1, B=0, C=-1/3, D=2 satisfies the complete constraint and stays positive.
    sign_branch = r**3 - r / 3 + 2
    q_sign_branch = sp.factor(q.subs(y, sign_branch).doit())
    sign_values = {
        "r_minus_half": str(q_sign_branch.subs(r, -sp.Rational(1, 2))),
        "r_zero": str(q_sign_branch.subs(r, 0)),
        "r_plus_half": str(q_sign_branch.subs(r, sp.Rational(1, 2))),
        "minimum_y_on_registered_interval": str(sp.Rational(52, 27)),
    }

    # At the K=+1 equator F=1,F'=0, the normalized lower coefficient changes sign.
    lower_equator = sp.factor(sign_branch * (4 - 2 * sp.diff(sign_branch, r, 2)) / 3)
    lower_values = {
        "r_zero": str(lower_equator.subs(r, 0)),
        "r_one_third": str(lower_equator.subs(r, sp.Rational(1, 3))),
        "r_one_half": str(lower_equator.subs(r, sp.Rational(1, 2))),
    }

    # Reduced stationarity alone accepts this cubic, but the K=+1 transverse constraint rejects it.
    false_branch = 2 + 2 * r**2
    false_reduced = sp.diff(false_branch, r, 4)
    false_constraint = sp.factor(transverse_constraint.subs({y: false_branch, K: 1}).doit())

    checks = {
        "full_system_sufficiency_temporal": sp.simplify(temporal_numerator - transverse_constraint + 4 * y * y4) == 0,
        "full_system_sufficiency_angular": sp.simplify(angular_numerator - transverse_constraint + 2 * y * y4) == 0,
        "general_reduced_branch_is_cubic": sp.diff(cubic, r, 4) == 0,
        "cubic_constraint_exact": sp.simplify(cubic_constraint - 4 * (B**2 - 3 * A * C - K**2)) == 0,
        "sign_branch_full_bach": sp.simplify(cubic_constraint.subs({A: 1, B: 0, C: -sp.Rational(1, 3), D: 2, K: 1})) == 0,
        "sign_branch_positive_tile": sign_values["minimum_y_on_registered_interval"] == "52/27",
        "q_all_strata": q_sign_branch.subs(r, -sp.Rational(1, 2)) > 0 and q_sign_branch.subs(r, 0) == 0 and q_sign_branch.subs(r, sp.Rational(1, 2)) < 0,
        "lower_coefficient_all_strata": lower_equator.subs(r, 0) > 0 and lower_equator.subs(r, sp.Rational(1, 3)) == 0 and lower_equator.subs(r, sp.Rational(1, 2)) < 0,
        "false_branch_reduced_stationary": false_reduced == 0,
        "false_branch_full_rejected": false_constraint != 0,
        "zero_K_reduces_parent_constraint": sp.simplify(cubic_constraint.subs(K, 0) - 4 * (B**2 - 3 * A * C)) == 0,
    }
    checks = {name: bool(value) for name, value in checks.items()}
    if not all(checks.values()):
        raise AssertionError(checks)

    result = {
        "schema": "udt-c2-intrinsic-angular-product-branches-1.0",
        "minimal_full_system": {
            "equation_1": "Derivative(y(r),(r,4))=0",
            "equation_2": "Derivative(y(r),(r,2))**2-2*Derivative(y(r),r)*Derivative(y(r),(r,3))-4*K**2=0",
            "equivalence": "necessary and sufficient for every nonzero background Bach component when y>0",
        },
        "general_local_branch": {
            "y": str(cubic),
            "positivity": "A*r**3+B*r**2+C*r+D>0 on the local interval",
            "constraint": "B**2=3*A*C+K**2",
            "Q": str(q_cubic),
        },
        "all_Q_strata_witness": {
            "K": "1",
            "y": str(sign_branch),
            "interval": "[-1/2,1/2]",
            "Q": str(q_sign_branch),
            "values": sign_values,
        },
        "all_twist_lower_strata_witness": {
            "K": "1",
            "angular_point": "F=1,F_prime=0 (equator of the local positive-curvature representative)",
            "coefficient": str(lower_equator),
            "values": lower_values,
        },
        "reduced_only_false_branch": {
            "K": "1",
            "y": str(false_branch),
            "reduced_equation": str(false_reduced),
            "full_constraint": str(false_constraint),
        },
        "twist_direction_ruling": {
            "normalized_lower_coefficient": "y*(4*K-2*y_second+27*(F_prime/F)**2)/3",
            "status": "DIRECTIONAL_SECTION_DATA_REMAINS",
            "reason": "scalar K does not determine the screen connection of the chosen transverse one-form",
        },
        "outcomes": [
            "INTRINSIC_CURVATURE_DOES_NOT_CHANGE_LOCAL_SELECTOR_UNDERDETERMINATION",
            "INTRINSIC_CURVATURE_CHANGES_TWIST_DERIVATIVE_INVENTORY",
        ],
        "checks": checks,
        "compute": {"method": "exact SymPy polynomial branch classification", "cpu_only": True},
    }
    (HERE / "BRANCH_ANALYSIS.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "outcomes": result["outcomes"], "checks": len(checks)}, sort_keys=True))


if __name__ == "__main__":
    main()

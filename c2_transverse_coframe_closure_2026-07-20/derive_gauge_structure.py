#!/usr/bin/env python3
"""Exact local gauge and reflection structure of the toric transverse connection."""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
r, theta = sp.symbols("r theta", real=True)
lam = sp.Function("lambda")(r, theta)
Ar = sp.Function("A_r")(r, theta)
At = sp.Function("A_theta")(r, theta)


def main():
    transformed_r = Ar + sp.diff(lam, r)
    transformed_theta = At + sp.diff(lam, theta)
    curvature = sp.diff(At, r) - sp.diff(Ar, theta)
    transformed_curvature = sp.simplify(sp.diff(transformed_theta, r) - sp.diff(transformed_r, theta))

    # Determinant of a one-fiber Kaluza block is independent of both connection components.
    gtt, grr, htheta, radius = sp.symbols("gtt grr htheta radius", nonzero=True)
    ar, atheta = sp.symbols("ar atheta")
    base = sp.diag(gtt, grr, htheta)
    avec = sp.Matrix([0, ar, atheta])
    upper = base + radius**2 * avec * avec.T
    metric = upper.row_join(radius**2 * avec)
    metric = metric.col_join(sp.Matrix([[0, ar * radius**2, atheta * radius**2, radius**2]]))
    determinant = sp.factor(metric.det())
    expected_determinant = sp.factor(gtt * grr * htheta * radius**2)

    checks = {
        "connection_curvature_gauge_invariant": sp.simplify(transformed_curvature - curvature) == 0,
        "connection_independent_determinant": sp.simplify(determinant - expected_determinant) == 0,
        "radial_gauge_curvature": sp.simplify(curvature.subs({Ar: 0, At: sp.Function("u")(r)}) - sp.diff(sp.Function("u")(r), r)) == 0,
        "constant_radial_gauge_zero": sp.simplify(curvature.subs({Ar: 0, At: sp.Symbol("u0")})) == 0,
    }
    checks = {name: bool(value) for name, value in checks.items()}
    if not all(checks.values()):
        raise AssertionError(checks)

    result = {
        "schema": "udt-c2-transverse-coframe-gauge-structure-1.0",
        "gauge_law": {
            "coordinate": "psi -> psi-lambda(r,theta)",
            "A_r": str(transformed_r),
            "A_theta": str(transformed_theta),
            "curvature": str(curvature),
            "transformed_curvature": str(transformed_curvature),
        },
        "radial_toric_gauge": {
            "A_r": "0",
            "A_theta": "epsilon*u(r)",
            "H_rtheta": "epsilon*Derivative(u(r),r)",
            "scope": "local gauge only; global holonomy, periods, caps, and boundary data remain",
        },
        "reflection": {
            "map": "psi -> -psi, A -> -A",
            "even_fields": ["y", "a", "s", "F"],
            "consequence": "any diffeomorphism-scalar metric action is even in A about A=0, so its Hessian has no A-area or A-shear mixed block",
        },
        "determinant": str(determinant),
        "checks": checks,
        "compute": {"method": "exact SymPy exterior-component and block-determinant identities", "cpu_only": True},
    }
    (HERE / "GAUGE_STRUCTURE.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "checks": len(checks)}, sort_keys=True))


if __name__ == "__main__":
    main()

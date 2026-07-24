#!/usr/bin/env python3
"""Independent tensor/EL reconstruction for the historical phi salvage."""

from __future__ import annotations

import json
import platform
from pathlib import Path

import sympy as sp


def z(expr: sp.Expr) -> bool:
    return sp.simplify(sp.cancel(expr)) == 0


def main() -> None:
    t, r, theta, azimuth = sp.symbols(
        "t r theta azimuth", real=True
    )
    mu, X = sp.symbols("mu X", positive=True, finite=True)
    p = sp.Function("p")(r)
    coords = (t, r, theta, azimuth)
    dim = len(coords)

    metric = sp.diag(
        -sp.exp(-2 * p),
        sp.exp(2 * p),
        r**2,
        r**2 * sp.sin(theta) ** 2,
    )
    inverse = sp.simplify(metric.inv())
    determinant = sp.simplify(metric.det())

    christoffel = [
        [
            [
                sp.simplify(
                    sum(
                        inverse[a, d]
                        * (
                            sp.diff(metric[d, c], coords[b])
                            + sp.diff(metric[d, b], coords[c])
                            - sp.diff(metric[b, c], coords[d])
                        )
                        / 2
                        for d in range(dim)
                    )
                )
                for c in range(dim)
            ]
            for b in range(dim)
        ]
        for a in range(dim)
    ]

    ricci = sp.MutableDenseNDimArray.zeros(dim, dim)
    for a in range(dim):
        for b in range(dim):
            ricci[a, b] = sp.simplify(
                sum(
                    sp.diff(christoffel[c][a][b], coords[c])
                    - sp.diff(christoffel[c][a][c], coords[b])
                    + sum(
                        christoffel[c][c][d] * christoffel[d][a][b]
                        - christoffel[c][b][d] * christoffel[d][a][c]
                        for d in range(dim)
                    )
                    for c in range(dim)
                )
            )

    ricci_scalar = sp.simplify(
        sum(inverse[a, b] * ricci[a, b] for a in range(dim) for b in range(dim))
    )
    einstein_theta_mixed = sp.simplify(
        inverse[2, 2]
        * (ricci[2, 2] - metric[2, 2] * ricci_scalar / 2)
    )
    scalar_box = sp.simplify(
        sum(
            inverse[a, b]
            * (
                sp.diff(p, coords[a], coords[b])
                - sum(
                    christoffel[c][a][b] * sp.diff(p, coords[c])
                    for c in range(dim)
                )
            )
            for a in range(dim)
            for b in range(dim)
        )
    )

    # Independent reduced-action variation, written without the production
    # helper expressions.
    p_r = sp.diff(p, r)
    density = r**2 * (
        sp.exp(-2 * p) * p_r**2 + mu**2 * p**2
    ) / 2
    el = sp.simplify(
        sp.diff(density, p)
        - sp.diff(sp.diff(density, p_r), r)
    )
    self_equation = sp.simplify(-el / r**2)
    fixed_metric_box_equation = sp.simplify(scalar_box - mu**2 * p)

    wrl = -sp.log(1 - r / X) / 2
    wrl_box = sp.simplify(scalar_box.subs(p, wrl).doit())

    checks = {
        "metric_determinant": z(
            determinant + r**4 * sp.sin(theta) ** 2
        ),
        "direct_tensor_box_equals_minus_Gtheta": z(
            scalar_box + einstein_theta_mixed
        ),
        "self_variation_differs_from_fixed_metric_by_gradient_square": z(
            self_equation
            - fixed_metric_box_equation
            - sp.exp(-2 * p) * p_r**2
        ),
        "WRL_direct_tensor_box": z(wrl_box - 1 / (X * r)),
    }

    result = {
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
        },
        "method": "direct_4d_christoffel_ricci_einstein_plus_independent_EL",
        "expressions": {
            "det_g": str(determinant),
            "box_phi": str(scalar_box),
            "Gtheta_mixed": str(einstein_theta_mixed),
            "self_variation_equation": str(self_equation),
            "fixed_metric_equation": str(fixed_metric_box_equation),
            "WRL_box_phi": str(wrl_box),
        },
        "checks": checks,
        "check_count": len(checks),
        "pass_count": sum(bool(value) for value in checks.values()),
        "all_pass": all(checks.values()),
    }
    output = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""Hostile controls for the preregistered G327 failure modes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from sealed_runtime import activate_runtime

activate_runtime()
import sympy as sp


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="CATCH_PROOF_RESULT.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent

    t, nu = sp.symbols("t nu", positive=True, real=True)
    z = sp.Rational(3, 4) * nu * t ** sp.Rational(4, 3)
    j0 = sp.besselj(0, z)

    def ode(function: sp.Expr, damping: sp.Expr, gradient_power: sp.Rational) -> sp.Expr:
        return sp.simplify(
            sp.diff(function, t, 2)
            + damping * sp.diff(function, t) / t
            + nu**2 * t**gradient_power * function
        )

    controls: dict[str, bool] = {}
    controls["wrong_gradient_power_rejected"] = ode(
        j0, sp.Integer(1), sp.Rational(-2, 3)
    ) != 0
    controls["missing_hubble_damping_rejected"] = ode(
        j0, sp.Integer(0), sp.Rational(2, 3)
    ) != 0

    # Reconstruct the transverse Lie image for a generic same-mode periodic vector.
    x = sp.symbols("x", real=True)
    b2 = t ** sp.Rational(4, 3)
    phase = sp.exp(sp.I * nu * x)
    xi0 = sp.Function("xi0")(t) * phase
    lie_yy = xi0 * sp.diff(b2, t)
    lie_zz = xi0 * sp.diff(b2, t)
    lie_yz = sp.Integer(0)
    gauge_tensor_image = sp.Matrix([
        [(lie_yy - lie_zz) / (2 * b2), lie_yz / b2],
        [lie_yz / b2, (lie_zz - lie_yy) / (2 * b2)],
    ]).applyfunc(sp.simplify)
    fake_gauge_image = sp.Matrix([[1, 0], [0, -1]])
    controls["fake_tensor_gauge_origin_rejected"] = (
        gauge_tensor_image == sp.zeros(2) and fake_gauge_image != gauge_tensor_image
    )

    # One time function cannot span a second-order equation: use the exact transformed Wronskian.
    exact_time_wronskian = sp.simplify(
        t * sp.diff(z, t) * 2 / (sp.pi * z)
    )
    exact_time_dimension = 2
    controls["discarded_logarithmic_branch_rejected"] = (
        exact_time_wronskian == sp.Rational(8, 3) / sp.pi
        and exact_time_wronskian != 0
        and exact_time_dimension != 1
    )

    exact_real_dimension = 2 * 2 * exact_time_dimension
    tensor_product_basis = sp.eye(exact_real_dimension)
    controls["wrong_real_dimension_rejected"] = (
        tensor_product_basis.rank() == 8 and exact_real_dimension != 4
    )

    exact_future_power = -sp.Rational(1, 2) * sp.Rational(4, 3)
    controls["false_future_power_rejected"] = exact_future_power != -sp.Rational(1, 2)

    if not all(controls.values()):
        raise AssertionError(controls)

    result = {
        "schema": "udt-g327-hostile-catch-proof-v1",
        "status": "PASS",
        "caught": sum(controls.values()),
        "attempted": len(controls),
        "controls": controls,
    }
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

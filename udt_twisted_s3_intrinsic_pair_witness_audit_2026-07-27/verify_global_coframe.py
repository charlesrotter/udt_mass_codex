#!/usr/bin/env python3
"""Exact SymPy check of the quaternion Maurer-Cartan coframe used by the audit."""

from __future__ import annotations

import json

import sympy as sp


def main() -> int:
    x, y, z = sp.symbols("x y z", real=True)
    coordinates = (x, y, z)
    radius_squared = x**2 + y**2 + z**2
    denominator = 1 + radius_squared
    q = ((1 - radius_squared) / denominator,
         2 * x / denominator, 2 * y / denominator, 2 * z / denominator)
    assert sp.factor(sum(component**2 for component in q)) == 1
    dq = sp.Matrix([[sp.diff(component, coordinate) for coordinate in coordinates]
                    for component in q])
    sigma = sp.zeros(3, 3)
    for axis in range(3):
        sigma[0, axis] = (q[0] * dq[1, axis] - q[1] * dq[0, axis]
                          - q[2] * dq[3, axis] + q[3] * dq[2, axis])
        sigma[1, axis] = (q[0] * dq[2, axis] - q[2] * dq[0, axis]
                          - q[3] * dq[1, axis] + q[1] * dq[3, axis])
        sigma[2, axis] = (q[0] * dq[3, axis] - q[3] * dq[0, axis]
                          - q[1] * dq[2, axis] + q[2] * dq[1, axis])
    determinant = sp.factor(sigma.det())
    assert sp.simplify(determinant - 8 / denominator**3) == 0

    coordinate_pairs = ((0, 1), (0, 2), (1, 2))
    cyclic = ((1, 2), (2, 0), (0, 1))
    for form, (left_form, right_form) in enumerate(cyclic):
        for left, right in coordinate_pairs:
            exterior = sp.diff(sigma[form, right], coordinates[left]) - sp.diff(
                sigma[form, left], coordinates[right]
            )
            wedge = (sigma[left_form, left] * sigma[right_form, right]
                     - sigma[left_form, right] * sigma[right_form, left])
            assert sp.simplify(exterior + 2 * wedge) == 0

    result = {
        "status": "PASS",
        "quaternion_unit_norm": "EXACT",
        "stereographic_coframe_determinant": "8/(1+r^2)^3",
        "maurer_cartan_kappa": -2,
        "forms_checked": 3,
        "coordinate_two_form_components_checked": 9,
        "sympy_version": sp.__version__,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

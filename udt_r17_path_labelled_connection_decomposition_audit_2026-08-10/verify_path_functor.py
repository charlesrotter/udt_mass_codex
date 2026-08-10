#!/usr/bin/env python3
"""Exact finite-dimensional path composition, reversal, and O(2) checks."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
alpha, beta, chi_p, chi_q = sp.symbols("alpha beta chi_p chi_q", real=True)


def rotation(angle):
    return sp.Matrix([[sp.cos(angle), -sp.sin(angle)], [sp.sin(angle), sp.cos(angle)]])


def matrix_zero(matrix):
    return all(sp.trigsimp(value) == 0 for value in matrix)


def main() -> None:
    identity = sp.eye(2)
    reflection = sp.diag(1, -1)
    checks = {
        "identity": matrix_zero(rotation(0) - identity),
        "composition": matrix_zero(rotation(beta) * rotation(alpha) - rotation(alpha + beta)),
        "reversal": matrix_zero(rotation(-alpha) - rotation(alpha).inv()),
        "reflection_reverses_angle": matrix_zero(reflection * rotation(alpha) * reflection - rotation(-alpha)),
        "trace_is_reflection_safe": sp.trigsimp(sp.trace(rotation(alpha)) - sp.trace(rotation(-alpha))) == 0,
        "gauge_integral_endpoint_shift": sp.simplify((alpha + chi_q - chi_p) - alpha - (chi_q - chi_p)) == 0,
        "closed_loop_gauge_shift_zero": sp.simplify((alpha + chi_p - chi_p) - alpha) == 0,
    }
    if not all(checks.values()):
        raise SystemExit(f"FAIL: {checks}")
    result = {
        "schema": "udt-r17-path-functor-exact-v1",
        "status": "PASS",
        "checks": checks,
        "passed_checks": sum(checks.values()),
        "base_path_selected": False,
        "physical_arrow_derived": False,
    }
    (HERE / "PATH_FUNCTOR_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: 7/7 exact path-functor and O(2) checks")


if __name__ == "__main__":
    main()

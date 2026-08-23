#!/usr/bin/env python3
"""Structural mutation catches for the G228 bounded theorem."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp

from derive_neighboring_curvature_first_variation import (
    DIRECTION_ORDER,
    build_differential_bianchi_matrix,
    direction_projection,
    DIRECTIONS,
    screen_and_phase_checks,
)
from verify_full_index_anchor import build_full_constraints


def block2(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix, d: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.vstack(sp.Matrix.hstack(a, b), sp.Matrix.hstack(c, d))


def derive_catches() -> dict[str, object]:
    bianchi, _ = build_differential_bianchi_matrix()
    base_rank = int(bianchi.rank())

    # Independent-row deletion must enlarge the compatible module.
    _, independent_row_indices = bianchi.T.rref()
    deleted_row = int(independent_row_indices[0])
    removed = bianchi.copy()
    removed.row_del(deleted_row)
    removed_rank = int(removed.rank())

    # In the unreduced 84-slot representation, replacing differential
    # Bianchi with repeated algebraic-Bianchi rows leaves 80 modes rather
    # than 60.  This is an actual wrong-constraint mutant, not a zero stub.
    full_algebraic, _, full_combined = build_full_constraints()
    repeated_algebraic = sp.Matrix.vstack(*(full_algebraic for _ in range(6)))
    duplicate_rank = int(repeated_algebraic.rank())
    wrong_module_dimension = 84 - duplicate_rank

    kernel = sp.Matrix.hstack(*bianchi.nullspace())
    one_direction_ranks = {
        name: int((direction_projection(DIRECTIONS[name]) * kernel).rank())
        for name in DIRECTION_ORDER
    }
    k_image = direction_projection(DIRECTIONS["k"]) * kernel
    artificial_output_constraint = k_image[0, :]
    constrained_coefficients = sp.Matrix.hstack(*sp.Matrix([artificial_output_constraint]).nullspace())
    artificially_constrained_rank = int((k_image * constrained_coefficients).rank())

    screen = screen_and_phase_checks()
    theta, omega = sp.symbols("theta omega", real=True)
    a, b, d, ap, bp, dp = sp.symbols("a b d ap bp dp", real=True)
    c = sp.cos(theta)
    s = sp.sin(theta)
    C = sp.Matrix(((c, -s), (s, c)))
    J2 = sp.Matrix(((0, -1), (1, 0)))
    Omega = omega * J2
    Cp = C * Omega
    T = sp.Matrix(((a, b), (b, d)))
    Tp = sp.Matrix(((ap, bp), (bp, dp)))
    TE = sp.simplify(C.T * T * C)
    TEprime = sp.simplify(Cp.T * T * C + C.T * Tp * C + C.T * T * Cp)
    reversed_commutator = sp.simplify(TEprime - Omega * TE + TE * Omega - C.T * Tp * C)

    I2 = sp.eye(2)
    Z2 = sp.zeros(2, 2)
    J4 = block2(Z2, I2, -I2, Z2)
    nonsymmetric_tide = sp.Matrix(((1, 2), (3, 4)))
    A_bad_tide = block2(-Omega, I2, -nonsymmetric_tide, -Omega)
    bad_tide_residual = sp.simplify(A_bad_tide.T * J4 + J4 * A_bad_tide)

    nonskew_connection = sp.Matrix(((1, 0), (0, 0)))
    A_bad_connection = block2(-nonskew_connection, I2, -sp.eye(2), -nonskew_connection)
    bad_connection_residual = sp.simplify(A_bad_connection.T * J4 + J4 * A_bad_connection)

    A_missing_upper = block2(Z2, I2, -sp.eye(2), -Omega)
    missing_upper_residual = sp.simplify(A_missing_upper.T * J4 + J4 * A_missing_upper)
    A_missing_lower = block2(-Omega, I2, -sp.eye(2), Z2)
    missing_lower_residual = sp.simplify(A_missing_lower.T * J4 + J4 * A_missing_lower)

    # Exact within-Jacobi finite-transfer ambiguity.  Start with the scalar
    # one-period oscillator u_ff + (2*pi)^2 u = 0.  Under the Liouville
    # reparameterization y=u(f)/sqrt(f'), the Jacobi tide is
    # (2*pi)^2 f'^2 + {f,t}/2.  The chosen f has identity endpoint jets, so
    # the full phase at t=1 stays I while the initial tide derivative changes.
    t = sp.symbols("t", real=True)
    epsilon = sp.Rational(1, 100)
    f = t + epsilon * (1 - sp.cos(2 * sp.pi * t)) ** 2
    fp = sp.diff(f, t)
    schwarzian = sp.diff(f, t, 3) / fp - sp.Rational(3, 2) * (sp.diff(f, t, 2) / fp) ** 2
    tide = sp.simplify((2 * sp.pi) ** 2 * fp ** 2 + sp.Rational(1, 2) * schwarzian)
    endpoint_jets = {
        "f0": sp.simplify(f.subs(t, 0)),
        "f1": sp.simplify(f.subs(t, 1)),
        "fp0": sp.simplify(fp.subs(t, 0)),
        "fp1": sp.simplify(fp.subs(t, 1)),
        "fpp0": sp.simplify(sp.diff(f, t, 2).subs(t, 0)),
        "fpp1": sp.simplify(sp.diff(f, t, 2).subs(t, 1)),
    }
    endpoint_same = endpoint_jets == {
        "f0": 0, "f1": 1, "fp0": 1, "fp1": 1, "fpp0": 0, "fpp1": 0,
    }
    tide_derivative = sp.simplify(sp.diff(tide, t).subs(t, 0))
    derivative_distinct = tide_derivative != 0
    monotone_bound = 1 - 8 * sp.pi * epsilon > 0

    root = Path(__file__).resolve().parent
    outcome_docs = [root / "AUDIT_REPORT.md", root / "EXACT_DERIVATION.md", root / "EVIDENCE_GATES.md"]
    value_nonpromotion = all(
        "does not generate" in path.read_text().lower()
        or "not generate" in path.read_text().lower()
        for path in outcome_docs
    )

    catches = {
        "delete_independent_bianchi_row": removed_rank == base_rank - 1,
        "algebraic_bianchi_duplicate_is_not_differential_bianchi": duplicate_rank == 4 and wrong_module_dimension == 80 and int(full_combined.rank()) == 24,
        "artificial_one_direction_constraint_detected": all(rank == 20 for rank in one_direction_ranks.values()) and artificially_constrained_rank == 19,
        "isolated_finite_jacobi_phase_derivative_ambiguity": endpoint_same and derivative_distinct and bool(monotone_bound),
        "omit_screen_commutator": bool(screen["omitted_commutator_detected"]),
        "reverse_screen_commutator_sign": reversed_commutator != sp.zeros(2, 2),
        "nonsymmetric_tide_breaks_symplecticity": bad_tide_residual != sp.zeros(4, 4),
        "nonskew_connection_breaks_symplecticity": bad_connection_residual != sp.zeros(4, 4),
        "delete_upper_connection_block": missing_upper_residual != sp.zeros(4, 4),
        "delete_lower_connection_block": missing_lower_residual != sp.zeros(4, 4),
        "outcome_docs_retain_value_generation_ceiling": value_nonpromotion,
    }
    return {
        "base_bianchi_rank": base_rank,
        "deleted_independent_row": deleted_row,
        "removed_row_rank": removed_rank,
        "algebraic_duplicate_rank": duplicate_rank,
        "wrong_duplicate_module_dimension": wrong_module_dimension,
        "one_direction_ranks": one_direction_ranks,
        "artificially_constrained_one_direction_rank": artificially_constrained_rank,
        "liouville_endpoint_jets": {key: str(value) for key, value in endpoint_jets.items()},
        "liouville_tide_derivative_at_zero": str(tide_derivative),
        "catches": catches,
        "passed": sum(bool(value) for value in catches.values()),
        "total": len(catches),
        "all_pass": all(bool(value) for value in catches.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "HOSTILE_CATCH_RESULT.json")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = derive_catches()
    if not args.no_write:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

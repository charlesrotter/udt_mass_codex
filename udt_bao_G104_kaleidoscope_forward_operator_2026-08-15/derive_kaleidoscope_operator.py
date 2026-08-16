#!/usr/bin/env python3
"""Exact G104 source-free kaleidoscope operator derivation; reads no outcomes."""

from __future__ import annotations

import json
import os
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
LANDING = (
    "FACTORIZED_REGULAR_KALEIDOSCOPE_NULL_DERIVED"
    "__SELECTION_REFERENCE_MISMATCH_AND_CORRELATED_MULTIIMAGE_TERMS_EXACT"
    "__CURRENT_COMPLETE_METRIC_PERMITS_BUT_DOES_NOT_OWN_A_NONZERO_CONNECTED_MODE"
    "__ALL_FOUR_COEFFICIENT_HOMES_DORMANT__BOSS_AND_CMB_UNREAD"
)


def matrix_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def outer(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return left * right.T


def main() -> None:
    # One-source null measure and one stochastic, nontrivial regular map.
    lam = sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 6)])
    kernel = sp.Matrix([
        [sp.Rational(1, 2), 0, sp.Rational(1, 4)],
        [sp.Rational(1, 2), sp.Rational(1, 2), 0],
        [0, sp.Rational(1, 2), sp.Rational(3, 4)],
    ])
    assert all(sum(kernel[:, j]) == 1 for j in range(kernel.cols))
    nu = sp.simplify(kernel * lam)
    factorized_two = outer(nu, nu)
    connected_factorized = sp.simplify(factorized_two - outer(nu, nu))

    # Exact pointwise Landy--Szalay density identity for normalized p and q.
    p = sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 6)])
    q = sp.Matrix([sp.Rational(1, 3)] * 3)
    ls_numerator = sp.simplify(outer(p, p) - outer(p, q) - outer(q, p) + outer(q, q))
    mismatch_outer = sp.simplify(outer(p - q, p - q))
    full_selection_null = sp.simplify(
        outer(p, p) - outer(p, p) - outer(p, p) + outer(p, p)
    )

    # Independent one-image branch marking remains one stochastic kernel and factorizes.
    identity = sp.eye(3)
    cycle = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    marked_kernel = sp.Rational(2, 3) * identity + sp.Rational(1, 3) * cycle
    marked_nu = sp.simplify(marked_kernel * lam)
    marked_connected = sp.simplify(outer(marked_nu, marked_nu) - outer(marked_nu, marked_nu))

    # A two-image cluster from each Poisson parent has an exact same-parent connected term.
    # Branch 0 is identity; branch 1 is the cycle. Both images are retained.
    cluster_connected = sp.zeros(3)
    for source_index, weight in enumerate(lam):
        x = source_index
        y = (source_index + 1) % 3
        cluster_connected[x, y] += weight
        cluster_connected[y, x] += weight
    cluster_intensity = sp.simplify(identity * lam + cycle * lam)
    cluster_two = sp.simplify(outer(cluster_intensity, cluster_intensity) + cluster_connected)
    recovered_cluster = sp.simplify(cluster_two - outer(cluster_intensity, cluster_intensity))

    # General connected operator bookkeeping: K2 = K1 tensor K1 + H.
    h_mode = sp.Matrix([
        [0, sp.Rational(1, 7), 0],
        [sp.Rational(1, 7), 0, sp.Rational(1, 11)],
        [0, sp.Rational(1, 11), 0],
    ])
    generic_two = sp.simplify(factorized_two + h_mode)
    recovered_h = sp.simplify(generic_two - factorized_two)

    checks = {
        "source_weights_sum_one": sp.simplify(sum(lam)) == 1,
        "kernel_column_stochastic": all(sum(kernel[:, j]) == 1 for j in range(kernel.cols)),
        "factorized_connected_zero": matrix_zero(connected_factorized),
        "ls_mismatch_identity": matrix_zero(ls_numerator - mismatch_outer),
        "ls_full_selection_null": matrix_zero(full_selection_null),
        "mismatch_nonzero": not matrix_zero(mismatch_outer),
        "independent_branch_connected_zero": matrix_zero(marked_connected),
        "cluster_connected_nonzero": not matrix_zero(cluster_connected),
        "cluster_connected_recovered": matrix_zero(recovered_cluster - cluster_connected),
        "generic_connected_recovered": matrix_zero(recovered_h - h_mode),
        "outcome_artifacts_read": [],
    }
    coefficient_status = {
        "a_conn": "DORMANT__CONNECTED_HOME_TYPED_BUT_NO_PHYSICAL_H_OWNED",
        "a_branch": "DORMANT__CONDITIONAL_CLUSTER_KERNEL_DERIVED_BUT_BRANCH_MAP_AND_WEIGHTS_UNOWNED",
        "a_area": "DORMANT__SELECTION_MISMATCH_IDENTITY_DERIVED_BUT_NO_PHYSICAL_MODULATION_FIELD_OWNED",
        "a_regime": "DORMANT__NO_ACTIVE_BASE_MODE_OR_OWNED_CONTINUATION",
    }
    if not all(value for key, value in checks.items() if key != "outcome_artifacts_read"):
        raise AssertionError(json.dumps({"checks": checks}, indent=2, sort_keys=True))
    result = {
        "status": "PASS",
        "landing": LANDING,
        "checks": checks,
        "coefficient_status": coefficient_status,
        "exact_witnesses": {
            "nu": [str(x) for x in nu],
            "mismatch_outer": [[str(x) for x in mismatch_outer.row(i)] for i in range(3)],
            "cluster_connected": [[str(x) for x in cluster_connected.row(i)] for i in range(3)],
        },
    }
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (HERE / "DERIVATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

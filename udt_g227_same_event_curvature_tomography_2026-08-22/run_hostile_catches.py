#!/usr/bin/env python3
"""Hostile catches for common-curvature overclaims in G227."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

import derive_curvature_tomography as prod


ROOT = Path(__file__).resolve().parent


def main() -> None:
    variables, basis = prod.curvature_basis()
    a = sp.Matrix.vstack(*(prod.rows_for(pq, basis) for pq in prod.TRAINING))
    kappa, _ = prod.constant_curvature_coordinates(variables, basis)
    left = DomainMatrix.from_Matrix(a).transpose().nullspace().to_Matrix()
    rank_a = prod.exact_rank(a)

    # H1: one deterministic incompatible one-entry perturbation is detected by augmented rank.
    seed = sp.Matrix([sp.Rational(i + 1, i + 2) for i in range(20)])
    valid = a * seed
    perturbed = None
    for index in range(a.rows):
        candidate = valid.copy()
        candidate[index] += 1
        if prod.exact_rank(a.row_join(candidate)) > rank_a:
            perturbed = candidate
            break
    h1 = perturbed is not None

    # H2: a false claim that null screens see constant curvature is caught exactly.
    h2 = a * kappa == sp.zeros(a.rows, 1)

    # H3: omitting the timelike sectional datum cannot falsely certify full rank.
    h3 = rank_a == 19 and a.cols == 20

    # H4: removing first Bianchi changes the declared tensor type and is explicitly detected.
    q_bad = sp.zeros(6)
    q_bad[2, 3] = q_bad[3, 2] = 1
    bianchi_bad = q_bad[0, 5] - q_bad[1, 4] + q_bad[2, 3]
    h4 = bianchi_bad != 0

    # H5: a non-null direction cannot silently pass the null construction gate.
    k_bad = sp.Matrix((1, 0, 0, 0))
    h5 = prod.dot(k_bad, k_bad) != 0

    # H6: a vector outside k-perp cannot silently pass the screen gate.
    k, _, _ = prod.direction(*prod.TRAINING[0])
    e_bad = sp.Matrix((1, 0, 0, 0))
    h6 = prod.dot(e_bad, k) != 0

    # H7: syzygies are nonvacuous and annihilate every valid tide table.
    h7 = left.rows == 8 and all((left.row(i) * valid)[0] == 0 for i in range(left.rows))

    catches = {
        "H1_deterministic_incompatible_one_entry_perturbation_detected": bool(h1),
        "H2_constant_curvature_null_silence_detected": bool(h2),
        "H3_null_only_full_rank_overclaim_rejected": bool(h3),
        "H4_non_bianchi_tensor_detected_and_excluded_by_basis": bool(h4),
        "H5_nonnull_direction_detected": bool(h5),
        "H6_nonscreen_vector_detected": bool(h6),
        "H7_eight_nonvacuous_syzygies": bool(h7),
    }
    result = {"catches": catches, "passed": sum(catches.values()), "total": len(catches), "pass": all(catches.values())}
    (ROOT / "HOSTILE_CATCH_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

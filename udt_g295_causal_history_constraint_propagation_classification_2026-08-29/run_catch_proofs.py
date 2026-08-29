#!/usr/bin/env python3
"""Hostile mutations and semantic non-promotion gates for G295."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def zero(a):
    return all(value == 0 for row in a for value in row)


def lower(a):
    return all(a[i][j] == 0 for i in range(len(a)) for j in range(len(a[0])) if j > i)


def main() -> None:
    catches = []

    def record(name, caught, reason):
        catches.append({"name": name, "caught": bool(caught), "reason": reason})
        if not caught:
            raise AssertionError(name)

    A = [[-1, 1, 0]]
    mutated_update = [[2, 0, 0], [2, 1, 0], [0, 0, 1]]
    record("missing_constraint_compensation", not zero(mm(A, mutated_update)), "AU no longer factors through A")

    dense_projection = [[0.5, 0, 0.5], [0, 1, 0], [0.5, 0, 0.5]]
    record("dense_projection_called_causal", not lower(dense_projection), "off-cone upper entry remains")

    causal_bad = [[1, 0, 0], [0, 2, 0], [0, 0, 1]]
    record("causal_mask_called_constraint_propagation", not zero(mm(A, causal_bad)), "causality does not imply preservation")

    cycle = [[1, 1, -1]]
    B = [[-1, 1, 0], [0, -1, 1], [-1, 0, 1]]
    v1 = [[0], [1], [2]]
    v2 = [[0], [3], [-4]]
    record(
        "cycle_identity_called_value_selector",
        zero(mm(cycle, mm(B, v1))) and zero(mm(cycle, mm(B, v2))) and mm(B, v1) != mm(B, v2),
        "distinct values satisfy the same composition identity",
    )

    full_a = [[2, 0, 0, 0], [1, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    full_b = [row[:] for row in full_a]
    full_b[3][2] = 5
    record("scalar_constraint_called_complete_screen_law", full_a != full_b, "screen update changes invisibly to scalar constraint")

    U = [[2, 0, 0], [1, 1, 0], [0, 1, 3]]
    x1 = [[1], [1], [0]]
    x2 = [[2], [2], [1]]
    for _ in range(3):
        x1 = mm(U, x1)
        x2 = mm(U, x2)
    record("one_law_called_one_history", x1 != x2 and zero(mm(A, x1)) and zero(mm(A, x2)), "initial data remain")

    founding = (REPO / "founding.md").read_text(encoding="utf-8")
    record("W6_called_constraint_formula", "concrete constraint and causal preservation law remain `OPEN`" in founding, "W6 retains formula boundary")
    record("W6_called_global_now", "does not assert a universal global present" in founding, "W6 retains foliation boundary")
    record("W6_called_kernel_change", "changes neither F1--F4, W1, W5, the metric, nor the reciprocal kernel" in founding, "kernel non-regression explicit")

    premise_text = (ROOT / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    record("finite_matrix_called_field_equation", "MATHEMATICAL_METHOD_ONLY" in premise_text, "method provenance explicit")
    record("slicing_called_preferred_foliation", "FREE_AND_NOT_ADOPTED" in premise_text, "slicing ownership remains open")
    record("observations_smuggled_into_classification", "observations\tOMITTED" in premise_text, "outcome blindness explicit")

    result = {
        "all_pass": all(item["caught"] for item in catches),
        "catch_count": len(catches),
        "catches": catches,
    }
    (ROOT / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

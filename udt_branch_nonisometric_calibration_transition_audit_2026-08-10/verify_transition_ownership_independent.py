#!/usr/bin/env python3
"""Independent stdlib/Fraction replay of the path-carried transition theorem and census."""

from __future__ import annotations

import csv
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def eye(n: int):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def diag(*values):
    return [[F(values[i]) if i == j else F(0) for j in range(len(values))] for i in range(len(values))]


def load(path: Path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    eta = diag(-1, 1, 1, 1)
    e = diag(F(1, 4), 4, 2, 2)
    u1 = [
        [F(5, 3), F(0), F(4, 3), F(0)],
        [F(0), F(1), F(0), F(0)],
        [F(4, 3), F(0), F(5, 3), F(0)],
        [F(0), F(0), F(0), F(1)],
    ]
    u2 = [
        [F(1), F(0), F(0), F(0)],
        [F(0), F(3, 5), F(0), -F(4, 5)],
        [F(0), F(0), F(1), F(0)],
        [F(0), F(4, 5), F(0), F(3, 5)],
    ]
    checks = {}
    checks["u1_lorentz"] = mul(mul(transpose(u1), eta), u1) == eta
    checks["u2_lorentz"] = mul(mul(transpose(u2), eta), u2) == eta
    a1 = mul(u1, e)
    checks["nonisometric"] = mul(mul(transpose(a1), eta), a1) != eta
    checks["strain"] = mul(mul(eta, transpose(a1)), mul(eta, a1)) == mul(e, e)
    pair = [[sum(a1[k][i] * eta[k][k] * a1[k][j] for k in range(4)) for j in range(2)] for i in range(2)]
    checks["terminal_pair"] = pair == [[-F(1, 16), F(0)], [F(0), F(16)]]
    checks["reciprocal_multiplier"] = (-pair[0][0]) / (-pair[0][0] * pair[1][1]) == F(1, 16)

    # With target grading carried by U1, its scale operator is U1 E U1^-1.
    u1_inv = mul(mul(eta, transpose(u1)), eta)
    eq = mul(mul(u1, e), u1_inv)
    a2 = mul(u2, eq)
    checks["composition"] = mul(a2, a1) == mul(mul(u2, u1), mul(e, e))

    atlas = load(HERE / "TRANSITION_OWNERSHIP_ATLAS.tsv")
    parent = load(ROOT / "udt_global_relation_family_branch_classification_2026-08-10/GLOBAL_RELATION_FAMILY_CLASSIFICATION.tsv")
    checks["coverage_24"] = len(atlas) == len(parent) == 24
    checks["unique_ids"] = len({row["branch_id"] for row in atlas}) == 24
    checks["same_identity_order"] = [row["stable_identity"] for row in atlas] == [row["stable_identity"] for row in parent]
    positive = [row for row in atlas if row["primary_disposition"] == "COMPLETE_NONISOMETRIC_TRANSITION_OWNED"]
    checks["zero_branch_owned_complete_transitions"] = len(positive) == 0
    r17 = next(row for row in atlas if row["branch_id"] == "R17")
    checks["r17_conditional_only"] = r17["primary_disposition"] == "CONDITIONAL_QUERY_OR_PRESENTATION_TRANSITION_ONLY"
    checks["r17_assembly_not_owned"] = "NOT_BRANCH_OWNED" in r17["nonisometric_transition"]
    checks["w02_partial"] = atlas[17]["primary_disposition"] == "PARTIAL_CLOCK_SCALE_TRANSITION_OWNED"
    checks["toric_set_only"] = atlas[23]["primary_disposition"] == "STRATIFIED_PROJECTOR_TRANSPORT_ONLY"
    assert all(checks.values()), [key for key, value in checks.items() if not value]
    result = {"schema": "udt-branch-transition-independent-v1", "status": "PASS", "checks": checks}
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"PASS: {len(checks)}/{len(checks)} independent Fraction and census checks")


if __name__ == "__main__":
    main()

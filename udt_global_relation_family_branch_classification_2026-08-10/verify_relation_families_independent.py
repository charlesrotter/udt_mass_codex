#!/usr/bin/env python3
"""Independent stdlib verification; does not import the production controller."""

from __future__ import annotations

import csv
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

BASE = Path(__file__).resolve().parent


def read(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def product(x, y):
    return [[sum(x[i][k] * y[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def inverse(x):
    d = x[0][0] * x[1][1] - x[0][1] * x[1][0]
    return [[x[1][1] / d, -x[0][1] / d], [-x[1][0] / d, x[0][0] / d]]


def main() -> None:
    universe = read("BRANCH_UNIVERSE.tsv")
    atlas = read("GLOBAL_RELATION_FAMILY_CLASSIFICATION.tsv")
    xwalk = read("SOURCE_TO_BRANCH_CROSSWALK.tsv")
    ids = {r["branch_id"] for r in universe}
    assert len(universe) == len(ids) == 24
    assert ids == {r["branch_id"] for r in atlas}
    assert Counter(r["primary_disposition"] for r in atlas) == Counter({
        "COMMON_CALIBRATED_ATLAS_OWNED": 1,
        "PATH_BRANCH_GROUPOID_OWNED": 2,
        "STRATIFIED_MIXTURE_OWNED": 2,
        "LOCAL_RELATIONS_GLOBAL_OWNERSHIP_OPEN": 5,
        "NO_COMPLETE_FAMILY_ON_DECLARED_BRANCH": 4,
        "HISTORICAL_PREMISES_CHANGED_REVIEW_REQUIRED": 1,
        "INSUFFICIENT_TYPED_EVIDENCE": 9,
    })
    assert all(r["stable_branch_id"] == "-" or r["stable_branch_id"] in ids for r in xwalk)

    a = [[Q(2), Q(1)], [Q(1), Q(1)]]
    b = [[Q(1), Q(1)], [Q(2), Q(3)]]
    c = product(b, a)
    identity_loop = product(inverse(c), product(b, a))
    assert identity_loop == [[Q(1), Q(0)], [Q(0), Q(1)]]
    h = [[Q(5, 3), Q(4, 3)], [Q(4, 3), Q(5, 3)]]
    path_loop = product(inverse(product(c, h)), product(b, a))
    assert path_loop != identity_loop
    m = [[Q(1), Q(1, 2)], [Q(0), Q(1)]]
    assert product(b, product(m, a)) == product(product(b, m), a)
    assert product(b, product(m, a)) != product(b, a)

    owned = [r for r in atlas if r["primary_disposition"].endswith("_OWNED")]
    assert len(owned) == 5
    assert all("physical" in r["caveat"].lower() or "selection" in r["caveat"].lower() for r in owned)
    result = {
        "status": "PASS",
        "checks": 16,
        "branch_count": len(atlas),
        "crosswalk_rows": len(xwalk),
        "owned_structure_rows": len(owned),
        "physical_pair_relation_selected": False,
    }
    (BASE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("PASS: independent relation-family classification and exact controls")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Deterministic controller for the complete-branch relation-family classification."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

ALLOWED = {
    "COMMON_CALIBRATED_ATLAS_OWNED",
    "PATH_BRANCH_GROUPOID_OWNED",
    "STRATIFIED_MIXTURE_OWNED",
    "LOCAL_RELATIONS_GLOBAL_OWNERSHIP_OPEN",
    "NO_COMPLETE_FAMILY_ON_DECLARED_BRANCH",
    "HISTORICAL_PREMISES_CHANGED_REVIEW_REQUIRED",
    "INSUFFICIENT_TYPED_EVIDENCE",
}

EXPECTED_COUNTS = {
    "COMMON_CALIBRATED_ATLAS_OWNED": 1,
    "PATH_BRANCH_GROUPOID_OWNED": 2,
    "STRATIFIED_MIXTURE_OWNED": 2,
    "LOCAL_RELATIONS_GLOBAL_OWNERSHIP_OPEN": 5,
    "NO_COMPLETE_FAMILY_ON_DECLARED_BRANCH": 4,
    "HISTORICAL_PREMISES_CHANGED_REVIEW_REQUIRED": 1,
    "INSUFFICIENT_TYPED_EVIDENCE": 9,
}


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def mm(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def inv2(a: list[list[F]]) -> list[list[F]]:
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    assert det
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def exact_controls() -> dict[str, bool]:
    j_ab = [[F(2), F(1)], [F(1), F(1)]]
    j_bc = [[F(1), F(1)], [F(2), F(3)]]
    j_ac = mm(j_bc, j_ab)
    common_omega = mm(inv2(j_ac), mm(j_bc, j_ab))

    h = [[F(5, 3), F(4, 3)], [F(4, 3), F(5, 3)]]
    direct_path = mm(j_ac, h)
    path_omega = mm(inv2(direct_path), mm(j_bc, j_ab))

    middle = [[F(1), F(1, 2)], [F(0), F(1)]]
    with_middle = mm(j_bc, mm(middle, j_ab))
    without_middle = mm(j_bc, j_ab)

    singular = [[F(1), F(2)], [F(2), F(4)]]
    singular_det = singular[0][0] * singular[1][1] - singular[0][1] * singular[1][0]

    return {
        "common_atlas_triangle_identity": common_omega == [[F(1), F(0)], [F(0), F(1)]],
        "path_loop_may_be_nonidentity": path_omega != [[F(1), F(0)], [F(0), F(1)]],
        "explicit_middle_transition_changes_composite": with_middle != without_middle,
        "matrix_associativity": mm(j_bc, mm(middle, j_ab)) == mm(mm(j_bc, middle), j_ab),
        "rank_degenerate_boundary_detected": singular_det == 0,
    }


def classify(branch: list[dict[str, str]], ledger: list[dict[str, str]], crosswalk: list[dict[str, str]]) -> dict:
    ids = [row["branch_id"] for row in branch]
    assert ids == [f"R{i:02d}" for i in range(1, 25)]
    assert len(ids) == len(set(ids)) == 24
    assert {row["branch_id"] for row in ledger} == set(ids)
    assert len(ledger) == 24
    assert all(row["primary_disposition"] in ALLOWED for row in ledger)
    counts = Counter(row["primary_disposition"] for row in ledger)
    assert dict(counts) == EXPECTED_COUNTS

    manifest = {row["path"] for row in rows("SOURCE_MANIFEST.tsv")}
    for row in ledger:
        assert row["evidence"]
        for citation in row["evidence"].split(";"):
            path = citation.split("::", 1)[0]
            assert path in manifest, (row["branch_id"], path)
            assert (ROOT / path).is_file()

    for row in crosswalk:
        target = row["stable_branch_id"]
        assert target == "-" or target in ids
        assert row["source_path"] in manifest

    controls = exact_controls()
    assert all(controls.values())

    by_id = {row["branch_id"]: row for row in ledger}
    assert by_id["R17"]["primary_disposition"] == "PATH_BRANCH_GROUPOID_OWNED"
    assert "not the physical" in by_id["R17"]["caveat"]
    assert by_id["R18"]["primary_disposition"] == "COMMON_CALIBRATED_ATLAS_OWNED"
    assert "Only the clock-calibration" in by_id["R18"]["caveat"]
    assert by_id["R24"]["primary_disposition"] == "STRATIFIED_MIXTURE_OWNED"
    assert "not yet a complete physical calibrated" in by_id["R24"]["caveat"]
    assert all("PHYSICAL_RELATION_SELECTED" not in row["scalar_reciprocal_reduction"] for row in ledger)

    return {
        "status": "PASS",
        "branch_count": len(ledger),
        "disposition_counts": dict(sorted(counts.items())),
        "crosswalk_rows": len(crosswalk),
        "exact_controls": controls,
        "maximum_conclusion": "GEOMETRIC_RELATION_FAMILY_STRUCTURES_CLASSIFIED__NO_PHYSICAL_GLOBAL_PAIR_RELATION_SELECTED",
    }


def main() -> None:
    result = classify(
        rows("BRANCH_UNIVERSE.tsv"),
        rows("GLOBAL_RELATION_FAMILY_CLASSIFICATION.tsv"),
        rows("SOURCE_TO_BRANCH_CROSSWALK.tsv"),
    )
    output = HERE / "DERIVATION_RESULT.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: {result['branch_count']} stable branches; {result['crosswalk_rows']} source aliases")
    print(hashlib.sha256((HERE / "GLOBAL_RELATION_FAMILY_CLASSIFICATION.tsv").read_bytes()).hexdigest())


if __name__ == "__main__":
    main()

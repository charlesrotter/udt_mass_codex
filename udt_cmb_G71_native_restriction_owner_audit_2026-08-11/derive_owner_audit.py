#!/usr/bin/env python3
"""Deterministic exact checks and census for the G71 restriction-owner audit."""

from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ALLOWED = {
    "OWNED_NATIVE", "DERIVED_CONDITIONAL_ON_QUERY", "CHOSE_CONTROL",
    "WORKING_GLOBAL_FRAME_ONLY", "OPEN_NO_OWNER", "TYPE_MISMATCH", "NOT_RELEVANT",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def tr(a):
    return [[a[j][i] for j in range(2)] for i in range(2)]


def inv(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    assert det
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def main() -> None:
    manifest = table(HERE / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == 21
    assert len({row["path"] for row in manifest}) == 21
    assert all(digest(ROOT / row["path"]) == row["sha256"] for row in manifest)

    targets = table(HERE / "OWNER_TARGET_LEDGER.tsv")
    atlas = table(HERE / "SOURCE_TARGET_ATLAS.tsv")
    graph = table(HERE / "DEPENDENCY_GRAPH.tsv")
    assert len(targets) == 6 and len(atlas) == 21 and len(graph) == 16
    assert {row["source_path"] for row in atlas} == {row["path"] for row in manifest}
    assert len({row["target"] for row in targets}) == 6
    status_columns = ("source_shape", "source_normalization", "physical_endpoint",
                      "physical_profile", "geometric_carry", "observable_carry")
    assert all(row["status"] in ALLOWED for row in targets)
    assert all(row[column] in ALLOWED for row in atlas for column in status_columns)
    assert not any(row["status"] == "OWNED_NATIVE" for row in targets)
    assert [row["status"] for row in targets].count("DERIVED_CONDITIONAL_ON_QUERY") == 1
    assert next(row for row in targets if row["target"] == "GEOMETRIC_CARRY_OWNER")["status"] == "DERIVED_CONDITIONAL_ON_QUERY"

    matrices = [
        [[F(2), F(1)], [F(1), F(1)]],
        [[F(3), F(-1)], [F(2), F(1)]],
        [[F(1), F(2)], [F(-1), F(3)]],
        [[F(5), F(2)], [F(1), F(1)]],
    ]
    covariances = [
        [[F(2), F(1, 3)], [F(1, 3), F(1)]],
        [[F(3), F(-1, 4)], [F(-1, 4), F(2)]],
        [[F(1), F(0)], [F(0), F(4)]],
    ]
    exact_trials = 0
    for dmat in matrices:
        di = inv(dmat)
        for observed in covariances:
            source = mm(mm(di, observed), tr(di))
            replay = mm(mm(dmat, source), tr(dmat))
            assert replay == observed
            assert source[0][0] > 0 and det(source) > 0
            exact_trials += 1

    result = {
        "schema": "udt-cmb-g71-owner-audit-v1",
        "primary_landing": "GEOMETRIC_CARRY_OWNED__OBSERVABLE_AND_SELECTION_OWNERS_OPEN",
        "source_manifest_rows": len(manifest),
        "owner_targets": len(targets),
        "source_target_rows": len(atlas),
        "dependency_edges": len(graph),
        "owned_native_targets": 0,
        "derived_conditional_targets": 1,
        "open_or_mismatched_physical_restriction_targets": 5,
        "exact_source_congruence_trials": exact_trials,
        "new_ODE_solves": 0,
        "observational_anchors_used": 0,
        "protected_draft_contents_read": False,
        "maximum_conclusion": "source-bounded typed ownership result only",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

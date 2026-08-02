#!/usr/bin/env python3
"""Independent stdlib reconstruction of the interface logic and source rulings."""

from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def rank2(matrix: list[list[F]]) -> int:
    assert all(len(row) == 2 for row in matrix)
    if not matrix or all(value == 0 for row in matrix for value in row):
        return 0
    for i, left in enumerate(matrix):
        for right in matrix[i + 1 :]:
            if left[0] * right[1] - left[1] * right[0] != 0:
                return 2
    return 1


def main() -> int:
    checks: list[bool] = []

    # Independent Jacobian construction; r=2 is a regular nonidentity control.
    r = F(2)
    graph = [[-r, F(1)]]
    local = graph + [[F(1), F(0)]]
    global_only = graph + [[F(0), F(1)]]
    coupled = graph + [[F(1), F(-1)]]
    reconstructed_ranks = {
        "graph_only": rank2(graph),
        "local_only_plus_graph": rank2(local),
        "global_only_plus_graph": rank2(global_only),
        "coupled_plus_graph_generic_r": rank2(coupled),
    }
    checks.extend((reconstructed_ranks["graph_only"] == 1, all(reconstructed_ranks[key] == 2 for key in reconstructed_ranks if key != "graph_only")))

    xs = ("x0", "x1", "x2", "x3")
    readout = {"x0": "o0", "x1": "o1", "x2": "o1", "x3": "o2"}
    global_window = {"o0": set(), "o1": set(xs), "o2": set()}
    local_projector = {"x1", "x2"}
    separable = {"o0": set(), "o1": local_projector, "o2": set()}
    modulated = {"o0": {"x0"}, "o1": {"x1"}, "o2": {"x0", "x2"}}

    def intersection(fibers: dict[str, set[str]]) -> list[str]:
        return sorted(x for x in xs if x in fibers[readout[x]])

    finite = {
        "readout_graph_projection": list(xs),
        "global_window_graph_intersection": intersection(global_window),
        "separable_graph_intersection": intersection(separable),
        "modulated_graph_intersection": intersection(modulated),
        "global_window_nonempty_fiber_shapes": len({frozenset(v) for v in global_window.values() if v}),
        "separable_nonempty_fiber_shapes": len({frozenset(v) for v in separable.values() if v}),
        "modulated_nonempty_fiber_shapes": len({frozenset(v) for v in modulated.values() if v}),
    }
    algebra = json.loads((HERE / "ALGEBRA_RESULT.json").read_text(encoding="utf-8"))
    checks.extend((algebra["jacobian_ranks"] == reconstructed_ranks, algebra["finite_controls"] == finite, algebra["graph_jacobian_nullity"] == 1))

    candidates = rows("INTERFACE_GATE_MATRIX.tsv")
    expected_rulings = {
        "C01": "OFFSHELL_LOCAL_FILTER_NOT_BOOTSTRAP",
        "C02": "READOUT_NOT_RETURN",
        "C03": "WORKING_ONE_WAY_SURVIVAL_FILTER_TYPE",
        "C04": "PROJECTOR_RESPONSE_CANNOT_BE_BOOTSTRAP_RETURN_ALONE",
        "C05": "CURVATURE_READOUT_NOT_RETURN_RELATION",
        "C06": "CONDITIONAL_MODEL_CANNOT_DEFINE_NATIVE_MEMBERSHIP",
        "C07": "TYPE_INCOMPLETE",
        "C08": "OPEN_MISSING_E_NATIVE_R_AND_A",
    }
    checks.extend((len(candidates) == 8, {row["candidate_id"] for row in candidates} == set(expected_rulings)))
    for row in candidates:
        checks.append(row["ruling"] == expected_rulings[row["candidate_id"]])
    checks.extend(
        (
            next(row for row in candidates if row["candidate_id"] == "C03")["X_dependence"] == "NO_BEFORE_SUBSTITUTION",
            next(row for row in candidates if row["candidate_id"] == "C04")["O_dependence"] == "NO",
            next(row for row in candidates if row["candidate_id"] == "C08")["proper_graph_intersection"] == "UNCOMPUTABLE",
        )
    )

    hierarchy = rows("ADMISSIBILITY_HIERARCHY.tsv")
    checks.extend((len(hierarchy) == 6, [row["level"] for row in hierarchy] == [f"L{i}" for i in range(6)]))
    checks.extend(
        (
            hierarchy[1]["name"] == "GLOBAL_SURVIVAL_WINDOW",
            hierarchy[2]["name"] == "SEPARABLE_MUTUAL_FILTER",
            hierarchy[3]["name"] == "FAMILY_TUNING",
            "F_O1_not_equal_F_O2" in hierarchy[3]["formal_object"],
            hierarchy[5]["name"] == "COMPLETE_ON_SHELL_CLOSURE",
        )
    )

    missing = rows("MISSING_INPUT_LEDGER.tsv")
    expected_status = {
        "M01": "DERIVED_CONDITIONAL_BOUNDED",
        "M02": "DERIVED_TYPED_NOT_SELECTED",
        "M03": "OPEN",
        "M04": "PARTIAL",
        "M05": "OPEN",
        "M06": "OPEN",
        "M07": "PARTIAL_CONSTRAINT",
        "M08": "OPEN_REQUIRED",
        "M09": "OPEN",
    }
    checks.extend((len(missing) == 9, {row["slot"]: row["status"] for row in missing} == expected_status))

    manifests = rows("SOURCE_MANIFEST.tsv")
    checks.extend((len(manifests) == 21, len({row["path"] for row in manifests}) == 21))
    for row in manifests:
        current = (ROOT / row["path"]).read_bytes()
        checks.extend((hashlib.sha256(current).hexdigest() == row["frozen_sha256"], row["unchanged_at_freeze"] == "YES"))

    anchors = rows("SOURCE_ANCHOR_LEDGER.tsv")
    checks.extend((len(anchors) == 12, len({row["anchor_id"] for row in anchors}) == 12))
    for row in anchors:
        checks.append(row["exact_anchor"] in (ROOT / row["path"]).read_text(encoding="utf-8"))

    external = json.loads(
        (ROOT / "udt_projector_deformation_neighborhood_review_2026-08-01/EXTERNAL_REVIEW_RESULT.json").read_text(encoding="utf-8")
    )
    checks.extend(
        (
            external["status"] == "PASS",
            external["mandatory_repairs"] == 0,
            external["target_manifest_sha256_after"]
            == "58dd9b3f272119db42757d5c66f00efd1ac26b6e2288bf92a479e547fe2bfeab",
        )
    )

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    checks.extend(
        (
            result["status"] == "PASS",
            result["candidate_count"] == 8,
            result["passing_complete_intersections"] == 0,
            result["hierarchy_levels"] == 6,
            result["missing_slots"] == 9,
            result["density_window_ruling"] == "WORKING_ONE_WAY_SURVIVAL_FILTER_TYPE_NOT_TWO_WAY_TUNING_BY_ITSELF",
        )
    )
    if not all(checks):
        failed = [index for index, passed in enumerate(checks, start=1) if not passed]
        raise AssertionError(f"independent checks failed: {failed}")
    output = {
        "schema": "udt.bootstrap_projector_admissibility_interface.independent.v1",
        "status": "PASS",
        "implementation": "stdlib_Fraction_and_finite_relations_no_production_import",
        "check_count": len(checks),
        "candidate_count": len(candidates),
        "source_count": len(manifests),
        "anchor_count": len(anchors),
        "reconstructed_ranks": reconstructed_ranks,
        "reconstructed_finite_controls": finite,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

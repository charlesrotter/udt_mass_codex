#!/usr/bin/env python3
"""Independent stdlib reconstruction; never imports the production derivation."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def det2(m: list[list[int]]) -> int:
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def rank(matrix: list[list[F]]) -> int:
    a = [list(row) for row in matrix]
    if not a:
        return 0
    nr, nc, pivot_row = len(a), len(a[0]), 0
    for col in range(nc):
        pivot = next((r for r in range(pivot_row, nr) if a[r][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [value / scale for value in a[pivot_row]]
        for r in range(nr):
            if r != pivot_row and a[r][col]:
                factor = a[r][col]
                a[r] = [a[r][c] - factor * a[pivot_row][c] for c in range(nc)]
        pivot_row += 1
        if pivot_row == nr:
            break
    return pivot_row


def canonical_row_space(matrix: list[list[F]]) -> tuple[tuple[F, ...], ...]:
    a = [list(row) for row in matrix]
    nr, nc, pivot_row = len(a), len(a[0]), 0
    for col in range(nc):
        pivot = next((r for r in range(pivot_row, nr) if a[r][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [value / scale for value in a[pivot_row]]
        for r in range(nr):
            if r != pivot_row and a[r][col]:
                factor = a[r][col]
                a[r] = [a[r][c] - factor * a[pivot_row][c] for c in range(nc)]
        pivot_row += 1
    return tuple(tuple(row) for row in a if any(row))


def main() -> int:
    checks: list[bool] = []
    source = rows("SOURCE_MANIFEST.tsv")
    checks.extend((len(source) == 36, len({row["path"] for row in source}) == 36))
    for row in source:
        checks.extend((hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["frozen_sha256"], row["unchanged_at_freeze"] == "YES"))

    anchors = rows("SOURCE_ANCHOR_LEDGER.tsv")
    checks.extend((len(anchors) == 16, len({row["anchor_id"] for row in anchors}) == 16))
    for row in anchors:
        checks.append(row["exact_anchor"] in (ROOT / row["path"]).read_text(encoding="utf-8"))

    registry_path = ROOT / "udt_global_metric_assembly_atlas_2026-07-22/TORUS_MONODROMY_REGISTRY.tsv"
    with registry_path.open(newline="", encoding="utf-8") as handle:
        registry = list(csv.DictReader(handle, delimiter="\t"))
    graphs: dict[str, tuple[tuple[F, ...], ...]] = {}
    fixed_dims: dict[str, int] = {}
    for row in registry:
        m = ast.literal_eval(row["matrix"])
        checks.append(abs(det2(m)) == 1)
        constraint = [[F(-m[0][0]), F(-m[0][1]), F(1), F(0)], [F(-m[1][0]), F(-m[1][1]), F(0), F(1)]]
        checks.append(rank(constraint) == 2)
        graphs[row["monodromy_id"]] = canonical_row_space(constraint)
        fixed_dims[row["monodromy_id"]] = 2 - rank([[F(m[0][0] - 1), F(m[0][1])], [F(m[1][0]), F(m[1][1] - 1)]])
    distinct = sum(graphs[a] != graphs[b] for a, b in combinations(graphs, 2))
    checks.extend((len(graphs) == 8, distinct == 28))
    expected_fixed = {"M_IDENTITY": 2, "M_MINUS_IDENTITY": 0, "M_ORDER4_ROTATION": 0, "M_ORDER6_ELLIPTIC": 0, "M_PARABOLIC": 1, "M_HYPERBOLIC": 0, "M_EXCHANGE": 1, "M_ORIENTATION_REVERSING_GLIDE": 1}
    checks.append(fixed_dims == expected_fixed)

    produced_graphs = rows("MONODROMY_LOCAL_FIBERS.tsv")
    checks.extend((len(produced_graphs) == 8, all(row["graph_dimension_in_R4"] == "2" and row["constraint_rank"] == "2" for row in produced_graphs)))
    checks.append({row["monodromy_id"]: int(row["conditional_fixed_parallel_dimension"]) for row in produced_graphs} == expected_fixed)

    jet = rows("JET_MATCHING_FIBERS.tsv")
    reconstructed_jets = [6 - max(0, k + 1) for k in (-1, 0, 1, 2)]
    checks.append([int(row["compatibility_fiber_dimension"]) for row in jet] == reconstructed_jets == [6, 5, 4, 3])

    caps = rows("CAP_LOCAL_JET_FIBERS.tsv")
    # Common denominator 2 cancels in -x/y for x=+-1/2, y=1/2.
    reconstructed_caps = sorted(str(F(-x, y)) for x, y in ((-1, 1), (1, 1)))
    checks.extend((sorted(row["f_cap"] for row in caps) == reconstructed_caps == ["-1", "1"], all(row["exceptional_stratum_c"] == "1" for row in caps)))

    gate = rows("GLOBAL_DATA_FIBER_GATE_MATRIX.tsv")
    by_id = {row["candidate_id"]: row for row in gate}
    checks.extend((len(gate) == 12, set(by_id) == {f"G{i:02d}" for i in range(1, 13)}))
    checks.extend((by_id["G07"]["ruling"] == "NATURAL_PARAMETRIC_LOCAL_JOIN_FIBER_SCHEMA", by_id["G08"]["ruling"] == "NATURAL_PARTIAL_CAP_JET_FIBER_CONDITIONAL_FAMILY", by_id["G09"]["ruling"] == "NATURAL_PARAMETRIC_JET_MATCHING_SCHEMA_PHYSICAL_SEAM_OPEN"))
    checks.extend((by_id["G07"]["same_configuration_reidentification"] == "SCHEMA_ONLY_NO_COMPLETE_METRIC_WITNESS", by_id["G09"]["same_configuration_reidentification"] == "SCHEMA_IF_FULL_TRANSITION_SUPPLIED"))
    checks.extend((by_id["G01"]["ruling"] == "FORWARD_LOCAL_READOUT_NOT_RETURN", by_id["G12"]["ruling"] == "NO_CURRENT_SELECTOR_OR_BOOTSTRAP_RETURN"))

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    checks.extend((result["status"] == "PASS", result["curvature_native_return_routes"] == 0, result["physical_completion_selectors"] == 0, result["parametric_fiber_schema_routes"] == ["G07", "G09"], result["conditional_completed_family_fiber_route"] == "G08"))
    if not all(checks):
        raise AssertionError(f"independent checks failed: {[i for i, ok in enumerate(checks, 1) if not ok]}")
    output = {"schema": "udt.completion_parameterized_local_fiber.independent.v1", "status": "PASS", "implementation": "stdlib_Fraction_no_production_import", "check_count": len(checks), "source_count": len(source), "anchor_count": len(anchors), "monodromy_graphs": len(graphs), "distinct_graph_pairs": distinct, "fixed_dimensions": expected_fixed, "jet_dimensions": reconstructed_jets, "cap_values": reconstructed_caps}
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

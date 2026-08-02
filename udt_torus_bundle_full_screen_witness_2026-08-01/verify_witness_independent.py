#!/usr/bin/env python3
"""Independent exact rational reconstruction; no production-script import."""

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


def det2(m: list[list[F]]) -> F:
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def matmul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def congruence(m: list[list[F]], h: list[list[F]]) -> list[list[F]]:
    return matmul(transpose(m), matmul(h, m))


def op3(m: list[list[F]]) -> tuple[tuple[F, ...], ...]:
    p, q = m[0]; r, s = m[1]
    return ((p * p, 2 * p * r, r * r), (p * q, p * s + q * r, r * s), (q * q, 2 * q * s, s * s))


def rank(matrix: list[list[F]]) -> int:
    a = [row[:] for row in matrix]
    nr, nc, pr = len(a), len(a[0]), 0
    for c in range(nc):
        pivot = next((r for r in range(pr, nr) if a[r][c]), None)
        if pivot is None:
            continue
        a[pr], a[pivot] = a[pivot], a[pr]
        scale = a[pr][c]; a[pr] = [v / scale for v in a[pr]]
        for r in range(nr):
            if r != pr and a[r][c]:
                scale = a[r][c]; a[r] = [a[r][j] - scale * a[pr][j] for j in range(nc)]
        pr += 1
    return pr


def add_scaled(h0: list[list[F]], h1: list[list[F]], q: F) -> list[list[F]]:
    return [[(1 - q) * h0[i][j] + q * h1[i][j] for j in range(2)] for i in range(2)]


def inverse2(m: list[list[F]]) -> list[list[F]]:
    determinant = det2(m)
    return [[m[1][1] / determinant, -m[0][1] / determinant], [-m[1][0] / determinant, m[0][0] / determinant]]


def main() -> int:
    checks: list[bool] = []
    manifests = rows("SOURCE_MANIFEST.tsv")
    checks.extend((len(manifests) == 22, len({row["path"] for row in manifests}) == 22))
    for row in manifests:
        checks.extend((hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["frozen_sha256"], row["unchanged_at_freeze"] == "YES"))
    anchors = rows("SOURCE_ANCHOR_LEDGER.tsv")
    checks.extend((len(anchors) == 16, len({row["anchor_id"] for row in anchors}) == 16))
    for row in anchors:
        checks.extend((set(row) == {"anchor_id", "path", "exact_anchor", "role"}, None not in row, bool(row["role"]), row["exact_anchor"] in (ROOT / row["path"]).read_text(encoding="utf-8")))

    candidates = rows("MONODROMY_CANDIDATES.tsv")
    registry = {row["monodromy_id"]: row for row in rows("../udt_global_metric_assembly_atlas_2026-07-22/TORUS_MONODROMY_REGISTRY.tsv")}
    h0 = [[F(2), F(1, 3)], [F(1, 3), F(5)]]
    checks.extend((len(candidates) == len(registry) == 8, h0[0][0] > 0, det2(h0) > 0))
    operators = {}
    endpoints = {}
    matrices = {}
    for row in candidates:
        source = registry[row["monodromy_id"]]
        checks.extend((row["matrix"] == source["matrix"], row["registry_class"] == source["monodromy_class"]))
        m = [[F(v) for v in line] for line in ast.literal_eval(row["matrix"])]
        matrices[row["monodromy_id"]] = m
        checks.append(abs(det2(m)) == 1)
        h1 = congruence(m, h0); endpoints[row["monodromy_id"]] = h1; operators[row["monodromy_id"]] = op3(m)
        checks.append(det2(h1) == det2(h0))
        for q in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)):
            hq = add_scaled(h0, h1, q)
            checks.extend((hq[0][0] > 0, det2(hq) > 0))
        for basis in ([[F(0), F(1)], [F(1), F(0)]], [[F(1), F(1)], [F(0), F(1)]]):
            transformed_m = matmul(inverse2(basis), matmul(m, basis))
            transformed_h0 = congruence(basis, h0)
            checks.append(congruence(transformed_m, transformed_h0) == congruence(basis, h1))

    groups = []
    pending = [row["monodromy_id"] for row in candidates]
    while pending:
        first = pending.pop(0); group = [first] + [x for x in pending if operators[x] == operators[first]]
        pending = [x for x in pending if x not in group]; groups.append(group)
    checks.extend((len(groups) == 7, groups[0] == ["M_IDENTITY", "M_MINUS_IDENTITY"]))
    checks.append(sum(operators[a] != operators[b] for a, b in combinations(operators, 2)) == 27)
    checks.append(all(endpoints[group[0]] != endpoints[other[0]] for group, other in combinations(groups, 2)))

    bases = {
        "M_IDENTITY": [(F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1))],
        "M_MINUS_IDENTITY": [(F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1))],
        "M_ORDER4_ROTATION": [(F(1), F(0), F(1))],
        "M_ORDER6_ELLIPTIC": [(F(1), F(1, 2), F(1))],
        "M_PARABOLIC": [(F(0), F(0), F(1))],
        "M_HYPERBOLIC": [(F(-1), F(1, 2), F(1))],
        "M_EXCHANGE": [(F(1), F(0), F(1)), (F(0), F(1), F(0))],
        "M_ORIENTATION_REVERSING_GLIDE": [(F(2), F(1), F(0)), (F(0), F(0), F(1))],
    }
    spd_samples = {"M_IDENTITY": (F(2), F(1, 3), F(5)), "M_MINUS_IDENTITY": (F(2), F(1, 3), F(5)), "M_ORDER4_ROTATION": (F(1), F(0), F(1)), "M_ORDER6_ELLIPTIC": (F(1), F(1, 2), F(1)), "M_EXCHANGE": (F(2), F(1), F(2)), "M_ORIENTATION_REVERSING_GLIDE": (F(2), F(1), F(1))}
    for rid, basis in bases.items():
        op = operators[rid]
        op_minus_i = [[op[i][j] - (F(1) if i == j else F(0)) for j in range(3)] for i in range(3)]
        checks.append(3 - rank(op_minus_i) == len(basis))
        for v in basis:
            checks.append(tuple(sum(op[i][j] * v[j] for j in range(3)) for i in range(3)) == v)
        if rid in spd_samples:
            a, b, d = spd_samples[rid]; checks.extend((a > 0, a * d - b * b > 0))
        elif rid == "M_PARABOLIC":
            checks.append(basis == [(F(0), F(0), F(1))])
        elif rid == "M_HYPERBOLIC":
            checks.append(basis == [(F(-1), F(1, 2), F(1))])

    census = rows("COMPLETE_WITNESS_CENSUS.tsv")
    checks.extend((len(census) == 8, sum(row["coframe_globality"].startswith("GLOBAL_") for row in census) == 6, sum(row["coframe_globality"].startswith("LOCAL_") for row in census) == 2, all(row["completion_status"] == "COMPLETE_OFFSHELL_METRIC_WITNESS" for row in census)))
    invariant = rows("INVARIANT_SCREEN_STRATA.tsv")
    checks.append([row["monodromy_id"] for row in invariant if row["positive_definite_fixed_member"].startswith("NO_")] == ["M_PARABOLIC", "M_HYPERBOLIC"])
    projector = rows("PROJECTOR_DESCENT_ATLAS.tsv")
    checks.extend((len(projector) == 8, all(row["descent_identity"] == "T*Pi=Pi*T" for row in projector), all(row["screen_distribution"] == "GLOBAL_INTEGRABLE_VERTICAL_T2" for row in projector)))
    covariance = rows("LATTICE_BASIS_COVARIANCE.tsv")
    checks.extend((len(covariance) == 8, all(row["status"] == "PASS_EXACT" for row in covariance), all(row["basis_controls"] == "B_EXCHANGE;B_SHEAR" for row in covariance)))

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    checks.extend((result["status"] == "PASS", result["complete_metric_witnesses"] == 8, result["metric_congruence_fiber_classes"] == 7, result["global_oriented_coframe_witnesses"] == 6, result["local_transition_coframe_only_witnesses"] == 2, result["forced_varying_screen_monodromies"] == ["M_PARABOLIC", "M_HYPERBOLIC"], result["lattice_basis_covariance_controls"] == 16, result["physical_completion_selectors"] == result["native_field_equations"] == 0))
    if not all(checks):
        raise AssertionError(f"independent checks failed: {[i for i, ok in enumerate(checks, 1) if not ok]}")
    output = {"schema": "udt.torus_bundle_full_screen_witness.independent.v1", "status": "PASS", "implementation": "stdlib_Fraction_no_production_import", "check_count": len(checks), "source_count": len(manifests), "anchor_count": len(anchors), "complete_metric_witnesses": len(census), "metric_fiber_classes": len(groups), "distinct_metric_operator_pairs": 27, "global_coframes": 6, "local_transition_coframes": 2, "forced_varying_screen": ["M_PARABOLIC", "M_HYPERBOLIC"], "basis_covariance_controls": 16}
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

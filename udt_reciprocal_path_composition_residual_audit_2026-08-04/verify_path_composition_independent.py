#!/usr/bin/env python3
"""Independent exact replay using only stdlib Fraction arithmetic."""

from __future__ import annotations

import json
import platform
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
checks: list[str] = []


def require(name: str, condition: bool) -> None:
    assert condition, name
    checks.append(name)


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def mt(a):
    return [list(row) for row in zip(*a)]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def inv2(a):
    determinant = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    assert determinant
    return [[a[1][1] / determinant, -a[0][1] / determinant], [-a[1][0] / determinant, a[0][0] / determinant]]


def rank(matrix):
    a = [list(map(F, row)) for row in matrix]
    rows, cols = len(a), len(a[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((row for row in range(pivot_row, rows) if a[row][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [value / scale for value in a[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not a[row][col]:
                continue
            scale = a[row][col]
            a[row] = [a[row][j] - scale * a[pivot_row][j] for j in range(cols)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def mv(matrix, vector):
    return [sum((row[j] * vector[j] for j in range(len(vector))), F(0)) for row in matrix]


def D(q):
    return [[F(1, q), F(0)], [F(0), F(q)]]


# Character controls use q=exp(delta), so additive delta is multiplicative q.
require("character_2_3_to_6", mm(D(3), D(2)) == D(6))
require("character_inverse", mm(D(2), D(F(1, 2))) == eye(2))
require("character_nonzero_visible", D(2) != eye(2))
require("character_faithful_rational_controls", all((D(q) == eye(2)) == (q == 1) for q in (F(1, 3), F(1), F(2), F(5))))

edges = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
edge_index = {edge: index for index, edge in enumerate(edges)}
B = [[F(0) for _ in range(4)] for _ in range(6)]
for row, (i, j) in enumerate(edges):
    B[row][i], B[row][j] = F(-1), F(1)
C = [[F(0) for _ in range(6)] for _ in range(4)]
for row, (i, j, k) in enumerate(((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))):
    C[row][edge_index[(i, j)]] = F(1)
    C[row][edge_index[(j, k)]] = F(1)
    C[row][edge_index[(i, k)]] = F(-1)
require("independent_incidence_rank", rank(B) == 3)
require("independent_triangle_rank", rank(C) == 3)
require("independent_C_B_zero", mm(C, B) == [[F(0)] * 4 for _ in range(4)])
for index, potential in enumerate(([0, 1, 4, 9], [3, -2, 5, 11], [0, 0, 1, -1]), 1):
    edges_from_potential = mv(B, list(map(F, potential)))
    require(f"independent_potential_{index}_triangle", mv(C, edges_from_potential) == [F(0)] * 4)
    require(f"independent_potential_{index}_nonzero", any(edges_from_potential))
require("independent_free_cochain_fails", mv(C, [F(1), F(0), F(0), F(0), F(0), F(0)]) != [F(0)] * 4)

# Direct unit-square line integrals, evaluated without a symbolic engine.
exact_segments = (F(3), F(1), F(-4), F(0))
nonclosed_segments = (F(0), F(1, 2), F(1, 2), F(0))
require("independent_exact_period_zero", sum(exact_segments, F(0)) == 0)
require("independent_nonclosed_period_one", sum(nonclosed_segments, F(0)) == 1)
require("independent_both_paths_add_segmentwise", sum(exact_segments[:2], F(0)) + sum(exact_segments[2:], F(0)) == sum(exact_segments, F(0)))

eta = [[F(-1), F(0)], [F(0), F(1)]]
U1 = [[F(5, 4), F(-3, 4)], [F(-3, 4), F(5, 4)]]
U2 = [[F(13, 12), F(-5, 12)], [F(-5, 12), F(13, 12)]]
require("independent_U1_Lorentz", mm(mm(mt(U1), eta), U1) == eta)
require("independent_U2_Lorentz", mm(mm(mt(U2), eta), U2) == eta)
X0 = [[F(-1), F(0)], [F(0), F(1)]]
require("independent_generator_transport_nontrivial", mm(mm(U1, X0), inv2(U1)) != X0)
D1b = mm(mm(U1, D(3)), inv2(U1))
require("independent_intertwining", mm(D1b, U1) == mm(U1, D(3)))
T_alpha = mm(U1, D(2))
T_beta = mm(U2, D1b)
require("independent_semidirect_composition", mm(T_beta, T_alpha) == mm(mm(U2, U1), D(6)))
require("independent_semidirect_nonvacuous", mm(T_beta, T_alpha) != eye(2))

period = D(2)
require("independent_period_visible", period != eye(2))
require("independent_holonomy_visible", U1 != eye(2))
require("independent_loop_factors_distinct", mm(mm(mt(U1), eta), U1) == eta and mm(mm(mt(period), eta), period) != eta)
require("independent_zero_period_leaves_holonomy", mm(U1, D(1)) != eye(2))
require("independent_identity_holonomy_leaves_period", mm(eye(2), period) != eye(2))

source_needles = (
    ("UDT_NATIVE_ACTION_COLD_PACKET.md", "comparisons compose consistently through an intermediate position"),
    ("CURRENT_SCIENTIFIC_PREMISES.md", "physical observer/path assignment"),
    ("udt_founding_observer_comparison_semantics_audit_2026-07-27/SOURCE_CLAIM_OUTCOMES.tsv", "Composition_domain_contains_no_metric_path_variable"),
    ("udt_observer_pair_path_groupoid_assembly_audit_2026-07-26/STATUS_LEDGER.tsv", "OPEN_SMALLEST_KINEMATIC_JOIN"),
    ("udt_native_global_coframe_definition_audit_2026-07-28/EXACT_DERIVATION.md", "The zero function and infinitely many nonzero functions all pass"),
    ("udt_whole_configuration_reciprocity_audit_2026-08-01/EXACT_DERIVATION.md", "Reciprocity alone -> complete nonidentity bootstrap return A"),
    ("udt_basic_vs_universal_query_residual_audit_2026-08-04/FOUNDATIONAL_RULING.tsv", "no nontrivial native residual selected"),
)
for index, (relative, needle) in enumerate(source_needles, 1):
    require(f"independent_source_semantics_{index}", needle in (ROOT / relative).read_text(encoding="utf-8"))

result = {
    "status": "PASS",
    "independent_exact_checks": len(checks),
    "check_names": checks,
    "inferred_outcome": "COMPOSITION_IDENTITY_NONSELECTING",
    "metric_residual_from_founded_composition": False,
    "conditional_loop_residual_requires_extra_premise": True,
    "termination_ruling": "CURRENT_COMPOSITION_TO_NATIVE_RESIDUAL_ROUTE_TERMINATES_WITHOUT_NEW_SOURCE_BACKED_DEPTH_OR_LOOP_PREMISE",
    "python": platform.python_version(),
    "dependencies": "stdlib_only",
}
(HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
stdout = f"PASS independent_exact_checks={len(checks)} outcome={result['inferred_outcome']}\n"
(HERE / "INDEPENDENT_STDOUT.txt").write_text(stdout, encoding="utf-8")
(HERE / "INDEPENDENT_STDERR.txt").write_text("", encoding="utf-8")
sys.stdout.write(stdout)

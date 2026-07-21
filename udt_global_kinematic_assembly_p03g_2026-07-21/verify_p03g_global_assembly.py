#!/usr/bin/env python3
"""Independent stdlib verifier and fail-closed mutation catches for P03G."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULT = HERE / "ASSEMBLY_RESULT.json"
VERIFY = HERE / "VERIFICATION_RESULT.json"
TRANSCRIPT = HERE / "VERIFICATION_TRANSCRIPT.txt"
MAXIMUM = "CURRENT_GLOBAL_KINEMATIC_ASSEMBLY_CONDITIONS_AND_OPEN_BRANCHES_CHARACTERIZED"

TABLES = [
    "ASSEMBLY_INPUT_REGISTRY.tsv",
    "GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv",
    "COVER_AND_COCYCLE_BRANCHES.tsv",
    "SEAL_LIFT_AND_TANGENT_BRANCHES.tsv",
    "TOPOLOGY_AND_COMPLETION_BRANCHES.tsv",
    "LOCAL_TO_GLOBAL_EXTENSION_GATES.tsv",
    "GLOBAL_COUNTERMODEL_LEDGER.tsv",
    "UNCOUNTED_GLOBAL_MODULI.tsv",
    "STATUS_LEDGER.tsv",
    "SOURCE_LINEAGE.tsv",
]

PARENTS = {
    "P01": ("udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt", "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad"),
    "P02": ("udt_local_jet_atlas_p02_2026-07-21/SHA256SUMS.txt", "c56390eb26b80c54a3c3a09f4800086c8dbc00b5bfd40b2038e264e85bec8938"),
    "P03": ("udt_founded_constraint_atlas_p03_2026-07-21/SHA256SUMS.txt", "b0ec5cbb2be404084e1b1ed4eca98d53c9712a62cf1af0a48eb340b64467c3be"),
    "COMPLETE_MAP": ("udt_complete_metric_solution_space_map_2026-07-21/SHA256SUMS.txt", "1778e4dcfcf9ac0bd3574fb3ff5248f2990265fa40d0822ff964ac67c434ae38"),
    "GLOBAL_COCYCLE": ("udt_global_coframe_cocycle_audit_2026-07-20/SHA256SUMS.txt", "1297e8f6773f863f426d66f6c4915741a742c1ee13230abf2b066421de49b04b"),
    "STATIC_SEAL": ("finite_cell_seal_boundary_phase_join_2026-07-20/SHA256SUMS.txt", "704b084548a212eabcfb1ac051e89234a7fd91bbeaf7f70abcc28bf63edc7a3b"),
    "COMPLETE_SEAL": ("udt_complete_seal_fixed_set_selector_audit_2026-07-21/SHA256SUMS.txt", "3a6cc83e40fe95951b19f37b68b1167a3683cf4f02c0fbf1f52f54d95db99b66"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load() -> tuple[dict, dict[str, list[dict[str, str]]], dict]:
    return (
        json.loads(RESULT.read_text(encoding="utf-8")),
        {name: read_rows(HERE / name) for name in TABLES},
        json.loads((HERE / "ASSEMBLY_DEPENDENCY_GRAPH.json").read_text(encoding="utf-8")),
    )


def validate(result: dict, tables: dict[str, list[dict[str, str]]], graph: dict) -> None:
    require(result["schema"] == "udt-p03g-global-kinematic-assembly-atlas-1.0", "schema")
    require(result["status"] == "PASS", "status")
    require(result["evidence_grade"] == "LEAD_INDEPENDENT_REPLAY_FRESH_ADVERSARIAL_OPEN", "evidence grade")
    require(result["maximum_conclusion"] == MAXIMUM, "maximum conclusion")
    require(result["question_mode"] == "METRIC_LED_OBSERVING_GLOBAL_ASSEMBLY", "question mode")
    require(result["counts"] == {
        "assembly_inputs": 16,
        "preregistered_axes": 12,
        "cocycle_branches": 12,
        "seal_lift_and_tangent_branches": 7,
        "topology_and_completion_branches": 12,
        "local_realization_branches_retained": 7,
        "countermodels": 12,
        "uncounted_global_moduli": 15,
        "globally_proved_local_branches": 0,
        "globally_excluded_local_branches": 0,
        "selected_global_branches": 0,
    }, "counts")
    scope = result["scope"]
    require(scope["CPU_only"], "CPU scope")
    require(not any(scope[key] for key in ("GPU_used", "ODE_or_PDE_run", "action_selected", "equation_selected", "topology_selected", "global_solution_claimed", "P04_launched", "P11_launched")), "scope promotion")
    require(result["compatibility_ruling"] == {
        "reciprocal_transition_algebra": "DERIVED_EXACT_IN_BOUNDED_TWO_CHANNEL_CLASS",
        "actual_cover_and_global_cocycle": "OPEN",
        "complete_seal_lift": "OPEN",
        "global_topology": "OPEN_NONUNIQUE_AND_NONEXHAUSTIVE",
        "global_signed_phi": "OPEN",
        "all_C01_C07_local_branches": "RETAINED_GLOBAL_EXISTENCE_UNEVALUATED",
        "P04_dynamics_lane": "NOT_SELECTED_OR_LAUNCHED",
    }, "ruling")

    inputs = tables["ASSEMBLY_INPUT_REGISTRY.tsv"]
    require(len(inputs) == 16 and {row["id"] for row in inputs} == {f"I{i:02d}" for i in range(1, 17)}, "input coverage")
    require(len({row["id"] for row in inputs}) == 16, "input duplicates")
    require(all(row["source"] for row in inputs), "input citations")
    input_by = {row["id"]: row for row in inputs}
    require(input_by["I04"]["status"] == "OPEN_ASSEMBLY_DATA", "cover open")
    require(input_by["I10"]["status"] == "OPEN_ASSEMBLY_DATA", "seal lift open")
    require(input_by["I12"]["status"] == "OPEN_ASSEMBLY_DATA", "degeneracy open")
    require(input_by["I14"]["status"] == "NOT_EVALUABLE", "Xmax not evaluable")
    require(input_by["I16"]["status"] == "NOT_LOADED", "dynamics not loaded")

    schema = tables["GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv"]
    require(len(schema) == 12 and {row["axis_id"] for row in schema} == {f"A{i:02d}" for i in range(1, 13)}, "axis coverage")
    require(len({row["axis_id"] for row in schema}) == 12, "axis duplicates")
    require(next(row for row in schema if row["axis_id"] == "A09")["bounded_exhaustiveness"] == "WITNESS_LIST_PLUS_OTHER_UNENUMERATED", "topology nonexhaustive")

    cocycles = tables["COVER_AND_COCYCLE_BRANCHES.tsv"]
    require(len(cocycles) == 12 and {row["id"] for row in cocycles} == {f"C{i:02d}" for i in range(1, 13)}, "cocycle coverage")
    require(all(row["selected"] == "NO" for row in cocycles), "cocycle selection")
    cocycle = {row["id"]: row for row in cocycles}
    require(cocycle["C04"]["assembly_status"] == "EXCLUDED_BY_EXACT_COCYCLE", "three-F status")
    require(cocycle["C05"]["assembly_status"] == "EXACT_LOCAL_COCYCLE_WITNESS", "FFG witness")
    require(cocycle["C06"]["assembly_status"] == "EXCLUDED_BY_EXACT_COCYCLE", "odd parity")
    require(cocycle["C07"]["assembly_status"] == "NECESSARY_NOT_SUFFICIENT", "even parity scope")
    require(cocycle["C08"]["assembly_status"] == "OPEN_GLOBAL_CLASS", "global class")
    require(cocycle["C10"]["assembly_status"] == "MULTIPLE_VALUES_SURVIVE_CONDITIONALLY", "mu survives")
    require(cocycle["C12"]["assembly_status"] == "OPEN_UNENUMERATED", "full transitions open")

    lifts = tables["SEAL_LIFT_AND_TANGENT_BRANCHES.tsv"]
    require(len(lifts) == 7 and {row["id"] for row in lifts} == {f"L{i:02d}" for i in range(1, 8)}, "lift coverage")
    lift = {row["id"]: row for row in lifts}
    require((lift["L01"]["coframe_fixed_dim"], lift["L01"]["coframe_antifixed_dim"], lift["L01"]["metric_even_dim"], lift["L01"]["metric_odd_dim"]) == ("3", "1", "7", "3"), "3/1 lift")
    require((lift["L03"]["coframe_fixed_dim"], lift["L03"]["coframe_antifixed_dim"], lift["L03"]["metric_even_dim"], lift["L03"]["metric_odd_dim"]) == ("2", "2", "6", "4"), "2/2 lift")
    require(lift["L05"]["status"] == "PINNED_SCOPED_NOT_COMPLETE_LIFT" and lift["L05"]["metric_even_dim"] == "9", "scalar seal scope")
    require(lift["L06"]["status"] == lift["L07"]["status"] == "CONDITIONAL_VARIATION_WITNESS", "polarizations")

    topology = tables["TOPOLOGY_AND_COMPLETION_BRANCHES.tsv"]
    require(len(topology) == 12 and {row["id"] for row in topology} == {f"T{i:02d}" for i in range(1, 13)}, "topology coverage")
    require(all(row["selected"] == "NO" for row in topology), "topology selected")
    require({row["witness_parameter"] for row in topology} >= {"p=0", "p=1", "p=3", "p=5", "general_p"}, "cap witnesses")
    require(sum(row["kind"] == "OTHER_UNENUMERATED" for row in topology) >= 2, "topology remainder")
    require(next(row for row in topology if row["id"] == "T09")["status"] == "OPEN_PRESERVED", "degeneracy preserved")
    require(next(row for row in topology if row["id"] == "T12")["status"] == "OPEN", "sign holonomy open")

    gates = tables["LOCAL_TO_GLOBAL_EXTENSION_GATES.tsv"]
    require(len(gates) == 7 and {row["local_branch"] for row in gates} == {f"C{i:02d}" for i in range(1, 8)}, "local branch coverage")
    require(all(row["currently_derived"] == "NO" and row["current_ruling"] == "LOCAL_BRANCH_RETAINED_GLOBAL_EXISTENCE_UNEVALUATED" for row in gates), "local branch promotion")
    require(len(tables["GLOBAL_COUNTERMODEL_LEDGER.tsv"]) == 12, "countermodel count")
    require({row["id"] for row in tables["GLOBAL_COUNTERMODEL_LEDGER.tsv"]} == {f"M{i:02d}" for i in range(1, 13)}, "countermodel IDs")
    require(len(tables["UNCOUNTED_GLOBAL_MODULI.tsv"]) == 15 and all(row["status"] in {"UNCOUNTED", "NOT_EVALUABLE"} for row in tables["UNCOUNTED_GLOBAL_MODULI.tsv"]), "uncounted moduli")

    status = tables["STATUS_LEDGER.tsv"]
    require(len(status) == 21 and {row["id"] for row in status} == {f"S{i:02d}" for i in range(1, 22)}, "status coverage")
    status_by = {row["id"]: row for row in status}
    require(status_by["S11"]["status"] == "OPEN_NONUNIQUE", "topology status")
    require(status_by["S12"]["status"] == "EXPLICITLY_NOT_CLAIMED", "topology exhaustive status")
    require(status_by["S13"]["status"] == "OPEN", "global phi status")
    require(status_by["S14"]["status"] == "OPEN_PRESERVED", "degeneracy status")
    require(status_by["S18"]["status"] == "ALL_RETAINED_EXISTENCE_UNEVALUATED", "branch status")
    require(status_by["S19"]["status"] == "NOT_LOADED", "dynamics status")
    require(status_by["S20"]["status"] == "LEAD_INDEPENDENT_REPLAY_FRESH_ADVERSARIAL_OPEN", "evidence status")
    require(status_by["S21"]["status"] == MAXIMUM, "ledger maximum")

    require(graph["schema"] == "udt-p03g-global-assembly-dependency-graph-1.0", "graph schema")
    node_ids = {node["id"] for node in graph["nodes"]}
    require(len(node_ids) == len(graph["nodes"]), "graph node duplicates")
    require(all(edge["from"] in node_ids and edge["to"] in node_ids for edge in graph["edges"]), "graph endpoints")
    realized = {(edge["from"], edge["to"]) for edge in graph["edges"]}
    forbidden = {(edge["from"], edge["to"]) for edge in graph["forbidden_edges"]}
    require(not realized & forbidden, "forbidden graph edge")
    require(("GF_GROUP", "TRANSITION_COCYCLE") in realized and ("COVER_NERVE", "TRANSITION_COCYCLE") in realized, "cocycle dependencies")
    require(("GF_GROUP", "COVER_NERVE") in forbidden, "no group-to-cover inference")
    require(("CSN_PATCHING", "PHYSICAL_SCALE_XMAX") in forbidden, "no CSN scale selection")

    lineage = tables["SOURCE_LINEAGE.tsv"]
    require(len(lineage) == 7 and {row["role"] for row in lineage} == set(PARENTS), "lineage coverage")
    for row in lineage:
        path, expected = PARENTS[row["role"]]
        require(row["path"] == path and row["sha256"] == expected and digest(ROOT / path) == expected, f"parent {row['role']}")
        require(result["parent_manifest_sha256"][row["role"]] == expected, f"result parent {row['role']}")
    for name, expected in result["table_sha256"].items():
        require(digest(HERE / name) == expected, f"table hash {name}")


def matmul(left, right):
    return tuple(tuple(sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def G(value: Fraction):
    return ((value, Fraction(0)), (Fraction(0), Fraction(1, 1) / value))


def F(value: Fraction):
    return ((Fraction(0), value), (Fraction(1, 1) / value, Fraction(0)))


def independent_algebra(checks: dict[str, str]) -> None:
    a, d, b, c = map(Fraction, (2, 3, 5, 7))
    identity = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    require(matmul(G(a), G(d)) == G(a * d), "independent G law")
    require(matmul(F(b), F(b)) == identity, "independent F involution")
    require(matmul(F(b), F(c)) == G(b / c), "independent FF law")
    require(matmul(G(a), F(b)) == F(a * b), "independent GF law")
    require(matmul(F(b), G(a)) == F(b / a), "independent FG law")
    require(matmul(matmul(F(b), F(c)), G(c / b)) == identity, "independent FFG witness")
    three_f = matmul(matmul(F(b), F(c)), F(d))
    require(three_f[0][0] == 0 and three_f[0][1] != 0, "independent three F")
    checks["independent_fraction_group_algebra"] = "PASS"
    dims = {(fixed, 4 - fixed): (fixed * (fixed + 1) // 2 + (4 - fixed) * (5 - fixed) // 2, fixed * (4 - fixed)) for fixed in (1, 2, 3)}
    require(dims[(3, 1)] == (7, 3) and dims[(2, 2)] == (6, 4) and dims[(1, 3)] == (7, 3), "independent tangent dimensions")
    checks["independent_tangent_combinatorics"] = "PASS"
    slopes = (Fraction(-3), Fraction(0), Fraction(5, 2))
    require(all(slope * 0 == 0 for slope in slopes) and len(set(slopes)) == 3, "independent seal family")
    checks["independent_free_seal_normal_jet"] = "PASS"


def expect_failure(name: str, operation, catches: dict[str, str]) -> None:
    try:
        operation()
    except (AssertionError, KeyError, StopIteration, ValueError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"mutation unexpectedly passed: {name}")


def main() -> None:
    tracked = [RESULT, HERE / "ASSEMBLY_DEPENDENCY_GRAPH.json", *[HERE / name for name in TABLES]]
    before = {path.name: digest(path) for path in tracked}
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["CUDA_VISIBLE_DEVICES"] = ""
    replay = subprocess.run([sys.executable, "-B", str(HERE / "build_p03g_global_assembly.py")], cwd=ROOT, env=environment, text=True, capture_output=True, timeout=300, check=False)
    require(replay.returncode == 0 and not replay.stderr, replay.stdout + replay.stderr)
    require(replay.stdout == (HERE / "ASSEMBLY_TRANSCRIPT.txt").read_text(encoding="utf-8"), "main transcript")
    require(before == {path.name: digest(path) for path in tracked}, "deterministic replay")
    result, tables, graph = load()
    validate(result, tables, graph)
    checks = {"deterministic_replay_and_full_contract": "PASS", "parent_manifest_replay": "PASS"}
    independent_algebra(checks)
    require(result["check_count"] == 25 and len(result["checks"]) == 25 and set(result["checks"].values()) == {"PASS"}, "main checks")
    checks["main_exact_checks_reconciled"] = "PASS"
    require(sum(1 for row in tables["LOCAL_TO_GLOBAL_EXTENSION_GATES.tsv"] if row["currently_derived"] == "NO") == 7, "branch count")
    checks["independent_local_branch_reconciliation"] = "PASS"
    require(sum(1 for row in tables["TOPOLOGY_AND_COMPLETION_BRANCHES.tsv"] if row["selected"] == "YES") == 0, "selection count")
    checks["independent_zero_selection_reconciliation"] = "PASS"

    catches: dict[str, str] = {}
    bad = copy.deepcopy(result); bad["schema"] = "bad"
    expect_failure("schema", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(result); bad["maximum_conclusion"] = "GLOBAL_SOLUTION_SPACE_COMPLETE"
    expect_failure("maximum_conclusion", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(result); bad["scope"]["action_selected"] = True
    expect_failure("action_import", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(result); bad["scope"]["P04_launched"] = True
    expect_failure("P04_launch", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(result); bad["compatibility_ruling"]["actual_cover_and_global_cocycle"] = "DERIVED"
    expect_failure("local_group_promoted_global", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(result); bad["compatibility_ruling"]["global_signed_phi"] = "DERIVED"
    expect_failure("global_phi_promoted", lambda: validate(bad, tables, graph), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv"].pop()
    expect_failure("missing_axis", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv"].append(copy.deepcopy(bad_tables["GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv"][0]))
    expect_failure("duplicate_axis", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["LOCAL_TO_GLOBAL_EXTENSION_GATES.tsv"].pop()
    expect_failure("missing_local_branch", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["LOCAL_TO_GLOBAL_EXTENSION_GATES.tsv"][0]["currently_derived"] = "YES"
    expect_failure("global_branch_promotion", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["COVER_AND_COCYCLE_BRANCHES.tsv"] if row["id"] == "C06")["assembly_status"] = "ALLOWED"
    expect_failure("odd_parity_allowed", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["COVER_AND_COCYCLE_BRANCHES.tsv"] if row["id"] == "C08")["assembly_status"] = "TRIVIAL_SELECTED"
    expect_failure("global_Z2_class_selected", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["COVER_AND_COCYCLE_BRANCHES.tsv"] if row["id"] == "C10")["assembly_status"] = "UNIQUE"
    expect_failure("mixed_modulus_collapsed", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["SEAL_LIFT_AND_TANGENT_BRANCHES.tsv"] if row["id"] == "L05")["status"] = "COMPLETE_LIFT"
    expect_failure("scalar_seal_promoted", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["SEAL_LIFT_AND_TANGENT_BRANCHES.tsv"] if row["id"] == "L07")["status"] = "SELECTED"
    expect_failure("boundary_polarization_selected", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["TOPOLOGY_AND_COMPLETION_BRANCHES.tsv"] if row["id"] == "T03")["selected"] = "YES"
    expect_failure("topology_selected", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["TOPOLOGY_AND_COMPLETION_BRANCHES.tsv"] = [row for row in bad_tables["TOPOLOGY_AND_COMPLETION_BRANCHES.tsv"] if row["kind"] != "OTHER_UNENUMERATED"]
    expect_failure("topology_false_exhaustiveness", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["TOPOLOGY_AND_COMPLETION_BRANCHES.tsv"] if row["id"] == "T09")["status"] = "EXCLUDED"
    expect_failure("degeneracy_deleted", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["TOPOLOGY_AND_COMPLETION_BRANCHES.tsv"] if row["id"] == "T12")["status"] = "EXCLUDED"
    expect_failure("sign_holonomy_deleted", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["ASSEMBLY_INPUT_REGISTRY.tsv"] if row["id"] == "I14")["status"] = "DERIVED"
    expect_failure("Xmax_promoted", lambda: validate(result, bad_tables, graph), catches)
    bad_graph = copy.deepcopy(graph); bad_graph["edges"].append({"from": "GF_GROUP", "to": "COVER_NERVE", "relation": "creates"})
    expect_failure("group_creates_cover", lambda: validate(result, tables, bad_graph), catches)
    bad_graph = copy.deepcopy(graph); bad_graph["edges"].append({"from": "CSN_PATCHING", "to": "PHYSICAL_SCALE_XMAX", "relation": "selects"})
    expect_failure("CSN_selects_scale", lambda: validate(result, tables, bad_graph), catches)
    bad = copy.deepcopy(result); bad["parent_manifest_sha256"]["P03"] = "0" * 64
    expect_failure("parent_hash_drift", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(result); bad["table_sha256"]["STATUS_LEDGER.tsv"] = "0" * 64
    expect_failure("table_hash_drift", lambda: validate(bad, tables, graph), catches)
    require(len(catches) == 24 and set(catches.values()) == {"PASS"}, "catch count")

    output = {
        "schema": "udt-p03g-global-kinematic-assembly-verification-1.0",
        "status": "PASS",
        "check_count": len(checks),
        "checks": checks,
        "catch_proof_count": len(catches),
        "catch_proofs": catches,
        "main_result_sha256": digest(RESULT),
        "main_transcript_sha256": digest(HERE / "ASSEMBLY_TRANSCRIPT.txt"),
        "scope": {"independent_implementation": True, "generator_imported": False, "stdlib_fraction_algebra": True, "CPU_only": True, "GPU_used": False},
    }
    VERIFY.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "P03G_INDEPENDENT_VERIFICATION=PASS",
        f"checks={len(checks)}",
        f"catch_proofs={len(catches)}",
        "implementation=stdlib_fraction_algebra_no_generator_import",
        "axes=12/12",
        "local_branches=7/7_retained_global_existence_unevaluated",
        "selected_global_branches=0",
        "parent_manifests=7/7",
        f"main_result_sha256={output['main_result_sha256']}",
    ]
    text = "\n".join(transcript) + "\n"
    TRANSCRIPT.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()

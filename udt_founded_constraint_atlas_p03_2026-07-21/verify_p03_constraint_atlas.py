#!/usr/bin/env python3
"""Independent verifier and exercised corruption catches for P03."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
P02 = ROOT / "udt_local_jet_atlas_p02_2026-07-21"
MAP = ROOT / "udt_complete_metric_solution_space_map_2026-07-21"
RESULT = HERE / "ATLAS_RESULT.json"
VERIFY = HERE / "VERIFICATION_RESULT.json"
TRANSCRIPT = HERE / "VERIFICATION_TRANSCRIPT.txt"
BASE = "df49e148dcf38d2ee1edeca0f1c0a67e7b0f27e2"

TABLES = [
    "FOUNDATION_INPUT_REGISTRY.tsv",
    "REALIZATION_BRANCHES.tsv",
    "CONSTRAINT_EFFECT_LEDGER.tsv",
    "SURVIVING_STRATA.tsv",
    "INCONSISTENT_COMBINATIONS.tsv",
    "UNCONSTRAINED_DIMENSIONS.tsv",
    "COUNTERMODEL_LEDGER.tsv",
]

P02_TABLES = {
    "METRIC_INERTIA": "ZERO_JET_INERTIA_STRATA.tsv",
    "SPLIT_INERTIA": "SPLIT_ZERO_JET_STRATA.tsv",
    "DPHI": "DPHI_FIRST_JET_STRATA.tsv",
    "SPLIT_FIRST_JET": "SPLIT_FIRST_JET_STRATA.tsv",
    "CURVATURE_RANK": "CURVATURE_OPERATOR_RANK_STRATA.tsv",
    "RICCI_RANK": "RICCI_ENDOMORPHISM_RANK_STRATA.tsv",
    "PETROV": "PETROV_STRATA.tsv",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load() -> tuple[dict, dict[str, list[dict[str, str]]], dict]:
    return (
        json.loads(RESULT.read_text(encoding="utf-8")),
        {name: rows(HERE / name) for name in TABLES},
        json.loads((HERE / "CONSTRAINT_DEPENDENCY_GRAPH.json").read_text(encoding="utf-8")),
    )


def validate(data: dict, tables: dict[str, list[dict[str, str]]], graph: dict) -> None:
    require(data["schema"] == "udt-p03-founded-constraint-atlas-1.0", "schema")
    require(data["status"] == "PASS", "status")
    require(
        data["maximum_conclusion"]
        == "CURRENT_FOUNDATION_CONSTRAINED_CONFIGURATION_SPACE_CHARACTERIZED",
        "maximum conclusion",
    )
    require(data["question_mode"] == "METRIC_LED_OBSERVING_CONSTRAINT_EFFECTS", "question mode")
    require(data["counts"] == {
        "foundation_input_rows": 36,
        "realization_branches": 7,
        "constraint_effects": 24,
        "P02_discrete_strata_accounted": 89,
        "inconsistent_combinations": 14,
        "dimension_rows": 13,
        "countermodels": 12,
        "split_first_jet_invariant_quotient_classes": 6,
    }, "counts")
    require(data["dimension_contract"] == {
        "internal_positive_pair_before_reciprocity": 2,
        "internal_reciprocal_character": 1,
        "conditional_4D_curvature_before_CSN": 20,
        "conditional_4D_curvature_after_local_CSN": 10,
        "conditional_generic_curvature_after_Lorentz_frame_quotient": 4,
        "conditional_split_first_jet_before_CSN": 8,
        "conditional_split_first_jet_after_CSN": 6,
        "static_seal_phi_value": 0,
        "static_seal_free_normal_phi_jet": 1,
    }, "dimension contract")
    require(data["check_count"] == 20, "check count")
    require(len(data["checks"]) == 20 and set(data["checks"].values()) == {"PASS"}, "checks")
    scope = data["scope"]
    require(scope["CPU_only"] and not any(scope[key] for key in (
        "GPU_used", "ODE_or_PDE_run", "action_selected", "equation_of_motion_selected",
        "comparison_or_empirical_target_loaded", "merit_filter_used", "P04_launched",
    )), "scope")

    inputs = tables["FOUNDATION_INPUT_REGISTRY.tsv"]
    expected_input_ids = {f"P{number:02d}" for number in range(1, 37)}
    require(len(inputs) == 36 and {row["id"] for row in inputs} == expected_input_ids, "input coverage")
    require(len({row["id"] for row in inputs}) == 36, "input duplicate")
    require(all(row["source"] and row["premise_stamp"] for row in inputs), "input citations")
    input_by_id = {row["id"]: row for row in inputs}
    require(input_by_id["P08"]["p03_treatment"] == "LOCAL_EQUIVALENCE", "CSN treatment")
    require(input_by_id["P10"]["p03_treatment"] == "OPEN_REALIZATION", "soldering open")
    require(input_by_id["P19"]["p03_treatment"] == "EXCLUDED_DYNAMICS", "dynamics excluded")
    require(input_by_id["P35"]["p03_treatment"] == "SEMANTIC_SEPARATION", "semantics")

    branches = tables["REALIZATION_BRANCHES.tsv"]
    require(len(branches) == 7 and {row["id"] for row in branches} == {f"B0{i}" for i in range(7)}, "branches")
    branch = {row["id"]: row for row in branches}
    require(branch["B00"]["metric_status"] == "NO_SPACETIME_SOLDERING_SUPPLIED", "B00 separation")
    require(branch["B02"]["metric_status"] == "Z09_WITHIN_SUPPLIED_CONVENTION", "B02 conditional")
    require(branch["B03"]["metric_status"] == "S27_WITHIN_SUPPLIED_SPLIT_CONVENTION", "B03 conditional")
    require("normal derivative" in branch["B04"]["open_data"], "seal normal free")

    effects = tables["CONSTRAINT_EFFECT_LEDGER.tsv"]
    require(len(effects) == 24 and {row["id"] for row in effects} == {f"E{i:02d}" for i in range(1, 25)}, "effects")
    allowed_effects = {"RESTRICT", "IDENTIFY", "PRESERVE", "NO_LOCAL_EFFECT", "CONDITIONAL_ONLY", "SEMANTIC_SEPARATION"}
    require({row["effect"] for row in effects} <= allowed_effects, "effect vocabulary")
    for row in effects:
        ids = row["premise_ids"].split(";")
        require(ids and all(item in expected_input_ids for item in ids), "effect citation")
    effect = {row["id"]: row for row in effects}
    require(effect["E02"]["domain"] == "B00" and effect["E02"]["effect"] == "RESTRICT", "internal relation")
    require(effect["E15"]["effect"] == "NO_LOCAL_EFFECT", "finite-cell locality")
    require(effect["E22"]["effect"] == "NO_LOCAL_EFFECT", "bootstrap locality")
    require(effect["E18"]["effect"] == "PRESERVE" and "free" in effect["E18"]["exact_relation_or_status"], "normal derivative")
    require(effect["E24"]["domain"] == "NOT_LOADED_IN_P03", "dynamics isolation")

    survival = tables["SURVIVING_STRATA.tsv"]
    require(len(survival) == 89, "survival total")
    require(len({(row["atlas"], row["source_id"]) for row in survival}) == 89, "survival uniqueness")
    observed_counts = Counter(row["atlas"] for row in survival)
    require(observed_counts == Counter({
        "METRIC_INERTIA": 15, "SPLIT_INERTIA": 36, "DPHI": 8,
        "SPLIT_FIRST_JET": 12, "CURVATURE_RANK": 7, "RICCI_RANK": 5, "PETROV": 6,
    }), "survival marginal counts")
    for atlas, filename in P02_TABLES.items():
        source = rows(P02 / filename)
        subset = [row for row in survival if row["atlas"] == atlas]
        require({row["source_id"] for row in subset} == {row["id"] for row in source}, f"{atlas} source IDs")
        require(all(row["source_table_sha256"] == sha256(P02 / filename) for row in subset), f"{atlas} hash")
    require(sum(row["conditional_branch_status"] == "IN_SUPPLIED_LORENTZ_CONVENTION" for row in survival) == 1, "Z09 count")
    require(next(row for row in survival if row["conditional_branch_status"] == "IN_SUPPLIED_LORENTZ_CONVENTION")["source_id"] == "Z09", "Z09 identity")
    require(sum(row["conditional_branch_status"] == "IN_SUPPLIED_RECIPROCAL_SPLIT_CONVENTION" for row in survival) == 1, "S27 count")
    require(next(row for row in survival if row["conditional_branch_status"] == "IN_SUPPLIED_RECIPROCAL_SPLIT_CONVENTION")["source_id"] == "S27", "S27 identity")
    require(all(row["local_foundation_status"] != "REMOVED" for row in survival), "no unconditional removal")
    require(all(row["csn_quotient_key"] == "UNDEFINED_ON_CSN_QUOTIENT" for row in survival if row["atlas"] in {"CURVATURE_RANK", "RICCI_RANK"}), "representative ranks")
    require(len({row["csn_quotient_key"] for row in survival if row["atlas"] == "SPLIT_FIRST_JET"}) == 6, "split quotient")
    require({row["source_label"] for row in survival if row["atlas"] == "PETROV"} == {"I", "D", "II", "III", "N", "O"}, "Petrov coverage")
    require(any(row["atlas"] == "DPHI" and row["source_id"] == "F01" for row in survival), "phi zero retained")

    inconsistencies = tables["INCONSISTENT_COMBINATIONS.tsv"]
    require(len(inconsistencies) == 14 and {row["id"] for row in inconsistencies} == {f"I{i:02d}" for i in range(1, 15)}, "inconsistencies")
    require("u=v=1" in inconsistencies[0]["conflict"], "ordinary covariance intersection")
    dimensions = tables["UNCONSTRAINED_DIMENSIONS.tsv"]
    require(len(dimensions) == 13 and {row["id"] for row in dimensions} == {f"D{i:02d}" for i in range(1, 14)}, "dimensions")
    dim = {row["id"]: row for row in dimensions}
    require((dim["D05"]["parent_dimension"], dim["D05"]["after_declared_equivalence"]) == ("20", "10"), "curvature dimensions")
    require((dim["D09"]["parent_dimension"], dim["D09"]["after_declared_equivalence"]) == ("8", "6"), "split dimensions")
    require(dim["D10"]["branch"] == "B04" and dim["D11"]["branch"] == "B04", "seal dimensions")
    require(dim["D12"]["status"] == "UNCOUNTED_OPEN_SPACE" and dim["D13"]["status"] == "UNCOUNTED_OPEN_SPACE", "unknown dimensions")

    countermodels = tables["COUNTERMODEL_LEDGER.tsv"]
    require(len(countermodels) == 12 and {row["id"] for row in countermodels} == {f"M{i:02d}" for i in range(1, 13)}, "countermodels")
    counter = {row["id"]: row for row in countermodels}
    require("F01-F08" in counter["M04"]["witness"], "dphi countermodel")
    require("K01 and K02" in counter["M05"]["witness"], "twist countermodel")
    require("a*n" in counter["M10"]["witness"], "seal countermodel")

    require(graph["schema"] == "udt-p03-constraint-dependency-graph-1.0", "graph schema")
    node_ids = {node["id"] for node in graph["nodes"]}
    require(len(node_ids) == len(graph["nodes"]), "graph node duplicate")
    require(all(edge["from"] in node_ids and edge["to"] in node_ids for edge in graph["edges"]), "graph edge endpoints")
    actual_edges = {(edge["from"], edge["to"]) for edge in graph["edges"]}
    forbidden_edges = {(edge["from"], edge["to"]) for edge in graph["forbidden_edges"]}
    require(not actual_edges & forbidden_edges, "forbidden graph edge")
    require(("F_CSN", "Q_CSN_ORBITS") in actual_edges, "CSN graph edge")

    require(data["constraint_ruling"]["unconditional_point_local_metric_strata_removed"] == 0, "removal ruling")
    require(data["constraint_ruling"]["internal_reciprocity_metric_soldering"] == "OPEN", "soldering ruling")
    require(data["constraint_ruling"]["static_seal_normal_derivative"] == "FREE", "seal ruling")
    require(data["source_sha256"]["P02_manifest"] == "c56390eb26b80c54a3c3a09f4800086c8dbc00b5bfd40b2038e264e85bec8938", "P02 manifest pin")
    require(data["source_sha256"]["premise_ledger"] == sha256(MAP / "PREMISE_AND_REDUCTION_LEDGER.tsv"), "premise hash")
    require(data["source_sha256"]["cold_packet"] == sha256(ROOT / "UDT_NATIVE_ACTION_COLD_PACKET.md"), "cold packet hash")
    for filename, digest in data["table_sha256"].items():
        require(sha256(HERE / filename) == digest, f"table hash {filename}")


def expect_failure(name: str, operation, catches: dict[str, str]) -> None:
    try:
        operation()
    except (AssertionError, KeyError, StopIteration, ValueError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"mutation unexpectedly passed: {name}")


def mutate(data, tables, graph, target: str, field: str, value: str) -> None:
    changed = copy.deepcopy(tables)
    key, column = field.split(":", 1)
    row = next(
        row for row in changed[target]
        if row.get("id") == key or row.get("source_id") == key
    )
    row[column] = value
    validate(data, changed, graph)


def main() -> None:
    tracked = [RESULT, HERE / "CONSTRAINT_DEPENDENCY_GRAPH.json", *[HERE / name for name in TABLES]]
    before = {path.name: sha256(path) for path in tracked}
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["CUDA_VISIBLE_DEVICES"] = ""
    replay = subprocess.run(
        [sys.executable, "-B", str(HERE / "build_p03_constraint_atlas.py")],
        cwd=ROOT, env=environment, text=True, capture_output=True, timeout=300, check=False,
    )
    require(replay.returncode == 0 and not replay.stderr, replay.stdout + replay.stderr)
    require(replay.stdout == (HERE / "ATLAS_TRANSCRIPT.txt").read_text(encoding="utf-8"), "main transcript")
    require(before == {path.name: sha256(path) for path in tracked}, "deterministic replay")
    data, tables, graph = load()
    validate(data, tables, graph)

    checks: dict[str, str] = {"deterministic_replay_and_full_contract": "PASS"}
    phi = sp.symbols("phi", real=True)
    require(sp.simplify(sp.exp(-phi) * sp.exp(phi)) == 1, "independent determinant")
    a, b = sp.symbols("a b", real=True)
    residual = (
        sp.diag(sp.exp(-a), sp.exp(a)) * sp.diag(sp.exp(-b), sp.exp(b))
        - sp.diag(sp.exp(-(a + b)), sp.exp(a + b))
    ).applyfunc(sp.simplify)
    require(residual == sp.zeros(2), "independent composition")
    checks["independent_reciprocal_character"] = "PASS"

    require(sum(1 for n in range(5) for p in range(5 - n)) == 15, "inertia combinatorics")
    require(sum(1 for n in range(3) for p in range(3 - n)) ** 2 == 36, "split combinatorics")
    checks["independent_zero_jet_combinatorics"] = "PASS"

    p02_result = json.loads((P02 / "ATLAS_RESULT.json").read_text(encoding="utf-8"))
    require(p02_result["counts"]["discrete_registered_strata_total"] == 89, "P02 total")
    require(sum(data["P02_axis_counts"].values()) == 89, "P03 total")
    checks["independent_P02_axis_reconciliation"] = "PASS"

    kinematic = rows(P02 / "SPLIT_FIRST_JET_STRATA.tsv")
    grouped: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in kinematic:
        grouped[(row["shear_map_rank"], row["twist_map_rank"])].add(row["expansion_rank"])
    require(len(grouped) == 6 and all(values == {"0", "1"} for values in grouped.values()), "expansion quotient")
    checks["independent_split_quotient_count"] = "PASS"

    require(20 == 10 + 10 and 10 - 6 == 4, "curvature counts")
    direct = rows(P02 / "SECOND_JET_DIRECT_SUM_BASIS.tsv")
    require(Counter(row["sector"] for row in direct) == Counter({"WEYL_PRE_SCALE": 10, "SCHOUTEN_REPRESENTATIVE": 10}), "direct sum")
    checks["independent_curvature_dimension_reconstruction"] = "PASS"

    n, alpha = sp.symbols("n alpha", real=True)
    seal = alpha * n
    require(seal.subs(n, 0) == 0 and sp.diff(seal, n).subs(alpha, 0) == 0 and sp.diff(seal, n).subs(alpha, 1) == 1, "seal family")
    checks["independent_static_seal_countermodel"] = "PASS"

    require(subprocess.run(["git", "diff", "--quiet", BASE, "--", str(P02.relative_to(ROOT))], cwd=ROOT, check=False).returncode == 0, "P02 tree changed")
    listing = subprocess.run(["git", "ls-tree", "-r", BASE, str(P02.relative_to(ROOT))], cwd=ROOT, text=True, capture_output=True, check=True).stdout
    require(hashlib.sha256(listing.encode()).hexdigest() == "1321107a72020019c421521732a0248e627e07eec77b70bdf64be71bc068b436", "P02 tree pin")
    checks["independent_P02_immutability"] = "PASS"

    effects_text = (HERE / "CONSTRAINT_EFFECT_LEDGER.tsv").read_text(encoding="utf-8")
    require("PREFERRED" not in effects_text and "MERIT" not in effects_text, "hidden ranking")
    checks["independent_no_ranking_scan"] = "PASS"

    premise_source = rows(MAP / "PREMISE_AND_REDUCTION_LEDGER.tsv")
    require({row["id"] for row in premise_source} == {row["id"] for row in tables["FOUNDATION_INPUT_REGISTRY.tsv"]}, "premise source reconciliation")
    checks["independent_premise_source_reconciliation"] = "PASS"

    catches: dict[str, str] = {}
    bad = copy.deepcopy(data); bad["schema"] = "bad"
    expect_failure("schema", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(data); bad["maximum_conclusion"] = "PREFERRED_CONFIGURATION_FOUND"
    expect_failure("maximum_conclusion", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(data); bad["question_mode"] = "TARGETING"
    expect_failure("question_mode", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(data); bad["scope"]["action_selected"] = True
    expect_failure("action_selection", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(data); bad["scope"]["equation_of_motion_selected"] = True
    expect_failure("equation_selection", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(data); bad["scope"]["merit_filter_used"] = True
    expect_failure("merit_filter", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(data); bad["scope"]["P04_launched"] = True
    expect_failure("P04_launch", lambda: validate(bad, tables, graph), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["FOUNDATION_INPUT_REGISTRY.tsv"].pop()
    expect_failure("missing_premise", lambda: validate(data, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["FOUNDATION_INPUT_REGISTRY.tsv"].append(copy.deepcopy(bad_tables["FOUNDATION_INPUT_REGISTRY.tsv"][0]))
    expect_failure("duplicate_premise", lambda: validate(data, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["FOUNDATION_INPUT_REGISTRY.tsv"] if row["id"] == "P08")["source"] = ""
    expect_failure("uncited_constraint", lambda: validate(data, bad_tables, graph), catches)
    expect_failure("internal_metric_soldering", lambda: mutate(data, tables, graph, "REALIZATION_BRANCHES.tsv", "B00:metric_status", "METRIC_PLANE_SELECTED"), catches)
    expect_failure("conditional_Lorentz_promotion", lambda: mutate(data, tables, graph, "REALIZATION_BRANCHES.tsv", "B02:metric_status", "UNCONDITIONAL"), catches)
    expect_failure("conditional_split_promotion", lambda: mutate(data, tables, graph, "REALIZATION_BRANCHES.tsv", "B03:metric_status", "UNCONDITIONAL"), catches)
    expect_failure("seal_normal_fixed", lambda: mutate(data, tables, graph, "REALIZATION_BRANCHES.tsv", "B04:open_data", "boundary functional"), catches)
    expect_failure("finite_cell_local_equation", lambda: mutate(data, tables, graph, "CONSTRAINT_EFFECT_LEDGER.tsv", "E15:effect", "RESTRICT"), catches)
    expect_failure("bootstrap_local_equation", lambda: mutate(data, tables, graph, "CONSTRAINT_EFFECT_LEDGER.tsv", "E22:effect", "RESTRICT"), catches)
    expect_failure("normal_derivative_elimination", lambda: mutate(data, tables, graph, "CONSTRAINT_EFFECT_LEDGER.tsv", "E18:effect", "RESTRICT"), catches)
    expect_failure("dynamics_loaded", lambda: mutate(data, tables, graph, "CONSTRAINT_EFFECT_LEDGER.tsv", "E24:domain", "B01"), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["SURVIVING_STRATA.tsv"] = [row for row in bad_tables["SURVIVING_STRATA.tsv"] if not (row["atlas"] == "DPHI" and row["source_id"] == "F01")]
    expect_failure("phi_zero_deleted", lambda: validate(data, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["SURVIVING_STRATA.tsv"].pop()
    expect_failure("missing_P02_stratum", lambda: validate(data, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["SURVIVING_STRATA.tsv"].append(copy.deepcopy(bad_tables["SURVIVING_STRATA.tsv"][0]))
    expect_failure("duplicate_P02_stratum", lambda: validate(data, bad_tables, graph), catches)
    expect_failure("Z09_wrong_identity", lambda: mutate(data, tables, graph, "SURVIVING_STRATA.tsv", "Z09:source_id", "Z08"), catches)
    expect_failure("S27_wrong_identity", lambda: mutate(data, tables, graph, "SURVIVING_STRATA.tsv", "S27:source_id", "S26"), catches)
    expect_failure("curvature_rank_promoted_invariant", lambda: mutate(data, tables, graph, "SURVIVING_STRATA.tsv", "R0:csn_quotient_key", "CURVATURE_RANK_0"), catches)
    expect_failure("Ricci_rank_promoted_invariant", lambda: mutate(data, tables, graph, "SURVIVING_STRATA.tsv", "C0:csn_quotient_key", "RICCI_RANK_0"), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["SURVIVING_STRATA.tsv"] if row["atlas"] == "SPLIT_FIRST_JET" and row["source_id"] == "K01")["csn_quotient_key"] = "EXTRA_CLASS"
    expect_failure("split_quotient_wrong", lambda: validate(data, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["UNCONSTRAINED_DIMENSIONS.tsv"] if row["id"] == "D05")["after_declared_equivalence"] = "11"
    expect_failure("curvature_dimension_wrong", lambda: validate(data, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["UNCONSTRAINED_DIMENSIONS.tsv"] if row["id"] == "D09")["after_declared_equivalence"] = "7"
    expect_failure("split_dimension_wrong", lambda: validate(data, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["UNCONSTRAINED_DIMENSIONS.tsv"] if row["id"] == "D10")["branch"] = "B01"
    expect_failure("seal_branch_mixed", lambda: validate(data, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["COUNTERMODEL_LEDGER.tsv"] if row["id"] == "M05")["witness"] = ""
    expect_failure("twist_countermodel_missing", lambda: validate(data, bad_tables, graph), catches)
    bad_graph = copy.deepcopy(graph); bad_graph["edges"].append({"from": "Q_INTERNAL_CHARACTER", "to": "P02_ATLAS", "relation": "silent_solder"})
    expect_failure("forbidden_solder_edge", lambda: validate(data, tables, bad_graph), catches)
    bad_graph = copy.deepcopy(graph); bad_graph["edges"] = [edge for edge in bad_graph["edges"] if not (edge["from"] == "F_CSN" and edge["to"] == "Q_CSN_ORBITS")]
    expect_failure("CSN_edge_missing", lambda: validate(data, tables, bad_graph), catches)
    bad = copy.deepcopy(data); bad["source_sha256"]["P02_manifest"] = "0" * 64
    expect_failure("P02_manifest_drift", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(data); bad["constraint_ruling"]["unconditional_point_local_metric_strata_removed"] = 1
    expect_failure("unconditional_metric_removal", lambda: validate(bad, tables, graph), catches)
    require(len(catches) == 34 and set(catches.values()) == {"PASS"}, "catch count")

    output = {
        "schema": "udt-p03-founded-constraint-atlas-verification-1.0",
        "status": "PASS",
        "check_count": len(checks),
        "checks": checks,
        "catch_proof_count": len(catches),
        "catch_proofs": catches,
        "main_result_sha256": sha256(RESULT),
        "main_transcript_sha256": sha256(HERE / "ATLAS_TRANSCRIPT.txt"),
        "P02_manifest_sha256": sha256(P02 / "SHA256SUMS.txt"),
        "P02_tree_sha256": hashlib.sha256(listing.encode()).hexdigest(),
        "scope": {
            "independent_implementation": True,
            "generator_imported": False,
            "CPU_only": True,
            "action_or_equation_loaded": False,
            "merit_filter_used": False,
        },
    }
    VERIFY.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = (
        "P03 independent verification\n"
        "status=PASS\n"
        f"checks={len(checks)}/{len(checks)}\n"
        f"catch_proofs={len(catches)}/{len(catches)}\n"
        f"main_result_sha256={output['main_result_sha256']}\n"
        f"P02_manifest_sha256={output['P02_manifest_sha256']}\n"
        f"P02_tree_sha256={output['P02_tree_sha256']}\n"
        "generator_imported=False action_or_equation_loaded=False merit_filter=False\n"
    )
    TRANSCRIPT.write_text(transcript, encoding="utf-8")
    print(transcript, end="")


if __name__ == "__main__":
    main()

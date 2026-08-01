#!/usr/bin/env python3
"""Fail-closed deterministic verifier for the seven-family survivor map."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


EXPECTED_READINESS = {
    "F01": "CPU_EXACT_CHECK_READY",
    "F02": "BLOCKED_MISSING_FIXED_REALIZATION",
    "F03": "CONTROL_ONLY",
    "F04": "BLOCKED_MISSING_TIME_EQUATION",
    "F05": "BLOCKED_MISSING_NATIVE_RESPONSE",
    "F06": "NOT_APPLICABLE_EMPTY",
    "F07": "BLOCKED_MISSING_FIXED_REALIZATION",
}

EXPECTED_STATES = {
    "F01": "CONDITIONAL_PARTIAL_SURVIVOR",
    "F02": "CONDITIONAL_SECTOR_SURVIVOR_CONTINUOUS",
    "F03": "CONTROL_NONISOLATED",
    "F04": "CONDITIONAL_STATIC_FINITE_BOX_SURVIVOR",
    "F05": "STRUCTURAL_EXISTENCE_FAMILY_NOT_STABILITY_TESTED",
    "F06": "EXACT_SCOPED_EMPTY",
    "F07": "FORMAL_MODULES_NO_REALIZED_SURVIVOR",
}

EXPECTED_RESULT = {
    "action_adopted": False,
    "active_derivation_queue_families": 5,
    "bootstrap_law_adopted": False,
    "bootstrap_selected": 0,
    "candidate_contract_rows": 10,
    "carrier_adopted": False,
    "cell_rows": 84,
    "cells_per_family": 12,
    "conditional_survivor_families": 3,
    "control_families": 1,
    "cpu_bounded_solve_ready": 0,
    "cpu_exact_check_ready": 1,
    "empty_families": 1,
    "dependency_rows": 7,
    "derivation_queue_groups": 4,
    "families": 7,
    "families_discarded": 0,
    "family_overlap": 0,
    "formal_only_families": 1,
    "gpu_ready": 0,
    "gpu_used": False,
    "new_computation_run": False,
    "outcome": "SURVIVOR_MAP_COMPLETE_WITH_CPU_CANDIDATE",
    "premises": 16,
    "source_anchors": 15,
    "source_paths_verified": 1513,
    "structural_only_families": 1,
    "time_persistence_derived": 0,
}


def survivor_ok(data: list[dict[str, str]]) -> bool:
    ids = [row.get("family_id") for row in data]
    if ids != [f"F{i:02d}" for i in range(1, 8)] or len(ids) != len(set(ids)):
        return False
    keyed = {row["family_id"]: row for row in data}
    return (
        all(keyed[key].get("present_state") == value for key, value in EXPECTED_STATES.items())
        and all(keyed[key].get("readiness") == value for key, value in EXPECTED_READINESS.items())
        and "lambda-Schur sign certification" in keyed["F01"].get("later_test", "")
        and "never whole-chain or full physical stability" in keyed["F01"].get("maximum_test_conclusion", "")
        and "continuous" in keyed["F02"].get("present_state", "").lower()
        and "not an isolated stable basin" in keyed["F03"].get("excluded_or_negative", "")
        and "round-S2 POSIT" in keyed["F04"].get("surviving_branch", "")
        and keyed["F04"].get("time_status") == "OPEN_NO_NATIVE_TIME_EQUATION"
        and "not instability" in keyed["F06"].get("maximum_test_conclusion", "")
        and "formal" in keyed["F07"].get("present_state", "").lower()
        and all(row.get("bootstrap_status") == "NOT_SELECTED" for row in data)
    )


def cells_ok(data: list[dict[str, str]]) -> bool:
    keys = [(row.get("family_id"), row.get("cell_id")) for row in data]
    expected = [(f"F{i:02d}", f"C{j:02d}") for i in range(1, 8) for j in range(1, 13)]
    if keys != expected or len(keys) != len(set(keys)):
        return False
    keyed = {(row["family_id"], row["cell_id"]): row["status"] for row in data}
    return (
        keyed[("F01", "C08")] == "OPEN_LAMBDA_SCHUR_AND_FREE_GERM_CURVATURE"
        and keyed[("F01", "C12")] == "CPU_EXACT_CHECK_READY_LAMBDA_SCHUR_ONLY"
        and keyed[("F02", "C07")] == "EXACT_CONTINUOUS_SECTOR_DICHOTOMY"
        and keyed[("F03", "C08")] == "NOT_ISOLATED"
        and keyed[("F04", "C09")] == "OPEN_NO_NATIVE_TIME_EQUATION"
        and keyed[("F05", "C07")] == "NOT_TESTED"
        and keyed[("F06", "C01")] == "EMPTY_MASSIVE_SCOPE"
        and keyed[("F07", "C02")] == "OPEN_COMMON_REALIZED_BACKGROUND"
        and all(keyed[(f"F{i:02d}", "C11")] == "ABSENT" for i in range(1, 8))
    )


def readiness_ok(data: list[dict[str, str]]) -> bool:
    ids = [row.get("family_id") for row in data]
    if ids != [f"F{i:02d}" for i in range(1, 8)]:
        return False
    keyed = {row["family_id"]: row for row in data}
    if any(keyed[key].get("readiness") != value for key, value in EXPECTED_READINESS.items()):
        return False
    return (
        keyed["F01"].get("perturbation_domain") == "YES_FOR_LAMBDA_SCHUR_BLOCK_ONLY"
        and "FREE_GERM_REMAINS_SEPARATE" in keyed["F01"].get("primary_blocker_or_target", "")
        and keyed["F04"].get("physical_time_equation") == "NO"
        and keyed["F04"].get("physical_boundary") == "NO"
        and keyed["F05"].get("response") == "NO_STABILITY_RESPONSE"
        and keyed["F06"].get("fixed_object") == "NO_EMPTY"
        and keyed["F07"].get("fixed_object") == "NO_FORMAL_ONLY"
        and sum(row.get("readiness") == "CPU_EXACT_CHECK_READY" for row in data) == 1
        and sum(row.get("readiness") == "CPU_BOUNDED_SOLVE_READY" for row in data) == 0
        and sum(row.get("readiness") == "GPU_READY" for row in data) == 0
    )


def development_ok(data: list[dict[str, str]]) -> bool:
    expected = {
        "F01": ("ACTIVE_DERIVATION_QUEUE", "Q02_F01_FREE_GERM_COMPLETION", "2"),
        "F02": ("ACTIVE_DERIVATION_QUEUE", "Q01_JOINT_REALIZATION", "1"),
        "F03": ("RETAIN_AS_CONTROL", "NONE", "-"),
        "F04": ("ACTIVE_DERIVATION_QUEUE_DOWNSTREAM", "Q04_NATIVE_TIME_AND_PHYSICAL_BOUNDARY", "4"),
        "F05": ("ACTIVE_DERIVATION_QUEUE", "Q03_RING_RESPONSE_AND_VARIATION_DOMAIN", "3"),
        "F06": ("RETAIN_NEGATIVE_CONTROL_REOPEN_ON_PREMISE_CHANGE", "NONE", "-"),
        "F07": ("ACTIVE_DERIVATION_QUEUE", "Q01_JOINT_REALIZATION", "1"),
    }
    keyed = {row.get("family_id"): row for row in data}
    return (
        [row.get("family_id") for row in data] == [f"F{i:02d}" for i in range(1, 8)]
        and all(
            (
                keyed[family_id].get("development_disposition"),
                keyed[family_id].get("queue_group"),
                keyed[family_id].get("queue_rank"),
            )
            == values
            for family_id, values in expected.items()
        )
        and sum(row.get("development_disposition", "").startswith("ACTIVE_DERIVATION_QUEUE") for row in data) == 5
        and len({row.get("queue_group") for row in data if row.get("queue_group") != "NONE"}) == 4
        and all("ABANDON" not in row.get("development_disposition", "") for row in data)
        and all(
            row.get("priority_grade")
            == ("NOT_RANKED" if row.get("queue_group") == "NONE" else "WORKING_OPERATIONAL_NOT_PHYSICS")
            for row in data
        )
        and next(row for row in data if row["family_id"] == "F03")["development_disposition"] == "RETAIN_AS_CONTROL"
        and next(row for row in data if row["family_id"] == "F06")["development_disposition"] == "RETAIN_NEGATIVE_CONTROL_REOPEN_ON_PREMISE_CHANGE"
    )


def contract_ok(data: list[dict[str, str]]) -> bool:
    if len(data) != 10 or len({row.get("item") for row in data}) != 10:
        return False
    keyed = {row["item"]: row for row in data}
    return (
        keyed["family"].get("value") == "F01 only"
        and "R05 free f/h traces" in keyed["branch"].get("value", "")
        and "R06 SUPPLIED ODD zero f/h traces" in keyed["branch"].get("value", "")
        and "every isolated root" in keyed["target"].get("value", "")
        and "F(s)=integral_-1^1 log(w_s(x)) dx=0" in keyed["target"].get("value", "")
        and "s in (1,3)" in keyed["target"].get("value", "")
        and "sources prove existence but not root uniqueness" in keyed["target"].get("limit", "")
        and "free f/h trace branch only" in keyed["existing_anchor"].get("limit", "")
        and "not evidence for the odd-zero-trace branch" in keyed["existing_anchor"].get("limit", "")
        and "every isolated root" in keyed["certification"].get("value", "")
        and "free-trace and supplied-odd-zero-trace branch" in keyed["certification"].get("value", "")
        and keyed["maximum_conclusion"].get("status") == "FIXED"
        and "local single-cell" in keyed["maximum_conclusion"].get("value", "")
        and "no whole mixed-chain/full stability" in keyed["maximum_conclusion"].get("limit", "")
    )


def main() -> None:
    checks: list[tuple[str, bool]] = []
    inventory = rows("SOURCE_INVENTORY.tsv")
    paths = [row["path"] for row in inventory]
    checks.append(("sources_1513", len(inventory) == 1513))
    checks.append(("sources_unique_sorted", paths == sorted(paths) and len(paths) == len(set(paths))))
    checks.append(("source_bytes", all((ROOT / row["path"]).is_file() and sha256(ROOT / row["path"]) == row["sha256"] for row in inventory)))
    checks.append(("source_git_blobs", all(subprocess.check_output(["git", "rev-parse", f"HEAD:{row['path']}"], cwd=ROOT, text=True).strip() == row["git_blob"] for row in inventory)))
    checks.append(("families_7", len(rows("FAMILY_UNIVERSE.tsv")) == 7))
    checks.append(("cells_12", len(rows("CELL_UNIVERSE.tsv")) == 12))

    anchors = rows("SOURCE_AUTHORITY_LEDGER.tsv")
    source_by_path = {row["path"]: row for row in inventory}
    checks.append(("anchors_15", len(anchors) == 15 and [row["anchor_id"] for row in anchors] == [f"A{i:02d}" for i in range(1, 16)]))
    checks.append(("anchors_admitted", all(row["path"] in source_by_path and source_by_path[row["path"]]["sha256"] == row["sha256"] for row in anchors)))
    text = {row["anchor_id"]: (ROOT / row["path"]).read_text(encoding="utf-8") for row in anchors}
    checks.append(("p4_cpu_option_source", "named next-tile OPTION" in text["A04"] and "bounded-numeric contract" in text["A04"] and "NOT a banked value" in text["A04"]))
    checks.append(("p4_two_obstructions", "free wall-germ curvature" in text["A06"] and "lambda-Schur block" in text["A06"]))
    checks.append(("native_solve_ceiling", "not yet sufficient to run a native stability solve" in text["A10"]))
    checks.append(("hopf_time_ceiling", "SETTLED_STATIC_FINITE_BOX_CONDITIONAL" in text["A12"] and "dynamical/topological persistence remains open" in text["A12"]))

    generated = ["SOURCE_AUTHORITY_LEDGER.tsv", "PREMISE_LEDGER.tsv", "SURVIVOR_LEDGER.tsv", "SURVIVOR_CELL_MATRIX.tsv", "READINESS_LEDGER.tsv", "FAMILY_DEPENDENCY_CLOSURE.tsv", "DEVELOPMENT_QUEUE.tsv", "F01_CPU_CANDIDATE_CONTRACT.tsv", "RANKED_NEXT_TESTS.tsv", "STATUS_LEDGER.tsv", "RESULT.json"]
    before = {name: sha256(PKG / name) for name in generated}
    proc = subprocess.run([sys.executable, str(PKG / "derive_survivor_map.py")], cwd=ROOT, text=True, capture_output=True, timeout=60, check=False)
    after = {name: sha256(PKG / name) for name in generated}
    checks.append(("derive_exit_0", proc.returncode == 0))
    checks.append(("deterministic_replay", before == after))

    survivor = rows("SURVIVOR_LEDGER.tsv")
    cells = rows("SURVIVOR_CELL_MATRIX.tsv")
    readiness = rows("READINESS_LEDGER.tsv")
    premises = rows("PREMISE_LEDGER.tsv")
    dependency = rows("FAMILY_DEPENDENCY_CLOSURE.tsv")
    development = rows("DEVELOPMENT_QUEUE.tsv")
    contract = rows("F01_CPU_CANDIDATE_CONTRACT.tsv")
    next_tests = rows("RANKED_NEXT_TESTS.tsv")
    result = json.loads((PKG / "RESULT.json").read_text(encoding="utf-8"))
    checks.append(("survivor_exact", survivor_ok(survivor)))
    checks.append(("cells_exact_84", cells_ok(cells)))
    checks.append(("readiness_exact", readiness_ok(readiness)))
    checks.append(("premises_16", [row["premise_id"] for row in premises] == [f"P{i:02d}" for i in range(1, 17)]))
    checks.append(("dependency_7", [row["family_id"] for row in dependency] == [f"F{i:02d}" for i in range(1, 8)]))
    checks.append(("development_queue_distinct_from_readiness", development_ok(development)))
    checks.append(("candidate_contract_10", contract_ok(contract)))
    checks.append(("ranked_three", [row["rank"] for row in next_tests] == ["1", "2", "3"]))
    checks.append(("only_rank1_ready", next_tests[0]["status"] == "SEPARATELY_PREREGISTRABLE_CPU_EXACT_CHECK" and all("BLOCKED" in row["status"] for row in next_tests[1:])))
    checks.append(("result_exact", result == EXPECTED_RESULT))

    catches: list[tuple[str, bool]] = []
    catches.append(("missing_family", not survivor_ok(survivor[:-1])))
    catches.append(("duplicate_family", not survivor_ok(survivor + [copy.deepcopy(survivor[0])])))
    catches.append(("missing_cell", not cells_ok(cells[:-1])))
    duplicate_cell = copy.deepcopy(cells)
    duplicate_cell[-1] = copy.deepcopy(duplicate_cell[0])
    catches.append(("duplicate_cell", not cells_ok(duplicate_cell)))
    catches.append(("missing_premise", len(premises[:-1]) != 16))
    catches.append(("missing_dependency", len(dependency[:-1]) != 7))
    catches.append(("missing_development_row", not development_ok(development[:-1])))
    abandoned = copy.deepcopy(development)
    next(row for row in abandoned if row["family_id"] == "F02")["development_disposition"] = "ABANDONED"
    catches.append(("blocked_mislabeled_abandoned", not development_ok(abandoned)))
    de_queued = copy.deepcopy(development)
    next(row for row in de_queued if row["family_id"] == "F07")["queue_group"] = "NONE"
    catches.append(("blocked_family_silently_dequeued", not development_ok(de_queued)))
    priority_promoted = copy.deepcopy(development)
    next(row for row in priority_promoted if row["family_id"] == "F01")["priority_grade"] = "DERIVED_PHYSICS_PRIORITY"
    catches.append(("working_queue_rank_promoted_to_physics", not development_ok(priority_promoted)))
    mutated_contract = copy.deepcopy(contract)
    mutated_contract[-1]["limit"] = "full stability allowed"
    catches.append(("candidate_ceiling_drop", not contract_ok(mutated_contract)))
    singular_root = copy.deepcopy(contract)
    next(row for row in singular_root if row["item"] == "target")["value"] = "sign at the registered massive root"
    catches.append(("unproved_unique_root_smuggle", not contract_ok(singular_root)))
    broadened_anchor = copy.deepcopy(contract)
    next(row for row in broadened_anchor if row["item"] == "existing_anchor")["limit"] = "corroborates both branches"
    catches.append(("Galerkin_scope_broadened", not contract_ok(broadened_anchor)))
    mutations = [
        ("F01", "present_state", "FULL_STABLE_SURVIVOR", "F01_full_certificate"),
        ("F01", "maximum_test_conclusion", "full physical stability", "F01_scope_drop"),
        ("F02", "present_state", "DISCRETE_ISOLATED_BASIN", "F02_discrete_promotion"),
        ("F03", "present_state", "CONDITIONAL_SURVIVOR", "control_promotion"),
        ("F04", "surviving_branch", "native derived carrier Hopfion", "carrier_promotion"),
        ("F04", "time_status", "DERIVED_TIME_PERSISTENCE", "Hopf_time_promotion"),
        ("F05", "present_state", "STABILITY_TESTED_SURVIVOR", "ring_stability_smuggle"),
        ("F06", "present_state", "UNSTABLE_MEMBER", "empty_to_instability"),
        ("F07", "present_state", "REALIZED_LIVE_SURVIVOR", "formal_to_realized"),
        ("F07", "bootstrap_status", "SELECTED", "bootstrap_selection"),
    ]
    for family_id, field, value, name in mutations:
        mutated = copy.deepcopy(survivor)
        next(row for row in mutated if row["family_id"] == family_id)[field] = value
        catches.append((name, not survivor_ok(mutated)))
    readiness_mutations = [
        ("F02", "readiness", "CPU_BOUNDED_SOLVE_READY", "F02_solve_promotion"),
        ("F04", "readiness", "GPU_READY", "Hopf_gpu_promotion"),
        ("F05", "readiness", "CPU_BOUNDED_SOLVE_READY", "ring_solve_without_response"),
        ("F06", "readiness", "GPU_READY", "empty_gpu_promotion"),
        ("F07", "readiness", "GPU_READY", "formal_gpu_promotion"),
        ("F01", "perturbation_domain", "COMPLETE_PHYSICAL", "F01_domain_promotion"),
        ("F04", "physical_time_equation", "YES", "invented_time_equation"),
    ]
    for family_id, field, value, name in readiness_mutations:
        mutated = copy.deepcopy(readiness)
        next(row for row in mutated if row["family_id"] == family_id)[field] = value
        catches.append((name, not readiness_ok(mutated)))
    result_mutations = [
        ("cpu_exact_check_ready", 0, "erase_cpu_candidate"),
        ("cpu_bounded_solve_ready", 1, "solve_smuggle"),
        ("gpu_ready", 1, "gpu_smuggle"),
        ("time_persistence_derived", 1, "time_smuggle"),
        ("bootstrap_selected", 1, "bootstrap_smuggle"),
        ("new_computation_run", True, "computation_smuggle"),
        ("outcome", "SURVIVOR_MAP_COMPLETE_WITH_GPU_CANDIDATE", "wrong_outcome"),
    ]
    for field, value, name in result_mutations:
        mutated = copy.deepcopy(result)
        mutated[field] = value
        catches.append((name, mutated != EXPECTED_RESULT))

    failed = [name for name, passed in checks if not passed]
    bad_catches = [name for name, passed in catches if not passed]
    write_rows = [{"catch_id": f"K{i:02d}", "catch": name, "status": "REJECTED" if passed else "FAILED"} for i, (name, passed) in enumerate(catches, 1)]
    with (PKG / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(write_rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(write_rows)
    verification = {
        "status": "PASS" if not failed and not bad_catches else "FAIL",
        "checks_passed": sum(passed for _, passed in checks),
        "checks_total": len(checks),
        "catch_proofs_passed": sum(passed for _, passed in catches),
        "catch_proofs_total": len(catches),
        "failed": failed + bad_catches,
        "derive_stdout_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest(),
        "derive_stderr_sha256": hashlib.sha256(proc.stderr.encode()).hexdigest(),
    }
    (PKG / "VERIFICATION_RESULT.json").write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if verification["status"] != "PASS":
        raise RuntimeError(verification)
    print(f"PASS survivor-map verification: {len(checks)}/{len(checks)}; catches={len(catches)}/{len(catches)}")


if __name__ == "__main__":
    main()

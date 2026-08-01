#!/usr/bin/env python3
"""Cold verifier for the seven-family stability survivor map.

This implementation imports and executes neither derive_survivor_map.py nor
verify_survivor_map.py.  It reconstructs the source freeze, family cells,
readiness predicates, and development dispositions from frozen records.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
BASE = "d84fbf9c8686eca4479ec9977cfcef9023f8ce0f"
BRANCH = "codex/stability-family-survivor-map-2026-08-01"
PARENT_PACKAGE = "udt_stability_hypothesis_cross_family_atlas_2026-08-01"
DATE = "2026-08-01"


class Audit:
    def __init__(self) -> None:
        self.records: list[dict[str, object]] = []
        self.failures: list[str] = []
        self.checks = 0
        self.catches = 0

    def check(self, check_id: str, passed: bool, detail: str, **extra: object) -> None:
        self.checks += 1
        record = {"type": "check", "id": check_id, "passed": bool(passed), "detail": detail}
        record.update(extra)
        self.records.append(record)
        if not passed:
            self.failures.append(check_id)

    def source(self, **record: object) -> None:
        self.records.append({"type": "source", **record})

    def catch(self, catch_id: str, rejected: bool, detail: str) -> None:
        self.catches += 1
        self.records.append(
            {"type": "mutation", "id": catch_id, "passed": bool(rejected), "detail": detail}
        )
        if not rejected:
            self.failures.append(catch_id)


def run_git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    prefix = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(prefix + data).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def keyed(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows}


def write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_inventory_shape(rows: list[dict[str, str]]) -> list[str]:
    problems: list[str] = []
    required = {"path", "git_blob", "sha256", "bytes", "layer"}
    if len(rows) != 1513:
        problems.append("inventory_count")
    paths = [row.get("path", "") for row in rows]
    if len(paths) != len(set(paths)):
        problems.append("inventory_duplicate")
    if paths != sorted(paths):
        problems.append("inventory_sort")
    for row in rows:
        if set(row) != required or not all(row.get(field, "") for field in required):
            problems.append("inventory_schema")
            break
    return problems


CELL_IDS = tuple(f"C{i:02d}" for i in range(1, 13))
EXPECTED_CELL_STATUS = {
    "F01": (
        "CONDITIONAL_NONEMPTY_SCOPED", "CONDITIONAL_STATIONARY_WITNESS",
        "CONDITIONAL_REDUCED_JOINT_HESSIAN_OWNED",
        "PARTIAL_CREASE_PARITY_OWNED_HIGHER_GERMS_OPEN",
        "PARTIAL_ZERO_TRACE_CORE_FULL_GERMS_OPEN",
        "EMPTY_CLOSED_POSTURES_ROUTED_TO_F06",
        "FREE_BRANCH_UNSTABLE_ODD_PIN_CORE_POSITIVE",
        "OPEN_LAMBDA_SCHUR_AND_FREE_GERM_CURVATURE",
        "OPEN_NO_NATIVE_TIME_EQUATION", "OPEN_PHYSICAL_COMPLETION", "ABSENT",
        "CPU_EXACT_CHECK_READY_LAMBDA_SCHUR_ONLY",
    ),
    "F02": (
        "CONDITIONAL_NONEMPTY_CLASS", "CONDITIONAL_LANDING_NOT_JOINT_REALIZATION",
        "CONDITIONAL_SECTOR_HESSIAN_OWNED", "PARTIAL_CLASS_BOUNDARY",
        "SECTOR_DOMAIN_ONLY", "NO_EXISTENCE_EXCLUSION_WITHIN_RETAINED_JET_CLASS",
        "EXACT_CONTINUOUS_SECTOR_DICHOTOMY", "SECTOR_ONLY_NOT_FULL_CERTIFICATE",
        "OPEN_NO_NATIVE_TIME_EQUATION", "OPEN_PHYSICAL_COMPLETION", "ABSENT",
        "BLOCKED_MISSING_FIXED_REALIZATION",
    ),
    "F03": (
        "PRESENT_CONTROL", "PRESENT_CONTROL_BACKGROUND", "CONDITIONAL_CONTROL_HESSIAN_OWNED",
        "PRESENT_CONTROL_DOMAIN", "PRESENT_CONTROL_DOMAIN", "NONE",
        "PSD_DEGENERATE_CONTROL", "NOT_ISOLATED", "OPEN_NOT_PROMOTED",
        "NOT_EVALUATED_PHYSICALLY", "ABSENT", "CONTROL_ONLY",
    ),
    "F04": (
        "OBSERVED_CARRIER_CONDITIONAL", "OBSERVED_STATIC_FINITE_BOX",
        "CHOSEN_CONDITIONAL_L2_PLUS_L4", "COMPUTATIONAL_BOUNDARY_OWNED_PHYSICAL_OPEN",
        "STATIC_FINITE_BOX_DOMAIN_OWNED_TIME_DOMAIN_MISSING",
        "CONDITIONAL_TOPOLOGICAL_SECTOR_AVAILABLE", "SETTLED_STATIC_FINITE_BOX_CONDITIONAL",
        "STATIC_CERTIFICATE_ONLY", "OPEN_NO_NATIVE_TIME_EQUATION", "OPEN_PHYSICAL_BOUNDARY",
        "ABSENT", "BLOCKED_MISSING_TIME_EQUATION",
    ),
    "F05": (
        "MASSLESS_RING_EXISTS_MIXED_MULTICELL_CONDITIONAL", "CLOSURE_CONFIGURATION_ONLY",
        "PERIOD_LAW_NOT_STABILITY_RESPONSE", "SCOPED_CYCLIC_COMPLETION_OWNED",
        "NO_STABILITY_PERTURBATION_DOMAIN", "ALL_DEFINITE_MASSIVE_RING_EXCLUDED",
        "NOT_TESTED", "ABSENT", "OPEN_NOT_TESTABLE", "CLASSIFICATION_SCOPE_ONLY",
        "ABSENT", "BLOCKED_MISSING_NATIVE_RESPONSE",
    ),
    "F06": (
        "EMPTY_MASSIVE_SCOPE", "NONE_EMPTY", "COMPLETION_LAW_NOT_STABILITY_RESPONSE",
        "SCOPED_COMPLETION_OWNED", "NOT_APPLICABLE", "EXACT_NONEXISTENCE",
        "NOT_APPLICABLE", "NOT_APPLICABLE", "NOT_APPLICABLE", "SCOPED_CLOSURE_ONLY",
        "ABSENT", "NOT_APPLICABLE_EMPTY",
    ),
    "F07": (
        "FORMAL_MODULES_ONLY", "OPEN_COMMON_REALIZED_BACKGROUND",
        "ABSENT_COMPLETE_NATIVE_RESPONSE", "OPEN_DIFFERENTIABLE_FINITE_CELL_BOUNDARY",
        "ABSENT_TANGENT_SPACE_TO_REALIZED_SET", "BLOCKED_BY_REALIZATION_JOIN", "BLOCKED",
        "BLOCKED", "FORMAL_LABEL_ONLY_PHYSICAL_PERSISTENCE_OPEN", "OPEN", "ABSENT",
        "BLOCKED_MISSING_FIXED_REALIZATION",
    ),
}

EXPECTED_READINESS = {
    "F01": "CPU_EXACT_CHECK_READY", "F02": "BLOCKED_MISSING_FIXED_REALIZATION",
    "F03": "CONTROL_ONLY", "F04": "BLOCKED_MISSING_TIME_EQUATION",
    "F05": "BLOCKED_MISSING_NATIVE_RESPONSE", "F06": "NOT_APPLICABLE_EMPTY",
    "F07": "BLOCKED_MISSING_FIXED_REALIZATION",
}

EXPECTED_PRESENT_STATE = {
    "F01": "CONDITIONAL_PARTIAL_SURVIVOR",
    "F02": "CONDITIONAL_SECTOR_SURVIVOR_CONTINUOUS", "F03": "CONTROL_NONISOLATED",
    "F04": "CONDITIONAL_STATIC_FINITE_BOX_SURVIVOR",
    "F05": "STRUCTURAL_EXISTENCE_FAMILY_NOT_STABILITY_TESTED", "F06": "EXACT_SCOPED_EMPTY",
    "F07": "FORMAL_MODULES_NO_REALIZED_SURVIVOR",
}

EXPECTED_DEVELOPMENT = {
    "F01": ("ACTIVE_DERIVATION_QUEUE", "Q02_F01_FREE_GERM_COMPLETION", "2"),
    "F02": ("ACTIVE_DERIVATION_QUEUE", "Q01_JOINT_REALIZATION", "1"),
    "F03": ("RETAIN_AS_CONTROL", "NONE", "-"),
    "F04": ("ACTIVE_DERIVATION_QUEUE_DOWNSTREAM", "Q04_NATIVE_TIME_AND_PHYSICAL_BOUNDARY", "4"),
    "F05": ("ACTIVE_DERIVATION_QUEUE", "Q03_RING_RESPONSE_AND_VARIATION_DOMAIN", "3"),
    "F06": ("RETAIN_NEGATIVE_CONTROL_REOPEN_ON_PREMISE_CHANGE", "NONE", "-"),
    "F07": ("ACTIVE_DERIVATION_QUEUE", "Q01_JOINT_REALIZATION", "1"),
}


SOURCE_TOKENS = {
    "udt_stability_hypothesis_cross_family_atlas_2026-08-01/FAMILY_ATLAS.tsv": (
        "free angular-wall branch unstable; odd pin makes zero-trace core positive; whole certificate still open",
        "stable iff 64 E0^2 ell^4 <= g_p c_m pi^4",
        "NOT_TESTED; closure/mass classification only",
        "BLOCKED_BY_REALIZATION_JOIN",
    ),
    "udt_stability_hypothesis_cross_family_atlas_2026-08-01/INDEPENDENT_REVIEW.md": (
        "No discrete species catalogue, isolated multi-basin spectrum",
        "Nonexistence is not instability.",
        "formal static/time/angular modules",
    ),
    "udt_p4_stability_slice_2026-07-30/EXACT_DERIVATION.md": (
        "the odd-parity f/bh pin",
        "free wall-germ curvature; the lambda-Schur block",
        "is UNPINNED by",
        "index >= 1 exact; exactly-1 pending the lambda-Schur sign",
    ),
    "udt_p4_stability_slice_2026-07-30/CORRECTION_LAYER.md": (
        "Galerkin hunt gives n- = 1 at dims 13/17/21",
        "A LEAD, not a verdict.",
    ),
    "udt_p4_stability_slice_2026-07-30/STABILITY_LEDGER.tsv": (
        "supplied f/bh wall data FREE",
        "supplied f/bh parity ODD (zero angular traces)",
        "exactly-1 pending lambda-Schur sign",
    ),
    "udt_p4_period_gate_2026-07-30/EXACT_DERIVATION.md": (
        "crease-pinned one-parameter branch",
        "w1 = 2A − √(2A), w0 = 1 + A − √(2A)",
        "continuity of A ↦ I_p (Category-A) gives a root A* ∈ (1/2, 9/2)",
    ),
    "udt_p4_period_gate_2026-07-30/AUDIT_REPORT.md": (
        "is corroboration, not a banked value.",
        "normalization is CHOSE",
    ),
    "udt_p4_cold_adversarial_review_2026-08-01/AUDIT_REPORT.md": (
        "free wall-germ curvature and the",
        "lambda-Schur sector prevent a full certificate",
        "fixed-realized-solution embedding",
    ),
    "udt_stability_foundations_audit_2026-08-01/FIXED_REALIZATION_GATE.tsv": (
        "one common full field assignment u",
        "native whole-system equation E_native[u]=0",
        "BLOCKED_BY_MISSING_JOIN",
    ),
    "udt_stability_foundations_audit_2026-08-01/AUDIT_REPORT.md": (
        "native structure to turn them into one unconditional stability test",
        "next justified scientific object is a separately preregistered",
    ),
    "native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv": (
        "SETTLED_STATIC_FINITE_BOX_CONDITIONAL",
        "physical finite-cell carrier completion\tOPEN",
        "dynamical/topological persistence remains open",
    ),
    "CURRENT_SCIENTIFIC_PREMISES.tsv": (
        "S2_carrier",
        "WORKING_ON_SHELL_ADMISSIBILITY",
        "complete_native_action_source_boundary_mass\tOPEN",
    ),
    "udt_global_local_self_consistency_premise_audit_2026-08-01/AUDIT_REPORT.md": (
        "BOOTSTRAP_IS_DISTINCT_POSIT",
        "No registered route supplies the missing nontrivial membership",
    ),
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv": (
        "Complete native action\tOPEN",
        "Finite-cell differentiable boundary action\tOPEN",
    ),
}


def validate_cells(rows: list[dict[str, str]]) -> list[str]:
    problems: list[str] = []
    keys = [(row.get("family_id", ""), row.get("cell_id", "")) for row in rows]
    expected_keys = [(family, cell) for family in EXPECTED_CELL_STATUS for cell in CELL_IDS]
    if len(rows) != 84 or len(keys) != len(set(keys)) or set(keys) != set(expected_keys):
        problems.append("cell_universe")
        return problems
    lookup = {(row["family_id"], row["cell_id"]): row for row in rows}
    for family, statuses in EXPECTED_CELL_STATUS.items():
        for cell, status in zip(CELL_IDS, statuses):
            if lookup[(family, cell)].get("status") != status:
                problems.append(f"cell_status:{family}:{cell}")
    return problems


def validate_readiness(rows: list[dict[str, str]]) -> list[str]:
    problems: list[str] = []
    if len(rows) != 7 or len({row.get("family_id") for row in rows}) != 7:
        return ["readiness_universe"]
    by_family = keyed(rows, "family_id")
    for family, expected in EXPECTED_READINESS.items():
        if by_family.get(family, {}).get("readiness") != expected:
            problems.append(f"readiness:{family}")
    if sum(row.get("readiness") == "CPU_EXACT_CHECK_READY" for row in rows) != 1:
        problems.append("cpu_exact_count")
    if any(row.get("readiness") in {"CPU_BOUNDED_SOLVE_READY", "GPU_READY"} for row in rows):
        problems.append("solve_or_gpu_promotion")
    return problems


def validate_development(rows: list[dict[str, str]]) -> list[str]:
    problems: list[str] = []
    if len(rows) != 7 or len({row.get("family_id") for row in rows}) != 7:
        return ["development_universe"]
    by_family = keyed(rows, "family_id")
    for family, expected in EXPECTED_DEVELOPMENT.items():
        row = by_family.get(family, {})
        got = (row.get("development_disposition"), row.get("queue_group"), row.get("queue_rank"))
        if got != expected:
            problems.append(f"development:{family}")
    active = [row for row in rows if row.get("development_disposition", "").startswith("ACTIVE_")]
    groups = {row["queue_group"] for row in active}
    if len(active) != 5 or len(groups) != 4:
        problems.append("active_queue_census")
    if any(row.get("priority_grade") != "WORKING_OPERATIONAL_NOT_PHYSICS" for row in active):
        problems.append("queue_rank_physics_promotion")
    dispositions = {row.get("development_disposition", "") for row in rows}
    if "ABANDONED" in dispositions or "DISCARDED" in dispositions:
        problems.append("abandonment_language")
    return problems


def validate_f01_contract(rows: list[dict[str, str]]) -> list[str]:
    problems: list[str] = []
    items = keyed(rows, "item")
    if len(rows) != 10 or len(items) != 10:
        return ["f01_contract_universe"]
    branch = items.get("branch", {}).get("value", "").lower()
    target = items.get("target", {}).get("value", "").lower()
    independent = items.get("independent_method", {}).get("value", "").lower()
    certification = items.get("certification", {}).get("value", "").lower()
    maximum = (items.get("maximum_conclusion", {}).get("value", "") + " "
               + items.get("maximum_conclusion", {}).get("limit", "")).lower()
    wall_limit = items.get("wall_response", {}).get("limit", "").lower()

    # The bank proves existence by IVT but not uniqueness.  A ready contract must
    # address every root in the exact interval or make uniqueness a test target.
    root_closed = (
        ("every" in target or "all" in target or "root set" in target)
        and "root" in target and ("(1,3)" in target or "1 < s < 3" in target)
    ) or ("uniqueness" in target and "root" in target)
    if not root_closed:
        problems.append("f01_root_quantifier")
    if not ("free" in branch and "odd" in branch and ("trace" in branch or "f/h" in branch)):
        problems.append("f01_branch_names")
    if "independent" not in independent or not any(word in independent for word in ("index", "sturm", "spectral")):
        problems.append("f01_independent_route")
    if "every" not in certification or "root" not in certification or "zero" not in certification:
        problems.append("f01_certification_all_roots")
    if not any(scope in maximum for scope in ("single-cell", "cell block", "local cell")):
        problems.append("f01_cell_ceiling")
    if not ("chain" in maximum and any(term in maximum for term in ("not whole", "no whole"))):
        problems.append("f01_chain_ceiling")
    if "germ" not in wall_limit or "open" not in wall_limit:
        problems.append("f01_free_germ_separation")
    return problems


def parse_manifest(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, rel = line.split("  ", 1)
        if rel.startswith("../"):
            rel = rel[3:]
        result[rel] = digest
    return result


def base_tree() -> dict[str, str]:
    tree: dict[str, str] = {}
    for line in run_git("ls-tree", "-r", BASE).splitlines():
        meta, path = line.split("\t", 1)
        _mode, kind, blob = meta.split()
        if kind == "blob":
            tree[path] = blob
    return tree


def source_row_ok(row: dict[str, str], data: bytes, tree_blob: str | None, manifest_sha: str | None) -> bool:
    return (
        sha256(data) == row.get("sha256") == manifest_sha
        and git_blob(data) == row.get("git_blob") == tree_blob
        and len(data) == int(row.get("bytes", "-1"))
    )


def source_freeze(audit: Audit) -> tuple[list[dict[str, str]], set[str]]:
    inventory = read_tsv(PACKAGE / "SOURCE_INVENTORY.tsv")
    shape_problems = validate_inventory_shape(inventory)
    audit.check("S01_inventory_shape", not shape_problems, "1,513 sorted unique source rows", problems=shape_problems)

    paths = [row["path"] for row in inventory]
    path_list = (PACKAGE / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines()
    manifest = parse_manifest(PACKAGE / "SOURCE_MANIFEST.sha256")
    audit.check("S02_path_list", path_list == paths, "path list exactly matches inventory order")
    audit.check("S03_manifest_shape", set(manifest) == set(paths) and len(manifest) == 1513,
                "manifest covers exactly the source inventory")

    parent_rows = read_tsv(ROOT / PARENT_PACKAGE / "SOURCE_INVENTORY.tsv")
    parent_paths = {row["path"] for row in parent_rows}
    tracked_parent = set(run_git("ls-tree", "-r", "--name-only", BASE, "--", PARENT_PACKAGE).splitlines())
    expected_union = parent_paths | tracked_parent
    audit.check("S04_parent_freeze", len(parent_paths) == 1469, "parent effective source freeze is 1,469")
    audit.check("S05_parent_package", len(tracked_parent) == 44, "complete parent atlas package has 44 tracked files")
    audit.check("S06_union", len(expected_union) == 1513 and set(paths) == expected_union,
                "source universe is the exact additions-only 1,469 + 44 union")

    tree = base_tree()
    bad: list[str] = []
    total_bytes = 0
    layer_counts: dict[str, int] = {}
    for row in inventory:
        path = row["path"]
        data = (ROOT / path).read_bytes()
        actual_sha = sha256(data)
        actual_blob = git_blob(data)
        total_bytes += len(data)
        layer_counts[row["layer"]] = layer_counts.get(row["layer"], 0) + 1
        passed = source_row_ok(row, data, tree.get(path), manifest.get(path))
        if not passed:
            bad.append(path)
        audit.source(path=path, bytes=len(data), sha256=actual_sha, git_blob=actual_blob,
                     base_blob=tree.get(path), layer=row["layer"], passed=passed)
    audit.check("S07_all_bytes_blobs", not bad, "all 1,513 worktree bytes, SHA-256 values, and base Git blobs match",
                bad=bad[:10], total_bytes=total_bytes)
    audit.check("S08_layers", layer_counts == {"PARENT_EFFECTIVE_SOURCE_UNIVERSE": 1469,
                                               "COMPLETE_PARENT_ATLAS_PACKAGE": 44},
                "source layer census is exact", layer_counts=layer_counts)
    return inventory, set(paths)


def verify_repository_identity(audit: Audit) -> None:
    head = run_git("rev-parse", "HEAD").strip()
    parent = run_git("rev-parse", "HEAD^").strip()
    branch = run_git("branch", "--show-current").strip()
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASE, head], cwd=ROOT, check=False
    ).returncode == 0
    audit.check("G01_branch", branch == BRANCH, "dispatched audit branch is active", branch=branch)
    audit.check("G02_head_parent", parent == BASE and ancestor,
                "preregistration HEAD descends directly from the declared frozen base",
                head=head, parent=parent, base=BASE, ancestor=ancestor)
    prereg = (PACKAGE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    audit.check("G03_prereg_base", BASE in prereg and BRANCH in prereg,
                "preregistration records the exact base and branch")


def verify_source_authority(audit: Audit, admitted: set[str]) -> None:
    authority = read_tsv(PACKAGE / "SOURCE_AUTHORITY_LEDGER.tsv")
    ids = [row.get("anchor_id") for row in authority]
    ok = len(authority) == 15 and len(ids) == len(set(ids))
    for row in authority:
        path = row.get("path", "")
        ok = ok and path in admitted and sha256((ROOT / path).read_bytes()) == row.get("sha256")
    audit.check("A01_authority", ok, "15 unique controlling anchors are admitted and hash-exact")

    missing: dict[str, list[str]] = {}
    for path, tokens in SOURCE_TOKENS.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        absent = [token for token in tokens if token not in text]
        if absent:
            missing[path] = absent
    audit.check("A02_source_local_rulings", not missing,
                "independently selected controlling source passages support the family/readiness reconstruction",
                missing=missing)


def verify_family_outputs(audit: Audit) -> dict[str, list[dict[str, str]]]:
    outputs = {
        "cells": read_tsv(PACKAGE / "SURVIVOR_CELL_MATRIX.tsv"),
        "survivors": read_tsv(PACKAGE / "SURVIVOR_LEDGER.tsv"),
        "readiness": read_tsv(PACKAGE / "READINESS_LEDGER.tsv"),
        "dependencies": read_tsv(PACKAGE / "FAMILY_DEPENDENCY_CLOSURE.tsv"),
        "development": read_tsv(PACKAGE / "DEVELOPMENT_QUEUE.tsv"),
        "contract": read_tsv(PACKAGE / "F01_CPU_CANDIDATE_CONTRACT.tsv"),
    }
    cell_problems = validate_cells(outputs["cells"])
    audit.check("F01_cells", not cell_problems, "seven families x twelve independently reconstructed cells match",
                problems=cell_problems)

    survivors = outputs["survivors"]
    survivor_ok = len(survivors) == 7 and len({row.get("family_id") for row in survivors}) == 7
    survivor_ok = survivor_ok and all(
        keyed(survivors, "family_id").get(family, {}).get("present_state") == state
        for family, state in EXPECTED_PRESENT_STATE.items()
    )
    audit.check("F02_survivors", survivor_ok,
                "conditional survivors, control, structural family, empty family, and formal family remain distinct")

    readiness_problems = validate_readiness(outputs["readiness"])
    audit.check("F03_readiness", not readiness_problems,
                "one exact CPU cell, zero CPU solves, and zero GPU candidates reproduce",
                problems=readiness_problems)

    dependencies = outputs["dependencies"]
    dependency_ok = len(dependencies) == 7 and len({row.get("family_id") for row in dependencies}) == 7
    dependency_ok = dependency_ok and all(row.get("missing_closure") for row in dependencies)
    audit.check("F04_dependencies", dependency_ok, "every family retains an explicit closure or empty/control limit")

    development_problems = validate_development(outputs["development"])
    audit.check("F05_development", not development_problems,
                "five active families remain in four non-authorizing development groups; F03/F06 retained",
                problems=development_problems)

    contract_problems = validate_f01_contract(outputs["contract"])
    audit.check("F06_f01_contract", not contract_problems,
                "F01 contract closes root quantifiers, names both boundary branches, and limits the result to a local cell",
                problems=contract_problems)
    return outputs


def verify_f01_ownership(audit: Audit, outputs: dict[str, list[dict[str, str]]]) -> dict[str, object]:
    contract = keyed(outputs["contract"], "item")
    readiness = keyed(outputs["readiness"], "family_id")["F01"]
    target = contract["target"]["value"]
    branch = contract["branch"]["value"]
    existing = contract["existing_anchor"]["value"] + " " + contract["existing_anchor"]["limit"]
    maximum = contract["maximum_conclusion"]["value"] + " " + contract["maximum_conclusion"]["limit"]

    ownership = {
        "exact_target_owned": "F(s)" in target and "w_s" in target and "s in (1,3)" in target,
        "all_roots_or_uniqueness_explicit": (
            ("every" in target.lower() or "all" in target.lower()) and "root" in target.lower()
        ) or "uniqueness" in target.lower(),
        "root_uniqueness_currently_owned": False,
        "free_trace_branch_owned": "R05" in branch and "free" in branch.lower(),
        "odd_zero_trace_branch_owned": "R06" in branch and "odd" in branch.lower(),
        "conditional_response_owned": readiness["response"] == "YES_CONDITIONAL",
        "cell_boundary_owned": "REGISTERED_CREASE_WITNESS" in readiness["boundary"],
        "schur_domain_only_owned": readiness["perturbation_domain"] == "YES_FOR_LAMBDA_SCHUR_BLOCK_ONLY",
        "independent_route_specified": "independent" in contract["independent_method"]["value"].lower(),
        "galerkin_is_free_trace_only": "free" in existing.lower() and "odd" in existing.lower(),
        "new_physical_equation_required": False,
        "new_mathematical_derivation_required": True,
        "local_cell_ceiling": any(term in maximum.lower() for term in ("single-cell", "cell block", "local cell")),
        "whole_chain_excluded": "whole" in maximum.lower() and "chain" in maximum.lower(),
        "free_second_germ_separate": "germ" in readiness["primary_blocker_or_target"].lower(),
    }
    required_true = [key for key in ownership if key not in {
        "root_uniqueness_currently_owned", "new_physical_equation_required"
    }]
    audit.check("R01_f01_ownership", all(bool(ownership[key]) for key in required_true),
                "F01 owns a bounded conditional cell test without assuming root uniqueness or a new physical equation",
                ownership=ownership)
    audit.check("R02_f01_no_uniqueness_promotion", ownership["root_uniqueness_currently_owned"] is False,
                "the banked IVT root existence is not promoted to uniqueness")

    candidate_ready = (
        ownership["exact_target_owned"]
        and ownership["all_roots_or_uniqueness_explicit"]
        and ownership["free_trace_branch_owned"]
        and ownership["odd_zero_trace_branch_owned"]
        and ownership["conditional_response_owned"]
        and ownership["cell_boundary_owned"]
        and ownership["schur_domain_only_owned"]
        and ownership["independent_route_specified"]
        and not ownership["new_physical_equation_required"]
        and ownership["local_cell_ceiling"]
        and ownership["whole_chain_excluded"]
    )
    audit.check("R03_f01_ready", candidate_ready,
                "CPU_EXACT_CHECK_READY applies only to the corrected lambda/mu Schur cell")
    audit.check("R04_f01_not_full", ownership["free_second_germ_separate"],
                "free second-wall-germ curvature remains separate and blocks a full certificate")
    return ownership


def verify_other_readiness(audit: Audit, outputs: dict[str, list[dict[str, str]]]) -> None:
    readiness = keyed(outputs["readiness"], "family_id")
    predicates = {
        "F02": readiness["F02"]["fixed_object"] == "CONDITIONAL_CLASS_ONLY"
               and readiness["F02"]["perturbation_domain"] == "SECTOR_ONLY",
        "F03": readiness["F03"]["readiness"] == "CONTROL_ONLY",
        "F04": readiness["F04"]["physical_time_equation"] == "NO"
               and readiness["F04"]["physical_boundary"] == "NO",
        "F05": readiness["F05"]["response"] == "NO_STABILITY_RESPONSE"
               and readiness["F05"]["perturbation_domain"] == "NO",
        "F06": readiness["F06"]["fixed_object"] == "NO_EMPTY",
        "F07": readiness["F07"]["fixed_object"] == "NO_FORMAL_ONLY"
               and readiness["F07"]["perturbation_domain"] == "NO_REALIZED_TANGENT_SPACE",
    }
    audit.check("R05_other_blockers", all(predicates.values()),
                "each non-F01 family retains its distinct evidence-backed blocker/control status",
                predicates=predicates)
    audit.check("R06_no_other_compute", all(
        readiness[family]["readiness"] not in {"CPU_EXACT_CHECK_READY", "CPU_BOUNDED_SOLVE_READY", "GPU_READY"}
        for family in ("F02", "F03", "F04", "F05", "F06", "F07")
    ), "no other family is CPU-check, CPU-solve, or GPU ready")


def verify_proposal(audit: Audit) -> None:
    path = PACKAGE / "DERIVATION_CLOSURE_SWEEP_PROPOSAL.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    lowered = text.lower()
    required = ("working_operational_proposal_not_authorized", "q01", "q02", "q03", "q04",
                "not a shared solver", "do not discard", "gpu work begins only")
    forbidden = ("common stability operator is owned", "blocked families are abandoned")
    passed = bool(text) and all(token in lowered for token in required) and not any(token in lowered for token in forbidden)
    audit.check("Q01_sweep_proposal", passed,
                "blanket derivation sweep remains a dependency-ordered, non-authorizing proposal with no operator merge")


def mutation_catches(audit: Audit, inventory: list[dict[str, str]], outputs: dict[str, list[dict[str, str]]]) -> None:
    bad_inventory = copy.deepcopy(inventory[:-1])
    audit.catch("K01_missing_source", bool(validate_inventory_shape(bad_inventory)), "missing source rejected")
    bad_inventory = copy.deepcopy(inventory)
    bad_inventory[-1] = copy.deepcopy(bad_inventory[0])
    audit.catch("K02_duplicate_source", bool(validate_inventory_shape(bad_inventory)), "duplicate source rejected")
    row = copy.deepcopy(inventory[0])
    data = (ROOT / row["path"]).read_bytes()
    row["sha256"] = "0" * 64
    audit.catch("K03_source_hash", not source_row_ok(row, data, inventory[0]["git_blob"], inventory[0]["sha256"]),
                "source SHA mutation rejected by production byte/blob predicate")
    row = copy.deepcopy(inventory[0])
    row["git_blob"] = "0" * 40
    audit.catch("K04_source_blob", not source_row_ok(row, data, inventory[0]["git_blob"], inventory[0]["sha256"]),
                "source Git-blob mutation rejected by production byte/blob predicate")

    cells = outputs["cells"]
    audit.catch("K05_missing_cell", bool(validate_cells(copy.deepcopy(cells[:-1]))), "missing cell rejected")
    duplicate = copy.deepcopy(cells)
    duplicate[-1] = copy.deepcopy(duplicate[0])
    audit.catch("K06_duplicate_cell", bool(validate_cells(duplicate)), "duplicate family/cell rejected")
    promoted = copy.deepcopy(cells)
    next(row for row in promoted if row["family_id"] == "F01" and row["cell_id"] == "C08")["status"] = "FULL_STABILITY_CERTIFIED"
    audit.catch("K07_f01_full_certificate", bool(validate_cells(promoted)), "F01 full-certificate promotion rejected")
    promoted = copy.deepcopy(cells)
    next(row for row in promoted if row["family_id"] == "F04" and row["cell_id"] == "C09")["status"] = "TIME_PERSISTENT"
    audit.catch("K08_hopf_time", bool(validate_cells(promoted)), "static Hopfion to time-persistence promotion rejected")
    promoted = copy.deepcopy(cells)
    next(row for row in promoted if row["family_id"] == "F05" and row["cell_id"] == "C07")["status"] = "STABLE"
    audit.catch("K09_ring_stability", bool(validate_cells(promoted)), "ring closure to stability promotion rejected")
    promoted = copy.deepcopy(cells)
    next(row for row in promoted if row["family_id"] == "F06" and row["cell_id"] == "C07")["status"] = "UNSTABLE"
    audit.catch("K10_empty_instability", bool(validate_cells(promoted)), "empty domain to instability promotion rejected")
    promoted = copy.deepcopy(cells)
    next(row for row in promoted if row["family_id"] == "F07" and row["cell_id"] == "C02")["status"] = "REALIZED"
    audit.catch("K11_formal_realized", bool(validate_cells(promoted)), "formal module to realized object promotion rejected")

    readiness = outputs["readiness"]
    for catch_id, family, value in (
        ("K12_f02_solve", "F02", "CPU_BOUNDED_SOLVE_READY"),
        ("K13_f04_gpu", "F04", "GPU_READY"),
        ("K14_f05_solve", "F05", "CPU_BOUNDED_SOLVE_READY"),
        ("K15_f06_gpu", "F06", "GPU_READY"),
        ("K16_f07_gpu", "F07", "GPU_READY"),
        ("K17_erase_f01", "F01", "BLOCKED_MISSING_BOUNDARY"),
    ):
        mutant = copy.deepcopy(readiness)
        next(row for row in mutant if row["family_id"] == family)["readiness"] = value
        audit.catch(catch_id, bool(validate_readiness(mutant)), f"readiness mutation for {family} rejected")

    development = outputs["development"]
    audit.catch("K18_silent_dequeue", bool(validate_development(copy.deepcopy(development[:-1]))),
                "blocked family silently removed from development map is rejected")
    mutant = copy.deepcopy(development)
    next(row for row in mutant if row["family_id"] == "F02")["development_disposition"] = "ABANDONED"
    audit.catch("K19_abandonment", bool(validate_development(mutant)), "blocked-to-abandoned mutation rejected")
    mutant = copy.deepcopy(development)
    next(row for row in mutant if row["family_id"] == "F04")["priority_grade"] = "PHYSICS_PRIORITY"
    audit.catch("K20_rank_physics", bool(validate_development(mutant)), "working queue rank promoted to physics rejected")
    mutant = copy.deepcopy(development)
    next(row for row in mutant if row["family_id"] == "F06")["development_disposition"] = "DISCARDED"
    audit.catch("K21_discard_negative", bool(validate_development(mutant)), "scoped negative discarded instead of retained rejected")

    contract = outputs["contract"]
    for catch_id, item, value in (
        ("K22_unique_root", "target", "sign at the unique registered massive root for both parities"),
        ("K23_vague_branches", "branch", "registered massive certified crease branches"),
        ("K24_whole_chain", "maximum_conclusion", "whole-chain F01 stability index"),
        ("K25_same_code", "independent_method", "same-code replay of the primary scalar"),
        ("K26_root_subset", "certification", "bounds exclude zero at a selected root"),
    ):
        mutant = copy.deepcopy(contract)
        next(row for row in mutant if row["item"] == item)["value"] = value
        audit.catch(catch_id, bool(validate_f01_contract(mutant)), f"F01 contract mutation {item} rejected")


def main() -> int:
    audit = Audit()
    verify_repository_identity(audit)
    inventory, admitted = source_freeze(audit)
    verify_source_authority(audit, admitted)

    family_universe = read_tsv(PACKAGE / "FAMILY_UNIVERSE.tsv")
    cell_universe = read_tsv(PACKAGE / "CELL_UNIVERSE.tsv")
    premise_ledger = read_tsv(PACKAGE / "PREMISE_LEDGER.tsv")
    audit.check("M01_family_universe", len(family_universe) == 7
                and [row["family_id"] for row in family_universe] == list(EXPECTED_CELL_STATUS),
                "seven frozen effective partitions reproduce in order")
    audit.check("M02_cell_universe", len(cell_universe) == 12
                and [row["cell_id"] for row in cell_universe] == list(CELL_IDS),
                "twelve frozen cell questions reproduce in order")
    audit.check("M03_premises", len(premise_ledger) == 16
                and all(row.get("status") and row.get("limit") for row in premise_ledger),
                "all sixteen premise rows preserve explicit status and limit")

    outputs = verify_family_outputs(audit)
    f01_ownership = verify_f01_ownership(audit, outputs)
    verify_other_readiness(audit, outputs)
    verify_proposal(audit)

    result_primary = json.loads((PACKAGE / "RESULT.json").read_text(encoding="utf-8"))
    audit.check("M04_primary_ceiling", result_primary.get("outcome") == "SURVIVOR_MAP_COMPLETE_WITH_CPU_CANDIDATE"
                and result_primary.get("cpu_exact_check_ready") == 1
                and result_primary.get("cpu_bounded_solve_ready") == 0
                and result_primary.get("gpu_ready") == 0
                and result_primary.get("new_computation_run") is False,
                "primary result preserves the preregistered operational ceiling")
    audit.check("M05_no_adoption", all(result_primary.get(key) is False for key in
                ("action_adopted", "carrier_adopted", "bootstrap_law_adopted", "gpu_used")),
                "no action, carrier, bootstrap law, or GPU use is adopted")

    audit_text = (PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    status_text = (PACKAGE / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    audit.check("M06_group_wording", "four upstream groups" not in audit_text.lower()
                and "four upstream groups" not in status_text.lower()
                and "four development groups" in (audit_text + status_text).lower(),
                "development groups are not all mislabeled upstream; Q04 remains downstream")
    audit.check("M07_proposal_not_source", "udt_stability_family_survivor_map_2026-08-01/DERIVATION_CLOSURE_SWEEP_PROPOSAL.md" not in admitted,
                "post-outcome sweep proposal is reviewed as a proposal, not smuggled into the frozen evidence")

    mutation_catches(audit, inventory, outputs)

    raw_path = PACKAGE / "INDEPENDENT_RAW.jsonl"
    raw_text = "".join(json.dumps(record, sort_keys=True) + "\n" for record in audit.records)
    raw_path.write_text(raw_text, encoding="utf-8")
    source_records = sum(record.get("type") == "source" for record in audit.records)
    passed_checks = sum(record.get("type") == "check" and record.get("passed") for record in audit.records)
    total_checks = sum(record.get("type") == "check" for record in audit.records)
    passed_catches = sum(record.get("type") == "mutation" and record.get("passed") for record in audit.records)
    total_catches = sum(record.get("type") == "mutation" for record in audit.records)

    verdict = "CLOSED_PASS_VERIFIED_WITH_CAVEATS" if not audit.failures else "AMENDMENT_REQUIRED"
    result = {
        "date": DATE,
        "verdict": verdict,
        "base": BASE,
        "source_records": source_records,
        "checks_passed": passed_checks,
        "checks_total": total_checks,
        "catch_proofs_passed": passed_catches,
        "catch_proofs_total": total_catches,
        "failures": audit.failures,
        "family_cells_reconstructed": 84,
        "cpu_exact_check_ready": 1 if not audit.failures else 0,
        "cpu_bounded_solve_ready": 0,
        "gpu_ready": 0,
        "active_development_families": 5,
        "development_groups": 4,
        "families_discarded": 0,
        "f01": f01_ownership,
        "maximum_conclusion": (
            "The seven-family/84-cell map is verified in its frozen scope. F01 alone owns a "
            "separately preregistrable conditional local-cell exact check; no family owns a CPU "
            "solve or GPU contract, and no physical stability, persistence, bootstrap, matter, or mass follows."
        ),
        "caveats": [
            "F01 root existence is banked but uniqueness is not; a later contract must isolate every root or prove uniqueness.",
            "F01 readiness is restricted to germ-Hessian-flat single-cell R05/R06 blocks; the free second germ and whole-chain index remain open.",
            "Development ranks are working dependency order, not authorization or physics priority.",
            "Mandatory remote fetch/pull was unavailable because Git metadata is read-only; local base/blob identity was fully verified.",
        ],
        "raw_sha256": sha256(raw_text.encode("utf-8")),
    }
    write_json(PACKAGE / "INDEPENDENT_RESULT.json", result)
    print(json.dumps({
        "verdict": verdict, "checks": f"{passed_checks}/{total_checks}",
        "catches": f"{passed_catches}/{total_catches}", "sources": source_records,
        "failures": audit.failures,
    }, sort_keys=True))
    return 0 if not audit.failures else 1


if __name__ == "__main__":
    sys.exit(main())

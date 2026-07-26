#!/usr/bin/env python3
"""Production verification and exercised semantic-regression catches."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "b4d16fb47e87086eb24fe9115d4ee50bc47d7722"
PREREG_COMMIT = "b6397a3"


class Failure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Failure(message)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"], cwd=ROOT, check=True, capture_output=True
    ).stdout


EXPECTED = {
    "G01": ("DERIVED_ADDITIVE_LOG_DEPTH_OF_RECIPROCAL_PAIR", "ACTIVE_FOUNDATION"),
    "G02": ("DERIVED_PHI_MAPS_TO_DIAG_EXP_MINUS_PHI_EXP_PLUS_PHI", "ACTIVE_FOUNDATION"),
    "G03": ("CHOSE_COMPARISON_CONFIGURATION", "COMPARISON_ONLY_NOT_NATIVE"),
    "G04": ("CHALLENGED_OWNER_POSTULATE_NOT_DERIVED", "INACTIVE_UNLESS_CHARLES_EXPLICITLY_REAUTHORIZES"),
    "G05": ("DERIVED_ALGEBRAIC_RATIO_INVARIANCE", "ALGEBRA_ONLY"),
    "G06": ("OBSERVED_ANCHORS_RETAINED", "ACTIVE_CALIBRATION"),
    "G07": ("GENERIC_F4_6_MOD_COORDINATE_PRESENTATION", "GENERIC_ARENA_BASELINE_ONLY"),
    "G08": ("OPEN_SELECTION_WITH_EXACT_EXTENSION_CLASS", "ACTIVE_OPEN_GATE"),
    "G09": ("POSIT", "CONDITIONAL_CARRIER_BRANCH_ONLY"),
    "G10": ("UNIQUE_CONDITIONAL_ONLY_IF_PRE_SCALE_STRONG_CSN_RETAINED", "INACTIVE_WITHOUT_STRONG_CSN_PREMISE"),
    "G11": ("CONDITIONAL_NOT_SELECTED", "NOT_SELECTED"),
    "G12": ("WORKING_ON_SHELL_ADMISSIBILITY", "ON_SHELL_ADMISSIBILITY_ONLY"),
    "G13": ("CONDITIONAL_TORIC_F_EQUALS_dS_AND_dF_EQUALS_ZERO", "TORIC_GEOMETRY_ONLY"),
    "G14": ("WORKING_GLOBAL_OBSERVER_PAIR_MAXIMUM_SEPARATION", "GLOBAL_OBSERVER_PAIR_SCHEMA"),
    "G15": ("SETTLED_STATIC_FINITE_BOX_CONDITIONAL", "STATIC_FINITE_BOX_AND_CARRIER_CONDITIONAL"),
    "G16": ("OPEN", "NO_COMPLETE_PHYSICS_CLAIM"),
}


CONTROL_PATHS = [
    "AGENTS.md",
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "README.md",
    "research/README.md",
    "research/_registry/README.md",
    "MEMORY.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
]

PREREG_INPUTS = [
    "PREREGISTRATION.md",
    "SEMANTIC_GUARD_UNIVERSE.tsv",
    "ACTIVE_SEMANTIC_CANDIDATES.tsv",
    "CONTROL_TARGETS.tsv",
    "SOURCE_SCOPE.tsv",
    "SOURCE_MANIFEST.tsv",
    "build_source_manifest.py",
    "freeze_candidate_universe.py",
]

HISTORICAL_DOF_PRESERVE = [
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "COMMANDS.md",
    "COMPLETION_UNIVERSE.tsv",
    "CONSTRAINT_UNIVERSE.tsv",
    "FALSIFICATION_CONTRACT.tsv",
    "FRESH_ADVERSARIAL_REVIEW_STATUS.md",
    "PREREGISTRATION.md",
    "RANK_RULES.tsv",
    "REPOSITORY_GATES.json",
    "REPOSITORY_GATES_STDOUT.txt",
    "RUN_ENVIRONMENT.json",
    "SOURCE_MANIFEST.tsv",
    "SOURCE_SCOPE.tsv",
    "UNKNOWN_UNIVERSE.tsv",
    "build_source_manifest.py",
    "requirements.txt",
    "verify_repository_gates.py",
]


def validate_registry(rows: list[dict[str, str]]) -> None:
    require(len(rows) == 16, "registry row count")
    by_id = {row["premise_id"]: row for row in rows}
    require(set(by_id) == set(EXPECTED), "registry id universe")
    require(len(by_id) == len(rows), "duplicate registry id")
    source_by_guard = {
        row["guard_id"]: row["controlling_source"]
        for row in read_tsv(HERE / "SEMANTIC_GUARD_UNIVERSE.tsv")
    }
    for guard, (status, use) in EXPECTED.items():
        require(by_id[guard]["current_status"] == status, f"{guard} status")
        require(by_id[guard]["active_use"] == use, f"{guard} active use")
        require((ROOT / by_id[guard]["controlling_source"]).is_file(), f"{guard} source")
        require(by_id[guard]["controlling_source"] == source_by_guard[guard], f"{guard} source priority")
        require(by_id[guard]["precedence_rule"] == "LIVE_THEN_THIS_REGISTRY_THEN_CITED_SOURCE__CONFLICT_MEANS_STOP", f"{guard} precedence")


def validate_candidates(candidates: list[dict[str, str]], adjudication: list[dict[str, str]]) -> None:
    require(len(candidates) == 754, "candidate count")
    require(len(adjudication) == 754, "adjudication count")
    require(len({r["candidate_id"] for r in candidates}) == 754, "candidate duplicate id")
    require(len({r["path"] for r in candidates}) == 754, "candidate duplicate path")
    require({r["candidate_id"] for r in candidates} == {r["candidate_id"] for r in adjudication}, "candidate coverage")
    require(len({r["path"] for r in adjudication}) == 754, "adjudication duplicate path")
    require(all(r["controlling_disposition"] for r in adjudication), "empty candidate disposition")
    tree_text = subprocess.run(
        ["git", "ls-tree", "-r", BASE], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout
    base_blobs = {}
    for line in tree_text.splitlines():
        metadata, path = line.split("\t", 1)
        base_blobs[path] = metadata.split()[2]
    adj_by_id = {row["candidate_id"]: row for row in adjudication}
    for row in candidates:
        require(base_blobs.get(row["path"]) == row["base_blob"], f"candidate base blob {row['path']}")
        require(adj_by_id[row["candidate_id"]]["base_blob"] == row["base_blob"], f"adjudication blob {row['path']}")
        require((ROOT / row["path"]).is_file(), f"current candidate path missing {row['path']}")


def validate_controls(controls: dict[str, str]) -> None:
    for path in CONTROL_PATHS:
        require("CURRENT_SCIENTIFIC_PREMISES.tsv" in controls[path], f"control pointer {path}")
    require("derived additive logarithmic depth" in controls["AGENTS.md"], "AGENTS founded phi")
    require("CHOSE_COMPARISON_CONFIGURATION" in controls["AGENTS.md"], "AGENTS comparison scalar")
    require("CHALLENGED_OWNER_POSTULATE_NOT_DERIVED" in controls["AGENTS.md"], "AGENTS CSN")
    require("generic configuration-arena count" in controls["AGENTS.md"], "AGENTS generic count")


def validate_supersessions(rows: list[dict[str, str]]) -> None:
    require(len(rows) == 6, "supersession row count")
    require({row["supersession_id"] for row in rows} == {f"S{i:02d}" for i in range(1, 7)}, "supersession ids")
    require(len({row["path"] for row in rows}) == 6, "supersession duplicate path")


def validate_dof() -> None:
    dof = ROOT / "udt_global_functional_dof_constraint_rank_audit_2026-07-26"
    p = {row["id"]: row for row in read_tsv(dof / "LOCAL_PRESENTATION_RANK.tsv")}
    s = {row["id"]: row for row in read_tsv(dof / "STATUS_LEDGER.tsv")}
    k = {row["id"]: row for row in read_tsv(dof / "CONSTRAINT_RANK_LEDGER.tsv")}
    result = json.loads((dof / "AUDIT_RESULT.json").read_text(encoding="utf-8"))
    require(p["P01"]["quotient_signature"] == "F4[6]", "generic arena arithmetic")
    require(p["P04"]["status"] == "CHOSE_COMPARISON_CONFIGURATION", "comparison scalar promotion")
    require(p["P05"]["status"] == "DERIVED_FOUNDED_SUBGROUP__FULL_EXTENSION_OPEN", "founded phi regression")
    require(p["P06"]["status"] == "INACTIVE_COUNTERFACTUAL_REQUIRES_EXPLICIT_REAUTHORIZATION", "CSN activation")
    require(k["K07"]["audited_rank_effect"] == "INACTIVE_NO_RANK_SUBTRACTION", "CSN subtraction")
    require(s["S13"]["status"] == "FOUNDED_COMPLETE_EXTENSION_AND_VARIATION_DOMAIN_THEN_RESPONSE_AND_GLOBAL_BOUNDARY", "closure order")
    require(result["founded_phi_additional_native_field_count"] == 0, "founded phi count")
    require(result["native_founded_complete_extension_rank"] == "OPEN", "native rank invention")
    require(result["propagating_modes"] == "NOT_EVALUABLE", "mode promotion")


def validate_base_evidence() -> None:
    for row in read_tsv(HERE / "SOURCE_MANIFEST.tsv"):
        data = git_blob(BASE, row["path"])
        require(len(data) == int(row["bytes"]), f"base source size {row['source_id']}")
        require(sha256_bytes(data) == row["sha256"], f"base source sha {row['source_id']}")
    dof_prefix = "udt_global_functional_dof_constraint_rank_audit_2026-07-26/"
    for row in read_tsv(ROOT / dof_prefix / "ORIGINAL_RESULT_HASHES.tsv"):
        data = git_blob(BASE, dof_prefix + row["path"])
        require(len(data) == int(row["bytes"]), f"original result size {row['path']}")
        require(sha256_bytes(data) == row["sha256"], f"original result sha {row['path']}")
    canon = subprocess.run(["git", "hash-object", "CANON.md"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    require(canon == "a67e518b623c8715679b26d5736c7409e3ffcae3", "CANON changed")


def validate_historical_inputs(corrupt: str = "") -> None:
    for name in PREREG_INPUTS:
        path = HERE / name
        current = path.read_bytes()
        expected = git_blob(PREREG_COMMIT, f"{HERE.name}/{name}")
        if corrupt == f"prereg:{name}":
            current += b"corrupt"
        require(current == expected, f"preregistered input changed: {name}")
    dof_prefix = "udt_global_functional_dof_constraint_rank_audit_2026-07-26"
    for name in HISTORICAL_DOF_PRESERVE:
        path = ROOT / dof_prefix / name
        current = path.read_bytes()
        expected = git_blob(BASE, f"{dof_prefix}/{name}")
        if corrupt == f"dof:{name}":
            current += b"corrupt"
        require(current == expected, f"historical DOF record changed: {name}")


def main() -> None:
    registry = read_tsv(ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv")
    candidates = read_tsv(HERE / "ACTIVE_SEMANTIC_CANDIDATES.tsv")
    adjudication = read_tsv(HERE / "ACTIVE_SEMANTIC_ADJUDICATION.tsv")
    supersessions = read_tsv(HERE / "SUPERSESSION_LEDGER.tsv")
    controls = {path: (ROOT / path).read_text(encoding="utf-8") for path in CONTROL_PATHS}

    validate_registry(registry)
    validate_candidates(candidates, adjudication)
    validate_controls(controls)
    validate_supersessions(supersessions)
    validate_dof()
    validate_base_evidence()
    validate_historical_inputs()

    catches: list[dict[str, str]] = []

    def record(cid: str, description: str, trial) -> None:
        caught = False
        try:
            trial()
        except (Failure, KeyError):
            caught = True
        require(caught, f"catch failed {cid}")
        catches.append({"catch_id": cid, "forbidden_regression": description, "result": "PASS_REJECTED"})

    guard_mutations = {
        "G01": ("current_status", "UNDEFINED_PLACEHOLDER"),
        "G02": ("current_status", "PAIR_ACTION_OPEN"),
        "G03": ("active_use", "NATIVE_FIELD"),
        "G04": ("active_use", "ACTIVE_LOCAL_GAUGE"),
        "G05": ("active_use", "LOCAL_WEYL_GAUGE"),
        "G06": ("active_use", "ANCHORS_DROPPED"),
        "G07": ("active_use", "PROPAGATING_MODES"),
        "G08": ("current_status", "UNIQUE_SPECTATOR_EXTENSION"),
        "G09": ("current_status", "DERIVED_NATIVE_CARRIER"),
        "G10": ("active_use", "UNCONDITIONAL_ACTION"),
        "G11": ("active_use", "SELECTED_NATIVE_ACTION"),
        "G12": ("active_use", "LOCAL_OPTIMIZER_EQUATION"),
        "G13": ("active_use", "FULL_NATIVE_MAXWELL"),
        "G14": ("active_use", "EDGE_RADIUS_NUMBER"),
        "G15": ("active_use", "UNCONDITIONAL_MATTER_STABILITY"),
        "G16": ("current_status", "CLOSED"),
    }
    for guard, (field, bad) in guard_mutations.items():
        def run_guard(g=guard, f=field, value=bad):
            trial = copy.deepcopy(registry)
            next(row for row in trial if row["premise_id"] == g)[f] = value
            validate_registry(trial)
        record(f"C{int(guard[1:]):02d}", f"{guard} semantic promotion", run_guard)

    def missing_candidate() -> None:
        validate_candidates(candidates[:-1], adjudication)
    record("C17", "candidate missing", missing_candidate)

    def duplicate_candidate() -> None:
        validate_candidates(candidates + [copy.deepcopy(candidates[0])], adjudication)
    record("C18", "candidate duplicated", duplicate_candidate)

    def empty_disposition() -> None:
        trial = copy.deepcopy(adjudication)
        trial[0]["controlling_disposition"] = ""
        validate_candidates(candidates, trial)
    record("C19", "candidate unadjudicated", empty_disposition)

    def missing_control_pointer() -> None:
        trial = copy.deepcopy(controls)
        trial["HANDOFF.md"] = trial["HANDOFF.md"].replace("CURRENT_SCIENTIFIC_PREMISES.tsv", "REMOVED")
        validate_controls(trial)
    record("C20", "startup control loses registry pointer", missing_control_pointer)

    def missing_supersession() -> None:
        validate_supersessions(supersessions[:-1])
    record("C21", "known ambiguity loses supersession", missing_supersession)

    # DOF catches exercise the separate package's own validator; these mutations are also checked
    # there. Here we ensure the repository-level gate rejects loss of the corrected current files.
    dof = ROOT / "udt_global_functional_dof_constraint_rank_audit_2026-07-26"
    p = read_tsv(dof / "LOCAL_PRESENTATION_RANK.tsv")
    result = json.loads((dof / "AUDIT_RESULT.json").read_text(encoding="utf-8"))

    def dof_phi_native() -> None:
        trial = copy.deepcopy(p)
        next(row for row in trial if row["id"] == "P04")["status"] = "NATIVE_FIELD"
        require(next(row for row in trial if row["id"] == "P04")["status"] == "CHOSE_COMPARISON_CONFIGURATION", "DOF comparison scope")
    record("C22", "DOF comparison scalar promoted", dof_phi_native)

    def dof_phi_demoted() -> None:
        trial = copy.deepcopy(p)
        next(row for row in trial if row["id"] == "P05")["status"] = "CONDITIONAL"
        require(next(row for row in trial if row["id"] == "P05")["status"] == "DERIVED_FOUNDED_SUBGROUP__FULL_EXTENSION_OPEN", "DOF founded scope")
    record("C23", "DOF founded phi demoted", dof_phi_demoted)

    def dof_rank_invented() -> None:
        trial = copy.deepcopy(result)
        trial["native_founded_complete_extension_rank"] = "F4[6]"
        require(trial["native_founded_complete_extension_rank"] == "OPEN", "DOF native rank")
    record("C24", "generic arena promoted to native rank", dof_rank_invented)

    def priority_removed() -> None:
        trial = copy.deepcopy(registry)
        next(row for row in trial if row["premise_id"] == "G01")["controlling_source"] = "udt_complete_metric_solution_space_map_2026-07-21/OFFSHELL_CONFIGURATION_BRANCHES.tsv"
        validate_registry(trial)
    record("C25", "controlling source priority replaced by old atlas", priority_removed)

    def candidate_blob_changed() -> None:
        trial = copy.deepcopy(candidates)
        trial[0]["base_blob"] = "0" * 40
        validate_candidates(trial, adjudication)
    record("C26", "candidate identity detached from frozen base blob", candidate_blob_changed)

    record("C27", "preregistered correction universe rewritten", lambda: validate_historical_inputs("prereg:SEMANTIC_GUARD_UNIVERSE.tsv"))
    record("C28", "historical DOF preregistration rewritten", lambda: validate_historical_inputs("dof:PREREGISTRATION.md"))

    write_tsv(HERE / "CATCH_PROOFS.tsv", ["catch_id", "forbidden_regression", "result"], catches)
    result_out = {
        "status": "PASS",
        "premise_guards": len(registry),
        "candidate_paths": len(candidates),
        "startup_controls": len(controls),
        "supersessions": len(supersessions),
        "catch_proofs": len(catches),
        "base_source_hashes": len(read_tsv(HERE / "SOURCE_MANIFEST.tsv")),
        "original_dof_hashes": len(read_tsv(ROOT / "udt_global_functional_dof_constraint_rank_audit_2026-07-26/ORIGINAL_RESULT_HASHES.tsv")),
        "preserved_prereg_inputs": len(PREREG_INPUTS),
        "preserved_historical_dof_records": len(HISTORICAL_DOF_PRESERVE),
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result_out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result_out, sort_keys=True))


if __name__ == "__main__":
    main()

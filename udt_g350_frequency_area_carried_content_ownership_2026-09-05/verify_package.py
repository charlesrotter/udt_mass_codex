#!/usr/bin/env python3
"""Aggregate, dependency-free, no-write verifier for the G350 package."""

import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LANDING = (
    "LOCAL_CONTINUOUS_FREQUENCY_AREA_MULTIPLICATIVE_TRANSFER_IS_THE_NONUNIQUE_CHARACTER_FAMILY_R_TO_P_A_TO_Q"
    "__OBSERVER_COVARIANCE_TYPES_P_BUT_SELECTS_NO_WEIGHT"
    "__INVERSE_AREA_REQUIRES_A_NEW_CONSERVATION_PREMISE"
    "__NONZERO_SOURCE_CAUSTIC_MEASURE_AND_LABEL_AGGREGATION_REMAIN_SUPPLIED"
    "__NO_LIGHT_FLUX_LUMINOSITY_DISTANCE_HISTORY_SCALE_OR_XMAX_SELECTED"
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package_bytes():
    return {
        path.relative_to(HERE).as_posix(): digest(path)
        for path in HERE.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }


def run_json(script):
    environment = os.environ.copy()
    environment["UDT_NO_WRITE"] = "1"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-B", "-S", script],
        cwd=HERE,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def frozen_hashes_pass():
    rows = (HERE / "FROZEN_PREREGISTRATION_HASHES.tsv").read_text(encoding="utf-8").splitlines()[1:]
    return all(digest(HERE / path) == expected for path, expected in (row.split("\t") for row in rows))


def source_hashes_pass():
    rows = (HERE / "SOURCE_SCOPE.tsv").read_text(encoding="utf-8").splitlines()[1:]
    for row in rows:
        path, expected, _use, status = row.split("\t")
        if status != "READ_ONLY_INPUT":
            continue
        if digest(ROOT / path) != expected:
            return False
    return True


def stdlib_only_pass():
    allowed = {
        "ast", "copy", "fractions", "hashlib", "json", "math", "os", "pathlib", "random",
        "subprocess", "sys",
    }
    for name in (
        "derive_carried_content_ownership.py",
        "verify_carried_content_ownership_independent.py",
        "run_catch_proofs.py",
        "run_semantic_mutation_checks.py",
        "verify_repair_numerics.py",
        "verify_package.py",
    ):
        tree = ast.parse((HERE / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [(node.module or "").split(".")[0]]
            else:
                continue
            if any(module not in allowed for module in modules):
                return False
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in {"__import__", "eval", "exec"}:
                    return False
    return True


def main():
    required = (
        "AUDIT_REPORT.md", "CATCH_PROOF_RESULT.json", "COMMANDS.md", "COMPLETENESS_MAP.md",
        "DERIVATION_RESULT.json", "EVIDENCE_GATES.md", "EXACT_DERIVATION.md",
        "EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md", "EXTERNAL_REPAIR_FOLLOWUP_TRANSMISSION.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md", "EXTERNAL_REVIEW_RESPONSE.md",
        "EXTERNAL_REVIEW_TRANSMISSION.md",
        "FROZEN_PREREGISTRATION_HASHES.tsv", "INDEPENDENT_VERIFICATION.json", "LAY_REPORT.md",
        "MAP.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md",
        "PREREGISTRATION_EXECUTION_NOTE.md", "REPAIR_COMMANDS.md", "REPAIR_EXECUTION_RECORD.md",
        "REPAIR_FOLLOWUP_REQUEST.md", "REPAIR_NUMERICS_RESULT.json", "REPAIR_PREMISE_LEDGER.tsv",
        "REPAIR_PREREGISTRATION.md", "RUN_RECORD.md",
        "SEMANTIC_MUTATION_RESULT.json", "SOURCE_SCOPE.tsv", "STATUS_LEDGER.tsv",
        "derive_carried_content_ownership.py", "run_catch_proofs.py",
        "run_semantic_mutation_checks.py", "verify_carried_content_ownership_independent.py",
        "verify_package.py", "verify_repair_numerics.py",
    )
    before = package_bytes()
    production = run_json("derive_carried_content_ownership.py")
    independent = run_json("verify_carried_content_ownership_independent.py")
    contract = run_json("run_catch_proofs.py")
    semantic = run_json("run_semantic_mutation_checks.py")
    repair_numerics = run_json("verify_repair_numerics.py")
    after = package_bytes()

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    audit = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    premises = (HERE / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    repair_premises = (HERE / "REPAIR_PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    commands = (HERE / "COMMANDS.md").read_text(encoding="utf-8")
    repair_commands = (HERE / "REPAIR_COMMANDS.md").read_text(encoding="utf-8")
    external = (HERE / "EXTERNAL_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    repair_external = (HERE / "EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md").read_text(encoding="utf-8")
    repair_transmission = (HERE / "EXTERNAL_REPAIR_FOLLOWUP_TRANSMISSION.md").read_text(encoding="utf-8")
    adjudication = (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")

    checks = {
        "all_required_files": all((HERE / name).is_file() for name in required),
        "frozen_preregistration_hashes": frozen_hashes_pass(),
        "frozen_source_hashes": source_hashes_pass(),
        "production_120010_of_120010": production.get("all_passed") is True
        and production.get("checks_passed") == production.get("checks_total") == 120010,
        "independent_35295_of_35295": independent.get("all_passed") is True
        and independent.get("checks_passed") == independent.get("checks_total") == 35295,
        "contract_guard_25_of_25": contract.get("all_passed") is True
        and contract.get("mutations_caught") == contract.get("mutations_total") == 25,
        "semantic_mutants_14_of_14": semantic.get("all_passed") is True
        and semantic.get("checks_passed") == semantic.get("checks_total") == 14,
        "repair_numerics_4000_of_4000": repair_numerics.get("all_passed") is True
        and repair_numerics.get("checks_passed") == repair_numerics.get("checks_total") == 4000
        and repair_numerics.get("log_domain_cases") == 2000
        and repair_numerics.get("tolerance") == 2.0e-11,
        "production_result_reproduced": production
        == json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8")),
        "independent_result_reproduced": independent
        == json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")),
        "contract_result_reproduced": contract
        == json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8")),
        "semantic_result_reproduced": semantic
        == json.loads((HERE / "SEMANTIC_MUTATION_RESULT.json").read_text(encoding="utf-8")),
        "repair_numerics_result_reproduced": repair_numerics
        == json.loads((HERE / "REPAIR_NUMERICS_RESULT.json").read_text(encoding="utf-8")),
        "aggregate_replay_changes_no_bytes": before == after,
        "stdlib_only_imports": stdlib_only_pass(),
        "character_family_and_nonuniqueness": "T_{(p,q)}(R,A)=R^pA^q" in exact
        and "primary alternative `B`" in audit,
        "universal_domain_and_realized_subgroup_caveat": "for every pair" in exact
        and "subgroup generated by that subset" in exact,
        "observer_weight_open": "Covariance therefore tells us what transformation type" in exact
        and "scalar-valued component" in exact and "Choosing `p` requires defining" in lay,
        "conservation_is_new_premise": "NEW_PREMISE_CANDIDATE_NOT_ADOPTED" in premises
        and "additional carried-sheet" in audit,
        "source_not_generated": "C_i=0" in exact and "cannot create nonzero content" in lay,
        "endpoint_coboundary_retained": "consistently endpoint-assigned" in exact
        and "positive zero-cochain" in repair_premises,
        "caustic_boundary_retained": "one-sided zero and infinite limits" in exact
        and "simultaneous-zero limit" in exact and "caustic" in premises,
        "labels_not_aggregated": "no physical sum, weight" in exact,
        "bounded_physical_scope": all(
            token in audit for token in ("No radiative content", "observational distance", "`X_max`", "canon")
        ),
        "metric_kernel_unchanged": "metric, reciprocal kernel, angular sector" in audit,
        "registered_no_write_commands": sum(
            "UDT_NO_WRITE=1 python3 -B -S" in line for line in commands.splitlines()
        ) == 4 and sum(
            "UDT_NO_WRITE=1 python3 -B -S" in line for line in repair_commands.splitlines()
        ) == 3,
        "external_accept_with_caveats_retained": external.rstrip().endswith(
            "ACCEPT_WITH_CAVEATS_G350_FREQUENCY_AREA_OWNERSHIP_BOUNDARY"
        ),
        "external_repair_acceptance": repair_external.rstrip().endswith(
            "ACCEPT_G350_R1_R4_REPAIR_FOLLOWUP"
        ) and "no regression" in repair_external,
        "external_repair_provenance": all(
            token in repair_transmission for token in (
                "01a071e9-ea4d-72d2-9f73-170942216110",
                "6b77e0f8aa2cbb1d7d8630ba23e349823a3feb9eba5def7a961c8579acbe5ec7",
                "ACCEPT_G350_R1_R4_REPAIR_FOLLOWUP",
            )
        ),
        "external_adjudication_final": "EXTERNAL_REPAIR_FOLLOWUP_ACCEPTED" in adjudication
        and "EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED_AFTER_PREREGISTERED_R1_R4_REPAIRS" in adjudication,
        "provenance_and_evidence_grades_repaired": "internal byte consistency" in external
        and "DOCUMENTARY_TO_INTAKE_ONLY_REVIEWER" in repair_premises
        and "tautological hard-coded contract" in exact,
        "no_bytecode": not any("__pycache__" in path.parts or path.suffix == ".pyc" for path in HERE.rglob("*")),
        "landing_exact": LANDING in exact.replace("\n", ""),
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    result = {
        "all_passed": not failed,
        "checks": checks,
        "checks_passed": sum(bool(value) for value in checks.values()),
        "checks_total": len(checks),
        "failed": failed,
        "landing": LANDING,
        "review_status": "EXTERNAL_REPAIR_FOLLOWUP_ACCEPTED",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") == "1":
        print(rendered, end="")
    else:
        (HERE / "VERIFICATION_RESULT.json").write_text(rendered, encoding="utf-8")
        print(rendered, end="")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

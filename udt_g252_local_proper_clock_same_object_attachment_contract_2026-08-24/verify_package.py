#!/usr/bin/env python3
"""No-write verifier for the bounded G252 package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
LANDING = (
    "ONE_BLINDED_INDEPENDENT_PROPER_CLOCK_RECORD_ON_ONE_FROZEN_IDENTIFIED_TIMELIKE_SEGMENT_"
    "CONDITIONALLY_FIXES_THE_SINGLE_G249_SCALE"
    "__CE_CONVERTS_THE_ATTACHED_DURATION_TO_LENGTH_WITHOUT_ADDING_A_SCALE_PARAMETER"
    "__A_SECOND_FROZEN_CLOCK_ATTACHMENT_TESTS_THE_SUPPLIED_DIMENSIONLESS_HISTORY_BY_EQUAL_SCALE_RECOVERY"
    "__EVENT_IDENTITY_AND_INDEPENDENT_CALIBRATION_ARE_SUPPLIED_OPERATIONAL_INPUTS_NOT_METRIC_DERIVATIONS"
    "__NO_CLOCK_VALUE_HISTORY_BRANCH_POPULATION_FIT_OUTCOME_OR_NEW_KERNEL_MECHANISM_SELECTED"
)
HOSTILE_KEYS = frozenset({
    "branch_mismatch_rejected",
    "c_E_alone_not_a_scale_equation",
    "control_common_scale",
    "control_recovers_scale",
    "empty_attachment_set_rejected",
    "end_event_mismatch_rejected",
    "inconsistent_second_attachment_rejected",
    "local_anchor_does_not_select_history",
    "missing_calibration_identity_rejected",
    "missing_clock_identity_rejected",
    "negative_clock_duration_rejected",
    "negative_model_duration_rejected",
    "nonindependent_calibration_rejected",
    "observer_mismatch_rejected",
    "per_attachment_scale_proliferation_rejected",
    "same_unit_change_control",
    "self_evaluation_rejected",
    "start_event_mismatch_rejected",
    "zero_clock_duration_rejected",
    "zero_model_duration_rejected",
})


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def source_payload_matches(payload: bytes, expected: str, relative: str) -> bool:
    if sha256_bytes(payload) == expected:
        return True
    if relative != "CURRENT_SCIENTIFIC_PREMISES.tsv":
        return False
    lines = payload.splitlines(keepends=True)
    g252 = [line for line in lines if line.startswith(b"G252\t")]
    stripped = b"".join(line for line in lines if not line.startswith(b"G252\t"))
    return len(g252) == 1 and sha256_bytes(stripped) == expected


def relocated_source_accepts(
    repository_payload: bytes | None,
    sealed_payload: bytes | None,
    expected: str,
) -> bool:
    present = [
        payload
        for payload in (repository_payload, sealed_payload)
        if payload is not None
    ]
    return len(present) == 1 and sha256_bytes(present[0]) == expected


def resolve_source(relative: str, expected: str) -> Path | None:
    candidates = (ROOT / relative, ROOT / "sources" / relative)
    existing = [path for path in candidates if path.is_file()]
    if len(existing) != 1 or not source_payload_matches(existing[0].read_bytes(), expected, relative):
        return None
    return existing[0]


def replay(script: str, *arguments: str) -> dict:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, str(PKG / script), *arguments],
        cwd=ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def hostile_valid(result: dict) -> bool:
    mutations = result.get("mutations", {})
    return (
        result.get("status") == "PASS"
        and result.get("implementation") == "executable_metadata_and_exact_arithmetic_mutations"
        and result.get("caught") == len(HOSTILE_KEYS)
        and result.get("total") == len(HOSTILE_KEYS)
        and result.get("missed") == []
        and frozenset(mutations) == HOSTILE_KEYS
        and all(mutations.values())
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    required = [
        "MAP.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "PREREGISTRATION_COMMIT.md",
        "SOURCE_MANIFEST.tsv", "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "LAY_REPORT.md",
        "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md", "RUN_RECORD.md", "COMMANDS.md",
        "REVIEW_REQUEST.md", "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json", "derive_local_proper_clock_attachment.py",
        "verify_local_proper_clock_attachment_independent.py", "run_catch_proofs.py",
        "verify_package.py", "build_review_intake.py", "EXTERNAL_REVIEW.md",
        "EXTERNAL_REVIEW_RAW.md", "REVIEW_TRANSMISSION_RECORD.md", "REPAIR_PREREGISTRATION.md",
        "REPAIR_PREREGISTRATION_COMMIT.md", "REPAIR_IMPLEMENTATION_RECORD.md",
        "SEALED_REPLAY_RECORD.md", "REPAIR_RESULT.md", "REPAIR_FOLLOWUP_REQUEST.md",
        "REPAIR_FOLLOWUP.md", "REPAIR_FOLLOWUP_RAW.md", "REPAIR_FOLLOWUP_TRANSMISSION_RECORD.md",
        "BANKING_INTEGRATION_PREREGISTRATION.md", "BANKING_INTEGRATION_PREREGISTRATION_ADDENDUM.md",
        "BANKING_INTEGRATION_PREREGISTRATION_SECOND_ADDENDUM.md",
        "BANKING_INTEGRATION_NOTE.md", "BANKING_REPLAY_RECORD.md",
    ]
    missing = [name for name in required if not (PKG / name).is_file()]

    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    source_checks = [
        resolve_source(row["path"], row["sha256"]) is not None
        for row in sources
    ]
    layout_control = b"G252 exact sealed source"
    layout_digest = sha256_bytes(layout_control)
    registry_manifest = next(row for row in sources if row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv")
    registry_path = resolve_source(registry_manifest["path"], registry_manifest["sha256"])
    if registry_path is None:
        raise AssertionError("banked registry source did not resolve")
    registry_payload = registry_path.read_bytes()
    registry_lines = registry_payload.splitlines(keepends=True)
    registry_without_g252 = b"".join(
        line for line in registry_lines if not line.startswith(b"G252\t")
    )
    registry_g252 = [line for line in registry_lines if line.startswith(b"G252\t")]
    registry_historical = registry_without_g252 if registry_g252 else registry_payload
    synthetic_g252 = b"G252\tbanked_registry_compatibility_control\n"
    registry_banked = registry_payload if registry_g252 else registry_historical + synthetic_g252
    registry_with_duplicate_g252 = registry_banked + (
        registry_g252[0] if registry_g252 else synthetic_g252
    )

    saved_production = json.loads((PKG / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    saved_independent = json.loads((PKG / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    saved_catches = json.loads((PKG / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    live_production = replay("derive_local_proper_clock_attachment.py", "--cases", "4096")
    live_independent = replay("verify_local_proper_clock_attachment_independent.py", "--cases", "12000")
    live_catches = replay("run_catch_proofs.py")

    deleted_catches = dict(saved_catches)
    deleted_mutations = dict(saved_catches.get("mutations", {}))
    deleted_mutations.pop("self_evaluation_rejected", None)
    deleted_catches["mutations"] = deleted_mutations
    deleted_catches["caught"] = len(deleted_mutations)
    deleted_catches["total"] = len(deleted_mutations)

    commands = (PKG / "COMMANDS.md").read_text(encoding="utf-8")
    derivation = (PKG / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    ledger = (PKG / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    checks = {
        "required_files": not missing,
        "source_manifest_six_exact": len(sources) == 6 and all(source_checks),
        "sealed_source_missing_rejected": not relocated_source_accepts(None, None, layout_digest),
        "sealed_source_ambiguity_rejected": not relocated_source_accepts(layout_control, layout_control, layout_digest),
        "sealed_source_hash_mismatch_rejected": not relocated_source_accepts(None, b"mutated", layout_digest),
        "sealed_source_repository_layout_control": relocated_source_accepts(layout_control, None, layout_digest),
        "sealed_source_relocated_layout_control": relocated_source_accepts(None, layout_control, layout_digest),
        "banked_registry_single_g252_accepted": source_payload_matches(
            registry_banked, registry_manifest["sha256"], registry_manifest["path"]
        ),
        "banked_registry_historical_bytes_exact": sha256_bytes(registry_historical) == registry_manifest["sha256"],
        "banked_registry_duplicate_g252_rejected": not source_payload_matches(
            registry_with_duplicate_g252, registry_manifest["sha256"], registry_manifest["path"]
        ),
        "banked_registry_other_mutation_rejected": not source_payload_matches(
            registry_banked + b"mutation\n", registry_manifest["sha256"], registry_manifest["path"]
        ),
        "production_saved_pass": saved_production.get("status") == "PASS",
        "independent_saved_pass": saved_independent.get("status") == "PASS",
        "catch_saved_pass": hostile_valid(saved_catches),
        "production_landing": saved_production.get("landing") == LANDING,
        "independent_landing": saved_independent.get("expected_landing") == LANDING,
        "production_replay_exact": live_production == saved_production,
        "independent_replay_exact": live_independent == saved_independent,
        "catch_replay_exact": live_catches == saved_catches,
        "production_case_floor": saved_production.get("sampled", {}).get("cases", 0) >= 4096,
        "independent_case_floor": saved_independent.get("cases", 0) >= 12000,
        "independent_implementation": saved_independent.get("implementation") == "standard_library_fraction_no_production_import_or_output_read",
        "inconsistent_second_anchor_floor": saved_independent.get("inconsistent_second_attachments_rejected") == saved_independent.get("cases"),
        "hostile_deleted_entry_rejected": not hostile_valid(deleted_catches),
        "attachment_status_explicit": "SUPPLIED-EMPIRICAL-CONTRACT" in ledger,
        "kernel_nonmodification_explicit": "does not add scaffolding to the kernel" in derivation,
        "outcomes_unused": saved_production.get("observational_values_used") == 0 and saved_independent.get("observational_values_used") == 0,
        "zero_fitted_coefficients": saved_production.get("fitted_coefficients") == 0 and saved_independent.get("fitted_coefficients") == 0,
        "no_new_kernel_mechanism": saved_production.get("new_kernel_mechanisms") == 0,
        "history_not_selected": saved_production.get("history_selected") is False and saved_independent.get("history_selected") is False,
        "external_repair_accepted": (PKG / "REPAIR_FOLLOWUP_RAW.md").read_text(encoding="utf-8").startswith("REPAIRS_ACCEPTED"),
        "sealed_and_repository_commands_separated": (
            "## Sealed-intake replays" in commands
            and "## Repository-only gate" in commands
            and commands.index("## Repository-only gate") < commands.index("python3 verify_current_scientific_premises.py")
        ),
    }
    failed = [name for name, value in checks.items() if not value]
    result = {"checks": checks, "failed": failed, "status": "PASS" if not failed else "FAIL"}
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

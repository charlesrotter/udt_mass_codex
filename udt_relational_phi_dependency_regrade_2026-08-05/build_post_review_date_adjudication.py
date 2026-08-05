#!/usr/bin/env python3
"""Freeze and render the individual audit of rows selected by the old date-only F18 rule."""

from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "DATE_RULE_ADJUDICATION.tsv"
SUMMARY = HERE / "DATE_RULE_ADJUDICATION_SUMMARY.json"
OLD_LEDGER_COMMIT = "b9497e3cf4c0b706db835c5edf7af17846838082"
OLD_LEDGER_SHA256 = "b77eea4240b7e3ab97ba97c5dbadfbfa10f5c1803785eb8790545050aedaf651"
CURRENT = {
    "UDT_NATIVE_ACTION_COLD_PACKET.md": "CURRENT_C1_FOUNDATION",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md": "CURRENT_RECIPROCAL_CHARACTER_SOURCE",
    "verify_udt_reciprocal_c_postulate.py": "CURRENT_RECIPROCAL_CHARACTER_VERIFIER",
}


def read(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def read_old_ledger() -> list[dict[str, str]]:
    """Read the preregistered pre-mutation ledger, never the corrected output."""
    relative = f"{HERE.name}/ACTIVE_REGRADING_LEDGER.tsv"
    payload = subprocess.check_output(
        ["git", "show", f"{OLD_LEDGER_COMMIT}:{relative}"], cwd=ROOT
    )
    assert hashlib.sha256(payload).hexdigest() == OLD_LEDGER_SHA256
    return list(csv.DictReader(io.StringIO(payload.decode("utf-8")), delimiter="\t"))


def retained_family(path: str) -> tuple[str, str]:
    if path.startswith("legacy/root_oneoffs_2026-07-01/"):
        return "LEGACY_ROOT_ONEOFF", "Archived root one-off; no current control cites it as affirmative authority."
    if path.startswith("native_action_sync_audit_2026-07-17/"):
        return "SYNC_TRANSCRIPT", "Synchronization transcript; final frozen adjudication supersedes it as current verdict."
    if path.startswith("grok/quarantine_free_DA/"):
        return "QUARANTINED_EXPLORATION", "Quarantined early field-equation exploration; no current affirmative authority."
    if path.startswith("scratchpad/"):
        return "SCRATCHPAD", "Scratch calculation; no current affirmative authority."
    if path.startswith("tests/"):
        return "RUNTIME_TEST_OF_SUPERSEDED_BRANCH", "Runtime test remains executable, but its tested field/action branch is not current native authority."
    if path == "research/_registry/MIGRATION_READINESS.tsv":
        return "FIXED_REORGANIZATION_SNAPSHOT", "Fixed navigation snapshot; incidental semantic exposure only."
    if "/" in path:
        return "EARLY_BOUNDED_AUDIT", "Early bounded audit/comparison family not named as a current controlling physics source."
    return "EARLY_ROOT_FIELD_ACTION_CORPUS", "Individually enumerated early root solver/design/result; not a current controlling source and gated at reuse."


def main() -> None:
    ledger = read_old_ledger()
    source = {row["path"]: row for row in read("ACTIVE_REGRADE_UNIVERSE.tsv")}
    selected = [row for row in ledger if row["family_id"] == "F18_EARLY_POSTJULY_FIELD_SOLVER"]
    assert len(selected) == 254
    output = []
    for row in selected:
        path = row["path"]
        if path in CURRENT:
            family, reason = CURRENT[path], (
                "Named in the present founding/action source chain; exact algebra remains current only with the relational supplied-depth and open-law overlay."
            )
            disposition = "CONDITIONAL_REINTERPRETATION_ONLY"
        else:
            family, reason = retained_family(path)
            disposition = "HISTORICAL_SUPERSEDED_NO_ACTION"
        output.append({
            "path": path,
            "source_sha256": row["source_sha256"],
            "first_date": row["first_date"],
            "current_frontier": row["current_frontier"],
            "founding_source": source[path]["founding_source"],
            "old_rule": row["family_id"],
            "old_disposition": row["disposition"],
            "adjudicated_family": family,
            "corrected_disposition": disposition,
            "reason": reason,
        })
    fields = list(output[0])
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", lineterminator="\n", fieldnames=fields)
        writer.writeheader()
        writer.writerows(output)
    identity = hashlib.sha256(("\n".join(row["path"] for row in output) + "\n").encode()).hexdigest()
    summary = {
        "schema": "udt.relational_phi_regrade.date_rule_adjudication.v1",
        "rows": len(output),
        "current_foundation_conditional": sum(row["corrected_disposition"] == "CONDITIONAL_REINTERPRETATION_ONLY" for row in output),
        "historical_retained": sum(row["corrected_disposition"] == "HISTORICAL_SUPERSEDED_NO_ACTION" for row in output),
        "identity_sha256": identity,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""No-write G251 package verifier."""

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
    "CURRENT_METRIC_CHAIN_OWNS_EVALUATORS_AND_SUPPLIED_GEOMETRIC_OBJECT_TYPES"
    "__NO_REGISTERED_CLASS_OWNS_AN_INDEPENDENT_SAME_OBJECT_ABSOLUTE_DATUM"
    "__METRIC_SELF_EVALUATION_IS_CIRCULAR_AND_CANNOT_BREAK_THE_G249_HOMOTHETY"
    "__DIRECT_CLOCK_JACOBI_AREA_VOLUME_AND_CURVATURE_ANCHORS_REQUIRE_ONE_SUPPLIED_OPERATIONAL_ATTACHMENT"
    "__MASS_DENSITY_ENERGY_COMPOSITES_REQUIRE_AN_ADDITIONAL_MATTER_OR_INSTRUMENT_LAW"
    "__NO_ANCHOR_VALUE_HISTORY_BRANCH_POPULATION_FIT_OR_OUTCOME_SELECTED"
)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def source_matches(path: Path, expected: str, relative: str) -> bool:
    payload = path.read_bytes()
    if sha256_bytes(payload) == expected:
        return True
    if relative != "CURRENT_SCIENTIFIC_PREMISES.tsv":
        return False
    lines = payload.splitlines(keepends=True)
    g251 = [line for line in lines if line.startswith(b"G251\t")]
    stripped = b"".join(line for line in lines if not line.startswith(b"G251\t"))
    return len(g251) == 1 and sha256_bytes(stripped) == expected


def resolve_source(relative: str, expected: str) -> Path | None:
    existing = [path for path in (ROOT / relative, ROOT / "sources" / relative) if path.is_file()]
    if len(existing) != 1 or not source_matches(existing[0], expected, relative):
        return None
    return existing[0]


def replay(script: str, *arguments: str) -> dict:
    process = subprocess.run(
        [sys.executable, str(PKG / script), *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    return json.loads(process.stdout)


def hostile_valid(result: dict) -> bool:
    return (
        result.get("status") == "PASS"
        and result.get("caught") == result.get("total") == 26
        and not result.get("missed")
        and len(result.get("mutations", {})) == 26
        and all(result.get("mutations", {}).values())
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    required = (
        "ATTACHMENT_OWNERSHIP.tsv", "AUDIT_REPORT.md", "CATCH_PROOF_RESULT.json", "COMMANDS.md",
        "DERIVATION_RESULT.json", "EVIDENCE_GATES.md", "EXACT_DERIVATION.md", "INDEPENDENT_VERIFICATION.json",
        "EXTERNAL_REVIEW_RAW.md", "LAY_REPORT.md", "MAP.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md",
        "REPAIR_IMPLEMENTATION_RECORD.md", "REPAIR_PREREGISTRATION.md", "REVIEW_TRANSMISSION_RECORD.md",
        "RUN_RECORD.md", "SEALED_PREMISE_REGISTRY_RESULT.json",
        "SOURCE_MANIFEST.tsv", "STATUS_LEDGER.tsv", "derive_attachment_ownership.py",
        "run_catch_proofs.py", "verify_attachment_ownership_independent.py", "verify_package.py",
        "verify_sealed_premise_registry.py",
    )
    missing = [name for name in required if not (PKG / name).is_file()]
    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    source_ok = [resolve_source(row["path"], row["sha256"]) is not None for row in sources]
    with (PKG / "ATTACHMENT_OWNERSHIP.tsv").open(newline="", encoding="utf-8") as stream:
        ledger = list(csv.DictReader(stream, delimiter="\t"))

    saved_production = json.loads((PKG / "DERIVATION_RESULT.json").read_text())
    saved_independent = json.loads((PKG / "INDEPENDENT_VERIFICATION.json").read_text())
    saved_catches = json.loads((PKG / "CATCH_PROOF_RESULT.json").read_text())
    saved_premises = json.loads((PKG / "SEALED_PREMISE_REGISTRY_RESULT.json").read_text())
    live_production = replay("derive_attachment_ownership.py", "--cases", "4096")
    live_independent = replay("verify_attachment_ownership_independent.py", "--cases", "12000")
    live_catches = replay("run_catch_proofs.py")
    live_premises = replay("verify_sealed_premise_registry.py")

    deleted = dict(saved_catches)
    deleted_mutations = dict(saved_catches.get("mutations", {}))
    deleted_mutations.pop("same_object_identity_erasure_rejected", None)
    deleted["mutations"] = deleted_mutations
    deleted["caught"] = len(deleted_mutations)
    deleted["total"] = len(deleted_mutations)

    classifications = [row["classification"] for row in ledger]
    source_by_name = {row["path"]: resolve_source(row["path"], row["sha256"]) for row in sources}
    cited_cells_valid = True
    expected_leg_fields = {
        field for leg in "EICW"
        for field in (leg, f"{leg}_source", f"{leg}_locator", f"{leg}_evidence")
    }
    for row in ledger:
        if not expected_leg_fields.issubset(row):
            cited_cells_valid = False
            break
        for leg in "EICW":
            source = source_by_name.get(row[f"{leg}_source"])
            locator = row[f"{leg}_locator"].replace("\\n", "\n")
            if source is None or not locator or locator not in source.read_text(encoding="utf-8") or not row[f"{leg}_evidence"]:
                cited_cells_valid = False
                break
    ledger_sha256 = sha256_bytes((PKG / "ATTACHMENT_OWNERSHIP.tsv").read_bytes())
    checks = {
        "required_files": not missing,
        "source_manifest_twelve_exact": len(sources) == 12 and all(source_ok),
        "production_saved_pass": saved_production.get("status") == "PASS",
        "independent_saved_pass": saved_independent.get("status") == "PASS",
        "catch_saved_pass": hostile_valid(saved_catches),
        "sealed_premise_saved_pass": saved_premises.get("status") == "PASS",
        "production_landing": saved_production.get("landing") == LANDING,
        "independent_landing": saved_independent.get("expected_landing") == LANDING,
        "production_replay_exact": live_production == saved_production,
        "independent_replay_exact": live_independent == saved_independent,
        "catch_replay_exact": live_catches == saved_catches,
        "sealed_premise_replay_exact": live_premises == saved_premises,
        "candidate_count_eighteen": len(ledger) == saved_production.get("candidate_count") == 18,
        "direct_count_seven": classifications.count("DIRECT_OBSERVATIONAL_ATTACHMENT_MUST_BE_SUPPLIED") == 7,
        "composite_count_three": classifications.count("MATTER_OR_INSTRUMENT_LAW_REQUIRED") == 3,
        "native_owner_count_zero": not any(row["native_attachment_owned"] == "True" for row in ledger),
        "explicit_cited_E_I_C_W": cited_cells_valid,
        "independent_ledger_digest_match": saved_independent.get("expected_ledger_sha256") == ledger_sha256,
        "owned_metric_evaluator_count_ten": sum(row["E"] == "True" for row in ledger) == 10,
        "realized_W_count_zero": not any(row["W"] == "True" for row in ledger),
        "production_case_floor": saved_production.get("sampled", {}).get("cases") == 4096,
        "independent_case_floor": saved_independent.get("cases") == 12000,
        "independent_route": saved_independent.get("implementation") == "independent_standard_library_manifest_source_and_fraction_route_no_production_import_or_output_read",
        "hostile_deleted_entry_rejected": not hostile_valid(deleted),
        "outcomes_unused": saved_production.get("observational_values_used") == saved_independent.get("observational_values_used") == 0,
        "zero_fitted_coefficients": saved_production.get("fitted_coefficients") == saved_independent.get("fitted_coefficients") == 0,
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

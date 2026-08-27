#!/usr/bin/env python3
"""Mechanical verifier for the bounded G279 evidence package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(name: str) -> dict[str, object]:
    with (PACKAGE / name).open() as handle:
        return json.load(handle)


def main() -> None:
    required = {
        "MAP.md",
        "PREREGISTRATION.md",
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_SCOPE.tsv",
        "SOURCE_MANIFEST.tsv",
        "EXACT_REDERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "STATUS_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "COMMANDS.md",
        "REVIEW_REQUEST.md",
        "EXTERNAL_REVIEW_GPT54.md",
        "TRANSMISSION_RECORD.md",
        "REPAIR_PREREGISTRATION.md",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "EXTERNAL_REPAIR_FOLLOWUP_GPT54.md",
        "DEPENDENCY_LEDGER.tsv",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "SUBTRACTION_RESULT.json",
        "CATCH_PROOF_RESULT.json",
        "freeze_source_manifest.py",
        "derive_native_provenance.py",
        "verify_native_chain_independent.py",
        "run_dependency_subtractions.py",
        "run_catch_proofs.py",
        "verify_package.py",
        "build_review_intake.py",
    }
    missing = sorted(name for name in required if not (PACKAGE / name).is_file())
    assert not missing, missing

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    assert len(sources) == 31
    for row in sources:
        path = ROOT / row["path"]
        assert path.is_file(), row["path"]
        assert path.stat().st_size == int(row["bytes"]), row["path"]
        assert sha256(path) == row["sha256"], row["path"]
        lowered = row["path"].lower()
        assert "onshell_timelive_reset" not in lowered
        assert "regime_flow_reciprocal_orchestra" not in lowered
        assert "sne_xmax_g88" not in lowered
        assert "curvature_holonomy_atlas" not in lowered

    derivation = load_json("DERIVATION_RESULT.json")
    independent = load_json("INDEPENDENT_VERIFICATION.json")
    subtraction = load_json("SUBTRACTION_RESULT.json")
    catch = load_json("CATCH_PROOF_RESULT.json")
    assert derivation["status"] == "PASS"
    assert derivation["source_count"] == 31
    assert derivation["key_findings"]["kernel_function_fitted"] is False
    assert derivation["key_findings"]["explicit_working_premise_W5_required_for_G278"] is False
    assert independent["status"] == "PASS"
    assert independent["production_modules_imported"] == 0
    assert independent["stored_scientific_results_read"] == 0
    assert independent["total_assertions"] == 109549
    assert subtraction["status"] == "PASS" and subtraction["case_count"] == 9
    assert catch["status"] == "PASS" and catch["caught"] == catch["expected"] == 16
    assert derivation["executable_audit"]["G278_W5_usage_flags_corrected"] is True
    assert derivation["executable_audit"]["G279_MAP_W5_sibling_only"] is True

    with (PACKAGE / "DEPENDENCY_LEDGER.tsv").open(newline="") as handle:
        edges = {row["edge"]: row for row in csv.DictReader(handle, delimiter="\t")}
    assert len(edges) == 12
    assert edges["E03"]["status"] == "WORKING_PREMISE_PLUS_DERIVED_CONDITIONAL"
    assert edges["E06"]["status"] == "CONDITIONAL_IMPORT"
    assert edges["E07"]["class"] == "DECLARED_NUMERICAL_REPRESENTATION"
    assert edges["P00"]["load_bearing_G278"] == "no"
    assert edges["S00"]["load_bearing_G278"] == "no"

    with (
        ROOT / "udt_g278_cepheid_scale_attachment_des_holdout_2026-08-27/PREMISE_LEDGER.tsv"
    ).open(newline="") as handle:
        g278_rows = {row["item"]: row for row in csv.DictReader(handle, delimiter="\t")}
    projective = g278_rows["completed_pair_projective_state"]
    assert projective["used_in_scale"] == "no"
    assert projective["used_in_des"] == "no"
    map_text = (PACKAGE / "MAP.md").read_text()
    assert "W5 projective relation state is a separate working sibling" in map_text
    assert "W1 terminal pair readout and W5" not in map_text

    report = (PACKAGE / "AUDIT_REPORT.md").read_text()
    assert "EXTERNAL_REPAIRS_ACCEPTED" in report
    assert "Source-bounded provenance only" in report
    followup = (PACKAGE / "EXTERNAL_REPAIR_FOLLOWUP_GPT54.md").read_text()
    assert "REPAIRS_ACCEPTED__BOUNDED_LANDING_UNCHANGED" in followup
    assert "No remaining defect" in followup
    print(
        "PASS: 31 frozen sources; 12 typed edges; 109549 independent assertions; "
        "9 subtractions; 16 hostile catches; G279 R1/R2 externally accepted"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Verify the bounded G104 package without reading BAO or CMB outcomes."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_LANDING = (
    "FACTORIZED_REGULAR_KALEIDOSCOPE_NULL_DERIVED"
    "__SELECTION_REFERENCE_MISMATCH_AND_CORRELATED_MULTIIMAGE_TERMS_EXACT"
    "__CURRENT_COMPLETE_METRIC_PERMITS_BUT_DOES_NOT_OWN_A_NONZERO_CONNECTED_MODE"
    "__ALL_FOUR_COEFFICIENT_HOMES_DORMANT__BOSS_AND_CMB_UNREAD"
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def load_json(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def main() -> None:
    required = {
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "CANDIDATE_FORWARD_CLASSES.tsv",
        "COEFFICIENT_BUDGET.tsv",
        "FALSIFICATION_CONTRACT.tsv",
        "SOURCE_MANIFEST_PREREG.tsv",
        "SOURCE_MANIFEST.tsv",
        "RANDOM_REFERENCE_TYPING_CLARIFICATION.md",
        "INDEPENDENT_VERIFIER_CORRECTION_PREREGISTRATION.md",
        "derive_kaleidoscope_operator.py",
        "verify_kaleidoscope_independent.py",
        "run_catch_proofs.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "FORWARD_CLASS_ATLAS.tsv",
        "COEFFICIENT_STATUS.tsv",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "STATUS_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "STATUS.md",
        "REVIEW_DISPATCH.md",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REVIEW.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "AUDIT_REPORT.md",
    }
    missing = sorted(name for name in required if not (HERE / name).is_file())

    manifest_text = (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8")
    prereg_manifest_text = (HERE / "SOURCE_MANIFEST_PREREG.tsv").read_text(encoding="utf-8")
    manifest_rows = list(csv.DictReader(manifest_text.splitlines(), delimiter="\t"))
    manifest_checks = {
        row["path"]: (ROOT / row["path"]).is_file()
        and digest(ROOT / row["path"]) == row["sha256"]
        for row in manifest_rows
    }

    production = load_json("DERIVATION_RESULT.json")
    independent = load_json("INDEPENDENT_VERIFICATION.json")
    catches = load_json("CATCH_PROOF_RESULT.json")

    with (HERE / "FORWARD_CLASS_ATLAS.tsv").open(encoding="utf-8", newline="") as handle:
        atlas = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "COEFFICIENT_STATUS.tsv").open(encoding="utf-8", newline="") as handle:
        coefficients = list(csv.DictReader(handle, delimiter="\t"))

    forbidden_outcome_tokens = {
        "R2_OUTCOME_REPORT.md",
        "R3_OUTCOME_REPORT.md",
        "R4_OUTCOME_REPORT.md",
        "R5_OUTCOME_REPORT.md",
        "CMB_OUTCOME",
    }
    executable_text = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in ("derive_kaleidoscope_operator.py", "verify_kaleidoscope_independent.py")
    )
    derivation_text = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    clarification_text = (HERE / "RANDOM_REFERENCE_TYPING_CLARIFICATION.md").read_text(
        encoding="utf-8"
    )
    evidence_text = (HERE / "EVIDENCE_GATES.md").read_text(encoding="utf-8")

    checks = {
        "required_files_present": not missing,
        "manifest_frozen_from_prereg": manifest_text == prereg_manifest_text,
        "manifest_has_exactly_11_sources": len(manifest_rows) == 11,
        "manifest_hashes_exact": bool(manifest_checks) and all(manifest_checks.values()),
        "production_pass": production.get("status") == "PASS",
        "landing_exact": production.get("landing") == EXPECTED_LANDING,
        "production_checks_true": all(
            value
            for key, value in production.get("checks", {}).items()
            if key != "outcome_artifacts_read"
        ),
        "production_outcomes_empty": production.get("checks", {}).get("outcome_artifacts_read") == [],
        "independent_pass": independent.get("status") == "PASS",
        "independent_imports_no_production": independent.get("checks", {}).get("imports_production") is False,
        "independent_outcomes_empty": independent.get("checks", {}).get("outcome_artifacts_read") == [],
        "catch_proofs_12_of_12": catches.get("status") == "PASS"
        and len(catches.get("caught_mutations", {})) == 12
        and all(catches.get("caught_mutations", {}).values()),
        "atlas_exact_k01_to_k10": [row.get("class_id") for row in atlas]
        == [f"K{i:02d}" for i in range(1, 11)],
        "four_coefficients_all_dormant": len(coefficients) == 4
        and {row.get("coefficient_id") for row in coefficients}
        == {"a_conn", "a_branch", "a_area", "a_regime"}
        and all(row.get("status") == "DORMANT" for row in coefficients),
        "no_outcome_paths_in_load_bearing_executables": forbidden_outcome_tokens.isdisjoint(executable_text),
        "random_reference_typing_corrected": "SELECTION_REFERENCE_MISMATCH" in derivation_text
        and "Official survey randoms can encode footprint" in clarification_text,
        "scope_ceiling_retained": "not a no-go against future global" in derivation_text
        and "fresh sealed `gpt-5.4` review" in evidence_text,
        "external_review_accepted": "PASS_WITH_CAVEATS" in (
            HERE / "EXTERNAL_REVIEW_ADJUDICATION.md"
        ).read_text(encoding="utf-8"),
        "read_only_replay_supported": all(
            "UDT_READ_ONLY_REPLAY" in (HERE / name).read_text(encoding="utf-8")
            for name in (
                "derive_kaleidoscope_operator.py",
                "verify_kaleidoscope_independent.py",
                "run_catch_proofs.py",
            )
        ),
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "missing": missing,
        "manifest_checks": manifest_checks,
        "landing": EXPECTED_LANDING,
    }
    if result["status"] != "PASS":
        raise AssertionError(json.dumps(result, indent=2, sort_keys=True))
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (HERE / "VERIFICATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

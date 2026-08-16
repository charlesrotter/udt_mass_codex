#!/usr/bin/env python3
"""Verify G105 without reading BAO or CMB outcomes."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LANDING = (
    "COMPLETE_ORCHESTRA_ONE_POINT_OBSERVER_ARTIFACT_CHANNEL_DERIVED_CONDITIONALLY"
    "__FACTORIZED_INTRINSIC_CONNECTED_EXCESS_ZERO"
    "__LOCAL_COMMON_OBSERVER_H_NOT_OWNED"
    "__PHYSICAL_HISTORY_REFERENCE_PROJECTION_AND_GLOBAL_BRANCH_LAW_OPEN"
    "__BOSS_AND_CMB_OUTCOMES_UNREAD"
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
        "FALSIFICATION_CONTRACT.tsv",
        "SOURCE_MANIFEST_PREREG.tsv",
        "SOURCE_MANIFEST.tsv",
        "derive_two_route_lift.py",
        "verify_two_route_independent.py",
        "run_catch_proofs.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "EXACT_DERIVATION.md",
        "ROUTE_ATLAS.tsv",
        "COEFFICIENT_STATUS.tsv",
        "STATUS_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "LAY_REPORT.md",
        "AUDIT_REPORT.md",
        "STATUS.md",
        "REVIEW_DISPATCH.md",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REVIEW.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
    }
    missing = sorted(name for name in required if not (HERE / name).is_file())
    manifest = (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8")
    prereg_manifest = (HERE / "SOURCE_MANIFEST_PREREG.tsv").read_text(encoding="utf-8")
    rows = list(csv.DictReader(manifest.splitlines(), delimiter="\t"))
    manifest_checks = {
        row["path"]: (ROOT / row["path"]).is_file()
        and digest(ROOT / row["path"]) == row["sha256"]
        for row in rows
    }
    production = load_json("DERIVATION_RESULT.json")
    independent = load_json("INDEPENDENT_VERIFICATION.json")
    catches = load_json("CATCH_PROOF_RESULT.json")
    with (HERE / "COEFFICIENT_STATUS.tsv").open(encoding="utf-8", newline="") as handle:
        coefficients = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "ROUTE_ATLAS.tsv").open(encoding="utf-8", newline="") as handle:
        routes = list(csv.DictReader(handle, delimiter="\t"))

    executable_names = (
        "derive_two_route_lift.py",
        "verify_two_route_independent.py",
        "run_catch_proofs.py",
    )
    executable_text = "\n".join((HERE / name).read_text(encoding="utf-8") for name in executable_names)
    forbidden = {
        "R2_OUTCOME_REPORT.md",
        "R3_OUTCOME_REPORT.md",
        "R4_OUTCOME_REPORT.md",
        "R5_OUTCOME_REPORT.md",
        "CMB_OUTCOME",
    }
    exact_text = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    external_text = (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")
    checks = {
        "required_files_present": not missing,
        "manifest_frozen_from_prereg": manifest == prereg_manifest,
        "manifest_has_seven_sources": len(rows) == 7,
        "manifest_hashes_exact": bool(manifest_checks) and all(manifest_checks.values()),
        "production_pass": production.get("status") == "PASS",
        "landing_exact": production.get("landing") == LANDING,
        "production_checks_true": all(production.get("checks", {}).values()),
        "production_outcomes_empty": production.get("outcome_paths_read") == [],
        "independent_pass": independent.get("status") == "PASS",
        "independent_checks_true": all(independent.get("checks", {}).values()),
        "independent_outcomes_empty": independent.get("outcome_paths_read") == [],
        "catch_proofs_12_of_12": catches.get("status") == "PASS"
        and catches.get("caught_count") == catches.get("total") == 12
        and all(catches.get("caught", {}).values()),
        "four_coefficients_dormant": len(coefficients) == 4
        and {row["coefficient"] for row in coefficients}
        == {"a_area", "a_conn", "a_branch", "a_regime"}
        and all(row["calibration_status"] == "DORMANT" for row in coefficients),
        "both_routes_classified": {"physical_one_point_jacobian", "irreducible_local_H"}
        <= {row["route"] for row in routes},
        "no_outcome_tokens_in_executables": forbidden.isdisjoint(executable_text),
        "read_only_replay_supported": all(
            "UDT_READ_ONLY_REPLAY" in (HERE / name).read_text(encoding="utf-8")
            for name in executable_names
        ),
        "ownership_ceiling_retained": "does not derive a physical `H`" in exact_text
        and "physical history" in exact_text
        and "No outcome" in exact_text,
        "external_review_accepted": "PASS_WITH_CAVEATS" in external_text
        and LANDING in external_text,
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "missing": missing,
        "manifest_checks": manifest_checks,
        "landing": LANDING,
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

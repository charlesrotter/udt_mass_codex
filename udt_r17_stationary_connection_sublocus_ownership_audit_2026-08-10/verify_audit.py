#!/usr/bin/env python3
"""Fail-closed package verifier for the R17 stationary sublocus audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "64b5319c1115589928317008548224600881b252"
PREREG = "d2ca6c7c"
PREREG_FILES = (
    "PREREGISTRATION.md",
    "PREMISE_LEDGER.tsv",
    "FALSIFICATION_CONTRACT.tsv",
    "SOURCE_SCOPE.tsv",
    "SOURCE_MANIFEST.tsv",
    "COMPLETENESS_MAP.md",
)


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git(*args: str) -> bytes:
    return subprocess.check_output(("git", *args), cwd=ROOT)


def validate() -> dict[str, bool]:
    checks: dict[str, bool] = {}
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    census_result = json.loads((HERE / "R17_OWNERSHIP_CENSUS_RESULT.json").read_text(encoding="utf-8"))
    flat = rows("FLAT_SUBLOCUS_ATLAS.tsv")
    descent = rows("DESCENT_ATLAS.tsv")
    holonomy = rows("HOLONOMY_ATLAS.tsv")
    ownership = rows("R17_OWNERSHIP_ADJUDICATION.tsv")
    census = rows("R17_TRACKED_REFERENCE_CENSUS.tsv")

    checks["preregistration_commit_parent"] = git("rev-parse", f"{PREREG}^").decode().strip() == BASE
    checks["preregistered_files_unchanged"] = all(
        (HERE / name).read_bytes() == git("show", f"{PREREG}:{HERE.name}/{name}")
        for name in PREREG_FILES
    )

    manifest_ok = True
    for row in rows("SOURCE_MANIFEST.tsv"):
        raw = git("show", row["source_ref"])
        manifest_ok &= git("rev-parse", row["source_ref"]).decode().strip() == row["git_blob"]
        manifest_ok &= hashlib.sha256(raw).hexdigest() == row["sha256"]
        manifest_ok &= len(raw) == int(row["size"])
    checks["source_manifest_16_exact"] = manifest_ok and len(rows("SOURCE_MANIFEST.tsv")) == 16

    checks["six_flat_rows"] = [row["lambda"] for row in flat] == ["-2", "-1", "0", "1/2", "1", "2"]
    checks["flat_root_counts"] = [row["regular_root_count_at_a_1_over_64"] for row in flat] == ["1", "1", "1", "1", "0", "2"]
    checks["all_witnesses_nonflat"] = all(
        row["C01_C06_witness"] == "NONCONSTANT_NOT_FLAT_FULL_SO2" for row in flat
    )
    checks["descent_covers_six_plus_controls"] = len(descent) == 8
    checks["global_horizontality_constant"] = all(
        "IFF_PHI_CONSTANT" in row["global_curvature_horizontal_on_RxS3"]
        for row in descent[:6]
    )
    checks["lambda_one_no_abstract_descent"] = next(
        row for row in descent if row["lambda"] == "1"
    )["abstract_parallel_quotient_descent"] == "NONE"
    checks["canonical_hopf_no_regular"] = all(
        row["canonical_Hopf_tangent_descent"].startswith("NONE_REGULAR") for row in descent[:6]
    )
    checks["holonomy_dichotomy_table"] = {
        row["complete_total_space_holonomy"] for row in holonomy
        if row["stationary_subfamily"] != "proper_nontrivial_reduced_holonomy"
    } == {"TRIVIAL", "FULL_SO2"}
    checks["proper_reduced_holonomy_rejected"] = holonomy[-1]["curvature_status"] == "IMPOSSIBLE_IN_DECLARED_ARENA"

    checks["independent_16_of_16"] = independent["status"] == "PASS" and independent["passed"] == independent["total"] == 16
    checks["manifest_backed_derivation_no_selection"] = result["manifest_backed_r17_source_selection"] is False
    checks["derivation_no_proper_reduction"] = result["proper_nontrivial_reduced_holonomy"] is False

    census_bytes = (HERE / "R17_TRACKED_REFERENCE_CENSUS.tsv").read_bytes()
    checks["census_hash"] = hashlib.sha256(census_bytes).hexdigest() == census_result["census_sha256"]
    checks["census_exact_count"] = len(census) == census_result["tracked_text_paths_with_r17_alias"] == 276
    checks["census_primary_occurrences"] = sum(int(row["primary_alias_occurrences"]) for row in census) == 697
    checks["protected_prefix_unread_absent"] = all(
        not row["path"].startswith(census_result["protected_prefix_excluded_unread"]) for row in census
    )
    checks["current_registry_no_owner"] = census_result["current_authoritative_owner"] == "NONE"
    checks["manual_adjudication_no_selection"] = all(
        row["selection_consequence"] in {"NO_OWNER", "NOT_RELEVANT"} for row in ownership
    )
    checks["manual_adjudication_current_registry"] = ownership[0]["selection_consequence"] == "NO_OWNER"

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    checks["scope_guard"] = all(term in exact for term in (
        "no physical branch", "non-isometric observer arrow", "NO OWNER IS SHOWN BY THE MANIFEST-BACKED"
    ))
    checks["three_descent_types_separated"] = all(term in exact for term in (
        "Abstract parallel quotient", "Canonical inherited Hopf tangent descent", "curvature horizontality"
    ))
    review_raw = (HERE / "EXTERNAL_REVIEW_RAW.md").read_bytes()
    checks["external_review_normalized_hash"] = (
        hashlib.sha256(review_raw).hexdigest()
        == "bb1f700ba002a13f1ebbd9a63b7e63abc4d238160163f828248d04705be24cea"
    )
    review = (HERE / "EXTERNAL_REVIEW.md").read_text(encoding="utf-8")
    checks["external_review_correction_accepted"] = all(term in review for term in (
        "VERIFIED_WITH_CORRECTIONS",
        "No owner is shown by the manifest-backed current authority",
        "repo-wide wording is therefore withdrawn",
    ))

    return checks


def main() -> int:
    checks = validate()
    failed = [name for name, passed in checks.items() if not passed]
    output = {
        "schema_version": 1,
        "checks": checks,
        "passed": len(checks) - len(failed),
        "total": len(checks),
        "failed": failed,
        "status": "PASS" if not failed else "FAIL",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Fail-closed verification of the F01/F02 external-review adjudication layer."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SEALED_COMMIT = "ade5977f"
EXPECTED = {
    "review_manifest": "a0dd0ef023dc6d3aaccbce4d60ed38a4c71571d9377eab0a503b9e5819269e76",
    "review": "f5dc223c8c25d45e82343dbd7a45c760854980d8e3cdb068907829ce09c05740",
    "transcript": "9c875950b38c6d78559c7b650ac1c4887e500331f1b70a62c41d58e9d8cf1870",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def verify_payload(payload: dict) -> None:
    require(payload["status"] == "VERIFIED_WITH_CAVEATS", "review verdict changed")
    require(payload["sealed_rows"] == 33, "sealed row count changed")
    require(payload["package_checks"] == "14/14", "package check count changed")
    require(payload["catch_proofs"] == "12/12", "catch-proof count changed")
    require(payload["independent_route"] == "6/6_PARTIALLY_INDEPENDENT", "independence scope changed")
    require(payload["finite_path_status"] == "REQUIRES_NEW_PREREGISTRATION", "finite path silently authorized")


def replay_sealed_manifest() -> int:
    manifest = HERE / "REVIEW_MANIFEST.tsv"
    require(sha256(manifest) == EXPECTED["review_manifest"], "sealed review manifest mutated")
    sealed_rows = rows(manifest)
    require(len(sealed_rows) == 33, "sealed review universe changed")
    for row in sealed_rows:
        data = subprocess.check_output(["git", "show", f"{SEALED_COMMIT}:{row['path']}"], cwd=ROOT)
        require(sha256_bytes(data) == row["sha256"], f"sealed intake replay failed: {row['path']}")
    return len(sealed_rows)


def verify_current_package() -> None:
    require(sha256(HERE / "EXTERNAL_REVIEW_RAW.md") == EXPECTED["review"], "raw review is not verbatim")
    require(sha256(HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt") == EXPECTED["transcript"], "review transcript changed")
    review = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    require(review.startswith("**Verdict**\n\n`VERIFIED_WITH_CAVEATS`"), "raw review verdict missing")
    adjudication = (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")
    require("`VERIFIED_WITH_CAVEATS` accepted" in adjudication, "adjudication landing missing")
    require("not conflicting claims" in adjudication and "0634b7f801253fc105d374c4c160dbbe19f5b9de" in adjudication
            and "456aeec5" in adjudication, "commit distinction missing")
    require("partially independent computational route" in adjudication, "independence caveat missing")
    require("not a finite-distance CMB map or prediction" in adjudication, "scope boundary missing")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    require("Final evidence grade: `VERIFIED_WITH_CAVEATS`" in report, "audit report not regraded")
    require("12/12` mutations certify\nvalidator sensitivity" in report, "catch-proof scope missing")

    package = json.loads((HERE / "PACKAGE_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULTS.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    require(package["passed"] == package["total"] == 14, "package checks failed")
    require(catches["passed"] == catches["total"] == 12, "catch proofs failed")
    require(independent["passed"] == independent["total"] == 6, "independent route failed")


def verify_postreview_manifest() -> int:
    manifest = HERE / "POSTREVIEW_MANIFEST.tsv"
    manifest_rows = rows(manifest)
    excluded = {manifest.name, "POSTREVIEW_VERIFICATION_RESULT.json"}
    expected_paths = sorted(
        (path for path in HERE.iterdir() if path.is_file() and path.name not in excluded),
        key=lambda path: str(path.relative_to(ROOT)),
    )
    require([row["path"] for row in manifest_rows] == [str(path.relative_to(ROOT)) for path in expected_paths],
            "post-review path universe changed")
    for row, path in zip(manifest_rows, expected_paths):
        require(sha256(path) == row["sha256"], f"post-review hash mismatch: {row['path']}")
    return len(manifest_rows)


def catch_proofs(payload: dict) -> dict[str, str]:
    caught: dict[str, str] = {}
    mutations = {
        "promoted_verdict": ("status", "VERIFIED_AS_STATED"),
        "promoted_finite_path": ("finite_path_status", "AUTHORIZED"),
        "inflated_independence": ("independent_route", "6/6_FULLY_INDEPENDENT"),
    }
    for name, (field, value) in mutations.items():
        mutant = copy.deepcopy(payload)
        mutant[field] = value
        try:
            verify_payload(mutant)
            caught[name] = "FAILED_TO_REJECT"
        except AssertionError:
            caught[name] = "REJECTED"
    require(set(caught.values()) == {"REJECTED"}, "post-review catch proof failed")
    return caught


def main() -> None:
    payload = {
        "status": "VERIFIED_WITH_CAVEATS",
        "sealed_rows": replay_sealed_manifest(),
        "package_checks": "14/14",
        "catch_proofs": "12/12",
        "independent_route": "6/6_PARTIALLY_INDEPENDENT",
        "finite_path_status": "REQUIRES_NEW_PREREGISTRATION",
    }
    verify_payload(payload)
    verify_current_package()
    payload["postreview_manifest_rows"] = verify_postreview_manifest()
    payload["postreview_catches"] = catch_proofs(payload)
    payload["hashes"] = {
        "review_manifest": sha256(HERE / "REVIEW_MANIFEST.tsv"),
        "raw_review": sha256(HERE / "EXTERNAL_REVIEW_RAW.md"),
        "raw_transcript": sha256(HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt"),
        "postreview_manifest": sha256(HERE / "POSTREVIEW_MANIFEST.tsv"),
    }
    payload["schema"] = "UDT_CMB_F01_F02_POSTREVIEW_VERIFICATION_V1"
    payload["result"] = "PASS"
    (HERE / "POSTREVIEW_VERIFICATION_RESULT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

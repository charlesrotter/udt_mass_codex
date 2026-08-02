#!/usr/bin/env python3
"""Fail-closed package verifier for the reciprocal-closure audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent


def load_json(name: str):
    return json.loads((PKG / name).read_text(encoding="utf-8"))


def rows(name: str):
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run_json(script: str):
    proc = subprocess.run([sys.executable, str(PKG / script)], cwd=ROOT, text=True, capture_output=True, timeout=60, check=False)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return json.loads(proc.stdout)


def blob_hash(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def main() -> int:
    checks = {}
    checks["primary_exact_replay"] = run_json("derive_reciprocal_closure.py") == load_json("RESULT.json")
    checks["independent_replay"] = run_json("independent_verify.py") == load_json("INDEPENDENT_VERIFICATION.json")
    checks["preregistration_replay"] = run_json("verify_preregistration.py") == load_json("PREREGISTRATION_VERIFICATION.json")

    candidates = rows("CANDIDATE_OUTCOMES.tsv")
    falsifiers = rows("FALSIFICATION_OUTCOMES.tsv")
    statuses = rows("STATUS_LEDGER.tsv")
    catches = rows("CATCH_PROOFS.tsv")
    checks["candidate_census_10_unique"] = len(candidates) == 10 and len({row["id"] for row in candidates}) == 10
    checks["null_outcome_retained"] = any(row["id"] == "C10" and row["outcome"] == "CURRENT_FOUNDATION_ALLOWED" for row in candidates)
    checks["falsifiers_15_unique"] = len(falsifiers) == 15 and len({row["id"] for row in falsifiers}) == 15
    checks["falsifier_split_13_2"] = sum(row["fired"] == "YES" for row in falsifiers) == 13 and sum(row["fired"] == "NO" for row in falsifiers) == 2
    checks["status_ledger_16_unique"] = len(statuses) == 16 and len({row["id"] for row in statuses}) == 16
    status = {row["id"]: row["status"] for row in statuses}
    checks["projector_selection_open"] = status["R03"] == "OPEN_NOT_SELECTED"
    checks["rank_one_blindness_free"] = status["R08"] == "FREE_CANDIDATE_NOT_DERIVED"
    checks["both_response_requirement_free"] = status["R09"] == "FREE_CANDIDATE_NOT_DERIVED"
    checks["coefficient_open"] = status["R11"] == "OPEN_CONTINUOUS"
    checks["complete_physics_open"] = status["R15"] == "OPEN_UNCHANGED"
    checks["overall_external_reviewed_bounded"] = status["R16"] == "VERIFIED_WITH_CAVEATS_EXTERNAL_REVIEWED"
    checks["catches_10_exercised"] = len(catches) == 10 and all(row["result"] == "PASS_REJECTED" for row in catches)

    sources = rows("SOURCE_INVENTORY.tsv")
    integrity = []
    for row in sources:
        data = (ROOT / row["path"]).read_bytes()
        integrity.append(hashlib.sha256(data).hexdigest() == row["sha256"] and blob_hash(data) == row["git_blob"])
    checks["source_integrity_24"] = len(sources) == 24 and all(integrity)

    report = (PKG / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    checks["report_keeps_conditional_scope"] = "OPEN_COHERENT_ARCHITECTURE_WITH_EXACT_CONDITIONAL_PROJECTOR_RESPONSE_THEOREM" in report
    checks["report_rejects_loop_only_L2_promotion"] = "loop-only principle selects `L4` alone, not `L2+L4`" in report
    checks["report_external_review_complete"] = "Fresh external-model review returned `PASS-WITH-REQUIRED-REPAIRS`" in report
    checks["report_no_stale_external_review_pending"] = "Fresh external-model review is still required" not in report
    checks["report_pinned_replay_wording_repaired"] = (
        "frozen `RESULT.json` records 24/24 exact SymPy 1.14.0 checks" in report
        and "replay requires the pinned SymPy" in report
    )

    review_data = (PKG / "EXTERNAL_ADVERSARIAL_REVIEW.md").read_bytes()
    review = (PKG / "EXTERNAL_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    review_result = load_json("EXTERNAL_REVIEW_RESULT.json")
    checks["external_review_sha256_exact"] = hashlib.sha256(review_data).hexdigest() == "a6d8801337c9090f2fc139c6ab80ff0de6c1c1de18ead5dd369f815ca9843345"
    checks["external_verdict_exact"] = review.startswith("VERDICT\n\nPASS-WITH-REQUIRED-REPAIRS\n")
    checks["external_claim_rulings_10"] = review_result["claim_rulings_sustained"] == 10
    checks["external_single_repair_applied"] = review_result["mandatory_repairs"] == review_result["mandatory_repairs_applied"] == 1
    checks["external_maximum_remains_conditional"] = review_result["maximum_conclusion"] == "OPEN_COHERENT_ARCHITECTURE_WITH_EXACT_CONDITIONAL_PROJECTOR_RESPONSE_THEOREM"

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Fail-closed semantic and evidence verification for the general-screen package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def main() -> int:
    required = [
        "PREREGISTRATION.md", "PREREGISTRATION_CLARIFICATION.md", "PREMISE_LEDGER.tsv",
        "FALSIFICATION_CONTRACT.tsv", "COMPLETENESS_PLAN.tsv", "CANDIDATE_STRATA.tsv",
        "SOURCE_SCOPE.tsv", "SOURCE_MANIFEST.tsv", "derive_general_screen.py",
        "verify_general_screen_independent.py", "DERIVATION_RESULT.json", "GENERAL_CARTAN_RESULT.json",
        "INDEPENDENT_RESULT.json", "CATCH_PROOFS.tsv", "POLAR_RESPONSE_ATLAS.tsv",
        "GAUGE_INVARIANT_ATLAS.tsv", "RESPONSE_RANK_ATLAS.tsv", "CARTAN_RESPONSE_ATLAS.tsv",
        "PAIR_SCREEN_MIXING_ATLAS.tsv", "BLOCK_PRESERVATION_CONDITIONS.tsv",
        "COMPLETE_S3_WITNESS_ATLAS.tsv", "GLOBAL_EXISTENCE_ATLAS.tsv",
        "ORIENTATION_DEGENERACY_ATLAS.tsv", "COMPLETION_DESCENT_ATLAS.tsv",
        "TEN_CRITERION_COVERAGE.tsv", "STATUS_LEDGER.tsv", "COMPLETENESS_MAP.md",
        "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "LAY_REPORT.md", "NEXT_STEP.md", "README.md",
        "FRESH_ADVERSARIAL_REVIEW.md",
    ]
    missing = [name for name in required if not (HERE / name).is_file()]
    require(not missing, f"missing required records: {missing}")

    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    cartan = json.loads((HERE / "GENERAL_CARTAN_RESULT.json").read_text())
    require(derivation["status"] == independent["status"] == "PASS", "machine status")
    require(derivation["coframe_response_rank"] == 4, "coframe rank")
    require(derivation["metric_screen_response_rank"] == 3, "metric rank")
    require(derivation["both_shear_tangents_at_isotropy"] is True, "isotropic shear tangents")
    require(derivation["all_direction_pair_screen_parallel_split"] is False, "parallel split")
    require(cartan["connection_checks"]["metric_compatible_lowered_connection"] is True, "metric compatibility")
    require(cartan["connection_checks"]["torsion_free_against_structure_coefficients"] is True, "torsion")
    require(cartan["connection_checks"]["D2_bottomright_minus_D3_topright"] == "t1", "block obstruction")
    require(independent["production_code_imported"] is False, "independent imports production")
    require(independent["cartan"]["independent_obstruction_method"] == "FROBENIUS_NONINTEGRABILITY",
            "different-method obstruction check")
    require(independent["catch_proofs_passed"] == 24, "catch proof count")

    catches = read_tsv("CATCH_PROOFS.tsv")
    require(len(catches) == 24 and all(row["status"] == "PASS" and row["observed"] == "REJECT" for row in catches),
            "exercised catches")
    require(len(read_tsv("SOURCE_MANIFEST.tsv")) == 15, "source manifest")
    require(len(read_tsv("COMPLETION_DESCENT_ATLAS.tsv")) == 12, "completion rows")
    require(len(read_tsv("TEN_CRITERION_COVERAGE.tsv")) == 10, "criterion rows")
    require(len(read_tsv("RESPONSE_RANK_ATLAS.tsv")) == 5, "rank rows")
    require(len(read_tsv("BLOCK_PRESERVATION_CONDITIONS.tsv")) == 6, "block rows")

    status = {row["claim_id"]: row for row in read_tsv("STATUS_LEDGER.tsv")}
    require(len(status) == 14, "status ledger rows")
    require(status["S08"]["status"] == "DERIVED" and "registered_twisted_S3" in status["S08"]["premise_scope"],
            "bounded no-go stamp")
    require(all(status[key]["status"] == "OPEN" for key in ("S10", "S11", "S12", "S13", "S14")),
            "open scope promoted")

    exact = (HERE / "EXACT_DERIVATION.md").read_text()
    audit = (HERE / "AUDIT_REPORT.md").read_text()
    lay = (HERE / "LAY_REPORT.md").read_text()
    require("It selects no physical branch or UDT dynamics" in exact, "exact scope guard")
    require("Lorentzian geodesic completeness is open" in audit, "completeness scope guard")
    require("not yet a force or matter law" in lay, "lay scope guard")

    fresh = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text()
    require("VERDICT: PASS" in fresh, "fresh review did not pass")
    fresh_normalized = " ".join(fresh.lower().split())
    for token in ("stationary", "off-shell", "Frobenius", "not selected"):
        require(token.lower() in fresh_normalized, f"fresh review missing scope token: {token}")

    result = {
        "schema": "udt-general-screen-audit-verification-1.0",
        "status": "PASS",
        "required_records": len(required),
        "source_rows": 15,
        "completion_rows": 12,
        "criterion_rows": 10,
        "catch_proofs": 24,
        "connection_matrices": 4,
        "fresh_adversarial_review_sha256": sha("FRESH_ADVERSARIAL_REVIEW.md"),
        "derivation_sha256": sha("DERIVATION_RESULT.json"),
        "independent_sha256": sha("INDEPENDENT_RESULT.json"),
        "cartan_sha256": sha("GENERAL_CARTAN_RESULT.json"),
        "maximum_verified_conclusion": "STATIONARY_OFF_SHELL_COMPLETE_S3_GENERAL_SCREEN_EXISTENCE_RESPONSE_AND_BOUNDED_PARALLEL_SPLIT_NO_GO_ONLY",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

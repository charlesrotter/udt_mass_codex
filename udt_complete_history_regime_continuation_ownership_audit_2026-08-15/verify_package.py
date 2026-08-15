#!/usr/bin/env python3
"""Package-consistency verifier for the G98 continuation-ownership audit."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> None:
    checks: dict[str, bool] = {}
    required = [
        "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "FALSIFICATION_CONTRACT.tsv",
        "SOURCE_MANIFEST.tsv", "CANDIDATE_OWNER_ATLAS.tsv", "EXACT_DERIVATION.md",
        "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
        "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md", "AUDIT_REPORT.md", "LAY_REPORT.md",
        "derive_continuation_ownership.py", "verify_continuation_independent.py",
        "run_catch_proofs.py",
        "POST_RESULT_AUTHORITY_APPEND_NOTE.md",
    ]
    for name in required:
        checks[f"exists:{name}"] = (HERE / name).is_file()

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    checks["ten_frozen_sources"] = len(sources) == 10
    source_hash_checks = []
    for row in sources:
        data = (ROOT / row["path"]).read_bytes()
        if row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv":
            lines = data.splitlines(keepends=True)
            checks["G98_is_final_authority_append"] = bool(lines and lines[-1].startswith(b"G98\t"))
            data = b"".join(lines[:-1]) if checks["G98_is_final_authority_append"] else data
        source_hash_checks.append(hashlib.sha256(data).hexdigest() == row["sha256"])
    checks["source_hashes"] = all(source_hash_checks)

    primary = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    checks["primary_pass"] = primary["all_checks_pass"] is True
    checks["landing_permitted_not_owned"] = primary["landing"] == "PERMITTED_NOT_OWNED"
    checks["three_families"] = [item["kind"] for item in primary["families"]] == ["flat", "monotone", "loud_quiet_loud"]
    checks["owner_count_zero"] = primary["owner_summary"]["active_native_history_owner_count"] == 0
    checks["independent_pass"] = independent["all_checks_pass"] is True
    checks["independent_no_sympy"] = "no SymPy" in independent["method"]
    checks["independent_caveat"] = "not a second symbolic proof" in independent["caveat"]
    checks["catch_pass"] = catches["all_checks_pass"] is True and catches["passed"] == 7
    checks["catch_role_scoped"] = "not independent mathematical evidence" in catches["role"]

    with (HERE / "CANDIDATE_OWNER_ATLAS.tsv").open(newline="") as handle:
        owners = list(csv.DictReader(handle, delimiter="\t"))
    checks["fifteen_owner_classes"] = len(owners) == 15
    checks["all_owner_flags_no"] = all(row["active_native_nonidentity_history_rule"] == "no" for row in owners)

    report = (HERE / "AUDIT_REPORT.md").read_text()
    checks["report_scoped"] = "frozen source universe" in report and "not a generic mathematical no-go" in report
    checks["observation_not_derivation"] = "OBSERVED/CONDITIONAL" in report
    checks["no_fit_guard"] = "Do not fit a sequence" in report

    payload = {
        "schema": "udt.complete_history_regime_continuation_package_verification.v1",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "all_checks_pass": all(checks.values()),
        "verifier_role": "package consistency and semantic guards; not independent derivation",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))
    if not payload["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

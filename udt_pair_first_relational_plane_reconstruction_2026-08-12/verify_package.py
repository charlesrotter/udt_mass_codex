#!/usr/bin/env python3
"""Bounded package verifier for the pair-first relational-plane result."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def load_json(name):
    with (HERE / name).open(encoding="utf-8") as f:
        return json.load(f, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def main():
    production = load_json("DERIVATION_RESULT.json")
    independent = load_json("INDEPENDENT_VERIFICATION.json")
    catches = load_json("CATCH_PROOF_RESULTS.json")
    external = load_json("EXTERNAL_REVIEW_RECORD.json")
    status_rows = list(csv.DictReader((HERE / "STATUS_LEDGER.tsv").open(encoding="utf-8"), delimiter="\t"))
    premise_rows = list(csv.DictReader((HERE / "PREMISE_LEDGER.tsv").open(encoding="utf-8"), delimiter="\t"))
    contract_rows = list(csv.DictReader((HERE / "FALSIFICATION_CONTRACT.tsv").open(encoding="utf-8"), delimiter="\t"))
    source_rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"), delimiter="\t"))
    source_hashes_match = all(
        hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"]
        for row in source_rows
    )

    required = [
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "FALSIFICATION_CONTRACT.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "STATUS_LEDGER.tsv",
        "DOWNSTREAM_REGRADE.tsv",
        "derive_pair_first.py",
        "verify_pair_first_independent.py",
        "run_catch_proofs.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULTS.json",
        "ADVERSARIAL_REVIEW.md",
        "EXTERNAL_REVIEW_RECORD.json",
    ]
    missing = [name for name in required if not (HERE / name).is_file()]
    checks = {
        "no_required_files_missing": not missing,
        "production_pass": production["status"] == "PASS" and all(production["checks"].values()),
        "independent_pass": independent["status"] == "PASS",
        "independent_direct_160": independent["checks"]["direct_pullback"] == 160,
        "independent_reduced_160": independent["checks"]["reduced_gram"] == 160,
        "independent_coordinate_160": independent["checks"]["coordinate_covariance"] == 160,
        "independent_screen_160": independent["checks"]["screen_covariance"] == 160,
        "catch_proofs_complete": catches["status"] == "PASS" and catches["caught"] == catches["catch_count"],
        "status_has_open_F": any(r["claim"] == "physical F or event pairing from founding postulates" and r["status"] == "OPEN" for r in status_rows),
        "status_has_conditional_plane": any(r["claim"] == "regular timelike F owns E_pair=dF(TSigma)" and r["status"] == "DERIVED_CONDITIONAL" for r in status_rows),
        "premises_present": len(premise_rows) >= 10,
        "contract_present": len(contract_rows) >= 10,
        "source_manifest_exact": len(source_rows) == 8 and source_hashes_match,
        "external_review_accept": external["status"] == "ACCEPT__VERIFIED_WITH_CAVEATS",
        "external_clean_replay_200": external["external_clean_replay"]["direct_pullbacks"] == 200,
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    result = {
        "schema": "udt-pair-first-package-verification-v1",
        "status": status,
        "checks": checks,
        "missing": missing,
        "production_exact_checks": len(production["checks"]),
        "independent_samples": independent["exact_fraction_samples"],
        "terminal_reconstructions": independent["checks"]["terminal_reconstruction"],
        "catch_count": catches["catch_count"],
        "status_rows": len(status_rows),
        "premise_rows": len(premise_rows),
        "contract_rows": len(contract_rows),
        "source_rows": len(source_rows),
    }
    (HERE / "PACKAGE_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

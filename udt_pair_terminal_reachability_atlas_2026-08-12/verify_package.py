#!/usr/bin/env python3
"""Administrative and saved-artifact consistency checks; not an independent derivation."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    checks = {}
    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    checks["source_count"] = len(sources) == 5
    checks["source_hashes"] = all(
        (REPO / row["path"]).is_file() and sha256(REPO / row["path"]) == row["sha256"]
        for row in sources
    )

    required = [
        "PRE_REGISTRATION.md", "PREMISE_LEDGER.tsv", "SOURCE_MANIFEST.tsv",
        "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md",
        "ADVERSARIAL_REVIEW.md",
        "derive_reachability.py", "verify_reachability_independent.py", "run_catch_proofs.py",
        "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOFS.json",
        "RATIONAL_ATLAS.tsv", "RESULT_MANIFEST.tsv",
    ]
    checks["required_files"] = all((ROOT / name).is_file() for name in required)

    derivation = json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((ROOT / "CATCH_PROOFS.json").read_text())
    checks["symbolic_checks"] = derivation["symbolic"]["checks"] == "12"
    checks["production_case_count"] = derivation["rational_case_count"] == 324
    checks["production_strata"] = all(value > 0 for value in derivation["counts"].values())
    checks["independent_forward"] = independent["forward"]["cases"] == 328
    checks["independent_inverse"] = independent["inverse"]["cases"] == 146
    checks["independent_strata"] = all(
        independent["forward"][key] > 0
        for key in ["LORENTZIAN", "DEGENERATE", "POSITIVE_DEFINITE", "rank0", "rank1", "rank2"]
    )
    checks["covariance"] = all(independent["covariance_controls"].values())
    checks["catch_proofs"] = catches["catch_count"] == 8 and all(catches["catches"].values())

    with (ROOT / "RATIONAL_ATLAS.tsv").open(newline="") as handle:
        atlas = list(csv.DictReader(handle, delimiter="\t"))
    checks["atlas_rows"] = len(atlas) == 324
    checks["atlas_unique_ids"] = len({row["case_id"] for row in atlas}) == 324

    with (ROOT / "RESULT_MANIFEST.tsv").open(newline="") as handle:
        results = list(csv.DictReader(handle, delimiter="\t"))
    checks["result_manifest_count"] = len(results) == 16
    checks["result_manifest_hashes"] = all(
        (ROOT / row["path"]).is_file() and sha256(ROOT / row["path"]) == row["sha256"]
        for row in results
    )

    assert all(checks.values()), checks
    result = {
        "status": "PASS",
        "scope": "administrative and saved-artifact consistency; not independent derivation",
        "checks": checks,
    }
    (ROOT / "PACKAGE_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

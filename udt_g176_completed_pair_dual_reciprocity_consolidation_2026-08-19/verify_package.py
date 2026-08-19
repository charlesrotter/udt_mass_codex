#!/usr/bin/env python3
"""Fail-closed G176 package verifier."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    manifest = (ROOT / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()
    require(manifest[0] == "sha256\tpath\trole", "manifest header")
    require(len(manifest) == 10, "manifest must contain nine sources")
    for row in manifest[1:]:
        expected, relative, _role = row.split("\t")
        require((REPO / relative).is_file(), f"missing source: {relative}")
        require(hashlib.sha256((REPO / relative).read_bytes()).hexdigest() == expected, f"hash: {relative}")

    for script in ("verify_completed_pair_reciprocity_independent.py", "run_catch_proofs.py"):
        run = subprocess.run(
            [sys.executable, str(ROOT / script)], cwd=REPO, text=True, capture_output=True, check=False
        )
        require(run.returncode == 0, f"{script}: {run.stdout}{run.stderr}")

    derivation = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    require(derivation["symbolic_check_count"] == 20, "symbolic count")
    require(all(derivation["symbolic_checks"].values()), "symbolic failure")
    require(independent["trials"] == 20_000, "trial count")
    require(independent["exact_assertion_count"] == 260_000, "exact assertion count")
    require(independent["pass"] is True, "independent failure")
    require(catches["catch_count"] == 18 and catches["pass"] is True, "catch failure")

    audit = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    adoption = (ROOT / "ADOPTION_RECORD.md").read_text(encoding="utf-8")
    for token in (
        "WORKING_FOUNDATIONAL_CLARIFICATION",
        "m=T L_sigma=sqrt(-det h_sigma)",
        "ARBITRARY_CALIBRATIONS_ARE_CONTROL_QUERIES_NOT_RIVAL_KERNELS",
        "does not select pair events or germs",
    ):
        require(token in audit + exact + adoption, f"semantic token absent: {token}")

    premise = subprocess.run(
        [sys.executable, str(REPO / "verify_current_scientific_premises.py")],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )
    require(premise.returncode == 0, premise.stdout + premise.stderr)
    require("PASS: 162-row premise registry" in premise.stdout, "premise pass token absent")

    result = {
        "audit": "G176",
        "status": "PASS__VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_REVIEW_PENDING",
        "source_hashes": 9,
        "symbolic_checks": 20,
        "independent_exact_assertions": 260_000,
        "angular_turn_checks": independent["angular_turn_positive_checks"],
        "mutation_catches": 18,
        "premise_verifier_returncode": premise.returncode,
    }
    (ROOT / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

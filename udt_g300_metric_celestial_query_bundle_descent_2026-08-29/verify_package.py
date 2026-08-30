#!/usr/bin/env python3
"""Aggregate no-write verifier for the G300 package."""

import json
from pathlib import Path
import subprocess
import sys


PACKAGE = Path(__file__).resolve().parent


def run(name):
    completed = subprocess.run(
        [sys.executable, "-S", str(PACKAGE / name)],
        cwd=PACKAGE.parent,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main():
    production = run("derive_celestial_query_bundle.py")
    independent = run("verify_celestial_query_bundle_independent.py")
    catches = run("run_catch_proofs.py")
    frozen_production = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    frozen_independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    frozen_catches = json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    assert production == frozen_production
    assert independent == frozen_independent
    assert catches == frozen_catches
    exact = (PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    audit = (PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    lay = (PACKAGE / "LAY_REPORT.md").read_text(encoding="utf-8")
    narrative = " ".join((exact + audit + lay).split()).lower()
    repaired_landing = (
        "NO_PROPER_LAWFUL_RANK_TWO_QUERY_FAMILY_IS_DERIVED__THE_QUERY_DOMAIN_REMAINS_"
        "WHOLLY_OPERATIONAL"
    )
    assert production["landing"] == repaired_landing
    assert production["lawful_query_family_ownership"] == "NOT_DERIVED"
    assert independent["lawful_query_family_ownership"] == "NOT_TESTED_BY_ALGEBRA"
    for token in (
        "full path-labelled frame morphism remains the composition owner",
        "lawful query-family ownership remains open",
        "regular evaluator input",
        "metric naturality cannot select one global query section",
        "No metric component or reciprocal-kernel formula changed",
    ):
        assert token.lower() in narrative, token
    forbidden = (
        "This closes G299's lawful **query-domain family**",
        "the metric owns the query bundle",
    )
    for token in forbidden:
        assert token.lower() not in narrative, token
    print(json.dumps({
        "status": "PASS",
        "production_cases": production["cases"],
        "production_assertions": production["assertions"],
        "independent_cases": independent["cases"],
        "independent_assertions": independent["assertions"],
        "hostile_catches": catches["hostile_catches"],
        "grade": "EXTERNALLY_REFUTED_AND_REPAIRED_WITH_CAVEATS",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

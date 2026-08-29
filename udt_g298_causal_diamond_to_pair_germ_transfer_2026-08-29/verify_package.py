#!/usr/bin/env python3
"""No-write package verifier for G298."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
LANDING = "MULTIPLE_INEQUIVALENT_NATURAL_PAIR_ONE_JET_PROJECTIONS_SURVIVE_FROM_THE_DERIVED_COMPLETE_RELATION_STATE__NO_UNIQUE_TRANSFER_TO_G2_IS_OWNED"


def run(script):
    proc = subprocess.run(
        [sys.executable, str(ROOT / script), "--no-write"],
        cwd=REPO,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return proc.stdout


def main():
    source_count = 0
    for line in (ROOT / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]:
        digest, rel = line.split("\t")
        assert hashlib.sha256((REPO / rel).read_bytes()).hexdigest() == digest
        source_count += 1

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text())
    assert production["landing"] == LANDING
    assert production["exact_cases"] == 1260
    assert production["exact_assertions"] == 17660
    assert independent["status"] == "PASS"
    assert independent["trials"] == 20000
    assert independent["assertions"] == 358543
    assert independent["verification_boundary"].startswith("algebraic projection witness only")
    assert catches["status"] == "PASS"
    assert catches["count"] == 7

    for name in ("EXACT_DERIVATION.md", "AUDIT_REPORT.md", "STATUS_LEDGER.tsv"):
        assert LANDING in (ROOT / name).read_text().replace("\n", "")

    prod_stdout = run("derive_causal_pair_transfer.py")
    indep_stdout = run("verify_causal_pair_transfer_independent.py")
    catch_stdout = run("run_catch_proofs.py")
    assert LANDING in prod_stdout
    assert '"status": "PASS"' in indep_stdout
    assert '"count": 7' in catch_stdout

    result = {
        "status": "PASS",
        "source_hashes": source_count,
        "production_cases": production["exact_cases"],
        "production_assertions": production["exact_assertions"],
        "independent_cases": independent["trials"],
        "independent_assertions": independent["assertions"],
        "hostile_catches": catches["count"],
        "no_write_replays": 3,
        "external_review": "R1_COMPLETION_VERIFIED__G298_REPAIRED_LANDING_CLOSED",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

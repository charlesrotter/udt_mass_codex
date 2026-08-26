#!/usr/bin/env python3
"""No-write G266 package verifier."""

import hashlib
import json
import pathlib
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_json(name):
    proc = subprocess.run(
        [sys.executable, str(ROOT / name)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def main():
    source_rows = (ROOT / "SOURCE_MANIFEST.tsv").read_text().splitlines()
    assert source_rows[0] == "path\tsha256\trole"
    assert len(source_rows) == 8
    for row in source_rows[1:]:
        rel, expected, _role = row.split("\t")
        path = REPO / rel
        assert path.is_file(), rel
        assert sha256(path) == expected, rel

    exact = run_json("derive_even_channel.py")
    independent = run_json("verify_independent.py")
    catches = run_json("run_catch_proofs.py")
    recorded_exact = json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
    recorded_independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
    recorded_catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text())
    assert exact == recorded_exact
    assert independent == recorded_independent
    assert catches == recorded_catches
    assert exact["status"] == independent["status"] == catches["status"] == "PASS"
    assert exact["exact_checks"] == 25
    assert independent["assertions"] == 768
    assert catches["catches"] == 8
    assert exact["history_rejection_by_current_premises"] == 0
    assert exact["physical_projection"] == "OPEN_NOT_SELECTED_BY_F1_F4_W1_W4"
    assert exact["distance_functional"] == "OPEN_QUERY_OWNED"
    assert "Fresh external adversarial review pending" not in (ROOT / "AUDIT_REPORT.md").read_text()
    assert "FRESH_EXTERNAL_ADVERSARIAL_REVIEW_PENDING" in (ROOT / "EVIDENCE_GATES.md").read_text()
    assert "No adoption of `P_INF`, `P_MUT`, `sech(delta)`" in (ROOT / "PREREGISTRATION.md").read_text()

    print(json.dumps({
        "status": "PASS",
        "grade": "INTERNALLY_VERIFIED_LEAD__FRESH_EXTERNAL_ADVERSARIAL_REVIEW_PENDING",
        "landing": exact["landing"],
        "selected_alternative": exact["selected_alternative"],
        "exact_checks": exact["exact_checks"],
        "independent_assertions": independent["assertions"],
        "mutation_catches": catches["catches"],
        "source_count": len(source_rows) - 1,
        "recorded_live_exact": True,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

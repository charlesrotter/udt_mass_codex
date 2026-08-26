#!/usr/bin/env python3
"""No-write G265 package verifier."""

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
    rows = (ROOT / "SOURCE_MANIFEST.tsv").read_text().splitlines()
    assert rows[0] == "path\tsha256\trole"
    resolutions = {}
    for row in rows[1:]:
        rel, expected, _role = row.split("\t")
        live = REPO / rel
        if live.exists() and sha256(live) == expected:
            resolutions[rel] = "live_exact"
            continue
        proc = subprocess.run(
            ["git", "rev-list", "--all", "--objects", "--", rel],
            cwd=REPO,
            check=True,
            capture_output=True,
            text=True,
        )
        matched = False
        for line in proc.stdout.splitlines():
            obj = line.split(" ", 1)[0]
            blob = subprocess.run(
                ["git", "cat-file", "-p", obj],
                cwd=REPO,
                check=True,
                capture_output=True,
            ).stdout
            if hashlib.sha256(blob).hexdigest() == expected:
                matched = True
                break
        assert matched, rel
        resolutions[rel] = "git_object_exact"

    exact = run_json("derive_closure.py")
    independent = run_json("verify_independent.py")
    catches = run_json("run_catch_proofs.py")
    assert exact["status"] == independent["status"] == catches["status"] == "PASS"
    assert exact["exact_checks"] == 18
    assert independent["assertions"] == 63
    assert catches["catches"] == 8

    recorded = json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
    assert recorded["landing"].startswith("INFINITE_BARE_C_METRIC_NULL_READING_IS_IDENTITY")
    assert "INTERNALLY_VERIFIED_LEAD" in (ROOT / "EVIDENCE_GATES.md").read_text()
    assert "PROPOSED_FOUNDATIONAL_RECOVERY_NOT_ADOPTED" in (ROOT / "STATUS_LEDGER.tsv").read_text()

    print(
        json.dumps(
            {
                "status": "PASS",
                "grade": "INTERNALLY_VERIFIED_LEAD__FRESH_ADVERSARIAL_REVIEW_AND_CHARLES_REGRADE_OPEN",
                "exact_checks": 18,
                "independent_assertions": 63,
                "mutation_catches": 8,
                "source_count": len(resolutions),
                "source_resolutions": resolutions,
                "landing": recorded["landing"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

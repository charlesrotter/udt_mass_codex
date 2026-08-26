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


def assert_exact_result(replayed, recorded):
    """Fail closed on any recorded/live result mismatch."""
    assert replayed == recorded, {
        "replayed_only": sorted(set(replayed) - set(recorded)),
        "recorded_only": sorted(set(recorded) - set(replayed)),
        "changed": sorted(
            key
            for key in set(replayed) & set(recorded)
            if replayed[key] != recorded[key]
        ),
    }


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
    assert_exact_result(exact, recorded)
    mutated = dict(recorded)
    mutated["landing"] += "__MUTATED_RECORDED_LANDING"
    mutation_caught = False
    try:
        assert_exact_result(exact, mutated)
    except AssertionError:
        mutation_caught = True
    assert mutation_caught

    assert "G265_REPAIRS_ACCEPTED" in (
        ROOT / "EVIDENCE_GATES.md"
    ).read_text()
    assert "PROPOSED_FOUNDATIONAL_RECOVERY_NOT_ADOPTED" in (ROOT / "STATUS_LEDGER.tsv").read_text()
    assert "not yet a founded physical readout" in (ROOT / "LAY_REPORT.md").read_text()
    assert "still-proposed mutuality statement" in (ROOT / "EXACT_DERIVATION.md").read_text()
    assert "Physical ownership of the even channel has not been adopted or derived" in (
        ROOT / "AUDIT_REPORT.md"
    ).read_text()

    print(
        json.dumps(
            {
                "status": "PASS",
                "grade": "EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS__G265_REPAIRS_ACCEPTED",
                "exact_checks": 18,
                "independent_assertions": 63,
                "mutation_catches": 8,
                "replay_result_exact": True,
                "recorded_result_mutation_caught": mutation_caught,
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

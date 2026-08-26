#!/usr/bin/env python3
"""No-write G266 package verifier."""

import hashlib
import importlib.util
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


def resolve_source(rel, expected):
    candidates = (REPO / rel, REPO / "private_sources" / rel)
    for path in candidates:
        if path.is_file() and sha256(path) == expected:
            return path
    raise AssertionError(rel)


def main():
    source_rows = (ROOT / "SOURCE_MANIFEST.tsv").read_text().splitlines()
    assert source_rows[0] == "path\tsha256\trole"
    assert len(source_rows) == 8
    for row in source_rows[1:]:
        rel, expected, _role = row.split("\t")
        resolve_source(rel, expected)

    first_rel, first_expected, _role = source_rows[1].split("\t")
    try:
        resolve_source(first_rel, "0" * 64)
    except AssertionError:
        source_hash_mutation_rejected = True
    else:
        source_hash_mutation_rejected = False
    assert source_hash_mutation_rejected

    exact = run_json("derive_even_channel_stdlib.py")
    if importlib.util.find_spec("sympy") is not None:
        assert run_json("derive_even_channel.py") == exact
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
    assert "EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS__G266_REPAIRS_ACCEPTED" in (
        ROOT / "EVIDENCE_GATES.md"
    ).read_text()
    followup = ROOT / "EXTERNAL_REPAIR_FOLLOWUP_GPT54.md"
    assert followup.read_bytes() == b"REPAIRS_ACCEPTED\n"
    assert sha256(followup) == "2341fe9ebce96341df2d3666523ef704cc49af071fa0c7480acbe94243cc952d"
    assert "No adoption of `P_INF`, `P_MUT`, `sech(delta)`" in (ROOT / "PREREGISTRATION.md").read_text()
    audit_text = (ROOT / "AUDIT_REPORT.md").read_text()
    assert "already-fixed invariant areal-radius" in audit_text
    assert "physical attachment `ds=dR`" in audit_text
    assert "formed only from that kernel" in exact["invariant_algebra"]

    print(json.dumps({
        "status": "PASS",
        "grade": "EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS__G266_REPAIRS_ACCEPTED",
        "landing": exact["landing"],
        "selected_alternative": exact["selected_alternative"],
        "exact_checks": exact["exact_checks"],
        "independent_assertions": independent["assertions"],
        "mutation_catches": catches["catches"],
        "source_count": len(source_rows) - 1,
        "source_hash_mutation_rejected": source_hash_mutation_rejected,
        "dependency_free_exact_replay": True,
        "sympy_reference_replayed": importlib.util.find_spec("sympy") is not None,
        "recorded_live_exact": True,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

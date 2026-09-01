#!/usr/bin/env python3
"""No-persistent-output aggregate verifier for G311."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PREREG_COMMIT = "ab93cf6e"
PREREG_PARENT = "8ec52db6"


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_checked(command: list[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, check=False)
    if result.returncode:
        raise SystemExit(
            f"command failed ({result.returncode}): {' '.join(command)}\n{result.stdout}{result.stderr}"
        )
    return result


def verify() -> dict[str, object]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory(prefix="g311_verify_") as tmp:
        tmpdir = Path(tmp)
        production_out = tmpdir / "production.json"
        independent_out = tmpdir / "independent.json"
        catches_out = tmpdir / "catches.json"
        run_checked(
            [sys.executable, "-S", "derive_covariant_response.py", "--output", str(production_out)],
            ROOT,
            env,
        )
        run_checked(
            [sys.executable, "-S", "verify_covariant_response_independent.py", "--output", str(independent_out)],
            ROOT,
            env,
        )
        run_checked(
            [sys.executable, "-S", "run_catch_proofs.py", "--output", str(catches_out)],
            ROOT,
            env,
        )
        assert load(production_out) == load(ROOT / "DERIVATION_RESULT.json")
        assert load(independent_out) == load(ROOT / "INDEPENDENT_VERIFICATION.json")
        assert load(catches_out) == load(ROOT / "CATCH_PROOF_RESULT.json")

    production = load(ROOT / "DERIVATION_RESULT.json")
    independent = load(ROOT / "INDEPENDENT_VERIFICATION.json")
    catches = load(ROOT / "CATCH_PROOF_RESULT.json")
    assert production["landing"] == (
        "FULL_COVARIANT_RECIPROCITY_CLOSES_RESPONSE_SHAPE_ONLY"
        "__RESPONSE_CONSTITUTION_REMAINS_OPEN"
    )
    assert production["reciprocal_shape_rank"] == independent["reciprocal_shape_rank"] == 9
    assert production["balance_rank"] == independent["balance_rank"] == 9
    assert production["full_response_annihilator"] == "span(g_ab)"
    assert independent["annihilator_is_metric_line"] is True
    assert independent["standard_library_only"] is True
    assert independent["shares_production_imports"] is False
    assert production["response_architecture_selected_by_covariance_alone"] is False
    assert independent["response_architecture_counterexample_verified"] is True
    assert catches["caught"] == catches["expected"] == 6

    exact = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (ROOT / "LAY_REPORT.md").read_text(encoding="utf-8")
    ledger = (ROOT / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    for token in (
        "E^{\\mathrm{TF}}_{ab}=0",
        "response architecture",
        "not derived or",
        "initial data select one history",
        "C_{abcd}=0",
        "two metric configuration degrees of freedom",
    ):
        assert token.lower() in exact.lower(), token
    for token in (
        "first-curvature G301 branch",
        "initial conditions select",
        "metric, reciprocal kernel, angular cancellation",
    ):
        assert token.lower() in lay.lower(), token
    assert "fresh_adversarial_review\tSCIENTIFIC_LANDING_UPHELD_REPAIRABLE_DEFECTS" in ledger
    assert (
        "repair_followup_review\tG311_ACCEPTED_WITH_RESPONSE_CONSTITUTION_BOUNDARY"
        in ledger
    )

    ancestry = (ROOT / "PREREGISTRATION_ANCESTRY.md").read_text(encoding="utf-8")
    repair = (ROOT / "REPAIR_PREREGISTRATION.md").read_text(encoding="utf-8")
    assert PREREG_COMMIT in ancestry and PREREG_PARENT in ancestry
    for repair_token in (
        "R1 — dependency-free independent verifier",
        "R2 — intake-self-contained aggregate replay",
        "R3 — hostile-harness evidence grade",
    ):
        assert repair_token in repair

    # Intake-containment guard: the registered aggregate replay may not resolve above ROOT or
    # invoke Git. Historical ancestry is frozen as documentary evidence, not recomputed here.
    own_source = Path(__file__).read_text(encoding="utf-8")
    forbidden_source_tokens = (
        "ROOT" + ".parent",
        "[" + "'git'",
        "[" + '"git"',
    )
    for forbidden_source_token in forbidden_source_tokens:
        assert forbidden_source_token not in own_source

    return {
        "verdict": "PASS",
        "preregistration_commit": PREREG_COMMIT,
        "saved_replays_match": True,
        "production_checks": production["production_checks"],
        "independent_checks": independent["checks"],
        "hostile_catches": catches["caught"],
        "hostile_harness_grade": catches["evidence_grade"],
        "scientific_landing": production["landing"],
        "sealed_replay_self_contained": True,
        "fresh_adversarial_review": "SCIENTIFIC_LANDING_UPHELD_REPAIRABLE_DEFECTS",
        "repair_followup_review": "G311_ACCEPTED_WITH_RESPONSE_CONSTITUTION_BOUNDARY",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

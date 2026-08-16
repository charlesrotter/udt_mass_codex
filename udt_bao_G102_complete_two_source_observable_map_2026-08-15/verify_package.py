#!/usr/bin/env python3
"""Fail-closed package and fresh-execution verifier for G102."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def fresh_json(script: str) -> dict:
    raw = subprocess.check_output([sys.executable, str(ROOT / script)], cwd=REPO, text=True)
    return json.loads(raw)


def read_json(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def main() -> None:
    checks = 0
    pairs = (
        ("derive_two_source_map.py", "DERIVATION_RESULT.json"),
        ("verify_two_source_independent.py", "INDEPENDENT_VERIFICATION.json"),
        ("run_catch_proofs.py", "CATCH_PROOF_RESULT.json"),
    )
    for script, artifact in pairs:
        require(fresh_json(script) == read_json(artifact), f"fresh execution mismatch: {artifact}")
        checks += 1

    with (ROOT / "SOURCE_MANIFEST_PREREG.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    require(len(sources) == 8, "source manifest cardinality changed")
    for row in sources:
        digest = hashlib.sha256((REPO / row["source"]).read_bytes()).hexdigest()
        require(digest == row["sha256"], f"source hash mismatch: {row['source']}")
    checks += 1

    result = read_json("DERIVATION_RESULT.json")
    require(result["outcome_artifacts_read"] == 0, "outcome artifact read declared")
    require(result["synthetic_pairs"]["terminal_depths_separately_typed"] == ["log(2)", "log(3)"], "endpoint typing regressed")
    require("ENDPOINT_DEPTH_CARRY_CONDITIONAL" in result["maximum_conclusion"], "endpoint caveat absent")
    checks += 3

    independent = read_json("INDEPENDENT_VERIFICATION.json")
    require(independent["landy_szalay"] == ["-58/35", "19/70", "39/70"], "independent estimator changed")
    require(independent["terminal_Z_separately_typed"] == [2, 3], "independent endpoint separation absent")
    checks += 2

    catch = read_json("CATCH_PROOF_RESULT.json")
    require(len(catch["mutations"]) == 5, "catch-proof cardinality changed")
    require(set(catch["mutations"].values()) == {"CAUGHT"}, "hostile mutation escaped")
    checks += 2

    required_files = (
        "PREREGISTRATION.md",
        "PREREGISTRATION_CLARIFICATION.md",
        "PREREGISTRATION_ENDPOINT_TYPE_CORRECTION.md",
        "INDEPENDENT_VERIFIER_CORRECTION_PREREGISTRATION.md",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "EVIDENCE_GATES.md",
        "EXTERNAL_REVIEW.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "EXTERNAL_REVIEW_RAW.md",
        "LAY_REPORT.md",
        "REVIEW_DISPATCH.md",
        "STATUS_LEDGER.tsv",
    )
    require(all((ROOT / name).is_file() for name in required_files), "required evidence file absent")
    checks += 1

    audit = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    for token in (
        "DIRECTION_IDENTIFICATION_QUERY_OWNED",
        "ENDPOINT_DEPTH_CARRY_CONDITIONAL",
        "PHYSICAL_HISTORY_AND_SOURCE_PAIR_MEASURE_OPEN",
        "zero BAO outcome artifacts",
    ):
        require(token in audit, f"audit guard absent: {token}")
    checks += 1

    exact = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    require("supported in that image" in exact, "identifiability support qualifier absent")
    require("not a survey-scale pipeline replay" in exact, "synthetic-estimator scope absent")
    review = (ROOT / "EXTERNAL_REVIEW.md").read_text(encoding="utf-8")
    require("PASS_WITH_CAVEATS" in review, "external verdict absent")
    status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
    require("No derivation script or result exists yet" not in status, "stale pre-result status")
    require("must be revised and rerun" not in status, "stale rerun instruction")
    checks += 4

    print(f"PASS: G102 package verification ({checks} gates, {len(sources)} source hashes)")


if __name__ == "__main__":
    main()

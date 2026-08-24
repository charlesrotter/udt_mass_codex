#!/usr/bin/env python3
"""No-write package verifier for G247 saved evidence and source freeze."""

from __future__ import annotations

import csv
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
LANDING = (
    "REGULAR_DIRECTION_ROUTE_LABELLED_NULL_BRANCH_ATLAS_DESCENDS_GLOBALLY"
    "__DIRECT_FUTURE_NULL_LINKS_FORM_A_QUIVER_NOT_A_CATEGORY_OR_GROUPOID"
    "__FREE_MATCHED_NULL_CHAIN_CATEGORY_CARRIES_ADDITIVE_DEPTH_AND_PATH_LABELLED_PHASE"
    "__CAUSTIC_BRANCH_AGGREGATION_GLOBAL_SELECTION_AND_PHYSICAL_HISTORY_REMAIN_OPEN"
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def replay(script: str, *args: str) -> dict:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    cp = subprocess.run(
        [sys.executable, str(PKG / script), *args],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(cp.stdout)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    required = [
        "MAP.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "PREREGISTRATION_COMMIT.md",
        "SOURCE_MANIFEST.tsv",
        "EXACT_DERIVATION.md", "LAY_REPORT.md", "AUDIT_REPORT.md", "EVIDENCE_GATES.md",
        "STATUS_LEDGER.tsv", "COMMANDS.md", "REVIEW_REQUEST.md", "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
        "derive_global_null_branch_network.py", "verify_global_null_branch_network_independent.py",
        "run_catch_proofs.py", "verify_package.py", "build_review_intake.py",
    ]
    missing = [name for name in required if not (PKG / name).is_file()]
    if missing:
        raise SystemExit(f"missing package files: {missing}")

    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in rows:
        path = ROOT / row["path"]
        if not path.is_file() or sha256(path) != row["sha256"]:
            raise SystemExit(f"source freeze mismatch: {row['path']}")

    saved_prod = json.loads((PKG / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    saved_ind = json.loads((PKG / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    saved_catch = json.loads((PKG / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    live_prod = replay("derive_global_null_branch_network.py", "--cases", "2048")
    live_ind = replay("verify_global_null_branch_network_independent.py", "--cases", "5000")
    live_catch = replay("run_catch_proofs.py")

    checks = {
        "source_manifest_rows": len(rows) == 10,
        "saved_production_pass": saved_prod.get("status") == "PASS",
        "saved_independent_pass": saved_ind.get("status") == "PASS",
        "saved_catch_pass": saved_catch.get("status") == "PASS",
        "production_landing": saved_prod.get("landing") == LANDING,
        "independent_landing": saved_ind.get("expected_landing") == LANDING,
        "production_replay_exact": live_prod == saved_prod,
        "independent_replay_exact": live_ind == saved_ind,
        "catch_replay_exact": live_catch == saved_catch,
        "production_floor": saved_prod.get("cases", 0) >= 2048
        and saved_prod.get("assertions", 0) >= 20000,
        "independent_floor": saved_ind.get("cases", 0) >= 5000
        and saved_ind.get("assertions", 0) >= 50000,
        "hostile_floor": saved_catch.get("caught", 0) >= 14
        and saved_catch.get("caught") == saved_catch.get("total"),
    }
    failed = [name for name, value in checks.items() if not value]
    result = {"checks": checks, "failed": failed, "status": "PASS" if not failed else "FAIL"}
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

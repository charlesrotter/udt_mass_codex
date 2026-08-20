#!/usr/bin/env python3
"""Read-only package and replay verifier for G185."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REQUIRED = [
    "PREREGISTRATION.md", "SOURCE_MANIFEST.tsv", "EXACT_DERIVATION.md", "AUDIT_REPORT.md",
    "LAY_REPORT.md", "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md", "COMPLETENESS_MAP.md",
    "ADVERSARIAL_REVIEW_REQUEST.md", "run_g185_channel_replay.py", "verify_g185_independent.py",
    "verify_sealed_intake.js", "run_catch_proofs.py", "PRODUCTION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
    "SEALED_REPLAY_RESULT.json",
    "CATCH_PROOF_RESULT.json",
]
SCRIPTS = ["run_g185_channel_replay.py", "verify_g185_independent.py", "run_catch_proofs.py"]
LANDING = (
    "CENTRAL_SPHERICAL_SNE_QUERY_RETAINS_THE_FULL_RELEVANT_METRIC_RESPONSE__"
    "RADIAL_PAIR_ANGULAR_TANGENT_ZERO_IS_QUERY_DERIVED__AREAL_SKY_RESPONSE_R2_REMAINS_ACTIVE__"
    "FROZEN_DUAL_SNE_REPLAY_IS_CONDITIONALLY_PRESERVED"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def hashes() -> dict[str, str]:
    return {path.name: sha256(path) for path in HERE.iterdir() if path.is_file()}


def main() -> None:
    missing = [name for name in REQUIRED if not (HERE / name).is_file()]
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    source_failures = []
    for row in rows:
        path = Path(row["path"])
        if not path.is_absolute():
            path = ROOT / path
        if not path.is_file() or sha256(path) != row["sha256"]:
            source_failures.append(row["path"])

    production = json.loads((HERE / "PRODUCTION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    sealed_result = json.loads((HERE / "SEALED_REPLAY_RESULT.json").read_text(encoding="utf-8"))
    before = hashes()
    sealed_mode = (ROOT / "sources").is_dir() and all(
        not Path(row["path"]).is_absolute() and Path(row["path"]).parts[:1] == ("sources",)
        for row in rows
    )
    replay = {}
    commands = (
        [["node", "verify_sealed_intake.js"], [sys.executable, "run_catch_proofs.py"]]
        if sealed_mode
        else [[sys.executable, script] for script in SCRIPTS]
    )
    for command in commands:
        completed = subprocess.run(
            command, cwd=HERE, capture_output=True, text=True,
            timeout=120, check=False, env=dict(os.environ),
        )
        replay[" ".join(command)] = {
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
    after = hashes()
    checks = {
        "files_present": not missing,
        "fourteen_sources_immutable": len(rows) == 14 and not source_failures,
        "production_pass": production.get("status") == "PASS",
        "independent_pass": independent.get("status") == "PASS",
        "thirteen_catches": catches.get("executable_catch_count") == 13 and not catches.get("failed_executable_catches"),
        "eleven_semantic_guards": catches.get("semantic_guard_count") == 11,
        "landing_matches": production.get("landing") == LANDING,
        "stored_sealed_replay_pass": sealed_result.get("status") == "PASS",
        "all_replays_pass": all(item["returncode"] == 0 for item in replay.values()),
        "default_replays_are_read_only": before == after,
        "sealed_paths_are_intake_relative": (
            not sealed_mode
            or all(
                not Path(row["path"]).is_absolute()
                and Path(row["path"]).parts[:1] == ("sources",)
                for row in rows
            )
        ),
    }
    external = "PENDING"
    followup_path = HERE / "EXTERNAL_REPAIR_FOLLOWUP_RAW.md"
    external_path = HERE / "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md"
    review_path = followup_path if followup_path.is_file() else external_path
    if review_path.is_file():
        raw = review_path.read_text(encoding="utf-8")
        if "G185_ACCEPTED_WITH_STATED_BOUNDS" in raw or "G185_REPAIR_ACCEPTED" in raw:
            external = "ACCEPTED"
            checks["external_review_accepted"] = True
        elif "G185_REPAIR_REQUIRED" in raw:
            external = "REPAIR_REQUIRED"
        elif "G185_REFUTED" in raw:
            external = "REFUTED"
            checks["external_review_not_refuted"] = False
    technical_pass = all(checks.values())
    if not technical_pass:
        status = "FAIL"
    elif external == "ACCEPTED":
        status = "PASS"
    elif external == "REPAIR_REQUIRED":
        status = "TECHNICAL_PASS__EXTERNAL_REPAIR_FOLLOWUP_PENDING"
    else:
        status = "TECHNICAL_PASS__EXTERNAL_REVIEW_PENDING"
    result = {
        "audit": "G185_PACKAGE", "status": status, "technical_pass": technical_pass,
        "external_review": external, "checks": checks, "missing": missing,
        "source_failures": source_failures, "replays": replay,
    }
    if os.environ.get("UDT_WRITE_G185_PACKAGE") == "1":
        (HERE / "VERIFICATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if technical_pass and external != "REFUTED" else 1)


if __name__ == "__main__":
    main()

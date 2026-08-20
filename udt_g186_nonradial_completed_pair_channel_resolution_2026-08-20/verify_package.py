#!/usr/bin/env python3
"""Live package verifier for G186."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LANDING = (
    "NONRADIAL_COMPLETED_PAIR_CHANNELS_RESOLVE_WITHOUT_EXTRA_SCALAR"
    "__CLOCK_ANGULAR_NORM_CONTROLS_DEPTH"
    "__FULL_ANGULAR_GRAM_CONTROLS_TAPE_SHIFT_AND_LOCAL_SCREEN"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def replay(name: str) -> dict:
    completed = subprocess.run(
        [sys.executable, str(HERE / name)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    parsed = json.loads(completed.stdout) if completed.returncode == 0 else {}
    return {
        "returncode": completed.returncode,
        "status": parsed.get("status"),
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def main() -> None:
    required = [
        "PREREGISTRATION.md",
        "SOURCE_MANIFEST.tsv",
        "EXACT_DERIVATION.md",
        "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "AUDIT_REPORT.md",
        "EVIDENCE_GATES.md",
        "STATUS_LEDGER.tsv",
        "derive_nonradial_channels.py",
        "verify_nonradial_channels_independent.py",
        "run_catch_proofs.py",
        "FROZEN_CURRENT_SCIENTIFIC_PREMISES.tsv",
        "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md",
        "EXTERNAL_ADVERSARIAL_REVIEW_TRANSCRIPT.txt.gz",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "TRANSMISSION_RECORD.md",
    ]
    missing = [name for name in required if not (HERE / name).is_file()]

    source_failures = []
    manifest = HERE / "SOURCE_MANIFEST.tsv"
    if manifest.is_file():
        for line in manifest.read_text(encoding="utf-8").splitlines()[1:]:
            relative, expected, _role = line.split("\t", 2)
            source = (
                HERE / "FROZEN_CURRENT_SCIENTIFIC_PREMISES.tsv"
                if relative == "CURRENT_SCIENTIFIC_PREMISES.tsv"
                else ROOT / relative
            )
            if not source.is_file() or sha256(source) != expected:
                source_failures.append(relative)

    replays = {name: replay(name) for name in [
        "derive_nonradial_channels.py",
        "verify_nonradial_channels_independent.py",
        "run_catch_proofs.py",
    ]}
    stored = {}
    for name in ["PRODUCTION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json"]:
        path = HERE / name
        if path.is_file():
            stored[name] = json.loads(path.read_text(encoding="utf-8"))

    checks = {
        "all_required_files": not missing,
        "all_sources_immutable": not source_failures,
        "catch_count_18": stored.get("CATCH_PROOF_RESULT.json", {}).get("executable_catch_count") == 18,
        "landing_matches": stored.get("PRODUCTION_RESULT.json", {}).get("landing") == LANDING,
        "production_pass": stored.get("PRODUCTION_RESULT.json", {}).get("status") == "PASS",
        "independent_20000_pass": (
            stored.get("INDEPENDENT_VERIFICATION.json", {}).get("status") == "PASS"
            and stored.get("INDEPENDENT_VERIFICATION.json", {}).get("trials") == 20_000
        ),
        "semantic_guard_count_12": stored.get("CATCH_PROOF_RESULT.json", {}).get("semantic_guard_count") == 12,
        "live_replays_pass": all(item["returncode"] == 0 and item["status"] == "PASS"
                                 for item in replays.values()),
        "stored_results_match_live": all(
            json.loads(replays[script]["stdout"]) == stored[result]
            for script, result in [
                ("derive_nonradial_channels.py", "PRODUCTION_RESULT.json"),
                ("verify_nonradial_channels_independent.py", "INDEPENDENT_VERIFICATION.json"),
                ("run_catch_proofs.py", "CATCH_PROOF_RESULT.json"),
            ]
        ),
        "external_review_accepted": (
            "G186_ACCEPTED_WITH_STATED_BOUNDS"
            in (HERE / "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md").read_text(encoding="utf-8")
            if (HERE / "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md").is_file()
            else False
        ),
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    print(json.dumps({
        "audit": "G186_PACKAGE",
        "checks": checks,
        "missing": missing,
        "replays": replays,
        "source_failures": source_failures,
        "status": status,
    }, indent=2, sort_keys=True))
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

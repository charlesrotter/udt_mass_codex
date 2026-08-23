#!/usr/bin/env python3
"""Build a sealed read-only G226 adversarial-review intake under /tmp."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.resolve()
PREREGISTRATION_COMMITS = (
    "1f60deb0",
    "35d33b99",
)
PACKAGE_FILES = (
    "MAP.md",
    "OBSERVATION.md",
    "PONDER.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "derive_null_chain_conformal_symplectic.py",
    "verify_null_chain_conformal_symplectic_independent.py",
    "run_catch_proofs.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "VERIFICATION_RESULT.json",
    "CONTROL_ATLAS.tsv",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "verify_package.py",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "FRESH_ADVERSARIAL_REVIEW.md",
    "REPAIR_PREREGISTRATION.md",
    "REPAIR_FOLLOWUP_REQUEST.md",
    "build_review_intake.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_bytes(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=REPO, check=True, capture_output=True).stdout


def main() -> None:
    prereg_fulls = [git_bytes("rev-parse", commit).decode().strip() for commit in PREREGISTRATION_COMMITS]

    intake = Path(tempfile.mkdtemp(prefix="udt_g226_phase_review_", dir="/tmp"))
    payloads: list[tuple[str, Path]] = []

    for name in PACKAGE_FILES:
        source = ROOT / name
        if not source.is_file():
            raise FileNotFoundError(source)
        relative = Path("g226_package") / name
        destination = intake / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        payloads.append((str(relative), destination))

    for prereg_full in prereg_fulls:
        commit_relative = Path("git_commit_objects") / f"{prereg_full}.commit"
        commit_destination = intake / commit_relative
        commit_destination.parent.mkdir(parents=True, exist_ok=True)
        commit_destination.write_bytes(git_bytes("cat-file", "commit", prereg_full))
        payloads.append((str(commit_relative), commit_destination))

    with (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(source_rows) != 13:
        raise RuntimeError("expected 13 frozen sources")
    for row in source_rows:
        source = (REPO / row["path"]).resolve()
        if not source.is_relative_to(REPO):
            raise RuntimeError(f"source path escape: {row['path']}")
        if digest(source) != row["sha256"]:
            raise RuntimeError(f"source drift: {row['path']}")
        relative = Path("frozen_sources") / row["path"]
        destination = intake / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        payloads.append((str(relative), destination))

    manifest_path = intake / "PAYLOAD_MANIFEST.tsv"
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("sha256", "path"))
        for relative, destination in sorted(payloads):
            writer.writerow((digest(destination), relative))

    scope = {
        "status": "SEALED_READ_ONLY_REVIEW_INTAKE",
        "package": "G226",
        "preregistration_commit": prereg_fulls[0],
        "repair_preregistration_commit": prereg_fulls[1],
        "sealed_commit_objects": len(prereg_fulls),
        "package_payloads": len(PACKAGE_FILES),
        "frozen_source_payloads": len(source_rows),
        "listed_payloads": len(payloads),
        "total_files_including_manifest_and_scope": len(payloads) + 2,
        "reviewer": "external Codex gpt-5.4",
        "allowed": [
            "inspect only this sealed intake",
            "run bounded read-only checks",
            "run the registered /dev/null no-persistent-output replay",
        ],
        "forbidden": ["edit files", "continue the research"],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    for path in intake.rglob("*"):
        if path.is_file():
            path.chmod(0o444)
        elif path.is_dir():
            path.chmod(0o555)
    intake.chmod(0o555)

    print(f"SEALED_INTAKE={intake}")
    print(f"LISTED_PAYLOADS={len(payloads)}")
    print(f"TOTAL_FILES={len(payloads) + 2}")
    print(f"REVIEW_SCOPE_SHA256={digest(scope_path)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build a sealed read-only G225 review intake under /tmp."""

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
FIXED_RESULT_COMMIT = "465991dd"
R1_PREREGISTRATION_COMMIT = "78818a4818fc20f2e45efbec8b844772f6901cab"
R1_IMPLEMENTATION_COMMIT = "6db43e9606acce0bcfc41a5e7557d9f1c514d292"
R2_PREREGISTRATION_COMMIT = "857b5277102e7ed874604b68a59d5cd32f2635ee"

PACKAGE_FILES = (
    "MAP.md",
    "OBSERVATION.md",
    "PONDER.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "derive_shared_event_normal_screen_carry.py",
    "verify_shared_event_normal_screen_independent.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CONTROL_ATLAS.tsv",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "run_catch_proofs.py",
    "CATCH_PROOF_RESULT.json",
    "VERIFICATION_RESULT.json",
    "verify_package.py",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "FRESH_ADVERSARIAL_REVIEW.md",
    "REPAIR_PREREGISTRATION.md",
    "REPAIR_FOLLOWUP_REQUEST.md",
    "REPAIR_FOLLOWUP_REVIEW.md",
    "REPAIR_R2_PREREGISTRATION.md",
    "FINAL_REPAIR_FOLLOWUP_REQUEST.md",
    "FINAL_REPAIR_FOLLOWUP_REVIEW.md",
    "build_review_intake.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def full_commit(revision: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", revision],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def direct_parent(revision: str) -> str:
    return full_commit(f"{revision}^")


def require_ancestor(ancestor: str, descendant: str) -> None:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=REPO,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"required ancestry absent: {ancestor} -> {descendant}")


def main() -> None:
    head = full_commit("HEAD")
    require_ancestor(FIXED_RESULT_COMMIT, head)
    require_ancestor(R1_PREREGISTRATION_COMMIT, R1_IMPLEMENTATION_COMMIT)
    require_ancestor(R1_IMPLEMENTATION_COMMIT, head)
    require_ancestor(R2_PREREGISTRATION_COMMIT, head)
    if direct_parent(R1_IMPLEMENTATION_COMMIT) != R1_PREREGISTRATION_COMMIT:
        raise RuntimeError("R1 implementation is not the direct child of R1 preregistration")
    if direct_parent(head) != R2_PREREGISTRATION_COMMIT:
        raise RuntimeError("intake builder HEAD is not the direct child of R2 preregistration")

    intake = Path(tempfile.mkdtemp(prefix="udt_g225_screen_review_", dir="/tmp"))
    payloads: list[tuple[str, Path]] = []

    for name in PACKAGE_FILES:
        source = ROOT / name
        if not source.is_file():
            raise FileNotFoundError(source)
        relative = Path("g225_package") / name
        destination = intake / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        payloads.append((str(relative), destination))

    commit_objects = (
        R1_PREREGISTRATION_COMMIT,
        R1_IMPLEMENTATION_COMMIT,
        R2_PREREGISTRATION_COMMIT,
        head,
    )
    for commit in commit_objects:
        raw = subprocess.run(
            ["git", "cat-file", "commit", commit],
            cwd=REPO,
            check=True,
            capture_output=True,
        ).stdout
        relative = Path("git_commit_objects") / f"{commit}.commit"
        destination = intake / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)
        payloads.append((str(relative), destination))

    with (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(source_rows) != 9:
        raise RuntimeError("expected nine frozen sources")
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
        "fixed_result_commit": FIXED_RESULT_COMMIT,
        "intake_builder_head": head,
        "r1_preregistration_commit": R1_PREREGISTRATION_COMMIT,
        "r1_implementation_commit": R1_IMPLEMENTATION_COMMIT,
        "r2_preregistration_commit": R2_PREREGISTRATION_COMMIT,
        "sealed_commit_objects": len(commit_objects),
        "package_payloads": len(PACKAGE_FILES),
        "frozen_source_payloads": len(source_rows),
        "listed_payloads": len(payloads),
        "total_files_including_manifest_and_scope": len(payloads) + 2,
        "reviewer": "external Codex gpt-5.4",
        "allowed": [
            "inspect only this sealed intake",
            "run bounded read-only checks",
            "run the registered no-write replay",
        ],
        "forbidden": [
            "edit files",
            "continue the research",
            "inspect anything outside the intake",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Seal payload bytes against accidental reviewer writes.
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

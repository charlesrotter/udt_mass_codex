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
    "build_review_intake.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    head = subprocess.run(
        ["git", "rev-parse", "--short=8", "HEAD"],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", FIXED_RESULT_COMMIT, "HEAD"],
        cwd=REPO,
        check=False,
    )
    if ancestry.returncode != 0:
        raise RuntimeError(f"fixed G225 result {FIXED_RESULT_COMMIT} is not an ancestor of {head}")

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

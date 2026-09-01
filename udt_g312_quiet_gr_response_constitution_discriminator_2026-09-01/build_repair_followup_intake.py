#!/usr/bin/env python3
"""Build the sealed self-contained G312 R1 repair-only follow-up intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
PACKAGE_FILES = (
    "CATCH_PROOF_RESULT.json",
    "DERIVATION_RESULT.json",
    "EVIDENCE_GATES.md",
    "EXACT_DERIVATION.md",
    "EXTERNAL_REVIEW_REQUEST.md",
    "EXTERNAL_REVIEW_RESPONSE.md",
    "EXTERNAL_REVIEW_TRANSMISSION.md",
    "INDEPENDENT_VERIFICATION.json",
    "LAY_REPORT.md",
    "MAP.md",
    "PACKAGE_VERIFICATION_RESULT.json",
    "PONDER.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "PREREGISTRATION_ANCESTRY.md",
    "REPAIR_ANCESTRY.md",
    "REPAIR_FOLLOWUP_REQUEST.md",
    "REPAIR_PREREGISTRATION.md",
    "RUN_RECORD.md",
    "SOURCE_SCOPE.tsv",
    "STATUS_LEDGER.tsv",
    "build_repair_followup_intake.py",
    "build_review_intake.py",
    "derive_response_constitution.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "verify_response_constitution_independent.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g312_repair_followup_", dir="/tmp"))
    package_target = intake / "package"
    package_target.mkdir()
    for name in PACKAGE_FILES:
        source = PACKAGE / name
        if not source.is_file():
            raise SystemExit(f"missing package file: {source}")
        shutil.copy2(source, package_target / name)

    sources_target = intake / "sources"
    for row in csv.DictReader(
        (PACKAGE / "SOURCE_SCOPE.tsv").open(encoding="utf-8", newline=""), delimiter="\t"
    ):
        source = ROOT / row["path"]
        target = sources_target / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        if row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv":
            shutil.copy2(source, intake / "CURRENT_SCIENTIFIC_PREMISES.tsv")

    replay = subprocess.run(
        [sys.executable, "-S", str(package_target / "verify_package.py")],
        cwd=package_target,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if replay.returncode:
        raise SystemExit(f"sealed aggregate replay failed: {replay.stderr}")
    replay_result = json.loads(replay.stdout)

    scope = {
        "question": "G312 R1 intake-self-containment repair-only follow-up",
        "mode": "read-only repair-only follow-up review",
        "repair": "R1_intake_self_contained_aggregate_replay",
        "retained_landing": "TWO_OR_MORE_INDEPENDENT_NEW_PREMISES_ARE_REQUIRED",
        "sealed_replay": replay_result,
        "allowed": ["inspect intake", "run registered checks in writable ephemeral copy"],
        "forbidden": [
            "edit evidence",
            "continue research",
            "change scientific question or landing",
            "access repository or protected packages",
            "use internet or unsealed observations",
            "adopt either premise or select history scale source action matter model or X_max",
        ],
        "required_verdicts": [
            "G312_ACCEPTED_WITH_TWO_PREMISE_BOUNDARY",
            "G312_REPAIR_INCOMPLETE__LANDING_RETAINED",
            "G312_REPAIR_CHANGED_SCIENCE",
            "G312_FOLLOWUP_INCOMPLETE",
        ],
    }
    (intake / "REVIEW_SCOPE.json").write_text(
        json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    payloads = sorted(path for path in intake.rglob("*") if path.is_file())
    manifest = intake / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "bytes", "sha256"))
        for path in payloads:
            writer.writerow((path.relative_to(intake).as_posix(), path.stat().st_size, digest(path)))
    seal = intake / "REVIEW_MANIFEST.sha256"
    seal.write_text(f"{digest(manifest)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "intake": str(intake),
                "payloads": len(payloads),
                "total_files": len(payloads) + 2,
                "scope_sha256": digest(intake / "REVIEW_SCOPE.json"),
                "manifest_sha256": digest(manifest),
                "detached_seal_sha256": digest(seal),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

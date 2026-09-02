#!/usr/bin/env python3
"""Build a sealed, self-contained G324 repair-only follow-up intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PACKAGE_FILES = (
    "MAP.md",
    "PREMISE_LEDGER.tsv",
    "COMPLETENESS_MAP.md",
    "PREREGISTRATION.md",
    "PREREGISTRATION_ANCESTRY.md",
    "SOURCE_SCOPE.tsv",
    "SOURCE_MANIFEST.tsv",
    "SOURCE_NOTE.md",
    "GLS_PRIMARY_SOURCE_EVIDENCE.json",
    "REPLAY_COMMANDS.txt",
    "derive_taub_mghd.py",
    "verify_independent.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "verify_review_intake.py",
    "build_repair_followup_intake.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "PACKAGE_VERIFICATION_RESULT.json",
    "EXACT_DERIVATION.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "AUDIT_REPORT.md",
    "RUN_RECORD.md",
    "EXTERNAL_REVIEW_REQUEST.md",
    "EXTERNAL_REVIEW_RESPONSE.md",
    "EXTERNAL_REVIEW_FINAL_RESPONSE.md",
    "EXTERNAL_REVIEW_TRANSCRIPT.txt",
    "EXTERNAL_REVIEW_TRANSMISSION.md",
    "REPAIR_LEDGER.tsv",
    "REPAIR_FOLLOWUP_REQUEST.md",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    package = Path(__file__).resolve().parent
    repo = package.parent
    source_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()
    intake = Path(tempfile.mkdtemp(prefix="udt_g324_repair_followup_", dir="/tmp"))
    package_out = intake / "package"
    sources_out = intake / "sources"
    package_out.mkdir()

    payloads: list[Path] = []
    for name in PACKAGE_FILES:
        source = package / name
        if not source.is_file():
            raise FileNotFoundError(source)
        target = package_out / name
        shutil.copy2(source, target)
        payloads.append(target)

    with (package / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in source_rows:
        source = repo / row["relative_path"]
        if not source.is_file() or sha(source) != row["sha256"]:
            raise RuntimeError(f"source mismatch: {row['relative_path']}")
        target = sources_out / row["relative_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        payloads.append(target)

    scope = {
        "schema": "udt-g324-repair-followup-scope-v1",
        "source_commit": source_commit,
        "purpose": "read-only repair-only verification of G324 repairs R1-R3",
        "allowed": [
            "inspect only this sealed intake",
            "verify only registered repairs R1-R3 and the unchanged bounded scientific landing",
            "run registered checks in a writable ephemeral copy",
            "write the response outside evidence files",
        ],
        "forbidden": [
            "edit evidence files",
            "continue the research",
            "access the repository or protected packages",
            "use internet or unsealed observations",
            "change the scientific question",
            "select or canonize a law, history, topology, occupancy, scale, or X_max",
        ],
        "package_payload_count": len(PACKAGE_FILES),
        "source_payload_count": len(source_rows),
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")
    payloads.append(scope_path)

    subprocess.run(
        [sys.executable, "-S", str(package_out / "verify_package.py"),
         "--source-root", str(sources_out)],
        cwd=package_out,
        check=True,
        capture_output=True,
        text=True,
    )

    manifest = intake / "REVIEW_MANIFEST.tsv"
    lines = ["sha256\tbytes\trelative_path"]
    for path in sorted(payloads, key=lambda item: item.relative_to(intake).as_posix()):
        lines.append(f"{sha(path)}\t{path.stat().st_size}\t{path.relative_to(intake)}")
    manifest.write_text("\n".join(lines) + "\n")
    manifest_hash = sha(manifest)
    seal = intake / "REVIEW_MANIFEST.sha256"
    seal.write_text(f"{manifest_hash}  REVIEW_MANIFEST.tsv\n")

    subprocess.run(
        [sys.executable, "-S", str(package_out / "verify_review_intake.py")],
        cwd=package_out,
        check=True,
        capture_output=True,
        text=True,
    )

    result = {
        "intake": str(intake),
        "payload_count": len(payloads),
        "total_file_count": len(payloads) + 2,
        "review_scope_sha256": sha(scope_path),
        "review_manifest_sha256": manifest_hash,
        "detached_seal_sha256": sha(seal),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

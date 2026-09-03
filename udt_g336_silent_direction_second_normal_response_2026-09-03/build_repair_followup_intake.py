#!/usr/bin/env python3
"""Build the sealed dependency-free G336 R2 repair-follow-up intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
PREREG_COMMIT = "eba7a42a"
PACKAGE_FILES = (
    "MAP.md", "EXPLORATORY_MAP_NOTE.md", "PREREGISTRATION.md",
    "PREREGISTRATION_SCOPE_REPAIR.md", "PREREGISTRATION_EXTERNAL_REPAIR.md",
    "PREMISE_LEDGER.tsv", "COMPLETENESS_MAP.md", "SOURCE_SCOPE.tsv",
    "SOURCE_MANIFEST.tsv", "EXECUTION_NOTE.md", "derive_silent_second_response.py",
    "verify_silent_second_response_independent.py", "run_catch_proofs.py",
    "verify_package.py", "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json", "PACKAGE_VERIFICATION_RESULT.json", "EXACT_DERIVATION.md",
    "LAY_REPORT.md", "STATUS_LEDGER.tsv", "AUDIT_REPORT.md", "EVIDENCE_GATES.md",
    "COMMANDS.md", "RUN_RECORD.md", "EXTERNAL_REVIEW_REQUEST.md",
    "EXTERNAL_REVIEW_RESPONSE.md", "EXTERNAL_REVIEW_TRANSMISSION.md",
    "EXTERNAL_REPAIR_FOLLOWUP.md",
    "REPAIR_IMPLEMENTATION.md", "REPAIR_FOLLOWUP_REQUEST.md",
    "build_review_intake.py", "build_repair_followup_intake.py", "verify_review_intake.py",
)


def digest_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def frozen_source(relative: Path, expected_bytes: int, expected_digest: str) -> bytes:
    candidate = (REPO / relative).resolve()
    if not candidate.is_relative_to(REPO.resolve()):
        raise SystemExit(f"source escaped repository: {relative}")
    payload = candidate.read_bytes() if candidate.is_file() else b""
    if len(payload) == expected_bytes and digest_bytes(payload) == expected_digest:
        return payload
    replay = subprocess.run(
        ["git", "show", f"{PREREG_COMMIT}:{relative.as_posix()}"],
        cwd=REPO,
        capture_output=True,
        check=False,
    )
    if replay.returncode:
        raise SystemExit(f"frozen source unavailable: {relative}")
    if len(replay.stdout) != expected_bytes or digest_bytes(replay.stdout) != expected_digest:
        raise SystemExit(f"frozen source mismatch: {relative}")
    return replay.stdout


def main() -> None:
    rows = list(csv.DictReader(
        (PACKAGE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"), delimiter="\t"
    ))
    intake = Path(tempfile.mkdtemp(prefix="udt_g336_repair_followup_", dir="/tmp"))
    package_out = intake / "package"
    source_out = intake / "sources"
    package_out.mkdir()
    source_out.mkdir()
    copied: list[Path] = []

    for filename in PACKAGE_FILES:
        source = PACKAGE / filename
        if not source.is_file():
            raise SystemExit(f"missing package file: {filename}")
        target = package_out / filename
        shutil.copy2(source, target)
        copied.append(target)

    for row in rows:
        relative = Path(row["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise SystemExit(f"unsafe source path: {relative}")
        payload = frozen_source(relative, int(row["bytes"]), row["sha256"])
        target = source_out / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        copied.append(target)

    scope = {
        "review": "read-only repair-only G336 R2 follow-up review",
        "allowed": [
            "inspect only this corrected sealed intake",
            "verify only the preregistered G336 R2 wording repair",
            "verify the unchanged bounded scientific landing",
            "run registered no-write replays or bounded checks in a writable ephemeral copy",
        ],
        "forbidden": [
            "edit evidence files", "continue the research", "change the scientific question",
            "access repository or protected packages", "use internet or unsealed observations",
            "select topology branch history occupancy action source matter mass fit scale or Xmax",
            "promote provisional equations or results into canon",
        ],
        "allowed_verdicts": [
            "REPAIRS_ACCEPTED__G336_BOUNDED_SILENT_SECOND_JET_RETAINED",
            "REPAIRS_INCOMPLETE__G336_BOUNDED_SILENT_SECOND_JET_RETAINED",
            "REFUTE__G336_BOUNDED_SILENT_SECOND_JET",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    copied.append(scope_path)

    lines = ["sha256\tbytes\tpath"]
    for path in sorted(copied, key=lambda item: item.relative_to(intake).as_posix()):
        lines.append(
            f"{digest(path)}\t{path.stat().st_size}\t{path.relative_to(intake).as_posix()}"
        )
    manifest = intake / "REVIEW_MANIFEST.tsv"
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    seal = intake / "REVIEW_MANIFEST.sha256"
    seal.write_text(f"{digest(manifest)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")
    print(json.dumps({
        "intake": str(intake),
        "file_count": len(copied) + 2,
        "payload_count": len(copied),
        "scope_sha256": digest(scope_path),
        "manifest_sha256": digest(manifest),
        "seal_sha256": digest(seal),
    }, sort_keys=True))


if __name__ == "__main__":
    main()

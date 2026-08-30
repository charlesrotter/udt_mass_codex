#!/usr/bin/env python3
"""Build a sealed G302 repair-only follow-up intake without transmitting it."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
PACKAGE_FILES = (
    "MAP.md", "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION_ANCESTRY.md",
    "REPAIR_PREREGISTRATION.md", "SOURCE_MANIFEST.tsv", "EXTERNAL_REVIEW_REQUEST.md",
    "EXTERNAL_REVIEW_GPT54.md", "EXTERNAL_REVIEW_TRANSMISSION.md", "REPAIR_FOLLOWUP_REQUEST.md",
    "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "LAY_REPORT.md", "EVIDENCE_GATES.md",
    "STATUS_LEDGER.tsv", "DOMAIN_CLASSIFICATION.tsv", "COMMANDS.md", "RUN_RECORD.md",
    "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
    "DOMAIN_CENSUS_VERIFICATION.json", "DOMAIN_CATCH_PROOF_RESULT.json",
    "PACKAGE_VERIFICATION_RESULT.json", "derive_trace_span_and_geometry.py",
    "verify_independent.py", "run_catch_proofs.py", "verify_domain_census_independent.py",
    "run_domain_catch_proofs.py", "verify_package.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_payload(intake: Path, source: Path, relative: Path, payloads: list[Path]) -> None:
    target = intake / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    payloads.append(target.relative_to(intake))


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g302_repair_followup_", dir="/tmp"))
    payloads: list[Path] = []
    for name in PACKAGE_FILES:
        copy_payload(intake, PACKAGE / name, Path(PACKAGE.name) / name, payloads)

    for line in (PACKAGE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        if not line:
            continue
        expected, relative = line.split("\t")
        source = ROOT / relative
        if digest(source) != expected:
            raise RuntimeError(f"source drift: {relative}")
        if not (intake / relative).exists():
            copy_payload(intake, source, Path(relative), payloads)

    scope = {
        "review": "G302 read-only repair-only domain-certification follow-up",
        "mode": "read-only repair-only",
        "allowed": (
            "verify only preregistered R1/R2 repairs, unchanged scientific landing, and registered "
            "checks in a writable ephemeral copy"
        ),
        "forbidden": "edit evidence; change the scientific question; continue the research",
        "package": PACKAGE.name,
        "payload_count": len(payloads),
        "repair_preregistration_commit": "3c08bb91",
        "repair_commit": "e85fdb2a",
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    payloads.append(scope_path.relative_to(intake))

    manifest = intake / "REVIEW_MANIFEST.tsv"
    rows = ["sha256\tbytes\tpath"]
    for relative in sorted(payloads, key=str):
        path = intake / relative
        rows.append(f"{digest(path)}\t{path.stat().st_size}\t{relative}")
    manifest.write_text("\n".join(rows) + "\n", encoding="utf-8")
    seal = intake / "REVIEW_MANIFEST.sha256"
    seal.write_text(f"{digest(manifest)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")

    print(json.dumps({
        "intake": str(intake),
        "files": len(payloads) + 2,
        "manifest_payloads": len(payloads),
        "scope_sha256": digest(scope_path),
        "manifest_sha256": digest(manifest),
        "seal_sha256": digest(seal),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()


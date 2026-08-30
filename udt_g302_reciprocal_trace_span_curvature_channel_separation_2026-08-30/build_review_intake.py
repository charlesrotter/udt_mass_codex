#!/usr/bin/env python3
"""Build a sealed G302 review intake without transmitting it."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
PACKAGE_FILES = (
    "MAP.md",
    "PREREGISTRATION.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION_ANCESTRY.md",
    "SOURCE_MANIFEST.tsv",
    "EVIDENCE_GATES.md",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "DOMAIN_CLASSIFICATION.tsv",
    "STATUS_LEDGER.tsv",
    "COMMANDS.md",
    "RUN_RECORD.md",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "PACKAGE_VERIFICATION_RESULT.json",
    "derive_trace_span_and_geometry.py",
    "verify_independent.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "EXTERNAL_REVIEW_REQUEST.md",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_payload(intake: Path, source: Path, relative: Path, payloads: list[Path]) -> None:
    target = intake / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    payloads.append(target.relative_to(intake))


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g302_review_", dir="/tmp"))
    payloads: list[Path] = []

    for name in PACKAGE_FILES:
        copy_payload(intake, PACKAGE / name, Path(PACKAGE.name) / name, payloads)

    lines = (PACKAGE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()
    for line in lines[1:]:
        if not line:
            continue
        expected, relative = line.split("\t")
        source = ROOT / relative
        if digest(source) != expected:
            raise RuntimeError(f"source drift: {relative}")
        target = intake / relative
        if not target.exists():
            copy_payload(intake, source, Path(relative), payloads)

    scope = {
        "review": "fresh adversarial G302 reciprocal trace-span and curvature-channel classification",
        "mode": "read-only",
        "allowed": "inspect only this intake; run registered checks in a writable ephemeral copy",
        "forbidden": (
            "edit evidence; continue research; access repository or protected packages; use internet; "
            "inspect unsealed observational outcomes; adopt or select a field equation, source, action, "
            "matter or mass interpretation, scale, history, physical query population, boundary, or X_max"
        ),
        "package": PACKAGE.name,
        "payload_count": len(payloads),
        "preregistration_commit": "887a91ad",
        "internal_result_commit": "b218f038",
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

    print(
        json.dumps(
            {
                "intake": str(intake),
                "files": len(payloads) + 2,
                "manifest_payloads": len(payloads),
                "scope_sha256": digest(scope_path),
                "manifest_sha256": digest(manifest),
                "seal_sha256": digest(seal),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

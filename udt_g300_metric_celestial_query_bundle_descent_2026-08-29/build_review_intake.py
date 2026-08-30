#!/usr/bin/env python3
"""Build a sealed, read-only-review intake for G300 without transmitting it."""

import hashlib
import json
from pathlib import Path
import shutil
import tempfile


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent

PACKAGE_FILES = (
    "MAP.md",
    "PREREGISTRATION.md",
    "PREREGISTRATION_SCOPE_REPAIR.md",
    "PREMISE_LEDGER.tsv",
    "SOURCE_MANIFEST.tsv",
    "EVIDENCE_GATES.md",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "COMMANDS.md",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "derive_celestial_query_bundle.py",
    "verify_celestial_query_bundle_independent.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "EXTERNAL_REVIEW_REQUEST.md",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    intake = Path(tempfile.mkdtemp(prefix="udt_g300_review_", dir="/tmp"))
    payloads = []

    for name in PACKAGE_FILES:
        source = PACKAGE / name
        target = intake / PACKAGE.name / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        payloads.append(target.relative_to(intake))

    for line in (PACKAGE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        expected, relative = line.split("\t")
        source = ROOT / relative
        if digest(source) != expected:
            raise RuntimeError(f"source drift: {relative}")
        target = intake / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        payloads.append(target.relative_to(intake))

    for relative in ("CURRENT_SCIENTIFIC_PREMISES.tsv", "founding.md"):
        target = intake / relative
        if target.exists():
            continue
        shutil.copy2(ROOT / relative, target)
        payloads.append(target.relative_to(intake))

    scope = {
        "review": "fresh adversarial G300 celestial query bundle",
        "mode": "read-only",
        "allowed": "inspect only this intake; run registered checks in a writable ephemeral copy",
        "forbidden": "edit evidence; continue research; access repository/protected packages; use internet",
        "package": PACKAGE.name,
        "payload_count": len(payloads),
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    payloads.append(scope_path.relative_to(intake))

    manifest = intake / "REVIEW_MANIFEST.tsv"
    rows = ["sha256\tbytes\tpath"]
    for relative in sorted(payloads, key=lambda p: str(p)):
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

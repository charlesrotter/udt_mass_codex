#!/usr/bin/env python3
"""Build a sealed, self-contained G296 adversarial-review intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    destination = Path(tempfile.mkdtemp(prefix="udt_g296_review_", dir="/tmp"))
    package_files = [
        "MAP.md", "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "SOURCE_MANIFEST.tsv",
        "ADVERSARIAL_REVIEW_REQUEST.md", "ARCHITECTURE_CLASSIFICATION.tsv", "EXACT_DERIVATION.md",
        "LAY_REPORT.md", "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md", "COMMANDS.md", "AUDIT_REPORT.md",
        "derive_native_residual_order_map.py", "verify_native_residual_independent.py",
        "run_catch_proofs.py", "verify_package.py", "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json", "PACKAGE_VERIFICATION_RESULT.json",
        "EXTERNAL_REVIEW_GPT54.md", "EXTERNAL_REVIEW_TRANSMISSION.md", "REPAIR_PREREGISTRATION.md",
        "PREREG_ANCESTRY_PROOF.json", "verify_prereg_ancestry_proof.py",
    ]
    copied: list[Path] = []
    package_root = destination / HERE.name
    for name in package_files:
        src = HERE / name
        assert src.is_file(), src
        dst = package_root / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(dst)

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            src = ROOT / row["path"]
            assert digest(src) == row["sha256"]
            dst = destination / row["path"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied.append(dst)

    scope = {
        "question": "Repair-only follow-up review of G296 R1-R3 and the unchanged bounded scientific landing",
        "preregistration_commit": "f7a050f0",
        "restrictions": [
            "inspect only this intake",
            "run checks only in a writable ephemeral copy",
            "do not edit evidence files",
            "do not continue the research",
            "do not promote any candidate residual into a UDT law",
            "verify only preregistered repairs R1-R3 and the unchanged bounded scientific landing",
        ],
        "manifest_payload_count": len(copied) + 1,
    }
    scope_path = destination / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    copied.append(scope_path)

    manifest_path = destination / "REVIEW_MANIFEST.tsv"
    rows = []
    for path in sorted(copied):
        rows.append((digest(path), path.relative_to(destination).as_posix(), path.stat().st_size))
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("sha256", "path", "bytes"))
        writer.writerows(rows)
    seal_path = destination / "REVIEW_MANIFEST.sha256"
    seal_path.write_text(f"{digest(manifest_path)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")

    print(json.dumps({
        "intake": str(destination),
        "file_count": len(copied) + 2,
        "manifest_payloads": len(rows),
        "scope_sha256": digest(scope_path),
        "manifest_sha256": digest(manifest_path),
        "seal_sha256": digest(seal_path),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build a sealed, read-only G167 review intake without transmitting it."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g167_pair_pullback_review_"))
    package_target = intake / HERE.name
    package_target.mkdir()

    package_names = [
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "AUDIT_REPORT.md",
        "CATCH_PROOF_RESULT.json",
        "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXACT_DERIVATION.md",
        "EXTERNAL_ADVERSARIAL_REVIEW.md",
        "INDEPENDENT_RESULT.json",
        "LAY_REPORT.md",
        "PREREGISTRATION.md",
        "REPAIR_PREREGISTRATION.md",
        "REPOSITORY_GATE_RECORD.json",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "VERIFICATION_RESULT.json",
        "derive_primary_metric_pair_pullback.py",
        "run_catch_proofs.py",
        "verify_package.py",
        "verify_primary_metric_pair_pullback_independent.py",
    ]
    copied: list[Path] = []
    for name in package_names:
        source = HERE / name
        target = package_target / name
        shutil.copy2(source, target)
        copied.append(target)

    source_rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    for row in source_rows:
        source = ROOT / row["path"]
        # Preserve the repository-relative layout expected by every packaged
        # verifier, whose ROOT is the sealed intake when executed there.
        target = intake / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)

    manifest_rows = []
    for path in sorted(copied):
        relative = path.relative_to(intake).as_posix()
        manifest_rows.append({"path": relative, "sha256": digest(path)})

    review_manifest = intake / "REVIEW_MANIFEST.tsv"
    with review_manifest.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["sha256", "path"], delimiter="\t")
        writer.writeheader()
        for row in manifest_rows:
            writer.writerow({"sha256": row["sha256"], "path": row["path"]})

    tree_material = "".join(f"{row['path']}\t{row['sha256']}\n" for row in manifest_rows)
    scope = {
        "package": HERE.name,
        "payload_file_count": len(manifest_rows),
        "manifest_included_separately": True,
        "tree_digest_sha256": hashlib.sha256(tree_material.encode()).hexdigest(),
        "restrictions": [
            "read-only",
            "no edits",
            "no continued research",
            "no internet",
            "no repository access outside intake",
            "no protected package access",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")

    for path in intake.rglob("*"):
        if path.is_file():
            os.chmod(path, 0o444)
    for path in sorted((p for p in intake.rglob("*") if p.is_dir()), reverse=True):
        os.chmod(path, 0o555)
    os.chmod(intake, 0o555)

    print(f"intake={intake}")
    print(f"payload_files={len(manifest_rows)}")
    print(f"total_files={len(manifest_rows) + 2}")
    print(f"review_scope_sha256={digest(scope_path)}")
    print(f"tree_digest_sha256={scope['tree_digest_sha256']}")


if __name__ == "__main__":
    main()

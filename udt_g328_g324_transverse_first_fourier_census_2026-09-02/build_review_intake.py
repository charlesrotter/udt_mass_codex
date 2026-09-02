#!/usr/bin/env python3
"""Build a sealed, self-contained, read-only G328 adversarial-review intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE_FILES = (
    "MAP.md", "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "COMPLETENESS_MAP.md",
    "EXACT_DERIVATION.md", "LAY_REPORT.md", "EVIDENCE_GATES.md", "STATUS_LEDGER.tsv",
    "RUN_RECORD.md", "REPLAY_COMMANDS.txt", "SOURCE_SCOPE.tsv", "SOURCE_MANIFEST.tsv",
    "sealed_runtime.py", "VENDORED_SYMPY_RUNTIME.zip", "VENDORED_RUNTIME_MANIFEST.json",
    "derive_transverse_modes.py", "verify_independent.py", "run_catch_proofs.py",
    "verify_package.py", "verify_preregistration_proof.py", "verify_review_intake.py",
    "build_review_intake.py", "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json", "PACKAGE_VERIFICATION_RESULT.json",
    "PREREGISTRATION_COMMIT_OBJECT.txt", "PREREGISTRATION_CHANGESET.tsv",
    "PREREGISTRATION_TREE.tsv", "ADVERSARIAL_REVIEW_REQUEST.md", "AUDIT_REPORT.md",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    package = Path(__file__).resolve().parent
    repository = package.parent
    destination = Path(tempfile.mkdtemp(prefix="udt_g328_review_", dir="/tmp"))
    payloads: list[Path] = []

    for name in PACKAGE_FILES:
        source = package / name
        assert source.is_file(), source
        target = destination / name
        shutil.copy2(source, target)
        payloads.append(target)

    with (package / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in source_rows:
        source = repository / row["path"]
        assert source.is_file(), source
        target = destination / "sources" / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        payloads.append(target)

    scope_path = destination / "REVIEW_SCOPE.json"
    scope = {
        "schema": "udt-g328-fresh-review-scope-v1",
        "question": "fresh adversarial review of bounded G328 transverse Fourier census",
        "manifest_payload_count": len(payloads) + 1,
        "evidence_write_allowed": False,
        "research_continuation_allowed": False,
        "repository_access_allowed": False,
        "protected_package_access_allowed": False,
        "internet_browsing_allowed": False,
        "download_or_install_allowed": False,
        "ephemeral_copy_checks_allowed": True,
        "new_physics_import_allowed": False,
        "law_history_scale_selection_allowed": False,
        "scientific_landing_change_requires_explicit_defect": True,
    }
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    payloads.append(scope_path)

    manifest = destination / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("relative_path", "bytes", "sha256"))
        for path in sorted(payloads, key=lambda item: item.relative_to(destination).as_posix()):
            writer.writerow((
                path.relative_to(destination).as_posix(), path.stat().st_size, digest(path)
            ))
    seal = destination / "REVIEW_MANIFEST.sha256"
    seal.write_text(digest(manifest) + "\n", encoding="utf-8")

    for path in destination.rglob("*"):
        path.chmod(0o555 if path.is_dir() else 0o444)
    destination.chmod(0o555)

    print(json.dumps({
        "intake": str(destination),
        "manifest_payload_count": len(payloads),
        "total_file_count": len(payloads) + 2,
        "scope_sha256": digest(scope_path),
        "manifest_sha256": digest(manifest),
        "detached_seal_sha256": digest(seal),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

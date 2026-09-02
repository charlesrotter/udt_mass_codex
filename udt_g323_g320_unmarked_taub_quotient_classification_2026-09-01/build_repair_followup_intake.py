#!/usr/bin/env python3
"""Build a sealed, self-contained G323 repair-only follow-up intake under /tmp."""

import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PACKAGE_FILES = (
    "MAP.md", "PREMISE_LEDGER.tsv", "COMPLETENESS_MAP.md", "PREREGISTRATION.md",
    "PREREGISTRATION_ANCESTRY.md", "SOURCE_SCOPE.tsv", "REPLAY_COMMANDS.txt",
    "derive_unmarked_quotients.py", "verify_independent.py", "run_catch_proofs.py",
    "verify_package.py", "verify_review_intake.py", "build_repair_followup_intake.py",
    "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
    "PACKAGE_VERIFICATION_RESULT.json", "QUOTIENT_ATLAS.tsv", "INDEPENDENT_FAILURE_AND_REPAIR.md",
    "EXACT_DERIVATION.md", "LAY_REPORT.md", "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md",
    "AUDIT_REPORT.md", "RUN_RECORD.md", "EXTERNAL_REVIEW_REQUEST.md",
    "EXTERNAL_REVIEW_RESPONSE.md", "EXTERNAL_REVIEW_TRANSCRIPT.txt",
    "EXTERNAL_REVIEW_TRANSMISSION.md", "REPAIR_LEDGER.tsv", "REPAIR_FOLLOWUP_REQUEST.md",
)
SOURCE_FILES = (
    "udt_g319_ratio_free_noncmc_constraint_descent_2026-09-01/EXACT_DERIVATION.md",
    "udt_g320_g319_physical_initial_geometry_quotient_audit_2026-09-01/EXACT_DERIVATION.md",
    "udt_g321_g320_local_cauchy_development_uniqueness_2026-09-01/EXACT_DERIVATION.md",
    "udt_g322_g321_maximal_globally_hyperbolic_development_2026-09-01/AUDIT_REPORT.md",
    "CURRENT_SCIENTIFIC_PREMISES.md",
)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    source_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout.strip()
    root = Path(tempfile.mkdtemp(prefix="udt_g323_repair_followup_", dir="/tmp"))
    package_target = root / "package"
    source_target = root / "sources"
    package_target.mkdir()
    source_target.mkdir()

    copied = []
    for name in PACKAGE_FILES:
        source = HERE / name
        if not source.is_file():
            raise FileNotFoundError(source)
        target = package_target / name
        shutil.copy2(source, target)
        copied.append(target)
    for relative in SOURCE_FILES:
        source = REPO / relative
        if not source.is_file():
            raise FileNotFoundError(source)
        target = source_target / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)

    scope = {
        "schema": "udt-g323-repair-followup-scope-v1",
        "source_commit": source_commit,
        "purpose": "read-only repair-only follow-up review of bounded G323 repairs R1-R4",
        "allowed": [
            "inspect only this sealed intake",
            "verify only registered repairs R1-R4 and the retained bounded landing",
            "run registered checks in a writable ephemeral copy",
            "write the review response outside evidence files",
        ],
        "forbidden": [
            "edit evidence files",
            "continue the research",
            "access the repository or protected packages",
            "use internet or unsealed observations",
            "select or canonize a law, topology, history, scale, occupancy, or X_max",
        ],
        "package_payload_count": len(PACKAGE_FILES),
        "source_payload_count": len(SOURCE_FILES),
    }
    scope_path = root / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    copied.append(scope_path)

    manifest_path = root / "REVIEW_MANIFEST.tsv"
    rows = []
    for path in sorted(copied, key=lambda item: item.relative_to(root).as_posix()):
        rows.append({
            "path": path.relative_to(root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=("path", "bytes", "sha256"), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    manifest_digest = sha256(manifest_path)
    seal_path = root / "REVIEW_MANIFEST.sha256"
    seal_path.write_text(f"{manifest_digest}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")

    subprocess.run(
        ["python3", "-S", str(package_target / "verify_review_intake.py")],
        cwd=root,
        check=True,
    )
    print(f"intake={root}")
    print(f"manifest_payloads={len(rows)}")
    print(f"total_files={len(rows) + 2}")
    print(f"scope_sha256={sha256(scope_path)}")
    print(f"manifest_sha256={manifest_digest}")
    print(f"detached_seal_sha256={sha256(seal_path)}")


if __name__ == "__main__":
    main()

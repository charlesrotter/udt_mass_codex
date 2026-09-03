#!/usr/bin/env python3
"""Build a sealed, dependency-free G330 external-review intake under /tmp."""

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
SOURCE_ROOT = REPO / "sources" if (REPO / "sources").is_dir() else REPO
FROZEN_SOURCE_COMMIT = "add519ae"
PACKAGE_FILES = (
    "MAP.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "COMPLETENESS_MAP.md",
    "derive_berger_hopf.py", "verify_berger_hopf_independent.py", "run_catch_proofs.py",
    "verify_package.py", "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json", "PACKAGE_VERIFICATION_RESULT.json", "EXACT_DERIVATION.md",
    "LAY_REPORT.md", "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md", "RUN_RECORD.md", "COMMANDS.md",
    "AUDIT_REPORT.md", "SOURCE_SCOPE.tsv", "SOURCE_MANIFEST.tsv", "EXTERNAL_REVIEW_REQUEST.md",
    "build_source_manifest.py", "build_review_intake.py", "verify_review_intake.py",
    "EXTERNAL_REVIEW.md", "EXTERNAL_REVIEW_TRANSMISSION.md", "REPAIR_PREREGISTRATION.md",
    "REPAIR_FOLLOWUP_REQUEST.md",
    "EXTERNAL_REPAIR_FOLLOWUP.md", "R3_COMPLETION_PREREGISTRATION.md",
    "R3_COMPLETION_FOLLOWUP_REQUEST.md", "R3_COMPLETION_TRANSMISSION.md",
    "EXTERNAL_R3_COMPLETION_FOLLOWUP.md",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source_rows = list(csv.DictReader((PACKAGE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"),
                                      delimiter="\t"))
    intake = Path(tempfile.mkdtemp(prefix="udt_g330_review_", dir="/tmp"))
    package_out = intake / "package"
    source_out = intake / "sources"
    package_out.mkdir()
    source_out.mkdir()
    copied = []
    for name in PACKAGE_FILES:
        src = PACKAGE / name
        if not src.is_file():
            raise SystemExit(f"missing package file: {name}")
        dst = package_out / name
        shutil.copy2(src, dst)
        copied.append(dst)
    for row in source_rows:
        src = SOURCE_ROOT / row["path"]
        source_bytes = src.read_bytes() if src.is_file() else b""
        if (len(source_bytes) != int(row["bytes"])
                or hashlib.sha256(source_bytes).hexdigest() != row["sha256"]):
            frozen = subprocess.run(
                ["git", "show", f"{FROZEN_SOURCE_COMMIT}:{row['path']}"],
                cwd=REPO, capture_output=True, check=False,
            )
            source_bytes = frozen.stdout if frozen.returncode == 0 else b""
        if (len(source_bytes) != int(row["bytes"])
                or hashlib.sha256(source_bytes).hexdigest() != row["sha256"]):
            raise SystemExit(f"source manifest drift: {row['path']}")
        dst = source_out / row["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(source_bytes)
        copied.append(dst)

    scope = {
        "review": "read-only G330 R3-completion-only follow-up review",
        "allowed": [
            "inspect only this intake",
            "verify only the preregistered R3 wording completion and unchanged bounded landing",
            "run registered commands or bounded repair checks in a writable ephemeral copy",
        ],
        "forbidden": [
            "edit evidence files", "continue the research", "access repository or protected packages",
            "use internet or unsealed observations", "import carrier action source matter mass scale Xmax",
            "change the scientific question", "promote the conditional equation or result into canon",
            "select physical occupancy or history",
        ],
        "expected_verdicts": [
            "R3_COMPLETION_ACCEPTED__G330_BOUNDED_SCIENTIFIC_LANDING_RETAINED",
            "R3_COMPLETION_INCOMPLETE__G330_BOUNDED_SCIENTIFIC_LANDING_RETAINED",
            "REFUTE__G330_BOUNDED_BERGER_HOPF_LINE",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    copied.append(scope_path)

    lines = ["sha256\tbytes\tpath"]
    for path in sorted(copied, key=lambda p: p.relative_to(intake).as_posix()):
        lines.append(f"{digest(path)}\t{path.stat().st_size}\t{path.relative_to(intake).as_posix()}")
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

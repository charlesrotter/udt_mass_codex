#!/usr/bin/env python3
"""Build a sealed read-only intake for the G90 external semantic review."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    intake = Path(tempfile.mkdtemp(prefix="udt_overlap_live_review_", dir="/tmp"))
    package_files = [
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "FALSIFICATION_CONTRACT.tsv",
        "SOURCE_MANIFEST.tsv",
        "SOURCE_SCOPE_CORRECTION.md",
        "derive_overlap_compatibility.py",
        "verify_independent.py",
        "run_catch_proofs.py",
        "verify_package.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "VERIFICATION_RESULT.json",
        "EXACT_DERIVATION.md",
        "WITNESS_ATLAS.tsv",
        "STATUS_LEDGER.tsv",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "AUDIT_REPORT.md",
        "REVIEW_DISPATCH.md",
    ]

    payload_paths = []
    for name in package_files:
        src = HERE / name
        if not src.is_file():
            raise FileNotFoundError(src)
        payload_paths.append(src)

    with (HERE / "SOURCE_MANIFEST.tsv").open() as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            src = ROOT / row["path"]
            if not src.is_file() or sha256(src) != row["sha256"]:
                raise RuntimeError(f"source mismatch: {row['path']}")
            payload_paths.append(src)

    unique = []
    seen = set()
    for src in payload_paths:
        rel = src.relative_to(ROOT)
        if rel not in seen:
            unique.append((src, rel))
            seen.add(rel)

    payload = []
    for src, rel in sorted(unique, key=lambda item: str(item[1])):
        dst = intake / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        payload.append({"path": str(rel), "bytes": dst.stat().st_size, "sha256": sha256(dst)})

    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    scope = {
        "schema": "udt.external_readonly_review_scope.v1",
        "package": HERE.name,
        "git_head": head,
        "payload_count": len(payload),
        "payload": payload,
        "permissions": {
            "read_only": True,
            "may_edit": False,
            "may_continue_research": False,
            "may_access_outside_intake": False,
        },
        "explicit_exclusions": [
            "protected curvature/holonomy atlas",
            "protected stopped native-on-shell draft",
            "protected unbanked fixed-Gram predecessor",
            "protected G88 package",
            "all repository files not copied into this intake",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")

    for path in intake.rglob("*"):
        if path.is_file():
            path.chmod(0o444)
        elif path.is_dir():
            path.chmod(0o555)
    intake.chmod(0o555)

    print(json.dumps({
        "intake": str(intake),
        "payload_count": len(payload),
        "review_scope_sha256": sha256(scope_path),
        "git_head": head,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

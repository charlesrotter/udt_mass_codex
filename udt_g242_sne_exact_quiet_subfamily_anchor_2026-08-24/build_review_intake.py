#!/usr/bin/env python3
"""Build a repository-relative sealed G242 review intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
PACKAGE_FILES = (
    "MAP.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "INTERPRETATION_CORRECTION_PREREGISTRATION.md",
    "REGISTRY_LINEAGE_PACKAGING_REPAIR_PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "EVIDENCE_GATES.md",
    "COMMANDS.md",
    "STATUS_LEDGER.tsv",
    "REVIEW_REQUEST.md",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "VERIFICATION_RESULT.json",
    "derive_exact_quiet_anchor.py",
    "verify_exact_quiet_anchor_independent.py",
    "run_catch_proofs.py",
    "verify_package.py",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def preregistration_registry_digest(path: Path) -> str:
    """Retain preregistration lineage after the append-only G243 and G242 banks."""
    lines = path.read_bytes().splitlines(keepends=True)
    g242_rows = [line for line in lines if line.startswith(b"G242\t")]
    g243_rows = [line for line in lines if line.startswith(b"G243\t")]
    if not g242_rows and not g243_rows:
        return sha256(path)
    if len(g242_rows) > 1 or len(g243_rows) > 1:
        raise RuntimeError("registry may contain at most one G242 row and one G243 row")
    historical = b"".join(
        line for line in lines if not line.startswith((b"G242\t", b"G243\t"))
    )
    return hashlib.sha256(historical).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=Path("/tmp"))
    args = parser.parse_args()
    destination = Path(tempfile.mkdtemp(prefix="udt_g242_review_", dir=args.output_root))

    copied: list[Path] = []
    for name in PACKAGE_FILES:
        source = PACKAGE / name
        target = destination / PACKAGE.name / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)

    manifest_lines = (PACKAGE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()
    for line in manifest_lines[1:]:
        expected, relative, _role = line.split("\t")
        source = ROOT / relative
        actual = (
            preregistration_registry_digest(source)
            if relative == "CURRENT_SCIENTIFIC_PREMISES.tsv"
            else sha256(source)
        )
        if actual != expected:
            raise RuntimeError(f"source hash mismatch: {relative}")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)

    entries = []
    for path in sorted(set(copied)):
        entries.append({"path": str(path.relative_to(destination)), "sha256": sha256(path)})
    review_scope = {
        "review": "G242_FRESH_READ_ONLY_ADVERSARIAL",
        "file_count_excluding_scope": len(entries),
        "files": entries,
        "allowed_actions": ["read sealed intake", "registered no-write replay", "bounded read-only checks"],
        "forbidden_actions": ["edit evidence", "continue research", "inspect BOSS outcomes"],
    }
    scope_path = destination / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(review_scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "intake": str(destination),
        "file_count_including_scope": len(entries) + 1,
        "review_scope_sha256": sha256(scope_path),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

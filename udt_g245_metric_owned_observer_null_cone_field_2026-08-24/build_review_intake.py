#!/usr/bin/env python3
"""Build a sealed repository-relative G245 review intake."""

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
    "SOURCE_MANIFEST.tsv",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "EVIDENCE_GATES.md",
    "STATUS_LEDGER.tsv",
    "COMMANDS.md",
    "REVIEW_REQUEST.md",
    "REVIEW_REPAIR_PREREGISTRATION.md",
    "REVIEW_REPAIR_CORRECTION_PREREGISTRATION.md",
    "REVIEW_REPAIR_EXECUTION_NOTE.md",
    "BANKING_INTEGRATION_PREREGISTRATION.md",
    "BANKING_INTEGRATION_NOTE.md",
    "BANKING_REPLAY_RECORD.md",
    "EXTERNAL_REVIEW.md",
    "EXTERNAL_REVIEW_RAW.md",
    "EXTERNAL_REPAIR_FOLLOWUP_RAW.md",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "VERIFICATION_RESULT.json",
    "derive_metric_owned_null_cone.py",
    "verify_metric_owned_null_cone_independent.py",
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
    """Recover the exact pre-G245 registry beneath append-only descendant rows."""
    lines = path.read_bytes().splitlines(keepends=True)
    indices = [index for index, line in enumerate(lines) if line.startswith(b"G245\t")]
    if len(indices) != 1 or not lines or not lines[0].startswith(b"premise_id\t"):
        raise RuntimeError("live registry must contain exactly one banked G245 row")
    historical = lines[0] + b"".join(lines[indices[0] + 1 :])
    return hashlib.sha256(historical).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=Path("/tmp"))
    args = parser.parse_args()
    destination = Path(tempfile.mkdtemp(prefix="udt_g245_review_", dir=args.output_root))

    copied: list[Path] = []
    for name in PACKAGE_FILES:
        source = PACKAGE / name
        target = destination / PACKAGE.name / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)

    lines = (PACKAGE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()
    for line in lines[1:]:
        expected, relative, _role = line.split("\t")
        source = ROOT / relative
        actual = sha256(source)
        if relative == "CURRENT_SCIENTIFIC_PREMISES.tsv" and actual != expected:
            actual = preregistration_registry_digest(source)
        if actual != expected:
            raise RuntimeError(f"source hash mismatch: {relative}")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)

    entries = [
        {"path": str(path.relative_to(destination)), "sha256": sha256(path)}
        for path in sorted(set(copied))
    ]
    scope = {
        "review": "G245_REPAIR_ONLY_FOLLOWUP",
        "file_count_excluding_scope": len(entries),
        "files": entries,
        "allowed_actions": [
            "read sealed intake",
            "run registered no-write replays in a writable ephemeral copy",
            "verify only the corrected command-list repair and the unchanged bounded landing",
            "bounded repair-only read-only checks",
        ],
        "forbidden_actions": [
            "edit evidence",
            "continue research",
            "inspect observational outcomes",
            "inspect repository outside intake",
        ],
    }
    scope_path = destination / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "intake": str(destination),
        "file_count_including_scope": len(entries) + 1,
        "review_scope_sha256": sha256(scope_path),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build a sealed, repository-relative G249 adversarial review intake."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
PACKAGE_FILES = (
    "MAP.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "PREREGISTRATION_COMMIT.md",
    "SOURCE_MANIFEST.tsv", "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "LAY_REPORT.md",
    "EVIDENCE_GATES.md", "STATUS_LEDGER.tsv", "COMMANDS.md", "REVIEW_REQUEST.md",
    "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
    "VERIFICATION_RESULT.json", "derive_reciprocal_angular_scale.py",
    "verify_reciprocal_angular_scale_independent.py", "run_catch_proofs.py",
    "verify_package.py", "build_review_intake.py",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def matches_frozen_source(path: Path, expected: str, relative: str) -> bool:
    if sha256(path) == expected:
        return True
    if relative != "CURRENT_SCIENTIFIC_PREMISES.tsv":
        return False
    lines = path.read_bytes().splitlines(keepends=True)
    rows = [index for index, line in enumerate(lines) if line.startswith(b"G249\t")]
    if len(rows) != 1 or not lines or not lines[0].startswith(b"premise_id\t"):
        return False
    historical = lines[0] + b"".join(lines[rows[0] + 1 :])
    return hashlib.sha256(historical).hexdigest() == expected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=Path("/tmp"))
    args = parser.parse_args()
    destination = Path(tempfile.mkdtemp(prefix="udt_g249_review_", dir=args.output_root))
    copied: list[Path] = []

    for name in PACKAGE_FILES:
        source = PACKAGE / name
        target = destination / PACKAGE.name / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in rows:
        relative = row["path"]
        source = ROOT / relative
        if not matches_frozen_source(source, row["sha256"], relative):
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
        "review": "G249_FRESH_READ_ONLY_ADVERSARIAL",
        "file_count_excluding_scope": len(entries),
        "files": entries,
        "allowed_actions": [
            "read sealed intake",
            "run registered no-write replays or bounded checks in a writable ephemeral copy",
        ],
        "forbidden_actions": ["edit evidence", "continue research"],
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

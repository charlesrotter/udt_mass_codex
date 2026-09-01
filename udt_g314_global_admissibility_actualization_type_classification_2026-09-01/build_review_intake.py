#!/usr/bin/env python3
"""Build a sealed self-contained read-only G314 review intake under /tmp."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
PACKAGE_FILES = (
    "PREREGISTRATION.md", "SOURCE_SCOPE.tsv", "REPLAY_COMMANDS.txt", "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md", "LAY_REPORT.md", "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md",
    "RUN_RECORD.md", "ADMISSIBILITY_TYPE_ATLAS.tsv", "WITNESS_SIGNATURES.tsv",
    "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
    "derive_admissibility_types.py", "verify_independent.py", "run_catch_proofs.py",
    "verify_package.py", "build_review_intake.py", "EXTERNAL_REVIEW_REQUEST.md",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_source(relative: str) -> Path:
    candidate = (ROOT / relative).resolve()
    root = ROOT.resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError(f"source escapes repository: {relative}")
    if not candidate.is_file() or candidate.is_symlink():
        raise ValueError(f"source is not a regular file: {relative}")
    return candidate


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g314_review_", dir="/tmp"))
    package_target = intake / "package"
    package_target.mkdir()
    for name in PACKAGE_FILES:
        source = PACKAGE / name
        if not source.is_file() or source.is_symlink():
            raise ValueError(f"package file missing or not regular: {name}")
        shutil.copy2(source, package_target / name)
    source_rows = list(csv.DictReader(
        (PACKAGE / "SOURCE_SCOPE.tsv").open(encoding="utf-8", newline=""), delimiter="\t"
    ))
    source_target = intake / "sources"
    for row in source_rows:
        relative = row["path"]
        source = safe_source(relative)
        target = source_target / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    scope = {
        "question": "G314 global admissibility versus actualization type classification",
        "mode": "fresh read-only adversarial review",
        "allowed": ["inspect sealed intake", "run registered checks in writable ephemeral copy"],
        "forbidden": [
            "edit evidence files", "continue research", "access repository or protected packages",
            "use internet or unsealed observations", "select or canonize a law history topology",
            "select a population scale X_max source action matter mass or observational fit",
        ],
        "required_verdicts": [
            "G314_ACCEPTED__ADMISSIBILITY_ACTUALIZATION_DISTINCTION_UPHELD",
            "G314_REPAIRABLE_DEFECTS__BOUNDED_LANDING_RETAINED",
            "G314_SCIENTIFIC_LANDING_REFUTED", "G314_REVIEW_INCOMPLETE",
        ],
        "package_files": len(PACKAGE_FILES),
        "source_files": len(source_rows),
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    payloads = sorted(path for path in intake.rglob("*") if path.is_file())
    manifest = intake / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "bytes", "sha256"))
        for path in payloads:
            writer.writerow((path.relative_to(intake).as_posix(), path.stat().st_size, digest(path)))
    seal = intake / "REVIEW_MANIFEST.sha256"
    seal.write_text(f"{digest(manifest)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")
    print(json.dumps({
        "intake": str(intake),
        "manifest_payloads": len(payloads),
        "total_files": len(payloads) + 2,
        "scope_sha256": digest(scope_path),
        "manifest_sha256": digest(manifest),
        "detached_seal_sha256": digest(seal),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

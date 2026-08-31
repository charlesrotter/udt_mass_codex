#!/usr/bin/env python3
"""Build a sealed, source-bounded G307 fresh-review intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PACKAGE_FILES = [
    "MAP.md", "PREREGISTRATION.md", "PREREGISTRATION_ANCESTRY.md",
    "PREMISE_LEDGER.tsv", "PREMISE_AUDIT_RESULT.json", "SOURCE_SCOPE.tsv",
    "SOURCE_MANIFEST.tsv", "COMPLETENESS_MAP.md",
    "derive_directed_member_reconstruction.py", "verify_directed_member_independent.py",
    "run_catch_proofs.py", "verify_package.py", "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json", "MEMBER_CENSUS.tsv",
    "STATUS_LEDGER.tsv", "VERIFICATION_RESULT.json", "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md", "LAY_REPORT.md", "EVIDENCE_GATES.md", "RUN_RECORD.md",
    "COMMANDS.md", "EXTERNAL_REVIEW_REQUEST.md", "build_review_intake.py",
]
CURRENT_FILES = [
    "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
]


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def main() -> None:
    target = Path(tempfile.mkdtemp(prefix="udt_g307_review_", dir="/tmp"))
    package_target = target / HERE.name
    package_target.mkdir()
    for name in PACKAGE_FILES:
        source = HERE / name
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copy2(source, package_target / name)

    frozen = target / "frozen_sources"
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in source_rows:
        source = REPO / row["path"]
        if digest(source) != row["sha256"]:
            raise AssertionError(f"source hash drift: {row['path']}")
        destination = frozen / row["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    frozen_current = target / "frozen_current"
    frozen_current.mkdir()
    for name in CURRENT_FILES:
        source = REPO / name
        shutil.copy2(source, frozen_current / name)

    premise_audit = json.loads((HERE / "PREMISE_AUDIT_RESULT.json").read_text(encoding="utf-8"))
    if digest(frozen_current / "CURRENT_SCIENTIFIC_PREMISES.tsv") != premise_audit["registry_sha256"]:
        raise AssertionError("current premise registry drift since G307 audit")

    scope = {
        "schema": "UDT_G307_FRESH_REVIEW_SCOPE_V1",
        "question": (
            "audit the bounded conditional Hopf-member reconstruction from supplied directed "
            "and transverse-screen germs and the retained physical-population boundary"
        ),
        "package": HERE.name,
        "package_file_count": len(PACKAGE_FILES),
        "frozen_source_count": len(source_rows),
        "frozen_current_count": len(CURRENT_FILES),
        "allowed": [
            "read intake",
            "independently rederive the bounded theorem",
            "run registered checks in a writable ephemeral copy",
            "write review response outside intake",
        ],
        "forbidden": [
            "edit evidence files",
            "continue research",
            "access repository or protected packages",
            "use internet or unsealed observations",
            "import field equation action source matter model physical population mass law fit scale or X_max",
            "change registered question",
            "promote a supplied relation datum into a UDT-populated physical field",
        ],
    }
    scope_path = target / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    payloads = sorted(path for path in target.rglob("*") if path.is_file())
    manifest = target / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["sha256", "bytes", "path"])
        for path in payloads:
            writer.writerow([digest(path), path.stat().st_size, path.relative_to(target).as_posix()])
    seal = target / "REVIEW_MANIFEST.sha256"
    seal.write_text(f"{digest(manifest)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")
    print(json.dumps({
        "intake": str(target),
        "manifest_payloads": len(payloads),
        "total_files": len(payloads) + 2,
        "scope_sha256": digest(scope_path),
        "manifest_sha256": digest(manifest),
        "detached_seal_sha256": digest(seal),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

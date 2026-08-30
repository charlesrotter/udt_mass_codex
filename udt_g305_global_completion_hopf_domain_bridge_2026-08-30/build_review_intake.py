#!/usr/bin/env python3
"""Build a sealed, source-bounded G305 external-review intake."""

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
    "MAP.md", "PREREGISTRATION.md", "PREREGISTRATION_ANCESTRY.md", "PREMISE_LEDGER.tsv",
    "derive_global_hopf_bridge.py", "verify_global_hopf_bridge_independent.py",
    "run_global_hopf_catches.py", "verify_package.py", "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json", "PACKAGE_VERIFICATION_RESULT.json",
    "EXACT_DERIVATION.md", "LAY_REPORT.md", "AUDIT_REPORT.md", "TOPOLOGY_CENSUS.tsv",
    "HOPF_REQUIREMENT_LEDGER.tsv", "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md", "RUN_RECORD.md",
    "COMMANDS.md", "SOURCE_SCOPE.tsv", "EXTERNAL_REVIEW_REQUEST.md", "EXTERNAL_REVIEW_RESPONSE.md",
    "EXTERNAL_REVIEW_TRANSMISSION.md", "REPAIR_PREREGISTRATION.md", "REPAIR_FOLLOWUP_REQUEST.md",
    "build_review_intake.py",
]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def frozen_source_bytes(source: Path, relative_path: str) -> bytes:
    data = source.read_bytes()
    if relative_path == "CURRENT_SCIENTIFIC_PREMISES.tsv":
        data = b"".join(line for line in data.splitlines(keepends=True) if not line.startswith(b"G305\t"))
    return data


def main() -> None:
    target = Path(tempfile.mkdtemp(prefix="udt_g305_review_", dir="/tmp"))
    package_target = target / HERE.name
    package_target.mkdir()
    for name in PACKAGE_FILES:
        source = HERE / name
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copy2(source, package_target / name)

    sources_target = target / "frozen_sources"
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        source = REPO / row["path"]
        data = frozen_source_bytes(source, row["path"])
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise AssertionError(f"source hash drift: {row['path']}")
        if row["path"].startswith(HERE.name + "/"):
            destination = target / row["path"]
            if destination.read_bytes() != data:
                raise AssertionError(f"package source drift: {row['path']}")
            continue
        destination = sources_target / row["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)

    scope = {
        "schema": "UDT_G305_REPAIR_FOLLOWUP_SCOPE_V1",
        "question": "verify only preregistered G305 repairs R1-R4 and unchanged bounded landing",
        "package": HERE.name,
        "frozen_source_count": len(rows),
        "package_file_count": len(PACKAGE_FILES),
        "allowed": [
            "read intake", "verify only preregistered repairs R1-R4",
            "run registered checks in writable ephemeral copy", "write review response outside intake",
        ],
        "forbidden": [
            "edit evidence files", "continue research", "access repository or protected packages",
            "use internet or unsealed observations", "import field equation action source matter model mass law fit scale or X_max",
            "change registered question or scientific landing", "continue research beyond repairs R1-R4",
            "promote candidate family to UDT canon",
        ],
    }
    scope_path = target / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")
    payloads = sorted(path for path in target.rglob("*") if path.is_file())
    manifest = target / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["sha256", "bytes", "path"])
        for path in payloads:
            writer.writerow([digest(path), path.stat().st_size, path.relative_to(target).as_posix()])
    seal = target / "REVIEW_MANIFEST.sha256"
    seal.write_text(f"{digest(manifest)}  REVIEW_MANIFEST.tsv\n")
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

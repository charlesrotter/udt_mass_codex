#!/usr/bin/env python3
"""Build a sealed, repair-only G236 follow-up intake."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
DES_ROOT = Path(os.environ["G236_DES_ROOT"]).resolve()

PACKAGE_FILES = [
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "AUDIT_REPORT.md",
    "CATCH_PROOF_RESULT.json",
    "CHRONOLOGY_AND_NONINTERFERENCE_PROOF.json",
    "COMMANDS.md",
    "EVIDENCE_GATES.md",
    "EXACT_DERIVATION.md",
    "EXTERNAL_REVIEW.md",
    "EXTERNAL_REVIEW_REPAIR_PREREGISTRATION.md",
    "INDEPENDENT_VERIFICATION.json",
    "LAY_REPORT.md",
    "OBSERVATIONAL_SOURCE_AUDIT.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "PREREGISTRATION_REPAIR.md",
    "PRODUCTION_RESULT.json",
    "REPAIR_FOLLOWUP_REQUEST.md",
    "SOURCE_MANIFEST.tsv",
    "STATE_RECONSTRUCTION.tsv",
    "STATUS_LEDGER.tsv",
    "VERIFICATION_RESULT.json",
    "build_chronology_proof.py",
    "derive_dual_sne_relational_state.py",
    "run_catch_proofs.py",
    "verify_dual_sne_relational_state_independent.py",
    "verify_package.py",
    "GIT_OBJECTS/184b1a78_commit_object.txt",
    "GIT_OBJECTS/184b1a78_recursive_tree.txt",
    "GIT_OBJECTS/318f35de_commit_object.txt",
    "GIT_OBJECTS/318f35de_exact_patch.txt",
    "GIT_OBJECTS/318f35de_recursive_tree.txt",
]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def resolve_source(logical: str) -> Path:
    external = {
        "external_data/README.md": DES_ROOT / "README.md",
        "external_data/DES-Dovekie_HD.csv": DES_ROOT / "DES-Dovekie_HD.csv",
        "external_data/STAT+SYS.npz": DES_ROOT / "STAT+SYS.npz",
    }
    return external.get(logical, REPO / logical)


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g236_repair_followup_", dir="/tmp"))
    package_target = intake / PACKAGE.name
    package_target.mkdir()
    copied: list[Path] = []

    for name in PACKAGE_FILES:
        source = PACKAGE / name
        if not source.is_file():
            raise FileNotFoundError(source)
        target = package_target / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in rows:
        logical = row["path"]
        source = resolve_source(logical)
        if not source.is_file() or digest(source) != row["sha256"]:
            raise RuntimeError(f"source mismatch: {logical}")
        target = intake / logical
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)

    entries = [
        {"path": str(path.relative_to(intake)), "sha256": digest(path)}
        for path in sorted(copied)
    ]
    first_scope = json.loads(Path("/tmp/udt_g236_review_5ex3_c3_/REVIEW_SCOPE.json").read_text())
    first_hashes = {entry["path"]: entry["sha256"] for entry in first_scope["files"]}
    unchanged_originals = {
        entry["path"]: first_hashes.get(entry["path"]) == entry["sha256"]
        for entry in entries
        if entry["path"] in first_hashes
    }
    if not unchanged_originals or not all(unchanged_originals.values()):
        raise RuntimeError("original sealed payload changed")
    tree_material = "".join(
        f"{entry['sha256']}  {entry['path']}\n" for entry in entries
    ).encode()
    scope = {
        "task": "read-only repair-only follow-up review of G236 chronology evidence",
        "instructions": str(Path(PACKAGE.name) / "REPAIR_FOLLOWUP_REQUEST.md"),
        "replay_environment": {"G236_DES_ROOT": str(intake / "external_data")},
        "restrictions": [
            "inspect only this sealed intake",
            "verify only the registered evidence repair and unchanged scientific landing",
            "run only bounded read-only checks or checks in an ephemeral copy",
            "do not edit evidence files",
            "do not continue the research",
        ],
        "first_review_scope_sha256": "87f46538fafa94b4e82e9d424dc17809b90c527f4b88c7ded9bc276a68cbc2cc",
        "all_original_payloads_byte_identical": all(unchanged_originals.values()),
        "unchanged_original_payloads": unchanged_originals,
        "payload_file_count": len(entries),
        "tree_digest_sha256": hashlib.sha256(tree_material).hexdigest(),
        "files": entries,
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "intake": str(intake),
        "payload_file_count": len(entries),
        "total_file_count_including_scope": len(entries) + 1,
        "tree_digest_sha256": scope["tree_digest_sha256"],
        "review_scope_sha256": digest(scope_path),
        "all_original_payloads_byte_identical": scope["all_original_payloads_byte_identical"],
    }, indent=2))


if __name__ == "__main__":
    main()

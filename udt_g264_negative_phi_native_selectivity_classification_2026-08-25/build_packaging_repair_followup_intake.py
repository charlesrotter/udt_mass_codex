#!/usr/bin/env python3
"""Build a self-contained sealed G264 packaging-repair follow-up intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE_NAME = "udt_g264_negative_phi_native_selectivity_classification_2026-08-25"
ORIGINAL_INTAKE = Path("/tmp/udt_g264_review_tme4dog9")
FIRST_REPAIR_INTAKE = Path("/tmp/udt_g264_repair_followup_hzqk15gj")
ORIGINAL_SCOPE_SHA = "1617c8f36792472db11e26a1d657e60dc0fc8195ee1c2181828b9e15d77650d2"
ORIGINAL_MANIFEST_SHA = "22b44394fe9d8bd75a2e9b17e8e2e1c65b9e0d89da897253084d8f2da00c9693"
FIRST_REPAIR_SCOPE_SHA = "a548227e8f9d9f033ef2ca7edca4e3b6599a29c02429822971a7c6502582aa79"
FIRST_REPAIR_MANIFEST_SHA = "2667c3faa02706de78ab4e065d7a119005577c82fa54d8fb9e1a91fa4a3f94d8"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def assert_seal(root: Path, scope_sha: str, manifest_sha: str) -> None:
    if sha(root / "REVIEW_SCOPE.json") != scope_sha:
        raise AssertionError(f"scope changed: {root}")
    if sha(root / "REVIEW_MANIFEST.tsv") != manifest_sha:
        raise AssertionError(f"manifest changed: {root}")


def main() -> None:
    package = Path(__file__).resolve().parent
    assert_seal(ORIGINAL_INTAKE, ORIGINAL_SCOPE_SHA, ORIGINAL_MANIFEST_SHA)
    assert_seal(FIRST_REPAIR_INTAKE, FIRST_REPAIR_SCOPE_SHA, FIRST_REPAIR_MANIFEST_SHA)
    target = Path(tempfile.mkdtemp(prefix="udt_g264_packaging_repair_followup_"))

    payloads: dict[str, Path] = {}

    # Preserve both earlier seals exactly for chronology and comparison.
    for label, root in (
        ("original_intake", ORIGINAL_INTAKE),
        ("first_repair_followup", FIRST_REPAIR_INTAKE),
    ):
        for source in sorted(path for path in root.rglob("*") if path.is_file()):
            payloads[f"{label}/{source.relative_to(root)}"] = source

    # Reconstruct an exact repository-shaped source root without repository or Git access.
    source_manifest = package / "SOURCE_MANIFEST.tsv"
    for row in read_tsv(source_manifest):
        source = ORIGINAL_INTAKE / row["path"]
        if not source.is_file() or sha(source) != row["sha256"]:
            raise AssertionError(f"frozen source unavailable or changed: {row['path']}")
        payloads[f"replay_root/{row['path']}"] = source

    package_names = (
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "AUDIT_REPORT.md",
        "CATCH_PROOF_RESULT.json",
        "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXACT_DERIVATION.md",
        "EXTERNAL_REPAIR_FOLLOWUP_GPT54.md",
        "EXTERNAL_REVIEW_GPT54.md",
        "INDEPENDENT_VERIFICATION.json",
        "LAY_REPORT.md",
        "MAP.md",
        "METRIC_FIRST_VERIFICATION.json",
        "OWNERSHIP_ATLAS.tsv",
        "PACKAGING_CATCH_RESULT.json",
        "PACKAGING_REPAIR_FOLLOWUP_REQUEST.md",
        "PACKAGING_REPAIR_PREREGISTRATION.md",
        "PACKAGING_REPAIR_RESULT.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "REPAIR_CATCH_RESULT.json",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "REPAIR_PREREGISTRATION.md",
        "REPAIR_RESULT.md",
        "RUN_RECORD.md",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "TRANSMISSION_RECORD.md",
        "VERIFICATION_RESULT.json",
        "build_packaging_repair_followup_intake.py",
        "build_repair_followup_intake.py",
        "build_review_intake.py",
        "derive_selectivity.py",
        "run_catch_proofs.py",
        "verify_independent.py",
        "verify_metric_first.py",
        "verify_package.py",
        "verify_packaging_catches.py",
        "verify_repair_catches.py",
    )
    for name in package_names:
        source = package / name
        if not source.is_file():
            raise FileNotFoundError(source)
        payloads[f"replay_root/{PACKAGE_NAME}/{name}"] = source

    rows: list[tuple[str, str, int]] = []
    for relative, source in sorted(payloads.items()):
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        rows.append((relative, sha(destination), destination.stat().st_size))

    commands = target / "REGISTERED_REPLAY_COMMANDS.md"
    commands.write_text(
        "# Registered G264 packaging-repair follow-up commands\n\n"
        "Run from `replay_root/udt_g264_negative_phi_native_selectivity_classification_2026-08-25/` "
        "inside a writable ephemeral copy of the seal:\n\n"
        "```bash\n"
        "python3 derive_selectivity.py\n"
        "python3 verify_metric_first.py\n"
        "python3 verify_independent.py\n"
        "python3 run_catch_proofs.py\n"
        "python3 verify_repair_catches.py\n"
        "python3 verify_package.py\n"
        "python3 verify_packaging_catches.py --replay-root ..\n"
        "```\n",
        encoding="utf-8",
    )
    rows.append((commands.name, sha(commands), commands.stat().st_size))
    rows.sort()

    manifest = target / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "bytes"))
        writer.writerows(rows)

    scope = {
        "purpose": "read-only G264 sealed-replay packaging repair-only follow-up review",
        "payload_count": len(rows),
        "total_file_count_including_manifest_and_scope": len(rows) + 2,
        "review_manifest_sha256": sha(manifest),
        "original_scope_sha256": ORIGINAL_SCOPE_SHA,
        "original_manifest_sha256": ORIGINAL_MANIFEST_SHA,
        "first_repair_scope_sha256": FIRST_REPAIR_SCOPE_SHA,
        "first_repair_manifest_sha256": FIRST_REPAIR_MANIFEST_SHA,
        "permissions": {
            "verify_only_packaging_repair_and_unchanged_landing": True,
            "run_registered_checks_in_writable_ephemeral_copy": True,
            "edit_evidence_files": False,
            "continue_research": False,
        },
    }
    scope_path = target / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(target)
    print(f"payload_count={len(rows)}")
    print(f"total_file_count={len(rows) + 2}")
    print(f"manifest_sha256={sha(manifest)}")
    print(f"scope_sha256={sha(scope_path)}")


if __name__ == "__main__":
    main()

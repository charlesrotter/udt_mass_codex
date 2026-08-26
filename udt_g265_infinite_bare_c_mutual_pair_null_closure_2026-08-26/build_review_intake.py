#!/usr/bin/env python3
"""Build a sealed G265 fresh adversarial-review intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


PACKAGE_NAME = "udt_g265_infinite_bare_c_mutual_pair_null_closure_2026-08-26"
PREREG_COMMIT = "8f716271ad068cf0ada7f18de26e01b11f7a0a11"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def frozen_source(repo: Path, relative: str, expected: str) -> bytes:
    live = repo / relative
    if live.is_file() and sha(live) == expected:
        return live.read_bytes()
    data = subprocess.check_output(["git", "show", f"{PREREG_COMMIT}:{relative}"], cwd=repo)
    if sha_bytes(data) != expected:
        raise AssertionError(f"frozen source mismatch: {relative}")
    return data


def main() -> None:
    package = Path(__file__).resolve().parent
    repo = package.parent
    target = Path(tempfile.mkdtemp(prefix="udt_g265_review_"))

    with (package / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))

    package_names = (
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "AUDIT_REPORT.md",
        "CATCH_PROOF_RESULT.json",
        "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXACT_DERIVATION.md",
        "INDEPENDENT_VERIFICATION.json",
        "LAY_REPORT.md",
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "RUN_RECORD.md",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "build_review_intake.py",
        "derive_closure.py",
        "run_catch_proofs.py",
        "verify_independent.py",
        "verify_package.py",
    )

    payloads: dict[str, bytes] = {}
    for row in source_rows:
        payloads[row["path"]] = frozen_source(repo, row["path"], row["sha256"])
    for name in package_names:
        path = package / name
        if not path.is_file():
            raise FileNotFoundError(path)
        payloads[f"{PACKAGE_NAME}/{name}"] = path.read_bytes()

    manifest_rows: list[tuple[str, str, int]] = []
    for relative, data in sorted(payloads.items()):
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        manifest_rows.append((relative, sha_bytes(data), len(data)))

    manifest = target / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "bytes"))
        writer.writerows(manifest_rows)

    scope = {
        "purpose": "fresh read-only adversarial G265 infinite-bare-c and mutual-pair closure review",
        "payload_count": len(manifest_rows),
        "total_file_count_including_manifest_and_scope": len(manifest_rows) + 2,
        "review_manifest_sha256": sha(manifest),
        "permissions": {
            "inspect_only_this_intake": True,
            "run_registered_replays_or_bounded_checks_in_ephemeral_copy": True,
            "edit_evidence_files": False,
            "continue_research": False,
        },
    }
    scope_path = target / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")
    print(target)
    print(f"payload_count={len(manifest_rows)}")
    print(f"total_file_count={len(manifest_rows) + 2}")
    print(f"manifest_sha256={sha(manifest)}")
    print(f"scope_sha256={sha(scope_path)}")


if __name__ == "__main__":
    main()

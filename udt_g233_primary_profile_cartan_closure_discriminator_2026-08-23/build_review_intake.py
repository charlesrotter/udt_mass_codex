#!/usr/bin/env python3
"""Build a sealed G233 review intake containing only allowlisted files."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import tempfile


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent

PACKAGE_FILES = [
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "AUDIT_REPORT.md",
    "EVIDENCE_GATES.md",
    "EXACT_DERIVATION.md",
    "INITIAL_INDEPENDENT_FAILURE.json",
    "PREMISE_LEDGER.tsv",
    "REPAIR_PREREGISTRATION.md",
    "REPLAY_INTERFACE_PREREGISTRATION.md",
    "RUN_LOG.md",
    "SOURCE_MANIFEST.tsv",
    "STARTUP_REPAIR_EXTENSION_PREREGISTRATION.md",
    "STARTUP_REPAIR_FINAL_SCOPE_PREREGISTRATION.md",
    "STARTUP_REPAIR_PREREGISTRATION.md",
    "STARTUP_REPAIR_TOKEN_CORRECTION.md",
    "STATUS_LEDGER.tsv",
    "derive_primary_profile_cartan_closure.py",
    "exact_results.json",
    "hostile_mutation_tests.py",
    "hostile_results.json",
    "independent_results.json",
    "package_verification.json",
    "verify_independent_series.py",
    "verify_package.py",
]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    intake = Path(tempfile.mkdtemp(prefix="udt_g233_review_"))
    package_dest = intake / PACKAGE.name
    package_dest.mkdir()
    for name in PACKAGE_FILES:
        source = PACKAGE / name
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copy2(source, package_dest / name)

    manifest_lines = (PACKAGE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()
    for line in manifest_lines[1:]:
        _, relative, _ = line.split("\t")
        source = REPO / relative
        destination = intake / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    payloads = sorted(path for path in intake.rglob("*") if path.is_file())
    tree_hasher = hashlib.sha256()
    entries = []
    for path in payloads:
        relative = path.relative_to(intake).as_posix()
        digest = sha256(path)
        tree_hasher.update(relative.encode("utf-8") + b"\0" + digest.encode("ascii") + b"\n")
        entries.append({"path": relative, "sha256": digest})

    scope = {
        "review": "fresh read-only adversarial G233 scientific and evidence-contract review",
        "allowed_actions": ["inspect sealed intake", "run registered no-write replay", "bounded read-only checks"],
        "forbidden_actions": ["edit files", "continue research", "use internet", "access repository outside intake"],
        "payload_count": len(entries),
        "sealed_file_count_including_scope": len(entries) + 1,
        "payload_tree_sha256": tree_hasher.hexdigest(),
        "files": entries,
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "intake": str(intake),
        "file_count": len(entries) + 1,
        "scope_sha256": sha256(scope_path),
        "payload_tree_sha256": scope["payload_tree_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

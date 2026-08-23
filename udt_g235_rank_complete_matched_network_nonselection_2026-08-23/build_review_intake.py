#!/usr/bin/env python3
"""Build a sealed G235 review intake containing only registered package files and sources."""

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
    "DERIVATION_RESULT.json",
    "EVIDENCE_GATES.md",
    "EXACT_DERIVATION.md",
    "INDEPENDENT_VERIFICATION.json",
    "LAY_REPORT.md",
    "MAP.md",
    "NETWORK_TWIN_ATLAS.tsv",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "STATUS_LEDGER.tsv",
    "VERIFICATION_STRENGTHENING_PREREGISTRATION.md",
    "EXTERNAL_REVIEW_REPAIR_PREREGISTRATION.md",
    "EXTERNAL_REVIEW.md",
    "REPAIR_FOLLOWUP_REQUEST.md",
    "EXTERNAL_REPAIR_FOLLOWUP.md",
    "FINAL_EVIDENCE_MANIFEST.tsv",
    "POST_REVIEW_STARTUP_REPAIR_PREREGISTRATION.md",
    "derive_matched_network_nonselection.py",
    "verify_matched_network_independent.py",
    "verify_package.py",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g235_review_", dir="/tmp"))
    package_target = intake / PACKAGE.name
    package_target.mkdir()

    copied: list[Path] = []
    for name in PACKAGE_FILES:
        source = PACKAGE / name
        target = package_target / name
        shutil.copy2(source, target)
        copied.append(target)

    manifest_lines = (PACKAGE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]
    for line in manifest_lines:
        _, relative, _ = line.split("\t")
        source = REPO / relative
        target = package_target / "SEALED_SOURCES" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)

    entries = []
    for path in sorted(copied):
        entries.append({"path": str(path.relative_to(intake)), "sha256": digest(path)})
    tree_material = "".join(f"{entry['sha256']}  {entry['path']}\n" for entry in entries).encode()
    scope = {
        "task": "fresh read-only adversarial review of the bounded G235 landing",
        "restrictions": [
            "inspect only this sealed intake",
            "run only bounded read-only checks",
            "do not edit files",
            "do not continue the research",
        ],
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
    }, indent=2))


if __name__ == "__main__":
    main()

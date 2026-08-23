#!/usr/bin/env python3
"""Build a sealed G236 review intake from registered package files and exact sources."""

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
    "COMMANDS.md",
    "EVIDENCE_GATES.md",
    "EXACT_DERIVATION.md",
    "INDEPENDENT_VERIFICATION.json",
    "LAY_REPORT.md",
    "OBSERVATIONAL_SOURCE_AUDIT.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "PREREGISTRATION_REPAIR.md",
    "PRODUCTION_RESULT.json",
    "SOURCE_MANIFEST.tsv",
    "STATE_RECONSTRUCTION.tsv",
    "STATUS_LEDGER.tsv",
    "VERIFICATION_RESULT.json",
    "derive_dual_sne_relational_state.py",
    "run_catch_proofs.py",
    "verify_dual_sne_relational_state_independent.py",
    "verify_package.py",
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
    intake = Path(tempfile.mkdtemp(prefix="udt_g236_review_", dir="/tmp"))
    package_target = intake / PACKAGE.name
    package_target.mkdir()

    copied: list[Path] = []
    for name in PACKAGE_FILES:
        source = PACKAGE / name
        if not source.is_file():
            raise FileNotFoundError(source)
        target = package_target / name
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
    tree_material = "".join(
        f"{entry['sha256']}  {entry['path']}\n" for entry in entries
    ).encode()
    scope = {
        "task": "fresh read-only adversarial review of the bounded G236 landing",
        "instructions": str(Path(PACKAGE.name) / "ADVERSARIAL_REVIEW_REQUEST.md"),
        "replay_environment": {
            "G236_DES_ROOT": str(intake / "external_data"),
        },
        "restrictions": [
            "inspect only this sealed intake",
            "run only bounded read-only checks or a replay in an ephemeral copy",
            "do not edit evidence files",
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

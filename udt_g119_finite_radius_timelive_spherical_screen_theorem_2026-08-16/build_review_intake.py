#!/usr/bin/env python3
"""Build a sealed G119 read-only review intake without protected local work."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    package_files = [
        "PREREGISTRATION.md", "SOURCE_MANIFEST.tsv", "EXACT_DERIVATION.md", "AUDIT_REPORT.md",
        "THEOREM_STRATA.tsv", "PREMISE_LEDGER.tsv", "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json", "LAY_REPORT.md", "EVIDENCE_GATES.md",
        "REVIEW_REQUEST.md", "derive_spherical_screen.py", "verify_spherical_screen_independent.py",
    ]
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))

    intake = Path(tempfile.mkdtemp(prefix="udt_g119_screen_review_"))
    package_target = intake / HERE.name
    package_target.mkdir(parents=True)
    copied: list[dict[str, str]] = []

    for name in package_files:
        source = HERE / name
        target = package_target / name
        shutil.copy2(source, target)
        copied.append({"path": str(target.relative_to(intake)), "sha256": sha256(target)})

    for row in sources:
        source = ROOT / row["path"]
        target = intake / "sources" / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append({"path": str(target.relative_to(intake)), "sha256": sha256(target)})

    scope = {
        "purpose": "fresh read-only adversarial review of the preregistered bounded G119 theorem",
        "package": HERE.name,
        "files": copied,
        "forbidden": [
            "repository access outside this intake", "file edits", "continuing the research",
            "internet", "protected local packages",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for path in intake.rglob("*"):
        if path.is_file():
            path.chmod(0o444)
    print(json.dumps({
        "intake": str(intake),
        "file_count": len(copied) + 1,
        "scope_sha256": sha256(scope_path),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

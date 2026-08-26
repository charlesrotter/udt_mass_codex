#!/usr/bin/env python3
"""Build a sealed G273 review intake containing only registered sources and package evidence."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PAYLOAD = (
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "AUDIT_REPORT.md",
    "CATCH_PROOF_RESULT.json",
    "COMMANDS.md",
    "DERIVATION_RESULT.json",
    "EVIDENCE_GATES.md",
    "EXACT_DERIVATION.md",
    "INDEPENDENT_VERIFICATION.json",
    "LAY_REPORT.md",
    "MAP.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "PREREGISTRATION_EXECUTION_NOTE.md",
    "RUN_RECORD.md",
    "SOURCE_MANIFEST.tsv",
    "SOURCE_PROPOSITION_LEDGER.tsv",
    "STATUS_LEDGER.tsv",
    "VERIFICATION_RESULT.json",
    "build_review_intake.py",
    "derive_projective_distance_ownership.py",
    "run_catch_proofs.py",
    "verify_projective_distance_independent.py",
    "verify_package.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_relative(source: Path, relative: Path, intake: Path) -> None:
    target = intake / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g273_review_", dir="/tmp"))
    package_relative = Path(ROOT.name)

    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    assert len(sources) == 11
    for row in sources:
        relative = Path(row["path"])
        source = (REPO / relative).resolve()
        assert source.is_relative_to(REPO.resolve())
        assert digest(source) == row["sha256"]
        copy_relative(source, relative, intake)

    for name in PAYLOAD:
        source = ROOT / name
        assert source.is_file(), name
        copy_relative(source, package_relative / name, intake)

    scope = {
        "title": "G273 projective pair distance foundational ownership fresh review",
        "mode": "READ_ONLY_ADVERSARIAL_REVIEW",
        "scientific_scope": (
            "Verify only the bounded source entailment, projective uniqueness, complete open-ball "
            "state, conditional physical attachment, and premise grades."
        ),
        "registered_replay": f"python3 {ROOT.name}/verify_package.py --no-write",
        "package_grade": "INTERNALLY_VERIFIED_LEAD__EXTERNAL_REVIEW_OPEN",
        "prohibited": [
            "edit evidence files",
            "continue the research",
            "access the repository outside this intake",
            "access protected packages",
            "inspect observational outcomes",
            "adopt or canonize the projective distance clarification",
            "select a scale history branch population or X_max",
            "import a field equation source action matter model fit or transfer law",
        ],
    }
    (intake / "REVIEW_SCOPE.json").write_text(
        json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    rows = []
    for path in sorted(p for p in intake.rglob("*") if p.is_file()):
        relative = path.relative_to(intake)
        rows.append((str(relative), digest(path), path.stat().st_size))
    manifest = intake / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as stream:
        stream.write("path\tsha256\tbytes\n")
        for relative, sha, size in rows:
            stream.write(f"{relative}\t{sha}\t{size}\n")

    result = {
        "intake": str(intake),
        "files_including_manifest": len(rows) + 1,
        "review_scope_sha256": digest(intake / "REVIEW_SCOPE.json"),
        "review_manifest_sha256": digest(manifest),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

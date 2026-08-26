#!/usr/bin/env python3
"""Build a sealed G274 read-only adversarial-review intake under /tmp."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.resolve()
PACKAGE_NAME = ROOT.name

PACKAGE_FILES = (
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
    "STATUS_LEDGER.tsv",
    "VERIFICATION_RESULT.json",
    "build_review_intake.py",
    "derive_projective_network_descent.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "verify_projective_network_independent.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_relative(relative: str, destination: Path) -> None:
    source = (REPO / relative).resolve()
    assert source.is_relative_to(REPO)
    assert source.is_file(), relative
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()

    if args.output:
        destination = Path(args.output).resolve()
        assert destination.is_relative_to(Path("/tmp")), destination
        destination.mkdir(parents=True, exist_ok=False)
    else:
        destination = Path(tempfile.mkdtemp(prefix="udt_g274_review_", dir="/tmp"))

    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    assert len(sources) == 11
    for row in sources:
        copy_relative(row["path"], destination)
        assert digest(destination / row["path"]) == row["sha256"]

    for name in PACKAGE_FILES:
        copy_relative(f"{PACKAGE_NAME}/{name}", destination)

    scope = {
        "review_type": "fresh_read_only_adversarial",
        "package": PACKAGE_NAME,
        "scientific_landing": (
            "FULL_PATH_LABELLED_FRAME_MORPHISMS_DESCEND_EXACTLY__"
            "PROJECTIVE_OPEN_BALL_VECTOR_IS_A_VALID_PAIR_COORDINATE_BUT_NOT_A_"
            "STANDALONE_NONRADIAL_COMPOSITION_LAW__SCREEN_FRAME_CARRY_IS_REQUIRED__"
            "RADIAL_MOBIUS_STRATUM_CLOSES__SCALE_HISTORY_BRANCH_POPULATION_AND_XMAX_REMAIN_OPEN"
        ),
        "allowed": [
            "inspect only this sealed intake",
            "run registered no-write replays or bounded read-only checks in an ephemeral copy",
        ],
        "forbidden": [
            "edit evidence files",
            "continue the research",
            "access repository files outside the intake",
            "inspect observational outcomes or protected packages",
            "adopt or canonize the physical-position clarification",
            "select a scale, history, branch population, path population, or X_max",
        ],
        "registered_replay": f"python3 {PACKAGE_NAME}/verify_package.py --no-write",
    }
    (destination / "REVIEW_SCOPE.json").write_text(
        json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (destination / "PROVENANCE.md").write_text(
        "# G274 sealed-intake provenance\n\n"
        "This intake contains the G274 evidence package plus only the eleven exact repository "
        "sources frozen in its `SOURCE_MANIFEST.tsv`. The projective physical-position "
        "clarification is not adopted. Observational outcomes and protected packages are absent.\n",
        encoding="utf-8",
    )

    rows = []
    for path in sorted(p for p in destination.rglob("*") if p.is_file()):
        relative = path.relative_to(destination).as_posix()
        rows.append((relative, digest(path), path.stat().st_size))
    manifest = destination / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "bytes"))
        writer.writerows(rows)

    print(json.dumps({
        "intake": str(destination),
        "payload_files": len(rows),
        "total_files_including_manifest": len(rows) + 1,
        "REVIEW_SCOPE_sha256": digest(destination / "REVIEW_SCOPE.json"),
        "REVIEW_MANIFEST_sha256": digest(manifest),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build a self-contained sealed G278 review intake under /tmp."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
DES_ROOT = Path(os.environ["G236_DES_ROOT"]).resolve()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g278_review_", dir="/tmp"))
    package_target = intake / PACKAGE.name
    package_target.mkdir()

    for source in sorted(PACKAGE.iterdir()):
        if source.is_file() and source.name != "build_review_intake.py":
            copy_file(source, package_target / source.name)
    copy_file(PACKAGE / "build_review_intake.py", package_target / "build_review_intake.py")

    external_map = {
        "external_data/DES-Dovekie_HD.csv": DES_ROOT / "DES-Dovekie_HD.csv",
        "external_data/STAT+SYS.npz": DES_ROOT / "STAT+SYS.npz",
    }
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            source = external_map.get(row["path"], ROOT / row["path"])
            copy_file(source, intake / "sources" / row["path"])

    extra_sources = [
        "udt_g275_projective_position_scale_attachment_xmax_separation_2026-08-26/AUDIT_REPORT.md",
        "udt_g275_projective_position_scale_attachment_xmax_separation_2026-08-26/EXACT_DERIVATION.md",
        "udt_g276_proper_clock_ce_scale_anchor_reconciliation_2026-08-26/AUDIT_REPORT.md",
        "udt_g276_proper_clock_ce_scale_anchor_reconciliation_2026-08-26/EXACT_DERIVATION.md",
        "udt_g277_observational_scale_anchor_ownership_2026-08-26/sources/PantheonPlus_4_DISTANCES_AND_COVAR_README.txt",
        "udt_g277_observational_scale_anchor_ownership_2026-08-26/sources/PantheonPlus_SH0ES_cosmosis_likelihood.py",
    ]
    for relative in extra_sources:
        copy_file(ROOT / relative, intake / "sources" / relative)

    scope = {
        "review": "G278 fresh read-only adversarial review",
        "intake_only": True,
        "may_run": "registered replays or bounded checks only in a writable ephemeral copy",
        "must_not": [
            "edit evidence files",
            "continue the research",
            "access the repository outside the intake",
            "access protected packages",
            "use the internet",
            "select a preferred resolution or average scales",
            "fit or alter a metric, history, kernel, transfer law, angular sector, X_max, or CMB model",
        ],
        "requested_output": "bounded adversarial landing plus exact defects and repair requirements",
    }
    (intake / "REVIEW_SCOPE.json").write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")

    files = sorted(path for path in intake.rglob("*") if path.is_file())
    manifest_path = intake / "REVIEW_MANIFEST.tsv"
    with manifest_path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["sha256", "bytes", "path"])
        for path in files:
            writer.writerow([sha256(path), path.stat().st_size, path.relative_to(intake)])

    print(json.dumps({
        "intake": str(intake),
        "payload_files": len(files),
        "total_files_including_manifest": len(files) + 1,
        "review_scope_sha256": sha256(intake / "REVIEW_SCOPE.json"),
        "review_manifest_sha256": sha256(manifest_path),
        "total_bytes": sum(path.stat().st_size for path in files) + manifest_path.stat().st_size,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build a sealed, read-only-source intake for external adversarial review."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent

PACKAGE_FILES = (
    "PREREGISTRATION.md",
    "SUITABILITY_GATES.tsv",
    "CANDIDATE_LEDGER.tsv",
    "STATUS_LEDGER.tsv",
    "SOURCE_MANIFEST.tsv",
    "ONTOLOGY_CORRECTION.md",
    "LINEAGE_SUITABILITY_ATLAS.tsv",
    "GATE_RESULTS.tsv",
    "DATA_PROVENANCE.tsv",
    "AUDIT_REPORT.md",
    "EVIDENCE_GATES.md",
    "LAY_REPORT.md",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "audit_official_dr2.py",
    "verify_gaussian_independent.py",
    "verify_preregistration.py",
    "verify_package.py",
    "OFFICIAL_DR2_AUDIT_RESULT.json",
    "OFFICIAL_DR2_AP_SHAPE.tsv",
    "INDEPENDENT_GAUSSIAN_REPLAY.json",
)

REPO_SOURCES = (
    "udt_xmax_scale_observational_M2_build_2026-08-07/PREREGISTRATION.md",
    "udt_xmax_scale_observational_M2_build_2026-08-07/v_bao.py",
    "udt_xmax_scale_observational_M3_runs_2026-08-07/BAO_RESULTS.md",
    "udt_xmax_scale_observational_M3_runs_2026-08-07/RESULTS_VERIFIER_REPORT.md",
    "simple_metric_bao_disk_inventory_results.md",
    "simple_metric_bao_pure_AP_character_results.md",
    "simple_metric_bao_proper_pass_results.md",
)

EXTERNAL_SOURCES = (
    Path("/media/udt-admin/ScratchDisk/Data/BAO/DESI_DR2_2503.14738.pdf"),
    Path(
        "/media/udt-admin/ScratchDisk/Data/BAO/CobayaSampler_bao_data/"
        "desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt"
    ),
    Path(
        "/media/udt-admin/ScratchDisk/Data/BAO/CobayaSampler_bao_data/"
        "desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt"
    ),
    Path(
        "/media/udt-admin/ScratchDisk/Data/BAO/CobayaSampler_cobaya/"
        "cobaya/likelihoods/base_classes/bao.py"
    ),
    Path(
        "/media/udt-admin/ScratchDisk/Data/BAO/CobayaSampler_cobaya/"
        "cobaya/likelihoods/bao/desi_dr2/desi_bao_all.py"
    ),
    Path(
        "/media/udt-admin/ScratchDisk/Data/BAO/CobayaSampler_cobaya/"
        "cobaya/likelihoods/bao/desi_dr2/desi_bao_all.yaml"
    ),
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def copy_one(source: Path, target: Path, role: str, records: list[dict[str, object]]) -> None:
    if not source.is_file():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    records.append(
        {
            "role": role,
            "source": str(source),
            "intake_path": str(target.relative_to(target.parents[1])),
            "bytes": target.stat().st_size,
            "sha256": digest(target),
        }
    )


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_bao_suitability_review_", dir="/tmp"))
    records: list[dict[str, object]] = []

    for name in PACKAGE_FILES:
        copy_one(PACKAGE / name, intake / "package" / name, "audit_package", records)
    for name in REPO_SOURCES:
        copy_one(REPO / name, intake / "repository_sources" / name, "repository_source", records)
    for index, source in enumerate(EXTERNAL_SOURCES, start=1):
        copy_one(
            source,
            intake / "external_sources" / f"{index:02d}_{source.name}",
            "external_source",
            records,
        )

    scope = {
        "status": "SEALED_READ_ONLY_REVIEW_INTAKE",
        "question": "observed correlation-pattern data suitability only",
        "forbidden": [
            "edit source repository",
            "continue research",
            "fit UDT",
            "estimate X_max",
            "import acoustic-scale, standard-ruler, yardstick, or Lambda-CDM ontology",
            "access anything outside this intake",
        ],
        "n_files": len(records),
        "files": records,
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"intake": str(intake), "scope_sha256": digest(scope_path), "n_files": len(records)}))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build a sealed, source-bounded G292 external-review intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent

PACKAGE_FILES = (
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "CATCH_PROOF_RESULT.json",
    "COMPLETENESS_MAP.md",
    "DERIVATION_RESULT.json",
    "EVIDENCE_GATES.md",
    "EXACT_DERIVATION.md",
    "INDEPENDENT_VERIFICATION.json",
    "LAY_REPORT.md",
    "MAP.md",
    "PACKAGE_VERIFICATION_RESULT.json",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "RUN_RECORD.md",
    "STATUS_LEDGER.tsv",
    "derive_orientable_screen_flux.py",
    "run_orientable_screen_flux_catches.py",
    "verify_orientable_screen_flux_independent.py",
    "verify_package.py",
)

SOURCE_PATHS = (
    "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "udt_g225_shared_event_normal_screen_carry_2026-08-22/AUDIT_REPORT.md",
    "udt_g225_shared_event_normal_screen_carry_2026-08-22/EXACT_DERIVATION.md",
    "udt_g226_null_chain_conformal_symplectic_assembly_2026-08-22/EXACT_DERIVATION.md",
    "udt_g270_completed_pair_transported_screen_ownership_2026-08-26/EXACT_DERIVATION.md",
    "udt_g290_metric_native_topology_history_bridge_whiteboard_2026-08-28/EXACT_DERIVATION.md",
    "udt_g290_metric_native_topology_history_bridge_whiteboard_2026-08-28/EXTERNAL_REVIEW_GPT54.md",
    "udt_g291_global_screen_flux_ownership_whiteboard_2026-08-28/PANEL_SYNTHESIS.md",
    "udt_g291_global_screen_flux_ownership_whiteboard_2026-08-28/WHITEBOARD_REPORT.md",
)

PROTECTED_FRAGMENTS = (
    "8_25",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10",
    "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12",
    "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12",
    "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_checked(relative: str, destination: Path) -> tuple[str, int, str]:
    if any(fragment in relative for fragment in PROTECTED_FRAGMENTS):
        raise AssertionError(f"protected path rejected: {relative}")
    source = ROOT / relative
    if not source.is_file():
        raise FileNotFoundError(source)
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return relative, target.stat().st_size, sha256(target)


def main() -> None:
    destination = Path(tempfile.mkdtemp(prefix="udt_g292_review_", dir="/tmp"))

    for filename in PACKAGE_FILES:
        copy_checked(f"{PACKAGE.name}/{filename}", destination)

    source_rows = [copy_checked(relative, destination) for relative in SOURCE_PATHS]
    source_manifest = destination / "SOURCE_MANIFEST.tsv"
    with source_manifest.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("source", "bytes", "sha256"))
        writer.writerows(source_rows)

    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, stdout=subprocess.PIPE
    ).stdout.strip()
    scope = {
        "audit": "G292_ORIENTABLE_SCREEN_DIFFERENTIAL_CHARACTER_DESCENT",
        "mode": "fresh read-only adversarial review",
        "allowed": (
            "inspect only the sealed intake; independently recompute the orientable screen "
            "differential-character descent, sky/pair typing, and global metric counterfamily; "
            "run registered replays or bounded checks only in a writable ephemeral copy"
        ),
        "forbidden": (
            "edit evidence files, continue the research, access repository files outside the "
            "intake or protected packages, use the internet, inspect observational outcomes, or "
            "import an action, source, field equation, matter model, mass, scale selection, Planck "
            "cutoff, physical history, pair or loop population, boundary, X_max, or canonization"
        ),
        "scientific_ceiling": (
            "bounded conditional orientable fixed-rank screen differential-character descent, "
            "supplied sky/pair identification, global same-pair-state same-Euler-class "
            "different-local-flux metric family, and explicit nonselection"
        ),
        "repository_head_at_seal": head,
        "immutable_sources": len(SOURCE_PATHS),
        "package_payloads": len(PACKAGE_FILES),
    }
    (destination / "REVIEW_SCOPE.json").write_text(
        json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    manifest_rows = []
    for path in sorted(item for item in destination.rglob("*") if item.is_file()):
        relative = path.relative_to(destination).as_posix()
        if any(fragment in relative for fragment in PROTECTED_FRAGMENTS):
            raise AssertionError(f"protected path entered intake: {relative}")
        manifest_rows.append((relative, path.stat().st_size, sha256(path)))
    manifest = destination / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "bytes", "sha256"))
        writer.writerows(manifest_rows)
    seal = destination / "REVIEW_MANIFEST.sha256"
    seal.write_text(f"{sha256(manifest)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")

    print(json.dumps({
        "path": str(destination),
        "payloads": len(manifest_rows),
        "total_files": len(manifest_rows) + 2,
        "scope_sha256": sha256(destination / "REVIEW_SCOPE.json"),
        "manifest_sha256": sha256(manifest),
        "seal_sha256": sha256(seal),
        "immutable_sources": len(SOURCE_PATHS),
        "package_payloads": len(PACKAGE_FILES),
        "repository_head_at_seal": head,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

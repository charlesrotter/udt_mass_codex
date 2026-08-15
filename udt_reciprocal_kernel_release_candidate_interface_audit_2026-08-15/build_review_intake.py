#!/usr/bin/env python3
"""Build a sealed, read-only G93 review intake from the package and frozen sources."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXCLUDED_PACKAGE_FILES = {
    "EXTERNAL_ADVERSARIAL_REVIEW.md",
    "EXTERNAL_REVIEW_ADJUDICATION.md",
}
SNE_PACKAGE_FILES = {
    "PROVISIONAL_RADIATIVE_INTERFACE.md",
    "SNE_EXTERNAL_REVIEW_DISPATCH.md",
    "SNE_REPLAY_PREREGISTRATION.md",
    "SNE_REPLAY_VERIFIER_CORRECTION_PREREGISTRATION.md",
    "run_complete_geometry_sne_replay.py",
    "verify_complete_geometry_sne_independent.py",
    "verify_sne_replay_package.py",
    "run_sne_replay_catch_proofs.py",
    "SNE_COMPLETE_GEOMETRY_CURVE.tsv",
    "SNE_COMPLETE_GEOMETRY_RESULT.json",
    "SNE_COMPLETE_GEOMETRY_INDEPENDENT.json",
    "SNE_REPLAY_REPORT.md",
    "SNE_REPLAY_EVIDENCE_GATES.md",
    "SNE_REPLAY_VERIFICATION.json",
    "SNE_REPLAY_CATCH_PROOF.json",
}
SNE_SOURCE_PATHS = (
    "Data/Pantheon+SH0ES.dat",
    "Data/Pantheon+SH0ES_STAT+SYS.cov",
    "udt_cmb_G68_F01_F02_finite_path_jacobi_controls_2026-08-11/solve_finite_path.py",
    "udt_cmb_G79_same_geometry_dimensional_sne_query_2026-08-11/EXACT_DERIVATION.md",
    "udt_cmb_G79_same_geometry_dimensional_sne_query_2026-08-11/EXTERNAL_REVIEW_ADJUDICATION.md",
    "udt_cmb_G79_same_geometry_dimensional_sne_query_2026-08-11/verify_same_geometry_sne_independent.py",
    "udt_sne_native_observer_query_replay_2026-08-11/EXACT_DERIVATION.md",
    "udt_sne_native_observer_query_replay_2026-08-11/EXTERNAL_REVIEW_ADJUDICATION.md",
    "udt_sne_native_observer_query_replay_2026-08-11/REPLAY_RESULT.json",
    "udt_native_flux_luminosity_law_ownership_audit_2026-08-15/EXACT_DERIVATION.md",
    "udt_native_flux_luminosity_law_ownership_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
    "udt_native_radiative_current_energy_owner_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
    "udt_null_carrier_measure_ownership_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
    "udt_uncompressed_pair_kernel_reconstruction_2026-08-14/EXACT_DERIVATION.md",
    "udt_uncompressed_pair_kernel_reconstruction_2026-08-14/EXTERNAL_REVIEW_ADJUDICATION.md",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--sne", action="store_true")
    args = parser.parse_args()
    prefix = "udt_g93_sne_review_" if args.sne else "udt_g93_kernel_review_"
    output = args.output or Path(tempfile.mkdtemp(prefix=prefix, dir="/tmp"))
    if args.output:
        output.mkdir(parents=True, exist_ok=False)

    if args.sne:
        package_files = sorted(HERE / name for name in SNE_PACKAGE_FILES)
        source_files = [ROOT / relative for relative in SNE_SOURCE_PATHS]
    else:
        package_files = sorted(
            path
            for path in HERE.iterdir()
            if path.is_file() and path.name not in EXCLUDED_PACKAGE_FILES
        )
        with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
            manifest_rows = list(csv.DictReader(handle, delimiter="\t"))
        source_files = [ROOT / row["path"] for row in manifest_rows]

    payload: dict[str, Path] = {}
    for path in package_files + source_files:
        relative = str(path.relative_to(ROOT))
        if relative in payload and payload[relative] != path:
            raise SystemExit(f"intake path collision: {relative}")
        if path.is_symlink() or not path.is_file():
            raise SystemExit(f"non-regular intake source: {relative}")
        payload[relative] = path

    records = []
    for relative, source in sorted(payload.items()):
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        destination.chmod(0o444)
        records.append(
            {
                "path": relative,
                "bytes": destination.stat().st_size,
                "sha256": sha256(destination),
            }
        )

    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    scope = {
        "schema": "udt.external_readonly_review_scope.v1",
        "package": HERE.name + ("::complete_geometry_sne_replay" if args.sne else ""),
        "git_head": head,
        "payload_count": len(records),
        "payload": records,
        "permissions": {
            "read_only": True,
            "may_edit": False,
            "may_continue_research": False,
            "may_access_outside_intake": False,
        },
        "explicit_exclusions": [
            "protected curvature/holonomy atlas",
            "stopped native-on-shell draft",
            "protected G88 SNe/Xmax package",
            "protected pair-regime-flow package",
            "all repository files not copied into this intake",
        ],
    }
    scope_path = output / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    scope_path.chmod(0o444)
    output.chmod(0o555)
    print(
        json.dumps(
            {
                "intake": str(output),
                "payload_count": len(records),
                "review_scope_sha256": sha256(scope_path),
                "git_head": head,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

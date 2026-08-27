#!/usr/bin/env python3
"""Fail-closed preregistration and frozen-source verifier for G283."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from verify_preregistration_chronology import verify_chronology


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def read_tsv(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    scope = read_tsv("SOURCE_SCOPE.tsv")
    manifest_rows = read_tsv("SOURCE_MANIFEST.tsv")
    premises = read_tsv("PREMISE_LEDGER.tsv")
    manifest = {row["path"]: row for row in manifest_rows}
    scope_paths = [row["path"] for row in scope]
    protected = (
        "udt_native_onshell_timelive_reset_owner_audit_2026-08-10",
        "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12",
        "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12",
        "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02",
    )
    prereg = (PACKAGE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    chronology = verify_chronology()
    checks = {
        "source_count_12": len(scope) == len(manifest_rows) == 12,
        "scope_manifest_exact": set(scope_paths) == set(manifest),
        "source_hashes_and_sizes_exact": all(
            (ROOT / path).is_file()
            and sha256(ROOT / path) == manifest[path]["sha256"]
            and str((ROOT / path).stat().st_size) == manifest[path]["bytes"]
            for path in scope_paths
        ),
        "protected_sources_excluded": not any(
            fragment in path for fragment in protected for path in scope_paths
        ),
        "premise_rows_17": len(premises) == 17,
        "candidate_landings_4": sum(line.startswith("- `") for line in prereg.splitlines()) >= 4,
        "arbitrary_T_witness_frozen": "T:I -> Sym(2,R)" in prereg and "T_3(u)" in prereg,
        "three_law_homes_tested": all(
            token in (PACKAGE / "MAP.md").read_text(encoding="utf-8")
            for token in ("metric two-jet/curvature", "first-order coframe/connection/curvature", "global neighboring-relation/Jacobi network")
        ),
        "field_law_outcomes_Xmax_omitted": all(
            token in prereg
            for token in ("no adopted field equation", "fit observations", "scale or `X_max`")
        ),
        "object_level_preregistration_chronology_verified": (
            chronology["status"] == "PASS" and all(chronology["checks"].values())
        ),
    }
    if not all(checks.values()):
        raise AssertionError({name: value for name, value in checks.items() if not value})
    print(
        {
            "audit": "G283_PREREGISTRATION_VERIFICATION",
            "status": "PASS",
            "sources": len(scope),
            "premises": len(premises),
            "checks": checks,
        }
    )


if __name__ == "__main__":
    main()

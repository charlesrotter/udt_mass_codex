#!/usr/bin/env python3
"""Fail-closed verifier for the frozen G282 preregistration."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    scope = rows("SOURCE_SCOPE.tsv")
    manifest = rows("SOURCE_MANIFEST.tsv")
    premises = rows("PREMISE_LEDGER.tsv")
    preregistration = (PACKAGE / "PREREGISTRATION.md").read_text()
    map_text = (PACKAGE / "MAP.md").read_text()

    scope_paths = [row["path"] for row in scope]
    manifest_paths = [row["path"] for row in manifest]
    protected_fragments = (
        "udt_native_onshell_timelive_reset_owner_audit_2026-08-10",
        "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12",
        "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12",
        "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02",
    )
    source_checks = {}
    for row in manifest:
        path = ROOT / row["path"]
        source_checks[row["path"]] = (
            path.is_file()
            and path.stat().st_size == int(row["bytes"])
            and sha256(path) == row["sha256"]
        )

    checks = {
        "source_count_18": len(scope) == len(manifest) == 18,
        "scope_manifest_same_order": scope_paths == manifest_paths,
        "sources_unique": len(scope_paths) == len(set(scope_paths)),
        "all_sources_hash_and_size_match": bool(source_checks) and all(source_checks.values()),
        "protected_sources_excluded": not any(
            fragment in path for fragment in protected_fragments for path in scope_paths
        ),
        "premise_rows_17": len(premises) == 17,
        "premise_ids_exact": [row["id"] for row in premises] == [f"P{i:02d}" for i in range(1, 18)],
        "metric_led_mode": "Mode: METRIC_LED" in preregistration,
        "three_candidate_landings": all(
            token in preregistration
            for token in (
                "OWNED_JOINT_DEPTH_JACOBI_HISTORY_LAW_FOUND",
                "NO_OWNED_JOINT_HISTORY_LAW__NEIGHBOR_RELATION_CURVATURE_CONSTRAINT_REQUIRED",
                "CURRENT_PREMISES_INCONSISTENT_WITH_JOINT_METRIC_EVALUATION",
            )
        ),
        "negative_order_scope_guard": (
            "first-order coframe/connection system" in preregistration
            and "global neighboring-relation law" in preregistration
        ),
        "no_candidate_adopted": "No candidate physical law will be adopted in G282." in map_text,
        "outcomes_omitted": any(
            row["id"] == "P16" and row["status"] == "OMITTED" for row in premises
        ),
        "field_law_omitted": any(
            row["id"] == "P17" and row["status"] == "OMITTED" for row in premises
        ),
    }
    if not all(checks.values()):
        raise AssertionError(
            json.dumps(
                {
                    "checks": checks,
                    "failed": [name for name, passed in checks.items() if not passed],
                    "source_checks": source_checks,
                },
                indent=2,
                sort_keys=True,
            )
        )
    print(
        json.dumps(
            {
                "audit": "G282_PREREGISTRATION_VERIFICATION",
                "status": "PASS",
                "checks": checks,
                "counts": {
                    "sources": len(scope),
                    "premises": len(premises),
                    "candidate_landings": 3,
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

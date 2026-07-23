#!/usr/bin/env python3
"""Freeze the exact prior evidence used by the intrinsic-object audit."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT_MANIFEST = (
    ROOT / "udt_complete_metric_realization_zoomout_2026-07-23/SOURCE_MANIFEST.sha256"
)

ADDITIONS = [
    "udt_complete_metric_realization_zoomout_2026-07-23/AUDIT_REPORT.md",
    "udt_complete_metric_realization_zoomout_2026-07-23/STATUS_LEDGER.tsv",
    "udt_complete_metric_realization_zoomout_2026-07-23/LAYER_SURVIVAL_LEDGER.tsv",
    "udt_complete_metric_realization_zoomout_2026-07-23/JOIN_GRAPH.tsv",
    "udt_complete_metric_realization_zoomout_2026-07-23/BOOTSTRAP_REALIZATION_MATRIX.tsv",
    "udt_chart_coframe_invariance_atlas_2026-07-21/AUDIT_REPORT.md",
    "udt_joint_invariant_subspace_atlas_2026-07-21/AUDIT_REPORT.md",
    "udt_joint_invariant_subspace_atlas_2026-07-21/ATLAS_RESULT.json",
    "udt_local_selector_holonomy_closure_2026-07-22/ATLAS_RESULT.json",
    "udt_global_metric_assembly_atlas_2026-07-22/ATLAS_RESULT.json",
    "udt_instrument_motif_atlas_2026-07-21/AUDIT_REPORT.md",
    "udt_structural_ensemble_metric_atlas_2026-07-21/CONFIGURATION_OBSERVATIONS.tsv",
    "metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    paths = [
        line.split("  ", 1)[1]
        for line in PARENT_MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    paths.extend(ADDITIONS)
    unique = sorted(set(paths))
    if len(unique) != len(paths):
        raise AssertionError("duplicate source path")
    missing = [path for path in unique if not (ROOT / path).is_file()]
    if missing:
        raise FileNotFoundError(missing)
    lines = [f"{digest(ROOT / path)}  {path}" for path in unique]
    (HERE / "SOURCE_MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"sources={len(lines)}")


if __name__ == "__main__":
    main()

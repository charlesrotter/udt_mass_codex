#!/usr/bin/env python3
"""Build deterministic source inventory for the reciprocal-c correction."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
SOURCES = [
    ("UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md", "FOUNDING_DERIVATION", "owner-origin reciprocal-c identity and complete short metric chain"),
    ("UDT_RECIPROCAL_C_FOUNDING_POSTULATE_MAP.md", "FOUNDING_PREREGISTRATION", "named channel formalizations and falsification gates"),
    ("UDT_NATIVE_ACTION_COLD_PACKET.md", "CURRENT_FOUNDATION", "synchronized Reciprocal-c dual Reciprocity composition CSN and readout stamps"),
    ("UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md", "CURRENT_FOUNDATION", "pre-scale equivalence and physical representative boundary"),
    ("projective_position_join_audit_2026-07-19/SHA256SUMS.txt", "IMMUTABILITY_ANCHOR", "first corrected package identity"),
    ("projective_position_direction_magnitude_correction_2026-07-19/SHA256SUMS.txt", "IMMUTABILITY_ANCHOR", "immediately corrected package identity"),
    ("projective_position_direction_magnitude_correction_2026-07-19/AUDIT_REPORT.md", "CORRECTED_PRIOR_EVIDENCE", "false symmetric clock-selector statements and surviving direction correction"),
    ("projective_position_direction_magnitude_correction_2026-07-19/DERIVATION_RESULT.json", "CORRECTED_PRIOR_EVIDENCE", "sech candidate definitions and clock status"),
    ("xmax_full_frame_realization_2026-07-19/AUDIT_REPORT.md", "CURRENT_FRAME_EVIDENCE", "complete frame character and additive-depth coframe"),
    ("xmax_dynamic_observer_frame_2026-07-19/AUDIT_REPORT.md", "CURRENT_FRAME_EVIDENCE", "ordered dynamic frame scope"),
    ("xmax_accelerating_finite_cell_cartan_2026-07-19/AUDIT_REPORT.md", "CURRENT_FRAME_EVIDENCE", "accelerating coframe algebra scope"),
    ("UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "CURRENT_FRONTIER", "pre-correction current open ledger"),
    ("CANON.md", "BINDING_SCOPE_SOURCE", "static finite-cell seal only; no new canon"),
]


def main() -> None:
    rows = []
    for path, status, role in SOURCES:
        target = ROOT / path
        if not target.is_file():
            raise FileNotFoundError(path)
        tracked = subprocess.run(["git", "ls-files", "--error-unmatch", path], cwd=ROOT, capture_output=True, text=True)
        if tracked.returncode:
            raise AssertionError(f"untracked source: {path}")
        rows.append({
            "path": path,
            "status": status,
            "role": role,
            "bytes": str(target.stat().st_size),
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        })
    output = HERE / "SOURCE_INVENTORY.tsv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "status", "role", "bytes", "sha256"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"PASS sources={len(rows)} output={output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

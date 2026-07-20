#!/usr/bin/env python3
"""Build deterministic source inventory for the correction package."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
SOURCES = [
    ("projective_position_join_audit_2026-07-19/AUDIT_REPORT.md", "CORRECTED_PRIOR_EVIDENCE", "signed-position wording and bounded chart result"),
    ("projective_position_join_audit_2026-07-19/DERIVATION_RESULT.json", "CORRECTED_PRIOR_EVIDENCE", "load-bearing ordered comparison and counterfamily algebra"),
    ("projective_position_join_audit_2026-07-19/STATUS_LEDGER.tsv", "CORRECTED_PRIOR_EVIDENCE", "claims requiring overlay"),
    ("projective_position_join_audit_2026-07-19/SHA256SUMS.txt", "IMMUTABILITY_ANCHOR", "prior package byte identity"),
    ("UDT_NATIVE_ACTION_COLD_PACKET.md", "CURRENT_FOUNDATION", "difference composition reversal reciprocal pair CSN and seal"),
    ("UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md", "CURRENT_FOUNDATION", "common-scale-neutral observables and limits"),
    ("xmax_full_frame_realization_2026-07-19/AUDIT_REPORT.md", "CURRENT_FRAME_EVIDENCE", "projective chart and L dphi coframe distinction"),
    ("xmax_dynamic_observer_frame_2026-07-19/AUDIT_REPORT.md", "CURRENT_FRAME_EVIDENCE", "dynamic ordered frame transformation scope"),
    ("xmax_accelerating_finite_cell_cartan_2026-07-19/AUDIT_REPORT.md", "CURRENT_FRAME_EVIDENCE", "accelerating coframe algebra and interpretation limit"),
    ("metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md", "CURRENT_METRIC_EVIDENCE", "radial-angular metric and open intrinsic direction geometry"),
    ("UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "CURRENT_FRONTIER", "current open action carrier and selector seam"),
    ("CANON.md", "BINDING_SCOPE_SOURCE", "static seal parity and absolute Phi zero"),
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

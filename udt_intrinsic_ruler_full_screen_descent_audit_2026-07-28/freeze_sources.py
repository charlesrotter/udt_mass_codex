#!/usr/bin/env python3
"""Freeze load-bearing sources from the preregistered fixed base."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path

BASE = "97d85edb7da351e6a96bb8c55b4e969ea8e3a749"
HERE = Path(__file__).resolve().parent
SOURCES = [
    ("CURRENT_SCIENTIFIC_PREMISES.md", "premise_controller"),
    ("CURRENT_SCIENTIFIC_PREMISES.tsv", "premise_controller"),
    ("UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "frontier"),
    ("udt_full_screen_hopf_toric_rederivation_2026-07-28/AUDIT_REPORT.md", "parent_dispatch"),
    ("udt_full_screen_hopf_toric_rederivation_2026-07-28/EXACT_DERIVATION.md", "parent_dispatch"),
    ("udt_full_screen_hopf_toric_rederivation_2026-07-28/STATUS_LEDGER.tsv", "parent_status"),
    ("udt_full_screen_hopf_toric_rederivation_2026-07-28/DERIVATION_RESULT.json", "parent_algebra"),
    ("udt_full_screen_hopf_toric_rederivation_2026-07-28/NEXT_STEP.md", "authorized_gate"),
    ("udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/AUDIT_REPORT.md", "intrinsic_pair_owner"),
    ("udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/EXACT_DERIVATION.md", "intrinsic_pair_owner"),
    ("udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/STATUS_LEDGER.tsv", "intrinsic_pair_status"),
    ("udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/CANDIDATE_OUTCOMES.tsv", "rank_three_certificate"),
    ("udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/PREREGISTRATION.md", "profile_definition"),
    ("udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/verify_global_coframe.py", "Maurer_Cartan_convention"),
    ("udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/AUDIT_REPORT.md", "intrinsic_screen_scope"),
    ("udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/EXACT_DERIVATION.md", "intrinsic_screen_scope"),
    ("udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/STATUS_LEDGER.tsv", "intrinsic_screen_status"),
    ("udt_general_screen_complete_cell_atlas_2026-07-28/AUDIT_REPORT.md", "general_screen_owner"),
    ("udt_general_screen_complete_cell_atlas_2026-07-28/EXACT_DERIVATION.md", "general_screen_owner"),
    ("udt_general_screen_complete_cell_atlas_2026-07-28/GENERAL_CARTAN_RESULT.json", "general_screen_algebra"),
    ("udt_general_screen_complete_cell_atlas_2026-07-28/derive_general_screen.py", "general_screen_algebra"),
    ("native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md", "carrier_boundary"),
    ("native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv", "carrier_boundary"),
]


def git(*args: str, binary: bool = False):
    output = subprocess.check_output(["git", *args], cwd=HERE.parent)
    return output if binary else output.decode().strip()


def main() -> None:
    rows = []
    for path, role in SOURCES:
        data = git("show", f"{BASE}:{path}", binary=True)
        rows.append({
            "path": path,
            "role": role,
            "blob": git("rev-parse", f"{BASE}:{path}"),
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
        })
    with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    identity = hashlib.sha256(
        "\n".join(row["path"] + "\t" + row["blob"] for row in rows).encode()
    ).hexdigest()
    print(f"base={BASE}")
    print(f"sources={len(rows)}")
    print(f"identity_sha256={identity}")


if __name__ == "__main__":
    main()

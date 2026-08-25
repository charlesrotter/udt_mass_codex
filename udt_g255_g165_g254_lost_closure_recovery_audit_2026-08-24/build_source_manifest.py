#!/usr/bin/env python3
"""Freeze the G255 source universe from the deterministic slot census."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    with (PACKAGE / "SLOT_CENSUS.tsv").open(newline="", encoding="utf-8") as handle:
        slots = list(csv.DictReader(handle, delimiter="\t"))
    assert len(slots) == 90
    paths = {
        "CURRENT_SCIENTIFIC_PREMISES.tsv",
        "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
    }
    for slot in slots:
        paths.add(slot["primary_report"])
        if slot["exact_derivation"]:
            paths.add(slot["exact_derivation"])
        directory = ROOT / slot["directory"]
        for name in ("PREMISE_LEDGER.tsv", "STATUS_LEDGER.tsv"):
            candidate = directory / name
            if candidate.is_file():
                paths.add(candidate.relative_to(ROOT).as_posix())
    rows = []
    for relative in sorted(paths):
        source = ROOT / relative
        assert source.is_file(), relative
        assert "udt_native_onshell_timelive_reset_owner_audit_2026-08-10" not in relative
        assert "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12" not in relative
        assert "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12" not in relative
        assert "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" not in relative
        rows.append({"path": relative, "sha256": sha256(source)})
    destination = PACKAGE / "SOURCE_MANIFEST.tsv"
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=("path", "sha256"), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"{destination}\t{len(rows)}")


if __name__ == "__main__":
    main()

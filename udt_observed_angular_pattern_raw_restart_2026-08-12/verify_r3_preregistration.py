#!/usr/bin/env python3
"""Outcome-absence and scope gate for the R3 preregistration."""

from __future__ import annotations

import json
from pathlib import Path

import run_r2_central_pattern as r2
import run_r3_covariance_atlas as r3


ROOT = Path(__file__).resolve().parent


def main() -> int:
    required = (
        "R3_PREREGISTRATION.md", "R3_PREMISE_LEDGER.tsv", "R3_FALSIFICATION_CONTRACT.tsv",
        "R3_ENGINE_PROVENANCE.tsv", "R3_PREFLIGHT_NOTE.md", "R3_BLOCK_ATLAS.tsv",
        "R3_BLOCK_RESULT.json", "R3_SYNTHETIC_PREFLIGHT_RESULT.json",
        "run_r3_covariance_atlas.py", "verify_r3.py",
    )
    assert all((ROOT / name).exists() for name in required)
    forbidden = (
        "R3_COVARIANCE_CELLS", "R3_COVARIANCE_SUMMARY.tsv", "R3_CENTRAL_ENGINE_COMPARISON.tsv",
        "R3_RESOURCE_OBSERVED.tsv", "R3_RESULT.json", "R3_RUN.log", "R3_OUTPUT_MANIFEST.tsv",
        "R3_VERIFICATION_RESULT.json",
    )
    assert all(not (ROOT / name).exists() for name in forbidden)
    blocks = json.loads((ROOT / "R3_BLOCK_RESULT.json").read_text())
    synthetic = json.loads((ROOT / "R3_SYNTHETIC_PREFLIGHT_RESULT.json").read_text())
    assert blocks["status"] == "OBSERVED__RANDOM_ONLY_BLOCK_GEOMETRY_FROZEN"
    assert blocks["atlas_rows"] == 2351 and blocks["galaxy_catalog_read"] is False
    assert blocks["r2_curve_or_descriptor_read"] is False
    assert synthetic["status"] == "PASS"
    assert r3.NSIDES == (4, 8, 16) and r3.RATIO == 20 and r3.NBIN == 119
    assert tuple(r3.LANES) == ("W0_UNIT", "W1_SPECTRO", "W2_IMAGING", "W3_OFFICIAL_OBS")
    selections = sum(sum(1 for _ in r2.groups(sample)) * 2 for sample in ("CMASS", "LOWZ"))
    assert selections == 194
    prereg = (ROOT / "R3_PREREGISTRATION.md").read_text()
    for phrase in (
        "No inverse, pseudoinverse", "No individual R2 feature", "outcome-blindness caveat",
        "NSIDE=16", "NSIDE=8", "NSIDE=4", "all four R2 weight lanes",
    ):
        assert phrase.lower() in prereg.lower()
    print("PASS: R3 preregistration (194 selections, 4 lanes, 3 NSIDEs, no covariance outcome)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

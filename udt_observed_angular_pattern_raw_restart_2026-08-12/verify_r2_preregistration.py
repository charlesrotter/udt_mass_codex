#!/usr/bin/env python3
"""Pre-outcome R2 scope and contamination verifier."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import run_r1_ingestion_nulls as r1
import run_r2_central_pattern as r2


ROOT = Path(__file__).resolve().parent


def main() -> int:
    assert r2.Corrfunc.__version__ == "2.5.3"
    assert len(list(r2.all_units())) == 194
    assert len(r2.LANES) * len(r2.RATIOS) * 194 == 2328
    assert len(r2.EDGES_DEG) - 1 == 119
    assert len(list(r2.groups("LOWZ"))) == 49
    assert len(list(r2.groups("CMASS"))) == 48

    engine = json.loads((ROOT / "R2_PREENGINE_RESULT.json").read_text())
    assert engine["status"] == "PASS" and engine["galaxy_catalog_read"] is False
    assert all(row["integer_counts_exact"] for row in engine["large_random_only"])
    assert all(row["integer_counts_exact"] for row in engine["compact_direct"])

    with (ROOT / "R2_ENGINE_PROVENANCE.tsv").open(newline="") as handle:
        provenance = list(csv.DictReader(handle, delimiter="\t"))
    assert [row["engine"] for row in provenance] == ["Corrfunc", "TreeCorr", "SciPy"]

    local_artifacts = {
        "Corrfunc": Path("/tmp/corrfunc-2.5.3-cp310-cp310-linux_x86_64.whl"),
        "TreeCorr": Path("/tmp/treecorr-5.1.3-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"),
    }
    for row in provenance[:2]:
        path = local_artifacts[row["engine"]]
        if path.exists():
            assert path.stat().st_size == int(row["bytes"])
            assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]

    for name in r2.FINAL_NAMES:
        assert not (ROOT / name).exists(), f"outcome artifact exists before execution: {name}"
    assert not (ROOT / "R2_VERIFICATION_RESULT.json").exists()
    checkpoint_dir = Path("/tmp/udt_boss_r2_checkpoints")
    if checkpoint_dir.exists():
        assert not list(checkpoint_dir.glob("*.npz")), "R2 component checkpoint exists before banked preregistration"

    text = (ROOT / "R2_PREREGISTRATION.md").read_text()
    exclusions = (
        "no Lambda-CDM", "no acoustic scale", "no expected feature angle", "no SNe profile",
        "no fitting", "no physical origin",
    )
    assert all(item in text for item in exclusions)
    print("PASS: R2 preregistration (194 selections, 2328 curves, 119 bins; no galaxy outcome)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Verify R5 was fully preregistered before any R5 outcome exists."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARENT_HASHES = {
    "R2_CURVE_ATLAS.tsv": "32b592a85cbadbc080391353be6d0ee73a2d0d8a37c10aead28e041a7810f603",
    "R4_RELATION_ATLAS.tsv": "1badac0c2eeedb2932a8d53f6116d4bfa247774c76f5750ad652da9f35696184",
    "R4_VERIFICATION_RESULT.json": "1028f4f80578995c20e5f020db4fbfafc9b73e64589e2fd055f0f3763469b05b",
    "R3_OUTPUT_MANIFEST.tsv": "3a38784ac248997bd987598308b98edbf60566759e4fdc35d54d98b161a11cfa",
}
OUTCOMES = (
    "R5_VIEW_SPECTRA.tsv",
    "R5_RANKED_SUBSPACE_OVERLAPS.tsv",
    "R5_COVARIANCE_MODE_ATLAS.tsv",
    "R5_COVARIANCE_MODE_SUMMARY.tsv",
    "R5_RESULT.json",
    "R5_OUTPUT_MANIFEST.tsv",
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    for name, expected in PARENT_HASHES.items():
        assert digest(HERE / name) == expected, name
    for name in OUTCOMES:
        assert not (HERE / name).exists(), f"R5 outcome already exists: {name}"

    prereg = (HERE / "R5_PREREGISTRATION.md").read_text()
    ledger = (HERE / "R5_PREMISE_LEDGER.tsv").read_text()
    contract = (HERE / "R5_FALSIFICATION_CONTRACT.tsv").read_text()
    source_path = HERE / "run_r5_common_subspace_atlas.py"
    source = source_path.read_text()
    ast.parse(source)

    required_prereg = (
        "2,607", "3,555", "275,868", "2,850",
        "No rank truncation", "No threshold labels", "full singular spectrum",
        "Zero cross-cap covariance remains `CHOSE`", "discovery/confirmation",
        "R5_ASSEMBLY_OR_VERIFICATION_FAILURE_TO_AUDIT",
    )
    for token in required_prereg:
        assert token in prereg, token
    for token in ("R5P07", "R5P08", "R5P09", "R5P12", "R5P14", "R5P15"):
        assert token in ledger, token
    for token in ("R5G04", "R5G05", "R5G06", "R5G08", "R5G11", "R5G13"):
        assert token in contract, token

    spec = importlib.util.spec_from_file_location("r5_preregistered_runner", source_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    assert module.RELATION_COUNTS == {
        "RANDOM_DENSITY": 1552,
        "WEIGHT_LANE": 1746,
        "CAP": 1164,
        "ADJACENT_SHELL": 2184,
        "COARSE_FINE_CONTAINMENT": 2640,
    }
    assert module.TRANSFORMS == ("CENTERED_UNIT", "FIRST_DIFFERENCE_UNIT")
    assert 11 * (119 + 118) == 2607
    assert 15 * (119 + 118) == 3555
    assert 1164 * (119 + 118) == 275868
    assert 4 * 3 * (119 + 118) + 2 * 3 == 2850
    assert "argmax" not in source
    assert "explained_variance" not in source
    print("PASS: R5 preregistration, frozen parents, complete censuses, and no outcome artifacts")


if __name__ == "__main__":
    main()

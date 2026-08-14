#!/usr/bin/env python3
"""Verify the frozen R4 contract without evaluating R4 outcome descriptors."""

from __future__ import annotations

import ast
import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_HASHES = {
    "R2_CURVE_ATLAS.tsv": "32b592a85cbadbc080391353be6d0ee73a2d0d8a37c10aead28e041a7810f603",
    "R2_OUTPUT_MANIFEST.tsv": "6eb143be6c41d4047eab1714de322ce15b8530646456cb6bc0ed43f237333031",
    "R3_OUTPUT_MANIFEST.tsv": "3a38784ac248997bd987598308b98edbf60566759e4fdc35d54d98b161a11cfa",
    "R3_FINAL_EVIDENCE_MANIFEST.tsv": "7c609d70b1d55122885c58705dcef9eeb81ca6ded17ec0d550985bd5ecc1913e",
}
EXPECTED_RELATIONS = {
    "RANDOM_DENSITY": 1552,
    "WEIGHT_LANE": 1746,
    "CAP": 1164,
    "ADJACENT_SHELL": 2184,
    "COARSE_FINE_CONTAINMENT": 2640,
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def assignment_literal(tree: ast.AST, name: str):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
                return ast.literal_eval(node.value)
    raise AssertionError(f"missing assignment {name}")


def main() -> None:
    for name, expected in EXPECTED_HASHES.items():
        actual = sha256(HERE / name)
        assert actual == expected, (name, actual, expected)

    prereg = (HERE / "R4_PREREGISTRATION.md").read_text()
    for required in (
        "9,286 relations", "1,164 cap-covariance records", "zero-cross-cap-covariance scale",
        "No angular bin is removed or weighted", "No grid is\npreferred",
        "preferred angular scale", "separate implementation",
    ):
        assert required in prereg, required

    with (HERE / "R4_PREMISE_LEDGER.tsv").open(newline="") as handle:
        premise_rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(premise_rows) == 12
    assert any(row["premise_id"] == "R4P08" and row["status"] == "CHOSE" for row in premise_rows)

    with (HERE / "R4_FALSIFICATION_CONTRACT.tsv").open(newline="") as handle:
        gate_rows = list(csv.DictReader(handle, delimiter="\t"))
    assert [row["gate_id"] for row in gate_rows] == [f"R4G{i:02d}" for i in range(1, 11)]

    source_path = HERE / "run_r4_empirical_relation_atlas.py"
    tree = ast.parse(source_path.read_text(), filename=str(source_path))
    assert assignment_literal(tree, "NBIN") == 119
    assert tuple(assignment_literal(tree, "NSIDES")) == (4, 8, 16)
    assert tuple(assignment_literal(tree, "RATIOS")) == (5, 10, 20)
    assert assignment_literal(tree, "RELATION_COUNTS") == EXPECTED_RELATIONS
    assert sum(EXPECTED_RELATIONS.values()) == 9286

    source = source_path.read_text()
    for forbidden in ("curve_fit", "least_squares", "chi2", "p_value", "acoustic_scale"):
        assert forbidden not in source, forbidden
    for required in (
        "np.correlate(ac, bc, mode=\"full\")",
        "np.correlate(dac, dbc, mode=\"full\")",
        "cn + cs",
        "NBIN * eps * lam_max",
        "refusing to overwrite",
    ):
        assert required in source, required

    print("PASS: R4 preregistration and implementation contract")


if __name__ == "__main__":
    main()

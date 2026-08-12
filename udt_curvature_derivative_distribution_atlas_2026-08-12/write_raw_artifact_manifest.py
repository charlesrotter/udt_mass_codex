#!/usr/bin/env python3
"""Write the fixed SHA-256 manifest for load-bearing raw/result artifacts."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ARTIFACTS = (
    "DERIVATIVE_DISTRIBUTION_ATLAS.tsv",
    "PRODUCTION_DERIVATIVE_TENSORS.npz",
    "DERIVATION_RESULT.json",
    "TENSOR_IDENTITY_VERIFICATION.json",
    "INDEPENDENT_COMPARISON.tsv",
    "INDEPENDENT_DERIVATIVE_TENSORS.npz",
    "INDEPENDENT_VERIFICATION.json",
    "ADJUDICATED_DERIVATIVE_ATLAS.tsv",
    "ADJUDICATION_RESULT.json",
    "GRAM_INTRINSIC_SUBSPACE_ATLAS.tsv",
    "GRAM_INTRINSIC_SUBSPACE_RESULT.json",
    "INDEPENDENT_GRAM_INTRINSIC_SUBSPACE_ATLAS.tsv",
    "GRAM_INTRINSIC_SUBSPACE_COMPARISON.tsv",
    "INDEPENDENT_GRAM_INTRINSIC_SUBSPACE_RESULT.json",
    "ADJUDICATED_GRAM_INTRINSIC_SUBSPACE_ATLAS.tsv",
    "GRAM_INTRINSIC_SUBSPACE_ADJUDICATION.json",
)


def main() -> None:
    output = []
    for name in ARTIFACTS:
        path = HERE / name
        if not path.is_file():
            raise RuntimeError(f"missing artifact: {name}")
        output.append({"path": name, "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    with (HERE / "RAW_ARTIFACT_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=("path", "bytes", "sha256"), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)
    print(f"wrote {len(output)} raw artifact hashes")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate the banked first-curvature-derivative atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(
    production: list[dict[str, str]],
    adjudicated: list[dict[str, str]],
    comparison: list[dict[str, str]],
    derivation: dict,
    independent: dict,
    adjudication: dict,
    identities: dict,
    manifest: list[dict[str, str]],
    raw_manifest: list[dict[str, str]],
    gram_production: list[dict[str, str]],
    gram_independent: list[dict[str, str]],
    gram_comparison: list[dict[str, str]],
    gram_adjudicated: list[dict[str, str]],
    gram_production_result: dict,
    gram_independent_result: dict,
    gram_adjudication_result: dict,
    status: list[dict[str, str]],
) -> dict:
    assert len(manifest) == len({row["path"] for row in manifest}) == 9
    base=(HERE / "SOURCE_BASE_COMMIT.txt").read_text().strip()
    for row in manifest:
        path = ROOT / row["path"]
        assert path.is_file()
        if row["path"] in {"CURRENT_SCIENTIFIC_PREMISES.md"}:
            blob=subprocess.run(["git","show",f"{base}:{row['path']}"],cwd=ROOT,capture_output=True,check=True).stdout
            assert hashlib.sha256(blob).hexdigest()==row["sha256"]
        else:
            assert sha(path) == row["sha256"]
    assert len(raw_manifest) == len({row["path"] for row in raw_manifest}) == 16
    for row in raw_manifest:
        path = HERE / row["path"]
        assert path.is_file() and path.stat().st_size == int(row["bytes"]) and sha(path) == row["sha256"]

    assert len(production) == len(adjudicated) == len(comparison) == 1221
    pkeys = [f"{row['scope']}|{row['identity']}|{row['point']}" for row in production]
    assert len(set(pkeys)) == 1221 and pkeys == [row["key"] for row in comparison]
    assert Counter(row["scope"] for row in production) == Counter({"G63": 42, "G85": 1179})
    assert all(row["scope"] == src["scope"] and row["identity"] == src["identity"] and row["point"] == src["point"] for row, src in zip(adjudicated, production))

    expected_prod_spi = {
        "SPI_RANK0_OR_1_UNDERDETERMINED": 11,
        "SPI_RANK2_ALTERNATIVE_PLANE": 392,
        "SPI_RANK3_OR_4_NO_INTRINSIC_2PLANE": 818,
    }
    expected_adj_spi = {
        "SPI_DEGENERATE_OR_NUMERICALLY_UNRESOLVED": 10,
        "SPI_RANK0_OR_1_UNDERDETERMINED": 3,
        "SPI_RANK2_ALTERNATIVE_PLANE": 390,
        "SPI_RANK3_OR_4_NO_INTRINSIC_2PLANE": 818,
    }
    expected_riem = {
        "DERIVATIVE_GRAM_DEFINES_ALTERNATIVE_SPECTRAL_STRUCTURE": 1208,
        "DERIVATIVE_GRAM_DEGENERATE": 1,
        "DERIVATIVE_GRAM_OWNS_REGISTERED_SPLIT": 6,
        "DERIVATIVE_GRAM_PRESERVES_WITHOUT_GAP": 3,
        "NUMERICALLY_UNRESOLVED": 3,
    }
    expected_ric = {
        "DERIVATIVE_GRAM_DEFINES_ALTERNATIVE_SPECTRAL_STRUCTURE": 1203,
        "DERIVATIVE_GRAM_DEGENERATE": 1,
        "DERIVATIVE_GRAM_OWNS_REGISTERED_SPLIT": 6,
        "DERIVATIVE_GRAM_PRESERVES_WITHOUT_GAP": 3,
        "NUMERICALLY_UNRESOLVED": 8,
    }
    expected_weyl = {
        "DERIVATIVE_GRAM_DEFINES_ALTERNATIVE_SPECTRAL_STRUCTURE": 1206,
        "DERIVATIVE_GRAM_DEGENERATE": 1,
        "DERIVATIVE_GRAM_OWNS_REGISTERED_SPLIT": 5,
        "DERIVATIVE_GRAM_PRESERVES_WITHOUT_GAP": 4,
        "NUMERICALLY_UNRESOLVED": 5,
    }
    assert dict(Counter(row["spi_class"] for row in production)) == expected_prod_spi
    assert dict(Counter(row["adjudicated_spi_class"] for row in adjudicated)) == expected_adj_spi
    assert dict(Counter(row["k_riem_class"] for row in production)) == expected_riem
    assert dict(Counter(row["k_ric_class"] for row in production)) == expected_ric
    assert dict(Counter(row["k_weyl_class"] for row in production)) == expected_weyl

    bad = [row for row in comparison if row["pass"] != "TRUE"]
    assert len(bad) == 10
    assert all(row["independent_spi"] == "SPI_DEGENERATE_OR_NUMERICALLY_UNRESOLVED" for row in bad)
    assert all(float(row["max_tensor_relative_error"]) <= 5e-3 for row in comparison)
    assert all(row["production_gram_classes"] == row["independent_gram_classes"] for row in comparison)
    assert Counter(row["cross_route_status"] for row in adjudicated) == Counter({"VERIFIED": 1211, "PREREGISTERED_SPI_UNRESOLVED": 10})
    assert Counter(row["ownership_adjudication"] for row in adjudicated) == Counter({"RESOLVED_NO_OWNER": 1200, "OWNERSHIP_UNRESOLVED": 15, "POSITIVE_OWNER": 6})

    misaligned = [row for row in adjudicated if row["parent_owner_class"] == "SPLIT_MISALIGNED_WITH_CURVATURE_PRINCIPALS"]
    assert len(misaligned) == 1194
    assert all(row["cross_route_status"] == "VERIFIED" for row in misaligned)
    assert Counter(row["adjudicated_spi_class"] for row in misaligned) == Counter({
        "SPI_RANK3_OR_4_NO_INTRINSIC_2PLANE": 810,
        "SPI_RANK2_ALTERNATIVE_PLANE": 384,
    })
    assert Counter(row["ownership_adjudication"] for row in misaligned) == Counter({"RESOLVED_NO_OWNER": 1187, "OWNERSHIP_UNRESOLVED": 7})
    owners = [row for row in adjudicated if row["tested_derivative_owner"] == "TRUE"]
    assert len(owners) == 6
    assert all(row["parent_owner_class"] == "RICCI_DERIVED_WITH_WEYL_ALIGNMENT" for row in owners)

    assert derivation["status"] == "PRODUCTION_COMPLETE"
    assert derivation["counts"] == {"G63": 42, "G85": 1179, "rows": 1221}
    assert derivation["spi_counts"] == expected_prod_spi
    assert derivation["primary_landing"] == "FIRST_DERIVATIVE_ATLAS_NUMERICALLY_OR_JET_UNRESOLVED"
    assert derivation["no_physical_selection"] is True
    assert independent["status"] == "FAIL" and independent["checks"] == 1221 and independent["pass_count"] == 1211
    assert independent["max_tensor_relative_error"] <= 5e-3
    assert independent["max_outer_ladder_difference"] <= 5e-3
    assert adjudication["status"] == "PASS_WITH_PREREGISTERED_UNRESOLVED"
    assert adjudication["primary_landing"] == "FIRST_DERIVATIVE_ATLAS_NUMERICALLY_OR_JET_UNRESOLVED"
    assert adjudication["adjudicated_spi_counts"] == expected_adj_spi
    assert adjudication["prior_misaligned_rows"] == adjudication["prior_misaligned_spi_independently_resolved"] == 1194
    assert adjudication["prior_misaligned_resolved_no_owner_count"] == 1187
    assert adjudication["prior_misaligned_ownership_unresolved_count"] == 7
    assert adjudication["prior_misaligned_positive_owner_count"] == 0
    assert adjudication["derivative_owner_count"] == 6
    assert adjudication["no_physical_history_selected"] is True and adjudication["no_query_or_realization_selected"] is True
    assert identities["status"] == "PASS" and identities["rows"] == 1221
    assert max(identities["maximum_defects"].values()) <= 2e-8
    assert "riemann_to_ricci_contraction" in identities["maximum_defects"]
    assert "weyl_trace_free_contraction" in identities["maximum_defects"]

    assert len(gram_production) == len(gram_independent) == len(gram_comparison) == len(gram_adjudicated) == 3663
    gram_keys = [(row["key"], row["tensor"]) for row in gram_production]
    assert len(set(gram_keys)) == 3663
    assert gram_keys == [(row["key"], row["tensor"]) for row in gram_independent]
    assert gram_keys == [(row["key"], row["tensor"]) for row in gram_comparison]
    assert gram_keys == [(row["key"], row["tensor"]) for row in gram_adjudicated]
    assert Counter(row["tensor"] for row in gram_production) == Counter({"k_riem": 1221, "k_ric": 1221, "k_weyl": 1221})
    required_gram_fields = {
        "operator_rank", "real_eigenvalue_count", "complex_pair_count", "jordan_defect",
        "spectral_block_count", "candidate_2plane_count", "spectral_blocks_json", "candidate_2planes_json",
        "eigen_1_real", "eigen_1_imag", "eigen_2_real", "eigen_2_imag",
        "eigen_3_real", "eigen_3_imag", "eigen_4_real", "eigen_4_imag",
    }
    assert all(required_gram_fields <= set(row) for row in gram_production)
    assert all(required_gram_fields <= set(row) for row in gram_independent)
    assert all(json.loads(row["spectral_blocks_json"]) is not None and json.loads(row["candidate_2planes_json"]) is not None for row in gram_production)
    expected_gram_structures = Counter({"SPECTRALLY_UNRESOLVED": 3266, "FOUR_REAL_SIMPLE_LINES": 391, "REAL_REPEATED_DIAGONALIZABLE": 6})
    assert Counter(row["adjudicated_structure"] for row in gram_adjudicated) == expected_gram_structures
    assert Counter(row["cross_route_status"] for row in gram_adjudicated) == Counter({"SPECTRALLY_UNRESOLVED": 3266, "VERIFIED": 397})
    resolved_gram = [row for row in gram_adjudicated if row["cross_route_status"] == "VERIFIED"]
    assert Counter(row["candidate_2plane_count"] for row in resolved_gram) == Counter({"6": 391, "0": 6})
    assert all(row["pass"] == "TRUE" for row in gram_comparison if (row["key"], row["tensor"]) in {(x["key"], x["tensor"]) for x in resolved_gram})
    assert gram_production_result["status"] == "COMPLETE" and gram_production_result["rows"] == 3663
    assert gram_independent_result["status"] == "PASS_WITH_SPECTRALLY_UNRESOLVED" and gram_independent_result["rows"] == 3663
    assert gram_independent_result["maximum_eigenvalue_error"] <= 5e-3
    assert gram_adjudication_result["status"] == "PASS_WITH_SPECTRALLY_UNRESOLVED"
    assert gram_adjudication_result["rows"] == 3663 and gram_adjudication_result["verified_rows"] == 397 and gram_adjudication_result["spectrally_unresolved_rows"] == 3266
    assert gram_adjudication_result["adjudicated_structure_counts"] == dict(expected_gram_structures)

    for name in ("PRODUCTION_DERIVATIVE_TENSORS.npz", "INDEPENDENT_DERIVATIVE_TENSORS.npz"):
        data = np.load(HERE / name)
        assert data["keys"].shape == (1221,)
        assert data["gradients"].shape == (1221, 7, 4)
        assert data["k_riem"].shape == data["k_ric"].shape == data["k_weyl"].shape == (1221, 4, 4)
        assert data["nabla_riemann"].shape == data["nabla_weyl"].shape == (1221, 4, 4, 4, 4, 4)
        assert data["nabla_ricci"].shape == (1221, 4, 4, 4)

    package_rows = [row for row in status if row["object"] == "package"]
    assert len(package_rows) == 1 and package_rows[0]["result"] == "VERIFIED_WITH_CAVEATS"
    return {
        "status": "PASS",
        "rows": 1221,
        "verified_rows": 1211,
        "spi_unresolved_rows": 10,
        "prior_misaligned_rows": 1194,
        "prior_misaligned_resolved_nonowners": 1187,
        "prior_misaligned_ownership_unresolved": 7,
        "prior_misaligned_positive_owners": 0,
        "derivative_owners": 6,
        "source_rows": 9,
        "raw_artifact_rows": 16,
        "gram_spectral_rows": 3663,
        "gram_spectral_verified": 397,
        "gram_spectral_unresolved": 3266,
    }


def main() -> None:
    result = validate(
        rows("DERIVATIVE_DISTRIBUTION_ATLAS.tsv"),
        rows("ADJUDICATED_DERIVATIVE_ATLAS.tsv"),
        rows("INDEPENDENT_COMPARISON.tsv"),
        json.loads((HERE / "DERIVATION_RESULT.json").read_text()),
        json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text()),
        json.loads((HERE / "ADJUDICATION_RESULT.json").read_text()),
        json.loads((HERE / "TENSOR_IDENTITY_VERIFICATION.json").read_text()),
        rows("SOURCE_MANIFEST.tsv"),
        rows("RAW_ARTIFACT_MANIFEST.tsv"),
        rows("GRAM_INTRINSIC_SUBSPACE_ATLAS.tsv"),
        rows("INDEPENDENT_GRAM_INTRINSIC_SUBSPACE_ATLAS.tsv"),
        rows("GRAM_INTRINSIC_SUBSPACE_COMPARISON.tsv"),
        rows("ADJUDICATED_GRAM_INTRINSIC_SUBSPACE_ATLAS.tsv"),
        json.loads((HERE / "GRAM_INTRINSIC_SUBSPACE_RESULT.json").read_text()),
        json.loads((HERE / "INDEPENDENT_GRAM_INTRINSIC_SUBSPACE_RESULT.json").read_text()),
        json.loads((HERE / "GRAM_INTRINSIC_SUBSPACE_ADJUDICATION.json").read_text()),
        rows("STATUS_LEDGER.tsv"),
    )
    (HERE / "PACKAGE_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

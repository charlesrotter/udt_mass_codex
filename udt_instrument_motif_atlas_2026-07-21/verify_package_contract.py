#!/usr/bin/env python3
"""Fail-closed verification of the saved motif atlas and its scoped readout."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MAXIMUM = "BOUNDED_POINTWISE_INSTRUMENT_MOTIF_LATTICE_CHARACTERIZED"
EXPECTED_MOTIFS = {
    "SCALAR_4_AMBIGUITY": 22656,
    "TWO_PLUS_TWO_LINES": 16431,
    "FOUR_LINES": 2764,
    "LINE_PLUS_THREE": 5760,
    "FULL_IRREDUCIBLE_4": 142836,
    "NUMERIC_UNCERTAIN": 17,
}
EXPECTED_TRANSITIONS = {
    "FULL_ALGEBRA_REMAINS_FULL": 313692,
    "PRIMITIVE_BLOCKS_PRESERVED": 57596,
    "MIXES_TO_FULL_ALGEBRA": 75996,
    "AMBIGUITY_TO_CERTIFIED_MOTIF": 13437,
    "NUMERIC_UNCERTAIN": 79,
}
EXPECTED_ADDED = {
    "R": (8061, 9984, 5369, 68731, 15),
    "H": (2688, 13822, 8442, 67193, 15),
    "D": (2688, 13822, 8435, 67200, 15),
    "RG": (0, 9984, 26875, 55284, 17),
    "WG": (0, 9984, 26875, 55284, 17),
}


class ContractError(AssertionError):
    pass


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def gzip_rows(path: Path):
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        yield from csv.DictReader(handle, delimiter="\t")


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise ContractError(detail)


def validate_registry(registry: list[dict[str, str]]) -> None:
    masks = [int(row["mask"]) for row in registry]
    ids = [row["family_id"] for row in registry]
    require(len(registry) == 31 and sorted(masks) == list(range(1, 32)), "registry masks")
    require(len(ids) == len(set(ids)), "registry family ids")


def registered_edges(registry: list[dict[str, str]]) -> set[tuple[int, int]]:
    masks = {int(row["mask"]) for row in registry}
    return {(source, source | bit) for source in masks for bit in (1, 2, 4, 8, 16)
            if not source & bit and source | bit in masks}


def validate_edges(edges: set[tuple[int, int]]) -> None:
    require(len(edges) == 75, "edge count")
    require(all(source and destination > source and (destination ^ source) in {1, 2, 4, 8, 16}
                for source, destination in edges), "edge identities")


def aggregate(path: Path, key: str) -> Counter[str]:
    total: Counter[str] = Counter()
    for row in rows(path):
        total[row[key]] += int(row["configurations"])
    return total


def validate_motif_counts(counts: Counter[str]) -> None:
    require(dict(counts) == EXPECTED_MOTIFS, "motif census")


def validate_transition_counts(counts: Counter[str]) -> None:
    require(dict(counts) == EXPECTED_TRANSITIONS, "transition census")


def validate_status(status: list[dict[str, str]]) -> None:
    by_id = {row["claim_id"]: row for row in status}
    require(len(status) == 15 and len(by_id) == 15, "status coverage")
    require(by_id["S04"]["status"] == "OPEN", "reciprocal interpretation promotion")
    require(by_id["S08"]["status"] == "OPEN" and by_id["S09"]["status"] == "OPEN", "physics promotion")
    require(by_id["S10"]["status"] == "OPEN" and by_id["S14"]["status"] == "OPEN", "global promotion")
    require(by_id["S15"]["status"] == "OPEN", "UDT uniqueness promotion")


def expect_rejection(identifier: str, callback) -> dict[str, str]:
    try:
        callback()
    except ContractError:
        return {"catch_id": identifier, "result": "REJECTED_AS_REQUIRED"}
    raise AssertionError(f"catch accepted corruption: {identifier}")


def source_immutability() -> dict[str, str]:
    observed = {}
    for row in rows(HERE / "SOURCE_LINEAGE.tsv"):
        path = HERE / row["path"] if row["role"] == "PREREGISTRATION" else ROOT / row["path"]
        require(path.exists() and digest(path) == row["sha256"], f"source hash {row['path']}")
        observed[row["path"]] = row["sha256"]
    require(len(observed) == 8, "source lineage count")
    return observed


def main() -> None:
    registry = rows(HERE / "INSTRUMENT_SUBSET_REGISTRY.tsv")
    validate_registry(registry)
    edges = registered_edges(registry)
    validate_edges(edges)
    motif_counts = aggregate(HERE / "FAMILY_MOTIF_CENSUS.tsv", "motif")
    transition_counts = aggregate(HERE / "EDGE_TRANSITION_CENSUS.tsv", "transition")
    validate_motif_counts(motif_counts)
    family_census_rows = rows(HERE / "FAMILY_MOTIF_CENSUS.tsv")
    expected_shapes = {
        "TWO_PLUS_TWO_LINES": ("1;1;2", "N0_P1_Z0;N0_P1_Z0;N1_P1_Z0"),
        "FOUR_LINES": ("1;1;1;1", "N0_P1_Z0;N0_P1_Z0;N0_P1_Z0;N1_P0_Z0"),
    }
    for motif, expected_shape in expected_shapes.items():
        observed_shapes = {(row["primitive_block_ranks"], row["primitive_block_signatures"])
                           for row in family_census_rows if row["motif"] == motif}
        require(observed_shapes == {expected_shape}, f"motif shape {motif}")
    line_three_shapes = {(row["primitive_block_ranks"], row["primitive_block_signatures"])
                         for row in family_census_rows if row["motif"] == "LINE_PLUS_THREE"}
    require(line_three_shapes == {
        ("1;3", "N0_P1_Z0;N1_P2_Z0"), ("1;3", "N0_P3_Z0;N1_P0_Z0")
    }, "line-plus-three shapes")
    validate_transition_counts(transition_counts)
    added_rows = rows(HERE / "ADDED_INSTRUMENT_TRANSITION_CENSUS.tsv")
    observed_added = {
        row["added_instrument"]: tuple(int(row[field]) for field in (
            "ambiguity_to_certified_motif", "primitive_blocks_preserved", "mixes_to_full_algebra",
            "full_algebra_remains_full", "numeric_uncertain",
        )) for row in added_rows
    }
    require(observed_added == EXPECTED_ADDED, "added-instrument census")
    require(all(int(row["total_edges"]) == 92160 for row in added_rows), "added-instrument totals")

    result = json.loads((HERE / "ATLAS_RESULT.json").read_text(encoding="utf-8"))
    require(result["maximum_conclusion"] == MAXIMUM, "maximum conclusion")
    require(result["configurations"] == 6144 and result["family_rows"] == 190464, "family coverage")
    require(result["edge_rows"] == 460800 and result["nonlinear_family_rows"] == 380928, "edge/nonlinear coverage")
    require(result["motif_fingerprints"] == 14 and result["numeric_margin_rows"] == 162, "fingerprints/margins")
    require(result["nonlinear_nonuncertain_discordances"] == 0, "family covariance")
    require(result["nonlinear_edge_nonuncertain_discordances"] == 0, "edge covariance")
    require(result["nonlinear_alignment_nonuncertain_discordances"] == 0, "alignment covariance")
    require(result["physical_merit_evaluated"] is False, "physical merit evaluated")
    require(all(row["result"] == "PASS" for row in rows(HERE / "COVERAGE_LEDGER.tsv")), "coverage ledger")
    require(len(rows(HERE / "NUMERIC_MARGIN_LEDGER.tsv")) == 162, "margin ledger")
    require(sum(int(row["configurations"]) for row in rows(HERE / "MOTIF_FINGERPRINT_CENSUS.tsv")) == 6144,
            "fingerprint coverage")

    alignment = aggregate(HERE / "RICCI_HESSIAN_ALIGNMENT_CENSUS.tsv", "alignment_class")
    require(alignment["NONCOMMUTING_CROSSING_SPLITS"] == 2090, "crossing split count")
    require(alignment["NUMERIC_UNCERTAIN"] == 2, "alignment uncertainty")
    incidence = aggregate(HERE / "GRADIENT_INCIDENCE_CENSUS.tsv", "gradient_incidence")
    require(incidence["SPLIT_ACROSS_BOTH_PLANES"] == 7840, "gradient split count")
    require(incidence["WHOLLY_IN_ONE_PLANE"] == 0 and incidence["WHOLLY_IN_COMPLEMENT"] == 0,
            "gradient confinement")
    family_by_mask = {int(row["mask"]): row["family_id"] for row in registry}
    equivalence = {
        tuple(sorted((row["first_family_id"], row["second_family_id"]))): int(row["configurations"])
        for row in rows(HERE / "FAMILY_EQUIVALENCE_CENSUS.tsv")
    }
    for lower in range(8):
        pair = tuple(sorted((family_by_mask[lower | 8], family_by_mask[lower | 16])))
        require(equivalence.get(pair) == 6144, f"RG/WG motif equivalence {lower}")
    for mask in range(1, 32):
        if not mask & 1 and mask & (8 | 16):
            pair = tuple(sorted((family_by_mask[mask], family_by_mask[mask | 1])))
            require(equivalence.get(pair) == 6144, f"Ricci motif redundancy {mask}")

    b02 = [row for row in rows(HERE / "BUILDING_BLOCK_LEDGER.tsv") if row["block_id"] == "B02"]
    require(len(b02) == 1 and b02[0]["physical_status"] == "OPEN_ALGEBRAIC_CANDIDATE_ONLY",
            "building-block scope")
    validate_status(rows(HERE / "STATUS_LEDGER.tsv"))
    anti = rows(HERE / "ANTI_IMPOSITION_AUDIT.tsv")
    require(len(anti) == 11 and all(row["answer"] == "NO" for row in anti), "anti-imposition audit")

    verify = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    margins = json.loads((HERE / "MARGIN_ESCALATION_RESULT.json").read_text(encoding="utf-8"))
    require(verify["status"] == "PASS" and verify["total_family_classifications"] == 35712, "independent verifier")
    require(verify["catch_proofs"] == 12 and verify["omitted_nonlinear_jet_residual"] > 1e-3,
            "independent catches")
    require(margins["status"] == "PASS" and margins["unique_target_identities"] == 124,
            "margin escalation")
    require(margins["discordant_identities"] == 0, "margin discordance")
    require(all(row["result"] == "REJECTED_AS_REQUIRED" for row in rows(HERE / "INDEPENDENT_CATCH_PROOFS.tsv")),
            "independent catch ledger")
    sources = source_immutability()

    bad_registry = registry[:-1]
    bad_edges = set(edges); bad_edges.pop()
    bad_motifs = Counter(motif_counts); bad_motifs["FULL_IRREDUCIBLE_4"] -= 1
    bad_transitions = Counter(transition_counts); bad_transitions["PRIMITIVE_BLOCKS_PRESERVED"] -= 1
    bad_status = [dict(row) for row in rows(HERE / "STATUS_LEDGER.tsv")]
    next(row for row in bad_status if row["claim_id"] == "S04")["status"] = "DERIVED"
    catches = [
        expect_rejection("K01_MISSING_SUBSET", lambda: validate_registry(bad_registry)),
        expect_rejection("K02_MISSING_EDGE", lambda: validate_edges(bad_edges)),
        expect_rejection("K03_MUTATED_MOTIF_COUNT", lambda: validate_motif_counts(bad_motifs)),
        expect_rejection("K04_MUTATED_TRANSITION_COUNT", lambda: validate_transition_counts(bad_transitions)),
        expect_rejection("K05_PHYSICAL_PROMOTION", lambda: validate_status(bad_status)),
    ]
    with (HERE / "CONTRACT_CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("catch_id", "result"), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(catches)
    output = {
        "schema": "udt-instrument-motif-package-contract-1.0",
        "status": "PASS",
        "maximum_conclusion": MAXIMUM,
        "configurations": 6144,
        "families": 31,
        "family_rows": sum(motif_counts.values()),
        "edges": len(edges),
        "edge_rows": sum(transition_counts.values()),
        "motif_counts": dict(sorted(motif_counts.items())),
        "transition_counts": dict(sorted(transition_counts.items())),
        "ricci_hessian_crossing_splits": 2090,
        "gradient_split_across_incidences": 7840,
        "source_lineage_entries": len(sources),
        "catch_proofs": len(catches),
    }
    (HERE / "CONTRACT_VERIFICATION_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    transcript = [
        "UDT_MOTIF_PACKAGE_CONTRACT=PASS",
        f"configurations=6144 families=31 family_rows={sum(motif_counts.values())}",
        f"edges={len(edges)} edge_rows={sum(transition_counts.values())}",
        f"motif_types={len(motif_counts) - 1} uncertainty_class=1 fingerprints=14",
        f"crossing_splits=2090 gradient_split_across={incidence['SPLIT_ACROSS_BOTH_PLANES']}",
        f"sources={len(sources)} catches={len(catches)}",
    ]
    (HERE / "CONTRACT_VERIFICATION_TRANSCRIPT.txt").write_text(
        "\n".join(transcript) + "\n", encoding="utf-8"
    )
    print("\n".join(transcript))


if __name__ == "__main__":
    main()

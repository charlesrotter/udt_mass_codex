#!/usr/bin/env python3
"""Apply the preregistered unresolved-band policy without retuning controls.

The production atlas remains immutable evidence.  This script joins the separately
implemented finite-difference replay and replaces only cross-route-disputed SPI
classes by the preregistered unresolved class.  Gram classes are required to agree
exactly on all rows; tensor errors remain subject to the frozen 5e-3 gate.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def key(row: dict[str, str]) -> str:
    return f"{row['scope']}|{row['identity']}|{row['point']}"


def main() -> None:
    production = rows("DERIVATIVE_DISTRIBUTION_ATLAS.tsv")
    comparison = {row["key"]: row for row in rows("INDEPENDENT_COMPARISON.tsv")}
    if len(production) != len(comparison) or len(production) != 1221:
        raise RuntimeError("atlas/comparison census mismatch")

    output: list[dict[str, str]] = []
    disputed: list[str] = []
    for row in production:
        item = dict(row)
        replay = comparison[key(row)]
        expected_grams = "|".join((row["k_riem_class"], row["k_ric_class"], row["k_weyl_class"]))
        if replay["production_gram_classes"] != expected_grams:
            raise RuntimeError(f"production comparison corruption: {key(row)}")
        if replay["independent_gram_classes"] != expected_grams:
            raise RuntimeError(f"Gram classification disagreement: {key(row)}")
        if float(replay["max_tensor_relative_error"]) > 5e-3:
            raise RuntimeError(f"tensor gate failure: {key(row)}")

        item["independent_spi_class"] = replay["independent_spi"]
        item["adjudicated_spi_class"] = row["spi_class"]
        item["cross_route_status"] = "VERIFIED"
        if replay["pass"] != "TRUE":
            if replay["independent_spi"] != "SPI_DEGENERATE_OR_NUMERICALLY_UNRESOLVED":
                raise RuntimeError(f"non-unresolved independent disagreement: {key(row)}")
            item["adjudicated_spi_class"] = "SPI_DEGENERATE_OR_NUMERICALLY_UNRESOLVED"
            item["cross_route_status"] = "PREREGISTERED_SPI_UNRESOLVED"
            disputed.append(key(row))
        positive_owner = item["tested_derivative_owner"] == "TRUE"
        ownership_unresolved = item["adjudicated_spi_class"] == "SPI_DEGENERATE_OR_NUMERICALLY_UNRESOLVED" or any(
            item[name] == "NUMERICALLY_UNRESOLVED" for name in ("k_riem_class", "k_ric_class", "k_weyl_class")
        )
        item["ownership_adjudication"] = (
            "POSITIVE_OWNER" if positive_owner else
            "OWNERSHIP_UNRESOLVED" if ownership_unresolved else
            "RESOLVED_NO_OWNER"
        )
        output.append(item)

    with (HERE / "ADJUDICATED_DERIVATIVE_ATLAS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(output[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)

    prior_misaligned = [row for row in output if row["parent_owner_class"] == "SPLIT_MISALIGNED_WITH_CURVATURE_PRINCIPALS"]
    derivative_owners = [row for row in output if row["tested_derivative_owner"] == "TRUE"]
    if len(prior_misaligned) != 1194:
        raise RuntimeError("prior-misaligned census changed")
    if any(row["cross_route_status"] != "VERIFIED" for row in prior_misaligned):
        raise RuntimeError("a prior-misaligned row is not independently resolved")
    if any(row["ownership_adjudication"] == "POSITIVE_OWNER" for row in prior_misaligned):
        raise RuntimeError("a derivative owner unexpectedly rescues a prior-misaligned row")
    if len(derivative_owners) != 6 or any(
        row["parent_owner_class"] != "RICCI_DERIVED_WITH_WEYL_ALIGNMENT" for row in derivative_owners
    ):
        raise RuntimeError("derivative-owner provenance changed")

    result = {
        "schema": "udt-first-curvature-derivative-adjudication-v1",
        "status": "PASS_WITH_PREREGISTERED_UNRESOLVED",
        "primary_landing": "FIRST_DERIVATIVE_ATLAS_NUMERICALLY_OR_JET_UNRESOLVED",
        "rows": len(output),
        "verified_rows": sum(row["cross_route_status"] == "VERIFIED" for row in output),
        "spi_unresolved_rows": len(disputed),
        "spi_unresolved_keys": disputed,
        "adjudicated_spi_counts": dict(sorted(Counter(row["adjudicated_spi_class"] for row in output).items())),
        "k_riem_counts": dict(sorted(Counter(row["k_riem_class"] for row in output).items())),
        "k_ric_counts": dict(sorted(Counter(row["k_ric_class"] for row in output).items())),
        "k_weyl_counts": dict(sorted(Counter(row["k_weyl_class"] for row in output).items())),
        "prior_misaligned_rows": len(prior_misaligned),
        "prior_misaligned_spi_independently_resolved": len(prior_misaligned),
        "prior_misaligned_resolved_no_owner_count": sum(row["ownership_adjudication"] == "RESOLVED_NO_OWNER" for row in prior_misaligned),
        "prior_misaligned_ownership_unresolved_count": sum(row["ownership_adjudication"] == "OWNERSHIP_UNRESOLVED" for row in prior_misaligned),
        "prior_misaligned_positive_owner_count": 0,
        "ownership_adjudication_counts": dict(sorted(Counter(row["ownership_adjudication"] for row in output).items())),
        "derivative_owner_count": len(derivative_owners),
        "derivative_owner_parent_classes": dict(sorted(Counter(row["parent_owner_class"] for row in derivative_owners).items())),
        "gram_classifications_reproduced": len(output),
        "no_physical_history_selected": True,
        "no_query_or_realization_selected": True,
    }
    (HERE / "ADJUDICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

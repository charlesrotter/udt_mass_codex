#!/usr/bin/env python3
"""Create deterministic scientific censuses from frozen correspondence ledgers."""

from __future__ import annotations

import csv
import gzip
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(path):
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        yield from csv.DictReader(handle, delimiter="\t")


def write(name, fields, values):
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(values)


def main():
    persistence = Counter(); transition_families = Counter(); transition_total = 0
    for row in rows(HERE / "PATH_CONTINUATION_SUMMARY.tsv.gz"):
        persistence[(row["distinct_motifs"], row["stable_projector_path"])] += 1
        if int(row["motif_transitions"]):
            transition_families[row["family_id"]] += 1
            transition_total += 1
    persistence_rows = [
        {"motif_word": key[0], "stable_projector_path": key[1], "family_paths": value}
        for key, value in sorted(persistence.items())
    ]
    write("PATH_MOTIF_PERSISTENCE.tsv", list(persistence_rows[0]), persistence_rows)
    family_rows = [{"family_id": key, "paths_with_transition_or_margin": value}
                   for key, value in sorted(transition_families.items())]
    write("FAMILY_TRANSITION_CENSUS.tsv", list(family_rows[0]), family_rows)

    distribution = Counter(); midpoint = {}; hd = Counter()
    for row in rows(HERE / "DISTRIBUTION_ATLAS.tsv.gz"):
        key = (row["identity_id"], row["family_id"])
        midpoint[key] = row["motif"]
        distribution[(row["motif"], row["distribution_kind"], row["rank"], row["frobenius_class"])] += 1
        if row["family_mask"] == "6":
            hd[(row["motif"], row["stencil_status"], row["frobenius_class"])] += 1
    distribution_rows = [
        {"motif": key[0], "distribution_kind": key[1], "rank": key[2],
         "frobenius_class": key[3], "rows": value}
        for key, value in sorted(distribution.items())
    ]
    write("DISTRIBUTION_CENSUS.tsv", list(distribution_rows[0]), distribution_rows)
    midpoint_census = Counter(midpoint.values())
    midpoint_rows = [{"motif": key, "identity_family_midpoints": value}
                     for key, value in sorted(midpoint_census.items())]
    write("MIDPOINT_MOTIF_CENSUS.tsv", list(midpoint_rows[0]), midpoint_rows)
    hd_rows = [{"motif": key[0], "stencil_status": key[1], "frobenius_class": key[2], "rows": value}
               for key, value in sorted(hd.items())]
    write("HD_CONTRAST_CENSUS.tsv", list(hd_rows[0]), hd_rows)

    result = {
        "stable_path_census": {
            "full_irreducible": persistence[("FULL_IRREDUCIBLE_4", "YES")],
            "scalar": persistence[("SCALAR_4_AMBIGUITY", "YES")],
            "one_one_two": persistence[("TWO_PLUS_TWO_LINES", "YES")],
            "line_three": persistence[("LINE_PLUS_THREE", "YES")],
            "four_lines": persistence[("FOUR_LINES", "YES")],
            "transition_or_margin": transition_total,
        },
        "midpoint_motif_census": dict(sorted(midpoint_census.items())),
        "one_one_two_primitive_rank2": {
            "locally_integrable": distribution[("TWO_PLUS_TWO_LINES", "PRIMITIVE_BLOCK", "2", "NUMERICALLY_INTEGRABLE_LOCAL")],
            "locally_nonintegrable": distribution[("TWO_PLUS_TWO_LINES", "PRIMITIVE_BLOCK", "2", "NUMERICALLY_NONINTEGRABLE_LOCAL")],
        },
        "four_line_rank2_split_sides": {
            "locally_integrable": distribution[("FOUR_LINES", "COMPLEMENTARY_RANK2", "2", "NUMERICALLY_INTEGRABLE_LOCAL")],
            "locally_nonintegrable": distribution[("FOUR_LINES", "COMPLEMENTARY_RANK2", "2", "NUMERICALLY_NONINTEGRABLE_LOCAL")],
        },
        "line_three_rank3": {
            "locally_integrable": distribution[("LINE_PLUS_THREE", "PRIMITIVE_BLOCK", "3", "NUMERICALLY_INTEGRABLE_LOCAL")],
            "uncertain": distribution[("LINE_PLUS_THREE", "PRIMITIVE_BLOCK", "3", "NUMERIC_UNCERTAIN_OBSTRUCTION")],
        },
        "HD_midpoint_contrast": {
            "scalar_rows": sum(value for (motif, _stencil, _frob), value in hd.items() if motif == "SCALAR_4_AMBIGUITY"),
            "full_irreducible_rows": sum(value for (motif, _stencil, _frob), value in hd.items() if motif == "FULL_IRREDUCIBLE_4"),
            "uncertain_rows": sum(value for (_motif, stencil, _frob), value in hd.items() if stencil != "STABLE_CLASSIFIED"),
            "four_line_rows": sum(value for (motif, _stencil, _frob), value in hd.items() if motif == "FOUR_LINES"),
        },
        "global_hopf_eligible_local_identities": 0,
        "toric_control_axis_recovery": "GENERIC_CONDITIONAL",
        "toric_control_seed_match": "EXACT",
        "carrier_emergence": "OPEN",
        "maximum_conclusion": "LOCAL_TWISTING_PROJECTOR_PRECURSOR_PLUS_CONDITIONAL_EXACT_HOPF_SEED_BRIDGE",
    }
    (HERE / "SCIENTIFIC_SUMMARY.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

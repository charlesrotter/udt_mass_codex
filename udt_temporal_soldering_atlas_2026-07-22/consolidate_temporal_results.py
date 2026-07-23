#!/usr/bin/env python3
"""Build the append-only cross-implementation correction layer."""

from __future__ import annotations

import csv
import gzip
import io
import json
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
CONFLICTS = {
    ("B3_R13_3_MB", "M04_D", 0): "INDEPENDENT_NUMERIC_UNCERTAIN_OBSTRUCTION",
    ("B3_V007_MF", "M04_D", 16): "PRODUCTION_NUMERIC_UNCERTAIN_OBSTRUCTION",
}


def read_tsv(path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def write_gzip(path, fields, rows):
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with io.TextIOWrapper(compressed, encoding="utf-8", newline="") as text:
                writer = csv.DictWriter(text, fieldnames=fields, delimiter="\t", lineterminator="\n")
                writer.writeheader(); writer.writerows(rows)


def main():
    production = read_tsv(HERE / "ORTHOGONAL_COMPLEMENT_ATLAS.tsv.gz")
    refinement = json.loads((HERE / "THRESHOLD_CONFLICT_REFINEMENT_RESULT.json").read_text())
    refined = {(row["identity_id"], row["family_id"], int(row["path_node"])): row["consolidated_class"]
               for row in refinement["cases"]}
    if set(refined) != set(CONFLICTS) or set(refined.values()) != {"REFINED_INTEGRABLE"}:
        raise AssertionError("frozen refinement result")
    rows = []
    for row in production:
        key = (row["identity_id"], row["family_id"], int(row["path_node"]))
        if key in refined:
            final_class = "NUMERICALLY_INTEGRABLE_LOCAL__REFINED_TWO_ROUTE"
            source = "CROSS_IMPLEMENTATION_THRESHOLD_REFINEMENT"
            conflict = CONFLICTS[key]
        else:
            final_class = row["frobenius_class"]
            source = "PRODUCTION_CLASS_EXACTLY_REPRODUCED_INDEPENDENTLY"
            conflict = "NONE"
        rows.append({
            "identity_id": key[0], "family_id": key[1], "path_node": key[2], "motif": row["motif"],
            "production_class": row["frobenius_class"], "initial_cross_implementation_conflict": conflict,
            "consolidated_class": final_class, "adjudication_source": source,
        })
    if len(rows) != 30_175 or len({(r["identity_id"], r["family_id"], r["path_node"]) for r in rows}) != 30_175:
        raise AssertionError("consolidated node coverage")
    write_gzip(HERE / "CROSS_IMPLEMENTATION_COMPLEMENT_CLASSIFICATION.tsv.gz", tuple(rows[0]), rows)

    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["identity_id"], row["family_id"])].append(row)
    line_rows = []
    for key in sorted(grouped):
        values = grouped[key]; census = Counter(row["consolidated_class"] for row in values)
        integrable = census["NUMERICALLY_INTEGRABLE_LOCAL"] + census["NUMERICALLY_INTEGRABLE_LOCAL__REFINED_TWO_ROUTE"]
        nonintegrable = census["NUMERICALLY_NONINTEGRABLE_LOCAL"]
        uncertain = len(values) - integrable - nonintegrable
        status = "ALL_17_NODES_CONSOLIDATED_INTEGRABLE" if integrable == 17 else \
            "NONINTEGRABILITY_OBSERVED_AT_ONE_OR_MORE_NODES" if nonintegrable else "NUMERICALLY_UNCERTAIN"
        line_rows.append({
            "identity_id": key[0], "family_id": key[1], "motif": values[0]["motif"], "nodes": len(values),
            "integrable_nodes": integrable, "nonintegrable_nodes": nonintegrable,
            "uncertain_nodes": uncertain, "consolidated_path_status": status,
            "highest_unconditional_completion_rung": "1_LOCAL_UNORIENTED_LINE",
        })
    write_tsv(HERE / "CROSS_IMPLEMENTATION_LINE_COMPLETION.tsv", tuple(line_rows[0]), line_rows)
    ladder = [
        {"rung": 1, "name": "LOCAL_UNORIENTED_TIMELIKE_LINE", "all_registered_paths": "1775_PATH_PRESENTATIONS_AT_17_NODES", "timelike_dphi_branch": "720_PATH_PRESENTATIONS", "spacelike_dphi_branch": "NO_TIMELIKE_LINE_SELECTED_IN_LORENTZIAN_LEAF", "four_line_branch": "1055_PATH_PRESENTATIONS", "global_status": "LOCAL_ONLY"},
        {"rung": 2, "name": "LOCAL_CONTINUOUS_TIMELIKE_LINE", "all_registered_paths": "NODE_NEIGHBORHOODS_ONLY__FULL_INTERVAL_NOT_CERTIFIED", "timelike_dphi_branch": "EXACT_WHERE_S_LT_0", "spacelike_dphi_branch": "OPEN_WITHIN_KER_DPHI", "four_line_branch": "SIMPLE_LINE_LOCAL_ONLY", "global_status": "OPEN"},
        {"rung": 3, "name": "LOCAL_TIME_ORIENTATION", "all_registered_paths": "OPEN", "timelike_dphi_branch": "GRAD_PHI_MATHEMATICAL_ORIENTATION__PHYSICAL_FUTURE_OPEN", "spacelike_dphi_branch": "OPEN", "four_line_branch": "OPEN", "global_status": "OPEN"},
        {"rung": 4, "name": "LOCAL_HYPERSURFACE_ORTHOGONAL_STRUCTURE", "all_registered_paths": "MOTIF_DEPENDENT", "timelike_dphi_branch": "EXACT_PHI_LEVEL_SETS_WHERE_S_LT_0", "spacelike_dphi_branch": "EXACT_LORENTZIAN_PHI_LEVEL_SETS__INTRALEAF_TIME_OPEN", "four_line_branch": "NONINTEGRABILITY_OBSERVED_ON_ALL_1055_PATHS", "global_status": "OPEN"},
        {"rung": 5, "name": "GLOBAL_TIMELIKE_LINE_BUNDLE", "all_registered_paths": "ZERO_DERIVED", "timelike_dphi_branch": "UNSAMPLED_INTERVALS_AND_GLOBAL_GLUE_OPEN", "spacelike_dphi_branch": "OPEN", "four_line_branch": "OPEN", "global_status": "OPEN"},
        {"rung": 6, "name": "GLOBAL_TIME_ORIENTED_THREADING", "all_registered_paths": "ZERO_DERIVED", "timelike_dphi_branch": "OPEN", "spacelike_dphi_branch": "OPEN", "four_line_branch": "OPEN", "global_status": "OPEN"},
        {"rung": 7, "name": "FULL_OPTICAL_CONNECTOR", "all_registered_paths": "ZERO_DERIVED", "timelike_dphi_branch": "OPEN", "spacelike_dphi_branch": "OPEN", "four_line_branch": "OPEN", "global_status": "OPEN"},
    ]
    write_tsv(HERE / "CONSOLIDATED_COMPLETION_LADDER.tsv", tuple(ladder[0]), ladder)
    reconstruction = [
        {"object": "LOCAL_NULL_CONE", "general_status": "CONDITIONAL_LORENTZIAN_METRIC_READOUT", "timelike_dphi_branch": "AVAILABLE", "spacelike_dphi_branch": "AVAILABLE_ON_LORENTZIAN_LEAF", "remaining_open": "PHYSICAL_OBSERVER_AND_GLOBAL_CONNECTOR"},
        {"object": "PHI_PROJECTOR", "general_status": "P_PHI=D/S_WHERE_S_NONZERO", "timelike_dphi_branch": "TIMELIKE_LINE", "spacelike_dphi_branch": "SPACELIKE_DEPTH_LINE", "remaining_open": "BRANCH_SELECTION_AND_INTERVAL_SIGN"},
        {"object": "PHI_LEVEL_SET_FOLIATION", "general_status": "EXACT_LOCAL_KER_DPHI", "timelike_dphi_branch": "POSITIVE_SPATIAL_LEAVES", "spacelike_dphi_branch": "LORENTZIAN_LEAVES", "remaining_open": "GLOBAL_COMPLETION"},
        {"object": "MATHEMATICAL_ORIENTATION", "general_status": "GRAD_PHI_WHERE_TIMELIKE", "timelike_dphi_branch": "AVAILABLE", "spacelike_dphi_branch": "NOT_A_TIME_ORIENTATION", "remaining_open": "PHYSICAL_FUTURE_SELECTION"},
        {"object": "ADAPTED_LAPSE", "general_status": "CONDITIONAL", "timelike_dphi_branch": "N_PHI=1/SQRT(-S)_FOR_TAU=PHI", "spacelike_dphi_branch": "NOT_A_TEMPORAL_LAPSE", "remaining_open": "PHYSICAL_CLOCK_SCALE_AND_REPARAMETERIZATION"},
        {"object": "ADAPTED_SHIFT", "general_status": "COORDINATE_DEPENDENT", "timelike_dphi_branch": "ZERO_IN_CHOSEN_NORMAL_FLOW_CHART", "spacelike_dphi_branch": "OPEN", "remaining_open": "NATIVE_THREAD_CONGRUENCE"},
        {"object": "INTRALEAF_TIMELIKE_LINE", "general_status": "OPEN", "timelike_dphi_branch": "NOT_NEEDED_LOCALLY", "spacelike_dphi_branch": "NOT_SELECTED_IN_N1_P2_COMPLEMENT", "remaining_open": "NATIVE_RANK_ONE_PROJECTOR_OR_EQUIVALENT"},
        {"object": "FULL_OPTICAL_CONNECTOR", "general_status": "OPEN", "timelike_dphi_branch": "OPEN", "spacelike_dphi_branch": "OPEN", "remaining_open": "GLOBAL_THREADING_SCALE_CURVE_ENDPOINT_SOLDERING"},
    ]
    write_tsv(HERE / "CONSOLIDATED_INVARIANT_RECONSTRUCTION_LEDGER.tsv", tuple(reconstruction[0]), reconstruction)
    result = {
        "node_rows": len(rows),
        "line_paths": len(line_rows),
        "node_class_census": dict(sorted(Counter(r["consolidated_class"] for r in rows).items())),
        "path_status_census": dict(sorted(Counter(r["consolidated_path_status"] for r in line_rows).items())),
        "motif_path_status_census": {"|".join(key): value for key, value in sorted(Counter((r["motif"], r["consolidated_path_status"]) for r in line_rows).items())},
        "initial_class_conflicts": len(CONFLICTS),
        "refined_integrable_conflicts": sum(value == "REFINED_INTEGRABLE" for value in refined.values()),
        "refined_nonintegrable_conflicts": sum(value == "REFINED_NONINTEGRABLE" for value in refined.values()),
        "unresolved_conflicts": sum(value == "CROSS_IMPLEMENTATION_NUMERIC_UNCERTAIN_OBSTRUCTION" for value in refined.values()),
        "original_production_atlas_modified": False,
        "maximum_conclusion": "BOUNDED_CONSOLIDATED_TEMPORAL_SOLDERING_CENSUS__GLOBAL_THREADING_OPEN",
    }
    (HERE / "CONSOLIDATED_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

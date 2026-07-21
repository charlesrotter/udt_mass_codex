#!/usr/bin/env python3
"""Independent non-importing verifier for the completion type-space atlas."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CLASSIFICATION = "CURRENT_FINITE_CELL_COMPLETION_TYPE_SPACE_MAPPED_WITH_UNBOUNDED_REMAINDERS"
MAXIMUM = "UDT_FINITE_CELL_COMPLETION_CONFIGURATION_ATLAS_CHARACTERIZED_WITHOUT_DYNAMICS"

SOURCE_HASHES = {
    "UDT_NATIVE_ACTION_COLD_PACKET.md": "d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0",
    "udt_premise_reset_audit_2026-07-19/SHA256SUMS.txt": "6123253b9370bce674c626a863dc595c773da3905cb155a7fe2b77c4667fd3a7",
    "udt_complete_metric_solution_space_map_2026-07-21/SHA256SUMS.txt": "1778e4dcfcf9ac0bd3574fb3ff5248f2990265fa40d0822ff964ac67c434ae38",
    "udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt": "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad",
    "udt_local_jet_atlas_p02_2026-07-21/SHA256SUMS.txt": "c56390eb26b80c54a3c3a09f4800086c8dbc00b5bfd40b2038e264e85bec8938",
    "udt_founded_constraint_atlas_p03_2026-07-21/SHA256SUMS.txt": "b0ec5cbb2be404084e1b1ed4eca98d53c9712a62cf1af0a48eb340b64467c3be",
    "udt_global_kinematic_assembly_p03g_2026-07-21/SHA256SUMS.txt": "62f9b3f33409b62fb841734e8a91e61d9b859247bf808c4a6cf3740b6a54b6c9",
    "udt_dynamics_branch_ruling_p04_2026-07-21/SHA256SUMS.txt": "d01d65fc5abcc35078c961d0d3fc0eec7ad26e205735a77f7d83e2b45121de3f",
    "udt_full_equation_variation_p05_2026-07-21/SHA256SUMS.txt": "5c26d4eb97c4dc370e286469c63d662f182a71a94a6e6899131fd6706c4e7f2e",
    "udt_pre_p06_boundary_selector_audit_2026-07-21/SHA256SUMS.txt": "45c239639d999c26f2e574592fafc392fbb7c1e6f20ea92e1d260b4784e00e51",
    "udt_time_live_characteristic_flux_audit_2026-07-21/SHA256SUMS.txt": "3089e66d65f85753d45e9e78596dba9ae2b962a015857c969ff6a0492d442f12",
    "udt_free_global_seal_transversality_audit_2026-07-21/SHA256SUMS.txt": "5198a69a1b8a3026af529bccd4d47639d718a21fc1153947b3ebfab8720502d8",
}

TABLES = [
    "SOURCE_LINEAGE.tsv", "P02_MARGINAL_CARRYFORWARD.tsv", "PARENT_ATLAS_CENSUS.tsv",
    "COMPLETION_AXIS_SCHEMA.tsv", "PHI_ZERO_SET_ATLAS.tsv", "FINITE_ORDER_GERM_WITNESSES.tsv",
    "METRIC_REGULARITY_ATLAS.tsv", "JET_MATCHING_ATLAS.tsv", "CAUSAL_TIME_LIVE_ATLAS.tsv",
    "FIELD_BUNDLE_ATLAS.tsv", "ANGULAR_MIXED_ATLAS.tsv", "GLOBAL_INCIDENCE_ATLAS.tsv",
    "GROUP_ACTION_QUOTIENT_ATLAS.tsv", "VARIATION_CHANNEL_ATLAS.tsv", "GLOBAL_OUTPUT_ATLAS.tsv",
    "COMPATIBILITY_RELATIONS.tsv", "FIELD_LANE_STATUS.tsv", "TEN_CRITERION_SCOPE.tsv",
    "ANTI_IMPOSITION_AUDIT.tsv",
]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            h.update(block)
    return h.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def canonical_row_hash(row: dict[str, str]) -> str:
    return hashlib.sha256(json.dumps(row, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate(result: dict, tables: dict[str, list[dict[str, str]]], graph: dict) -> list[str]:
    checks: list[str] = []

    def require(condition: bool, name: str) -> None:
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    require(result["schema"] == "udt-finite-cell-completion-atlas-1.0", "schema")
    require(result["status"] == "PASS", "status")
    require(result["classification"] == CLASSIFICATION, "classification")
    require(result["maximum_conclusion"] == MAXIMUM, "maximum")
    require(result["parent_p02_strata"] == 89 and result["parent_p03_accounted"] == 89, "parent_local_counts")
    require(result["parent_p03g_axes"] == 12 and result["parent_p03g_uncounted"] == 15, "parent_global_counts")
    require(result["finite_exhaustiveness_claim"] is False, "no_finite_exhaustiveness")
    require(result["branch_ranking_used"] is False, "no_ranking")
    require(result["dynamics_loaded"] is False and result["solutions_run"] == 0, "no_dynamics")
    require(result["P06_ready_pairs"] == 0 and result["gpu_used"] is False, "stop_boundary")
    require(result["evidence_grade"] == "LEAD_PENDING_FRESH_ADVERSARIAL_REVIEW", "grade")

    sources = tables["SOURCE_LINEAGE.tsv"]
    require(len(sources) == 12, "source_count")
    require({r["path"]: r["sha256"] for r in sources} == SOURCE_HASHES, "source_registry")
    require(all(digest(ROOT / path) == expected for path, expected in SOURCE_HASHES.items()), "source_rehash")

    parent_specs = [
        ("METRIC_INERTIA", "udt_local_jet_atlas_p02_2026-07-21/ZERO_JET_INERTIA_STRATA.tsv", 15),
        ("SPLIT_INERTIA", "udt_local_jet_atlas_p02_2026-07-21/SPLIT_ZERO_JET_STRATA.tsv", 36),
        ("DPHI", "udt_local_jet_atlas_p02_2026-07-21/DPHI_FIRST_JET_STRATA.tsv", 8),
        ("SPLIT_FIRST_JET", "udt_local_jet_atlas_p02_2026-07-21/SPLIT_FIRST_JET_STRATA.tsv", 12),
        ("CURVATURE_RANK", "udt_local_jet_atlas_p02_2026-07-21/CURVATURE_OPERATOR_RANK_STRATA.tsv", 7),
        ("RICCI_RANK", "udt_local_jet_atlas_p02_2026-07-21/RICCI_ENDOMORPHISM_RANK_STRATA.tsv", 5),
        ("PETROV", "udt_local_jet_atlas_p02_2026-07-21/PETROV_STRATA.tsv", 6),
    ]
    expected_carry = {}
    for atlas, rel, count in parent_specs:
        rows = read_tsv(ROOT / rel)
        require(len(rows) == count, f"parent_count_{atlas}")
        for row in rows:
            expected_carry[(atlas, row["id"])] = (rel, canonical_row_hash(row))
    carry = tables["P02_MARGINAL_CARRYFORWARD.tsv"]
    require(len(carry) == 89 and len({(r["atlas"], r["source_id"]) for r in carry}) == 89, "carry_89_unique")
    observed_carry = {(r["atlas"], r["source_id"]): (r["source_path"], r["parent_row_sha256"]) for r in carry}
    require(observed_carry == expected_carry, "carry_exact_rows")
    require(all(r["treatment"] == "CARRIED_WITHOUT_RANKING" for r in carry), "carry_unranked")

    p03 = read_tsv(ROOT / "udt_founded_constraint_atlas_p03_2026-07-21/SURVIVING_STRATA.tsv")
    require(len(p03) == 89 and len({(r["atlas"], r["source_id"]) for r in p03}) == 89, "p03_89")
    require(len(read_tsv(ROOT / "udt_global_kinematic_assembly_p03g_2026-07-21/GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv")) == 12, "p03g_12")
    require(len(read_tsv(ROOT / "udt_global_kinematic_assembly_p03g_2026-07-21/UNCOUNTED_GLOBAL_MODULI.tsv")) == 15, "p03g_15")

    census = {(r["parent"], r["object"]): int(r["count"]) for r in tables["PARENT_ATLAS_CENSUS.tsv"]}
    require(census[("P00", "conditional_metric_slots")] == 10, "p00_slots")
    require(census[("P02", "marginal_registered_strata")] == 89, "census_p02")
    require(census[("P03", "founded-constraint-accounted_strata")] == 89, "census_p03")
    require(census[("P03G", "global_assembly_axes")] == 12 and census[("P03G", "uncounted_global_moduli")] == 15, "census_p03g")

    axes = tables["COMPLETION_AXIS_SCHEMA.tsv"]
    require(len(axes) == 10 and len({r["id"] for r in axes}) == 10 and len({r["axis"] for r in axes}) == 10, "axis_ten")
    require(all(r["ranking_allowed"] == "NO" for r in axes), "axis_no_ranking")
    require({r["axis"] for r in axes} == {"METRIC_ZERO_JET", "METRIC_HIGHER_JETS", "PHI_ZERO_SET", "CAUSAL_TIME_LIVE", "FIELD_COFRAME_BUNDLE", "ANGULAR_MIXED_GEOMETRY", "GLOBAL_INCIDENCE", "TRANSITION_COCYCLE", "VARIATION_CHANNEL", "GLOBAL_OUTPUT"}, "axis_names")

    expected_counts = {
        "p02_carryforward": 89, "completion_axes": 10, "phi_zero_families": 12, "finite_germs": 9,
        "metric_regularity": 11, "jet_matching": 9, "causal_time_live": 11, "field_bundle": 11,
        "angular_mixed": 13, "global_incidence": 14, "quotient_action": 10, "variation": 11,
        "global_outputs": 8, "relations": 18, "field_lane_pairs": 21, "completeness": 10,
        "anti_imposition": 15,
    }
    require(result["table_counts"] == expected_counts, "table_counts")

    phi = {r["id"]: r for r in tables["PHI_ZERO_SET_ATLAS.tsv"]}
    require(len(phi) == 12 and phi["Z03"]["family"] == "REGULAR_LEVEL_HYPERSURFACE", "phi_regular")
    require(phi["Z10"]["family"] == "INFINITE_ORDER_FLAT_ZERO", "phi_infinite_jet")
    require(phi["Z12"]["status"] == "OTHER_UNENUMERATED_REQUIRED", "phi_remainder")
    require({"EMPTY_ZERO_SET", "IDENTICALLY_ZERO", "ZERO_ON_OPEN_REGION"}.issubset({r["family"] for r in phi.values()}), "phi_extremes")

    germs = {r["id"]: r for r in tables["FINITE_ORDER_GERM_WITNESSES.tsv"]}
    require(len(germs) == 9, "germ_count")
    for order in range(1, 7):
        row = germs[f"G{order:02d}"]
        require(int(row["first_nonzero_order"]) == order, f"germ_order_{order}")
        require(int(row["first_nonzero_derivative"]) == math.factorial(order), f"germ_derivative_{order}")
        require(row["sign_behavior"] == ("CROSSING" if order % 2 else "TOUCHING"), f"germ_parity_{order}")
        require(row["gradient_regular"] == ("YES" if order == 1 else "NO"), f"germ_regular_{order}")
    require(germs["G07"]["zero_geometry"] == "TWO_INTERSECTING_BRANCHES", "germ_branching")
    require(germs["G08"]["zero_geometry"] == "CODIMENSION_TWO_IN_n_y_SLICE", "germ_codim2")
    require(germs["G09"]["zero_geometry"] == "THREE_COMPONENTS_IN_ONE_DIMENSION", "germ_multicomponent")

    remainder_tables = {
        "METRIC_REGULARITY_ATLAS.tsv": "M11", "JET_MATCHING_ATLAS.tsv": "J09",
        "CAUSAL_TIME_LIVE_ATLAS.tsv": "T11", "FIELD_BUNDLE_ATLAS.tsv": "F11",
        "ANGULAR_MIXED_ATLAS.tsv": "A13", "GLOBAL_INCIDENCE_ATLAS.tsv": "I14",
        "GROUP_ACTION_QUOTIENT_ATLAS.tsv": "Q10", "VARIATION_CHANNEL_ATLAS.tsv": "V11",
        "GLOBAL_OUTPUT_ATLAS.tsv": "O08",
    }
    for table, row_id in remainder_tables.items():
        rows = {r["id"]: r for r in tables[table]}
        require(row_id in rows and "OTHER_UNENUMERATED_REQUIRED" in " ".join(rows[row_id].values()), f"remainder_{table}")

    metric = {r["id"]: r for r in tables["METRIC_REGULARITY_ATLAS.tsv"]}
    require(len(metric) == 11 and {"DEGENERATE_FIXED_RANK", "SIGNATURE_TYPE_CHANGE", "CURVATURE_SINGULAR"}.issubset({r["family"] for r in metric.values()}), "metric_closures")
    matching = {r["id"]: r for r in tables["JET_MATCHING_ATLAS.tsv"]}
    require(len(matching) == 9 and {"C0_JOIN", "C1_JOIN", "C2_JOIN", "CK_JOIN", "CINFINITY_JOIN", "ANALYTIC_JOIN"}.issubset({r["family"] for r in matching.values()}), "matching_orders")
    time = {r["id"]: r for r in tables["CAUSAL_TIME_LIVE_ATLAS.tsv"]}
    require(len(time) == 11 and {"REGULAR_TIMELIKE_SURFACE", "REGULAR_NULL_SURFACE", "REGULAR_SPACELIKE_SURFACE", "CAUSAL_TYPE_CHANGING_SURFACE"}.issubset({r["family"] for r in time.values()}), "all_causal")
    require("GENERAL_MOVING_EMBEDDING" in {r["family"] for r in time.values()} and "NO_DISTINGUISHED_SURFACE" in {r["family"] for r in time.values()}, "time_extremes")

    fields = {r["id"]: r for r in tables["FIELD_BUNDLE_ATLAS.tsv"]}
    require(len(fields) == 11 and {"METRIC_ONLY", "INDEPENDENT_ORDINARY_PHI_SCALAR", "INDEPENDENT_TWISTED_OR_SIGN_PHI", "INDEPENDENT_CONNECTION", "MIXED_FIELD_REALIZATION"}.issubset({r["family"] for r in fields.values()}), "field_realizations")
    angular = {r["id"]: r for r in tables["ANGULAR_MIXED_ATLAS.tsv"]}
    require(len(angular) == 13 and {"TIME_ANGULAR_SHIFT", "DEPTH_ANGULAR_SHIFT", "ZERO_OR_NONZERO_TWIST", "NON_TORIC_CAP_OR_FIXED_SET"}.issubset({r["family"] for r in angular.values()}), "angular_mixed_complete")
    global_rows = {r["id"]: r for r in tables["GLOBAL_INCIDENCE_ATLAS.tsv"]}
    require(len(global_rows) == 14 and {"COMPACT_WITHOUT_BOUNDARY", "ONE_OR_MORE_RETAINED_BOUNDARIES", "SMOOTH_EXTENSION_ACROSS_MARKED_SET", "PAIRWISE_GLUING", "MULTIPLE_OR_GRAPH_GLUING", "FREE_QUOTIENT", "FIXED_SET_QUOTIENT", "MIXED_COMPLETION"}.issubset({r["family"] for r in global_rows.values()}), "global_incidence_complete")
    quotient = {r["id"]: r for r in tables["GROUP_ACTION_QUOTIENT_ATLAS.tsv"]}
    require(len(quotient) == 10 and quotient["Q02"]["family"] == "FREE_PROPER_ACTION", "free_action")
    require(quotient["Q03"]["local_result"] == "local manifold-with-boundary model", "codim1_action")
    require(quotient["Q08"]["family"] == "NONPROPER_ACTION", "nonproper_retained")

    variation = {r["id"]: r for r in tables["VARIATION_CHANNEL_ATLAS.tsv"]}
    require(len(variation) == 11 and variation["V01"]["family"] == "NO_DYNAMICS_LOADED", "variation_no_law")
    require({"ONE_SIDED_FIXED_EMBEDDING", "ONE_SIDED_MOVING_EMBEDDING", "TWO_SIDED_SMOOTH_MATCHING", "TWO_SIDED_INTERFACE", "NULL_OR_CHARACTERISTIC_DATA", "DEGENERATE_OR_TYPE_CHANGE_VARIATION"}.issubset({r["family"] for r in variation.values()}), "variation_families")
    require(variation["V04"]["scope"] == "cancellation requires complete matching", "matching_not_assumed")
    outputs = tables["GLOBAL_OUTPUT_ATLAS.tsv"]
    require(len(outputs) == 8 and all(r["status"] in {"NOT_EVALUABLE", "BRANCH_FUNCTIONAL_OPEN", "OTHER_UNENUMERATED_REQUIRED"} for r in outputs), "outputs_unresolved")

    relations = {r["id"]: r for r in tables["COMPATIBILITY_RELATIONS.tsv"]}
    require(len(relations) == 18, "relation_count")
    require(relations["R01"]["consequence"] == "regular_codimension_one_local_level_set", "regular_value_relation")
    require(relations["R01"]["limit"] == "DOES_NOT_SET_GLOBAL_INCIDENCE", "regular_value_no_global_selection")
    require(relations["R04"]["consequence"] == "all_transformed_jets_through_k_match", "jet_relation")
    require(relations["R13"]["limit"] == "NO_COMPLETION_FAMILY_RANKING", "law_no_ranking")
    require(relations["R16"]["limit"] == "NOT_PHYSICAL_EVOLUTION_WITHOUT_OPERATOR", "time_not_evolution")
    require(relations["R17"]["limit"] == "NOT_UNIVERSAL_MERIT_FILTER", "regularity_no_merit")

    pairs = tables["FIELD_LANE_STATUS.tsv"]
    require(len(pairs) == 21 and len({r["pair_id"] for r in pairs}) == 21, "pairs_21")
    require(all(r["atlas_role"] == "STATUS_BOOKKEEPING_ONLY" and r["P06_ready"] == "NO" for r in pairs), "pairs_not_solved")

    completeness = tables["TEN_CRITERION_SCOPE.tsv"]
    require(len(completeness) == 10 and len({r["criterion"] for r in completeness}) == 10, "completeness_ten")
    require(next(r for r in completeness if r["criterion"] == "FULL_EQUATIONS")["covered"] == "none solved", "equations_open")
    require(next(r for r in completeness if r["criterion"] == "STABILITY")["covered"] == "not entered", "stability_open")
    anti = tables["ANTI_IMPOSITION_AUDIT.tsv"]
    require(len(anti) == 15 and all(r["present"] == "ABSENT" for r in anti), "anti_imposition")

    forbidden = ("PREFERRED", "UNIQUELY_SELECTED", "BEST_BRANCH", "PHYSICAL_WINNER")
    atlas_tables = [name for name in TABLES if name not in {"SOURCE_LINEAGE.tsv", "P02_MARGINAL_CARRYFORWARD.tsv"}]
    corpus = "\n".join("\t".join(row.values()) for name in atlas_tables for row in tables[name])
    require(not any(token in corpus for token in forbidden), "no_ranking_tokens")

    require(graph["schema"] == "udt-finite-cell-completion-atlas-graph-1.0", "graph_schema")
    require(graph["classification"] == CLASSIFICATION, "graph_classification")
    require(len(graph["axes"]) == 10 and len(graph["edges"]) == 5 and len(graph["forbidden_edges"]) == 5, "graph_counts")
    require(graph["layers"][-1] == "FUTURE_DYNAMICAL_SOLUTIONS", "dynamics_downstream")
    return checks


def expect_failure(name: str, fn, catches: list[str]) -> None:
    try:
        fn()
    except (AssertionError, KeyError, ValueError, TypeError):
        catches.append(name)
        return
    raise AssertionError(f"mutation escaped: {name}")


def main() -> None:
    result = json.loads((HERE / "ATLAS_RESULT.json").read_text(encoding="utf-8"))
    tables = {name: read_tsv(HERE / name) for name in TABLES}
    graph = json.loads((HERE / "ATLAS_GRAPH.json").read_text(encoding="utf-8"))
    checks = validate(result, tables, graph)
    catches: list[str] = []

    result_mutations = [
        ("classification", "EDGE_SELECTED"), ("maximum_conclusion", "PHYSICAL_UNIVERSE"),
        ("parent_p02_strata", 88), ("parent_p03_accounted", 88), ("parent_p03g_axes", 11),
        ("parent_p03g_uncounted", 14), ("finite_exhaustiveness_claim", True),
        ("branch_ranking_used", True), ("dynamics_loaded", True), ("solutions_run", 1),
        ("P06_ready_pairs", 1), ("gpu_used", True), ("evidence_grade", "SETTLED"),
    ]
    for key, value in result_mutations:
        bad = copy.deepcopy(result)
        bad[key] = value
        expect_failure(f"result_{key}", lambda b=bad: validate(b, tables, graph), catches)

    def mutate(table: str, row: int, key: str, value: str, name: str) -> None:
        bad = copy.deepcopy(tables)
        bad[table][row][key] = value
        expect_failure(name, lambda: validate(result, bad, graph), catches)

    bad = copy.deepcopy(tables); bad["P02_MARGINAL_CARRYFORWARD.tsv"].pop()
    expect_failure("missing_parent_stratum", lambda: validate(result, bad, graph), catches)
    bad = copy.deepcopy(tables); bad["P02_MARGINAL_CARRYFORWARD.tsv"][-1] = copy.deepcopy(bad["P02_MARGINAL_CARRYFORWARD.tsv"][0])
    expect_failure("duplicate_parent_stratum", lambda: validate(result, bad, graph), catches)
    mutate("P02_MARGINAL_CARRYFORWARD.tsv", 0, "parent_row_sha256", "0" * 64, "parent_hash")
    mutate("P02_MARGINAL_CARRYFORWARD.tsv", 0, "treatment", "PREFERRED", "parent_ranked")

    bad = copy.deepcopy(tables); bad["COMPLETION_AXIS_SCHEMA.tsv"].pop()
    expect_failure("missing_axis", lambda: validate(result, bad, graph), catches)
    mutate("COMPLETION_AXIS_SCHEMA.tsv", 0, "ranking_allowed", "YES", "axis_ranking")
    mutate("COMPLETION_AXIS_SCHEMA.tsv", 5, "axis", "ANGULAR_OMITTED", "angular_axis")

    bad = copy.deepcopy(tables); bad["PHI_ZERO_SET_ATLAS.tsv"].pop()
    expect_failure("phi_remainder_missing", lambda: validate(result, bad, graph), catches)
    mutate("PHI_ZERO_SET_ATLAS.tsv", 9, "family", "REGULAR_LEVEL_HYPERSURFACE", "flat_zero_removed")
    mutate("PHI_ZERO_SET_ATLAS.tsv", 11, "status", "EXHAUSTED", "phi_finite_claim")
    for order in range(1, 7):
        mutate("FINITE_ORDER_GERM_WITNESSES.tsv", order - 1, "first_nonzero_derivative", "0", f"germ_derivative_{order}")
        mutate("FINITE_ORDER_GERM_WITNESSES.tsv", order - 1, "sign_behavior", "CROSSING" if order % 2 == 0 else "TOUCHING", f"germ_parity_{order}")
    mutate("FINITE_ORDER_GERM_WITNESSES.tsv", 6, "zero_geometry", "ONE_SMOOTH_BRANCH", "branching_removed")
    mutate("FINITE_ORDER_GERM_WITNESSES.tsv", 7, "zero_geometry", "HYPERSURFACE", "codim2_removed")

    remainder_specs = [
        ("METRIC_REGULARITY_ATLAS.tsv", -1, "status"), ("JET_MATCHING_ATLAS.tsv", -1, "limit"),
        ("CAUSAL_TIME_LIVE_ATLAS.tsv", -1, "scope"), ("FIELD_BUNDLE_ATLAS.tsv", -1, "required_data"),
        ("ANGULAR_MIXED_ATLAS.tsv", -1, "scope"), ("GLOBAL_INCIDENCE_ATLAS.tsv", -1, "scope"),
        ("GROUP_ACTION_QUOTIENT_ATLAS.tsv", -1, "local_result"), ("VARIATION_CHANNEL_ATLAS.tsv", -1, "scope"),
        ("GLOBAL_OUTPUT_ATLAS.tsv", -1, "status"),
    ]
    for table, row, key in remainder_specs:
        mutate(table, row, key, "FINITE_EXHAUSTIVE", f"remainder_{table}")

    mutate("METRIC_REGULARITY_ATLAS.tsv", 2, "family", "REMOVED_DEGENERATE", "degenerate_removed")
    mutate("CAUSAL_TIME_LIVE_ATLAS.tsv", 2, "family", "REMOVED_NULL", "null_removed")
    mutate("CAUSAL_TIME_LIVE_ATLAS.tsv", 8, "family", "STATIC_ONLY", "moving_removed")
    mutate("FIELD_BUNDLE_ATLAS.tsv", 2, "family", "REMOVED_SIGN_SECTION", "twisted_field_removed")
    mutate("ANGULAR_MIXED_ATLAS.tsv", 4, "family", "ZERO_SHIFT", "time_angular_removed")
    mutate("ANGULAR_MIXED_ATLAS.tsv", 5, "family", "ZERO_SHIFT", "depth_angular_removed")
    mutate("ANGULAR_MIXED_ATLAS.tsv", 3, "family", "TWIST_FREE", "twist_removed")
    mutate("GLOBAL_INCIDENCE_ATLAS.tsv", 0, "family", "REMOVED_CLOSED", "closed_removed")
    mutate("GLOBAL_INCIDENCE_ATLAS.tsv", 5, "family", "PAIR_ONLY", "network_removed")
    mutate("GROUP_ACTION_QUOTIENT_ATLAS.tsv", 1, "family", "FIXED_ONLY", "free_quotient_removed")
    mutate("GROUP_ACTION_QUOTIENT_ATLAS.tsv", 2, "local_result", "all_quotients_are_boundaries", "quotient_type_corrupt")

    mutate("VARIATION_CHANNEL_ATLAS.tsv", 0, "family", "NATIVE_DYNAMICS", "law_imported")
    mutate("VARIATION_CHANNEL_ATLAS.tsv", 3, "scope", "AUTOMATIC_CANCELLATION", "matching_assumed")
    mutate("GLOBAL_OUTPUT_ATLAS.tsv", 1, "status", "DERIVED", "scale_promoted")
    mutate("GLOBAL_OUTPUT_ATLAS.tsv", 2, "status", "DERIVED", "xmax_promoted")

    mutate("COMPATIBILITY_RELATIONS.tsv", 0, "limit", "SELECTS_EXTERNAL_EDGE", "regular_value_overreach")
    mutate("COMPATIBILITY_RELATIONS.tsv", 12, "limit", "RANKS_COMPLETIONS", "conditional_law_ranking")
    mutate("COMPATIBILITY_RELATIONS.tsv", 15, "limit", "PHYSICAL_EVOLUTION", "time_promoted")
    mutate("COMPATIBILITY_RELATIONS.tsv", 16, "limit", "MERIT_FILTER", "regularity_filter")

    mutate("FIELD_LANE_STATUS.tsv", 0, "P06_ready", "YES", "p06_promoted")
    mutate("FIELD_LANE_STATUS.tsv", 0, "atlas_role", "PHYSICAL_RANKING", "lane_ranked")
    bad = copy.deepcopy(tables); bad["FIELD_LANE_STATUS.tsv"].pop()
    expect_failure("field_lane_missing", lambda: validate(result, bad, graph), catches)

    mutate("TEN_CRITERION_SCOPE.tsv", 2, "covered", "all equations solved", "equations_claimed")
    mutate("TEN_CRITERION_SCOPE.tsv", 8, "covered", "stable", "stability_claimed")
    mutate("ANTI_IMPOSITION_AUDIT.tsv", 0, "present", "PRESENT", "named_target_present")
    mutate("ANTI_IMPOSITION_AUDIT.tsv", 1, "present", "PRESENT", "ranking_present")
    mutate("ANTI_IMPOSITION_AUDIT.tsv", 6, "present", "PRESENT", "remainder_hidden")

    bad_graph = copy.deepcopy(graph); bad_graph["classification"] = "SEAL_SELECTED"
    expect_failure("graph_classification", lambda: validate(result, tables, bad_graph), catches)
    bad_graph = copy.deepcopy(graph); bad_graph["forbidden_edges"].pop()
    expect_failure("graph_forbidden_missing", lambda: validate(result, tables, bad_graph), catches)
    bad_graph = copy.deepcopy(graph); bad_graph["layers"][-1] = "CURRENT_PHYSICAL_SOLUTION"
    expect_failure("dynamics_layer_promoted", lambda: validate(result, tables, bad_graph), catches)

    verification = {
        "schema": "udt-finite-cell-completion-atlas-verification-1.0",
        "verdict": "PASS",
        "generator_imported": "NO",
        "independent_checks": len(checks),
        "catch_proofs": len(catches),
        "main_result_sha256": digest(HERE / "ATLAS_RESULT.json"),
        "classification": CLASSIFICATION,
        "fresh_adversarial_context": "OPEN_NOT_PERFORMED",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "UDT_FINITE_CELL_COMPLETION_ATLAS_VERIFICATION=PASS",
        f"independent_checks={len(checks)}",
        f"catch_proofs={len(catches)}",
        "generator_imported=NO",
        "P02_marginal_strata=89/89",
        "completion_axes=10/10",
        "required_unbounded_remainders=10/10",
        "angular_mixed_families=13/13",
        "global_incidence_families=14/14",
        "field_lane_pairs=21/21 P06_ready=0",
        "ranking_or_merit_filter=NO",
        f"main_result_sha256={verification['main_result_sha256']}",
        "fresh_adversarial_context=OPEN_NOT_PERFORMED",
    ]
    (HERE / "VERIFICATION_TRANSCRIPT.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))


if __name__ == "__main__":
    main()

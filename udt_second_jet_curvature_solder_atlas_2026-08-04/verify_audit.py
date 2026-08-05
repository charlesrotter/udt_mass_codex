#!/usr/bin/env python3
"""Fail-closed verification for the second-jet curvature-solder atlas."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "eac22f9e8fa038f6ccaa5dd21764f6964c3c468b"
OUTCOME = (
    "DERIVED_COMPLETE_SECOND_JET_CURVATURE_SURJECTION__"
    "DERIVED_SINGLE_BIANCHI_RECIPROCAL_ANGULAR_BLOCK_RELATION__"
    "DERIVED_CAUSAL_STRATUM_TIDAL_QUOTIENTS__"
    "NO_UNIQUE_CURVATURE_SOLDER_OR_KINEMATIC_EVOLUTION_RETURN"
)
RELATION = [0, 0, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
CATEGORY_RANKS = {"founded": 8, "other_base": 11, "screen": 14, "mixing": 18}
BLOCK_RANKS = {"base_base": 1, "mixed_mixed": 10, "screen_screen": 1, "base_mixed": 4, "mixed_screen": 4, "base_screen": 1}
UNION_RANKS = [8, 11, 14, 18, 14, 19, 19, 19, 19, 19, 19, 19, 20, 20, 20]
INTERSECTIONS = [5, 3, 7, 6, 10, 13]
MINIMAL_FULL = [["founded", "screen", "mixing"], ["other_base", "screen", "mixing"]]


def table(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git_blob(path: str):
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)


def validate(result, independent, sources, sectors, strata, observables, operations, premises, operation_ledger, hypothesis_ledger):
    checks = []
    assert result["outcome"] == OUTCOME, "outcome mismatch"
    assert result["sympy_version"] == "1.13.1", "SymPy version drift"
    checks.append("outcome_and_environment_exact")

    maps = result["second_jet_maps"]
    assert maps["coframe_second_jet_components"] == 160 and maps["metric_second_jet_components"] == 100, "second-jet census changed"
    assert (maps["coframe_to_metric_rank"], maps["coframe_to_metric_nullity"]) == (100, 60), "coframe/metric map changed"
    assert (maps["metric_to_Riemann_rank"], maps["metric_to_Riemann_nullity"]) == (20, 80), "metric/Riemann map changed"
    assert (maps["coframe_to_Riemann_rank"], maps["coframe_to_Riemann_nullity"]) == (20, 140), "coframe/Riemann map changed"
    assert maps["all_ten_Hessian_slots_released"] and (maps["time_time_slots"], maps["time_space_slots"], maps["space_space_slots"]) == (1, 3, 6), "Hessian slot frozen"
    assert maps["extra_kinematic_curvature_constraint_count"] == 0, "extra curvature law invented"
    checks.append("complete_second_jet_maps_exact")

    identities = result["Riemann_identities"]
    assert identities["pair_antisymmetries_exact"] and identities["pair_exchange_exact"] and identities["algebraic_Bianchi_exact"], "Riemann identity failed"
    assert identities["bivector_symmetric_entries"] == 21 and identities["relation_dimension_among_21_entries"] == 1, "Bianchi relation dimension changed"
    assert identities["primitive_relation"] == RELATION, "Bianchi relation changed"
    assert [row["slot"] for row in identities["relation_nonzero_entries"]] == [[0, 5], [1, 4], [2, 3]], "Bianchi support changed"
    checks.append("Riemann_and_Bianchi_exact")

    blocks = result["bivector_blocks"]
    actual_blocks = {row["block"]: row["projection_rank"] for row in blocks["rows"]}
    assert actual_blocks == BLOCK_RANKS, "2+2 block ranks changed"
    assert blocks["all_six_block_classes_nonzero"] and blocks["sum_displayed_entries"] == 21 and blocks["joint_rank"] == 20 and blocks["joint_relation_count"] == 1, "block atlas changed"
    assert all(row["all_entries_individually_nonzero_available"] for row in blocks["rows"]), "cross block erased"
    checks.append("complete_2plus2_block_atlas_exact")

    ensembles = result["source_ensembles"]
    actual_categories = {row["category"]: row["image_rank"] for row in ensembles["category_rows"]}
    assert actual_categories == CATEGORY_RANKS, "category ranks changed"
    assert [row["image_rank"] for row in ensembles["all_nonempty_category_unions"]] == UNION_RANKS, "union ranks changed"
    assert [row["intersection_dimension"] for row in ensembles["pairwise_intersections"]] == INTERSECTIONS, "intersection dimensions changed"
    assert ensembles["minimal_full_category_sets"] == MINIMAL_FULL and ensembles["complete_union_rank"] == 20, "minimal full ensembles changed"
    expected_category_blocks = {
        "founded": {"base_base": 1, "mixed_mixed": 3, "screen_screen": 0, "base_mixed": 4, "mixed_screen": 0, "base_screen": 0},
        "other_base": {"base_base": 1, "mixed_mixed": 6, "screen_screen": 0, "base_mixed": 4, "mixed_screen": 0, "base_screen": 0},
        "screen": {"base_base": 0, "mixed_mixed": 9, "screen_screen": 1, "base_mixed": 0, "mixed_screen": 4, "base_screen": 0},
        "mixing": {"base_base": 0, "mixed_mixed": 10, "screen_screen": 0, "base_mixed": 4, "mixed_screen": 4, "base_screen": 1},
    }
    assert {row["category"]: row["block_projection_ranks"] for row in ensembles["category_rows"]} == expected_category_blocks, "category block support changed"
    assert all(row["image_rank"] == 8 for row in ensembles["generator_rows"]), "single-generator ranks changed"
    checks.append("source_ensemble_orchestra_exact")

    depth_rows = result["depth_strata"]["rows"]
    assert [(row["stratum"], row["N_rank"], row["quotient_dimension"], row["tidal_image_rank"]) for row in depth_rows] == [
        ("timelike", 3, 3, 6), ("spacelike", 3, 3, 6), ("nonzero_null", 1, 2, 3), ("zero", 0, 0, 0)
    ], "depth stratum ranks changed"
    assert all(row["N_squared_equals_s_times_N"] for row in depth_rows), "N algebra failed"
    assert depth_rows[2]["N_nilpotent_nonzero"] and depth_rows[2]["null_quotient_representative_independence"], "null quotient failed"
    assert result["depth_strata"]["nonnull_N_rank_three"] and result["depth_strata"]["null_N_rank_one_nilpotent"] and result["depth_strata"]["zero_N_and_tidal"], "stratified N summary changed"
    assert not result["depth_strata"]["constant_rank_normalized_screen_across_all_strata"], "constant-rank screen invented"
    checks.append("depth_and_tidal_strata_exact")

    boundary = result["rank_and_asymptotic_boundary"]
    assert boundary["Levi_Civita_curvature_defined_only_at_coframe_rank_four"] and not boundary["generalized_inverse_or_curvature_continuation_derived"], "rank-loss curvature invented"
    assert boundary["finite_phi_pair_determinant"] == -1 and not boundary["finite_phi_rank_loss"] and boundary["phi_asymptotes_are_limit_only"] and not boundary["Xmax_derived"], "phi boundary promoted"
    assert not result["configuration_path_is_physical_time"] and not result["same_solution_source_dphi_join_derived"] and not result["physical_evolution_operator_derived"] and not result["native_bootstrap_return_derived"] and not result["unique_curvature_solder_derived"], "physical return promoted"
    checks.append("boundary_and_authority_scope_exact")

    assert independent["map_ranks"] == {"coframe_to_Riemann": 20, "coframe_to_metric": 100, "metric_to_Riemann": 20}, "independent map mismatch"
    assert independent["Bianchi_relation_dimension"] == 1 and independent["Bianchi_primitive_relation"] == RELATION, "independent Bianchi mismatch"
    assert {row["block"]: row["projection_rank"] for row in independent["block_rows"]} == BLOCK_RANKS, "independent block mismatch"
    assert {row["category"]: row["image_rank"] for row in independent["ensembles"]["category_rows"]} == CATEGORY_RANKS, "independent category mismatch"
    assert [row["image_rank"] for row in independent["ensembles"]["union_rows"]] == UNION_RANKS and independent["ensembles"]["minimal_full_category_sets"] == MINIMAL_FULL, "independent unions mismatch"
    assert [row["intersection_dimension"] for row in independent["ensembles"]["pairwise_intersections"]] == INTERSECTIONS, "independent intersections mismatch"
    assert [(row["stratum"], row["N_rank"], row["quotient_dimension"], row["tidal_image_rank"]) for row in independent["depth_rows"]] == [
        ("timelike", 3, 3, 6), ("spacelike", 3, 3, 6), ("nonzero_null", 1, 2, 3), ("zero", 0, 0, 0)
    ], "independent depth mismatch"
    independent_null = next(row for row in independent["depth_rows"] if row["stratum"] == "nonzero_null")
    assert independent_null["null_quotient_representative_independence"], "independent null representative-independence failed"
    assert not independent["same_solution_source_dphi_join_derived"] and not independent["physical_evolution_operator_derived"] and not independent["unique_curvature_solder_derived"], "independent promotion"
    checks.append("independent_rational_reconstruction_matches")

    assert len(sources) == 27 and [row["source_id"] for row in sources] == [f"S{i:02d}" for i in range(1, 28)], "source universe changed"
    for row in sources:
        assert hashlib.sha256(git_blob(row["path"])).hexdigest() == row["sha256"], f"source hash mismatch: {row['path']}"
    checks.append("base_source_hashes_27_exact")

    assert len(sectors) == 17 and [row["sector_id"] for row in sectors] == [f"J{i:02d}" for i in range(1, 18)], "sector universe changed"
    assert len(strata) == 14 and {row["stratum_id"] for row in strata} == {"P00", "P01", "P02", "P03", "C04", "C03M", "A00", "A01", "A02", "E01", "E02", "E03", "E04", "E05"}, "stratum universe changed"
    assert len(observables) == 25 and [row["observable_id"] for row in observables] == [f"O{i:02d}" for i in range(1, 26)], "observable universe changed"
    assert len(operations) == 12 and [row["operation_id"] for row in operations] == [f"T{i:02d}" for i in range(1, 13)], "operation universe changed"
    assert len(premises) == 26 and [row["premise_id"] for row in premises] == [f"P{i:02d}" for i in range(1, 27)], "premise universe changed"
    by_premise = {row["premise_id"]: row["status"] for row in premises}
    assert by_premise["P08"] == "FREE_AND_EXPLORED" and by_premise["P21"] == "NOT_ASSUMED" and by_premise["P22"] == "OPEN_NOT_SUPPLIED", "physical choice promoted"
    assert by_premise["P24"] == "INACTIVE" and by_premise["P26"] == "POSIT_UNUSED", "inactive premise promoted"
    checks.append("frozen_universes_and_premises_exact")

    assert len(operation_ledger) == 12 and [row["operation_id"] for row in operation_ledger] == [f"T{i:02d}" for i in range(1, 13)], "operation ledger changed"
    assert next(row for row in operation_ledger if row["operation_id"] == "T12")["physical_ruling"] == "NO_PHYSICAL_EVOLUTION_BOOTSTRAP_OR_ACTION", "operation return promoted"
    assert len(hypothesis_ledger) == 9 and [row["hypothesis_id"] for row in hypothesis_ledger] == [f"H{i}" for i in range(1, 10)], "hypothesis ledger changed"
    assert next(row for row in hypothesis_ledger if row["hypothesis_id"] == "H7")["ruling"] == "SUPPORTED_DERIVED", "null plurality erased"
    checks.append("operation_and_hypothesis_ledgers_exact")

    report_text = "\n".join((HERE / name).read_text(encoding="utf-8") for name in ["EXACT_DERIVATION.md", "COMPLETENESS_MAP.md", "LAY_REPORT.md", "AUDIT_REPORT.md"])
    for required in ["SAME_SOLUTION_JOIN_OPEN_NOT_DERIVED", "SUPPLIED_SPLIT_LOCAL_ATLAS"]:
        assert required in report_text, f"missing scope disclosure: {required}"
    for forbidden in ["NATIVE_ACTION_DERIVED", "PHYSICAL_TIME_EVOLUTION_DERIVED", "BOOTSTRAP_RETURN_DERIVED", "UNIQUE_PHYSICAL_SOLDER_DERIVED", "SAME_SOLUTION_JOIN_DERIVED", "XMAX_DERIVED", "STRONG_CSN_ACTIVE"]:
        assert forbidden not in report_text, f"forbidden promotion: {forbidden}"
    checks.append("semantic_scope_guards")
    return checks


def expect_caught(mutation_id, description, mutate, baseline):
    trial = copy.deepcopy(baseline)
    mutate(*trial)
    try:
        validate(*trial)
    except (AssertionError, KeyError) as exc:
        return {"mutation_id": mutation_id, "description": description, "status": "CAUGHT", "reason": str(exc)}
    raise AssertionError(f"mutation escaped: {mutation_id} {description}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    fresh_result = json.loads(subprocess.check_output(["python3", str(HERE / "derive_second_jet_solder.py"), "--no-write"], cwd=ROOT, text=True))
    fresh_independent = json.loads(subprocess.check_output(["python3", str(HERE / "independent_second_jet_solder.py"), "--no-write"], cwd=ROOT, text=True))
    assert fresh_result == result, "fresh primary replay mismatch"
    assert fresh_independent == independent, "fresh independent replay mismatch"

    baseline = [
        result, independent, table(HERE / "SOURCE_ADJUDICATION.tsv"), table(HERE / "SECTOR_UNIVERSE.tsv"),
        table(HERE / "STRATUM_UNIVERSE.tsv"), table(HERE / "OBSERVABLE_UNIVERSE.tsv"),
        table(HERE / "OPERATION_UNIVERSE.tsv"), table(HERE / "PREMISE_LEDGER.tsv"),
        table(HERE / "OPERATION_LEDGER.tsv"), table(HERE / "HYPOTHESIS_LEDGER.tsv"),
    ]
    checks = validate(*baseline)
    checks.append("fresh_primary_and_independent_replays_match_saved_results")
    mutations = [
        ("M01", "wrong outcome", lambda r, *_: r.update(outcome="CLOSED")),
        ("M02", "Hessian slot frozen", lambda r, *_: r["second_jet_maps"].update(all_ten_Hessian_slots_released=False)),
        ("M03", "coframe-to-metric rank reduced", lambda r, *_: r["second_jet_maps"].update(coframe_to_metric_rank=99)),
        ("M04", "curvature rank reduced", lambda r, *_: r["second_jet_maps"].update(metric_to_Riemann_rank=19)),
        ("M05", "Bianchi relation deleted", lambda r, *_: r["Riemann_identities"].update(relation_dimension_among_21_entries=0)),
        ("M06", "Bianchi relation changed", lambda r, *_: r["Riemann_identities"]["primitive_relation"].__setitem__(5, 2)),
        ("M07", "cross block erased", lambda r, *_: r["bivector_blocks"].update(all_six_block_classes_nonzero=False)),
        ("M08", "founded category promoted", lambda r, *_: next(row for row in r["source_ensembles"]["category_rows"] if row["category"] == "founded").update(image_rank=20)),
        ("M09", "mixing category reduced", lambda r, *_: next(row for row in r["source_ensembles"]["category_rows"] if row["category"] == "mixing").update(image_rank=17)),
        ("M10", "minimal full set deleted", lambda r, *_: r["source_ensembles"]["minimal_full_category_sets"].pop()),
        ("M11", "founded plus screen made full", lambda r, *_: r["source_ensembles"]["all_nonempty_category_unions"][5].update(image_rank=20)),
        ("M12", "null N rank promoted", lambda r, *_: r["depth_strata"]["rows"][2].update(N_rank=3)),
        ("M13", "null quotient descent erased", lambda r, *_: r["depth_strata"]["rows"][2].update(null_quotient_representative_independence=False)),
        ("M14", "null tidal rank reduced", lambda r, *_: r["depth_strata"]["rows"][2].update(tidal_image_rank=2)),
        ("M15", "zero stratum screen invented", lambda r, *_: r["depth_strata"]["rows"][3].update(quotient_dimension=2)),
        ("M16", "rank-loss curvature invented", lambda r, *_: r["rank_and_asymptotic_boundary"].update(generalized_inverse_or_curvature_continuation_derived=True)),
        ("M17", "configuration path promoted to time", lambda r, *_: r.update(configuration_path_is_physical_time=True)),
        ("M18", "unique solder promoted", lambda r, *_: r.update(unique_curvature_solder_derived=True)),
        ("M19", "source hash corrupted", lambda r, i, sources, *_: sources[0].update(sha256="0" * 64)),
        ("M20", "sector deleted", lambda r, i, sources, sectors, *_: sectors.pop()),
        ("M21", "stratum deleted", lambda r, i, sources, sectors, strata, *_: strata.pop()),
        ("M22", "observable deleted", lambda r, i, sources, sectors, strata, observables, *_: observables.pop()),
        ("M23", "operation deleted", lambda r, i, sources, sectors, strata, observables, operations, *_: operations.pop()),
        ("M24", "premise deleted", lambda r, i, sources, sectors, strata, observables, operations, premises, *_: premises.pop()),
        ("M25", "operation return promoted", lambda r, i, sources, sectors, strata, observables, operations, premises, operation_ledger, *_: next(row for row in operation_ledger if row["operation_id"] == "T12").update(physical_ruling="PHYSICAL_EVOLUTION")),
        ("M26", "null plurality erased", lambda r, i, sources, sectors, strata, observables, operations, premises, operation_ledger, hypotheses: next(row for row in hypotheses if row["hypothesis_id"] == "H7").update(ruling="UNIQUE")),
        ("M27", "same-solution source/dphi join promoted", lambda r, *_: r.update(same_solution_source_dphi_join_derived=True)),
        ("M28", "independent null representative-independence erased", lambda r, i, *_: next(row for row in i["depth_rows"] if row["stratum"] == "nonzero_null").update(null_quotient_representative_independence=False)),
    ]
    catches = [expect_caught(mid, description, mutate, baseline) for mid, description, mutate in mutations]
    verification = {
        "schema": "udt.second_jet_curvature_solder.verification.v1",
        "status": "PASS",
        "checks_passed": len(checks),
        "checks": checks,
        "mutations_caught": len(catches),
        "catch_proofs": catches,
        "source_adjudication_sha256": hashlib.sha256((HERE / "SOURCE_ADJUDICATION.tsv").read_bytes()).hexdigest(),
    }
    rendered = json.dumps(verification, indent=2, sort_keys=True) + "\n"
    if not args.no_write:
        (HERE / "VERIFICATION_RESULT.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

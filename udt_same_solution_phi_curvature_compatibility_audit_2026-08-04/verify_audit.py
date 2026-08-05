#!/usr/bin/env python3
"""Fail-closed verifier and mutation catch-proofs for the same-solution audit."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "VERIFICATION_RESULT.json"
CATCH_OUT = HERE / "CATCH_PROOFS.tsv"
BASE = "a353af410e84abc1982401d9367e0845a1b1458d"
EXPECTED_RANKS = {"F01": 20, "F02": 20, "F03": 19, "F04": 19, "F05": 8, "F06": 10, "F07": 10, "F08": 20, "F09": None}
EXPECTED_STRATA = {"ZERO", "TIMELIKE", "SPACELIKE", "NONZERO_NULL"}


def read_tsv(name):
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def source_bytes(path):
    return subprocess.run(
        ["git", "show", f"{BASE}:{path}"], cwd=ROOT, check=True, stdout=subprocess.PIPE
    ).stdout


def source_hashes(rows):
    return {
        row["source_id"]: hashlib.sha256(source_bytes(row["path"])).hexdigest()
        for row in rows
    }


def state_from_disk():
    primary = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    return {
        "sources": read_tsv("SOURCE_ADJUDICATION.tsv"),
        "architectures": read_tsv("OWNERSHIP_ARCHITECTURE_UNIVERSE.tsv"),
        "families_universe": read_tsv("REALIZATION_FAMILY_UNIVERSE.tsv"),
        "jets": read_tsv("JET_STRATUM_UNIVERSE.tsv"),
        "observables": read_tsv("OBSERVABLE_UNIVERSE.tsv"),
        "operations": read_tsv("OPERATION_UNIVERSE.tsv"),
        "premises": read_tsv("PREMISE_LEDGER.tsv"),
        "primary": primary,
        "independent": independent,
        "actual_source_hashes": source_hashes(read_tsv("SOURCE_ADJUDICATION.tsv")),
    }


def validate(state):
    checks = []

    def require(name, condition):
        checks.append((name, bool(condition)))
        if not condition:
            raise AssertionError(name)

    sources = state["sources"]
    require("source_count_28", len(sources) == 28 and {row["source_id"] for row in sources} == {f"S{i:02d}" for i in range(1, 29)})
    require("source_hashes_exact_at_base", all(state["actual_source_hashes"].get(row["source_id"]) == row["sha256_at_base"] for row in sources))
    require("architecture_count_5", len(state["architectures"]) == 5 and {row["architecture_id"] for row in state["architectures"]} == {f"A{i:02d}" for i in range(1, 6)})
    architecture = {row["architecture_id"]: row for row in state["architectures"]}
    require("supplied_chart_not_selected", architecture["A02"]["status"] == "DEFINED_CONFIGURATION_ARCHITECTURE" and "preferred frame" in architecture["A02"]["forbidden_promotion"])
    require("independent_scalar_not_native", architecture["A04"]["status"] == "CHOSE_COMPARISON_CONFIGURATION" and "native" in architecture["A04"]["forbidden_promotion"])
    require("family_universe_exact_9", len(state["families_universe"]) == 9 and {row["family_id"] for row in state["families_universe"]} == set(EXPECTED_RANKS))
    require("all_ten_depth_hessians_free", any(row["axis_id"] == "J05" and row["exact_representative"] == "10 slots" and row["freedom"] == "FREE_AND_EXPLORED" for row in state["jets"]))
    require("causal_strata_frozen", {row["member"] for row in state["jets"] if row["axis"] == "depth_first_jet"} == EXPECTED_STRATA)
    require("operation_universe_exact_10", len(state["operations"]) == 10 and {row["operation_id"] for row in state["operations"]} == {f"P{i:02d}" for i in range(1, 11)})
    require("ownership_operation_retained", any(row["operation_id"] == "P08" for row in state["operations"]))
    require("premise_universe_exact_12", len(state["premises"]) == 12 and {row["premise_id"] for row in state["premises"]} == {f"L{i:02d}" for i in range(1, 13)})
    require("assignment_remains_open", any(row["premise_id"] == "L10" and row["status"] == "OPEN" for row in state["premises"]))
    result_rows = {row["family_id"]: row for row in state["primary"]["families"]}
    observed_ranks = {family: row["curvature_rank"] for family, row in result_rows.items()}
    require("primary_family_ranks_exact", observed_ranks == EXPECTED_RANKS)
    require("independent_family_ranks_match", state["independent"]["family_ranks"] == EXPECTED_RANKS)
    require("all_four_strata_each_typed_family", all(set(row["causal_stratum_ranks"]) == EXPECTED_STRATA for row in result_rows.values()))
    require("causal_ranks_constant", all(len(set(value for value in row["causal_stratum_ranks"].values() if value is not None)) <= 1 for row in result_rows.values()))
    require("first_jet_only_affine_offset", state["primary"]["affine_curvature_theorem"]["Hessian_coefficient_independent_of_first_jet"] and not state["primary"]["affine_curvature_theorem"]["causal_type_or_amplitude_changes_rank_on_regular_tile"])
    first_kernel = state["primary"]["factorization"]["released_reference_first_jet"]
    second_kernel = state["primary"]["factorization"]["released_reference_second_jet_fixed_first_jets"]
    require("reference_factorization_kernel", first_kernel["explicit_phi_kernel_verified"] and first_kernel["per_derivative_nullity"] == 8 and second_kernel["explicit_phi_hessian_kernel_verified"] and second_kernel["per_symmetric_slot_nullity"] == 8)
    require("finite_redefinition_exact", state["primary"]["factorization"]["exact_finite_redefinition"]["theta_unchanged"] and state["independent"]["finite_redefinition_check"]["all_exact"])
    require("independent_scalar_untyped", result_rows["F09"]["same_solution_class"] == "UNTYPED_NO_METRIC_ACTION" and result_rows["F09"]["ownership"] == "CHOSE_COMPARISON_CONFIGURATION")
    require("no_unique_selection_promotion", all("UNIQUE" not in row["same_solution_class"] for row in result_rows.values()) and not state["primary"]["ownership_verdict"]["physical_extension_selected"])
    require("no_time_or_bootstrap_promotion", not state["primary"]["ownership_verdict"]["response_or_evolution_law_derived"] and not state["primary"]["ownership_verdict"]["bootstrap_closure_derived"])
    require("coframe_phi_not_identified", not state["primary"]["ownership_verdict"]["complete_coframe_identifies_phi_jets"] and not state["independent"]["coframe_only_phi_identifiable"])
    return checks


def replay_results():
    primary_module = load_module("same_solution_primary_replay", "derive_same_solution.py")
    replay_primary, replay_witnesses, replay_rows = primary_module.derive()
    saved_primary = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    saved_witnesses = json.loads((HERE / "RIGHT_INVERSE_WITNESSES.json").read_text(encoding="utf-8"))
    independent_module = load_module("same_solution_independent_replay", "independent_same_solution.py")
    replay_independent = independent_module.derive()
    saved_independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    return {
        "primary_result_exact": replay_primary == saved_primary,
        "right_inverse_result_exact": replay_witnesses == saved_witnesses,
        "primary_family_ledger_rows": len(replay_rows),
        "independent_result_exact": replay_independent == saved_independent,
    }


def verify_right_inverses():
    primary_module = load_module("same_solution_primary_witness", "derive_same_solution.py")
    curvature = primary_module.curvature_map()
    matrices = primary_module.family_matrices(curvature)
    witnesses = json.loads((HERE / "RIGHT_INVERSE_WITNESSES.json").read_text(encoding="utf-8"))["families"]
    results = {}
    for family, witness in witnesses.items():
        matrix = matrices[family]
        rows = witness["independent_display_rows"]
        cols = witness["pivot_hessian_columns"]
        inverse = sp.Matrix([[sp.Rational(value) for value in row] for row in witness["inverse"]])
        results[family] = bool(matrix[rows, cols] * inverse == sp.eye(20))
    return results


def mutation_catches(base_state):
    mutations = []

    def exercise(catch_id, description, mutate):
        state = copy.deepcopy(base_state)
        mutate(state)
        caught = False
        try:
            validate(state)
        except AssertionError:
            caught = True
        mutations.append({"catch_id": catch_id, "description": description, "caught": caught})

    exercise("C01", "delete realization family", lambda s: s["families_universe"].pop())
    exercise("C02", "promote supplied chart to selected section", lambda s: s["architectures"][1].update(status="SELECTED_PHYSICAL_SECTION"))
    exercise("C03", "erase reference factorization kernel", lambda s: s["primary"]["factorization"]["released_reference_first_jet"].update(explicit_phi_kernel_verified=False))
    exercise("C04", "promote independent scalar to native", lambda s: next(row for row in s["primary"]["families"] if row["family_id"] == "F09").update(ownership="NATIVE_FIELD"))
    exercise("C05", "freeze one depth Hessian universe", lambda s: next(row for row in s["jets"] if row["axis_id"] == "J05").update(freedom="PINNED_BY_HABIT"))
    exercise("C06", "change a family curvature rank", lambda s: next(row for row in s["primary"]["families"] if row["family_id"] == "F06").update(curvature_rank=11))
    exercise("C07", "omit nonzero-null causal stratum", lambda s: next(row for row in s["primary"]["families"] if row["family_id"] == "F01")["causal_stratum_ranks"].pop("NONZERO_NULL"))
    exercise("C08", "claim first-jet rank dependence", lambda s: s["primary"]["affine_curvature_theorem"].update(causal_type_or_amplitude_changes_rank_on_regular_tile=True))
    exercise("C09", "promote existence to unique selection", lambda s: next(row for row in s["primary"]["families"] if row["family_id"] == "F01").update(same_solution_class="UNIQUE_PHYSICAL_SELECTION"))
    exercise("C10", "promote local algebra to physical time", lambda s: s["primary"]["ownership_verdict"].update(response_or_evolution_law_derived=True))
    exercise("C11", "promote local algebra to bootstrap closure", lambda s: s["primary"]["ownership_verdict"].update(bootstrap_closure_derived=True))
    exercise("C12", "drift a fixed source hash", lambda s: s["sources"][0].update(sha256_at_base="0" * 64))
    exercise("C13", "delete assignment-open premise", lambda s: s["premises"].remove(next(row for row in s["premises"] if row["premise_id"] == "L10")))
    exercise("C14", "delete ownership operation", lambda s: s["operations"].remove(next(row for row in s["operations"] if row["operation_id"] == "P08")))
    exercise("C15", "falsely identify phi from coframe", lambda s: s["primary"]["ownership_verdict"].update(complete_coframe_identifies_phi_jets=True))
    exercise("C16", "erase independent-scalar untyped status", lambda s: next(row for row in s["primary"]["families"] if row["family_id"] == "F09").update(same_solution_class="ALL_ALGEBRAIC_RIEMANN"))
    return mutations


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    state = state_from_disk()
    checks = validate(state)
    replay = replay_results()
    right_inverses = verify_right_inverses()
    catches = mutation_catches(state)
    result = {
        "schema": "udt.same_solution_phi_curvature.verification.v1",
        "checks": [{"check": name, "pass": passed} for name, passed in checks],
        "check_count": len(checks),
        "all_checks_pass": all(passed for _, passed in checks),
        "replay": replay,
        "all_replays_exact": all(value is True or key == "primary_family_ledger_rows" for key, value in replay.items()),
        "right_inverse_checks": right_inverses,
        "all_right_inverses_exact": all(right_inverses.values()),
        "catches": catches,
        "catch_count": len(catches),
        "all_catches_pass": all(row["caught"] for row in catches),
    }
    assert result["all_checks_pass"] and result["all_replays_exact"] and result["all_right_inverses_exact"] and result["all_catches_pass"]
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if not args.no_write:
        OUT.write_text(rendered, encoding="utf-8")
        lines = ["catch_id\tdescription\tcaught"] + [f"{row['catch_id']}\t{row['description']}\t{str(row['caught']).lower()}" for row in catches]
        CATCH_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

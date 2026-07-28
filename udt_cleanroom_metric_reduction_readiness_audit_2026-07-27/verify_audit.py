#!/usr/bin/env python3
"""Fail-closed verifier and exercised catch proofs for the clean-room audit."""

from __future__ import annotations

import ast
import copy
import csv
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent

EXPECTED_CLASSES = {
    "C01": "OPEN_UNDERDETERMINED_CONFIGURATION",
    "C02": "OPEN_UNDERDETERMINED_EVOLUTION",
    "C03": "CONFIGURATION_FAMILY_NOT_PROFILE_EQUATION",
    "C04": "REGISTERED_FIXED_CONTROL_NO_NONTRIVIAL_EVOLUTION",
    "C05": "CLOSED_KINEMATIC_ON_SUPPLIED_CONFIGURATION",
    "C06": "CLOSED_KINEMATIC_ON_SUPPLIED_CONFIGURATION",
    "C07": "CLOSED_KINEMATIC_ON_SUPPLIED_CONFIGURATION_AND_SCREEN_STRATUM",
    "C08": "CLOSED_KINEMATIC_ON_SUPPLIED_CONFIGURATION_AND_GEODESIC",
    "C09": "OPEN_NO_SELECTED_CURVATURE_RESPONSE",
    "C10": "OPEN_ON_SHELL_ADMISSIBILITY_NOT_EVOLUTION",
    "C11": "OPEN_CARRIER_AND_ACTION_UNSELECTED",
    "C12": "OPEN_COMPATIBILITY_NOT_BOUNDARY_EVOLUTION",
    "C13": "DERIVED_EVALUATOR_NOT_BACKGROUND_EQUATION",
    "C14": "DERIVED_IDENTITY_NOT_BACKGROUND_EQUATION",
    "C15": "QUARANTINED_PENDING_POSTVERDICT_PROVENANCE",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    clean = data.get("cleanroom", {})
    require(clean.get("legacy_equation_files_opened") is False, "legacy equation content entered clean room", errors)
    require(clean.get("old_solver_results_used") is False, "old solver result used", errors)
    require(clean.get("legacy_solver_imports") == [], "legacy solver imported", errors)

    neutral = data.get("neutral_chart", {})
    require(neutral.get("configuration_directions") == 8, "not all eight chart directions retained", errors)
    require(neutral.get("coframe_tangent_rank") == 8, "coframe tangent rank is not eight", errors)
    require(neutral.get("metric_tangent_rank") == 8, "metric tangent rank is not eight", errors)
    require(neutral.get("founded_phi_is_extra_scalar") is False, "phi promoted to extra scalar", errors)

    c1 = data.get("cartan_first_equation", {})
    require((c1.get("connection_unknowns"), c1.get("linear_rank")) == (24, 24), "Cartan connection rank mismatch", errors)
    require(c1.get("background_equation_rank") == 0, "first Cartan definition promoted to background equation", errors)
    require(data.get("cartan_second_equation", {}).get("background_equation_rank") == 0, "second Cartan definition promoted", errors)
    require(data.get("bianchi", {}).get("background_equation_rank") == 0, "Bianchi identity promoted", errors)
    require(data.get("maurer_cartan", {}).get("zero") is True, "Maurer-Cartan identity replay failed", errors)

    reductions = data.get("background_reductions", {})
    ode = reductions.get("cohomogeneity_one", {})
    require((ode.get("live_profile_directions"), ode.get("metric_supplied_profile_equation_rank"), ode.get("closure_deficit"), ode.get("closed")) == (8, 0, 8, False), "background ODE closure incorrectly graded", errors)
    live = reductions.get("one_plus_one", {})
    require((live.get("time_principal_directions"), live.get("metric_supplied_evolution_principal_rank"), live.get("evolution_closure_deficit"), live.get("closed")) == (8, 0, 8, False), "time-live closure incorrectly graded", errors)

    inactive = data.get("inactive_inputs", {})
    for key in ("strong_local_CSN", "action", "source", "carrier", "bootstrap_local_equation", "GR_field_equation"):
        require(inactive.get(key) is False, f"inactive input activated: {key}", errors)
    require(data.get("acceptance_filters") == [], "merit filter introduced", errors)
    require(data.get("cross_spliced_controls") is False, "conditional controls cross-spliced", errors)

    systems = data.get("systems", [])
    ids = [row.get("candidate_id") for row in systems]
    require(len(ids) == 15 and len(set(ids)) == 15 and set(ids) == set(EXPECTED_CLASSES), "candidate coverage mismatch", errors)
    lookup = {row.get("candidate_id"): row for row in systems}
    for cid, expected in EXPECTED_CLASSES.items():
        require(lookup.get(cid, {}).get("classification") == expected, f"classification mismatch {cid}", errors)
    executable = {cid for cid, row in lookup.items() if row.get("conditionally_executable") is True}
    require(executable == {"C05", "C06", "C07", "C08"}, "wrong executable system set", errors)
    require(lookup.get("C13", {}).get("supplied_equation_rank") == 24 and lookup.get("C13", {}).get("conditionally_executable") is False, "connection evaluator promoted", errors)

    auth = data.get("authorization", {})
    for key in ("metric_background_ode", "metric_time_live", "legacy_solver_execution", "gpu"):
        require(auth.get(key) is False, f"unauthorized solve enabled: {key}", errors)
    require(auth.get("conditional_kinematic_path_ode_atlas") is True, "conditional path ODE readiness lost", errors)
    return errors


def mutate_system(data: dict, cid: str, key: str, value: object) -> dict:
    out = copy.deepcopy(data)
    next(row for row in out["systems"] if row["candidate_id"] == cid)[key] = value
    return out


def catch_proofs(data: dict) -> list[dict[str, object]]:
    mutations: list[tuple[str, dict]] = []
    m = copy.deepcopy(data); m["cartan_first_equation"]["background_equation_rank"] = 24; mutations.append(("F01", m))
    m = copy.deepcopy(data); m["cartan_second_equation"]["background_equation_rank"] = 36; mutations.append(("F02", m))
    m = copy.deepcopy(data); m["bianchi"]["background_equation_rank"] = 1; mutations.append(("F03", m))
    m = copy.deepcopy(data); m["background_reductions"]["cohomogeneity_one"]["live_profile_directions"] = 7; mutations.append(("F04", m))
    m = copy.deepcopy(data); m["neutral_chart"]["founded_phi_is_extra_scalar"] = True; mutations.append(("F05", m))
    m = copy.deepcopy(data); m["inactive_inputs"]["strong_local_CSN"] = True; mutations.append(("F06", m))
    mutations.append(("F07", mutate_system(data, "C05", "classification", "BACKGROUND_DYNAMICS")))
    mutations.append(("F08", mutate_system(data, "C07", "classification", "UNIVERSAL_PHYSICAL_SCREEN")))
    mutations.append(("F09", mutate_system(data, "C08", "classification", "METRIC_EVOLUTION")))
    mutations.append(("F10", mutate_system(data, "C09", "conditionally_executable", True)))
    mutations.append(("F11", mutate_system(data, "C10", "conditionally_executable", True)))
    m = copy.deepcopy(data); m["cleanroom"]["legacy_equation_files_opened"] = True; mutations.append(("F12", m))
    m = copy.deepcopy(data); m["authorization"]["metric_time_live"] = True; mutations.append(("F13", m))
    mutations.append(("F14", mutate_system(data, "C12", "conditionally_executable", True)))
    m = copy.deepcopy(data); m["acceptance_filters"] = ["smooth_particle_like_only"]; mutations.append(("F15", m))
    mutations.append(("F16", mutate_system(data, "C03", "conditionally_executable", True)))
    m = copy.deepcopy(data); m["cross_spliced_controls"] = True; mutations.append(("F17", m))
    m = copy.deepcopy(data); m["authorization"]["metric_background_ode"] = True; mutations.append(("F18", m))
    return [{"catch_id": cid, "result": "PASS" if validate(mutated) else "FAIL"} for cid, mutated in mutations]


def main() -> None:
    errors: list[str] = []
    production = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((PACKAGE / "INDEPENDENT_RESULT.json").read_text())
    errors.extend(validate(production))

    require(independent.get("result") == "PASS", "independent implementation failed", errors)
    require((independent.get("coframe_tangent_rank"), independent.get("metric_tangent_rank")) == (8, 8), "independent tangent ranks disagree", errors)
    require((independent.get("cartan_connection_unknowns"), independent.get("cartan_connection_rank"), independent.get("cartan_background_equation_rank")) == (24, 24, 0), "independent Cartan classification disagrees", errors)
    require(independent.get("cohomogeneity_one") == {"live_directions": 8, "supplied_equation_rank": 0, "deficit": 8, "closed": False}, "independent ODE closure disagrees", errors)
    require(independent.get("one_plus_one") == {"time_principal_directions": 8, "supplied_principal_rank": 0, "deficit": 8, "closed": False}, "independent time-live closure disagrees", errors)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    require(len(sources) == 10, "source manifest count mismatch", errors)
    for row in sources:
        path = REPO / row["path"]
        require(path.is_file(), f"missing source {row['path']}", errors)
        if path.is_file():
            require(digest(path) == row["sha256"], f"source hash mismatch {row['path']}", errors)

    with (PACKAGE / "SYSTEM_OUTCOMES.tsv").open(newline="") as handle:
        table = list(csv.DictReader(handle, delimiter="\t"))
    require(len(table) == 15 and {row["candidate_id"] for row in table} == set(EXPECTED_CLASSES), "system table coverage mismatch", errors)
    prod_lookup = {row["candidate_id"]: row for row in production["systems"]}
    for row in table:
        require(row["classification"] == prod_lookup[row["candidate_id"]]["classification"], f"table/result mismatch {row['candidate_id']}", errors)

    tree = ast.parse((PACKAGE / "verify_cleanroom_reduction_independent.py").read_text())
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    require(imported <= {"__future__", "argparse", "json", "fractions", "pathlib"}, "independent implementation has non-stdlib or production import", errors)

    catches = catch_proofs(production)
    require(len(catches) == 18 and all(row["result"] == "PASS" for row in catches), "one or more catch proofs did not reject mutation", errors)
    with (PACKAGE / "FALSIFICATION_CONTRACT.tsv").open(newline="") as handle:
        prereg_catches = list(csv.DictReader(handle, delimiter="\t"))
    require([row["catch_id"] for row in prereg_catches] == [row["catch_id"] for row in catches], "catch universe mismatch", errors)

    result = {
        "schema": "udt-cleanroom-metric-reduction-verification-1.0",
        "result": "PASS" if not errors else "FAIL",
        "errors": errors,
        "checks": {
            "production_semantic_and_rank": "PASS" if not validate(production) else "FAIL",
            "independent_reconstruction": independent.get("result"),
            "source_hashes": len(sources),
            "candidate_systems": len(table),
            "catch_proofs": len(catches),
            "catch_proofs_passed": sum(row["result"] == "PASS" for row in catches),
            "legacy_solver_content_used": False,
        },
        "catch_proofs": catches,
        "hashes": {
            "production": digest(PACKAGE / "DERIVATION_RESULT.json"),
            "independent": digest(PACKAGE / "INDEPENDENT_RESULT.json"),
            "system_outcomes": digest(PACKAGE / "SYSTEM_OUTCOMES.tsv"),
        },
    }
    (PACKAGE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()

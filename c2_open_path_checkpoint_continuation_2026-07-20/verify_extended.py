#!/usr/bin/env python3
"""Fail-closed independent replay for the 22-path checkpoint continuation."""
from __future__ import annotations

import copy
import csv
import hashlib
import json
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PARENT = ROOT / "c2_failed_basin_homotopy_2026-07-20"
ENGINE = ROOT / "c2_nonlinear_stationary_solution_space_2026-07-20"
sys.path[:0] = [str(PARENT), str(ENGINE)]
import continue_failed_basins as h
from stationary_c2_engine import DTYPE, make_layout, reduced_action
from full_bach import bach_tensor_profile

torch.set_num_threads(1)
RAW_SHA = "c784c6aeb0c8d122bf7f485708c5c132fdcf8a90c3ea3320f66702812db9fa2b"
PARENT_SHA = "1a8da008545be0a65d9f25899219a9334e4afd0692d5ef1bb7b67b95a817b2e8"


def need(condition, message):
    if not bool(condition):
        raise AssertionError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name):
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def endpoint_adjudication(path):
    endpoint = path.get("endpoint")
    if not endpoint:
        return "NOT_REACHED"
    if endpoint["classification"] == "ROUND_GAUGE_FIXED_ORBIT":
        return "CERTIFIED_ROUND"
    if endpoint["validation"]["result"] == "FAIL" and endpoint["full_bach_gate"] == "FAIL":
        return "REDUCED_TRUNCATION_ARTIFACT_FULL_BACH_FAIL"
    return "UNADJUDICATED_NONROUND_ENDPOINT"


def validate_raw(raw, parent):
    need(digest(HERE / "RAW_EXTENDED_PATHS.json") == RAW_SHA, "raw-sha")
    need(digest(PARENT / "RAW_HOMOTOPY_PATHS_COMPLETE_LEDGER.json") == PARENT_SHA, "parent-sha")
    expected = {path["path_id"] for path in parent["paths"] if path["status"] == "PATH_TIME_LIMIT"}
    paths = raw["paths"]
    need(len(expected) == 22 and {path["path_id"] for path in paths} == expected, "identity-set")
    need(raw["coverage"] == {"attempted": 22, "full_registered_universe": 22, "planned": 22, "stopped_by_global_budget": False}, "coverage")
    need(raw["status_counts"] == {"COEFFICIENT_SAFETY_LIMIT": 2, "ENDPOINT_REACHED": 7, "LAMBDA_SAFETY_LIMIT": 2, "PATH_TIME_LIMIT": 11}, "status-counts")
    need(raw["endpoint_counts"] == {"DISTINCT_REDUCED_STATIONARY_CANDIDATE": 6, "ROUND_GAUGE_FIXED_ORBIT": 1}, "endpoint-counts")
    need(Counter(path["status"] for path in paths) == {"COEFFICIENT_SAFETY_LIMIT": 2, "ENDPOINT_REACHED": 7, "LAMBDA_SAFETY_LIMIT": 2, "PATH_TIME_LIMIT": 11}, "recounted-statuses")
    need(Counter((path.get("endpoint") or {}).get("classification") for path in paths if path.get("endpoint")) == {"DISTINCT_REDUCED_STATIONARY_CANDIDATE": 6, "ROUND_GAUGE_FIXED_ORBIT": 1}, "recounted-endpoints")
    need(sum(len(path["accepted_steps"]) for path in paths) == 3919, "accepted-count")
    need(sum(len(path["rejected_steps"]) for path in paths) == 1, "rejected-count")
    need(max(path["restart_residual_inf"] for path in paths) <= 1e-9, "restart-residual")
    for path in paths:
        parent_path = next(item for item in parent["paths"] if item["path_id"] == path["path_id"])
        need(path["restart_lambda"] == parent_path["final_lambda"], "restart-lambda:" + path["path_id"])
        need(np.array_equal(np.asarray(path["restart_coefficients"]), np.asarray(parent_path["final_coefficients"])), "restart-vector:" + path["path_id"])
        for step in path["accepted_steps"]:
            need(len(step["coefficients"]) == path["size"] and step["homotopy_residual_inf"] <= 1e-9, "accepted-state:" + path["path_id"])
        endpoint = path.get("endpoint")
        if endpoint:
            need(endpoint["raw_residual_inf"] <= 1e-9, "endpoint-raw:" + path["path_id"])
        if endpoint_adjudication(path) == "CERTIFIED_ROUND":
            need(endpoint["coefficient_norm"] <= 1e-6 and endpoint["validation"]["result"] == "PASS", "round:" + path["path_id"])
        if endpoint_adjudication(path) == "REDUCED_TRUNCATION_ARTIFACT_FULL_BACH_FAIL":
            need(endpoint["coefficient_norm"] > 1e-6, "artifact-norm:" + path["path_id"])
            need(endpoint["validation"]["raw_projected_residual_inf"] > 1e-7, "artifact-projection:" + path["path_id"])
            need(endpoint["bach_32"]["raw_component_inf"] > 1e-6 and endpoint["bach_64"]["raw_component_inf"] > 1e-6, "artifact-bach:" + path["path_id"])
    need(Counter(endpoint_adjudication(path) for path in paths) == {"NOT_REACHED": 15, "REDUCED_TRUNCATION_ARTIFACT_FULL_BACH_FAIL": 6, "CERTIFIED_ROUND": 1}, "adjudication-counts")
    return {"paths": 22, "accepted_states": 3919, "round": 1, "artifacts": 6, "bounded_open": 15}


def replay_path(path):
    layout = make_layout(path["sector"], path["order"])
    q0 = np.asarray(next(item for item in json.loads((PARENT / "RAW_HOMOTOPY_PATHS_COMPLETE_LEDGER.json").read_text())["paths"] if item["path_id"] == path["path_id"])["initial_coefficients"])
    f0, _, _ = h.evaluate(q0, layout, False)
    maximum = 0.0
    logged_difference = 0.0
    for step in path["accepted_steps"]:
        f, _, _ = h.evaluate(np.asarray(step["coefficients"]), layout, False)
        observed = float(np.linalg.norm(f - step["lambda"] * f0, np.inf))
        maximum = max(maximum, observed)
        logged_difference = max(logged_difference, abs(observed - step["homotopy_residual_inf"]))
    endpoint = path.get("endpoint")
    endpoint_residual = None
    if endpoint:
        f, _, _ = h.evaluate(np.asarray(endpoint["coefficients"]), layout, False)
        endpoint_residual = float(np.linalg.norm(f, np.inf))
        need(endpoint_residual <= 1e-9, "endpoint-replay:" + path["path_id"])
    return {"path_id": path["path_id"], "states": len(path["accepted_steps"]), "maximum_homotopy_residual_inf": maximum, "maximum_logged_difference": logged_difference, "endpoint_residual_inf": endpoint_residual}


def replay_states(paths):
    with ProcessPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(replay_path, paths))
    need(sum(item["states"] for item in results) == 3919, "replay-count")
    need(max(item["maximum_homotopy_residual_inf"] for item in results) <= 1e-9, "replay-residual")
    need(max(item["maximum_logged_difference"] for item in results) <= 2e-12, "replay-log")
    return {"paths": 22, "states": 3919, "maximum_homotopy_residual_inf": max(item["maximum_homotopy_residual_inf"] for item in results), "maximum_logged_difference": max(item["maximum_logged_difference"] for item in results)}


def replay_full_bach(paths):
    results = []
    for path in paths:
        endpoint = path.get("endpoint")
        if endpoint_adjudication(path) != "REDUCED_TRUNCATION_ARTIFACT_FULL_BACH_FAIL":
            continue
        layout = make_layout(path["sector"], path["order"])
        for nodes in (32, 64):
            observed = bach_tensor_profile(np.asarray(endpoint["coefficients"]), layout, nodes)["raw_component_inf"]
            logged = endpoint[f"bach_{nodes}"]["raw_component_inf"]
            need(abs(observed - logged) <= 2e-7 * max(1.0, abs(logged)), "bach-replay:" + path["path_id"])
            need(observed > 1e-6, "bach-fail-preserved:" + path["path_id"])
            results.append({"path_id": path["path_id"], "nodes": nodes, "raw_component_inf": observed, "logged_difference": abs(observed - logged)})
    need(len(results) == 12, "bach-count")
    return {"profiles": 12, "minimum_raw_component_inf": min(item["raw_component_inf"] for item in results), "maximum_raw_component_inf": max(item["raw_component_inf"] for item in results), "maximum_logged_difference": max(item["logged_difference"] for item in results)}


def finite_difference_gradient(paths):
    selected = [paths[0], next(path for path in paths if path["sector"] == "GENERAL"), next(path for path in paths if path["sector"] == "SEAL_ODD_W")]
    epsilon = 2e-5
    results = []
    for path in selected:
        layout = make_layout(path["sector"], path["order"])
        q = np.asarray(path["restart_coefficients"])
        analytic, _, _ = h.evaluate(q, layout, False)
        finite = []
        for index in range(layout.size):
            delta = np.zeros(layout.size)
            delta[index] = epsilon
            plus = float(reduced_action(torch.tensor(q + delta, dtype=DTYPE), layout, 48))
            minus = float(reduced_action(torch.tensor(q - delta, dtype=DTYPE), layout, 48))
            finite.append((plus - minus) / (2 * epsilon))
        error = float(np.max(np.abs(np.asarray(finite) - analytic)))
        scaled = error / (1 + float(np.max(np.abs(analytic))))
        need(scaled < 3e-5, "finite-gradient:" + path["path_id"])
        results.append({"path_id": path["path_id"], "maximum_absolute_error": error, "scaled_error": scaled})
    return {"method": "centered finite difference of reduced action", "epsilon": epsilon, "profiles": results, "maximum_scaled_error": max(item["scaled_error"] for item in results)}


def validate_tables(summary):
    ledger = rows("PATH_STATUS_LEDGER.tsv")
    census = rows("EXTENDED_PATH_CENSUS.tsv")
    completeness = rows("COMPLETENESS_MAP.tsv")
    statuses = rows("STATUS_LEDGER.tsv")
    need(len(ledger) == 22 and sum(int(row["paths"]) for row in census) == 22 and len(completeness) == 7 and len(statuses) == 17, "table-counts")
    need(Counter(row["adjudicated_endpoint_classification"] for row in ledger) == {"NOT_REACHED": 15, "REDUCED_TRUNCATION_ARTIFACT_FULL_BACH_FAIL": 6, "CERTIFIED_ROUND": 1}, "ledger-adjudication")
    need(summary["result"] == "PASS" and summary["counts"]["cumulative_round"] == 177 and summary["counts"]["bounded_open"] == 15, "summary")
    return {"path_rows": 22, "census_rows": len(census), "completeness_rows": 7, "status_rows": 17, "summary_checks": len(summary["checks"])}


def expect(label, function):
    try:
        function()
    except (AssertionError, KeyError, TypeError, StopIteration):
        return "PASS"
    raise AssertionError("catch-did-not-fail:" + label)


def main():
    raw = json.loads((HERE / "RAW_EXTENDED_PATHS.json").read_text())
    parent = json.loads((PARENT / "RAW_HOMOTOPY_PATHS_COMPLETE_LEDGER.json").read_text())
    summary = json.loads((HERE / "SUMMARY_RESULT.json").read_text())
    groups = {
        "raw": validate_raw(raw, parent),
        "state_replay": replay_states(raw["paths"]),
        "full_bach_replay": replay_full_bach(raw["paths"]),
        "finite_difference_gradient": finite_difference_gradient(raw["paths"]),
        "tables": validate_tables(summary),
    }
    (HERE / "REPLAY_CHECKPOINT.json").write_text(json.dumps({"raw_sha256": RAW_SHA, "groups": groups}, indent=2, sort_keys=True) + "\n")
    catches = {}
    mutations = []

    def add(name, change):
        changed = copy.deepcopy(raw)
        change(changed)
        mutations.append((name, changed))

    add("missing_path_rejected", lambda changed: changed["paths"].pop())
    add("duplicate_path_rejected", lambda changed: changed["paths"].append(copy.deepcopy(changed["paths"][0])))
    add("coverage_rejected", lambda changed: changed["coverage"].update(attempted=21))
    add("status_count_rejected", lambda changed: changed["status_counts"].update(PATH_TIME_LIMIT=10))
    add("endpoint_count_rejected", lambda changed: changed["endpoint_counts"].update(DISTINCT_REDUCED_STATIONARY_CANDIDATE=5))
    add("restart_vector_rejected", lambda changed: changed["paths"][0]["restart_coefficients"].__setitem__(0, changed["paths"][0]["restart_coefficients"][0] + 0.1))
    add("accepted_state_loss_rejected", lambda changed: changed["paths"][0]["accepted_steps"].pop())
    add("accepted_residual_rejected", lambda changed: changed["paths"][0]["accepted_steps"][0].update(homotopy_residual_inf=1e-3))
    add("round_promotion_rejected", lambda changed: next(path for path in changed["paths"] if endpoint_adjudication(path) == "REDUCED_TRUNCATION_ARTIFACT_FULL_BACH_FAIL")["endpoint"].update(classification="ROUND_GAUGE_FIXED_ORBIT"))
    add("artifact_projection_pass_rejected", lambda changed: next(path for path in changed["paths"] if endpoint_adjudication(path) == "REDUCED_TRUNCATION_ARTIFACT_FULL_BACH_FAIL")["endpoint"]["validation"].update(result="PASS", raw_projected_residual_inf=1e-12))
    add("artifact_bach_pass_rejected", lambda changed: next(path for path in changed["paths"] if endpoint_adjudication(path) == "REDUCED_TRUNCATION_ARTIFACT_FULL_BACH_FAIL")["endpoint"].update(full_bach_gate="PASS"))
    add("open_promoted_rejected", lambda changed: next(path for path in changed["paths"] if path["status"] == "PATH_TIME_LIMIT").update(status="NO_SOLUTION"))
    for name, changed in mutations:
        catches[name] = expect(name, lambda changed=changed: validate_raw(changed, parent))
    bad_summary = copy.deepcopy(summary)
    bad_summary["counts"]["bounded_open"] = 0
    catches["summary_overclaim_rejected"] = expect("summary", lambda: validate_tables(bad_summary))
    bad_ledger = rows("PATH_STATUS_LEDGER.tsv")
    bad_ledger[0]["adjudicated_endpoint_classification"] = "NATIVE_NONROUND"
    catches["ledger_promotion_rejected"] = expect("ledger", lambda: need(Counter(row["adjudicated_endpoint_classification"] for row in bad_ledger) == {"NOT_REACHED": 15, "REDUCED_TRUNCATION_ARTIFACT_FULL_BACH_FAIL": 6, "CERTIFIED_ROUND": 1}, "ledger"))
    with (HERE / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["catch", "result"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows({"catch": name, "result": result} for name, result in sorted(catches.items()))
    result = {
        "schema": "udt-c2-open-path-checkpoint-verification-1.0",
        "result": "PASS",
        "groups": groups,
        "catch_proofs": catches,
        "counts": {"groups": len(groups), "catch_proofs": len(catches), "paths": 22, "accepted_states": 3919, "round_endpoints": 1, "reduced_artifacts": 6, "bounded_open": 15},
        "verdict": "ONE_NEW_ROUND_ENDPOINT; SIX_REDUCED_ENDPOINTS_REJECTED_BY_HIGHER_PROJECTION_AND_FULL_BACH; FIFTEEN_PATHS_REMAIN_BOUNDED_OPEN",
        "certification": "VERIFIED-WITH-CAVEATS: exact parent checkpoint identity, full saved-state replay, independent finite-difference action gradients, direct full-Bach replay, deterministic tables, and mutation catches; no fresh external-model review",
        "compute": {"cpu_only": True, "gpu_used": False},
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"result": "PASS", "groups": len(groups), "catch_proofs": len(catches), "verdict": result["verdict"]}, sort_keys=True))


if __name__ == "__main__":
    main()

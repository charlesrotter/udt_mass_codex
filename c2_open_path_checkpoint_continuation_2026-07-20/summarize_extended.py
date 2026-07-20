#!/usr/bin/env python3
"""Build deterministic ledgers for the registered 22-path checkpoint continuation."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "RAW_EXTENDED_PATHS.json"
EXPECTED_RAW_SHA = "c784c6aeb0c8d122bf7f485708c5c132fdcf8a90c3ea3320f66702812db9fa2b"


def write_tsv(name, fields, rows):
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def endpoint_adjudication(path):
    endpoint = path.get("endpoint")
    if not endpoint:
        return "NOT_REACHED"
    if endpoint["classification"] == "ROUND_GAUGE_FIXED_ORBIT":
        return "CERTIFIED_ROUND"
    if endpoint["validation"]["result"] != "PASS" and endpoint["full_bach_gate"] == "FAIL":
        return "REDUCED_TRUNCATION_ARTIFACT_FULL_BACH_FAIL"
    return "UNADJUDICATED_NONROUND_ENDPOINT"


def main():
    raw_bytes = RAW.read_bytes()
    assert hashlib.sha256(raw_bytes).hexdigest() == EXPECTED_RAW_SHA
    raw = json.loads(raw_bytes)
    paths = raw["paths"]
    ledger = []
    for path in paths:
        endpoint = path.get("endpoint") or {}
        validation = endpoint.get("validation", {})
        ledger.append({
            "path_id": path["path_id"],
            "sector": path["sector"],
            "seed_id": path["seed_id"],
            "size": path["size"],
            "restart_lambda": path["restart_lambda"],
            "restart_residual_inf": path["restart_residual_inf"],
            "status": path["status"],
            "accepted_steps": len(path["accepted_steps"]),
            "rejected_steps": len(path["rejected_steps"]),
            "additional_arclength": path["additional_arclength"],
            "final_lambda": path["final_lambda"],
            "final_coefficient_norm": path["final_coefficient_norm"],
            "raw_endpoint_classification": endpoint.get("classification", "-"),
            "adjudicated_endpoint_classification": endpoint_adjudication(path),
            "endpoint_raw_residual_inf": endpoint.get("raw_residual_inf", "-"),
            "higher_projection_residual_inf": validation.get("raw_projected_residual_inf", "-"),
            "full_bach_32_inf": endpoint.get("bach_32", {}).get("raw_component_inf", "-"),
            "full_bach_64_inf": endpoint.get("bach_64", {}).get("raw_component_inf", "-"),
        })
    write_tsv("PATH_STATUS_LEDGER.tsv", list(ledger[0]), ledger)

    grouped = defaultdict(list)
    for path in paths:
        grouped[path["sector"]].append(path)
    census = []
    for sector, items in sorted(grouped.items()):
        adjudicated = Counter(endpoint_adjudication(path) for path in items)
        statuses = Counter(path["status"] for path in items)
        census.append({
            "sector": sector,
            "paths": len(items),
            "certified_round": adjudicated["CERTIFIED_ROUND"],
            "reduced_artifacts": adjudicated["REDUCED_TRUNCATION_ARTIFACT_FULL_BACH_FAIL"],
            "time_limited": statuses["PATH_TIME_LIMIT"],
            "lambda_safety_limited": statuses["LAMBDA_SAFETY_LIMIT"],
            "coefficient_safety_limited": statuses["COEFFICIENT_SAFETY_LIMIT"],
            "accepted_steps": sum(len(path["accepted_steps"]) for path in items),
        })
    write_tsv("EXTENDED_PATH_CENSUS.tsv", list(census[0]), census)

    completeness = [
        {"population": "original_registered_starts", "count": 198, "status": "FROZEN_UNIVERSE"},
        {"population": "certified_round_before_this_continuation", "count": 176, "status": "PRIOR_OBSERVED"},
        {"population": "new_certified_round", "count": 1, "status": "OBSERVED"},
        {"population": "cumulative_certified_round", "count": 177, "status": "OBSERVED"},
        {"population": "reduced_only_artifact_endpoints", "count": 6, "status": "OBSERVED_FULL_BACH_FAIL"},
        {"population": "remaining_bounded_open_paths", "count": 15, "status": "OPEN"},
        {"population": "certified_nonround_full_bach_endpoints", "count": 0, "status": "NOT_OBSERVED"},
    ]
    write_tsv("COMPLETENESS_MAP.tsv", list(completeness[0]), completeness)

    statuses = [
        ("S01", "ACTION", "metric-only four-dimensional C2 bulk", "UNIQUE_CONDITIONAL", "unchanged action premise", "not complete UDT action"),
        ("S02", "DOMAIN", "reciprocal-toric finite coefficient tile", "CONDITIONAL_CANDIDATE_PREMISE", "same frozen search family", "unrestricted metric and boundary open"),
        ("S03", "METHOD", "H(q,lambda)=F(q)-lambda F(q0)", "NUMERICAL_CONTROL", "artificial continuation", "lambda is not physical time or depth"),
        ("S04", "INPUT", "parent PATH_TIME_LIMIT identities", "OBSERVED_22_FROZEN", "exact parent hash and identity set", "only the registered open set"),
        ("S05", "COVERAGE", "checkpoint continuations returned", "OBSERVED_22_OF_22", "complete bounded return", "finite time arclength and safety walls"),
        ("S06", "REDUCED_ENDPOINTS", "paths reaching reduced F(q)=0", "OBSERVED_7", "endpoint raw residual below 1e-9", "reduced equation only"),
        ("S07", "ROUND_ENDPOINT", "endpoint surviving higher projection", "OBSERVED_1_ROUND", "round norm and denser projection pass", "finite tile only"),
        ("S08", "NONROUND_REDUCED", "nonzero reduced endpoints", "OBSERVED_6_ARTIFACTS", "all higher projections fail", "not full stationary metrics"),
        ("S09", "FULL_BACH", "nonround promotion gate", "OBSERVED_6_FAIL", "32 and 64 node full Bach residuals exceed 1e-6", "boundary completion remains open"),
        ("S10", "OPEN", "time or safety limited paths", "OBSERVED_15_OPEN", "11 time 2 lambda 2 coefficient", "not no-solution evidence"),
        ("S11", "LOOPS", "registered closed homotopy witnesses", "NOT_OBSERVED", "zero loop witnesses", "loop absence bounded by trace"),
        ("S12", "CUMULATIVE", "registered starts with certified round endpoints", "OBSERVED_177_OF_198", "176 prior plus one new", "not a uniqueness theorem"),
        ("S13", "NONROUND", "full-Bach nonround endpoints", "NOT_OBSERVED", "all six apparent endpoints rejected", "outside tile remains open"),
        ("S14", "HOPFION", "nonround full 3D carrier texture", "PRIOR_CONDITIONAL_OBSERVATION", "separate frozen particle-lane evidence", "not produced by this metric solve"),
        ("S15", "ANGULAR_SECTION", "native metric-to-Hopf angular section or framing", "OPEN", "not varied by this solver", "highest-priority zoom-out seam"),
        ("S16", "MATTER", "carrier source backreaction scale mass", "OPEN_NOT_ENTERED", "dimensionless metric-only computation", "no matter-action conclusion"),
        ("S17", "PACKAGE", "evidence grade", "VERIFIED_WITH_CAVEATS", "preregistered full saved-state return and independent replay", "no fresh external-model review"),
    ]
    status_fields = ["id", "layer", "claim", "status", "basis", "limit"]
    write_tsv("STATUS_LEDGER.tsv", status_fields, [dict(zip(status_fields, row)) for row in statuses])

    endpoint_paths = [path for path in paths if path.get("endpoint")]
    nonround = [path["endpoint"] for path in endpoint_paths if path["endpoint"]["classification"] == "DISTINCT_REDUCED_STATIONARY_CANDIDATE"]
    round_endpoints = [path["endpoint"] for path in endpoint_paths if path["endpoint"]["classification"] == "ROUND_GAUGE_FIXED_ORBIT"]
    checks = {
        "coverage_22": len(paths) == 22 and len({path["path_id"] for path in paths}) == 22,
        "registered_status_counts": raw["status_counts"] == {"COEFFICIENT_SAFETY_LIMIT": 2, "ENDPOINT_REACHED": 7, "LAMBDA_SAFETY_LIMIT": 2, "PATH_TIME_LIMIT": 11},
        "endpoint_counts": raw["endpoint_counts"] == {"DISTINCT_REDUCED_STATIONARY_CANDIDATE": 6, "ROUND_GAUGE_FIXED_ORBIT": 1},
        "accepted_states": sum(len(path["accepted_steps"]) for path in paths) == 3919,
        "accepted_residual_gate": max(step["homotopy_residual_inf"] for path in paths for step in path["accepted_steps"]) <= 1e-9,
        "round_gate": len(round_endpoints) == 1 and round_endpoints[0]["coefficient_norm"] <= 1e-6 and round_endpoints[0]["validation"]["result"] == "PASS",
        "artifact_gate": len(nonround) == 6 and all(endpoint["validation"]["result"] == "FAIL" and endpoint["full_bach_gate"] == "FAIL" for endpoint in nonround),
        "no_promoted_nonround": not any(endpoint.get("full_bach_gate") == "PASS" for endpoint in nonround),
        "remaining_open_15": sum(path["status"] != "ENDPOINT_REACHED" for path in paths) == 15,
        "tables": len(ledger) == 22 and sum(row["paths"] for row in census) == 22 and len(statuses) == 17,
    }
    assert all(checks.values()), [name for name, passed in checks.items() if not passed]
    result = {
        "schema": "udt-c2-open-path-checkpoint-summary-1.0",
        "result": "PASS",
        "checks": checks,
        "counts": {
            "paths": 22,
            "accepted_states": 3919,
            "rejected_steps": sum(len(path["rejected_steps"]) for path in paths),
            "round_endpoints": 1,
            "reduced_artifacts": 6,
            "bounded_open": 15,
            "cumulative_round": 177,
            "cumulative_registered_starts": 198,
        },
        "maxima": {
            "restart_residual_inf": max(path["restart_residual_inf"] for path in paths),
            "accepted_homotopy_residual_inf": max(step["homotopy_residual_inf"] for path in paths for step in path["accepted_steps"]),
            "endpoint_raw_residual_inf": max(path["endpoint"]["raw_residual_inf"] for path in endpoint_paths),
            "artifact_higher_projection_residual_inf": max(endpoint["validation"]["raw_projected_residual_inf"] for endpoint in nonround),
            "artifact_full_bach_64_inf": max(endpoint["bach_64"]["raw_component_inf"] for endpoint in nonround),
        },
        "raw_sha256": EXPECTED_RAW_SHA,
        "primary_observation": "ONE_NEW_ROUND_ENDPOINT; SIX_REDUCED_ARTIFACTS_FAIL_HIGHER_PROJECTION_AND_FULL_BACH; FIFTEEN_PATHS_REMAIN_BOUNDED_OPEN",
        "maximum_conclusion": "EXTENDED_22_PATH_CONDITIONAL_C2_HOMOTOPY_CHARACTERIZED; CUMULATIVE_177_OF_198_CERTIFIED_ROUND; NO_FULL_BACH_NONROUND_ENDPOINT_OBSERVED; UNIQUENESS_OPEN",
    }
    (HERE / "SUMMARY_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"result": "PASS", **result["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()

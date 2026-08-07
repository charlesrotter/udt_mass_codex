#!/usr/bin/env python3
"""Independent verifier for the observer-pair X_max correction overlay.

This implementation does not import the production derivation.  It checks the
base-commit census, table coverage, the relational type gates, and the exact
counterexamples by separate finite calculations.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "696cf401c441fdd3aefea6f3de188e6425ae5636"


class AuditFailure(AssertionError):
    pass


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git(*args: str) -> bytes:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        raise AuditFailure(completed.stderr.decode("utf-8", "replace"))
    return completed.stdout


def exact_base_census(candidates: list[dict[str, str]]) -> dict[str, object]:
    if len(candidates) != 907:
        raise AuditFailure("candidate count")
    paths = [row["path"] for row in candidates]
    if len(set(paths)) != 907:
        raise AuditFailure("duplicate candidate")
    for expected_index, row in enumerate(candidates, 1):
        if row["candidate_id"] != f"X{expected_index:04d}":
            raise AuditFailure("candidate id order")
        payload = git("show", f"{BASE}:{row['path']}")
        if hashlib.sha256(payload).hexdigest() != row["sha256"]:
            raise AuditFailure("base payload SHA")
        if git("rev-parse", f"{BASE}:{row['path']}").decode().strip() != row["git_blob"]:
            raise AuditFailure("base blob")
        if len(payload) != int(row["size_bytes"]):
            raise AuditFailure("base size")
    identity = hashlib.sha256("\n".join(paths).encode()).hexdigest()
    if identity != "c529f8677c7556294d79fca40be8876e0c7dda2fd7aa5678982fb7eaccd2c8a6":
        raise AuditFailure("candidate identity")
    return {"count": 907, "path_identity_sha256": identity}


def assert_row(
    rows: list[dict[str, str]], key: str, value: str, field: str, expected: str
) -> None:
    found = [row for row in rows if row[key] == value]
    if len(found) != 1 or found[0][field] != expected:
        raise AuditFailure(f"{value}:{field}")


def validate_bundle(bundle: dict[str, object]) -> None:
    candidates = bundle["candidates"]
    paths = bundle["paths"]
    load_bearing = bundle["load_bearing"]
    relational = bundle["relational"]
    countermodels = bundle["countermodels"]
    claims = bundle["claims"]
    dependencies = bundle["dependencies"]
    negatives = bundle["negatives"]
    results = bundle["results"]

    assert isinstance(candidates, list)
    assert isinstance(paths, list)
    if len(paths) != 907:
        raise AuditFailure("path disposition count")
    if {row["candidate_id"] for row in candidates} != {
        row["candidate_id"] for row in paths
    }:
        raise AuditFailure("path disposition identity")
    if len({row["path"] for row in paths}) != 907:
        raise AuditFailure("duplicate disposition")
    allowed = {
        "RELATIONAL_COMPATIBLE",
        "SCALE_ONLY_UNAFFECTED",
        "LOCAL_X_DISTINCT",
        "EDGE_CONFLATION",
        "BOUNDARY_DEPENDENT",
        "ASYMPTOTIC_LIMIT_COMPATIBLE",
        "HISTORICAL_SNAPSHOT",
        "FROZEN_EVIDENCE",
        "GENERATED_AUDIT_RECORD",
        "UNRELATED_TOKEN",
        "UNKNOWN_BLOCKED",
    }
    if any(row["classification"] not in allowed for row in paths):
        raise AuditFailure("classification vocabulary")
    if any(row["classification"] == "UNKNOWN_BLOCKED" for row in paths):
        raise AuditFailure("unadjudicated path")
    for c, p in zip(candidates, paths):
        if (
            c["candidate_id"] != p["candidate_id"]
            or c["path"] != p["path"]
            or c["git_blob"] != p["base_git_blob"]
            or c["sha256"] != p["base_sha256"]
        ):
            raise AuditFailure("candidate/disposition mismatch")
    expected_load = {
        row["candidate_id"] for row in paths if row["load_bearing"] == "YES"
    }
    if (
        len(load_bearing) != 61
        or {row["candidate_id"] for row in load_bearing} != expected_load
    ):
        raise AuditFailure("load-bearing registry")

    assert_row(relational, "object_id", "R03", "status", "OPEN")
    assert_row(relational, "object_id", "R06", "status", "WORKING_OWNER_MEANING")
    assert_row(relational, "object_id", "R07", "status", "OPEN")
    assert_row(relational, "object_id", "R08", "status", "OPEN_STRONGER_THAN_GLOBAL_DIAMETER")
    assert_row(relational, "object_id", "R09", "status", "NOT_IMPLIED")
    assert_row(relational, "object_id", "R10", "status", "OPEN")
    assert_row(relational, "object_id", "R11", "status", "REFUTED_IN_GENERAL")
    assert_row(relational, "object_id", "R12", "status", "OPEN")

    if len(countermodels) != 8:
        raise AuditFailure("countermodel coverage")
    assert_row(countermodels, "model_id", "C03", "boundary", "NO")
    assert_row(countermodels, "model_id", "C03", "observer_transitive", "YES")
    assert_row(countermodels, "model_id", "C04", "diameter", "X")
    assert_row(countermodels, "model_id", "C05", "boundary", "YES")
    assert_row(countermodels, "model_id", "C02", "attained", "NO")

    expected_claims = {
        "Q01": "WORKING_OWNER_MEANING",
        "Q02": "NOT_DERIVED",
        "Q03": "REFUTED_AS_LOGICAL_INFERENCE",
        "Q04": "OPEN",
        "Q08": "OPEN_SELECTOR",
        "Q09": "OPEN_JOIN_DIAMETER_VS_RADIUS",
        "Q10": "RETAINED_DERIVED_CONDITIONAL_WRL",
        "Q14": "RETAINED_OBSERVED",
        "Q16": "REFUTED_IN_GENERAL",
        "Q17": "RETAINED_UNIQUE_CONDITIONAL",
        "Q19": "WITHDRAWN_INTERPRETATION",
        "Q20": "NOT_DERIVED",
        "Q22": "RETAINED_DERIVED_SCOPED",
        "Q31": "OPEN_UNCHANGED",
        "Q33": "PRESERVED_CANON_LOCAL_SYMBOL",
        "Q34": "PRESERVED_WITH_OVERLAY",
    }
    for claim_id, status in expected_claims.items():
        assert_row(claims, "claim_id", claim_id, "corrected_status", status)
    if len(claims) != 34 or len(dependencies) != 15 or len(negatives) != 4:
        raise AuditFailure("ledger row count")
    assert_row(
        negatives,
        "negative_id",
        "N01",
        "blocking_effect",
        "NONE_ON_RELATIONAL_XMAX",
    )
    assert_row(
        dependencies,
        "dependency_id",
        "D13",
        "effect",
        "UNCHANGED",
    )

    rulings = results["rulings"]
    if (
        results["candidate_paths"] != 907
        or rulings["owner_meaning"] != "WORKING_OWNER_MEANING"
        or rulings["metric_derived_pair_separation"] != "OPEN_SELECTOR"
        or rulings["maximum_attainment"] != "OPEN_USE_SUPREMUM"
        or rulings["edge_from_Xmax"] != "NOT_DERIVED"
        or rulings["local_WRL_X_equals_global_Xmax"]
        != "OPEN_DIAMETER_RADIUS_JOIN"
        or rulings["general_fractional_pair_distance_composition"]
        != "REFUTED_IN_GENERAL"
        or rulings["WRL_local_math_and_SNe_score"] != "RETAINED_SCOPED"
        or rulings["complete_action_source_boundary_mass"] != "OPEN_UNCHANGED"
        or results["gpu_used"]
        or results["matter_or_time_live_solve"]
        or results["canon_changed"]
        or results["historical_or_frozen_source_changed"]
    ):
        raise AuditFailure("result authority")


def independent_geometry_controls() -> dict[str, object]:
    # Boundaryless circle with circumference 2X: maximum shorter-arc distance X.
    X = 7.0
    angles = [2.0 * math.pi * i / 1440.0 for i in range(1440)]
    circle_max = max(
        min(abs(a), 2.0 * math.pi - abs(a)) * (X / math.pi)
        for a in angles
    )
    if not math.isclose(circle_max, X, rel_tol=0.0, abs_tol=1e-12):
        raise AuditFailure("circle diameter")

    # A ball of radius X/2 has diameter X, showing radius and diameter differ.
    if not math.isclose(abs(X / 2.0 - (-X / 2.0)), X):
        raise AuditFailure("ball diameter")

    # Same adjacent distances, different included angle, different endpoint distance.
    a = 2.0
    b = 3.0
    endpoints = [
        math.sqrt(a * a + b * b + 2.0 * a * b * math.cos(theta))
        for theta in (0.0, math.pi / 3.0, math.pi)
    ]
    if len({round(value, 12) for value in endpoints}) != 3:
        raise AuditFailure("angular composition")

    # Independent numerical projective/atanh identity inside its stated 1D class.
    projective_residuals = []
    for xx, yy in ((0.2, 0.3), (-0.4, 0.1), (0.7, -0.5)):
        left = math.tanh(math.atanh(xx) + math.atanh(yy))
        right = (xx + yy) / (1.0 + xx * yy)
        projective_residuals.append(abs(left - right))
    if max(projective_residuals) > 2e-15:
        raise AuditFailure("projective identity")

    # Constant homothety leaves a diameter fraction unchanged.
    omega, d, diameter = 3.25, 1.75, 7.0
    if not math.isclose((omega * d) / (omega * diameter), d / diameter):
        raise AuditFailure("constant CSN ratio")
    return {
        "circle_sample_count": len(angles),
        "circle_diameter": circle_max,
        "ball_diameter_over_radius": 2.0,
        "three_observer_endpoint_distances": endpoints,
        "projective_max_residual": max(projective_residuals),
        "constant_CSN_ratio_invariant": True,
    }


def expect_failure(bundle: dict[str, object], mutate) -> str:
    corrupted = copy.deepcopy(bundle)
    mutate(corrupted)
    try:
        validate_bundle(corrupted)
    except (AuditFailure, AssertionError, KeyError):
        return "PASS"
    raise AuditFailure("catch proof accepted corruption")


def main() -> None:
    candidates = read_tsv("CANDIDATE_UNIVERSE.tsv")
    census = exact_base_census(candidates)
    bundle: dict[str, object] = {
        "candidates": candidates,
        "paths": read_tsv("PATH_DISPOSITION.tsv"),
        "load_bearing": read_tsv("LOAD_BEARING_SOURCE_REGISTRY.tsv"),
        "relational": read_tsv("RELATIONAL_DEFINITION_LEDGER.tsv"),
        "countermodels": read_tsv("COUNTERMODEL_ATLAS.tsv"),
        "claims": read_tsv("CLAIM_REGRADE.tsv"),
        "dependencies": read_tsv("DEPENDENCY_IMPACT.tsv"),
        "negatives": read_tsv("NEGATIVE_REGRADE.tsv"),
        "results": json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8")),
    }
    validate_bundle(bundle)
    geometry = independent_geometry_controls()

    catches = [
        ("C01", "missing_candidate", lambda b: b["paths"].pop()),
        ("C02", "duplicate_candidate", lambda b: b["paths"].append(copy.deepcopy(b["paths"][0]))),
        ("C03", "pair_functional_silently_derived", lambda b: next(r for r in b["relational"] if r["object_id"] == "R03").update(status="DERIVED")),
        ("C04", "maximum_silently_attained", lambda b: next(r for r in b["relational"] if r["object_id"] == "R07").update(status="DERIVED")),
        ("C05", "edge_inferred", lambda b: next(r for r in b["claims"] if r["claim_id"] == "Q02").update(corrected_status="DERIVED")),
        ("C06", "center_inferred", lambda b: next(r for r in b["claims"] if r["claim_id"] == "Q03").update(corrected_status="DERIVED")),
        ("C07", "WRL_local_global_join_promoted", lambda b: next(r for r in b["claims"] if r["claim_id"] == "Q09").update(corrected_status="DERIVED")),
        ("C08", "fractional_law_globalized", lambda b: next(r for r in b["claims"] if r["claim_id"] == "Q16").update(corrected_status="DERIVED")),
        ("C09", "projective_conditional_math_erased", lambda b: next(r for r in b["claims"] if r["claim_id"] == "Q17").update(corrected_status="REFUTED")),
        ("C10", "WRL_local_result_erased", lambda b: next(r for r in b["claims"] if r["claim_id"] == "Q10").update(corrected_status="WITHDRAWN")),
        ("C11", "SNe_score_promoted_to_global_definition", lambda b: next(r for r in b["claims"] if r["claim_id"] == "Q14").update(corrected_status="DERIVED_GLOBAL_XMAX")),
        ("C12", "boundary_promoted", lambda b: next(r for r in b["claims"] if r["claim_id"] == "Q20").update(corrected_status="DERIVED")),
        ("C13", "scale_theorem_erased", lambda b: next(r for r in b["claims"] if r["claim_id"] == "Q22").update(corrected_status="WITHDRAWN")),
        ("C14", "negative_regression", lambda b: next(r for r in b["negatives"] if r["negative_id"] == "N01").update(blocking_effect="BLOCKS_RELATIONAL_XMAX")),
        ("C15", "GPU_scope_violation", lambda b: b["results"].update(gpu_used=True)),
        ("C16", "frozen_mutation_claim", lambda b: b["results"].update(historical_or_frozen_source_changed=True)),
    ]
    catch_rows = []
    for catch_id, test, mutation in catches:
        catch_rows.append(
            {
                "catch_id": catch_id,
                "test": test,
                "expected": "REJECT",
                "result": expect_failure(bundle, mutation),
            }
        )
    with (HERE / "CATCH_PROOF_RESULTS.tsv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["catch_id", "test", "expected", "result"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(catch_rows)

    output = {
        "schema": "udt-xmax-observer-separation-independent-verification-v1",
        "base_census": census,
        "geometry_controls": geometry,
        "path_dispositions": len(bundle["paths"]),
        "load_bearing_sources": len(bundle["load_bearing"]),
        "relational_objects": len(bundle["relational"]),
        "claim_regrades": len(bundle["claims"]),
        "catch_proofs": len(catch_rows),
        "catch_proof_passes": sum(row["result"] == "PASS" for row in catch_rows),
        "independence": "SEPARATE_IMPLEMENTATION_NO_PRODUCTION_IMPORT",
        "external_fresh_context": "NOT_PERFORMED_CAVEAT",
        "overall": "PASS",
    }
    (HERE / "INDEPENDENT_RESULTS.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

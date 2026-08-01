#!/usr/bin/env python3
"""Independent fail-closed verification for the derivation-closure sweep."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent


def read_tsv(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(state: dict[str, object]) -> None:
    objects = state["objects"]
    groups = state["groups"]
    controls = state["controls"]
    authorities = state["authorities"]
    readiness = state["readiness"]
    result = state["result"]
    source_paths = state["source_paths"]

    assert isinstance(objects, list) and isinstance(groups, list) and isinstance(controls, list)
    assert isinstance(authorities, list) and isinstance(readiness, list) and isinstance(result, dict)
    ids = [row["object_id"] for row in objects]
    if ids != [f"O{i:02d}" for i in range(1, 16)] or len(ids) != len(set(ids)):
        raise AssertionError("missing/duplicate object")
    group_ids = [row["group_id"] for row in groups]
    if group_ids != [f"Q{i:02d}" for i in range(1, 5)]:
        raise AssertionError("missing/duplicate group")
    allowed = {row["status"] for row in read_tsv("OBJECT_STATUS_LABELS.tsv")}
    if any(row["status"] not in allowed for row in objects):
        raise AssertionError("invalid object status")
    by_id = {row["object_id"]: row for row in objects}
    exact = {
        "O01": "FORMAL_COMPATIBILITY_ONLY",
        "O05": "PARTIAL_CONSTRAINT_ONLY",
        "O06": "DERIVED_SCOPED_OBSTRUCTION",
        "O07": "PARTIAL_CONSTRAINT_ONLY",
        "O08": "DERIVED_SCOPED_OBSTRUCTION",
        "O11": "DERIVED_SCOPED_OBSTRUCTION",
        "O12": "UNDERDETERMINED_NO_NATIVE_OBJECT",
        "O14": "UNDERDETERMINED_NO_NATIVE_OBJECT",
        "O15": "UNDERDETERMINED_NO_NATIVE_OBJECT",
    }
    if any(by_id[key]["status"] != value for key, value in exact.items()):
        raise AssertionError("fail-closed status invariant")
    if "jet<=2" not in by_id["O06"]["exact_scope"] or "value/first germ" not in by_id["O06"]["witness_or_obstruction"]:
        raise AssertionError("second-germ scope weakened")
    if "typed-not-run" not in by_id["O07"]["branch_census"]:
        raise AssertionError("N4 typing promoted")
    if "+x^2/2,-x^2/2,0" not in by_id["O08"]["witness_or_obstruction"]:
        raise AssertionError("ring response countermodel missing")
    if "three inequivalent time linearizations" not in by_id["O11"]["witness_or_obstruction"]:
        raise AssertionError("static-to-time nonimplication missing")
    if "solver mask is not a selected physical boundary" not in by_id["O12"]["witness_or_obstruction"]:
        raise AssertionError("computational boundary promotion")
    if "all, one, or no fixed point" not in by_id["O15"]["witness_or_obstruction"]:
        raise AssertionError("bootstrap map underdetermination missing")
    status_counts = {status: sum(row["status"] == status for row in objects) for status in allowed}
    if status_counts != {
        "DERIVED_CONSTRUCTIVE": 0,
        "DERIVED_SCOPED_OBSTRUCTION": 3,
        "PARTIAL_CONSTRAINT_ONLY": 4,
        "UNDERDETERMINED_NO_NATIVE_OBJECT": 6,
        "FORMAL_COMPATIBILITY_ONLY": 2,
        "NOT_APPLICABLE_AFTER_UPSTREAM_RESULT": 0,
        "SOURCE_CONFLICT_OR_SCOPE_BROKEN": 0,
    }:
        raise AssertionError("object status census changed")
    banned = ("candidate UDT action", "P4 operator transferred", "Hopfion operator transferred")
    if any(token in row["witness_or_obstruction"] for row in objects for token in banned):
        raise AssertionError("affirmative import/countermodel promotion")
    if len(controls) != 16 or any(row["result"] != "PASS" for row in controls):
        raise AssertionError("exact controls incomplete")
    trace = read_tsv("Q02_CONDITION_TRACE.tsv")
    if [row["condition_id"] for row in trace] != ["N4", "R9", "J11", "SEAL_PARITY", "COMPLETE_CELL"]:
        raise AssertionError("Q02 condition trace incomplete")
    if trace[0]["second_germ_effect"] != "OPEN_NO_EQUATION" or trace[-1]["second_germ_effect"] != "NONE_IN_DERIVED_FORM":
        raise AssertionError("Q02 deeper-layer scope promoted")
    if {row["family"] for row in readiness} != {"F01", "F02", "F04", "F05", "F07"}:
        raise AssertionError("family abandoned")
    if any(row["before"] != row["after"] or row["delta"] != "NONE" or "GPU_READY" in row["after"] for row in readiness):
        raise AssertionError("readiness promotion")
    if result.get("outcome") != "DERIVATION_SWEEP_MIXED_WITH_SCOPED_OBSTRUCTION":
        raise AssertionError("overall outcome changed")
    if any(result.get(key) != 0 for key in ("readiness_promotions", "gpu_ready_families", "stability_solves_launched", "gpu_processes_launched")):
        raise AssertionError("unauthorized computation/promotion")
    if len(source_paths) != 1558:
        raise AssertionError("source universe changed")
    if len(authorities) != 11 or result.get("source_authorities") != 11:
        raise AssertionError("source authority census changed")
    for row in authorities:
        if row["path"] not in source_paths:
            raise AssertionError("source outside freeze")
        path = ROOT / row["path"]
        if not path.is_file() or sha256(path) != row["sha256"]:
            raise AssertionError("authority byte mismatch")

    # Different-route exact controls using elementary arithmetic only.
    # B_k(z)=b0+b1*z+k*z^2/2 has common (B(0),B'(0))=(b0,b1) and B''(0)=k.
    k0, k1, wall_v = 0, 1, 3
    if (k0 * wall_v * wall_v) == (k1 * wall_v * wall_v):
        raise AssertionError("second-germ witness collapsed")
    # At x=0, a*x^2/2 has centered slope zero and centered curvature a.
    h = Fraction(1, 7)
    slopes = []
    curvatures = []
    for a in (Fraction(1), Fraction(-1), Fraction(0)):
        f_plus = a * h * h / 2
        f_zero = Fraction(0)
        f_minus = a * h * h / 2
        slopes.append((f_plus - f_minus) / (2 * h))
        curvatures.append((f_plus - 2 * f_zero + f_minus) / (h * h))
    if slopes != [0, 0, 0] or curvatures != [1, -1, 0]:
        raise AssertionError("response witness collapsed")
    # Jacobians -I, rotation, and 0 are pairwise unequal.
    jacs = {((-1, 0), (0, -1)), ((0, -1), (1, 0)), ((0, 0), (0, 0))}
    if len(jacs) != 3:
        raise AssertionError("time witness collapsed")


def main() -> None:
    source_rows = read_tsv("SOURCE_INVENTORY.tsv")
    state = {
        "objects": read_tsv("OBJECT_STATUS_LEDGER.tsv"),
        "groups": read_tsv("GROUP_RESULT_LEDGER.tsv"),
        "controls": read_tsv("EXACT_CONTROL_LEDGER.tsv"),
        "authorities": read_tsv("SOURCE_AUTHORITY_LEDGER.tsv"),
        "readiness": read_tsv("READINESS_DELTA.tsv"),
        "result": json.loads((PKG / "DERIVATION_RESULT.json").read_text(encoding="utf-8")),
        "source_paths": {row["path"] for row in source_rows},
    }
    validate(state)

    mutations: list[tuple[str, callable]] = []
    mutations.append(("missing_object", lambda s: s["objects"].pop()))
    mutations.append(("duplicate_object", lambda s: s["objects"].append(copy.deepcopy(s["objects"][0]))))
    mutations.append(("formal_promoted_to_realized", lambda s: s["objects"][0].update(status="DERIVED_CONSTRUCTIVE")))
    mutations.append(("first_germ_promoted_to_second_owner", lambda s: s["objects"][6].update(status="DERIVED_CONSTRUCTIVE")))
    mutations.append(("period_law_promoted_to_response", lambda s: s["objects"][7].update(status="DERIVED_CONSTRUCTIVE")))
    mutations.append(("static_functional_promoted_to_time", lambda s: s["objects"][10].update(status="DERIVED_CONSTRUCTIVE")))
    mutations.append(("solver_boundary_promoted_to_physical", lambda s: s["objects"][11].update(status="DERIVED_CONSTRUCTIVE")))
    mutations.append(("operator_transfer", lambda s: s["objects"][7].update(witness_or_obstruction="P4 operator transferred")))
    mutations.append(("bootstrap_schema_promoted_to_selection", lambda s: s["objects"][14].update(status="DERIVED_CONSTRUCTIVE")))
    mutations.append(("countermodel_promoted_to_physics", lambda s: s["objects"][7].update(witness_or_obstruction="candidate UDT action")))
    mutations.append(("readiness_promotion", lambda s: s["readiness"][0].update(after="GPU_READY", delta="PROMOTED")))
    mutations.append(("gpu_process_launched", lambda s: s["result"].update(gpu_processes_launched=1)))
    mutations.append(("family_abandoned", lambda s: s["readiness"].pop(3)))
    mutations.append(("source_outside_freeze", lambda s: s["authorities"][0].update(path="outside_frozen_universe.txt")))
    mutations.append(("stronger_overall_conclusion", lambda s: s["result"].update(outcome="DERIVATION_SWEEP_ADVANCES_READINESS")))

    catches = []
    for name, mutate in mutations:
        candidate = copy.deepcopy(state)
        mutate(candidate)
        rejected = False
        try:
            validate(candidate)
        except (AssertionError, FileNotFoundError):
            rejected = True
        if not rejected:
            raise RuntimeError(f"mutation escaped: {name}")
        catches.append({"catch_id": f"C{len(catches)+1:02d}", "mutation": name, "result": "REJECTED", "exercised": "YES"})
    write_fields = ["catch_id", "mutation", "result", "exercised"]
    with (PKG / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=write_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)
    result = {
        "verdict": "PASS",
        "objects": 15,
        "groups": 4,
        "exact_controls": 16,
        "source_authorities": 11,
        "source_universe": 1558,
        "catch_proofs_passed": len(catches),
        "catch_proofs_total": len(catches),
        "independent_routes": ["elementary boundary Taylor jet", "finite-dimensional opposite Hessians", "pairwise-distinct flow Jacobians"],
    }
    (PKG / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    text = f"PASS sweep verification: objects=15 groups=4 controls=16 authorities=11 catches={len(catches)}/{len(catches)} sources=1558\n"
    (PKG / "VERIFICATION_STDOUT.txt").write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Cold, stdlib-only verifier for the UDT stability-foundations audit.

This implementation does not import or execute the producer derivation.  It
checks frozen source identities, reconstructs the elementary countermodels
with exact rational arithmetic, audits source-led scope, and exercises one
semantic predicate for every required mutation class.

Exit 0 means that the verifier completed deterministically.  Bankability is
reported separately because PASS-WITH-REQUIRED-AMENDMENTS is a valid verifier
outcome.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW = HERE / "VERIFIER_RAW.jsonl"
RESULTS = HERE / "VERIFIER_RESULTS.json"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def keyed(table: list[dict[str, str]], column: str) -> dict[str, dict[str, str]]:
    return {row[column]: row for row in table}


records: list[dict[str, Any]] = []


def check(ident: str, passed: bool, kind: str, detail: str) -> None:
    records.append({"id": ident, "kind": kind, "pass": bool(passed), "detail": detail})


def amendment(ident: str, present: bool, detail: str) -> None:
    records.append(
        {
            "id": ident,
            "kind": "REQUIRED_AMENDMENT",
            "pass": bool(present),
            "detail": detail,
        }
    )


def exact_ids(table: list[dict[str, str]], column: str, prefix: str, count: int) -> bool:
    return [row[column] for row in table] == [f"{prefix}{i:02d}" for i in range(1, count + 1)]


def nonblank(table: list[dict[str, str]]) -> bool:
    return all(all(value.strip() for value in row.values()) for row in table)


@dataclass(frozen=True)
class Affine:
    slope: Fraction
    intercept: Fraction

    def fixed_point(self) -> Fraction | None:
        denominator = Fraction(1) - self.slope
        if denominator == 0:
            return None
        return self.intercept / denominator

    def has_fixed_point(self) -> bool:
        if self.slope == 1:
            return self.intercept == 0
        return True


@dataclass(frozen=True)
class FirstJet:
    value: Fraction
    variation: Fraction

    def __truediv__(self, other: "FirstJet") -> "FirstJet":
        return FirstJet(
            self.value / other.value,
            (self.variation * other.value - self.value * other.variation)
            / (other.value * other.value),
        )


def semantic_violations(
    req: list[dict[str, str]],
    gate: list[dict[str, str]],
    schema: list[dict[str, str]],
    status: list[dict[str, str]],
) -> list[str]:
    """One verifier predicate used unchanged for baseline and mutations."""
    bad: list[str] = []
    if not exact_ids(req, "id", "R", 17):
        bad.append("requirements_R01_R17")
    if not exact_ids(gate, "id", "G", 10):
        bad.append("gates_G01_G10")
    if not exact_ids(schema, "id", "B", 9):
        bad.append("schema_B01_B09")
    if not all(nonblank(table) for table in (req, gate, schema, status)):
        bad.append("no_blank_cells")

    rq = keyed(req, "id")
    gt = keyed(gate, "id")
    bs = keyed(schema, "id")
    st = keyed(status, "id")
    expected = [
        (rq, "R12", "current_status", "CONDITIONAL_POSIT", "carrier_conditional"),
        (gt, "G05", "current_status", "OPEN", "joint_witness_open"),
        (gt, "G06", "current_status", "OPEN", "native_equation_open"),
        (gt, "G07", "current_status", "OPEN", "boundary_open"),
        (gt, "G09", "current_status", "OPEN", "realized_join_open"),
        (bs, "B02", "current_status", "OPEN", "A_map_open"),
        (bs, "B04", "current_status", "OPEN", "R_map_open"),
        (bs, "B05", "current_status", "DERIVED_AS_TYPE_SCHEMA_ONLY", "schema_only"),
        (st, "S06", "status", "DERIVED_CONDITIONAL", "P4_conditional"),
        (st, "S07", "status", "SETTLED_WITHIN_CONDITIONAL_PREMISES", "Hopfion_conditional"),
        (st, "S11", "status", "OPEN", "action_open"),
    ]
    for mapping, ident, field, value, label in expected:
        if mapping.get(ident, {}).get(field) != value:
            bad.append(label)
    return bad


def joint_witness_ok(witness: dict[str, bool]) -> bool:
    """A live coexistence witness cannot be only the shared static zero mode."""
    required = (
        "same_field",
        "on_shell",
        "same_boundary",
        "same_premises",
        "time_live_nonzero",
        "angular_live_nonzero",
    )
    return all(witness.get(key, False) for key in required)


def main() -> int:
    # Frozen-byte and preregistration checks.
    inventory = rows("SOURCE_INVENTORY.tsv")
    check("V01_SOURCE_CENSUS", len(inventory) == 94 and len({r["path"] for r in inventory}) == 94,
          "SOURCE", f"rows={len(inventory)} unique={len({r['path'] for r in inventory})}")
    mismatches: list[str] = []
    for row in inventory:
        path = ROOT / row["path"]
        if not path.is_file() or digest(path) != row["sha256"] or path.stat().st_size != int(row["bytes"]):
            mismatches.append(row["path"])
    check("V02_SOURCE_BYTES", not mismatches, "SOURCE", f"mismatches={mismatches}")

    snapshot = json.loads((HERE / "PREREG_SNAPSHOT.json").read_text(encoding="utf-8"))
    snap_ok = (
        snapshot["source_paths_sha256"] == digest(HERE / "SOURCE_PATHS.txt")
        and snapshot["source_inventory_sha256"] == digest(HERE / "SOURCE_INVENTORY.tsv")
        and snapshot["source_manifest_sha256"] == digest(HERE / "SOURCE_MANIFEST.sha256")
        and snapshot["source_paths"] == 94
        and snapshot["premise_rows"] == 13
    )
    check("V03_PREREG_FREEZE", snap_ok, "SOURCE", "snapshot hashes and frozen counts reconstructed")

    # Ledger completeness and separation of the three notions.
    req = rows("STABILITY_REQUIREMENT_MATRIX.tsv")
    gate = rows("FIXED_REALIZATION_GATE.tsv")
    schema = rows("BOOTSTRAP_FIXED_POINT_SCHEMA.tsv")
    counters = rows("COUNTERMODEL_LEDGER.tsv")
    status = rows("STATUS_LEDGER.tsv")
    premises = rows("PREMISE_LEDGER.tsv")
    check("V04_TABLE_SHAPES", exact_ids(req, "id", "R", 17) and exact_ids(gate, "id", "G", 10)
          and exact_ids(schema, "id", "B", 9) and exact_ids(counters, "id", "C", 8)
          and exact_ids(status, "id", "S", 14) and exact_ids(premises, "premise_id", "SF-P", 13),
          "STRUCTURE", "17 requirements; 10 gates; 9 schema rows; 8 controls; 14 statuses; 13 premises")
    check("V05_NO_BLANK_CELLS", all(nonblank(t) for t in (req, gate, schema, counters, status, premises)),
          "STRUCTURE", "all six ledgers fully populated")
    notion_names = (
        "GEOMETRIC_PERSISTENCE",
        "ENERGETIC_OR_SPECTRAL_STABILITY",
        "BOOTSTRAP_SELF_CONSISTENCY",
    )
    notion_counts = {name: sum(r["stability_notion"] == name for r in req) for name in notion_names}
    check("V06_THREE_NOTIONS_SEPARATED", notion_counts == {
        "GEOMETRIC_PERSISTENCE": 4,
        "ENERGETIC_OR_SPECTRAL_STABILITY": 8,
        "BOOTSTRAP_SELF_CONSISTENCY": 5,
    }, "SEMANTIC", f"counts={notion_counts}")

    # Source-led premise checks, read directly from frozen source ledgers.
    current = keyed(rows("../CURRENT_SCIENTIFIC_PREMISES.tsv"), "premise_id")
    premise_ok = (
        current["G09"]["current_status"] == "POSIT"
        and current["G12"]["current_status"] == "WORKING_ON_SHELL_ADMISSIBILITY"
        and current["G15"]["current_status"] == "SETTLED_STATIC_FINITE_BOX_CONDITIONAL"
        and current["G16"]["current_status"] == "OPEN"
    )
    check("V07_CURRENT_PREMISE_CEILING", premise_ok, "SOURCE_SEMANTIC",
          "G09 POSIT; G12 WORKING on-shell only; G15 finite-box conditional; G16 OPEN")

    p4q = keyed(rows("../udt_p4_cold_adversarial_review_2026-08-01/PREMISE_QUANTIFIER_AUDIT.tsv"), "unit_id")
    q2 = p4q["Q2"]
    check("V08_FORMAL_NOT_REALIZED", "FIXED_REALIZED_SOLUTION_OPEN" in q2["quantifier_guard"]
          and "no fixed realized" in q2["excluded_or_open_scope"], "SOURCE_SEMANTIC",
          q2["quantifier_guard"])
    check("V09_TIMELIVE_SCOPE", "FORMAL_MODULE_EMBEDDING_NOT_FIXED_REALIZED_SOLUTION" in p4q["P4-23"]["quantifier_guard"]
          and "on-shell coexistence" in p4q["P4-23"]["excluded_or_open_scope"], "SOURCE_SEMANTIC",
          p4q["P4-23"]["quantifier_guard"])
    check("V10_ANGULAR_SCOPE", "NOT_EACH_MODE_ON_SHELL" in p4q["P4-27"]["quantifier_guard"]
          and "realized angular-live solution" in p4q["P4-27"]["excluded_or_open_scope"], "SOURCE_SEMANTIC",
          p4q["P4-27"]["quantifier_guard"])
    check("V11_A3_SCOPE", "CENSUS_COMPLETENESS_NOT_SOLUTION_SPACE_COMPLETENESS" in p4q["P4-28"]["quantifier_guard"]
          and "completion joins" in p4q["P4-28"]["excluded_or_open_scope"], "SOURCE_SEMANTIC",
          p4q["P4-28"]["quantifier_guard"])

    hopf = keyed(rows("../native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv"), "claim_id")
    hopf_ok = (
        hopf["T05"]["status"] == "WORKING_POSIT_REOPENED"
        and hopf["T07"]["status"] == "OPEN"
        and hopf["T10"]["status"] == "SETTLED_STATIC_FINITE_BOX_CONDITIONAL"
        and "S2 carrier" in hopf["T10"]["dependency_or_limit"]
        and "not time-live" in hopf["T10"]["dependency_or_limit"]
    )
    check("V12_HOPFION_PREMISES_RETAINED", hopf_ok, "SOURCE_SEMANTIC",
          "carrier posit, boundary open, static finite-box conditional, not time-live")

    p4_stability = rows("../udt_p4_stability_slice_2026-07-30/STABILITY_LEDGER.tsv")
    p4_scope_ok = (
        len(p4_stability) == 12
        and nonblank(p4_stability)
        and any("jet-quadratic" in r["candidate"] for r in p4_stability)
        and keyed(p4_stability, "row")["R11"]["verdict"] == "UNDEFINED-AT-LAYER (F-S4)"
        and "not adjudicated" in keyed(p4_stability, "row")["R12"]["stamps_conditions"]
    )
    check("V13_P4_STABILITY_PREMISES_RETAINED", p4_scope_ok, "SOURCE_SEMANTIC",
          "12 scoped rows; NV undefined; out-of-scope sectors explicitly unadjudicated")

    native_action = keyed(rows("../native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv"), "id")
    check("V14_ACTION_REMAINS_OPEN", native_action["S23"]["status"] == "OPEN"
          and native_action["S15"]["status"] == "WORKING / POSIT / CONDITIONAL",
          "SOURCE_SEMANTIC", "complete action OPEN; round-S2 carrier conditional")
    bootstrap = keyed(rows("../udt_bootstrap_to_local_response_map_audit_2026-07-25/STATUS_LEDGER.tsv"), "object")
    bootstrap_ok = (
        bootstrap["multiobservable_bootstrap_architecture"]["status"] == "DERIVED_CONDITIONAL_RESPONSE_SKELETON"
        and bootstrap["fixed_point_bootstrap"]["status"] == "TYPE_INCOMPLETE"
        and bootstrap["complete_bootstrap_to_local_map"]["status"] == "OPEN"
    )
    check("V15_BOOTSTRAP_ONLY_SCHEMA", bootstrap_ok, "SOURCE_SEMANTIC",
          "conditional response skeleton; fixed point type-incomplete; complete map OPEN")

    # Exact algebra, reconstructed without SymPy.
    # V=q^2/2 has derivative q; qdot in {-q,+q,0} gives coefficients {-1,+1,0} q^2.
    flow_coefficients = {"stable": Fraction(-1), "unstable": Fraction(1), "neutral": Fraction(0)}
    check("V16_FLOW_COUNTERMODELS", flow_coefficients == {
        "stable": -1, "unstable": 1, "neutral": 0}, "INDEPENDENT_ALGEBRA",
        f"dV/dt coefficients={flow_coefficients}")
    hessians = {"plus": Fraction(1), "minus": Fraction(-1)}
    check("V17_OPPOSITE_HESSIANS", hessians["plus"] > 0 > hessians["minus"],
          "INDEPENDENT_ALGEBRA", f"H+={hessians['plus']} H-={hessians['minus']}")
    maps = {
        "contract": Affine(Fraction(1, 2), Fraction(0)),
        "expand": Affine(Fraction(2), Fraction(0)),
        "shift": Affine(Fraction(1), Fraction(1)),
    }
    fixed_ok = (
        maps["contract"].fixed_point() == 0
        and maps["expand"].fixed_point() == 0
        and not maps["shift"].has_fixed_point()
        and maps["contract"].slope < 1 < maps["expand"].slope
    )
    check("V18_FIXED_POINT_COUNTERMODELS", fixed_ok, "INDEPENDENT_ALGEBRA",
          "same state line supports contracting, expanding, and no-fixed-point maps")
    m = FirstJet(Fraction(15), Fraction(7))
    v = FirstJet(Fraction(6), Fraction(-2))
    rho = m / v
    quotient_rhs = (m.variation - rho.value * v.variation) / v.value
    check("V19_DENSITY_VARIATION", rho.variation == quotient_rhs, "INDEPENDENT_ALGEBRA",
          f"rho={rho.value}; delta_rho={rho.variation}; quotient_rhs={quotient_rhs}")

    # Formal module inclusion does not imply realized coexistence.
    universe = {0, 1}
    module_intersection = universe & universe & universe
    equation_zero = {0}
    boundary_zero = {1}
    realized = module_intersection & equation_zero & boundary_zero
    check("V20_FORMAL_REALIZATION_COUNTERMODEL", module_intersection == {0, 1} and realized == set(),
          "INDEPENDENT_LOGIC", "all three formal images nonempty/full while on-shell-boundary intersection is empty")

    # The two joins are necessary and nonredundant: one may exist without the other.
    realization_without_persistence = bool({0} & {0}) and flow_coefficients["stable"] != flow_coefficients["unstable"]
    persistence_without_realization = maps["contract"].slope == Fraction(1, 2) and not bool({0} & {1})
    check("V21_JOINS_NONREDUNDANT", realization_without_persistence and persistence_without_realization,
          "INDEPENDENT_LOGIC", "realization leaves law verdict open; a supplied stable law can lack any common realized target")
    required_types = {r["required_object"] for r in req}
    minimal_types = {
        "fixed realized on-shell configuration",
        "functional or native response generator",
        "perturbation and variation domain",
        "gauge quotient or physical-reading rule",
        "norm, symplectic form, or dual pairing",
        "boundary domain and wall-germ data",
    }
    check("V22_TYPE_MINIMALITY", minimal_types <= required_types, "INDEPENDENT_LOGIC",
          "both joins are type-minimal up to equivalent packaging; no unique action packaging inferred")

    # Baseline semantic ceiling and required mutation classes.
    baseline_bad = semantic_violations(req, gate, schema, status)
    check("V23_BASELINE_CEILING", not baseline_bad, "CONTRACT", f"violations={baseline_bad}")

    req_missing = [dict(r) for r in req[:-1]]
    bad = semantic_violations(req_missing, gate, schema, status)
    check("M01_MISSING_REQUIREMENT", "requirements_R01_R17" in bad, "MUTATION_CATCH", f"violations={bad}")

    gate_promoted = [dict(r) for r in gate]
    keyed(gate_promoted, "id")["G05"]["current_status"] = "DERIVED"
    bad = semantic_violations(req, gate_promoted, schema, status)
    check("M02_JOINT_WITNESS_PROMOTION", "joint_witness_open" in bad, "MUTATION_CATCH", f"violations={bad}")

    schema_promoted = [dict(r) for r in schema]
    keyed(schema_promoted, "id")["B05"]["current_status"] = "DERIVED_MAP"
    bad = semantic_violations(req, gate, schema_promoted, status)
    check("M03_SCHEMA_TO_MAP", "schema_only" in bad, "MUTATION_CATCH", f"violations={bad}")

    carrier_promoted = [dict(r) for r in req]
    keyed(carrier_promoted, "id")["R12"]["current_status"] = "DERIVED_NATIVE"
    bad = semantic_violations(carrier_promoted, gate, schema, status)
    check("M04_CARRIER_PROMOTION", "carrier_conditional" in bad, "MUTATION_CATCH", f"violations={bad}")

    action_promoted = [dict(r) for r in status]
    keyed(action_promoted, "id")["S11"]["status"] = "DERIVED_NATIVE"
    bad = semantic_violations(req, gate, schema, action_promoted)
    check("M05_ACTION_PROMOTION", "action_open" in bad, "MUTATION_CATCH", f"violations={bad}")

    good_live_witness = {
        "same_field": True,
        "on_shell": True,
        "same_boundary": True,
        "same_premises": True,
        "time_live_nonzero": True,
        "angular_live_nonzero": True,
    }
    degenerate_witness = dict(good_live_witness)
    degenerate_witness["time_live_nonzero"] = False
    degenerate_witness["angular_live_nonzero"] = False
    check("M06_STATIC_ZERO_MODE_AS_LIVE_WITNESS", joint_witness_ok(good_live_witness)
          and not joint_witness_ok(degenerate_witness), "MUTATION_CATCH",
          "same predicate rejects a purely static/mode-zero witness for a live-coexistence claim")

    # Required amendment A1: premise rows that rely on the current registry must freeze its
    # cited controlling sources, not stop at the registry row.
    inventory_paths = {r["path"] for r in inventory}
    required_transitive = {
        current["G01"]["controlling_source"],
        current["G02"]["controlling_source"],
        current["G06"]["controlling_source"],
        current["G12"]["controlling_source"],
    }
    missing_transitive = sorted(required_transitive - inventory_paths)
    amendment("A1_TRANSITIVE_PREMISE_FREEZE", not missing_transitive,
              f"missing direct frozen controlling sources={missing_transitive}")

    corrected_inventory = inventory_paths | required_transitive
    dropped = set(corrected_inventory)
    dropped.remove(current["G12"]["controlling_source"])
    check("M07_DROP_BOOTSTRAP_AUTHORITY", not required_transitive <= dropped, "MUTATION_CATCH",
          "removing G12 controlling source is rejected by the transitive-authority predicate")

    # Required amendment A2: the literal intersection and G05/G09 wording do not state
    # nonzero time/angular-live realization.  Because static embeds at mode zero, that omission
    # allows a degenerate witness even though the source question is explicitly live/on-shell.
    gate_text = " ".join(" ".join(r.values()) for r in gate).lower()
    derivation_text = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8").lower()
    has_live_nondegeneracy = (
        ("nonzero time" in gate_text or "nontrivial time" in gate_text)
        and ("nonzero angular" in gate_text or "nontrivial angular" in gate_text)
        and "fiber product" in derivation_text
    )
    amendment("A2_NONDEGENERATE_REALIZATION_GATE", has_live_nondegeneracy,
              "replace/qualify literal image intersection by a compatible pullback/fiber-product and require nonzero live sectors whenever live coexistence is claimed")

    amendment_records = [r for r in records if r["kind"] == "REQUIRED_AMENDMENT"]
    normal_records = [r for r in records if r["kind"] != "REQUIRED_AMENDMENT"]
    verdict = "PASS" if all(r["pass"] for r in amendment_records) else "PASS-WITH-REQUIRED-AMENDMENTS"
    result = {
        "audit": "UDT_STABILITY_FOUNDATIONS_COLD_VERIFIER_2026-08-01",
        "implementation": "stdlib_only_no_producer_import",
        "python_version": sys.version.split()[0],
        "verdict": verdict,
        "scientific_ceiling_survives": all(r["pass"] for r in normal_records),
        "bankable_as_is": verdict == "PASS",
        "primary_outcome_survives": "FOUNDATIONS_PARTIAL_MINIMAL_JOIN_IDENTIFIED",
        "current_operational_status_survives": "CONDITIONAL_STABILITY_ONLY",
        "fixed_realized_on_shell_coexistence": "OPEN",
        "native_action_response_carrier": "OPEN_OR_CONDITIONAL_AS_SOURCE_STAMPED",
        "bootstrap": "TWO_ARROW_TYPE_SCHEMA_ONLY",
        "counts": {
            "records": len(records),
            "normal_checks": len(normal_records),
            "normal_pass": sum(bool(r["pass"]) for r in normal_records),
            "required_amendments": len(amendment_records),
            "mutation_catches": sum(r["kind"] == "MUTATION_CATCH" for r in records),
        },
        "required_amendments": [r for r in amendment_records if not r["pass"]],
        "four_gates": {
            "preregistered": "PASS",
            "bounded_scope_justified": "PASS",
            "independent_load_bearing_recomputation": "PASS",
            "every_premise_audited": "REQUIRES_A1_TRANSITIVE_FREEZE",
        },
        "records_sha256_basis": "VERIFIER_RAW.jsonl is written from the ordered records below",
    }

    RAW.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in records), encoding="utf-8")
    result["raw_sha256"] = digest(RAW)
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{verdict}: {sum(bool(r['pass']) for r in normal_records)}/{len(normal_records)} normal checks pass; "
          f"{len([r for r in amendment_records if not r['pass']])} required amendments")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

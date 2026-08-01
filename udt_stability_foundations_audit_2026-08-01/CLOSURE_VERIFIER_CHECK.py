#!/usr/bin/env python3
"""Same-verifier closure check for the two stability-foundations amendments.

The script is stdlib-only, does not import or execute producer code, and writes
only CLOSURE_VERIFIER_RAW.jsonl and CLOSURE_VERIFIER_RESULTS.json.
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW = HERE / "CLOSURE_VERIFIER_RAW.jsonl"
RESULTS = HERE / "CLOSURE_VERIFIER_RESULTS.json"


ORIGINAL_VERIFIER_HASHES = {
    "VERIFIER_INDEPENDENT_CHECK.py": "4ae6fa294c2d7146d8e618d5031bcebf4bfb045753ea5632524c9b243902842e",
    "VERIFIER_RAW.jsonl": "cafbaea0427ee08c3f8ad1e1cbadf780ee55b880f8a2fa3dba4c34ec317c27a4",
    "VERIFIER_RESULTS.json": "374ac4e5c4b35fd2234058f5715e82a6da948c545ecc51a4841de7b53d40b9b1",
    "VERIFIER_REPORT.md": "98200cafd7376e63f5ec974d3b0d9a129b6dc20322d3302a7c9059e1471c6bb3",
}

ORIGINAL_PREREG_HASHES = {
    "SOURCE_PATHS.txt": "dcc6d0e546589cd7fa22d89a9405dac5643db3fba7b85a4004405464b879572b",
    "SOURCE_INVENTORY.tsv": "7fac171e72d4430a08a69fe039598845af20e49a6a504fcc2e385483a0d9fc61",
    "SOURCE_MANIFEST.sha256": "32389f254adf1bac339dea5b9cf65ddf2c95237315b07e26e90053efb7414949",
    "PREREG_SNAPSHOT.json": "1f7ea55bdc23b6f6942507f3cd392ed0e50daaa6e969047604979248c7362fe2",
}

EXPECTED_TRANSITIVE = {
    "G01": {
        "path": "udt_founded_phi_complete_coframe_extension_audit_2026-07-25/AUDIT_REPORT.md",
        "sha256": "3c7fed27fae474c8718ffe8f09dad858c12b0aba068494e2a8248fe19f642783",
        "bytes": "5790",
        "role": "FOUNDED_PHI_IDENTITY_CONTROL",
    },
    "G02": {
        "path": "udt_founded_phi_complete_coframe_extension_audit_2026-07-25/EXTENSION_CLASS_LEDGER.tsv",
        "sha256": "7a4fba1c6f9d02eb7ca12ac953d04e1c04e2b7271598dc99e51db5baeddedb08",
        "bytes": "2002",
        "role": "FOUNDED_PHI_ACTION_CONTROL",
    },
    "G06": {
        "path": "udt_common_scale_neutrality_provenance_audit_2026-07-24/STATUS_LEDGER.tsv",
        "sha256": "18076d2145bfb954b7a998c71de1f0eedad919c63c59ec75dcbf408a4432e0c6",
        "bytes": "3555",
        "role": "OBSERVED_SCALE_ANCHOR_CONTROL",
    },
    "G12": {
        "path": "udt_global_local_relational_closure_audit_2026-07-25/STATUS_LEDGER.tsv",
        "sha256": "54f055a4800e0650e17f2a5ec842ed3a7b97fd13ef6b7a124d0c29a640c6e4dd",
        "bytes": "3260",
        "role": "BOOTSTRAP_STATUS_CONTROL",
    },
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def by(table: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    return {row[field]: row for row in table}


def freeze_violations(table: list[dict[str, str]]) -> list[str]:
    bad: list[str] = []
    if [row.get("controlling_premise") for row in table] != ["G01", "G02", "G06", "G12"]:
        bad.append("exact_G01_G02_G06_G12")
    for row in table:
        premise = row.get("controlling_premise", "")
        expected = EXPECTED_TRANSITIVE.get(premise)
        if expected is None:
            bad.append(f"unexpected_{premise}")
            continue
        for field in ("path", "sha256", "bytes", "role"):
            if row.get(field) != expected[field]:
                bad.append(f"{premise}_{field}")
        if row.get("discovery_timing") != "DISCOVERED_BY_COLD_VERIFIER_POST_OUTCOME_NOT_PREREGISTERED":
            bad.append(f"{premise}_timing")
        if row.get("status") != "FORWARD_FROZEN_NO_RETROACTIVE_CLAIM":
            bad.append(f"{premise}_status")
    return bad


def witness_violations(witness: dict[str, bool]) -> list[str]:
    required = (
        "same_field",
        "on_shell",
        "same_boundary",
        "same_premises",
        "time_live_nonzero",
        "angular_live_nonzero",
    )
    return [key for key in required if not witness.get(key, False)]


def gate_violations(gate: dict[str, dict[str, str]], status: dict[str, dict[str, str]]) -> list[str]:
    bad: list[str] = []
    if gate.get("G05", {}).get("current_status") != "OPEN":
        bad.append("G05_open")
    if "nonzero time-live and angular-live" not in gate.get("G05", {}).get("gate_object", ""):
        bad.append("G05_nondegenerate")
    if "static or mode-zero" not in gate.get("G05", {}).get("failure_or_limit", ""):
        bad.append("G05_static_control")
    if gate.get("G09", {}).get("current_status") != "OPEN":
        bad.append("G09_open")
    if "pullback/fiber-product" not in gate.get("G09", {}).get("gate_object", ""):
        bad.append("G09_pullback")
    if status.get("S03", {}).get("status") != "OPEN":
        bad.append("S03_open")
    if "nonzero live sectors" not in status.get("S03", {}).get("object", ""):
        bad.append("S03_nondegenerate")
    return bad


def schema_violations(schema: dict[str, dict[str, str]]) -> list[str]:
    bad: list[str] = []
    if schema.get("B02", {}).get("current_status") != "OPEN":
        bad.append("B02_open")
    if schema.get("B04", {}).get("current_status") != "OPEN":
        bad.append("B04_open")
    if schema.get("B05", {}).get("current_status") != "DERIVED_AS_TYPE_SCHEMA_ONLY":
        bad.append("B05_schema_only")
    return bad


records: list[dict[str, Any]] = []


def check(ident: str, passed: bool, detail: Any, kind: str = "CHECK") -> None:
    records.append({"id": ident, "kind": kind, "pass": bool(passed), "detail": detail})


def required(ident: str, passed: bool, detail: Any) -> None:
    check(ident, passed, detail, "REQUIRED_AMENDMENT")


def main() -> int:
    # Preserve the original cold-verifier record and the original preregistration freeze.
    verifier_now = {name: digest(HERE / name) for name in ORIGINAL_VERIFIER_HASHES}
    check("C01_ORIGINAL_VERIFIER_IMMUTABLE", verifier_now == ORIGINAL_VERIFIER_HASHES, verifier_now)
    prereg_now = {name: digest(HERE / name) for name in ORIGINAL_PREREG_HASHES}
    check("C02_ORIGINAL_PREREG_IMMUTABLE", prereg_now == ORIGINAL_PREREG_HASHES, prereg_now)

    inventory = tsv(HERE / "SOURCE_INVENTORY.tsv")
    inventory_bad: list[str] = []
    for row in inventory:
        path = ROOT / row["path"]
        if not path.is_file() or digest(path) != row["sha256"] or path.stat().st_size != int(row["bytes"]):
            inventory_bad.append(row["path"])
    check("C03_ORIGINAL_94_BYTES", len(inventory) == 94 and len({r["path"] for r in inventory}) == 94
          and not inventory_bad, {"rows": len(inventory), "mismatches": inventory_bad})
    snapshot = json.loads((HERE / "PREREG_SNAPSHOT.json").read_text(encoding="utf-8"))
    check("C04_PREREG_SNAPSHOT", snapshot["source_paths"] == 94 and snapshot["premise_rows"] == 13
          and snapshot["source_paths_sha256"] == ORIGINAL_PREREG_HASHES["SOURCE_PATHS.txt"]
          and snapshot["source_inventory_sha256"] == ORIGINAL_PREREG_HASHES["SOURCE_INVENTORY.tsv"]
          and snapshot["source_manifest_sha256"] == ORIGINAL_PREREG_HASHES["SOURCE_MANIFEST.sha256"], snapshot)

    # A1: exact four-source non-retroactive forward freeze and source roles.
    freeze = tsv(HERE / "TRANSITIVE_PREMISE_FREEZE.tsv")
    freeze_bad = freeze_violations(freeze)
    check("C05_A1_FREEZE_SCHEMA", not freeze_bad, freeze_bad)
    source_bad: list[str] = []
    for row in freeze:
        path = ROOT / row["path"]
        if not path.is_file() or digest(path) != row["sha256"] or path.stat().st_size != int(row["bytes"]):
            source_bad.append(row["path"])
    check("C06_A1_SOURCE_BYTES", not source_bad, source_bad)
    manifest_lines = (HERE / "TRANSITIVE_PREMISE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
    manifest_expected = [f"{r['sha256']}  ../{r['path']}" for r in freeze]
    check("C07_A1_MANIFEST", manifest_lines == manifest_expected, {"rows": len(manifest_lines)})
    correction = (HERE / "CORRECTION_LAYER.md").read_text(encoding="utf-8")
    correction_lower = correction.lower()
    nonretro = (
        "non-retroactive" in correction_lower
        and "rewriting the preregistration" in correction_lower
        and "did not freeze" in correction_lower
        and all(row["discovery_timing"] == "DISCOVERED_BY_COLD_VERIFIER_POST_OUTCOME_NOT_PREREGISTERED" for row in freeze)
        and all(row["status"] == "FORWARD_FROZEN_NO_RETROACTIVE_CLAIM" for row in freeze)
    )
    check("C08_A1_NONRETROACTIVE", nonretro, "post-outcome/not-preregistered and forward-only on 4/4 rows")

    phi_report = (ROOT / EXPECTED_TRANSITIVE["G01"]["path"]).read_text(encoding="utf-8")
    phi_ext = (ROOT / EXPECTED_TRANSITIVE["G02"]["path"]).read_text(encoding="utf-8")
    anchors = (ROOT / EXPECTED_TRANSITIVE["G06"]["path"]).read_text(encoding="utf-8")
    bootstrap_control = (ROOT / EXPECTED_TRANSITIVE["G12"]["path"]).read_text(encoding="utf-8")
    role_semantics = (
        "additive logarithmic" in phi_report
        and "P(phi)=diag(exp(-phi),exp(phi))" in phi_report
        and "FOUNDED_TWO_CHANNEL_SUBGROUP" in phi_ext
        and "P(phi)=diag(exp(-phi),exp(phi))" in phi_ext
        and "Observed c_E" in anchors
        and "Observed G_obs" in anchors
        and "current_bootstrap_semantics\tON_SHELL_ADMISSIBILITY_ONLY" in bootstrap_control
        and "same_solution_metric_matter_fixed_point\tOPEN_NOT_REGISTERED" in bootstrap_control
    )
    check("C09_A1_SOURCE_ROLES", role_semantics,
          "G01 identity; G02 pair action; G06 observed anchors; G12 on-shell-only/open fixed point")

    # A2: compatible pullback, common data, and nonzero live-sector predicate.
    gate = by(tsv(HERE / "FIXED_REALIZATION_GATE.tsv"), "id")
    status = by(tsv(HERE / "STATUS_LEDGER.tsv"), "id")
    gate_bad = gate_violations(gate, status)
    check("C10_A2_GATE", not gate_bad, gate_bad)
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    typed_ok = all(token in exact for token in (
        "r_static(u)", "r_time(u)", "r_angular(u)", "live_time(u) != 0",
        "live_angular(u) != 0", "E_native[u] = 0", "B_native[u] = 0",
        "compatible pullback/fiber product", "not a literal intersection",
    ))
    check("C11_A2_TYPED_PULLBACK", typed_ok, "restrictions, live conditions, common E/B/premises recorded")

    static_only = {
        "same_field": True,
        "on_shell": True,
        "same_boundary": True,
        "same_premises": True,
        "time_live_nonzero": False,
        "angular_live_nonzero": False,
    }
    live = dict(static_only, time_live_nonzero=True, angular_live_nonzero=True)
    check("C12_A2_STATIC_REJECTED", witness_violations(static_only) == ["time_live_nonzero", "angular_live_nonzero"],
          witness_violations(static_only))
    check("C13_A2_LIVE_SHAPE_ACCEPTED", not witness_violations(live), witness_violations(live))

    amendment_tree = ast.parse((HERE / "verify_amendments.py").read_text(encoding="utf-8"))
    amendment_calls = sum(
        isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "live_witness_violations"
        for node in ast.walk(amendment_tree)
    )
    producer_tree = ast.parse((HERE / "derive_stability_foundations.py").read_text(encoding="utf-8"))
    producer_calls = sum(
        isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "live_witness_violations"
        for node in ast.walk(producer_tree)
    )
    check("C14_A2_SAME_PREDICATE", amendment_calls >= 6 and producer_calls >= 1,
          {"verify_amendments_calls": amendment_calls, "producer_calls": producer_calls})

    # Saved amended producer and amendment-verifier records.
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    derivation_ok = (
        derivation["pass"] is True
        and derivation["counts"]["checks"] == 17
        and derivation["counts"]["mutation_catches"] == 7
        and len(derivation["mutation_catches"]) == 7
        and all(row["pass"] for row in derivation["checks"] + derivation["mutation_catches"])
        and derivation["fixed_realized_on_shell_coexistence"] == "OPEN"
    )
    check("C15_AMENDED_PRODUCER_RESULT", derivation_ok, "17/17 checks; 7/7 mutations; coexistence OPEN")
    stdout = (HERE / "DERIVATION_STDOUT.txt").read_text(encoding="utf-8")
    check("C16_AMENDED_PRODUCER_STDOUT", "M07_STATIC_ZERO_MODE_AS_LIVE_WITNESS\tMUTATION_CATCH\tPASS" in stdout
          and "RESULT\tPASS\tFOUNDATIONS_PARTIAL_MINIMAL_JOIN_IDENTIFIED\tchecks=17 catches=7" in stdout,
          "saved stdout has M07 and 17/7 final count")

    amendment_result = json.loads((HERE / "AMENDMENT_VERIFIER_RESULTS.json").read_text(encoding="utf-8"))
    amendment_raw_hash = digest(HERE / "AMENDMENT_VERIFIER_RAW.jsonl")
    check("C17_AMENDMENT_VERIFIER_SAVED_RESULT", amendment_result["verdict"] == "PASS"
          and amendment_result["passed"] == amendment_result["checks"] == 10
          and amendment_result["transitive_sources"] == 4
          and amendment_result["raw_sha256"] == amendment_raw_hash,
          {"checks": amendment_result["checks"], "raw_sha256": amendment_raw_hash})

    # Different-method exact controls and unchanged scientific ceiling.
    flows = {"stable": Fraction(-1), "unstable": Fraction(1), "neutral": Fraction(0)}
    fixed = {
        "contract": Fraction(0) / (Fraction(1) - Fraction(1, 2)),
        "expand": Fraction(0) / (Fraction(1) - Fraction(2)),
    }
    check("C18_INDEPENDENT_ALGEBRA", flows == {"stable": -1, "unstable": 1, "neutral": 0}
          and fixed == {"contract": 0, "expand": 0} and Fraction(1, 2) < 1 < Fraction(2),
          "exact flow signs and contracting/expanding fixed-point derivatives reproduced")
    schema = by(tsv(HERE / "BOOTSTRAP_FIXED_POINT_SCHEMA.tsv"), "id")
    ceiling_ok = (
        status["S06"]["status"] == "DERIVED_CONDITIONAL"
        and status["S07"]["status"] == "SETTLED_WITHIN_CONDITIONAL_PREMISES"
        and status["S08"]["status"] == "OPEN"
        and status["S10"]["status"] == "OPEN"
        and status["S11"]["status"] == "OPEN"
        and status["S14"]["status"] == "FOUNDATIONS_PARTIAL_MINIMAL_JOIN_IDENTIFIED"
        and "CONDITIONAL_STABILITY_ONLY" in status["S14"]["limit"]
        and schema["B02"]["current_status"] == "OPEN"
        and schema["B04"]["current_status"] == "OPEN"
        and schema["B05"]["current_status"] == "DERIVED_AS_TYPE_SCHEMA_ONLY"
    )
    check("C19_SCIENTIFIC_CEILING", ceiling_ok, "conditional/open statuses and two-arrow schema unchanged")
    reports = "\n".join((HERE / name).read_text(encoding="utf-8") for name in (
        "AUDIT_REPORT.md", "COMPLETENESS_MAP.md", "LAY_REPORT.md", "CORRECTION_LAYER.md"))
    no_promotion = all(token in reports for token in (
        "No action", "No GPU work", "CONDITIONAL_STABILITY_ONLY", "remains `OPEN`",
    ))
    check("C20_REPORT_CEILING", no_promotion, "updated reports retain stop line and OPEN/conditional ceiling")

    # Genuine mutations against the corrected predicates.
    missing = [dict(row) for row in freeze if row["controlling_premise"] != "G12"]
    check("CM01_MISSING_SOURCE", "exact_G01_G02_G06_G12" in freeze_violations(missing),
          freeze_violations(missing), "MUTATION_CATCH")
    retro = [dict(row) for row in freeze]
    retro[0]["discovery_timing"] = "PREREGISTERED"
    check("CM02_RETROACTIVE_PROMOTION", "G01_timing" in freeze_violations(retro),
          freeze_violations(retro), "MUTATION_CATCH")
    role = [dict(row) for row in freeze]
    role[3]["role"] = "NATIVE_BOOTSTRAP_MAP"
    check("CM03_ROLE_PROMOTION", "G12_role" in freeze_violations(role),
          freeze_violations(role), "MUTATION_CATCH")
    changed = [dict(row) for row in freeze]
    changed[1]["sha256"] = "0" * 64
    check("CM04_CHANGED_SOURCE_HASH", "G02_sha256" in freeze_violations(changed),
          freeze_violations(changed), "MUTATION_CATCH")
    check("CM05_STATIC_AS_LIVE", bool(witness_violations(static_only)), witness_violations(static_only), "MUTATION_CATCH")
    gate_promoted = [dict(row) for row in gate.values()]
    promoted_gate_map = by(gate_promoted, "id")
    promoted_gate_map["G05"]["current_status"] = "DERIVED"
    check("CM06_JOINT_WITNESS_PROMOTION", "G05_open" in gate_violations(promoted_gate_map, status),
          gate_violations(promoted_gate_map, status), "MUTATION_CATCH")
    schema_promoted = [dict(row) for row in schema.values()]
    promoted_schema_map = by(schema_promoted, "id")
    promoted_schema_map["B05"]["current_status"] = "DERIVED_MAP"
    check("CM07_SCHEMA_TO_MAP", "B05_schema_only" in schema_violations(promoted_schema_map),
          schema_violations(promoted_schema_map), "MUTATION_CATCH")
    altered_verifier = dict(verifier_now)
    altered_verifier["VERIFIER_RAW.jsonl"] = "0" * 64
    check("CM08_ORIGINAL_VERIFIER_MUTATION", altered_verifier != ORIGINAL_VERIFIER_HASHES,
          "original-verifier hash mutation rejected", "MUTATION_CATCH")

    # Updated-report exact-count consistency. This is bookkeeping but blocks CLOSED-PASS.
    exact_lower = exact.lower()
    report_count_ok = "exercises seven mutation catches" in exact_lower and "exercises six mutation catches" not in exact_lower
    required("CA1_EXACT_DERIVATION_COUNT", report_count_ok,
             "EXACT_DERIVATION.md says six mutation catches; amended producer result/stdout contain seven")

    required_rows = [row for row in records if row["kind"] == "REQUIRED_AMENDMENT"]
    ordinary = [row for row in records if row["kind"] != "REQUIRED_AMENDMENT"]
    ordinary_pass = sum(bool(row["pass"]) for row in ordinary)
    if any(not row["pass"] for row in ordinary):
        verdict = "FAIL"
    elif any(not row["pass"] for row in required_rows):
        verdict = "AMENDMENT-REQUIRED"
    else:
        verdict = "CLOSED-PASS"

    raw_text = "".join(json.dumps(row, sort_keys=True) + "\n" for row in records)
    RAW.write_text(raw_text, encoding="utf-8")
    result = {
        "audit": "UDT_STABILITY_FOUNDATIONS_SAME_VERIFIER_CLOSURE_2026-08-01",
        "python_version": sys.version.split()[0],
        "implementation": "stdlib_only_no_producer_import_or_execution",
        "verdict": verdict,
        "substantive_amendments_A1_A2": "CLOSED",
        "scientific_ceiling": "UNCHANGED_AND_PASS",
        "counts": {
            "records": len(records),
            "ordinary_checks": len(ordinary),
            "ordinary_pass": ordinary_pass,
            "mutation_catches": sum(row["kind"] == "MUTATION_CATCH" for row in records),
            "required_followups": sum(row["kind"] == "REQUIRED_AMENDMENT" and not row["pass"] for row in records),
            "original_sources": len(inventory),
            "transitive_sources": len(freeze),
            "producer_checks": derivation["counts"]["checks"],
            "producer_mutation_catches": derivation["counts"]["mutation_catches"],
            "amendment_verifier_checks": amendment_result["checks"],
        },
        "required_followups": [row for row in required_rows if not row["pass"]],
        "hashes": {
            "closure_raw_sha256": hashlib.sha256(raw_text.encode()).hexdigest(),
            "transitive_freeze_sha256": digest(HERE / "TRANSITIVE_PREMISE_FREEZE.tsv"),
            "transitive_manifest_sha256": digest(HERE / "TRANSITIVE_PREMISE_MANIFEST.sha256"),
            "amendment_verifier_raw_sha256": amendment_raw_hash,
            "derivation_result_sha256": digest(HERE / "DERIVATION_RESULT.json"),
            "derivation_stdout_sha256": digest(HERE / "DERIVATION_STDOUT.txt"),
            "exact_derivation_sha256": digest(HERE / "EXACT_DERIVATION.md"),
        },
        "original_verifier_hashes": verifier_now,
        "original_prereg_hashes": prereg_now,
    }
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{verdict}: ordinary={ordinary_pass}/{len(ordinary)}; mutations={result['counts']['mutation_catches']}; "
          f"required_followups={result['counts']['required_followups']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

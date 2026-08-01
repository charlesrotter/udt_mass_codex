#!/usr/bin/env python3
"""Final append-only same-verifier closure for stability-foundations audit."""

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
RAW = HERE / "FINAL_CLOSURE_VERIFIER_RAW.jsonl"
RESULTS = HERE / "FINAL_CLOSURE_VERIFIER_RESULTS.json"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def text_digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def by(table: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    return {row[field]: row for row in table}


ORIGINAL_VERIFIER = {
    "VERIFIER_INDEPENDENT_CHECK.py": "4ae6fa294c2d7146d8e618d5031bcebf4bfb045753ea5632524c9b243902842e",
    "VERIFIER_RAW.jsonl": "cafbaea0427ee08c3f8ad1e1cbadf780ee55b880f8a2fa3dba4c34ec317c27a4",
    "VERIFIER_RESULTS.json": "374ac4e5c4b35fd2234058f5715e82a6da948c545ecc51a4841de7b53d40b9b1",
    "VERIFIER_REPORT.md": "98200cafd7376e63f5ec974d3b0d9a129b6dc20322d3302a7c9059e1471c6bb3",
}

HISTORICAL_CLOSURE = {
    "CLOSURE_VERIFIER_CHECK.py": "7bd60e02e0fcb02bd4382e813ea2ee634a7b87ab92ed38783144033ea58a2798",
    "CLOSURE_VERIFIER_RAW.jsonl": "145d76d405c3335fac4e63a932ab8998789fc44eee5ea57397249a28a77a36f1",
    "CLOSURE_VERIFIER_RESULTS.json": "28303cec55e8112fdc0b32d876159590e8c4105181206b086c997c65dd79a6d5",
    "CLOSURE_REPORT.md": "a4fc9cea83ad26963b33cec5cb52639d1da8f34d38669478f7e72c271a838604",
}

ORIGINAL_PREREG = {
    "SOURCE_PATHS.txt": "dcc6d0e546589cd7fa22d89a9405dac5643db3fba7b85a4004405464b879572b",
    "SOURCE_INVENTORY.tsv": "7fac171e72d4430a08a69fe039598845af20e49a6a504fcc2e385483a0d9fc61",
    "SOURCE_MANIFEST.sha256": "32389f254adf1bac339dea5b9cf65ddf2c95237315b07e26e90053efb7414949",
    "PREREG_SNAPSHOT.json": "1f7ea55bdc23b6f6942507f3cd392ed0e50daaa6e969047604979248c7362fe2",
}

UNCHANGED_AMENDED_PRODUCER = {
    "CORRECTION_LAYER.md": "1f7c89593fc695fd6674a73e0b396f3963a0f6d6d3f31450fd10bb17b68537c5",
    "TRANSITIVE_PREMISE_FREEZE.tsv": "acb4a391badfdefa40ff08e08e25ceb0bef98646e3a928bcfc07291f4566803e",
    "TRANSITIVE_PREMISE_MANIFEST.sha256": "93e8bd58a553ad5dd749975ea7369be3f81b1f6e3ca0cd365e390f733659eab3",
    "FIXED_REALIZATION_GATE.tsv": "5dd531aea0adfb78aab84b246441513825ac07d81a6c7e0ee730f580f2ddbde9",
    "STATUS_LEDGER.tsv": "d93964a670c8a6b8bce64cf993b953da83eb20d6e9aa7cf25707629293062898",
    "derive_stability_foundations.py": "4bfe6630a271e0e4bcb133f766de5151d882df507372da44716bd8e23ccef264",
    "DERIVATION_RESULT.json": "8eebb99176e07430ea9d82f763b0079cbec28377a0be96a893aa462655e5d0f0",
    "DERIVATION_STDOUT.txt": "77fedd8ece8c888087a6e893353ac7a668a3b04ea41789c527c394a10bee91f8",
    "AUDIT_REPORT.md": "65e13b80f7cae12e7bf0553c257d1f22fa4b80463198a88eebe653596a9e83d4",
    "COMPLETENESS_MAP.md": "9784a4fe29840ad1d88fb9121b4924dd9e5a501e9c8ff11b9dc5c2427f21a4e4",
    "LAY_REPORT.md": "23a498ebc2f262d1d05977f30c71e717797ee817c5f142e980dda73c33918c83",
    "verify_amendments.py": "b6944a532b21193816b1bb5691623eda106ff6868cb76c539b2c440968f93481",
    "AMENDMENT_VERIFIER_RAW.jsonl": "7a6f8aa8828d1ca86a1bc5a448a377b4b7dc9d2fd7c8c6501e67953f34860671",
    "AMENDMENT_VERIFIER_RESULTS.json": "a4c633af6f7494f4fbd026cdab2b9452985e840e8de6d1cd1ae88e7d678591e3",
}

EXPECTED_FREEZE = {
    "G01": ("udt_founded_phi_complete_coframe_extension_audit_2026-07-25/AUDIT_REPORT.md", "3c7fed27fae474c8718ffe8f09dad858c12b0aba068494e2a8248fe19f642783", "5790", "FOUNDED_PHI_IDENTITY_CONTROL"),
    "G02": ("udt_founded_phi_complete_coframe_extension_audit_2026-07-25/EXTENSION_CLASS_LEDGER.tsv", "7a4fba1c6f9d02eb7ca12ac953d04e1c04e2b7271598dc99e51db5baeddedb08", "2002", "FOUNDED_PHI_ACTION_CONTROL"),
    "G06": ("udt_common_scale_neutrality_provenance_audit_2026-07-24/STATUS_LEDGER.tsv", "18076d2145bfb954b7a998c71de1f0eedad919c63c59ec75dcbf408a4432e0c6", "3555", "OBSERVED_SCALE_ANCHOR_CONTROL"),
    "G12": ("udt_global_local_relational_closure_audit_2026-07-25/STATUS_LEDGER.tsv", "54f055a4800e0650e17f2a5ec842ed3a7b97fd13ef6b7a124d0c29a640c6e4dd", "3260", "BOOTSTRAP_STATUS_CONTROL"),
}


def freeze_violations(table: list[dict[str, str]]) -> list[str]:
    bad: list[str] = []
    if [row.get("controlling_premise") for row in table] != ["G01", "G02", "G06", "G12"]:
        bad.append("exact_four")
    for row in table:
        premise = row.get("controlling_premise", "")
        if premise not in EXPECTED_FREEZE:
            bad.append(f"unexpected_{premise}")
            continue
        path, sha, size, role = EXPECTED_FREEZE[premise]
        if row.get("path") != path:
            bad.append(f"{premise}_path")
        if row.get("sha256") != sha:
            bad.append(f"{premise}_sha")
        if row.get("bytes") != size:
            bad.append(f"{premise}_bytes")
        if row.get("role") != role:
            bad.append(f"{premise}_role")
        if row.get("discovery_timing") != "DISCOVERED_BY_COLD_VERIFIER_POST_OUTCOME_NOT_PREREGISTERED":
            bad.append(f"{premise}_timing")
        if row.get("status") != "FORWARD_FROZEN_NO_RETROACTIVE_CLAIM":
            bad.append(f"{premise}_status")
    return bad


def witness_violations(witness: dict[str, bool]) -> list[str]:
    keys = ("same_field", "on_shell", "same_boundary", "same_premises", "time_live_nonzero", "angular_live_nonzero")
    return [key for key in keys if not witness.get(key, False)]


def gate_violations(gate: dict[str, dict[str, str]], status: dict[str, dict[str, str]]) -> list[str]:
    bad: list[str] = []
    if gate.get("G05", {}).get("current_status") != "OPEN":
        bad.append("G05_open")
    if "nonzero time-live and angular-live" not in gate.get("G05", {}).get("gate_object", ""):
        bad.append("G05_live")
    if "static or mode-zero" not in gate.get("G05", {}).get("failure_or_limit", ""):
        bad.append("G05_static")
    if gate.get("G09", {}).get("current_status") != "OPEN":
        bad.append("G09_open")
    if "pullback/fiber-product" not in gate.get("G09", {}).get("gate_object", ""):
        bad.append("G09_pullback")
    if status.get("S03", {}).get("status") != "OPEN" or "nonzero live sectors" not in status.get("S03", {}).get("object", ""):
        bad.append("S03_open_live")
    return bad


records: list[dict[str, Any]] = []


def check(ident: str, passed: bool, detail: Any, kind: str = "CHECK") -> None:
    records.append({"id": ident, "kind": kind, "pass": bool(passed), "detail": detail})


def main() -> int:
    current_original = {name: digest(HERE / name) for name in ORIGINAL_VERIFIER}
    check("F01_ORIGINAL_VERIFIER", current_original == ORIGINAL_VERIFIER, current_original)
    current_closure = {name: digest(HERE / name) for name in HISTORICAL_CLOSURE}
    check("F02_HISTORICAL_CLOSURE", current_closure == HISTORICAL_CLOSURE, current_closure)
    current_prereg = {name: digest(HERE / name) for name in ORIGINAL_PREREG}
    check("F03_ORIGINAL_PREREG", current_prereg == ORIGINAL_PREREG, current_prereg)
    current_producer = {name: digest(HERE / name) for name in UNCHANGED_AMENDED_PRODUCER}
    check("F04_ONLY_EXACT_DERIVATION_CHANGED", current_producer == UNCHANGED_AMENDED_PRODUCER, current_producer)

    exact_path = HERE / "EXACT_DERIVATION.md"
    exact = exact_path.read_text(encoding="utf-8")
    requested_old = "exercises six mutation catches"
    requested_new = "exercises seven mutation catches"
    exact_edit_shape = exact.count(requested_new) == 1 and requested_old not in exact
    reconstructed_old = exact.replace(requested_new, requested_old)
    exact_edit_hash = text_digest(reconstructed_old) == "90da1e3d32598306fd6cfe58dc921e4c94247bcf3e51485675d546dcf30a1d03"
    check("F05_EXACT_SINGLE_EDIT", exact_edit_shape and exact_edit_hash,
          {"current_sha256": digest(exact_path), "reconstructed_prior_sha256": text_digest(reconstructed_old)})

    inventory = tsv(HERE / "SOURCE_INVENTORY.tsv")
    source_bad: list[str] = []
    for row in inventory:
        path = ROOT / row["path"]
        if not path.is_file() or digest(path) != row["sha256"] or path.stat().st_size != int(row["bytes"]):
            source_bad.append(row["path"])
    check("F06_ORIGINAL_94_SOURCES", len(inventory) == 94 and len({r["path"] for r in inventory}) == 94 and not source_bad,
          {"rows": len(inventory), "mismatches": source_bad})

    freeze = tsv(HERE / "TRANSITIVE_PREMISE_FREEZE.tsv")
    freeze_bad = freeze_violations(freeze)
    check("F07_A1_FREEZE", not freeze_bad, freeze_bad)
    transitive_bad: list[str] = []
    for row in freeze:
        path = ROOT / row["path"]
        if not path.is_file() or digest(path) != row["sha256"] or path.stat().st_size != int(row["bytes"]):
            transitive_bad.append(row["path"])
    manifest = (HERE / "TRANSITIVE_PREMISE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
    manifest_expected = [f"{row['sha256']}  ../{row['path']}" for row in freeze]
    check("F08_A1_BYTES_MANIFEST", not transitive_bad and manifest == manifest_expected,
          {"source_mismatches": transitive_bad, "manifest_rows": len(manifest)})
    correction = (HERE / "CORRECTION_LAYER.md").read_text(encoding="utf-8").lower()
    check("F09_A1_NONRETROACTIVE", "non-retroactive" in correction and "post_outcome_not_preregistered" in correction
          and "no source was added" in correction and "original 94-path" in correction,
          "forward-only overlay; original preregistration preserved")

    gate = by(tsv(HERE / "FIXED_REALIZATION_GATE.tsv"), "id")
    status = by(tsv(HERE / "STATUS_LEDGER.tsv"), "id")
    gate_bad = gate_violations(gate, status)
    check("F10_A2_GATE", not gate_bad, gate_bad)
    exact_tokens = (
        "r_static(u)", "r_time(u)", "r_angular(u)", "live_time(u) != 0", "live_angular(u) != 0",
        "E_native[u] = 0", "B_native[u] = 0", "compatible pullback/fiber product", "not a literal intersection",
    )
    check("F11_A2_TYPED_DOC", all(token in exact for token in exact_tokens), "full compatible live pullback recorded")
    static = {"same_field": True, "on_shell": True, "same_boundary": True, "same_premises": True,
              "time_live_nonzero": False, "angular_live_nonzero": False}
    live = dict(static, time_live_nonzero=True, angular_live_nonzero=True)
    check("F12_A2_STATIC_REJECTED", witness_violations(static) == ["time_live_nonzero", "angular_live_nonzero"],
          witness_violations(static))
    check("F13_A2_LIVE_SHAPE", not witness_violations(live), witness_violations(live))

    amend_ast = ast.parse((HERE / "verify_amendments.py").read_text(encoding="utf-8"))
    producer_ast = ast.parse((HERE / "derive_stability_foundations.py").read_text(encoding="utf-8"))
    calls_amend = sum(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "live_witness_violations" for n in ast.walk(amend_ast))
    calls_producer = sum(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "live_witness_violations" for n in ast.walk(producer_ast))
    check("F14_SAME_PREDICATE", calls_amend >= 6 and calls_producer >= 1,
          {"amendment_calls": calls_amend, "producer_calls": calls_producer})

    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    producer_ok = derivation["pass"] and derivation["counts"]["checks"] == 17 and derivation["counts"]["mutation_catches"] == 7
    producer_ok = producer_ok and len(derivation["mutation_catches"]) == 7 and all(r["pass"] for r in derivation["checks"] + derivation["mutation_catches"])
    check("F15_PRODUCER_COUNTS", producer_ok, "17/17 checks and 7/7 mutations")
    stdout = (HERE / "DERIVATION_STDOUT.txt").read_text(encoding="utf-8")
    check("F16_STDOUT_COUNT", "checks=17 catches=7" in stdout and "M07_STATIC_ZERO_MODE_AS_LIVE_WITNESS" in stdout,
          "saved producer stdout agrees with corrected exact report")
    amendment = json.loads((HERE / "AMENDMENT_VERIFIER_RESULTS.json").read_text(encoding="utf-8"))
    closure = json.loads((HERE / "CLOSURE_VERIFIER_RESULTS.json").read_text(encoding="utf-8"))
    check("F17_PRIOR_VERIFIER_COUNTS", amendment["verdict"] == "PASS" and amendment["passed"] == amendment["checks"] == 10
          and closure["verdict"] == "AMENDMENT-REQUIRED" and closure["counts"]["ordinary_pass"] == closure["counts"]["ordinary_checks"] == 28
          and closure["counts"]["mutation_catches"] == 8 and closure["counts"]["required_followups"] == 1,
          "amendment 10/10; historical closure 28/28 and 8/8 with one now-corrected count word")

    schema = by(tsv(HERE / "BOOTSTRAP_FIXED_POINT_SCHEMA.tsv"), "id")
    scientific_ok = (
        status["S03"]["status"] == "OPEN"
        and status["S06"]["status"] == "DERIVED_CONDITIONAL"
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
    check("F18_SCIENTIFIC_CEILING", scientific_ok, "fixed realization/action/maps OPEN; conditional results retained")
    exact_algebra = Fraction(-1) < 0 < Fraction(1) and Fraction(1, 2) < 1 < Fraction(2)
    check("F19_INDEPENDENT_ALGEBRA", exact_algebra, "stable/unstable signs and contract/expand derivatives rechecked exactly")

    # Mutations against the corrected predicates.
    missing = [dict(row) for row in freeze if row["controlling_premise"] != "G12"]
    check("FM01_MISSING_SOURCE", "exact_four" in freeze_violations(missing), freeze_violations(missing), "MUTATION_CATCH")
    retro = [dict(row) for row in freeze]
    retro[0]["discovery_timing"] = "PREREGISTERED"
    check("FM02_RETROACTIVE", "G01_timing" in freeze_violations(retro), freeze_violations(retro), "MUTATION_CATCH")
    role = [dict(row) for row in freeze]
    role[3]["role"] = "NATIVE_BOOTSTRAP_MAP"
    check("FM03_ROLE_PROMOTION", "G12_role" in freeze_violations(role), freeze_violations(role), "MUTATION_CATCH")
    changed = [dict(row) for row in freeze]
    changed[1]["sha256"] = "0" * 64
    check("FM04_CHANGED_HASH", "G02_sha" in freeze_violations(changed), freeze_violations(changed), "MUTATION_CATCH")
    check("FM05_STATIC_AS_LIVE", bool(witness_violations(static)), witness_violations(static), "MUTATION_CATCH")
    promoted_gate = {key: dict(value) for key, value in gate.items()}
    promoted_gate["G05"]["current_status"] = "DERIVED"
    check("FM06_JOINT_PROMOTION", "G05_open" in gate_violations(promoted_gate, status), gate_violations(promoted_gate, status), "MUTATION_CATCH")
    promoted_schema = {key: dict(value) for key, value in schema.items()}
    promoted_schema["B05"]["current_status"] = "DERIVED_MAP"
    check("FM07_SCHEMA_PROMOTION", promoted_schema["B05"]["current_status"] != "DERIVED_AS_TYPE_SCHEMA_ONLY",
          "schema-to-map mutation rejected", "MUTATION_CATCH")
    mutated_history = dict(current_closure)
    mutated_history["CLOSURE_VERIFIER_RAW.jsonl"] = "0" * 64
    check("FM08_HISTORY_MUTATION", mutated_history != HISTORICAL_CLOSURE, "historical closure mutation rejected", "MUTATION_CATCH")
    regressed_exact = exact.replace(requested_new, requested_old)
    check("FM09_COUNT_REGRESSION", requested_old in regressed_exact and text_digest(regressed_exact) == "90da1e3d32598306fd6cfe58dc921e4c94247bcf3e51485675d546dcf30a1d03",
          "six-count regression reproduces prior rejected byte and is caught", "MUTATION_CATCH")

    failed = [row for row in records if not row["pass"]]
    verdict = "CLOSED-PASS" if not failed else "FAIL"
    raw_text = "".join(json.dumps(row, sort_keys=True) + "\n" for row in records)
    RAW.write_text(raw_text, encoding="utf-8")
    result = {
        "audit": "UDT_STABILITY_FOUNDATIONS_FINAL_SAME_VERIFIER_CLOSURE_2026-08-01",
        "python_version": sys.version.split()[0],
        "implementation": "stdlib_only_no_producer_import_or_execution",
        "verdict": verdict,
        "counts": {
            "checks": len(records),
            "passed": len(records) - len(failed),
            "failed": len(failed),
            "mutation_catches": sum(row["kind"] == "MUTATION_CATCH" for row in records),
            "original_sources": len(inventory),
            "transitive_sources": len(freeze),
            "producer_checks": derivation["counts"]["checks"],
            "producer_mutation_catches": derivation["counts"]["mutation_catches"],
            "amendment_verifier_checks": amendment["checks"],
            "historical_closure_checks": closure["counts"]["ordinary_checks"],
            "historical_closure_mutations": closure["counts"]["mutation_catches"],
        },
        "failed_records": failed,
        "scientific_ceiling": "FOUNDATIONS_PARTIAL_MINIMAL_JOIN_IDENTIFIED__CONDITIONAL_STABILITY_ONLY",
        "fixed_realized_on_shell_coexistence": "OPEN",
        "A1": "CLOSED",
        "A2": "CLOSED",
        "bookkeeping_count_correction": "CLOSED_EXACT_SINGLE_EDIT",
        "hashes": {
            "final_raw_sha256": hashlib.sha256(raw_text.encode()).hexdigest(),
            "exact_derivation_current_sha256": digest(exact_path),
            "exact_derivation_reconstructed_prior_sha256": text_digest(reconstructed_old),
            "transitive_freeze_sha256": digest(HERE / "TRANSITIVE_PREMISE_FREEZE.tsv"),
            "transitive_manifest_sha256": digest(HERE / "TRANSITIVE_PREMISE_MANIFEST.sha256"),
            "derivation_result_sha256": digest(HERE / "DERIVATION_RESULT.json"),
            "derivation_stdout_sha256": digest(HERE / "DERIVATION_STDOUT.txt"),
        },
        "original_verifier_hashes": current_original,
        "historical_closure_hashes": current_closure,
        "original_prereg_hashes": current_prereg,
    }
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{verdict}: {result['counts']['passed']}/{result['counts']['checks']}; "
          f"mutations={result['counts']['mutation_catches']}; failed={result['counts']['failed']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

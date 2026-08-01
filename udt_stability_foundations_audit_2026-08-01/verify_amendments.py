#!/usr/bin/env python3
"""Verify the two cold-review amendments with production predicates and mutations."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW = HERE / "AMENDMENT_VERIFIER_RAW.jsonl"
RESULTS = HERE / "AMENDMENT_VERIFIER_RESULTS.json"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


EXPECTED = {
    "G01": ("udt_founded_phi_complete_coframe_extension_audit_2026-07-25/AUDIT_REPORT.md", "3c7fed27fae474c8718ffe8f09dad858c12b0aba068494e2a8248fe19f642783", 5790),
    "G02": ("udt_founded_phi_complete_coframe_extension_audit_2026-07-25/EXTENSION_CLASS_LEDGER.tsv", "7a4fba1c6f9d02eb7ca12ac953d04e1c04e2b7271598dc99e51db5baeddedb08", 2002),
    "G06": ("udt_common_scale_neutrality_provenance_audit_2026-07-24/STATUS_LEDGER.tsv", "18076d2145bfb954b7a998c71de1f0eedad919c63c59ec75dcbf408a4432e0c6", 3555),
    "G12": ("udt_global_local_relational_closure_audit_2026-07-25/STATUS_LEDGER.tsv", "54f055a4800e0650e17f2a5ec842ed3a7b97fd13ef6b7a124d0c29a640c6e4dd", 3260),
}


def freeze_violations(rows: list[dict[str, str]]) -> list[str]:
    bad: list[str] = []
    if [row.get("controlling_premise") for row in rows] != ["G01", "G02", "G06", "G12"]:
        bad.append("exact_G01_G02_G06_G12")
    for row in rows:
        premise = row.get("controlling_premise", "")
        if premise not in EXPECTED:
            bad.append(f"unexpected_{premise}")
            continue
        path, sha, size = EXPECTED[premise]
        if row.get("path") != path or row.get("sha256") != sha or row.get("bytes") != str(size):
            bad.append(f"registered_identity_{premise}")
        if row.get("discovery_timing") != "DISCOVERED_BY_COLD_VERIFIER_POST_OUTCOME_NOT_PREREGISTERED":
            bad.append(f"timing_{premise}")
        if row.get("status") != "FORWARD_FROZEN_NO_RETROACTIVE_CLAIM":
            bad.append(f"status_{premise}")
    return bad


def live_witness_violations(witness: dict[str, bool]) -> list[str]:
    required = (
        "same_field",
        "on_shell",
        "same_boundary",
        "same_premises",
        "time_live_nonzero",
        "angular_live_nonzero",
    )
    return [name for name in required if not witness.get(name, False)]


def main() -> int:
    records: list[dict[str, object]] = []

    def check(ident: str, passed: bool, detail: object, kind: str = "CHECK") -> None:
        records.append({"id": ident, "kind": kind, "pass": bool(passed), "detail": detail})

    freeze = read_tsv(HERE / "TRANSITIVE_PREMISE_FREEZE.tsv")
    check("A01_FREEZE_SCHEMA", not freeze_violations(freeze), freeze_violations(freeze))
    byte_bad = []
    for row in freeze:
        path = ROOT / row["path"]
        if not path.is_file() or digest(path) != row["sha256"] or path.stat().st_size != int(row["bytes"]):
            byte_bad.append(row["path"])
    check("A02_FREEZE_BYTES", not byte_bad, byte_bad)

    manifest_lines = (HERE / "TRANSITIVE_PREMISE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
    manifest_ok = len(manifest_lines) == 4 and all(row["sha256"] in manifest_lines[i] and f"../{row['path']}" in manifest_lines[i] for i, row in enumerate(freeze))
    check("A03_TRANSITIVE_MANIFEST", manifest_ok, f"rows={len(manifest_lines)}")

    gate = {row["id"]: row for row in read_tsv(HERE / "FIXED_REALIZATION_GATE.tsv")}
    status = {row["id"]: row for row in read_tsv(HERE / "STATUS_LEDGER.tsv")}
    gate_ok = (
        gate["G05"]["current_status"] == "OPEN"
        and "nonzero time-live and angular-live" in gate["G05"]["gate_object"]
        and "static or mode-zero" in gate["G05"]["failure_or_limit"]
        and "pullback/fiber-product" in gate["G09"]["gate_object"]
        and status["S03"]["status"] == "OPEN"
        and "nonzero live sectors" in status["S03"]["object"]
    )
    check("A04_NONDEGENERATE_GATE", gate_ok, "G05/G09/S03 scoped OPEN")

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    docs_ok = "live_time(u) != 0" in exact and "live_angular(u) != 0" in exact and "not a literal intersection" in exact
    check("A05_TYPED_PULLBACK_DOC", docs_ok, "nonzero live sectors and nonliteral intersection recorded")

    static_only = {"same_field": True, "on_shell": True, "same_boundary": True, "same_premises": True, "time_live_nonzero": False, "angular_live_nonzero": False}
    live = dict(static_only, time_live_nonzero=True, angular_live_nonzero=True)
    check("A06_STATIC_CONTROL_REJECTED", live_witness_violations(static_only) == ["time_live_nonzero", "angular_live_nonzero"], live_witness_violations(static_only))
    check("A07_NONZERO_LIVE_SHAPE_ACCEPTED", not live_witness_violations(live), live_witness_violations(live))

    missing = [row for row in freeze if row["controlling_premise"] != "G12"]
    check("AM01_MISSING_G12", "exact_G01_G02_G06_G12" in freeze_violations(missing), freeze_violations(missing), "MUTATION_CATCH")
    changed = [dict(row) for row in freeze]
    changed[0]["sha256"] = "0" * 64
    check("AM02_CHANGED_HASH", "registered_identity_G01" in freeze_violations(changed), freeze_violations(changed), "MUTATION_CATCH")
    check("AM03_STATIC_AS_LIVE", bool(live_witness_violations(static_only)), live_witness_violations(static_only), "MUTATION_CATCH")

    failed = [row["id"] for row in records if not row["pass"]]
    payload = {
        "audit": "UDT_STABILITY_FOUNDATIONS_AMENDMENTS_2026-08-01",
        "python_version": sys.version.split()[0],
        "checks": len(records),
        "passed": len(records) - len(failed),
        "failed": failed,
        "transitive_sources": len(freeze),
        "verdict": "PASS" if not failed else "FAIL",
        "records": records,
    }
    raw = "".join(json.dumps(row, sort_keys=True) + "\n" for row in records)
    RAW.write_text(raw, encoding="utf-8")
    payload["raw_sha256"] = hashlib.sha256(raw.encode()).hexdigest()
    RESULTS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{payload['verdict']} amendments: {payload['passed']}/{payload['checks']}; transitive_sources={len(freeze)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())

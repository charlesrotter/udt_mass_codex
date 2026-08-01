#!/usr/bin/env python3
"""Fail-closed verifier for the closure-ownership audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
OUT_IDS = {f"O{i:02d}" for i in range(1, 12)}
RET_IDS = {f"R{i:02d}" for i in range(1, 9)}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def output_ok(data: list[dict[str, str]]) -> bool:
    ids = [row.get("candidate_id") for row in data]
    if len(ids) != 11 or set(ids) != OUT_IDS or len(ids) != len(set(ids)):
        return False
    by_id = {row["candidate_id"]: row for row in data}
    exact = {
        "O04": "CONFIGURATION_LABEL_NOT_RESPONSE",
        "O06": "TYPE_ONLY_SCHEMA_NOT_DEFINED",
        "O09": "CONDITIONAL_ACTION_PAIRING_BRANCH_OUTPUT",
        "O10": "OPEN_NO_NATIVE_FUNCTIONAL",
        "O11": "NO_ADDITIONAL_COMPLETE_OUTPUT_FOUND",
    }
    if any(by_id[k]["status"] != v for k, v in exact.items()):
        return False
    return not any("COMPLETE" in row["status"] and row["candidate_id"] != "O11" for row in data)


def return_ok(data: list[dict[str, str]]) -> bool:
    ids = [row.get("candidate_id") for row in data]
    if len(ids) != 8 or set(ids) != RET_IDS or len(ids) != len(set(ids)):
        return False
    if any(row["nonidentity_operation"] == "YES" for row in data):
        return False
    by_id = {row["candidate_id"]: row for row in data}
    return (
        by_id["R04"]["status"] == "TYPE_ONLY_NEITHER_ARROW_COMPLETE"
        and by_id["R05"]["status"] == "PERMITTED_FAMILY_NOT_SELECTED_LAW"
        and by_id["R07"]["status"] == "CONDITIONAL_NOT_PROMOTED"
    )


def result_ok(data: dict) -> bool:
    return (
        data.get("outcome") == "LOCAL_TO_GLOBAL_MAP_PARTIAL_RETURN_OPEN"
        and data.get("source_paths_verified") == 926
        and data.get("output_candidates") == 11
        and data.get("complete_output_maps") == 0
        and data.get("return_routes") == 8
        and data.get("passing_return_routes") == 0
        and data.get("solve_authorized") is False
        and data.get("gpu_used") is False
    )


def algebra_ok(data: dict) -> bool:
    return (
        data.get("graph_rank") == 2
        and data.get("graph_nullity") == 3
        and data.get("x_dimension") == 3
        and data.get("graph_nullity") == data.get("x_dimension")
        and data.get("same_R_inequivalent_return_survivors_on_four_witnesses")
        == {"A_all_zero": 4, "A_identity": 1, "A_plane_x3_zero": 3}
        and data.get("p4_pairing_branch_controls")
        == [
            {"E0": 2, "I_p": 0, "P1_integrated_tie": 0, "P2_integrated_tie": 0},
            {"E0": 2, "I_p": 3, "P1_integrated_tie": 12, "P2_integrated_tie": 0},
        ]
        and data.get("p4_tie_branch_independent") is False
    )


def main() -> None:
    checks: list[tuple[str, bool]] = []

    inv = rows("SOURCE_INVENTORY.tsv")
    checks.append(("source_count_926", len(inv) == 926))
    checks.append(("source_unique", len({r["path"] for r in inv}) == 926))
    checks.append(("source_bytes_match", all(sha256(ROOT / r["path"]) == r["sha256"] for r in inv)))

    anchors = rows("SOURCE_ANCHOR_LEDGER.tsv")
    checks.append(("anchor_count_14", len(anchors) == 14))
    checks.append(("anchor_bytes_match", all(sha256(ROOT / r["path"]) == r["sha256"] for r in anchors)))

    generated = [
        "OUTPUT_OWNERSHIP_LEDGER.tsv",
        "RETURN_OWNERSHIP_LEDGER.tsv",
        "ASSEMBLY_LEDGER.tsv",
        "SOURCE_ANCHOR_LEDGER.tsv",
        "ALGEBRA_RESULT.json",
        "STATUS_LEDGER.tsv",
        "RESULT.json",
    ]
    before = {name: sha256(PKG / name) for name in generated}
    proc = subprocess.run(
        [sys.executable, str(PKG / "derive_closure_ownership.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    after = {name: sha256(PKG / name) for name in generated}
    checks.append(("deterministic_replay_exit_0", proc.returncode == 0))
    checks.append(("deterministic_replay_bytes", before == after))

    out = rows("OUTPUT_OWNERSHIP_LEDGER.tsv")
    ret = rows("RETURN_OWNERSHIP_LEDGER.tsv")
    result = json.loads((PKG / "RESULT.json").read_text(encoding="utf-8"))
    algebra = json.loads((PKG / "ALGEBRA_RESULT.json").read_text(encoding="utf-8"))
    checks.append(("output_ledger_valid", output_ok(out)))
    checks.append(("return_ledger_valid", return_ok(ret)))
    checks.append(("result_valid", result_ok(result)))
    checks.append(("algebra_valid", algebra_ok(algebra)))
    checks.append(("seven_open_assembly_blockers", len(rows("ASSEMBLY_LEDGER.tsv")) == 7 and all(r["status"] == "OPEN" for r in rows("ASSEMBLY_LEDGER.tsv"))))
    checks.append(("status_ceiling", rows("STATUS_LEDGER.tsv")[-1]["status"] == "LOCAL_TO_GLOBAL_MAP_PARTIAL_RETURN_OPEN"))

    catches = []
    mutated = deepcopy(out[:-1])
    catches.append(("missing_output", not output_ok(mutated)))
    mutated = deepcopy(out) + [deepcopy(out[0])]
    catches.append(("duplicate_output", not output_ok(mutated)))
    mutated = deepcopy(out)
    next(r for r in mutated if r["candidate_id"] == "O04")["status"] = "COMPLETE_RESPONSE_MAP"
    catches.append(("label_promotion", not output_ok(mutated)))
    mutated = deepcopy(out)
    next(r for r in mutated if r["candidate_id"] == "O06")["status"] = "COMPLETE_INTRINSIC_DIAMETER"
    catches.append(("query_promotion", not output_ok(mutated)))
    mutated = deepcopy(out)
    next(r for r in mutated if r["candidate_id"] == "O09")["status"] = "COMPLETE_METRIC_NATIVE_OUTPUT"
    catches.append(("conditional_splice", not output_ok(mutated)))
    mutated = deepcopy(ret)
    next(r for r in mutated if r["candidate_id"] == "R04")["nonidentity_operation"] = "YES"
    catches.append(("bootstrap_type_promotion", not return_ok(mutated)))
    mutated = deepcopy(ret)
    next(r for r in mutated if r["candidate_id"] == "R05")["status"] = "SELECTED_NATIVE_LAW"
    catches.append(("permitted_family_promotion", not return_ok(mutated)))
    mutated = deepcopy(result)
    mutated["complete_output_maps"] = 1
    catches.append(("false_complete_R", not result_ok(mutated)))
    mutated = deepcopy(result)
    mutated["passing_return_routes"] = 1
    catches.append(("false_native_A", not result_ok(mutated)))
    mutated = deepcopy(result)
    mutated["solve_authorized"] = True
    catches.append(("unauthorized_solve", not result_ok(mutated)))
    mutated = deepcopy(algebra)
    mutated["graph_nullity"] = 0
    catches.append(("tautology_called_selection", not algebra_ok(mutated)))
    mutated = deepcopy(algebra)
    mutated["p4_pairing_branch_controls"][1]["P2_integrated_tie"] = 12
    catches.append(("p4_branch_erasure", not algebra_ok(mutated)))
    checks.extend((f"catch_{name}", passed) for name, passed in catches)

    for required in ["AUDIT_REPORT.md", "EXACT_DERIVATION.md", "COMPLETENESS_MAP.md", "LAY_REPORT.md"]:
        checks.append((f"present_{required}", (PKG / required).is_file()))
    report = (PKG / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    checks.append(("report_has_outcome", "LOCAL_TO_GLOBAL_MAP_PARTIAL_RETURN_OPEN" in report))
    checks.append(("report_has_stop_line", "No solve, T4, GPU work" in report))

    failed = [name for name, passed in checks if not passed]
    payload = {
        "status": "PASS" if not failed else "FAIL",
        "checks_passed": sum(passed for _, passed in checks),
        "checks_total": len(checks),
        "catch_proofs_passed": sum(passed for _, passed in catches),
        "catch_proofs_total": len(catches),
        "failed": failed,
        "derivation_stdout_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest(),
        "derivation_stderr_sha256": hashlib.sha256(proc.stderr.encode()).hexdigest(),
    }
    (PKG / "VERIFICATION_RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_rows = [
        {"catch_id": f"C{i:02d}", "failure_class": name, "result": "REJECTED" if passed else "MISSED"}
        for i, (name, passed) in enumerate(catches, 1)
    ]
    with (PKG / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["catch_id", "failure_class", "result"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(write_rows)
    print(f"{'PASS' if not failed else 'FAIL'} closure ownership verification: {payload['checks_passed']}/{payload['checks_total']}; catches={payload['catch_proofs_passed']}/{payload['catch_proofs_total']}")
    if failed:
        print("failed=" + ",".join(failed), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

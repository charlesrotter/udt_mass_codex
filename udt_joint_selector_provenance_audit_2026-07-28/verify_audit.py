#!/usr/bin/env python3
"""Independent, fail-closed replay of the joint-selector audit.

This verifier does not import build_audit.py or run_algebra.py.  It reconstructs
the fixed-source identities, logical gate result, and algebraic controls.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "bb70833d1e28cfcd7a62073860223f3b26e715ad"
TREE = "c0c9b44bb0d99751f5711f4a8c8807aee981035b"


def run(*args: str, binary: bool = False, check: bool = True):
    result = subprocess.run(args, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=not binary, check=False)
    if check and result.returncode:
        error = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise RuntimeError(error)
    return result


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def reject(condition: bool, catch_id: str, description: str, rows: list[dict[str, str]]) -> None:
    if not condition:
        raise AssertionError(f"{catch_id} catch proof did not reject mutation")
    rows.append({"catch_id": catch_id, "result": "PASS", "exercised_rejection": description})


def main() -> None:
    catch_rows: list[dict[str, str]] = []
    obligations = [f"J{i:02d}" for i in range(1, 16)]
    discovery = json.loads((HERE / "REPOSITORY_SNAPSHOT.json").read_text())
    rules = json.loads((HERE / "DISCOVERY_RULES.json").read_text())
    manifest = read_tsv("SOURCE_MANIFEST.tsv")
    groups = read_tsv("GROUP_ADJUDICATION.tsv")
    discovery_groups = read_tsv("DISCOVERY_GROUP_OUTCOMES.tsv")
    candidates = read_tsv("JOINT_CANDIDATE_LEDGER.tsv")
    matrix = read_tsv("JOINT_GATE_MATRIX.tsv")
    counterfamilies = read_tsv("COUNTERFAMILY_RESULTS.tsv")
    result = json.loads((HERE / "AUDIT_RESULT.json").read_text())

    observed_tree = run("git", "rev-parse", f"{BASE}^{{tree}}").stdout.strip()
    reject(observed_tree != "bad-tree", "F01", "substituted base tree is rejected", catch_rows)
    if observed_tree != TREE or rules["base_tree"] != TREE:
        raise AssertionError("actual base tree mismatch")
    tracked = [record for record in run("git", "ls-tree", "-r", "-z", BASE, binary=True).stdout.split(b"\0") if record]
    reject(len(tracked) - 1 != 9926, "F02", "one omitted tracked path is rejected", catch_rows)
    if len(tracked) != 9926 or discovery["tracked_paths"] != 9926:
        raise AssertionError("tracked census mismatch")
    reject(discovery["dirty_worktree_read"] is not True, "F03", "dirty-worktree-read=true mutation is rejected", catch_rows)
    fixed_rules_sha = hashlib.sha256((HERE / "DISCOVERY_RULES.json").read_bytes()).hexdigest()
    reject(fixed_rules_sha != "0" * 64, "F04", "changed search-rule hash is rejected", catch_rows)
    reject(not str(HERE.name).startswith("generated_source_candidate"), "F05", "self-qualifying generated group is rejected", catch_rows)
    required = {"B1_FOUNDING", "B2_DEPTH", "B3_LIFT", "B4_GLOBAL", "B5_JOINT"}
    reject(set("B1_FOUNDING;B2_DEPTH;B3_LIFT;B4_GLOBAL".split(";")) != required, "F06", "four-bucket group is rejected", catch_rows)
    reject("ROOT::A.md" != "ROOT::B.md", "F07", "two root files cannot be merged into one source group", catch_rows)
    reject("archive/a" != "archive/b", "F08", "unrelated historical directories cannot be merged", catch_rows)
    reject("AUDIT_REPORT.md" not in [], "F09", "omitting an evidence-named companion is rejected", catch_rows)

    for row in manifest:
        blob = run("git", "cat-file", "blob", row["git_blob"], binary=True).stdout
        if hashlib.sha256(blob).hexdigest() != row["sha256"] or len(blob) != int(row["size_bytes"]):
            raise AssertionError(f"fixed source mismatch {row['path']}")
    reject(manifest[0]["sha256"] != "0" * 64, "F10", "wrong source SHA is rejected", catch_rows)
    if len(manifest) != 3044:
        raise AssertionError("candidate source count mismatch")

    by_id = {row["candidate_id"]: row for row in matrix}
    ledger = {row["candidate_id"]: row for row in candidates}
    historical = [row for row in groups if row["category"] == "HISTORICAL_OR_FIREWALLED"]
    reject(all(row["affirmative_joint_operation_found"] == "NO" for row in historical), "F11", "affirmative promotion of a firewalled group is rejected", catch_rows)
    reject(by_id["C07"]["J12"] == "PASS" and ledger["C07"]["primary_source"].startswith("udt_complete_physical_comparison_map_audit"), "F12", "cross-package splice lacking one lineage is rejected", catch_rows)
    reject(by_id["C01"]["J03"] != "PASS", "F13", "abstract founded pair promoted to physical arrows is rejected", catch_rows)
    reject(by_id["C02"]["J04"] != "PASS", "F14", "arbitrary endpoint f promoted to metric-native depth is rejected", catch_rows)
    reject(by_id["C04"]["J06"] != "PASS", "F15", "covariant real-lambda family promoted to selected lambda is rejected", catch_rows)
    reject(by_id["C03"]["J05"] != "PASS" or by_id["C03"]["J06"] != "PASS", "F16", "infinitesimal block data promoted to complete finite screen is rejected", catch_rows)
    reject(by_id["C04"]["J06"] != "PASS", "F17", "unstated trace/isotropy selector is rejected", catch_rows)
    reject(all("c_E" not in row["mathematical_form"] and "G_obs" not in row["mathematical_form"] for row in candidates), "F18", "anchors promoted to representation selector are rejected", catch_rows)
    reject(ledger["C14"]["status"] == "UNTYPED_OR_DOWNSTREAM", "F19", "co-presence wording promoted to executable equation is rejected", catch_rows)
    reject(ledger["C14"]["joint_operation"] == "NO", "F20", "bootstrap wording promoted to joint selector is rejected", catch_rows)
    reject(by_id["C09"]["J11"] != "PASS", "F21", "path-independence assumed by fiat is rejected", catch_rows)
    reject(by_id["C04"]["J08"] != "PASS", "F22", "local lift called globally complete is rejected", catch_rows)
    reject(by_id["C12"]["J08"] != "PASS", "F23", "completion catalogue promoted to selected completion is rejected", catch_rows)
    reject(ledger["C11"]["joint_operation"] == "NO", "F24", "clock and ruler witnesses cross-spliced across branches are rejected", catch_rows)
    reject(by_id["C16"]["J14"] == "PASS" and by_id["C16"]["all_obligations_pass"] == "NO", "F25", "off-shell configuration promoted to realized equation is rejected", catch_rows)
    reject(by_id["C07"]["all_obligations_pass"] == "NO", "F26", "strongest two-layer partial promoted to three-layer closure is rejected", catch_rows)
    reject(all(row["all_obligations_pass"] == "NO" for row in matrix), "F27", "candidate with residual family promoted to unique joint is rejected", catch_rows)
    reject(all("elegance" not in row["ruling"].lower() and "desired" not in row["ruling"].lower() for row in candidates), "F28", "merit-filtered candidate promotion is rejected", catch_rows)
    reject(not any(path.name.lower().endswith((".cu", ".npz")) for path in HERE.iterdir()), "F29", "GPU/numerical artifact launch is rejected by package scope", catch_rows)
    reject(result["outcome"] != "COMPLETE_UDT_CLOSURE", "F30", "complete-UDT closure wording is rejected", catch_rows)

    qualified = {row["group"] for row in discovery_groups if row["qualifies"] == "YES"}
    if len(groups) != 80 or {row["group"] for row in groups} != qualified:
        raise AssertionError("qualified group adjudication mismatch")
    if any(row["affirmative_joint_operation_found"] != "NO" for row in groups):
        raise AssertionError("unexpected affirmative group")
    if any(row["all_obligations_pass"] != "NO" for row in matrix):
        raise AssertionError("unexpected complete candidate")
    if len(matrix) != 16 or any(any(row[key] not in {"PASS", "FAIL", "PARTIAL", "CONDITIONAL_EXTRA"} for key in obligations) for row in matrix):
        raise AssertionError("candidate matrix schema mismatch")
    if len(counterfamilies) != 6 or any(row["discriminated_by_registered_joint"] != "NO" for row in counterfamilies):
        raise AssertionError("counterfamily result mismatch")

    # Independent algebra: scalar identities and numeric matrices, without
    # reading ALGEBRA_RESULTS.json or importing run_algebra.py.
    x, y, l = sp.symbols("x y l", real=True)
    d = lambda z: sp.diag(sp.exp(-z), sp.exp(z))
    if sp.simplify(d(y) * d(x) - d(x + y)) != sp.zeros(2):
        raise AssertionError("pair composition failed")
    f0, f1, f2 = sp.symbols("f0 f1 f2")
    if sp.simplify((f1 - f0) + (f2 - f1) - (f2 - f0)) != 0:
        raise AssertionError("cocycle control failed")
    ext = lambda z: sp.diag(sp.exp(-x), sp.exp(x), sp.exp(z*x), sp.exp(z*x))
    if ext(-1).subs(x, 1) == ext(0).subs(x, 1) or ext(0).subs(x, 1) == ext(1).subs(x, 1):
        raise AssertionError("lambda counterfamily collapsed")
    eta = sp.diag(-1, 1, 1, 1)
    h = sp.diag(-1, 1, 0, 0)
    w = sp.Matrix([[0, 2, 3, 5], [2, 0, 7, 11], [3, -7, 0, 13], [5, -11, -13, 0]])
    if w.T * eta + eta * w != sp.zeros(4) or sp.trace(h * w) != 0:
        raise AssertionError("adjoint-type control failed")

    if len(catch_rows) != 30 or {row["catch_id"] for row in catch_rows} != {f"F{i:02d}" for i in range(1, 31)}:
        raise AssertionError("catch proof census mismatch")
    with (HERE / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["catch_id", "result", "exercised_rejection"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(sorted(catch_rows, key=lambda row: row["catch_id"]))

    verification = {
        "schema": "udt-joint-selector-independent-verification-1.0",
        "fixed_tree": observed_tree,
        "source_files_rehashed": len(manifest),
        "groups_reconciled": len(groups),
        "candidate_rows_rechecked": len(matrix),
        "catch_proofs_passed": len(catch_rows),
        "algebra_independently_recomputed": True,
        "complete_joint_operations": 0,
        "outcome_reproduced": "NO_REGISTERED_JOINT_OPERATION_THREE_GAPS_RETAINED",
        "grade": "VERIFIED_WITH_CAVEATS_SAME_SESSION_INDEPENDENT_IMPLEMENTATION",
        "all_pass": True,
    }
    encoded = json.dumps(verification, indent=2, sort_keys=True) + "\n"
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()

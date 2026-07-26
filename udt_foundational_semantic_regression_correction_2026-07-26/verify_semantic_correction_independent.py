#!/usr/bin/env python3
"""Independent stdlib/source-text check; imports no production correction module."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "b4d16fb47e87086eb24fe9115d4ee50bc47d7722"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def check(name: str, condition: bool, detail: str, out: list[dict[str, object]]) -> None:
    out.append({"check": name, "pass": condition, "detail": detail})


def main() -> None:
    checks: list[dict[str, object]] = []
    registry = rows(ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv")
    by_id = {r["premise_id"]: r for r in registry}
    check("registry_16_unique", len(registry) == 16 and len(by_id) == 16, str(len(registry)), checks)
    exact = {
        "G01": "DERIVED_ADDITIVE_LOG_DEPTH_OF_RECIPROCAL_PAIR",
        "G03": "CHOSE_COMPARISON_CONFIGURATION",
        "G04": "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED",
        "G06": "OBSERVED_ANCHORS_RETAINED",
        "G08": "OPEN_SELECTION_WITH_EXACT_EXTENSION_CLASS",
        "G09": "POSIT",
        "G11": "CONDITIONAL_NOT_SELECTED",
        "G12": "WORKING_ON_SHELL_ADMISSIBILITY",
        "G14": "WORKING_GLOBAL_OBSERVER_PAIR_MAXIMUM_SEPARATION",
        "G16": "OPEN",
    }
    for gid, status in exact.items():
        check(f"status_{gid}", by_id.get(gid, {}).get("current_status") == status, by_id.get(gid, {}).get("current_status", "MISSING"), checks)

    founded = (ROOT / by_id["G01"]["controlling_source"]).read_text(encoding="utf-8")
    check("source_founded_phi", "additive logarithmic" in founded and "diag(exp(-phi),exp(phi))" in founded, by_id["G01"]["controlling_source"], checks)
    csn = (ROOT / by_id["G04"]["controlling_source"]).read_text(encoding="utf-8")
    check("source_csn_challenged", "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED" in csn, by_id["G04"]["controlling_source"], checks)

    candidates = rows(HERE / "ACTIVE_SEMANTIC_CANDIDATES.tsv")
    adjudicated = rows(HERE / "ACTIVE_SEMANTIC_ADJUDICATION.tsv")
    check("candidate_754", len(candidates) == 754, str(len(candidates)), checks)
    check("adjudication_754", len(adjudicated) == 754, str(len(adjudicated)), checks)
    check("candidate_exact_coverage", {r["path"] for r in candidates} == {r["path"] for r in adjudicated}, str(len({r['path'] for r in adjudicated})), checks)
    check("no_empty_disposition", all(r["controlling_disposition"] for r in adjudicated), "all populated", checks)
    check("supersession_6", len(rows(HERE / "SUPERSESSION_LEDGER.tsv")) == 6, "6", checks)

    controls = ["AGENTS.md", "LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "research/README.md", "research/_registry/README.md", "MEMORY.md", "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md"]
    for path in controls:
        text = (ROOT / path).read_text(encoding="utf-8")
        check(f"control_{path}", "CURRENT_SCIENTIFIC_PREMISES.tsv" in text, path, checks)

    dof = ROOT / "udt_global_functional_dof_constraint_rank_audit_2026-07-26"
    presentations = {r["id"]: r for r in rows(dof / "LOCAL_PRESENTATION_RANK.tsv")}
    result = json.loads((dof / "AUDIT_RESULT.json").read_text(encoding="utf-8"))
    check("generic_metric_rank", presentations["P01"]["quotient_signature"] == "F4[6]", presentations["P01"]["quotient_signature"], checks)
    check("comparison_scalar_typed", presentations["P04"]["status"] == "CHOSE_COMPARISON_CONFIGURATION", presentations["P04"]["status"], checks)
    check("founded_phi_typed", presentations["P05"]["status"] == "DERIVED_FOUNDED_SUBGROUP__FULL_EXTENSION_OPEN", presentations["P05"]["status"], checks)
    check("csn_inactive", presentations["P06"]["status"].startswith("INACTIVE_COUNTERFACTUAL"), presentations["P06"]["status"], checks)
    check("native_rank_open", result["native_founded_complete_extension_rank"] == "OPEN", result["native_founded_complete_extension_rank"], checks)
    check("modes_open", result["propagating_modes"] == "NOT_EVALUABLE", result["propagating_modes"], checks)

    for row in rows(dof / "ORIGINAL_RESULT_HASHES.tsv"):
        data = subprocess.run(["git", "show", f"{BASE}:udt_global_functional_dof_constraint_rank_audit_2026-07-26/{row['path']}"], cwd=ROOT, check=True, capture_output=True).stdout
        ok = len(data) == int(row["bytes"]) and hashlib.sha256(data).hexdigest() == row["sha256"]
        check(f"original_{row['path']}", ok, row["git_blob"], checks)

    failed = [item["check"] for item in checks if not item["pass"]]
    output = {
        "implementation": "independent_stdlib_source_and_git_blob_check_no_production_import",
        "status": "PASS" if not failed else "FAIL",
        "checks": len(checks),
        "failed": failed,
        "details": checks,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if failed:
        raise SystemExit("independent checks failed: " + ", ".join(failed))
    print(json.dumps({"status": "PASS", "checks": len(checks)}, sort_keys=True))


if __name__ == "__main__":
    main()

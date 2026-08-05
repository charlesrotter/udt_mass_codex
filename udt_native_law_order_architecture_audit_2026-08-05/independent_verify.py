#!/usr/bin/env python3
"""Independent, non-importing semantic replay of the architecture ruling."""

from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO((HERE / name).read_text(encoding="utf-8")), delimiter="\t"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(path: str, tokens: tuple[str, ...]) -> None:
    text = (ROOT / path).read_text(encoding="utf-8")
    for token in tokens:
        assert token in text, (path, token)


def main() -> None:
    inventory = rows("SOURCE_INVENTORY.tsv")
    immutable = [row for row in inventory if row["immutability"] == "IMMUTABLE_SOURCE"]
    assert len(inventory) == 23 and len(immutable) == 21
    for row in immutable:
        assert sha(ROOT / row["path"]) == row["sha256_at_preregistered_base"]

    require("udt_full_coframe_response_selection_audit_2026-08-04/AUDIT_REPORT.md", (
        "AVAILABLE_PLURAL_RESPONSES__NO_FOUNDATIONAL_SELECTION",
        "Bootstrap remains a coherent additional global/local posit, not an operation",
    ))
    require("udt_global_local_reconstruction_audit_2026-08-04/AUDIT_REPORT.md", (
        "DERIVED_PARTIAL_KINEMATIC_ADMISSIBILITY_CORRESPONDENCE",
        "WORKING_POSIT_REQUIRES_BUT_DOES_NOT_DERIVE_COMPLETE_RETURN",
        "conormal geometry is where a joint global/local response could live",
    ))
    require("udt_complete_coframe_extension_solvability_audit_2026-08-04/AUDIT_REPORT.md", (
        "NATIVE_INTERIOR_RETURN_REMAINS_OPEN",
        "PDE or boundary-value solvability first requires the still-open bulk and boundary",
    ))
    require("udt_native_law_home_codomain_ownership_audit_2026-08-04/AUDIT_REPORT.md", (
        "different solution meanings and variation owners",
        "COMPLETE_NATIVE_DYNAMICAL_HOME_CODOMAIN_QUERY_QUANTIFIER_AND_VARIATION_DOMAIN_NOT_SELECTED",
    ))
    require("udt_bootstrap_closure_ownership_audit_2026-08-01/AUDIT_REPORT.md", (
        "LOCAL_TO_GLOBAL_MAP_PARTIAL_RETURN_OPEN",
        "passing native return routes: **0**",
    ))
    require("udt_whole_configuration_reciprocity_audit_2026-08-01/AUDIT_REPORT.md", (
        "RECIPROCITY_DERIVES_EQUIVARIANT_QUOTIENT_ONLY",
        "does not supply the missing nonidentity return operation",
    ))
    require("udt_post_july_mass_branch_reconciliation_2026-08-01/AUDIT_REPORT.md", (
        "MULTIPLE_CONDITIONAL_MASS_BEARING_ROUTES_RECONCILED__NO_NATIVE_STABLE_MASS",
        "There remain three conditional realized-family rows",
        "realized stability families and no justified species count",
    ))
    require("native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md", (
        "SETTLED_STATIC_FINITE_BOX_CONDITIONAL",
        "No native carrier or Hopfion has been derived",
    ))
    require("native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md", (
        "C-squared/Bach bulk is `UNIQUE-CONDITIONAL`",
        "complete action, native source law, differentiable finite-cell boundary action",
    ))
    require("udt_conceptual_object_type_dependency_audit_2026-08-05/AUDIT_REPORT.md", (
        "Law and variation ownership are probably one joint",
        "Source and mass are downstream roles",
        "Bootstrap needs one nonidentity return",
    ))

    architecture = {row["architecture"]: row for row in rows("ARCHITECTURE_COMPARISON.tsv")}
    assert set(architecture) == {"R_FIRST", "A_FIRST"}
    assert "partial completion-dependent" in architecture["R_FIRST"]["positive_evidence"]
    assert "conditional C2/Bach and EH" in architecture["A_FIRST"]["positive_evidence"]
    assert architecture["R_FIRST"]["current_ruling"].endswith("NOT_DERIVED")
    assert architecture["A_FIRST"]["current_ruling"].endswith("NOT_SELECTED")

    joint = rows("JOINT_DEPENDENCY.tsv")
    order = {row["object"]: int(row["order"]) for row in joint}
    assert order["native global/local law"] < order["variation and boundary ownership"]
    assert order["variation and boundary ownership"] < order["native source"]
    assert order["variation and boundary ownership"] < order["physical mass"]
    assert all(row["status"] != "DERIVED" for row in joint if row["order"] in {"3", "4", "6", "7", "8", "9"})

    program = (ROOT / "CURRENT_RESEARCH_PROGRAM.md").read_text(encoding="utf-8")
    assert "Law-order `NOT_DERIVED`" in program
    assert "This is a research priority, not adoption of a response law" in program
    assert "The investigation is proposed, not launched" in program

    result = {
        "schema": "udt.native_law_order_architecture.independent_replay.v1",
        "status": "PASS",
        "immutable_source_hashes": len(immutable),
        "direct_source_semantic_checks": 10,
        "architecture_rows": len(architecture),
        "dependency_rows": len(joint),
        "imports_production_verifier": False,
        "imports_third_party": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

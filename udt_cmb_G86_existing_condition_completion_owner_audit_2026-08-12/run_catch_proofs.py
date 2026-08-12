#!/usr/bin/env python3
"""Hostile in-memory mutation suite for G86's fail-closed ownership rules."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path

from verify_independent import PKG, read_tsv, validate


def base() -> dict:
    return {
        "source_rows": read_tsv(PKG / "SOURCE_MANIFEST.tsv"),
        "owner_rows": read_tsv(PKG / "CONDITION_OWNER_ATLAS.tsv"),
        "matrix_rows": read_tsv(PKG / "FAMILY_CONDITION_MATRIX.tsv"),
        "conditional_rows": read_tsv(PKG / "CONDITIONAL_SELECTOR_ATLAS.tsv"),
        "result": json.loads((PKG / "DERIVATION_RESULT.json").read_text()),
    }


def mutation(name: str, mutate) -> dict:
    state = copy.deepcopy(base())
    mutate(state)
    errors = validate(state)
    return {"name": name, "caught": bool(errors), "errors": errors}


def main() -> None:
    catches = [
        mutation("missing_source", lambda s: s["source_rows"].pop()),
        mutation("duplicate_family_cell", lambda s: s["matrix_rows"].append(copy.deepcopy(s["matrix_rows"][0]))),
        mutation("promote_owner_to_selector", lambda s: s["owner_rows"][0].update(owner_class="OWNED_NONIDENTITY_SELECTOR")),
        mutation("set_owned_exclusion", lambda s: s["matrix_rows"][0].update(owned_exclusion="true")),
        mutation("corrupt_Xmax_source_hash", lambda s: s["source_rows"][2].update(sha256="0" * 64)),
        mutation("promote_conditional_selector", lambda s: s["conditional_rows"][1].update(premise_status="OWNED")),
        mutation("change_current_owned_result", lambda s: s["conditional_rows"][0].update(selection_status="SELECTED")),
        mutation("claim_selector_in_result", lambda s: s["result"].update(owned_nonidentity_selector_count=1)),
        mutation("claim_exclusion_in_result", lambda s: s["result"].update(owned_exclusion_count=1)),
        mutation("claim_physical_promotion", lambda s: s["result"].update(physical_promotions=1)),
        mutation("wrong_landing", lambda s: s["result"].update(primary_landing="ONE_EXISTING_OWNED_CONDITION_SELECTS_ONE_G85_FAMILY")),
        mutation("generated_G86_source", lambda s: s["owner_rows"][0].update(source_path="udt_cmb_G86_existing_condition_completion_owner_audit_2026-08-12/AUDIT_REPORT.md")),
    ]
    output = {
        "total": len(catches),
        "caught": sum(row["caught"] for row in catches),
        "all_caught": all(row["caught"] for row in catches),
        "cases": catches,
        "evidence_scope": "regression_mutations_not_standalone_semantic_proof",
    }
    (PKG / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    raise SystemExit(not output["all_caught"])


if __name__ == "__main__":
    main()

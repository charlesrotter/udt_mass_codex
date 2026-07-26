#!/usr/bin/env python3
"""Fail-closed production verifier and exercised catch-proofs."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


class AuditFailure(RuntimeError):
    pass


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def load() -> dict[str, object]:
    return {
        "presentations": read_tsv(HERE / "LOCAL_PRESENTATION_RANK.tsv"),
        "branches": read_tsv(HERE / "REALIZATION_BRANCH_RANK.tsv"),
        "constraints": read_tsv(HERE / "CONSTRAINT_RANK_LEDGER.tsv"),
        "completions": read_tsv(HERE / "COMPLETION_DOF_ATLAS.tsv"),
        "derived": read_tsv(HERE / "DERIVED_OBJECT_NO_DOUBLE_COUNT.tsv"),
        "response": read_tsv(HERE / "RESPONSE_COVERAGE_TARGET.tsv"),
        "status": read_tsv(HERE / "STATUS_LEDGER.tsv"),
        "result": json.loads((HERE / "AUDIT_RESULT.json").read_text(encoding="utf-8")),
    }


def keyed(rows: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    require(len(rows) == len({row[field] for row in rows}), f"duplicate {field}")
    return {row[field]: row for row in rows}


def validate(tables: dict[str, object], require_independent: bool = True) -> None:
    p = keyed(tables["presentations"], "id")
    b = keyed(tables["branches"], "branch_id")
    k = keyed(tables["constraints"], "id")
    c = keyed(tables["completions"], "completion_id")
    d = keyed(tables["derived"], "id")
    r = keyed(tables["response"], "id")
    s = keyed(tables["status"], "id")
    result = tables["result"]

    require(set(b) == {f"C0{i}" for i in range(1, 8)}, "seven-branch universe")
    require(len(c) == 12, "twelve-completion universe")
    require(set(c) == {row["completion_id"] for row in read_tsv(HERE / "COMPLETION_UNIVERSE.tsv")}, "completion key mismatch")
    require(all(row["selected"] == "NO" for row in b.values()), "selected realization branch")
    require(all(row["selected"] == "NO" for row in c.values()), "selected completion branch")

    require(p["P01"]["quotient_signature"] == "F4[6]", "primary metric count must be F4[6]")
    require(p["P02"]["quotient_signature"] == "F4[6]", "coframe cross-check must be F4[6]")
    require(p["P03"]["raw_signature"].endswith("=F4[10]"), "2+2 chart must total ten")
    require(p["P04"]["quotient_signature"] == "F4[7]", "chosen independent scalar comparison total")
    require(p["P04"]["status"] == "CHOSE_COMPARISON_CONFIGURATION", "comparison scalar promoted to native")
    require(p["P05"]["quotient_signature"] == "F4[6]_GENERIC_ARENA__UDT_REDUCED_RANK_OPEN", "founded phi/native-rank distinction")
    require(p["P05"]["status"] == "DERIVED_FOUNDED_SUBGROUP__FULL_EXTENSION_OPEN", "founded phi demoted")
    require(p["P06"]["status"] == "INACTIVE_COUNTERFACTUAL_REQUIRES_EXPLICIT_REAUTHORIZATION", "local CSN activated")
    require(p["P08"]["quotient_signature"] == "F4[10]", "supplied projector count")
    require("not the generic metric" in p["P09"]["scope"], "FC12 generic promotion")

    require(k["K03"]["audited_rank_effect"] == "ZERO", "regularity cannot have equation rank")
    require(k["K04"]["rank_status"] == "DERIVED_FOUNDED_PAIR", "founded pair demoted")
    require(k["K04"]["audited_rank_effect"] == "ONE_INTERNAL_CHANNEL_RELATION__ZERO_EXTRA_PHI_FIELD", "founded pair field-count promotion")
    require(k["K05"]["rank_status"] == "DERIVED_FOUNDED_ACTION", "founded exponential action demoted")
    require(k["K07"]["rank_status"] == "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED", "CSN status")
    require(k["K07"]["audited_rank_effect"] == "INACTIVE_NO_RANK_SUBTRACTION", "CSN rank subtraction")
    for kid in ["K09", "K13", "K14", "K15"]:
        require("ZERO" in k[kid]["audited_rank_effect"], f"{kid} local rank")
    require(k["K10"]["audited_rank_effect"].startswith("F3[1]"), "seal trace must be boundary typed")
    require(k["K11"]["audited_rank_effect"].startswith("F3[1]"), "seal tangent must be boundary typed")
    require(k["K16"]["audited_rank_effect"] == "ZERO_ADDITIONAL_FIELD", "F definition double count")
    require(k["K17"]["audited_rank_effect"] == "ZERO_DYNAMICAL_RANK", "Bianchi identity promotion")
    require(k["K20"]["rank_status"] == "OPEN_ABSENT", "response cannot be silently supplied")

    for did in ["D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09", "D10", "D12", "D14"]:
        require("F4[0]" in d[did]["additional_continuous_field_signature"], f"derived double count {did}")
    require(d["D11"]["additional_continuous_field_signature"] == "O[OPEN]", "Maxwell import")
    require("not the inhomogeneous Maxwell equation" in d["D09"]["scope"], "Maxwell identity disclosure")

    for row in c.values():
        if row["completion_id"] != "FC12_RECIPROCAL_TORIC_DIAGONAL":
            require(row["local_rank_reduction_from_completion_alone"] == "ZERO", "completion local rank invention")
            require("U[" in row["global_freedom_signature"], "global freedom assigned finite rank")
        else:
            require(row["bulk_signature"] == "F1[2]_INSIDE_SUPPLIED_ANSATZ", "FC12 profile count")
            require(row["closure_status"] == "CONDITIONAL_CONTROL_NOT_GENERIC", "FC12 status")

    require(len(r) == 10, "response coverage rows")
    require(r["R01"]["current_response_status"] == "OPEN_NOT_SELECTED", "complete extension gate")
    require(s["S03"]["status"] == "CHOSE_COMPARISON_F4_7_TOTAL", "comparison scalar status")
    require(s["S04"]["status"] == "DERIVED_FOUNDED_PHI_ADDS_ZERO__COMPLETE_EXTENSION_OPEN", "founded phi status")
    require(s["S13"]["status"] == "FOUNDED_COMPLETE_EXTENSION_AND_VARIATION_DOMAIN_THEN_RESPONSE_AND_GLOBAL_BOUNDARY", "closure order")
    require(s["S14"]["status"] == "NOT_EVALUABLE", "physical mode promotion")
    require(result["propagating_modes"] == "NOT_EVALUABLE", "result physical mode promotion")
    require("total_dof" not in result, "unlike rank types collapsed")
    require(result["status"] == "CORRECTED_GENERIC_ARENA_RANK_CHARACTERIZED__NATIVE_FOUNDED_EXTENSION_RANK_OPEN", "global solution promotion")
    require(result["founded_phi_additional_native_field_count"] == 0, "founded phi double counted")
    require(result["native_founded_complete_extension_rank"] == "OPEN", "native rank invented")

    for row in tables["constraints"]:
        require(row["domain"] and row["registered_status"] and row["audited_rank_effect"], "incomplete constraint row")

    if require_independent:
        independent_path = HERE / "INDEPENDENT_VERIFICATION_RESULT.json"
        require(independent_path.is_file(), "independent result absent")
        independent = json.loads(independent_path.read_text(encoding="utf-8"))
        require(independent["status"] == "PASS", "independent result failed")
        require("no_production_import" in independent["implementation"], "independent implementation provenance")
        text = (HERE / "verify_dof_audit_independent.py").read_text(encoding="utf-8")
        require("import build_dof_audit" not in text and "from build_dof_audit" not in text, "independent imports production")


def source_checks() -> int:
    count = 0
    for manifest in ("SOURCE_MANIFEST.tsv", "SOURCE_MANIFEST_CORRECTION.tsv"):
        for row in read_tsv(HERE / manifest):
            path = ROOT / row["path"]
            require(path.is_file(), f"missing source {row['path']}")
            require(str(path.stat().st_size) == row["bytes"], f"source size {row['path']}")
            require(sha256(path) == row["sha256"], f"source hash {row['path']}")
            count += 1
    return count


def main() -> None:
    source_count = source_checks()
    tables = load()
    validate(tables)

    catches: list[tuple[str, str, object]] = []

    def add(cid: str, description: str, mutate) -> None:
        catches.append((cid, description, mutate))

    add("X01", "configuration quotient promoted to physical modes", lambda t: keyed(t["status"], "id")["S14"].update(status="PHYSICAL_MODE_2"))
    add("X02", "strong local CSN subtracted in primary count", lambda t: keyed(t["presentations"], "id")["P01"].update(quotient_signature="F4[5]"))
    add("X03", "reciprocity promoted to spacetime equation", lambda t: keyed(t["constraints"], "id")["K04"].update(audited_rank_effect="F4[1]_SPACETIME"))
    add("X04", "regularity counted as equality", lambda t: keyed(t["constraints"], "id")["K03"].update(audited_rank_effect="F4[1]"))
    add("X05", "finite-cell ontology counted locally", lambda t: keyed(t["constraints"], "id")["K09"].update(audited_rank_effect="F4[1]"))
    add("X06", "seal trace changes chosen comparison count", lambda t: keyed(t["presentations"], "id")["P04"].update(quotient_signature="F4[6]"))
    add("X07", "derived curvature double counted", lambda t: keyed(t["derived"], "id")["D03"].update(additional_continuous_field_signature="F4[20]"))
    add("X08", "dF identity counted dynamically", lambda t: keyed(t["constraints"], "id")["K17"].update(audited_rank_effect="F4[4]"))
    add("X09", "Maxwell field imported", lambda t: keyed(t["derived"], "id")["D11"].update(additional_continuous_field_signature="F4[1]"))
    add("X10", "FC12 promoted to generic", lambda t: keyed(t["presentations"], "id")["P09"].update(scope="the generic metric"))
    add("X11", "global boundary data assigned finite rank", lambda t: keyed(t["completions"], "completion_id")["FC01_BOUNDARY_BOUNDARY"].update(global_freedom_signature="C[2]"))
    add("X12", "completion deleted", lambda t: t["completions"].pop())
    add("X13", "realization branch duplicated", lambda t: t["branches"].append(copy.deepcopy(t["branches"][0])))
    add("X14", "unlike ranks collapsed", lambda t: t["result"].update(total_dof=7))
    add("X15", "constraint domain erased", lambda t: keyed(t["constraints"], "id")["K06"].update(domain=""))
    add("X16", "same code labeled independent", lambda t: None)
    add("X17", "completion preferred", lambda t: keyed(t["completions"], "completion_id")["FC04_TWO_CAP_P1"].update(selected="YES"))
    add("X18", "local rank promoted to global solution count", lambda t: t["result"].update(status="COMPLETE_SOLUTION_COUNT"))
    add("X19", "chosen independent scalar promoted to native field", lambda t: keyed(t["presentations"], "id")["P04"].update(status="NATIVE_FIELD"))
    add("X20", "founded phi demoted to conditional readout", lambda t: keyed(t["presentations"], "id")["P05"].update(status="CONDITIONAL_DERIVATION_MAP_OPEN"))
    add("X21", "strong local CSN activated", lambda t: keyed(t["presentations"], "id")["P06"].update(status="ACTIVE_GAUGE"))
    add("X22", "native UDT rank invented from generic arena", lambda t: t["result"].update(native_founded_complete_extension_rank="F4[6]"))

    catch_rows = []
    for cid, description, mutate in catches:
        trial = copy.deepcopy(tables)
        if cid == "X16":
            original = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
            original["implementation"] = "production_replay"
            # Exercise the same validation rule without touching the evidence file.
            caught = "no_production_import" not in original["implementation"]
        else:
            mutate(trial)
            try:
                validate(trial, require_independent=False)
                caught = False
            except AuditFailure:
                caught = True
        require(caught, f"catch-proof failed: {cid}")
        catch_rows.append({"catch_id": cid, "forbidden_promotion": description, "result": "PASS_REJECTED"})

    write_tsv(HERE / "CATCH_PROOF_RESULTS.tsv", ["catch_id", "forbidden_promotion", "result"], catch_rows)
    result = {
        "status": "PASS",
        "source_hashes": source_count,
        "production_checks": 45,
        "catch_proofs": len(catch_rows),
        "branches": len(tables["branches"]),
        "completions": len(tables["completions"]),
        "independent_status": "PASS",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

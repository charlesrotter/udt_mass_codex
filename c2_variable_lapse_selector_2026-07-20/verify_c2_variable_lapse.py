#!/usr/bin/env python3
"""Independent fail-closed verification of the conditional variable-lapse C2 audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "309e85fb51fd8d6562eb2ffd020ac3e5259fcdb7"
EXPECTED_CENSUS = {
    "CONTEXT_CANDIDATE": 1625,
    "LOAD_BEARING_CANDIDATE": 39,
    "EXCLUDED_DUPLICATE_RAW_RECORD": 64,
    "PROVENANCE_OR_COUNTEREXAMPLE_ONLY": 1803,
    "EXCLUDED_GENERATED_ORGANIZATION": 226,
}


def need(condition: bool, message: str) -> None:
    if not bool(condition):
        raise AssertionError(message)


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def one(items: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    found = [row for row in items if row[key] == value]
    need(len(found) == 1, f"one:{key}:{value}")
    return found[0]


def validate_census(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 3757 and len({row["path"] for row in items}) == 3757, "census-count")
    counts: dict[str, int] = {}
    for row in items:
        counts[row["initial_disposition"]] = counts.get(row["initial_disposition"], 0) + 1
        need(len(row["blob"]) == 40 and len(row["sha256"]) == 64 and row["matched_tokens"], "census-fields")
        need(not row["path"].startswith("c2_variable_lapse_selector_2026-07-20/"), "census-feedback")
    need(counts == EXPECTED_CENSUS, "census-dispositions")
    return {"rows": len(items), "dispositions": counts}


def validate_sources(items: list[dict[str, str]], census: list[dict[str, str]]) -> dict[str, object]:
    expected = {row["path"] for row in census if row["initial_disposition"] == "LOAD_BEARING_CANDIDATE"}
    need(len(items) == 39 and len({row["path"] for row in items}) == 39, "source-count")
    need({row["path"] for row in items} == expected, "source-coverage")
    by_path = {row["path"]: row for row in census}
    for row in items:
        path = row["path"]
        data = subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)
        need(hashlib.sha256(data).hexdigest() == by_path[path]["sha256"], f"source-sha:{path}")
        blob = subprocess.check_output(["git", "rev-parse", f"{BASE}:{path}"], cwd=ROOT, text=True).strip()
        need(blob == by_path[path]["blob"], f"source-blob:{path}")
    need(one(items, "path", "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md")["audit_ruling"] == "FOUNDING_SELECTOR", "source-CSN")
    need(one(items, "path", "UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md")["audit_ruling"] == "CARRIER_EXCLUSION", "source-carrier")
    need(one(items, "path", "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv")["audit_ruling"] == "FROZEN_ACTION_STATUS", "source-action")
    need(one(items, "path", "c2_angular_reduction_selector_2026-07-20/NEXT_SCIENTIFIC_DECISION.md")["audit_ruling"] == "QUESTION_ONLY", "source-question")
    return {"rows": len(items), "base_hashes_replayed": len(items)}


def validate_equations(items: list[dict[str, str]]) -> dict[str, object]:
    expected = {
        "E01": "DERIVED_CONDITIONAL", "E02": "DERIVED_CONDITIONAL", "E03": "DERIVED_CONDITIONAL",
        "E04": "DERIVED_CONDITIONAL", "E05": "DERIVED_CONDITIONAL", "E06": "DERIVED_CONDITIONAL",
        "E07": "DERIVED_CONDITIONAL", "E08": "DERIVED_CONDITIONAL", "E09": "DERIVED_CONDITIONAL",
        "E10": "DERIVED_CONDITIONAL", "E11": "OBSERVED_EXACT_COUNTEREXAMPLE", "E12": "DERIVED_CONDITIONAL",
        "E13": "OBSERVED_EXACT", "E14": "DERIVED_SCOPED", "E15": "OPEN_NOT_AN_EQUATION",
        "E16": "OPEN", "E17": "NOT_SUPPLIED",
    }
    need(len(items) == 17 and len({row["id"] for row in items}) == 17, "equation-count")
    for identity, status in expected.items():
        need(one(items, "id", identity)["status"] == status, f"equation:{identity}")
    return {"rows": len(items), "rulings_checked": len(expected)}


def validate_branches(items: list[dict[str, str]]) -> dict[str, object]:
    expected = {
        "B01": "SURVIVES_SAME_CSN_CLASS", "B02": "EXCLUDED_IN_FIXED_ROUND_NO_SHIFT_SLICE",
        "B03": "SURVIVES_AS_CSN_EQUIVALENT_COPY", "B04": "EXCLUDED_AS_NEW_PHYSICAL_COMPACT_BRANCH",
        "B05": "OPEN_SINGULAR_STRATUM", "B06": "OPEN_BOUNDARY_BRANCH",
        "B07": "OPEN_SHIFT_TIME_LIVE_BRANCH", "B08": "OPEN_BASIS_AND_GLOBAL_BRANCH",
        "B09": "OPEN_GLOBAL_GEOMETRY_BRANCH",
    }
    need(len(items) == 9 and len({row["id"] for row in items}) == 9, "branch-count")
    for identity, ruling in expected.items():
        need(one(items, "id", identity)["ruling"] == ruling, f"branch:{identity}")
    return {"rows": len(items), "rulings_checked": len(expected)}


def validate_completeness(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 12 and len({row["layer"] for row in items}) == 12, "completeness-count")
    need(one(items, "layer", "external adversarial review")["status"] == "NOT_PERFORMED", "external-review")
    need(one(items, "layer", "time and connection")["status"] == "BOUNDED", "time-scope")
    need(one(items, "layer", "carrier and matter")["status"] == "NOT_PART_OF_SOLVE", "matter-scope")
    return {"rows": len(items), "external_review": "NOT_PERFORMED"}


def validate_status(items: list[dict[str, str]]) -> dict[str, object]:
    expected = {
        "S01": "DERIVED_CONDITIONAL", "S02": "DERIVED_CONDITIONAL", "S03": "DERIVED_CONDITIONAL",
        "S04": "DERIVED_CONDITIONAL", "S05": "DERIVED_CONDITIONAL", "S06": "OBSERVED_EXACT",
        "S07": "DERIVED_CONDITIONAL", "S08": "REFUTED_IN_SLICE", "S09": "REFUTED_IN_SLICE",
        "S10": "NOT_DERIVED", "S11": "NOT_DERIVED", "S12": "NOT_SUPPLIED",
        "S13": "FALSE_EXCLUDED", "S14": "FALSE_EXCLUDED", "S15": "REFUTED_CONFLATION",
        "S16": "VERIFIED_WITH_CAVEATS", "S17": "OPEN",
    }
    need(len(items) == 17 and len({row["id"] for row in items}) == 17, "status-count")
    for identity, status in expected.items():
        need(one(items, "id", identity)["status"] == status, f"status:{identity}")
    return {"rows": len(items), "rulings_checked": len(expected)}


def validate_derivation(result: dict[str, object]) -> dict[str, object]:
    need(result["result"] == "PASS" and len(result["checks"]) == 19, "derivation-checks")
    need(result["fixed_reciprocal_orbit_gauge"]["result"] == "s=1; N*r0/b=1 constant; u=eta or axis exchange; H=1", "derive-orbit")
    need(result["direct_lapse_check"]["sample_C2"] == "64/21", "derive-sample")
    need(result["common_factor_copy"]["status"].startswith("SAME_CSN_CLASS"), "derive-CSN-copy")
    need(result["maximum_conclusion"] == "CONDITIONAL_ROUND_CSN_CLASS_SURVIVES_POSITIVE_VARIABLE_LAPSE_IN_COMPACT_FIXED_BASIS_C2_FAMILY; NO_NEW_PHYSICAL_LAPSE_BRANCH; SCALE_MATERIAL_BOUNDARY_AND_TIME_SHIFT_OPEN", "derive-maximum")
    return {"checks": len(result["checks"]), "maximum_conclusion": result["maximum_conclusion"]}


def diagonal_4d_invariants(lapse: sp.Expr, spatial_factor: sp.Expr, point: sp.Expr) -> dict[str, sp.Expr]:
    t, eta, x, y = sp.symbols("t eta x y", real=True)
    coords = [t, eta, x, y]; n = 4
    g = sp.diag(lapse**2, spatial_factor**2, spatial_factor**2*sp.cos(eta)**2,
                spatial_factor**2*sp.sin(eta)**2)
    inv = sp.simplify(g.inv())
    gamma = [[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                gamma[a][b][c] = sp.simplify(sum(inv[a,d]*(sp.diff(g[d,c],coords[b]) +
                    sp.diff(g[d,b],coords[c])-sp.diff(g[b,c],coords[d])) for d in range(n))/2)
    rup = [[[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    rup[a][b][c][d] = sp.simplify(sp.diff(gamma[a][b][d],coords[c])-
                        sp.diff(gamma[a][b][c],coords[d])+sum(gamma[a][e][c]*gamma[e][b][d]-
                        gamma[a][e][d]*gamma[e][b][c] for e in range(n)))
    ric = sp.zeros(n)
    for b in range(n):
        for d in range(n):
            ric[b,d] = sp.simplify(sum(rup[a][b][a][d] for a in range(n)))
    sub = {eta: point}; gp = sp.simplify(g.subs(sub)); ip = sp.simplify(inv.subs(sub)); rp = sp.simplify(ric.subs(sub))
    scalar = sp.simplify(sum(ip[a,b]*rp[a,b] for a in range(n) for b in range(n)))
    ric2 = sp.simplify(sum(ip[a,a]*ip[b,b]*rp[a,b]**2 for a in range(n) for b in range(n)))
    rlow = [[[[sp.simplify(sum(g[a,e]*rup[e][b][c][d] for e in range(n)).subs(sub))
              for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    riem2 = sp.simplify(sum(ip[a,a]*ip[b,b]*ip[c,c]*ip[d,d]*rlow[a][b][c][d]**2
                            for a in range(n) for b in range(n) for c in range(n) for d in range(n)))
    c2 = sp.simplify(riem2-2*ric2+scalar**2/3)
    return {"R": scalar, "Ricci2": ric2, "Riemann2": riem2, "C2": c2}


def independent_algebra() -> dict[str, object]:
    eta = sp.symbols("eta", real=True)
    lapse = 1+sp.Rational(1,3)*sp.sin(2*eta)**2
    lapse_only = diagonal_4d_invariants(lapse, sp.Integer(1), sp.pi/8)
    expected_lapse = {"R": sp.Rational(26,7), "Ricci2": sp.Rational(524,49),
                      "Riemann2": sp.Rational(972,49), "C2": sp.Rational(64,21)}
    need(lapse_only == expected_lapse, "direct-lapse-invariants")
    omega = sp.exp(sp.Rational(1,3)*sp.sin(2*eta)**2)
    common = diagonal_4d_invariants(omega, omega, sp.pi/8)
    expected_common = {"R": -sp.Rational(14,3)*sp.exp(-sp.Rational(1,3)),
                       "Ricci2": sp.Rational(52,3)*sp.exp(-sp.Rational(2,3)),
                       "Riemann2": sp.Rational(740,27)*sp.exp(-sp.Rational(2,3)), "C2": 0}
    need(all(sp.simplify(common[key]-value) == 0 for key,value in expected_common.items()), "direct-common-invariants")

    q, squash, F = sp.symbols("q squash F", positive=True)
    need(sp.solve(q**2*(squash**2-1), squash) == [1], "independent-cross-squash")
    need(sp.solve(F**2*(sp.cos(eta)**2+sp.sin(eta)**2)-1, F) == [1], "independent-orbit-sum")
    nprime = sp.symbols("Nprime", real=True)
    angular_difference = -nprime*(sp.tan(eta)+sp.cot(eta))
    need(sp.trigsimp(angular_difference+nprime/(sp.sin(eta)*sp.cos(eta)), method="fu") == 0,
         "independent-hessian")
    return {"lapse_only": {k: str(v) for k,v in lapse_only.items()},
            "common_factor": {k: str(v) for k,v in common.items()},
            "orbit_cross_root": "s=1", "zero_Weyl_toric_lapse": "Nprime=0"}


def source_syntax_checks() -> dict[str, str]:
    csn = (ROOT/"UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md").read_text(encoding="utf-8")
    need("A native pre-scale bulk law must respect local common-scale neutrality" in csn, "syntax-CSN")
    parent = (ROOT/"c2_angular_reduction_selector_2026-07-20/NEXT_SCIENTIFIC_DECISION.md").read_text(encoding="utf-8")
    need("g4 = epsilon_t N(eta)^2 d tau^2 + g3[H(eta),s]" in parent, "syntax-parent-question")
    carrier = (ROOT/"UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md").read_text(encoding="utf-8")
    need("HISTORICAL WORKING POSIT, now REOPENED" in carrier, "syntax-carrier")
    return {"CSN": "PASS", "parent_question": "PASS", "carrier": "PASS"}


def expect_failure(label: str, fn) -> str:
    try:
        fn()
    except (AssertionError, KeyError, subprocess.CalledProcessError):
        return "PASS"
    raise AssertionError(f"catch-did-not-fail:{label}")


def main() -> None:
    census=rows("SOURCE_CENSUS.tsv"); sources=rows("SOURCE_ADJUDICATION.tsv")
    equations=rows("EQUATION_LEDGER.tsv"); branches=rows("CANDIDATE_BRANCHES.tsv")
    completeness=rows("COMPLETENESS_SCOPE.tsv"); status=rows("STATUS_LEDGER.tsv")
    derivation=json.loads((HERE/"DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    groups = {
        "source_census": validate_census(census), "source_adjudication": validate_sources(sources,census),
        "equations": validate_equations(equations), "branches": validate_branches(branches),
        "completeness": validate_completeness(completeness), "status": validate_status(status),
        "derivation": validate_derivation(derivation), "source_syntax": source_syntax_checks(),
        "independent_4d_algebra": independent_algebra(),
    }
    catches: dict[str,str] = {}
    catches["missing_census_row_rejected"] = expect_failure("census", lambda: validate_census(census[:-1]))
    altered=copy.deepcopy(census); one(altered,"path","LIVE.md")["sha256"]="0"*64
    catches["base_source_mutation_rejected"] = expect_failure("source-hash", lambda: validate_sources(sources,altered))
    catches["missing_source_adjudication_rejected"] = expect_failure("source", lambda: validate_sources(sources[:-1],census))
    altered=copy.deepcopy(sources); one(altered,"path","UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md")["audit_ruling"]="NATIVE_CARRIER"
    catches["carrier_import_rejected"] = expect_failure("carrier", lambda: validate_sources(altered,census))
    catches["missing_equation_rejected"] = expect_failure("equation", lambda: validate_equations(equations[:-1]))
    for identity,bad,label in [
        ("E03","UNCONDITIONAL_ACTION","Bach"),("E05","PHYSICAL_BOUNDARY_THEOREM","boundary"),
        ("E08","ABSOLUTE_CLOCK_SELECTED","clock"),("E11","ZERO_WEYL","sample"),
        ("E12","NEW_PHYSICAL_BRANCH","CSN-copy"),("E14","SCALE_SELECTED","scale"),
        ("E15","DERIVED_BOUNDARY_EQUATION","wall"),("E16","SOLVED","shift"),
        ("E17","MATERIAL_ACTION_DERIVED","matter")]:
        changed=copy.deepcopy(equations); one(changed,"id",identity)["status"]=bad
        catches[f"{label}_overclaim_rejected"] = expect_failure(label, lambda changed=changed: validate_equations(changed))
    catches["missing_branch_rejected"] = expect_failure("branch", lambda: validate_branches(branches[:-1]))
    for identity,bad,label in [("B02","SURVIVES_PHYSICAL","lapse"),("B03","NEW_BRANCH","copy"),
                               ("B05","EXCLUDED","singular"),("B06","EXCLUDED","boundary-branch"),
                               ("B07","SOLVED","time-live")]:
        changed=copy.deepcopy(branches); one(changed,"id",identity)["ruling"]=bad
        catches[f"{label}_branch_misgrade_rejected"] = expect_failure(label, lambda changed=changed: validate_branches(changed))
    catches["missing_completeness_layer_rejected"] = expect_failure("scope", lambda: validate_completeness(completeness[:-1]))
    catches["missing_status_rejected"] = expect_failure("status", lambda: validate_status(status[:-1]))
    for identity,bad,label in [("S08","UNCONDITIONAL_REFUTATION","lapse-status"),
                               ("S10","SCALE_DERIVED","scale-status"),("S11","WALL_DERIVED","wall-status"),
                               ("S12","BOOTSTRAP_EOM","bootstrap-status"),("S13","SOLVED","shift-status"),
                               ("S14","ELECTRON_INPUT","electron-status"),("S15","CARRIER_L2","carrier-status"),
                               ("S17","COMPLETE_ACTION","action-status")]:
        changed=copy.deepcopy(status); one(changed,"id",identity)["status"]=bad
        catches[f"{label}_overclaim_rejected"] = expect_failure(label, lambda changed=changed: validate_status(changed))
    changed=copy.deepcopy(derivation); changed["direct_lapse_check"]["sample_C2"]="0"
    catches["derivation_lapse_cost_loss_rejected"] = expect_failure("derive-lapse", lambda: validate_derivation(changed))
    changed=copy.deepcopy(derivation); changed["common_factor_copy"]["status"]="NEW_PHYSICAL_BRANCH"
    catches["derivation_CSN_copy_promotion_rejected"] = expect_failure("derive-copy", lambda: validate_derivation(changed))
    changed=copy.deepcopy(derivation); changed["maximum_conclusion"]="COMPLETE_NATIVE_ACTION"
    catches["maximum_conclusion_overreach_rejected"] = expect_failure("derive-max", lambda: validate_derivation(changed))
    with (HERE/"CATCH_PROOFS.tsv").open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=["catch","result"],delimiter="\t",lineterminator="\n")
        writer.writeheader(); writer.writerows({"catch":k,"result":v} for k,v in sorted(catches.items()))
    result={"schema":"udt-conditional-c2-variable-lapse-verification-1.0","result":"PASS",
            "groups":groups,"catch_proofs":catches,
            "counts":{"census":len(census),"sources":len(sources),"equations":len(equations),
                      "branches":len(branches),"completeness":len(completeness),"status":len(status),
                      "catch_proofs":len(catches)},
            "derivation_sha256":hashlib.sha256((HERE/"DERIVATION_RESULT.json").read_bytes()).hexdigest(),
            "verdict":"CONDITIONAL_ROUND_CSN_CLASS_SURVIVES_POSITIVE_VARIABLE_LAPSE_IN_COMPACT_FIXED_BASIS_C2_FAMILY; NO_NEW_PHYSICAL_LAPSE_BRANCH; SCALE_MATERIAL_BOUNDARY_AND_TIME_SHIFT_OPEN",
            "certification":"VERIFIED-WITH-CAVEATS: independent 4D coordinate curvature and orbit matching; no fresh external-model review",
            "compute":{"cpu_only":True,"gpu_used":False,"sympy":sp.__version__}}
    (HERE/"VERIFICATION_RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"result":"PASS","groups":len(groups),"catch_proofs":len(catches),"verdict":result["verdict"]},sort_keys=True))


if __name__ == "__main__":
    main()

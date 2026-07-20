#!/usr/bin/env python3
"""Independent fail-closed verification of the time/fiber shift Jacobi audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
BASE="61f6bc01e5732b3bc59120d506bd6b2716646369"
EXPECTED_CENSUS={"CONTEXT_CANDIDATE":1644,"LOAD_BEARING_CANDIDATE":45,
    "EXCLUDED_DUPLICATE_RAW_RECORD":68,"PROVENANCE_OR_COUNTEREXAMPLE_ONLY":1803,
    "EXCLUDED_GENERATED_ORGANIZATION":226}


def need(condition: bool,message: str) -> None:
    if not bool(condition): raise AssertionError(message)


def rows(name: str) -> list[dict[str,str]]:
    with (HERE/name).open(encoding="utf-8",newline="") as handle:
        return list(csv.DictReader(handle,delimiter="\t"))


def one(items: list[dict[str,str]],key: str,value: str) -> dict[str,str]:
    found=[row for row in items if row[key]==value]; need(len(found)==1,f"one:{key}:{value}"); return found[0]


def validate_census(items: list[dict[str,str]]) -> dict[str,object]:
    need(len(items)==3786 and len({row["path"] for row in items})==3786,"census-count")
    counts: dict[str,int]={}
    for row in items:
        counts[row["initial_disposition"]]=counts.get(row["initial_disposition"],0)+1
        need(len(row["blob"])==40 and len(row["sha256"])==64 and row["matched_tokens"],"census-fields")
        need(not row["path"].startswith("c2_time_fiber_shift_jacobi_2026-07-20/"),"census-feedback")
    need(counts==EXPECTED_CENSUS,"census-dispositions")
    return {"rows":len(items),"dispositions":counts}


def validate_sources(items: list[dict[str,str]],census: list[dict[str,str]]) -> dict[str,object]:
    expected={row["path"] for row in census if row["initial_disposition"]=="LOAD_BEARING_CANDIDATE"}
    need(len(items)==45 and len({row["path"] for row in items})==45,"source-count")
    need({row["path"] for row in items}==expected,"source-coverage")
    by_path={row["path"]:row for row in census}
    for row in items:
        data=subprocess.check_output(["git","show",f"{BASE}:{row['path']}"],cwd=ROOT)
        need(hashlib.sha256(data).hexdigest()==by_path[row["path"]]["sha256"],f"source-sha:{row['path']}")
        blob=subprocess.check_output(["git","rev-parse",f"{BASE}:{row['path']}"],cwd=ROOT,text=True).strip()
        need(blob==by_path[row["path"]]["blob"],f"source-blob:{row['path']}")
    need(one(items,"path","UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md")["audit_ruling"]=="FOUNDING_SELECTOR","source-CSN")
    need(one(items,"path","UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md")["audit_ruling"]=="CARRIER_EXCLUSION","source-carrier")
    need(one(items,"path","c2_variable_lapse_selector_2026-07-20/NEXT_SCIENTIFIC_DECISION.md")["audit_ruling"]=="QUESTION_ONLY","source-question")
    return {"rows":len(items),"base_hashes_replayed":len(items)}


def validate_table(items: list[dict[str,str]],key: str,expected: dict[str,str],field: str,label: str) -> dict[str,object]:
    need(len(items)==len(expected) and len({row[key] for row in items})==len(expected),f"{label}-count")
    for identity,value in expected.items(): need(one(items,key,identity)[field]==value,f"{label}:{identity}")
    return {"rows":len(items),"rulings_checked":len(expected)}


def validate_completeness(items: list[dict[str,str]]) -> dict[str,object]:
    need(len(items)==13 and len({row["layer"] for row in items})==13,"scope-count")
    need(one(items,"layer","branch and bifurcation")["status"]=="LINEAR_COMPLETE","scope-linear")
    need(one(items,"layer","stability spectrum")["status"]=="NOT_TESTED","scope-stability")
    need(one(items,"layer","external adversarial review")["status"]=="NOT_PERFORMED","scope-external")
    return {"rows":len(items),"external_review":"NOT_PERFORMED"}


def validate_derivation(result: dict[str,object]) -> dict[str,object]:
    need(result["result"]=="PASS" and len(result["checks"])==16,"derivation-checks")
    need(result["direct_coordinate_result"]["nonzero_linear_Weyl_components"]==36,"derive-Weyl")
    need(result["direct_coordinate_result"]["Bach_projection_matches_reduced_Jacobi"] is True,"derive-Bach")
    need(result["complete_regular_kernel"]["result"]=="w=constant only","derive-kernel")
    need(result["complete_regular_kernel"]["constant_status"].startswith("exact rotating-coordinate"),"derive-gauge")
    need(result["maximum_conclusion"]=="NO_REGULAR_NON_GAUGE_TIME_FIBER_SHIFT_JACOBI_MODE_IN_CONDITIONAL_ROUND_COMPACT_C2_SLICE; NONLINEAR_BOUNDARY_TIME_LIVE_SCALE_AND_MATTER_OPEN","derive-max")
    return {"checks":len(result["checks"]),"maximum_conclusion":result["maximum_conclusion"]}


def explicit_euclidean_sample() -> dict[str,sp.Expr]:
    """Independent explicit-profile linearization from the finite off-diagonal metric."""
    tau,eta,x1,x2,p=sp.symbols("tau eta x1 x2 p",real=True)
    coords=[tau,eta,x1,x2]; n=4; c=sp.cos(eta); s=sp.sin(eta); w=sp.cos(2*eta)
    g=sp.Matrix([[1+p**2*w**2,0,p*w*c**2,p*w*s**2],[0,1,0,0],
                 [p*w*c**2,0,c**2,0],[p*w*s**2,0,0,s**2]])
    g0=g.subs(p,0); h=sp.diff(g,p).subs(p,0); inv0=sp.simplify(g0.inv()); inv1=sp.simplify(-inv0*h*inv0)
    gamma0=[[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    gamma1=[[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for d in range(n):
                base=[sp.diff(g0[e,d],coords[b])+sp.diff(g0[e,b],coords[d])-sp.diff(g0[b,d],coords[e]) for e in range(n)]
                varied=[sp.diff(h[e,d],coords[b])+sp.diff(h[e,b],coords[d])-sp.diff(h[b,d],coords[e]) for e in range(n)]
                gamma0[a][b][d]=sp.simplify(sum(inv0[a,e]*base[e] for e in range(n))/2)
                gamma1[a][b][d]=sp.simplify((sum(inv1[a,e]*base[e] for e in range(n))+
                                              sum(inv0[a,e]*varied[e] for e in range(n)))/2)
    rup0=[[[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    rup1=[[[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for d in range(n):
                for e in range(n):
                    rup0[a][b][d][e]=sp.simplify(sp.diff(gamma0[a][b][e],coords[d])-sp.diff(gamma0[a][b][d],coords[e])+
                        sum(gamma0[a][f][d]*gamma0[f][b][e]-gamma0[a][f][e]*gamma0[f][b][d] for f in range(n)))
                    rup1[a][b][d][e]=sp.simplify(sp.diff(gamma1[a][b][e],coords[d])-sp.diff(gamma1[a][b][d],coords[e])+
                        sum(gamma1[a][f][d]*gamma0[f][b][e]+gamma0[a][f][d]*gamma1[f][b][e]-
                            gamma1[a][f][e]*gamma0[f][b][d]-gamma0[a][f][e]*gamma1[f][b][d] for f in range(n)))
    ric0=sp.zeros(n); ric1=sp.zeros(n)
    for b in range(n):
        for d in range(n):
            ric0[b,d]=sp.simplify(sum(rup0[a][b][a][d] for a in range(n)))
            ric1[b,d]=sp.simplify(sum(rup1[a][b][a][d] for a in range(n)))
    scalar0=sp.simplify(sum(inv0[a,b]*ric0[a,b] for a in range(n) for b in range(n)))
    scalar1=sp.simplify(sum(inv1[a,b]*ric0[a,b]+inv0[a,b]*ric1[a,b] for a in range(n) for b in range(n)))
    c1=[[[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for d in range(n):
                for e in range(n):
                    low1=sum(h[a,f]*rup0[f][b][d][e]+g0[a,f]*rup1[f][b][d][e] for f in range(n))
                    trace1=(h[a,d]*ric0[b,e]+g0[a,d]*ric1[b,e]-h[a,e]*ric0[b,d]-g0[a,e]*ric1[b,d]
                            -h[b,d]*ric0[a,e]-g0[b,d]*ric1[a,e]+h[b,e]*ric0[a,d]+g0[b,e]*ric1[a,d])
                    wedge0=g0[a,d]*g0[b,e]-g0[a,e]*g0[b,d]
                    wedge1=h[a,d]*g0[b,e]+g0[a,d]*h[b,e]-h[a,e]*g0[b,d]-g0[a,e]*h[b,d]
                    c1[a][b][d][e]=sp.simplify(low1-trace1/2+scalar1*wedge0/6+scalar0*wedge1/6)
    coefficient=sp.simplify(sum(inv0[a,a]*inv0[b,b]*inv0[d,d]*inv0[e,e]*c1[a][b][d][e]**2
        for a in range(n) for b in range(n) for d in range(n) for e in range(n)).subs(eta,sp.pi/6))
    return {"C2_epsilon2_at_pi_over_6":coefficient,"background_R":sp.simplify(scalar0.subs(eta,sp.pi/6))}


def independent_algebra() -> dict[str,object]:
    sample=explicit_euclidean_sample(); need(sample["C2_epsilon2_at_pi_over_6"]==48,"independent-sample-C2")
    need(sample["background_R"]==6,"independent-background")
    x=sp.symbols("x",real=True); w=sp.Function("w")(x)
    density=(1-x**2)**2*sp.diff(w,x,2)**2+4*(1-x**2)*sp.diff(w,x)**2
    EL=sp.factor(sp.diff(sp.diff(density,sp.diff(w,x,2)),x,2)-sp.diff(sp.diff(density,sp.diff(w,x)),x))
    target=2*(sp.diff((1-x**2)**2*sp.diff(w,x,2),x,2)-4*sp.diff((1-x**2)*sp.diff(w,x),x))
    need(sp.simplify(EL-target)==0,"independent-x-EL")
    # Polynomial-space check is a finite regression anchor for the analytic positive energy proof.
    coeff=sp.symbols("a0:7"); poly=sum(coeff[k]*x**k for k in range(7))
    action=sp.integrate(((1-x**2)**2*sp.diff(poly,x,2)**2+4*(1-x**2)*sp.diff(poly,x)**2),(x,-1,1))
    hessian=sp.hessian(action,coeff)
    need(hessian.rank()==6 and hessian.nullspace()==[sp.Matrix([1,0,0,0,0,0,0])],"polynomial-kernel-anchor")
    alpha=sp.symbols("alpha")
    need(sp.solve(alpha*(alpha+1),alpha)==[-1,0],"endpoint-homogeneous-indicial")
    eta=sp.pi/6; S=sp.sin(2*eta); C=sp.cos(2*eta)
    wp=-2*S; wpp=-4*C; w3=8*S; w4=16*C
    jac=sp.simplify(S*w4+4*C*w3-(16*S+4*C**2/S)*wpp+8*C*(C**2/S**2-1)*wp)
    need(jac==32*sp.sqrt(3),"sample-Jacobi-residual")
    need(sp.simplify(-jac/(4*S))==-16,"sample-Bach-projection")
    return {"finite_metric_sample":{k:str(v) for k,v in sample.items()},"degree_six_energy_rank":hessian.rank(),
            "endpoint_v_exponents":["-1","0"],"sample_Jacobi":str(jac),"sample_Bach_projection":"-16"}


def source_syntax() -> dict[str,str]:
    parent=(ROOT/"c2_variable_lapse_selector_2026-07-20/NEXT_SCIENTIFIC_DECISION.md").read_text(encoding="utf-8")
    need("W(eta)" in parent and "full Bach" in parent,"syntax-parent")
    csn=(ROOT/"UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md").read_text(encoding="utf-8")
    need("A native pre-scale bulk law must respect local common-scale neutrality" in csn,"syntax-CSN")
    return {"parent_question":"PASS","CSN":"PASS"}


def expect_failure(label: str,fn) -> str:
    try: fn()
    except (AssertionError,KeyError,subprocess.CalledProcessError): return "PASS"
    raise AssertionError(f"catch-did-not-fail:{label}")


def main() -> None:
    census=rows("SOURCE_CENSUS.tsv"); sources=rows("SOURCE_ADJUDICATION.tsv")
    equations=rows("EQUATION_LEDGER.tsv"); branches=rows("CANDIDATE_BRANCHES.tsv")
    completeness=rows("COMPLETENESS_SCOPE.tsv"); status=rows("STATUS_LEDGER.tsv")
    derivation=json.loads((HERE/"DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    equation_expected={f"E{i:02d}":value for i,value in enumerate([
        "DERIVED_CONDITIONAL","DERIVED_CONDITIONAL","DERIVED_CONDITIONAL","DERIVED_CONDITIONAL",
        "DERIVED_CONDITIONAL","DERIVED_CONDITIONAL","DERIVED_CONDITIONAL","DERIVED_CONDITIONAL",
        "DERIVED_CONDITIONAL","DERIVED_CONDITIONAL","DERIVED_EXACT_COORDINATE","OBSERVED_EXACT_DIAGNOSTIC",
        "CHARACTERIZED_OPEN_STRATA","DERIVED_SCOPED","OPEN","OPEN_NOT_AN_EQUATION","NOT_SUPPLIED"],1)}
    branch_expected={"B01":"SURVIVES_AS_COORDINATE_GAUGE_ORBIT","B02":"EXCLUDED_AT_JACOBI_ORDER_IN_SLICE",
        "B03":"EXACT_NONSOLUTION_DIAGNOSTIC","B04":"RETAINED_SINGULAR_STRATA","B05":"OPEN_BOUNDARY_BRANCH",
        "B06":"OPEN_NONLINEAR_BRANCH","B07":"OPEN_CONNECTION_BRANCHES","B08":"OPEN_TIME_LIVE_BRANCH",
        "B09":"OPEN_GLOBAL_GEOMETRY_BRANCH"}
    status_values=["DERIVED_CONDITIONAL","DERIVED_CONDITIONAL","DERIVED_CONDITIONAL","DERIVED_CONDITIONAL",
        "DERIVED_CONDITIONAL","DERIVED_EXACT_COORDINATE","REFUTED_IN_SLICE","NOT_DERIVED","FALSE",
        "FALSE_EXCLUDED","NOT_DERIVED","NOT_DERIVED","FALSE_EXCLUDED","REFUTED_CONFLATION",
        "VERIFIED_WITH_CAVEATS","OPEN","OPEN"]
    status_expected={f"S{i:02d}":value for i,value in enumerate(status_values,1)}
    groups={"source_census":validate_census(census),"source_adjudication":validate_sources(sources,census),
        "equations":validate_table(equations,"id",equation_expected,"status","equation"),
        "branches":validate_table(branches,"id",branch_expected,"ruling","branch"),
        "completeness":validate_completeness(completeness),
        "status":validate_table(status,"id",status_expected,"status","status"),
        "derivation":validate_derivation(derivation),"source_syntax":source_syntax(),
        "independent_algebra":independent_algebra()}
    catches: dict[str,str]={}
    catches["missing_census_row_rejected"]=expect_failure("census",lambda:validate_census(census[:-1]))
    changed=copy.deepcopy(census); one(changed,"path","LIVE.md")["sha256"]="0"*64
    catches["base_source_mutation_rejected"]=expect_failure("source-hash",lambda:validate_sources(sources,changed))
    catches["missing_source_rejected"]=expect_failure("source",lambda:validate_sources(sources[:-1],census))
    changed=copy.deepcopy(sources); one(changed,"path","UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md")["audit_ruling"]="NATIVE_CARRIER"
    catches["carrier_import_rejected"]=expect_failure("carrier",lambda:validate_sources(changed,census))
    catches["missing_equation_rejected"]=expect_failure("equation",lambda:validate_table(equations[:-1],"id",equation_expected,"status","equation"))
    for identity,bad,label in [("E04","LORENTZIAN_STABILITY_ENERGY","stability"),("E07","REDUCED_ONLY","Bach"),
        ("E10","ALL_NONLINEAR_SHIFTS_EXCLUDED","nonlinear"),("E11","PHYSICAL_ROTATION","gauge"),
        ("E13","DISCARDED","singular"),("E16","PHYSICAL_WALL_SOLVED","boundary"),("E17","MATTER_DERIVED","matter")]:
        changed=copy.deepcopy(equations); one(changed,"id",identity)["status"]=bad
        catches[f"{label}_equation_overclaim_rejected"]=expect_failure(label,lambda changed=changed:validate_table(changed,"id",equation_expected,"status","equation"))
    catches["missing_branch_rejected"]=expect_failure("branch",lambda:validate_table(branches[:-1],"id",branch_expected,"ruling","branch"))
    for identity,bad,label in [("B01","PHYSICAL_ROTATION","constant"),("B04","REJECTED","singular-branch"),
        ("B05","EXCLUDED","boundary-branch"),("B06","EXCLUDED","nonlinear-branch"),("B08","SOLVED","time-live")]:
        changed=copy.deepcopy(branches); one(changed,"id",identity)["ruling"]=bad
        catches[f"{label}_misgrade_rejected"]=expect_failure(label,lambda changed=changed:validate_table(changed,"id",branch_expected,"ruling","branch"))
    catches["missing_scope_rejected"]=expect_failure("scope",lambda:validate_completeness(completeness[:-1]))
    catches["missing_status_rejected"]=expect_failure("status",lambda:validate_table(status[:-1],"id",status_expected,"status","status"))
    for identity,bad,label in [("S07","UNCONDITIONAL_NO_GO","scoped-negative"),("S08","ALL_EXCLUDED","nonlinear-status"),
        ("S10","EQUIVALENCE_DERIVED","acceleration"),("S11","SCALE_SELECTED","scale"),
        ("S12","WALL_DERIVED","wall"),("S13","ELECTRON_INPUT","electron"),
        ("S14","COMPLETE_ACTION","action"),("S17","CLOSED","closure")]:
        changed=copy.deepcopy(status); one(changed,"id",identity)["status"]=bad
        catches[f"{label}_overclaim_rejected"]=expect_failure(label,lambda changed=changed:validate_table(changed,"id",status_expected,"status","status"))
    changed=copy.deepcopy(derivation); changed["complete_regular_kernel"]["result"]="nonconstant physical rotation"
    catches["derivation_kernel_mutation_rejected"]=expect_failure("derive-kernel",lambda:validate_derivation(changed))
    changed=copy.deepcopy(derivation); changed["direct_coordinate_result"]["Bach_projection_matches_reduced_Jacobi"]=False
    catches["derivation_full_equation_loss_rejected"]=expect_failure("derive-Bach",lambda:validate_derivation(changed))
    changed=copy.deepcopy(derivation); changed["maximum_conclusion"]="COMPLETE_UDT_TIME_DYNAMICS"
    catches["maximum_overreach_rejected"]=expect_failure("derive-max",lambda:validate_derivation(changed))
    with (HERE/"CATCH_PROOFS.tsv").open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=["catch","result"],delimiter="\t",lineterminator="\n"); writer.writeheader()
        writer.writerows({"catch":k,"result":v} for k,v in sorted(catches.items()))
    result={"schema":"udt-conditional-c2-time-fiber-shift-verification-1.0","result":"PASS",
        "groups":groups,"catch_proofs":catches,"counts":{"census":len(census),"sources":len(sources),
        "equations":len(equations),"branches":len(branches),"completeness":len(completeness),
        "status":len(status),"catch_proofs":len(catches)},
        "derivation_sha256":hashlib.sha256((HERE/"DERIVATION_RESULT.json").read_bytes()).hexdigest(),
        "verdict":"NO_REGULAR_NON_GAUGE_TIME_FIBER_SHIFT_JACOBI_MODE_IN_CONDITIONAL_ROUND_COMPACT_C2_SLICE; NONLINEAR_BOUNDARY_TIME_LIVE_SCALE_AND_MATTER_OPEN",
        "certification":"VERIFIED-WITH-CAVEATS: independent finite-metric Euclidean curvature sample and energy/operator reconstruction; no fresh external-model review",
        "compute":{"cpu_only":True,"gpu_used":False,"sympy":sp.__version__}}
    (HERE/"VERIFICATION_RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"result":"PASS","groups":len(groups),"catch_proofs":len(catches),"verdict":result["verdict"]},sort_keys=True))


if __name__=="__main__": main()

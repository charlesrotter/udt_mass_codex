#!/usr/bin/env python3
"""Independent reconstruction and fail-closed mutation tests for the pre-P06 audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULT = HERE / "DERIVATION_RESULT.json"
MAXIMUM = "EXISTING_UDT_BOUNDARY_SELECTOR_STATUS_CLASSIFIED_FOR_P05_LANES"
PRIMARY = "PARTIAL_NATIVE_DATA_ONLY_MULTIPLE_POLARIZATIONS_AND_FUNCTIONALS_REMAIN"
TABLES = [
    "PRINCIPLE_TO_BOUNDARY_SLOT.tsv", "BOUNDARY_TYPE_BRANCHES.tsv",
    "LANE_POLARIZATION_MATRIX.tsv", "FUNCTIONAL_AMBIGUITY.tsv",
    "FIELD_LANE_CLOSURE.tsv", "OPERATOR_BOUNDARY_REQUIREMENTS.tsv",
    "STATUS_LEDGER.tsv", "SOURCE_LINEAGE.tsv",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load():
    return (
        json.loads(RESULT.read_text(encoding="utf-8")),
        {name: rows(HERE / name) for name in TABLES},
        json.loads((HERE / "SELECTOR_DEPENDENCY_GRAPH.json").read_text(encoding="utf-8")),
    )


def validate(result: dict, tables: dict[str, list[dict[str, str]]], graph: dict) -> None:
    require(result["schema"] == "udt-pre-p06-boundary-selector-result-1.0", "schema")
    require(result["status"] == "PASS", "status")
    require(result["evidence_grade"] == "LEAD_PENDING_FRESH_ADVERSARIAL_REVIEW", "grade")
    require(result["primary_result"] == PRIMARY and result["maximum_conclusion"] == MAXIMUM, "maximum")
    require(result["lane_outcomes"] == {
        "L01":"PARTIAL_NATIVE_DATA_MULTIPLE_COMPLETIONS",
        "L02":"PARTIAL_NATIVE_DATA_MULTIPLE_COMPLETIONS",
        "L03":"EXCLUDED_NO_BULK_OPERATOR",
    }, "lane outcomes")
    require(result["counts"] == {
        "principles_mapped":10,"boundary_type_branches":5,"polarization_rows":10,
        "functional_ambiguities":8,"field_lane_pairs":21,"P06_ready_pairs":0,
        "source_files":17,"solutions_computed":0,
    }, "counts")
    scope = result["scope"]
    require(scope["CPU_only"], "CPU scope")
    require(not any(scope[key] for key in (
        "GPU_used","ODE_or_PDE_run","P06_launched","boundary_functional_adopted",
        "boundary_type_selected","carrier_or_source_loaded","startup_controls_changed","canon_changed",
    )), "scope promotion")

    principles = {row["id"]:row for row in tables["PRINCIPLE_TO_BOUNDARY_SLOT.tsv"]}
    require(len(principles) == 10 and set(principles) == {f"P{i:02d}" for i in range(1,11)}, "principle coverage")
    require(principles["P02"]["classification"] == "PARTIAL_ONE_SCALAR_WIRE", "seal scope")
    require(principles["P02"]["normal_jet"] == "normal_phi_derivative_free", "free normal derivative")
    require(principles["P03"]["classification"] == "PARTIAL_RATIO_ONLY", "Reciprocity scope")
    require(principles["P04"]["classification"] == "NULL_DIRECTION_NOT_POLARIZATION", "CSN scope")
    require(principles["P05"]["classification"] == "NO_OFFSHELL_JOIN", "co-presence scope")
    require(principles["P07"]["off_shell_status"] == "COMPLETED_SOLUTION_ADMISSIBILITY", "bootstrap scope")
    require(principles["P08"]["classification"] == "DOES_NOT_SELECT_POLARIZATION", "coframe scope")
    require(principles["P09"]["classification"] == "DOES_NOT_SELECT_BOUNDARY_TYPE", "surface scope")

    types = {row["id"]:row for row in tables["BOUNDARY_TYPE_BRANCHES.tsv"]}
    require(len(types) == 5 and set(types) == {f"T{i:02d}" for i in range(1,6)}, "boundary type coverage")
    require(all(row["selected_by_current_UDT"].startswith("NO") for row in types.values()), "boundary type unselected")
    require("non_null split inapplicable" in types["T02"]["L01_operator_coverage"], "no null extrapolation")
    require(types["T03"]["causal_or_domain_status"] == "OPEN", "moving branch")
    require("boundary versus matching" in types["T04"]["L01_operator_coverage"], "quotient branch")

    pol = {row["id"]:row for row in tables["LANE_POLARIZATION_MATRIX.tsv"]}
    require(len(pol) == 10 and set(pol) == {f"W{i:02d}" for i in range(1,11)}, "polarization coverage")
    require(sum(row["lane"] == "L01" for row in pol.values()) == 5, "L01 polarization count")
    require(sum(row["lane"] == "L02" for row in pol.values()) == 4, "L02 polarization count")
    require("all delta_K free" in pol["W01"]["allowed_or_fixed_data"] and "all delta_K free" in pol["W02"]["allowed_or_fixed_data"], "compatible free normal jets")
    require(pol["W01"]["allowed_or_fixed_data"] != pol["W02"]["allowed_or_fixed_data"], "inequivalent compatible pair")
    require(pol["W03"]["UDT_selection_status"] == "NOT_COMPATIBLE_IF_RECIPROCAL_NORMAL_JET_FIXED", "clamp rejection")
    require(pol["W06"]["UDT_selection_status"] == "NOT_COMPATIBLE_IF_RECIPROCAL_NORMAL_JET_FIXED", "EH clamp rejection")
    require(pol["W07"]["UDT_selection_status"] == "NOT_ADOPTED", "GHY unadopted")
    require(pol["W08"]["UDT_selection_status"] == "NOT_SELECTED" and "normal jet free" in pol["W08"]["allowed_or_fixed_data"], "EH alternate witness")
    require(pol["W10"]["mathematical_status"] == "EXCLUDED_NO_BULK_OPERATOR", "L03 excluded")
    require(all(row["UDT_selection_status"] not in {"SELECTED","NATIVE","ADOPTED"} for row in pol.values()), "nothing selected")

    ambiguity = {row["id"]:row for row in tables["FUNCTIONAL_AMBIGUITY.tsv"]}
    require(len(ambiguity) == 8 and set(ambiguity) == {f"F{i:02d}" for i in range(1,9)}, "ambiguity coverage")
    require(ambiguity["F02"]["bulk_equation_effect"] == "zero regular_4D bulk metric equation", "Euler bulk blind")
    require(ambiguity["F02"]["current_selector"] == "NONE", "beta unselected")
    require(ambiguity["F03"]["bulk_equation_effect"] == "unchanged", "divergence ambiguity")
    require("exchanges fixed coordinate and momentum" in ambiguity["F05"]["boundary_effect"], "Legendre ambiguity")
    require(ambiguity["F06"]["current_selector"] == "COMPARISON_ONLY_NOT_UDT", "GHY status")

    closure = tables["FIELD_LANE_CLOSURE.tsv"]
    require(len(closure) == 21 and len({row["pair_id"] for row in closure}) == 21, "field pair coverage")
    require({(row["lane_id"],row["realization_id"]) for row in closure} == {
        (lane,f"C{i:02d}") for lane in ("L01","L02","L03") for i in range(1,8)
    }, "field Cartesian product")
    require(all(row["P06_ready"] == "NO" and row["global_status"] == "UNEVALUATED_OPEN" for row in closure), "P06 and global stop")
    require(sum(row["extra_field_status"] == "METRIC_ONLY_DECLARED" for row in closure) == 2, "metric only rows")
    require(sum(row["boundary_selector_status"] == "EXCLUDED_NO_BULK_OPERATOR" for row in closure) == 7, "L03 rows")

    requirements = {row["id"]:row for row in tables["OPERATOR_BOUNDARY_REQUIREMENTS.tsv"]}
    require(len(requirements) == 11 and requirements["R07"]["status"] == "CONDITIONAL_COMPARISON_ONLY", "operator requirements")
    require(requirements["R08"]["status"] == "EXPOSED_BETA_FREE", "Euler requirement")
    require(requirements["R10"]["status"] == "OPEN" and requirements["R11"]["status"] == "EXCLUDED_NO_OPERATOR", "open branches")

    status = {row["id"]:row for row in tables["STATUS_LEDGER.tsv"]}
    require(len(status) == 18 and status["S03"]["status"] == "FREE_BY_CANON", "status coverage")
    require(status["S11"]["status"] == "REFUTED_FROM_CURRENT_INPUTS", "functional uniqueness")
    require(status["S12"]["status"] == status["S13"]["status"] == "PARTIAL_NATIVE_DATA_MULTIPLE_COMPLETIONS", "lane status")
    require(status["S15"]["status"] == "ACCOUNTED_ZERO_P06_READY" and status["S17"]["status"] == "CLOSED", "P06 stop")
    require(status["S18"]["status"] == MAXIMUM, "status maximum")

    require(graph["schema"] == "udt-pre-p06-boundary-selector-graph-1.0", "graph schema")
    node_ids = {node["id"] for node in graph["nodes"]}
    require(len(node_ids) == len(graph["nodes"]), "graph nodes")
    realized = {(edge["from"],edge["to"]) for edge in graph["edges"]}
    forbidden = {(edge["from"],edge["to"]) for edge in graph["forbidden_edges"]}
    require(all(edge["from"] in node_ids and edge["to"] in node_ids for edge in graph["edges"]), "graph endpoints")
    require(not realized & forbidden, "forbidden graph edge")
    require(("STATIC_SEAL","COMPLETE_OPERATOR") in forbidden and ("COMPLETE_OPERATOR","P06") in forbidden, "graph stop edges")

    lineage = tables["SOURCE_LINEAGE.tsv"]
    require(len(lineage) == 17 and len({row["role"] for row in lineage}) == 17, "lineage coverage")
    for row in lineage:
        require(digest(ROOT / row["path"]) == row["sha256"] == result["source_sha256"][row["role"]], f"source {row['role']}")
    for name, expected in result["table_sha256"].items():
        require(digest(HERE / name) == expected, f"table {name}")


def independent_algebra(checks: dict[str,str]) -> None:
    # Rational reciprocal-family reconstruction at b=2 and D=diag(a,1/a).
    a = Fraction(3,2)
    D = [[a,Fraction(0)],[Fraction(0),1/a]]
    F = [[Fraction(0),Fraction(2)],[Fraction(1,2),Fraction(0)]]
    def mul(A,B):
        return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    require(mul(F,F) == [[1,0],[0,1]], "independent involution")
    require(mul(mul(F,D),F) == [[1/a,0],[0,a]], "independent reciprocal conjugation")
    eta = [[Fraction(-1),0],[0,Fraction(1)]]
    FT = [[F[j][i] for j in range(2)] for i in range(2)]
    require(mul(mul(FT,eta),F) != eta, "independent diagonal readout obstruction")
    checks["independent_reciprocal_involution"]="PASS"

    # A nonzero 3x3 minor of the three registered tangents proves rank three;
    # the two surviving columns are visibly independent after delta_phi=0.
    minor = [[1,-1,0],[1,1,0],[1,0,1]]
    det = (
        minor[0][0]*(minor[1][1]*minor[2][2]-minor[1][2]*minor[2][1])
        - minor[0][1]*(minor[1][0]*minor[2][2]-minor[1][2]*minor[2][0])
        + minor[0][2]*(minor[1][0]*minor[2][1]-minor[1][1]*minor[2][0])
    )
    require(det == 2, "independent tangent rank")
    checks["independent_seal_tangent_rank"]="PASS"

    # New deterministic derivative tensor, independently contracted with the
    # EH P tensor; no generated-table or primary routine is imported.
    D3 = [[[Fraction((d+1)*37+(i+2)*11+(j+3)*5+(i-j)**2) for j in range(4)] for i in range(4)] for d in range(4)]
    for d in range(4):
        for i in range(4):
            for j in range(i):
                D3[d][i][j]=D3[d][j][i]
    for aa in range(4):
        theta=Fraction(0)
        for i in range(4):
            for j in range(4):
                for d in range(4):
                    p=Fraction(int(aa==j)*int(d==i)-int(aa==d)*int(j==i),2)
                    theta += 2*p*D3[d][i][j]
        expected=sum(D3[i][aa][i] for i in range(4))-sum(D3[aa][i][i] for i in range(4))
        require(theta==expected,"independent EH current")
    checks["independent_EH_current"]="PASS"

    # Boundary Legendre transform: coefficient vectors on (dq,dp).
    p,q=Fraction(7),Fraction(5)
    before=(p,Fraction(0)); deltaF=(-p,-q); after=tuple(before[i]+deltaF[i] for i in range(2))
    require(after==(0,-q),"independent Legendre shift")
    checks["independent_boundary_Legendre_ambiguity"]="PASS"

    beta1,beta2,sample=Fraction(2),Fraction(9),Fraction(4)
    require(beta2*sample-beta1*sample==(beta2-beta1)*sample != 0,"independent beta ambiguity")
    checks["independent_Euler_beta_boundary_ambiguity"]="PASS"


def expect_failure(name: str, operation, catches: dict[str,str]) -> None:
    try:
        operation()
    except (AssertionError, KeyError, StopIteration, ValueError):
        catches[name]="PASS"; return
    raise AssertionError(f"mutation passed: {name}")


def main() -> None:
    tracked=[RESULT,HERE/"SELECTOR_DEPENDENCY_GRAPH.json",*[HERE/name for name in TABLES]]
    before={str(path.relative_to(HERE)):digest(path) for path in tracked}
    environment=dict(os.environ); environment["PYTHONDONTWRITEBYTECODE"]="1"; environment["CUDA_VISIBLE_DEVICES"]=""
    replay=subprocess.run([sys.executable,"-B",str(HERE/"derive_boundary_selector.py")],cwd=ROOT,env=environment,text=True,capture_output=True,timeout=300,check=False)
    require(replay.returncode==0 and not replay.stderr,replay.stdout+replay.stderr)
    require(replay.stdout==(HERE/"DERIVATION_TRANSCRIPT.txt").read_text(encoding="utf-8"),"transcript")
    require(before=={str(path.relative_to(HERE)):digest(path) for path in tracked},"deterministic replay")
    result,tables,graph=load(); validate(result,tables,graph)
    checks={"deterministic_replay":"PASS","full_contract":"PASS","source_hash_replay":"PASS","table_hash_replay":"PASS"}
    independent_algebra(checks)
    require(result["check_count"]==54 and len(result["checks"])==54 and set(result["checks"].values())=={"PASS"},"main checks")
    checks["main_checks_reconciled"]="PASS"

    catches:dict[str,str]={}
    bad=copy.deepcopy(result); bad["schema"]="bad"; expect_failure("schema",lambda:validate(bad,tables,graph),catches)
    bad=copy.deepcopy(result); bad["evidence_grade"]="DERIVED"; expect_failure("grade_promotion",lambda:validate(bad,tables,graph),catches)
    bad=copy.deepcopy(result); bad["primary_result"]="UNIQUE"; expect_failure("primary_promotion",lambda:validate(bad,tables,graph),catches)
    bad=copy.deepcopy(result); bad["lane_outcomes"]["L01"]="UNIQUE_NATIVE_POLARIZATION_AND_FUNCTIONAL"; expect_failure("L01_promotion",lambda:validate(bad,tables,graph),catches)
    bad=copy.deepcopy(result); bad["lane_outcomes"]["L02"]="UNIQUE_NATIVE_POLARIZATION_AND_FUNCTIONAL"; expect_failure("L02_promotion",lambda:validate(bad,tables,graph),catches)
    bad=copy.deepcopy(result); bad["counts"]["P06_ready_pairs"]=1; expect_failure("P06_count",lambda:validate(bad,tables,graph),catches)
    bad=copy.deepcopy(result); bad["scope"]["boundary_functional_adopted"]=True; expect_failure("functional_adoption",lambda:validate(bad,tables,graph),catches)
    bad=copy.deepcopy(result); bad["scope"]["boundary_type_selected"]=True; expect_failure("type_selection",lambda:validate(bad,tables,graph),catches)
    bad=copy.deepcopy(result); bad["scope"]["P06_launched"]=True; expect_failure("P06_launch",lambda:validate(bad,tables,graph),catches)

    bt=copy.deepcopy(tables); bt["PRINCIPLE_TO_BOUNDARY_SLOT.tsv"].pop(); expect_failure("missing_principle",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["PRINCIPLE_TO_BOUNDARY_SLOT.tsv"] if r["id"]=="P02")["classification"]="COMPLETE"; expect_failure("seal_overreach",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["PRINCIPLE_TO_BOUNDARY_SLOT.tsv"] if r["id"]=="P02")["normal_jet"]="fixed"; expect_failure("normal_derivative_fixed",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["PRINCIPLE_TO_BOUNDARY_SLOT.tsv"] if r["id"]=="P03")["classification"]="FULL_BOUNDARY"; expect_failure("Reciprocity_overreach",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["PRINCIPLE_TO_BOUNDARY_SLOT.tsv"] if r["id"]=="P04")["classification"]="SELECTED_SECTION"; expect_failure("CSN_section",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["PRINCIPLE_TO_BOUNDARY_SLOT.tsv"] if r["id"]=="P07")["off_shell_status"]="VARIED_FUNCTIONAL"; expect_failure("bootstrap_functional_invented",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["PRINCIPLE_TO_BOUNDARY_SLOT.tsv"] if r["id"]=="P08")["classification"]="UNIQUE"; expect_failure("coframe_unique",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["PRINCIPLE_TO_BOUNDARY_SLOT.tsv"] if r["id"]=="P09")["classification"]="SELECTS_NULL"; expect_failure("surface_selected",lambda:validate(result,bt,graph),catches)

    bt=copy.deepcopy(tables); bt["BOUNDARY_TYPE_BRANCHES.tsv"].pop(); expect_failure("missing_boundary_type",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["BOUNDARY_TYPE_BRANCHES.tsv"] if r["id"]=="T01")["selected_by_current_UDT"]="YES"; expect_failure("fold_selected",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["BOUNDARY_TYPE_BRANCHES.tsv"] if r["id"]=="T02")["L01_operator_coverage"]="reuse non_null split"; expect_failure("null_extrapolation",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["BOUNDARY_TYPE_BRANCHES.tsv"] if r["id"]=="T04")["L01_operator_coverage"]="ordinary terminal wall"; expect_failure("quotient_erased",lambda:validate(result,bt,graph),catches)

    bt=copy.deepcopy(tables); bt["LANE_POLARIZATION_MATRIX.tsv"].pop(); expect_failure("missing_polarization",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["LANE_POLARIZATION_MATRIX.tsv"] if r["id"]=="W01")["allowed_or_fixed_data"]="delta_K=0"; expect_failure("compatible_normal_jet_lost",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); w1=next(r for r in bt["LANE_POLARIZATION_MATRIX.tsv"] if r["id"]=="W01"); next(r for r in bt["LANE_POLARIZATION_MATRIX.tsv"] if r["id"]=="W02")["allowed_or_fixed_data"]=w1["allowed_or_fixed_data"]; expect_failure("counterpair_collapsed",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["LANE_POLARIZATION_MATRIX.tsv"] if r["id"]=="W03")["UDT_selection_status"]="SELECTED"; expect_failure("clamp_adopted",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["LANE_POLARIZATION_MATRIX.tsv"] if r["id"]=="W07")["UDT_selection_status"]="ADOPTED"; expect_failure("GHY_adopted",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["LANE_POLARIZATION_MATRIX.tsv"] if r["id"]=="W08")["allowed_or_fixed_data"]="delta_phi=0"; expect_failure("EH_alternate_normal_jet_erased",lambda:validate(result,bt,graph),catches)

    bt=copy.deepcopy(tables); bt["FUNCTIONAL_AMBIGUITY.tsv"]=[r for r in bt["FUNCTIONAL_AMBIGUITY.tsv"] if r["id"]!="F02"]; expect_failure("Euler_ambiguity_removed",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["FUNCTIONAL_AMBIGUITY.tsv"] if r["id"]=="F02")["current_selector"]="beta=0"; expect_failure("beta_selected",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["FUNCTIONAL_AMBIGUITY.tsv"] if r["id"]=="F03")["bulk_equation_effect"]="changes bulk"; expect_failure("divergence_misclassified",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["FUNCTIONAL_AMBIGUITY.tsv"] if r["id"]=="F06")["current_selector"]="UDT"; expect_failure("GHY_called_UDT",lambda:validate(result,bt,graph),catches)

    bt=copy.deepcopy(tables); bt["FIELD_LANE_CLOSURE.tsv"].pop(); expect_failure("missing_field_pair",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); bt["FIELD_LANE_CLOSURE.tsv"].append(copy.deepcopy(bt["FIELD_LANE_CLOSURE.tsv"][0])); expect_failure("duplicate_field_pair",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["FIELD_LANE_CLOSURE.tsv"] if r["pair_id"]=="L01_C01")["P06_ready"]="YES"; expect_failure("field_pair_promoted",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["FIELD_LANE_CLOSURE.tsv"] if r["pair_id"]=="L02_C02")["extra_field_status"]="METRIC_ONLY_DECLARED"; expect_failure("extra_field_erased",lambda:validate(result,bt,graph),catches)

    bt=copy.deepcopy(tables); next(r for r in bt["OPERATOR_BOUNDARY_REQUIREMENTS.tsv"] if r["id"]=="R07")["status"]="NATIVE"; expect_failure("operator_GHY_promotion",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["OPERATOR_BOUNDARY_REQUIREMENTS.tsv"] if r["id"]=="R08")["status"]="beta=0"; expect_failure("operator_Euler_erased",lambda:validate(result,bt,graph),catches)
    bt=copy.deepcopy(tables); next(r for r in bt["STATUS_LEDGER.tsv"] if r["id"]=="S17")["status"]="OPEN"; expect_failure("P06_opened",lambda:validate(result,bt,graph),catches)

    bg=copy.deepcopy(graph); bg["edges"].append({"from":"STATIC_SEAL","to":"COMPLETE_OPERATOR","relation":"automatic"}); expect_failure("one_wire_called_complete",lambda:validate(result,tables,bg),catches)
    bg=copy.deepcopy(graph); bg["edges"].append({"from":"COMPLETE_OPERATOR","to":"P06","relation":"launch"}); expect_failure("graph_P06_launch",lambda:validate(result,tables,bg),catches)
    bad=copy.deepcopy(result); bad["source_sha256"]["CANON"]="0"*64; expect_failure("source_hash_drift",lambda:validate(bad,tables,graph),catches)
    bad=copy.deepcopy(result); bad["table_sha256"]["STATUS_LEDGER.tsv"]="0"*64; expect_failure("table_hash_drift",lambda:validate(bad,tables,graph),catches)
    require(len(catches)==42 and set(catches.values())=={"PASS"},f"catch count {len(catches)}")

    output={
        "schema":"udt-pre-p06-boundary-selector-verification-1.0","status":"PASS",
        "check_count":len(checks),"checks":checks,"catch_proof_count":len(catches),"catch_proofs":catches,
        "main_result_sha256":digest(RESULT),"main_transcript_sha256":digest(HERE/"DERIVATION_TRANSCRIPT.txt"),
        "scope":{"independent_implementation":True,"generator_imported":False,"CPU_only":True,"solutions_computed":False},
    }
    (HERE/"VERIFICATION_RESULT.json").write_text(json.dumps(output,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    transcript="\n".join([
        "PRE_P06_BOUNDARY_SELECTOR_VERIFICATION=PASS",f"checks={len(checks)}",f"catch_proofs={len(catches)}",
        "generator_imported=NO","boundary_types=5/5","field_pairs=21/21","P06_ready_pairs=0",
        f"main_result_sha256={output['main_result_sha256']}",
    ])+"\n"
    (HERE/"VERIFICATION_TRANSCRIPT.txt").write_text(transcript,encoding="utf-8"); print(transcript,end="")


if __name__=="__main__":
    main()

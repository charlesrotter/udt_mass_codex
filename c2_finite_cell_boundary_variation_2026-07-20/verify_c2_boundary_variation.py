#!/usr/bin/env python3
"""Independent fail-closed verification of the conditional C2 boundary audit."""
from __future__ import annotations
import copy,csv,hashlib,json,subprocess
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
BASE="eb06c7b5157ffb893ee3e6cd1d10de0816a07e3a"
EXPECTED_CENSUS={"CONTEXT_CANDIDATE":1681,"LOAD_BEARING_CANDIDATE":57,
 "EXCLUDED_DUPLICATE_RAW_RECORD":76,"PROVENANCE_OR_COUNTEREXAMPLE_ONLY":1803,
 "EXCLUDED_GENERATED_ORGANIZATION":226}
def need(c,m):
 if not bool(c):raise AssertionError(m)
def rows(name):
 with (HERE/name).open(encoding="utf-8",newline="") as h:return list(csv.DictReader(h,delimiter="\t"))
def one(items,key,value):
 found=[r for r in items if r[key]==value];need(len(found)==1,f"one:{key}:{value}");return found[0]
def validate_census(items):
 need(len(items)==3843 and len({r["path"] for r in items})==3843,"census-count")
 counts={}
 for r in items:
  counts[r["initial_disposition"]]=counts.get(r["initial_disposition"],0)+1
  need(len(r["blob"])==40 and len(r["sha256"])==64 and r["matched_tokens"],"census-fields")
  need(not r["path"].startswith("c2_finite_cell_boundary_variation_2026-07-20/"),"census-feedback")
 need(counts==EXPECTED_CENSUS,"census-dispositions")
 return {"rows":len(items),"dispositions":counts}
def validate_sources(items,census):
 expected={r["path"] for r in census if r["initial_disposition"]=="LOAD_BEARING_CANDIDATE"}
 need(len(items)==57 and len({r["path"] for r in items})==57 and {r["path"] for r in items}==expected,"source-coverage")
 by={r["path"]:r for r in census}
 for r in items:
  data=subprocess.check_output(["git","show",f"{BASE}:{r['path']}"],cwd=ROOT)
  need(hashlib.sha256(data).hexdigest()==by[r["path"]]["sha256"],f"source-sha:{r['path']}")
  blob=subprocess.check_output(["git","rev-parse",f"{BASE}:{r['path']}"],cwd=ROOT,text=True).strip()
  need(blob==by[r["path"]]["blob"],f"source-blob:{r['path']}")
 need(one(items,"path","UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md")["audit_ruling"]=="FOUNDING_SELECTOR","source-csn")
 need(one(items,"path","UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md")["audit_ruling"]=="CARRIER_EXCLUSION","source-carrier")
 need(one(items,"path","c2_rigidity_three_route_zoomout_2026-07-20/NEXT_SCIENTIFIC_DECISION.md")["audit_ruling"]=="QUESTION_ONLY","source-question")
 return {"rows":len(items),"base_hashes_replayed":len(items)}
def validate_table(items,key,expected,field,label):
 need(len(items)==len(expected) and len({r[key] for r in items})==len(expected),f"{label}-count")
 for ident,value in expected.items():need(one(items,key,ident)[field]==value,f"{label}:{ident}")
 return {"rows":len(items),"rulings_checked":len(expected)}
def validate_completeness(items):
 need(len(items)==16 and len({r["layer"] for r in items})==16,"scope-count")
 need(one(items,"layer","unrestricted covariant bulk variation")["status"]=="COMPLETE_IN_CONDITIONAL_ACTION","scope-bulk")
 need(one(items,"layer","non-null boundary decomposition")["status"]=="VERIFIED_WITH_CAVEATS","scope-boundary")
 need(one(items,"layer","external adversarial model review")["status"]=="NOT_PERFORMED","scope-external")
 return {"rows":len(items),"external_review":"NOT_PERFORMED"}
def validate_conventions(items):
 need(len(items)==12 and len({r["id"] for r in items})==12,"convention-count")
 need(one(items,"id","V05")["status"]=="BOUNDED_DIAGNOSTIC","convention-fixed-wall")
 need(one(items,"id","V10")["status"]=="CHOSE_FOR_AUDIT","convention-potential")
 need(one(items,"id","V12")["status"]=="PREREGISTERED_EXCLUSION","convention-completion")
 return {"rows":len(items)}
def validate_derivation(d):
 need(d["result"]=="PASS" and len(d["checks"])==19,"derive-checks")
 need(d["curvature_momentum"]["P_abcd"]=="2 C_abcd","derive-P")
 need(d["non_null_Gaussian_decomposition"]["principal_momentum"]=="P_K^ij=-8 epsilon E^ij; trace-free","derive-PK")
 need(d["CSN"]["pure_variation"]=="delta g_ab=2 sigma g_ab gives Theta=0","derive-CSN")
 need(d["conformally_flat_branch"]["bare_Q_xi"]=="0","derive-flat-Q")
 need(d["selector_ruling"]["physical_boundary_polarization"]=="OPEN_NOT_SELECTED","derive-selector")
 need(d["maximum_conclusion"]=="CONDITIONAL_C2_BARE_BOUNDARY_PHASE_SPACE_AND_CORNER_FLUX_DERIVED; COMMON_SCALE_IS_NULL_AND_CONFORMALLY_FLAT_BARE_CHARGE_VANISHES; PHYSICAL_BOUNDARY_POLARIZATION_REFERENCE_AND_NORMALIZATION_OPEN","derive-max")
 return {"checks":len(d["checks"]),"maximum_conclusion":d["maximum_conclusion"]}
def independent_algebra():
 # Independent diagonal-curvature-operator check of d(C2)=2 C:dR on all six planes.
 planes=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)];ks=sp.symbols("k01 k02 k03 k12 k13 k23")
 ric=[sum(k for k,(a,b) in zip(ks,planes) if i in (a,b)) for i in range(4)];R=2*sum(ks)
 C2=4*sum(k*k for k in ks)-2*sum(r*r for r in ric)+R**2/sp.Integer(3)
 for k,(a,b) in zip(ks,planes):
  Cplane=k-(ric[a]+ric[b])/2+R/6
  need(sp.simplify(sp.diff(C2,k)-8*Cplane)==0,f"independent-P:{a}{b}")
 values=dict(zip(ks,[2,0,0,0,0,3]));need(sp.simplify(C2.subs(values))==sp.Rational(100,3),"product-C2")
 E=[sp.simplify((ks[i]-(ric[0]+ric[j])/2+R/6).subs(values)) for i,j in [(0,1),(1,2),(2,3)]]
 need(E==[sp.Rational(5,3),sp.Rational(-5,6),sp.Rational(-5,6)] and sum(E)==0,"product-E")
 # Independent component-level Gaussian-normal split of the normal derivative term.
 E3=sp.Matrix([[2,1,0],[1,-1,1],[0,1,-1]]);K=sp.Matrix([[1,2,0],[2,0,1],[0,1,3]])
 dh=sp.Matrix([[3,1,2],[1,-2,0],[2,0,1]]);dK=sp.Matrix([[0,2,1],[2,1,-1],[1,-1,-1]])
 contract=lambda A,B:sum(A[i,j]*B[i,j] for i in range(3) for j in range(3))
 cov_dn=2*dK-K*dh-dh*K
 raw=-4*contract(E3,cov_dn)
 split=-8*contract(E3,dK)+8*contract((E3*K+K*E3)/2,dh)
 need(sp.simplify(raw-split)==0,"independent-normal-split");need(sp.trace(E3)==0,"independent-E-trace")
 C,DC,deltah,Ddeltah,eps=sp.symbols("C DC deltah Ddeltah epsilon")
 need(sp.expand(4*eps*C*Ddeltah-(4*eps*(DC*deltah+C*Ddeltah)-4*eps*DC*deltah))==0,"tangent-product-rule")
 sigma,dsigma,T,DT=sp.symbols("sigma dsigma T DT")
 theta=8*dsigma*T-8*sigma*DT
 need(theta.subs({T:0,DT:0})==0,"independent-Weyl-null")
 return {"six_plane_curvature_momentum":"PASS","product_C2":"100/3","product_E":[str(x) for x in E],
  "gaussian_normal_component_split":"PASS","tangential_product_rule":"PASS","pure_Weyl_trace_test":"PASS"}
def source_syntax():
 csn=(ROOT/"UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md").read_text()
 parent=(ROOT/"c2_rigidity_three_route_zoomout_2026-07-20/NEXT_SCIENTIFIC_DECISION.md").read_text()
 need("A native pre-scale bulk law must respect local common-scale neutrality" in csn,"syntax-CSN")
 need("boundary" in parent.lower() and "variation" in parent.lower(),"syntax-parent")
 return {"CSN":"PASS","parent_boundary_seam":"PASS"}
def expect(label,fn):
 try:fn()
 except (AssertionError,KeyError,subprocess.CalledProcessError):return "PASS"
 raise AssertionError(f"catch-did-not-fail:{label}")
def main():
 census=rows("SOURCE_CENSUS.tsv");sources=rows("SOURCE_ADJUDICATION.tsv");eq=rows("EQUATION_LEDGER.tsv")
 bc=rows("BOUNDARY_CLASS_LEDGER.tsv");branches=rows("CANDIDATE_BRANCHES.tsv");conv=rows("CONVENTION_LEDGER.tsv")
 scope=rows("COMPLETENESS_SCOPE.tsv");status=rows("STATUS_LEDGER.tsv");d=json.loads((HERE/"DERIVATION_RESULT.json").read_text())
 eq_expected={f"E{i:02d}":v for i,v in enumerate(["UNIQUE_CONDITIONAL","DERIVED_CONDITIONAL","DERIVED_CONDITIONAL","DERIVED_CONDITIONAL",
  "DERIVED_CONDITIONAL","DERIVED_CONDITIONAL","DERIVED_CONDITIONAL","DERIVED_CONDITIONAL","DERIVED_CONDITIONAL","DERIVED_CONDITIONAL",
  "DERIVED_CONDITIONAL","DERIVED_CONDITIONAL","DERIVED_CONDITIONAL","OBSERVED_EXACT_DIAGNOSTIC","DERIVED_CONDITIONAL","CHARACTERIZED_CONDITIONAL",
  "OPEN_NOT_SELECTED","OPEN"],1)}
 bc_expected={"B01":"ADMISSIBLE_NOT_SELECTED","B02":"ADMISSIBLE_NOT_SELECTED","B03":"ADMISSIBLE_NOT_SELECTED","B04":"ADMISSIBLE_NOT_SELECTED",
  "B05":"OPEN_COMPLETION_FAMILY","B06":"ADMISSIBLE_NOT_SELECTED","B07":"OPEN_MIXED_FAMILY","B08":"OPEN_CORNER_FAMILY","B09":"DEGENERATE_NOT_SELECTOR","B10":"OPEN_OUTSIDE_SLICE"}
 branch_expected={"C01":"DERIVED_CONDITIONAL","C02":"RETAINED_NOT_SELECTED","C03":"RETAINED_NOT_SELECTED","C04":"RETAINED_NOT_SELECTED",
  "C05":"OPEN_CONDITIONAL","C06":"NULL_DIRECTION_RETAINED","C07":"DEGENERATE_BARE_PHASE_SPACE","C08":"NONTRIVIAL_PHASE_SPACE_RETAINED",
  "C09":"OPEN_OUTSIDE_DECOMPOSITION","C10":"OPEN_NOT_DERIVED"}
 status_values=["DERIVED_FROZEN_INHERITED","UNIQUE_CONDITIONAL_FROZEN_INHERITED","DERIVED_CONDITIONAL","DERIVED_CONDITIONAL","VERIFIED_WITH_CAVEATS",
  "DERIVED_CONDITIONAL","DERIVED_CONDITIONAL","NULL_DIRECTION_DERIVED_CONDITIONAL","VANISH_DERIVED_CONDITIONAL","DERIVED_UNNORMALIZED_CONDITIONAL",
  "NOT_DERIVED","NOT_DERIVED","REFUTED_FOR_BARE_C2","NOT_DERIVED_FALSE_INFERENCE","OPEN","OPEN","OPEN","OPEN","OPEN","VERIFIED_WITH_CAVEATS"]
 status_expected={f"S{i:02d}":v for i,v in enumerate(status_values,1)}
 groups={"source_census":validate_census(census),"source_adjudication":validate_sources(sources,census),
  "equations":validate_table(eq,"id",eq_expected,"status","equation"),"boundary_classes":validate_table(bc,"id",bc_expected,"status","boundary-class"),
  "branches":validate_table(branches,"id",branch_expected,"ruling","branch"),"conventions":validate_conventions(conv),
  "completeness":validate_completeness(scope),"status":validate_table(status,"id",status_expected,"status","status"),
  "derivation":validate_derivation(d),"source_syntax":source_syntax(),"independent_algebra":independent_algebra()}
 catches={}
 catches["missing_census_row_rejected"]=expect("census",lambda:validate_census(census[:-1]))
 changed=copy.deepcopy(census);one(changed,"path","LIVE.md")["sha256"]="0"*64
 catches["base_source_mutation_rejected"]=expect("source-hash",lambda:validate_sources(sources,changed))
 catches["missing_source_rejected"]=expect("source",lambda:validate_sources(sources[:-1],census))
 changed=copy.deepcopy(sources);one(changed,"path","UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md")["audit_ruling"]="NATIVE_CARRIER"
 catches["carrier_import_rejected"]=expect("carrier",lambda:validate_sources(changed,census))
 catches["missing_equation_rejected"]=expect("equation",lambda:validate_table(eq[:-1],"id",eq_expected,"status","equation"))
 for ident,bad,label in [("E01","DERIVED_UNCONDITIONAL","action"),("E05","COMPLETE_NULL_WALL","wall"),("E10","SCALE_SELECTED","scale"),
  ("E11","PHYSICAL_VACUUM","flat-vacuum"),("E13","ZERO_PHYSICAL_MASS","mass"),("E16","UNIQUE_BOUNDARY","boundary-selector"),
  ("E17","DERIVED","polarization"),("E18","NORMALIZED_MASS","charge")]:
  changed=copy.deepcopy(eq);one(changed,"id",ident)["status"]=bad
  catches[f"{label}_equation_overclaim_rejected"]=expect(label,lambda changed=changed:validate_table(changed,"id",eq_expected,"status","equation"))
 catches["missing_boundary_class_rejected"]=expect("boundary-class",lambda:validate_table(bc[:-1],"id",bc_expected,"status","boundary-class"))
 for ident,bad,label in [("B01","UDT_SELECTED","clamped"),("B05","NATIVE_COMPLETION","completion"),("B09","ZERO_MASS","flat-charge"),("B10","CLASSIFIED","null-wall")]:
  changed=copy.deepcopy(bc);one(changed,"id",ident)["status"]=bad
  catches[f"{label}_misgrade_rejected"]=expect(label,lambda changed=changed:validate_table(changed,"id",bc_expected,"status","boundary-class"))
 catches["missing_branch_rejected"]=expect("branch",lambda:validate_table(branches[:-1],"id",branch_expected,"ruling","branch"))
 for ident,bad,label in [("C02","SELECTED","clamped-branch"),("C06","REPRESENTATIVE_FIXED","CSN-branch"),("C07","PHYSICAL_MASS_ZERO","flat-branch"),
  ("C09","EXCLUDED","null-branch"),("C10","DERIVED_MASS","charge-branch")]:
  changed=copy.deepcopy(branches);one(changed,"id",ident)["ruling"]=bad
  catches[f"{label}_overclaim_rejected"]=expect(label,lambda changed=changed:validate_table(changed,"id",branch_expected,"ruling","branch"))
 catches["missing_convention_rejected"]=expect("convention",lambda:validate_conventions(conv[:-1]))
 catches["missing_scope_rejected"]=expect("scope",lambda:validate_completeness(scope[:-1]))
 catches["missing_status_rejected"]=expect("status",lambda:validate_table(status[:-1],"id",status_expected,"status","status"))
 for ident,bad,label in [("S02","NATIVE_ACTION_DERIVED","action-status"),("S05","COMPLETE_ALL_WALLS","wall-status"),("S11","DERIVED","selector-status"),
  ("S13","SCALE_SELECTED","CSN-status"),("S14","ZERO_MASS","mass-status"),("S15","DERIVED","completion-status"),("S17","CLOSED","matter-status"),
  ("S18","ELECTRON_CALIBRATED","anchor-status"),("S19","DERIVED","bridge-status"),("S20","SETTLED","grade")]:
  changed=copy.deepcopy(status);one(changed,"id",ident)["status"]=bad
  catches[f"{label}_overclaim_rejected"]=expect(label,lambda changed=changed:validate_table(changed,"id",status_expected,"status","status"))
 changed=copy.deepcopy(d);changed["selector_ruling"]["physical_boundary_polarization"]="DERIVED"
 catches["derivation_selector_mutation_rejected"]=expect("derive-selector",lambda:validate_derivation(changed))
 changed=copy.deepcopy(d);changed["conformally_flat_branch"]["bare_Q_xi"]="normalized physical mass"
 catches["derivation_charge_mutation_rejected"]=expect("derive-charge",lambda:validate_derivation(changed))
 changed=copy.deepcopy(d);changed["maximum_conclusion"]="COMPLETE_NATIVE_ACTION_AND_MASS"
 catches["maximum_overreach_rejected"]=expect("derive-max",lambda:validate_derivation(changed))
 with (HERE/"CATCH_PROOFS.tsv").open("w",encoding="utf-8",newline="") as h:
  w=csv.DictWriter(h,fieldnames=["catch","result"],delimiter="\t",lineterminator="\n");w.writeheader();w.writerows({"catch":k,"result":v} for k,v in sorted(catches.items()))
 out={"schema":"udt-conditional-c2-finite-cell-boundary-verification-1.0","result":"PASS","groups":groups,"catch_proofs":catches,
  "counts":{"census":len(census),"sources":len(sources),"equations":len(eq),"boundary_classes":len(bc),"branches":len(branches),
  "conventions":len(conv),"completeness":len(scope),"status":len(status),"catch_proofs":len(catches)},
  "derivation_sha256":hashlib.sha256((HERE/"DERIVATION_RESULT.json").read_bytes()).hexdigest(),
  "verdict":"BARE_CONDITIONAL_C2_EXPOSES_NON_NULL_BOUNDARY_PHASE_SPACE_AND_CORNER_FLUX_BUT_SELECTS_NO_PHYSICAL_POLARIZATION; COMMON_SCALE_REMAINS_NULL; CONFORMALLY_FLAT_BARE_Q_ZERO_IS_NOT_A_MASS_THEOREM",
  "certification":"VERIFIED-WITH-CAVEATS: independent six-plane curvature-momentum algebra and component Gaussian-normal split; no fresh external-model review",
  "compute":{"cpu_only":True,"gpu_used":False,"sympy":sp.__version__}}
 (HERE/"VERIFICATION_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"result":"PASS","groups":len(groups),"catch_proofs":len(catches),"verdict":out["verdict"]},sort_keys=True))
if __name__=="__main__":main()

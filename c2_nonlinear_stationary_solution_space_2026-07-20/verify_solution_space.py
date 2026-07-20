#!/usr/bin/env python3
"""Independent fail-closed verifier for the nonlinear stationary solution-space tile."""
from __future__ import annotations
import copy,csv,hashlib,json,subprocess
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
import torch
from stationary_c2_engine import DTYPE,curvature_from_metric,eta_derivatives,make_layout,metric_from_coefficients,stationarity
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent;BASE="786d00a05a4475fcd8495645d39ee2897f5185b3"
EXPECTED_CENSUS={"CONTEXT_CANDIDATE":1726,"LOAD_BEARING_CANDIDATE":92,"EXCLUDED_DUPLICATE_RAW_RECORD":88,"PROVENANCE_OR_COUNTEREXAMPLE_ONLY":1802,"EXCLUDED_GENERATED_ORGANIZATION":226}
def need(c,m):
 if not bool(c):raise AssertionError(m)
def rows(name):
 with (HERE/name).open(encoding="utf-8",newline="") as h:return list(csv.DictReader(h,delimiter="\t"))
def one(items,key,value):
 found=[r for r in items if r[key]==value];need(len(found)==1,f"one:{key}:{value}");return found[0]
def validate_census(items):
 need(len(items)==3934 and len({r["path"] for r in items})==3934,"census-count");counts=Counter(r["initial_disposition"] for r in items);need(dict(counts)==EXPECTED_CENSUS,"census-dispositions")
 for r in items:need(len(r["blob"])==40 and len(r["sha256"])==64 and r["matched_tokens"] and not r["path"].startswith("c2_nonlinear_stationary_solution_space_2026-07-20/"),"census-fields")
 return {"rows":len(items),"dispositions":dict(counts)}
def validate_sources(items,census):
 expected={r["path"] for r in census if r["initial_disposition"]=="LOAD_BEARING_CANDIDATE"};need(len(items)==92 and len({r["path"] for r in items})==92 and {r["path"] for r in items}==expected,"source-coverage");by={r["path"]:r for r in census}
 for r in items:
  data=subprocess.check_output(["git","show",f"{BASE}:{r['path']}"],cwd=ROOT);need(hashlib.sha256(data).hexdigest()==by[r["path"]]["sha256"],f"source-sha:{r['path']}");need(subprocess.check_output(["git","rev-parse",f"{BASE}:{r['path']}"],cwd=ROOT,text=True).strip()==by[r["path"]]["blob"],f"source-blob:{r['path']}")
 need(one(items,"path","complete_coframe_seal_involution_2026-07-20/NEXT_SCIENTIFIC_DECISION.md")["audit_ruling"]=="QUESTION_ONLY","source-question");need(one(items,"path","UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md")["audit_ruling"]=="CARRIER_EXCLUSION","source-carrier")
 return {"rows":len(items),"base_hashes_replayed":len(items)}
def validate_raw(raw):
 need(raw["schema"]=="udt-c2-nonlinear-stationary-galerkin-census-1.0" and raw["result"]=="COMPLETE_WITHIN_BUDGET","raw-schema");need(raw["coverage"]=={"attempted":198,"planned":198,"stopped_by_global_budget":False},"raw-coverage");need(raw["controls"]["orders"]==[2,4] and raw["controls"]["sectors"]==["GENERAL","SEAL_EVEN","SEAL_ODD_W"],"raw-controls");need(raw["controls"]["nodes"]==48 and raw["controls"]["validation_nodes"]==96,"raw-grids")
 attempts=raw["attempts"];need(len(attempts)==198,"raw-attempts");counts=Counter(a["status"] for a in attempts);need(counts=={"SOLVE_RESIDUAL_PASS":147,"NO_RESIDUAL_DECREASING_NEWTON_STEP":51},"raw-statuses");by=defaultdict(list)
 for a in attempts:by[(a["order"],a["sector"])].append(a)
 need(len(by)==6 and all(len(v)==33 for v in by.values()),"raw-strata");passed=[a for a in attempts if a["status"]=="SOLVE_RESIDUAL_PASS"];failed=[a for a in attempts if a["status"]!="SOLVE_RESIDUAL_PASS"]
 need(max(a["raw_residual_inf"] for a in passed)<=1e-9,"raw-solve-gate");need(all(a.get("validation",{}).get("result")=="PASS" for a in passed),"raw-validation-count");need(max(a["validation"]["raw_projected_residual_inf"] for a in passed)<=1e-7,"raw-validation-gate");need(max(a["coefficient_norm"] for a in passed)<=1e-6,"raw-round");need(len(raw["clusters"])==6 and sum(len(c["seed_ids"]) for c in raw["clusters"])==147,"raw-clusters");need(all(c["classification"]=="ROUND_GAUGE_FIXED_ORBIT" for c in raw["clusters"]),"raw-cluster-class");need(sum("0.20" in a["seed_id"] for a in failed)==48,"raw-failure-amplitude");need(min(a["raw_residual_inf"] for a in failed)>1e-3,"raw-unresolved")
 return {"attempts":198,"certified":147,"unresolved":51,"strata":6,"clusters":6,"max_solve":max(a["raw_residual_inf"] for a in passed),"max_validation":max(a["validation"]["raw_projected_residual_inf"] for a in passed),"max_coefficient_norm":max(a["coefficient_norm"] for a in passed)}
def validate_summary(result):
 need(result["result"]=="PASS" and len(result["checks"])==22,"summary-checks");need(result["raw_counts"]=={"attempts":198,"certified_reduced_roots":147,"clusters":6,"strata":6,"unresolved_attempt_basins":51},"summary-counts");need(result["primary_observation"]=="ONLY_ROUND_COORDINATE_CSN_ORBIT_OBSERVED_AMONG_147_CERTIFIED_ROOTS_IN_BOUNDED_SEARCH","summary-observation");need(result["solver_caveat"]=="51_PREREGISTERED_ATTEMPT_BASINS_UNRESOLVED; NO_BRANCH_EXCLUSION","summary-caveat");need(result["coframe_ruling"]=="METRIC_ONLY_C2_CANNOT_DISTINGUISH_COFRAME_LIFTS_WITH_IDENTICAL_METRIC_PULLBACK","summary-coframe");need(result["maximum_conclusion"]=="BROAD_ROUND_BASIN_OBSERVED_IN_CONDITIONAL_SMOOTH_CAP_TORIC_STATIONARY_C2_GALERKIN_TILE; DISCONNECTED_LARGE_AMPLITUDE_PHYSICAL_BOUNDARY_NONTORIC_TIME_LIVE_ACTION_AND_UDT_COMPLETION_OPEN","summary-max");return {"checks":22}
def validate_tables(attempts,clusters,unresolved,status,scope):
 need(len(attempts)==6 and {(int(r["order"]),r["sector"]) for r in attempts}=={(p,s) for p in (2,4) for s in ("GENERAL","SEAL_EVEN","SEAL_ODD_W")},"table-attempts");need(sum(int(r["raw_passes"]) for r in attempts)==147 and sum(int(r["unresolved"]) for r in attempts)==51,"table-attempt-counts");need(len(clusters)==6 and all(r["classification"]=="ROUND_GAUGE_FIXED_ORBIT" for r in clusters),"table-clusters");need(len(unresolved)==51 and len({r["id"] for r in unresolved})==51,"table-unresolved");expected={"S01":"UNIQUE_CONDITIONAL","S03":"BOUNDED_SLICE","S07":"OBSERVED_147","S08":"OBSERVED_147_PASS","S11":"BROAD_ROUND_BASIN_LEAD","S12":"OBSERVED_51_UNRESOLVED","S14":"NOT_OBSERVED","S15":"METRICALLY_INDISTINGUISHABLE","S18":"ONLY_ROUND_ORBIT_OBSERVED_IN_BOUNDED_SEARCH","S19":"NOT_REACHED","S20":"OPEN_NOT_TESTED","S21":"OPEN_NOT_TESTED","S22":"OPEN_NOT_TESTED","S23":"OPEN_NOT_ENTERED","S25":"VERIFIED_WITH_CAVEATS"}
 need(len(status)==25 and len({r["id"] for r in status})==25,"status-count")
 for ident,value in expected.items():need(one(status,"id",ident)["status"]==value,f"status:{ident}")
 need(len(scope)==10 and {r["criterion"].split("_",1)[0] for r in scope}=={str(i) for i in range(1,11)},"scope-ten")
 return {"attempt_rows":6,"cluster_rows":6,"unresolved_rows":51,"status_rows":25,"completeness_rows":10}
def ref_metric(eta,coeff):
 x=np.cos(2*eta);T=[1.0,x,2*x*x-1];n=coeff[0]*T[1]+coeff[1]*(T[2]+1);h=coeff[2]*T[0]+coeff[3]*T[1]+coeff[4]*T[2];s=coeff[5]*T[0]+coeff[6]*T[1]+coeff[7]*T[2];w=coeff[8]*T[1]+coeff[9]*(T[2]+1);N=np.exp(n);H=np.exp((1-x*x)*h);S=np.exp(s);c2=np.cos(eta)**2;s2=np.sin(eta)**2;q=np.sin(eta)*np.cos(eta);g=np.zeros((4,4));g[0,0]=-N*N+S*S*w*w;g[1,1]=H*H;g[0,2]=g[2,0]=S*S*w*c2;g[0,3]=g[3,0]=S*S*w*s2;g[2,2]=q*q+S*S*c2*c2;g[2,3]=g[3,2]=-q*q+S*S*c2*s2;g[3,3]=q*q+S*S*s2*s2;return g
def ref_curvature(eta,coeff):
 h=2e-4;g=ref_metric(eta,coeff);gm1=ref_metric(eta-h,coeff);gp1=ref_metric(eta+h,coeff);gm2=ref_metric(eta-2*h,coeff);gp2=ref_metric(eta+2*h,coeff);dg=(gm2-8*gm1+8*gp1-gp2)/(12*h);ddg=(-gp2+16*gp1-30*g+16*gm1-gm2)/(12*h*h);inv=np.linalg.inv(g);dinv=-inv@dg@inv;G=np.zeros((4,4,4));dG=np.zeros_like(G)
 for a in range(4):
  for b in range(4):
   for c in range(4):
    base=np.array([(dg[e,c] if b==1 else 0)+(dg[e,b] if c==1 else 0)-(dg[b,c] if e==1 else 0) for e in range(4)]);var=np.array([(ddg[e,c] if b==1 else 0)+(ddg[e,b] if c==1 else 0)-(ddg[b,c] if e==1 else 0) for e in range(4)]);G[a,b,c]=inv[a]@base/2;dG[a,b,c]=(dinv[a]@base+inv[a]@var)/2
 R=np.zeros((4,4,4,4))
 for a in range(4):
  for b in range(4):
   for c in range(4):
    for d in range(4):R[a,b,c,d]=(dG[a,b,d] if c==1 else 0)-(dG[a,b,c] if d==1 else 0)+sum(G[a,e,c]*G[e,b,d]-G[a,e,d]*G[e,b,c] for e in range(4))
 Ric=np.einsum("abad->bd",R);scalar=np.einsum("ab,ab",inv,Ric);Rlow=np.einsum("ae,ebcd->abcd",g,R);C=np.zeros_like(Rlow)
 for a in range(4):
  for b in range(4):
   for c in range(4):
    for d in range(4):C[a,b,c,d]=Rlow[a,b,c,d]-(g[a,c]*Ric[b,d]-g[a,d]*Ric[b,c]-g[b,c]*Ric[a,d]+g[b,d]*Ric[a,c])/2+scalar*(g[a,c]*g[b,d]-g[a,d]*g[b,c])/6
 C2=np.einsum("abcd,ae,bf,cg,dh,efgh",C,inv,inv,inv,inv,C);return {"g":g,"determinant":np.linalg.det(g),"scalar":scalar,"weyl_squared":C2}
def independent_tensor():
 coeff=np.array([.03,-.02,.04,-.02,.01,-.03,.02,-.015,.05,-.02]);layout=make_layout("GENERAL",2);points=[.31,.73,1.19];eta=torch.tensor(points,dtype=DTYPE,requires_grad=True);tc=torch.tensor(coeff,dtype=DTYPE,requires_grad=True);g,_=metric_from_coefficients(eta,tc,layout);dg,ddg=eta_derivatives(g,eta);primary=curvature_from_metric(g,dg,ddg);errors=[]
 for i,point in enumerate(points):
  ref=ref_curvature(point,coeff);errors.append({"eta":point,"metric":float(np.max(np.abs(g[i].detach().numpy()-ref["g"]))),"determinant":abs(float(primary["determinant"][i])-ref["determinant"]),"scalar":abs(float(primary["scalar"][i])-ref["scalar"]),"weyl_squared":abs(float(primary["weyl_squared"][i])-ref["weyl_squared"])})
 need(max(e["metric"] for e in errors)<1e-13,"tensor-metric");need(max(e["determinant"] for e in errors)<1e-10,"tensor-det");need(max(e["scalar"] for e in errors)<2e-6,"tensor-scalar");need(max(e["weyl_squared"] for e in errors)<2e-5,"tensor-weyl")
 for sector in ("GENERAL","SEAL_EVEN","SEAL_ODD_W"):
  for order in (2,4):
   layout=make_layout(sector,order);zero=torch.zeros(layout.size,dtype=DTYPE,requires_grad=True);need(float(stationarity(zero,layout,96).abs().max())<1e-10,f"round-residual:{sector}:{order}")
 return {"method":"independent NumPy five-point metric derivatives and separate coordinate contraction","profiles":len(points),"errors":errors,"round_strata":6}
def source_syntax():
 pre=(HERE/"PREREGISTRATION.md").read_text();parent=(ROOT/"complete_coframe_seal_involution_2026-07-20/AUDIT_REPORT.md").read_text();shift=(ROOT/"c2_time_fiber_shift_jacobi_2026-07-20/AUDIT_REPORT.md").read_text();need("observing" in pre.lower() and "No solution is rejected" in pre,"syntax-observe");need("147 certified" not in pre and "51_PREREGISTERED" not in pre,"syntax-preregistered-before-outcome");need("metric-only `C^2` solve cannot rank" in pre,"syntax-coframe");need("MULTIPLE_COMPLETIONS" in parent,"syntax-parent");need("nonlinear disconnected shift branches" in shift,"syntax-shift-open");return {"preregistration":"PASS","parent":"PASS","shift":"PASS"}
def expect(label,fn):
 try:fn()
 except (AssertionError,KeyError,subprocess.CalledProcessError):return "PASS"
 raise AssertionError(f"catch-did-not-fail:{label}")
def main():
 census=rows("SOURCE_CENSUS.tsv");sources=rows("SOURCE_ADJUDICATION.tsv");raw=json.loads((HERE/"RAW_ATTEMPTS.json").read_text());summary=json.loads((HERE/"SUMMARY_RESULT.json").read_text());attempts=rows("ATTEMPT_CENSUS.tsv");clusters=rows("CLUSTER_LEDGER.tsv");unresolved=rows("UNRESOLVED_BASIN_LEDGER.tsv");status=rows("STATUS_LEDGER.tsv");scope=rows("COMPLETENESS_MAP.tsv")
 groups={"source_census":validate_census(census),"source_adjudication":validate_sources(sources,census),"raw_census":validate_raw(raw),"summary":validate_summary(summary),"tables":validate_tables(attempts,clusters,unresolved,status,scope),"independent_tensor":independent_tensor(),"source_syntax":source_syntax()};catches={}
 catches["missing_census_rejected"]=expect("census",lambda:validate_census(census[:-1]));changed=copy.deepcopy(census);one(changed,"path","CANON.md")["sha256"]="0"*64;catches["canon_mutation_rejected"]=expect("canon",lambda:validate_sources(sources,changed));catches["missing_source_rejected"]=expect("source",lambda:validate_sources(sources[:-1],census));changed=copy.deepcopy(sources);one(changed,"path","UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md")["audit_ruling"]="NATIVE_CARRIER";catches["carrier_import_rejected"]=expect("carrier",lambda:validate_sources(changed,census))
 changed=copy.deepcopy(raw);changed["attempts"].pop();catches["missing_attempt_rejected"]=expect("attempt",lambda:validate_raw(changed));changed=copy.deepcopy(raw);changed["controls"]["nodes"]=24;catches["grid_mutation_rejected"]=expect("grid",lambda:validate_raw(changed));changed=copy.deepcopy(raw);changed["attempts"][0]["status"]="FILTERED_UNATTRACTIVE";catches["merit_filter_rejected"]=expect("merit",lambda:validate_raw(changed));changed=copy.deepcopy(raw);passed=next(a for a in changed["attempts"] if a["status"]=="SOLVE_RESIDUAL_PASS");passed["validation"]["result"]="FAIL";catches["validation_failure_rejected"]=expect("validation",lambda:validate_raw(changed));changed=copy.deepcopy(raw);passed=next(a for a in changed["attempts"] if a["status"]=="SOLVE_RESIDUAL_PASS");passed["coefficient_norm"]=.1;catches["nonround_cluster_rejected"]=expect("round",lambda:validate_raw(changed));changed=copy.deepcopy(raw);next(a for a in changed["attempts"] if a["status"]!="SOLVE_RESIDUAL_PASS")["status"]="NO_SOLUTION";catches["failure_promotion_rejected"]=expect("failure",lambda:validate_raw(changed));changed=copy.deepcopy(raw);changed["clusters"][0]["classification"]="UNIQUE_UDT_METRIC";catches["cluster_overclaim_rejected"]=expect("cluster",lambda:validate_raw(changed))
 changed=copy.deepcopy(summary);changed["primary_observation"]="UNIQUE_UDT_SOLUTION";catches["summary_uniqueness_rejected"]=expect("summary-unique",lambda:validate_summary(changed));changed=copy.deepcopy(summary);changed["solver_caveat"]="ALL_BASINS_CLOSED";catches["summary_caveat_loss_rejected"]=expect("summary-caveat",lambda:validate_summary(changed));changed=copy.deepcopy(summary);changed["coframe_ruling"]="COFRAME_SELECTED";catches["coframe_promotion_rejected"]=expect("coframe",lambda:validate_summary(changed));changed=copy.deepcopy(summary);changed["maximum_conclusion"]="COMPLETE_ACTION_MASS_DERIVED";catches["maximum_overreach_rejected"]=expect("maximum",lambda:validate_summary(changed))
 catches["missing_attempt_table_rejected"]=expect("attempt-table",lambda:validate_tables(attempts[:-1],clusters,unresolved,status,scope));catches["missing_cluster_rejected"]=expect("cluster-table",lambda:validate_tables(attempts,clusters[:-1],unresolved,status,scope));catches["missing_unresolved_rejected"]=expect("unresolved-table",lambda:validate_tables(attempts,clusters,unresolved[:-1],status,scope));catches["missing_status_rejected"]=expect("status",lambda:validate_tables(attempts,clusters,unresolved,status[:-1],scope));catches["missing_scope_rejected"]=expect("scope",lambda:validate_tables(attempts,clusters,unresolved,status,scope[:-1]))
 for ident,bad,label in [("S01","NATIVE_ACTION","action"),("S03","COMPLETE_METRIC","ansatz"),("S11","UNIQUE_BASIN","basin"),("S12","NO_SOLUTIONS","unresolved"),("S14","PARITY_SELECTED","parity"),("S15","COFRAME_SELECTED","coframe-status"),("S18","UNIQUE_SOLUTION","outcome"),("S19","CLOSED","closure"),("S20","DERIVED_WALL","boundary"),("S21","TIME_LIVE_DERIVED","time"),("S22","S3_NATIVE","topology"),("S23","MASS_DERIVED","mass"),("S25","SETTLED","grade")]:
  changed=copy.deepcopy(status);one(changed,"id",ident)["status"]=bad;catches[f"{label}_overclaim_rejected"]=expect(label,lambda changed=changed:validate_tables(attempts,clusters,unresolved,changed,scope))
 with (HERE/"CATCH_PROOFS.tsv").open("w",encoding="utf-8",newline="") as h:w=csv.DictWriter(h,fieldnames=["catch","result"],delimiter="\t",lineterminator="\n");w.writeheader();w.writerows({"catch":k,"result":v} for k,v in sorted(catches.items()))
 out={"schema":"udt-c2-nonlinear-stationary-solution-space-verification-1.0","result":"PASS","groups":groups,"catch_proofs":catches,"counts":{"groups":len(groups),"catch_proofs":len(catches),"sources":len(sources),"attempts":198,"certified":147,"unresolved":51},"raw_sha256":hashlib.sha256((HERE/"RAW_ATTEMPTS.json").read_bytes()).hexdigest(),"summary_sha256":hashlib.sha256((HERE/"SUMMARY_RESULT.json").read_bytes()).hexdigest(),"verdict":"BROAD_ROUND_BASIN_OBSERVED_IN_CONDITIONAL_SMOOTH_CAP_TORIC_STATIONARY_C2_TILE; 51_ATTEMPT_BASINS_UNRESOLVED; NO_UNIQUENESS_OR_COFRAME_SELECTION","certification":"VERIFIED-WITH-CAVEATS: independent finite-difference tensor reference, exact raw census, source hashes, and mutation catches; no fresh external-model review","compute":{"cpu_only":True,"gpu_used":False}}
 (HERE/"VERIFICATION_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps({"result":"PASS","groups":len(groups),"catch_proofs":len(catches),"verdict":out["verdict"]},sort_keys=True))
if __name__=="__main__":main()

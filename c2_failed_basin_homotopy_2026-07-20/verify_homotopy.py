#!/usr/bin/env python3
"""Fail-closed verifier for the complete-ledger failed-basin homotopy return."""
from __future__ import annotations
import copy,csv,hashlib,json,sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
import torch
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent;PARENT=ROOT/"c2_nonlinear_stationary_solution_space_2026-07-20";sys.path.insert(0,str(PARENT))
from explore_stationary_space import evaluate_gradient,validate
from stationary_c2_engine import DTYPE,make_layout,reduced_action
from full_bach import bach_point
torch.set_num_threads(1)
RAW_SHA="1a8da008545be0a65d9f25899219a9334e4afd0692d5ef1bb7b67b95a817b2e8";OLD_SHA="05583c69d82ed8afb713fa17094a790b7c30146012f4616ef32ed22d5f57586c";INPUT_SHA="0671c58e9684390ce82fa136dc9d2986337efcf5edc63453ecabe3b802197d55"
EXPECTED_CENSUS={"CONTEXT_CANDIDATE":1742,"LOAD_BEARING_CANDIDATE":104,"EXCLUDED_DUPLICATE_RAW_RECORD":92,"PROVENANCE_OR_COUNTEREXAMPLE_ONLY":1802,"EXCLUDED_GENERATED_ORGANIZATION":226}
def need(c,m):
 if not bool(c):raise AssertionError(m)
def rows(name):
 with (HERE/name).open(encoding="utf-8",newline="") as h:return list(csv.DictReader(h,delimiter="\t"))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def endpoint_class(p):return (p.get("endpoint") or {}).get("classification")
def identity_set(raw):return {(p["path_id"],p["status"],endpoint_class(p)) for p in raw["paths"]}
def validate_sources(census,sources):
 need(len(census)==3966 and len({r["path"] for r in census})==3966,"census-count");need(dict(Counter(r["initial_disposition"] for r in census))==EXPECTED_CENSUS,"census-dispositions");expected={r["path"] for r in census if r["initial_disposition"]=="LOAD_BEARING_CANDIDATE"};need(len(sources)==104 and {r["path"] for r in sources}==expected,"source-coverage")
 for r in census:need(len(r["blob"])==40 and len(r["sha256"])==64,"census-hash")
 return {"census_rows":3966,"source_rows":104,"dispositions":EXPECTED_CENSUS}
def validate_input(parent):
 need(digest(PARENT/"RAW_ATTEMPTS.json")==INPUT_SHA,"input-sha");failed=[a for a in parent["attempts"] if a["status"]!="SOLVE_RESIDUAL_PASS"];need(len(failed)==51 and len({(a["order"],a["sector"],a["seed_id"]) for a in failed})==51,"input-identities");return {"failed_identities":51,"sha256":INPUT_SHA}
def validate_raw(raw,old):
 need(digest(HERE/"RAW_HOMOTOPY_PATHS_COMPLETE_LEDGER.json")==RAW_SHA and digest(HERE/"RAW_HOMOTOPY_PATHS_INCOMPLETE_LEDGER.json")==OLD_SHA,"raw-hashes");need(raw["result"]=="COMPLETE_WITHIN_BUDGET" and raw["coverage"]=={"attempted":51,"full_registered_universe":51,"planned":51,"stopped_by_global_budget":False},"coverage");need(raw["status_counts"]=={"ENDPOINT_REACHED":29,"PATH_TIME_LIMIT":22} and raw["endpoint_counts"]=={"ROUND_GAUGE_FIXED_ORBIT":29},"counts");need(identity_set(raw)==identity_set(old) and len(identity_set(raw))==51,"regression-identities")
 paths=raw["paths"];need(len(paths)==51 and len({p["path_id"] for p in paths})==51,"path-count");need(sum(len(p["accepted_steps"]) for p in paths)==1764 and sum(len(p["rejected_steps"]) for p in paths)==6,"state-counts")
 for p in paths:
  need(len(p["initial_coefficients"])==p["size"],f"initial-vector:{p['path_id']}")
  for a in p["accepted_steps"]:need(len(a["coefficients"])==p["size"] and len(a["tangent"])==p["size"]+1 and a["homotopy_residual_inf"]<=1e-9,f"accepted-vector:{p['path_id']}")
  for r in p["rejected_steps"]:need(len(r["predictor_coefficients"])==p["size"] and len(r["last_coefficients"])==p["size"] and r["corrector_history"],f"rejected-vector:{p['path_id']}")
  if p["status"]=="ENDPOINT_REACHED":need(endpoint_class(p)=="ROUND_GAUGE_FIXED_ORBIT" and p["endpoint"]["raw_residual_inf"]<=1e-9 and p["endpoint"]["validation"]["raw_projected_residual_inf"]<=1e-7 and p["endpoint"]["coefficient_norm"]<=1e-6,f"endpoint:{p['path_id']}")
  else:need(p.get("endpoint") is None and p["final_lambda"]>0,"timeout-scope")
 need(Counter((p["order"],p["status"]) for p in paths)=={(2,"ENDPOINT_REACHED"):14,(4,"ENDPOINT_REACHED"):15,(4,"PATH_TIME_LIMIT"):22},"order-split");need(not any(endpoint_class(p) not in {None,"ROUND_GAUGE_FIXED_ORBIT"} for p in paths),"nonround")
 return {"paths":51,"accepted_points":1764,"rejected_steps":6,"round_endpoints":29,"unresolved":22,"identity_regression":51}
def replay_path(p):
 layout=make_layout(p["sector"],p["order"]);q0=np.asarray(p["initial_coefficients"]);f0,_,_=evaluate_gradient(q0,layout,48,False);maximum=0.;difference=0.
 for a in p["accepted_steps"]:
  f,_,_=evaluate_gradient(np.asarray(a["coefficients"]),layout,48,False);observed=float(np.linalg.norm(f-a["lambda"]*f0,np.inf));maximum=max(maximum,observed);difference=max(difference,abs(observed-a["homotopy_residual_inf"]))
 endpoint=p.get("endpoint")
 if endpoint:
  f,_,_=evaluate_gradient(np.asarray(endpoint["coefficients"]),layout,48,False);need(float(np.linalg.norm(f,np.inf))<=1e-9,"endpoint-replay")
 return {"path_id":p["path_id"],"points":len(p["accepted_steps"]),"maximum_recomputed_homotopy_residual_inf":maximum,"maximum_log_difference":difference}
def replay_all(paths):
 with ProcessPoolExecutor(max_workers=4) as pool:items=list(pool.map(replay_path,paths))
 need(sum(x["points"] for x in items)==1764,"replay-count");need(max(x["maximum_recomputed_homotopy_residual_inf"] for x in items)<=1e-9,"replay-gate");need(max(x["maximum_log_difference"] for x in items)<=2e-12,"replay-log")
 return {"paths":51,"points":1764,"maximum_recomputed_homotopy_residual_inf":max(x["maximum_recomputed_homotopy_residual_inf"] for x in items),"maximum_log_difference":max(x["maximum_log_difference"] for x in items)}
def finite_difference_gradient(raw):
 selected=[next(p for p in raw["paths"] if p["order"]==2 and p["sector"]=="GENERAL"),next(p for p in raw["paths"] if p["order"]==4 and p["sector"]=="GENERAL"),next(p for p in raw["paths"] if p["order"]==4 and p["sector"]=="SEAL_EVEN")];items=[];eps=2e-5
 for p in selected:
  layout=make_layout(p["sector"],p["order"]);q=np.asarray(p["initial_coefficients"]);analytic,_,_=evaluate_gradient(q,layout,48,False);finite=[]
  for i in range(layout.size):
   d=np.zeros(layout.size);d[i]=eps;plus=float(reduced_action(torch.tensor(q+d,dtype=DTYPE),layout,48));minus=float(reduced_action(torch.tensor(q-d,dtype=DTYPE),layout,48));finite.append((plus-minus)/(2*eps))
  error=float(np.max(np.abs(np.asarray(finite)-analytic)));scale=1+float(np.max(np.abs(analytic)));need(error/scale<3e-5,f"finite-gradient:{p['path_id']}:{error/scale}");items.append({"path_id":p["path_id"],"size":layout.size,"maximum_absolute_error":error,"scaled_error":error/scale})
 return {"method":"centered finite difference of the reduced action, independent of coefficient autograd","epsilon":eps,"profiles":items,"maximum_scaled_error":max(x["scaled_error"] for x in items)}
def bach_anchor():
 layout=make_layout("SEAL_EVEN",2);q=torch.zeros(layout.size,dtype=DTYPE);items=[]
 for eta in (.02,float(np.pi/4)):
  b=bach_point(torch.tensor(eta,dtype=DTYPE),q,layout).detach().numpy();items.append({"eta":eta,"raw_component_inf":float(np.max(np.abs(b))),"symmetry_error_inf":float(np.max(np.abs(b-b.T)))})
 need(max(x["raw_component_inf"] for x in items)<=1e-6 and max(x["symmetry_error_inf"] for x in items)<=1e-10,"bach-anchor");return {"round_points":items,"boundary":"OPEN_NOT_TESTED"}
def validate_tables(summary):
 census=rows("PATH_CENSUS.tsv");ledger=rows("PATH_STATUS_LEDGER.tsv");folds=rows("FOLD_LEDGER.tsv");status=rows("STATUS_LEDGER.tsv");need(len(census)==6 and len(ledger)==51 and len(folds)==7 and len(status)==22,"table-counts");need(summary["result"]=="PASS" and summary["counts"]=={"accepted_points":1764,"fold_paths":7,"nonround_endpoints":0,"paths":51,"rejected_steps":6,"round_endpoints":29,"unresolved":22},"summary");by={r["id"]:r["status"] for r in status};need(by["S09"]=="OBSERVED_22_UNRESOLVED" and by["S15"]=="NOT_OBSERVED" and by["S19"]=="PARTIALLY_CLOSED_29_ROUND_22_OPEN" and by["S22"]=="VERIFIED_WITH_CAVEATS","status-scope");return {"path_census":6,"path_ledger":51,"folds":7,"statuses":22,"summary_checks":len(summary["checks"])}
def expect(label,fn):
 try:fn()
 except (AssertionError,KeyError,TypeError):return "PASS"
 raise AssertionError("catch-did-not-fail:"+label)
def main():
 census=rows("SOURCE_CENSUS.tsv");sources=rows("SOURCE_ADJUDICATION.tsv");parent=json.loads((PARENT/"RAW_ATTEMPTS.json").read_text());raw=json.loads((HERE/"RAW_HOMOTOPY_PATHS_COMPLETE_LEDGER.json").read_text());old=json.loads((HERE/"RAW_HOMOTOPY_PATHS_INCOMPLETE_LEDGER.json").read_text());summary=json.loads((HERE/"SUMMARY_RESULT.json").read_text())
 groups={"sources":validate_sources(census,sources),"input":validate_input(parent),"raw":validate_raw(raw,old),"state_replay":replay_all(raw["paths"]),"finite_difference_gradient":finite_difference_gradient(raw),"bach_anchor":bach_anchor(),"tables":validate_tables(summary)};catches={}
 mutations=[]
 def add(name,change):
  x=copy.deepcopy(raw);change(x);mutations.append((name,x))
 add("missing_path_rejected",lambda x:x["paths"].pop());add("duplicate_path_rejected",lambda x:x["paths"].append(copy.deepcopy(x["paths"][0])));add("coverage_loss_rejected",lambda x:x["coverage"].update(attempted=50));add("status_count_rejected",lambda x:x["status_counts"].update(PATH_TIME_LIMIT=21));add("endpoint_count_rejected",lambda x:x["endpoint_counts"].update(ROUND_GAUGE_FIXED_ORBIT=30));add("timeout_promoted_rejected",lambda x:next(p for p in x["paths"] if p["status"]=="PATH_TIME_LIMIT").update(status="NO_SOLUTION"));add("nonround_promotion_rejected",lambda x:next(p for p in x["paths"] if p.get("endpoint"))["endpoint"].update(classification="NATIVE_NONROUND_BRANCH"));add("endpoint_residual_rejected",lambda x:next(p for p in x["paths"] if p.get("endpoint"))["endpoint"].update(raw_residual_inf=1e-3));add("endpoint_validation_rejected",lambda x:next(p for p in x["paths"] if p.get("endpoint"))["endpoint"]["validation"].update(raw_projected_residual_inf=1e-3));add("round_norm_rejected",lambda x:next(p for p in x["paths"] if p.get("endpoint"))["endpoint"].update(coefficient_norm=.1));add("missing_coefficients_rejected",lambda x:next(p for p in x["paths"] if p["accepted_steps"])["accepted_steps"][0].pop("coefficients"));add("missing_tangent_rejected",lambda x:next(p for p in x["paths"] if p["accepted_steps"])["accepted_steps"][0].pop("tangent"));add("homotopy_gate_rejected",lambda x:next(p for p in x["paths"] if p["accepted_steps"])["accepted_steps"][0].update(homotopy_residual_inf=1e-3));add("timeout_endpoint_rejected",lambda x:next(p for p in x["paths"] if p["status"]=="PATH_TIME_LIMIT").update(endpoint={"classification":"ROUND_GAUGE_FIXED_ORBIT"}));add("timeout_lambda_rejected",lambda x:next(p for p in x["paths"] if p["status"]=="PATH_TIME_LIMIT").update(final_lambda=-.1));add("order2_open_rejected",lambda x:next(p for p in x["paths"] if p["order"]==2).update(status="PATH_TIME_LIMIT",endpoint=None,final_lambda=.2));
 for name,x in mutations:catches[name]=expect(name,lambda x=x:validate_raw(x,old))
 changed=copy.deepcopy(old);changed["paths"][0]["status"]="ENDPOINT_REACHED";catches["regression_mismatch_rejected"]=expect("regression",lambda:validate_raw(raw,changed));changed=copy.deepcopy(census);changed.pop();catches["census_loss_rejected"]=expect("census",lambda:validate_sources(changed,sources));changed=copy.deepcopy(sources);changed.pop();catches["source_loss_rejected"]=expect("source",lambda:validate_sources(census,changed));changed=copy.deepcopy(summary);changed["counts"]["unresolved"]=0;catches["summary_overclaim_rejected"]=expect("summary",lambda:validate_tables(changed));
 with (HERE/"CATCH_PROOFS.tsv").open("w",encoding="utf-8",newline="") as h:w=csv.DictWriter(h,fieldnames=["catch","result"],delimiter="\t",lineterminator="\n");w.writeheader();w.writerows({"catch":k,"result":v} for k,v in sorted(catches.items()))
 out={"schema":"udt-c2-failed-basin-homotopy-verification-1.0","result":"PASS","groups":groups,"catch_proofs":catches,"counts":{"groups":len(groups),"catch_proofs":len(catches),"paths":51,"accepted_points":1764,"round_endpoints":29,"unresolved":22},"verdict":"29_FORMER_FAILURES_CERTIFIED_ROUND; 22_PATHS_REMAIN_UNRESOLVED; NO_NONROUND_ENDPOINT_OBSERVED","certification":"VERIFIED-WITH-CAVEATS: full saved-state replay, independent finite-difference action gradients, duplicate-run identity agreement, sources and mutation catches; no fresh external-model review","compute":{"cpu_only":True,"gpu_used":False}}
 (HERE/"VERIFICATION_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps({"result":"PASS","groups":len(groups),"catch_proofs":len(catches),"verdict":out["verdict"]},sort_keys=True))
if __name__=="__main__":main()

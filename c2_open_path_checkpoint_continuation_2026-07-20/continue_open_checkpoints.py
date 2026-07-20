#!/usr/bin/env python3
"""Restart the exact 22 open artificial homotopy paths from their saved checkpoints."""
from __future__ import annotations
import argparse,gc,hashlib,json,math,sys,time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
import torch
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent;PARENT_DIR=ROOT/"c2_failed_basin_homotopy_2026-07-20";sys.path.insert(0,str(PARENT_DIR));sys.path.insert(0,str(ROOT/"c2_nonlinear_stationary_solution_space_2026-07-20"))
import continue_failed_basins as h
from stationary_c2_engine import make_layout
from full_bach import bach_tensor_profile
INPUT=PARENT_DIR/"RAW_HOMOTOPY_PATHS_COMPLETE_LEDGER.json";INPUT_SHA="1a8da008545be0a65d9f25899219a9334e4afd0692d5ef1bb7b67b95a817b2e8"
MIN_STEP=.002;MAX_STEP=.10;MAX_CORRECTOR=12;MAX_HALVINGS=8;MAX_POINTS=500;MAX_ARC=20.;MAX_NORM=5.;MAX_LAMBDA=5.;MAX_SECONDS=900.;MAX_WALL=3600.;SOLVE_TOL=1e-9
torch.set_num_threads(1);h.MAX_PATH_SECONDS=MAX_SECONDS

def restart(parent):
 start=time.monotonic();layout=make_layout(parent["sector"],parent["order"]);q0=np.asarray(parent["initial_coefficients"],float);q=np.asarray(parent["final_coefficients"],float);lam=float(parent["final_lambda"]);f0,_,_=h.evaluate(q0,layout,False);f,B,action=h.evaluate(q,layout,True);restart_res=float(np.linalg.norm(f-lam*f0,np.inf));previous_tangent=np.asarray(parent["accepted_steps"][-1]["tangent"],float);tan=h.tangent(B,f0,previous_tangent);ds=min(MAX_STEP,max(MIN_STEP,float(parent["accepted_steps"][-1]["step_size"])));arc=0.;accepted=[];rejected=[];refreshes=1;endpoint=None;status="MAX_POINTS";states=[{"z":np.r_[q,lam],"tangent":tan.copy(),"index":-1}]
 if restart_res>SOLVE_TOL:status="RESTART_RESIDUAL_FAIL"
 else:
  for index in range(MAX_POINTS):
   if time.monotonic()-start>MAX_SECONDS:status="PATH_TIME_LIMIT";break
   if arc>=MAX_ARC:status="ARCLENGTH_LIMIT";break
   if np.linalg.norm(q)>=MAX_NORM:status="COEFFICIENT_SAFETY_LIMIT";break
   if abs(lam)>=MAX_LAMBDA:status="LAMBDA_SAFETY_LIMIT";break
   success=False;previous_q=q.copy();previous_lam=lam
   for halving in range(MAX_HALVINGS+1):
    local=ds*(.5**halving);qp=q+local*tan[:-1];lp=lam+local*tan[-1]
    if local<MIN_STEP:
     rejected.append({"step":index,"halving":halving,"step_size":local,"predictor_coefficients":qp.tolist(),"predictor_lambda":float(lp),"reason":"BELOW_REGISTERED_MINIMUM_STEP"});break
    ok,nq,nl,nB,nf,na,events=h.correct(qp,lp,tan,B,f0,layout)
    if ok:
     q=nq;lam=float(nl);B=nB;f=nf;action=na;arc+=local;success=True;accepted.append({"step":index,"additional_arclength":arc,"step_size":local,"lambda":lam,"coefficients":q.tolist(),"coefficient_norm":float(np.linalg.norm(q)),"action":action,"homotopy_residual_inf":float(np.linalg.norm(f-lam*f0,np.inf)),"corrector_iterations":len(events)-1,"predictor_tangent":tan.tolist(),"exact_refresh":False});ds=min(MAX_STEP,local*(1.25 if len(events)-1<=3 else .75 if len(events)-1>=9 else 1.0));break
    rejected.append({"step":index,"halving":halving,"step_size":local,"predictor_coefficients":qp.tolist(),"predictor_lambda":float(lp),"last_coefficients":nq.tolist(),"last_lambda":float(nl),"last_augmented_residual_inf":events[-1]["augmented_residual_inf"] if events else math.inf,"corrector_history":events})
    if halving==0:_,B,_=h.evaluate(q,layout,True);refreshes+=1
   if not success:status="MINIMUM_STEP_STALL";break
   if (index+1)%2==0:_,B,_=h.evaluate(q,layout,True);refreshes+=1;accepted[-1]["exact_refresh"]=True
   new_tangent=h.tangent(B,f0,tan);accepted[-1]["outgoing_tangent"]=new_tangent.tolist()
   if previous_lam>0 and lam<=0:
    fraction=previous_lam/(previous_lam-lam);guess=previous_q+fraction*(q-previous_q);endpoint=h.endpoint_solve(guess,B,layout,start);status="ENDPOINT_REACHED" if endpoint["status"]=="SOLVE_RESIDUAL_PASS" else "ENDPOINT_UNRESOLVED";tan=new_tangent;break
   z=np.r_[q,lam];loop=None
   if len(states)>=20:
    for old in states[:-19]:
     distance=float(np.linalg.norm(z-old["z"]));alignment=float(new_tangent@old["tangent"])
     if distance<=1e-5 and alignment>=.999:loop={"prior_index":old["index"],"current_index":index,"state_distance":distance,"tangent_alignment":alignment};break
   states.append({"z":z.copy(),"tangent":new_tangent.copy(),"index":index});tan=new_tangent
   if loop is not None:status="CLOSED_HOMOTOPY_LOOP_CANDIDATE";accepted[-1]["loop_witness"]=loop;break
   gc.collect()
 result={"path_id":parent["path_id"],"order":parent["order"],"sector":parent["sector"],"seed_id":parent["source_seed_id"],"size":parent["size"],"parent_status":parent["status"],"parent_final_lambda":parent["final_lambda"],"restart_coefficients":np.asarray(parent["final_coefficients"]).tolist(),"restart_lambda":float(parent["final_lambda"]),"restart_residual_inf":restart_res,"status":status,"elapsed_seconds":time.monotonic()-start,"additional_arclength":arc,"accepted_steps":accepted,"rejected_steps":rejected,"exact_hessian_refreshes":refreshes,"final_coefficients":q.tolist(),"final_lambda":lam,"final_coefficient_norm":float(np.linalg.norm(q)),"endpoint":endpoint}
 if endpoint and endpoint["status"]=="SOLVE_RESIDUAL_PASS":
  proxy={"sector":parent["sector"],"order":parent["order"],"final_coefficients":endpoint["coefficients"]};endpoint["validation"]=h.validate(proxy,48);endpoint["coefficient_norm"]=float(np.linalg.norm(endpoint["coefficients"]));endpoint["classification"]="ROUND_GAUGE_FIXED_ORBIT" if endpoint["coefficient_norm"]<=1e-6 else "DISTINCT_REDUCED_STATIONARY_CANDIDATE"
  if endpoint["classification"]!="ROUND_GAUGE_FIXED_ORBIT":endpoint["bach_32"]=bach_tensor_profile(np.asarray(endpoint["coefficients"]),layout,32);endpoint["bach_64"]=bach_tensor_profile(np.asarray(endpoint["coefficients"]),layout,64);endpoint["full_bach_gate"]="PASS" if max(endpoint["bach_32"]["raw_component_inf"],endpoint["bach_64"]["raw_component_inf"])<=1e-6 else "FAIL"
 return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--workers",type=int,default=8);ap.add_argument("--max-wall-seconds",type=float,default=MAX_WALL);ap.add_argument("--max-paths",type=int);ap.add_argument("--output",type=Path,default=HERE/"RAW_EXTENDED_PATHS.json");ap.add_argument("--transcript",type=Path,default=HERE/"EXTENDED_TRANSCRIPT.txt");args=ap.parse_args()
 if hashlib.sha256(INPUT.read_bytes()).hexdigest()!=INPUT_SHA:raise AssertionError("parent input hash")
 raw=json.loads(INPUT.read_text());open_paths=[p for p in raw["paths"] if p["status"]=="PATH_TIME_LIMIT"]
 if len(open_paths)!=22 or any(p["order"]!=4 or p["final_lambda"]<=0 for p in open_paths):raise AssertionError("open path census")
 selected=open_paths if args.max_paths is None else open_paths[:args.max_paths];transcript=args.transcript.open("w");start=time.monotonic();paths=[];stopped=False
 def emit(x):line=json.dumps(x,sort_keys=True);print(line,flush=True);print(line,file=transcript,flush=True)
 for offset in range(0,len(selected),args.workers):
  batch=selected[offset:offset+args.workers]
  if time.monotonic()-start>args.max_wall_seconds:stopped=True;break
  for p in batch:emit({"event":"RESTART","path_id":p["path_id"],"lambda":p["final_lambda"]})
  with ProcessPoolExecutor(max_workers=args.workers) as pool:completed=list(pool.map(restart,batch))
  for p in completed:paths.append(p);emit({"event":"END","path_id":p["path_id"],"status":p["status"],"final_lambda":p["final_lambda"],"additional_arclength":p["additional_arclength"],"accepted_steps":len(p["accepted_steps"]),"seconds":p["elapsed_seconds"],"endpoint_classification":(p.get("endpoint") or {}).get("classification")})
 counts=Counter(p["status"] for p in paths);endpoint_counts=Counter((p.get("endpoint") or {}).get("classification") for p in paths if p.get("endpoint"));result={"schema":"udt-c2-open-path-checkpoint-continuation-1.0","result":"COMPLETE_WITHIN_BUDGET" if not stopped and len(paths)==len(selected) else "THROUGHPUT_LIMITED","base":"99c57d7800eee2f9f2ebabff34dc6d17a18ed847","parent_sha256":INPUT_SHA,"coverage":{"planned":len(selected),"attempted":len(paths),"full_registered_universe":22,"stopped_by_global_budget":stopped},"controls":{"workers":args.workers,"nodes":48,"solve_tolerance":1e-9,"validation_tolerance":1e-7,"minimum_step":MIN_STEP,"maximum_step":MAX_STEP,"maximum_points":MAX_POINTS,"maximum_additional_arclength":MAX_ARC,"maximum_coefficient_norm":MAX_NORM,"maximum_absolute_lambda":MAX_LAMBDA,"maximum_path_seconds":MAX_SECONDS,"maximum_wall_seconds":args.max_wall_seconds},"elapsed_seconds":time.monotonic()-start,"status_counts":dict(counts),"endpoint_counts":dict(endpoint_counts),"paths":paths,"compute":{"device":"cpu","dtype":"float64"}};args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");emit({"result":result["result"],"attempted":len(paths),"planned":len(selected),"status_counts":dict(counts),"endpoint_counts":dict(endpoint_counts)});transcript.close()
if __name__=="__main__":main()

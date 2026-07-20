#!/usr/bin/env python3
"""Pseudo-arclength Newton homotopy for the 51 frozen unresolved stationary starts."""
from __future__ import annotations
import argparse,gc,hashlib,json,math,sys,time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
import torch
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
PARENT=ROOT/"c2_nonlinear_stationary_solution_space_2026-07-20";sys.path.insert(0,str(PARENT))
from explore_stationary_space import evaluate_gradient,validate
from stationary_c2_engine import make_layout
from full_bach import bach_tensor_profile
RAW=PARENT/"RAW_ATTEMPTS.json";RAW_SHA="0671c58e9684390ce82fa136dc9d2986337efcf5edc63453ecabe3b802197d55"
SOLVE_TOL=1e-9;VALIDATE_TOL=1e-7;INITIAL_STEP=.05;MIN_STEP=.002;MAX_STEP=.10
MAX_CORRECTOR=12;MAX_HALVINGS=8;MAX_STEPS=160;MAX_ARCLENGTH=8.;MAX_NORM=5.;MAX_PATH_SECONDS=180.;MAX_WALL_SECONDS=2400.
torch.set_num_threads(1)

def evaluate(q,layout,hessian=False):return evaluate_gradient(q,layout,48,hessian)
def symmetric_secant(B,s,y):
 den=float(s@s)
 if den<=1e-24:return B
 r=y-B@s
 return B+(np.outer(r,s)+np.outer(s,r))/den-(float(r@s)/(den*den))*np.outer(s,s)
def tangent(B,f0,previous=None):
 A=np.column_stack((B,-f0));_,_,vh=np.linalg.svd(A,full_matrices=True);t=vh[-1];t=t/np.linalg.norm(t)
 if previous is None:
  if t[-1]>0:t=-t
 elif float(t@previous)<0:t=-t
 return t
def residual(q,lam,f0,layout):
 f,_,action=evaluate(q,layout,False);return f-lam*f0,f,action
def correct(qp,lp,tan,B,f0,layout):
 q=qp.copy();lam=float(lp);events=[];f,_,action=evaluate(q,layout,False)
 for iteration in range(MAX_CORRECTOR+1):
  h=f-lam*f0;arc=float(tan@np.r_[q-qp,lam-lp]);norm=max(float(np.linalg.norm(h,np.inf)),abs(arc))
  events.append({"iteration":iteration,"augmented_residual_inf":norm,"homotopy_residual_inf":float(np.linalg.norm(h,np.inf)),"arclength_residual":arc,"lambda":lam,"coefficients":q.tolist(),"coefficient_norm":float(np.linalg.norm(q)),"action":action})
  if norm<=SOLVE_TOL:return True,q,lam,B,f,action,events
  if iteration==MAX_CORRECTOR:return False,q,lam,B,f,action,events
  aug=np.block([[B,-f0[:,None]],[tan[None,:]]]);rhs=-np.r_[h,arc]
  try:step=np.linalg.lstsq(aug,rhs,rcond=1e-12)[0]
  except np.linalg.LinAlgError:return False,q,lam,B,f,action,events
  sn=float(np.linalg.norm(step))
  if sn>.5:step*=.5/sn
  accepted=False
  for power in range(8):
   trial_q=q+(0.5**power)*step[:-1];trial_lam=lam+(0.5**power)*step[-1]
   try:trial_h,trial_f,trial_action=residual(trial_q,trial_lam,f0,layout)
   except (RuntimeError,ValueError,np.linalg.LinAlgError):continue
   trial_arc=float(tan@np.r_[trial_q-qp,trial_lam-lp]);trial_norm=max(float(np.linalg.norm(trial_h,np.inf)),abs(trial_arc))
   if np.isfinite(trial_norm) and trial_norm<norm:
    B=symmetric_secant(B,trial_q-q,trial_f-f);q=trial_q;lam=float(trial_lam);f=trial_f;action=trial_action;accepted=True;break
  if not accepted:return False,q,lam,B,f,action,events
 return False,q,lam,B,f,action,events
def endpoint_solve(initial,B,layout,start_time):
 q=initial.copy();f,_,action=evaluate(q,layout,False);history=[];refreshes=0
 for iteration in range(31):
  res=float(np.linalg.norm(f,np.inf));history.append({"iteration":iteration,"raw_residual_inf":res,"coefficients":q.tolist(),"coefficient_norm":float(np.linalg.norm(q)),"action":action})
  if res<=SOLVE_TOL:return {"status":"SOLVE_RESIDUAL_PASS","coefficients":q.tolist(),"raw_residual_inf":res,"action":action,"history":history,"exact_hessian_refreshes":refreshes}
  if iteration==30 or time.monotonic()-start_time>MAX_PATH_SECONDS:break
  if iteration%6==0:
   f,B,action=evaluate(q,layout,True);refreshes+=1
  step=np.linalg.lstsq(B,-f,rcond=1e-12)[0];sn=float(np.linalg.norm(step))
  if sn>.5:step*=.5/sn
  accepted=False
  for power in range(9):
   trial=q+(0.5**power)*step
   try:tf,_,ta=evaluate(trial,layout,False)
   except (RuntimeError,ValueError,np.linalg.LinAlgError):continue
   if np.isfinite(tf).all() and np.linalg.norm(tf,np.inf)<res:
    B=symmetric_secant(B,trial-q,tf-f);q=trial;f=tf;action=ta;accepted=True;break
  if not accepted:
   f,B,action=evaluate(q,layout,True);refreshes+=1
   step=np.linalg.lstsq(B,-f,rcond=1e-12)[0];trial=q+step
   try:tf,_,ta=evaluate(trial,layout,False)
   except (RuntimeError,ValueError,np.linalg.LinAlgError):break
   if np.linalg.norm(tf,np.inf)>=res:break
   q=trial;f=tf;action=ta
 return {"status":"ENDPOINT_UNRESOLVED","coefficients":q.tolist(),"raw_residual_inf":float(np.linalg.norm(f,np.inf)),"action":action,"history":history,"exact_hessian_refreshes":refreshes}
def trace(attempt):
 start=time.monotonic();layout=make_layout(attempt["sector"],attempt["order"]);q0=np.asarray(attempt["initial_coefficients"],float);f0,B,action=evaluate(q0,layout,True)
 q=q0.copy();lam=1.;tan=tangent(B,f0);ds=INITIAL_STEP;arc=0.;accepted=[];rejected=[];refreshes=1;previous_q=q.copy();previous_lam=lam;status="MAX_STEPS";endpoint=None
 for step_index in range(MAX_STEPS):
  elapsed=time.monotonic()-start
  if elapsed>MAX_PATH_SECONDS:status="PATH_TIME_LIMIT";break
  if arc>=MAX_ARCLENGTH:status="ARCLENGTH_LIMIT";break
  if np.linalg.norm(q)>MAX_NORM:status="COEFFICIENT_SAFETY_LIMIT";break
  success=False
  for halving in range(MAX_HALVINGS+1):
   local=ds*(.5**halving);qp=q+local*tan[:-1];lp=lam+local*tan[-1]
   if local<MIN_STEP:
    rejected.append({"step":step_index,"halving":halving,"step_size":local,"predictor_lambda":float(lp),"last_augmented_residual_inf":math.inf,"reason":"BELOW_REGISTERED_MINIMUM_STEP"});break
   ok,nq,nl,nB,nf,na,events=correct(qp,lp,tan,B,f0,layout)
   if ok:
    previous_q=q.copy();previous_lam=lam;q=nq;lam=nl;B=nB;action=na;arc+=local;success=True
    accepted.append({"step":step_index,"arclength":arc,"step_size":local,"lambda":lam,"coefficients":q.tolist(),"coefficient_norm":float(np.linalg.norm(q)),"action":action,"homotopy_residual_inf":float(np.linalg.norm(nf-lam*f0,np.inf)),"corrector_iterations":len(events)-1,"tangent":tan.tolist(),"tangent_lambda":float(tan[-1]),"exact_refresh":False})
    ds=min(MAX_STEP,local*(1.25 if len(events)-1<=3 else .75 if len(events)-1>=9 else 1.0));break
   rejected.append({"step":step_index,"halving":halving,"step_size":local,"predictor_coefficients":qp.tolist(),"predictor_lambda":float(lp),"last_coefficients":nq.tolist(),"last_lambda":float(nl),"last_augmented_residual_inf":events[-1]["augmented_residual_inf"] if events else math.inf,"corrector_history":events})
   if halving==0:
    _,B,_=evaluate(q,layout,True);refreshes+=1
  if not success:status="MIN_STEP_OR_CORRECTOR_STALL";break
  # Alternating exact curvature Hessians with symmetric secants avoids both stale-matrix
  # step collapse and an exact fourth-order differentiation at every small accepted step.
  # This is stricter than the registered "at least every eight" refresh requirement.
  if (step_index+1)%2==0:
   _,B,_=evaluate(q,layout,True);refreshes+=1;accepted[-1]["exact_refresh"]=True
  new_tan=tangent(B,f0,tan);tan=new_tan
  if previous_lam>0 and lam<=0:
   fraction=previous_lam/(previous_lam-lam);guess=previous_q+fraction*(q-previous_q);endpoint=endpoint_solve(guess,B,layout,start);status="ENDPOINT_REACHED" if endpoint["status"]=="SOLVE_RESIDUAL_PASS" else "ENDPOINT_UNRESOLVED";break
  gc.collect()
 result={"path_id":f"P{attempt['order']}_{attempt['sector']}_{attempt['seed_id']}","source_seed_id":attempt["seed_id"],"sector":attempt["sector"],"order":attempt["order"],"size":attempt["size"],"initial_coefficients":q0.tolist(),"initial_norm":float(np.linalg.norm(q0)),"initial_stationarity_inf":float(np.linalg.norm(f0,np.inf)),"status":status,"elapsed_seconds":time.monotonic()-start,"accepted_steps":accepted,"rejected_steps":rejected,"exact_hessian_refreshes":refreshes,"final_lambda":lam,"final_coefficients":q.tolist(),"final_coefficient_norm":float(np.linalg.norm(q)),"traced_arclength":arc,"endpoint":endpoint}
 if endpoint and endpoint["status"]=="SOLVE_RESIDUAL_PASS":
  proxy={"sector":attempt["sector"],"order":attempt["order"],"final_coefficients":endpoint["coefficients"]};endpoint["validation"]=validate(proxy,48);endpoint["coefficient_norm"]=float(np.linalg.norm(endpoint["coefficients"]));endpoint["classification"]="ROUND_GAUGE_FIXED_ORBIT" if endpoint["coefficient_norm"]<=1e-6 else "DISTINCT_REDUCED_STATIONARY_CANDIDATE"
  if endpoint["classification"]!="ROUND_GAUGE_FIXED_ORBIT":
   endpoint["bach_32"]=bach_tensor_profile(np.asarray(endpoint["coefficients"]),layout,32);endpoint["bach_64"]=bach_tensor_profile(np.asarray(endpoint["coefficients"]),layout,64);endpoint["full_bach_gate"]="PASS" if max(endpoint["bach_32"]["raw_component_inf"],endpoint["bach_64"]["raw_component_inf"])<=1e-6 else "FAIL"
 return result
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--max-paths",type=int);ap.add_argument("--workers",type=int,default=1);ap.add_argument("--max-wall-seconds",type=float,default=MAX_WALL_SECONDS);ap.add_argument("--output",type=Path,default=HERE/"RAW_HOMOTOPY_PATHS.json");ap.add_argument("--transcript",type=Path,default=HERE/"HOMOTOPY_TRANSCRIPT.txt");args=ap.parse_args()
 if hashlib.sha256(RAW.read_bytes()).hexdigest()!=RAW_SHA:raise AssertionError("frozen raw input hash")
 raw=json.loads(RAW.read_text());failed=[a for a in raw["attempts"] if a["status"]!="SOLVE_RESIDUAL_PASS"]
 if len(failed)!=51 or len({(a["order"],a["sector"],a["seed_id"]) for a in failed})!=51:raise AssertionError("failed identity census")
 selected=failed if args.max_paths is None else failed[:args.max_paths];transcript=args.transcript.open("w");start=time.monotonic();paths=[];stopped=False
 def emit(x):line=json.dumps(x,sort_keys=True);print(line,flush=True);print(line,file=transcript,flush=True)
 for offset in range(0,len(selected),args.workers):
  batch=selected[offset:offset+args.workers]
  if time.monotonic()-start>args.max_wall_seconds:stopped=True;break
  for a in batch:emit({"event":"START","order":a["order"],"sector":a["sector"],"seed":a["seed_id"]})
  if args.workers==1:completed=[trace(a) for a in batch]
  else:
   with ProcessPoolExecutor(max_workers=args.workers) as pool:completed=list(pool.map(trace,batch))
  for p in completed:
   paths.append(p);emit({"event":"END","path_id":p["path_id"],"status":p["status"],"final_lambda":p["final_lambda"],"accepted_steps":len(p["accepted_steps"]),"seconds":p["elapsed_seconds"],"endpoint_classification":p.get("endpoint",{}).get("classification") if p.get("endpoint") else None})
 counts=Counter(p["status"] for p in paths);endpoint_counts=Counter(p["endpoint"]["classification"] for p in paths if p.get("endpoint") and p["endpoint"].get("classification"))
 result={"schema":"udt-c2-failed-basin-homotopy-1.0","result":"COMPLETE_WITHIN_BUDGET" if not stopped and len(paths)==len(selected) else "THROUGHPUT_LIMITED","base":"33eaed961d4601019ee59df5ee8aa59fdc105353","input_raw_sha256":RAW_SHA,"controls":{"nodes":48,"solve_tolerance":SOLVE_TOL,"validation_tolerance":VALIDATE_TOL,"initial_step":INITIAL_STEP,"minimum_step":MIN_STEP,"maximum_step":MAX_STEP,"maximum_corrector_iterations":MAX_CORRECTOR,"maximum_halvings":MAX_HALVINGS,"maximum_steps":MAX_STEPS,"maximum_arclength":MAX_ARCLENGTH,"maximum_coefficient_norm":MAX_NORM,"maximum_path_seconds":MAX_PATH_SECONDS,"maximum_wall_seconds":args.max_wall_seconds},"coverage":{"planned":len(selected),"attempted":len(paths),"full_registered_universe":51,"stopped_by_global_budget":stopped},"elapsed_seconds":time.monotonic()-start,"status_counts":dict(counts),"endpoint_counts":dict(endpoint_counts),"paths":paths,"compute":{"device":"cpu","dtype":"float64"}}
 args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");emit({"result":result["result"],"attempted":len(paths),"planned":len(selected),"status_counts":dict(counts),"endpoint_counts":dict(endpoint_counts)});transcript.close()
if __name__=="__main__":main()

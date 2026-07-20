#!/usr/bin/env python3
"""Bounded deterministic Galerkin census for the conditional nonlinear stationary C2 tile."""
from __future__ import annotations

import argparse
import gc
import json
import math
import time
from pathlib import Path

import numpy as np
import torch

from stationary_c2_engine import DTYPE, SpectralLayout, make_layout, reduced_action, stationarity


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "RAW_ATTEMPTS.json"
DEFAULT_TRANSCRIPT = HERE / "SOLVE_TRANSCRIPT.txt"
SEED = 20260720  # NUMERICAL_CONTROL: preregistered deterministic mixed directions.
SOLVE_TOL = 1.0e-9  # NUMERICAL_CONTROL: preregistered raw stationarity gate.
VALIDATE_TOL = 1.0e-7  # NUMERICAL_CONTROL: preregistered doubled-grid/higher-mode gate.
TRUST_RADIUS = 0.5  # NUMERICAL_CONTROL: coefficient-space Newton safeguard.


def field_index(layout: SpectralLayout, name: str) -> int | None:
    section = layout.slices[name]
    return section.start if section.stop > section.start else None


def seeds(layout: SpectralLayout) -> list[tuple[str, np.ndarray]]:
    result: list[tuple[str, np.ndarray]] = [("ZERO", np.zeros(layout.size))]
    # One canonical direction per retained field sector, both signs and both preregistered norms.
    for name in "nhsw":
        index = field_index(layout, name)
        if index is None:
            continue
        for amplitude in (0.05, 0.20):  # NUMERICAL_CONTROL: preregistered seed amplitudes.
            for sign in (-1.0, 1.0):
                value = np.zeros(layout.size); value[index] = sign * amplitude
                result.append((f"SINGLE_{name.upper()}_{sign:+.0f}_{amplitude:.2f}", value))
    rng = np.random.default_rng(SEED + layout.order + sum(ord(c) for c in layout.sector))
    directions = []
    for _ in range(8):  # NUMERICAL_CONTROL: preregistered mixed-direction count.
        direction = rng.normal(size=layout.size); direction /= np.linalg.norm(direction)
        directions.append(direction)
    for number, direction in enumerate(directions):
        for amplitude in (0.05, 0.20):
            result.append((f"MIXED_{number:02d}_{amplitude:.2f}", amplitude * direction))
    return result


def evaluate_gradient(values: np.ndarray, layout: SpectralLayout, nodes: int,
                      with_hessian: bool) -> tuple[np.ndarray, np.ndarray | None, float]:
    coefficients = torch.tensor(values, dtype=DTYPE, requires_grad=True)
    if with_hessian:
        def gradient(variable: torch.Tensor) -> torch.Tensor:
            return stationarity(variable, layout, nodes, create_graph=True)
        raw = gradient(coefficients)
        hessian = torch.autograd.functional.jacobian(gradient, coefficients, vectorize=True)
        matrix = ((hessian + hessian.T) / 2).detach().cpu().numpy()
    else:
        raw = stationarity(coefficients, layout, nodes, create_graph=False)
        matrix = None
    action = float(reduced_action(coefficients, layout, nodes).detach().cpu())
    return raw.detach().cpu().numpy(), matrix, action


def root_attempt(seed_id: str, initial: np.ndarray, initial_jacobian: np.ndarray,
                 layout: SpectralLayout, nodes: int, max_iterations: int,
                 max_seconds: float) -> dict[str, object]:
    start = time.monotonic(); values = initial.copy(); history=[]; status="MAX_ITERATIONS"
    jacobian = initial_jacobian.copy()
    try:
        gradient,_,action=evaluate_gradient(values,layout,nodes,with_hessian=False)
    except (RuntimeError,ValueError,np.linalg.LinAlgError) as error:
        return {"seed_id":seed_id,"sector":layout.sector,"order":layout.order,"size":layout.size,
                "initial_coefficients":initial.tolist(),"final_coefficients":values.tolist(),
                "status":f"NUMERIC_EXCEPTION:{type(error).__name__}","iterations":0,
                "elapsed_seconds":time.monotonic()-start,"raw_residual_inf":math.inf,
                "action":math.nan,"coefficient_norm":float(np.linalg.norm(values)),"history":[]}
    for iteration in range(max_iterations + 1):
        if time.monotonic() - start > max_seconds:
            status="ATTEMPT_TIME_LIMIT";break
        residual=float(np.linalg.norm(gradient,ord=np.inf));coefficient_norm=float(np.linalg.norm(values))
        condition=float(np.linalg.cond(jacobian)) if np.all(np.isfinite(jacobian)) else math.inf
        history.append({"iteration":iteration,"raw_residual_inf":residual,"action":action,
                        "coefficient_norm":coefficient_norm,"hessian_condition":condition})
        if not np.isfinite(residual) or not np.all(np.isfinite(values)):
            status="NONFINITE";break
        if residual <= SOLVE_TOL:
            status="SOLVE_RESIDUAL_PASS";break
        if iteration == max_iterations:
            break
        step=np.linalg.lstsq(jacobian,-gradient,rcond=1.0e-12)[0]  # NUMERICAL_CONTROL: SVD cutoff.
        step_norm=float(np.linalg.norm(step))
        if step_norm>TRUST_RADIUS:step*=TRUST_RADIUS/step_norm
        accepted=False;trial_gradient=None;trial_action=None;trial=None
        for half_power in range(8):  # NUMERICAL_CONTROL: bounded residual line search.
            trial=values+(0.5**half_power)*step
            try:trial_gradient,_,trial_action=evaluate_gradient(trial,layout,nodes,with_hessian=False)
            except (RuntimeError,ValueError):continue
            trial_residual=float(np.linalg.norm(trial_gradient,ord=np.inf))
            if np.isfinite(trial_residual) and trial_residual<residual:
                accepted=True;break
        if not accepted:
            status="NO_RESIDUAL_DECREASING_NEWTON_STEP";break
        displacement=trial-values;gradient_change=trial_gradient-gradient
        denominator=float(displacement@displacement)
        if denominator>1.0e-24:  # NUMERICAL_CONTROL: avoid a vacuous Broyden update.
            jacobian=jacobian+np.outer(gradient_change-jacobian@displacement,displacement)/denominator
            jacobian=(jacobian+jacobian.T)/2
        values=trial;gradient=trial_gradient;action=float(trial_action)
        gc.collect()
    final_gradient,_,final_action=evaluate_gradient(values,layout,nodes,with_hessian=False)
    return {"seed_id":seed_id,"sector":layout.sector,"order":layout.order,"size":layout.size,
            "initial_coefficients":initial.tolist(),"final_coefficients":values.tolist(),
            "status":status,"iterations":len(history)-1,"elapsed_seconds":time.monotonic()-start,
            "raw_residual_inf":float(np.linalg.norm(final_gradient,ord=np.inf)),"action":final_action,
            "coefficient_norm":float(np.linalg.norm(values)),"history":history}


def embed(values: np.ndarray, source: SpectralLayout, target: SpectralLayout) -> np.ndarray:
    output=np.zeros(target.size)
    for name in "nhsw":
        source_degrees=getattr(source,f"{name}_degrees");target_degrees=getattr(target,f"{name}_degrees")
        source_values=values[source.slices[name]];lookup=dict(zip(source_degrees,source_values))
        for offset,degree in enumerate(target_degrees):
            if degree in lookup:output[target.slices[name].start+offset]=lookup[degree]
    return output


def validate(attempt: dict[str, object], nodes: int) -> dict[str, object]:
    layout=make_layout(str(attempt["sector"]),int(attempt["order"]));higher=make_layout(layout.sector,layout.order+2)
    values=embed(np.asarray(attempt["final_coefficients"],dtype=float),layout,higher)
    gradient,_,action=evaluate_gradient(values,higher,nodes*2,with_hessian=False)
    residual=float(np.linalg.norm(gradient,ord=np.inf))
    return {"higher_order":higher.order,"higher_size":higher.size,"doubled_nodes":nodes*2,
            "raw_projected_residual_inf":residual,"action":action,
            "result":"PASS" if residual<=VALIDATE_TOL else "FAIL"}


def cluster(attempts: list[dict[str, object]]) -> list[dict[str, object]]:
    clusters=[]
    for attempt in attempts:
        if attempt["status"]!="SOLVE_RESIDUAL_PASS" or attempt.get("validation",{}).get("result")!="PASS":continue
        values=np.asarray(attempt["final_coefficients"],dtype=float);assigned=None
        for item in clusters:
            if item["sector"]==attempt["sector"] and item["order"]==attempt["order"]:
                distance=float(np.linalg.norm(values-np.asarray(item["representative_coefficients"])))
                if distance<=1.0e-5:assigned=item;break  # NUMERICAL_CONTROL: preregistered branch match.
        if assigned is None:
            assigned={"cluster_id":f"C{len(clusters)+1:03d}","sector":attempt["sector"],
                      "order":attempt["order"],"representative_coefficients":values.tolist(),
                      "coefficient_norm":float(np.linalg.norm(values)),"seed_ids":[]}
            clusters.append(assigned)
        assigned["seed_ids"].append(attempt["seed_id"])
    for item in clusters:
        item["classification"]="ROUND_GAUGE_FIXED_ORBIT" if item["coefficient_norm"]<=1.0e-6 else "DISTINCT_REDUCED_STATIONARY_CANDIDATE"
    return clusters


def main() -> None:
    parser=argparse.ArgumentParser();parser.add_argument("--orders",nargs="+",type=int,default=[2,4]);parser.add_argument("--sectors",nargs="+",default=["GENERAL","SEAL_EVEN","SEAL_ODD_W"]);parser.add_argument("--nodes",type=int,default=48);parser.add_argument("--max-iterations",type=int,default=30);parser.add_argument("--max-attempt-seconds",type=float,default=60);parser.add_argument("--max-wall-seconds",type=float,default=1200);parser.add_argument("--output",type=Path,default=DEFAULT_OUTPUT);parser.add_argument("--transcript",type=Path,default=DEFAULT_TRANSCRIPT);args=parser.parse_args()
    transcript=args.transcript.open("w",encoding="utf-8")
    def emit(record: dict[str, object]) -> None:
        line=json.dumps(record,sort_keys=True);print(line,flush=True);print(line,file=transcript,flush=True)
    global_start=time.monotonic();attempts=[];stopped=False
    layouts=[make_layout(sector,order) for order in args.orders for sector in args.sectors]
    seed_sets={f"{layout.order}:{layout.sector}":seeds(layout) for layout in layouts}
    jacobians={}
    for layout in layouts:
        key=f"{layout.order}:{layout.sector}";zero=np.zeros(layout.size)
        _,matrix,_=evaluate_gradient(zero,layout,args.nodes,with_hessian=True);jacobians[key]=matrix
    # Interleave all registered orders/sectors so a hard wall stop cannot hide an entire stratum.
    for seed_number in range(max(len(seed_sets[f"{layout.order}:{layout.sector}"]) for layout in layouts)):
        for layout in layouts:
            key=f"{layout.order}:{layout.sector}";registered=seed_sets[key]
            if seed_number>=len(registered):continue
            seed_id,initial=registered[seed_number]
            if time.monotonic()-global_start>args.max_wall_seconds:
                stopped=True;break
            emit({"event":"START","order":layout.order,"sector":layout.sector,"seed":seed_id})
            attempt=root_attempt(seed_id,initial,jacobians[key],layout,args.nodes,args.max_iterations,args.max_attempt_seconds)
            if attempt["status"]=="SOLVE_RESIDUAL_PASS":attempt["validation"]=validate(attempt,args.nodes)
            attempts.append(attempt)
            emit({"event":"END","order":layout.order,"sector":layout.sector,"seed":seed_id,
                  "status":attempt["status"],"residual":attempt["raw_residual_inf"],
                  "seconds":attempt["elapsed_seconds"]})
        if stopped:break
    clusters=cluster(attempts);counts={}
    for attempt in attempts:counts[attempt["status"]]=counts.get(attempt["status"],0)+1
    result={"schema":"udt-c2-nonlinear-stationary-galerkin-census-1.0","result":"COMPLETE_WITHIN_BUDGET" if not stopped else "THROUGHPUT_LIMITED","controls":{"orders":args.orders,"sectors":args.sectors,"nodes":args.nodes,"validation_nodes":args.nodes*2,"solve_tolerance":SOLVE_TOL,"validation_tolerance":VALIDATE_TOL,"max_iterations":args.max_iterations,"max_attempt_seconds":args.max_attempt_seconds,"max_wall_seconds":args.max_wall_seconds,"seed":SEED},"elapsed_seconds":time.monotonic()-global_start,"attempts":attempts,"status_counts":counts,"clusters":clusters,"coverage":{"attempted":len(attempts),"planned":sum(len(seeds(make_layout(s,p))) for p in args.orders for s in args.sectors),"stopped_by_global_budget":stopped},"compute":{"device":"cpu","dtype":"float64","torch":torch.__version__}}
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    emit({"result":result["result"],"attempted":len(attempts),"planned":result["coverage"]["planned"],"clusters":len(clusters),"status_counts":counts});transcript.close()


if __name__=="__main__":main()

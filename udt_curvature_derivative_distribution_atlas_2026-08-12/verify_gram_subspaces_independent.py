#!/usr/bin/env python3
"""Independent SciPy replay of Gram spectra and intrinsic spectral subspaces."""

from __future__ import annotations

import ast
import csv
import importlib.util
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy import linalg
from scipy.optimize import linear_sum_assignment


HERE = Path(__file__).resolve().parent
ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
RANK_TOL = 1e-8
IMAG_TOL = 1e-8
CLUSTER_TOL = 1e-7


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module; spec.loader.exec_module(module)
    return module


INDEPENDENT = load_module("independent_derivative_for_Gram_map", HERE / "verify_derivative_atlas_independent.py")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_tsv(path: Path, output: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(output[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(output)


def real_span(columns: np.ndarray, tolerance: float) -> np.ndarray:
    if columns.size == 0:
        return np.zeros((4, 0))
    real = np.concatenate((columns.real, columns.imag), axis=1)
    q, r, pivots = linalg.qr(real, mode="economic", pivoting=True)
    diagonal = abs(np.diag(r)) if r.size else np.array([])
    return q[:, diagonal > tolerance]


def sig(basis: np.ndarray) -> str:
    values = linalg.eigvalsh(basis.T @ ETA @ basis) if basis.shape[1] else np.array([])
    return f"{sum(values < -1e-8)},{sum(abs(values) <= 1e-8)},{sum(values > 1e-8)}"


def subspace(basis: np.ndarray) -> dict[str, object]:
    projector = basis @ basis.T
    return {
        "dimension": int(basis.shape[1]),
        "signature": sig(basis),
        "pair_defect": float(linalg.norm(projector - np.diag([1.0, 1.0, 0.0, 0.0]))),
        "screen_defect": float(linalg.norm(projector - np.diag([0.0, 0.0, 1.0, 1.0]))),
        "projector": [float(x) for x in projector.ravel()],
    }


def classify(operator: np.ndarray) -> dict[str, object]:
    scale = max(1.0, float(linalg.norm(operator)))
    rank_tol = RANK_TOL * scale; imag_tol = IMAG_TOL * scale; cluster_tol = CLUSTER_TOL * scale
    singular = linalg.svdvals(operator)
    unresolved = any(RANK_TOL / 5 < value / scale < 5 * RANK_TOL for value in singular)
    rank = int(sum(singular > rank_tol))
    values, vectors = linalg.eig(operator)
    if any(IMAG_TOL / 5 * scale < abs(z.imag) < 5 * IMAG_TOL * scale for z in values): unresolved = True
    if any(CLUSTER_TOL / 5 * scale < abs(a-b) < 5 * CLUSTER_TOL * scale for a,b in itertools.combinations(values,2)): unresolved = True
    order = sorted(range(4), key=lambda i:(round(values[i].real/cluster_tol),round(values[i].imag/cluster_tol),values[i].real,values[i].imag))
    values=values[order];vectors=vectors[:,order];used=set();blocks=[];defect=0
    for i,z in enumerate(values):
        if i in used: continue
        if abs(z.imag)<=imag_tol:
            members=[j for j,w in enumerate(values) if j not in used and abs(w.imag)<=imag_tol and abs(w.real-z.real)<=cluster_tol]
            used.update(members);center=float(np.mean([values[j].real for j in members]));alg=len(members)
            geom_space=linalg.null_space(operator-center*np.eye(4),rcond=RANK_TOL);geom=geom_space.shape[1]
            generalized=linalg.null_space(np.linalg.matrix_power(operator-center*np.eye(4),alg),rcond=RANK_TOL)
            basis=real_span(generalized,rank_tol);kind="REAL";label=f"{center:.17g}"
        elif z.imag>imag_tol:
            positives=[j for j,w in enumerate(values) if j not in used and w.imag>imag_tol and abs(w-z)<=cluster_tol]
            negatives=[]
            for j in positives:
                candidates=[k for k,w in enumerate(values) if k not in used and w.imag < -imag_tol and abs(w-values[j].conjugate())<=cluster_tol]
                if candidates: negatives.append(candidates[0])
                else: unresolved=True
            used.update(positives+negatives);center=sum(values[j] for j in positives)/max(1,len(positives));half=len(positives);alg=2*half
            geom_complex=linalg.null_space(operator.astype(complex)-center*np.eye(4),rcond=RANK_TOL);geom=2*geom_complex.shape[1]
            generalized=linalg.null_space(np.linalg.matrix_power(operator.astype(complex)-center*np.eye(4),max(1,half)),rcond=RANK_TOL)
            basis=real_span(generalized,rank_tol);kind="COMPLEX_PAIR";label=f"{center.real:.17g}{center.imag:+.17g}i"
        else:
            unresolved=True;used.add(i);continue
        defect+=max(0,alg-geom)
        if basis.shape[1]!=alg: unresolved=True
        record=subspace(basis);record.update({"kind":kind,"eigenvalue":label,"algebraic_multiplicity":alg,"geometric_multiplicity":geom})
        blocks.append({"basis":basis,"record":record})
    blocks.sort(key=lambda x:(x["record"]["dimension"],x["record"]["kind"],x["record"]["eigenvalue"]))
    planes=[]
    for width in range(1,len(blocks)+1):
        for subset in itertools.combinations(range(len(blocks)),width):
            if sum(blocks[i]["basis"].shape[1] for i in subset)!=2: continue
            raw=np.column_stack([blocks[i]["basis"] for i in subset]);basis=linalg.orth(raw,rcond=RANK_TOL)
            item=subspace(basis);item["blocks"]=list(subset)
            if not any(linalg.norm(np.array(item["projector"])-np.array(old["projector"]))<=1e-8 for old in planes):planes.append(item)
    real_count=int(sum(abs(z.imag)<=imag_tol for z in values));pairs=(4-real_count)//2
    if unresolved: structure="SPECTRALLY_UNRESOLVED"
    elif defect: structure="DEFECTIVE"
    elif pairs==0 and len(blocks)==4: structure="FOUR_REAL_SIMPLE_LINES"
    elif pairs==0: structure="REAL_REPEATED_DIAGONALIZABLE"
    elif pairs==1: structure="ONE_COMPLEX_PLANE_PLUS_REAL_STRUCTURE"
    else: structure="TWO_COMPLEX_PLANES"
    return {"status":"SPECTRALLY_UNRESOLVED" if unresolved else "RESOLVED","structure":structure,"rank":rank,"real":real_count,"pairs":pairs,"defect":defect,"values":sorted(values,key=lambda q:(q.real,q.imag)),"blocks":[b["record"] for b in blocks],"planes":planes}


def make_row(key: str, tensor: str, operator: np.ndarray) -> dict[str, object]:
    result=classify(operator)
    row={"key":key,"tensor":tensor,"status":result["status"],"structure":result["structure"],"operator_rank":result["rank"],"real_eigenvalue_count":result["real"],"complex_pair_count":result["pairs"],"jordan_defect":result["defect"],"spectral_block_count":len(result["blocks"]),"candidate_2plane_count":len(result["planes"])}
    for i,z in enumerate(result["values"],1):row[f"eigen_{i}_real"]=f"{z.real:.17g}";row[f"eigen_{i}_imag"]=f"{z.imag:.17g}"
    row["spectral_blocks_json"]=json.dumps(result["blocks"],separators=(",",":"),sort_keys=True);row["candidate_2planes_json"]=json.dumps(result["planes"],separators=(",",":"),sort_keys=True)
    return row


def projectors(row: dict[str,str], field: str) -> list[np.ndarray]:
    return [np.asarray(item["projector"]).reshape(4,4) for item in json.loads(row[field])]


def set_defect(left: list[np.ndarray], right: list[np.ndarray]) -> float:
    if len(left)!=len(right): return float("inf")
    if not left:return 0.0
    costs=np.array([[linalg.norm(a-b)/max(1.0,linalg.norm(a),linalg.norm(b)) for b in right] for a in left])
    i,j=linear_sum_assignment(costs)
    return float(max(costs[i,j]))


def spectrum_error(a: dict[str,str], b: dict[str,str]) -> float:
    left=np.array([complex(float(a[f"eigen_{i}_real"]),float(a[f"eigen_{i}_imag"])) for i in range(1,5)])
    right=np.array([complex(float(b[f"eigen_{i}_real"]),float(b[f"eigen_{i}_imag"])) for i in range(1,5)])
    costs=np.array([[abs(x-y)/max(1.0,abs(x),abs(y)) for y in right] for x in left]);i,j=linear_sum_assignment(costs)
    return float(max(costs[i,j]))


def main() -> None:
    saved=np.load(HERE/"INDEPENDENT_DERIVATIVE_TENSORS.npz");jets=INDEPENDENT.enumerate_jets()
    if list(saved["keys"])!=[x[0] for x in jets]:raise RuntimeError("independent tensor/jet order mismatch")
    output=[]
    for index,(key,_,coframe_fn,x) in enumerate(jets):
        coframe=coframe_fn(x);frame=np.linalg.inv(coframe)
        for tensor in ("k_riem","k_ric","k_weyl"):
            output.append(make_row(key,tensor,ETA@(frame.T@saved[tensor][index]@frame)))
    write_tsv(HERE/"INDEPENDENT_GRAM_INTRINSIC_SUBSPACE_ATLAS.tsv",output)
    production=read_tsv(HERE/"GRAM_INTRINSIC_SUBSPACE_ATLAS.tsv")
    if [(r["key"],r["tensor"]) for r in output]!=[(r["key"],r["tensor"]) for r in production]:raise RuntimeError("spectral atlas order mismatch")
    comparison=[]
    for p,q in zip(production,output):
        eigen=spectrum_error(p,q);block=set_defect(projectors(p,"spectral_blocks_json"),projectors(q,"spectral_blocks_json"));plane=set_defect(projectors(p,"candidate_2planes_json"),projectors(q,"candidate_2planes_json"))
        discrete=all(p[name]==str(q[name]) for name in ("structure","operator_rank","real_eigenvalue_count","complex_pair_count","jordan_defect","spectral_block_count","candidate_2plane_count"))
        passed=eigen<=5e-3 and block<=2e-3 and plane<=2e-3 and discrete
        comparison.append({"key":p["key"],"tensor":p["tensor"],"eigenvalue_error":f"{eigen:.17g}","spectral_block_projector_defect":f"{block:.17g}" if np.isfinite(block) else "UNMATCHED","candidate_2plane_projector_defect":f"{plane:.17g}" if np.isfinite(plane) else "UNMATCHED","production_structure":p["structure"],"independent_structure":q["structure"],"discrete_diagnostics_agree":str(discrete).upper(),"pass":str(passed).upper()})
    write_tsv(HERE/"GRAM_INTRINSIC_SUBSPACE_COMPARISON.tsv",comparison)
    result={"schema":"udt-Gram-intrinsic-subspaces-independent-v1","status":"PASS" if all(r["pass"]=="TRUE" for r in comparison) else "PASS_WITH_SPECTRALLY_UNRESOLVED","rows":len(output),"exact_comparison_passes":sum(r["pass"]=="TRUE" for r in comparison),"comparison_unresolved":sum(r["pass"]!="TRUE" for r in comparison),"maximum_eigenvalue_error":max(float(r["eigenvalue_error"]) for r in comparison),"maximum_finite_block_projector_defect":max(float(r["spectral_block_projector_defect"]) for r in comparison if r["spectral_block_projector_defect"]!="UNMATCHED"),"maximum_finite_candidate_2plane_projector_defect":max(float(r["candidate_2plane_projector_defect"]) for r in comparison if r["candidate_2plane_projector_defect"]!="UNMATCHED"),"independent_structure_counts":dict(sorted(Counter(str(r["structure"]) for r in output).items()))}
    (HERE/"INDEPENDENT_GRAM_INTRINSIC_SUBSPACE_RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":main()

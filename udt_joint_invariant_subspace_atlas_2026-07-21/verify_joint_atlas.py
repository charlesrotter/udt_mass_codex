#!/usr/bin/env python3
"""Independent anchor verifier for the joint invariant-subspace atlas.

This module deliberately imports neither the builder nor invariant_subspace_core.
"""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
import os
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_structural_ensemble_metric_atlas_2026-07-21"
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
TOL = 1.0e-9
CLUSTER = 1.0e-8
LOW = 1.0e-11
HIGH = 1.0e-7
MAXIMUM = "BOUNDED_POINTWISE_JOINT_INVARIANT_SUBSPACE_ATLAS_CHARACTERIZED"
ANCHOR_CARRIERS = {
    "R00_1", "R05_1", "R10_1", "R15_1", "R00_3", "R05_3",
    "R10_3", "R15_3", "V001", "V006", "V011", "V016",
}
ANCHOR_MASKS = {0, 1, 3, 7, 15}
FAMILIES = (
    ("F01_RICCI", ("R",)), ("F02_PHI_HESSIAN", ("H",)),
    ("F03_PHI_DYAD", ("D",)), ("F04_RICCI_HESSIAN", ("R", "H")),
    ("F05_RICCI_HESSIAN_DYAD", ("R", "H", "D")),
    ("F06_RIEMANN_GENERATORS", ("RG",)), ("F07_WEYL_GENERATORS", ("WG",)),
    ("F08_FULL_RIEMANN_JOINT", ("R", "H", "D", "RG")),
    ("F09_FULL_WEYL_JOINT", ("R", "H", "D", "WG")),
)
COMPARE = (
    "algebra_dimension", "commutant_dimension", "commutant_center_dimension",
    "selfadjoint_center_dimension", "central_block_ranks", "central_rank2_split_count",
    "central_block_status", "gradient_orbit_dimension", "gradient_orbit_metric_rank",
    "gradient_orbit_signature", "reducibility_class", "numeric_status",
)


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], values: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(values)


def relmax(actual, expected) -> float:
    a, b = np.asarray(actual, dtype=float), np.asarray(expected, dtype=float)
    return float(np.max(np.abs(a - b)) / max(1.0, float(np.max(np.abs(b)))))


def rank_info(matrix: np.ndarray) -> tuple[int, bool, np.ndarray]:
    singular = np.linalg.svd(np.asarray(matrix, dtype=float), compute_uv=False)
    scale = max(1.0, float(singular[0]) if singular.size else 0.0)
    rank = int(np.count_nonzero(singular > TOL * scale))
    uncertain = bool(np.any((singular >= LOW * scale) & (singular <= HIGH * scale)))
    return rank, uncertain, singular


def independent_geometry(g: np.ndarray, dg: np.ndarray, ddg: np.ndarray) -> dict[str, np.ndarray | float]:
    inverse = np.linalg.inv(g)
    dinverse = np.asarray([-inverse @ dg[k] @ inverse for k in range(4)])
    gamma = np.zeros((4, 4, 4)); dgamma = np.zeros((4, 4, 4, 4))
    for r, m, n in itertools.product(range(4), repeat=3):
        h = np.array([dg[m, s, n] + dg[n, s, m] - dg[s, m, n] for s in range(4)])
        gamma[r, m, n] = 0.5 * inverse[r] @ h
        for k in range(4):
            dh = np.array([ddg[k, m, s, n] + ddg[k, n, s, m] - ddg[k, s, m, n] for s in range(4)])
            dgamma[k, r, m, n] = 0.5 * (dinverse[k, r] @ h + inverse[r] @ dh)
    up = np.zeros((4, 4, 4, 4))
    for r, s, m, n in itertools.product(range(4), repeat=4):
        up[r, s, m, n] = dgamma[m, r, n, s] - dgamma[n, r, m, s] + sum(
            gamma[r, m, q] * gamma[q, n, s] - gamma[r, n, q] * gamma[q, m, s] for q in range(4)
        )
    down = np.einsum("ar,rsuv->asuv", g, up)
    ricci = np.einsum("rsrn->sn", up)
    scalar = float(np.einsum("ab,ab", inverse, ricci))
    weyl = np.zeros_like(down)
    for a, b, c, d in itertools.product(range(4), repeat=4):
        weyl[a, b, c, d] = down[a, b, c, d] - 0.5 * (
            g[a, c] * ricci[b, d] - g[a, d] * ricci[b, c]
            - g[b, c] * ricci[a, d] + g[b, d] * ricci[a, c]
        ) + scalar * (g[a, c] * g[b, d] - g[a, d] * g[b, c]) / 6.0
    return {"inverse": inverse, "gamma": gamma, "up": up, "down": down, "ricci": ricci, "scalar": scalar, "weyl": weyl}


def phi_dyad(metric: np.ndarray, dphi: np.ndarray, normalize: bool = False) -> np.ndarray:
    gradient=np.linalg.inv(metric)@dphi
    if normalize:
        norm=float(dphi@gradient)
        if abs(norm)<=TOL:
            raise ValueError("cannot normalize a null phi dyad")
        return np.outer(gradient,dphi)/norm
    return np.outer(gradient,dphi)


def independent_objects(g: np.ndarray, dg: np.ndarray, ddg: np.ndarray, dphi: np.ndarray, ddphi: np.ndarray) -> tuple[dict[str, object], dict[str, object]]:
    geometry = independent_geometry(g, dg, ddg)
    inverse = geometry["inverse"]
    gradient = inverse @ dphi
    hessian = ddphi.copy()
    gamma = geometry["gamma"]
    for a, b in itertools.product(range(4), repeat=2):
        hessian[a, b] -= sum(gamma[r, a, b] * dphi[r] for r in range(4))
    weyl_up = np.einsum("ar,rsuv->asuv", inverse, geometry["weyl"])
    objects = {
        "metric": g, "inverse": inverse, "gradient": gradient,
        "R": inverse @ geometry["ricci"], "H": inverse @ hessian,
        "D": phi_dyad(g,dphi),
        "RG": [geometry["up"][:, :, a, b] for a, b in PAIRS],
        "WG": [weyl_up[:, :, a, b] for a, b in PAIRS],
        "riemann_down": geometry["down"], "weyl_down": geometry["weyl"],
    }
    return objects, geometry


def operators(objects: dict[str, object], keys: tuple[str, ...]) -> list[np.ndarray]:
    result = []
    for key in keys:
        value = objects[key]
        result.extend(value if isinstance(value, list) else [value])
    return [np.asarray(item, dtype=float) for item in result]


def normalized(values: list[np.ndarray]) -> list[np.ndarray]:
    result = []
    for value in values:
        norm = float(np.linalg.norm(value))
        if norm > 1.0e-12:
            result.append(value / norm)
    return result


def row_basis(values: list[np.ndarray]) -> tuple[list[np.ndarray], bool]:
    vectors = []
    for value in values:
        flat = np.asarray(value).reshape(-1)
        norm = float(np.linalg.norm(flat))
        if norm > 1.0e-12:
            vectors.append(flat / norm)
    if not vectors:
        return [], False
    matrix = np.asarray(vectors)
    rank, uncertain, _ = rank_info(matrix)
    _, _, vh = np.linalg.svd(matrix, full_matrices=False)
    return [vh[i].reshape(4, 4) for i in range(rank)], uncertain


def algebra_basis(values: list[np.ndarray]) -> tuple[list[np.ndarray], bool]:
    ops = normalized(values); candidates = [np.eye(4), *ops]; prior = -1; uncertain = False
    while True:
        basis, current_uncertain = row_basis(candidates); uncertain |= current_uncertain
        if len(basis) == prior or len(basis) == 16:
            return basis, uncertain
        prior = len(basis)
        candidates = [*basis, *(left @ right for left in basis for right in ops)]


def nullspace(matrix: np.ndarray) -> tuple[np.ndarray, bool]:
    rank, uncertain, _ = rank_info(matrix)
    _, _, vh = np.linalg.svd(matrix, full_matrices=True)
    return vh[rank:].T, uncertain


def commutant_basis(values: list[np.ndarray]) -> tuple[list[np.ndarray], bool]:
    ops = normalized(values)
    if not ops:
        elementary = []
        for column in range(4):
            for row in range(4):
                value = np.zeros((4, 4)); value[row, column] = 1.0; elementary.append(value)
        return elementary, False
    identity = np.eye(4)
    constraint = np.vstack([np.kron(operator.T, identity) - np.kron(identity, operator) for operator in ops])
    kernel, uncertain = nullspace(constraint)
    return [kernel[:, i].reshape(4, 4, order="F") for i in range(kernel.shape[1])], uncertain


def center_basis(commutant: list[np.ndarray]) -> tuple[list[np.ndarray], bool]:
    blocks = []
    for other in commutant:
        blocks.append(np.column_stack([(item @ other - other @ item).reshape(-1, order="F") for item in commutant]))
    kernel, uncertain = nullspace(np.vstack(blocks))
    return [sum(kernel[i, j] * commutant[i] for i in range(len(commutant))) for j in range(kernel.shape[1])], uncertain


def selfcenter_basis(center: list[np.ndarray], metric: np.ndarray) -> tuple[list[np.ndarray], bool]:
    matrix = np.column_stack([(item.T @ metric - metric @ item).reshape(-1) for item in center])
    kernel, uncertain = nullspace(matrix)
    inverse = np.linalg.inv(metric)
    result = []
    for j in range(kernel.shape[1]):
        value = sum(kernel[i, j] * center[i] for i in range(len(center)))
        result.append(0.5 * (value + inverse @ value.T @ metric))
    return result, uncertain


def independent_real_primary_projectors(z: np.ndarray) -> tuple[list[np.ndarray], bool]:
    """Independent CRT construction using Vandermonde interpolation, not product projectors."""
    eigenvalues = list(np.linalg.eigvals(z))
    clusters: list[list[complex]] = []
    for eigenvalue in sorted(eigenvalues, key=lambda item: (float(item.real), float(item.imag))):
        choices = [
            index for index, cluster in enumerate(clusters)
            if abs(eigenvalue - sum(cluster) / len(cluster))
            <= CLUSTER * max(1.0, abs(eigenvalue), abs(sum(cluster) / len(cluster)))
        ]
        if choices:
            clusters[choices[0]].append(complex(eigenvalue))
        else:
            clusters.append([complex(eigenvalue)])
    centers = np.array([sum(cluster) / len(cluster) for cluster in clusters], dtype=complex)
    # Independent semisimplicity gate.  The CRT interpolation below is not valid for a defective
    # primary cluster, so compare algebraic multiplicity with SVD-certified geometric multiplicity
    # before constructing any projector.
    complex_z = np.asarray(z, dtype=complex)
    identity = np.eye(4, dtype=complex)
    for cluster, center in zip(clusters, centers):
        singular = np.linalg.svd(complex_z - center * identity, compute_uv=False)
        scale = max(1.0, float(singular[0]) if singular.size else 0.0)
        rank = int(np.count_nonzero(singular > TOL * scale))
        uncertain = bool(np.any((singular >= LOW * scale) & (singular <= HIGH * scale)))
        if uncertain or 4 - rank != len(cluster):
            return [], True
    groups: list[list[int]] = []
    used: set[int] = set()
    for index, center in enumerate(centers):
        if index in used:
            continue
        if abs(center.imag) <= CLUSTER * max(1.0, abs(center)):
            group = [index]
        else:
            partner = [
                other for other in range(len(centers)) if other != index and other not in used
                and len(clusters[other]) == len(clusters[index])
                and abs(centers[other] - center.conjugate())
                <= CLUSTER * max(1.0, abs(centers[other]), abs(center))
            ]
            if len(partner) != 1:
                return [], True
            group = [index, partner[0]]
        used.update(group); groups.append(group)
    if len(used) != len(centers):
        return [], True
    vandermonde = np.array([[center ** power for power in range(len(centers))] for center in centers], dtype=complex)
    if np.linalg.cond(vandermonde) > 1.0e12:
        return [], True
    powers = [np.linalg.matrix_power(np.asarray(z, dtype=complex), power) for power in range(len(centers))]
    projectors=[]
    for group in groups:
        target=np.zeros(len(centers),dtype=complex); target[group]=1.0
        coefficients=np.linalg.solve(vandermonde,target)
        projector=sum((coefficients[power]*powers[power] for power in range(len(powers))),np.zeros((4,4),dtype=complex))
        if np.max(np.abs(projector.imag))>TOL:
            return [], True
        projectors.append(projector.real)
    return projectors, False


def independent_projector_set_distance(first: list[np.ndarray], second: list[np.ndarray]) -> float:
    if len(first)!=len(second): return math.inf
    unused=set(range(len(second))); worst=0.0
    for projector in first:
        distance,index=min((relmax(projector,second[item]),item) for item in unused)
        unused.remove(index); worst=max(worst,distance)
    return worst


def central_blocks(values: list[np.ndarray], metric: np.ndarray, commutant: list[np.ndarray], selfcenter: list[np.ndarray]) -> tuple[str, int, str]:
    ops = normalized(values)
    if len(selfcenter) == 1:
        return "4", 0, "NO_NONTRIVIAL_CENTRAL_BLOCK"
    candidates = []
    for trial in range(9):
        z = sum((((-1) ** (trial * (i + 1))) * (i + 1) ** (trial + 1)) * item for i, item in enumerate(selfcenter))
        norm = float(np.linalg.norm(z))
        if norm <= 1.0e-12:
            continue
        z /= norm
        projectors,spectral_uncertain=independent_real_primary_projectors(z)
        if spectral_uncertain:
            continue
        ranks=[]; valid=True;maximum_residual=0.0
        for p in projectors:
            rank, uncertain, _ = rank_info(p)
            residual=max(relmax(p@p,p),relmax(p.T@metric,metric@p),max((relmax(p@a,a@p) for a in ops),default=0.0),max((relmax(p@a,a@p) for a in commutant),default=0.0))
            valid &= not uncertain and residual <= TOL
            maximum_residual=max(maximum_residual,residual);ranks.append(rank)
        maximum_residual=max(maximum_residual,relmax(sum(projectors,np.zeros((4,4))),np.eye(4)),max((relmax(projectors[i]@projectors[j],np.zeros((4,4))) for i in range(len(projectors)) for j in range(i+1,len(projectors))),default=0.0))
        valid &= maximum_residual<=TOL
        if valid and sum(ranks)==4: candidates.append((sorted(ranks),projectors))
    if not candidates:
        return "", 0, "NUMERIC_UNCERTAIN_CENTRAL_BLOCKS"
    maximum=max(len(x[0]) for x in candidates); finalists=[x for x in candidates if len(x[0])==maximum];ranks,reference=finalists[0]
    stability=max((independent_projector_set_distance(reference,item[1]) for item in finalists[1:]),default=0.0)
    subset=sum(sum(ranks[i] for i in range(len(ranks)) if mask&(1<<i))==2 for mask in range(1,2**len(ranks)-1))
    splits=subset//2
    status="NUMERIC_UNCERTAIN_CENTRAL_BLOCKS" if stability>TOL else "UNIQUE_CENTRAL_2PLUS2" if splits==1 else "MULTIPLE_CENTRAL_2PLUS2" if splits>1 else "NO_NONTRIVIAL_CENTRAL_BLOCK" if ranks==[4] else "CENTRAL_BLOCKS_NO_2PLUS2"
    return ";".join(map(str,ranks)),splits,status


def orbit(values: list[np.ndarray], seed: np.ndarray, metric: np.ndarray) -> tuple[int, int, str, bool]:
    ops=normalized(values)
    if np.linalg.norm(seed)<=1.0e-12: return 0,0,"ZERO_SEED",False
    candidates=[seed]; prior=-1; uncertain=False
    while True:
        matrix=np.column_stack([v/np.linalg.norm(v) for v in candidates if np.linalg.norm(v)>1.0e-12])
        rank,current,_=rank_info(matrix); uncertain|=current
        u,_,_=np.linalg.svd(matrix,full_matrices=False); basis=u[:,:rank]
        if rank==prior or rank==4: break
        prior=rank; candidates=[basis[:,i] for i in range(rank)]+[a@basis[:,i] for a in ops for i in range(rank)]
    eigen=np.linalg.eigvalsh(0.5*(basis.T@metric@basis+(basis.T@metric@basis).T)); scale=max(1.0,float(np.max(np.abs(eigen))))
    neg=int(np.count_nonzero(eigen < -TOL*scale)); pos=int(np.count_nonzero(eigen > TOL*scale)); zero=rank-neg-pos
    uncertain |= bool(np.any((np.abs(eigen)>=LOW*scale)&(np.abs(eigen)<=HIGH*scale)))
    return rank,neg+pos,f"N{neg}_P{pos}_Z{zero}",uncertain


def classify(values: list[np.ndarray], seed: np.ndarray, metric: np.ndarray) -> dict[str, object]:
    algebra, ua=algebra_basis(values); commutant,uc=commutant_basis(values); center,uz=center_basis(commutant); selfcenter,us=selfcenter_basis(center,metric)
    block_ranks,splits,block_status=central_blocks(values,metric,commutant,selfcenter); odim,orank,osig,uo=orbit(values,seed,metric)
    if len(algebra)==16: reducibility="FULL_MATRIX_ALGEBRA_IRREDUCIBLE"
    elif splits==1: reducibility="UNIQUE_CENTRAL_2PLUS2"
    elif splits>1: reducibility="MULTIPLE_CENTRAL_2PLUS2"
    elif len(commutant)>len(center): reducibility="PROPER_ALGEBRA_NONCENTRAL_AMBIGUITY"
    else: reducibility="PROPER_ALGEBRA_NO_CENTRAL_2PLUS2"
    return {"algebra_dimension":len(algebra),"commutant_dimension":len(commutant),"commutant_center_dimension":len(center),"selfadjoint_center_dimension":len(selfcenter),"central_block_ranks":block_ranks,"central_rank2_split_count":splits,"central_block_status":block_status,"gradient_orbit_dimension":odim,"gradient_orbit_metric_rank":orank,"gradient_orbit_signature":osig,"reducibility_class":reducibility,"numeric_status":"NUMERIC_UNCERTAIN" if ua or uc or uz or us or uo or block_status.startswith("NUMERIC_UNCERTAIN") else "NUMERIC_CLASSIFIED"}


def bivector_operator_summary(operator: np.ndarray, metric: np.ndarray) -> dict[str, int | str]:
    eig,vec=np.linalg.eig(operator)
    used=set(); simple=[]; repeated=0;complex=0;uncertain=False
    for i in range(6):
        if i in used:continue
        group=[j for j in range(6) if j not in used and abs(eig[i]-eig[j])<=CLUSTER*max(1.0,abs(eig[i]),abs(eig[j]))];used.update(group)
        if len(group)>1: repeated+=len(group);continue
        if abs(eig[i].imag)>CLUSTER or np.max(np.abs(vec[:,i].imag))>CLUSTER:complex+=1;continue
        v=vec[:,i].real;v/=np.linalg.norm(v);b01,b02,b03,b12,b13,b23=v;pf=abs(b01*b23-b02*b13+b03*b12)
        gap=min(abs(eig[i]-eig[j])/max(1.0,abs(eig[i]),abs(eig[j])) for j in range(6) if j!=i)
        uncertain|=LOW<=pf<=HIGH or LOW<=gap<=HIGH
        if pf>TOL:continue
        b=np.zeros((4,4))
        for x,(a,c) in zip(v,PAIRS):b[a,c]=x;b[c,a]=-x
        rank,ur,_=rank_info(b);uncertain|=ur
        if rank!=2:continue
        u,_,_=np.linalg.svd(b);basis=u[:,:2];gram=basis.T@metric@basis;ge=np.linalg.eigvalsh(0.5*(gram+gram.T));scale=max(1.0,float(np.max(np.abs(ge))));zero=int(np.count_nonzero(np.abs(ge)<=TOL*scale))
        projector=None if zero else basis@np.linalg.inv(gram)@basis.T@metric
        simple.append(projector)
    nondeg=[p for p in simple if p is not None];pairs=sum(max(relmax(nondeg[i]+nondeg[j],np.eye(4)),relmax(nondeg[i]@nondeg[j],np.zeros((4,4))))<=TOL for i in range(len(nondeg)) for j in range(i+1,len(nondeg)))
    return {"isolated_real_simple_eigenplanes":len(simple),"nondegenerate_simple_eigenplanes":len(nondeg),"complementary_split_count":pairs,"repeated_eigenvalue_multiplicity":repeated,"complex_isolated_count":complex,"numeric_status":"NUMERIC_UNCERTAIN" if uncertain else "NUMERIC_CLASSIFIED"}


def bivector_summary(tensor: np.ndarray, inverse: np.ndarray, metric: np.ndarray) -> dict[str, int | str]:
    raised=np.einsum("ae,bf,efcd->abcd",inverse,inverse,tensor)
    operator=np.array([[raised[a,b,c,d] for c,d in PAIRS] for a,b in PAIRS])
    return bivector_operator_summary(operator,metric)


def multiply(left, right):
    lv,lf,ls=left;rv,rf,rs=right
    return lv*rv,lf*rv+lv*rf,ls*rv+lv*rs+np.outer(lf,rf)+np.outer(rf,lf)


def transform_jets(g,dg,ddg,pv,pf,ps,j,k,ell):
    gj=[[(j[mu,a],k[mu,a].copy(),ell[mu,a].copy()) for a in range(4)] for mu in range(4)]
    gt=np.zeros((4,4));dgt=np.zeros((4,4,4));ddgt=np.zeros((4,4,4,4))
    for a,b in itertools.product(range(4),repeat=2):
        total=(0.0,np.zeros(4),np.zeros((4,4)))
        for mu,nu in itertools.product(range(4),repeat=2):
            comp=(g[mu,nu],np.einsum("r,rc->c",dg[:,mu,nu],j),np.einsum("rs,rc,sd->cd",ddg[:,:,mu,nu],j,j)+np.einsum("r,rcd->cd",dg[:,mu,nu],k))
            total=tuple(x+y for x,y in zip(total,multiply(multiply(gj[mu][a],gj[nu][b]),comp)))
        gt[a,b],dgt[:,a,b],ddgt[:,:,a,b]=total
    pft=np.einsum("r,ra->a",pf,j);pst=np.einsum("rs,ra,sb->ab",ps,j,j)+np.einsum("r,rab->ab",pf,k)
    return gt,dgt,ddgt,pv,pft,pst


def family_values(objects, keys):return operators(objects,keys)


def must_fail(catch_id, predicate, output):
    if predicate(): raise AssertionError(f"catch did not fail: {catch_id}")
    output.append({"catch_id":catch_id,"result":"REJECTED_AS_REQUIRED"})


def must_reject(catch_id, validator, mutation, output):
    try:
        validator(mutation)
    except (AssertionError, ValueError, KeyError):
        output.append({"catch_id":catch_id,"result":"REJECTED_AS_REQUIRED"})
        return
    raise AssertionError(f"catch did not reject mutation: {catch_id}")


def validate_operator_registry(candidate: list[dict[str,str]]) -> None:
    expected=[
        {"family_id":family_id,"operator_keys":";".join(keys),"scope":"REGISTERED_NAMED_POINTWISE_FAMILY"}
        for family_id,keys in FAMILIES
    ]
    if candidate!=expected:
        raise AssertionError("operator-family registry mutation")


def validate_transform_registry(candidate: list[dict[str,str]], expected: list[dict[str,str]]) -> None:
    if candidate!=expected or len(candidate)!=2:
        raise AssertionError("nonlinear transform registry mutation")


def validate_bivector_rows(candidate: dict[str,dict[str,dict[str,object]]], expected: dict[str,dict[str,dict[str,object]]]) -> None:
    if set(candidate)!=set(expected):
        raise AssertionError("bivector configuration coverage")
    for key,value in candidate.items():
        for name,summary in value.items():
            for field,observed in summary.items():
                if str(observed)!=str(expected[key][name][field]):
                    raise AssertionError("bivector output mutation")


def validate_uncertainty_set(candidate: set[tuple[str,str,str]], expected: set[tuple[str,str,str]]) -> None:
    if candidate!=expected:
        raise AssertionError("uncertainty ledger mismatch")


def validate_full_coverage(
    all_ids: set[str], family_saved: dict[tuple[str,str],dict[str,str]],
    config_saved: dict[str,dict[str,str]],
    nonlinear_saved: dict[tuple[str,str,str],dict[str,str]],
    nonlinear_config: dict[tuple[str,str],dict[str,str]], transform_ids: set[str],
) -> None:
    family_ids={family_id for family_id,_ in FAMILIES}
    expected_family={(configuration_id,family_id) for configuration_id in all_ids for family_id in family_ids}
    expected_nonlinear={(configuration_id,transform_id,family_id) for configuration_id in all_ids for transform_id in transform_ids for family_id in family_ids}
    expected_nonlinear_config={(configuration_id,transform_id) for configuration_id in all_ids for transform_id in transform_ids}
    if len(all_ids)!=6144 or set(config_saved)!=all_ids:
        raise AssertionError("configuration coverage")
    if set(family_saved)!=expected_family:
        raise AssertionError("family-row coverage")
    if set(nonlinear_saved)!=expected_nonlinear:
        raise AssertionError("nonlinear-family coverage")
    if set(nonlinear_config)!=expected_nonlinear_config:
        raise AssertionError("nonlinear-configuration coverage")


def validate_result_contract(candidate: dict[str,object], family_saved: dict[tuple[str,str],dict[str,str]], nonlinear_saved: dict[tuple[str,str,str],dict[str,str]]) -> None:
    unique=sum(row["numeric_status"]=="NUMERIC_CLASSIFIED" and int(row["central_rank2_split_count"])==1 for row in family_saved.values())
    multiple=sum(row["numeric_status"]=="NUMERIC_CLASSIFIED" and int(row["central_rank2_split_count"])>1 for row in family_saved.values())
    nonlinear_uncertain=sum(row["comparison_status"]=="NUMERIC_UNCERTAIN_RETAINED" for row in nonlinear_saved.values())
    required={
        "status":"PASS", "maximum_conclusion":MAXIMUM, "configurations":6144,
        "family_rows":55296, "nonlinear_configuration_rows":12288,
        "nonlinear_family_rows":110592, "unique_central_2plus2_rows":unique,
        "multiple_central_2plus2_rows":multiple,
        "nonlinear_uncertain_comparisons":nonlinear_uncertain,
        "nonlinear_classification_discordances":0, "discarded_rows":0,
        "physical_split_selected":False, "supplied_split_loaded":False,
        "action_or_equation_loaded":False, "global_distribution_claimed":False,
        "full_group_claimed":False, "gpu_used":False,
    }
    if any(candidate.get(key)!=value for key,value in required.items()):
        raise AssertionError("result contract mismatch")


def main() -> None:
    os.environ["CUDA_VISIBLE_DEVICES"]=""
    operator_registry=rows(HERE/"OPERATOR_FAMILY_REGISTRY.tsv");validate_operator_registry(operator_registry)
    registry=rows(HERE/"NONLINEAR_TRANSFORM_REGISTRY.tsv");registered_transforms=[dict(row) for row in registry];validate_transform_registry(registry,registered_transforms)
    transforms={r["transform_id"]:(np.array(json.loads(r["jacobian_json"])),np.array(json.loads(r["second_jet_json"])),np.array(json.loads(r["third_jet_json"]))) for r in registry}
    anchor_count=0; nonlinear_count=0; family_checks=0; max_parent=0.0; max_cov=0.0; check_count=0; nonsimple_anchor=None; omitted_jet_anchor=None; actual_uncertain=set();computed_family={};computed_config={};computed_nonlinear={};computed_nonlinear_config={};anchor_ids=set();all_ids=set();conjugate_operator=None
    for shard in rows(PARENT/"RAW_SHARD_REGISTRY.tsv"):
        with (PARENT/shard["path"]).open() as handle:
            for line in handle:
                raw=json.loads(line)
                all_ids.add(raw["configuration_id"])
                if raw["carrier_id"] not in ANCHOR_CARRIERS or int(raw["mask_integer"]) not in ANCHOR_MASKS:continue
                anchor_count+=1;cid=raw["configuration_id"];anchor_ids.add(cid);g=np.array(raw["metric"]);dg=np.array(raw["metric_first"]);ddg=np.array(raw["metric_second"]);pf=np.array(raw["phi"]["first"]);ps=np.array(raw["phi"]["second"])
                obj,geo=independent_objects(g,dg,ddg,pf,ps);max_parent=max(max_parent,relmax(geo["down"],raw["riemann_down"]),relmax(geo["ricci"],raw["ricci"]),relmax(geo["weyl"],raw["weyl_down"]))
                if cid=="R00_1_M1_B0_P0":conjugate_operator=np.asarray(obj["R"]).copy()
                summaries={"riemann":bivector_summary(obj["riemann_down"],obj["inverse"],g),"weyl":bivector_summary(obj["weyl_down"],obj["inverse"],g)}
                computed_config[cid]=summaries
                if nonsimple_anchor is None:
                    raised=np.einsum("ae,bf,efcd->abcd",obj["inverse"],obj["inverse"],obj["riemann_down"]);op=np.array([[raised[a,b,c,d] for c,d in PAIRS] for a,b in PAIRS]);ev,v=np.linalg.eig(op)
                    for i in range(6):
                        if abs(ev[i].imag)<=CLUSTER and np.max(np.abs(v[:,i].imag))<=CLUSTER:
                            q=v[:,i].real;q/=np.linalg.norm(q);pfaff=abs(q[0]*q[5]-q[1]*q[4]+q[2]*q[3])
                            if pfaff>HIGH:nonsimple_anchor=pfaff;break
                base={}
                for fid,keys in FAMILIES:
                    current=classify(family_values(obj,keys),obj["gradient"],g);base[fid]=current;computed_family[(cid,fid)]=current
                    family_checks+=1
                for tid,(j,k,ell) in transforms.items():
                    nonlinear_count+=1;z=transform_jets(g,dg,ddg,raw["phi"]["value"],pf,ps,j,k,ell);tobj,tgeo=independent_objects(z[0],z[1],z[2],z[4],z[5]);ji=np.linalg.inv(j)
                    cov=max(relmax(tobj["metric"],j.T@g@j),relmax(tobj["gradient"],ji@obj["gradient"]),relmax(tobj["R"],ji@obj["R"]@j),relmax(tobj["H"],ji@obj["H"]@j),relmax(tobj["D"],ji@obj["D"]@j));max_cov=max(max_cov,cov)
                    if omitted_jet_anchor is None and np.linalg.norm(np.einsum("r,rab->ab",pf,k))>1.0e-8: omitted_jet_anchor=(pf,ps,j,k,z[5])
                    for name,tensor in (("riemann",tobj["riemann_down"]),("weyl",tobj["weyl_down"])):
                        summary=bivector_summary(tensor,tobj["inverse"],tobj["metric"]);computed_nonlinear_config.setdefault((cid,tid),{})[name]=summary
                    for fid,keys in FAMILIES:
                        current=classify(family_values(tobj,keys),tobj["gradient"],tobj["metric"]);computed_nonlinear[(cid,tid,fid)]=current
                        if current["numeric_status"]=="NUMERIC_UNCERTAIN" or base[fid]["numeric_status"]=="NUMERIC_UNCERTAIN":actual_uncertain.add((cid,tid,fid))
                        family_checks+=1
                check_count+=1
    if anchor_count!=480 or nonlinear_count!=960 or family_checks!=12960:raise AssertionError(f"anchor counts {anchor_count} {nonlinear_count} {family_checks}")
    # Only after every independent anchor has been computed may saved builder classifications enter.
    result=json.loads((HERE/"ATLAS_RESULT.json").read_text());family_saved={(r["configuration_id"],r["family_id"]):r for r in rows(HERE/"FAMILY_SUBSPACE_ATLAS.tsv")};config_saved={r["configuration_id"]:r for r in rows(HERE/"CONFIGURATION_SUBSPACE_CENSUS.tsv")};nonlinear_saved={(r["configuration_id"],r["transform_id"],r["family_id"]):r for r in rows(HERE/"NONLINEAR_FAMILY_COMPARISON.tsv")};nonlinear_config={(r["configuration_id"],r["transform_id"]):r for r in rows(HERE/"NONLINEAR_CONFIGURATION_ATLAS.tsv")}
    validate_full_coverage(all_ids,family_saved,config_saved,nonlinear_saved,nonlinear_config,set(transforms))
    saved_bivectors={
        cid:{name:{field:config_saved[cid][f"{name}_{field}"] for field in summary} for name,summary in summaries.items()}
        for cid,summaries in computed_config.items()
    }
    validate_bivector_rows(saved_bivectors,computed_config)
    for key,current in computed_family.items():
        saved=family_saved[key]
        for field in COMPARE:
            if str(current[field])!=saved[field]:raise AssertionError(f"family {key} {field}: {current[field]} {saved[field]}")
    for key,summaries in computed_nonlinear_config.items():
        saved=nonlinear_config[key]
        for name,summary in summaries.items():
            for field,value in summary.items():
                if str(value)!=saved[f"{name}_{field}"]:raise AssertionError(f"nonlinear bivector {key} {name} {field}")
    for key,current in computed_nonlinear.items():
        saved=nonlinear_saved[key]
        for field in COMPARE:
            if str(current[field])!=saved[f"transformed_{field}"]:raise AssertionError(f"nonlinear family {key} {field}")
    margin={(r["configuration_id"],r["probe"],r["object"]) for r in rows(HERE/"NUMERIC_MARGIN_LEDGER.tsv")}; expected_anchor_margin={x for x in margin if x[0].split("_M")[0] in ANCHOR_CARRIERS and int(x[0].split("_M")[1].split("_")[0],16) in ANCHOR_MASKS}
    validate_uncertainty_set(actual_uncertain,expected_anchor_margin)
    validate_result_contract(result,family_saved,nonlinear_saved)
    catches=[]
    supplied_registry=[dict(row) for row in operator_registry];supplied_registry.append({"family_id":"BAD_SUPPLIED_SPLIT","operator_keys":"SUPPLIED_2PLUS2","scope":"REGISTERED_NAMED_POINTWISE_FAMILY"})
    must_reject("K01_SUPPLIED_2PLUS2_PROJECTOR",validate_operator_registry,supplied_registry,catches)
    dropped_registry=[dict(row) for row in operator_registry];dropped_registry[5]["operator_keys"]=""
    must_reject("K02_DROPPED_OPERATOR",validate_operator_registry,dropped_registry,catches)
    null_metric=np.diag((-1.0,1.0,1.0,1.0));null_cov=np.array((1.0,1.0,0.0,0.0))
    must_reject("K03_NORMALIZED_NULL_DYAD",lambda requested:phi_dyad(null_metric,null_cov,requested),True,catches)
    omitted_registry=[dict(row) for row in registry];omitted_registry[0]["second_jet_json"]="[]";omitted_registry[0]["third_jet_json"]="[]"
    must_reject("K04_OMITTED_NONLINEAR_MAP_JETS",lambda candidate:validate_transform_registry(candidate,registered_transforms),omitted_registry,catches)
    nonsimple=np.array((1.0,0.0,0.0,0.0,0.0,1.0))/math.sqrt(2.0);nonsimple_summary=bivector_operator_summary(2.0*np.outer(nonsimple,nonsimple),null_metric)
    if nonsimple_summary["isolated_real_simple_eigenplanes"]!=0:raise AssertionError("nonsimple eigenbivector accepted by classifier")
    first_config=next(iter(saved_bivectors));mutated_bivectors={key:{name:dict(summary) for name,summary in value.items()} for key,value in saved_bivectors.items()};field="isolated_real_simple_eigenplanes";mutated_bivectors[first_config]["riemann"][field]=str(int(mutated_bivectors[first_config]["riemann"][field])+1)
    must_reject("K05_NONSIMPLE_EIGENBIVECTOR_ACCEPTED",lambda candidate:validate_bivector_rows(candidate,computed_config),mutated_bivectors,catches)
    if not actual_uncertain:raise AssertionError("missing registered uncertainty anchors")
    removed=set(actual_uncertain);removed.pop()
    must_reject("K06_HIDDEN_UNCERTAIN_RANK",lambda candidate:validate_uncertainty_set(candidate,expected_anchor_margin),removed,catches)
    filtered_family=dict(family_saved);del filtered_family[next(iter(filtered_family))]
    must_reject("K07_FILTERED_CONFIGURATION",lambda candidate:validate_full_coverage(all_ids,candidate,config_saved,nonlinear_saved,nonlinear_config,set(transforms)),filtered_family,catches)
    escalated=dict(result);escalated["maximum_conclusion"]="GLOBAL_PHYSICAL_ANGULAR_SPLIT_DERIVED"
    must_reject("K08_UNIQUENESS_ESCALATION",lambda candidate:validate_result_contract(candidate,family_saved,nonlinear_saved),escalated,catches)
    if conjugate_operator is None:raise AssertionError("missing conjugate anchor")
    def real_only_mutation(z):
        eig=np.linalg.eigvals(z)
        return [] if np.max(np.abs(eig.imag))>CLUSTER else independent_real_primary_projectors(z)[0]
    def validate_conjugate_blocks(projectors):
        ranks=sorted(rank_info(item)[0] for item in projectors)
        if ranks!=[1,1,2]:raise AssertionError(f"lost conjugate primary block {ranks}")
    validate_conjugate_blocks(independent_real_primary_projectors(conjugate_operator)[0])
    must_reject("K09_DROPPED_CONJUGATE_PRIMARY_BLOCK",validate_conjugate_blocks,real_only_mutation(conjugate_operator),catches)
    jordan_metric=np.array(((0.0,1.0,0.0,0.0),(1.0,0.0,0.0,0.0),(0.0,0.0,1.0,0.0),(0.0,0.0,0.0,1.0)));jordan=np.zeros((4,4));jordan[0,1]=1.0;jordan_result=classify([jordan],np.zeros(4),jordan_metric)
    def validate_jordan(candidate):
        if candidate["numeric_status"]!="NUMERIC_UNCERTAIN" or candidate["central_block_status"]!="NUMERIC_UNCERTAIN_CENTRAL_BLOCKS":raise AssertionError("defective Jordan primary classified")
    validate_jordan(jordan_result)
    jordan_mutation=dict(jordan_result);jordan_mutation["numeric_status"]="NUMERIC_CLASSIFIED";jordan_mutation["central_block_status"]="NO_NONTRIVIAL_CENTRAL_BLOCK"
    must_reject("K10_DEFECTIVE_JORDAN_PRIMARY_CLASSIFIED",validate_jordan,jordan_mutation,catches)
    write_tsv("CATCH_PROOFS.tsv",["catch_id","result"],catches)
    output={"status":"PASS","anchors":anchor_count,"nonlinear_anchors":nonlinear_count,"family_classifications":family_checks,"max_parent_tensor_residual":max_parent,"max_nonlinear_covariance_residual":max_cov,"anchor_uncertain_comparisons":len(actual_uncertain),"catch_proofs":len(catches),"maximum_conclusion":MAXIMUM}
    (HERE/"VERIFICATION_RESULT.json").write_text(json.dumps(output,indent=2,sort_keys=True)+"\n")
    transcript=["UDT_JOINT_INVARIANT_SUBSPACE_ATLAS_VERIFICATION=PASS",f"anchors={anchor_count} nonlinear_anchors={nonlinear_count} family_classifications={family_checks}",f"max_parent_residual={max_parent:.17g} max_nonlinear_covariance={max_cov:.17g}",f"anchor_uncertain={len(actual_uncertain)} catch_proofs={len(catches)}",f"maximum_conclusion={MAXIMUM}"]
    (HERE/"VERIFICATION_TRANSCRIPT.txt").write_text("\n".join(transcript)+"\n");print("\n".join(transcript))


if __name__=="__main__":main()

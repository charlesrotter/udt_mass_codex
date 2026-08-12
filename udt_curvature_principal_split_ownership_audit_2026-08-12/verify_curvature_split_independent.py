#!/usr/bin/env python3
"""Independent NumPy finite-difference verification of curvature split atlas.

This implementation intentionally does not import the production module or use
automatic differentiation.
"""

from __future__ import annotations

import csv
import itertools
import json
import math
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G63 = ROOT / "udt_solved_geometry_relation_family_survivor_atlas_2026-08-11"
G85 = ROOT / "udt_cmb_G85_mixed_timelive_completion_atlas_2026-08-12"
ETA = np.diag([-1.0,1.0,1.0,1.0])
FD_LADDER = (8.0e-4,4.0e-4,2.0e-4)


@dataclass(frozen=True)
class Sample:
    name: str
    geometry: str
    lam: float
    eps: float
    twist: float = .4


def read_tsv(path):
    return list(csv.DictReader(Path(path).open(),delimiter='\t'))


def samples():
    out=[]
    for row in read_tsv(G63/'NUMERICAL_SAMPLE_UNIVERSE.tsv'):
        p={x.split('=',1)[0]:x.split('=',1)[1] for x in (row['parameter_1'],row['parameter_2']) if '=' in x}
        out.append(Sample(row['sample_id'],row['geometry'],float(p.get('lambda',0)),float(p.get('epsilon',0))))
    assert len(out)==14 and len({x.name for x in out})==14
    return out


def profiles():
    s=sp.symbols('s'); out={}
    for row in read_tsv(G85/'PROFILE_ARCHETYPE_ATLAS.tsv'):
        poly=sp.Poly(sp.sympify(row['q_of_s'],locals={'s':s}),s)
        coeff=tuple(float(poly.nth(i)) for i in range(poly.degree()+1))
        old=out.setdefault(row['profile_id'],coeff); assert old==coeff
    assert len(out)==196
    return out


def r17_phi(x,e):
    _,th,va,ps=x
    a=np.cos(th/2)*np.cos((ps+va)/2); b=np.cos(th/2)*np.sin((ps+va)/2)
    c=np.sin(th/2)*np.cos((ps-va)/2); d=np.sin(th/2)*np.sin((ps-va)/2)
    return .12*a+.08*b*c-.05*(d*d-c*c)+e*(.11*d+.07*a*b)


def r17_E(x,s):
    _,th,_,ps=x; ph=r17_phi(x,s.eps); u=np.exp(ph); v=np.exp(s.lam*ph)
    a=.5*np.array([0.,np.cos(ps),np.sin(ps)*np.sin(th),0.])
    b=.5*np.array([0.,-np.sin(ps),np.cos(ps)*np.sin(th),0.])
    c=.5*np.array([0.,0.,np.cos(th),1.]); dt=np.array([1.,0.,0.,0.])
    return np.vstack(((dt+s.twist*c)/u,u*c,v*a,v*b))


def live_E(x,s):
    t,xx,y,z=x; e=s.eps
    k=.035*np.sin(t+.3*y)+.018*np.cos(xx-z)+e*.025*np.sin(t+xx+y)
    ph=.11*np.cos(xx-.2*t)+.025*np.sin(y+z)+e*.08*np.cos(t-z+.4*xx)
    be=.12*np.sin(t+xx)+.04*np.cos(y-z)+e*.05*np.sin(t+y)
    ga=.16*np.sin(t-y+.2*z)+e*.04*np.cos(xx+z)
    q1=.045*np.cos(t+y)+e*.03*np.sin(xx-z); q2=-.035*np.sin(xx+z)+e*.025*np.cos(t-y)
    sh=.07*np.sin(t+xx+y+z)+e*.025*np.cos(xx-y)
    S=np.array([[.055*np.cos(t+y)+e*.02*np.sin(z),.045*np.sin(xx-z)+e*.015*np.cos(t+y)],[-.04*np.cos(t-xx+y)+e*.02*np.sin(xx+z),.05*np.sin(t+z)+e*.018*np.cos(xx-y)]])
    T,L=np.exp(k-ph),np.exp(k+ph); B=np.array([[T,T*be],[0.,L]])
    R=np.array([[np.cos(ga),-np.sin(ga)],[np.sin(ga),np.cos(ga)]]); Q=R@np.array([[np.exp(q1),sh],[0.,np.exp(q2)]])
    E=np.zeros((4,4));E[:2,:2]=B;E[2:,:2]=Q@S;E[2:,2:]=Q
    return E


def g63_metric(x,s):
    E=r17_E(x,s) if s.geometry=='R17_GLOBAL' else live_E(x,s)
    return E.T@ETA@E


def eval_poly(x,c):
    v=0.
    for a in reversed(c):v=v*x+a
    return v


def g85_metric(x,coeff,arch,eps):
    tau,chi,th,_=x; A=np.cos(chi)**2; D=4*np.sin(chi)**2; C=D*np.sin(th)**2; fac=1+eps*np.sin(1.1*tau)
    if arch=='A03_RADIAL_SHIFT_TIMELIVE': u,b,h=-A,.6*fac,D*eval_poly(D,coeff)
    elif arch=='A04_LAPSE_LIFT_TIMELIVE': u,b,h=-A-.45*fac,0.,D*eval_poly(D,coeff)
    elif arch=='A05_SHIFT_SUPPORTED_TAPER': u,b,h=-A,.6*fac,0.
    else: raise ValueError(arch)
    H=h*np.sin(th)**2
    return np.array([[u,b,0.,H],[b,4.,0.,0.],[0.,0.,D,0.],[H,0.,0.,C]])


def fd1(fun,x,axis,h):
    d=np.zeros(4);d[axis]=h
    return (-fun(x+2*d)+8*fun(x+d)-8*fun(x-d)+fun(x-2*d))/(12*h)


def connection(fun,x,h):
    g=fun(x); gi=np.linalg.inv(g); dg=np.array([fd1(fun,x,k,h) for k in range(4)])
    G=np.zeros((4,4,4))
    for a,b,c in itertools.product(range(4),repeat=3):
        G[a,b,c]=.5*sum(gi[a,d]*(dg[b,d,c]+dg[c,d,b]-dg[d,b,c]) for d in range(4))
    return G


def curvature(fun,x,h):
    g=fun(x); gi=np.linalg.inv(g); G=connection(fun,x,h)
    dG=np.array([fd1(lambda y:connection(fun,y,h),x,k,h) for k in range(4)])
    Rup=np.zeros((4,4,4,4))
    for a,b,c,d in itertools.product(range(4),repeat=4):
        Rup[a,b,c,d]=dG[c,a,d,b]-dG[d,a,c,b]+sum(G[a,c,e]*G[e,d,b]-G[a,d,e]*G[e,c,b] for e in range(4))
    Rdn=np.einsum('ae,ebcd->abcd',g,Rup); Ric=np.einsum('abad->bd',Rup); R=np.einsum('ab,ab',gi,Ric)
    W=np.zeros_like(Rdn)
    for a,b,c,d in itertools.product(range(4),repeat=4):
        W[a,b,c,d]=Rdn[a,b,c,d]-.5*(g[a,c]*Ric[d,b]-g[a,d]*Ric[c,b]-g[b,c]*Ric[d,a]+g[b,d]*Ric[c,a])+R/6*(g[a,c]*g[d,b]-g[a,d]*g[c,b])
    return W,Ric


def metric_coframe(g):
    screen=g[2:,2:]; cross=g[:2,2:]; S=np.linalg.solve(screen,cross.T); base=g[:2,:2]-cross@S
    val,vec=np.linalg.eigh(base); neg=int(np.argmin(val)); pos=1-neg
    B=np.vstack((vec[:,neg]*np.sqrt(-val[neg]),vec[:,pos]*np.sqrt(val[pos])))
    Q=np.linalg.cholesky(screen).T; E=np.zeros((4,4));E[:2,:2]=B;E[2:,:2]=Q@S;E[2:,2:]=Q
    assert np.linalg.norm(E.T@ETA@E-g)<2e-9
    return E


def Q_from(W,E):
    F=np.linalg.inv(E); C=np.einsum('ma,nb,pc,qd,mnpq->abcd',F,F,F,F,W)
    eps=np.zeros((3,3,3));eps[0,1,2]=eps[1,2,0]=eps[2,0,1]=1;eps[0,2,1]=eps[2,1,0]=eps[1,0,2]=-1
    electric=np.array([[C[0,i+1,0,j+1] for j in range(3)] for i in range(3)])
    magnetic=np.array([[.5*sum(eps[i,k,l]*C[k+1,l+1,0,j+1] for k in range(3) for l in range(3)) for j in range(3)] for i in range(3)])
    return electric+1j*magnetic,F


def petrov(Q):
    norm=np.linalg.norm(Q); scale=max(1.,norm); Q2=Q@Q;Q3=Q2@Q;e=np.linalg.eigvals(Q)
    near=lambda value:2e-10<value/scale<5e-9
    if near(norm) or near(np.linalg.norm(Q2)) or near(np.linalg.norm(Q3)):return 'NUMERICALLY_UNRESOLVED'
    if norm<=1e-9:return 'O'
    if np.linalg.norm(Q2)<=1e-9*scale:return 'N'
    if np.linalg.norm(Q3)<=1e-9*scale:return 'III'
    ds=[abs(e[i]-e[j])/scale for i in range(3) for j in range(i+1,3)]
    if 4e-8<min(ds)<1e-6:return 'NUMERICALLY_UNRESOLVED'
    if min(ds)>2e-7:return 'I'
    i,j=min(((i,j) for i in range(3) for j in range(i+1,3)),key=lambda z:abs(e[z[0]]-e[z[1]])); lam=(e[i]+e[j])/2
    rank=np.sum(np.linalg.svd(Q-lam*np.eye(3),compute_uv=False)>1e-9*scale)
    return 'D' if rank<=1 else 'II'


def owner(W,Ric,g,E):
    Q,F=Q_from(W,E); pt=petrov(Q);scale=max(1.,np.linalg.norm(Q));ev,vec=np.linalg.eig(Q)
    residual=np.linalg.norm(Q[1:,0])/scale; best=int(np.argmax(np.abs(vec[0,:])/np.linalg.norm(vec,axis=0)));v=vec[:,best]/np.linalg.norm(vec[:,best]);target=np.zeros((3,3),complex);target[0,0]=1
    defect=np.linalg.norm(np.outer(v,v.conj())-target);gap=min(abs(ev[best]-ev[j]) for j in range(3) if j!=best)/scale; aligned=residual<=2e-7 and defect<=1e-6
    unique=pt=='D' and aligned and gap>2e-7; finite=pt=='I' and aligned
    Rf=np.einsum('ma,nb,mn->ab',F,F,Ric); op=ETA@Rf; rs=max(1.,np.linalg.norm(op));off=np.block([[np.zeros((2,2)),op[:2,2:]],[op[2:,:2],np.zeros((2,2))]])
    rr=np.linalg.norm(off)/rs; rg=min(abs(a-b) for a in np.linalg.eigvals(op[:2,:2]) for b in np.linalg.eigvals(op[2:,2:]))/rs; preserve=rr<=2e-7; owns=preserve and rg>=2e-6
    if pt=='NUMERICALLY_UNRESOLVED':oc='NUMERICALLY_UNRESOLVED'
    elif unique and owns:oc='WEYL_AND_RICCI_AGREE_ON_SPLIT'
    elif unique:oc='UNIQUE_WEYL_DERIVED_SPLIT'
    elif finite and owns:oc='RICCI_DERIVED_WITH_WEYL_ALIGNMENT'
    elif finite:oc='FINITE_WEYL_PRINCIPAL_CANDIDATES__REGISTERED_ONE_ALIGNED'
    elif pt=='O' and owns:oc='RICCI_DERIVED_WHEN_WEYL_DEGENERATE'
    elif preserve or aligned:oc='CURVATURE_ALIGNED_BUT_NOT_UNIQUE'
    elif pt in {'I','D','II'}:oc='SPLIT_MISALIGNED_WITH_CURVATURE_PRINCIPALS'
    else:oc='NO_TESTED_POINTWISE_CURVATURE_OWNER'
    return pt,oc


def relative(a,b):
    return np.linalg.norm(a-b)/max(1.,np.linalg.norm(a),np.linalg.norm(b))


def main():
    production=read_tsv(HERE/'CURVATURE_SPLIT_ATLAS.tsv'); prod_npz=np.load(HERE/'PRODUCTION_CURVATURE_TENSORS.npz')
    assert len(production)==len(prod_npz['keys'])==1806
    prod={k:(row,W,R) for k,row,W,R in zip(prod_npz['keys'],production,prod_npz['weyl'],prod_npz['ricci'])}
    comparisons=[]; independent_W=[]; independent_R=[]; keys=[]; cache={}; convergence=[]
    for s in samples():
        p=np.array([.07,1.08,.31,.44]) if s.geometry=='R17_GLOBAL' else np.array([.12,-.18,.23,-.14])
        offs=[np.zeros(4),np.array([.08,.035,-.04,.06]),np.array([.13,-.025,.07,.11])] if s.geometry=='R17_GLOBAL' else [np.zeros(4),np.array([.07,-.05,.04,.03]),np.array([.14,.025,-.06,.08])]
        for name,off in zip(('p','q','r'),offs):
            key=f'G63|{s.name}|{name}';fun=lambda x,s=s:g63_metric(x,s);x=p+off; vals=[curvature(fun,x,h) for h in FD_LADDER];W,R=vals[1];E=r17_E(x,s) if s.geometry=='R17_GLOBAL' else live_E(x,s);pt,oc=owner(W,R,fun(x),E);cache[key]=(W,R,pt,oc,vals)
    prof=profiles();controls=(('C0',0.,0.),('CMINUS',-.3,.4),('CPLUS',.3,.4));arches=('A03_RADIAL_SHIFT_TIMELIVE','A04_LAPSE_LIFT_TIMELIVE','A05_SHIFT_SUPPORTED_TAPER')
    for pid,c in sorted(prof.items()):
        for arch in arches:
            for name,eps,tau in controls:
                key=f'G85|{pid}:{arch}|{name}';ck=(arch,name) if arch=='A05_SHIFT_SUPPORTED_TAPER' else (pid,arch,name)
                if ck not in cache:
                    fun=lambda x,c=c,arch=arch,eps=eps:g85_metric(x,c,arch,eps);x=np.array([tau,np.pi/2,1.1,.37]);vals=[curvature(fun,x,h) for h in FD_LADDER];W,R=vals[1];E=metric_coframe(fun(x));pt,oc=owner(W,R,fun(x),E);cache[ck]=(W,R,pt,oc,vals)
                cache[key]=cache[ck]
    for key in prod_npz['keys']:
        row,pW,pR=prod[key];W,R,pt,oc,vals=cache[key];wd=relative(W,pW);rd=relative(R,pR);convW=relative(vals[0][0],vals[2][0]);convR=relative(vals[0][1],vals[2][1])
        passed=wd<=2e-5 and rd<=2e-5 and pt==row['petrov'] and oc==row['owner_class']
        comparisons.append({'key':key,'weyl_relative_error':f'{wd:.17g}','ricci_relative_error':f'{rd:.17g}','ladder_weyl_outer_error':f'{convW:.17g}','ladder_ricci_outer_error':f'{convR:.17g}','production_petrov':row['petrov'],'independent_petrov':pt,'production_owner':row['owner_class'],'independent_owner':oc,'pass':str(passed).upper()})
        keys.append(key);independent_W.append(W);independent_R.append(R);convergence.append((convW,convR))
    write=csv.DictWriter((HERE/'INDEPENDENT_COMPARISON.tsv').open('w',newline=''),fieldnames=list(comparisons[0]),delimiter='\t',lineterminator='\n');write.writeheader();write.writerows(comparisons)
    np.savez_compressed(HERE/'INDEPENDENT_CURVATURE_TENSORS.npz',keys=np.asarray(keys),weyl=np.asarray(independent_W),ricci=np.asarray(independent_R))
    unique_values=[value for key,value in cache.items() if isinstance(key,tuple) or (isinstance(key,str) and key.startswith('G63|'))]
    assert len(unique_values)==1221
    result={'schema':'udt-curvature-split-independent-v1','status':'PASS' if all(x['pass']=='TRUE' for x in comparisons) else 'FAIL','checks':len(comparisons),'pass_count':sum(x['pass']=='TRUE' for x in comparisons),'unique_metric_jets':len(unique_values),'unique_metric_jet_owner_counts':dict(sorted(Counter(value[3] for value in unique_values).items())),'max_weyl_relative_error':max(float(x['weyl_relative_error']) for x in comparisons),'max_ricci_relative_error':max(float(x['ricci_relative_error']) for x in comparisons),'max_ladder_weyl_outer_error':max(x[0] for x in convergence),'max_ladder_ricci_outer_error':max(x[1] for x in convergence),'petrov_counts':dict(sorted(Counter(x['independent_petrov'] for x in comparisons).items())),'owner_counts':dict(sorted(Counter(x['independent_owner'] for x in comparisons).items()))}
    (HERE/'INDEPENDENT_VERIFICATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2,sort_keys=True));assert result['status']=='PASS'


if __name__=='__main__':main()

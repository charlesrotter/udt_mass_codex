#!/usr/bin/env python3
"""Independent finite-difference/RK4 verification of the survivor atlas.

This file intentionally does not import the production implementation.
"""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
FD_H = 2.0e-5
DEXP_H = 2.0e-6
AFFINE_END = 0.40
STEPS_PER_UNIT = 1600


@dataclass(frozen=True)
class Sample:
    sample_id: str
    geometry: str
    lam: float
    eps: float
    twist: float = 0.4


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def samples():
    rows = csv.DictReader((HERE / "NUMERICAL_SAMPLE_UNIVERSE.tsv").open(), delimiter="\t")
    out = []
    for row in rows:
        p = {x.split("=", 1)[0]: x.split("=", 1)[1] for x in (row["parameter_1"], row["parameter_2"]) if "=" in x}
        out.append(Sample(row["sample_id"], row["geometry"], float(p.get("lambda", 0)), float(p.get("epsilon", 0))))
    assert len(out) == 14 and len({s.sample_id for s in out}) == 14
    return out


def phi_r17(x, eps):
    _, th, va, ps = x
    a = np.cos(th / 2) * np.cos((ps + va) / 2)
    b = np.cos(th / 2) * np.sin((ps + va) / 2)
    c = np.sin(th / 2) * np.cos((ps - va) / 2)
    d = np.sin(th / 2) * np.sin((ps - va) / 2)
    return .12*a + .08*b*c - .05*(d*d-c*c) + eps*(.11*d+.07*a*b)


def E_r17(x, s):
    _, th, _, ps = x
    u = np.exp(phi_r17(x, s.eps)); v = np.exp(s.lam * phi_r17(x, s.eps))
    one = .5*np.array([0., np.cos(ps), np.sin(ps)*np.sin(th), 0.])
    two = .5*np.array([0., -np.sin(ps), np.cos(ps)*np.sin(th), 0.])
    three = .5*np.array([0., 0., np.cos(th), 1.])
    time = np.array([1., 0., 0., 0.])
    return np.vstack(((time+s.twist*three)/u, u*three, v*one, v*two))


def E_live(x, s):
    t, xx, y, z = x; e = s.eps
    kap=.035*np.sin(t+.3*y)+.018*np.cos(xx-z)+e*.025*np.sin(t+xx+y)
    phi=.11*np.cos(xx-.2*t)+.025*np.sin(y+z)+e*.08*np.cos(t-z+.4*xx)
    beta=.12*np.sin(t+xx)+.04*np.cos(y-z)+e*.05*np.sin(t+y)
    gam=.16*np.sin(t-y+.2*z)+e*.04*np.cos(xx+z)
    q1=.045*np.cos(t+y)+e*.03*np.sin(xx-z)
    q2=-.035*np.sin(xx+z)+e*.025*np.cos(t-y)
    sh=.07*np.sin(t+xx+y+z)+e*.025*np.cos(xx-y)
    S=np.array([[.055*np.cos(t+y)+e*.02*np.sin(z), .045*np.sin(xx-z)+e*.015*np.cos(t+y)],
                [-.04*np.cos(t-xx+y)+e*.02*np.sin(xx+z), .05*np.sin(t+z)+e*.018*np.cos(xx-y)]])
    T=np.exp(kap-phi); L=np.exp(kap+phi)
    B=np.array([[T,T*beta],[0.,L]])
    R=np.array([[np.cos(gam),-np.sin(gam)],[np.sin(gam),np.cos(gam)]])
    U=np.array([[np.exp(q1),sh],[0.,np.exp(q2)]])
    Q=R@U
    E=np.zeros((4,4)); E[:2,:2]=B; E[2:,:2]=Q@S; E[2:,2:]=Q
    return E


def E(x, s):
    return E_r17(x, s) if s.geometry == "R17_GLOBAL" else E_live(x, s)


def g(x, s):
    z=E(x,s); return z.T@ETA@z


def Gamma(x, s):
    dg=np.empty((4,4,4))
    for k in range(4):
        step=np.zeros(4); step[k]=FD_H
        dg[k]=(g(x+step,s)-g(x-step,s))/(2*FD_H)
    term=dg.transpose(1,0,2)+dg.transpose(1,2,0)-dg
    return .5*np.einsum('ad,dbc->abc',np.linalg.inv(g(x,s)),term)


def x0(s):
    return np.array([.07,1.08,.31,.44]) if s.geometry=="R17_GLOBAL" else np.array([.12,-.18,.23,-.14])


def v0(s, causal):
    fr=np.linalg.inv(E(x0(s),s))
    if causal=="TIMELIKE": return (fr[:,0]+.18*fr[:,2])/np.sqrt(1-.18**2)
    return (fr[:,1]+.22*fr[:,3])/np.sqrt(1+.22**2)


def rk4(fun, y, lo, hi, n):
    h=(hi-lo)/n; t=lo
    for _ in range(n):
        k1=fun(t,y); k2=fun(t+h/2,y+h*k1/2); k3=fun(t+h/2,y+h*k2/2); k4=fun(t+h,y+h*k3)
        y=y+h*(k1+2*k2+2*k3+k4)/6; t+=h
    return y


def geodesic(s, causal, dv=None, transport=False):
    vv=v0(s,causal).copy()
    if dv is not None: vv+=dv
    y=np.concatenate((x0(s),vv,np.eye(4).ravel())) if transport else np.concatenate((x0(s),vv))
    def rhs(_, y):
        xx=y[:4]; vel=y[4:8]; GG=Gamma(xx,s); acc=-np.einsum('abc,b,c->a',GG,vel,vel)
        if not transport: return np.concatenate((vel,acc))
        P=y[8:].reshape(4,4); W=np.einsum('abc,b->ac',GG,vel)
        return np.concatenate((vel,acc,(-W@P).ravel()))
    return rk4(rhs,y,0.,AFFINE_END,int(round(STEPS_PER_UNIT*AFFINE_END)))


def dexp_sv(s, causal):
    cols=[]
    for j in range(4):
        d=np.zeros(4); d[j]=DEXP_H
        cols.append((geodesic(s,causal,d)[:4]-geodesic(s,causal,-d)[:4])/(2*DEXP_H))
    return np.linalg.svd(np.column_stack(cols),compute_uv=False)


def segment_paths(s,name):
    base=x0(s)
    if s.geometry=="R17_GLOBAL" and name=="HOPF_FIBER":
        def f(t):
            xx=base.copy(); xx[3]+=4*np.pi*t
            return xx,np.array([0.,0.,0.,4*np.pi])
        return [f]
    if s.geometry=="R17_GLOBAL": seq=[(1,.17),(2,.19),(1,-.17),(2,-.19)]
    else:
        a,b=(0,1) if name=="TX_RECTANGLE" else (2,3)
        seq=[(a,.16),(b,.18),(a,-.16),(b,-.18)]
    out=[]; cur=base.copy()
    for axis,amount in seq:
        start=cur.copy()
        def f(t,start=start,axis=axis,amount=amount):
            xx=start.copy(); xx[axis]+=amount*t
            dx=np.zeros(4); dx[axis]=amount
            return xx,dx
        out.append(f); cur[axis]+=amount
    return out


def grad_phi_r17(x,s):
    out=np.empty(4)
    for k in range(4):
        d=np.zeros(4); d[k]=FD_H
        out[k]=(phi_r17(x+d,s.eps)-phi_r17(x-d,s.eps))/(2*FD_H)
    return out


def A_normal(x,s):
    if s.geometry!="R17_GLOBAL": return np.zeros(4)
    ee=E_r17(x,s); frame=np.linalg.inv(ee); p=frame.T@grad_phi_r17(x,s)
    ph=phi_r17(x,s.eps); u=np.exp(ph); v=np.exp(s.lam*ph)
    comp=np.array([s.twist/(u*v*v),2/u-u/(v*v),-s.lam*p[3]/v,s.lam*p[2]/v])
    return comp@ee


def loop(s,name):
    y=np.concatenate((np.eye(4).ravel(),[0.]))
    for path in segment_paths(s,name):
        def rhs(t,y):
            xx,dx=path(t); W=np.einsum('abc,b->ac',Gamma(xx,s),dx); P=y[:16].reshape(4,4)
            return np.concatenate(((-W@P).ravel(),[float(A_normal(xx,s)@dx)]))
        y=rk4(rhs,y,0.,1.,STEPS_PER_UNIT)
    return y[:16].reshape(4,4),float(y[16])


def read_tsv(name):
    return list(csv.DictReader((HERE/name).open(),delimiter='\t'))


def parse_matrix(text):
    return np.array([float(x) for x in text.split(';')]).reshape(4,4)


def main():
    prod_geo={r['sample_id']:r for r in read_tsv('SOLVED_GEOMETRY_ATLAS.tsv')}
    prod_g={(r['sample_id'],r['causal_class']):r for r in read_tsv('GEODESIC_DIAGNOSTICS.tsv')}
    prod_p={(r['sample_id'],r['path']):r for r in read_tsv('PATH_DIAGNOSTICS.tsv')}
    checks=[]; max_endpoint=0.; max_hol=0.; max_angle=0.; max_norm=0.; max_metric=0.; max_atlas=0.; max_phi=0.
    for s in samples():
        # Independent endpoint atlas and R17 phi identity.
        p=x0(s); q=p+(np.array([.08,.035,-.04,.06]) if s.geometry=='R17_GLOBAL' else np.array([.07,-.05,.04,.03])); r=p+(np.array([.13,-.025,.07,.11]) if s.geometry=='R17_GLOBAL' else np.array([.14,.025,-.06,.08]))
        Ep,Eq,Er=E(p,s),E(q,s),E(r,s)
        defect=np.linalg.norm(np.linalg.solve(Er,Eq)@np.linalg.solve(Eq,Ep)-np.linalg.solve(Er,Ep)); max_atlas=max(max_atlas,float(defect))
        if s.geometry=='R17_GLOBAL':
            def pp(x):
                gg=g(x,s); J=np.zeros((4,2)); J[0,0]=1; J[3,1]=2; h=J.T@gg@J
                return .25*np.log((-np.linalg.det(h))/(h[0,0]**2))
            max_phi=max(max_phi,abs((pp(q)-pp(p))-(phi_r17(q,s.eps)-phi_r17(p,s.eps))))
        for causal in ('TIMELIKE','SPACELIKE'):
            y=geodesic(s,causal,transport=True); row=prod_g[(s.sample_id,causal)]
            xp=np.array([float(z) for z in row['endpoint_x'].split(';')]); ed=float(np.linalg.norm(y[:4]-xp)); max_endpoint=max(max_endpoint,ed)
            vv=v0(s,causal); ni=vv@g(p,s)@vv; nf=y[4:8]@g(y[:4],s)@y[4:8]; max_norm=max(max_norm,abs(float(nf-ni)))
            P=y[8:].reshape(4,4); md=np.linalg.norm(P.T@g(y[:4],s)@P-g(p,s)); max_metric=max(max_metric,float(md))
            sv=dexp_sv(s,causal); independent_class='NEAR_CONJUGATE_OR_NUMERICALLY_UNRESOLVED' if sv[-1]<1e-5 else ('REGULAR_PROPAGATOR' if abs(nf-ni)<=5e-8 and md<=5e-8 else 'NUMERIC_UNRESOLVED')
            checks.append({'sample_id':s.sample_id,'object':causal,'kind':'GEODESIC','endpoint_diff':f'{ed:.17g}','holonomy_diff':'NA','normal_angle_diff':'NA','independent_class':independent_class,'production_class':row['classification'],'pass':str(ed<=2e-4 and independent_class==row['classification']).upper()})
        names=('HOPF_FIBER','LOCAL_RECTANGLE') if s.geometry=='R17_GLOBAL' else ('TX_RECTANGLE','YZ_RECTANGLE')
        for name in names:
            P,angle=loop(s,name); row=prod_p[(s.sample_id,name)]; hp=parse_matrix(row['holonomy_matrix']); hd=float(np.linalg.norm(P-hp)); max_hol=max(max_hol,hd)
            ad=0. if row['normal_connection_angle']=='NA' else abs(angle-float(row['normal_connection_angle'])); max_angle=max(max_angle,ad)
            ic='NONIDENTITY' if np.linalg.norm(P-np.eye(4))>1e-5 else 'IDENTITY_WITHIN_TOLERANCE'
            checks.append({'sample_id':s.sample_id,'object':name,'kind':'PATH','endpoint_diff':'NA','holonomy_diff':f'{hd:.17g}','normal_angle_diff':f'{ad:.17g}' if row['normal_connection_angle']!='NA' else 'NA','independent_class':ic,'production_class':row['classification'],'pass':str(hd<=3e-4 and ad<=3e-4 and ic==row['classification']).upper()})
    fields=list(checks[0]);
    with (HERE/'INDEPENDENT_COMPARISON.tsv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(checks)
    result={'schema':'UDT_SOLVED_GEOMETRY_INDEPENDENT_V1','status':'PASS' if all(r['pass']=='TRUE' for r in checks) else 'FAIL','checks':len(checks),'pass_count':sum(r['pass']=='TRUE' for r in checks),'maxima':{'atlas_defect':max_atlas,'r17_phi_identity_defect':max_phi,'geodesic_endpoint_diff':max_endpoint,'geodesic_norm_drift':max_norm,'transport_metric_defect':max_metric,'holonomy_matrix_diff':max_hol,'normal_angle_diff':max_angle},'production_hashes':{n:file_hash(HERE/n) for n in ('SOLVED_GEOMETRY_ATLAS.tsv','GEODESIC_DIAGNOSTICS.tsv','PATH_DIAGNOSTICS.tsv','DERIVATION_RESULT.json')}}
    (HERE/'INDEPENDENT_VERIFICATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
    if result['status']!='PASS': raise SystemExit(1)


if __name__=='__main__':
    main()

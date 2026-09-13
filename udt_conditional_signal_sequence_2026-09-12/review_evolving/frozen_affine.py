#!/usr/bin/env python3
import json,time
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root
from independent_affine import field,sky_angles,basis,A,B,TMAX
HERE=Path(__file__).resolve().parent
rows=[json.loads(x)['row']['fine'] for x in (HERE/'affine_initial.stdout').read_text().splitlines() if json.loads(x)['kind']=='sample']
def frozen_ray(te,to,s,eps):
    N,ll,*_=field(te,A[0],eps);v0=np.r_[te,A,-N,ll*s]
    def rhs(l,v):
        N,ll,gi,gt,gx=field(te,v[1],eps)
        return np.r_[gi*v[4:],0.,-.5*np.dot(gx,v[4:]**2),0.,0.]
    def ev(l,v):return v[0]-to
    ev.terminal=True;ev.direction=1
    sol=solve_ivp(rhs,(0,200),v0,rtol=2e-12,atol=2e-14,method='DOP853',events=ev)
    if not sol.success or len(sol.t_events[0])!=1:raise RuntimeError('frozen event failure')
    return sol.y[:,-1],max(abs(sol.y[4]+N))
started=time.time();results=[]
for row in rows:
    te=row['t_e'];eps=row['eps'];N,ll,*_=field(te,A[0],eps);d=ll*(B-A);s=d/np.linalg.norm(d)
    guess=[np.arccos(s[0]),np.arctan2(s[2],s[1]),te+np.linalg.norm(d)/N]
    def resid(z):
        if not te<z[2]<TMAX:return np.ones(3)*1000+(z[2]-te)
        return frozen_ray(te,z[2],sky_angles(*z[:2]),eps)[0][1:4]-B
    rr=root(resid,guess,tol=1e-10);ss=sky_angles(*rr.x[:2]);to=rr.x[2]
    out,pt_error=frozen_ray(te,to,ss,eps)
    No,lo,*_=field(te,B[0],eps);omega=-out[4]/No;R=1/omega;so=out[5:]/lo/omega
    cols=[];eta=1e-4
    for e in basis(ss).T:
        p=ss+eta*e;p/=np.linalg.norm(p);m=ss-eta*e;m/=np.linalg.norm(m)
        yp=frozen_ray(te,to,p,eps)[0];ym=frozen_ray(te,to,m,eps)[0]
        cols.append((yp[1:4]-ym[1:4])/(2*eta))
    DD=basis(so).T@(lo[:,None]*np.column_stack(cols))
    result={'eps':eps,'tau_e':row['tau_e'],'t_e':te,'t_o':float(to),'coordinate_flight':float(to-te),
      'sky_e':ss.tolist(),'sky_o':so.tolist(),'area':float(abs(np.linalg.det(DD))),
      'widths':np.linalg.svd(DD,compute_uv=False).tolist(),'R':R,'stationary_R':No/N,
      'stationary_error':abs(R/(No/N)-1),'p_t_conservation':float(pt_error),
      'endpoint_error':float(np.linalg.norm(out[1:4]-B)),'root_success':bool(rr.success)}
    result['pass']=bool(result['stationary_error']<2e-8 and result['endpoint_error']<2e-8 and te<to<TMAX)
    results.append(result);print(json.dumps({'kind':'frozen','row':result}),flush=True)
passed=all(r['pass'] for r in results)
print(json.dumps({'kind':'summary','all_pass':passed,'count':len(results),'elapsed_seconds':time.time()-started}),flush=True)
if not passed:raise SystemExit(1)

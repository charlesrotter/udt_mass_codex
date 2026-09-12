"""Independent affine-geodesic replay; no parent scientific implementation imports."""
import hashlib
import json
import math
from pathlib import Path
import platform
import time
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

BASE=Path(__file__).resolve().parent
START=time.monotonic()
RA,RB,PHI=6.,8.,2.
CASES=[(a,b) for a in [-.002,0.,.002] for b in [-.4,0.,.4]]
CONTROLS={'coarse':dict(rtol=2e-10,atol=2e-12,max_step=.1),
          'fine':dict(rtol=2e-12,atol=2e-14,max_step=.05)}
rows=[]
failures=[]
checks=[]

def check(label,passed,actual=None,limit=None):
    checks.append(dict(name=label,passed=bool(passed),actual=actual,limit=limit))
    if not passed: failures.append(label)

def integrate(p,a,b,controls,detail=False):
    def lapse(r):return 1+a*r*r+b/r
    j=p/math.sqrt(lapse(p))
    def rhs(lam,y):
        r,v,T,phi=y
        return [v,j*j*(2*r+3*b)/(2*r**4),1/lapse(r),j/r**2]
    def event_a(lam,y):return y[0]-RA
    def event_b(lam,y):return y[0]-RB
    event_a.direction=1
    event_b.direction=1
    event_b.terminal=True
    sol=solve_ivp(rhs,(0.,100.),[p,0.,0.,0.],method='DOP853',
                  events=[event_a,event_b],dense_output=True,**controls)
    if not sol.success or len(sol.t_events[0])!=1 or len(sol.t_events[1])!=1:
        raise RuntimeError(f'IVP/event failure at p={p}, a={a}, b={b}: {sol.message}')
    ya,yb=sol.y_events[0][0],sol.y_events[1][0]
    mismatch=float(ya[3]+yb[3]-PHI)
    if not detail:return mismatch
    # Tetrad tangent components (the source direction is opposite the arriving tangent).
    fB=lapse(RB)
    khat_rad=float(yb[1])/math.sqrt(fB)
    khat_ang=j/RB
    psi=math.atan2(khat_ang,khat_rad)
    rtt=2*math.sqrt(lapse(RA))*float(ya[2]+yb[2])
    lam=np.unique(np.r_[sol.t,np.linspace(0,sol.t[-1],201)])
    vals=sol.sol(lam)
    rr,vv=vals[0],vals[1]
    ff=1+a*rr*rr+b/rr
    residual=(-1+vv*vv+j*j*ff/(rr*rr))/ff
    return dict(p=p,j=j,psi_B=psi,tau_round_over_L_cE=rtt,
                T_oneway=float(ya[2]+yb[2]),phi_residual=mismatch,
                null_residual_max=float(np.max(np.abs(residual))),
                endpoint_radius_error=max(abs(float(ya[0])-RA),abs(float(yb[0])-RB)),
                lambda_max=float(sol.t[-1]),sample_count=len(lam),nfev=sol.nfev,
                r_min=float(np.min(rr)),r_max=float(np.max(rr)),sampled_f_min=float(np.min(ff)),
                endpoint_A=ya.tolist(),endpoint_B=yb.tolist())

try:
    for a,b in CASES:
        for label,controls in CONTROLS.items():
            left,right=integrate(2.,a,b,controls),integrate(5.5,a,b,controls)
            check(f'{a},{b},{label}: bracket',left*right<0,[left,right],0)
            if left*right>=0:raise RuntimeError('frozen root bracket does not enclose ray')
            p=brentq(lambda p:integrate(p,a,b,controls),2.,5.5,xtol=2e-12,rtol=1e-13,maxiter=100)
            data=integrate(p,a,b,controls,True)
            data.update(a=a,b=b,control=label,controls=controls,bracket_residuals=[left,right])
            rows.append(data)
            check(f'{a},{b},{label}: original null equation',data['null_residual_max']<=2e-8,data['null_residual_max'],2e-8)
            check(f'{a},{b},{label}: endpoint radii',data['endpoint_radius_error']<=2e-10,data['endpoint_radius_error'],2e-10)
            check(f'{a},{b},{label}: angular boundary',abs(data['phi_residual'])<=2e-8,abs(data['phi_residual']),2e-8)
            check(f'{a},{b},{label}: finite admitted window',data['r_min']>=1.5 and data['r_max']<=10.,[data['r_min'],data['r_max']],[1.5,10.])
    lookup={(d['a'],d['b'],d['control']):d for d in rows}
    for a,b in CASES:
        coarse,fine=lookup[(a,b,'coarse')],lookup[(a,b,'fine')]
        for field in ['p','psi_B','tau_round_over_L_cE']:
            err=abs(coarse[field]-fine[field]);lim=2e-8*max(1,abs(fine[field]))
            check(f'{a},{b}: convergence {field}',err<=lim,err,lim)
    d=math.sqrt(RA**2+RB**2-2*RA*RB*math.cos(PHI))
    pf=RA*RB*math.sin(PHI)/d
    flat={'p':pf,'psi_B':math.asin(pf/RB),'tau_round_over_L_cE':2*d}
    for field,value in flat.items():
        err=abs(lookup[(0.,0.,'fine')][field]-value);lim=2e-8*max(1,abs(value))
        check('flat exact chord '+field,err<=lim,err,lim)
    for b in [-.4,0.,.4]:
        subset=[lookup[(a,b,'fine')] for a in [-.002,0.,.002]]
        prange=max(d['p'] for d in subset)-min(d['p'] for d in subset)
        arange=max(d['psi_B'] for d in subset)-min(d['psi_B'] for d in subset)
        check(f'{b}: fixed-shape periapse invariance',prange<=2e-8,prange,2e-8)
        check(f'{b}: retained local angle sensitivity',arange>1e-5,arange,1e-5)
except Exception as exc:
    failures.append(type(exc).__name__+': '+str(exc))
finally:
    result={'status':'PASS' if not failures else 'FAIL','method':'independent affine DOP853 geodesic integration',
            'imports_parent_scientific_code':False,'dtype':'FLOAT64','rows':rows,'checks':checks,'failures':failures,
            'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'freeze_sha256':hashlib.sha256((BASE/'NUMERICAL_REPLAY_FREEZE.md').read_bytes()).hexdigest(),
            'elapsed_seconds':time.monotonic()-START}
    with (BASE/'INDEPENDENT_GEODESIC_RESULT.json').open('x') as out:json.dump(result,out,indent=2);out.write('\n')
    print(json.dumps({'status':result['status'],'rows':len(rows),'checks':len(checks),'failures':failures,
                      'elapsed_seconds':result['elapsed_seconds'],
                      'max_null_residual':max((r['null_residual_max'] for r in rows),default=None)},sort_keys=True))
if failures:raise SystemExit(1)

#!/usr/bin/env python3
import json,time
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from independent_affine import field,rhs,endpoint,ray,basis,A,B

HERE=Path(__file__).resolve().parent
rows=[json.loads(x)['row'] for x in (HERE/'affine_initial.stdout').read_text().splitlines() if json.loads(x)['kind']=='sample']

def back(te,to,s,eps,tol=2e-12,wrongomega=None):
    N,ll,*_=field(to,B[0],eps)
    scale=1 if wrongomega is None else wrongomega
    # Wrong variant keeps momentum magnitude omega_o while using unit-frequency angular increments.
    y0=np.r_[to,B,-N*scale,ll*s]
    if wrongomega is not None:
        y0[4]=-N*np.linalg.norm(s)
    def ev(l,v):return v[0]-te
    ev.terminal=True;ev.direction=-1
    out=solve_ivp(lambda l,v:rhs(l,v,eps),(0.,-200.),y0,rtol=tol,atol=tol*.01,method='DOP853',events=ev)
    if not out.success or len(out.t_events[0])!=1:raise RuntimeError('backward failure')
    return out.y[:,-1]

def reverse(row,eta,wrong=False):
    rr=row['fine'];eps=rr['eps'];te=rr['t_e'];to=rr['t_o'];so=np.array(rr['sky_o']);ee=basis(so)
    central=back(te,to,so,eps)
    cols=[]
    for e in ee.T:
        if not wrong:
            p=so+eta*e;p/=np.linalg.norm(p)
            m=so-eta*e;m/=np.linalg.norm(m)
            yp=back(te,to,p,eps);ym=back(te,to,m,eps)
        else:
            om=1/rr['R']
            p=om*so+eta*e;m=om*so-eta*e
            yp=back(te,to,p,eps,wrongomega=om);ym=back(te,to,m,eps,wrongomega=om)
        cols.append((yp[1:4]-ym[1:4])/(2*eta))
    NA,la,*_=field(te,A[0],eps);ea=basis(np.array(rr['sky_e']))
    dd=ea.T@(la[:,None]*np.column_stack(cols));area=abs(np.linalg.det(dd))
    ratio=row['beam_fine_angle']['area']/area
    return {'area':float(area),'widths':np.linalg.svd(dd,compute_uv=False).tolist(),
      'clock_area_error':float(abs(ratio/rr['R']**2-1)),
      'central_endpoint_error':float(np.linalg.norm(central[1:4]-A))}

started=time.time();rev=[];dur=[];cal=[];host=[]
for row in rows:
    r1=reverse(row,1e-4);r2=reverse(row,5e-5)
    rr={'eps':row['eps'],'tau_e':row['tau_e'],'coarse':r1,'fine':r2,
        'angle_convergence':abs(r1['area']/r2['area']-1)}
    rr['pass']=r2['clock_area_error']<2e-6 and r2['central_endpoint_error']<2e-8 and rr['angle_convergence']<2e-6
    rev.append(rr);print(json.dumps({'kind':'reverse','row':rr}),flush=True)
for eps in [-.5,0.,.5]:
    records=[]
    for n in [8,16]:
        xx,ww=np.polynomial.legendre.leggauss(n);vals=[]
        for s in .6*(xx+1): vals.append(endpoint(float(s),eps,tol=2e-12)['R'])
        records.append(float(.6*np.dot(ww,vals)))
    r0=next(r['fine'] for r in rows if r['eps']==eps and r['tau_e']==0)
    r1=next(r['fine'] for r in rows if r['eps']==eps and r['tau_e']==1.2)
    du=r1['tau_o']-r0['tau_o'];expected=1.2*r0['R']
    dd={'eps':eps,'arrival_difference':du,'quadratures':records,'D_event':du/1.2,
      'initial_pulse_R':r0['R'],'initial_pulse_duration_error':expected-du,
      'quadrature_error':abs(records[-1]/du-1),'convergence':abs(records[-1]/records[0]-1)}
    dd['pass']=dd['quadrature_error']<2e-7 and dd['convergence']<2e-7
    dur.append(dd);print(json.dumps({'kind':'duration','row':dd}),flush=True)
    for x in [.7,np.pi/(2*.75)]:
        estimates=[]
        for h in [2e-5,1e-5]:
            N0,l0,*_=field(1.,x,eps)
            lp=field(1+h,x,eps)[1];lm=field(1-h,x,eps)[1]
            H=(np.log(lp)-np.log(lm))/(2*h*N0*1.7)
            S=H[1]+H[2];D=H[1]-H[2];scale=4/(3*S)
            eh=None if x!=.7 else 2*D/(3*S*np.cos(.75*x))
            estimates.append({'H':H.tolist(),'scale':scale,'epsilon':eh})
        ce={'eps':eps,'x':x,'estimates':estimates,'scale_error':abs(estimates[-1]['scale']/1.7-1)}
        ce['epsilon_error']=None if x!=.7 else abs(estimates[-1]['epsilon']-eps)
        ce['pass']=bool(ce['scale_error']<2e-7 and (ce['epsilon_error'] is None or ce['epsilon_error']<2e-7))
        cal.append(ce);print(json.dumps({'kind':'calibration','row':ce}),flush=True)
# Wrong source t=1 covector, at later emission, evolved on actual metric.
r=next(r for r in rows if r['eps']==.5 and r['tau_e']==.4)['fine'];te=r['t_e'];to=r['t_o'];s=np.array(r['sky_e'])
N0,ll0,*_=field(1.,A[0],.5);Ne,lle,gie,*_=field(te,A[0],.5)
pwrong=ll0*s
# Enforce null after wrong source ruler, so this tests endpoint protocol rather than just nullness.
ptwrong=-Ne*np.linalg.norm(pwrong/lle)
y0=np.r_[te,A,ptwrong,pwrong]
def ev(l,v):return v[0]-to
ev.terminal=True;ev.direction=1
sol=solve_ivp(lambda l,v:rhs(l,v,.5),(0,200),y0,rtol=2e-12,atol=2e-14,method='DOP853',events=ev)
o=sol.y[:,-1]
host.append({'mutation':'old source ruler at later actual te, null reimposed','endpoint_error':float(np.linalg.norm(o[1:4]-B)),
             'caught':bool(np.linalg.norm(o[1:4]-B)>2e-8)})
wrong=reverse(next(x for x in rows if x['eps']==.5 and x['tau_e']==.4),5e-5,wrong=True)
host.append({'mutation':'reverse retains forward omega while angular ruler uses unit frequency','result':wrong,
             'caught':bool(wrong['clock_area_error']>2e-6)})
print(json.dumps({'kind':'hostile','rows':host}),flush=True)
passed=all(x['pass'] for x in rev+dur+cal) and all(x['caught'] for x in host)
print(json.dumps({'kind':'summary','all_pass':passed,'reverse_count':len(rev),'duration_count':len(dur),
                 'calibration_count':len(cal),'elapsed_seconds':time.time()-started}),flush=True)
if not passed:raise SystemExit(1)

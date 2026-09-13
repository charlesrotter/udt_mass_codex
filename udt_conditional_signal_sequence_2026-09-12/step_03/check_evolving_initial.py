#!/usr/bin/env python3
"""CSS3/5 finite protocol; source metric/Hessian reused unchanged, not independent."""
import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys
sys.dont_write_bytecode=True
import argparse,importlib.util,json,math,platform,pathlib,traceback
import numpy as np
import scipy
from scipy.integrate import solve_ivp,quad
from scipy.optimize import least_squares,brentq
from scipy.special import jv,yv
from numpy.polynomial.legendre import leggauss
ROOT=pathlib.Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('ntb',ROOT/'udt_ne1_tilted_beam_geometry_2026-09-12/discover_beams.py')
ntb=importlib.util.module_from_spec(spec);spec.loader.exec_module(ntb)
XA=np.array([.7,0.,0.]);XB=np.array([1.7,1.2,.7]);MUT=None
SYM=np.block([[np.zeros((3,3)),np.eye(3)],[-np.eye(3),np.zeros((3,3))]])
CHECKS=[]
def guard(name,error,tol=2e-7):
    value=float(error);CHECKS.append({'name':name,'error':value,'tolerance':tol})
    if not np.isfinite(value) or value>tol:raise AssertionError((name,value,tol))
def diff(a,b):return float(np.max(np.abs(np.asarray(a)-np.asarray(b))/(1+np.abs(b))))
def clock(t,xi,eps):return quad(lambda u:ntb.fields(u,xi,eps)[0][0],1,t,epsabs=2e-11,epsrel=2e-11)[0]
def emit(s,eps):return 1. if s==0 else brentq(lambda t:clock(t,XA[0],eps)-s,1,8,xtol=2e-12,rtol=2e-14)
def chart(q):
    v=np.r_[1.,q];n=np.linalg.norm(v);s=v/n
    return s,(np.eye(3)-np.outer(s,s))[:,1:]/n

def integrate(te,to,initial,eps,tight=False,frozen=False):
    sol=solve_ivp(lambda t,y:ntb.flow(te if frozen else t,y,eps),(te,to),initial,
        method='DOP853',rtol=2e-11 if tight else 2e-10,atol=2e-13 if tight else 2e-12,
        max_step=.05 if tight else .1)
    if not sol.success:raise RuntimeError(sol.message)
    return sol.y[:,-1]

def shoot(te,eps,q,to,tight=False,frozen=False):
    se,_=chart(q);le=ntb.fields(te,XA[0],eps)[0]
    if MUT=='source_epoch':le=ntb.fields(1.,XA[0],eps)[0]
    ini=np.r_[XA,le*se,np.eye(6).ravel()]
    return integrate(te,to,ini,eps,tight,frozen),ini,se

def readout(te,to,eps,state,ini,se,frozen=False,implicit=True):
    le=ntb.fields(te,XA[0],eps)[0];lo=ntb.fields(te if frozen else to,state[0],eps)[0]
    guard('actual_source_frequency',abs(np.linalg.norm(ini[3:6]/le)-1),2e-12)
    E=ntb.screen(se);p=state[3:6];w=np.linalg.norm(p/lo);so=p/lo/w;Eo=ntb.screen(so)
    M=state[6:].reshape(6,6);beam_le=ntb.fields(1.,XA[0],eps)[0] if MUT=='beam_epoch' else le
    X=lo[:,None]*(M[:3,3:]@(beam_le[:,None]*E));D=Eo.T@X
    widths=np.linalg.svd(D,compute_uv=False);area=abs(np.linalg.det(D))
    v=ntb.flow(te if frozen else to,state,eps,False)[:3]
    J=np.column_stack((M[:3,3:]@(le[:,None]*E),v))
    guard('endpoint_condition',np.linalg.cond(J),1e8)
    guard('positive_beam_width',1e-8/max(float(min(widths)),1e-300),1.)
    guard('symplectic',np.linalg.norm(M.T@SYM@M-SYM,np.inf)/(1+np.linalg.norm(M,np.inf)**2))
    guard('screen_orthogonality',np.max(np.abs(so@X))/(1+np.linalg.norm(X)))
    guard('endpoint_beam_rank_identity',diff(np.linalg.det(J),np.linalg.det(D)/ (te if frozen else to)))
    R=1/w;implicit_R=None
    if not frozen and implicit:
        f=ntb.AA*jv(0,ntb.K*te)+ntb.BB*yv(0,ntb.K*te)
        fp=-ntb.K*(ntb.AA*jv(1,ntb.K*te)+ntb.BB*yv(1,ntb.K*te))
        pt=eps*fp*np.cos(ntb.K*XA[0]);px=-eps*ntb.K*f*np.sin(ntb.K*XA[0])
        logs=np.array([-1/(4*te)+te*(pt*pt+px*px)/4,1/(2*te)+pt/2,1/(2*te)-pt/2])
        we=np.r_[np.zeros(3),le*logs*se]
        if MUT!='missing_initial_flow':we-=ntb.flow(te,ini,eps,False)
        deriv=np.linalg.solve(J,-(M@we)[:3]);implicit_R=lo[0]/le[0]*deriv[2]
        guard('changing_initial_time_clock',diff(implicit_R,R))
    if frozen:guard('stationary_frozen_clock',diff(R,lo[0]/le[0]))
    return dict(epsilon=eps,te=te,to=to,flight=to-te,R=R,implicit_R=implicit_R,
        arrival_clock=None if frozen else clock(to,XB[0],eps),source_sky=se,arrival_sky=so,
        source_screen=E,arrival_screen=Eo,screen_map=D,widths=widths,area=area,
        endpoint_condition=np.linalg.cond(J),state=state,initial=ini,frozen=frozen)

def boundary(s,eps,tight=False,frozen=False):
    te=emit(s,eps);le=ntb.fields(te,XA[0],eps)[0];v=le*(XB-XA)
    guess=np.r_[v[1:]/v[0],np.linalg.norm(v)/le[0]];cache={}
    def calc(z):
        key=tuple(z)
        if key not in cache:
            state,ini,se=shoot(te,eps,z[:2],te+z[2],tight,frozen)
            _,ds=chart(z[:2]);M=state[6:].reshape(6,6)
            jac=np.column_stack((M[:3,3:]@(le[:,None]*ds),ntb.flow(te if frozen else te+z[2],state,eps,False)[:3]))
            cache[key]=(state[:3]-XB,jac,state,ini,se)
        return cache[key]
    opt=least_squares(lambda z:calc(z)[0],guess,jac=lambda z:calc(z)[1],
        bounds=([-8,-8,.02],[8,8,12-te]),max_nfev=30,xtol=2e-12,ftol=2e-12,gtol=2e-12)
    residual,jac,state,ini,se=calc(opt.x)
    guard('original_endpoint',np.max(np.abs(residual)),2e-8)
    row=readout(te,te+opt.x[2],eps,state,ini,se,frozen)
    row.update(source_clock=s,endpoint_residual=np.max(np.abs(residual)),root_nfev=opt.nfev)
    return row

def reverse(row):
    eps,te,to=row['epsilon'],row['te'],row['to'];state=row['state']
    out=integrate(to,te,np.r_[state[:6],np.eye(6).ravel()],eps,True)
    guard('reverse_central_endpoint',diff(out[:6],row['initial'][:6]))
    le=ntb.fields(te,XA[0],eps)[0];lo=ntb.fields(to,XB[0],eps)[0]
    scale=1. if MUT=='reverse_frequency' else 1/row['R']
    Dr=row['source_screen'].T@(le[:,None]*(out[6:].reshape(6,6)[:3,3:]@(scale*lo[:,None]*row['arrival_screen'])))
    ar=abs(np.linalg.det(Dr));guard('same_segment_area_reciprocity',diff(row['area']/ar,row['R']**2))
    return {'epsilon':eps,'source_clock':row['source_clock'],'reverse_area':ar,'reverse_map':Dr,'reverse_state':out}

def axial(eps,te):
    le=ntb.fields(te,XA[0],eps)[0];ini=np.r_[XA,le*np.array([1.,0.,0.]),np.eye(6).ravel()]
    state=integrate(te,te+1,ini,eps,True);row=readout(te,te+1,eps,state,ini,np.array([1.,0.,0.]))
    lo=ntb.fields(te+1,XA[0]+1,eps)[0]
    expected=[lo[j]*le[j]/le[0]*quad(lambda u:ntb.fields(u,XA[0]+u-te,eps)[1][j],te,te+1,epsabs=2e-11,epsrel=2e-11)[0] for j in [1,2]]
    guard('exact_axial_widths',diff(sorted(row['widths']),sorted(expected)))
    guard('exact_axial_clock',diff(row['R'],lo[0]/le[0]));row['exact_widths']=expected
    return row

def calibration():
    import sympy as sp
    L,c,S,e,C,ds,A=sp.symbols('L c S e C ds A',nonzero=True,real=True)
    hy=2*c/(3*L)+c*e*C/L;hz=2*c/(3*L)-c*e*C/L
    identities=[sp.simplify(4*c/(3*(hy+hz))-L),sp.simplify(sp.Rational(2,3)*(hy-hz)/((hy+hz)*C)-e),
        sp.simplify(L**2*A/(c**2*(L/c*ds)**2)-A/ds**2)]
    assert identities==[0,0,0]
    assert sp.simplify((hy-hz).subs(C,0))==0
    return {'exact_sympy_identities':[str(v) for v in identities],'sympy':sp.__version__,
      'limits':'C=cos(k xi_A) nonzero required for amplitude. Epoch/phase/axes supplied; no native scale selection. Scale identity uses jointly scaled protocol.'}

def serial(v):
    if isinstance(v,np.ndarray):return v.tolist()
    if isinstance(v,np.generic):return v.item()
    raise TypeError(type(v).__name__)

def main():
    global MUT
    p=argparse.ArgumentParser();p.add_argument('--mutate',choices=['source_epoch','missing_initial_flow','reverse_frequency','beam_epoch']);args=p.parse_args();MUT=args.mutate
    records=[];out={'records':records,'mutation':MUT,'checks':CHECKS,'dtype':'float64',
      'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},'scope':'Conditional finite diagnostics, not global uniqueness or observed physics.'}
    try:
        if MUT:
            row=boundary(.4,.5);records.append(row)
            if MUT=='reverse_frequency':out['reverse']=[reverse(row)]
            raise AssertionError('hostile mutation survived intended guards')
        for eps in [-.5,0.,.5]:
            for s in [0.,.4,.8,1.2]:
                row=boundary(s,eps);records.append(row);tight=boundary(s,eps,True)
                for key in ['to','arrival_clock','R','source_sky','arrival_sky','widths','area','screen_map']:
                    guard('tighter_'+key,diff(row[key],tight[key]))
                row['tight']=tight;row['frozen_control']=boundary(s,eps,frozen=True)
        out['clock_finite_difference']=[];out['reverse']=[]
        for eps in [-.5,0.,.5]:
            row=next(r for r in records if r['epsilon']==eps and r['source_clock']==.4)
            minus=boundary(.4-1e-4,eps,True);plus=boundary(.4+1e-4,eps,True)
            derivative=(plus['arrival_clock']-minus['arrival_clock'])/2e-4
            guard('independent_emission_clock_difference',diff(derivative,row['R']),2e-6)
            out['clock_finite_difference'].append({'epsilon':eps,'derivative':derivative,'minus':minus,'plus':plus})
            out['reverse'].append(reverse(row))
        out['axial']=[axial(.5,1.6),axial(-.5,2.4)]
        out['events']=[]
        for eps in [-.5,0.,.5]:
            endpoints=[next(r for r in records if r['epsilon']==eps and r['source_clock']==s) for s in [0.,1.2]]
            delta=endpoints[1]['arrival_clock']-endpoints[0]['arrival_clock'];qs=[]
            ev={'epsilon':eps,'source_duration':1.2,'arrival_duration':delta,'mean_R':delta/1.2,'initial_R':endpoints[0]['R'],'quadratures':[]}
            out['events'].append(ev)
            for n in [8,16]:
                x,w=leggauss(n);nodes=[boundary(.6*(xx+1),eps,True) for xx in x]
                val=.6*sum(ww*r['R'] for ww,r in zip(w,nodes));qs.append(val)
                ev['quadratures'].append({'n':n,'integral':val,'nodes':nodes})
                guard('whole_event_endpoint_vs_integral',diff(val,delta))
            guard('whole_event_quadrature_refinement',diff(qs[0],qs[1]))
            ev['single_initial_pulse_duration_error']=1.2*endpoints[0]['R']-delta
        out['calibration']=calibration();out['status']='PASS'
    except Exception as exc:
        out['status']='FAIL';out['failure']=repr(exc);traceback.print_exc(file=sys.stderr)
    print(json.dumps(out,indent=2,default=serial,allow_nan=False));return 0 if out['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())

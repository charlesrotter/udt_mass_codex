#!/usr/bin/env python3
"""Finite float64 support, never an asymptotic proof or interval certificate."""
import itertools
import json
import math
import platform
import sys
import warnings
import numpy as np
import scipy
from scipy.integrate import quad, solve_ivp
from scipy.special import jv, yv

# SUPPLIED G394 normalization, not a selected physical scale.
k=0.75
Ac=-3*math.pi*yv(0,k)/4
Bc=3*math.pi*jv(0,k)/4
sigma=k*(Ac*Ac+Bc*Bc)/math.pi
phase=math.pi/4+math.atan2(Bc,Ac)
records=[]
warning_log=[]

def point(t, x, eps, s):
    f=Ac*jv(0,k*t)+Bc*yv(0,k*t)
    fp=-k*(Ac*jv(1,k*t)+Bc*yv(1,k*t))
    fpp=-fp/t-k*k*f
    co,si=math.cos(k*x),math.sin(k*x)
    p=eps*f*co
    p1=eps*(fp*co-s*k*f*si)
    p2=eps*((fpp-k*k*f)*co-2*s*k*fp*si)
    ell=eps*eps*(t*t*(fp*fp+k*k*f*f)/2+t*f*fp/2-9/8+t*f*fp*math.cos(2*k*x)/2)
    n=0.75*t**(-0.25)*math.exp(ell/4)
    bs=np.array([math.sqrt(t)*math.exp(p/2),math.sqrt(t)*math.exp(-p/2)])
    ap=(t*p1*p1-1/t)/4  # Original NE1 null constraint, checked against closed ell below.
    qp=np.array([(1/t+p1)/2,(1/t-p1)/2])
    qpp=np.array([(-1/t**2+p2)/2,(-1/t**2-p2)/2])
    bracket=qpp+qp*qp-2*ap*qp
    return n,bs,ell,p,p1,ap,bracket

def integ(fun,lo,hi):
    val,err=quad(fun,lo,hi,epsabs=2e-11,epsrel=2e-11,limit=500)
    return val,err

def finite(eps,te,xe,s,d,rtol=2e-11,atol=2e-12):
    to=te+d
    at=lambda t:point(t,xe+s*(t-te),eps,s)
    ne,be,le,*_=at(te)
    no,bo,lo,*_=at(to)
    ints=[integ(lambda t:at(t)[0]**2/at(t)[1][i]**2,te,to) for i in (0,1)]
    expected=be*bo/ne*np.array([q[0] for q in ints])
    def rhs(t,state):
        n,bs,ell,p,p1,ap,br=at(t)
        return [state[1],2*ap*state[1]+br[0]*state[0],state[3],2*ap*state[3]+br[1]*state[2],-ap*state[4]]
    sol=solve_ivp(rhs,(te,to),[0,ne,0,ne,1],method='DOP853',rtol=rtol,atol=atol)
    assert sol.success, sol.message
    actual=sol.y[[0,2],-1]
    err=float(np.max(np.abs(actual-expected)/(1+np.abs(expected))))
    clock_err=abs(1/sol.y[4,-1]-no/ne)/(1+no/ne)
    ell_integral,ell_error=integ(lambda t:t*at(t)[4]**2,te,to)
    constraint_err=abs(lo-le-ell_integral)/(1+abs(lo-le))
    assert max(err,clock_err,constraint_err)<=2e-8, (err,clock_err,constraint_err)
    assert min(expected)>0
    assert abs(sum(at((te+to)/2)[-1]))<2e-12
    assert no/ne/((te/to)**0.25)>=1-1e-12
    if eps==0:
        bg=1.5*te**0.25*(math.sqrt(to)-math.sqrt(te))
        assert max(abs(expected-bg))<=2e-12
    return {'epsilon':eps,'te':te,'xe':xe,'sign':s,'length':d,'widths_quadrature':expected.tolist(),'widths_metric_Jacobi_ODE':actual.tolist(),'mixed_scaled_width_error':err,'clock_ratio':no/ne,'clock_ODE_error':clock_err,'null_constraint_error':constraint_err,'quad_error_estimates':[q[1] for q in ints],'lambda_quad_error_estimate':ell_error,'ode_nfev':sol.nfev,'rtol':rtol,'atol':atol}

try:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        for eps,te,xe,s,d in itertools.product((0,1/6,-1/6,1/2),(1,2),(0,0.7),(-1,1),(0.2,2)):
            records.append(finite(eps,te,xe,s,d))
        hardest=max(records,key=lambda r:r['mixed_scaled_width_error'])
        tight=finite(hardest['epsilon'],hardest['te'],hardest['xe'],hardest['sign'],hardest['length'],2e-12,2e-13)
        long=[]
        for to in (10,100,1000):
            eps=1/6; ne=0.75
            at=lambda t:point(t,t-1,eps,1)
            no,bo,lo,po,*_=at(to)
            ints=[integ(lambda t:at(t)[0]**2/at(t)[1][i]**2,1,to) for i in (0,1)]
            widths=bo/ne*np.array([v[0] for v in ints])
            A0=(1.5*(math.sqrt(to)-1))**2
            long.append({'to':to,'P_endpoint':po,'clock_over_background':math.exp(lo/4),'area_over_background':float(np.prod(widths)/A0),'width_ratio_y_z':float(widths[0]/widths[1]),'log_clock_contrast_over_t':lo/(4*to),'log_area_contrast_over_t':math.log(float(np.prod(widths)/A0))/to,'quad_error_estimates':[v[1] for v in ints]})
        late=[]
        for te,s in itertools.product((100,200,400,800),(-1,1)):
            eps=1/6; d=1; xe=0.7
            le=point(te,xe,eps,s)[2];lo=point(te+d,xe+s*d,eps,s)[2]
            asym=eps*eps*sigma*(d-math.sin(2*k*d)/(2*k)*math.cos(2*k*te+2*s*k*xe-2*phase+2*k*d))
            late.append({'te':te,'sign':s,'lambda_difference':lo-le,'formula_13_leading':asym,'error':lo-le-asym,'te_times_error':te*(lo-le-asym)})
        warning_log=[str(w.message) for w in caught]
    status='PASS'
except Exception as exc:
    status='FAIL';failure=repr(exc)
output={'status':status,'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'dtype':'float64','method':'Independent numerical Jacobi ODE versus quadrature; shared special-function library; not interval certification','sigma':sigma,'phase_delta':phase,'finite_cases':records,'hardest_case_tight_repeat':locals().get('tight'),'long_reception_illustrations':locals().get('long'),'fixed_path_asymptotic_diagnostics':locals().get('late'),'warnings':warning_log,'failure':locals().get('failure')}
print(json.dumps(output,indent=2,allow_nan=False))
sys.exit(0 if status=='PASS' else 1)

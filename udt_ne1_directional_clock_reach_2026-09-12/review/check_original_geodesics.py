#!/usr/bin/env python3
"""Frozen finite original-connection versus reduced-rapidity check; no imports from parent."""
import hashlib
import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.special import jv, yv

MUTATION = sys.argv[1] if len(sys.argv) > 1 else 'baseline'
assert MUTATION in {'baseline', 'suppress_lambda', 'invert_frequency'}
K = .75  # SOURCED: G394 supplied coordinate normalization.
A = -3*math.pi/4*yv(0,K)
B = 3*math.pi/4*jv(0,K)
LAM0 = 4*math.log(.75)


def metric_arrays(t, xi, eps):
    """Original diagonal g and first derivative arrays, derivative index first."""
    f=A*jv(0,K*t)+B*yv(0,K*t)
    ft=-K*(A*jv(1,K*t)+B*yv(1,K*t))
    cs,sn=math.cos(K*xi),math.sin(K*xi)
    p=eps*f*cs
    pt,px=eps*ft*cs,-eps*K*f*sn
    ell=t*t*(ft*ft+K*K*f*f)/2+t*f*ft/2-9/8
    lam=LAM0+eps*eps*(ell+t*f*ft*math.cos(2*K*xi)/2)
    lt=t*(pt*pt+px*px)
    lx=2*t*pt*px
    if MUTATION=='suppress_lambda':
        lam,lt,lx=LAM0,0.,0.
    a=lam/4-math.log(t)/4
    at,ax=lt/4-1/(4*t),lx/4
    g=np.array([-math.exp(2*a),math.exp(2*a),t*math.exp(p),t*math.exp(-p)])
    d=np.zeros((4,4,4))
    for i,val in enumerate([2*at*g[0],2*at*g[1],(1/t+pt)*g[2],(1/t-pt)*g[3]]):
        d[0,i,i]=val
    for i,val in enumerate([2*ax*g[0],2*ax*g[1],px*g[2],-px*g[3]]):
        d[1,i,i]=val
    return g,d,a


def connection_rhs(t, state, eps):
    # Seven components: three positions, all three coordinate slopes, log k^t.
    g,d,a=metric_arrays(t,state[0],eps)
    gamma=.5*(1/g)[:,None,None]*(d.transpose(1,0,2)+d.transpose(1,2,0)-d)
    u=np.r_[1.,state[3:6]]
    contraction=np.einsum('abc,b,c->a',gamma,u,u)
    return np.r_[state[3:6],-contraction[1:]+state[3:6]*contraction[0],-contraction[0]]


def reduced_coefficients(t, xi, eps, py, pz):
    # Independent scalar assembly of the admitted P and first-derivative constraints.
    ft0=(-3*math.pi/4*yv(0,.75))*jv(0,.75*t)+(3*math.pi/4*jv(0,.75))*yv(0,.75*t)
    ft1=-.75*((-3*math.pi/4*yv(0,.75))*jv(1,.75*t)+(3*math.pi/4*jv(0,.75))*yv(1,.75*t))
    p=eps*ft0*math.cos(.75*xi)
    dtp=eps*ft1*math.cos(.75*xi)
    dxp=-eps*.75*ft0*math.sin(.75*xi)
    q=py*py*math.exp(-p)+pz*pz*math.exp(p)
    eta=(pz*pz*math.exp(p)-py*py*math.exp(-p))/q
    return q,eta,dtp,dxp,t*(dtp*dtp+dxp*dxp),2*t*dtp*dxp


def reduced_rhs(t,state,eps,py,pz):
    xi,rapidity=state
    v=math.tanh(rapidity)
    q,eta,pt,px,lt,lx=reduced_coefficients(t,xi,eps,py,pz)
    return [v,-(lx+v*lt)/4+3*v/(4*t)-eta*(px+v*pt)/2]


CASES=[
    (0.,.2,[.8,.6,0.],20.),
    (.4,.2,[.8,.6,0.],80.),
    (-.4,.7,[-.8,0.,.6],80.),
    (.4,1.1,[.6,.48,.64],120.),
    (1.2,.3,[-.6,.48,-.64],30.),
    (.4,0.,[0.,1.,0.],80.),
    (.4,2*math.pi/3,[0.,1/math.sqrt(2),1/math.sqrt(2)],80.),
    (.4,.2,[math.sqrt(1-.01**2),.01,0.],80.),
]


def run_case(case, fine=False):
    eps,xi,sky,end=case
    c,py,pz=sky
    assert abs(c*c+py*py+pz*pz-1)<5e-15
    times=np.linspace(1,end,129)
    initial=[xi,0.,0.,c,.75*py,.75*pz,math.log(4/3)]
    original=solve_ivp(lambda t,y:connection_rhs(t,y,eps),(1.,end),initial,
        method='DOP853',rtol=2e-12 if fine else 2e-10,
        atol=2e-14 if fine else 2e-12,max_step=.1 if fine else .2,t_eval=times)
    reduced=solve_ivp(lambda t,y:reduced_rhs(t,y,eps,py,pz),(1.,end),[xi,math.atanh(c)],
        method='DOP853',rtol=2e-11,atol=2e-13,max_step=.1,t_eval=times)
    assert original.success and reduced.success, 'solver completion'
    max_frequency_error=max_null=max_momentum=max_control=0.
    final={}
    for j,t in enumerate(times):
        g,d,a=metric_arrays(t,original.y[0,j],eps)
        slopes=original.y[3:6,j]
        kt=math.exp(original.y[6,j])
        omega=math.exp(a)*kt
        if MUTATION=='invert_frequency': omega=1/omega
        q,_,_,_,_,_=reduced_coefficients(t,reduced.y[0,j],eps,py,pz)
        ref=math.sqrt(q)*math.cosh(reduced.y[1,j])/math.sqrt(t)
        max_frequency_error=max(max_frequency_error,abs(omega/ref-1))
        null=abs((g[0]+np.dot(g[1:],slopes*slopes))/(-g[0]))
        max_null=max(max_null,null)
        max_momentum=max(max_momentum,abs(g[2]*slopes[1]*kt-py),abs(g[3]*slopes[2]*kt-pz))
        omega0=math.sqrt(c*c*math.sqrt(t)+(py*py+pz*pz)/t)
        if eps==0:
            max_control=max(max_control,abs(omega/omega0-1))
        if c==0 and xi==0:
            source_p=eps*(A*jv(0,K*t)+B*yv(0,K*t))
            expected=math.sqrt((py*py*math.exp(-source_p)+pz*pz*math.exp(source_p))/t)
            max_control=max(max_control,abs(omega/expected-1),abs(original.y[0,j]-xi))
        if c==0 and xi==2*math.pi/3:
            max_control=max(max_control,abs(omega*math.sqrt(t)-1),abs(original.y[0,j]-xi))
        if j==len(times)-1:
            final={'omega':omega,'omega_reduced':ref,'R_over_R0':omega0/omega,
                'xi':float(original.y[0,j]),'v_xi':float(slopes[0]),
                'rapidity_reduced':float(reduced.y[1,j]),'E':omega*math.sqrt(t)}
    xerr=float(np.max(np.abs(original.y[0]-reduced.y[0])/(1+np.abs(reduced.y[0]))))
    result={'case':case,'fine':fine,'max_relative_frequency_error':max_frequency_error,
        'max_scaled_xi_error':xerr,'max_relative_original_null_residual':max_null,
        'max_absolute_killing_momentum_error':max_momentum,'max_analytic_control_error':max_control,
        'original_nfev':original.nfev,'reduced_nfev':reduced.nfev,'shape_original':list(original.y.shape),
        'shape_reduced':list(reduced.y.shape),'endpoint':final}
    print(json.dumps(result,sort_keys=True),flush=True)
    assert max_frequency_error<2e-7, 'original metric frequency vs reduced rapidity'
    assert xerr<2e-7, 'original metric trajectory vs reduced rapidity'
    assert max_null<2e-7, 'original metric null residual'
    assert max_momentum<2e-7, 'original metric Killing momenta'
    assert max_control<2e-7, 'analytic zero amplitude/equator controls'
    return result


started=time.monotonic()
print(json.dumps({'stage':'source-first numerical','mutation':MUTATION,'python':sys.version,
    'platform':platform.platform(),'numpy':np.__version__,'scipy':scipy.__version__,
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'dtype':'float64','grid_samples_per_case':129}),flush=True)
results=[run_case(case) for case in CASES]
worst=max(range(len(results)),key=lambda i:max(results[i]['max_relative_frequency_error'],results[i]['max_scaled_xi_error']))
repeat=run_case(CASES[worst],fine=True)
baseline_error=max(results[worst]['max_relative_frequency_error'],results[worst]['max_scaled_xi_error'])
fine_error=max(repeat['max_relative_frequency_error'],repeat['max_scaled_xi_error'])
assert fine_error<2e-8 and fine_error<baseline_error+2e-10, 'tighter repeat discrepancy'
print(json.dumps({'result':'PASS','cases':len(CASES),'worst_case_index':worst,
    'baseline_error':baseline_error,'fine_error':fine_error,'duration_seconds':time.monotonic()-started,
    'limits':'Finite numerical support only; no asymptotic or interval certification.'}),flush=True)

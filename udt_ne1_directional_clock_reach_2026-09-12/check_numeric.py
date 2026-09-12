#!/usr/bin/env python3
"""NCR1 finite float64 consistency/support; not an asymptotic certificate."""
import argparse
import itertools
import json
import math
import platform
import sys
import warnings

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.special import jv, yv

parser = argparse.ArgumentParser()
parser.add_argument('--mutate', choices=('drop_bxi', 'freeze_lambda', 'axial_background'))
parser.add_argument('--finite-only', action='store_true')
args = parser.parse_args()

# SUPPLIED G394 normalization, not selected physical constants.
k = 3 / 4
Ac = -3 * math.pi * yv(0, k) / 4
Bc = 3 * math.pi * jv(0, k) / 4
sigma = k * (Ac * Ac + Bc * Bc) / math.pi
MAX_STEP = math.pi / (8 * k)  # NUMERICAL control from CHECK_CONTRACT.
records, long_records, warnings_seen = [], [], []


def field(t, xi, eps):
    f = Ac * jv(0, k * t) + Bc * yv(0, k * t)
    fp = -k * (Ac * jv(1, k * t) + Bc * yv(1, k * t))
    co, si = math.cos(k * xi), math.sin(k * xi)
    P, Pt, Px = eps * f * co, eps * fp * co, -eps * k * f * si
    lt, lx = t * (Pt * Pt + Px * Px), 2 * t * Pt * Px
    at, ax = lt / 4 - 1 / (4 * t), lx / 4
    ell = eps * eps * (t * t * (fp * fp + k * k * f * f) / 2
                      + t * f * fp / 2 - 9 / 8
                      + t * f * fp * math.cos(2 * k * xi) / 2)
    return f, P, Pt, Px, at, ax, ell


def logcosh(eta):
    u = abs(eta)
    return u + math.log1p(math.exp(-2 * u)) - math.log(2)


def solve(eps, mu, psi, xe, to, rtol=2e-10, atol=2e-12, step=MAX_STEP):
    rho2 = 1 - mu * mu
    assert rho2 > 0, 'numerical rapidity chart excludes exact axis'
    py2, pz2 = rho2 * math.cos(psi)**2, rho2 * math.sin(psi)**2

    def rhs(t, state):
        xi, eta, _ = state
        _, P, Pt, Px, at, ax, _ = field(t, xi, eps)
        ey, ez = py2 * math.exp(-P), pz2 * math.exp(P)
        r = (ez - ey) / (ez + ey)
        v = math.tanh(eta)
        bt, bx = at - 1 / (2 * t) + r * Pt / 2, ax + r * Px / 2
        if args.mutate == 'drop_bxi':
            bx = 0.0  # Deliberate incorrect equation; original clock check unchanged.
        elif args.mutate == 'freeze_lambda':
            bt, bx = -3 / (4 * t) + r * Pt / 2, r * Px / 2
        logw_prime = -at * v * v - ax * v + (1-v*v) * (-1/(2*t)+r*Pt/2)
        return (v, -bx-v*bt, logw_prime)

    sol = solve_ivp(rhs, (1.0, to), (xe, math.atanh(mu), 0.0),
                    method='DOP853', rtol=rtol, atol=atol,
                    max_step=step, dense_output=True)
    assert sol.success, sol.message
    assert np.isfinite(sol.y).all(), 'nonfinite solver state'
    return sol, (py2, pz2), (rtol, atol, step)


def inspect(eps, mu, psi, xe, t, state, momenta):
    xi, eta, logw = map(float, state)
    py2, pz2 = momenta
    f, P, _, _, _, _, _ = field(t, xi, eps)
    M = py2 * math.exp(-P) + pz2 * math.exp(P)
    reconstructed = (math.log(M)-math.log(t))/2 + logcosh(eta)
    discrepancy = abs(logw-reconstructed)
    assert discrepancy <= 2e-7, ('clock_transport', discrepancy, eps, mu, xe, t)
    logw0 = 0.5 * math.log(mu*mu*math.sqrt(t)+(1-mu*mu)/t)
    if args.mutate == 'axial_background':
        logw0 = math.log(t)/4
    logC = logw0-logw
    if eps == 0:
        assert abs(logC) <= 2e-7, ('zero_amplitude_recovery', logC, mu, t)
    if mu == 0 and xe == 0:
        expected = -math.log(M)/2
        assert max(abs(xi),abs(eta),abs(logC-expected)) <= 2e-7, 'invariant_equator'
    bound = abs(eps*f)/2+0.5*math.log1p(t**1.5*mu*mu/(1-mu*mu))
    assert logC <= bound+2e-7, ('finite_momentum_bound', logC, bound)
    return {'epsilon':eps,'mu':mu,'psi':psi,'source_xi':xe,'reception_t':t,
            'xi':xi,'eta':eta,'log_frequency_integrated':logw,
            'log_frequency_reconstructed':reconstructed,
            'clock_transport_log_error':discrepancy,
            'clock_ratio':math.exp(-logw),'background_clock_ratio':math.exp(-logw0),
            'clock_contrast':math.exp(logC),'log_contrast':logC,
            'log_momentum_upper_bound':bound,
            'log_contrast_over_t':logC/t,
            'log_contrast_over_log_t':logC/math.log(t)}


def finite_case(eps, mu, psi, xe, to, tight=False):
    controls = (2e-11,2e-13,MAX_STEP/2) if tight else (2e-10,2e-12,MAX_STEP)
    sol,mom,settings = solve(eps,mu,psi,xe,to,*controls)
    result=inspect(eps,mu,psi,xe,to,sol.y[:,-1],mom)
    result.update({'nfev':sol.nfev,'rtol':settings[0],'atol':settings[1],'max_step':settings[2]})
    return result


def convergence(old, new):
    err=max(abs(old[key]-new[key])/(1+abs(new[key]))
            for key in ('xi','log_frequency_integrated'))
    assert err <= 2e-6, ('tight_repeat_convergence',err)
    return err


try:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        for values in itertools.product((0,1/6,-1/6,1/2),(-0.8,0,0.8),
                                        (0,math.pi/4,math.pi/2),(0,0.7),(2,8)):
            records.append(finite_case(*values))
        worst=max(records,key=lambda r:r['clock_transport_log_error'])
        tight=finite_case(*(worst[k] for k in ('epsilon','mu','psi','source_xi','reception_t')),tight=True)
        finite_repeat_error=convergence(worst,tight)
        if not args.finite_only:
            for eps,sign,angle in itertools.product((1/6,1/2),(-1,1),(0.4,0.04,0.0004)):
                mu=sign*math.cos(angle); psi=math.pi/4; xe=0.7
                sol,mom,settings=solve(eps,mu,psi,xe,1600)
                samples=[]
                for t in (10,40,100,400,1600):
                    row=inspect(eps,mu,psi,xe,t,sol.sol(t),mom)
                    row['log_axial_contrast_control']=field(t,xe+sign*(t-1),eps)[-1]/4
                    samples.append(row)
                item={'epsilon':eps,'sign':sign,'tilt_radians':angle,'psi':psi,
                      'nfev':sol.nfev,'rtol':settings[0],'atol':settings[1],
                      'max_step':settings[2],'samples':samples}
                long_records.append(item)
            selected=next(r for r in long_records if r['epsilon']==0.5 and r['sign']==-1 and r['tilt_radians']==0.04)
            tsol,tmom,tsettings=solve(0.5,-math.cos(0.04),math.pi/4,0.7,1600,
                                     2e-11,2e-13,MAX_STEP/2)
            long_tight=[inspect(0.5,-math.cos(0.04),math.pi/4,0.7,t,tsol.sol(t),tmom)
                        for t in (10,40,100,400,1600)]
            long_repeat_error=max(convergence(a,b) for a,b in zip(selected['samples'],long_tight))
        warnings_seen=[str(w.message) for w in caught]
    status='PASS'
except Exception as exc:
    status='FAIL'; failure=repr(exc)

result={'status':status,'mutation':args.mutate,'finite_only':args.finite_only,
        'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
        'dtype':'float64','sigma':sigma,'frozen_contract':'CHECK_CONTRACT.md',
        'epistemic_scope':'Finite consistency/support; shared field/Bessel code. No interval or asymptotic certificate.',
        'finite_cases':records,'worst_finite_tight_repeat':locals().get('tight'),
        'finite_repeat_scaled_error':locals().get('finite_repeat_error'),
        'long_reception_illustrations':long_records,'long_tight_repeat':locals().get('long_tight'),
        'long_repeat_scaled_error':locals().get('long_repeat_error'),
        'warnings':warnings_seen,'failure':locals().get('failure')}
print(json.dumps(result,indent=2,allow_nan=False))
sys.exit(0 if status=='PASS' else 1)

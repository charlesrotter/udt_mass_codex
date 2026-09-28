"""Scoped exact geometry and independent numerical signal readouts; no fitted physics.

All numeric metrics/observer data below are FREE controls in c_E=1 units.
They do not select a physical UDT geometry or distance scale.
"""
import json
import math
import platform
from pathlib import Path

import scipy
import sympy as sp
from scipy.integrate import quad, solve_ivp

ROOT = Path(__file__).resolve().parent
exact = []


def zero(name, expr):
    residual = sp.simplify(expr)
    if residual != 0:
        raise AssertionError((name, residual))
    exact.append({"name": name, "residual": str(residual)})


t, x, w = sp.symbols('t x w', real=True)
N, A = sp.Function('N')(t, x), sp.Function('A')(t, x)
coords = [t, x]
g = sp.diag(-N**2, A**2)
gi = g.inv()
Gamma = [[[sp.simplify(sum(gi[i, m] * (
    sp.diff(g[m, k], coords[j]) + sp.diff(g[m, j], coords[k])
    - sp.diff(g[j, k], coords[m])) / 2 for m in range(2)))
    for k in range(2)] for j in range(2)] for i in range(2)]

for eps in [-1, 1]:
    k = [w/N, eps*w/A]
    kt_dot = -sum(Gamma[0][i][j]*k[i]*k[j]
                  for i in range(2) for j in range(2))
    # omega=N k^t for the static-coordinate unit observer, from -g(U,k).
    omega_dot = sum(sp.diff(N, coords[i])*k[i]*k[0] for i in range(2)) + N*kt_dot
    expected = -w**2 * (sp.diff(A,t)/(A*N) + eps*sp.diff(N,x)/(A*N))
    zero(f'geodesic_energy_direction_{eps}', omega_dot-expected)
    p = A/N
    integrand_one = eps*sp.diff(sp.log(N),x) + p*sp.diff(sp.log(N),t) + sp.diff(p,t)
    integrand_two = eps*sp.diff(sp.log(N),x) + p*sp.diff(sp.log(A),t)
    zero(f'endpoint_plus_slowness_direction_{eps}', integrand_one-integrand_two)

eA,eB=sp.symbols('eA eB', real=True)
for eps in [-1,1]:
    factor = ((1-eps*sp.tanh(eA))/(1-eps*sp.tanh(eB))
              *sp.cosh(eA)/sp.cosh(eB))
    zero(f'moving_endpoint_rapidity_{eps}', sp.expand_trig(factor).rewrite(sp.exp)-sp.exp(eps*(eB-eA)))

a0,b,L,c,tau = sp.symbols('a0 b L c tau', positive=True)
F=((a0+b*tau)*sp.exp(b*L/c)-a0)/b
zero('affine_incidence', c/b*sp.log((a0+b*F)/(a0+b*tau))-L)
zero('affine_clock_slope', sp.diff(F,tau)-sp.exp(b*L/c))
zero('affine_echo_slope', sp.diff(F.subs(tau,F),tau)-sp.exp(2*b*L/c))
zero('affine_zero_parameter_timing', sp.limit(F,b,0)-tau-a0*L/c)
zero('affine_reciprocal_time_change', (1/(a0+b*tau)**2)*(a0+b*tau)**2-1)
j = sp.symbols('j', positive=True)
flat_arrival=sp.log(sp.exp(j*t)+j*L/c)/j
zero('lapse_only_clock_ratio', sp.exp(j*(flat_arrival-t))*sp.diff(flat_arrival,t)-1)

# Numeric definitions below are separate from the symbolic expressions above.
# Four declared positive metrics, both distinct future directions. Coordinates dimensionless.
cases = [
    ('flat_motion',0.,0.,0.,0.,.05,-.03),
    ('static',.08,0.,.02,0.,0.,0.),
    ('lapse_only',0.,.04,0.,0.,0.,0.),
    ('mixed',.03,.02,.01,.07,.02,-.03),
]
records=[]
mutations={'omit_endpoint_clock_normalization':[], 'omit_time_live_integral':[],
           'reverse_endpoint_motion':[]}

for name,gx,nt,ax,at,v_left,v_right in cases:
    for eps in [-1,1]:
        xa,xb=(0.,1.) if eps==1 else (1.,0.)
        va,vb=(v_left,v_right) if eps==1 else (v_right,v_left)

        def scales(tt,xx):
            return math.exp(gx*xx+nt*tt),math.exp(ax*xx+at*tt)

        def proper_rate(tt,x0,v):
            nn,aa=scales(tt,x0+v*tt)
            beta=aa*v/nn
            if abs(beta)>=1:
                raise AssertionError('non-timelike test observer')
            return nn*math.sqrt(1-beta*beta)

        def arrival(te):
            # Null path ODE in coordinate time, no affine momenta/frequency evolution.
            def rhs(tt,y):
                nn,aa=scales(tt,y[0]); return [eps*nn/aa]
            def hit(tt,y): return y[0]-(xb+vb*tt)
            hit.terminal=True;hit.direction=eps
            sol=solve_ivp(rhs,(te,te+5.),[xa+va*te],events=hit,
                          rtol=2e-12,atol=2e-14,method='DOP853',max_step=.05)
            if not sol.success or len(sol.t_events[0])!=1:
                raise AssertionError(('missing regular arrival',name,eps))
            return float(sol.t_events[0][0])

        te=.2
        tr=arrival(te)
        na,aa=scales(te,xa+va*te);nb,ab=scales(tr,xb+vb*tr)
        ba,bb=aa*va/na,ab*vb/nb
        lapse=math.log(nb/na)
        motion=eps*(math.atanh(bb)-math.atanh(ba))
        # In this exponential family partial_t p * |dx/dt| = at-nt.
        integral=(at-nt)*(tr-te)
        prediction=math.exp(lapse+motion+integral)

        # Independent affine Hamiltonian null geodesic, with covector readout.
        def ham_rhs(lam,y):
            tt,xx,pt,px=y;nn,aa=scales(tt,xx)
            return [-pt/nn**2,px/aa**2,
                    -nt*pt**2/nn**2+at*px**2/aa**2,
                    -gx*pt**2/nn**2+ax*px**2/aa**2]
        def hit_ham(lam,y): return y[1]-(xb+vb*y[0])
        hit_ham.terminal=True;hit_ham.direction=eps
        initial=[te,xa+va*te,-na,eps*aa]
        sol=solve_ivp(ham_rhs,(0.,6.),initial,events=hit_ham,
                      rtol=2e-12,atol=2e-14,method='DOP853',max_step=.05)
        if not sol.success or len(sol.t_events[0])!=1:
            raise AssertionError(('missing Hamiltonian arrival',name,eps))
        th,xh,pth,pxh=sol.y_events[0][0]
        emitted=-(initial[2]+va*initial[3])/proper_rate(te,xa,va)
        received=-(pth+vb*pxh)/proper_rate(th,xb,vb)
        energy_ratio=emitted/received
        null_residual=max(abs(-pt**2/scales(tt,xx)[0]**2
                              +px**2/scales(tt,xx)[1]**2)
                          for tt,xx,pt,px in sol.y.T)
        # Finite emitted/received pulse intervals converge to the differential ratio.
        pulse=[]
        for step in [.01,.003,.001]:
            tm,tp=arrival(te-step),arrival(te+step)
            de=quad(lambda tt:proper_rate(tt,xa,va),te-step,te+step,
                    epsabs=1e-13,epsrel=1e-13)[0]
            dr=quad(lambda tt:proper_rate(tt,xb,vb),tm,tp,
                    epsabs=1e-13,epsrel=1e-13)[0]
            pulse.append({'half_interval':step,'ratio':dr/de,'error':abs(dr/de-prediction)})
        assert abs(th-tr)<1e-9
        assert abs(energy_ratio-prediction)<1e-9
        assert null_residual<1e-9
        assert pulse[-1]['error']<2e-8
        if pulse[0]['error']>1e-10:
            assert pulse[-1]['error']<.1*pulse[0]['error']
        records.append({'case':name,'direction':eps,'parameters':[gx,nt,ax,at,va,vb],
                        'emission_time':te,'arrival_time':tr,'formula_ratio':prediction,
                        'hamiltonian_ratio':energy_ratio,'hamiltonian_arrival_difference':abs(th-tr),
                        'max_null_residual':null_residual,'pulse_intervals':pulse})
        tests={
            'omit_endpoint_clock_normalization':math.exp(motion+integral),
            'omit_time_live_integral':math.exp(lapse+motion),
            'reverse_endpoint_motion':math.exp(lapse-motion+integral),
        }
        for label,bad in tests.items():
            if abs(bad-energy_ratio)>1e-5:
                mutations[label].append({'case':name,'direction':eps,'error':abs(bad-energy_ratio)})

assert all(mutations.values()),mutations
out={'scope':'Conditional geometry checks, not physical UDT selection or observational evidence',
     'versions':{'python':platform.python_version(),'sympy':sp.__version__,'scipy':scipy.__version__},
     'exact_checks':exact,'numeric_controls':records,'wrong_formula_rejections':mutations,
     'numeric_method':'DOP853; rtol=2e-12, atol=2e-14, max_step=.05; quad atol/rtol=1e-13',
     'thresholds':{'ratio_and_event_and_null':1e-9,'final_pulse_ratio':2e-8},
     'classification':'Exact symbolic identities plus floating-point cross-checks; not numerical certification'}
(ROOT/'CHECK_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'exact_checks':len(exact),'numeric_controls':len(records),
                  'wrong_formula_types_rejected':len(mutations),
                  'max_formula_hamiltonian_error':max(abs(r['formula_ratio']-r['hamiltonian_ratio']) for r in records),
                  'max_final_pulse_error':max(r['pulse_intervals'][-1]['error'] for r in records)}))

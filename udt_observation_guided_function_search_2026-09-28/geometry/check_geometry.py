#!/usr/bin/env python3
"""Original-equation checks for the declared geometry tiles; no data fits.

Numeric tools are methods. Metrics, controls, domains and rates are FREE / supplied.
No physical evolution equation, source, action or observational transfer is used.
"""
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import sympy as sp


def zero(expr):
    return sp.simplify(sp.trigsimp(expr)) == 0


def tensor_geometry(diagonal, coords):
    """Levi-Civita coefficients and Riemann, computed from metric derivatives."""
    n = len(coords)
    gamma = {}
    for i in range(n):
        for j in range(n):
            for k in range(n):
                v = ((sp.diff(diagonal[i], coords[j]) if i == k else 0)
                     + (sp.diff(diagonal[i], coords[k]) if i == j else 0)
                     - (sp.diff(diagonal[j], coords[i]) if j == k else 0)) / (2 * diagonal[i])
                v = sp.simplify(v)
                if v != 0:
                    gamma[i, j, k] = v

    def G(i, j, k):
        return gamma.get((i, j, k), sp.S.Zero)

    riemann = {}
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    v = (sp.diff(G(i, l, j), coords[k])
                         - sp.diff(G(i, k, j), coords[l])
                         + sum(G(i, k, m)*G(m, l, j) - G(i, l, m)*G(m, k, j)
                               for m in range(n)))
                    v = sp.simplify(sp.trigsimp(v))
                    if v != 0:
                        riemann[i, j, k, l] = v
    ricci = sp.Matrix(n, n, lambda j, l: sp.simplify(sum(
        riemann.get((i, j, i, l), 0) for i in range(n))))
    scalar = sp.simplify(sum(ricci[i, i]/diagonal[i] for i in range(n)))
    return gamma, riemann, ricci, scalar


def symbolic_checks():
    checks = {}
    T, R, th, ph, K = sp.symbols('T R theta phi K', real=True)
    f = 1-K*R**2
    diag = [-f, 1/f, R**2, R**2*sp.sin(th)**2]
    gam, riem, ric, scal = tensor_geometry(diag, [T, R, th, ph])
    checks['static_ricci_scalar'] = zero(scal-12*K)
    checks['static_constant_sectional_curvature'] = all(zero(
        riem.get((a,b,c,d), 0)-K*((1 if a == c else 0)*(diag[b] if b == d else 0)
                                      -(1 if a == d else 0)*(diag[b] if b == c else 0)))
        for a in range(4) for b in range(4) for c in range(4) for d in range(4))
    kretsch = sp.simplify(sum(diag[a]*v*v/(diag[b]*diag[c]*diag[d])
                             for (a,b,c,d), v in riem.items()))
    checks['static_kretschmann'] = zero(kretsch-24*K*K)
    # Affine radial tangent is independently inserted in the metric geodesic equation.
    E = sp.symbols('E', positive=True)
    radial_results = []
    for direction in [-1, 1]:
        tangent = [E/f, direction*E, 0, 0]
        residual = []
        for i in range(4):
            dv = direction*E*sp.diff(tangent[i], R)
            dv += sum(gam.get((i,j,k),0)*tangent[j]*tangent[k]
                      for j in range(4) for k in range(4))
            residual.append(sp.simplify(dv))
        radial_results.append(all(zero(v) for v in residual))
    checks['static_original_geodesic_both_directions'] = all(radial_results)
    checks['static_null_tangent'] = zero(-f*(E/f)**2+E**2/f)
    checks['static_null_ricci'] = zero(ric[0,0]*(E/f)**2+ric[1,1]*E**2)
    # x=L sqrt(K) and y=rho sqrt(K) identities avoid branch-ambiguous simplification.
    x, y, h = sp.symbols('x y h', positive=True)
    checks['radar_distance_original_derivative'] = zero(sp.diff(sp.atanh(h*R)/h,R)-1/(1-h*h*R*R))
    checks['proper_distance_original_derivative'] = zero(sp.diff(sp.asin(h*R)/h,R)**2-1/(1-h*h*R*R))
    checks['radar_redshift_squared'] = zero(1/(1-sp.tanh(x)**2)-sp.cosh(x)**2)
    checks['proper_redshift_squared'] = zero(1/(1-sp.sin(y)**2)-1/sp.cos(y)**2)
    checks['kernel_redshift_algebra'] = zero(((1/(1-K*R*R))-1)/((1/(1-K*R*R))+1)-K*R*R/(2-K*R*R))
    # Generic homogeneous 4-metric: curvature is computed from derivatives, no field equation.
    X, Y, Z = sp.symbols('X Y Z', real=True)
    a = sp.Function('a')(T)
    hg, hr, hric, hscal = tensor_geometry([-1,a*a,a*a,a*a], [T,X,Y,Z])
    H = sp.diff(a,T)/a
    nullric = sp.simplify(hric[0,0]+hric[1,1]/a**2)
    checks['homogeneous_null_tide_from_curvature'] = zero(nullric/2+sp.diff(H,T))
    checks['homogeneous_scalar_from_curvature'] = zero(hscal-6*(sp.diff(H,T)+2*H*H))
    # Inverse construction uses an arbitrary smooth F, no coefficients.
    F = sp.Function('F')(x)
    Fp = sp.diff(F,x)
    Hi = h*sp.exp(x)/Fp
    ai = sp.exp(-x)
    d = ai*F/h
    dT = lambda expr: -Hi*sp.diff(expr,x)
    ds = lambda expr: Hi*sp.diff(expr,x)
    dl = lambda expr: sp.exp(x)*Hi*sp.diff(expr,x)
    checks['inverse_scale_rate'] = zero(dT(ai)/ai-Hi)
    checks['inverse_deceleration'] = zero(-ai*dT(dT(ai))/dT(ai)**2 + sp.diff(F,x,2)/Fp)
    checks['inverse_affine_jacobi_original'] = zero(dl(dl(d))+(-dT(Hi))*sp.exp(2*x)*d)
    checks['inverse_reparameterized_jacobi'] = zero(ds(ds(d))+Hi*ds(d)+(-dT(Hi))*d)
    checks['inverse_AP_ratio'] = zero((F/h)*Hi-sp.exp(x)*F/Fp)
    C = sp.symbols('C', positive=True)
    checks['AP_amplitude_cancellation'] = zero(sp.exp(x)*(C*F)/sp.diff(C*F,x)-sp.exp(x)*F/Fp)
    kappa = sp.symbols('kappa', real=True)
    Hcurved = Hi*sp.sqrt(1-kappa*F**2)
    qc = -1+sp.diff(Hcurved,x)/Hcurved
    checks['curved_inverse_deceleration'] = zero(qc + sp.diff(F,x,2)/Fp + kappa*F*Fp/(1-kappa*F**2))
    # Local Jacobi coefficients are derived from original equation, not asserted alone.
    s = sp.symbols('s', real=True)
    q0,q1,F0,c2,c3 = sp.symbols('q0 q1 F0 c2 c3')
    poly=s+c2*s*s+c3*s**3
    residual=sp.expand(sp.diff(poly,s,2)+(q0+q1*s)*sp.diff(poly,s)+F0*poly)
    solved=sp.solve([residual.coeff(s,0),residual.coeff(s,1)], [c2,c3])
    checks['local_area_series'] = zero(solved[c2]+q0/2) and zero(solved[c3]-(q0*q0-q1-F0)/6)
    # Static K>0 central-past s is radial proper distance; null tide is zero.
    dstatic=sp.sin(h*s)/h
    qstatic=h*sp.tan(h*s)
    checks['static_clock_area_differential'] = zero(sp.diff(dstatic,s,2)+qstatic*sp.diff(dstatic,s))
    # An explicit rejection control: inward/outward stationary redshifts multiply to one.
    checks['static_future_clock_product_one'] = zero((1/sp.sqrt(f))*sp.sqrt(f)-1)
    return {'checks':checks, 'count':len(checks), 'failed':[k for k,v in checks.items() if not v],
            'static_ricci_scalar':str(scal), 'static_kretschmann':str(kretsch),
            'homogeneous_null_tide':str(sp.simplify(nullric/2)),
            'local_series_coefficients':{str(k):str(v) for k,v in solved.items()}}


# FREE algebraic control, not fit: F=x+x^2/4, h0=1 on 0<=x<=2.
def shape(x):
    return x+x*x/4.0


def proper_time(x):
    return (1.5+0.5*x)*np.exp(-x)-1.5


def affine_time(x):
    return 0.625-(0.625+0.25*x)*np.exp(-2*x)


def metric_at_time(t):
    # Independent root inversion of the saved proper-time construction.
    x=brentq(lambda q: float(proper_time(q))-t, -0.2, 2.5,
             xtol=1e-14, rtol=4*np.finfo(float).eps)
    a=math.exp(-x)
    H=math.exp(x)/(1+x/2)
    Hx=H*(1-1/(2+x))
    Hdot=-H*Hx
    return a,H,Hdot


def geodesic_rhs(lam, state):
    t,chi,kt,kchi,J,V=state
    a,H,Hdot=metric_at_time(t)
    # Christoffels Gamma^T_chichi=a^2 H, Gamma^chi_Tchi=H.
    # Full radial-screen Riemann contraction, before imposing nullness.
    tide=-(Hdot+H*H)*kt*kt+H*H*a*a*kchi*kchi
    return [kt,kchi,-a*a*H*kchi*kchi,-2*H*kt*kchi,V,-tide*J]


def numerical_checks():
    xs=np.linspace(0,2,41)
    lambdas=affine_time(xs)
    original_ode=[]
    for tol in [1e-8,1e-10,1e-12]:
        sol=solve_ivp(geodesic_rhs,(0,float(lambdas[-1])),[0,0,-1,1,0,1],
                      rtol=tol,atol=tol*0.02,method='DOP853',dense_output=True)
        if not sol.success:
            raise RuntimeError(sol.message)
        actual=sol.sol(lambdas)
        expected=np.array([proper_time(xs),shape(xs),-np.exp(xs),np.exp(2*xs),
                           np.exp(-xs)*shape(xs),np.exp(xs)*(1-shape(xs)/(1+xs/2))])
        err=np.max(np.abs(actual-expected)/(1+np.abs(expected)),axis=1)
        null=[]; momentum=[]
        for j in range(len(xs)):
            a,H,Hdot=metric_at_time(actual[0,j])
            null.append(abs(-actual[2,j]**2+a*a*actual[3,j]**2)/(1+actual[2,j]**2))
            momentum.append(abs(a*a*actual[3,j]-1))
        original_ode.append({'rtol':tol,'atol':tol*.02,'nfev':sol.nfev,
            'state_scaled_max_errors':dict(zip(['T','chi','kT','kchi','J','Jdot'],map(float,err))),
            'original_null_constraint_max':max(null),'conserved_spatial_momentum_max':max(momentum)})
    # Integrate null incidence separately in coordinate distance and finite-difference pulses.
    pulses=[]
    for xe in [0.2,0.7,1.5]:
        te=float(proper_time(xe)); distance=shape(xe)
        def arrival(tstart):
            sol=solve_ivp(lambda y,t:[metric_at_time(float(t[0]))[0]],(0,distance),[tstart],
                          rtol=2e-12,atol=2e-14,method='DOP853')
            if not sol.success:raise RuntimeError(sol.message)
            return float(sol.y[0,-1])
        for eps in [1e-3,1e-4,1e-5]:
            ratio=(arrival(te+eps)-arrival(te-eps))/(2*eps)
            pulses.append({'x_e':xe,'epsilon':eps,'arrival_nominal':arrival(te),
                           'pulse_slope':ratio,'geodesic_expected':math.exp(xe),
                           'absolute_error':abs(ratio-math.exp(xe))})
    # Exact-control pulse maps in dimensionless units, free b=H=1.
    future=[]
    for chi in [.02,.2,.4]:
        # Coasting a=T, emit T=1. Both future legs exist.
        tA=1.; tB=tA*math.exp(chi); tC=tB*math.exp(chi)
        future.append({'control':'affine_scale','chi':chi,'T_A':tA,'T_B':tB,'T_C':tC,
                       'r_out':math.exp(chi),'r_return':math.exp(chi),'r_echo':math.exp(2*chi)})
        # Exponential a=e^T, emit T=0, return only 2chi<1.
        tB=-math.log1p(-chi); tC=-math.log1p(-2*chi)
        future.append({'control':'exponential_scale','chi':chi,'T_A':0,'T_B':tB,'T_C':tC,
                       'r_out':1/(1-chi),'r_return':(1-chi)/(1-2*chi),'r_echo':1/(1-2*chi)})
    boosts=[]
    for r in [0.3,1.,2.,10.]:
        for De,Do in [(0.2,3.),(2.,.3),(1.,1.)]:
            do=.7; de=r*do
            ratio=(De*de)/(Do*do); rp=(De/Do)*r
            boosts.append(abs(ratio-rp)/(1+abs(rp)))
    good=(max(original_ode[-1]['state_scaled_max_errors'].values())<2e-10
          and original_ode[-1]['original_null_constraint_max']<2e-10
          and original_ode[-1]['conserved_spatial_momentum_max']<2e-10
          and max(p['absolute_error'] for p in pulses if p['epsilon']==1e-5)<1e-7
          and max(boosts)<1e-14)
    return {'passed':good,'geodesic_jacobi_resolution':original_ode,'separate_pulse_incidence':pulses,
            'actual_future_return_controls':future,'endpoint_boost_area_covariance_max':max(boosts),
            'no_independence_claim':'Author context; metric construction shared, original geodesic/Jacobi and pulse-incidence algorithms distinct. Fresh review is separate.'}


def main():
    symbolic=symbolic_checks()
    numerical=numerical_checks()
    result={'python':sys.version,'platform':platform.platform(),'sympy':sp.__version__,
            'numpy':np.__version__,'scipy':scipy.__version__,
            'symbolic':symbolic,'numerical':numerical,
            'passed':not symbolic['failed'] and numerical['passed']}
    print(json.dumps(result,indent=2,allow_nan=False))
    if not result['passed']:sys.exit(1)


if __name__=='__main__':
    main()

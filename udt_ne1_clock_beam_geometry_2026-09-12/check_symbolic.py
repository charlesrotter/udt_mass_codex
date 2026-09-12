#!/usr/bin/env python3
"""Original-metric checks. No import from new candidate or reviewer code."""
import functools
import json
import platform
import sys
import sympy as S

mutation = sys.argv[1] if len(sys.argv) > 1 else 'baseline'
checks = []
def zero(name, expression):
    defect = S.simplify(S.expand(expression))
    checks.append({'name': name, 'pass': defect == 0, 'defect': str(defect)})
    if defect != 0:
        raise AssertionError(name)

try:
    t, x, y, z = coords = S.symbols('t x y z', positive=True)
    C, be, Ne, No = S.symbols('C be Ne No', positive=True)
    a, b, c = [S.Function(n)(t, x) for n in ('a', 'b', 'c')]
    g = S.diag(-S.exp(2*a), S.exp(2*a), S.exp(2*b), S.exp(2*c))
    gi = g.inv()
    @functools.lru_cache(None)
    def G(i,j,k):
        return S.simplify(sum(gi[i,l]*(S.diff(g[l,k],coords[j])+S.diff(g[l,j],coords[k])-S.diff(g[j,k],coords[l]))/2 for l in range(4)))
    @functools.lru_cache(None)
    def R(i,j,k,l):
        return S.diff(G(i,l,j),coords[k])-S.diff(G(i,k,j),coords[l])+sum(G(i,k,m)*G(m,l,j)-G(i,l,m)*G(m,k,j) for m in range(4))
    for sign in (-1,1):
        ds = lambda f: S.diff(f,t)+sign*S.diff(f,x)
        a_ray = -S.log(t)/4 if mutation == 'drop_lapse_response' else a
        K = [C*S.exp(-2*a_ray), sign*C*S.exp(-2*a_ray),0,0]
        zero(f'null_{sign}', sum(g[i,i]*K[i]**2 for i in range(4)))
        for i in range(4):
            zero(f'affine_geodesic_{sign}_{i}',sum(K[j]*S.diff(K[i],coords[j]) for j in range(4))+sum(G(i,j,k)*K[j]*K[k] for j in range(4) for k in range(4)))
        tides = []
        for axis,q in ((2,b),(3,c)):
            E = [S.exp(-q) if i==axis else 0 for i in range(4)]
            for i in range(4):
                zero(f'parallel_screen_{sign}_{axis}_{i}',sum(K[j]*S.diff(E[i],coords[j]) for j in range(4))+sum(G(i,j,k)*K[j]*E[k] for j in range(4) for k in range(4)))
            tide = sum(R(axis,j,axis,l)*K[j]*K[l] for j in range(4) for l in range(4))
            expected = -C**2*S.exp(-4*a)*(ds(ds(q))+ds(q)**2-2*ds(a)*ds(q))
            zero(f'original_tide_{sign}_{axis}',tide-expected)
            tides.append(tide)
        zero(f'mixed_tide_{sign}',sum(R(2,j,3,l)*K[j]*K[l] for j in range(4) for l in range(4)))
    # Independently differentiate the quadrature solution along one ray.
    ar, qr, ir = [S.Function(n)(t) for n in ('ar','qr','ir')]
    J = (1 if mutation=='drop_source_width' else be)*S.exp(qr)*ir/C
    dv = lambda f:C*S.exp(-2*ar)*S.diff(f,t)
    tide = -C**2*S.exp(-4*ar)*(S.diff(qr,t,2)+S.diff(qr,t)**2-2*S.diff(ar,t)*S.diff(qr,t))
    ip=S.exp(2*ar-2*qr)
    zero('quadrature_original_Jacobi', (dv(dv(J))+tide*J).subs({S.diff(ir,t,2):S.diff(ip,t),S.diff(ir,t):ip}))
    slope=dv(J).subs({S.diff(ir,t):ip,ir:0}).subs(qr,S.log(be))
    zero('vertex_unit_affine_slope',slope-1)
    p1, p2, ell1=S.symbols('p1 p2 ell1',real=True)
    ap=(ell1-1/t)/4
    brackets=sum((-1/t**2+sgn*p2)/2+((1/t+sgn*p1)/2)**2-2*ap*(1/t+sgn*p1)/2 for sgn in (-1,1))
    zero('original_tide_trace_on_NE1',brackets.subs(ell1,t*p1**2))
    clock=Ne/No if mutation=='invert_clock' else No/Ne
    zero('clock_frequency_and_correspondence',clock-(C/Ne)/(C/No))
    Dy,Dz=S.symbols('Dy Dz',positive=True)
    zero('affine_invariant_area',(C/Ne)**2*(Ne/C)**2*Dy*Dz-Dy*Dz)
    te,to=S.symbols('te to',positive=True)
    I0=S.Rational(9,8)*(te**S.Rational(-1,2)-to**S.Rational(-1,2))
    zero('background_integrand',S.diff(I0,to)-S.Rational(9,16)*to**S.Rational(-3,2))
    zero('background_endpoint_map',S.sqrt(te*to)*I0/(S.Rational(3,4)*te**S.Rational(-1,4))-S.Rational(3,2)*te**S.Rational(1,4)*(S.sqrt(to)-S.sqrt(te)))
    verdict='PASS'
except AssertionError as exc:
    verdict='FAIL'; failure=str(exc)
print(json.dumps({'status':verdict,'mutation':mutation,'python':platform.python_version(),'sympy':S.__version__,'checks':checks,'failure':locals().get('failure'),'limits':'Exact symbolic predicates; structural zeros and bookkeeping are not independent proofs'},indent=2))
sys.exit(0 if verdict=='PASS' else 1)

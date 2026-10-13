"""Independent FAC1 world-function computation; no author imports."""
import hashlib
import json
import platform
from pathlib import Path
import sympy as sp

z, b, s, e, h, D, T = sp.symbols('z b s e h D T')
R = sp.Rational

def trunc(expr):
    return sp.Poly(sp.expand(expr), e).nth(0) + e*sp.Poly(sp.expand(expr), e).nth(1) + e**2*sp.Poly(sp.expand(expr), e).nth(2)

def Q(r):
    return r+h*e*r**3/12+h**2*e**2*r**5/480

def C(r):
    return 1+h*e*r**2/4+h**2*e**2*r**4/96

r = z+b-s
A = sp.cancel((Q(z+b)-Q(b))/z)
V = sp.cancel(((Q(z+b)-Q(b))*(C(z+b)-C(b))+Q(z)-z)/z**2)
K = 1+h*e*r**2/6-h**2*e**2*r**4/180
correction = trunc(-r*V+A**2*K-1)
f2 = sp.factor(sp.expand(correction).coeff(e, 1)/h)
f4 = sp.factor(sp.expand(correction).coeff(e, 2)/h**2)
W = 1-(b-s)**2+e*D*f2+e**2*T*f4
assert sp.simplify(W.subs(e,0) - (1-(b-s)**2)) == 0

# This is log(-W_s/W_b) before inserting the perturbed incidence root.
d = b-s
g2 = sp.factor(D*(sp.diff(f2,s)+sp.diff(f2,b))/(2*d))
g4 = sp.factor(T*(sp.diff(f4,s)+sp.diff(f4,b))/(2*d)
    + D**2*(sp.diff(f2,b)**2-sp.diff(f2,s)**2)/(8*d**2))

records = {}
for name, emitter, receiver in [('plus',s,b), ('minus',b,s)]:
    point = {emitter:0, receiver:1}
    alpha = sp.factor(D*f2.subs(point)/2)
    beta = sp.factor((-alpha**2+D*alpha*sp.diff(f2,receiver).subs(point)
                       +T*f4.subs(point))/2)
    root = 1+e*alpha+e**2*beta
    incidence = trunc(W.subs(emitter,0).subs(receiver,root))
    assert sp.expand(incidence) == 0
    sign = 1 if name == 'plus' else -1
    c2 = sp.factor(sign*g2.subs(point))
    c4 = sp.factor(sign*(g4.subs(point)+alpha*sp.diff(g2,receiver).subs(point)))
    # Endpoint derivative expansion, separately from the log formula above.
    numerator = -sp.diff(W,emitter)
    denominator = sp.diff(W,receiver)
    ns = trunc(numerator.subs(emitter,0).subs(receiver,root))
    ds = trunc(denominator.subs(emitter,0).subs(receiver,root))
    n0,n1,n2 = [sp.expand(ns).coeff(e,k) for k in range(3)]
    d0,d1,d2 = [sp.expand(ds).coeff(e,k) for k in range(3)]
    assert n0 == d0
    alt2 = n1/n0-d1/d0
    alt4 = n2/n0-n1**2/(2*n0**2)-d2/d0+d1**2/(2*d0**2)
    assert sp.simplify(alt2-c2) == 0
    assert sp.simplify(alt4-c4) == 0

    def mean(expr):
        poly=sp.Poly(sp.expand(expr),D,T)
        ans=0
        for (dp,tp),coeff in poly.terms():
            if dp == 1:
                continue
            assert dp in (0,2)
            phi = (1-z*z)**tp * (1 if dp==0 else (1-z*z)**2/2)
            ans += sp.integrate(coeff*phi,(z,-1,1))/2
        return sp.factor(ans)
    records[name] = {'arrival_correction_L3':str(alpha),
        'arrival_correction_L5':str(beta), 'log_L2':str(c2),
        'log_L4':str(c4), 'spherical_L2':str(mean(c2)),
        'spherical_L4':str(mean(c4)),
        'longitudinal_reflection_difference_L4':str(sp.factor(c4-c4.subs(z,-z)))}

path=Path(__file__)
result={'method':'independent exact plane-wave world function and full-sphere moments',
    'supplied_metric':'-2du dv+dx^2+dy^2+(x^2-y^2)du^2',
    'f2':str(f2), 'f4':str(f4), 'clock_series':records,
    'python':platform.python_version(),'sympy':sp.__version__,
    'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
    'scope':'formal exact coefficients plus analytic local remainder argument; no interval sign radius'}
out=path.with_name('source_first_plane_wave_result.json')
with out.open('x') as f:
    json.dump(result,f,indent=2)
    f.write('\n')
print(json.dumps(result,indent=2))

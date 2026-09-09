"""Author implementation: original Christoffel/Riemann/Ricci, not reduced residual only.

Before new reviewer scientific disclosure. SymPy exact arithmetic is a method,
not formal proof. No imports from prior scientific checks or reviewer code.
"""
import functools
import hashlib
import json
import platform
import sys
from pathlib import Path
import sympy as s

t, x, y, z = coords = s.symbols('t x y z', real=True)
a = s.Function('a')(t, x)
p = s.Function('p')(t, x)
g = [-s.exp(2*a), s.exp(2*a), t*s.exp(p), t*s.exp(-p)]
tests = []

def zero(name, expression):
    r = s.simplify(s.expand(expression))
    assert r == 0, (name, r)
    tests.append(name)

@functools.lru_cache(None)
def G(i,j,k):
    return s.simplify(((s.diff(g[i],coords[j]) if i==k else 0)
                     +(s.diff(g[i],coords[k]) if i==j else 0)
                     -(s.diff(g[j],coords[i]) if j==k else 0))/(2*g[i]))

@functools.lru_cache(None)
def R(i,j,k,l):
    return s.simplify(s.diff(G(i,l,j),coords[k])-s.diff(G(i,k,j),coords[l])
         +sum(G(i,k,h)*G(h,l,j)-G(i,l,h)*G(h,k,j) for h in range(4)))

pt, px = s.diff(p,t), s.diff(p,x)
ptt = s.diff(p,t,2)
wave = s.diff(p,x,2)-pt/t
at = -1/(4*t)+t*(pt**2+px**2)/4
ax = t*pt*px/2
subs = {s.diff(a,t,2): s.diff(at,t).subs(ptt,wave),
        s.diff(a,x,2): s.diff(ax,x),
        s.diff(a,t,x): s.diff(at,x),
        s.diff(a,t): at, s.diff(a,x): ax, ptt: wave}

def shell(expression):
    return s.simplify(s.expand(expression.subs(subs, simultaneous=True)))

zero('constraint_integrability', s.diff(at,x)-s.diff(ax,t).subs(ptt,wave))
ric = [[s.simplify(sum(R(i,j,i,k) for i in range(4))) for k in range(4)] for j in range(4)]
for j in range(4):
    for k in range(4):
        zero('original_Ric_%s%s'%(j,k), shell(ric[j][k]))

# Direct orthonormal tidal components R(e_i,n,e_i,n), sign agrees with SE1.
tidal = [s.simplify(R(i,0,i,0)/s.exp(2*a)) for i in (1,2,3)]
delta = s.simplify(s.exp(2*a)*(tidal[1]-tidal[2]))
delta_expected = -s.diff(p,x,2)+at*pt+ax*px
zero('original_Riemann_transverse_difference', shell(delta)-delta_expected)
zero('Ricci_trace_tidal', sum(shell(v) for v in tidal))
theta = s.diff(s.log(s.exp(a)*t),t)/s.exp(a)
zero('volume_expansion', shell(theta)-(3/(4*t)+t*(pt**2+px**2)/4)/s.exp(a))

# Full initial data, including lapse and pullback x=4X/3.
e, X, m = s.symbols('e X m', real=True)
q = e*s.cos(m*X)
ini = {t:s.Integer(1),a:s.log(s.Rational(3,4)),p:s.Integer(0),
       pt:3*q/2,px:s.Integer(0),s.diff(a,t):-s.Rational(1,4)+9*q**2/16}
N0 = s.Rational(3,4)
gamma0 = [s.Rational(16,9)*g[1],g[2],g[3]]
for i,v in enumerate(gamma0):
    zero('initial_gamma_%s'%i,v.subs(ini,simultaneous=True)-1)
K = [-s.diff(s.log(g[i]),t)/(2*s.exp(a)) for i in (1,2,3)]
K0 = [s.simplify(v.subs(ini,simultaneous=True)) for v in K]
target = [s.Rational(1,3)-3*q**2/4,-s.Rational(2,3)-q,-s.Rational(2,3)+q]
for i in range(3):
    zero('initial_K_%s'%i,K0[i]-target[i])
zero('initial_Hamiltonian',sum(K0)**2-sum(v*v for v in K0))
zero('initial_momentum_X',s.diff(K0[0],X)-s.diff(sum(K0),X))
zero('initial_momentum_y',s.diff(K0[1],y)-s.diff(sum(K0),y))
zero('initial_momentum_z',s.diff(K0[2],z)-s.diff(sum(K0),z))

# Actual mutation catches: full nonlinear metric cannot keep Taub a unchanged.
bg = {s.diff(a,t,2):1/(4*t**2),s.diff(a,x,2):0,
      s.diff(a,t,x):0,s.diff(a,t):-1/(4*t),s.diff(a,x):0,ptt:wave}
broken = s.simplify(ric[0][0].subs(bg,simultaneous=True))
sample = broken.subs({pt:s.Rational(1,4),px:s.Integer(0)})
assert sample != 0, ('fixed_background_a_false_pass',sample)
tests.append('mutant_fixed_background_a_rejected_by_original_Ric00')
wrong_Kx = s.Rational(1,3)
bad_H = s.expand((wrong_Kx+target[1]+target[2])**2-wrong_Kx**2-target[1]**2-target[2]**2)
assert s.simplify(bad_H+2*q*q)==0 and bad_H.subs({e:s.Rational(1,6),X:0,m:1})!=0
tests.append('mutant_omitted_quadratic_K_completion_rejected_by_H')

print(json.dumps({'python':platform.python_version(),'sympy':s.__version__,
 'implementation':'author original diagonal metric tensor construction',
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'tests':tests,'count':len(tests),
 'metric_shape':[4,4], 'Ricci_original':[[str(v) for v in row] for row in ric],
 'tidal_delta_divided_by_Z':str(s.expand(delta_expected)),
 'fixed_background_a_Ric00':str(broken), 'mutant_sample':str(sample),
 'initial_K':[str(v) for v in K0]},indent=2))

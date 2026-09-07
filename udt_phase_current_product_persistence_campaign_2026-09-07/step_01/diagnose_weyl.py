"""Exact pre-freeze diagnostic; full Weyl recipe, not R on Lambda !=0."""
import contextlib
import io
import json
import runpy
from pathlib import Path
from itertools import product
import sympy as s
# Deliberately reused author exploratory tensor assembly; NOT independent.
with contextlib.redirect_stdout(io.StringIO()):
    a=runpy.run_path(str(Path(__file__).with_name('explore_algebra.py')))
Q,R,E,v,sub,eta,I=[a[x] for x in ('Q','R','E','v','sub','eta','I')]
lam=-s.trace(E)
assert all(s.expand(sum(eta[a]*Q[a,b,c,a] for a in I)-lam*eta[b]*int(b==c))==0
           for b,c in product(I,repeat=2))
assert all(s.expand(Q[a,b,c,d]+Q[b,c,a,d]+Q[c,a,b,d])==0
           for a,b,c,d in product(I,repeat=4))
rho,p,q=v[2],v[8],v[7]
lambda_seed=-rho
def g(a,b): return eta[a] if a==b else 0
W={(a,b,c,d):s.expand(x-lambda_seed*s.Rational(1,3)*(g(b,c)*g(a,d)-g(a,c)*g(b,d)))
   for (a,b,c,d),x in R.items()}
assert all(s.expand(sum(eta[a]*W[a,b,c,a] for a in I))==0 for b,c in product(I,repeat=2))
star={(a,b,c,d):s.expand(sum(s.LeviCivita(a,b,m,n)*eta[m]*eta[n]*W[m,n,c,d]
    for m,n in product(I,repeat=2))/2) for a,b,c,d in product(I,repeat=4)}
B={(a,b,c,d):s.expand(sum(eta[e]*eta[h]*(W[a,e,c,h]*W[b,e,d,h]+
    star[a,e,c,h]*star[b,e,d,h]) for e,h in product(I,repeat=2)))
    for a,b,c,d in product(I,repeat=4)}
l=(-1,0,0,1)
assert all(s.expand(R[a,b,0,d]+R[a,b,3,d]).subs(rho,0)==0 for a,b,d in product(I,repeat=3))
assert all(s.expand(B[a,b,c,d].subs(rho,0)-4*(p*p+q*q)*l[a]*l[b]*l[c]*l[d])==0
           for a,b,c,d in product(I,repeat=4))
print(json.dumps(dict(status='PASS',tracefree=True,
    E_seed=[[str(x.subs(sub,simultaneous=True)) for x in E.row(k)] for k in range(3)],
    M_seed=[[str(x.subs(sub,simultaneous=True)) for x in a['M'].row(k)] for k in range(3)],
    lambda_seed=str(lambda_seed),B1111=str(B[1,1,1,1]),
    B0000=str(B[0,0,0,0]),B0011=str(B[0,0,1,1]),B1000=str(B[1,0,0,0]),
    B2000=str(B[2,0,0,0]),
    root_subcase='Lambda=0 gives B=4*(p^2+q^2)*ell_flat^4 for normalized ell=e0+e3',
    ambient_nonzero={str((a,b,d)):str(s.expand(R[a,b,0,d]+R[a,b,3,d]))
    for a,b,d in product(I,repeat=3) if s.expand(R[a,b,0,d]+R[a,b,3,d])!=0},
    B_full={str(z):str(x) for z,x in B.items()}),indent=2,sort_keys=True))

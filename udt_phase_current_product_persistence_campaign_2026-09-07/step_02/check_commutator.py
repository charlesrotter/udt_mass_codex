"""Full bundle-wave commutator control on a NONVACUUM exact metric."""
import argparse
from functools import lru_cache
from itertools import product
import json
import sys
import sympy as s
ap=argparse.ArgumentParser()
ap.add_argument('--mutant',choices=('omit_div_curvature','omit_Ricci','half_curvature'))
mode=ap.parse_args().mutant
t,x,y,z=s.symbols('t x y z',real=True)
coords=(t,x,y,z); I=range(4); eta=(-1,1,1,1); scale=t*t+2
g=s.diag(*[a*scale**2 for a in eta]); gi=g.inv()
simp=s.cancel
G={(a,b,c):simp(sum(gi[a,d]*(s.diff(g[d,b],coords[c])+s.diff(g[d,c],coords[b])-
    s.diff(g[b,c],coords[d])) for d in I)/2) for a,b,c in product(I,repeat=3)}
R={(b,c,m,n):simp(s.diff(G[b,n,c],coords[m])-s.diff(G[b,m,c],coords[n])+
    sum(G[b,m,d]*G[d,n,c]-G[b,n,d]*G[d,m,c] for d in I))
   for b,c,m,n in product(I,repeat=4)}
Ric={(a,c):simp(sum(R[m,c,m,a] for m in I)) for a,c in product(I,repeat=2)}
V=(1+t*x,x+y*t,y+z*t*t,z+x*x)
# covariant tensors below have one upper slot then any number of lower slots.
def derivative(data,lower_rank):
    out={}
    for indices in product(I,repeat=lower_rank+2):
        b,*low,a=indices
        val=s.diff(data[tuple([b]+low)],coords[a])
        val+=sum(G[b,a,c]*data[tuple([c]+low)] for c in I)
        for k,l in enumerate(low):
            val-=sum(G[c,a,l]*data[tuple([b]+low[:k]+[c]+low[k+1:])] for c in I)
        out[indices]=simp(val)
    return out
vec={(b,):V[b] for b in I}
A=derivative(vec,0) # A[b,a]=nabla_a V^b
dA=derivative(A,1)
ddA=derivative(dA,2)
boxV={(b,):simp(sum(gi[m,m]*dA[b,m,m] for m in I)) for b in I}
gradBox=derivative(boxV,0)
boxA={(b,a):simp(sum(gi[m,m]*ddA[b,a,m,m] for m in I)) for b,a in product(I,repeat=2)}
# Compute divergence of curvature by differentiating its FULL tensor, including
# the connection on both curvature-form slots; do not differentiate components only.
dR=derivative(R,3) # order b,c,m,n ; appended derivative
divR={(b,c,a):simp(sum(gi[m,m]*dR[b,c,m,a,m] for m in I))
      for b,c,a in product(I,repeat=3)}
termF={(b,a):simp(2*sum(gi[m,m]*R[b,c,m,a]*A[c,m] for c,m in product(I,repeat=2)))
       for b,a in product(I,repeat=2)}
termRic={(b,a):simp(sum(Ric[a,c]*gi[c,c]*A[b,c] for c in I))
         for b,a in product(I,repeat=2)}
termDiv={(b,a):simp(sum(divR[b,c,a]*V[c] for c in I)) for b,a in product(I,repeat=2)}
assert any(v!=0 for v in termF.values())
assert any(v!=0 for v in termRic.values())
assert any(v!=0 for v in termDiv.values())
factor=s.Rational(1,2) if mode=='half_curvature' else 1
res={(b,a):simp(boxA[b,a]-gradBox[b,a]-factor*termF[b,a]-
    (0 if mode=='omit_Ricci' else termRic[b,a])-
    (0 if mode=='omit_div_curvature' else termDiv[b,a]))
     for b,a in product(I,repeat=2)}
bad={str(k):str(v) for k,v in res.items() if v!=0}
result=dict(status='FAIL' if bad else 'PASS',mutant=mode,
    equation='Box(nabla_a V)=nabla_a(Box V)+2 R^m_a(nabla_m V)+Ric_a^c nabla_c V+(nabla^m R_ma)V',
    metric='(t^2+2)^2 diag(-1,1,1,1), t near0; OFF-EQUATION identity control',
    V=list(map(str,V)),components=16,nonzero_term_counts={
        'two_curvature_gradient':sum(v!=0 for v in termF.values()),
        'Ricci_gradient':sum(v!=0 for v in termRic.values()),
        'div_curvature_vector':sum(v!=0 for v in termDiv.values())},
    residuals=bad,python=sys.version,sympy=s.__version__,
    scope='exact coordinate support for general bundle identity, NOT PDE preservation proof')
print(json.dumps(result,indent=2,sort_keys=True))
raise SystemExit(1 if bad else 0)

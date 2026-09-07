"""Exploratory exact linear algebra, not a frozen theorem checker."""
from itertools import product
import json
import sympy as s
I=range(4); J=range(1,4); eta=(-1,1,1,1)
v=s.symbols('a b c d e f h i j k l')
a,b,c,d,e,f,h,i,j,k,l=v
E=s.Matrix([[a,d,f],[d,b,e],[f,e,c]])
M=s.Matrix([[h,j,l],[j,i,k],[l,k,-h-i]])
Q={}
def put(a,b,c,d,x):
    for aa,bb,cc,dd,sign in ((a,b,c,d,1),(b,a,c,d,-1),(a,b,d,c,-1),
        (b,a,d,c,1),(c,d,a,b,1),(d,c,a,b,-1),(c,d,b,a,-1),(d,c,b,a,1)):
        y=s.expand(sign*x); key=(aa,bb,cc,dd)
        assert key not in Q or s.expand(Q[key]-y)==0
        Q[key]=y
for a,b in product(J,repeat=2): put(a,0,0,b,E[a-1,b-1])
for a,b,c in product(J,repeat=3):
    put(a,0,b,c,sum(s.LeviCivita(b,c,d)*M[d-1,a-1] for d in J))
for a,b,c,d in product(J,repeat=4):
    put(a,b,c,d,sum(s.LeviCivita(a,b,m)*s.LeviCivita(c,d,n)*E[m-1,n-1]
                    for m,n in product(J,repeat=2)))
Q={z:Q.get(z,s.S.Zero) for z in product(I,repeat=4)}
eq=[Q[a,b,0,d]+Q[a,b,3,d] for a,b in product(J,repeat=2) for d in I]
A,_=s.linear_eq_to_matrix(eq,v)
solution=next(iter(s.linsolve((A,s.zeros(A.rows,1)),v)))
sub=dict(zip(v,solution))
R={z:s.expand(x.subs(sub,simultaneous=True)) for z,x in Q.items()}
star={(a,b,c,d):s.expand(sum(s.LeviCivita(a,b,m,n)*eta[m]*eta[n]*R[m,n,c,d]
        for m,n in product(I,repeat=2))/2) for a,b,c,d in product(I,repeat=4)}
B={(a,b,c,d):s.expand(sum(eta[e]*eta[h]*(R[a,e,c,h]*R[b,e,d,h]+
        star[a,e,c,h]*star[b,e,d,h]) for e,h in product(I,repeat=2)))
        for a,b,c,d in product(I,repeat=4)}
print(json.dumps(dict(sympy=s.__version__,variables=list(map(str,v)),
    seed_rank=A.rank(),solution=list(map(str,solution)),
    lambda_on_seed=str(s.expand(-s.trace(E).subs(sub,simultaneous=True))),
    ambient_annihilation=all(s.expand(R[a,b,0,d]+R[a,b,3,d])==0
                             for a,b,d in product(I,repeat=3)),
    B_nonzero={str(z):str(x) for z,x in B.items() if x!=0},
    R_nonzero={str(z):str(x) for z,x in R.items() if x!=0}),indent=2,sort_keys=True))

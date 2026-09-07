"""G358 source algebra, separately implemented; no author scientific import."""
import itertools
import json
import platform
import sympy as s

ids=range(4); spatial=range(1,4); tuples=list(itertools.product(ids,repeat=4))
aa,bb,dd,ee,ff,mm,nn,pp,qq,rr=s.symbols('a b d e f m n p q r',real=True)
variables=(aa,bb,dd,ee,ff,mm,nn,pp,qq,rr)
E=s.Matrix([[aa,dd,ee],[dd,bb,ff],[ee,ff,-aa-bb]])
M=s.Matrix([[mm,pp,qq],[pp,nn,rr],[qq,rr,-mm-nn]])
eta=(-1,1,1,1)
Q={t:s.S.Zero for t in tuples}
def fill(a,b,c,d,val):
    for i,j,k,l,sign in ((a,b,c,d,1),(b,a,c,d,-1),(a,b,d,c,-1),(b,a,d,c,1),(c,d,a,b,1),(d,c,a,b,-1),(c,d,b,a,-1),(d,c,b,a,1)):
        Q[i,j,k,l]=val*sign
for i,j in itertools.product(spatial,repeat=2):fill(i,0,0,j,E[i-1,j-1])
for i,j,k in itertools.product(spatial,repeat=3):
    if j<k:fill(i,0,j,k,sum(s.LeviCivita(j,k,l)*M[l-1,i-1] for l in spatial))
for i,j,k,l in itertools.product(spatial,repeat=4):
    Q[i,j,k,l]=sum(s.LeviCivita(i,j,h)*s.LeviCivita(k,l,n)*E[h-1,n-1] for h,n in itertools.product(spatial,repeat=2))
assert all(s.expand(Q[a,b,c,d]+Q[b,c,a,d]+Q[c,a,b,d])==0 for a,b,c,d in tuples)
assert all(s.expand(sum(eta[a]*Q[a,b,c,a] for a in ids))==0 for b,c in itertools.product(ids,repeat=2))
star={(a,b,c,d):s.expand(sum(s.LeviCivita(a,b,m,n)*eta[m]*eta[n]*Q[m,n,c,d] for m,n in itertools.product(ids,repeat=2))/2) for a,b,c,d in tuples}
def B(a,b,c,d):return s.expand(sum(eta[h]*eta[k]*(Q[a,h,c,k]*Q[b,h,d,k]+star[a,h,c,k]*star[b,h,d,k]) for h,k in itertools.product(ids,repeat=2)))
energy=B(0,0,0,0); flux=B(0,0,0,3); saturation=s.expand(energy+flux)
gram=s.hessian(saturation,variables)/2
kernel=gram.nullspace()
assert len(kernel)==2
# Exact eigenvalues certify this quadratic is positive semidefinite, not an
# indefinite equation whose cancellation would invalidate a kernel argument.
eigen=gram.eigenvals(); assert all(k.is_nonnegative for k in eigen)
P,T=s.symbols('P T',real=True)
special={aa:-P,bb:P,dd:-T,ee:0,ff:0,mm:-T,nn:T,pp:P,qq:0,rr:0}
assert (gram*s.Matrix([special[q] for q in variables]))==s.zeros(10,1)
# This is exactly the null-annihilating two-parameter Weyl class.
assert all(s.expand((Q[a,b,0,d]+Q[a,b,3,d]).subs(special))==0 for a,b,d in itertools.product(ids,repeat=3))
Lflat=(-1,0,0,1)
assert all(s.expand(B(*t).subs(special)-4*(P*P+T*T)*s.prod(Lflat[k] for k in t))==0 for t in tuples)
print(json.dumps(dict(python=platform.python_version(),sympy=s.__version__,variables=list(map(str,variables)),energy=str(energy),flux=str(flux),saturation=str(saturation),gram=str(gram),gram_eigenvalues={str(k):int(v) for k,v in eigen.items()},kernel=[str(k) for k in kernel],full_null_annihilation=True,full256_root_class=True),indent=2))

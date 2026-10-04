#!/usr/bin/env python3
"""Original diagonal metric curvature and response diagnostic; independent code."""
import hashlib
import json
from pathlib import Path
import resource
import sys
import time
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import sympy as s
start=time.time()
p=Path(__file__).resolve().parent
t,r,theta,phi=s.symbols('t r theta phi',real=True)
m,lam,a=s.symbols('m Lambda a',positive=True)
coords=[t,r,theta,phi]
f=1-2*m/r-lam*r*r/3
g=[-f,1/f,r*r,r*r*s.sin(theta)**2]
gi=[1/q for q in g]
Gamma={}
for i in range(4):
 for j in range(4):
  for k in range(4):
   z=gi[i]*((s.diff(g[i],coords[j]) if k==i else 0)+(s.diff(g[i],coords[k]) if j==i else 0)-(s.diff(g[j],coords[i]) if j==k else 0))/2
   z=s.simplify(z)
   if z!=0: Gamma[i,j,k]=z
G=lambda i,j,k: Gamma.get((i,j,k),0)
R={}
for i in range(4):
 for j in range(4):
  for k in range(4):
   for l in range(4):
    z=s.diff(G(i,j,l),coords[k])-s.diff(G(i,j,k),coords[l])+sum(G(i,k,n)*G(n,j,l)-G(i,l,n)*G(n,j,k) for n in range(4))
    z=s.trigsimp(s.simplify(z))
    if z!=0:R[i,j,k,l]=z
Ric=[s.simplify(sum(R.get((i,j,i,j),0) for i in range(4))) for j in range(4)]
assert all(s.simplify(Ric[j]-lam*g[j])==0 for j in range(4))
K=s.simplify(sum(gi[i]*gi[j]*gi[k]*gi[l]*(g[i]*z)**2 for (i,j,k,l),z in R.items()))
Rscalar=s.simplify(sum(gi[j]*Ric[j] for j in range(4)))
Ric2=s.simplify(sum((gi[j]*Ric[j])**2 for j in range(4)))
Weyl2=s.simplify(K-2*Ric2+Rscalar**2/3)
assert s.simplify(Weyl2-48*m*m/r**6)==0
trace=s.simplify((r*r*s.diff(f,r,2)-r*s.diff(f,r))/2+1-f+r*s.diff(f,r)/2)
assert trace==0
assert s.simplify((r*r*s.diff(f,r,2)-r*s.diff(f,r))/2+3*m/r)==0
assert s.simplify(1-f+r*s.diff(f,r)/2-3*m/r)==0
response_contraction=s.factor(2*f*s.diff(Weyl2,r)**2)
assert s.simplify(response_contraction-2*f*(288*m*m/r**7)**2)==0
h=1-3*m/a
ell2=a*a*(m/a-lam*a*a/3)/h
Vpp=s.simplify(s.diff(f*(1+ell2/r**2),r,2).subs(r,a))
assert s.simplify(Vpp-2*(m*(a-6*m)-(lam*a**3/3)*(4*a-15*m))/(a**3*(a-3*m)))==0
assert s.simplify(s.diff(f/r**2,r)+2*(r-3*m)/r**4)==0
out={'status':'PASS','python':sys.version,'sympy':s.__version__,'metric':'diagonal original four-dimensional metric; curvature from Christoffels','nonzero_connection_components':len(Gamma),'nonzero_riemann_components':len(R),'Ricci':list(map(str,Ric)),'Kretschmann':str(K),'Weyl_squared':str(Weyl2),'native_angular_trace':str(trace),'DDR_witness_contraction':str(response_contraction),'radial_Vpp':str(Vpp),'elapsed_seconds':time.time()-start,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(p/'exposed_exact_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

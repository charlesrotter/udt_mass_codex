"""Off-equation, finite-epsilon original intrinsic Gauss/Codazzi sign control."""
import contextlib
import io
import itertools
import json
from pathlib import Path
import runpy
with contextlib.redirect_stdout(io.StringIO()):
    d=runpy.run_path(str(Path(__file__).with_name('compare_frozen.py')))
s=d['s']; u,v,x,y,e=(d[z] for z in ('u','v','x','y','e'))
I=range(4); J=range(3); q=(u,x,y); simplify=s.simplify
# Free exact diagnostic value: original equation is intentionally NOT satisfied.
value=s.Rational(1,5); sub={e:value,v:-2*u}
T=d['T']; metric=d['finite'].subs(e,value)
gamma=(T.T*metric*T).subs(v,-2*u); inverse=gamma.inv()
S=d['S'].subs(sub)
K=s.Matrix(3,3,lambda i,j:simplify(-sum(T[a,i]*T[b,j]*(2*d['Gamma'][0,a,b]+d['Gamma'][1,a,b]).subs(sub) for a,b in itertools.product(I,repeat=2))/s.sqrt(S)))
C={}
for a,b,c in itertools.product(J,repeat=3):
    C[a,b,c]=simplify(sum(inverse[a,z]*(s.diff(gamma[z,c],q[b])+s.diff(gamma[z,b],q[c])-s.diff(gamma[b,c],q[z])) for z in J)/2)
ric=s.Matrix(3,3,lambda a,b:simplify(sum(s.diff(C[c,a,b],q[c])-s.diff(C[c,c,a],q[b])+sum(C[c,c,z]*C[z,a,b]-C[c,b,z]*C[z,c,a] for z in J) for c in J)))
A=inverse*K
ham=simplify(s.trace(inverse*ric)+s.trace(A)**2-s.trace(A*A))
mom=s.Matrix([simplify(sum(s.diff(A[j,i],q[j])+sum(C[j,j,m]*A[m,i]-C[m,j,i]*A[j,m] for m in J) for j in J)-s.diff(s.trace(A),q[i])) for i in J])
expected_ham=simplify(8*value**2*x*x/S)
expected_mom=s.Matrix([-4*value**2*x*x/s.sqrt(S),0,0])
assert simplify(ham-expected_ham)==0
assert (mom-expected_mom).applyfunc(simplify)==s.zeros(3,1)
point={u:0,x:1,y:0}
assert ham.subs(point)!=0 and mom[0].subs(point)!=0
print(json.dumps(dict(status='PASS',epsilon=value,diagnostic_type='OFF_EQUATION_NOT_AN_ADMITTED_COUNTEREXAMPLE',intrinsic_H=ham,intrinsic_M=list(mom),H_at_point=ham.subs(point),M_at_point=list(mom.subs(point)),identity_scope='exact expressions on regular graph for epsilon=1/5; analytic Gauss/Codazzi owns general identity'),indent=2,default=str))

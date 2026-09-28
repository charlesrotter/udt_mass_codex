#!/usr/bin/env python3
"""Direct-stage exact algebra, written after text/code exposure, imports no producer code."""
import datetime,hashlib,json,platform
from pathlib import Path
import sympy as s
done=[]
def zero(name, expr):
    vals=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
    assert all(s.simplify(v)==0 for v in vals),(name,vals)
    done.append(name)

eta=s.diag(-1,1,1,1)
slots=[(i,j) for i in range(4) for j in range(i,4)]
# Use both signs of each mixed spatial null direction; no author direction list reused.
dirs=[]
for i in range(3):
    for sign in [-1,1]:
        v=s.zeros(3,1);v[i]=sign;dirs.append(v)
for i,j in [(0,1),(1,2),(0,2)]:
    for sign in [-1,1]:
        v=s.zeros(3,1);v[i]=s.Rational(5,13);v[j]=sign*s.Rational(12,13);dirs.append(v)
nulls=[s.Matrix([1,*list(v)]) for v in dirs]
design=s.Matrix([[n[a]*n[b]*(1 if a==b else 2) for a,b in slots] for n in nulls])
for n in nulls:zero('null vector', (n.T*eta*n)[0])
zero('null design rank nine',design.rank()-9)
ker=design.nullspace()
zero('single null ambiguity',len(ker)-1)
gvec=s.Matrix([eta[a,b] for a,b in slots])
zero('ambiguity exactly metric line',ker[0]-ker[0][0]*gvec/gvec[0])
trace=s.Matrix([[eta[a,b] if a==b else 0 for a,b in slots]])
zero('trace row completes rank ten',design.col_join(trace).rank()-10)

# Generic non-orthonormal coordinate values make lowering explicit.
g=s.diag(-9,4,16,25);gi=g.inv();U=s.Matrix([s.Rational(1,3),0,0,0]);n=s.Matrix([0,s.Rational(1,2),0,0])
P=(g*U)*(g*U).T/2;H=2*((g*U)*(g*U).T+(g*n)*(g*n).T)
pair=lambda B,C:s.trace(gi*B*gi*C)
zero('kernel coefficient pairing',pair(P,H)-1)
zero('inverse coefficient same pairing',pair(-P,H)+1)
eps=s.symbols('eps',real=True);K=s.Matrix([1,0,0,0])
phi=lambda metric:-s.log(-(K.T*metric*K)[0])/2
zero('same physical covariant variation',s.diff(phi(g+eps*H),eps).subs(eps,0)-1)
inverse_tangent=-gi*H*gi
zero('same physical inverse variation',s.diff(phi((gi+eps*inverse_tangent).inv()),eps).subs(eps,0)-1)

c=s.symbols('c',positive=True)
a,b,R=s.symbols('a b R')
q=s.symbols('q:10')
Q=s.Matrix(4,4,lambda i,j:q[slots.index((min(i,j),max(i,j)))])
tf=lambda tensor,metric:tensor-metric*s.trace(metric.inv()*tensor)/4
T=tf(Q,g)
zero('projection under scaled metric',tf(Q,c*c*g)-T)
zero('zero trace under both metrics',s.trace((c*c*g).inv()*T))
zero('arbitrary pure trace ignored',tf(T+R*c**7*g,c*c*g)-T)
# Trace of the classified a Ric+b Rg forces a+4b=0, independently of normalization.
zero('class coefficient trace',s.trace(gi*(a*Q+b*s.trace(gi*Q)*g))-(a+4*b)*s.trace(gi*Q))
zero('tracefree class',tf(a*Q+b*s.trace(gi*Q)*g,g)-a*tf(Q,g))

# Open-interval contradiction as a polynomial identity, not finite interpolation.
r=s.symbols('r',positive=True);A,B,C=s.symbols('A B C')
u0=(r+1/r)/2;u1=(r-1/r)/2
poly=s.Poly(s.expand(r*r*(A*u0*u0+2*B*u0*u1+C*u1*u1-1/r)),r)
zero('linear readout obstruction coefficient',poly.coeff_monomial(r)+1)
assert poly.coeff_monomial(r)==-1

print(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'python':platform.python_version(),'sympy':s.__version__,'checks':done,
  'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
  'null_design_rank':design.rank(),'null_kernel':list(map(str,ker[0])),
  'boost_polynomial':str(poly.as_expr()),
  'scope':'exact algebra plus analytic argument audit; exposed direct stage, no physical law identification'},indent=2))

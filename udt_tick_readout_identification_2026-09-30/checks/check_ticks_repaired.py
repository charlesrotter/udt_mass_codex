import json
import sympy as s
from pathlib import Path
results=[]
def eq(name,a,b):
    d=a-b
    ok=all(s.simplify(x)==0 for x in d) if isinstance(d,s.MatrixBase) else s.simplify(d)==0
    assert ok,(name,a,b)
    results.append(name)
def neq(name,a,b):
    assert s.simplify(a-b)!=0,name
    rejected.append(name)
rejected=[]
g=s.diag(-1,1,1,1)
k=s.Matrix([1,1,0,0]); km=s.Matrix([1,-1,0,0])
ue=s.Matrix([1,0,0,0]); uo=s.Matrix([s.Rational(5,4),s.Rational(3,4),0,0]); v=s.Matrix([s.Rational(5,3),s.Rational(4,3),0,0])
def dot(a,b): return (a.T*g*b)[0]
def w(k,u): return -dot(k,u)
eq('future null plus',dot(k,k),0); eq('future null minus',dot(km,km),0)
for name,u in [('emitter',ue),('receiver',uo),('auxiliary',v)]: eq(name+' unit',dot(u,u),-1)
Z=w(k,ue)/w(k,uo)
eq('endpoint ratio',Z,2)
a=s.symbols('a',positive=True)
eq('per-ray affine cancellation',w(a*k,ue)/w(a*k,uo),Z)
eq('calibrated cadence receipt',w(7*k/w(k,ue),uo),s.Rational(7,2))
eq('auxiliary subdivision',w(k,ue)/w(k,v)*w(k,v)/w(k,uo),Z)
neq('actual endpoint replacement is not gauge',w(k,ue)/w(k,ue),Z)
x,t=s.symbols('x t',nonnegative=True)
A=x+x*x; Zx=s.diff(A,x)
eq('whole nonlinear interval',s.integrate(Zx,(x,0,1)),2)
neq('initial rate times interval is not whole duration',Zx.subs(x,0),2)
inv=(s.sqrt(1+4*t)-1)/2
eq('arrival inverse',s.simplify(A.subs(x,inv)),t)
ro=1/s.sqrt(1+4*t)
eq('density radicand factorization',1+4*A,(2*x+1)**2)
eq('density Jacobian positive branch',Zx/s.sqrt(s.factor(1+4*A)),1)
eq('whole count after pushforward',s.integrate(ro,(t,0,2)),1)
neq('omitted density Jacobian',s.integrate(s.Integer(1),(t,0,2)),1)
eq('first discrete tick',A.subs(x,s.Rational(1,4)),s.Rational(5,16))
eq('second discrete tick',A.subs(x,s.Rational(3,4)),s.Rational(21,16))
# Exact atom accounting on (0,1] at reception: exactly the first atom.
arrivals=[s.Rational(5,16),s.Rational(21,16)]
eq('finite atom count',sum(int(bool(0<y<=1)) for y in arrivals),1)
r11=s.Rational(1,2)+s.Rational(1,4); r31=s.Rational(3,2)+s.Rational(1,4)
eq('aggregate unit cadences',r11,s.Rational(3,4))
eq('aggregate different cadences',r31,s.Rational(7,4))
eq('normalized first aggregate',r11/2,s.Rational(3,8))
eq('normalized second aggregate',r31/4,s.Rational(7,16))
neq('same shifts do not fix aggregate normalized rate',r11/2,r31/4)
neq('redshift is not received/emitted rate',Z,1/Z)
J=4*k+km; Jnew=2*k+km
M=4*(g*k)*(g*k).T+(g*km)*(g*km).T
Mn=(g*k)*(g*k).T+(g*km)*(g*km).T
um=s.Matrix([3/s.sqrt(8),1/s.sqrt(8),0,0])
eq('old first moment',J,s.Matrix([5,3,0,0]))
eq('new first moment',Jnew,s.Matrix([3,1,0,0]))
eq('new current timelike',dot(Jnew,Jnew),-8)
eq('old moment minimizer',g*M*um,-4*um)
eq('new moment minimizer',g*Mn*ue,-2*ue)
eq('old current velocity',J[1]/J[0],s.Rational(3,5))
eq('new current velocity',Jnew[1]/Jnew[0],s.Rational(1,3))
neq('population moment invariant under spectral change',M[0,0],Mn[0,0])
neq('population rest frame invariant under spectral change',um[1]/um[0],ue[1])
print(json.dumps({'status':'PASS','exact_controls':len(results),'rejected_wrong_identities':len(rejected),'controls':results,'rejections':rejected,'sympy':s.__version__,'scope':'Exact finite controls; general hypotheses and proofs remain in candidate. No physical adoption.'},indent=2))

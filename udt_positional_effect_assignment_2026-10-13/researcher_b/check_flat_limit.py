"""Exact special-conformal identities for the PEA1 flat-limit discriminator."""
import hashlib
import json
import platform
from pathlib import Path
import sympy as S

HERE = Path(__file__).resolve().parent
t,x,y,z = X = S.symbols('t x y z', real=True)
a,L = S.symbols('a L', positive=True)
eta = S.diag(-1,1,1,1)
v = 1+2*a*t+a*a*(t*t-x*x-y*y-z*z)
F = S.Matrix([t+a*(t*t-x*x-y*y-z*z),x,y,z])/v
J = F.jacobian(X)
checks = {}

def equal(name, actual, expected):
    res = (S.Matrix(actual)-S.Matrix(expected)).applyfunc(S.factor)
    assert res == S.zeros(*res.shape), (name,res)
    checks[name] = 'EXACT_ZERO'

equal('full_pullback',J.T*eta*J,eta/v**2)
equal('determinant',[J.det(method='domain-ge')],[v**-4])
origin={q:0 for q in X}
equal('fixed_origin',F.subs(origin),S.zeros(4,1))
equal('identity_tangent',J.subs(origin),S.eye(4))
dv=S.Matrix([S.diff(v,q) for q in X])
equal('timelike_gradient_norm',[(dv.T*eta*dv)[0]],[-4*a*a*v])
equal('null_endpoint_factor',[v.subs({t:L,x:L,y:0,z:0})],[1+2*a*L])
equal('null_endpoint_image',F.subs({t:L,x:L,y:0,z:0}),
      [L/(1+2*a*L),L/(1+2*a*L),0,0])
sources=[Path(__file__),HERE/'FLAT_LIMIT_CHECK_PLAN.md']
out={'status':'PASS','scope':'Exact rational conformal-map identities only; family and clock limit proven analytically',
     'versions':{'python':platform.python_version(),'sympy':S.__version__},
     'checks':checks,'v':str(v),'F':[str(q) for q in F],
     'gradient_norm':str(-4*a*a*v),
     'source_sha256':{str(p.relative_to(HERE.parents[1])):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
with (HERE/'FLAT_LIMIT_CHECK_RESULT.json').open('x') as output:
    json.dump(out,output,indent=2);output.write('\n')
print(json.dumps(out,indent=2),flush=True)

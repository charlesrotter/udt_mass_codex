#!/usr/bin/env python3
"""Direct connection contraction for the bounded time-dependent diagnostic."""
from pathlib import Path
import hashlib,json,platform
import sympy as s
HERE=Path(__file__).resolve().parent
T,x=s.symbols('T x',real=True);f=s.Function('f')(T,x)
eps=s.symbols('epsilon',real=True);b=s.symbols('b',positive=True)
coords=(T,x);g=s.diag(-f,1/f);gi=g.inv()
Gamma=[[[s.simplify(sum(gi[i,l]*(s.diff(g[l,k],coords[j])+s.diff(g[l,j],coords[k])-s.diff(g[j,k],coords[l])) for l in range(2))/2) for k in range(2)] for j in range(2)] for i in range(2)]
U=s.Matrix([1/s.sqrt(f),0]);Ul=g*U
DU=s.Matrix(2,2,lambda i,j:s.simplify(s.diff(Ul[j],coords[i])-sum(Gamma[k][i][j]*Ul[k] for k in range(2))))
checks={}
for sign in (-1,1):
    k=s.Matrix([1/s.sqrt(f),sign*s.sqrt(f)])
    # omega=1 at the event; dS/dT=sqrt(f).
    direct=s.simplify((k.T*DU*k)[0]*s.sqrt(f))
    expected=-s.diff(f,T)/(2*f)+sign*s.diff(f,x)/2
    checks[f'direct_null_clock_contraction_{sign}']=s.simplify(direct-expected)==0
    C=s.Function('C')(T)
    supplied=direct.subs(f,C-b*x).doit()
    checks[f'spatial_Popt_time_live_{sign}']=s.simplify(supplied-(-s.diff(C,T)/(2*(C-b*x))-sign*b/2))==0
    for v in (0,2*b,-2*b):
        point=s.simplify(supplied.subs(C,1-v*T).doit().subs({T:0,x:0}))
        checks[f'local_rate_{sign}_{str(v)}']=s.simplify(point-(v-sign*b)/2)==0
phi=-s.log(f)/2
checks['spatial_Popt_residual']=s.simplify(1/f-(2/b)*s.diff(phi,x)-(1+s.diff(f,x)/b)/f)==0
checks['stationary_point_domain_counterexample']=s.diff(s.exp(-x**3),x).subs(x,0)==0
counter={'positive_both_directions':[str((2*b-sign*b)/2) for sign in (-1,1)],'negative_both_directions':[str((-2*b-sign*b)/2) for sign in (-1,1)]}
# Meaningful mutant: replace actual clock slope with total phi derivative.
wrong=s.diff(phi,T)+f*s.diff(phi,x)
right=-s.diff(f,T)/(2*f)+s.diff(f,x)/2
mutant_difference=s.simplify((wrong-right).subs(f,1-b*x).doit())
assert mutant_difference!=0
out={'scope':'single-context exact geometric controls, no selected dynamics','python':platform.python_version(),'sympy':s.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':checks,'local_sign_controls':counter,'wrong_endpoint_depth_rejected':bool(mutant_difference!=0),'mutant_difference':str(mutant_difference),'passed':all(checks.values())}
(HERE/'TIME_DEPENDENT_CHECK_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert all(checks.values())

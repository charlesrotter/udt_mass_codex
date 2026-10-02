"""Exact exposed check of direct shape equation's fourth-derivative rank."""
import json,hashlib
from pathlib import Path
import sympy as s
p0,p1,p2,p3,p4,alpha=s.symbols('p0 p1 p2 p3 p4 alpha')
jets=[p0,p1,p2,p3,p4]
dL=lambda e:sum(s.diff(e,jets[k])*jets[k+1] for k in range(4))
dt=lambda e:dL(e)/p0
H=p1/p0**2;R=6*p2/p0**3;K=dt(H);J=s.factor(2*R*K+dt(dt(R))-H*dt(R))
assert s.simplify(s.diff(J,p4)-6/p0**5)==0
normal=s.factor(s.solve(K+alpha*J,p4)[0])
assert s.factor((K+alpha*J).subs(p4,normal))==0
result={'pass':True,'J':str(J),'p4_coefficient_in_J':str(s.diff(J,p4)),
 'p4_normal_form':str(normal),'regular_domain':'p0>0 and constant alpha!=0; unrestricted Lambda is the conserved integration datum; prescribed Lambda additionally constrains initial data.',
 'limits':'Local smooth ODE normal form only; no global positivity, noisy inference, general PDE or physical admission.'}
p=Path(__file__).resolve().parent
with (p/'DIRECT_RANK_RESULT.json').open('x') as out:json.dump(result,out,indent=2);out.write('\n')
print(json.dumps(result,indent=2))

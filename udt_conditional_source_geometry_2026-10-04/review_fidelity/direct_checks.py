#!/usr/bin/env python3
"""Exposed-stage independent equation checks; no parent implementation imports."""
import json,os,platform,resource
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(2147483648,2147483648))
assert os.environ['OPENBLAS_NUM_THREADS']=='1' and os.environ['OMP_NUM_THREADS']=='1'
import sympy as S
checks=[]
def zero(name,x):
    y=S.simplify(x)
    if y!=0: raise AssertionError((name,str(y)))
    checks.append(name)
r,t,th,ph=S.symbols('r t th ph',real=True)
m,la,b,E=S.symbols('m Lambda b E',real=True)
f=1-2*m/r-la*r*r/3
g=S.diag(-f,1/f,r*r,r*r*S.sin(th)**2)
gi=g.inv(); xx=[t,r,th,ph]
G=[[[S.simplify(sum(gi[i,d]*(S.diff(g[d,k],xx[j])+S.diff(g[d,j],xx[k])-S.diff(g[j,k],xx[d])) for d in range(4))/2).subs(th,S.pi/2) for k in range(4)] for j in range(4)] for i in range(4)]
q=S.sqrt(1-f*b*b/r**2)
k=[1/f,q,0,b/r**2]
v=S.sqrt(E*E-f)
u=[E/f,v,0,0]
for name,vec in [('affine_null',k),('radial_receiver',u)]:
    for i in range(4):
        zero(f'{name}_original_geodesic_{i}',S.diff(vec[i],r)*vec[1]+sum(G[i][j][l]*vec[j]*vec[l] for j in range(4) for l in range(4)))
F,Q,V,En,B,R,I,Om=S.symbols('F Q V En B R I Om',positive=True)
Jac=S.Matrix([[(V-En*Q)/(F*Q*V),B*I],[B/(R**2*Q),I]])
det=Jac.det()
target=-I*(En-V*Q)/(F*V)
zero('incidence_determinant',(det-target).subs(B**2,R**2*(1-Q**2)/F))
Rprime=S.Matrix([[-1,B*I],[-Om,I]]).det()/target
zero('incidence_R_prime',Rprime-V*F*(1-Om*B)/(En-V*Q))
ell2=S.symbols('ell2')
pot=f*(1+ell2/r**2)
ellcirc=S.factor(r**3*S.diff(f,r)/(2*f-r*S.diff(f,r)))
zero('circular_stationary_effective_potential',S.diff(pot,r).subs(ell2,ellcirc))
V2=S.factor(S.diff(pot,r,2).subs(ell2,ellcirc))
finite=[]
for L0 in [S.Integer(0),S.Rational(1,10000)]:
    v2=V2.subs({m:1,r:10,la:L0})
    assert v2>0
    finite.append({'m':'1','a':'10','Lambda':str(L0),'fixed_ell_V_second':str(v2)})
result={'status':'PASS','checks':checks,'finite_case_count':len(finite),'cases':finite,'V_second_general':str(V2),'versions':{'python':platform.python_version(),'sympy':S.__version__},'maxrss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(__file__).with_name('DIRECT_CHECK_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','exact_checks':len(checks),'finite_cases':len(finite),'V_second_general':str(V2)},indent=2))

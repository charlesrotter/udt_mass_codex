"""Exact comparison geometry; no UDT field equation or physical source adopted.

Metric: diag(-A(r), B(r), r^2, r^2 sin(theta)^2), x0=c_E t.
Domain: r>0, A,B>0, regular angular chart. Static spherical control only.
Convention: Ric_ab = d_c Gamma^c_ab - d_b Gamma^c_ac
                     + Gamma^c_cd Gamma^d_ab - Gamma^c_bd Gamma^d_ac.
Compute from the connection, independently of stored scientific package code.
"""
import json
import platform
import time
from pathlib import Path

import sympy as s

start = time.monotonic()
x0, r, theta, az = s.symbols('x0 r theta az', real=True)
A, B = s.Function('A')(r), s.Function('B')(r)
x = (x0, r, theta, az)
g = s.diag(-A, B, r**2, r**2*s.sin(theta)**2)
gi = g.inv()
def clean(v):
    return s.factor(s.trigsimp(s.simplify(v)))
gamma = [[[clean(sum(gi[a,d]*(s.diff(g[d,c],x[b])+s.diff(g[d,b],x[c])-s.diff(g[b,c],x[d]))/2 for d in range(4)))
           for c in range(4)] for b in range(4)] for a in range(4)]
ric = s.Matrix(4,4,lambda a,b:clean(sum(
    s.diff(gamma[c][a][b],x[c])-s.diff(gamma[c][a][c],x[b])
    +sum(gamma[c][c][d]*gamma[d][a][b]-gamma[c][b][d]*gamma[d][a][c] for d in range(4))
    for c in range(4))))
scalar = clean(s.trace(gi*ric))
einstein = (gi*ric-s.eye(4)*scalar/2).applyfunc(clean)
checks = []
def equal(name, value, expected=0):
    residual = clean(value-expected)
    assert residual == 0, (name, residual)
    checks.append(name)

for a in range(4):
    for b in range(4):
        if a != b:
            equal(f'off_diagonal_{a}_{b}',einstein[a,b])
equal('general_clock_radial_difference',einstein[1,1]-einstein[0,0],
      (s.diff(A,r)/A+s.diff(B,r)/B)/(r*B))
equal('general_tt',einstein[0,0],(1/B-1)/r**2-s.diff(B,r)/(r*B**2))
equal('general_rr',einstein[1,1],(1/B-1)/r**2+s.diff(A,r)/(r*A*B))
primary=einstein.subs(B,1/A).doit().applyfunc(clean)
e0=(r*s.diff(A,r)+A-1)/r**2
e1=s.diff(A,r)/r+s.diff(A,r,2)/2
for i,v in enumerate((e0,e0,e1,e1)):
    equal(f'primary_component_{i}',primary[i,i],v)
equal('primary_conservation_identity',s.diff(e0,r)+2*(e0-e1)/r)
equal('all_primary_flat',sum(v**2 for v in primary.subs(A,1).doit()))
a,b,eps,L=s.symbols('a b eps L', real=True, nonzero=True)
f_einstein=1+a*r**2+b/r
einstein_family=primary.subs(A,f_einstein).doit().applyfunc(clean)
equal('einstein_family_residual',sum((einstein_family[i,i]-3*a)**2 for i in range(4)))
f_control=1+eps*r**4/L**4
control=primary.subs(A,f_control).doit().applyfunc(clean)
equal('control_tt',control[0,0],5*eps*r**2/L**4)
equal('control_angle',control[2,2],10*eps*r**2/L**4)
# This nonzero contrast distinguishes the control from an Einstein metric locally.
equal('control_anisotropy',control[2,2]-control[0,0],5*eps*r**2/L**4)
assert (control[2,2]-control[0,0]).subs({eps:1,L:1,r:1}) == 5
checks.append('nonzero_control_contrast_at_regular_positive_point')

# Completed-pair normalization is a different operation from fixing areal g_rr.
T,ls,beta=s.symbols('T ls beta', positive=True)
h=s.Matrix([[-T**2,-T**2*beta],[-T**2*beta,ls**2-T**2*beta**2]])
m=T*ls
hs=s.diag(1,1/m)*h*s.diag(1,1/m)
equal('completed_pair_det',hs.det(),-1)
equal('completed_pair_clock_kept',hs[0,0],-T**2)
equal('completed_pair_shift_kept',hs[0,1],-T*beta/ls)

out={
 'status':'PASS', 'checks':checks, 'count':len(checks),
 'python':platform.python_version(),'sympy':s.__version__,
 'elapsed_seconds':time.monotonic()-start,
 'general_einstein_mixed_diagonal':[str(einstein[i,i]) for i in range(4)],
 'primary_einstein_mixed_diagonal':[str(primary[i,i]) for i in range(4)],
 'control_mixed_diagonal':[str(control[i,i]) for i in range(4)],
 'limits':'Exact supplied static-spherical geometry on a regular positive domain. GR diagnostic only; no native metric admission, source interpretation, new law or full spacetime classification.'
}
Path(__file__).with_name('GEOMETRY_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

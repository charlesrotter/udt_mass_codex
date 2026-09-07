#!/usr/bin/env python3
"""Author exact algebra checks; no observations or imported author tensor code."""
import json
import platform
import sympy as s

checks = []
def check(name, value):
    assert value, name
    checks.append(name)
def zero(m):
    return all(s.expand(v) == 0 for v in m)

x,y,z,dx,dy,dz=s.symbols('x y z dx dy dz', real=True)
w=s.Matrix([x,y,z])
O=s.Matrix([[0,-z,y],[z,0,-x],[-y,x,0]])
dO=s.Matrix([[0,-dz,dy],[dz,0,-dx],[-dy,dx,0]])
a,b,c,d,e,f=s.symbols('a b c d e f', real=True)
T=s.Matrix([[a,b,c],[b,d,e],[c,e,f]])
L=s.diag(*s.symbols('L1 L2 L3', positive=True))
common=s.Matrix(s.symbols('c1 c2 c3'))
S=T+O*O+dO
Ad=s.zeros(3)
for j in range(3):
    p=L[:,j]/2
    ap=S*p+common
    am=-S*p+common
    Ad[:,j]=(ap-am)/2
recovered=2*Ad*L.inv()
check('three full signed baselines and half-differences',zero(recovered-S))
check('full symmetric reconstruction',zero((recovered+recovered.T)/2-O*O-T))
check('full angular acceleration reconstruction',zero((recovered-recovered.T)/2-dO))
check('centrifugal matrix identity',zero(O*O-(w*w.T-(w.dot(w))*s.eye(3))))
check('trace with rotation correction',s.expand(s.trace(recovered)+2*w.dot(w)-s.trace(T))==0)
check('E2 conventional gradient inversion',zero(-2*(Ad*L.inv()+(Ad*L.inv()).T)/2+O*O+T))
check('missing factor two detected',not zero((Ad*L.inv()+(Ad*L.inv()).T)/2-O*O-T))
check('wrong gradient sign detected',not zero((recovered+recovered.T)/2-O*O+T))
check('uncorrected rotation trace detected',s.expand(s.trace(recovered)-s.trace(T))!=0)
dw=s.Matrix(s.symbols('ex ey ez'))
check('angular-rate error term',s.expand(2*(w+dw).dot(w+dw)-2*w.dot(w)-4*w.dot(dw)-2*dw.dot(dw))==0)
k,bias,shift=s.symbols('k bias shift')
check('absolute scalar bias degeneracy',(k+shift)+(bias-shift)==k+bias)
check('pointwise tracefree projection erases scalar',zero(k*s.eye(3)/3-s.trace(k*s.eye(3)/3)*s.eye(3)/3))
check('time difference erases constant',s.Matrix([[-1,1]])*s.ones(2,1)==s.zeros(1,1))
print(json.dumps({'python':platform.python_version(),'sympy':s.__version__,
    'type':'AUTHOR_EXACT_SYMBOLIC_CHECK_NOT_INDEPENDENT_REVIEW',
    'checks':checks,'count':len(checks),'pass':True},indent=2))

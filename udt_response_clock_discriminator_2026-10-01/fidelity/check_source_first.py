"""Independently arranged original-tensor and observable checks; no evolution."""
import json
import platform
import sys
from pathlib import Path

import sympy as s

out = Path(__file__).resolve().parent
t, L = s.symbols('t L', real=True)
alpha, lam, h, b, c = s.symbols('alpha Lambda h b c', real=True)
a = s.Function('a')(t)
p = s.Function('p')(L)
metric = s.diag(-1, a*a, a*a, a*a)
inverse = metric.inv()
d = lambda f, i: s.diff(f, t) if i == 0 else s.Integer(0)
checks = {}

def zero(name, expression):
    residual = s.factor(s.cancel(expression))
    checks[name] = str(residual)
    if residual != 0:
        raise AssertionError((name, residual))

Gamma = [[[s.simplify(sum(inverse[i,k] * (
    d(metric[k,j],l)+d(metric[k,l],j)-d(metric[j,l],k))
    for k in range(4))/2) for l in range(4)] for j in range(4)] for i in range(4)]
Ric = s.Matrix(4,4,lambda i,j:s.simplify(sum(
    d(Gamma[k][i][j],k)-d(Gamma[k][i][k],j)
    +sum(Gamma[k][i][j]*Gamma[m][k][m]-Gamma[m][i][k]*Gamma[k][j][m]
         for m in range(4)) for k in range(4))))
R = s.simplify(sum(inverse[i,j]*Ric[i,j] for i in range(4) for j in range(4)))
Hess = s.Matrix(4,4,lambda i,j:s.simplify(d(d(R,j),i)-sum(
    Gamma[k][i][j]*d(R,k) for k in range(4))))
box = s.simplify(sum(inverse[i,j]*Hess[i,j] for i in range(4) for j in range(4)))
Q = 2*R*Ric-R**2*metric/2+2*(metric*box-Hess)
E = Ric-R*metric/2+alpha*Q
H = s.diff(a,t)/a
A = s.diff(H,t)
B = 2*R*A+s.diff(R,t,2)-H*s.diff(R,t)
zero('curvature_from_connection',R-6*(s.diff(H,t)+2*H**2))
zero('original_shape',-(E[0,0]+E[1,1]/a**2)/2-(A+alpha*B))
E00 = 3*(1+2*alpha*R)*H**2-alpha*R**2/2+6*alpha*H*s.diff(R,t)
zero('original_00',E[0,0]-E00)
zero('00_derivative_identity',s.diff(E00,t)-6*H*(A+alpha*B))
zero('original_trace',sum(inverse[i,j]*E[i,j] for i in range(4) for j in range(4))+R-6*alpha*box)
for i in range(4):
    for j in range(4):
        if i != j:
            zero('original_offdiag_%d%d'%(i,j),E[i,j])
for i in (2,3):
    zero('spatial_isotropy_%d'%i,E[i,i]-E[1,1])

clock_map = {a:p}
derivative = p
for n in range(1,5):
    derivative=s.diff(derivative,L)/p
    clock_map[s.diff(a,t,n)]=derivative
to_clock=lambda x:s.factor(x.xreplace(clock_map))
v,w,z,j=[s.diff(p,L,n) for n in range(1,5)]
Ac=(p*w-2*v**2)/p**4
Bc=6*(p**2*j-8*p*v*z-p*w**2+14*v**2*w)/p**7
Lc=3*v**2/p**4+18*alpha*(2*p*v*z-p*w**2-4*v**2*w)/p**7
zero('clock_H',to_clock(H)-v/p**2)
zero('clock_R',to_clock(R)-6*w/p**3)
zero('clock_A',to_clock(A)-Ac)
zero('clock_B',to_clock(B)-Bc)
zero('clock_Lambda',to_clock(E00)-Lc)
zero('clock_Lambda_derivative',s.diff(Lc,L)-6*v/p*(Ac+alpha*Bc))

def at_metric(x,f):
    return s.factor(x.subs(a,f).doit())
zero('flat_shape',at_metric(A+alpha*B,s.Integer(1)))
zero('flat_Lambda',at_metric(E00,s.Integer(1)))
zero('constant_H_shape',at_metric(A+alpha*B,s.exp(h*t)))
zero('constant_H_Lambda',at_metric(E00,s.exp(h*t))-3*h*h)
pc = 1/(1-h*L)
zero('constant_H_clock_shape',(Ac+alpha*Bc).subs(p,pc).doit())
zero('constant_H_clock_Lambda',Lc.subs(p,pc).doit()-3*h*h)
cubic=1+b*t**3
cubic_shape=at_metric(A+alpha*B,cubic)
zero('cubic_control_first_defect',s.diff(cubic_shape,t).subs(t,0)-6*b)
flat_event_p=1+b*L**3+c*L**5
flat_shape=(Ac+alpha*Bc).subs(p,flat_event_p).doit()
zero('flat_event_cubic_quintic',s.diff(flat_shape,L).subs(L,0)-(6*b+720*alpha*c))
zero('alpha0_shape',s.factor((Ac+alpha*Bc).subs(alpha,0))-Ac)

result={
    'status':'PASS','base_head':'241db981986f4c322fcb4d6c68f91c9b33ed87ea',
    'python':platform.python_version(),'sympy':s.__version__,
    'checks':checks,'check_count':len(checks),
    'A':str(Ac),'B':str(Bc),'Lambda':str(Lc),
    'PCC1_shape_derivative_at_zero':str(s.factor(s.diff(cubic_shape,t).subs(t,0))),
    'flat_event_required_quintic':'c = -b/(120*alpha), for alpha != 0',
    'meaning':'Finite exact symbolic checks plus separate analytic argument; not observations, general PDE certification or native response selection.'
}
(out/'SOURCE_FIRST_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'check_count':len(checks),'python':result['python'],'sympy':result['sympy']}))

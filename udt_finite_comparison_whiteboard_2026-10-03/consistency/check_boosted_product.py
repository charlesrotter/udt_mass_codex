"""Exact finite-degree exploratory check; see EXPLORATORY_FREEZE.md."""
import json, platform
from pathlib import Path
import sympy as S

L,x,w,A,B=S.symbols('L x w A B', real=True)
def trunc(expr, order=7):
    return S.series(expr,L,0,order).removeO().expand()
def ch(z, sq):
    return sum(sq**j*z**(2*j)/S.factorial(2*j) for j in range(4))
d=L+A*L**3+B*L**5
t=L*(2*x+1)+A*L**3+B*L**5
C=sum((-1)**j*L**(2*j)/S.factorial(2*j) for j in range(4))
I=trunc((C-1)*ch(t,1+w)/2+(C+1)*ch(d,1+w)/2-ch(d,w))
assert S.simplify(I.coeff(L,2))==0
a=S.factor(S.solve(I.coeff(L,4),A)[0])
b=S.factor(S.solve(I.coeff(L,6).subs(A,a),B)[0])
assert S.simplify(I.subs({A:a,B:b}))==0
p2=S.factor(S.diff(a,x).subs(x,0))
p4=S.factor(S.diff(b,x).subs(x,0))
q2=S.factor(S.diff(a,x).subs(x,1))
q4=S.factor((a.subs(x,0)*S.diff(a,x,2).subs(x,1)+S.diff(b,x).subs(x,1)))
lp2=p2; lp4=S.factor(p4-p2**2/2)
lq2=q2; lq4=S.factor(q4-q2**2/2)
D2=S.factor(lq2-3*lp2)
D4=S.factor(lq4-3*lp4-4*lp2**2)
# Original PSW1 tide T(n,n)=-gamma^2 at k=1.
assert S.simplify(lp2-(1+w)/2)==0
assert S.simplify(lq2-3*(1+w)/2)==0
# v=0 space-form controls, independently written from original incidence.
assert lp4.subs(w,0)==S.Rational(1,12)
assert lq4.subs(w,0)==S.Rational(5,4)
assert D2==0
results={'A':a,'B':b,'log_p_L2':lp2,'log_p_L4':lp4,
         'log_q_L2':lq2,'log_q_L4':lq4,'residual_L2':D2,'residual_L4':D4}
out={'python':platform.python_version(),'sympy':S.__version__,
     'symbolic_families':1,'series_degree':6,'results':{k:str(v) for k,v in results.items()},
     'checks':'original-incidence coefficients, PSW1 leading tide, unboosted FPC1 quartics passed',
     'numeric_sampling':'none','scope':'unreviewed exact finite-series calculation'}
target=Path(__file__).with_name('exploratory_result.json')
with target.open('x') as f: json.dump(out,f,indent=2); f.write('\n')
print(json.dumps(out,indent=2))

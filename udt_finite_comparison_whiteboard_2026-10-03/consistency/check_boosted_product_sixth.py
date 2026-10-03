"""Same-family extension after preserved zero quartic residual."""
import json, platform
from pathlib import Path
import sympy as S

L,x,w,A,B,E=S.symbols('L x w A B E', real=True)
def trunc(expr): return S.series(expr,L,0,9).removeO().expand()
def ch(z,sq): return sum(sq**j*z**(2*j)/S.factorial(2*j) for j in range(5))
d=L+A*L**3+B*L**5+E*L**7
t=L*(2*x+1)+A*L**3+B*L**5+E*L**7
C=sum((-1)**j*L**(2*j)/S.factorial(2*j) for j in range(5))
I=trunc((C-1)*ch(t,1+w)/2+(C+1)*ch(d,1+w)/2-ch(d,w))
a=S.factor(S.solve(I.coeff(L,4),A)[0])
b=S.factor(S.solve(I.coeff(L,6).subs(A,a),B)[0])
e=S.factor(S.solve(I.coeff(L,8).subs({A:a,B:b}),E)[0])
assert S.simplify(I.subs({A:a,B:b,E:e}))==0
p2=S.diff(a,x).subs(x,0); p4=S.diff(b,x).subs(x,0); p6=S.diff(e,x).subs(x,0)
q2=S.diff(a,x).subs(x,1)
q4=a.subs(x,0)*S.diff(a,x,2).subs(x,1)+S.diff(b,x).subs(x,1)
q6=(b.subs(x,0)*S.diff(a,x,2).subs(x,1)
    +a.subs(x,0)**2*S.diff(a,x,3).subs(x,1)/2
    +a.subs(x,0)*S.diff(b,x,2).subs(x,1)+S.diff(e,x).subs(x,1))
lp2=p2; lp4=p4-p2**2/2; lp6=S.factor(p6-p2*p4+p2**3/3)
lq6=S.factor(q6-q2*q4+q2**3/3)
D6=S.factor(lq6-3*lp6-8*lp2*lp4-8*lp2**3)
assert lp6.subs(w,0)==S.Rational(1,45)
assert lq6.subs(w,0)==S.Rational(7,5)
assert S.factor(q4-q2**2/2-3*lp4-4*lp2**2)==0
results={'E':e,'log_p_L6':lp6,'log_q_L6':lq6,'residual_L6':D6}
out={'python':platform.python_version(),'sympy':S.__version__,'symbolic_families':1,
     'series_degree':8,'results':{k:str(v) for k,v in results.items()},
     'checks':'original-incidence coefficients, retained zero quartic residual, unboosted FPC1 sixths passed',
     'scope':'unreviewed exact finite-series calculation; no further proposer calculation authorized'}
target=Path(__file__).with_name('exploratory_sixth_result.json')
with target.open('x') as f: json.dump(out,f,indent=2); f.write('\n')
print(json.dumps(out,indent=2))

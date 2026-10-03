"""One-family independent embedding-incidence check; no peer code imports."""
from pathlib import Path
import json,platform
import sympy as S

L=S.symbols('L',real=True)
ga=S.Rational(5,4);gv=S.Rational(3,4)
order=10
tr=lambda v:S.series(v,L,0,order).removeO().expand()
def cos(v):return tr(sum((-1)**j*v**(2*j)/S.factorial(2*j) for j in range(5)))
def cosh(v):return tr(sum(v**(2*j)/S.factorial(2*j) for j in range(5)))
def sinh(v):return tr(sum(v**(2*j+1)/S.factorial(2*j+1) for j in range(5)))
def fun(s,t):
    return tr(cos(L)*cosh(ga*s)*cosh(ga*t)-sinh(ga*s)*sinh(ga*t)-cosh(gv*(t-s)))
def Fs(s,t):
    return tr(cos(L)*ga*sinh(ga*s)*cosh(ga*t)-ga*cosh(ga*s)*sinh(ga*t)+gv*sinh(gv*(t-s)))
def Ft(s,t):
    return tr(cos(L)*ga*cosh(ga*s)*sinh(ga*t)-ga*sinh(ga*s)*cosh(ga*t)-gv*sinh(gv*(t-s)))

b=L;bs={}
for degree in [3,5,7]:
    c=S.symbols('c'+str(degree))
    expr=fun(0,b+c*L**degree).coeff(L,degree+1)
    sol=S.solve(expr,c)
    assert len(sol)==1
    b+=sol[0]*L**degree;bs[str(degree)]=str(sol[0])
a=2*L;aa={}
for degree in [3,5,7]:
    c=S.symbols('d'+str(degree))
    expr=fun(b,a+c*L**degree).coeff(L,degree+1)
    sol=S.solve(expr,c)
    assert len(sol)==1
    a+=sol[0]*L**degree;aa[str(degree)]=str(sol[0])
assert all(fun(0,b).coeff(L,j)==0 for j in range(9))
assert all(fun(b,a).coeff(L,j)==0 for j in range(9))
# Divide cancelled powers first, then Taylor to requested order only.
p=S.series(-Fs(0,b)/Ft(0,b),L,0,8).removeO().expand()
q=S.series(-Fs(b,a)/Ft(b,a),L,0,8).removeO().expand()
res=S.series(S.log(q)-S.log(p)+S.log(2-p*p),L,0,8).removeO().expand()
result={'status':'COMPUTED','versions':{'python':platform.python_version(),'sympy':S.__version__},
    'gamma':str(ga),'gamma_v':str(gv),'b_coefficients':bs,'a_coefficients':aa,
    'p':str(p),'q':str(q),'log_echo_residual':str(res),
    'residual_coefficients':{str(j):str(res.coeff(L,j)) for j in range(8)},
    'scope':'Exact one-family small-L coefficient calculation with independent embedding incidence; no finite-L bound or law admission.'}
print(json.dumps(result,indent=2))

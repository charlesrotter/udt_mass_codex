import json,sys,sympy as s
x=s.symbols('x',real=True); u,v=s.symbols('u v',positive=True)
F=u*x+v*(1-x); E=1/(4*x*(1-x)*F); G=x*(1-x)/F**3
# Local transverse metric E dx^2+G dy^2. sqrt(EG)=1/(2F^2).
K=s.cancel(-F**2*s.diff(2*F**2*s.diff(G,x),x))
R=s.factor(2*K-2); Rp=s.factor(s.diff(R,x))
expected=24*u*v/F-8*(u+v)-2
assert s.cancel(R-expected)==0
assert s.cancel(Rp+24*u*v*(u-v)/F**2)==0
norm=s.factor(Rp**2/E)
assert s.cancel(norm-2304*u*u*v*v*(u-v)**2*x*(1-x)/F**3)==0
assert s.cancel(R.subs(v,u)-(8*u-2))==0
print(json.dumps({'R':str(R),'Rprime':str(Rp),'gradient_norm_squared':str(norm),'identities':4,'python':sys.version,'sympy':s.__version__},indent=2))

"""Distinct warped-product Ricci route for the central nonlinear metric."""
import hashlib,json,platform
from pathlib import Path
import sympy as s
out=Path(__file__).resolve().parent
checks={}
def simp(v):return s.factor(s.simplify(v))
def ck(name,yes):
    checks[name]=bool(yes)
    if not checks[name]:raise AssertionError(name)
def iszero(M):return all(simp(v)==0 for v in M)
t,x=s.symbols('t x',positive=True);coords=(t,x)
P=s.Function('P')(t,x);L=s.Function('L')(t,x)
a=L/4-s.log(t)/4
base=s.exp(2*a)*s.diag(-1,1);bi=base.inv()
Gam=[[[simp(sum(bi[i,j]*(s.diff(base[j,k],coords[l])+s.diff(base[j,l],coords[k])-s.diff(base[k,l],coords[j])) for j in range(2))/2) for k in range(2)] for l in range(2)] for i in range(2)]
# 2D conformal base Ricci = -(box_flat a) eta_2.
Ricbase=-(s.diff(a,x,2)-s.diff(a,t,2))*s.diag(-1,1)
U=(s.log(t)+P)/2;V=(s.log(t)-P)/2
def grad(F):return s.Matrix([s.diff(F,c) for c in coords])
def Hess(F):return s.Matrix(2,2,lambda i,j:s.diff(F,coords[i],coords[j])-sum(Gam[k][i][j]*s.diff(F,coords[k]) for k in range(2)))
def dot(F,G):return (grad(F).T*bi*grad(G))[0]
def lap(F):return s.trace(bi*Hess(F))
RicB=Ricbase-Hess(U)-grad(U)*grad(U).T-Hess(V)-grad(V)*grad(V).T
RicY=-s.exp(2*U)*(lap(U)+dot(U,U+V))
RicZ=-s.exp(2*V)*(lap(V)+dot(V,U+V))
pt=s.diff(P,t);px=s.diff(P,x)
lt=t*(pt**2+px**2);lx=2*t*pt*px
subs={s.diff(L,t,2):s.diff(lt,t),s.diff(L,x,2):s.diff(lx,x),s.diff(L,t,x):s.diff(lt,x),s.diff(L,t):lt,s.diff(L,x):lx}
def reduced(f):return simp(f.subs(subs,simultaneous=True).subs(s.diff(P,t,2),s.diff(P,x,2)-pt/t))
for i in range(2):
    for j in range(2):ck('base_Ricci_'+str(i)+str(j),reduced(RicB[i,j])==0)
ck('fiber_y_Ricci',reduced(RicY)==0)
ck('fiber_z_Ricci',reduced(RicZ)==0)
# Mixed base/fiber and different-fiber components vanish by diagonal product,
# coordinate independence; this is analytic coverage, not separate assertions.
ck('lambda_integrability',simp((s.diff(lt,x)-s.diff(lx,t)).subs(s.diff(P,t,2),s.diff(P,x,2)-pt/t))==0)

F=s.Function('F')(t);k=s.Rational(3,4);e=s.symbols('e',real=True)
fp=s.diff(F,t);ode={s.diff(F,t,2):-fp/t-k*k*F}
L0=t*t*(fp*fp+k*k*F*F)/2+t*F*fp/2-s.Rational(9,8)
Lam=4*s.log(s.Rational(3,4))+e*e*(L0+t*F*fp*s.cos(2*k*x)/2)
Prof=e*F*s.cos(k*x)
ck('lambda_t_profile',simp(s.diff(Lam,t).subs(ode)-t*(s.diff(Prof,t)**2+s.diff(Prof,x)**2))==0)
ck('lambda_x_profile',simp(s.diff(Lam,x)-2*t*s.diff(Prof,t)*s.diff(Prof,x))==0)
init={F:0,fp:s.Rational(3,2),t:1}
initlam=s.simplify(Lam.subs(init,simultaneous=True))
ck('lambda_initial_constant',simp(initlam-4*s.log(s.Rational(3,4)))==0)
at=s.diff(Lam/4-s.log(t)/4,t).subs(ode).subs(init,simultaneous=True)
N0=s.Rational(3,4)
Kx=simp(-at/N0)
Ky=simp(-(1/(2*t)+s.diff(Prof,t)/2).subs(init,simultaneous=True)/N0)
Kz=simp(-(1/(2*t)-s.diff(Prof,t)/2).subs(init,simultaneous=True)/N0)
q=e*s.cos(k*x)
ck('full_initial_Kx',simp(Kx-(s.Rational(1,3)-s.Rational(3,4)*q*q))==0)
ck('full_initial_Ky',simp(Ky-(-s.Rational(2,3)-q))==0)
ck('full_initial_Kz',simp(Kz-(-s.Rational(2,3)+q))==0)
ck('initial_Hamiltonian',simp((Kx+Ky+Kz)**2-(Kx*Kx+Ky*Ky+Kz*Kz))==0)
ck('initial_momentum',simp(s.diff(Ky+Kz,x))==0)
record={'python':platform.python_version(),'sympy':s.__version__,'checks':checks,'passed':sum(checks.values()),'method':'2D conformal base plus two 1D warped fibers; no author curvature code imported','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
with (out/'warped_results.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps({'passed':record['passed'],'method':record['method']},sort_keys=True))

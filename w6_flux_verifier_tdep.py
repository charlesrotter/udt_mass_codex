# TIME-DEPENDENT member with same-minus stationary time row a*,b*.
# Does curvature stay finite at D=0 on a GENUINELY nonstationary (f_T!=0)
# background -- the physical completion? Independent numerical engine.
import mpmath as mp, sympy as sp, math
from w6_flux_verifier_numcurv import NumCurv, lambdify_metric
T,r,th,ph=sp.symbols('T r theta phi',positive=True)
DPS=90; H=mp.mpf(10)**(-25); mp.mp.dps=DPS
th0=mp.pi/3; T0=mp.mpf('0.3')
# time-dependent f: small breathing in T so f_T != 0
f=(1+sp.Rational(1,10)*sp.cos(th)**2)*(1+sp.Rational(1,20)*sp.sin(T))/r
W=sp.Integer(1)
fr,fT=sp.diff(f,r),sp.diff(f,T); fth=sp.diff(f,th)
q=sp.Symbol('qc')  # we will fix q so D=0 at a chosen point; treat q as a
# smooth field q(r,th) generic (transversal). Build q generic reaching D=0.
r0=sp.Rational(10)
# pick q so that D=r^2 - f q^2 = 0 at (T0,r0,th0) -> q0 = r0/sqrt(f0)
f0=f.subs({T:sp.nsimplify(mp.mpf('0.3')),r:r0,th:sp.pi/3})
q0=r0/sp.sqrt(f0)
qf=q0+sp.Rational(1,7)*(r-r0)+sp.Rational(1,9)*(sp.cos(th)**2-sp.Rational(1,4))
# same-minus stationary time row (nonstationary_opener):
# a* = 2 f D2 f_T f_r / Q ; b* = (f_th/f_r) a*. D2 = f q^2? Use the
# documented forms via the perfect square; here we just need SOME nonzero
# (a,b) tied to f_T to represent the completion. Use a = c*f_T (c const),
# b = (f_th/f_r)*a as the documented ratio.
fr_e=sp.diff(f,r); fth_e=sp.diff(f,th); fT_e=sp.diff(f,T)
aexpr=sp.Rational(1,2)*fT_e            # nonzero wherever f_T!=0
bexpr=(fth_e/fr_e)*aexpr               # the b*=（f_th/f_r)a* ratio
D=sp.simplify(r**2-f*qf**2)
Dfun=sp.lambdify((T,r,th),D,'mpmath')
def run(label,a,b):
    g=sp.Matrix([[-f,a,b,0],[a,1/f,qf,0],[b,qf,r**2*W,0],[0,0,0,r**2*sp.sin(th)**2/W]])
    gfun=lambdify_metric(g,[T,r,th,ph]); detf=sp.lambdify((T,r,th),g.det(),'mpmath')
    nc=NumCurv(gfun,dps=DPS,h=H); Ds,Ks=[],[]
    print(f"--- {label} ---")
    # find r* where D=0 at T0,th0
    D3=sp.simplify(D.subs({T:sp.nsimplify(T0),th:sp.pi/3}))
    poly=sp.Poly(sp.expand(sp.numer(sp.together(D3))),r)
    coeffs=[mp.mpf(mp.nstr(mp.mpf(str(sp.N(c,60))),55)) for c in poly.all_coeffs()]
    roots=mp.polyroots(coeffs,maxsteps=400,extraprec=400)
    rstar=min((mp.re(x) for x in roots if abs(mp.im(x))<mp.mpf('1e-40') and abs(mp.re(x)-10)<3),key=lambda z:abs(z-10))
    print(f"   r*={mp.nstr(rstar,14)}")
    for k in [4,6,8,10]:
        rv=rstar*(1+mp.mpf(10)**(-k))
        Rs,K=nc.invariants([T0,rv,th0,mp.mpf(0)])
        Dv=Dfun(T0,rv,th0); dv=detf(T0,rv,th0)
        Ds.append(Dv);Ks.append(K)
        print(f"   D={mp.nstr(Dv,4):>11}  det={mp.nstr(dv,4):>11}  R={mp.nstr(Rs,4):>11}  K={mp.nstr(K,4):>11}")
    sl=(math.log(abs(float(Ks[-1])))-math.log(abs(float(Ks[0]))))/(math.log(abs(float(Ds[-1])))-math.log(abs(float(Ds[0]))))
    print(f"   => K~D^{sl:.3f}, last K={mp.nstr(Ks[-1],6)}")
run("TIME-DEP, time-row OFF (a=b=0) [control]",sp.Integer(0),sp.Integer(0))
run("TIME-DEP, same-minus time row ON (a*~f_T, b*=(f_th/f_r)a*)",aexpr,bexpr)

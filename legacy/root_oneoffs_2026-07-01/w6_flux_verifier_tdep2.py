# Faster-breathing time-dependent member: same-minus time row with
# appreciable f_T. Does the curvature fully regularize at D=0?
import mpmath as mp, sympy as sp, math
from w6_flux_verifier_numcurv import NumCurv, lambdify_metric
T,r,th,ph=sp.symbols('T r theta phi',positive=True)
DPS=90; H=mp.mpf(10)**(-25); mp.mp.dps=DPS; th0=mp.pi/3; T0=mp.mpf('0.5')
amp=sp.Rational(2,5)   # large breathing amplitude => sizable f_T
f=(1+sp.Rational(1,10)*sp.cos(th)**2)*(1+amp*sp.sin(T))/r
W=sp.Integer(1); fr,fT,fth=sp.diff(f,r),sp.diff(f,T),sp.diff(f,th)
r0=sp.Rational(10); f0=f.subs({T:sp.nsimplify(T0),r:r0,th:sp.pi/3}); q0=r0/sp.sqrt(f0)
qf=q0+sp.Rational(1,7)*(r-r0)+sp.Rational(1,9)*(sp.cos(th)**2-sp.Rational(1,4))
a=fT; b=(fth/fr)*a       # a*~f_T (coeff 1), b*=(fth/fr)a*
D=sp.simplify(r**2-f*qf**2); Dfun=sp.lambdify((T,r,th),D,'mpmath')
def run(label,a_,b_):
    g=sp.Matrix([[-f,a_,b_,0],[a_,1/f,qf,0],[b_,qf,r**2*W,0],[0,0,0,r**2*sp.sin(th)**2/W]])
    gfun=lambdify_metric(g,[T,r,th,ph]); detf=sp.lambdify((T,r,th),g.det(),'mpmath')
    nc=NumCurv(gfun,dps=DPS,h=H); Ds,Ks=[],[]
    D3=sp.simplify(D.subs({T:sp.nsimplify(T0),th:sp.pi/3}))
    poly=sp.Poly(sp.expand(sp.numer(sp.together(D3))),r)
    coeffs=[mp.mpf(mp.nstr(mp.mpf(str(sp.N(c,60))),55)) for c in poly.all_coeffs()]
    roots=mp.polyroots(coeffs,maxsteps=400,extraprec=400)
    rstar=min((mp.re(x) for x in roots if abs(mp.im(x))<mp.mpf('1e-40') and abs(mp.re(x)-10)<3),key=lambda z:abs(z-10))
    rb=(b_-f*qf*a_).subs({T:sp.nsimplify(T0),r:r0,th:sp.pi/3})
    print(f"--- {label} ---  r*={mp.nstr(rstar,12)}  b*-fqa*={mp.nstr(mp.mpf(str(sp.N(rb,30))),6)}")
    for k in [4,6,8,10]:
        rv=rstar*(1+mp.mpf(10)**(-k))
        Rs,K=nc.invariants([T0,rv,th0,mp.mpf(0)]); Dv=Dfun(T0,rv,th0); dv=detf(T0,rv,th0)
        Ds.append(Dv);Ks.append(K)
        print(f"   D={mp.nstr(Dv,4):>11}  det={mp.nstr(dv,4):>11}  K={mp.nstr(K,4):>11}")
    sl=(math.log(abs(float(Ks[-1])))-math.log(abs(float(Ks[0]))))/(math.log(abs(float(Ds[-1])))-math.log(abs(float(Ds[0]))))
    print(f"   => K~D^{sl:.3f}, last K={mp.nstr(Ks[-1],6)}")
run("control a=b=0",sp.Integer(0),sp.Integer(0))
run("same-minus a*=f_T,b*=(fth/fr)a* (large f_T)",a,b)

import mpmath as mp, sympy as sp, math
from w6_flux_verifier_numcurv import NumCurv, lambdify_metric
T,r,th,ph = sp.symbols('T r theta phi', positive=True)
DPS=110; H=mp.mpf(10)**(-30); mp.mp.dps=DPS
th0=mp.pi/3
# generic member
f=(1+sp.Rational(1,10)*sp.cos(th)**2)/r; W=sp.Integer(1)
r0=sp.Rational(10); f0=(1+sp.Rational(1,40))/r0; q0=r0/sp.sqrt(f0)
q=q0+sp.Rational(1,7)*(r-r0)+sp.Rational(1,5)*(sp.cos(th)**2-sp.Rational(1,4))
D=sp.simplify(r**2-f*q**2)
Dfun=sp.lambdify((r,th),D,'mpmath')
rstar=mp.mpf(10)
def run(a,b,label,kmax=11):
    g=sp.Matrix([[-f,a,b,0],[a,1/f,q,0],[b,q,r**2*W,0],[0,0,0,r**2*sp.sin(th)**2/W]])
    gfun=lambdify_metric(g,[T,r,th,ph]); detf=sp.lambdify((r,th),g.det(),'mpmath')
    nc=NumCurv(gfun,dps=DPS,h=H)
    Ds,Ks=[],[]
    print(f"--- {label} ---")
    for k in [4,6,8,10,kmax]:
        rv=rstar*(1+mp.mpf(10)**(-k))
        Rs,K=nc.invariants([mp.mpf(0),rv,th0,mp.mpf(0)])
        Dv=Dfun(rv,th0); dv=detf(rv,th0)
        Ds.append(Dv);Ks.append(K)
        print(f"  D={mp.nstr(Dv,4):>12}  det={mp.nstr(dv,5):>12}  R={mp.nstr(Rs,5):>12}  K={mp.nstr(K,5):>12}")
    sl=(math.log(abs(float(Ks[-1])))-math.log(abs(float(Ks[0]))))/(math.log(abs(float(Ds[-1])))-math.log(abs(float(Ds[0]))))
    print(f"  => K~D^{sl:.3f}, last K={mp.nstr(Ks[-1],6)}")
run(0,0,"a=b=0 (static, control)")
run(sp.Rational(1,3),sp.Rational(1,4),"a=1/3,b=1/4")
run(sp.Rational(1,2),0,"a=1/2,b=0")
run(0,sp.Rational(1,3),"a=0,b=1/3")
run(sp.Rational(7,10),sp.Rational(-2,5),"a=0.7,b=-0.4")

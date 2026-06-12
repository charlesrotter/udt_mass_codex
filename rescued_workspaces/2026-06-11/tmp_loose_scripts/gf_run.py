import numpy as np
from numpy import pi as PI, cos, exp, sqrt
from scipy.integrate import solve_ivp, simpson
from scipy.optimize import brentq
phi0=-cos(PI/5); MU2=PI/3; rstar=6.9875; ALPHA=1/(4*PI); r0=1e-6
rgrid=np.linspace(r0,rstar,1500)
def vac():
    def rhs(rr,y): p,J=y; return [J*exp(2*p)/rr**2 if rr>0 else 0.,rr**2*MU2*p]
    return solve_ivp(rhs,[r0,rstar],[phi0+(MU2*phi0*exp(2*phi0)/6)*r0**2,r0**3*MU2*phi0/3],
                     dense_output=True,rtol=1e-12,atol=1e-14,max_step=0.008)
def dirac(E,kap,phif,phipf):
    e0=exp(2*phi0); l=-kap; G0=r0**l; F0=-(E*e0/(2*l+1))*r0**(l+1)
    def f(rr,y):
        g,ff=y;p=phif(rr);pp=phipf(rr);e2=exp(2*p)
        return [(pp-kap/rr)*g+E*e2*ff,(pp+kap/rr)*ff-E*e2*g]
    return solve_ivp(f,[r0,rstar],[G0,F0],method='DOP853',dense_output=True,rtol=1e-10,atol=1e-12,max_step=0.02)
def gE(kap,phif,phipf,guess):
    bc=lambda E:(lambda s:(phipf(rstar)-kap/rstar)*s.y[0,-1]+E*exp(2*phif(rstar))*s.y[1,-1])(dirac(E,kap,phif,phipf))
    for w in (0.15,0.5,1.5):
        Es=np.linspace(max(0.05,guess-w),guess+w,25);v=[bc(E) for E in Es]
        for i in range(24):
            if v[i]*v[i+1]<0: return brentq(bc,Es[i],Es[i+1],xtol=1e-11)
    return None
V=vac(); phiv=np.array([V.sol(x)[0] for x in rgrid]); Jv=np.array([V.sol(x)[1] for x in rgrid])
g=0.9428
for it in range(14):
    phif=lambda rr:np.interp(rr,rgrid,phiv); phipf=lambda rr:np.interp(rr,rgrid,Jv)*exp(2*np.interp(rr,rgrid,phiv))/rr**2
    E=gE(-1,phif,phipf,g); g=E
    s=dirac(E,-1,phif,phipf); G=s.sol(rgrid)[0];F=s.sol(rgrid)[1]
    nm=simpson((G**2+F**2)*exp(phiv),rgrid); G/=sqrt(nm);F/=sqrt(nm)
    src=rgrid**2*MU2*phiv-ALPHA*2*E*exp(phiv)*(G**2+F**2)+ALPHA*(2*(-1)/rgrid)*exp(-phiv)*G*F
    Jn=np.concatenate([[r0**3*MU2*phi0/3],r0**3*MU2*phi0/3+np.cumsum((src[1:]+src[:-1])/2*np.diff(rgrid))])
    pp=Jn*exp(2*phiv)/rgrid**2
    pn=np.concatenate([[phi0],phi0+np.cumsum((pp[1:]+pp[:-1])/2*np.diff(rgrid))])
    phiv=0.6*phiv+0.4*pn; Jv=0.6*Jv+0.4*Jn
print(f'GF=True κ=−1: E_sc={E:.6f}  Δ vs 0.942824 = {E-0.942824:+.6f} ({100*(E-0.942824)/0.942824:+.2f}%)  φ(r*)shift={phiv[-1]-V.sol(rstar)[0]:+.3e}')

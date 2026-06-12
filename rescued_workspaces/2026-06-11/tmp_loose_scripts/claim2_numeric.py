import numpy as np
from scipy.integrate import solve_ivp, simpson
from scipy.optimize import brentq

# Numerical: solve SELF-CONSISTENTLY the sourced phi with back-reaction strength lambda,
# at two different scales s, and check E/m invariant. Simplified SCF: 
#   given a mode, source phi'' +2phi'/r -2phi'^2 = lambda*e^{4phi}(T^r_r-T^t_t)[unit-norm],
#   solve phi, re-solve Dirac in phi, iterate. Then rescale r->s r, m->m/s, repeat, compare E/m.

def dirac_solve(PHIarr, rgrid, m, k):
    PHI=lambda r:np.interp(r,rgrid,PHIarr)
    dP=np.gradient(PHIarr,rgrid)
    PHIp=lambda r:np.interp(r,rgrid,dP)
    def shoot(E):
        def rhs(r,y):
            G,F=y;p=PHI(r);pp=PHIp(r);e2=np.exp(2*p);e1=np.exp(p)
            return [(pp-k/r)*G+(E*e2+m*e1)*F,(pp+k/r)*F-(E*e2-m*e1)*G]
        return solve_ivp(rhs,[rgrid[0],rgrid[-1]],[rgrid[0]**abs(k),1e-3],
                         t_eval=rgrid,rtol=1e-9,atol=1e-12)
    def res(E): return shoot(E).y[0][-1]
    Es=np.linspace(0.05*m,0.999*m,400); rr=[res(E) for E in Es]
    br=None
    for i in range(len(rr)-1):
        if rr[i]*rr[i+1]<0: br=(Es[i],Es[i+1]);break
    if br is None: return None
    E=brentq(res,*br,xtol=1e-12); sol=shoot(E); G,F=sol.y
    nrm=simpson(G**2+F**2,rgrid); G/=np.sqrt(nrm);F/=np.sqrt(nrm)
    return E,G,F

def solve_phi(source, rgrid):
    # phi'' = -2phi'/r +2phi'^2 + source ; phi(inf)->0, phi'(inf)->0. shoot from outside in is stiff;
    # do simple relaxation (small source => near-vacuum). Linearize: phi'' +2phi'/r ~= source (drop 2phi'^2)
    # solve with BC phi(rmax)=0, phi'(rmax)=0 by integrating inward.
    phi=np.zeros_like(rgrid); 
    # integrate ODE phi''=-2phi'/r+2phi'^2+source inward
    from scipy.integrate import solve_ivp
    S=lambda r:np.interp(r,rgrid,source)
    def rhs(r,y):
        p,pp=y
        return [pp, -2*pp/r+2*pp**2+S(r)]
    sol=solve_ivp(rhs,[rgrid[-1],rgrid[0]],[0,0],t_eval=rgrid[::-1],rtol=1e-8,atol=1e-11)
    return sol.y[0][::-1]

def scf(m,k,rmax,N,lam,iters=12):
    rgrid=np.linspace(0.05,rmax,N)
    PHI=np.zeros_like(rgrid)
    Eprev=None
    for it in range(iters):
        out=dirac_solve(PHI,rgrid,m,k)
        if out is None: return None
        E,G,F=out
        p=PHI; dP=np.gradient(PHI,rgrid); sigma=-1
        src=lam*np.exp(4*p)*(-2*sigma*(k*(F**2-G**2)/rgrid+dP*(F**2+G**2)+m*np.exp(p)*G*F))
        PHInew=solve_phi(src,rgrid)
        PHI=0.5*PHI+0.5*PHInew
        if Eprev is not None and abs(E-Eprev)<1e-10: break
        Eprev=E
    return E

m,k=0.5,-1
for lam in [0.0,0.1,0.2,0.4]:
    E1=scf(m,k,20,4000,lam)
    # rescaled: s=2 => r in [0.1,40], m->m/2
    s=2.0
    E2=scf(m/s,k,20*s,4000,lam)
    if E1 and E2:
        print(f"lam={lam}: (E/m) scale1={E1/m:.6f}  scale-s={E2/(m/s):.6f}  rel.diff={abs(E1/m-E2/(m/s))/(E1/m):.2e}")

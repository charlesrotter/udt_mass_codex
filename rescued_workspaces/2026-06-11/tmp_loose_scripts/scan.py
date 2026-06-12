import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from numpy import trapezoid
phi0=-np.cos(np.pi/5); mu2=np.pi/3
def run(rstar):
    def vrhs(r,y): p,J=y; return [J*np.exp(2*p)/r**2 if r>0 else 0.0, r**2*mu2*p]
    r0=1e-6
    V=solve_ivp(vrhs,[r0,rstar],[phi0+(mu2*phi0*np.exp(2*phi0)/6)*r0**2,r0**3*mu2*phi0/3],
                dense_output=True,rtol=1e-10,atol=1e-12,max_step=0.02)
    ph=lambda r:V.sol(r)[0]; php=lambda r:V.sol(r)[1]*np.exp(2*V.sol(r)[0])/r**2
    def dirac(E):
        def f(r,y):
            g,ff=y;p=ph(r);pp=php(r);e2=np.exp(2*p)
            return [(pp+1/r)*g+E*e2*ff,(pp-1/r)*ff-E*e2*g]  # kappa=-1
        return solve_ivp(f,[r0,rstar],[r0,-(E/3)*np.exp(2*phi0)*r0**2],dense_output=True,
                         rtol=1e-9,atol=1e-11,max_step=0.02)
    def bc(E):
        s=dirac(E);g,ff=s.y[:,-1];p=ph(rstar);pp=php(rstar);return (pp+1/rstar)*g+E*np.exp(2*p)*ff
    Es=np.linspace(0.02,2.0,120);R=[bc(E) for E in Es];E1=None
    for i in range(len(Es)-1):
        if R[i]*R[i+1]<0: E1=brentq(bc,Es[i],Es[i+1],xtol=1e-10);break
    if E1 is None: return rstar,None,None,None
    s=dirac(E1);rr=np.linspace(1e-6,rstar,8000);g=s.sol(rr)[0];ff=s.sol(rr)[1]
    p=np.array([ph(x) for x in rr]);e2=np.exp(2*p)
    cond=trapezoid((g**2-ff**2)*e2*rr**2,rr)/trapezoid((g**2+ff**2)*e2*rr**2,rr)
    return rstar,E1,E1*rstar,cond   # E1*rstar ~ m_pi proxy (since C ∝ r*)
print(f"{'r*':>6} {'E1':>8} {'E1*r* (~m_pi proxy)':>20} {'condensate':>11}")
for rs in [6.9875,7.5,8.5,10,12,15,20,30]:
    rstar,E1,mp,c=run(rs)
    print(f"{rs:>6.3f} {('%.4f'%E1) if E1 else 'none':>8} {('%.3f'%mp) if mp else '-':>20} {('%.4f'%c) if c is not None else '-':>11}")

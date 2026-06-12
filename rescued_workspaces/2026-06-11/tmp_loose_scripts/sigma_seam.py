import numpy as np
from numpy import pi, cos, exp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
phi0=-cos(pi/5); mu2=pi/3; rstar=6.9875
def rhs(r,y): p,J=y; return [J*exp(2*p)/r**2 if r>0 else 0.0, r**2*mu2*p]
r0=1e-6
V=solve_ivp(rhs,[r0,rstar],[phi0+(mu2*phi0*exp(2*phi0)/6)*r0**2,r0**3*mu2*phi0/3],
            dense_output=True,rtol=1e-12,atol=1e-14,max_step=0.008)
phi=lambda r: float(V.sol(r)[0])
# scalar breathing modes: R'=K e^{2phi}/r^2 ; K'=r^2(mu2 - w^2 e^{2phi})R ; K(r*)=0
def bc(w):
    def f(r,y):
        R,K=y; p=phi(r)
        return [K*exp(2*p)/r**2, r**2*(mu2-w**2*exp(2*p))*R]
    s=solve_ivp(f,[r0,rstar],[1.0,0.0],method='DOP853',rtol=1e-10,atol=1e-12,max_step=0.02)
    return s.y[1,-1]
ws=np.linspace(0.1,12,400); vals=[bc(w) for w in ws]; roots=[]
for i in range(len(ws)-1):
    if vals[i]*vals[i+1]<0:
        roots.append(brentq(bc,ws[i],ws[i+1],xtol=1e-10))
    if len(roots)>=4: break
me=0.51099895; C=4*pi**2*me*rstar
print("scalar breathing (sigma, 0+) omega_n =",[round(x,4) for x in roots])
print("  in MeV (xC):",[round(x*C,1) for x in roots])
print("C =",round(C,3),"MeV ; m_pi/C =",round(134.98/C,4))
print("kappa=-1 ground 0.94282 -> ",round(0.94282*C,2),"MeV (cf m_pi=135)")

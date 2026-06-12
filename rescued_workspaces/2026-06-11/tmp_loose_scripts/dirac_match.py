import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

def phi_metric(r): return 0.5*np.log(r/(2.0+r))
def phip_metric(r): return 1.0/(r*(2.0+r))
m=1.0

def rhs(r,y,E,kappa,sign):
    PHI=sign*phi_metric(r); PHIp=sign*phip_metric(r)
    G,F=y
    e2=np.exp(2*PHI); e1=np.exp(PHI)
    return [ (PHIp-kappa/r)*G+(E*e2+m*e1)*F,
             (PHIp+kappa/r)*F-(E*e2-m*e1)*G ]

def out_sol(E,kappa,sign,r0,rmatch):
    ak=abs(kappa)
    if kappa<0: y0=[r0**ak,0.0]
    else:       y0=[0.0,r0**ak]
    sol=solve_ivp(rhs,[r0,rmatch],y0,args=(E,kappa,sign),rtol=1e-10,atol=1e-13,
                  dense_output=True,max_step=0.02)
    return sol.y[:,-1]

def in_sol(E,kappa,sign,rmax,rmatch):
    # exterior PHI->0: decaying solution. Asymptotically G~e^{-beta r}, with F/G ratio fixed.
    beta=np.sqrt(m**2-E**2)
    # For PHI=0 system: G'=-kappa/r G+(E+m)F ; F'=kappa/r F-(E-m)G
    # large r drop 1/r: G'=(E+m)F, F'=-(E-m)G => decaying: G~e^{-beta r}, F=-(beta/(E+m))G... 
    # set ratio F/G = -beta/(E+m)? check: G'=-beta G => (E+m)F=-beta G => F=-beta/(E+m) G. ok
    G0=1.0; F0=-beta/(E+m)*G0
    y0=[G0,F0]
    sol=solve_ivp(rhs,[rmax,rmatch],y0,args=(E,kappa,sign),rtol=1e-10,atol=1e-13,
                  dense_output=True,max_step=0.02)
    return sol.y[:,-1]

def match_det(E,kappa,sign,r0=1e-6,rmax=40.0,rmatch=None):
    if rmatch is None: rmatch=min(8.0,rmax*0.4)
    yo=out_sol(E,kappa,sign,r0,rmatch)
    yi=in_sol(E,kappa,sign,rmax,rmatch)
    # match: G,F proportional => Wronskian Go*Fi - Fo*Gi =0
    Go,Fo=yo; Gi,Fi=yi
    # scale to avoid overflow
    no=np.hypot(Go,Fo); ni=np.hypot(Gi,Fi)
    return (Go*Fi-Fo*Gi)/(no*ni+1e-300)

def find_levels(kappa,sign,Egrid):
    D=np.array([match_det(E,kappa,sign) for E in Egrid])
    levels=[]
    for i in range(len(Egrid)-1):
        if np.isfinite(D[i]) and np.isfinite(D[i+1]) and D[i]*D[i+1]<0:
            try:
                Eroot=brentq(lambda E:match_det(E,kappa,sign),Egrid[i],Egrid[i+1],xtol=1e-10)
                levels.append(Eroot)
            except Exception:
                pass
    return levels

Egrid=np.linspace(0.02,0.999,400)
print("=== BARE phi (sign=+1), expect 0 bound states ===")
for kappa in [-1,-2,-3]:
    L=find_levels(kappa,1,Egrid)
    print(f" kappa={kappa}: {len(L)} levels", [round(x,4) for x in L[:12]])

print("=== INVERTED -phi (sign=-1), expect a tower ===")
for kappa in [-1,-2,-3]:
    L=find_levels(kappa,-1,Egrid)
    print(f" kappa={kappa}: {len(L)} levels", [round(x,4) for x in L[:12]])

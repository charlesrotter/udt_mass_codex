import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

def phi_metric(r): return 0.5*np.log(r/(2.0+r))
def phip_metric(r): return 1.0/(r*(2.0+r))
m=1.0
def rhs(r,y,E,kappa,sign):
    PHI=sign*phi_metric(r); PHIp=sign*phip_metric(r); G,F=y
    e2=np.exp(2*PHI); e1=np.exp(PHI)
    return [(PHIp-kappa/r)*G+(E*e2+m*e1)*F,(PHIp+kappa/r)*F-(E*e2-m*e1)*G]
def out_sol(E,kappa,sign,r0,rmatch):
    ak=abs(kappa); y0=[r0**ak,0.0] if kappa<0 else [0.0,r0**ak]
    s=solve_ivp(rhs,[r0,rmatch],y0,args=(E,kappa,sign),rtol=1e-10,atol=1e-13,max_step=0.02)
    return s.y[:,-1]
def in_sol(E,kappa,sign,rmax,rmatch):
    beta=np.sqrt(m**2-E**2); G0=1.0; F0=-beta/(E+m)*G0
    s=solve_ivp(rhs,[rmax,rmatch],[G0,F0],args=(E,kappa,sign),rtol=1e-10,atol=1e-13,max_step=0.02)
    return s.y[:,-1]
def match_det(E,kappa,sign,rmax,r0=1e-6,rmatch=8.0):
    yo=out_sol(E,kappa,sign,r0,rmatch); yi=in_sol(E,kappa,sign,rmax,rmatch)
    Go,Fo=yo; Gi,Fi=yi
    return (Go*Fi-Fo*Gi)/(np.hypot(Go,Fo)*np.hypot(Gi,Fi)+1e-300)
def find_levels(kappa,sign,rmax,Egrid):
    D=np.array([match_det(E,kappa,sign,rmax) for E in Egrid]); L=[]
    for i in range(len(Egrid)-1):
        if np.isfinite(D[i]*D[i+1]) and D[i]*D[i+1]<0:
            try: L.append(brentq(lambda E:match_det(E,kappa,sign,rmax),Egrid[i],Egrid[i+1],xtol=1e-11))
            except: pass
    return L
Eg=np.linspace(0.02,0.999,500)
print("BOX-SIZE INDEPENDENCE (inverted -phi, kappa=-1, first 4 levels):")
for rmax in [25,40,60,90]:
    L=find_levels(-1,-1,rmax,Eg)
    print(f"  rmax={rmax}: nlev={len(L)} first4={np.round(L[:4],5)}")
print()
# Channel ground states for ratios
g1=find_levels(-1,-1,60,Eg)[0]
g2=find_levels(-2,-1,60,Eg)[0]
g3=find_levels(-3,-1,60,Eg)[0]
print("Channel ground states:",round(g1,4),round(g2,4),round(g3,4))
print("E2/E1=",round(g2/g1,4)," E3/E1=",round(g3/g1,4))
# Koide on the three ground states (mass=E reading)
ms=np.array([g1,g2,g3])
Q=np.sum(ms)/(np.sum(np.sqrt(ms)))**2
print("Koide Q (mass=E):",round(Q,4))
# binding-energy reading mass=m-E
bs=m-ms
print("binding m-E:",np.round(bs,4)," ratios:",round(bs[1]/bs[0],3),round(bs[2]/bs[0],3))
Qb=np.sum(bs)/(np.sum(np.sqrt(bs)))**2
print("Koide Q (mass=m-E):",round(Qb,4))

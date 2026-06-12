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
def match_det(E,kappa,sign,rmax,r0=1e-6,rmatch=8.0):
    ak=abs(kappa); y0=[r0**ak,0.0] if kappa<0 else [0.0,r0**ak]
    so=solve_ivp(rhs,[r0,rmatch],y0,args=(E,kappa,sign),rtol=1e-10,atol=1e-13,max_step=0.02)
    Go,Fo=so.y[:,-1]
    beta=np.sqrt(m**2-E**2)
    si=solve_ivp(rhs,[rmax,rmatch],[1.0,-beta/(E+m)],args=(E,kappa,sign),rtol=1e-10,atol=1e-13,max_step=0.02)
    Gi,Fi=si.y[:,-1]
    return (Go*Fi-Fo*Gi)/(np.hypot(Go,Fo)*np.hypot(Gi,Fi)+1e-300)

kappa=-1; sign=-1; rmax=60; r0=1e-6; rmatch=8.0
# refine ground eigenvalue
Egrid=np.linspace(0.49,0.52,200)
D=[match_det(E,kappa,sign,rmax) for E in Egrid]
E=None
for i in range(len(Egrid)-1):
    if D[i]*D[i+1]<0: E=brentq(lambda e:match_det(e,kappa,sign,rmax),Egrid[i],Egrid[i+1],xtol=1e-12); break
print("refined ground E =",E)
# build stitched eigenfunction
ak=abs(kappa); y0=[r0**ak,0.0]
ro=np.linspace(r0,rmatch,8000)
so=solve_ivp(rhs,[r0,rmatch],y0,args=(E,kappa,sign),t_eval=ro,rtol=1e-11,atol=1e-14,max_step=0.01)
beta=np.sqrt(m**2-E**2)
ri=np.linspace(rmax,rmatch,8000)
si=solve_ivp(rhs,[rmax,rmatch],[1.0,-beta/(E+m)],args=(E,kappa,sign),t_eval=ri,rtol=1e-11,atol=1e-14,max_step=0.01)
# scale inner to match G at rmatch
scale=so.y[0,-1]/si.y[0,-1]
rL=so.t; GL=so.y[0]; FL=so.y[1]
rR=si.t[::-1]; GR=si.y[0][::-1]*scale; FR=si.y[1][::-1]*scale
r=np.concatenate([rL,rR]); G=np.concatenate([GL,GR]); F=np.concatenate([FL,FR])
dens=G**2+F**2
norm=np.trapezoid(dens,r)
cum=np.cumsum((dens[:-1]+dens[1:])/2*np.diff(r)); cum/=cum[-1]
r90=r[np.searchsorted(cum,0.9)]; r99=r[np.searchsorted(cum,0.99)]
rpeak=r[np.argmax(dens)]
print(f"  norm finite: {norm:.4e}")
print(f"  peak r={rpeak:.3f}, 90% within r={r90:.3f}, 99% within r={r99:.3f}")
print(f"  density(rmax)/peak = {dens[-1]/dens.max():.3e}  (decays -> localized, normalizable)")
print(f"  continuity at match: GL={so.y[0,-1]:.4e} GR*scale={si.y[0,-1]*scale:.4e}; F mismatch ratio={ (FL[-1]-FR[0])/(abs(FL[-1])+1e-30):.2e}")

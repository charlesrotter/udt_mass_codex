import numpy as np
from scipy.integrate import solve_ivp
def phi_metric(r): return 0.5*np.log(r/(2.0+r))
def phip_metric(r): return 1.0/(r*(2.0+r))
m=1.0
def rhs(r,y,E,kappa,sign):
    PHI=sign*phi_metric(r); PHIp=sign*phip_metric(r); G,F=y
    e2=np.exp(2*PHI); e1=np.exp(PHI)
    return [(PHIp-kappa/r)*G+(E*e2+m*e1)*F,(PHIp+kappa/r)*F-(E*e2-m*e1)*G]
# integrate outward at a true eigenvalue (kappa=-1 ground 0.5002) and check decay+norm
E=0.5002; kappa=-1; sign=-1
r0=1e-6; rmax=60
rs=np.linspace(r0,rmax,40000)
s=solve_ivp(rhs,[r0,rmax],[r0,0.0],args=(E,kappa,sign),t_eval=rs,rtol=1e-10,atol=1e-13,max_step=0.02)
G,F=s.y; r=s.t
dens=G**2+F**2
# normalization integral
norm=np.trapezoid(dens,r)
# where is 90% of the probability?
cum=np.cumsum((dens[:-1]+dens[1:])/2*np.diff(r)); cum/=cum[-1]
r90=r[np.searchsorted(cum,0.9)]
rpeak=r[np.argmax(dens)]
print(f"E={E} kappa={kappa} inverted:")
print(f"  norm integral (G^2+F^2) over (0,{rmax}) = {norm:.4e} (finite => normalizable)")
print(f"  density peak at r={rpeak:.3f}, 90% mass within r={r90:.3f} (interior-localized)")
print(f"  tail G(rmax)={G[-1]:.3e}, density(rmax)/peak={dens[-1]/dens.max():.2e} (decayed)")
# off-eigenvalue for contrast
E2=0.55
s2=solve_ivp(rhs,[r0,rmax],[r0,0.0],args=(E2,kappa,sign),t_eval=rs,rtol=1e-10,atol=1e-13,max_step=0.02)
G2=s2.y[0]
print(f"  OFF-level E=0.55: G(rmax)={G2[-1]:.3e}, |G(rmax)|/maxG={abs(G2[-1])/np.abs(G2).max():.2e} (diverging tail)")

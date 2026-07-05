import numpy as np
from scipy.integrate import solve_ivp
Z=1.0
# DEEP core (physical hadronic-ish ambient): phi0 negative => W0 large near core, but u shoots up,
# W freezes SMALL over a huge intermediate range => clean monopole there. Where does flux break?
def run(phi0, tmax=40):
    W0=np.exp(-2*phi0); ut0=4*W0/Z
    def rhs(t,y):
        u,ut,v,vt=y; W=np.exp(-2*u)
        return [ut,4*W/Z-ut, vt, -vt-8*W*v/Z]
    ts=np.linspace(0,tmax,80000)
    s=solve_ivp(rhs,[0,tmax],[phi0,ut0,1.0,-0.3],t_eval=ts,rtol=1e-12,atol=1e-14,method='DOP853')
    u,ut,v,vt=s.y; W=np.exp(-2*u); Pi=Z*np.exp(ts)*vt
    return ts,r_of(ts),v,Pi,W,u
def r_of(ts): return np.exp(ts)
print("DEEP core phi0=-1 (W0=7.4): frozen-W intermediate regime => is monopole clean?")
ts,r,v,Pi,W,u=run(-1.0)
for i in (0,20000,40000,60000,79999):
    print(f"  ln r={ts[i]:5.1f} W={W[i]:.3e} (Z/32={Z/32:.3f}) delta_phi={v[i]:+.4e} flux Pi={Pi[i]:+.5e}")
sel=(ts>6)&(ts<38)
print(f"  flux variation over ln r in [6,38]: max/min |Pi| = {np.abs(Pi[sel]).max()/np.abs(Pi[sel]).min():.4f}  (~1 => clean monopole over this huge range)")
print(f"  frozen W over [6,38]: {W[20000]:.2e} .. {W[79999]:.2e}  (tiny, ~const => real roots, near-clean 1/r)")
# where would attractor catch up (screening onset)? u vs attractor 0.5 ln(8 t)
tt=np.linspace(1,1e5,100000); 
print(f"\n  attractor u_att=0.5 ln(8 t) reaches frozen u={u[-1]:.2f} at t~{np.exp(2*u[-1])/8:.3e} (=ln r); r_onset=e^that = astronomically large")
print("  => for a DEEP ambient, marginal screening onset is at trans-astronomical r; clean monopole holds over all physical r.")

import numpy as np, sympy as sp
from VERIF_indep_matter import EL_lam
import axisym_matter_el as ME
# Round limit: c=d=0, all theta-derivs of metric =0, Theta = Theta(r) only.
# Compare residual form. The radial audited EL (radial_Bfree_soliton.theta_ddot_freed)
# gives Thpp = num/den, i.e. residual_radial = Thpp - num/den.
# We evaluate at a generic radial point with random a,b,Th,Thp,Thpp.
rng=np.random.default_rng(3)
def radial_resid(r,a,b,Th,ap,bp,Thp,Thpp,xi=1.0,kap=1.0):
    s=np.sin(Th); e2b=np.exp(2*b)
    num=(-2*kap*r**2*s**2*Thp*ap + 2*kap*r**2*s**2*Thp*bp
         - kap*r**2*np.sin(2*Th)*Thp**2 + 2*kap*e2b*s**3*np.cos(Th)
         - r**4*xi*Thp*ap + r**4*xi*Thp*bp - 2*r**3*xi*Thp
         + r**2*xi*e2b*np.sin(2*Th))
    den=r**2*(2*kap*s**2 + r**2*xi)
    return Thpp - num/den

print("=== ROUND (theta-indep, c=d=0) EL comparison ===")
print("indep_EL, committed_axisym_EL, radial_audited(Thpp-rhs):")
for trial in range(4):
    r=float(rng.uniform(0.8,4)); a=float(rng.uniform(-.3,.3)); b=float(rng.uniform(-.4,.1))
    Th=float(rng.uniform(0.4,2.6)); ap=float(rng.uniform(-.2,.2)); bp=float(rng.uniform(-.2,.2))
    Thp=float(rng.uniform(-.3,.3)); Thpp=float(rng.uniform(-.3,.3))
    z=0.0
    # indep EL lambdify order: r,th, then a,b,c,d,Th each (val,r,t,rr,tt,rt), xi,kap
    # set theta=pi/2, all theta-derivs 0, c=d=0
    args=[r, np.pi/2,
          a,ap,z,Thpp*0+ float(rng.uniform(-.1,.1)),z,z,   # a: val,a_r,a_t,a_rr,a_tt,a_rt
          b,bp,z, float(rng.uniform(-.1,.1)),z,z,           # b
          z,z,z,z,z,z,                                       # c
          z,z,z,z,z,z,                                       # d
          Th,Thp,z,Thpp,z,z,                                 # Th
          1.0,1.0]
    mine=float(EL_lam(*args))
    comm=float(ME.matter_el_resid(r,np.pi/2, a,b,z,z,Th, ap,bp,z,z,Thp,
        z,z,z,z,z, args[9],args[15],z,z,Thpp, z,z,z,z,z, z,z,z,z,z, 1.0,1.0))
    rad=radial_resid(r,a,b,Th,ap,bp,Thp,Thpp)
    print(f"r={r:.2f} Th={Th:.2f}: indep={mine:+.5e} committed={comm:+.5e} radial_audit={rad:+.5e}  indep/rad={mine/rad if abs(rad)>1e-12 else float('nan'):.4f}  comm/rad={comm/rad if abs(rad)>1e-12 else float('nan'):.4f}")

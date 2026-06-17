#!/usr/bin/env python
"""
VERIF_ceff_potential_eigen.py -- OBSERVE. float64. New file only.

Follow-on to VERIF_ceff_potential.py.  Two jobs:
 (A) Characterize V(r*) on a CLEAN representative DEEP negative-phi matter cell
     (phi0 ~ -0.8, monotonic, phi(seal)=0) -- the profile the task describes,
     since the #56 hedgehog profile is non-monotonic (core spike + body bump,
     phi only -0.14 deep).  Profile constructed & stated explicitly below.
 (B) BOX-INDEPENDENCE eigen-scan: solve  -psi'' + V(r*) psi = (omega^2) psi  in the
     tortoise coordinate r* with a hard outer wall at R_wall, vary R_wall ~3x at
     FIXED phi-profile; report whether omega_1 is intrinsic (constant) or ~1/R_wall.

REDUCTION (from VERIF_ceff_potential.py, verified symbolically there):
   W2 f-weighted w-wave  ->  (P f u')' + om^2 (P/f) u = 0,  P=2r^2/(1+w)^2, f=e^{-2phi}.
   tortoise dr*=dr/f, u=psi/sqrt(P):  -psi'' + V psi = om^2 psi,
   V(r*) = (1/sqrt(P)) d^2 sqrt(P)/dr*^2.   With w0=0:  V = -2 phi' f^2 / r  (as fn of r).
"""
import numpy as np
from scipy.linalg import eigh_tridiagonal

# ---- representative DEEP negative-phi matter cell (STATED explicitly) ----
# phi(r) = phi0 * exp(-(r/Rc)^2),  phi0 = -0.8, core scale Rc.
# This is a smooth, monotonic-magnitude negative-phi bump: phi(0)=phi0<0 (deep),
# phi -> 0 at large r (matches a flat exterior / seal).  phi'(r) = -2 phi0 r/Rc^2 * exp(...) > 0
# (since phi0<0), so V = -2 phi' f^2/r < 0 -- attractive everywhere in r>0.  NOT a hedgehog;
# a clean dilation well, exactly the "deep negative-phi" object Conjecture A is about.
def phi_profile(r, phi0=-0.8, Rc=1.0):
    return phi0*np.exp(-(r/Rc)**2)
def phip_profile(r, phi0=-0.8, Rc=1.0):
    return phi0*np.exp(-(r/Rc)**2)*(-2*r/Rc**2)

def V_of_r(r, phi0=-0.8, Rc=1.0):
    phi = phi_profile(r,phi0,Rc); phip=phip_profile(r,phi0,Rc)
    f = np.exp(-2*phi)
    with np.errstate(divide='ignore', invalid='ignore'):
        V = -2*phip*f**2/r
    # r->0 limit: phip/r -> -2 phi0/Rc^2 (finite); f->e^{-2phi0}. V0 = -2*(-2 phi0/Rc^2)*e^{-4phi0}
    V0 = -2*(-2*phi0/Rc**2)*np.exp(-4*phi0)
    V = np.where(r>1e-9, V, V0)
    return V, f

def tortoise(r, f):
    # dr* = dr/f, r ascending, r*[0]=0
    rs = np.concatenate([[0.0], np.cumsum(np.diff(r)/((f[1:]+f[:-1])/2))])
    return rs

def solve_box(R_wall, phi0=-0.8, Rc=1.0, Nr=6000):
    """Hard-wall Dirichlet at r=0 (regular) and r=R_wall. Solve on uniform r* grid."""
    r = np.linspace(1e-4, R_wall, Nr)
    V, f = V_of_r(r, phi0, Rc)
    rs = tortoise(r, f)
    # interpolate V onto a UNIFORM r* grid (Schrodinger op is -d^2/dr*^2 + V)
    Ns = Nr
    rsu = np.linspace(rs[0], rs[-1], Ns)
    Vu = np.interp(rsu, rs, V)
    h = rsu[1]-rsu[0]
    # interior points (Dirichlet at both ends)
    diag = 2.0/h**2 + Vu[1:-1]
    off  = -1.0/h**2*np.ones(len(diag)-1)
    w = eigh_tridiagonal(diag, off, select='i', select_range=(0,5))[0]
    om = np.sqrt(np.maximum(w,0.0)+0j)  # omega^2 = eigenvalue; may be negative (bound)
    return w, rs[-1]  # eigenvalues (=omega^2), tortoise length

if __name__=="__main__":
    np.set_printoptions(suppress=True,precision=6,linewidth=120)
    print("="*78); print("DEEP negative-phi cell:  phi(r)=phi0 exp(-(r/Rc)^2), phi0=-0.8, Rc=1.0")
    print("  V(r)= -2 phi' f^2/r  (Liouville form of W2 w-wave; tortoise dr*=dr/f)")
    print("="*78)
    r=np.linspace(1e-4,8,400); V,f=V_of_r(r)
    print(f"  phi range [{phi_profile(r).min():.4f},{phi_profile(r).max():.4f}]; "
          f"f=c_eff range [{f.min():.4f},{f.max():.4f}] (finite -> NO horizon)")
    print(f"  V range [{V.min():.5g},{V.max():.5g}]; V(0+)~{V[0]:.5g}")
    imin=np.argmin(V); print(f"  V min {V[imin]:.5g} at r={r[imin]:.4f}; V->0 outward: {V[-1]:.4g}")
    print(f"  phi' sign: [{phip_profile(r).min():.4g},{phip_profile(r).max():.4g}] (>=0 => V<=0 attractive)")
    print("\n   r       phi       f       V(r)")
    for i in np.linspace(0,len(r)-1,12).astype(int):
        print(f"  {r[i]:6.3f}  {phi_profile(r[i]):7.4f}  {f[i]:6.4f}  {V[i]:10.5g}")

    print("\n"+"="*78); print("BOX-INDEPENDENCE: vary R_wall 3x at FIXED phi-profile (phi0=-0.8,Rc=1)")
    print("  report lowest eigenvalues omega^2 (negative=intrinsic bound; ~ -1/R^0 if intrinsic)")
    print("="*78)
    print(f"  {'R_wall':>8} {'rstar_len':>10} {'  omega^2_0':>12} {'omega^2_1':>12} {'omega^2_2':>12} {'omega^2_3':>12}")
    rows=[]
    for Rw in [4.0, 8.0, 12.0, 16.0]:
        w,Ls=solve_box(Rw); rows.append((Rw,w))
        print(f"  {Rw:8.1f} {Ls:10.3f}  "+" ".join(f"{x:12.5f}" for x in w[:4]))
    # intrinsic check: do the NEGATIVE eigenvalues (bound states) stay put?
    print("\n  INTRINSIC TEST: a true well's bound states (omega^2<0) are R_wall-independent;")
    print("  box modes (omega^2>0) scale ~1/R_wall^2.  Compare omega^2_0 across R_wall:")
    base=rows[0][1][0]
    for Rw,w in rows:
        tag = "BOUND(intrinsic)" if w[0]<0 else "positive(box?)"
        print(f"    R_wall={Rw:5.1f}: omega^2_0={w[0]:+.6f}  drift_from_R=4: {w[0]-base:+.2e}  [{tag}]")

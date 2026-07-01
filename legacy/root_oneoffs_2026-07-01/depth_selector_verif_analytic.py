"""
depth_selector_verif_analytic.py
================================
EXACT analytic resolution of the confinement question. No grid artifacts.

U(D) = c_grav(e^{2D}-1) + (1/2)A0^2*omega2(D),  omega2(D)=floor - c_bind D^k,
c_bind = floor/D*^k  (so omega2(D*)=0).  Physical only where omega2>=0, i.e. D<=D*.

A confining interior minimum EXISTS in (0,D*) iff dU/dD = 0 has a root there with the
RIGHT sign change (- to +).  dU/dD = 2 c_grav e^{2D} - (1/2)A0^2 c_bind k D^{k-1}.
Define G(D)=2 c_grav e^{2D} (rising), H(D)=(1/2)A0^2 c_bind k D^{k-1} (carrier downpull).
dU/dD<0  <=>  H>G.  An interior MIN exists iff H crosses ABOVE G then BACK below it
within (0,D*): a region where the carrier out-pulls gravity bracketed by rising regions.

This depends ONLY on the dimensionless ratio  R := A0^2/c_grav  (both prefactors),
plus floor, D*, k.  Solve exactly: for which (R,floor,D*,k) in the derived ranges does
dU/dD have a sign change to NEGATIVE somewhere in (0,D*)?

THE HONEST QUESTION FOR THE VERDICT:
  (i) Does a genuine interior well exist for SOME legitimate (R,floor,D*,k)?  If yes the
      constructor's 'monotone, construction-robust' claim is FALSE as stated.
  (ii) But is that well CONFINING in the relevant sense (does it sit comfortably below D*,
       with omega2>0 by a margin, hosting >1 level), or is it a sliver pinned against the
       cap (omega2->0) that hosts no real tower?  That decides whether the well RESCUES
       the depth-selector or whether the NON-CLOSURE verdict survives on stronger grounds.
"""
import numpy as np
import sympy as sp

D,cg,A,fl,Ds,k = sp.symbols('D c_grav A0sq floor Dstar k',positive=True)
cb = fl/Ds**k
U  = cg*(sp.exp(2*D)-1) + sp.Rational(1,2)*A*(fl - cb*D**k)
dU = sp.diff(U,D)
print("dU/dD =", sp.simplify(dU))
print("     = 2 c_grav e^{2D} - (1/2)A0^2*floor*k*D^{k-1}/D*^k")

# minimum downpull-vs-rise: does H(D) ever exceed G(D) for D in (0,D*)?  H/G ratio max.
def dip_exists(R, floor, Dstar, kk, n=2_000_000):
    """R = A0^2/c_grav.  Return (dip_exists, D_dip_window, omega2_at_dip_center)."""
    cb_v = floor/Dstar**kk
    D = np.linspace(1e-6, Dstar, n)
    G = 2*np.exp(2*D)                      # = (1/c_grav)*2 c_grav e^{2D}, scaled by c_grav
    H = 0.5*R*cb_v*kk*D**(kk-1)            # = (1/c_grav)*(1/2)A0^2 c_bind k D^{k-1}
    dUdD_over_cg = G - H                   # sign of dU/dD (c_grav>0 scales out)
    neg = dUdD_over_cg < 0
    if not neg.any():
        return False, None, None
    Dn = D[neg]
    Dc = Dn.mean()
    w2 = floor - cb_v*Dc**kk
    return True, (Dn.min(),Dn.max()), w2

print("\n"+"="*78)
print("EXACT: does dU/dD go negative in (0,D*) for legitimate (R=A0^2/c_grav,floor,D*,k)?")
print("="*78)
# find the THRESHOLD R at which a dip first appears, for several (floor,D*,k)
import itertools
print(f"\n{'floor':>6}{'D*':>6}{'k':>6}{'R_threshold(A0^2/c_grav)':>26}{'dip window':>22}{'omega2@dip':>12}")
for floor,Dstar,kk in itertools.product([2.0,6.0,12.0],[2.4,2.6,3.0,3.4],[3.5,4.0,4.5,4.9]):
    # bisection on R for first appearance of a dip
    lo,hi=1e-2,1e12
    if not dip_exists(hi,floor,Dstar,kk,400000)[0]:
        print(f"{floor:6}{Dstar:6}{kk:6}{'no dip even at R=1e12':>26}")
        continue
    for _ in range(60):
        mid=np.sqrt(lo*hi)
        if dip_exists(mid,floor,Dstar,kk,400000)[0]: hi=mid
        else: lo=mid
    Rth=hi
    ok,win,w2=dip_exists(Rth*1.5,floor,Dstar,kk,2_000_000)
    print(f"{floor:6}{Dstar:6}{kk:6}{Rth:26.3e}{f'[{win[0]:.3f},{win[1]:.3f}]':>22}{w2:12.3f}")

print("""
READ:
 - If R_threshold is FINITE for a (floor,D*,k), then for A0^2/c_grav above it a genuine
   interior dip (omega2>0) EXISTS -> U is NOT monotone -> constructor over-claim on 'monotone
   construction-robust'.
 - The decisive sub-question: WHERE is the dip's omega2? If omega2@dip is SMALL (dip pinned
   against the cap D*), the 'well' is a sliver in the tachyon-cap corner: the right wall is the
   tachyon cap itself (A^2->inf there) and the well hosts ~no bound depth tower -> NON-CLOSURE
   survives on the deeper ground that the well only forms by pressing against the cap.
 - If omega2@dip is LARGE (a fat well well clear of D*), that would RESCUE confinement and
   the constructor's central claim would be FALSIFIED, not just corrected.
""")

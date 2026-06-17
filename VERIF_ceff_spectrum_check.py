"""
PART 3: SPECTRUM / BOX-SCAN.  Independent eigensolver.

Solve the SL eigenproblem in u directly (most physical, avoids tortoise issues):
    (P f u')' + omega^2 (P/f) u = 0 ,  P = 2 r^2 ,  f = e^{-2 phi(r)}
  generalized eigenproblem  -d/dr(p u') = omega^2 rho u , p=Pf, rho=P/f.
  Regular BC at r=0: u finite (Neumann-like on u: u'(0)=0 for even core; but the
     r^2 weight already kills the boundary -- we impose the regular branch).
  Wall BC at r=R_wall: u(R_wall)=0 (the "box").

KEY TEST: vary R_wall by ~4x. If omega_0^2 ~ const/R_wall^2 -> pure box (NO intrinsic state).
If omega_0^2 -> R-independent constant as R_wall grows -> INTRINSIC BOUND STATE (BREAK!).

Also cross-check against the Liouville-normal Schrodinger form
   -psi_xx + V psi = omega^2 psi , V=-2 phi' f^2/r , x=tortoise.

Finite-difference, float64. mpmath spot-check at the end.
"""
import numpy as np
from scipy.linalg import eigh
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

def solve_SL(phi_fun, phip_fun, R_wall, N=4000, r0=1e-6):
    """Generalized eigenproblem on u: -(p u')' = w^2 rho u, Dirichlet at wall,
       regular (Neumann u'=0) at r0. Returns smallest few omega^2."""
    r = np.linspace(r0, R_wall, N)
    h = r[1]-r[0]
    phi = phi_fun(r)
    f = np.exp(-2*phi)
    p = 2*r**2*f           # = P f
    rho = 2*r**2/f         # = P/f
    # interior nodes 1..N-2 ; node N-1 (wall) Dirichlet u=0 -> drop.
    # node 0: regular core. Use u'(0)=0 (even). We'll keep node 0 with Neumann.
    # Build stiffness K (from int p u'^2) and mass M (from int rho u^2) -> generalized eig.
    # p at half-points:
    rh = 0.5*(r[:-1]+r[1:]); ph = np.interp(rh, r, p)
    n = N
    main = np.zeros(n); lo = np.zeros(n-1); up = np.zeros(n-1)
    for i in range(n):
        left = ph[i-1] if i>0 else 0.0
        right = ph[i] if i<n-1 else 0.0
        main[i] = (left+right)/h
        if i>0: lo[i-1] = -left/h
        if i<n-1: up[i] = -right/h
    K = diags([lo, main, up], [-1,0,1]).toarray()
    M = np.diag(rho)*h   # lumped mass (consistent enough for trend)
    # Dirichlet at wall: remove last node
    K2 = K[:-1,:-1].copy(); M2 = M[:-1,:-1].copy()
    # regular at core: Neumann already natural in FE (no action needed)
    w2, V = eigh(K2, M2)
    w2 = np.sort(w2.real)
    return w2[w2 > -1e-9][:6]

# ---- Profiles ----
def make_gaussian(phi0, width):
    # clean monotonic deep cell: phi(r) = phi0 * exp(-(r/width)^2), phi(inf)=0
    def phi(r): return phi0*np.exp(-(r/width)**2)
    def phip(r): return phi0*np.exp(-(r/width)**2)*(-2*r/width**2)
    return phi, phip

def make_tanh_well(phi0, R0, sharp):
    # deep flat core then rises to 0: phi = phi0*0.5*(1-tanh((r-R0)/sharp))
    def phi(r): return phi0*0.5*(1-np.tanh((r-R0)/sharp))
    def phip(r): return phi0*0.5*(-(1/sharp)/np.cosh((r-R0)/sharp)**2)
    return phi, phip

def make_hedgehog(phi0):
    # non-monotonic: central dip + overshoot (mimics #56 hedgehog), phi(inf)->0
    def phi(r):
        return phi0*np.exp(-(r/0.7)**2) + 0.25*abs(phi0)*np.exp(-((r-1.3)/0.4)**2)
    def phip(r):
        return (phi0*np.exp(-(r/0.7)**2)*(-2*r/0.7**2)
                + 0.25*abs(phi0)*np.exp(-((r-1.3)/0.4)**2)*(-2*(r-1.3)/0.4**2))
    return phi, phip

print("="*70)
print("BOX SCAN: vary R_wall ~4x.  Pure box => omega0^2 * R_wall^2 ~ const.")
print("Intrinsic bound state => omega0^2 -> R-independent constant.")
print("="*70)

profiles = {
    "Gaussian phi0=-0.8 w=1.0": make_gaussian(-0.8, 1.0),
    "Gaussian phi0=-1.5 w=1.0": make_gaussian(-1.5, 1.0),
    "tanh-well phi0=-0.8 R0=1.0": make_tanh_well(-0.8, 1.0, 0.3),
    "tanh-well phi0=-3.0 R0=1.0": make_tanh_well(-3.0, 1.0, 0.3),
    "hedgehog(#56-like) phi0=-0.8": make_hedgehog(-0.8),
}

for name,(phi,phip) in profiles.items():
    print(f"\n--- {name} ---")
    print(f"{'R_wall':>8} {'omega0^2':>14} {'omega0^2*Rw^2':>16} {'omega1^2':>14}")
    base = None
    for Rw in [3.0, 6.0, 9.0, 12.0]:
        w2 = solve_SL(phi, phip, Rw, N=3000)
        o0 = w2[0]; o1 = w2[1] if len(w2)>1 else np.nan
        print(f"{Rw:8.1f} {o0:14.6e} {o0*Rw**2:16.6e} {o1:14.6e}")

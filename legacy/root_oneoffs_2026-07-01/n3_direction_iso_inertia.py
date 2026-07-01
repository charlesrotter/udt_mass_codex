#!/usr/bin/env python3
"""
n3_direction_iso_inertia.py  — UDT mass codex.  GATED, DATA-BLIND.

THE QUESTION: the charge-1 L2+L4 hedgehog soliton has an internal SO(3)
orientation in target space.  The THREE N=3 directions are the three target
axes / the l=1 internal channel — operationally the THREE iso-rotation
generators T_a (a=1,2,3) of SO(3) acting on n.  Compute the energy associated
with each of the three directions and ask: DEGENERATE or SPLIT?

OPERATIONAL DEFINITION (tagged CHOSE):  promote the soliton's internal
orientation R in SO(3) to a slow collective coordinate R(t)=exp(omega_a T_a t).
The l=1 channel = an infinitesimal iso-rotation of the field about target axis a:
    delta_a n = (T_a n) = (e_a x n)      [T_a = SO(3) generator, (T_a)_{bc}=-eps_{abc}]
The kinetic energy of iso-rotation is  (1/2) Lambda_{ab} omega_a omega_b , with
the ISO-MOMENT-OF-INERTIA TENSOR

    Lambda_{ab} = INT d^3x sqrt(g) * M_{munu}^{spatial-time}  evaluated on the
                  iso-rotation zero-direction (e_a x n),(e_b x n).

From L = L2 + L4 the field-space metric (the coefficient of dot-n dot-n in the
Lagrangian, i.e. the t-t kinetic form) is, for a unit-vector n on the UDT
static slice with sqrt(g)=e^{phi} r^2 sin th and g^{tt}=-e^{2phi}/c^2:

  L2 kinetic:  +(xi/2) e^{2phi}/c^2 (dot n . dot n)
  L4 kinetic:  +(kappa/2) e^{2phi}/c^2 [ (dot n . dot n)(grad-piece) - cross ]
               = +(kappa/2) e^{2phi}/c^2 * g^{ij}( (dot n.dot n)(d_i n.d_j n)
                                                   - (dot n.d_i n)(dot n.d_j n) )
(the standard L4 = -(kappa/4)(d_m n x d_n n)^2 expanded; the t-t part picks the
spatial g^{ij} once.)  So per unit omega^2 the inertia DENSITY about axis a,b is

  lambda_{ab}(x) = (1/c^2) sqrt(g) e^{2phi} [
        (xi/2) (v_a . v_b)
      + (kappa/2) g^{ij}( (v_a.v_b)(d_i n.d_j n) - (v_a.d_i n)(v_b.d_j n) ) ]
  with v_a = e_a x n  (the iso-rotation velocity field).

DEGENERATE  <=>  Lambda_{ab} ∝ delta_{ab}.   We compute all 9 components on the
finite back-reacted cell with the BVP soliton profile Theta(r), and read off the
three eigenvalues + whether anything splits them.

PREMISE LEDGER (chose vs derived):
 - DERIVED: L2+L4 field-space (t-t kinetic) metric from the settled action
   (native_stabilizer_results.md L4 = |omega_H1|^2_g; this is its t-t reduction).
 - DERIVED: iso-rotation generator v_a = e_a x n is the l=1 / SO(3) channel.
 - DERIVED: the hedgehog Theta=theta and BVP profile Theta(r) on the cell.
 - CHOSE: operationalize "3 N=3 directions" = 3 SO(3) iso-generators T_a (the
   eps_abc triplet, the spin-1 piece of End(H1)=1+3+5).  [The natural l=1 reading]
 - CHOSE: collective-coordinate (slow iso-rotation) energy as the "energy of a
   direction".  This is the standard soliton-quantization inertia; here used
   data-blind, classically (NO hbar: we report Lambda_ab, a pure-number RATIO
   structure; we do NOT multiply by hbar or form hbar^2/2Lambda).
 - CHOSE: xi=1 units; only kappa/xi physical.  Finite cell [r_core,r_int].
 - CHOSE: phi background (flat and deep log cell) per native_profile_bvp.

DATA-BLIND: no masses, ratios, walls, Koide, sqrt(2), 45-deg.  Report the pure
number that falls out of the winding sector ALONE.  No spinor/Dirac/hbar/photon.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import numpy as np
import torch
from scipy.integrate import solve_bvp

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[device] {DEV}, torch {torch.__version__}")


# ---------------------------------------------------------------------------
# Soliton profile machinery (reused EL BVP from native_profile_bvp.py; DERIVED).
# ---------------------------------------------------------------------------
def theta_ddot(r, Th, Thp, phi, phip, xi, kappa):
    s = np.sin(Th)
    num = ((0.5) * Thp * r**2 * (
        -4*Thp*kappa*np.sin(2*Th) + Thp*kappa*np.sin(4*Th)
        - Thp*r**2*xi*np.sin(2*Th) + kappa*phip*(1 - np.cos(2*Th))**2
        - 2*kappa*phip*np.cos(2*Th) + 2*kappa*phip
        - phip*r**2*xi*np.cos(2*Th) + 5*phip*r**2*xi
        + 2*r*xi*np.cos(2*Th) - 10*r*xi)
        + 2*kappa*np.exp(2*phi)*s**3*np.cos(Th)
        + 2*r**2*xi*np.exp(2*phi)*np.sin(2*Th))
    den = r**2 * (2*kappa*s**4 + 2*kappa*s**2 + r**2*xi*s**2 + 2*r**2*xi)
    return num / den


def phi_bg(r, p, r_int):
    if p == 0.0:
        return np.zeros_like(r), np.zeros_like(r)
    phi = p * np.log(r / r_int)
    phip = p / r
    return phi, phip


def solve_bvp_profile(r_core, r_int, xi, kappa, p, N=400):
    x0 = np.linspace(r_core, r_int, N)

    def rhs(r, y):
        Th, Thp = y
        phi, phip = phi_bg(r, p, r_int)
        return np.vstack([Thp, theta_ddot(r, Th, Thp, phi, phip, xi, kappa)])

    def bc(ya, yb):
        return np.array([ya[0] - math.pi, yb[0] - 0.0])

    L = math.sqrt(kappa / xi)
    w = 2.0 * L
    Th0 = math.pi * 0.5 * (1 - np.tanh((x0 - (r_core + w)) / (0.8 * L)))
    Thp0 = np.gradient(Th0, x0)
    y0 = np.vstack([Th0, Thp0])
    sol = solve_bvp(rhs, bc, x0, y0, tol=1e-8, max_nodes=200000, verbose=0)
    return sol


# ---------------------------------------------------------------------------
# THE ISO-MOMENT-OF-INERTIA TENSOR Lambda_{ab}.
#
# Hedgehog field:  n(r,th,ph) = ( sinTheta(r) sinth cosph,
#                                 sinTheta(r) sinth sinph,
#                                 cosTheta(r) )
# Iso-rotation velocity about axis a:  v_a = e_a x n.
# Spatial metric:  g_rr=e^{2phi}, g_thth=r^2, g_phph=r^2 sin^2 th.
#   g^{rr}=e^{-2phi}, g^{thth}=1/r^2, g^{phph}=1/(r^2 sin^2 th).
# sqrt(g) = e^{phi} r^2 sin th.
#
# Inertia density (per omega_a omega_b, classical; c=1 absorbed -> overall
#   constant, cancels in ratios / in degeneracy test):
#   lambda_{ab}(x) = sqrt(g) e^{2phi} [
#        (xi/2)(v_a.v_b)
#      + (kappa/2) [ (v_a.v_b)(grad n.grad n)_g - (v_a.grad n)_g.(v_b.grad n)_g ] ]
#   where (grad n.grad n)_g = g^{ij} d_i n.d_j n  (scalar)
#   and (v_a.grad n)_g.(v_b.grad n)_g = g^{ij} (v_a.d_i n)(v_b.d_j n).
#
# Lambda_{ab} = INT lambda_{ab}(x) dr dth dph.   Build it on the GPU grid.
# ---------------------------------------------------------------------------
def iso_inertia_tensor(r_np, Theta_np, phi_np, xi, kappa,
                       nth=160, nph=160, e2phi_in_measure=True):
    """Return 3x3 Lambda_{ab} integrated over the cell.  GPU float64."""
    r = torch.as_tensor(r_np, device=DEV)             # (Nr,)
    Th = torch.as_tensor(Theta_np, device=DEV)        # Theta(r), (Nr,)
    phi = torch.as_tensor(phi_np, device=DEV)         # phi(r), (Nr,)
    Thp_np = np.gradient(Theta_np, r_np)
    Thp = torch.as_tensor(Thp_np, device=DEV)         # Theta'(r), (Nr,)

    th = torch.linspace(1e-6, math.pi - 1e-6, nth, device=DEV)
    ph = torch.linspace(0.0, 2*math.pi, nph, device=DEV)
    dr = (r[1:] - r[:-1])
    # use midpoint in r
    rm = 0.5*(r[1:]+r[:-1]); Thm = 0.5*(Th[1:]+Th[:-1])
    phim = 0.5*(phi[1:]+phi[:-1]); Thpm = 0.5*(Thp[1:]+Thp[:-1])
    Nr = rm.shape[0]
    dth = th[1]-th[0]; dph = ph[1]-ph[0]

    # broadcast grids (Nr, nth, nph)
    R = rm.view(Nr,1,1); TH = Thm.view(Nr,1,1); PHI = phim.view(Nr,1,1)
    THP = Thpm.view(Nr,1,1)
    TT = th.view(1,nth,1); PP = ph.view(1,1,nph)

    ONE = torch.ones((Nr, nth, nph), device=DEV, dtype=torch.float64)
    sTh = torch.sin(TH)*ONE; cTh = torch.cos(TH)*ONE
    st = torch.sin(TT)*ONE; ct = torch.cos(TT)*ONE
    sp = torch.sin(PP)*ONE; cp = torch.cos(PP)*ONE

    # n components (all full shape (Nr,nth,nph))
    n1 = sTh*st*cp; n2 = sTh*st*sp; n3 = cTh
    # d_r n = (cTh st cp, cTh st sp, -sTh) * Theta'(r)
    dr_n1 = cTh*st*cp*THP; dr_n2 = cTh*st*sp*THP; dr_n3 = -sTh*THP
    # d_th n = (sTh ct cp, sTh ct sp, 0)
    dt_n1 = sTh*ct*cp; dt_n2 = sTh*ct*sp; dt_n3 = torch.zeros_like(n1)
    # d_ph n = (-sTh st sp, sTh st cp, 0)
    dp_n1 = -sTh*st*sp; dp_n2 = sTh*st*cp; dp_n3 = torch.zeros_like(n1)

    e2phi = torch.exp(2*PHI); em2phi = torch.exp(-2*PHI)
    sqrtg = torch.exp(PHI)*R**2*st     # e^{phi} r^2 sin th

    # gradient invariant (grad n . grad n)_g = g^{ij} d_i n . d_j n
    grr = em2phi; gthth = 1.0/R**2; gphph = 1.0/(R**2*st**2)
    dn_r2 = dr_n1**2+dr_n2**2+dr_n3**2
    dn_t2 = dt_n1**2+dt_n2**2+dt_n3**2
    dn_p2 = dp_n1**2+dp_n2**2+dp_n3**2
    grad2 = grr*dn_r2 + gthth*dn_t2 + gphph*dn_p2   # scalar field

    # iso-rotation velocities v_a = e_a x n :
    #   v_1 = ( 0 , -n3, n2 )
    #   v_2 = ( n3, 0  , -n1)
    #   v_3 = (-n2, n1 , 0  )
    v = [
        (torch.zeros_like(n1), -n3, n2),
        (n3, torch.zeros_like(n1), -n1),
        (-n2, n1, torch.zeros_like(n1)),
    ]
    # v_a . d_i n  (for i=r,th,ph), and v_a.v_b
    def dot(A, B):
        return A[0]*B[0]+A[1]*B[1]+A[2]*B[2]
    dn = {'r': (dr_n1,dr_n2,dr_n3), 't': (dt_n1,dt_n2,dt_n3), 'p': (dp_n1,dp_n2,dp_n3)}
    va_di = {}
    for a in range(3):
        va_di[a] = {ax: dot(v[a], dn[ax]) for ax in ('r','t','p')}

    measure = sqrtg * (e2phi if e2phi_in_measure else 1.0)
    Lam = torch.zeros((3,3), device=DEV, dtype=torch.float64)
    Lam2 = torch.zeros((3,3), device=DEV, dtype=torch.float64)  # L2-only piece
    Lam4 = torch.zeros((3,3), device=DEV, dtype=torch.float64)  # L4-only piece
    cell_dr = dr.view(Nr,1,1)
    for a in range(3):
        for b in range(3):
            vavb = dot(v[a], v[b])
            # L4 cross term: g^{ij}(va.di n)(vb.dj n)
            cross = (grr*va_di[a]['r']*va_di[b]['r']
                     + gthth*va_di[a]['t']*va_di[b]['t']
                     + gphph*va_di[a]['p']*va_di[b]['p'])
            dens2 = (xi/2.0)*vavb
            dens4 = (kappa/2.0)*(vavb*grad2 - cross)
            integ2 = (measure*dens2*cell_dr).sum()*dth*dph
            integ4 = (measure*dens4*cell_dr).sum()*dth*dph
            Lam2[a,b] = integ2; Lam4[a,b] = integ4; Lam[a,b] = integ2+integ4
    return (Lam.cpu().numpy(), Lam2.cpu().numpy(), Lam4.cpu().numpy())


def report_tensor(name, Lam):
    evals = np.linalg.eigvalsh(Lam)
    diag = np.diag(Lam)
    offmax = np.max(np.abs(Lam - np.diag(diag)))
    spread = (evals.max()-evals.min())/evals.mean() if evals.mean() != 0 else float('nan')
    print(f"\n[{name}]")
    np.set_printoptions(precision=6, suppress=True)
    print(Lam)
    print(f"  eigenvalues = {evals}")
    print(f"  off-diagonal max |.| = {offmax:.3e}")
    print(f"  eigenvalue spread (max-min)/mean = {spread:.3e}")
    return evals, offmax, spread


def main():
    xi = 1.0
    r_core = 0.05
    print("="*78)
    print("ISO-MOMENT-OF-INERTIA Lambda_ab of the L2+L4 hedgehog soliton")
    print("The THREE N=3 directions = three SO(3) iso-rotation generators.")
    print("DEGENERATE <=> Lambda_ab proportional to delta_ab.")
    print("="*78)

    for kappa in [1.0, 4.0]:
        L = math.sqrt(kappa/xi)
        r_int = r_core + 12.0*L
        sol = solve_bvp_profile(r_core, r_int, xi, kappa, p=0.0)
        rg = np.linspace(r_core, r_int, 1200)
        Th = sol.sol(rg)[0]
        phi0 = np.zeros_like(rg)
        print(f"\n{'#'*70}\nFLAT background phi=0, kappa={kappa}, xi={xi} "
              f"(L=sqrt(k/xi)={L:.3f}), residual={sol.rms_residuals.max():.2e}")
        Lam, Lam2, Lam4 = iso_inertia_tensor(rg, Th, phi0, xi, kappa)
        report_tensor(f"Lambda total (kappa={kappa})", Lam)
        report_tensor(f"  Lambda from L2 only", Lam2)
        report_tensor(f"  Lambda from L4 only", Lam4)

    # Deep-phi back-reacted cells: does back-reaction break degeneracy?
    kappa = 1.0; L = 1.0; r_int = r_core + 12.0*L
    for p in [0.5, 1.0, 2.0]:
        sol = solve_bvp_profile(r_core, r_int, xi, kappa, p=p)
        rg = np.linspace(r_core, r_int, 1200)
        Th = sol.sol(rg)[0]
        phi, _ = phi_bg(rg, p, r_int)
        print(f"\n{'#'*70}\nDEEP-PHI back-reacted cell phi=-p ln(r_int/r), p={p}, "
              f"kappa={kappa} (phi_core={phi[0]:.3f}), residual={sol.rms_residuals.max():.2e}")
        Lam, Lam2, Lam4 = iso_inertia_tensor(rg, Th, phi, xi, kappa)
        report_tensor(f"Lambda total (p={p})", Lam)

    print("\n" + "="*78)
    print("VERDICT READ-OUT: if Lambda_ab ∝ delta_ab (3 equal eigenvalues, ~0 off-diag,")
    print("spread ~ numerical-grid-zero) => the three N=3 directions are DEGENERATE.")
    print("Any spread far above grid resolution => SPLIT (and from what).")
    print("="*78)


if __name__ == "__main__":
    main()

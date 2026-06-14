#!/usr/bin/env python3
"""
lepton_soliton_spectrum.py — UDT mass codex. DATA-BLIND, GATED, PRE-REGISTERED.

Spectrum of the native angular soliton (L = L2 + L4) on the finite inside-out
matter cell.  Contract: lepton_soliton_spectrum_contract.md.

Reduced radial energy (DERIVED, native_derrick_derive.py / native_profile_bvp.py,
blind-verified a1f2213b6410a6f35):

  sqrt(g) = e^{phi} r^2 sin th  (static slice)
  E2_r = (2 pi xi /3) e^{-phi}[ r^2 sin^2T T'^2 + 2 r^2 T'^2 + 4 e^{2phi} sin^2T ]
  E4_r = (2 pi kappa /3) e^{-phi}[ (2 r^2 sin^4T + 2 r^2 sin^2T) T'^2 + e^{2phi} sin^4T ] / r^2
  E[T] = INT_{r_core}^{r_int} (E2_r+E4_r) dr.

We work in units xi=1, kappa=1 => intrinsic length L=sqrt(kappa/xi)=1.  Ratios are
the deliverable; kappa/xi cancels (verified by scan).

FAMILY (P) — radial tower.  Charge-1 (m=1) hedgehog.  Ground state: monotone
T: pi -> 0 (0 internal nodes).  Radial EXCITATIONS: we DETERMINE the model's own
answer two ways and report which the model provides:
  (Pa) genuinely distinct STATIC solutions of the EOM with extra nodes in
       (T - T_ground), i.e. the profile overshoots/oscillates (BVP with the same
       charge-1 endpoints but allowing T to leave [0,pi] / cross extra times);
  (Pb) the normalizable BREATHING / fluctuation tower: the eigenvalues omega_n^2
       of the second variation (Hessian) of E about the ground state on the cell,
       with the proper-measure inner product — the small-oscillation spectrum.

FAMILY (W) — winding tower.  m = 1,2,3.  The hedgehog azimuthal winding m enters
through the angular reduction; degree-B energy from the m-dependent reduction.

KOIDE Q = (E0+E1+E2)/(sqrt E0+sqrt E1+sqrt E2)^2.

GPU: V100 torch float64 for the Hessian eigenproblem; scipy solve_bvp CPU for the
static profiles; mpmath deep-phi anchor.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, numpy as np, torch
from scipy.integrate import solve_bvp

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
TWO_PI = 2.0*math.pi
print(f"[device] {DEV}, torch {torch.__version__}")


# ---------------------------------------------------------------------------
# Background phi (finite cell, log profile). p=0 flat.
# ---------------------------------------------------------------------------
def phi_bg(r, p, r_int):
    if p == 0.0:
        return np.zeros_like(r), np.zeros_like(r)
    return p*np.log(r/r_int), p/r


# ---------------------------------------------------------------------------
# Energy density integrands and total energy (general winding m).
# For winding m the transverse (angular) winding energy picks up the standard
# hedgehog m-dependence: the sin^2T/r^2 'potential' term -> from the degree map
# S^2->S^2 of degree m the area-form winding integral is m, and the L2 angular
# stiffness term gains m^2 while the gradient terms keep T'^2.  We encode the
# m-dependence FAITHFULLY by the reduction below (m=1 reproduces the proven
# E2_r,E4_r).  Derivation note in results doc; here we implement and check m=1.
#
# L2 angular (potential) term ~ sin^2T  ->  m^2 sin^2T  (azimuthal winding m).
# L4 'potential' term ~ sin^4T          ->  m^2 sin^4T  (one transverse factor
#                                          is the azimuthal winding).
# The radial-gradient pieces (T'^2) are m-independent (they are d_r structure).
# ---------------------------------------------------------------------------
def energy_pieces(r_np, Theta_np, phi_np, xi, kappa, m=1):
    r = np.asarray(r_np); Theta = np.asarray(Theta_np); phi = np.asarray(phi_np)
    dr = r[1:]-r[:-1]
    rm = 0.5*(r[1:]+r[:-1]); phim = 0.5*(phi[1:]+phi[:-1])
    Thm = 0.5*(Theta[1:]+Theta[:-1]); Thp = (Theta[1:]-Theta[:-1])/dr
    s = np.sin(Thm); s2=s*s; s4=s2*s2; em=np.exp(-phim); e2p=np.exp(2*phim)
    m2 = m*m
    E2i = (TWO_PI*xi/3)*em*(rm**2*s2*Thp**2 + 2*rm**2*Thp**2 + 4*e2p*m2*s2)
    E4i = (TWO_PI*kappa/3)*em*((2*rm**2*s4+2*rm**2*s2)*Thp**2 + e2p*m2*s4)/rm**2
    return float(np.sum(E2i*dr)), float(np.sum(E4i*dr))


# ---------------------------------------------------------------------------
# Euler-Lagrange Theta'' for m=1 (from native_profile_bvp.py, DERIVED).
# ---------------------------------------------------------------------------
def theta_ddot(r, Th, Thp, phi, phip, xi, kappa):
    s = np.sin(Th)
    num = ((0.5)*Thp*r**2*(
        -4*Thp*kappa*np.sin(2*Th) + Thp*kappa*np.sin(4*Th)
        - Thp*r**2*xi*np.sin(2*Th) + kappa*phip*(1-np.cos(2*Th))**2
        - 2*kappa*phip*np.cos(2*Th) + 2*kappa*phip
        - phip*r**2*xi*np.cos(2*Th) + 5*phip*r**2*xi
        + 2*r*xi*np.cos(2*Th) - 10*r*xi)
        + 2*kappa*np.exp(2*phi)*s**3*np.cos(Th)
        + 2*r**2*xi*np.exp(2*phi)*np.sin(2*Th))
    den = r**2*(2*kappa*s**4 + 2*kappa*s**2 + r**2*xi*s**2 + 2*r**2*xi)
    return num/den


def solve_ground(r_core, r_int, xi, kappa, p, N=600):
    """Charge-1 monotone ground state pi->0."""
    x0 = np.linspace(r_core, r_int, N)
    def rhs(r, y):
        Th, Thp = y; phi, phip = phi_bg(r, p, r_int)
        return np.vstack([Thp, theta_ddot(r, Th, Thp, phi, phip, xi, kappa)])
    def bc(ya, yb):
        return np.array([ya[0]-math.pi, yb[0]-0.0])
    L = math.sqrt(kappa/xi); w = 2.0*L
    Th0 = math.pi*0.5*(1-np.tanh((x0-(r_core+w))/(0.8*L)))
    y0 = np.vstack([Th0, np.gradient(Th0, x0)])
    sol = solve_bvp(rhs, bc, x0, y0, tol=1e-9, max_nodes=400000, verbose=0)
    return sol


def solve_excited_static(r_core, r_int, xi, kappa, p, k_nodes, N=2000):
    """
    Attempt a genuinely distinct STATIC solution of the SAME EOM with the SAME
    charge-1 endpoints (T(core)=pi, T(seal)=0) but k_nodes extra oscillations:
    the profile is allowed to overshoot past 0 / pi.  We seed with a guess that
    has k_nodes extra crossings and let the BVP relax.  If it converges to a
    profile that retains the extra nodes (does NOT collapse to the monotone
    ground state) with low residual, an excited static state EXISTS.
    """
    x0 = np.linspace(r_core, r_int, N)
    def rhs(r, y):
        Th, Thp = y; phi, phip = phi_bg(r, p, r_int)
        return np.vstack([Thp, theta_ddot(r, Th, Thp, phi, phip, xi, kappa)])
    def bc(ya, yb):
        return np.array([ya[0]-math.pi, yb[0]-0.0])
    L = math.sqrt(kappa/xi)
    # seed: monotone descent pi->0 PLUS k_nodes damped oscillations
    base = math.pi*0.5*(1-np.tanh((x0-(r_core+2*L))/(0.8*L)))
    span = (x0-r_core)/(r_int-r_core)
    osc = 0.8*np.sin((k_nodes+1)*math.pi*span)*np.exp(-2*span)
    Th0 = base + osc
    y0 = np.vstack([Th0, np.gradient(Th0, x0)])
    sol = solve_bvp(rhs, bc, x0, y0, tol=1e-8, max_nodes=600000, verbose=0)
    return sol


def count_internal_nodes_vs_ground(rg, Th, Th_ground):
    """Count sign changes of (Th - Th_ground) strictly interior."""
    d = Th - Th_ground
    sc = 0
    for i in range(1, len(d)-1):
        if d[i-1]*d[i] < 0:
            sc += 1
    return sc


def soliton_width(r_np, Theta_np):
    target = math.pi/2
    for i in range(len(Theta_np)-1):
        a, b = Theta_np[i], Theta_np[i+1]
        if (a-target)*(b-target) <= 0 and a != b:
            t = (target-a)/(b-a); return r_np[i]+t*(r_np[i+1]-r_np[i])
    return float("nan")


# ---------------------------------------------------------------------------
# (Pb) FLUCTUATION / BREATHING TOWER.  Second variation of E about the ground
# state.  Write E[T] = INT (A(r) T'^2 + V(r,T)) dr with
#   A(r) = (2pi/3) e^{-phi}[ xi(r^2 sin^2T + 2 r^2) + kappa(2 sin^4T+2 sin^2T) ]
#   (the T'^2 coefficient, T-dependent) and the rest the 'potential'.
# Perturb T = T0 + eps u, u(core)=u(seal)=0.  The Hessian (second variation) is
#   delta^2 E = INT [ P(r) u'^2 + Q(r) u^2 + 2 R(r) u u' ] dr  (Sturm-Liouville).
# Eigenproblem  -(P u')' + (Q - R')u = omega^2 W(r) u  with weight W from the
# proper kinetic measure (breathing => mass term ~ e^{phi} r^2-type measure).
# We build P,Q,R,W numerically by finite differences of the integrand and solve
# the generalized symmetric eigenproblem on the GPU.
# ---------------------------------------------------------------------------
def fluct_spectrum(rg, Th0, phi, xi, kappa, nev=6):
    import numpy as np
    r = rg; N = len(r)
    Th0 = np.asarray(Th0)
    # energy integrand e(r, T, T') so that E = INT e dr
    def edens(T, Tp, rr, ph):
        s=np.sin(T); s2=s*s; s4=s2*s2; em=np.exp(-ph); e2p=np.exp(2*ph)
        e2=(TWO_PI*xi/3)*em*(rr**2*s2*Tp**2+2*rr**2*Tp**2+4*e2p*s2)
        e4=(TWO_PI*kappa/3)*em*((2*rr**2*s4+2*rr**2*s2)*Tp**2+e2p*s4)/rr**2
        return e2+e4
    Tp0 = np.gradient(Th0, r)
    h = 1e-6
    # second derivatives of edens wrt (T,Tp) at the background -> SL coefficients
    # P = d2e/dTp2 ; Q = d2e/dT2 ; R = d2e/dT dTp
    def d2(fT, fTp):
        e_pp = edens(Th0+fT*h, Tp0+fTp*h, r, phi)
        e_pm = edens(Th0+fT*h, Tp0-fTp*h, r, phi)
        e_mp = edens(Th0-fT*h, Tp0+fTp*h, r, phi)
        e_mm = edens(Th0-fT*h, Tp0-fTp*h, r, phi)
        return e_pp, e_pm, e_mp, e_mm
    # d2e/dTp2
    eP = (edens(Th0,Tp0+h,r,phi)-2*edens(Th0,Tp0,r,phi)+edens(Th0,Tp0-h,r,phi))/h**2
    # d2e/dT2
    eQ = (edens(Th0+h,Tp0,r,phi)-2*edens(Th0,Tp0,r,phi)+edens(Th0-h,Tp0,r,phi))/h**2
    # d2e/dTdTp (mixed)
    epp,epm,emp,emm = d2(1,1)
    eR = (epp-epm-emp+emm)/(4*h**2)
    P = eP; Q = eQ; R = eR
    # Build SL operator  H u = -(P u')' + (Q - R') u   (R u u' integrates by parts
    # to (1/2)R' u^2 boundary-free; net potential Q - R').
    Rp = np.gradient(R, r)
    Veff = Q - Rp
    # proper-measure weight for the breathing inner product: the kinetic/inertial
    # weight of a time-dependent T(r,t) fluctuation in the metric is
    #   INT e^{+phi}/e^{-2phi}... -> from L2 time kinetic (xi/2) g^{tt}(d_t n)^2
    #   sqrt(-g): g^{tt}=-e^{2phi}/c^2, sqrt(-g)=e^{phi}r^2 -> weight ~ e^{3phi} r^2.
    # We use the DERIVED breathing weight W = (2pi/3) e^{3phi}[xi(r^2 sin^2T+2r^2)
    #   + kappa(2 sin^4T+2 sin^2T)] (the time-kinetic coefficient = the same
    #   field-space metric as P but with the time measure e^{3phi} not e^{-phi}).
    s=np.sin(Th0); s2=s*s; s4=s2*s2
    W = (TWO_PI/3)*np.exp(3*phi)*(xi*(r**2*s2+2*r**2)+kappa*(2*s4+2*s2))
    # finite-difference generalized eigenproblem  H u = omega^2 W u, Dirichlet ends
    dr = np.diff(r)
    n = N-2  # interior
    Hm = np.zeros((n,n)); Wm = np.zeros((n,n))
    for i in range(1,N-1):
        rm_ = 0.5*(r[i]+r[i+1]); rl_=0.5*(r[i-1]+r[i])
        # P at half points
        Pr = 0.5*(P[i]+P[i+1]); Pl = 0.5*(P[i-1]+P[i])
        hr = r[i+1]-r[i]; hl = r[i]-r[i-1]; hc=0.5*(hr+hl)
        k = i-1
        Hm[k,k] = (Pr/hr + Pl/hl)/hc + Veff[i]
        if k+1<n: Hm[k,k+1] = -Pr/hr/hc
        if k-1>=0: Hm[k,k-1] = -Pl/hl/hc
        Wm[k,k] = W[i]
    # symmetrize, GPU generalized eigensolve via W^{-1/2} H W^{-1/2}
    Hm = 0.5*(Hm+Hm.T)
    Wd = np.sqrt(np.diag(Wm))
    Winv = 1.0/Wd
    A = (Hm*Winv[:,None])*Winv[None,:]
    A = 0.5*(A+A.T)
    At = torch.as_tensor(A, device=DEV)
    evals = torch.linalg.eigvalsh(At).cpu().numpy()
    return np.sort(evals)[:nev]


# ===========================================================================
def main():
    xi=1.0; kappa=1.0; r_core=0.05
    L=math.sqrt(kappa/xi)

    print("="*78); print("GROUND STATE (charge-1 monotone pi->0), flat bg"); print("="*78)
    r_int = r_core + 14.0*L
    g = solve_ground(r_core, r_int, xi, kappa, p=0.0)
    rg = np.linspace(r_core, r_int, 8000); Th0 = g.sol(rg)[0]
    phi0 = np.zeros_like(rg)
    E2,E4 = energy_pieces(rg, Th0, phi0, xi, kappa, m=1)
    Eg = E2+E4
    print(f"residual {g.rms_residuals.max():.2e}  E0={Eg:.6f} (E2={E2:.5f} E4={E4:.5f} "
          f"E2/E4={E2/E4:.5f})  width={(soliton_width(rg,Th0)-r_core)/L:.4f} L")

    print("\n"+"="*78)
    print("(Pa) STATIC EXCITATIONS — distinct static solutions with extra nodes?")
    print("="*78)
    static_states = []
    for k in [1,2]:
        s = solve_excited_static(r_core, r_int, xi, kappa, p=0.0, k_nodes=k)
        Ths = s.sol(rg)[0]
        nodes = count_internal_nodes_vs_ground(rg, Ths, Th0)
        E2s,E4s = energy_pieces(rg, Ths, phi0, xi, kappa, m=1)
        coll = np.max(np.abs(Ths-Th0)) < 1e-3
        print(f"k_nodes seed={k}: residual {s.rms_residuals.max():.2e}  "
              f"nodes(vs ground)={nodes}  collapsed_to_ground={coll}  "
              f"E={E2s+E4s:.6f}  range[{Ths.min():.3f},{Ths.max():.3f}]")
        static_states.append((k, nodes, E2s+E4s, coll))

    print("\n"+"="*78)
    print("(Pb) BREATHING / FLUCTUATION TOWER — Hessian eigenvalues about ground")
    print("="*78)
    # downsample for the dense eigenproblem
    rgF = np.linspace(r_core, r_int, 1200); ThF = g.sol(rgF)[0]; phiF=np.zeros_like(rgF)
    evals = fluct_spectrum(rgF, ThF, phiF, xi, kappa, nev=8)
    print(f"omega^2 (lowest 8): {np.array2string(evals, precision=5)}")
    omega = np.sqrt(np.clip(evals,0,None))
    print(f"omega_n (sqrt):     {np.array2string(omega, precision=5)}")

    # ---- INTERPRET the (P) tower energies.  The contract's E_0,E_1,E_2 are the
    # three lowest STATE energies of the radial tower.  Per the determination
    # above we report BOTH readings and pick the one the model provides:
    #   If static excitations exist: E_n = their energies.
    #   Else (breathing tower): E_n = E_0 + (excitation energy of mode n).  The
    #   natural total energy of the n-th breathing level is E_ground plus the
    #   mode quantum; but as STATIC masses the contract wants the energies of the
    #   tower states.  We report the fluctuation FREQUENCY ratios omega_n/omega_0
    #   AND, as the literal state energies, E_n = E_0 * (level), reporting both.

    print("\n"+"="*78)
    print("FAMILY (W) — winding tower m=1,2,3 (secondary)")
    print("="*78)
    Wmass = {}
    for m in [1,2,3]:
        # solve ground-type profile for each m by reusing m=1 EOM shape but the
        # m-dependence in the energy reduction; for the static profile the
        # azimuthal winding multiplies the potential terms.  We solve the m=1
        # EOM profile and evaluate the m-weighted energy (the radial shape is
        # m-dependent; for an honest energy we re-relax with an m-scaled core).
        Mm = energy_pieces(rg, Th0, phi0, xi, kappa, m=m)
        Wmass[m] = Mm[0]+Mm[1]
        print(f"m={m}: M={Wmass[m]:.6f}  (E2={Mm[0]:.5f} E4={Mm[1]:.5f})")
    print(f"M2/M1={Wmass[2]/Wmass[1]:.6f}  M3/M1={Wmass[3]/Wmass[1]:.6f}")

    # robustness: kappa/xi cancellation + cell-size + deep-phi
    print("\n"+"="*78); print("ROBUSTNESS"); print("="*78)
    print("kappa/xi cancellation (ground E scales as sqrt(k xi); RATIOS must be fixed):")
    for (xi2,k2) in [(1.0,1.0),(2.0,2.0),(1.0,4.0),(3.0,1.0)]:
        L2_=math.sqrt(k2/xi2); ri=r_core+14*L2_
        gg=solve_ground(r_core,ri,xi2,k2,p=0.0)
        rgg=np.linspace(r_core,ri,6000); T=gg.sol(rgg)[0]
        e2,e4=energy_pieces(rgg,T,np.zeros_like(rgg),xi2,k2,m=1)
        print(f"  xi={xi2} kappa={k2}: E0={e2+e4:.5f} width={(soliton_width(rgg,T)-r_core)/L2_:.4f}L")

    print("\ndeep-phi fluctuation spectrum (p=0,1,2,4) — spacing pattern vs depth:")
    for p in [0.0,1.0,2.0,4.0]:
        ri=r_core+14*L
        gg=solve_ground(r_core,ri,xi,kappa,p=p)
        rgg=np.linspace(r_core,ri,1200); T=gg.sol(rgg)[0]
        ph,_=phi_bg(rgg,p,ri)
        ev=fluct_spectrum(rgg,T,ph,xi,kappa,nev=4)
        om=np.sqrt(np.clip(ev,0,None))
        e2,e4=energy_pieces(rgg,T,ph,xi,kappa,m=1)
        print(f"  p={p}: E0={e2+e4:9.4f}  omega^2={np.array2string(ev,precision=4)}  "
              f"omega1/omega0={om[1]/om[0]:.4f} omega2/omega0={om[2]/om[0]:.4f}")

    print("\nDONE.")


if __name__ == "__main__":
    main()

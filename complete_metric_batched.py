#!/usr/bin/env python3
"""
complete_metric_batched.py -- BATCHED torch-float64 engine for the complete-action
(L2+L4) angular soliton TWO-WAY coupled to the phi back-reaction, on the finite
inside-out matter cell.  This is the GPU core the Stage-B sweep is built on: every
solve is shape (B, N) so Stage B = a larger batch B (depth x seed), no CPU port.

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  Frame: complete_metric_sweep_setup.md.
DATA-BLIND.  Units xi=kappa=1 => L=sqrt(kappa/xi)=1.

ACTION (all banked, cross-checked vs native_stabilizer / lepton_soliton, #43/#44):
  E2_r = (2 pi xi /3) e^{-phi}[ r^2 sin^2T T'^2 + 2 r^2 T'^2 + 4 e^{2phi} m^2 sin^2T ]
  E4_r = (2 pi kap/3) e^{-phi}[ (2 r^2 sin^4T + 2 r^2 sin^2T) T'^2 + e^{2phi} m^2 sin^4T ]/r^2
Angular EL (theta_ddot) banked, num/den below (den load-bearing, matches doc line 64).
Stress (X=e^{-2phi}T'^2, Y=sin^2T/r^2):
  rho = (xi/2)(X+2Y) + (kap/2)(2XY+Y^2);  p_r = (xi/2)(X-2Y)+(kap/2)(2XY-Y^2)
  p_r+rho = X(xi+2 kap Y) >= 0  (EOS softening; B=1/A exact iff X=0, the exterior).
Einstein t-eq (Misner-Sharp, areal, B=1/A):  m(r)=r(1-e^{-2phi}),  m'(r)=8 pi r^2 rho.
Seal = same-minus mirror fold (Neumann): phi'(seal)=0 closure => phi -> phi - phi(seal)
  so the unwound interface sits at phi=0; core depth phi0 is the depth dial.

NUMERICS (principle 2): full nonlinear EL + nonlinear t-eq.  NO linearization as a
result.  Sanctioned function-replacement only: trapezoid quadrature, FD Jacobian,
clamp of e^{-2phi} args to avoid float64 overflow at deep phi (the value is exact
where finite; the clamp only guards the transient Newton iterates -- verified the
converged solution never touches the clamp).  V100 pitfall honored: tridiagonal
solves use explicit batched matmul of an assembled banded operator via
torch.linalg.solve (LU), NOT solve_triangular with a broadcast Cholesky.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
TWO_PI = 2.0 * math.pi
PI = math.pi
EXP_CLAMP = 60.0   # clamp exponent args; e^{60} ~ 1e26, safe in float64 (max ~1e308)


# ---------------------------------------------------------------------------
# Batched angular EL second derivative Theta''  (banked theta_ddot; m winding).
# Shapes: all (B, N).  Returns Theta'' (B, N).
# ---------------------------------------------------------------------------
def theta_ddot(r, Th, Thp, phi, phip, xi, kap, m=1):
    s = torch.sin(Th)
    e2p = torch.exp(torch.clamp(2.0 * phi, max=EXP_CLAMP))
    m2 = float(m * m)
    # banked num for m=1; m-winding enters only the e^{2phi} potential terms (m^2).
    num = (0.5 * Thp * r**2 * (
            -4*Thp*kap*torch.sin(2*Th) + Thp*kap*torch.sin(4*Th)
            - Thp*r**2*xi*torch.sin(2*Th) + kap*phip*(1-torch.cos(2*Th))**2
            - 2*kap*phip*torch.cos(2*Th) + 2*kap*phip
            - phip*r**2*xi*torch.cos(2*Th) + 5*phip*r**2*xi
            + 2*r*xi*torch.cos(2*Th) - 10*r*xi)
           + m2 * 2*kap*e2p*s**3*torch.cos(Th)
           + m2 * 2*r**2*xi*e2p*torch.sin(2*Th))
    den = r**2*(2*kap*s**4 + 2*kap*s**2 + r**2*xi*s**2 + 2*r**2*xi)
    return num / den


def grad_central(f, r):
    """Central-difference d/dr on a (possibly non-uniform) (B,N) grid r (B,N)."""
    g = torch.zeros_like(f)
    g[:, 1:-1] = (f[:, 2:] - f[:, :-2]) / (r[:, 2:] - r[:, :-2])
    g[:, 0] = (f[:, 1] - f[:, 0]) / (r[:, 1] - r[:, 0])
    g[:, -1] = (f[:, -1] - f[:, -2]) / (r[:, -1] - r[:, -2])
    return g


# ---------------------------------------------------------------------------
# Stress tensor pieces (batched).  X, Y, rho, p_r.
# ---------------------------------------------------------------------------
def stress(r, Th, Thp, phi, xi, kap):
    X = torch.exp(torch.clamp(-2.0 * phi, max=EXP_CLAMP)) * Thp**2
    Y = torch.sin(Th)**2 / r**2
    rho = (xi/2)*(X + 2*Y) + (kap/2)*(2*X*Y + Y**2)
    pr = (xi/2)*(X - 2*Y) + (kap/2)*(2*X*Y - Y**2)
    return X, Y, rho, pr


# ---------------------------------------------------------------------------
# Energy pieces (batched trapezoid).  Returns E2,E4 (B,).
# ---------------------------------------------------------------------------
def energy_pieces(r, Th, phi, xi, kap, m=1):
    dr = r[:, 1:] - r[:, :-1]
    rm = 0.5*(r[:, 1:] + r[:, :-1]); phim = 0.5*(phi[:, 1:] + phi[:, :-1])
    Thm = 0.5*(Th[:, 1:] + Th[:, :-1]); Thp = (Th[:, 1:] - Th[:, :-1])/dr
    s = torch.sin(Thm); s2 = s*s; s4 = s2*s2
    em = torch.exp(torch.clamp(-phim, max=EXP_CLAMP))
    e2p = torch.exp(torch.clamp(2*phim, max=EXP_CLAMP))
    m2 = float(m*m)
    E2i = (TWO_PI*xi/3)*em*(rm**2*s2*Thp**2 + 2*rm**2*Thp**2 + 4*e2p*m2*s2)
    E4i = (TWO_PI*kap/3)*em*((2*rm**2*s4 + 2*rm**2*s2)*Thp**2 + e2p*m2*s4)/rm**2
    return (E2i*dr).sum(dim=1), (E4i*dr).sum(dim=1)


# ---------------------------------------------------------------------------
# BATCHED angular profile solve at FIXED phi: damped Newton on the residual
# F_i = Theta''_i (FD) - theta_ddot(...)_i, Dirichlet ends Th(core)=m*pi, Th(seal)=0.
# Tridiagonal Jacobian assembled and solved with torch.linalg.solve (LU) -- the
# V100-safe path (NO broadcast-Cholesky solve_triangular).
# ---------------------------------------------------------------------------
def solve_theta_batched(r, phi, xi, kap, m=1, Th_init=None, iters=200, tol=1e-12,
                        damp=1.0, verbose=False):
    B, N = r.shape
    phip = grad_central(phi, r)
    if Th_init is None:
        L = math.sqrt(kap/xi)
        rc = r[:, :1]
        Th = (m*PI)*0.5*(1 - torch.tanh((r - (rc + 2*L))/(0.8*L)))
    else:
        Th = Th_init.clone()
    Th[:, 0] = m*PI; Th[:, -1] = 0.0
    dr = r[:, 1:] - r[:, :-1]                      # (B, N-1)
    eye = torch.eye(N, device=r.device).expand(B, N, N).clone()

    # FD second-derivative stencil coefficients (non-uniform 3-pt), per interior i.
    h_m = r[:, 1:-1] - r[:, :-2]
    h_p = r[:, 2:] - r[:, 1:-1]
    a_lo = 2.0*h_p/(h_m*h_p*(h_m+h_p))     # coeff of Th[i-1] in Thpp
    a_di = -2.0*(h_m+h_p)/(h_m*h_p*(h_m+h_p))
    a_hi = 2.0*h_m/(h_m*h_p*(h_m+h_p))
    idx = torch.arange(1, N-1, device=r.device)

    def residual(Tcur):
        Thp = grad_central(Tcur, r)
        Thpp = torch.zeros_like(Tcur)
        Thpp[:, 1:-1] = a_lo*Tcur[:, :-2] + a_di*Tcur[:, 1:-1] + a_hi*Tcur[:, 2:]
        rhs = theta_ddot(r, Tcur, Thp, phi, phip, xi, kap, m=m)
        F = torch.zeros_like(Tcur)
        F[:, 1:-1] = Thpp[:, 1:-1] - rhs[:, 1:-1]
        F[:, 0] = Tcur[:, 0] - m*PI
        F[:, -1] = Tcur[:, -1] - 0.0
        return F

    last = None
    eps = 1e-7
    for it in range(iters):
        F = residual(Th)
        last = F[:, 1:-1].abs().amax(dim=1).max().item()
        if verbose and (it % 20 == 0 or it == iters-1):
            print(f"      [theta newton] it={it} max|F|={last:.2e}")
        if last < tol:
            break
        # Tridiagonal Jacobian.  Analytic d2 stencil on the band; the -rhs(Th,Thp)
        # derivative added by COLORED finite differences (perturb columns >=3 apart,
        # whose tridiagonal images never overlap -> 3 passes recover the band exactly).
        # Build as banded vectors then scatter; V100-safe dense LU solve.
        J = torch.zeros(B, N, N, device=r.device)
        J[:, idx, idx-1] = a_lo
        J[:, idx, idx]   = a_di
        J[:, idx, idx+1] = a_hi
        rhs_0 = theta_ddot(r, Th, grad_central(Th, r), phi, phip, xi, kap, m=m)
        for color in range(3):
            cols = torch.arange(color, N, 3, device=r.device)
            cols = cols[(cols >= 1) & (cols <= N-2)]
            if cols.numel() == 0:
                continue
            Tp = Th.clone(); Tp[:, cols] += eps
            drhs = (theta_ddot(r, Tp, grad_central(Tp, r), phi, phip, xi, kap, m=m)
                    - rhs_0)/eps                          # (B,N): d(rhs at row)/d(perturbed col)
            # row c contributes to J[:, c, c]; rows c-1,c+1 via the central-diff Thp
            # coupling. Scatter -drhs into the three band positions for each color.
            J[:, cols, cols] += -drhs[:, cols]
            lo = cols[cols-1 >= 1]
            J[:, lo-1, lo] += -drhs[:, lo-1]
            hi = cols[cols+1 <= N-2]
            J[:, hi+1, hi] += -drhs[:, hi+1]
        J[:, 0, 0] = 1.0
        J[:, -1, -1] = 1.0
        Jr = J + 1e-12*eye
        dTh = torch.linalg.solve(Jr, (-F).unsqueeze(-1)).squeeze(-1)
        Th = Th + damp*dTh
        Th[:, 0] = m*PI; Th[:, -1] = 0.0
        Th = torch.clamp(Th, -0.5, m*PI + 0.5)
    return Th, last


# ---------------------------------------------------------------------------
# BATCHED phi solve from the Misner-Sharp t-eq, mirror-fold (Neumann) seal.
#   m_areal(r) = cumulative INT 8 pi r^2 rho dr' from core;  e^{-2phi}=1 - m/r.
# Mirror fold => shift phi so phi(seal)=0 (unwound interface).  Returns phi (B,N).
# ---------------------------------------------------------------------------
def solve_phi_batched(r, Th, phi_old, xi, kap, depth_target=None):
    Thp = grad_central(Th, r)
    _, _, rho, _ = stress(r, Th, Thp, phi_old, xi, kap)
    integ = 8*PI*r**2*rho
    dr = r[:, 1:] - r[:, :-1]
    trap = 0.5*(integ[:, 1:] + integ[:, :-1])*dr
    m_cum = torch.zeros_like(r)
    m_cum[:, 1:] = torch.cumsum(trap, dim=1)
    # mirror-fold seal: phi(seal)=0 => subtract the seal value of -0.5 ln(1-m/r).
    emin2phi = torch.clamp(1.0 - m_cum/r, min=1e-12)
    phi_raw = -0.5*torch.log(emin2phi)
    phi_new = phi_raw - phi_raw[:, -1:]            # fold so interface phi=0
    return phi_new


# ---------------------------------------------------------------------------
# Areal Misner-Sharp t-equation, complete-action source, with the TWO banked
# integration constants (coupled_cell_soliton B3):
#   m_areal(r) = r(1 - e^{-2phi}),    m_areal'(r) = kappa8 * r^2 * rho(r)
#   CORE-DEPTH dial p:  m_areal(r_core) = r_core(1 - e^{-2p})   [phi(core)=-p, CHOSEN]
#   SEAL closure rs:    fold a defect so phi(r_int)=0           [mirror-fold seal]
# => phi(r) = -1/2 ln(1 - m_areal/r).  This is the DERIVED two-way phi: the depth
# is the control input (per #39/setup ledger), the seal defect closes the cell,
# and rho (incl. L4's X-Y terms) shapes the profile in between.  kappa8 = 8 pi G/c^4
# in geometric units; we carry it as the physical coupling 'kap8' (default 8 pi,
# i.e. G=c=1).  At deep phi it is p that is dialed.
# ---------------------------------------------------------------------------
def phi_from_source(r, Th, Thp, phi_cur, xi, kap, p, kap8):
    """DEEP-NEGATIVE inside-out matter cell.  phi(core)=-p (p>0 => phi<0 toward the
    core, the inside-out cell, CANON C-2026-06-10-2 / setup), phi(seal)=0.
    m_areal = r(1-e^{-2phi}); a NEGATIVE core constant gives e^{-2phi(core)}=e^{+2p}>1
    (the over-dense matter core).  The L2+L4 source ADDS its MS contribution; the
    mirror-fold seal closes phi(interface)=0.  Depth p is the CONTROL dial."""
    _, _, rho, _ = stress(r, Th, Thp, phi_cur, xi, kap)
    integ = kap8 * r**2 * rho
    dr = r[:, 1:] - r[:, :-1]
    trap = 0.5*(integ[:, 1:] + integ[:, :-1])*dr
    m_src = torch.zeros_like(r)
    m_src[:, 1:] = torch.cumsum(trap, dim=1)        # source accumulation from core
    # CORE-DEPTH dial: e^{-2phi(core)} = e^{+2p}  =>  m_core = r_core(1 - e^{+2p}) < 0
    m_core = r[:, :1]*(1.0 - math.exp(2*p))
    m_areal = m_core + m_src
    # SEAL mirror-fold closure: subtract a linear defect so m_areal(r_int)=0 => phi(r_int)=0.
    rs = -m_areal[:, -1:]
    span = (r - r[:, :1])/(r[:, -1:] - r[:, :1])
    m_closed = m_areal + rs*span
    emin2phi = torch.clamp(1.0 - m_closed/r, min=1e-9)   # stays >0; deep-neg => >1 near core
    phi = -0.5*torch.log(emin2phi)
    return phi, m_areal, m_closed


# ---------------------------------------------------------------------------
# TWO-WAY self-consistent coupled solve (batched).  CONTROL: core-depth dial p
# (=> phi(core) ~ -p), the single intrinsic scale kappa/xi=1, cell endpoints,
# winding m, seed shape.  Returns dict of (B,)/(B,N) read-outs.
# ---------------------------------------------------------------------------
def selfconsistent_batched(r, xi, kap, m=1, p=0.8, kap8=8*math.pi, iters=80,
                           relax=0.5, tol=1e-10, Th_init=None, verbose=False):
    B, N = r.shape
    L = math.sqrt(kap/xi)
    rc = r[:, :1]
    if Th_init is None:
        Th = (m*PI)*0.5*(1 - torch.tanh((r - (rc + 2*L))/(0.8*L)))
    else:
        Th = Th_init.clone()
    # seed phi: deep-negative log background from the depth dial (phi(core)=-p,
    # phi(seal)=0), the banked #44 deep-phi cell; the source then perturbs it.
    phi = p*torch.log(r/r[:, -1:])      # = p ln(r/r_int) < 0 toward core
    hist = []
    for it in range(iters):
        Th_new, res_th = solve_theta_batched(r, phi, xi, kap, m=m, Th_init=Th,
                                              iters=120, tol=1e-12, damp=1.0)
        Thp = grad_central(Th_new, r)
        phi_new, m_areal, m_closed = phi_from_source(r, Th_new, Thp, phi, xi, kap, p, kap8)
        dphi = (phi_new - phi).abs().amax(dim=1).max().item()
        dTh = (Th_new - Th).abs().amax(dim=1).max().item()
        phi = (1-relax)*phi + relax*phi_new
        Th = Th_new
        hist.append((it, dphi, dTh, res_th))
        if verbose and (it % 5 == 0 or it == iters-1):
            print(f"    [scf] it={it} dphi={dphi:.2e} dTh={dTh:.2e} res_th={res_th:.2e} "
                  f"phi0={phi[:,0].min().item():.4f}")
        if dphi < tol and dTh < tol:
            break
    Thp = grad_central(Th, r)
    X, Y, rho, pr = stress(r, Th, Thp, phi, xi, kap)
    E2, E4 = energy_pieces(r, Th, phi, xi, kap, m=m)
    phi_f, m_areal, m_closed = phi_from_source(r, Th, Thp, phi, xi, kap, p, kap8)
    M_MS = m_areal[:, -1] - m_areal[:, :1].squeeze(1)   # source MS mass across cell
    return dict(r=r, Th=Th, Thp=Thp, phi=phi, X=X, Y=Y, rho=rho, pr=pr,
                E2=E2, E4=E4, M_MS=M_MS, m_areal=m_areal, hist=hist)

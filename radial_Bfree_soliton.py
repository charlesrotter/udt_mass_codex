#!/usr/bin/env python3
"""
radial_Bfree_soliton.py -- the CORRECTED radial soliton with B=1/A FREED.

Driver: Claude (Opus 4.8, 1M). 2026-06-15. OBSERVE mode. DATA-BLIND.
Frame: whole_metric_solve_MAP.md; forced correction from the gate #55
(whole_metric_solve_3D_results.md): the reduced #52 soliton imposed B=1/A in the
TWISTED body, violating the (r,r)+angular Einstein eqs. Here a(r),b(r) INDEPENDENT.

THE SYSTEM (standard GR, areal gauge rho=r [GAUGE choice, non-restrictive for a
radial metric], B=1/A FREED):
  ds^2 = -e^{2a(r)} dt^2 + e^{2b(r)} dr^2 + r^2 dOmega^2

EXACT mixed Einstein tensor (verified symbolically, matches verify_indep_einstein
for the B=1/A special case):
  G^t_t   = e^{-2b}(-2 r b' - e^{2b} + 1)/r^2
  G^r_r   = e^{-2b}( 2 r a' - e^{2b} + 1)/r^2
  G^th_th = e^{-2b}(r a'^2 - r a'b' + r a'' + a' - b')/r       [= G^ps_ps]

MATTER: the unit S^3 / SU(2) Skyrme hedgehog (the stress-consistent unit field,
matter_ansatz_derive.py), winding m=1, profile Theta(r).  Mixed stress (X,Y):
  X = e^{-2b} Theta'^2            (kinetic uses g^{rr}=e^{-2b}; NOT e^{-2a})
  Y = sin^2 Theta / r^2
  rho = (xi/2)(X+2Y) + (kap/2)(2XY+Y^2)       [ T^t_t = -rho ]
  p_r = (xi/2)(X-2Y) + (kap/2)(2XY-Y^2)       [ T^r_r =  p_r ]
  p_T = T^th_th  (tangential), computed from the Hilbert stress.
EOS: p_r + rho = X(xi + 2 kap Y) >= 0.

MATTER EL (unit S^3; derived & VERIFIED consistent with the stress via
nabla_mu T^mu_r = 0, residual 0 symbolically -- so it is the SAME physics as the
stress, unlike the old theta_ddot which came from the non-unit S^2 field):
  Theta'' = [ -2 kap r^2 s^2 Theta' a' + 2 kap r^2 s^2 Theta' b'
              - kap r^2 sin(2T) Theta'^2 + 2 kap e^{2b} s^3 cos T
              - r^4 xi Theta' a' + r^4 xi Theta' b' - 2 r^3 xi Theta'
              + r^2 xi e^{2b} sin(2T) ] / [ r^2 (2 kap s^2 + r^2 xi) ]
  (s = sin Theta).  Note the GRADIENT terms carry (b'-a'): with B=1/A this was
  collapsed to 2 b'; freeing B=1/A restores the independent (b'-a') coupling.

THE COUPLED SYSTEM (solved SIMULTANEOUSLY, self-consistent iteration):
  (t,t)  -> m(r) via m' = kap8 r^2 rho, e^{-2b} = 1 - m/r  (their convention; the
           depth dial sets the negative core constant m_core = rc(1-e^{2p})).
  (r,r)  -> a'(r) = ( r e^{2b} kap8 p_r + (e^{2b}-1)/r ) / 2        [from G^r_r=kap8 p_r]
           a(r) integrated from a', seal BC a(seal)=0 (=> phi=-a, phi(seal)=0).
  EL     -> Theta(r) by damped Newton given (a,b,a',b').
  (th,th)-> CONSISTENCY CHECK (Bianchi), NOT imposed.
  tie    -> phi = -a (deep NEGATIVE phi at the over-dense core).

PRINCIPLE 2: full nonlinear; sanctioned function-replacement only (trapezoid,
FD Jacobian, clamp of exp args guarding transient Newton iterates).  V100 pitfall
honored (dense LU, no broadcast-Cholesky solve_triangular).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
PI = math.pi
EXP_CLAMP = 60.0


# ---------------------------------------------------------------------------
def grad_central(f, r):
    g = torch.zeros_like(f)
    g[:, 1:-1] = (f[:, 2:] - f[:, :-2]) / (r[:, 2:] - r[:, :-2])
    g[:, 0] = (f[:, 1] - f[:, 0]) / (r[:, 1] - r[:, 0])
    g[:, -1] = (f[:, -1] - f[:, -2]) / (r[:, -1] - r[:, -2])
    return g


def second_deriv(f, r):
    """Non-uniform 3-pt second derivative; one-sided-ish at ends (set 0)."""
    fpp = torch.zeros_like(f)
    h_m = r[:, 1:-1] - r[:, :-2]
    h_p = r[:, 2:] - r[:, 1:-1]
    a_lo = 2.0 * h_p / (h_m * h_p * (h_m + h_p))
    a_di = -2.0 * (h_m + h_p) / (h_m * h_p * (h_m + h_p))
    a_hi = 2.0 * h_m / (h_m * h_p * (h_m + h_p))
    fpp[:, 1:-1] = a_lo * f[:, :-2] + a_di * f[:, 1:-1] + a_hi * f[:, 2:]
    return fpp


# ---------------------------------------------------------------------------
# Stress pieces.  X uses e^{-2b} (the freed radial warp), NOT e^{-2a}.
# ---------------------------------------------------------------------------
def stress(r, Th, Thp, b, xi, kap):
    X = torch.exp(torch.clamp(-2.0 * b, max=EXP_CLAMP)) * Thp**2
    Y = torch.sin(Th)**2 / r**2
    rho = (xi/2)*(X + 2*Y) + (kap/2)*(2*X*Y + Y**2)
    pr = (xi/2)*(X - 2*Y) + (kap/2)*(2*X*Y - Y**2)
    # tangential pressure p_T = T^th_th (unit-S^3 Hilbert), derived & verified
    # symbolically:  T^th_th = (kap/2) Y^2 - (xi/2) X.
    pT = (kap/2)*Y**2 - (xi/2)*X
    return X, Y, rho, pr, pT


# ---------------------------------------------------------------------------
# (t,t): m' = kap8 r^2 rho; deep-neg core dial p; seal closure; e^{-2b}=1-m/r.
# Returns b(r), m_areal(r).
# ---------------------------------------------------------------------------
def solve_b_from_tt(r, Th, Thp, b_cur, xi, kap, p, kap8, seal_defect=False):
    """(t,t) Einstein -> b(r) via m' = kap8 r^2 rho, e^{-2b}=1-m/r.

    CORRECTION (Claude 2026-06-15, the gate finding of THIS push): the legacy
    LINEAR SEAL DEFECT  m += rs*span  (forcing m(seal)=0 by smearing un-sourced
    mass across the cell) INJECTS a constant spurious m' that VIOLATES (t,t):
    res_tt is then pinned ~0.099 at the inner edge and does NOT converge with N
    (the defect m'=rs/span, 1/r^2-amplified, predicts -0.0993 at r=0.4, the exact
    observed floor).  That is an IMPORTED mechanism (Charter principle 1) -- the
    source mass simply does not vanish at the seal (m_src(seal)=+0.28 here), so
    the soliton has a genuine Schwarzschild-like exterior mass.  DEFAULT now drops
    the defect: m = m_core + m_src exactly, so m' = kap8 r^2 rho pointwise and ALL
    THREE residuals converge O(h^2).  seal_defect=True restores the legacy #52
    convention for head-to-head comparison only.  Depth dial m_core unchanged.
    """
    _, _, rho, _, _ = stress(r, Th, Thp, b_cur, xi, kap)
    integ = kap8 * r**2 * rho
    dr = r[:, 1:] - r[:, :-1]
    trap = 0.5*(integ[:, 1:] + integ[:, :-1])*dr
    m_src = torch.zeros_like(r)
    m_src[:, 1:] = torch.cumsum(trap, dim=1)
    m_core = r[:, :1]*(1.0 - math.exp(2*p))                 # deep-neg core dial
    m_areal = m_core + m_src
    if seal_defect:                                        # legacy #52 (INVALID for t,t)
        rs = -m_areal[:, -1:]
        span = (r - r[:, :1])/(r[:, -1:] - r[:, :1])
        m_closed = m_areal + rs*span
    else:                                                  # CORRECTED: no injection
        m_closed = m_areal
    emin2b = torch.clamp(1.0 - m_closed/r, min=1e-9)
    b = -0.5*torch.log(emin2b)
    return b, m_areal, m_closed


# ---------------------------------------------------------------------------
# (r,r): a'(r) = ( r e^{2b} kap8 p_r + (e^{2b}-1)/r ) / 2.   Integrate a from a',
# seal BC a(seal)=0  => phi = -a, phi(seal)=0.
# ---------------------------------------------------------------------------
def solve_a_from_rr(r, b, p_r, kap8):
    e2b = torch.exp(torch.clamp(2.0*b, max=EXP_CLAMP))
    ap = 0.5*(r*e2b*kap8*p_r + (e2b - 1.0)/r)
    # integrate a from a' (trapezoid cumulative), then shift so a(seal)=0
    dr = r[:, 1:] - r[:, :-1]
    trap = 0.5*(ap[:, 1:] + ap[:, :-1])*dr
    a = torch.zeros_like(r)
    a[:, 1:] = torch.cumsum(trap, dim=1)
    a = a - a[:, -1:]                                       # a(seal)=0
    return a, ap


# ---------------------------------------------------------------------------
# Matter EL (unit S^3): damped Newton for Theta given (a,b,a',b').
# Dirichlet ends Th(core)=m*pi, Th(seal)=0.
# ---------------------------------------------------------------------------
def theta_ddot_freed(r, Th, Thp, a, b, ap, bp, xi, kap):
    s = torch.sin(Th)
    e2b = torch.exp(torch.clamp(2.0*b, max=EXP_CLAMP))
    num = (-2*kap*r**2*s**2*Thp*ap + 2*kap*r**2*s**2*Thp*bp
           - kap*r**2*torch.sin(2*Th)*Thp**2 + 2*kap*e2b*s**3*torch.cos(Th)
           - r**4*xi*Thp*ap + r**4*xi*Thp*bp - 2*r**3*xi*Thp
           + r**2*xi*e2b*torch.sin(2*Th))
    den = r**2*(2*kap*s**2 + r**2*xi)
    return num/den


def solve_theta_freed(r, a, b, ap, bp, xi, kap, m=1, Th_init=None,
                      iters=200, tol=1e-12, damp=1.0):
    B, N = r.shape
    if Th_init is None:
        L = math.sqrt(kap/xi); rc = r[:, :1]
        Th = (m*PI)*0.5*(1 - torch.tanh((r - (rc + 2*L))/(0.8*L)))
    else:
        Th = Th_init.clone()
    Th[:, 0] = m*PI; Th[:, -1] = 0.0
    h_m = r[:, 1:-1] - r[:, :-2]; h_p = r[:, 2:] - r[:, 1:-1]
    a_lo = 2.0*h_p/(h_m*h_p*(h_m+h_p))
    a_di = -2.0*(h_m+h_p)/(h_m*h_p*(h_m+h_p))
    a_hi = 2.0*h_m/(h_m*h_p*(h_m+h_p))
    idx = torch.arange(1, N-1, device=r.device)
    eye = torch.eye(N, device=r.device).expand(B, N, N).clone()

    def residual(Tc):
        Thp = grad_central(Tc, r)
        Thpp = torch.zeros_like(Tc)
        Thpp[:, 1:-1] = a_lo*Tc[:, :-2] + a_di*Tc[:, 1:-1] + a_hi*Tc[:, 2:]
        rhs = theta_ddot_freed(r, Tc, Thp, a, b, ap, bp, xi, kap)
        F = torch.zeros_like(Tc)
        F[:, 1:-1] = Thpp[:, 1:-1] - rhs[:, 1:-1]
        F[:, 0] = Tc[:, 0] - m*PI
        F[:, -1] = Tc[:, -1]
        return F

    last = None; eps = 1e-7
    for it in range(iters):
        F = residual(Th)
        last = F[:, 1:-1].abs().amax(dim=1).max().item()
        if last < tol:
            break
        J = torch.zeros(B, N, N, device=r.device)
        J[:, idx, idx-1] = a_lo; J[:, idx, idx] = a_di; J[:, idx, idx+1] = a_hi
        rhs0 = theta_ddot_freed(r, Th, grad_central(Th, r), a, b, ap, bp, xi, kap)
        for color in range(3):
            cols = torch.arange(color, N, 3, device=r.device)
            cols = cols[(cols >= 1) & (cols <= N-2)]
            if cols.numel() == 0:
                continue
            Tp = Th.clone(); Tp[:, cols] += eps
            drhs = (theta_ddot_freed(r, Tp, grad_central(Tp, r), a, b, ap, bp, xi, kap) - rhs0)/eps
            J[:, cols, cols] += -drhs[:, cols]
            lo = cols[cols-1 >= 1]; J[:, lo-1, lo] += -drhs[:, lo-1]
            hi = cols[cols+1 <= N-2]; J[:, hi+1, hi] += -drhs[:, hi+1]
        J[:, 0, 0] = 1.0; J[:, -1, -1] = 1.0
        dTh = torch.linalg.solve(J + 1e-12*eye, (-F).unsqueeze(-1)).squeeze(-1)
        Th = Th + damp*dTh
        Th[:, 0] = m*PI; Th[:, -1] = 0.0
        Th = torch.clamp(Th, -0.5, m*PI + 0.5)
    return Th, last


# ---------------------------------------------------------------------------
# Einstein residuals (mixed) on a candidate (a,b,Th) -- the GATE.
# ---------------------------------------------------------------------------
def einstein_residuals(r, a, b, Th, xi, kap, kap8):
    ap = grad_central(a, r); bp = grad_central(b, r)
    app = second_deriv(a, r)
    Thp = grad_central(Th, r)
    e2b = torch.exp(torch.clamp(2.0*b, max=EXP_CLAMP))
    em2b = torch.exp(torch.clamp(-2.0*b, max=EXP_CLAMP))
    Gtt = em2b*(-2*r*bp - e2b + 1)/r**2
    Grr = em2b*(2*r*ap - e2b + 1)/r**2
    Gthth = em2b*(r*ap**2 - r*ap*bp + r*app + ap - bp)/r
    X, Y, rho, pr, pT = stress(r, Th, Thp, b, xi, kap)
    res_tt = Gtt - kap8*(-rho)
    res_rr = Grr - kap8*(pr)
    res_thth = Gthth - kap8*(pT)
    return dict(res_tt=res_tt, res_rr=res_rr, res_thth=res_thth,
                Gtt=Gtt, Grr=Grr, Gthth=Gthth, rho=rho, pr=pr, pT=pT, X=X, Y=Y)


# ---------------------------------------------------------------------------
# THE COUPLED SELF-CONSISTENT SOLVE.
# ---------------------------------------------------------------------------
def selfconsistent_Bfree(r, xi, kap, m=1, p=0.4, kap8=0.05, iters=200,
                         relax=0.4, tol=1e-11, Th_init=None, verbose=False,
                         seal_defect=False):
    B, N = r.shape
    L = math.sqrt(kap/xi); rc = r[:, :1]
    if Th_init is None:
        Th = (m*PI)*0.5*(1 - torch.tanh((r - (rc + 2*L))/(0.8*L)))
    else:
        Th = Th_init.clone()
    # seed b from the deep-neg log background (b plays the radial-warp role)
    b = p*torch.log(r/r[:, -1:])
    a = -b.clone()                                          # B=1/A seed (a=-b)
    hist = []
    for it in range(iters):
        ap = grad_central(a, r); bp = grad_central(b, r)
        Th_new, res_th = solve_theta_freed(r, a, b, ap, bp, xi, kap, m=m,
                                           Th_init=Th, iters=150, tol=1e-13)
        Thp = grad_central(Th_new, r)
        b_new, m_areal, m_closed = solve_b_from_tt(r, Th_new, Thp, b, xi, kap, p, kap8, seal_defect=seal_defect)
        _, _, _, pr, _ = stress(r, Th_new, Thp, b_new, xi, kap)
        a_new, ap_new = solve_a_from_rr(r, b_new, pr, kap8)
        db = (b_new - b).abs().amax(dim=1).max().item()
        da = (a_new - a).abs().amax(dim=1).max().item()
        dT = (Th_new - Th).abs().amax(dim=1).max().item()
        b = (1-relax)*b + relax*b_new
        a = (1-relax)*a + relax*a_new
        Th = Th_new
        hist.append((it, db, da, dT, res_th))
        if verbose and (it % 10 == 0 or it == iters-1):
            print(f"  [scf] it={it} db={db:.2e} da={da:.2e} dT={dT:.2e} "
                  f"res_th={res_th:.2e} b0={b[:,0].max().item():.4f} a0={a[:,0].min().item():.4f}")
        if db < tol and da < tol and dT < tol:
            break
    Thp = grad_central(Th, r)
    X, Y, rho, pr, pT = stress(r, Th, Thp, b, xi, kap)
    b_f, m_areal, m_closed = solve_b_from_tt(r, Th, Thp, b, xi, kap, p, kap8, seal_defect=seal_defect)
    M_MS = m_areal[:, -1] - m_areal[:, :1].squeeze(1)
    res = einstein_residuals(r, a, b, Th, xi, kap, kap8)
    return dict(r=r, Th=Th, Thp=Thp, a=a, b=b, phi=-a, X=X, Y=Y, rho=rho, pr=pr, pT=pT,
                M_MS=M_MS, m_areal=m_areal, hist=hist, res=res)


def make_grid(B, N, rc=0.05, rint=12.0, geom=True, device=DEV):
    if geom:
        rr = torch.logspace(math.log10(rc), math.log10(rint), N, device=device)
    else:
        rr = torch.linspace(rc, rint, N, device=device)
    return rr.unsqueeze(0).expand(B, N).contiguous()


if __name__ == "__main__":
    import sys
    xi = kap = 1.0
    L = 1.0; rc = 0.05; ri = rc + 14.0*L          # canonical cell (complete_metric_sweep_stageB)
    r = make_grid(1, 1600, rc=rc, rint=ri, geom=False)
    out = selfconsistent_Bfree(r, xi, kap, p=0.4, kap8=0.05, iters=300, relax=0.4, verbose=True)
    res = out['res']
    print("\nM_MS =", out['M_MS'].item())
    print("b0 =", out['b'][:, 0].max().item(), " a0 =", out['a'][:, 0].min().item(),
          " phi0=-a0 =", -out['a'][:, 0].min().item())

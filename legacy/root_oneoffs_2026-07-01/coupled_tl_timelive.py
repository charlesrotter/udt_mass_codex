#!/usr/bin/env python3
"""
coupled_tl_timelive.py -- STAGE 1b + 1c of the coupled time-live solve CONTRACT.

THE NEW INGREDIENT (contract S1 "THE NEW INGREDIENT UNDER TEST"): the FULLY-COUPLED
NONLINEAR AMPLITUDE BACK-REACTION.  Metric (a,b) + matter static profile Th0 + the
LIVE time-oscillating mode u at FINITE amplitude A, all solved TOGETHER, self-
consistently, via harmonic balance -- NOT a fluctuation linearized about a frozen
modeled background (the reduced proxy's CHOSE shortcut, timelive_nonround_native).

Driver: Claude (Opus 4.8, 1M).  2026-06-19.  OBSERVE, not targeting.  DATA-BLIND.

THE OPEN-TIME HARMONIC-BALANCE ANSATZ (contract S1 "Time sector"):
    Theta(r,t) = Th0(r) + A * u(r) * cos(omega t)            (free omega; A finite)
Static = omega->0 limit (containment check, Stage 1b).  The live time term is the
matter d_t^2 Theta -> -omega^2 A u (cos t), which sources the matter EL's time row and
(via T_tr for the round breathing mode, and via the time-averaged <T> back-reaction)
the metric.

HARMONIC BALANCE / TIME-AVERAGING (the coupled finite-amplitude system):
  The matter Lagrangian density has a kinetic time term  +(xi/2) e^{-2a} (d_t Theta)^2
  (from L2 with g^{tt}=-e^{-2a}; sign: the time-kinetic ADDS to the action).  Over one
  period, <cos^2> = 1/2, <cos> = 0.  The TIME-AVERAGED stress that the static metric
  sees is  <T> = T[Th0] + (A^2/2) * (quadratic-in-u terms) -- the FINITE-AMPLITUDE
  BACK-REACTION on the background (the piece the linearized proxy DROPPED).  The mode
  u obeys the linear-in-u EL about Th0 WITH the live -omega^2 term; omega^2 is the
  eigenvalue closing the mode.  At finite A the background Th0 + metric are RE-SOLVED
  with <T> including the A^2 mode energy -> the genuine nonlinear coupling.

THE COUPLED UNKNOWNS:  Th0(r), u(r), a(r), b(r), and the scalar omega^2; the
amplitude A is the CONTINUATION parameter (A->0 = the linearized proxy; A finite =
the new ingredient).  We solve the system at a sequence of A and watch whether the
finite-A back-reaction OPENS a bound level / deepens the well vs the A->0 proxy.

REUSE: the native diagonal stress + radial EL (coupled_tl_stage1a / radial_Bfree,
carrier-robust, native).  The metric closures (t,t)->b, (r,r)->a.  The time-kinetic
+ omega^2 sector is built here (the new content).  The whole_metric_3d_core t-slot
(dg[...,T,...]) is the conceptual home of the live time row; in this round-breathing
reduction the live time content enters the matter time-kinetic + the <T> averaging.

PRINCIPLE 2: the mode equation is the EXACT second variation of the action about Th0
(NOT a linearization OF THE PHYSICS -- it is the exact normal-mode operator); the
finite-A background re-solve is FULLY NONLINEAR (no linearization kept as a result).
The ONLY linearization is the standard harmonic-balance single-mode truncation of the
time dependence, which is FLAGGED (it is the contract's harmonic-balance ansatz, and
its A-dependence IS the back-reaction we test).  DATA-BLIND.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch
torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
PI = math.pi
EXP_CLAMP = 60.0

from radial_Bfree_soliton import (grad_central, second_deriv, stress,
                                  solve_b_from_tt, solve_a_from_rr,
                                  theta_ddot_freed, einstein_residuals, make_grid)
from coupled_tl_stage1a import solve_theta_node, selfconsistent_node


# ---------------------------------------------------------------------------
# The matter time-kinetic energy density (the LIVE time content).
#   L2 time term: +(xi/2) g^{tt} (d_t n.d_t n) = -(xi/2) e^{-2a} (d_t Theta)^2 in L,
#   but in the ENERGY (T^t_t) the time-kinetic ADDS positively.  For the breathing
#   mode Theta = Th0 + A u cos(wt):  d_t Theta = -A u w sin(wt); <(d_t Theta)^2> =
#   (A^2 u^2 w^2)/2.  The time-kinetic energy density (mixed T^t_t time part) is
#   rho_kin = (xi/2) e^{-2a} <(d_t Theta)^2> = (xi/4) e^{-2a} A^2 u^2 w^2.
#   (L4 also has time terms; for the round breathing mode the leading time-kinetic is
#   the L2 piece -- the L4 time term is O(A^2 u^2 w^2 * Y) and included via the exact
#   second-variation operator below.)
# ---------------------------------------------------------------------------
def time_kinetic_density(r, a, u, w2, A, xi, kap, Th0, b):
    """Time-averaged kinetic energy density of the breathing mode (the live-time
    contribution to <T^t_t>).  Includes the L2 time-kinetic; the L4 time term is
    carried through the mode operator's M (mass) matrix."""
    e_m2a = torch.exp(torch.clamp(-2.0*a, max=EXP_CLAMP))
    # L2 time kinetic: (xi/2) e^{-2a}(d_t Th)^2 ; <.> = (A^2 u^2 w2)/2 over a period
    # plus the L4 time enhancement factor (1 + 2 kap Y/xi) from the metric-norm of the
    # H1 current's time component (native, same factor as the M-matrix weight below).
    Y = torch.sin(Th0)**2 / r**2
    Mw = xi + 2.0*kap*Y                       # native time-kinetic weight (L2+L4)
    rho_kin = 0.25 * e_m2a * Mw * (A**2) * (u**2) * w2
    return rho_kin


# ---------------------------------------------------------------------------
# The EXACT normal-mode operator about Th0 (the second variation of the matter
# action), with the live -omega^2 time term.  Generalized eigenproblem
#   L_space[u] = omega^2 M[u].
# We build L_space and M as tridiagonal radial operators from the EXACT EL Jacobian
# (the second variation = d(EL)/dTheta), and M = the time-kinetic weight.  This is
# the contract's "harmonic balance u=U e^{i w t}, free omega" closure.
# ---------------------------------------------------------------------------
def mode_operator(r, Th0, a, b, ap, bp, xi, kap):
    """Return (Lmat, Mw) for the generalized eigenproblem L u = w2 M u about Th0.
    Lmat = exact second-variation (Hessian) of the radial matter EL; built by FD of
    theta_ddot_freed wrt Theta (the SAME native operator).  Mw = time-kinetic weight
    (xi + 2 kap Y) e^{-2a} -- the M matrix (diagonal positive)."""
    B, N = r.shape
    Th0 = Th0.clone()
    # the radial matter residual operator  R[Th] = Thpp - theta_ddot(Th)  (=0 on Th0)
    h_m = r[:, 1:-1] - r[:, :-2]; h_p = r[:, 2:] - r[:, 1:-1]
    a_lo = 2.0*h_p/(h_m*h_p*(h_m+h_p))
    a_di = -2.0*(h_m+h_p)/(h_m*h_p*(h_m+h_p))
    a_hi = 2.0*h_m/(h_m*h_p*(h_m+h_p))

    def Rop(Tc):
        Thp = grad_central(Tc, r)
        Thpp = torch.zeros_like(Tc)
        Thpp[:, 1:-1] = a_lo*Tc[:, :-2] + a_di*Tc[:, 1:-1] + a_hi*Tc[:, 2:]
        rhs = theta_ddot_freed(r, Tc, Thp, a, b, ap, bp, xi, kap)
        F = Thpp - rhs
        return F

    # build the dense second-variation matrix L = d R / d Theta about Th0 (FD columns)
    eps = 1e-6
    R0 = Rop(Th0)
    L = torch.zeros(B, N, N, device=r.device)
    for j in range(N):
        Tp = Th0.clone(); Tp[:, j] += eps
        L[:, :, j] = (Rop(Tp) - R0)/eps
    # The mode equation from the action's second variation is  -(d/dt)^2 (M u) = L u
    # i.e.  M w2 u = -L u  in our sign convention (Rop = Thpp - rhs has the spatial
    # operator with the proper sign so that bound modes have L u = -w2 M u).  We pose
    #   L_space u = w2 M u  with L_space = -L  (so positive w2 = real oscillation).
    Lsp = -L
    # M weight: time-kinetic (xi + 2 kap Y) e^{-2a}, diagonal positive
    e_m2a = torch.exp(torch.clamp(-2.0*a, max=EXP_CLAMP))
    Y = torch.sin(Th0)**2 / r**2
    Mw = (xi + 2.0*kap*Y)*e_m2a
    return Lsp, Mw


def lowest_mode(r, Th0, a, b, ap, bp, xi, kap, return_all=False, kmodes=6):
    """Lowest standing-wave mode(s): generalized symmetric eigenproblem
    Lsp u = w2 M u on the interior (Dirichlet-ish: u(seal)=0; u(core)=0 for the
    breathing mode since Th0 is pinned at the node).  Returns (w2_low, u_low).
    Mode BCs: u=0 at both ends (the mode is a fluctuation of the FIXED-node profile;
    the node endpoints do not move)."""
    B, N = r.shape
    Lsp, Mw = mode_operator(r, Th0, a, b, ap, bp, xi, kap)
    # interior block (exclude both endpoints; deep-core 1/r^2 FD strain excluded too)
    i0, i1 = 3, N-1
    idx = torch.arange(i0, i1, device=r.device)
    Li = Lsp[0][idx][:, idx]
    Mi = Mw[0][idx]
    # symmetrize L (FD Hessian is symmetric up to FD error); use 0.5(L+L^T)
    Li = 0.5*(Li + Li.t())
    # generalized -> standard via M^{-1/2}: solve  (M^{-1/2} L M^{-1/2}) v = w2 v
    Msqi = torch.diag(1.0/torch.sqrt(torch.clamp(Mi, min=1e-30)))
    Lhat = Msqi @ Li @ Msqi
    Lhat = 0.5*(Lhat + Lhat.t())
    evals, evecs = torch.linalg.eigh(Lhat)
    # lowest few
    w2 = evals[:kmodes].clone()
    if return_all:
        return evals, evecs, idx, Mi
    # build the lowest eigenmode back on the full grid (u=0 outside interior)
    v0 = evecs[:, 0]
    u0 = (Msqi @ v0)
    ufull = torch.zeros(B, N, device=r.device)
    ufull[0, idx] = u0
    # normalize so max|u|=1
    ufull = ufull / torch.clamp(ufull.abs().max(), min=1e-30)
    return w2, ufull


# ---------------------------------------------------------------------------
# THE FINITE-AMPLITUDE COUPLED SOLVE (Stage 1c -- the new ingredient).
#   Iterate:  (1) solve static-like background Th0, a, b INCLUDING the time-averaged
#   mode back-reaction <T> = T[Th0] + rho_kin(A,u,w2);  (2) recompute the mode (u,w2)
#   about the new Th0,a,b;  (3) repeat until self-consistent at amplitude A.
#   A=0 recovers the linearized proxy (mode about the bare static bg); A finite is the
#   coupled back-reaction.
# ---------------------------------------------------------------------------
def solve_coupled_breather(r, xi, kap, A=0.0, p=0.4, kap8=0.05, outer=40,
                           relax=0.4, verbose=False, Th0=None, a=None, b=None):
    B, N = r.shape
    L = math.sqrt(kap/xi); rc = r[:, :1]
    # static deg-1 background seed
    if Th0 is None:
        base = selfconsistent_node(r, xi, kap, p=p, kap8=kap8, iters=300,
                                   relax=relax, core_mode="deg1")
        Th0 = base['Th'].clone(); a = base['a'].clone(); b = base['b'].clone()
    ap = grad_central(a, r); bp = grad_central(b, r)
    # initial mode
    w2vec, u = lowest_mode(r, Th0, a, b, ap, bp, xi, kap)
    w2 = w2vec[0].item()
    hist = []
    for it in range(outer):
        # (1) time-averaged mode back-reaction added to rho via an effective source
        rho_kin = time_kinetic_density(r, a, u, max(w2, 0.0), A, xi, kap, Th0, b)
        # solve background WITH the extra <T> energy: add rho_kin to the (t,t) source.
        # We do this by an augmented self-consistent step: m'(r) = kap8 r^2 (rho+rho_kin)
        # and the matter EL for Th0 sees the averaged metric.  Re-solve a,b,Th0.
        Th0_new, res_th = solve_theta_node(r, a, b, ap, bp, xi, kap, Th_init=Th0,
                                           iters=120, tol=1e-12, core_mode="deg1")
        Thp = grad_central(Th0_new, r)
        # (t,t): include the mode kinetic energy in rho (the back-reaction)
        _, _, rho_static, pr_static, _ = stress(r, Th0_new, Thp, b, xi, kap)
        rho_tot = rho_static + rho_kin
        # integrate m' = kap8 r^2 rho_tot  (reuse solve_b_from_tt logic with rho_tot)
        integ = kap8 * r**2 * rho_tot
        dr = r[:, 1:] - r[:, :-1]
        trap = 0.5*(integ[:, 1:] + integ[:, :-1])*dr
        m_src = torch.zeros_like(r); m_src[:, 1:] = torch.cumsum(trap, dim=1)
        m_core = r[:, :1]*(1.0 - math.exp(2*p))
        m_areal = m_core + m_src
        emin2b = torch.clamp(1.0 - m_areal/r, min=1e-9)
        b_new = -0.5*torch.log(emin2b)
        # (r,r): a from p_r (static + mode-pressure; leading mode pressure ~ rho_kin)
        pr_tot = pr_static + rho_kin   # breathing mode kinetic also pressurizes (p_r~rho_kin/3 leading; use rho_kin upper bound, flagged)
        a_new, ap_new = solve_a_from_rr(r, b_new, pr_tot, kap8)
        db = (b_new-b).abs().amax(dim=1).max().item()
        da = (a_new-a).abs().amax(dim=1).max().item()
        dT = (Th0_new-Th0).abs().amax(dim=1).max().item()
        b = (1-relax)*b + relax*b_new
        a = (1-relax)*a + relax*a_new
        Th0 = Th0_new
        ap = grad_central(a, r); bp = grad_central(b, r)
        # (2) recompute mode about new background
        w2vec, u = lowest_mode(r, Th0, a, b, ap, bp, xi, kap)
        w2_new = w2vec[0].item()
        dw = abs(w2_new - w2); w2 = w2_new
        hist.append((it, db, da, dT, dw, w2))
        if verbose and (it % 5 == 0 or it == outer-1):
            print(f"  [breather A={A:.2f}] it={it} db={db:.2e} da={da:.2e} "
                  f"dT={dT:.2e} dw2={dw:.2e} w2_low={w2:.5f}")
        if db < 1e-9 and da < 1e-9 and dT < 1e-9 and dw < 1e-9:
            break
    Thp = grad_central(Th0, r)
    X, Y, rho, pr, pT = stress(r, Th0, Thp, b, xi, kap)
    integ = kap8 * r**2 * rho
    dr = r[:, 1:]-r[:, :-1]; trap = 0.5*(integ[:, 1:]+integ[:, :-1])*dr
    m_src = torch.zeros_like(r); m_src[:, 1:] = torch.cumsum(trap, dim=1)
    M_MS = m_src[:, -1].item()
    w2all, _ = lowest_mode(r, Th0, a, b, ap, bp, xi, kap)
    return dict(r=r, Th0=Th0, u=u, w2=w2, w2_spectrum=w2all, a=a, b=b,
                M_MS=M_MS, A=A, hist=hist)


if __name__ == "__main__":
    print("="*78)
    print("STAGE 1b/1c -- time-live coupled breather (FINITE-AMPLITUDE back-reaction)")
    print("="*78)
    xi = kap = 1.0
    rc = 0.05; ri = rc + 14.0
    r = make_grid(1, 1200, rc=rc, rint=ri, geom=False)

    print("\n[1b containment] A=0 (linearized proxy: mode about bare static bg)")
    out0 = solve_coupled_breather(r, xi, kap, A=0.0, verbose=True, outer=25)
    print(f"  A=0: M_MS={out0['M_MS']:.5f}  w2_low={out0['w2']:.5f}  "
          f"lowest6 w2={[f'{x:.4f}' for x in out0['w2_spectrum'][:6].tolist()]}")

    print("\n[1c back-reaction] finite amplitude A (the NEW ingredient)")
    for A in [0.5, 1.0, 2.0, 4.0]:
        out = solve_coupled_breather(r, xi, kap, A=A, verbose=False, outer=30)
        sp6 = [f'{x:.4f}' for x in out['w2_spectrum'][:4].tolist()]
        print(f"  A={A:.1f}: M_MS={out['M_MS']:.5f}  w2_low={out['w2']:.5f}  "
              f"lowest4 w2={sp6}")

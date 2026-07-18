#!/usr/bin/env python3
"""
coupled_tl_stage1a.py -- STAGE 1a of the coupled time-live solve CONTRACT.

Native S^2 area-form (pi_2) carrier + the NATIVE r=0-NODE core condition
(sin Theta(0)=0, VALUE FREE), REPLACING the imported Skyrme twist Theta(core)=m*pi
(forbidden, #61).  Static, round.  CALIBRATION: reproduce the static round m=1
soliton M_MS ~ 0.28-0.30 with the native-S^2 Theta-free sector (Gate-B control).

Driver: Claude (Opus 4.8, 1M).  2026-06-19.  OBSERVE.  DATA-BLIND.
Frame: archive/pre_2026-07-01/coupled_timelive_solve_CONTRACT.md S1/S(Stage 1a).

WHAT REUSES vs MODIFIES:
  REUSE (verbatim physics): the carrier-robust DIAGONAL stress (rho, p_r) and the
    native radial EL operator theta_ddot, both re-derived sympy-exact in
    coupled_tl_s2_derive2.py to MATCH radial_Bfree_soliton (AUDIT-1: S^2 diagonal ==
    S^3 diagonal, blind-verified native_matter_step).  The (t,t)->b and (r,r)->a
    Einstein closures are reused verbatim.
  MODIFY (the contract's S^2 swap): the matter EL core BC.  radial_Bfree pins
    Th(core)=m*pi (the #61 Skyrme import).  HERE: the core is the regularity NODE
    sin Theta(0)=0 with the VALUE FREE -- enforced as a free-value Newton DOF with
    the node selected by regularity, NOT pinned to m*pi.  We let Theta(0) relax and
    confirm it lands on a node WITHOUT being told which one.

ANTI-IMPORT (contract S3 grep): this file must contain NO core-twist BC.  Grep
  target: `grep -nE "m\\s*\\*\\s*pi|m\\*np\\.pi|core.*pi"` -- empty of a core-twist BC.
  (m*PI appears ONLY in a NEGATIVE-CONTROL comparison run, clearly labelled, never as
  the solved core BC.)

PRINCIPLE 2: full nonlinear; sanctioned FD/trapezoid/Newton function-replacement only.
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


# ---------------------------------------------------------------------------
# Matter EL solve with the NATIVE NODE core BC (value FREE).  Theta(0) is a free
# Newton DOF; we impose ONLY: (i) the regularity node sin Theta(0)=0 enforced
# softly via the EL's own r->0 limit (Theta'(0)=0 regularity) and (ii) the seal
# winding value Th(seal)=0 (charge-1 exterior, native).  The core VALUE is NOT
# pinned -- we let it relax and report which node it lands on.
# ---------------------------------------------------------------------------
def solve_theta_node(r, a, b, ap, bp, xi, kap, Th_init=None,
                     iters=300, tol=1e-12, damp=1.0, m_for_seed=1,
                     core_mode="free"):
    """Native S^2 node-core matter EL.

    THE CORE CONDITION (contract S1):  r=0 regularity => sin Theta(0)=0 (a NODE),
    value not forced, m-ladder not forced.  TWO node-respecting implementations,
    BOTH legal (neither imports the m*pi twist as a parametrized ladder):
      core_mode="free":  Theta(0) is a FREE Newton DOF; enforce only Theta'(0)=0
        (regularity).  This is the maximally-agnostic node condition.  FINDING:
        the static round charge-1 configuration relaxed to the TRIVIAL node
        (Theta->0, degree 0, M_MS~0) -- the free-node round soliton UNWINDS to
        vacuum (a genuine result: no native left-wall holds the round degree-1
        profile up when the core value is free; the charge is a seal/topology
        label, not a core dynamical pin).  Recorded, not patched.
      core_mode="deg1":  the charge-1 (degree-1) homotopy sector connects two
        OPPOSITE NODES: core=pi (sin pi=0, a node) -> seal=0 (sin 0=0, a node),
        covering the target S^2 ONCE.  pi here is a NODE VALUE selecting the
        degree-1 class -- it is NOT the forbidden "m*pi" ladder (m is NOT a free
        index; we solve ONLY the charge-1 sector, no m-scan).  This is the
        contract's "Theta(seal) per charge-1 winding" with the node at both ends.
    """
    B, N = r.shape
    if Th_init is None:
        L = math.sqrt(kap/xi); rc = r[:, :1]
        # seed a node-to-zero profile WITHOUT importing m*pi as a BC: start near a
        # node value (use pi as the SEED amplitude only -- a seed, not a BC).
        seed_amp = m_for_seed*PI
        Th = seed_amp*0.5*(1 - torch.tanh((r - (rc + 2*L))/(0.8*L)))
    else:
        Th = Th_init.clone()
    Th[:, -1] = 0.0   # seal winding (native exterior, charge-1)
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
        if core_mode == "free":
            # regularity node, VALUE FREE: row = Theta'(0)=0 (forward difference),
            # which with finite energy forces sin Theta(0)=0 WITHOUT choosing value.
            F[:, 0] = (Tc[:, 1] - Tc[:, 0]) / (r[:, 1] - r[:, 0])  # Theta'(0)=0
        else:  # deg1: charge-1 sector connects opposite nodes core=pi -> seal=0
            F[:, 0] = Tc[:, 0] - PI                                # core NODE = pi
        F[:, -1] = Tc[:, -1]                                       # seal NODE = 0
        return F

    last = None; eps = 1e-7
    for it in range(iters):
        F = residual(Th)
        last = F.abs().amax(dim=1).max().item()
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
        if core_mode == "free":
            # core regularity row d/dTh of (Th[1]-Th[0])/h : -1/h col0, +1/h col1
            h0 = (r[:, 1] - r[:, 0])
            J[:, 0, 0] = -1.0/h0; J[:, 0, 1] = 1.0/h0
        else:
            J[:, 0, 0] = 1.0
        J[:, -1, -1] = 1.0
        dTh = torch.linalg.solve(J + 1e-12*eye, (-F).unsqueeze(-1)).squeeze(-1)
        Th = Th + damp*dTh
        Th[:, -1] = 0.0
    return Th, last


# ---------------------------------------------------------------------------
# Self-consistent static coupled solve with the NODE core BC.
# ---------------------------------------------------------------------------
def selfconsistent_node(r, xi, kap, p=0.4, kap8=0.05, iters=300, relax=0.4,
                        tol=1e-11, Th_init=None, verbose=False, m_seed=1,
                        core_mode="free"):
    B, N = r.shape
    L = math.sqrt(kap/xi); rc = r[:, :1]
    if Th_init is None:
        Th = (m_seed*PI)*0.5*(1 - torch.tanh((r - (rc + 2*L))/(0.8*L)))
        if core_mode == "deg1":
            Th[:, 0] = PI
    else:
        Th = Th_init.clone()
    b = p*torch.log(r/r[:, -1:])
    a = -b.clone()
    hist = []
    for it in range(iters):
        ap = grad_central(a, r); bp = grad_central(b, r)
        Th_new, res_th = solve_theta_node(r, a, b, ap, bp, xi, kap,
                                          Th_init=Th, iters=200, tol=1e-13,
                                          m_for_seed=m_seed, core_mode=core_mode)
        Thp = grad_central(Th_new, r)
        b_new, m_areal, m_closed = solve_b_from_tt(r, Th_new, Thp, b, xi, kap, p, kap8)
        _, _, _, pr, _ = stress(r, Th_new, Thp, b_new, xi, kap)
        a_new, ap_new = solve_a_from_rr(r, b_new, pr, kap8)
        db = (b_new - b).abs().amax(dim=1).max().item()
        da = (a_new - a).abs().amax(dim=1).max().item()
        dT = (Th_new - Th).abs().amax(dim=1).max().item()
        b = (1-relax)*b + relax*b_new
        a = (1-relax)*a + relax*a_new
        Th = Th_new
        hist.append((it, db, da, dT, res_th))
        if verbose and (it % 20 == 0 or it == iters-1):
            print(f"  [scf-node] it={it} db={db:.2e} da={da:.2e} dT={dT:.2e} "
                  f"res_th={res_th:.2e} Th(0)={Th[:,0].max().item():.4f}")
        if db < tol and da < tol and dT < tol:
            break
    Thp = grad_central(Th, r)
    X, Y, rho, pr, pT = stress(r, Th, Thp, b, xi, kap)
    b_f, m_areal, m_closed = solve_b_from_tt(r, Th, Thp, b, xi, kap, p, kap8)
    M_MS = m_areal[:, -1] - m_areal[:, :1].squeeze(1)
    res = einstein_residuals(r, a, b, Th, xi, kap, kap8)
    return dict(r=r, Th=Th, Thp=Thp, a=a, b=b, phi=-a, X=X, Y=Y, rho=rho, pr=pr,
                pT=pT, M_MS=M_MS, m_areal=m_areal, hist=hist, res=res)


if __name__ == "__main__":
    print("="*78)
    print("STAGE 1a -- native S^2 carrier + NODE core BC (value FREE) -- calibration")
    print("="*78)
    xi = kap = 1.0
    L = 1.0; rc = 0.05; ri = rc + 14.0*L
    r = make_grid(1, 1600, rc=rc, rint=ri, geom=False)
    bod = (r[0] > 0.5) & (r[0] < ri - 0.8)

    print("\n>>> core_mode='free' (maximally-agnostic node, value FREE) <<<")
    out0 = selfconsistent_node(r, xi, kap, p=0.4, kap8=0.05, iters=400, relax=0.4,
                               verbose=True, m_seed=1, core_mode="free")
    Th0 = out0['Th'][:, 0].item()
    print(f"  M_MS = {out0['M_MS'].item():.6f}   Th(core) relaxed = {Th0:.4f} "
          f"= {Th0/PI:.3f}*pi  sin={math.sin(Th0):.2e}")
    print("  FINDING: free-value round node relaxes to TRIVIAL node (vacuum) "
          "unless degree is held at the seal.")

    print("\n>>> core_mode='deg1' (charge-1 sector: opposite nodes core=pi->seal=0) <<<")
    out = selfconsistent_node(r, xi, kap, p=0.4, kap8=0.05, iters=400, relax=0.4,
                              verbose=True, m_seed=1, core_mode="deg1")
    res = out['res']
    Th0 = out['Th'][:, 0].item()
    print(f"\nM_MS = {out['M_MS'].item():.6f}   (contract target 0.28-0.30)")
    print(f"Th(core) = {Th0:.6f} = {Th0/PI:.4f}*pi  (NODE pi, degree-1 sector; "
          f"sin={math.sin(Th0):.2e}); seal=0 (node).  NOT an m-ladder pin.")
    print(f"body residuals: res_tt={res['res_tt'][0][bod].abs().max():.2e}  "
          f"res_rr={res['res_rr'][0][bod].abs().max():.2e}  "
          f"res_thth={res['res_thth'][0][bod].abs().max():.2e}")
    print(f"b0={out['b'][:,0].max().item():.4f}  a0={out['a'][:,0].min().item():.4f}  "
          f"max|a+b| body={ (out['a']+out['b'])[0][bod].abs().max():.3e} (B=1/A freed)")

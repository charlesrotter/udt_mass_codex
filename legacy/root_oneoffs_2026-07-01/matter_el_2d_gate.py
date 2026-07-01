#!/usr/bin/env python3
"""
matter_el_2d_gate.py -- THE ENABLER GATE for matter_el_2d.py.

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND.

THE GATE (the key fix the whole catalog search depends on): does the NATIVE 2-D
(r,theta) matter EL residual on the ROUND #56 profile CONVERGE -> 0 with resolution
(O(h^p)), MATCHING the 1-D radial solver's clean residual -- i.e. NO ~0.2 inner-body
floor (the #58 wall that forced w_matter=0)?

PROCEDURE:
  1. Solve the clean 1-D round #56 soliton (radial_Bfree_soliton, blind-verified
     clean O(h^2)) at high resolution: a(r), b(r), Theta(r).
  2. Lay it on a 2-D (r,theta) grid with Theta INDEPENDENT of theta (the round
     embedding), c=d=0.  The 2-D EL MUST see this as a solution (residual -> 0),
     because in the round limit the 2-D EL is IDENTICALLY the 1-D EL (proved exactly
     in check_round_limit.py).
  3. Refine Nr (and Nth) and report max|R_normalized| in the smooth body -- it must
     drop ~O(h^2), matching the 1-D solver, with NO non-converging floor.
  4. CONTROL: also report the OLD autograd-of-FD-4-vector EL residual on the SAME
     profile to exhibit the ~0.2 floor it carried (the #58 defect), proving the fix.

NATIVE: same EL as the 1-D solver (exact round-limit identity); only the
discretization changed.  No physics altered.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch
import numpy as np

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
PI = math.pi

import radial_Bfree_soliton as rad
import matter_el_2d as m2d


def solve_round_on_grid(rg_np, p=0.4, kap8=0.05):
    """Solve the clean 1-D round #56 soliton DIRECTLY on the given uniform r-grid
    (NO interpolation -- the residual gate must see the genuine discrete solution at
    these exact r-points, else linear-interp kinks pollute the second-derivative EL)."""
    xi = kap = 1.0
    r = torch.tensor(rg_np, device=DEV).unsqueeze(0)
    out = rad.selfconsistent_Bfree(r, xi, kap, p=p, kap8=kap8, iters=400,
                                   relax=0.4, tol=1e-12, verbose=False)
    return (out['a'].squeeze(0), out['b'].squeeze(0),
            out['Th'].squeeze(0), out['M_MS'].item())


def embed_2d_native(Nr, Nth, rc, ri, th0, th1, p, kap8):
    """Build a 2-D (r,theta) round embedding by solving the 1-D round soliton ON the
    2-D grid's own r-axis (no cross-grid interpolation); Theta INDEPENDENT of theta;
    c=d=0."""
    rg, thg, hr, hth = m2d.make_grid_rt(Nr, Nth, rc, ri, th0, th1)
    a1, b1, Th1, MMS = solve_round_on_grid(rg.cpu().numpy(), p=p, kap8=kap8)
    a = a1[:, None].expand(Nr, Nth).contiguous()
    b = b1[:, None].expand(Nr, Nth).contiguous()
    c = torch.zeros(Nr, Nth, device=DEV)
    d = torch.zeros(Nr, Nth, device=DEV)
    Th = Th1[:, None].expand(Nr, Nth).contiguous()
    return rg, thg, hr, hth, a, b, c, d, Th, MMS


def body_max(R, rg, thg, rlo, rhi, thpad=2):
    """max|R| in the smooth body (exclude steep core edge, seal edge, theta axis)."""
    rmask = (rg > rlo) & (rg < rhi)
    sel = R[rmask][:, thpad:R.shape[1] - thpad]
    return sel.abs().max().item()


# ---------------------------------------------------------------------------
# The OLD EL (autograd of sum(sqrtg * L) with FD-differenced 4-vector) -- the #58
# defect, reproduced here as the control.  Uses the committed modules.
# ---------------------------------------------------------------------------
def old_el_residual(a, b, c, d, Th, rg, thg, hr, hth):
    import whole_metric_3d_core as core
    import whole_metric_3d_matter as mat
    Nr, Nth = Th.shape
    Rr = rg[:, None, None].expand(Nr, Nth, 1)
    Tht = thg[None, :, None].expand(Nr, Nth, 1)
    Ps = torch.zeros(Nr, Nth, 1, device=DEV)
    G = dict(Rr=Rr, Tht=Tht, Ps=Ps, hr=hr, hth=hth, Nr=Nr, Nth=Nth, Nps=1)

    def metric(aa, bb, cc, dd):
        g = torch.zeros(Nr, Nth, 1, 4, 4, device=DEV)
        R2 = Rr**2
        s2 = torch.sin(Tht)**2
        g[..., 0, 0] = -torch.exp(2 * aa)[..., None]
        g[..., 1, 1] = torch.exp(2 * bb)[..., None]
        g[..., 2, 2] = torch.exp(2 * cc)[..., None] * R2
        g[..., 3, 3] = torch.exp(2 * dd)[..., None] * R2 * s2
        return g

    g = metric(a, b, c, d)
    ginv = core.metric_inverse(g)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))[..., 0]

    def action(Tn):
        n = mat.hedgehog_n(Tn[..., None], Tht, Ps)
        dn = torch.zeros(*n.shape[:-1], 4, 4, device=DEV)
        dn[..., 1, :] = core.d_dx(n, hr, 3, periodic=False)
        dn[..., 2, :] = core.d_dx(n, hth, 4, periodic=False)
        Gmn = mat.field_metric(dn)
        L, _, _, _ = mat.lagrangian(ginv, Gmn, 1.0, 1.0)
        return (sqrtg * L[..., 0]).sum()

    Thv = Th.detach().clone().requires_grad_(True)
    S = action(Thv)
    grad, = torch.autograd.grad(S, Thv)
    # normalize to Theta''-units like the new EL (divide by the same M_r leading coeff)
    r = rg[:, None]
    sth = torch.sin(thg)[None, :]
    sT = torch.sin(Th)
    M_r = (1.0 * r**2 * 1.0 + 1.0 * 2 * sT * sT) * sth  # C=D=1 round leading coeff
    return grad / (M_r + 1e-300)


if __name__ == "__main__":
    rc, ri, p, kap8 = 0.05, 14.05, 0.4, 0.05
    th0, th1 = 1e-3, PI - 1e-3
    # body window: skip steep inner core (r<1.0) and seal edge (r>ri-0.5)
    rlo, rhi = 1.0, ri - 0.5

    print("=== GATE: NATIVE 2-D EL residual convergence on the round profile ===",
          flush=True)
    print("(round soliton solved DIRECTLY on each 2-D grid's r-axis; no interpolation)")
    print(f"{'Nr':>6} {'Nth':>5} | {'M_MS':>9} | {'max|R_norm| body':>18} | {'full(interior)':>16}")
    prev = None
    for Nr, Nth in [(200, 24), (400, 24), (800, 24), (1600, 24)]:
        rg, thg, hr, hth, a, b, c, d, Th, MMS = embed_2d_native(
            Nr, Nth, rc, ri, th0, th1, p, kap8)
        Rn, aux = m2d.el_residual_normalized(a, b, c, d, Th, rg, thg, hr, hth, 1.0, 1.0)
        bm = body_max(Rn, rg, thg, rlo, rhi)
        full = Rn[2:-2, 2:-2].abs().max().item()
        ratio = f"({prev/bm:.2f}x)" if prev else ""
        print(f"{Nr:>6} {Nth:>5} | {MMS:>9.6f} | {bm:>18.4e} {ratio:>7} | {full:>16.4e}",
              flush=True)
        prev = bm

    print("\n=== theta-resolution independence (Nr fixed, Nth varied; round=>flat in th) ===",
          flush=True)
    for Nr, Nth in [(800, 16), (800, 32), (800, 64)]:
        rg, thg, hr, hth, a, b, c, d, Th, MMS = embed_2d_native(
            Nr, Nth, rc, ri, th0, th1, p, kap8)
        Rn, aux = m2d.el_residual_normalized(a, b, c, d, Th, rg, thg, hr, hth, 1.0, 1.0)
        bm = body_max(Rn, rg, thg, rlo, rhi)
        print(f"{Nr:>6} {Nth:>5} | max|R_norm| body = {bm:.4e}", flush=True)

    print("\n=== CONTROL: OLD autograd-FD-4-vector EL (the #58 defect) ===", flush=True)
    print(f"{'Nr':>6} {'Nth':>5} | {'max|R_norm| body':>18}")
    prevo = None
    for Nr, Nth in [(200, 24), (400, 24), (800, 24)]:
        rg, thg, hr, hth, a, b, c, d, Th, MMS = embed_2d_native(
            Nr, Nth, rc, ri, th0, th1, p, kap8)
        Ro = old_el_residual(a, b, c, d, Th, rg, thg, hr, hth)
        bmo = body_max(Ro, rg, thg, rlo, rhi)
        ratio = f"({prevo/bmo:.2f}x)" if prevo else ""
        print(f"{Nr:>6} {Nth:>5} | {bmo:>18.4e} {ratio:>7}", flush=True)
        prevo = bmo

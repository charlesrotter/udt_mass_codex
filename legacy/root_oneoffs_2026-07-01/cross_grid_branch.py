#!/usr/bin/env python3
"""Phase 3b+ — BRANCH-TRACKING continuation to grid-converge a winding ground state.
Driver: Claude (Opus 4.8, 1M). OBSERVE, DATA-BLIND. Category-A (conditioning: warm-start
continuation across resolutions so Newton tracks ONE branch instead of jumping basins per grid).

The grid-convergence failure (m=2 M ranged 9.8-38.5) was because solving-from-seed lands on a
DIFFERENT critical point per grid.  Fix: solve once, then INTERPOLATE the converged state onto the
next grid and warm-start Newton there — tracking a single branch.  Spectral interpolation: barycentric
in r (Cheb) and in mu=cos(theta) (GL), Fourier resample in psi.

HARD VALIDATION GATES (no masses banked unless these pass):
 A. interpolation accuracy on a known analytic field (round-trip / refinement).
 B. m=1 branch-track reproduces the DIRECT m=1 solve masses across grids (the round minimum).
Only then is the m=2 branch-track trusted.  Foreground/synchronous.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import json, time
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from full3d_grid_shexact import make_grid_shexact
from full3d_solver import pack, unpack
import full3d_newton as NEW
import winding_catalog_map as WC


def bary_weights(x):
    n = len(x); w = np.ones(n)
    for j in range(n):
        d = x[j] - x; d[j] = 1.0
        w[j] = 1.0 / np.prod(d)
    return w


def bary_matrix(xf, xt):
    """Barycentric interpolation matrix L (len(xt) x len(xf)) mapping values on xf -> xt."""
    xf = np.asarray(xf, float); xt = np.asarray(xt, float)
    w = bary_weights(xf)
    L = np.zeros((len(xt), len(xf)))
    for i, x in enumerate(xt):
        diff = x - xf
        hit = np.where(np.abs(diff) < 1e-14)[0]
        if len(hit):
            L[i, hit[0]] = 1.0
        else:
            t = w / diff
            L[i, :] = t / t.sum()
    return L


def interp_field(f, Gf, Gt, Lr, Lth):
    """f: (Nr,Nth,Nps) torch on Gf -> (Nr',Nth',Nps') on Gt.
    r: Lr matmul (axis0); theta(mu): Lth matmul (axis1); psi: Fourier resample (axis2)."""
    x = f
    x = torch.tensordot(Lr, x, dims=([1], [0]))                 # (Nr',Nth,Nps)
    x = torch.tensordot(Lth, x, dims=([1], [1])).permute(1, 0, 2)  # (Nr',Nth',Nps)
    # psi Fourier resample Nps -> Nps'
    Np, Npt = Gf.Nps, Gt.Nps
    if Np != Npt:
        xn = x.cpu().numpy()
        F = np.fft.rfft(xn, axis=2)
        nmodes = min(F.shape[2], Npt // 2 + 1)
        Fn = np.zeros(x.shape[:2] + (Npt // 2 + 1,), dtype=complex)
        Fn[:, :, :nmodes] = F[:, :, :nmodes]
        xr = np.fft.irfft(Fn, n=Npt, axis=2) * (Npt / Np)
        x = torch.tensor(xr, device=f.device)
    return x.contiguous()


def interp_state(u, Gf, Gt):
    Lr = torch.tensor(bary_matrix(Gf.r.cpu().numpy(), Gt.r.cpu().numpy()), device=u.device)
    Lth = torch.tensor(bary_matrix(np.cos(Gf.th.cpu().numpy()), np.cos(Gt.th.cpu().numpy())), device=u.device)
    flds = [interp_field(f, Gf, Gt, Lr, Lth) for f in unpack(u, Gf)]
    return pack(*flds)


def Msolve(G, u0, m, maxit=40, p=0.4, kap8=0.05):
    u, hist = NEW.newton_solve(u0, G, p, kap8, m=m, maxit=maxit, tol=1e-12, verbose=False)
    dg, _ = WC.full_diag(u, G, p, kap8, m)
    return u, dg['M_MS'], dg['psivar'], hist[0], hist[-1]


def gate_A():
    """interpolation accuracy: smooth analytic field 18x8x8 -> 24x12x12, compare to exact."""
    Gf = make_grid_shexact(18, 8, 8, mmax=4); Gt = make_grid_shexact(24, 12, 12, mmax=6)
    def af(G):
        r = G.Rg / G.ri; th = G.THg; ps = G.PSg
        return torch.exp(-3 * r) * (1 + 0.3 * torch.cos(th)**2 + 0.2 * torch.sin(th)**2 * torch.cos(2 * ps))
    ff = af(Gf); exact = af(Gt)
    Lr = torch.tensor(bary_matrix(Gf.r.cpu().numpy(), Gt.r.cpu().numpy()), device=ff.device)
    Lth = torch.tensor(bary_matrix(np.cos(Gf.th.cpu().numpy()), np.cos(Gt.th.cpu().numpy())), device=ff.device)
    got = interp_field(ff, Gf, Gt, Lr, Lth)
    err = float((got - exact).abs().max())
    print(f"[GATE A] interp analytic 18x8x8->24x12x12 max err = {err:.2e}  {'PASS' if err < 1e-3 else 'FAIL'}")
    return err < 1e-3


def gate_B():
    """m=1 branch-track vs direct solve across grids (must match the round minimum)."""
    grids = [(16, 8, 8), (18, 8, 8), (20, 8, 8), (22, 8, 8)]
    G0 = make_grid_shexact(*grids[0], mmax=grids[0][2] // 2)
    u0, _ = WC.winding_seed(G0, 1)
    u, M0, ps0, h0, hf = Msolve(G0, u0, 1)
    print(f"[GATE B m=1] {grids[0]} direct M={M0:.5f} (Phi {h0:.1e}->{hf:.1e})")
    tracked = [M0]; ok = True; Gprev = G0
    for g in grids[1:]:
        Gt = make_grid_shexact(*g, mmax=g[2] // 2)
        ui = interp_state(u, Gprev, Gt)
        u, Mt, pst, hi, hf = Msolve(Gt, ui, 1, maxit=20)
        # direct comparison
        ud0, _ = WC.winding_seed(Gt, 1)
        _, Md, _, _, _ = Msolve(Gt, ud0, 1)
        dd = abs(Mt - Md)
        print(f"[GATE B m=1] {g} tracked M={Mt:.5f} (warm Phi {hi:.1e}->{hf:.1e}) vs direct M={Md:.5f} "
              f"diff={dd:.2e} {'ok' if dd < 5e-3 else 'MISMATCH'}")
        tracked.append(Mt); ok = ok and dd < 5e-3; Gprev = Gt
    print(f"[GATE B] m=1 tracked masses {np.round(tracked,5)}  {'PASS' if ok else 'FAIL'}")
    return ok


def branch_track_m2():
    """find lowest m=2 local min at 18x8x8 over seeds, then track up in resolution."""
    from phase3b_platonic_solve import platonic_shapes
    G0 = make_grid_shexact(18, 8, 8, mmax=4)
    u0, _ = WC.winding_seed(G0, 2)
    base_u, baseM, baseps, _, _ = Msolve(G0, u0, 2)
    cands = [(baseM, baseps, base_u, 'base')]
    a, b, c, d, Th = unpack(base_u, G0)
    for nm, sh in platonic_shapes(G0).items():
        for amp in (0.2, 0.4):
            us = pack(a.clone(), b.clone(), c.clone(), d.clone(), Th + amp * sh)
            uu, MM, pp, _, _ = Msolve(G0, us, 2, maxit=30)
            cands.append((MM, pp, uu, f'{nm}@{amp}'))
            print(f"[m=2 seed {nm}@{amp}] M={MM:.5f} psivar={pp:.3e}")
    M, ps, u, lbl = min(cands, key=lambda x: x[0])
    print(f"[m=2] LOWEST at 18x8x8: M={M:.5f} psivar={ps:.3e} via {lbl}")
    track = [dict(grid=[18, 8, 8], M=M, psivar=ps)]
    Gprev = G0
    for g in [(20, 8, 8), (22, 8, 8), (18, 10, 10), (20, 10, 10)]:
        Gt = make_grid_shexact(*g, mmax=g[2] // 2)
        ui = interp_state(u, Gprev, Gt)
        u, Mt, pst, hi, hf = Msolve(Gt, ui, 2, maxit=25)
        print(f"[m=2 track] {g} M={Mt:.5f} psivar={pst:.3e} (warm Phi {hi:.1e}->{hf:.1e})")
        track.append(dict(grid=list(g), M=Mt, psivar=pst, Phi=hf))
        Gprev = Gt
    json.dump(dict(lowest_18=dict(M=M, psivar=ps, via=lbl), track=track),
              open("/home/udt-admin/udt_mass_codex/cross_grid_branch_m2_out.json", "w"), indent=1)
    print("[m=2] tracked masses:", [round(t['M'], 4) for t in track])


if __name__ == "__main__":
    t0 = time.time()
    A = gate_A()
    B = gate_B() if A else False
    print(f"=== GATES: A={'PASS' if A else 'FAIL'} B={'PASS' if B else 'FAIL'} ({time.time()-t0:.0f}s) ===")
    if A and B:
        print("=== branch-tracking m=2 (gates passed) ===")
        branch_track_m2()
    else:
        print("=== GATES FAILED — interpolation/continuation not trusted; NO masses banked ===")
    print("DONE_BRANCH")

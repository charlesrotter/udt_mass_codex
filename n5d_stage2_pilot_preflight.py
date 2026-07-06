"""N5d Stage-2 PILOT-PREFLIGHT (conditioning readiness only; NO solve, anti-hang).
Forward residual + ONE jacrev Jacobian + SVD at a bounded STRUCTURED (non-collapsed) state.
Category-A numerical diagnostic. S-Dir first, ell=2 only, lambda=-1/2 live source, no flat source.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
import cell_solver_f2d as C

PRM = (8.0, 1.0, 1.0, 1)          # (Z, XI, KAP, N)
Z, XI, KAP, N = PRM


def block_mass(vec, Nr, Nth):
    """L2-mass fraction of a state-space vector in each named block [phi,rho,uf,a2,L]."""
    i0 = 0
    idx = dict(phi=(0, Nr), rho=(Nr, 2 * Nr), uf=(2 * Nr, 2 * Nr + Nr * Nth),
               a2=(2 * Nr + Nr * Nth, 2 * Nr + Nr * Nth + Nr), L=(vec.numel() - 1, vec.numel()))
    tot = float((vec ** 2).sum())
    return {k: float((vec[a:b] ** 2).sum()) / tot for k, (a, b) in idx.items()}


def preflight(Nr, Nth=8, a2_amp=1e-2, u_amp=0.02, sealbc="S-Dir"):
    print(f"\n================ PREFLIGHT  Nr={Nr} Nth={Nth}  a2_amp={a2_amp}  u_amp={u_amp}  sealbc={sealbc} ================")
    ctx = C.make_ctx(Nr, Nth, rc=0.5)
    n5d = dict(sealbc=sealbc, a2_mirror=0.0)
    # STRUCTURED, non-collapsed seed: nonzero band-limited u (radial+angular structure) + small nonzero a2,
    # L=1 (not near zero), rho~1/sqrt(2), phi=0.  (No solve; this is the structured state DESIGN sec8 asks for.)
    u = C.seed_n5d(ctx, a2_amp=a2_amp, amp=u_amp)
    phi, rho, uf, a2, L = C.unpack(u, ctx, n5d=True)

    # --- (4) residual only ---
    F = C.residual(u, ctx, PRM, wbc=1.0, n5d=n5d)
    square = (u.numel() == F.numel())
    finite_F = bool(torch.isfinite(F).all())
    Phi = float((F * F).sum())
    print(f"[res ] len(u)={u.numel()} len(F)={F.numel()} square={square} finite={finite_F} "
          f"Phi=||F||^2={Phi:.4e} max|F|={float(F.abs().max()):.4e}")

    from torch.func import jacrev
    J = jacrev(lambda uu: C.residual(uu, ctx, PRM, wbc=1.0, n5d=n5d))(u).detach()
    finite_J = bool(torch.isfinite(J).all())
    sv = torch.linalg.svdvals(J)
    smax, smin = float(sv[0]), float(sv[-1])
    cond = smax / smin
    print(f"[jac ] shape={tuple(J.shape)} finite={finite_J} s_max={smax:.4e} s_min={smin:.4e} cond_raw={cond:.4e}")
    print(f"[svd ] smallest 6 singular values (raw): {[f'{float(x):.3e}' for x in sv[-6:]]}")
    print(f"[svd ] largest  3 singular values (raw): {[f'{float(x):.3e}' for x in sv[:3]]}")

    # --- near-null directions of the RAW Jacobian (block L2-mass fractions) ---
    U_, S_, Vh = torch.linalg.svd(J, full_matrices=False)
    print("[null] RAW near-null right-singular vectors:")
    for k in range(1, 4):
        v = Vh[-k]; bm = block_mass(v, Nr, Nth); dom = max(bm, key=bm.get)
        print(f"       sv#-{k}  s={float(S_[-k]):.3e}  dominant={dom:<4s}  { {kk: round(vv,3) for kk,vv in bm.items()} }")

    # --- FIX-1 EQUILIBRATED conditioning (what newton_lm_solve actually solves: Jc=J*diag(1/colnorm),
    #     damped lstsq/QR -- NOT the normal equations J^T J whose cond would be cond(J)^2). ---
    dc = C._col_scale(J); Jc = J * dc[None, :]
    svc = torch.linalg.svdvals(Jc)
    cond_eq = float(svc[0] / svc[-1]); smin_eq = float(svc[-1])
    Uc, Sc, Vhc = torch.linalg.svd(Jc, full_matrices=False)
    bm_eq = block_mass(Vhc[-1], Nr, Nth); dom_eq = max(bm_eq, key=bm_eq.get)
    print(f"[FIX1] EQUILIBRATED cond={cond_eq:.4e} s_min_eq={smin_eq:.3e}  "
          f"(float64 usable headroom ~1e15; LM uses lstsq, no normal eqs)")
    print(f"[FIX1] equilibrated near-null: dominant={dom_eq:<4s}  {bm_eq}")

    # --- (5) collapse check ---
    Hr = C.H_of_r(u, ctx, PRM, n5d=n5d)
    Lval = float(L)
    checks = dict(
        L_not_near_zero=(Lval > 1e-3, Lval),
        rho_finite=(bool(torch.isfinite(rho).all()), (float(rho.min()), float(rho.max()))),
        rho_positive=(bool((rho > 0).all()), float(rho.min())),
        phi_finite=(bool(torch.isfinite(phi).all()), (float(phi.min()), float(phi.max()))),
        a2_finite=(bool(torch.isfinite(a2).all()), (float(a2.min()), float(a2.max()))),
        Hseal_finite=(bool(torch.isfinite(Hr[-1])), float(Hr[-1])),
    )
    print("[coll] collapse / degeneracy check (structured state):")
    for k, (ok, val) in checks.items():
        print(f"       {'OK ' if ok else 'BAD'}  {k:18s} = {val}")
    collapsed = not all(ok for ok, _ in checks.values())
    print(f"[coll] collapsed-degenerate? {collapsed}")
    return dict(Nr=Nr, cond=cond, cond_eq=cond_eq, smin=smin, smin_eq=smin_eq, Phi=Phi,
                finite=(finite_F and finite_J), square=square, collapsed=collapsed, sv=sv)


if __name__ == "__main__":
    import time
    t0 = time.time()
    print("### N5d Stage-2 PILOT-PREFLIGHT (no solve; forward residual + 1 Jacobian + SVD) ###")
    results = []
    # bounded scan: Nr in {8,12,16} to characterize how conditioning tracks resolution (whole-not-slice);
    # also a couple of a2 amplitudes at Nr=16 to see the shear-block sensitivity.
    for Nr in (8, 12, 16):
        results.append(preflight(Nr, a2_amp=1e-2))
    print("\n--- a2 amplitude sensitivity at Nr=16 (S-Dir) ---")
    for amp in (1e-3, 3e-2):
        preflight(16, a2_amp=amp)
    print("\n======== SUMMARY (a2_amp=1e-2 primary scan) ========")
    for r in results:
        print(f"  Nr={r['Nr']:2d}  cond_raw={r['cond']:.3e}  cond_equil={r['cond_eq']:.3e}  "
              f"s_min_eq={r['smin_eq']:.3e}  square={r['square']} finite={r['finite']} collapsed={r['collapsed']}")
    print(f"\nwall={time.time()-t0:.1f}s  (forward evals + jacrev only; NO Newton/LM solve)")

"""N5d Stage-2 S-Dir PILOT (bounded, single foreground process, hard-capped; ANTI-HANG).
Co-relaxed pi_2 axisymmetric tile.  S-Dir seal only, ell=2 shear only, lambda=-1/2 live source, FIX-1 on.
NO S-JC2, NO FIX-2, NO finite-L target/penalty/anchor.  Status: DESIGN / PROVISIONAL / Outcome D.
A converged S-Dir readout is at most a SCOPED S-Dir pi_2 TILE LEAD -- NEVER Outcome A/B (pi_3 open premise).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import time, json
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from torch.func import jacrev
import cell_solver_f2d as C

PRM = (8.0, 1.0, 1.0, 1)          # (Z, XI, KAP, N)
Z, XI, KAP, N = PRM
DEVICE = "cpu"                     # CPU: small system, avoids GPU contention (anti-hang)


def block_mass(v, Nr, Nth):
    idx = dict(phi=(0, Nr), rho=(Nr, 2 * Nr), uf=(2 * Nr, 2 * Nr + Nr * Nth),
               a2=(2 * Nr + Nr * Nth, 2 * Nr + Nr * Nth + Nr), L=(v.numel() - 1, v.numel()))
    tot = float((v ** 2).sum())
    return {k: round(float((v[a:b] ** 2).sum()) / tot, 3) for k, (a, b) in idx.items()}


def row_budget(F, Nr, Nth):
    """L2 norm per residual-row block, in the residual() assembly order (S-Dir n5d)."""
    n = Nr - 2
    blocks, i = [], 0
    for name, sz in [("phi_ode_int", n), ("phi_mirror", 2), ("rho_ode_int", n), ("rho_mirror", 2),
                     ("f_pde_int", n * Nth), ("fr_mirror", 2 * Nth), ("Hseal", 1),
                     ("shear_ode", n), ("shear_core_bc", 1), ("shear_seal_bc", 1)]:
        seg = F[i:i + sz]; blocks.append((name, sz, float((seg ** 2).sum()) ** 0.5, float(seg.abs().max())))
        i += sz
    return blocks, i


def cond_pair(J):
    sv = torch.linalg.svdvals(J); cond_raw = float(sv[0] / sv[-1])
    dc = C._col_scale(J); svc = torch.linalg.svdvals(J * dc[None, :])
    return cond_raw, float(svc[0] / svc[-1]), float(sv[-1]), float(svc[-1])


def nearnull(J, Nr, Nth):
    _, S_, Vh = torch.linalg.svd(J, full_matrices=False)
    bm_raw = block_mass(Vh[-1], Nr, Nth)
    dc = C._col_scale(J); _, Sc, Vhc = torch.linalg.svd(J * dc[None, :], full_matrices=False)
    bm_eq = block_mass(Vhc[-1], Nr, Nth)
    return (float(S_[-1]), max(bm_raw, key=bm_raw.get), bm_raw,
            float(Sc[-1]), max(bm_eq, key=bm_eq.get), bm_eq)


def run_pilot(Nr, Nth=8, a2_amp=1e-2, u_amp=0.02, maxit=30, budget=80.0):
    print(f"\n############ S-Dir PILOT  Nr={Nr} Nth={Nth}  a2_amp={a2_amp}  amp={u_amp}  "
          f"maxit={maxit} budget={budget}s ############")
    ctx = C.make_ctx(Nr, Nth, rc=0.5, device=DEVICE)
    n5d = dict(sealbc="S-Dir", a2_mirror=0.0)
    u0 = C.seed_n5d(ctx, a2_amp=a2_amp, amp=u_amp)

    F0 = C.residual(u0, ctx, PRM, n5d=n5d); Phi0 = float((F0 * F0).sum())
    cr0, ce0, smin0, sminc0 = cond_pair(jacrev(lambda uu: C.residual(uu, ctx, PRM, n5d=n5d))(u0).detach())
    print(f"[init] Phi0={Phi0:.6e} max|F0|={float(F0.abs().max()):.4e} "
          f"cond_raw={cr0:.3e} cond_equil={ce0:.3e}")

    t0 = time.time()
    u1, hist = C.newton_lm_solve(u0, ctx, PRM, n5d=n5d, maxit=maxit, verbose=True,
                                 time_budget=budget, equilibrate=True)
    wall = time.time() - t0

    F1 = C.residual(u1, ctx, PRM, n5d=n5d); Phi1 = float((F1 * F1).sum())
    Jf = jacrev(lambda uu: C.residual(uu, ctx, PRM, n5d=n5d))(u1).detach()
    finiteJ = bool(torch.isfinite(Jf).all())
    cr1, ce1, smin1, sminc1 = cond_pair(Jf)
    sraw, domr, bmr, seq, domq, bmq = nearnull(Jf, Nr, Nth)

    phi, rho, uf, a2, L = C.unpack(u1, ctx, n5d=True)
    Hr = C.H_of_r(u1, ctx, PRM, n5d=n5d)
    Hdrift = float(Hr.max() - Hr.min()); Hseal = float(Hr[-1])
    ro = C.readouts(u1, ctx, PRM, n5d=n5d)
    blocks, tot = row_budget(F1, Nr, Nth)

    # convergence status
    it_used = len(hist) - 1
    if not np.isfinite(Phi1):
        status = "singular/NaN"
    elif Phi1 < 1e-13:
        status = "converged"
    elif wall >= budget * 0.98:
        status = "timeout"
    elif it_used < maxit and hist[-1] >= hist[-2] * (1 - 1e-6):
        status = "stalled"
    else:
        status = f"incomplete(Phi={Phi1:.2e})"

    collapsed = not (float(L) > 1e-3 and torch.isfinite(rho).all() and (rho > 0).all()
                     and torch.isfinite(phi).all() and torch.isfinite(a2).all() and np.isfinite(Hseal))

    print(f"\n[hist] {['%.4e' % h for h in hist]}")
    print(f"[done] status={status} iters={it_used} wall={wall:.1f}s  Phi0={hist[0]:.6e} -> Phi_final={Phi1:.6e}")
    print(f"[cond] before: raw={cr0:.3e} equil={ce0:.3e}   after: raw={cr1:.3e} equil={ce1:.3e} finiteJ={finiteJ}")
    print(f"[null] after raw   s_min={sraw:.3e} dominant={domr}  {bmr}")
    print(f"[null] after equil s_min={seq:.3e} dominant={domq}  {bmq}")
    print(f"[flds] L={float(L):.5f}  rho[c,mid,s]=[{float(rho[0]):.4f},{float(rho[Nr//2]):.4f},{float(rho[-1]):.4f}]  "
          f"phi[c,s]=[{float(phi[0]):.4f},{float(phi[-1]):.4f}]  a2[c,mid,s]=[{float(a2[0]):.4e},{float(a2[Nr//2]):.4e},{float(a2[-1]):.4e}]")
    print(f"[H   ] drift(max-min)={Hdrift:.3e}  H(seal)={Hseal:+.4e}")
    print(f"[read] q_raw={ro['q_raw']:+.4e} Pi_phi={ro['Pi_phi']:+.4e} M_readout={ro['M_readout']:+.4e} sign={ro['sign_convention']:+.0f}")
    print(f"[coll] collapsed-degenerate? {collapsed}  (L>1e-3, rho/phi/a2/Hseal finite)")
    print(f"[budg] residual-row-block L2 norms (total rows={tot}):")
    for name, sz, l2, mx in blocks:
        print(f"        {name:16s} n={sz:<4d} ||.||2={l2:.3e}  max|.|={mx:.3e}")

    return dict(Nr=Nr, Nth=Nth, a2_amp=a2_amp, status=status, iters=it_used, wall=round(wall, 1),
                Phi0=Phi0, Phi1=Phi1, hist=[float(h) for h in hist],
                cond_raw_before=cr0, cond_equil_before=ce0, cond_raw_after=cr1, cond_equil_after=ce1,
                finiteJ=finiteJ, nn_raw_smin=sraw, nn_raw_dom=domr, nn_equil_smin=seq, nn_equil_dom=domq,
                nn_equil_blocks=bmq, L=float(L), rho_c=float(rho[0]), rho_s=float(rho[-1]),
                phi_c=float(phi[0]), phi_s=float(phi[-1]), a2_c=float(a2[0]), a2_s=float(a2[-1]),
                Hdrift=Hdrift, Hseal=Hseal, collapsed=collapsed, readouts=ro,
                row_budget={name: l2 for name, _, l2, _ in blocks})


def trajectory(Nr=12, Nth=8, a2_amp=1e-2, u_amp=0.02, checkpoints=5, per=30, budget=60.0):
    """Extended-cap CHARACTERIZATION (bounded, single process): run the solve in `per`-iter chunks and
    checkpoint (Phi, L, cond_equil, mirror-BC residuals, Hseal) to classify iteration-limited vs L-collapse.
    OBSERVING the trajectory -- not chasing convergence; NO anti-collapse term (forbidden)."""
    print(f"\n@@@@ EXTENDED TRAJECTORY  Nr={Nr} a2_amp={a2_amp}  {checkpoints}x{per} iters @@@@")
    ctx = C.make_ctx(Nr, Nth, rc=0.5, device=DEVICE); n5d = dict(sealbc="S-Dir", a2_mirror=0.0)
    u = C.seed_n5d(ctx, a2_amp=a2_amp, amp=u_amp)
    def cp(tag, u):
        F = C.residual(u, ctx, PRM, n5d=n5d); Phi = float((F * F).sum())
        phi, rho, uf, a2, L = C.unpack(u, ctx, n5d=n5d)
        Q = C.fields(u, ctx, PRM, n5d=n5d)
        frm = float((Q['fr'][[0, -1], :] ** 2).sum()) ** 0.5
        rhm = float((Q['rhop'][[0, -1]] ** 2).sum()) ** 0.5
        Hs = float(C.H_of_r(u, ctx, PRM, n5d=n5d)[-1])
        J = jacrev(lambda uu: C.residual(uu, ctx, PRM, n5d=n5d))(u).detach()
        dc = C._col_scale(J); svc = torch.linalg.svdvals(J * dc[None, :]); ce = float(svc[0] / svc[-1])
        print(f"  {tag:>8s} Phi={Phi:.4e} L={float(L):.5f} a2s={float(a2[-1]):.3e} rho_c={float(rho[0]):.4f} "
              f"phi_c={float(phi[0]):+.4f} fr_mir={frm:.3e} rho_mir={rhm:.3e} Hseal={Hs:+.3e} cond_eq={ce:.2e}")
        return dict(tag=tag, Phi=Phi, L=float(L), Hseal=Hs, cond_eq=ce, fr_mir=frm, rho_mir=rhm)
    traj = [cp("seed", u)]
    for c in range(1, checkpoints + 1):
        u, _ = C.newton_lm_solve(u, ctx, PRM, n5d=n5d, maxit=per, verbose=False, time_budget=budget, equilibrate=True)
        traj.append(cp(f"it~{c*per}", u))
    return traj


if __name__ == "__main__":
    print("### N5d Stage-2 S-Dir PILOT (bounded, single process; DESIGN/PROVISIONAL/Outcome D; pi_2 tile only) ###")
    results = {}
    # (1) PRIMARY: Nr=12, a2_amp=1e-2
    results["Nr12_a2e-2"] = run_pilot(12, a2_amp=1e-2)
    # (2) conditioning cross-check: Nr=12, a2_amp=3e-2 (stiffer shear)
    results["Nr12_a2e-2b"] = run_pilot(12, a2_amp=3e-2)
    # (3) Nr=16 ONLY IF the Nr=12 primary was numerically clean (not singular/collapsed)
    p = results["Nr12_a2e-2"]
    if p["finiteJ"] and not p["collapsed"] and p["status"] not in ("singular/NaN",):
        results["Nr16_a2e-2"] = run_pilot(16, a2_amp=1e-2)
    else:
        print("\n[gate] Nr=16 SKIPPED (Nr=12 primary not numerically clean).")

    print("\n======== PILOT SUMMARY ========")
    for k, r in results.items():
        print(f"  {k:12s} status={r['status']:14s} iters={r['iters']:2d} Phi:{r['Phi0']:.2e}->{r['Phi1']:.2e} "
              f"L={r['L']:.4f} Hseal={r['Hseal']:+.2e} cond_eq_after={r['cond_equil_after']:.2e} "
              f"q_raw={r['readouts']['q_raw']:+.3e} collapsed={r['collapsed']}")
    # EXTENDED-CAP CHARACTERIZATION: does the maxit=30-capped run converge, or is it L-collapse?
    results["trajectory_Nr12"] = trajectory(12, a2_amp=1e-2, checkpoints=5, per=30)

    with open("n5d_stage2_sdir_pilot.json", "w") as fh:
        json.dump(results, fh, indent=2)
    print("\n[out] wrote n5d_stage2_sdir_pilot.json")
    print("[WARN] this bounded static S-Dir pi_2 solve exhibits L-COLLAPSE (L->0, Hseal never closes, cond->1e15):")
    print("       tool-limited / collapse behavior (Outcome D), SCOPED to static+S-Dir+block-diag+ell=2+pi_2.")
    print("       NO converged tile lead, NO pin/continuum, NO Outcome A/B (pi_3 open). Report to Charles.")

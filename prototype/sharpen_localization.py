#!/usr/bin/env python3
"""
sharpen_localization.py -- TIGHTEN the X-continuation floors + INTERIOR/EDGE
discriminator + the cold-vs-continuation MULTI-BRANCH check at X=-2e5.

Driver: Claude (Opus 4.8). 2026-06-24. OBSERVE. DATA-BLIND. NEW FILE; reuses
the immutable residual/lm_solve verbatim.

The X-continuation found a more-structured branch (conc~2.5) the cold seed
missed, but it was edge-pinned (r_peak at the body's OUTER edge), loosely
floored (~2 iters), and differed from the cold -2e5 state (multi-branch).
Charles: TIGHTEN + interior/edge test.  This script:
  1. Re-floors saved continuation fields at representative X TIGHTLY (more iters).
  2. Prints the FULL radial proper-energy profile -> classify INTERIOR CORE
     (real body: interior max, declines both sides) vs OUTER-EDGE/seal pile-up
     (monotone rise to the boundary) vs CORE-concentrated.
  3. Multi-branch: floors BOTH the continuation field AND a cold seed at -2e5,
     compares (same solution = drift; distinct low-residual = two real branches).
"""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import sys, time
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import branchGP_native_s2_coupled_OBSERVE as B
from jfnk_branch_solver import _grid

NR = 10; P = 1.0; BR = "P"
XI, KAP, KAP8, M = B.XI_PROD, B.KAP_PROD, B.KAP8, B.M_WIND
t0 = time.time(); log = lambda s: print(s, flush=True)
G = _grid(NR)
rfull = G.r.cpu().numpy()
bodymask = G.body.cpu().numpy()
# body radial nodes (mid angular column) -- which r indices are interior body
jt, jp = G.Nth // 2, G.Nps // 2
body_r_idx = np.where(bodymask[:, jt, jp])[0]
log(f"grid r nodes: " + " ".join(f"{x:.2f}" for x in rfull))
log(f"body radial idx (mid-ang): {list(body_r_idx)}  -> r in "
    f"[{rfull[body_r_idx.min()]:.2f}, {rfull[body_r_idx.max()]:.2f}]  "
    f"(cell rc={G.rc:.2f}..ri={G.ri:.2f})")


def classify(u, X, tag):
    dg = B.diagnose(u, G, X, XI, KAP, m=M, kap8=KAP8, branch=BR)
    pr = dg['proper_rho']      # full radial line, mid-angle
    r = dg['r']
    bi = body_r_idx
    prb = pr[bi]; rb = r[bi]
    imax = bi[int(np.argmax(np.abs(prb)))]
    # position of peak within body: 0=core-edge .. 1=outer-edge
    frac = (np.where(bi == imax)[0][0]) / max(len(bi) - 1, 1)
    # monotonicity over body
    dpr = np.diff(np.abs(prb))
    mono_up = np.all(dpr > -1e-30); mono_dn = np.all(dpr < 1e-30)
    interior = (0.15 < frac < 0.85) and not mono_up and not mono_dn
    if interior:
        kind = "INTERIOR CORE (body!)"
    elif frac >= 0.85 or mono_up:
        kind = "OUTER-EDGE/seal pile-up"
    elif frac <= 0.15 or mono_dn:
        kind = "CORE-concentrated (r->rc)"
    else:
        kind = "ambiguous"
    centroid = float((rb * np.abs(prb)).sum() / max(np.abs(prb).sum(), 1e-30))
    log(f"\n  [{tag}] X={X:.1e}  M_MS={dg['M_MS']:.4e}  AB={dg['AB']:.3e}  "
        f"phi_depth={max(abs(dg['phi_min']),abs(dg['phi_max'])):.3e}  tw={dg['tw_amp']:.2e}")
    log(f"     proper-energy peak at r={r[imax]:.2f} (body-frac {frac:.2f})  "
        f"centroid <r>={centroid:.2f}  => {kind}")
    log(f"     proper-rho(r) FULL: " +
        " ".join(f"{rfull[i]:.2f}{'*' if bodymask[i,jt,jp] else ' '}:{pr[i]:+.2e}"
                 for i in range(len(rfull))))
    log(f"     phi(r) FULL:        " +
        " ".join(f"{rfull[i]:.2f}:{dg['phi_r'][i]:+.2e}" for i in range(len(rfull))))
    return dg


# ---- 1+2. tighten + classify representative X (load saved continuation fields) ----
for absX, X in [(3e1, -30.0), (1e3, -1e3), (2e5, -2e5)]:
    path = f"/tmp/uP_X{absX:.0e}.pt"
    if not os.path.exists(path):
        log(f"  (missing {path})"); continue
    log("\n" + "=" * 78); log(f"TIGHTEN X={X:.1e}  (from {path})")
    u = torch.load(path).to('cuda' if torch.cuda.is_available() else 'cpu')
    u, hist, tsec, capped = B.lm_solve(u, G, P, X, XI, KAP, m=M, kap8=KAP8,
                                       branch=BR, maxit=20, lam0=1e-4,
                                       wall_cap=110.0, verbose=False)
    log(f"  floored Phi {hist[0]:.2e} -> {hist[-1]:.2e}  in {len(hist)-1} it / {tsec:.0f}s")
    classify(u, X, f"cont-tight")
    if abs(X) == 2e5:
        torch.save(u.cpu(), "/tmp/uP_X2e5_tight.pt")

# ---- 3. multi-branch at -2e5: continuation-tight vs cold-seed-tight ----
log("\n" + "=" * 78); log("MULTI-BRANCH CHECK at X=-2e5  (continuation vs cold seed)")
Xt = -2e5
u_cold0 = B.make_seed(G, P)
u_cold, hc, tc, capc = B.lm_solve(u_cold0, G, P, Xt, XI, KAP, m=M, kap8=KAP8,
                                  branch=BR, maxit=20, lam0=1e-3,
                                  wall_cap=140.0, verbose=False)
log(f"  cold-seed floored Phi -> {hc[-1]:.2e}  in {len(hc)-1} it / {tc:.0f}s")
dg_cold = classify(u_cold, Xt, "cold")
u_cont = torch.load("/tmp/uP_X2e5_tight.pt").to(u_cold.device) \
    if os.path.exists("/tmp/uP_X2e5_tight.pt") else None
if u_cont is not None:
    dg_cont = classify(u_cont, Xt, "cont")
    diff = float((u_cont - u_cold).abs().max())
    log(f"\n  MULTI-BRANCH VERDICT: max|u_cont - u_cold| = {diff:.3e}")
    log(f"     AB: cont={dg_cont['AB']:.3e} cold={dg_cold['AB']:.3e}   "
        f"M_MS: cont={dg_cont['M_MS']:.4e} cold={dg_cold['M_MS']:.4e}")
    log(f"     => {'DISTINCT branches (both floored)' if diff > 1e-2 else 'SAME (continuation drift)'}")

log(f"\n=== SHARPEN DONE  total={time.time()-t0:.0f}s ===")

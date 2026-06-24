#!/usr/bin/env python3
"""
jfnk_equil_floor.py -- JFNK (matrix-free) + DETERMINISTIC Ruiz 2-sided
equilibration PC.  The synthesis of the 2026-06-23 ponder:

  * JFNK matrix-free LSMR floored Branch P to 3.49 (good globalization on the
    stiff exp(2phi) phi-equation) but used a NOISY stochastic Jacobi PC.
  * Ruiz equilibration provably FIXED the conditioning (smax 2.5e6->13.5; the
    interior-Einstein "obstruction" was a SCALING artifact -> Einstein residual
    went to 0, residual moved to EL_phi) but the dense-LM globalization STALLED
    at 569.
  => Combine: JFNK's inexact-Newton + Ruiz's deterministic 2-sided diagonal PC,
     replacing the stochastic Jacobi PC.  Reuses the IMMUTABLE make_ops + lsmr
     verbatim, wrapped with frozen row/col scales D_r, D_c.

Solve the SCALED Newton system  (D_r J D_c)(D_c^-1 du) = -(D_r F)  via LSMR,
then du = D_c * dy.  D_r, D_c from Ruiz on a dense J formed at the seed
(refreshed once mid-run).  No frozen DOF, no import; deterministic.

Driver: Claude (Opus 4.8).  2026-06-23.  OBSERVE.  DATA-BLIND.  NEW FILE.
Bounded: Nr=10, single process, hard wall-cap.
"""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import sys, time, math
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import branchGP_native_s2_coupled_OBSERVE as B
from jfnk_branch_solver import _grid, make_ops, lsmr

NR = 10; P = 1.0; BR = "P"
X, XI, KAP, KAP8, M = B.X_PROD, B.XI_PROD, B.KAP_PROD, B.KAP8, B.M_WIND
WBC = 30.0; WALL = 360.0
t0 = time.time(); log = lambda s: print(s, flush=True)

log("=" * 72); log(f"JFNK + RUIZ-EQUILIBRATION FLOOR  branch={BR}  Nr={NR}"); log("=" * 72)
G = _grid(NR)
u = B.make_seed(G, P)
fwd = lambda uu: B.residual_vec(uu, G, P, X, XI, KAP, m=M, kap8=KAP8, branch=BR, wbc=WBC)
nU = u.numel()


def ruiz_scales(uu, iters=12, eps=1e-30):
    J, _ = B.jac_jacrev(uu, G, P, X, XI, KAP, M, KAP8, BR, WBC, chunk_size=128)
    J = J.reshape(-1, nU)
    Dr = torch.ones(J.shape[0], device=J.device); Dc = torch.ones(nU, device=J.device)
    Js = J
    for _ in range(iters):
        r = torch.sqrt(torch.clamp(Js.abs().amax(dim=1), min=eps))
        c = torch.sqrt(torch.clamp(Js.abs().amax(dim=0), min=eps))
        Js = Js / r[:, None] / c[None, :]; Dr = Dr / r; Dc = Dc / c
    return Dr.detach(), Dc.detach()


log("\n[equil] Ruiz scales from dense J at seed ...")
Dr, Dc = ruiz_scales(u)
log(f"  Dr range [{float(Dr.min()):.2e},{float(Dr.max()):.2e}]  "
    f"Dc range [{float(Dc.min()):.2e},{float(Dc.max()):.2e}]")

F = fwd(u); Phi = float((F * F).sum()); hist = [Phi]; lam = 1e-3
log(f"start Phi={Phi:.4e}  nU={nU} nF={F.numel()}")
for it in range(30):
    if Phi < 1e-10 or time.time() - t0 > WALL:
        break
    if it == 10:                          # refresh scales once mid-run
        Dr, Dc = ruiz_scales(u)
    F0, Jv, JTw = make_ops(u, G, P, X, XI, KAP, M, KAP8, BR, WBC)
    # scaled matrix-free operators: J~ = Dr J Dc
    Jv_s = lambda v: Dr * Jv(Dc * v)
    JTw_s = lambda w: Dc * JTw(Dr * w)
    Fs = Dr * F0
    ratio = math.sqrt(max(Phi, 1e-300) / max(hist[0], 1e-300))
    eta = min(1e-1, max(1e-4, 1e-1 * ratio))
    accepted = False
    for _t in range(12):
        if time.time() - t0 > WALL:
            break
        damp = math.sqrt(lam)
        dy, nit = lsmr(Jv_s, JTw_s, Fs, nU, damp, maxit=300, tol=eta)
        du = (Dc * dy).reshape(u.shape)
        Pn = float((fwd(u + du) ** 2).sum())
        if np.isfinite(Pn) and Pn < Phi:
            u = u + du; Phi = Pn; lam = max(lam * 0.3, 1e-13); accepted = True; break
        lam = min(lam * 4.0, 1e8)
    hist.append(Phi)
    log(f"  it={it:2d} Phi={Phi:.4e} lam={lam:.1e} eta={eta:.1e} lsmr={nit} "
        f"t={time.time()-t0:.0f}s {'acc' if accepted else 'STALL'}")
    if not accepted:
        break
torch.save(u.cpu(), "/tmp/uP_jfnk_equil.pt")
log(f"\nFLOORED: Phi={Phi:.4e}  iters={len(hist)-1}  t={time.time()-t0:.0f}s")

# verdict diagnostics on the floored field
F = fwd(u).detach()
dg = B.diagnose(u, G, X, XI, KAP, m=M, kap8=KAP8, branch=BR)
B.print_diag(f"JFNK-EQUIL-{BR}", dg, hist, time.time()-t0, False, G)
nbody = int(G.body.sum()); nINT = 9 * nbody; totF = float((F**2).sum())
names = ["E_TT","E_RR","E_THTH","E_PSPS","E_RTH","E_RPS","E_THPS","EL_phi","EL_gtw"]
log("\n  raw ||F||^2 share by interior block:")
for k, nm in enumerate(names):
    log(f"     {nm:8s} {float((F[k*nbody:(k+1)*nbody]**2).sum())/totF:.3f}")
log(f"     BC-rows  {float((F[nINT:]**2).sum())/totF:.3f}")

log("\n  DERRICK curve  E(s)=M_MS(u(r/s))  on the floored field:")
rgrid = G.r
def dilate(u_in, s):
    flds = B.unpack6(u_in); out = []
    rq = (rgrid / s).clamp(min=float(rgrid.min()), max=float(rgrid.max()))
    idx = torch.searchsorted(rgrid.contiguous(), rq.contiguous()).clamp(1, len(rgrid)-1)
    r0 = rgrid[idx-1]; r1 = rgrid[idx]; w = ((rq-r0)/(r1-r0)).view(-1,1,1)
    for f in flds:
        out.append((1-w)*f[idx-1] + w*f[idx])
    return torch.stack(out, 0)
for s in [0.6, 0.75, 0.87, 1.0, 1.15, 1.33, 1.55, 1.8]:
    us = dilate(u, s); d2 = B.diagnose(us, G, X, XI, KAP, m=M, kap8=KAP8, branch=BR)
    log(f"     s={s:.2f}  M_MS={d2['M_MS']:.5e}  phi_min={d2['phi_min']:+.3e}  "
        f"tw={d2['tw_amp']:.2e}  AB={d2['AB']:.3e}")
log(f"\n=== JFNK+EQUIL FLOOR DONE  total={time.time()-t0:.0f}s ===")

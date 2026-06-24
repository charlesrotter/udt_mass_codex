#!/usr/bin/env python3
"""
equilibrated_lm_floor.py -- FLOOR Branch P with a Ruiz-EQUILIBRATED LM.

Driver: Claude (Opus 4.8).  2026-06-23.  OBSERVE mode.  DATA-BLIND.  NEW FILE;
reuses the immutable branchGP residual + jac_jacrev verbatim.

WHY (the ponder's verdict, 2026-06-23):
  The Branch-P "stall" was a stochastic-PC artifact; the REAL wall is the #60
  conditioning wall -- cond(J)~1e10 (sigma 1.5e-4 .. 2.5e6), localized on the
  interior time/radial Einstein equations (E_TT, E_RR carry the irreducible
  residual).  That is a SCALING/equilibration problem (X=-2e5 + e^{2phi} weight
  amplify some rows; phi~1e-5 vs a,b~O(1) mis-scale columns), NOT a physical
  modulus (the dilation direction is NOT the flat mode: overlap ~0.09).  Charles
  (2026-06-23): EQUILIBRATE, then floor.  Solver-first: fix our application.

WHAT:
  Standard Ruiz (2001) 2-sided equilibration of the Newton system each LM step:
  D_r J D_c has unit inf-norm rows & cols => cond cut by orders of magnitude.
  Solve the WELL-SCALED damped least squares in y=D_c^{-1} du space, unscale.
  This is deterministic non-dimensionalization, no frozen DOF, no import.
  Report cond(J) BEFORE vs AFTER (success criterion) + re-run the cokernel /
  Derrick diagnostics on the PROPERLY floored field for the real verdict.

Bounded: Nr=10, single process, hard wall-cap.  jacrev ~36s/iter at Nr=10.
"""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import sys, time, math
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import branchGP_native_s2_coupled_OBSERVE as B
from jfnk_branch_solver import _grid

NR = 10; P = 1.0; BR = "P"
X, XI, KAP, KAP8, M = B.X_PROD, B.XI_PROD, B.KAP_PROD, B.KAP8, B.M_WIND
WBC = 30.0
WALL = 420.0
t0 = time.time()
log = lambda s: print(s, flush=True)

log("=" * 72)
log(f"EQUILIBRATED-LM FLOOR  branch={BR}  Nr={NR}  (Ruiz 2-sided)")
log("=" * 72)

G = _grid(NR)
u = B.make_seed(G, P)
fwd = lambda uu: B.residual_vec(uu, G, P, X, XI, KAP, m=M, kap8=KAP8, branch=BR, wbc=WBC)
nU = u.numel()


def ruiz(J, iters=12, eps=1e-30):
    """Ruiz inf-norm 2-sided equilibration. Returns D_r (nF), D_c (nU)."""
    nF, nU = J.shape
    Dr = torch.ones(nF, device=J.device); Dc = torch.ones(nU, device=J.device)
    Js = J
    for _ in range(iters):
        r = torch.sqrt(torch.clamp(Js.abs().amax(dim=1), min=eps))
        c = torch.sqrt(torch.clamp(Js.abs().amax(dim=0), min=eps))
        Js = Js / r[:, None] / c[None, :]
        Dr = Dr / r; Dc = Dc / c
    return Dr, Dc, Js


def cond_est(J):
    s = torch.linalg.svdvals(J)
    return float(s[0] / torch.clamp(s[-1], min=1e-300)), float(s[0]), float(s[-1])


# ---------------- equilibrated LM loop ----------------
F = fwd(u); Phi = float((F * F).sum()); hist = [Phi]
lam = 1e-3
log(f"\nstart Phi={Phi:.4e}  nU={nU} nF={F.numel()}")
for it in range(14):
    if Phi < 1e-12 or time.time() - t0 > WALL:
        break
    J, F = B.jac_jacrev(u, G, P, X, XI, KAP, M, KAP8, BR, WBC, chunk_size=128)
    J = J.reshape(F.numel(), nU)
    if it == 0:
        c0, smax0, smin0 = cond_est(J)
        log(f"  [cond BEFORE equilibration] cond={c0:.2e}  smax={smax0:.2e} smin={smin0:.2e}")
    Dr, Dc, Js = ruiz(J, iters=12)
    if it == 0:
        c1, smax1, smin1 = cond_est(Js)
        log(f"  [cond AFTER  equilibration] cond={c1:.2e}  smax={smax1:.2e} smin={smin1:.2e}  "
            f"(reduction {c0/c1:.1e}x)")
    Fs = Dr * F
    I = torch.eye(nU, device=u.device)
    accepted = False
    for _t in range(10):
        Jaug = torch.cat([Js, math.sqrt(lam) * I], dim=0)
        Faug = torch.cat([-Fs, torch.zeros(nU, device=u.device)], dim=0)
        try:
            dy = torch.linalg.lstsq(Jaug, Faug).solution
        except Exception:
            lam *= 4.0; continue
        du = (Dc * dy).reshape(u.shape)
        un = u + du
        Pn = float((fwd(un) ** 2).sum())
        if np.isfinite(Pn) and Pn < Phi:
            u = un; Phi = Pn; lam = max(lam * 0.3, 1e-13); accepted = True; break
        lam *= 4.0
    hist.append(Phi)
    log(f"  it={it:2d} Phi={Phi:.4e} lam={lam:.1e} t={time.time()-t0:.0f}s "
        f"{'acc' if accepted else 'STALL'}")
    if not accepted:
        break
torch.save(u.cpu(), "/tmp/uP_equil.pt")
log(f"\nFLOORED: Phi={Phi:.4e}  iters={len(hist)-1}  t={time.time()-t0:.0f}s")

# ---------------- verdict diagnostics on the floored field ----------------
F = fwd(u).detach()
dg = B.diagnose(u, G, X, XI, KAP, m=M, kap8=KAP8, branch=BR)
B.print_diag(f"EQUIL-{BR}", dg, hist, time.time()-t0, False, G)

# cokernel localization (did the interior-Einstein obstruction shrink?)
J, _ = B.jac_jacrev(u, G, P, X, XI, KAP, M, KAP8, BR, WBC, chunk_size=128)
J = J.reshape(F.numel(), nU)
cF, smax, smin = cond_est(J)
log(f"\n  cond(J) at floor = {cF:.2e}  (smax={smax:.2e} smin={smin:.2e})")
U, S, Vh = torch.linalg.svd(J, full_matrices=False)
nbody = int(G.body.sum()); nINT = 9 * nbody
eps_sv = 1e-6 * float(S[0]); mask = S < eps_sv
Us = U[:, mask]; PcokF = Us @ (Us.t() @ F)
log(f"  ||P_coker F||^2/||F||^2 = {float((PcokF.norm()/F.norm())**2):.4f}  "
    f"(#sigma<1e-6 smax = {int(mask.sum())})")
names = ["E_TT","E_RR","E_THTH","E_PSPS","E_RTH","E_RPS","E_THPS","EL_phi","EL_gtw"]
log("  raw ||F||^2 share by interior block (where residual lives now):")
totF = float((F**2).sum())
for k, nm in enumerate(names):
    seg = F[k*nbody:(k+1)*nbody]
    log(f"     {nm:8s} {float((seg**2).sum())/totF:.3f}")
log(f"     BC-rows  {float((F[nINT:]**2).sum())/totF:.3f}")

# Derrick energy curve on the PROPERLY floored field
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
        f"AB={d2['AB']:.3e}")

log(f"\n=== EQUILIBRATED FLOOR DONE  total={time.time()-t0:.0f}s ===")

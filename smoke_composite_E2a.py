"""smoke_composite_E2a.py -- the ONE bounded smoke solve of the E2a brief (NOT a physics verdict;
NOT the E2b sweep). Purpose: CONDITIONING REPORT -- Jacobian conditioning, step behavior, where
the residual mass sits. Whatever the solve does is reported as smoke-test behavior only.

Pre-committed smoke configuration (E2a brief):
  bracket     : A1 m=3 Z=8                                  (ONE bracket)
  window cell : N=1, xi=0.5, kap=0.1                        (E1 necessary-map admissible N=1
                moderate-xi plateau cell; microphysics_E1_probe_results.json necessary_map:
                plateau_admissible=True, outer_seal_admissible=False -- position-selective)
  seed        : ONE -- rigid + moderate bulge (amp=0.5), r_p0 = 100 (deep plateau interior)
                [amp, r_p0 = CHOSE-smoke conditioning values, reported]
  grids       : cell Nr=12 (<= 12 per brief), Nth=8; ambient Na=192, kmap=2.5 (wall-resolved)
  iters       : LM <= 60, wall budget 480 s, SINGLE process (anti-hang)
  device      : cuda if available (Charles GPU addition), with CPU spot-check of the residual.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import sys
import time
import math
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

REPO = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, REPO)
import cell_solver_composite as C

t0 = time.time()
LAB = "A1 m=3 Z=8"
XI, KAP, NW = 0.5, 0.1, 1
Nr, Nth, Na = 12, 8, 192
KMAP = 2.5
RP0, AMP = 100.0, 0.5
MAXIT, BUDGET = 60, 480.0
DEV = "cuda" if torch.cuda.is_available() else "cpu"

br = C.load_bracket(LAB)
prm = (br["Z"], XI, KAP, NW)
ctx = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device=DEV)
v0 = C.seed_comp(ctx, br, rp0=RP0, amp=AMP, device=DEV)
n = v0.numel()

print("=" * 92)
print(f"E2a SMOKE TEST  bracket={LAB}  window cell (N,xi,kap)=({NW},{XI},{KAP})  device={DEV}")
print(f"  grids: cell Nr={Nr} Nth={Nth} | ambient Na={Na} kmap={KMAP} | unknowns n={n}")
print(f"  seed: rigid + bulge amp={AMP} at r_p0={RP0} (CHOSE-smoke), r_sU0={br['r_s']:.3f}")
print("  PURPOSE: conditioning report only -- no physics verdict is read from this run.")
print("=" * 92)

# ---------- row / unknown block maps (for residual-mass and singular-vector reporting) ----------
row_blocks = []
def add_block(name, k):
    s = sum(k2 for _, k2 in row_blocks)
    row_blocks.append((name, k))
    return s
for name, k in [("cell phi-ODE", Nr - 2), ("cell rho-ODE", Nr - 2), ("f-PDE", (Nr - 2) * Nth),
                ("core phi'", 1), ("core rho'", 1), ("core f_r", Nth), ("C1c f_r(seal)", Nth),
                ("amb phi-ODE", Na - 2), ("amb rho-ODE", Na - 2),
                ("seal [phi]", 1), ("seal [rho]", 1), ("C1a", 1), ("C1b", 1), ("C2", 1),
                ("fold phi", 1), ("fold rho'", 1), ("fold H_amb", 1)]:
    add_block(name, k)
unk_blocks = [("phi_cell", Nr), ("rho_cell", Nr), ("u", Nr * Nth),
              ("phi_amb", Na), ("rho_amb", Na), ("r_p", 1), ("r_sU", 1)]

def block_norms(F, blocks):
    out = []; i = 0
    for name, k in blocks:
        seg = F[i:i + k]; i += k
        out.append((name, float(np.sqrt((seg * seg).sum())), float(np.abs(seg).max())))
    return out

resfn = lambda vv: C.residual_comp(vv, ctx, prm, br)

# ---------- seed diagnostics ----------
F0 = resfn(v0)
print(f"\nSEED: Phi0=||F||^2 = {float((F0*F0).sum()):.6e}   max|F| = {float(F0.abs().max()):.3e}"
      f"   all-finite: {bool(torch.isfinite(F0).all())}")
if DEV == "cuda":   # banked GPU discipline: CPU spot-check
    ctx_c = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device="cpu")
    F0c = C.residual_comp(v0.cpu(), ctx_c, prm, br)
    print(f"  GPU-vs-CPU residual spot-check: rel maxdiff = "
          f"{float((F0.cpu()-F0c).abs().max())/max(1.0,float(F0c.abs().max())):.2e}")
print("  residual mass by ROW BLOCK at seed (l2, max):")
for name, l2, mx in block_norms(F0.detach().cpu().numpy(), row_blocks):
    print(f"    {name:16s} l2={l2:10.3e}  max={mx:10.3e}")

from torch.func import jacrev
J0 = jacrev(resfn)(v0).detach()
sv0 = torch.linalg.svdvals(J0)
print(f"\nSEED JACOBIAN: shape=({J0.shape[0]},{J0.shape[1]})  cond={float(sv0[0]/sv0[-1]):.3e}"
      f"  s_max={float(sv0[0]):.3e}  s_min={float(sv0[-1]):.3e}")
csJ = J0.abs().amax(dim=0)
Js = J0 / csJ.clamp(min=1e-30)
svs = torch.linalg.svdvals(Js)
print(f"  column-scaled cond = {float(svs[0]/svs[-1]):.3e} (the LM working conditioning)")

# ---------- bounded LM run ----------
print(f"\nLM (QR trust steps, column-scaled; maxit={MAXIT}, wall<{BUDGET:.0f}s):")
hist = []
w, info = C.lm_qr(resfn, v0.detach().cpu().numpy().astype(np.longdouble), maxit=MAXIT,
                  time_budget=BUDGET, device=DEV, verbose=True)
vf = torch.as_tensor(w.astype(float), device=DEV)
Ff = resfn(vf)
print(f"\nPhi history: {['%.3e' % h for h in info['hist']]}")
print(f"final Phi = {info['Phi']:.6e}  iters = {info['iters']}  wall = {info['wall']:.1f}s")
print("  residual mass by ROW BLOCK at end (l2, max):")
for name, l2, mx in block_norms(Ff.detach().cpu().numpy(), row_blocks):
    print(f"    {name:16s} l2={l2:10.3e}  max={mx:10.3e}")

Jf = jacrev(resfn)(vf).detach()
svf = torch.linalg.svdvals(Jf)
print(f"\nFINAL JACOBIAN: cond={float(svf[0]/svf[-1]):.3e}  s_max={float(svf[0]):.3e}"
      f"  s_min={float(svf[-1]):.3e}")
# smallest singular directions: which unknown blocks do they live in?
U_, S_, Vh_ = torch.linalg.svd(Jf)
print("  softest 3 singular directions (unknown-block weights):")
for kk in range(1, 4):
    vec = Vh_[-kk].abs()
    i = 0; parts = []
    for name, k in unk_blocks:
        seg = vec[i:i + k]; i += k
        parts.append(f"{name}={float((seg*seg).sum()):.2f}")
    print(f"    s[{-kk}]={float(S_[-kk]):.3e}  " + "  ".join(parts))

# ---------- state movement + instruments (smoke-behavior report only) ----------
phi_c0, rho_c0, _, _, _, rp_0, rsU_0 = C.unpack_comp(v0, ctx)
phi_cf, rho_cf, uf_f, _, _, rp_f, rsU_f = C.unpack_comp(vf, ctx)
print(f"\nSTATE MOVEMENT (seed -> end):")
print(f"  r_p : {float(rp_0):.4f} -> {float(rp_f):.6f}    r_sU: {float(rsU_0):.4f} -> {float(rsU_f):.6f}")
print(f"  phi_core: {float(phi_c0[0]):+.4f} -> {float(phi_cf[0]):+.6f}   "
      f"rho_core: {float(rho_c0[0]):.4f} -> {float(rho_cf[0]):.6f}")
print(f"  max|u|: {float(torch.zeros(1).max()):.3f}(rigid)+bulge {AMP} -> {float(uf_f.abs().max()):.4f}")
g = C.gates_comp(vf, ctx, prm, br)
print("\nINSTRUMENTS at the end state (smoke behavior only; ~0 is owed ONLY on a true solution):")
for k in ["H_cell_max", "H_amb_max", "matched_derrick_gate", "E_ang_core", "E_ang_seal",
          "q_fold", "q_seal", "dphi_float", "dphi_anchor_gap", "rho_core", "rho_c_floor"]:
    print(f"    {k:22s} = {g[k]:+.6e}")
print(f"    sigma_amb max_rel      = {g['sigma_amb']['max_rel']:.3e}")
print(f"    sigma_cell max_rel     = {g['sigma_cell']['max_rel']:.3e}")

print(f"\nwall time total: {time.time()-t0:.1f}s")
print("SMOKE TEST COMPLETE -- conditioning report only; no cell claimed, no physics verdict.")

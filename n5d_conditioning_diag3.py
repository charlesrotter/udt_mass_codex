"""n5d_conditioning_diag3.py -- constructive confirmation of the category-A fix path.
(1) S-JC2: does Ruiz-equilibration + deflating the exact constant-a2 mode restore a workable cond?
(2) does the phi-constant near-null LIFT at a NON-trivial (non-homogeneous) phi/rho state?
    -> tests 'phi-null = degenerate/stalled-state artifact' vs 'converged soft mode'.
Category-A only; nothing in the physics residual changed.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from torch.func import jacrev

import cell_solver_f2d as cs
import n5d_pilot as pilot
import n5d_conditioning_diag as d1

PRM = pilot.PRM
Nth = 8


def ruiz(J, iters=40):
    A = J.clone()
    dr = torch.ones(J.shape[0], dtype=torch.float64); dc = torch.ones(J.shape[1], dtype=torch.float64)
    for _ in range(iters):
        rn = torch.linalg.norm(A, dim=1).clamp_min(1e-300)
        cn = torch.linalg.norm(A, dim=0).clamp_min(1e-300)
        A = A / rn.sqrt()[:, None] / cn.sqrt()[None, :]
        dr /= rn.sqrt(); dc /= cn.sqrt()
    return A, dr, dc


def cond_of(J):
    S = torch.linalg.svdvals(J).cpu().numpy()
    return S[0] / S[-1], S[-1], S[0]


print("=" * 90)
print("CONFIRM 1: S-JC2 final -- Ruiz alone vs Ruiz + deflate the exact constant-a2 gauge mode")
print("=" * 90)
st, source_rc, source_sh2 = pilot.load_frozen_source()
ctx, u_final, u_seed, n5d, n5d_seed, L0 = d1.reproduce_final_state("S-JC2", source_rc, source_sh2)
Nr = ctx["Nr"]
J = jacrev(lambda uu: cs.residual(uu, ctx, PRM, n5d=n5d))(u_final).detach()
c0, smin0, smax0 = cond_of(J)
print(f"  raw:                      cond={c0:.3e} smin={smin0:.3e}")
Jr, dr, dc = ruiz(J)
cr, sminr, smaxr = cond_of(Jr)
print(f"  Ruiz equilibrated:        cond={cr:.3e} smin={sminr:.3e}")

# deflate the constant-a2 column direction (numerical gauge fix of the unobservable offset):
# replace the a2-mean direction with a unit 'pin' row/col. Simplest: append a gauge row that fixes
# sum(a2)=0 and drop one redundant shear-interior row equivalent -> here we test by projecting the
# constant-a2 direction out of the column space (deflation) and re-conditioning.
a2sl = d1.block_slices(ctx)["a2"]
gauge = torch.zeros(J.shape[1], dtype=torch.float64)
gauge[a2sl] = 1.0 / np.sqrt(Nr)                       # unit constant-a2 direction in variable space
# projector removing that direction from the columns
P = torch.eye(J.shape[1], dtype=torch.float64) - torch.outer(gauge, gauge)
Jdef = J @ P
# add the gauge equation as an extra row (fix the offset) -> square-ish; use Ruiz then cond of stacked
Jstack = torch.cat([Jdef, gauge[None, :]], dim=0)
Js_r, _, _ = ruiz(Jstack)
cs_r, smin_sr, smax_sr = cond_of(Js_r)
print(f"  Ruiz + constant-a2 gauge-pinned (deflate+pin row): cond={cs_r:.3e} smin={smin_sr:.3e}")
print("  -> if this drops many orders, the S-JC2 blow-up IS the unpinned constant-a2 offset (fixable).")

print()
print("=" * 90)
print("CONFIRM 2: does the phi-constant near-null LIFT at a NON-homogeneous phi/rho state?")
print("=" * 90)
# take the pilot final state and inject a genuine non-constant phi & rho profile (structure), then
# recompute the smallest singular value / phi-mode. NOTE: this is a DIAGNOSTIC probe of the Jacobian
# at a different point in state space -- it does NOT change the equations or run a solve.
ctx2, u_f2, _, n5d2, _, _ = d1.reproduce_final_state("S-Dir", source_rc, source_sh2)
Nr = ctx2["Nr"]
zeta = ctx2["zeta"]
for amp_phi in (0.0, 0.05, 0.2, 0.5):
    u = u_f2.detach().clone()
    # non-constant, mirror-respecting (zero-slope ends) phi & rho bumps: cos(pi(zeta+1)/2) has f'=0 ends
    bump = torch.cos(np.pi * (zeta + 1.0) / 2.0)
    u[0:Nr] = u[0:Nr] + amp_phi * bump                 # phi profile
    u[Nr:2*Nr] = u[Nr:2*Nr] + 0.5 * amp_phi * bump     # rho profile
    J = jacrev(lambda uu: cs.residual(uu, ctx2, PRM, n5d=n5d2))(u).detach()
    U, S, Vh = torch.linalg.svd(J)
    Snp = S.cpu().numpy()
    # block frac of smallest mode
    v = Vh[-1].detach().cpu().numpy(); tot = np.linalg.norm(v)
    bphi = np.linalg.norm(v[0:Nr]) / tot
    ba2 = np.linalg.norm(v[d1.block_slices(ctx2)["a2"]]) / tot
    with torch.no_grad():
        rhop = cs.fields(u, ctx2, PRM, n5d=n5d2)["rhop"].abs().max().item()
    print(f"  phi/rho bump amp={amp_phi:.2f}: max|rho'|={rhop:.3e}  smin={Snp[-1]:.3e}  "
          f"cond={Snp[0]/Snp[-1]:.3e}  smallest-mode phi-frac={bphi:.3f} a2-frac={ba2:.3f}")
print("  -> smin RISING with structure => the phi-null was a stalled-homogeneous-state artifact,")
print("     not a converged physical soft mode (a genuine soft mode would persist).")

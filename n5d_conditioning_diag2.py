"""n5d_conditioning_diag2.py -- follow-up: is the phi near-null mode from the BASE solver or the
shear extension?  Is it a non-convergence artifact?  How does cond scale with Nr (Cheb N^4)?

Category-A only.  No equations/BCs/source/readouts changed.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from torch.func import jacrev

import cell_solver_f2d as cs
import n5d_pilot as pilot

PRM = pilot.PRM
Nth = 8


def blockslc(Nr, Nth):
    return dict(phi=slice(0, Nr), rho=slice(Nr, 2 * Nr),
               uf=slice(2 * Nr, 2 * Nr + Nr * Nth),
               a2=slice(2 * Nr + Nr * Nth, 2 * Nr + Nr * Nth + Nr),
               L=slice(2 * Nr + Nr * Nth + Nr, 2 * Nr + Nr * Nth + Nr + 1))


def svd_at(u, ctx, n5d):
    J = jacrev(lambda uu: cs.residual(uu, ctx, PRM, n5d=n5d))(u).detach()
    U, S, Vh = torch.linalg.svd(J)
    return J, U, S.cpu().numpy(), Vh


def block_frac(vec, Nr, Nth):
    v = vec.detach().cpu().numpy(); tot = np.linalg.norm(v) + 1e-300
    return {k: float(np.linalg.norm(v[s]) / tot) for k, s in blockslc(Nr, Nth).items()}


print("=" * 90)
print("PROBE 1: BASE (no-shear) system conditioning at the ROUND SEED across Nr  (n5d=None)")
print("=" * 90)
for Nr in (8, 12, 16, 24):
    ctx = cs.make_ctx(Nr, Nth, rc=0.5)
    u = cs.seed(ctx)                              # base seed, no a2
    J = jacrev(lambda uu: cs.residual(uu, ctx, PRM))(u).detach()
    S = torch.linalg.svdvals(J).cpu().numpy()
    U, Sv, Vh = torch.linalg.svd(J)
    vmin = Vh[-1]
    bf = block_frac(torch.cat([vmin, torch.zeros(Nr + 0)]) if False else
                    torch.cat([vmin[:2*Nr+Nr*Nth], torch.zeros(Nr), vmin[2*Nr+Nr*Nth:]]), Nr, Nth)
    # base has no a2 block; recompute block fractions on the base layout directly
    v = vmin.detach().cpu().numpy(); tot = np.linalg.norm(v)
    bphi = np.linalg.norm(v[0:Nr]) / tot
    brho = np.linalg.norm(v[Nr:2*Nr]) / tot
    buf = np.linalg.norm(v[2*Nr:2*Nr+Nr*Nth]) / tot
    bL = np.linalg.norm(v[-1]) / tot
    print(f"  Nr={Nr:2d}: cond={S[0]/S[-1]:.3e}  smax={S[0]:.3e}  smin={S[-1]:.3e}  "
          f"smin/(smax*eps)={S[-1]/(S[0]*np.finfo(float).eps):.2e}")
    print(f"         smallest-sv right-vector block-frac: phi={bphi:.3f} rho={brho:.3f} "
          f"uf={buf:.3f} L={bL:.3f}")

print()
print("=" * 90)
print("PROBE 2: base cond after Ruiz two-sided equilibration (isolates SCALING vs genuine rank)")
print("=" * 90)


def ruiz_cond(J, iters=30):
    A = J.clone()
    for _ in range(iters):
        rn = torch.linalg.norm(A, dim=1).clamp_min(1e-300)
        cn = torch.linalg.norm(A, dim=0).clamp_min(1e-300)
        A = A / rn.sqrt()[:, None] / cn.sqrt()[None, :]
    S = torch.linalg.svdvals(A).cpu().numpy()
    return S[0] / S[-1], S[-1]


for Nr in (8, 16):
    ctx = cs.make_ctx(Nr, Nth, rc=0.5)
    u = cs.seed(ctx)
    J = jacrev(lambda uu: cs.residual(uu, ctx, PRM))(u).detach()
    S = torch.linalg.svdvals(J).cpu().numpy()
    c_r, smin_r = ruiz_cond(J)
    print(f"  Nr={Nr:2d}: raw cond={S[0]/S[-1]:.3e}  ->  Ruiz-equilibrated cond={c_r:.3e}  (smin={smin_r:.2e})")

print()
print("=" * 90)
print("PROBE 3: is the phi near-null a NON-CONVERGENCE artifact? rho' magnitude in the pilot state")
print("=" * 90)
st, source_rc, source_sh2 = pilot.load_frozen_source()
import n5d_conditioning_diag as d1
for sealbc in ("S-Dir", "S-JC2"):
    ctx, u_final, u_seed, n5d, n5d_seed, L0 = d1.reproduce_final_state(sealbc, source_rc, source_sh2)
    with torch.no_grad():
        Q = cs.fields(u_final, ctx, PRM, n5d=n5d)
        rhop = Q["rhop"].cpu().numpy(); phip = Q["phip"].cpu().numpy()
        rho = Q["rho"].cpu().numpy(); phi = Q["phi"].cpu().numpy()
    # the phi near-null singular vector's PROFILE
    J, U, S, Vh = svd_at(u_final, ctx, n5d)
    # find the smallest-sv mode that is phi-dominated
    Nr = ctx["Nr"]
    for k in range(1, 5):
        v = Vh[-k].detach().cpu().numpy()
        bphi = np.linalg.norm(v[0:Nr]) / np.linalg.norm(v)
        if bphi > 0.9:
            phiv = v[0:Nr] / np.linalg.norm(v[0:Nr])
            zeta = ctx["zeta"].cpu().numpy()
            cst = np.ones(Nr)/np.sqrt(Nr); ramp = zeta-zeta.mean(); ramp/=np.linalg.norm(ramp)
            print(f"  [{sealbc}] phi-null mode = sv#{k} (sigma={S[-k]:.3e}): "
                  f"|overlap const|={abs(cst@phiv):.3f} |overlap linear|={abs(ramp@phiv):.3f}")
            break
    print(f"  [{sealbc}] non-converged state: max|rho'|={np.abs(rhop).max():.3e}  "
          f"max|phi'|={np.abs(phip).max():.3e}  rho range=[{rho.min():.4f},{rho.max():.4f}]  "
          f"phi range=[{phi.min():.3e},{phi.max():.3e}]")
    print(f"  [{sealbc}] -> if rho' and phi' are ~0 the phi-flatness is (partly) the un-relaxed seed, "
          f"not necessarily a converged soft mode")

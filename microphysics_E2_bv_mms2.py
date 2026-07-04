"""microphysics_E2_bv_mms2.py -- attack 1 follow-up: convergence-RADIUS ladder for the MMS
root. Questions: (a) can the LM polish the exact root to the 1e-8 contract floor AT ALL
(scale 1e-6)? (b) what perturbation scale still converges? (c) does the scale-1e-2 case
converge given 3000 iterations (was still falling at 400)? Bounded, single process, GPU.
"""
import os, math, time
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
import cell_solver_composite as C

DEV = "cuda" if torch.cuda.is_available() else "cpu"
LAB = "A1 m=3 Z=8"
br = C.load_bracket(LAB)
prm = (br["Z"], 0.5, 0.1, 1)
Nr, Nth, Na, KMAP = 12, 8, 192, 2.5
ctx = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device=DEV)

def genericize(v):
    phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(v, ctx)
    z = ctx["cell"]["zeta"].to(DEV); mu = ctx["cell"]["mu"].to(DEV); h = ctx["ha"].to(DEV)
    phi_c = phi_c + 0.05 * torch.cos(math.pi * z)
    rho_c = rho_c + 0.03 * torch.sin(0.5 * math.pi * (z + 1.0))
    uf = uf + 0.05 * (1.0 - mu[None, :] ** 2) * mu[None, :] * torch.cos(math.pi * (z[:, None] + 1.0))
    phi_a = phi_a + 0.02 * torch.sin(math.pi * h)
    rho_a = rho_a + 0.01 * h * (1.0 - h)
    return C.pack_comp(phi_c, rho_c, uf, phi_a, rho_a, float(r_p), float(r_sU), device=DEV)

def perturb(v, scale, dr):
    phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(v, ctx)
    z = ctx["cell"]["zeta"].to(DEV); mu = ctx["cell"]["mu"].to(DEV); h = ctx["ha"].to(DEV)
    phi_c = phi_c + scale * torch.sin(math.pi * (z + 1.0))
    rho_c = rho_c + scale * torch.cos(0.5 * math.pi * z)
    uf = uf + scale * (1.0 - mu[None, :] ** 2) * torch.sin(0.5 * math.pi * (z[:, None] + 1.0))
    phi_a = phi_a + scale * torch.sin(2 * math.pi * h) * 0.5
    rho_a = rho_a + scale * torch.cos(math.pi * h) * 0.5
    return C.pack_comp(phi_c, rho_c, uf, phi_a, rho_a, float(r_p) + dr, float(r_sU) + 1.1 * dr,
                       device=DEV)

v_star = genericize(C.seed_comp(ctx, br, rp0=0.95 * br["r_s"], amp=0.8, device=DEV))
F_star = C.residual_comp(v_star, ctx, prm, br).detach()
resfn = lambda vv: C.residual_comp(vv, ctx, prm, br) - F_star

print(f"root residual check: max|F(v*)| = {float(resfn(v_star).abs().max()):.3e} (exact 0 by construction)")

for scale, dr, maxit, budget in [(1e-6, 1e-4, 200, 200), (1e-4, 1e-2, 200, 200),
                                 (1e-3, 0.1, 400, 300), (3e-3, 0.5, 800, 300),
                                 (1e-2, 2.0, 3000, 600)]:
    v0 = perturb(v_star, scale, dr)
    F0 = resfn(v0).detach()
    t0 = time.time()
    w, info = C.lm_qr(resfn, v0.cpu().numpy(), maxit=maxit, device=DEV, time_budget=budget)
    wt = torch.as_tensor(np.asarray(w, dtype=float), device=DEV)
    maxF = float(resfn(wt).abs().max())
    dv = float((wt - v_star).abs().max())
    drp = float(wt[-2] - v_star[-2])
    tail = info["hist"][-5:]
    print(f"scale={scale:.0e} dr={dr:<6} seed maxF={float(F0.abs().max()):.1e} -> iters={info['iters']:4d} "
          f"({time.time()-t0:5.1f}s)  end maxF={maxF:.3e}  ||w-v*||={dv:.2e}  d r_p={drp:+.3f}  "
          f"{'CONV' if maxF<=1e-8 else 'no'}  Phi tail={['%.1e'%x for x in tail]}")
print("\nDONE (bv_mms2)")

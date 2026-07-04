"""BLIND VERIFIER re-run: (2) null is real, (3) stiffness/immediate-fold, (4) runaway control.
Independent driver calls; does NOT touch physics; not committed."""
import os, time, math
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
import cell_solver_composite as C
import e2d_continuation_driver as D
import e2e_physinformed_seed as S

LAB = "A1 m=3 Z=8"
DEV = D.DEV
Nr, Nth, Na, KMAP = 12, 8, 192, 2.5
CONV = 1e-8
br = C.load_bracket(LAB); RS = br["r_s"]
ctx = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device=DEV)

# ---- ATTACK 2 + 4: independently re-run 2 sweep cell x slice cases, my own driver call ----
# W1/plateau (rp0=100) and W6/plateau (the low-maxF case flagged in attack 2).
CASES = [("W1", "plateau", 1, 0.5, 0.1, 100.0),
         ("W6", "plateau", 2, 0.05, 1.0, 100.0)]
print("=== ATTACK 2/4: independent re-run of sweep cases (newton_homotopy) ===")
for cname, sname, N, xi, kap, rp0 in CASES:
    prm = (br["Z"], xi, kap, N)
    for sk, v0 in [("phys-blend", S.physinformed_seed(ctx, br, prm, rp0, amp=0.8, family="blend", device=DEV)),
                   ("flat", S.flat_seed(ctx, br, rp0, amp=0.8, device=DEV))]:
        resfn = lambda vv: C.residual_comp(vv, ctx, prm, br)
        v0n = v0.detach().cpu().numpy().astype(np.longdouble)
        t0 = time.time()
        w, info = D.newton_homotopy(resfn, v0n, v0.numel(), s_steps=10, maxit_final=200, budget=60.0)
        vf = torch.as_tensor(w.astype(float), device=DEV)
        maxF = float(resfn(vf).abs().max())
        status = "CONVERGED" if maxF <= CONV else "no"
        print(f"  {cname}/{sname} {sk:11s}: maxF={maxF:.3e} status={status} "
              f"s_reached={info.get('s_reached')} rp_end={float(w[-2]):.1f} ({time.time()-t0:.0f}s)")

# ---- ATTACK 3: stiffness -- W1/plateau MMS delta=0.1 phys seed carries large residual, folds early ----
print("\n=== ATTACK 3: stiffness (W1 plateau MMS delta=0.1) ===")
N, XI, KAP, frac, delta = 1, 0.5, 0.1, 0.5, 0.1
prm = (br["Z"], XI, KAP, N)
rp0 = frac * br["r_s"]
base = S.physinformed_seed(ctx, br, prm, rp0, amp=0.8, family="blend", device=DEV)
# replicate generic_bump (from certification script) to build v_star
phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(base, ctx)
z = ctx["cell"]["zeta"].to(DEV); mu = ctx["cell"]["mu"].to(DEV); h = ctx["ha"].to(DEV)
phi_c = phi_c + delta * torch.cos(math.pi * z)
rho_c = rho_c + 0.6 * delta * torch.sin(0.5 * math.pi * (z + 1.0))
uf = uf + delta * (1.0 - mu[None, :] ** 2) * mu[None, :] * torch.cos(math.pi * (z[:, None] + 1.0))
phi_a = phi_a + 0.3 * delta * torch.sin(math.pi * h)
rho_a = rho_a + 0.15 * delta * h * (1.0 - h)
v_star = C.pack_comp(phi_c, rho_c, uf, phi_a, rho_a, float(r_p), float(r_sU), device=DEV)
F_star = C.residual_comp(v_star, ctx, prm, br).detach()
resfn = lambda vv: C.residual_comp(vv, ctx, prm, br) - F_star
rootF = float(resfn(v_star).abs().max())
seed_dist = float(np.abs(base.cpu().numpy().astype(np.longdouble) - v_star.cpu().numpy().astype(np.longdouble)).max())
seedF = float(resfn(base).abs().max())
print(f"  root max|F(v*)|={rootF:.2e} (should be ~0)")
print(f"  phys seed_dist to v*={seed_dist:.3f} (should be ~0.1)  seedF={seedF:.3f} (claim ~17)")
# immediate fold: arclength homotopy s_max
t0 = time.time()
v0n = base.detach().cpu().numpy().astype(np.longdouble)
w, ainfo = D.arclength_homotopy(resfn, v0n, base.numel(), budget=45.0, maxsteps=120,
                                s_target=1.0, fold_abort=0.03, runaway_cap=1e5)
print(f"  arclen s_max={ainfo['s_max']:.3e} (claim ~9e-4 = immediate fold) ({time.time()-t0:.0f}s)")
print("DONE")

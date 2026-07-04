"""e2c_mms_certification.py -- the MMS gauntlet certifying cell_solver_composite.lm_hardened.

Method (same as the E2 blind verifier's decisive instrument, microphysics_E2_bv_mms.py): build a
manufactured composite state v* whose EXACT root is guaranteed by forcing-subtraction
(resfn(v) = residual(v) - residual(v*), same Jacobian/stiffness as the physical system), perturb
by seed-CLASS amounts, and ask whether the hardened optimizer re-finds max|F| <= 1e-8.

Two manufactured solutions (different bracket + a nonzero-bulge case) so the certification is not
a single lucky point.  Axes are reported SEPARATELY (cell fields / ambient fields / boundaries)
because the E2c diagnosis showed they have different intrinsic radii (the ambient dilaton is
intrinsically stiff: e^{-2phi} ~ 1e4-1e6 at depth).

Bounded: production grid (Nr<=12, Nth<=8, Na=192), capped iters, single process, GPU with CPU
spot-check on every declared convergence.  NOT committed as a result until blind-verified.  Data-blind
(synthetic problem, no observational numbers).
"""
import os, math, time
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
import cell_solver_composite as C

DEV = "cuda" if torch.cuda.is_available() else "cpu"
Nr, Nth, Na, KMAP = 12, 8, 192, 2.5


def build_mms(label, rp0_frac, amp, bulge=0.0):
    """Manufactured composite root v* (generic smooth state) + its forced residual resfn."""
    br = C.load_bracket(label); prm = (br["Z"], 0.5, 0.1, 1)
    ctx = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device=DEV)
    rp0 = rp0_frac * br["r_s"] if rp0_frac <= 1.0 else rp0_frac

    def genericize(v):
        phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(v, ctx)
        z = ctx["cell"]["zeta"].to(DEV); mu = ctx["cell"]["mu"].to(DEV); h = ctx["ha"].to(DEV)
        phi_c = phi_c + 0.05 * torch.cos(math.pi * z)
        rho_c = rho_c + 0.03 * torch.sin(0.5 * math.pi * (z + 1.0))
        uf = uf + 0.05 * (1.0 - mu[None, :] ** 2) * mu[None, :] * torch.cos(math.pi * (z[:, None] + 1.0))
        # nonzero-bulge case: a genuine theta-structured deformation (E1 P3: solutions are
        # non-perturbative in theta) so the certification includes a bulged root
        uf = uf + bulge * (1.0 - mu[None, :] ** 2) * torch.sin(math.pi * (z[:, None] + 1.0) / 2.0)
        phi_a = phi_a + 0.02 * torch.sin(math.pi * h)
        rho_a = rho_a + 0.01 * h * (1.0 - h)
        return C.pack_comp(phi_c, rho_c, uf, phi_a, rho_a, float(r_p), float(r_sU), device=DEV)

    v_star = genericize(C.seed_comp(ctx, br, rp0=rp0, amp=amp, device=DEV))
    F_star = C.residual_comp(v_star, ctx, prm, br).detach()
    resfn = lambda vv: C.residual_comp(vv, ctx, prm, br) - F_star
    return dict(br=br, prm=prm, ctx=ctx, v_star=v_star, resfn=resfn, F_star=F_star, n=v_star.numel())


def perturb(mm, cell_sc=0.0, amb_sc=0.0, dr=0.0, seed=1234):
    """Perturb v* by seed-class amounts, on chosen axes.  cell_sc -> phi_c,rho_c,u; amb_sc ->
    phi_a,rho_a; dr -> the two free boundaries (the soft translation axis)."""
    ctx = mm["ctx"]; v = mm["v_star"]
    phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(v, ctx)
    z = ctx["cell"]["zeta"].to(DEV); mu = ctx["cell"]["mu"].to(DEV); h = ctx["ha"].to(DEV)
    phi_c = phi_c + cell_sc * torch.sin(math.pi * (z + 1.0))
    rho_c = rho_c + cell_sc * torch.cos(0.5 * math.pi * z)
    uf = uf + cell_sc * (1.0 - mu[None, :] ** 2) * torch.sin(0.5 * math.pi * (z[:, None] + 1.0))
    phi_a = phi_a + amb_sc * torch.sin(2 * math.pi * h) * 0.5
    rho_a = rho_a + amb_sc * torch.cos(math.pi * h) * 0.5
    return C.pack_comp(phi_c, rho_c, uf, phi_a, rho_a, float(r_p) + dr, float(r_sU) + 1.1 * dr,
                       device=DEV)


def run(mm, name, cell_sc=0.0, amb_sc=0.0, dr=0.0, solver="hard", maxit=300, budget=200.0):
    n = mm["n"]; resfn = mm["resfn"]; v_star = mm["v_star"]
    v0 = perturb(mm, cell_sc, amb_sc, dr)
    F0 = float(resfn(v0).abs().max())
    dvn = float((v0 - v_star).abs().max())
    t0 = time.time()
    if solver == "hard":
        w, info = C.lm_hardened(resfn, v0.cpu().numpy(), maxit=maxit, time_budget=budget,
                                device=DEV, pos_idx=[n - 2, n - 1], order_idx=(n - 2, n - 1))
        maxF = info["maxF"]; iters = info["iters"]
    else:                                                # baseline (old column-scaled LM)
        w, info = C.lm_qr(resfn, v0.cpu().numpy(), maxit=maxit, device=DEV, time_budget=budget)
        wt = torch.as_tensor(np.asarray(w, dtype=float), device=DEV)
        maxF = float(resfn(wt).abs().max()); iters = info["iters"]
    # CPU spot-check of the declared residual (independent of the GPU path)
    wt = torch.as_tensor(np.asarray(w, dtype=float), device="cpu")
    ctx_c = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device="cpu")
    Fc = C.residual_comp(wt, ctx_c, mm["prm"], mm["br"]) - mm["F_star"].cpu()
    maxF_cpu = float(Fc.abs().max())
    ok = maxF <= 1e-8 and maxF_cpu <= 1e-7
    print(f"  [{solver}] {name:26s} cell={cell_sc:<4} amb={amb_sc:<4} dr={dr:<5} "
          f"||v0-v*||={dvn:6.2f} seedF={F0:.1e} -> it={iters:3d} ({time.time()-t0:5.1f}s) "
          f"maxF={maxF:.2e} cpu={maxF_cpu:.1e} {'CONV' if ok else 'no'}")
    return ok, maxF


if __name__ == "__main__":
    print(f"E2c MMS CERTIFICATION  grid Nr{Nr}/Nth{Nth}/Na{Na} kmap={KMAP} device={DEV}\n")
    # --- Manufactured solution #1: A1 Z=8, wall slice (the representative sweep cell) ---
    mm1 = build_mms("A1 m=3 Z=8", 0.95, 0.8)
    print(f"MMS#1 A1Z8 wall-slice  n={mm1['n']}  root max|F(v*)|={float(mm1['resfn'](mm1['v_star']).abs().max()):.2e}")

    print("\n== BASELINE (old column-scaled LM, lm_qr) -- reproduce the ~1e-3 radius ==")
    run(mm1, "boundary dr=10", dr=10.0, solver="qr", maxit=300)
    run(mm1, "cell 0.3", cell_sc=0.3, solver="qr", maxit=300)

    print("\n== HARDENED (lm_hardened) -- BOUNDARY / soft-translation axis (the documented failure) ==")
    for dr in [1.0, 5.0, 10.0, 20.0, 30.0]:
        run(mm1, f"boundary dr={dr}", dr=dr)
    print("\n== HARDENED -- CELL/carrier field axis (the DOFs a real sweep varies) ==")
    for sc in [0.1, 0.2, 0.3, 0.5]:
        run(mm1, f"cell {sc}", cell_sc=sc)
    print("\n== HARDENED -- AMBIENT field axis (intrinsically stiff: e^-2phi ~ 1e4 at depth) ==")
    for sc in [0.02, 0.05, 0.1]:
        run(mm1, f"ambient {sc}", amb_sc=sc)
    print("\n== HARDENED -- COMBINED cell+boundary (seed-class) ==")
    for sc, dr in [(0.1, 5.0), (0.2, 10.0), (0.3, 10.0)]:
        run(mm1, f"cell {sc}+dr {dr}", cell_sc=sc, dr=dr)

    # --- Manufactured solution #2: different bracket (A3 Z=1) + nonzero bulge ---
    print("\n" + "=" * 70)
    mm2 = build_mms("A3 Z=1", 100.0, 0.8, bulge=0.4)
    print(f"MMS#2 A3Z1 plateau-slice +bulge  n={mm2['n']}  "
          f"root max|F(v*)|={float(mm2['resfn'](mm2['v_star']).abs().max()):.2e}")
    print("== HARDENED -- second manufactured solution (bulged) ==")
    for dr in [5.0, 10.0, 20.0]:
        run(mm2, f"boundary dr={dr}", dr=dr)
    for sc in [0.1, 0.2, 0.3]:
        run(mm2, f"cell {sc}", cell_sc=sc)
    for sc, dr in [(0.2, 10.0), (0.3, 10.0)]:
        run(mm2, f"cell {sc}+dr {dr}", cell_sc=sc, dr=dr)
    print("\nDONE certification")

"""microphysics_E2_bv_mms.py -- BLIND VERIFIER attack 1 (decisive): METHOD OF MANUFACTURED
SOLUTIONS on the FULL monolithic composite at the production grid (Nr=12, Nth=8, Na=192,
kmap=2.5, n=506). No full composite solve has ever converged (0/256 phase-1); this tests whether
the LM/discretization CAN converge at all on this architecture when a solution provably exists.

Method: pick a generic smooth composite state v* (seed_comp + smooth genericizers, wall AND
plateau slices -- same stiffness class as the sweeps); compute F* = residual(v*); solve the
forced system F(v) - F* = 0 (v* is an exact root, same Jacobian as the physical system along
the path) from perturbed seeds. PASS = max|F| <= 1e-8 re-found and state == v*.

Bounded: maxit 400, wall 420 s per case, single process, GPU w/ CPU spot-check. NOT committed.
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
prm = (br["Z"], 0.5, 0.1, 1)          # W1 window cell -- the representative sweep cell
Nr, Nth, Na, KMAP = 12, 8, 192, 2.5
ctx = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device=DEV)
print(f"MMS attack: bracket={LAB} prm={prm} grid Nr{Nr}/Nth{Nth}/Na{Na} kmap={KMAP} device={DEV}")

def genericize(v):
    """Add smooth low-order structure so v* is generic (no accidental symmetry)."""
    phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(v, ctx)
    z = ctx["cell"]["zeta"].to(DEV); mu = ctx["cell"]["mu"].to(DEV); h = ctx["ha"].to(DEV)
    phi_c = phi_c + 0.05 * torch.cos(math.pi * z)
    rho_c = rho_c + 0.03 * torch.sin(0.5 * math.pi * (z + 1.0))
    uf = uf + 0.05 * (1.0 - mu[None, :] ** 2) * mu[None, :] * torch.cos(math.pi * (z[:, None] + 1.0))
    phi_a = phi_a + 0.02 * torch.sin(math.pi * h)
    rho_a = rho_a + 0.01 * h * (1.0 - h)
    return C.pack_comp(phi_c, rho_c, uf, phi_a, rho_a, float(r_p), float(r_sU), device=DEV)

def perturb(v, scale, dr):
    g = torch.Generator(device="cpu").manual_seed(1234)
    phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(v, ctx)
    z = ctx["cell"]["zeta"].to(DEV); mu = ctx["cell"]["mu"].to(DEV); h = ctx["ha"].to(DEV)
    # smooth low-order perturbations (representative of seed error, not white noise)
    phi_c = phi_c + scale * torch.sin(math.pi * (z + 1.0))
    rho_c = rho_c + scale * torch.cos(0.5 * math.pi * z)
    uf = uf + scale * (1.0 - mu[None, :] ** 2) * torch.sin(0.5 * math.pi * (z[:, None] + 1.0))
    phi_a = phi_a + scale * torch.sin(2 * math.pi * h) * 0.5
    rho_a = rho_a + scale * torch.cos(math.pi * h) * 0.5
    return C.pack_comp(phi_c, rho_c, uf, phi_a, rho_a, float(r_p) + dr, float(r_sU) + 1.1 * dr,
                       device=DEV)

def run_case(name, rp0, amp, scale, dr, maxit=400, budget=420.0):
    v_star = genericize(C.seed_comp(ctx, br, rp0=rp0, amp=amp, device=DEV))
    F_star = C.residual_comp(v_star, ctx, prm, br).detach()
    resfn = lambda vv: C.residual_comp(vv, ctx, prm, br) - F_star
    v0 = perturb(v_star, scale, dr)
    F0 = resfn(v0).detach()
    print(f"\n--- {name}: rp0={rp0} amp={amp} | perturbation scale={scale} dr_p={dr} ---")
    print(f"  seed maxF={float(F0.abs().max()):.3e}  Phi0={float((F0*F0).sum()):.3e}"
          f"  ||v0-v*||_inf={float((v0-v_star).abs().max()):.3e}")
    t0 = time.time()
    w, info = C.lm_qr(resfn, v0.cpu().numpy(), maxit=maxit, device=DEV, time_budget=budget)
    wt = torch.as_tensor(np.asarray(w, dtype=float), device=DEV)
    Ff = resfn(wt).detach()
    maxF = float(Ff.abs().max())
    dv = float((wt - v_star).abs().max())
    # CPU spot-check of the final residual
    ctx_c = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device="cpu")
    Fc = C.residual_comp(wt.cpu(), ctx_c, prm, br) - F_star.cpu()
    print(f"  END: iters={info['iters']} wall={time.time()-t0:.1f}s  Phi={info['Phi']:.3e}"
          f"  max|F|={maxF:.3e}  ||w-v*||_inf={dv:.3e}")
    print(f"  CPU spot-check max|F|={float(Fc.abs().max()):.3e}"
          f"  r_p: {float(wt[-2]):.6f} vs {float(v_star[-2]):.6f}"
          f"  r_sU: {float(wt[-1]):.6f} vs {float(v_star[-1]):.6f}")
    verdict = "CONVERGED (<=1e-8)" if maxF <= 1e-8 else "DID NOT CONVERGE"
    print(f"  VERDICT: {verdict}")
    return maxF, dv

# Case A: wall slice (the stiff outer-seal-wall ambient), moderate perturbation
run_case("A wall/moderate", rp0=0.95 * br["r_s"], amp=0.8, scale=1e-2, dr=2.0)
# Case B: plateau slice, moderate perturbation
run_case("B plateau/moderate", rp0=100.0, amp=0.8, scale=1e-2, dr=2.0)
# Case C: wall slice, LARGE perturbation (seed-distance class)
run_case("C wall/large", rp0=0.95 * br["r_s"], amp=0.8, scale=1e-1, dr=10.0)
print("\nDONE (bv_mms)")

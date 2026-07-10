"""VERIFIER-2 TASK 2b: PUSH the sustained-I_r candidates (open seal, random-kick seeds, L~20,
I_r~3.7e-2, Phi~7e-4).  Is Phi~7e-4 a genuine STALL (non-solution numerical floor) whose I_r
drains when pushed, or a slow approach to a REAL converged sustained-I_r cell?
Method: continuation restarts (warm-start from endpoint), watch Phi + I_r trajectory, vary lam0.
"""
import torch, math, numpy as np
import cell_solver_f2d as M
torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
Z, XI, KAP, N = 8.0, 1.0, 1.0, 1
prm = (Z, XI, KAP, N)
SEAL = dict(phi="mirror", matter="open")

def kick_seed(ctx, amp, rng, gen):
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    zeta = ctx["zeta"]; mu = ctx["mu"]
    gr = torch.cos(np.pi * (zeta + 1.0) / 2.0)
    s2 = (1.0 - mu ** 2)
    uf = amp * s2[None, :] * gr[:, None]
    uf = uf + rng * torch.randn(Nr, Nth, dtype=torch.float64, device=zeta.device, generator=gen) * s2[None, :]
    phi = torch.zeros(Nr, dtype=torch.float64, device=zeta.device)
    rho = torch.full((Nr,), 0.7071, dtype=torch.float64, device=zeta.device)
    return M.pack(phi, rho, uf, 1.0)

Nr, Nth = 16, 8
ctx = M.make_ctx(Nr, Nth, rc=0.5, device=DEV)

for (amp, rng, sd) in [(0.3, 0.05, 1234), (0.4, 0.1, 1234), (0.3, 0.1, 7), (0.5, 0.2, 42)]:
    gen = torch.Generator(device=DEV); gen.manual_seed(sd)
    u = kick_seed(ctx, amp, rng, gen)
    Ir0 = float(M.fields(u, ctx, prm)["Ir"].mean())
    print(f"\n### seed amp={amp} rng={rng} sd={sd}  I_r0={Ir0:.3e}")
    # continuation: 6 warm restarts of maxit=250, alternating lam0 to escape stalls
    for r in range(6):
        lam0 = 1e-3 if r % 2 == 0 else 1e-6
        u, hist = M.newton_lm_solve(u, ctx, prm, maxit=250, verbose=False,
                                     time_budget=70.0, seal=SEAL, lam0=lam0)
        Q = M.fields(u, ctx, prm)
        Ir = Q["Ir"]; L = float(Q["L"]); Phi = hist[-1]
        # residual row-block breakdown to see WHAT is stalling
        F = M.residual(u, ctx, prm, seal=SEAL)
        nphi = Nr - 2
        rphi = F[:nphi]; rest = F[nphi:]
        print(f"  restart{r} lam0={lam0:.0e} it={len(hist)-1:3d} Phi={Phi:.3e} "
              f"Ir_mean={float(Ir.mean()):.3e} Ir_max={float(Ir.max()):.3e} L={L:9.3f} "
              f"max|F_phi|={float(rphi.abs().max()):.2e} max|F_rest|={float(rest.abs().max()):.2e} "
              f"conv={Phi<1e-4}")
    print(f"  FINAL: converged={Phi<1e-4}  sustained_I_r(>1e-3)={float(Ir.mean())>1e-3}")

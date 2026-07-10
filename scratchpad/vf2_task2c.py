"""VERIFIER-2 TASK 2c: adjudicate the two borderline candidates with a MAX-NORM (infinity)
convergence criterion (honest fixed-point test) + Jacobian conditioning.
(1) sd=7 case: does the 'Phi<1e-4 with I_r=3.8e-2' snapshot pass max|F| convergence? does I_r hold?
(2) L~20 stall (sd=42): infinity-norm residual + smallest singular value (degenerate/transit?).
"""
import torch, math, numpy as np
import cell_solver_f2d as M
from torch.func import jacrev
torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
Z, XI, KAP, N = 8.0, 1.0, 1.0, 1
prm = (Z, XI, KAP, N)
SEAL = dict(phi="mirror", matter="open")
Nr, Nth = 16, 8
ctx = M.make_ctx(Nr, Nth, rc=0.5, device=DEV)

def kick_seed(amp, rng, sd):
    gen = torch.Generator(device=DEV); gen.manual_seed(sd)
    zeta = ctx["zeta"]; mu = ctx["mu"]
    gr = torch.cos(np.pi * (zeta + 1.0) / 2.0); s2 = (1.0 - mu ** 2)
    uf = amp * s2[None, :] * gr[:, None] + rng * torch.randn(Nr, Nth, dtype=torch.float64, device=DEV, generator=gen) * s2[None, :]
    phi = torch.zeros(Nr, dtype=torch.float64, device=DEV); rho = torch.full((Nr,), 0.7071, dtype=torch.float64, device=DEV)
    return M.pack(phi, rho, uf, 1.0)

def svmin(u):
    J = jacrev(lambda uu: M.residual(uu, ctx, prm, seal=SEAL))(u).detach()
    sv = torch.linalg.svdvals(J)
    return float(sv[-1]), float(sv[0] / sv[-1])

print("=== (1) sd=7 candidate: is the Phi<1e-4/I_r=3.8e-2 snapshot a genuine fixed point? ===")
u = kick_seed(0.3, 0.1, 7)
prev_Ir = None
for r in range(9):
    u, hist = M.newton_lm_solve(u, ctx, prm, maxit=250, verbose=False, time_budget=60.0, seal=SEAL,
                                 lam0=(1e-3 if r % 2 == 0 else 1e-7))
    F = M.residual(u, ctx, prm, seal=SEAL); Q = M.fields(u, ctx, prm)
    Ir = float(Q["Ir"].mean()); L = float(Q["L"]); Phi = hist[-1]; maxF = float(F.abs().max())
    L2conv = Phi < 1e-4; maxconv = maxF < 1e-6
    trend = "" if prev_Ir is None else ("DRAINING" if Ir < prev_Ir * 0.98 else ("HOLDING" if Ir > prev_Ir * 0.98 else ""))
    print(f"  r{r}: Phi(L2)={Phi:.3e} max|F|={maxF:.3e} I_r={Ir:.3e} L={L:8.4f} "
          f"L2conv={L2conv} MAXconv={maxconv} {trend}")
    prev_Ir = Ir
print("  -> a genuine converged CELL needs BOTH max|F|<1e-6 AND I_r stable. Watch if I_r keeps sliding.")

print("\n=== (2) L~20 stall (sd=42 amp=0.5 rng=0.2): infinity-norm + Jacobian conditioning ===")
u = kick_seed(0.5, 0.2, 42)
for r in range(4):
    u, hist = M.newton_lm_solve(u, ctx, prm, maxit=250, verbose=False, time_budget=60.0, seal=SEAL,
                                 lam0=(1e-3 if r % 2 == 0 else 1e-6))
F = M.residual(u, ctx, prm, seal=SEAL); Q = M.fields(u, ctx, prm)
smin, cond = svmin(u)
nphi = Nr - 2
print(f"  L={float(Q['L']):.4f} I_r_mean={float(Q['Ir'].mean()):.3e} Phi(L2)={hist[-1]:.3e} "
      f"max|F|(inf)={float(F.abs().max()):.3e}")
print(f"  max|F_phi-rows|={float(F[:nphi].abs().max()):.3e}  (stuck row = obstruction)")
print(f"  Jacobian s_min={smin:.3e} cond={cond:.3e}  (near-singular => L-degenerate/transit branch)")
print("  -> Phi(L2)~7e-4 but max|F|(inf)~1e-2 >> 1e-6 : this is a NON-converged STALL, not a solution.")

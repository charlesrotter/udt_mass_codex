"""Q3e: characterize the two wall-reaching outcomes.
 (1) ramp seed -> does L run away UNBOUNDEDLY (L-degeneracy) or converge to a finite large L?
     Track L across iteration by re-solving with increasing maxit.
 (2) flat seed (bounded L) -> push maxit high: does it CONVERGE to machine-zero at the wall with
     bounded L, or stall / drift to the runaway?
 (3) verify the runaway branch is scale-degenerate: is L a near-null direction of the Jacobian?
"""
import math, torch, numpy as np, cell_solver_f2d as M
torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
Nr, Nth = 16, 8
prm = (8.0, 1.0, 1.0, 1)
A = 0.3; phi_wall = -0.5*math.log(A)
seal = dict(phi="wall", phi_wall=phi_wall, matter="mirror")

def seed_ramp(ctx, L0, flat=False):
    zeta = ctx["zeta"]; mu = ctx["mu"]; Nr_=ctx["Nr"]
    x = (zeta+1.0)/2.0
    phi = torch.full((Nr_,), float(phi_wall), device=zeta.device) if flat else (phi_wall*x)
    gr = torch.cos(np.pi*(zeta+1.0)/2.0)
    uf = 0.02*(1.0-mu[None,:]**2)*gr[:,None]
    rho = torch.full((Nr_,), 0.7071, device=zeta.device)
    return M.pack(phi.to(torch.float64).to(zeta.device), rho, uf, float(L0))

print("=== (1) ramp seed: L vs maxit (runaway vs finite) ===")
for mit in [20, 50, 100, 200, 250]:
    ctx = M.make_ctx(Nr, Nth, rc=0.5, device=DEV)
    u1, hist = M.newton_lm_solve(seed_ramp(ctx, 0.05), ctx, prm, maxit=mit, verbose=False,
                                 time_budget=120.0, seal=seal)
    Q = M.fields(u1, ctx, prm)
    print(f"maxit={mit:3d} Phi={hist[-1]:.3e} L={float(Q['L']):.4e} phi_s={float(Q['phi'][-1]):.4f} "
          f"phi_c={float(Q['phi'][0]):+.3f} Ir={float(Q['Ir'].mean()):.2e}")

print("\n=== (2) flat seed (bounded L): push maxit; converge bounded or drift to runaway? ===")
for mit in [50, 120, 250]:
    ctx = M.make_ctx(Nr, Nth, rc=0.5, device=DEV)
    u1, hist = M.newton_lm_solve(seed_ramp(ctx, 0.05, flat=True), ctx, prm, maxit=mit, verbose=False,
                                 time_budget=120.0, seal=seal)
    Q = M.fields(u1, ctx, prm)
    F = M.residual(u1, ctx, prm, seal=seal); Phi=float((F*F).sum())
    wall = float(Q['phi'][-1])-phi_wall
    print(f"maxit={mit:3d} Phi={Phi:.3e} wallrow^2={wall**2:.3e} (frac {wall**2/Phi:.2f}) "
          f"L={float(Q['L']):.4e} phi_s={float(Q['phi'][-1]):.4f} Ir={float(Q['Ir'].mean()):.2e} "
          f"Fmax@{int(F.abs().argmax())}")

print("\n=== (3) runaway root: smallest singular values of Jacobian (L-degeneracy?) ===")
ctx = M.make_ctx(Nr, Nth, rc=0.5, device=DEV)
u1, _ = M.newton_lm_solve(seed_ramp(ctx, 0.05), ctx, prm, maxit=200, verbose=False,
                          time_budget=120.0, seal=seal)
from torch.func import jacrev
J = jacrev(lambda uu: M.residual(uu, ctx, prm, seal=seal))(u1).detach()
sv = torch.linalg.svdvals(J)
print(f"J shape={tuple(J.shape)} s_max={float(sv[0]):.3e} s_min={float(sv[-1]):.3e} "
      f"cond={float(sv[0]/sv[-1]):.3e}")
print(f"smallest 4 singular values: {[f'{float(s):.3e}' for s in sv[-4:]]}")
# which variable does the null-ish direction load on? (last right-singular vector)
U,S,Vh = torch.linalg.svd(J)
nullvec = Vh[-1].abs()
Nr_=ctx['Nr']
print(f"null right-vec mass: phi={float(nullvec[:Nr_].sum()):.3f} rho={float(nullvec[Nr_:2*Nr_].sum()):.3f} "
      f"uf={float(nullvec[2*Nr_:2*Nr_+Nr_*Nth].sum()):.3f} L={float(nullvec[-1]):.3f}")

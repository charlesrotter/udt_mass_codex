"""Q3d: decisive structural test. SEED phi AT/ABOVE the wall depth (phi(r_s)=phi_wall already
satisfied). If the solver KEEPS phi_s at wall depth with Phi->small, the earlier stalls were
NUMERIC (obstruction FALSE). If phi_s COLLAPSES back toward 0 and the wall row blows up, the
obstruction is STRUCTURAL (field cannot self-consistently hold the wall depth)."""
import math, torch, numpy as np, cell_solver_f2d as M
torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
Nr, Nth = 16, 8
prm = (8.0, 1.0, 1.0, 1)
A = 0.3
phi_wall = -0.5*math.log(A)   # 0.6020

def seal(matter): return dict(phi="wall", phi_wall=phi_wall, matter=matter)

def seed_at_wall(ctx, ramp=True, rho0=0.7071, L0=0.05):
    """seed with phi a smooth ramp from 0 at core to phi_wall at seal (satisfies the Dirichlet)."""
    Nr_, Nth_ = ctx["Nr"], ctx["Nth"]
    zeta = ctx["zeta"]; mu = ctx["mu"]
    x = (zeta + 1.0)/2.0                    # 0..1 core->seal
    if ramp:
        phi = phi_wall * x                  # 0 at core, phi_wall at seal
    else:
        phi = torch.full((Nr_,), float(phi_wall))
    gr = torch.cos(np.pi*(zeta+1.0)/2.0)
    uf = 0.02*(1.0-mu[None,:]**2)*gr[:,None]
    rho = torch.full((Nr_,), float(rho0), device=zeta.device)
    return M.pack(phi.to(torch.float64).to(zeta.device), rho, uf, float(L0))

for matter in ["mirror", "open"]:
    for ramp in [True, False]:
        for L0 in [0.05, 0.5, 1.0]:
            ctx = M.make_ctx(Nr, Nth, rc=0.5, device=DEV)
            u0 = seed_at_wall(ctx, ramp=ramp, L0=L0)
            # confirm seed satisfies the wall row:
            phis0 = float(M.fields(u0, ctx, prm)["phi"][-1])
            u1, hist = M.newton_lm_solve(u0, ctx, prm, maxit=200, verbose=False,
                                         time_budget=120.0, seal=seal(matter))
            Q = M.fields(u1, ctx, prm)
            phis = float(Q["phi"][-1]); phic = float(Q["phi"][0])
            wallrow = phis - phi_wall
            print(f"matter={matter:6s} ramp={ramp!s:5s} L0={L0:.2f} | seed phi_s={phis0:+.3f} "
                  f"-> final phi_s={phis:+.4f}(wall {phi_wall:.4f}) phi_c={phic:+.4f} "
                  f"wallrow={wallrow:+.3e} Phi={hist[-1]:.3e} Ir={float(Q['Ir'].mean()):.2e} "
                  f"L={float(Q['L']):.4f}")

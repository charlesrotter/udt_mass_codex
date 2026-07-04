"""microphysics_E2_bv_rs_soft.py -- BLIND VERIFIER attack 2: the E2a r_s soft-direction reading.
Claims under attack: (i) the pure-universe recovery's weak digit is r_s (~5 digits) because of a
PLATEAU-SLIDE soft direction; (ii) a*, q, rho_s are well-conditioned invariants; (iii) nothing
physics-level hides in the softness (it is the exponentially-flat plateau translating the fold,
not a second branch).
Method: solve the pure-universe system on one bracket (the E2a path), then OWN analysis:
  (1) SVD of the Jacobian at the solution: softest right-singular directions -- component
      weights on r_sU vs a vs the profile; where in r the profile component lives.
  (2) finite-move test: v + t*(soft dir) vs v + t*(random dir of equal norm): residual growth.
  (3) invariant conditioning: |dF| response to unit rel changes of a vs r_sU.
Bounded (one bracket + one Na cross-check), single process. NOT committed.
"""
import os, math
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from torch.func import jacrev
import cell_solver_composite as C

LAB = "A1 m=3 Z=8"
for Na in (192, 288):
    out = C.solve_pure_universe(LAB, Na=Na, maxit=140, device="cpu", time_budget=280.0)
    print(f"\nNa={Na}: Phi={out['Phi']:.3e} iters={out['iters']} "
          f"a_rel_err={out['a_rel_err']:+.2e} dr_s={out['dr_s']:+.3e} "
          f"({out['dr_s']/out['r_s_banked']:+.1e} rel) dq_rel={out['dq']/out['q_banked']:+.1e} "
          f"drho_s_rel={out['drho_s']/out['rho_s_banked']:+.1e} rho_c={out['rho_c']:.10f} "
          f"H_drift={out['H_drift']:.1e}")
    if Na == 288:
        w = out["w"]; ctx = out["ctx"]; br = out["bracket"]
        res_t = lambda ww: C.residual_pure(ww, ctx, br, torch)
        wt = torch.as_tensor(w.astype(float))
        J = jacrev(res_t)(wt).detach()
        U_, S_, Vh = torch.linalg.svd(J)
        print(f"  cond(J) = {float(S_[0]/S_[-1]):.3e}  s_min={float(S_[-1]):.3e} s_max={float(S_[0]):.3e}")
        # block weights of the softest 3 right-singular vectors
        idx_rsU, idx_a = 2*Na, 2*Na + 1
        r_phys = float(w[idx_rsU]) * np.asarray(ctx["ha_ld"], dtype=float)
        for k in range(1, 4):
            v = Vh[-k, :]
            wphi = float((v[:Na]**2).sum()); wrho = float((v[Na:2*Na]**2).sum())
            print(f"  soft dir #{k}: s={float(S_[-k]):.3e}  weights: phi={wphi:.3f} rho={wrho:.3f} "
                  f"r_sU={float(v[idx_rsU])**2:.3f} a={float(v[idx_a])**2:.3f}")
            prof = (v[:Na]**2 + v[Na:2*Na]**2).cpu().numpy()
            # where does the profile weight live? (plateau = small r/r_s, wall = r ~ r_s)
            half = prof[r_phys < 0.5*float(w[idx_rsU])].sum()
            wall = prof[r_phys > 0.95*float(w[idx_rsU])].sum()
            print(f"     profile weight: r<0.5 r_s: {half:.3f}   r>0.95 r_s: {wall:.3f}")
        # finite-move test along softest dir vs random dir
        v1 = Vh[-1, :]
        g = torch.Generator().manual_seed(7)
        rnd = torch.randn(v1.shape, generator=g); rnd /= rnd.norm()
        F0 = res_t(wt).detach()
        for t in (1e-4, 1e-2):
            Fs = res_t(wt + t*v1).detach(); Fr = res_t(wt + t*rnd).detach()
            print(f"  finite move t={t:.0e}: ||dF|| soft={float((Fs-F0).norm()):.3e} "
                  f"random={float((Fr-F0).norm()):.3e}  (soft dir moves r_sU by {t*float(v1[idx_rsU]):+.2e})")
        # invariant conditioning: unit-RELATIVE parameter kicks
        for name, idx in (("a", idx_a), ("r_sU", idx_rsU)):
            e = torch.zeros_like(wt); e[idx] = float(w[idx]) * 1e-6   # 1e-6 relative kick
            dF = (res_t(wt + e) - F0).norm()
            print(f"  1e-6 REL kick on {name}: ||dF|| = {float(dF):.3e}")
print("\nDONE (bv_rs_soft)")

"""cell_solver_f2d_embedded_scan.py -- test #1: does the EMBEDDED closure H(seal)=H_amb admit an
isolated finite cell? (embedded_cell_closure_H_amb_results.md, BLIND-VERIFIED). Two instruments:

  MODE A  free-L square system, closure row H(seal)-H_amb=0, L a Newton unknown. Scan fixed H_amb.
          -> tests whether Newton converges to a FINITE L (vs collapse L->0 / runaway L->inf).
  MODE B  FIXED-L scan (well-conditioned: converges to 1e-13 at every L, unlike free-L). Record the
          clean H(seal)(L) curve. Embedded cells = where H(seal)(L)=H_amb; MULTIPLE crossings
          (non-monotone H(seal)(L)) => discrete family; constant/monotone => continuum / single.

FINDING (2026-07-01, scoped/provisional -- see embedded_cell_scan_results.md): NO clean isolated
finite cell at N=1,2,3. Where the solver converges cleanly it shows CONTINUUM/scale-free behaviour
(N=3 large-L: H_seal~+4.18 constant, I_r->0); across much of the space (N=2 all L, N=3 small L, all
free-L) the solver STALLS (Phi~1e-2, cond~5e9 Chebyshev-endpoint) -> SOLVER-LIMITED, not a verdict.
Solver-first: install the galerkin BC-recombined basis + continuation before banking any negative.

Reuses the DERIVED+CAS-verified operators in cell_solver_f2d.py. Bounded per anti-hang. UNLABELED.
"""
import sys, time, math
import numpy as np, torch
from cell_solver_f2d import make_ctx, seed, fields, H_of_r, derrick, unpack, pack


def _lm(fn, w0, maxit, budget, tol=1e-13):
    from torch.func import jacrev
    t0 = time.time(); w = w0.clone()
    F = fn(w); Phi = float((F * F).sum()); lam = 1e-3; nu = 2.0
    for _ in range(maxit):
        if Phi < tol or time.time() - t0 > budget:
            break
        J = jacrev(fn)(w).detach(); F = fn(w).detach()
        Hm = J.T @ J; g = J.T @ (-F); dH = torch.diag(Hm)
        for _try in range(30):
            try:
                dx = torch.linalg.solve(Hm + lam * torch.diag(dH), g)
            except Exception:
                lam = min(lam * nu, 1e12); nu *= 2; continue
            wn = w + dx
            try:
                Fn = fn(wn); Pn = float((Fn * Fn).sum())
            except Exception:
                Pn = float("inf")
            pred = float((dx * (lam * dH * dx + g)).sum())
            gr = (Phi - Pn) / pred if (pred > 0 and math.isfinite(Pn)) else -1.0
            if gr > 0:
                w = wn; Phi = Pn
                lam = max(lam * max(1 / 3, 1 - (2 * gr - 1) ** 3), 1e-14); nu = 2.0; break
            lam = min(lam * nu, 1e12); nu *= 2
        else:
            break
    return w.detach(), Phi


def mode_A(ctx, prm, Hambs, amp=0.1, maxit=120, budget=25.0):
    """Free-L embedded solve; scan fixed H_amb. Reports L_final (finite/collapse/runaway)."""
    def resid(v, Hamb):
        Q = fields(v, ctx, prm)
        rows = [Q["phi_ode"][1:-1], Q["phip"][[0, -1]], Q["rho_ode"][1:-1], Q["rhop"][[0, -1]],
                Q["res_f"][1:-1].reshape(-1), Q["fr"][0, :], Q["fr"][-1, :]]
        rows.append((H_of_r(v, ctx, prm)[-1] - Hamb).reshape(1))
        return torch.cat([r.reshape(-1) for r in rows])
    print(f"--- MODE A (free-L) N={prm[3]} ---  H_amb | Phi  L_final  rho_c  max|u|  verdict", flush=True)
    for Hamb in Hambs:
        u1, Phi = _lm(lambda uu: resid(uu, Hamb), seed(ctx, rho0=0.7071, L0=1.0, amp=amp), maxit, budget)
        phi, rho, uf, L = unpack(u1, ctx); Lf = float(L)
        v = "FINITE" if (Phi < 1e-8 and 0 < Lf < 1e4) else ("runaway" if abs(Lf) >= 1e4 else "collapse/nc")
        print(f"  {Hamb:+.2f} | {Phi:.2e} {Lf:11.4f} {float(rho[0]):6.3f} {float(uf.abs().max()):.2e}  {v}", flush=True)


def mode_B(ctx, prm, Ls, amp=0.3, maxit=80, budget=10.0):
    """Fixed-L scan; clean H(seal)(L) curve (well-conditioned). Look for non-monotonicity."""
    Nr, Nth = ctx["Nr"], ctx["Nth"]; NF = 2 * Nr + Nr * Nth
    def resid(w, Lfix):
        v = torch.cat([w, torch.as_tensor([Lfix], dtype=torch.float64)])
        Q = fields(v, ctx, prm)
        rows = [Q["phi_ode"][1:-1], Q["phip"][[0, -1]], Q["rho_ode"][1:-1], Q["rhop"][[0, -1]],
                Q["res_f"][1:-1].reshape(-1), Q["fr"][0, :], Q["fr"][-1, :]]
        return torch.cat([r.reshape(-1) for r in rows])
    def wseed():
        u0 = seed(ctx, rho0=0.7071, L0=1.0, amp=amp); p, r, u, _ = unpack(u0, ctx)
        return pack(p, r, u, 1.0)[:NF]
    print(f"--- MODE B (fixed-L) N={prm[3]} ---  L | Phi  H_seal  rho_c  max|u|  I_r", flush=True)
    w = wseed()
    for L in Ls:
        w, Phi = _lm(lambda ww: resid(ww, float(L)), w, maxit, budget)
        if Phi > 1e-8:
            w, Phi = _lm(lambda ww: resid(ww, float(L)), wseed(), maxit, budget)
        v = torch.cat([w, torch.as_tensor([float(L)])]); Q = fields(v, ctx, prm)
        phi, rho, uf, _ = unpack(v, ctx)
        print(f"  {L:8.4f} | {Phi:.2e} {float(H_of_r(v, ctx, prm)[-1]):+8.3f} {float(rho[0]):7.3f} "
              f"{float(uf.abs().max()):.2e} {float(Q['Ir'].abs().max()):.2e}", flush=True)


if __name__ == "__main__":
    Z, XI, KAP = 8.0, 1.0, 1.0           # CHOSE-fixed (OBS-2 Route-A/Z=8; repo units)
    ctx = make_ctx(12, 14, rc=0.5)       # BOUNDED (anti-hang)
    Ls = np.geomspace(0.15, 25.0, 24)
    Hambs = [-0.95, -0.9, -0.6, -0.3, 0.0, 0.5]
    for N in (1, 2, 3):
        prm = (Z, XI, KAP, N)
        mode_A(ctx, prm, Hambs)
        mode_B(ctx, prm, Ls)
        print(flush=True)

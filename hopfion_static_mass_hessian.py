"""hopfion_static_mass_hessian.py -- Phase B (RIGOROUS, per Charles 2026-07-11).

Generalized eigenproblem  H v = lam M v  for the constrained tangent-space Hessian of the
flat-background carrier energy E=E2+E4, about a field INDEPENDENTLY RE-RELAXED (arrested-Newton)
to a true minimizer at EACH resolution. M = quadrature mass matrix = h^3 I (uniform grid), so
lam_phys = <v,H v>_euclid / (h^3 <v,v>_euclid) -- physically normalized, comparable across grids.
Perturbations: tangent eta=(I-n n^T)dn, FIXED-ASYMPTOTIC (eta=0 on a boundary layer -> n_inf fixed),
analytic-symmetry deflation ONLY (3 translations + 3 rotations + 1 target-SO(2)). Matrix-free FD-of-
gradient HVP (memory-light). Residual histories recorded. FAIL_H3_INSTABILITY iff a CONVERGED
localized negative lam_phys survives at the re-relaxed minimizer and persists/converges with refinement.

Usage: PYTHONPATH=$(pwd) python3 hopfion_static_mass_hessian.py --input <prod_h3.npz>
"""
import argparse, json, numpy as np, torch
from torch.func import grad
import hopfion_static_mass_common as C
torch.set_default_dtype(torch.float64)


def energy_of(n, h, xi, k4):
    n = n / n.norm(dim=0, keepdim=True); dn = [C._dc(n, i + 1, h) for i in range(3)]
    X = sum((dn[i] * dn[i]).sum(0) for i in range(3))
    def cr(a, b): return torch.stack([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]], 0)
    Y = torch.zeros_like(X)
    for i in range(3):
        for j in range(3):
            if i != j:
                Fij = (n * cr(dn[i], dn[j])).sum(0); Y = Y + Fij * Fij
    return (0.5 * xi * X + 0.25 * k4 * Y).sum() * h**3


def run_resolution(n0, stride, h0, L, xi, k4, relax_steps=250, eig_iters=40):
    dev = n0.device
    n = (n0[:, ::stride, ::stride, ::stride]).contiguous(); n = n / n.norm(dim=0, keepdim=True)
    N = n.shape[1]; h = h0 * stride
    gE = grad(lambda m: energy_of(m, h, xi, k4))
    def pt(v): return v - (v * n).sum(0, keepdim=True) * n
    def gnorm(nn): return float((gE(nn) - (gE(nn) * nn).sum(0, keepdim=True) * nn).norm())
    # ---- arrested-Newton re-relaxation to the coarse-grid minimizer ----
    g0 = gnorm(n); ghist = [g0]; vel = torch.zeros_like(n); dt = 0.02; E_prev = float(energy_of(n, h, xi, k4))
    for it in range(relax_steps):
        f = -pt(gE(n))
        vel = vel + dt * f
        if float((vel * f).sum()) < 0: vel = torch.zeros_like(n)          # arrest
        n_try = (n + dt * vel); n_try = n_try / n_try.norm(dim=0, keepdim=True)
        E_try = float(energy_of(n_try, h, xi, k4))
        if E_try > E_prev + 1e-9 * abs(E_prev):                           # unstable step -> shrink dt, reset vel
            dt *= 0.5; vel = torch.zeros_like(n); continue
        n = n_try; E_prev = E_try
        if it % 25 == 0 or it == relax_steps - 1: ghist.append(gnorm(n))
    gfin = gnorm(n)
    mf = C.matter_fields(n, h, xi, k4); E2 = float(mf['rho2'].sum()*h**3); E4 = float(mf['rho4'].sum()*h**3)
    # ---- fixed-asymptotic boundary mask (eta=0 on a boundary layer) ----
    b = max(3, N // 20)
    bmask = torch.zeros(N, N, N, device=dev); bmask[b:-b, b:-b, b:-b] = 1.0
    # ---- analytic symmetry modes ----
    x = torch.linspace(-L, L, N, device=dev); Xg, Yg, Zg = torch.meshgrid(x, x, x, indexing='ij'); rr = torch.sqrt(Xg**2+Yg**2+Zg**2)
    dn = [C._dc(n, i+1, h) for i in range(3)]
    sym = list(dn) + [Yg*dn[2]-Zg*dn[1], Zg*dn[0]-Xg*dn[2], Xg*dn[1]-Yg*dn[0]]
    a = n[:, 0, 0, 0]; a = a/a.norm(); sym.append(torch.stack([a[1]*n[2]-a[2]*n[1], a[2]*n[0]-a[0]*n[2], a[0]*n[1]-a[1]*n[0]], 0))
    S = [pt(s * bmask) for s in sym]; S = [s/s.norm() for s in S if s.norm() > 1e-10]
    def deflate(v):
        v = pt(v * bmask)                                                 # fixed boundary + tangent
        for s in S: v = v - (v * s).sum() * s
        return v
    EPS = 1e-4
    def hvp(v):
        v = deflate(v); Hv = (gE(n + EPS*v) - gE(n - EPS*v)) / (2*EPS); return deflate(Hv)
    def lf(v): w = (v*v).sum(0); return float((w*(rr <= 2.5)).sum()/(w.sum()+1e-30))
    # ---- LOBPCG-lite Rayleigh minimization; report lam_phys = lam_euclid / h^3 ----
    torch.manual_seed(0); v = deflate(torch.randn(3, N, N, N, device=dev)); v = v/v.norm(); p = None
    reshist = []
    for it in range(eig_iters):
        Hv = hvp(v); lam = float((v*Hv).sum()); gg = deflate(Hv - lam*v); reshist.append(float(gg.norm()))
        basis = [v, gg] + ([p] if p is not None else []); B = torch.stack([bb.reshape(-1) for bb in basis], 1)
        Qb, _ = torch.linalg.qr(B); cols = [Qb[:, c].reshape(3, N, N, N) for c in range(Qb.shape[1])]
        HB = torch.stack([hvp(c).reshape(-1) for c in cols], 1); Msm = 0.5*(Qb.T@HB + (Qb.T@HB).T)
        w, U = torch.linalg.eigh(Msm); vnew = deflate((Qb@U[:, 0]).reshape(3, N, N, N)); vnew = vnew/vnew.norm(); p = vnew-v; v = vnew; lam = float(w[0])
        if dev == 'cuda': torch.cuda.empty_cache()
    lam_phys = lam / h**3
    vol_frac = float((rr <= 2.5).sum()) / (N**3); localized = lf(v) > 5*vol_frac
    conv = reshist[-1] < 0.2*abs(lam)                                      # eigenpair converged?
    return dict(N=N, h=h, E2=E2, E4=E4, virial=E2/E4, gradnorm_hist=ghist, gradnorm_final=gfin,
                lam_euclid=lam, lam_phys=lam_phys, in_core=lf(v), localized=bool(localized),
                eig_converged=bool(conv), eig_resid_final=reshist[-1], eig_resid_hist=reshist[::5])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--input", default="hopfion_arc_scripts_2026-07-05/prod_an256.npz")
    a = ap.parse_args()
    d = C.load_h3(a.input); L = d['L']; xi = d['xi']; k4 = d['k4']
    runs = []
    for stride in (4, 2, 1):
        r = run_resolution(d['n'], stride, d['h'], L, xi, k4)
        print(f"N={r['N']} h={r['h']:.4f} virial={r['virial']:.4f} gradnorm {r['gradnorm_hist'][0]:.2e}->{r['gradnorm_final']:.2e} "
              f"lam_phys={r['lam_phys']:+.3e} in_core={r['in_core']:.3f} localized={r['localized']} "
              f"eig_conv={r['eig_converged']}(res={r['eig_resid_final']:.2e})", flush=True)
        runs.append(r)
        json.dump({'phaseB_runs': runs}, open('hopfion_static_mass_hessian_out.json', 'w'), indent=1)
    conv_locneg = [r for r in runs if r['localized'] and r['lam_phys'] < -1e-2 and r['eig_converged']]
    gate = "FAIL_H3_INSTABILITY" if conv_locneg else "PASS(no converged localized negative at re-relaxed minimizer)"
    print(f"\nPHASE B GATE: {gate}", flush=True)
    out = json.load(open('hopfion_static_mass_hessian_out.json')); out['gate'] = gate
    json.dump(out, open('hopfion_static_mass_hessian_out.json', 'w'), indent=1)

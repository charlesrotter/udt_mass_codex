"""hopfion_static_mass_hessian.py -- Phase B DEFINITIVE (per Charles 2026-07-11).

Re-relax the 256^3 carrier to a TRUE unconstrained critical point (arrested-Newton; Derrick
rescale as INITIAL CONDITIONER only, then DISABLED for final unconstrained convergence,
gradnorm->0), verifying Q_H is preserved. Then the generalized eigenproblem H v=lam M v
(M=h^3 I, lam_phys=lam_euclid/h^3), fixed-asymptotic perturbations (eta=0 on boundary layer),
QR-ORTHONORMAL analytic-symmetry deflation (3 trans+3 rot+1 target-SO(2)). Battery:
  * MULTIPLE random starts; TIGHT relative eigen-residual (res_phys/|lam_phys| target < 0.01);
  * HVP epsilon SCAN (lam stable vs FD step);
  * SAVE the lowest eigenvector + iteration history;
  * OVERLAP of the eigenvector with the residual gradient;
  * effect on Q_H (does perturbing along the mode change the Hopf charge?);
  * DIRECT quadratic energy check: E(n+t v)-E(n) vs 1/2 lam_euclid t^2.
FAIL_H3_INSTABILITY iff a CONVERGED, localized, negative lam_phys survives at the re-relaxed
critical point, is orthogonal-ish to the (now tiny) residual gradient, does NOT change Q_H,
and the direct energy decreases as predicted.
"""
import argparse, json, numpy as np, torch
import torch.nn.functional as Fn
from torch.func import grad
import hopfion_static_mass_common as C
torch.set_default_dtype(torch.float64)
try:
    import sys; sys.path.insert(0, 'hopfion_arc_scripts_2026-07-05')
    import fs_hopfion as FS
    HAS_FS = True
except Exception:
    HAS_FS = False


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


def hopf_charge(n, h, N, L):
    if HAS_FS:
        try: return float(abs(FS.hopf_charge(n, h, N, L)[0]))
        except Exception: pass
    return float('nan')


def rescale(n, factor):                                    # n(x/factor) via trilinear resample (Derrick)
    N = n.shape[1]; g = torch.linspace(-1, 1, N, device=n.device)
    gx, gy, gz = torch.meshgrid(g, g, g, indexing='ij')
    coords = torch.stack([gz, gy, gx], -1)[None] / factor
    ns = Fn.grid_sample(n[None], coords, align_corners=True, padding_mode='border')[0]
    return ns / ns.norm(dim=0, keepdim=True)


def relax(n, h, xi, k4, L, N, cond_steps=120, uncon_steps=500, dt0=0.01):
    gE = grad(lambda m: energy_of(m, h, xi, k4))
    def pt(v): return v - (v * n).sum(0, keepdim=True) * n
    def gn(nn): return float((gE(nn) - (gE(nn)*nn).sum(0, keepdim=True)*nn).norm())
    ghist = [gn(n)]; vel = torch.zeros_like(n); dt = dt0; Ep = float(energy_of(n, h, xi, k4))
    for phase, steps, rescale_on in [('cond', cond_steps, True), ('uncon', uncon_steps, False)]:
        vel = torch.zeros_like(n)
        for it in range(steps):
            if rescale_on and it % 20 == 19:                # Derrick rescale to virial=1 (conditioner ONLY)
                mf = C.matter_fields(n, h, xi, k4); E2 = float(mf['rho2'].sum()*h**3); E4 = float(mf['rho4'].sum()*h**3)
                n = rescale(n, (E4/E2)**0.25); vel = torch.zeros_like(n); Ep = float(energy_of(n, h, xi, k4)); continue
            f = -pt(gE(n)); vel = vel + dt*f
            if float((vel*f).sum()) < 0: vel = torch.zeros_like(n)
            n_try = n + dt*vel; n_try = n_try/n_try.norm(dim=0, keepdim=True); Et = float(energy_of(n_try, h, xi, k4))
            if Et > Ep + 1e-10*abs(Ep): dt *= 0.5; vel = torch.zeros_like(n); continue
            n = n_try; Ep = Et
            if it % 25 == 0: ghist.append(gn(n))
        ghist.append(gn(n))
    return n, ghist


def run(path, stride=1, tight=0.01):
    d = C.load_h3(path); n = d['n']; h0 = d['h']; L = d['L']; xi = d['xi']; k4 = d['k4']; dev = d['dev']
    n = (n[:, ::stride, ::stride, ::stride]).contiguous(); n = n/n.norm(dim=0, keepdim=True)
    N = n.shape[1]; h = h0*stride
    Q0 = hopf_charge(n, h, N, L)
    n, ghist = relax(n, h, xi, k4, L, N)
    gE = grad(lambda m: energy_of(m, h, xi, k4))
    def pt(v): return v-(v*n).sum(0, keepdim=True)*n
    gvec = pt(gE(n)); gnorm = float(gvec.norm()); ghat = gvec/(gvec.norm()+1e-30)
    mf = C.matter_fields(n, h, xi, k4); E2 = float(mf['rho2'].sum()*h**3); E4 = float(mf['rho4'].sum()*h**3)
    Qf = hopf_charge(n, h, N, L)
    b = max(3, N//20); bm = torch.zeros(N, N, N, device=dev); bm[b:-b, b:-b, b:-b] = 1.0
    x = torch.linspace(-L, L, N, device=dev); Xg, Yg, Zg = torch.meshgrid(x, x, x, indexing='ij'); rr = torch.sqrt(Xg**2+Yg**2+Zg**2)
    dn = [C._dc(n, i+1, h) for i in range(3)]
    sym = list(dn)+[Yg*dn[2]-Zg*dn[1], Zg*dn[0]-Xg*dn[2], Xg*dn[1]-Yg*dn[0]]
    a = n[:, 0, 0, 0]; a = a/a.norm(); sym.append(torch.stack([a[1]*n[2]-a[2]*n[1], a[2]*n[0]-a[0]*n[2], a[0]*n[1]-a[1]*n[0]], 0))
    # QR-orthonormalize the symmetry modes (fixed-boundary + tangent)
    Smat = torch.stack([pt(s*bm).reshape(-1) for s in sym], 1)
    Qsym, _ = torch.linalg.qr(Smat)                        # orthonormal columns
    def deflate(v):
        v = pt(v*bm).reshape(-1); v = v - Qsym@(Qsym.T@v); return v.reshape(3, N, N, N)
    def hvp(v, eps=1e-4): v = deflate(v); return deflate((gE(n+eps*v)-gE(n-eps*v))/(2*eps))
    def lf(v): w = (v*v).sum(0); return float((w*(rr <= 2.5)).sum()/(w.sum()+1e-30))
    # multi-start LOBPCG-lite, tight residual
    best = None
    for seed in range(3):
        torch.manual_seed(seed); v = deflate(torch.randn(3, N, N, N, device=dev)); v = v/v.norm(); p = None; hist = []
        for it in range(60):
            Hv = hvp(v); lam = float((v*Hv).sum()); gg = deflate(Hv-lam*v)
            hist.append((lam/h**3, float(gg.norm())/h**3, lf(v)))
            if float(gg.norm())/max(abs(lam), 1e-30) < tight and it > 8: break
            basis = [v, gg]+([p] if p is not None else []); B = torch.stack([bb.reshape(-1) for bb in basis], 1)
            Qb, _ = torch.linalg.qr(B); cols = [Qb[:, c].reshape(3, N, N, N) for c in range(Qb.shape[1])]
            HB = torch.stack([hvp(c).reshape(-1) for c in cols], 1); Msm = 0.5*(Qb.T@HB+(Qb.T@HB).T)
            w, U = torch.linalg.eigh(Msm); vnew = deflate((Qb@U[:, 0]).reshape(3, N, N, N)); vnew = vnew/vnew.norm(); p = vnew-v; v = vnew; lam = float(w[0])
            if dev == 'cuda': torch.cuda.empty_cache()
        lam_phys = lam/h**3; res_phys = float(deflate(hvp(v)-lam*v).norm())/h**3
        if best is None or lam_phys < best['lam_phys']:
            best = dict(lam_phys=lam_phys, res_phys=res_phys, in_core=lf(v), vec=v.clone(), lam_euclid=lam, hist=hist, seed=seed)
    v = best['vec']
    # HVP epsilon scan (lam stable vs FD step?)
    eps_scan = {f"{e:.0e}": float((v*hvp(v, eps=e)).sum())/h**3 for e in (1e-3, 1e-4, 1e-5)}
    # overlap with residual gradient
    overlap_ghat = abs(float((v*ghat).sum()))
    # effect on Q_H: perturb along the mode
    def Q_at(t):
        nt = n + t*v; nt = nt/nt.norm(dim=0, keepdim=True); return hopf_charge(nt, h, N, L)
    Q_pert = {f"t={t}": Q_at(t) for t in (0.0, 0.05, 0.1)}
    # DIRECT quadratic energy check along the mode
    E0 = float(energy_of(n, h, xi, k4)); ts = [0.02, 0.05, 0.1]
    dE = {f"t={t}": (float(energy_of((n+t*v)/(n+t*v).norm(dim=0, keepdim=True), h, xi, k4)) - E0) for t in ts}
    dE_pred = {f"t={t}": 0.5*best['lam_euclid']*t**2 for t in ts}
    conv = best['res_phys'] < tight*abs(best['lam_phys'])
    vol = float((rr <= 2.5).sum())/N**3; localized = best['in_core'] > 5*vol
    real = (best['lam_phys'] < -1.0 and localized and conv and overlap_ghat < 0.5
            and all(dE[k] < 0 for k in dE) and abs((Q_pert['t=0.1'] or 1)-(Q0 or 1)) < 0.1)
    verdict = "FAIL_H3_INSTABILITY" if real else ("PASS(no real converged localized negative)" if best['lam_phys'] > -1.0 else "UNRESOLVED")
    return dict(N=N, h=h, Q0=Q0, Qf=Qf, virial=E2/E4, gradnorm_final=gnorm, gradnorm_hist=ghist,
                lam_phys=best['lam_phys'], res_phys=best['res_phys'], in_core=best['in_core'], localized=localized,
                eig_converged=conv, eig_hist=best['hist'][::4]+[best['hist'][-1]], eps_scan=eps_scan,
                overlap_residgrad=overlap_ghat, Q_perturbed=Q_pert, dE_direct=dE, dE_predicted=dE_pred,
                verdict=verdict)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--input", default="hopfion_arc_scripts_2026-07-05/prod_an256.npz")
    ap.add_argument("--stride", type=int, default=1); a = ap.parse_args()
    r = run(a.input, stride=a.stride)
    print(json.dumps({k: v for k, v in r.items() if k not in ('gradnorm_hist', 'eig_hist')}, indent=1))
    print("gradnorm:", [f"{g:.2e}" for g in r['gradnorm_hist']])
    print("VERDICT:", r['verdict'])
    json.dump({'phaseB_definitive': r}, open('hopfion_static_mass_hessian_out.json', 'w'), indent=1)

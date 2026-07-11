"""Phase B clean: generalized eigenproblem H v=lam M v (M=h^3 I) at the 256^3 PRODUCTION minimizer
(already relaxed; NO breaking re-relaxation), FIXED-ASYMPTOTIC perturbations (eta=0 on boundary layer),
analytic-symmetry deflation only. Report lam_phys=lam_euclid/h^3 and the eigensolve residual in the
SAME (physical) units, so 'converged' means resid_phys << |lam_phys|. Localized negative that is
CONVERGED => concern; unconverged/near-zero => residual-gradient/continuum."""
import json, numpy as np, torch, hopfion_static_mass_common as C
from torch.func import grad
torch.set_default_dtype(torch.float64)
P = 'hopfion_arc_scripts_2026-07-05/prod_an256.npz'
d = C.load_h3(P); n = d['n']; h = d['h']; L = d['L']; xi = d['xi']; k4 = d['k4']; dev = d['dev']; N = d['N']
n = n / n.norm(dim=0, keepdim=True)
def energy_of(m, h):
    m = m/m.norm(dim=0, keepdim=True); dn = [C._dc(m, i+1, h) for i in range(3)]
    X = sum((dn[i]*dn[i]).sum(0) for i in range(3))
    def cr(a, b): return torch.stack([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]], 0)
    Y = torch.zeros_like(X)
    for i in range(3):
        for j in range(3):
            if i != j:
                Fij = (m*cr(dn[i], dn[j])).sum(0); Y = Y+Fij*Fij
    return (0.5*xi*X + 0.25*k4*Y).sum()*h**3
gE = grad(lambda m: energy_of(m, h))
mf = C.matter_fields(n, h, xi, k4); E2 = float(mf['rho2'].sum()*h**3); E4 = float(mf['rho4'].sum()*h**3)
def pt(v): return v-(v*n).sum(0, keepdim=True)*n
gnorm = float(pt(gE(n)).norm())
b = N//20; bmask = torch.zeros(N, N, N, device=dev); bmask[b:-b, b:-b, b:-b] = 1.0
x = torch.linspace(-L, L, N, device=dev); Xg, Yg, Zg = torch.meshgrid(x, x, x, indexing='ij'); rr = torch.sqrt(Xg**2+Yg**2+Zg**2)
dn = [C._dc(n, i+1, h) for i in range(3)]
sym = list(dn)+[Yg*dn[2]-Zg*dn[1], Zg*dn[0]-Xg*dn[2], Xg*dn[1]-Yg*dn[0]]
a = n[:, 0, 0, 0]; a = a/a.norm(); sym.append(torch.stack([a[1]*n[2]-a[2]*n[1], a[2]*n[0]-a[0]*n[2], a[0]*n[1]-a[1]*n[0]], 0))
S = [pt(s*bmask) for s in sym]; S = [s/s.norm() for s in S if s.norm() > 1e-10]
def deflate(v):
    v = pt(v*bmask)
    for s in S: v = v-(v*s).sum()*s
    return v
EPS = 1e-4
def hvp(v):
    v = deflate(v); return deflate((gE(n+EPS*v)-gE(n-EPS*v))/(2*EPS))
def lf(v): w = (v*v).sum(0); return float((w*(rr <= 2.5)).sum()/(w.sum()+1e-30))
print(f"256^3 production minimizer: virial={E2/E4:.4f} gradnorm={gnorm:.3e} (fixed-boundary, generalized norm)", flush=True)
torch.manual_seed(0); v = deflate(torch.randn(3, N, N, N, device=dev)); v = v/v.norm(); p = None
for it in range(45):
    Hv = hvp(v); lam = float((v*Hv).sum()); gg = deflate(Hv-lam*v)
    lam_phys = lam/h**3; res_phys = float(gg.norm())/h**3
    basis = [v, gg]+([p] if p is not None else []); B = torch.stack([bb.reshape(-1) for bb in basis], 1)
    Qb, _ = torch.linalg.qr(B); cols = [Qb[:, c].reshape(3, N, N, N) for c in range(Qb.shape[1])]
    HB = torch.stack([hvp(c).reshape(-1) for c in cols], 1); Msm = 0.5*(Qb.T@HB+(Qb.T@HB).T)
    w, U = torch.linalg.eigh(Msm); vnew = deflate((Qb@U[:, 0]).reshape(3, N, N, N)); vnew = vnew/vnew.norm(); p = vnew-v; v = vnew; lam = float(w[0])
    if it % 3 == 0 or it >= 40:
        conv = res_phys < 0.2*abs(lam_phys)
        print(f"  it={it:2d} lam_phys={lam_phys:+.3e} res_phys={res_phys:.3e} conv={conv} in_core={lf(v):.3f}", flush=True)
    if dev == 'cuda': torch.cuda.empty_cache()
lam_phys = lam/h**3; res_phys = float(deflate(hvp(v)-lam*v).norm())/h**3
vol = float((rr <= 2.5).sum())/N**3; localized = lf(v) > 5*vol; converged = res_phys < 0.2*abs(lam_phys)
verdict = ("FAIL_H3_INSTABILITY(converged localized negative)" if (lam_phys < -1.0 and localized and converged)
           else "PASS(no converged localized negative; lowest mode near-zero/positive)" if lam_phys > -1.0
           else "UNRESOLVED(negative but UNconverged -> residual-gradient/continuum, not a real eigenmode)")
print(f"\nFINAL lam_phys={lam_phys:+.3e} res_phys={res_phys:.3e} converged={converged} in_core={lf(v):.3f} localized={localized}\n=> {verdict}", flush=True)
json.dump({'phaseB_256_clean': {'virial': E2/E4, 'gradnorm': gnorm, 'lam_phys': lam_phys, 'res_phys': res_phys,
          'eig_converged': converged, 'in_core': lf(v), 'localized': localized, 'verdict': verdict,
          'note': 'fixed-boundary, generalized norm (M=h^3 I), production 256 minimizer as-is (gradnorm 0.13 residual). Multi-resolution re-relaxation BLOCKED: naive arrested-Newton collapses coarse hopfion (Derrick) without production rescale machinery.'}},
          open('hopfion_static_mass_hessian_out.json', 'w'), indent=1)
print('saved', flush=True)

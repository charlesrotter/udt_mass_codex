"""Controlled relaxation-to-best + tight Hessian (per Charles). The long unconstrained run DRIFTED
toward unwinding; the useful point is the LOWEST-gradnorm field BEFORE the drift. So: arrested-Newton
(fixed boundary, Q-monitored), track & save the best (lowest-gradnorm) field, STOP at the drift onset
(gradnorm rising or Q dropping), then a proper MULTI-START, TIGHT, QR-orthonormal-deflated generalized
eigenproblem at the best field. Tests whether the -312 localized negative lifts to positive as the
field approaches a true critical point (mode-follow log already showed +69 at gradnorm 0.086)."""
import sys, time, json, numpy as np, torch
sys.path.insert(0, 'hopfion_arc_scripts_2026-07-05')
import fs_hopfion as m
from torch.func import grad
torch.set_default_dtype(torch.float64); dev = m.dev
import os
d = np.load('prod_relax256uncon.npz' if os.path.exists('prod_relax256uncon.npz') else 'hopfion_arc_scripts_2026-07-05/prod_an256.npz')
n = torch.tensor(d['n'], device=dev); N = int(d['N']); L = float(d['L']); h = float(d['h']); xi = float(d['xi']); kap = float(d['kappa'])
n = n / n.norm(dim=0, keepdim=True)
n_inf = torch.tensor([0., 0., -1.], device=dev).view(3, 1, 1, 1)
def E_of(nn): return m.energy(nn, h, xi, kap)[0]
gE = grad(E_of)
def pinned(nn):
    with torch.no_grad(): m.pin_boundary(nn, n_inf, 2)
    return nn / nn.norm(dim=0, keepdim=True)
def tang(nn, v): return v - (v * nn).sum(0, keepdim=True) * nn
def tgrad(nn): return tang(nn, gE(nn))
def Qof(nn):
    try: return float(abs(m.hopf_charge(nn, h, N, L)[0]))
    except Exception: return float('nan')
LOG = 'scratchpad/controlled_relax.log'; open(LOG, 'w').close()
def logline(s):
    with open(LOG, 'a') as f: f.write(s + '\n')

# --- relaxation-to-best ---
n = pinned(n); vel = torch.zeros_like(n); dt = 0.02; Ep = float(E_of(n))
best_gn = float(tgrad(n).norm()); best_n = n.clone(); rising = 0; t0 = time.time()
logline(f"# start gradnorm={best_gn:.4e} Q={Qof(n):.4f}")
for it in range(1, 1801):
    g = tgrad(n)
    with torch.no_grad():
        vel = tang(n, vel - dt*g); n_try = pinned(n + dt*vel)
        Et = float(E_of(n_try)); Qt = Qof(n_try)
    if Et > Ep or Qt < 0.99:                          # arrest on E-rise; STRICT topology guard
        vel = torch.zeros_like(n)
        if Et > Ep: dt = max(dt*0.7, 2e-3)
        if Qt < 0.99: dt = max(dt*0.5, 2e-3)
    else:
        n = n_try; Ep = Et
    if it % 40 == 0:
        gn = float(tgrad(n).norm()); Q = Qof(n)
        logline(f"it={it} t={time.time()-t0:.0f}s gradnorm={gn:.4e} Q={Q:.4f} E={Ep:.4f} dt={dt:.1e}")
        if gn < best_gn and Q > 0.99: best_gn = gn; best_n = n.clone()   # track GLOBAL best (not first min)
        if Q < 0.99:                                  # STOP only at real drift onset (unwinding)
            logline(f"# STOP (drift) at it={it}: Q={Q:.4f}; best_gradnorm={best_gn:.4e}"); break
n = best_n; gn_best = float(tgrad(n).norm()); Qb = Qof(n)
with torch.no_grad(): np.savez('controlled_best_field.npz', n=(n/n.norm(dim=0, keepdim=True)).cpu().numpy(), N=N, L=L, xi=xi, kappa=kap, h=h)
logline(f"# BEST field: gradnorm={gn_best:.4e} Q={Qb:.4f}")

# --- tight multi-start Hessian at the best field ---
b = N // 20; bm = torch.zeros(N, N, N, device=dev); bm[b:-b, b:-b, b:-b] = 1.0
x = torch.linspace(-L, L, N, device=dev); Xg, Yg, Zg = torch.meshgrid(x, x, x, indexing='ij'); rr = torch.sqrt(Xg**2+Yg**2+Zg**2)
dn = [(torch.roll(n, -1, a+1)-torch.roll(n, 1, a+1))/(2*h) for a in range(3)]
sym = list(dn)+[Yg*dn[2]-Zg*dn[1], Zg*dn[0]-Xg*dn[2], Xg*dn[1]-Yg*dn[0]]
a = n[:, 0, 0, 0]; a = a/a.norm(); sym.append(torch.stack([a[1]*n[2]-a[2]*n[1], a[2]*n[0]-a[0]*n[2], a[0]*n[1]-a[1]*n[0]], 0))
Smat = torch.stack([tang(n, s*bm).reshape(-1) for s in sym], 1); Qsym, _ = torch.linalg.qr(Smat)
def defl(v):
    v = tang(n, v*bm).reshape(-1); v = v - Qsym@(Qsym.T@v); return v.reshape(3, N, N, N)
def hvp(v): v = defl(v); return defl((gE(n+1e-4*v)-gE(n-1e-4*v))/2e-4)
def lf(v): w = (v*v).sum(0); return float((w*(rr <= 2.5)).sum()/(w.sum()+1e-30))
best = None
for seed in range(3):
    torch.manual_seed(seed); v = defl(torch.randn(3, N, N, N, device=dev)); v = v/v.norm(); p = None
    for it in range(45):
        Hv = hvp(v); lam = float((v*Hv).sum()); gg = defl(Hv-lam*v)
        if float(gg.norm())/max(abs(lam), 1e-30) < 0.03 and it > 10: break
        B = torch.stack([bb.reshape(-1) for bb in ([v, gg]+([p] if p is not None else []))], 1)
        Qb2, _ = torch.linalg.qr(B); cols = [Qb2[:, c].reshape(3, N, N, N) for c in range(Qb2.shape[1])]
        HB = torch.stack([hvp(c).reshape(-1) for c in cols], 1); Msm = 0.5*(Qb2.T@HB+(Qb2.T@HB).T)
        w, U = torch.linalg.eigh(Msm); vn = defl((Qb2@U[:, 0]).reshape(3, N, N, N)); vn = vn/vn.norm(); p = vn-v; v = vn; lam = float(w[0])
        if dev == 'cuda': torch.cuda.empty_cache()
    lam_phys = lam/h**3; res = float(defl(hvp(v)-lam*v).norm())/h**3
    logline(f"  [eig seed={seed}] lam_phys={lam_phys:.3e} res_phys={res:.3e} in_core={lf(v):.3f} conv={res<0.03*abs(lam_phys)}")
    if best is None or lam_phys < best[0]: best = (lam_phys, res, lf(v))
lam_phys, res_phys, incore = best
verdict = ("STABLE-LEAN (lowest mode positive at best-relaxed field)" if lam_phys > 0
           else "localized-negative persists" if incore > 0.3 else "near-zero")
logline(f"# HESSIAN@best gradnorm={gn_best:.4e} Q={Qb:.4f} lowest_lam_phys={lam_phys:.3e} res={res_phys:.3e} in_core={incore:.3f} => {verdict}")
json.dump({'best_gradnorm': gn_best, 'Q': Qb, 'lowest_lam_phys': lam_phys, 'res_phys': res_phys,
           'in_core': incore, 'verdict': verdict}, open('controlled_relax_hessian_out.json', 'w'), indent=1)

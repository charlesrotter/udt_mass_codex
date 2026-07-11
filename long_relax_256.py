"""Multi-hour 256^3 mode-following relaxation (per Charles 2026-07-11) -- TOPOLOGY-SAFE.

Base = production arrested-Newton (velocity Verlet + arrest on E-rise; SMALL steps that stay in the
Q_H=1 sector -- aggressive CG unwinds to vacuum, verified). Plus:
  * FIXED BOUNDARY (pin n_inf each step),
  * TOPOLOGY MONITORING + Q-GUARD (reject any update that drops |Q_H| below 0.95),
  * MODE-FOLLOWING: every K steps compute the lowest Hessian mode; if localized-negative take a SMALL,
    Q-checked descent step along it (escape the arrested-Newton stall without unwinding),
  * final unconstrained (rescale-off) convergence -- this whole run is rescale-off.
Runs for many thousands of steps (hours) to test whether gradnorm goes below the ~0.12 arrested-Newton
stall. Logs gradnorm/Q/E; checkpoints the field. Resumable from long_relax_256_ckpt.npz.
"""
import sys, os, time, json, numpy as np, torch
sys.path.insert(0, 'hopfion_arc_scripts_2026-07-05')
import fs_hopfion as m
from torch.func import grad
torch.set_default_dtype(torch.float64); dev = m.dev
START = 'long_relax_256_ckpt.npz' if os.path.exists('long_relax_256_ckpt.npz') else 'prod_relax256uncon.npz'
d = np.load(START); n = torch.tensor(d['n'], device=dev); N = int(d['N']); L = float(d['L']); h = float(d['h']); xi = float(d['xi']); kap = float(d['kappa'])
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
LOG = 'scratchpad/long_relax_256.log'
def logline(s):
    with open(LOG, 'a') as f: f.write(s + '\n')
if not os.path.exists('long_relax_256_ckpt.npz'): open(LOG, 'w').close()

def lowest_mode(nn, iters=16):
    b = N // 20; bm = torch.zeros(N, N, N, device=dev); bm[b:-b, b:-b, b:-b] = 1.0
    x = torch.linspace(-L, L, N, device=dev); Xg, Yg, Zg = torch.meshgrid(x, x, x, indexing='ij'); rr = torch.sqrt(Xg**2+Yg**2+Zg**2)
    dn = [(torch.roll(nn, -1, a+1)-torch.roll(nn, 1, a+1))/(2*h) for a in range(3)]
    sym = list(dn)+[Yg*dn[2]-Zg*dn[1], Zg*dn[0]-Xg*dn[2], Xg*dn[1]-Yg*dn[0]]
    a = nn[:, 0, 0, 0]; a = a/a.norm(); sym.append(torch.stack([a[1]*nn[2]-a[2]*nn[1], a[2]*nn[0]-a[0]*nn[2], a[0]*nn[1]-a[1]*nn[0]], 0))
    Smat = torch.stack([tang(nn, s*bm).reshape(-1) for s in sym], 1); Qsym, _ = torch.linalg.qr(Smat)
    def defl(v):
        v = tang(nn, v*bm).reshape(-1); v = v - Qsym@(Qsym.T@v); return v.reshape(3, N, N, N)
    def hvp(v): v = defl(v); return defl((gE(nn+1e-4*v)-gE(nn-1e-4*v))/2e-4)
    torch.manual_seed(0); v = defl(torch.randn(3, N, N, N, device=dev)); v = v/v.norm(); p = None; lam = 0.0
    for _ in range(iters):
        Hv = hvp(v); lam = float((v*Hv).sum()); gg = defl(Hv-lam*v)
        B = torch.stack([bb.reshape(-1) for bb in ([v, gg]+([p] if p is not None else []))], 1)
        Qb, _ = torch.linalg.qr(B); cols = [Qb[:, c].reshape(3, N, N, N) for c in range(Qb.shape[1])]
        HB = torch.stack([hvp(c).reshape(-1) for c in cols], 1); Msm = 0.5*(Qb.T@HB+(Qb.T@HB).T)
        w, U = torch.linalg.eigh(Msm); vnew = defl((Qb@U[:, 0]).reshape(3, N, N, N)); vnew = vnew/vnew.norm(); p = vnew-v; v = vnew; lam = float(w[0])
        if dev == 'cuda': torch.cuda.empty_cache()
    w2 = (v*v).sum(0); return lam/h**3, v, float((w2*(rr <= 2.5)).sum()/(w2.sum()+1e-30))

n = pinned(n); vel = torch.zeros_like(n); dt = 0.02
Ep = float(E_of(n)); Q = Qof(n); t0 = time.time()
logline(f"# start(topology-safe) gradnorm={float(tgrad(n).norm()):.4e} Q={Q:.4f} E={Ep:.4f} dt={dt}")
MAXIT = 20000
for it in range(1, MAXIT+1):
    g = tgrad(n)
    with torch.no_grad():
        vel = vel - dt*g
        vel = tang(n, vel)
        n_try = pinned(n + dt*vel)
        Et = float(E_of(n_try)); Qt = Qof(n_try)
    if Et > Ep or Qt < 0.95:                         # arrest on E-rise OR topology guard
        vel = torch.zeros_like(n)
        if Et > Ep: dt = max(dt*0.7, 2e-3)
    else:
        n = n_try; Ep = Et; Q = Qt
    if it % 40 == 0:
        gn = float(tgrad(n).norm())
        logline(f"it={it} t={time.time()-t0:.0f}s gradnorm={gn:.4e} Q={Q:.4f} E={Ep:.4f} dt={dt:.1e}")
        if gn < 1e-3: logline(f"converged gradnorm<1e-3 at it={it}"); break
    if it % 1000 == 0:                               # MODE-FOLLOWING (small, Q-checked)
        lam, v, incore = lowest_mode(n)
        logline(f"  [mode-follow it={it}] lowest lam_phys={lam:.3e} in_core={incore:.3f}")
        if lam < -1.0 and incore > 0.3:
            for amp in (0.05, 0.02, 0.01):
                nt = pinned(n + amp*v)
                if float(E_of(nt)) < Ep and Qof(nt) >= 0.95:
                    n = nt; Ep = float(E_of(n)); vel = torch.zeros_like(n); break
    if it % 500 == 0:
        with torch.no_grad(): nf = (n/n.norm(dim=0, keepdim=True)).cpu().numpy()
        np.savez('long_relax_256_ckpt.npz', n=nf, N=N, L=L, xi=xi, kappa=kap, h=h)
lam, v, incore = lowest_mode(n)
with torch.no_grad(): nf = (n/n.norm(dim=0, keepdim=True)).cpu().numpy()
np.savez('long_relax_256_final.npz', n=nf, N=N, L=L, xi=xi, kappa=kap, h=h)
gn = float(tgrad(n).norm())
logline(f"# FINAL gradnorm={gn:.4e} Q={Qof(n):.4f} lowest_lam_phys={lam:.3e} in_core={incore:.3f} time={time.time()-t0:.0f}s iters={it}")
json.dump({'final_gradnorm': gn, 'Q': Qof(n), 'lowest_lam_phys': lam, 'in_core': incore, 'iters': it,
           'start_gradnorm': 0.1197}, open('long_relax_256_out.json', 'w'), indent=1)

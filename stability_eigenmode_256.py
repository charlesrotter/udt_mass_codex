"""Lowest tangent-space Hessian mode(s) at the best-relaxed 256^3 field, via BLOCK LOBPCG (block size 3).
Per Charles 2026-07-11: a converged block LOBPCG/Lanczos with ||Hv-lam M v||/(|lam| ||M v||)<1e-2 (pref
1e-3). A single-vector iteration STALLS at rel~0.11 and RISES (verified) because the lowest mode is
near-degenerate (symmetry multiplet); a block resolves the multiplet.

Robustness (all verified by scratchpad/memdiag*.py -- flat 7GB, 26GB free, no leak):
 * manual-autograd gE (no functorch);  * FD-of-gradient HVP (matches exact analytic HVP to 6.5e-10);
 * MANUAL Gram-Schmidt on the <=9 basis vectors (NO torch.linalg.qr on the 50M-row tall matrix -- that
   cuSOLVER workspace spike, ~13GB, was the earlier OOM);  * streamed gram (one HVP live at a time).
Constrained core-masked tangent space; 7 analytic symmetry modes deflated. M=h^3 I => lam_phys=
lam_euclid/h^3; rel = ||R_euclid||/|lam_euclid|. Saves M-normalized lowest eigenvector (v^T M v=1)."""
import sys, os, gc, time, json, numpy as np, torch
sys.path.insert(0, 'hopfion_arc_scripts_2026-07-05')
import fs_hopfion as m
torch.set_default_dtype(torch.float64); dev = m.dev
FIELD = 'controlled_best_field.npz'
d = np.load(FIELD); n = torch.tensor(d['n'], device=dev); N = int(d['N']); L = float(d['L']); h = float(d['h']); xi = float(d['xi']); kap = float(d['kappa'])
n = n / n.norm(dim=0, keepdim=True)
def E_of(nn): return m.energy(nn, h, xi, kap)[0]
def gE(nn):
    nn2 = nn.detach().clone().requires_grad_(True)
    g, = torch.autograd.grad(m.energy(nn2, h, xi, kap)[0], nn2); return g.detach()
def tang(nn, v): return v - (v * nn).sum(0, keepdim=True) * nn
def Qof(nn):
    try: return float(abs(m.hopf_charge(nn, h, N, L)[0]))
    except Exception: return float('nan')
LOG = 'scratchpad/stability_eigenmode_256.log'; open(LOG, 'w').close()
def logline(s):
    with open(LOG, 'a') as f: f.write(s + '\n')
    print(s, flush=True)
gn0 = float(tang(n, gE(n)).norm()); Q0 = Qof(n)
logline(f"# BLOCK LOBPCG  field={FIELD} N={N} L={L} h={h:.5f} gradnorm={gn0:.4e} Q={Q0:.4f}")

bmask = N // 20; bm = torch.zeros(N, N, N, device=dev); bm[bmask:-bmask, bmask:-bmask, bmask:-bmask] = 1.0
x = torch.linspace(-L, L, N, device=dev); Xg, Yg, Zg = torch.meshgrid(x, x, x, indexing='ij')
rr = torch.sqrt(Xg**2 + Yg**2 + Zg**2)
dn = [(torch.roll(n, -1, a + 1) - torch.roll(n, 1, a + 1)) / (2 * h) for a in range(3)]
sym = list(dn) + [Yg * dn[2] - Zg * dn[1], Zg * dn[0] - Xg * dn[2], Xg * dn[1] - Yg * dn[0]]
a0 = n[:, 0, 0, 0]; a0 = a0 / a0.norm()
sym.append(torch.stack([a0[1] * n[2] - a0[2] * n[1], a0[2] * n[0] - a0[0] * n[2], a0[0] * n[1] - a0[1] * n[0]], 0))
Qsym, _ = torch.linalg.qr(torch.stack([tang(n, s * bm).reshape(-1) for s in sym], 1)); del sym, dn
def defl(v):
    v = tang(n, v * bm).reshape(-1); v = v - Qsym @ (Qsym.T @ v); return v.reshape(3, N, N, N)
EPS = 1e-4
def hvp(v):
    v = defl(v); return defl((gE(n + EPS * v) - gE(n - EPS * v)) / (2 * EPS))
def core_frac(v):
    w = (v * v).sum(0); return float((w * (rr <= 2.5)).sum() / (w.sum() + 1e-30))
def ip(a, b): return float((a * b).sum())
def atomic_savez(path, **kw):                    # write-temp-then-rename: a kill never corrupts the ckpt
    tmp = path + '.tmp.npz'; np.savez(tmp, **kw); os.replace(tmp, path)
def mgs(cols):                                   # manual Gram-Schmidt (NO cuSOLVER tall-QR)
    out = []
    for c in cols:
        c = defl(c)
        for o in out: c = c - ip(c, o) * o
        nc = float(c.norm())
        if nc > 1e-9: out.append(c / nc)
    return out

bs = 4; torch.manual_seed(0)
if os.environ.get('RESUME_EIG', '0') == '1' and os.path.exists('stability_lowmode_256.npz'):
    Z = np.load('stability_lowmode_256.npz'); v0 = defl(torch.tensor(Z['v'], device=dev))
    X = mgs([v0] + [torch.randn(3, N, N, N, device=dev) * (rr <= 3.5).double() for _ in range(bs - 1)])
    logline(f"# WARM START from saved v: lam_phys={float(Z['lam_phys']):.3e} rel={float(Z['rel_res']):.2e}")
else:
    X = mgs([torch.randn(3, N, N, N, device=dev) * (rr <= 3.5).double() for _ in range(bs)])
# initialize the best-bar from any existing checkpoint so a run NEVER overwrites a better saved v
best = None
if os.path.exists('stability_lowmode_256.npz'):
    try:
        Zb = np.load('stability_lowmode_256.npz'); best = dict(rel=float(Zb['rel_res']), lam_phys=float(Zb['lam_phys']), core=float(Zb['core']), it=-1)
        logline(f"# best-bar from checkpoint: rel={best['rel']:.3e}")
    except Exception: best = None
P = []; t0 = time.time(); prev_lam0 = None
for it in range(80):
    R = []                                        # residuals of the current block X (expand search space)
    for j in range(len(X)):
        Hxj = hvp(X[j]); th = ip(X[j], Hxj); R.append(defl(Hxj - th * X[j])); del Hxj
        if dev == 'cuda': torch.cuda.empty_cache()
    basis = mgs(X + R + P)                         # <=9 orthonormal vectors
    k = len(basis); A = torch.zeros(k, k, device=dev)
    for j in range(k):                            # streamed gram: one HVP live at a time
        Hj = hvp(basis[j])
        for i in range(k): A[i, j] = ip(basis[i], Hj)
        del Hj; gc.collect()
        if dev == 'cuda': torch.cuda.empty_cache()
    A = 0.5 * (A + A.T); w, U = torch.linalg.eigh(A)
    newX = [defl(sum(U[i, j] * basis[i] for i in range(k))) for j in range(bs)]
    newX = [v / v.norm() for v in newX]
    lam0 = float(w[0]); Hx0 = hvp(newX[0]); R0 = defl(Hx0 - lam0 * newX[0]); r0 = float(R0.norm()); del Hx0
    rel = r0 / (abs(lam0) + 1e-30); lamp = lam0 / h**3; cf = core_frac(newX[0])
    dlam = abs(lamp - prev_lam0) / (abs(lamp) + 1e-30) if prev_lam0 is not None else 1.0; prev_lam0 = lamp
    logline(f"it={it} t={time.time()-t0:.0f}s lam_phys={lamp:.4e} rel_res={rel:.3e} core={cf:.3f} "
            f"dlam={dlam:.2e} lam1_phys={float(w[1])/h**3:.3e} lam2_phys={float(w[2])/h**3:.3e} "
            f"resv={torch.cuda.memory_reserved()/1e9:.1f}G")
    if lamp < 0 and (best is None or rel < best['rel']):
        vn = newX[0] / (newX[0].norm() * h**1.5)  # M-normalize: v^T M v = h^3||v||^2 = 1
        v1 = (newX[1] / (newX[1].norm() * h**1.5)).detach().cpu().numpy()
        v2 = (newX[2] / (newX[2].norm() * h**1.5)).detach().cpu().numpy()
        best = dict(rel=rel, lam_phys=lamp, core=cf, it=it)
        atomic_savez('stability_lowmode_256.npz', v=vn.detach().cpu().numpy(), v1=v1, v2=v2, lam_phys=lamp,
                     rel_res=rel, core=cf, lam1_phys=float(w[1]) / h**3, lam2_phys=float(w[2]) / h**3,
                     core1=core_frac(newX[1]), core2=core_frac(newX[2]),
                     N=N, L=L, h=h, xi=xi, kappa=kap, field=FIELD, gradnorm=gn0, Q=Q0)
    if lamp < 0 and rel < 1e-2 and it > 4:
        logline(f"# CONVERGED rel_res={rel:.2e} < 1e-2 at it={it}")
        if rel < 1e-3: logline("#   (also < 1e-3)")
        break
    P = [defl(newX[j] - X[j]) for j in range(min(bs, len(X)))]   # search-direction memory
    X = newX
    del basis, A, U, w, R, R0; gc.collect()
    if dev == 'cuda': torch.cuda.empty_cache()

logline(f"# BEST lam_phys={best['lam_phys']:.4e} rel_res={best['rel']:.3e} core={best['core']:.3f} it={best['it']} "
        f"(saved stability_lowmode_256.npz; M-normalized v^T M v=1)")
json.dump({'lam_phys': best['lam_phys'], 'rel_res': best['rel'], 'core_frac': best['core'],
           'field': FIELD, 'field_gradnorm': gn0, 'field_Q': Q0, 'converged_1e-3': best['rel'] < 1e-3,
           'converged_1e-2': best['rel'] < 1e-2, 'method': 'block LOBPCG bs=3, manual-GS, streamed, FD-HVP'},
          open('stability_eigenmode_256_out.json', 'w'), indent=1)

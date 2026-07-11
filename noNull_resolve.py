"""STEP 3b (per Charles + collaborating AI): re-relax the carrier under the corrected NO-NULL energy to a
Q_H=1 critical field, then compute the TRUE lowest tangent-space Hessian mode of E_noNull. Question:
once the Nyquist artifact is removed, is the carrier STABLE (lowest mode >= 0 up to deflated zero modes),
or does a genuine SMOOTH negative mode remain?

Stage 1: Riemannian L-BFGS on E_noNull (memory 6, transport-by-projection, backtracking Armijo, FIXED
  asymptotic boundary, NO Derrick rescaling). Track E, E2, E4, gradnorm, Q_H (centered monitor + caveat).
  Resumable via noNull_relaxed_field.npz.
Stage 2: block LOBPCG (bs=4, manual-GS, streamed, FD-of-gradient HVP) for the lowest Hessian mode of
  E_noNull at the relaxed field; deflate the 7 analytic symmetry modes; report lam_phys and the mode's
  checkerboard content R_cb (a genuine physical mode is smooth: R_cb ~ 1).
E_noNull is 8x the centered energy -> ~8x slower; run bounded, one clean GPU process, reliable launch
(timeout python3, NOT nohup&). DATA-BLIND."""
import sys, os, gc, time, json, numpy as np, torch
from collections import deque
sys.path.insert(0, 'hopfion_arc_scripts_2026-07-05')
import fs_hopfion as m
from noNull_energy import energy_noNull, grad_noNull
torch.set_default_dtype(torch.float64); dev = 'cuda' if torch.cuda.is_available() else 'cpu'

d0 = np.load('controlled_best_field.npz')
N = int(d0['N']); L = float(d0['L']); h = float(d0['h']); xi = float(d0['xi']); kap = float(d0['kappa'])
n_inf = torch.tensor([0., 0., -1.], device=dev).view(3, 1, 1, 1)
@torch.no_grad()
def E_of(nn): return float(energy_noNull(nn, h, xi, kap)[0])
@torch.no_grad()
def E3(nn):
    e = energy_noNull(nn, h, xi, kap); return float(e[0]), float(e[1]), float(e[2])
def gE(nn): return grad_noNull(nn, h, xi, kap)          # memory-safe per-orientation accumulation
def tang(nn, a): return a - (a * nn).sum(0, keepdim=True) * nn
def pin(nn):
    with torch.no_grad(): m.pin_boundary(nn, n_inf, 2)
    return nn / nn.norm(dim=0, keepdim=True)
def rgrad(nn): return tang(nn, gE(nn))
def Qof(nn):
    try: return float(abs(m.hopf_charge(nn, h, N, L)[0]))   # centered monitor (caveat: null operator)
    except Exception: return float('nan')
def ip(a, b): return float((a * b).sum())
LOG = 'scratchpad/noNull_resolve.log'
def logline(s):
    with open(LOG, 'a') as f: f.write(s + '\n')
    print(s, flush=True)

BUDGET1 = float(os.environ.get('RELAX_BUDGET_S', '2400'))
GN_TARGET = float(os.environ.get('GN_TARGET', '2e-2'))
# ---------------- Stage 1: relax under E_noNull (always continues from checkpoint or n0) ----------------
if os.path.exists('noNull_relaxed_field.npz'):
    R = np.load('noNull_relaxed_field.npz'); n = pin(torch.tensor(R['n'], device=dev))
    logline(f"# RESUME relaxed field: gradnorm={float(rgrad(n).norm()):.4e} Q={Qof(n):.4f}")
else:
    open(LOG, 'w').close()
    n = pin(torch.tensor(d0['n'], device=dev))
E, E2, E4 = E3(n); gn0start = float(rgrad(n).norm()); Q = Qof(n)
logline(f"# STAGE 1 relax under E_noNull (target gradnorm<{GN_TARGET:.0e}). E={E:.4f} (E2={E2:.3f} E4={E4:.3f}) gradnorm={gn0start:.4e} Q={Q:.4f}")
if gn0start < GN_TARGET:
    logline("# already at target -> skip to stage 2")
else:
    hist = deque(maxlen=6); g = rgrad(n); E = float(E_of(n)); t0 = time.time()
    for it in range(1, 4000):
        q = g.clone(); alphas = []
        H = [(tang(n, s), tang(n, y)) for (s, y) in hist]
        use = [(s, y) for (s, y) in H if ip(y, s) > 1e-12]; rhos = [1.0 / ip(y, s) for (s, y) in use]
        for (s, y), rho in zip(reversed(use), reversed(rhos)):
            a = rho * ip(s, q); alphas.append(a); q = q - a * y
        r = (ip(use[-1][0], use[-1][1]) / ip(use[-1][1], use[-1][1])) * q if use else q
        for (s, y), rho, a in zip(use, rhos, reversed(alphas)):
            b = rho * ip(y, r); r = r + (a - b) * s
        dvec = tang(n, -r)
        if ip(g, dvec) >= -1e-14 * (g.norm() * dvec.norm() + 1e-30): dvec = -g; hist.clear()
        slope = ip(g, dvec); a = 1.0 if hist else min(1.0, 1.0 / (g.norm() + 1e-30)); En = None
        for _ in range(30):
            nt = pin(n + a * dvec); Et = float(E_of(nt))
            if Et <= E + 1e-4 * a * slope: En = Et; break
            a *= 0.5
        if En is None:
            if hist: hist.clear(); continue
            logline(f"# stage1 line-search stuck at it={it}"); break
        gnew = rgrad(nt); s = tang(nt, a * dvec); y = gnew - tang(nt, g)
        if ip(s, y) > 1e-12: hist.append((s.clone(), y.clone()))
        n = nt; g = gnew; E = En
        if it % 10 == 0: gc.collect(); torch.cuda.empty_cache()
        if it % 25 == 0 or it == 1:
            gn = float(g.norm()); E2, E4 = float(energy_noNull(n, h, xi, kap)[1]), float(energy_noNull(n, h, xi, kap)[2]); Q = Qof(n)
            logline(f"  [relax] it={it} t={time.time()-t0:.0f}s E={E:.4f} (E2={E2:.3f} E4={E4:.3f}) gradnorm={gn:.4e} Q={Q:.4f}")
            with torch.no_grad():
                np.savez('noNull_relaxed_field.npz.tmp.npz', n=(n / n.norm(dim=0, keepdim=True)).cpu().numpy(),
                         N=N, L=L, h=h, xi=xi, kappa=kap); os.replace('noNull_relaxed_field.npz.tmp.npz', 'noNull_relaxed_field.npz')
            if gn < GN_TARGET: logline(f"# stage1 converged gradnorm<{GN_TARGET:.0e}"); break
            if time.time() - t0 > BUDGET1: logline("# stage1 budget hit"); break
    gnf = float(rgrad(n).norm()); Ef, E2f, E4f = E3(n)
    logline(f"# STAGE 1 DONE gradnorm={gnf:.4e} Q={Qof(n):.4f} E={Ef:.4f} (E2={E2f:.3f} E4={E4f:.3f})")

# ---------------- Stage 2: lowest Hessian mode of E_noNull ----------------
logline("# STAGE 2: block LOBPCG lowest Hessian mode of E_noNull at the relaxed field")
gn0 = float(rgrad(n).norm())
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
def ip3(a, b): return float((a * b).sum())
def mgs(cols):
    out = []
    for c in cols:
        c = defl(c)
        for o in out: c = c - ip3(c, o) * o
        nc = float(c.norm())
        if nc > 1e-9: out.append(c / nc)
    return out
def R_cb(v):
    Dc = lambda f, ax: (torch.roll(f, -1, ax) - torch.roll(f, 1, ax)) / (2 * h)
    Dp = lambda f, ax: (torch.roll(f, -1, ax) - f) / h
    num = sum((Dc(v[c], a)**2).sum() for c in range(3) for a in range(3))
    den = sum((Dp(v[c], a)**2).sum() for c in range(3) for a in range(3))
    return float(num / (den + 1e-300))

bs = 4; torch.manual_seed(0)
X = mgs([torch.randn(3, N, N, N, device=dev) * (rr <= 3.5).double() for _ in range(bs)])
P = []; best = None; t0 = time.time(); prev = None
for it in range(80):
    Rr = []
    for j in range(len(X)):
        Hx = hvp(X[j]); th = ip3(X[j], Hx); Rr.append(defl(Hx - th * X[j])); del Hx
        if dev == 'cuda': torch.cuda.empty_cache()
    basis = mgs(X + Rr + P); k = len(basis); A = torch.zeros(k, k, device=dev)
    for j in range(k):
        Hj = hvp(basis[j])
        for i in range(k): A[i, j] = ip3(basis[i], Hj)
        del Hj; gc.collect()
        if dev == 'cuda': torch.cuda.empty_cache()
    A = 0.5 * (A + A.T); w, U = torch.linalg.eigh(A)
    newX = [defl(sum(U[i, j] * basis[i] for i in range(k))) for j in range(bs)]
    newX = [v / v.norm() for v in newX]
    lam0 = float(w[0]); Hx0 = hvp(newX[0]); r0 = float(defl(Hx0 - lam0 * newX[0]).norm()); del Hx0
    rel = r0 / (abs(lam0) + 1e-30); lamp = lam0 / h**3; rcb = R_cb(newX[0])
    dl = abs(lamp - prev) / (abs(lamp) + 1e-30) if prev is not None else 1.0; prev = lamp
    logline(f"  [hess] it={it} t={time.time()-t0:.0f}s lam0_phys={lamp:.4e} rel={rel:.3e} R_cb={rcb:.3f} "
            f"dl={dl:.2e} lam123_phys=[{float(w[1])/h**3:.2e},{float(w[2])/h**3:.2e},{float(w[3])/h**3:.2e}]")
    if best is None or rel < best['rel']:
        best = dict(rel=rel, lam_phys=lamp, R_cb=rcb, lam123=[float(w[i]) / h**3 for i in range(1, 4)], it=it)
    if rel < 1e-2 and it > 4:
        logline(f"# hessian CONVERGED rel={rel:.2e}"); break
    P = [defl(newX[j] - X[j]) for j in range(min(bs, len(X)))]; X = newX
    del basis, A, U, w, Rr; gc.collect()
    if dev == 'cuda': torch.cuda.empty_cache()

verdict = ("STABLE (lowest mode >= 0 up to deflated zero modes)" if best['lam_phys'] > -1.0
           else ("SMOOTH negative mode remains -> genuine" if best['R_cb'] > 0.5 else "still-Nyquist (deflation/relax incomplete)"))
logline(f"# STAGE 2 DONE lowest lam_phys={best['lam_phys']:.4e} rel={best['rel']:.3e} R_cb={best['R_cb']:.3f} "
        f"next3={best['lam123']} => {verdict}")
json.dump({'relaxed_gradnorm': gn0, 'lowest_lam_phys': best['lam_phys'], 'rel_res': best['rel'],
           'lowest_R_cb': best['R_cb'], 'next3_lam_phys': best['lam123'], 'verdict': verdict,
           'operator': 'noNull 8-orientation', 'field': 'noNull_relaxed_field.npz'},
          open('noNull_resolve_out.json', 'w'), indent=1)

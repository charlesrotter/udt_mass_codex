# BLIND VERIFIER — independent negative-mode hunt at N=128.
# Own LOBPCG (block Rayleigh-Ritz over [X, W, P]) with own FFT diagonal preconditioner.
# Two deflation variants: 'u1' (only exact U(1) removed -> FULL space incl. T/R quasi-modes)
#                         'u1tr' (u1 + 6 T/R directions removed -> 'genuine' subspace)
import os, sys, time, math
import numpy as np, torch
sys.path.insert(0, '/home/udt-admin/udt_mass_codex')
from noNull_energy import grad_noNull

torch.set_default_dtype(torch.float64)
dev = 'cuda'
SEED = int(os.environ.get('SEED', '0'))
VAR = os.environ.get('VAR', 'u1tr')
NIT = int(os.environ.get('NIT', '150'))
BK = int(os.environ.get('BK', '8'))

root = '/home/udt-admin/udt_mass_codex/'
d = np.load(root + 'noNull_critical_field_128.npz')
N = int(d['N']); L = float(d['L']); h = float(d['h']); xi = float(d['xi']); kap = float(d['kappa'])
n = torch.tensor(d['n'], device=dev)
W2 = 2
msk = torch.zeros(N, N, N, device=dev); msk[W2:-W2, W2:-W2, W2:-W2] = 1.0
def P(v): return (v - (v * n).sum(0, keepdim=True) * n) * msk
def ipf(a, b): return float((a * b).sum())
def gE(x): return grad_noNull(x, h, xi, kap)

# symmetry basis
xg = torch.linspace(-L, L, N, device=dev)
Xg, Yg, Zg = torch.meshgrid(xg, xg, xg, indexing='ij')
dnc = [(torch.roll(n, -1, a + 1) - torch.roll(n, 1, a + 1)) / (2 * h) for a in range(3)]
u1 = P(torch.stack([-n[1], n[0], torch.zeros_like(n[0])], 0)); u1 = u1 / u1.norm()
trs = [dnc[0], dnc[1], dnc[2],
       Yg * dnc[2] - Zg * dnc[1], Zg * dnc[0] - Xg * dnc[2], Xg * dnc[1] - Yg * dnc[0]]
Q = [u1]
for v in trs:
    c = P(v)
    for q in Q: c = c - ipf(c, q) * q
    nc = float(c.norm())
    if nc > 1e-9: Q.append(c / nc)
Q_TR = Q[1:]
del dnc, trs, Xg, Yg, Zg
DEFL = [u1] if VAR == 'u1' else Q
print(f"# VAR={VAR} deflating {len(DEFL)} dirs; seed={SEED} block={BK} nit={NIT}", flush=True)

def D(v):
    v = P(v)
    for q in DEFL: v = v - ipf(v, q) * q
    return v
EPS = 1e-4
def A(v):  # deflated Hessian in lam_phys units
    vd = D(v)
    return D((gE(n + EPS * vd) - gE(n - EPS * vd)) / (2 * EPS)) / h**3

# undeflated RQ of the TR basis vectors themselves (pseudomode floor)
def Araw(v):
    vp = P(v)
    return P((gE(n + EPS * vp) - gE(n - EPS * vp)) / (2 * EPS)) / h**3
if VAR == 'u1':
    print("RQ(u1) =", f"{ipf(u1, Araw(u1)):.6f}")
    for i, q in enumerate(Q_TR):
        Aq = Araw(q); rq = ipf(q, Aq)
        res = float(P(Aq - rq * q).norm())
        print(f"RQ(qTR{i}) = {rq:+.6f}  ||res||/|rq| ~ {res/(abs(rq)+1e-12):.2e}")

# operator symmetry sanity
torch.manual_seed(999)
a1 = D(torch.randn(3, N, N, N, device=dev)); a1 /= a1.norm()
a2 = D(torch.randn(3, N, N, N, device=dev)); a2 /= a2.norm()
s12, s21 = ipf(a1, A(a2)), ipf(a2, A(a1))
print(f"symmetry check <a1,Aa2>={s12:.6e} <a2,Aa1>={s21:.6e} reldiff={abs(s12-s21)/max(abs(s12),1e-12):.2e}")
del a1, a2

# FFT diagonal preconditioner (own): symbol = c0 + 2*xi*k^2 + c4*k^4
k1 = 2 * math.pi * torch.fft.fftfreq(N, d=h, device=dev)
KX, KY, KZ = torch.meshgrid(k1, k1, k1, indexing='ij')
k2 = KX * KX + KY * KY + KZ * KZ
sym = 0.5 + 2.0 * xi * k2 + 0.02 * k2 * k2
del KX, KY, KZ, k2
def T(v):
    out = torch.empty_like(v)
    for c in range(3):
        out[c] = torch.fft.ifftn(torch.fft.fftn(v[c]) / sym).real
    return out

# ---- LOBPCG ----
CKPT = os.environ.get('CKPT', '')
g = torch.Generator(device='cuda'); g.manual_seed(SEED * 7919 + 13)
if CKPT and os.path.exists(CKPT):
    ck = np.load(CKPT)
    X = [D(torch.tensor(ck[f'x{j}'], device=dev)) for j in range(int(ck['k']))]
    print(f"# resumed {len(X)} vectors from {CKPT}", flush=True)
else:
    X = [D(torch.randn(3, N, N, N, device=dev, generator=g)) for _ in range(BK)]
def orthonorm(vecs):
    out = []
    for v in vecs:
        for o in out: v = v - ipf(v, o) * o
        for o in out: v = v - ipf(v, o) * o
        nv = float(v.norm())
        if nv > 1e-8: out.append(v / nv)
    return out
X = orthonorm(X)
AX = [A(x) for x in X]
Pdir = []
t0 = time.time()
for it in range(NIT):
    lam = [ipf(X[j], AX[j]) for j in range(len(X))]
    R = [D(AX[j] - lam[j] * X[j]) for j in range(len(X))]
    rn = [float(R[j].norm()) / (float(AX[j].norm()) + abs(lam[j])) for j in range(len(X))]
    if it % 5 == 0 or it == NIT - 1:
        print(f"it={it} t={time.time()-t0:.0f}s lam={['%.4f'%l for l in sorted(lam)]} rmax={max(rn):.2e} rmin={min(rn):.2e}", flush=True)
    Wd = [D(T(r)) for r in R]
    S = X + Wd + Pdir
    S = orthonorm(S)
    m = len(S)
    AS = [A(s) for s in S]
    G = torch.zeros(m, m, dtype=torch.float64)
    for i in range(m):
        for j in range(i, m):
            G[i, j] = ipf(S[i], AS[j]); G[j, i] = G[i, j]
    ew, ev = torch.linalg.eigh(G)
    k = min(BK, m)
    Xn = []; AXn = []
    for j in range(k):
        v = torch.zeros_like(S[0]); av = torch.zeros_like(S[0])
        for i in range(m):
            c = float(ev[i, j])
            if abs(c) > 1e-14:
                v = v + c * S[i]; av = av + c * AS[i]
        Xn.append(v); AXn.append(av)
    # P dirs = component of new X outside old X span
    Pdir = []
    for j in range(min(k, BK)):
        v = Xn[j].clone()
        for x in X: v = v - ipf(v, x) * x
        nv = float(v.norm())
        if nv > 1e-6: Pdir.append(v / nv)
    Pdir = Pdir[:BK]
    # renormalize Xn (they are orthonormal combos of orthonormal S up to roundoff)
    X = []; AX = []
    for j in range(k):
        nv = float(Xn[j].norm())
        X.append(Xn[j] / nv); AX.append(AXn[j] / nv)
    del R, Wd, S, AS, Xn, AXn
if CKPT:
    np.savez(CKPT, k=len(X), **{f'x{j}': X[j].cpu().numpy() for j in range(len(X))})
    print(f"# checkpoint saved to {CKPT}", flush=True)
# final report
AX = [A(x) for x in X]
lam = [ipf(X[j], AX[j]) for j in range(len(X))]
order = np.argsort(lam)
r = np.load(root + 'noNull_hess_refine_s128_0.npz')
Vf = [torch.tensor(r['V'][j], device=dev) for j in range(3)]
print("=== FINAL (sorted) ===")
for o in order:
    x = X[o]
    rn = float(D(AX[o] - lam[o] * x).norm()) / (float(AX[o].norm()) + abs(lam[o]))
    sTR = sum(ipf(q, x) ** 2 for q in Q_TR)
    ovf = [abs(ipf(x, vf)) for vf in Vf]
    print(f"lam={lam[o]:+.6f} r={rn:.2e} s_TR={sTR:.3f} |<x,Vfile>|=[{ovf[0]:.3f},{ovf[1]:.3f},{ovf[2]:.3f}] |<x,u1>|={abs(ipf(x,u1)):.2e}")
print(f"total time {time.time()-t0:.0f}s")

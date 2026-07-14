# BLIND VERIFIER — exact Rayleigh-Ritz over span{u1, 6 T/R generators, 8 LOBPCG hunt vectors} at N=128.
import os, sys, math, numpy as np, torch
sys.path.insert(0, '/home/udt-admin/udt_mass_codex')
from noNull_energy import grad_noNull
torch.set_default_dtype(torch.float64); dev = 'cuda'
root = '/home/udt-admin/udt_mass_codex/'
d = np.load(root + 'noNull_critical_field_128.npz')
N = int(d['N']); L = float(d['L']); h = float(d['h']); xi = float(d['xi']); kap = float(d['kappa'])
n = torch.tensor(d['n'], device=dev)
msk = torch.zeros(N, N, N, device=dev); msk[2:-2, 2:-2, 2:-2] = 1.0
def P(v): return (v - (v * n).sum(0, keepdim=True) * n) * msk
def ipf(a, b): return float((a * b).sum())
def gE(x): return grad_noNull(x, h, xi, kap)
EPS = 1e-4
def A(v):
    vp = P(v)
    return P((gE(n + EPS * vp) - gE(n - EPS * vp)) / (2 * EPS)) / h**3
xg = torch.linspace(-L, L, N, device=dev)
Xg, Yg, Zg = torch.meshgrid(xg, xg, xg, indexing='ij')
dnc = [(torch.roll(n, -1, a + 1) - torch.roll(n, 1, a + 1)) / (2 * h) for a in range(3)]
u1 = P(torch.stack([-n[1], n[0], torch.zeros_like(n[0])], 0)); u1 = u1 / u1.norm()
gens = [u1] + [P(v) for v in [dnc[0], dnc[1], dnc[2],
        Yg * dnc[2] - Zg * dnc[1], Zg * dnc[0] - Xg * dnc[2], Xg * dnc[1] - Yg * dnc[0]]]
del dnc, Xg, Yg, Zg
ck = np.load('/tmp/claude-1000/-home-udt-admin-udt-mass-codex/918f430f-ba82-47c1-a949-c3464efcc696/scratchpad/hunt_u1_s0.npz')
hunt = [torch.tensor(ck[f'x{j}'], device=dev) for j in range(int(ck['k']))]
S = []
for v in gens + hunt:
    c = P(v)
    for o in S: c = c - ipf(c, o) * o
    for o in S: c = c - ipf(c, o) * o
    nc = float(c.norm())
    if nc > 1e-8: S.append(c / nc)
m = len(S)
print(f"# RR subspace dim = {m} (from 7 sym gens + {len(hunt)} hunt vecs)")
AS = [A(s) for s in S]
G = torch.zeros(m, m, dtype=torch.float64)
for i in range(m):
    for j in range(i, m):
        G[i, j] = ipf(S[i], AS[j]); G[j, i] = G[i, j]
asym = 0.0
for i in range(m):
    for j in range(m):
        asym = max(asym, abs(float(G[i, j] - G[j, i])))
ew, ev = torch.linalg.eigh((G + G.T) / 2)
# per-Ritz-vector: s_TR content and residual
tr_on = []
for q in gens[1:]:
    c = q.clone()
    # orthonormalize TR gens among themselves + vs u1 for s_TR metric
    pass
# build orthonormal TR basis for s_TR metric
QTR = []
for v in gens[1:]:
    c = v - ipf(v, gens[0]) * gens[0]
    for q in QTR: c = c - ipf(c, q) * q
    nc = float(c.norm())
    if nc > 1e-9: QTR.append(c / nc)
print("Ritz values (lam_phys) with s_TR content and true residual:")
for j in range(min(m, 12)):
    v = torch.zeros_like(S[0]); av = torch.zeros_like(S[0])
    for i in range(m):
        c = float(ev[i, j])
        if abs(c) > 1e-14: v = v + c * S[i]; av = av + c * AS[i]
    lam = float(ew[j])
    res = float(P(av - lam * v).norm()) / (float(av.norm()) + abs(lam))
    sTR = sum(ipf(q, v)**2 for q in QTR)
    su1 = ipf(gens[0], v)**2
    print(f"  lam={lam:+.6f}  r={res:.2e}  s_TR={sTR:.3f} s_u1={su1:.3f}")
print(f"max Gram asym = {asym:.2e}")

# BLIND VERIFIER — check 4: FD-step sensitivity at 256^3 (doublet member 0, seed 0)
# + cross-seed subspace agreement s0 vs s1 at all grids.
import sys, math, numpy as np, torch
sys.path.insert(0, '/home/udt-admin/udt_mass_codex')
from noNull_energy import grad_noNull
torch.set_default_dtype(torch.float64); dev = 'cuda'
root = '/home/udt-admin/udt_mass_codex/'

# --- eps sensitivity at 256 ---
d = np.load(root + 'noNull_critical_field.npz')
N = int(d['N']); h = float(d['h']); xi = float(d['xi']); kap = float(d['kappa'])
n = torch.tensor(d['n'], device=dev)
msk = torch.zeros(N, N, N, device=dev); msk[2:-2, 2:-2, 2:-2] = 1.0
def P(v): return (v - (v * n).sum(0, keepdim=True) * n) * msk
def gE(x): return grad_noNull(x, h, xi, kap)
r = np.load(root + 'noNull_hess_refine_s0.npz')
v = torch.tensor(r['V'][0], device=dev)
for eps in [5e-5, 1e-4, 2e-4]:
    vp = P(v)
    Hv = P((gE(n + eps * vp) - gE(n - eps * vp)) / (2 * eps))
    lam = float((v * Hv).sum()) / h**3
    print(f"eps={eps:.0e}: lam_phys(doublet0@256)={lam:.12f}")
del n, v, Hv, vp, msk

# --- cross-seed subspace agreement (numpy, CPU) ---
for tag, f0, f1 in [('128', 'noNull_hess_refine_s128_0.npz', 'noNull_hess_refine_s128_1.npz'),
                    ('192', 'noNull_hess_refine_s192_0.npz', 'noNull_hess_refine_s192_1.npz'),
                    ('256', 'noNull_hess_refine_s0.npz', 'noNull_hess_refine_s1.npz')]:
    a = np.load(root + f0)['V']; b = np.load(root + f1)['V']
    A2 = a[:2].reshape(2, -1); B2 = b[:2].reshape(2, -1)
    M = A2 @ B2.T
    sv = np.linalg.svd(M, compute_uv=False)
    iso = abs(float(a[2].reshape(-1) @ b[2].reshape(-1)))
    print(f"grid {tag}: doublet-subspace principal cosines s0-vs-s1 = {sv}, |<iso_s0,iso_s1>| = {iso:.10f}")
    del a, b, A2, B2

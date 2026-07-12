"""Residual decomposition (Charles correction 2026-07-12): is ||g||_{M^-1}=5.84 at the relaxed carrier
pinned-boundary contamination or a genuine INTERIOR residual? Decompose the tangent free gradient
g_f = P_free P_T grad(E_noNull) by mask width w (zero the outer w layers) for w=2,4,8,12, and by radius.
The TRUE free projection removes exactly the w=2 fixed layers (pin_boundary w=2); wider w probes how much
residual sits in the outer shells. ||g_f||_{M^-1} = ||g_f||_2 / h^{3/2}."""
import sys, numpy as np, torch
sys.path.insert(0, 'hopfion_arc_scripts_2026-07-05')
import fs_hopfion as m
from noNull_energy import grad_noNull
torch.set_default_dtype(torch.float64); dev = 'cuda' if torch.cuda.is_available() else 'cpu'
d = np.load('noNull_critical_field.npz'); n = torch.tensor(d['n'], device=dev)
N = int(d['N']); L = float(d['L']); h = float(d['h']); xi = float(d['xi']); kap = float(d['kappa'])
n = n / n.norm(dim=0, keepdim=True)
def tang(nn, a): return a - (a * nn).sum(0, keepdim=True) * nn
gT = tang(n, grad_noNull(n, h, xi, kap))
mnorm = lambda g: float(g.norm()) / h**1.5

def free_mask(w):
    msk = torch.zeros(N, N, N, device=dev); msk[w:-w, w:-w, w:-w] = 1.0; return msk
print(f"# full tangent gradient: raw={float(gT.norm()):.4e}  ||g||_M-1={mnorm(gT):.4e}", flush=True)
print("# free gradient g_f = P_free(w) g_T  (w = # fixed outer layers):", flush=True)
prev = float((gT * gT).sum())
for w in (2, 4, 8, 12):
    gf = gT * free_mask(w)
    frac_removed = 1 - float((gf * gf).sum()) / float((gT * gT).sum())
    print(f"  w={w:2d}: raw={float(gf.norm()):.4e}  ||g_f||_M-1={mnorm(gf):.4e}  "
          f"(power removed vs full: {frac_removed*100:.1f}%)", flush=True)
# radial shells of the full tangent gradient
x = torch.linspace(-L, L, N, device=dev); X, Y, Z = torch.meshgrid(x, x, x, indexing='ij'); r = torch.sqrt(X**2 + Y**2 + Z**2)
gp = (gT * gT).sum(0); tot = float(gp.sum())
print("# radial distribution of |g_T|^2:", flush=True)
for lo, hi in [(0, 2), (2, 3), (3, 4), (4, 5), (5, 5.5), (5.5, 99)]:
    print(f"  {lo:.1f}<=r<{hi:.1f}: {float(gp[(r>=lo)&(r<hi)].sum())/tot*100:5.1f}%", flush=True)
print(f"# box half-size L={L}; pinned layers w=2 reach r>~{L-2*h:.2f}", flush=True)

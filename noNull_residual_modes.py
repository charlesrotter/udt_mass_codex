"""Decompose the free gradient g_f at the (partially-relaxed) carrier into (a) the approximate symmetry
pseudomodes (translations, spatial rotations, U(1)) and (b) the ORTHOGONAL physical residual. If g_f is
mostly pseudomode drift, the non-criticality is harmless soft-mode mis-positioning (physical Hessian modes
uncontaminated); if it has a large physical-orthogonal part, the field is genuinely non-critical.
Free projection P_free = 2 fixed layers (matches pin_boundary). ||.||_{M^-1} = ||.||/h^{3/2}."""
import sys, numpy as np, torch
sys.path.insert(0, 'hopfion_arc_scripts_2026-07-05')
import fs_hopfion as m
from noNull_energy import grad_noNull
torch.set_default_dtype(torch.float64); dev = 'cuda' if torch.cuda.is_available() else 'cpu'
d = np.load('noNull_critical_field.npz'); n = torch.tensor(d['n'], device=dev)
N = int(d['N']); L = float(d['L']); h = float(d['h']); xi = float(d['xi']); kap = float(d['kap' if 'kap' in d else 'kappa'])
n = n / n.norm(dim=0, keepdim=True)
def tang(nn, a): return a - (a * nn).sum(0, keepdim=True) * nn
FW = 2; fm = torch.zeros(N, N, N, device=dev); fm[FW:-FW, FW:-FW, FW:-FW] = 1.0
def fp(v): return tang(n, v) * fm
mnorm = lambda g: float(g.norm()) / h**1.5
gf = fp(grad_noNull(n, h, xi, kap))
x = torch.linspace(-L, L, N, device=dev); X, Y, Z = torch.meshgrid(x, x, x, indexing='ij')
dc = [(torch.roll(n, -1, a + 1) - torch.roll(n, 1, a + 1)) / (2 * h) for a in range(3)]
modes = {'Tx': dc[0], 'Ty': dc[1], 'Tz': dc[2],
         'Rx': Y * dc[2] - Z * dc[1], 'Ry': Z * dc[0] - X * dc[2], 'Rz': X * dc[1] - Y * dc[0],
         'U1': torch.stack([-n[1], n[0], torch.zeros_like(n[0])], 0)}
cols = [fp(v).reshape(-1) for v in modes.values()]
B = torch.stack(cols, 1); Q, _ = torch.linalg.qr(B)              # orthonormal basis of the pseudomode span
gfv = gf.reshape(-1)
coeffs = Q.T @ gfv; proj = Q @ coeffs
frac = float((proj @ proj) / (gfv @ gfv))
resid = (gfv - proj)
print(f"||g_f||_M-1 = {mnorm(gf):.4e}", flush=True)
print(f"fraction of ||g_f||^2 in the 7 pseudomode span = {frac:.4f}", flush=True)
print(f"  PHYSICAL (orthogonal) residual ||g_f_perp||_M-1 = {float(resid.norm())/h**1.5:.4e}", flush=True)
print("per-mode |<g_f, mode_hat>| (M-1 units, contribution to residual):", flush=True)
for nm, v in modes.items():
    vh = fp(v); vh = vh / (vh.norm() + 1e-30)
    print(f"  {nm}: {abs(float((gf*vh).sum()))/h**1.5:.4e}", flush=True)

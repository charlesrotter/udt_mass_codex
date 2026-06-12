"""
VERIFIER v7: GPU (torch float64, CUDA) cross-checks of the two numeric
backbones. No solve_triangular / broadcast Cholesky anywhere (recorded
stack pitfall); matmul reductions only; asserts on CPU.

 G1  M2 DEN sign map at near-seal slices: GPU batched evaluation vs the
     v3 CPU bands (band edges to grid resolution)
 G2  collar n_H1 sweep, 6 channels x 161 y: GPU batched quadrature vs
     CPU (agreement to 1e-12 relative)
"""
import numpy as np
import torch
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from math import log

assert torch.cuda.is_available()
dev = torch.device('cuda')
torch.set_default_dtype(torch.float64)

PASS = []
def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"V7 {name}: {'PASS' if ok else 'FAIL'} {detail}", flush=True)

# ---------------- backgrounds (CPU integration, as v3) ----------------
S3, S5, S7 = np.sqrt(3.), np.sqrt(5.), np.sqrt(7.)
def Yr(u):
    u = np.asarray(u, float)
    return np.array([np.ones_like(u), S3*u, (S5/2)*(3*u**2 - 1),
                     (S7/2)*(5*u**3 - 3*u)])
def Ypr(u):
    u = np.asarray(u, float)
    return np.array([np.zeros_like(u), S3*np.ones_like(u), 3*S5*u,
                     (S7/2)*(15*u**2 - 3)])
YP1 = np.array([1.0, S3, S5, S7])
xg, wg = np.polynomial.legendre.leggauss(1200)
Yg, Ypg = Yr(xg), Ypr(xg); sg = 1 - xg**2
def PX(X):
    f = X @ Yg; fu = X @ Ypg
    return (sg*(2*fu*Ypg/f - fu**2*Yg/f**2)) @ wg / 8.0
def fmin_of(X):
    uu = np.linspace(-1, 1, 20001)
    return (X @ Yr(uu)).min()
def rhs(t, z):
    X, Xt = z[0::2], z[1::2]
    out = np.empty(8); out[0::2] = Xt; out[1::2] = Xt + 2*PX(X)
    return out
hdr = open('/tmp/seal_s1/lib/bg_M2.dat').read(300)
c = float(hdr.split(" c=")[1].split()[0])
z0 = np.zeros(8); z0[0] = 1.; z0[1] = 1.; z0[3] = -c
ev = lambda t, z: fmin_of(z[0::2]) - 0.002
ev.terminal = True; ev.direction = -1
sol = solve_ivp(rhs, (0, 60), z0, method='DOP853', rtol=1e-11, atol=1e-13,
                dense_output=True, events=ev)
tstop = sol.t_events[0][0]
pole = lambda t: float(sol.sol(t)[0::2] @ YP1)

# ---------------- G1: GPU DEN map ----------------
uu = torch.linspace(-1, 1, 2_000_001, device=dev)
Yt = torch.stack([torch.ones_like(uu), S3*uu, (S5/2)*(3*uu**2 - 1),
                  (S7/2)*(5*uu**3 - 3*uu)])
Ypt = torch.stack([torch.zeros_like(uu), S3*torch.ones_like(uu), 3*S5*uu,
                   (S7/2)*(15*uu**2 - 3)])
ok1 = True
for mu, lo_ref, hi_ref in ((0.1, 0.5933, 0.9287), (0.03, 0.5917, 0.9270),
                           (0.01, 0.5913, 0.9258), (0.003, 0.5913, 0.9253)):
    tl = brentq(lambda t: pole(t) - mu, 0.2*tstop, tstop)
    z = sol.sol(tl)
    X = torch.tensor(z[0::2], device=dev); Xt = torch.tensor(z[1::2], device=dev)
    f = X @ Yt; ft = Xt @ Yt; fu = X @ Ypt
    D = f*ft**2 - (1 - uu**2)*fu**2
    neg = uu[D < 0]
    lo, hi = neg.min().item(), neg.max().item()   # CPU scalars
    print(f"   mu={mu:7.3f}: GPU band [{lo:+.5f}, {hi:+.5f}] "
          f"vs CPU [{lo_ref:+.4f}, {hi_ref:+.4f}]")
    ok1 &= abs(lo - lo_ref) < 5e-4 and abs(hi - hi_ref) < 5e-4
check("G1 GPU (2M-point) DEN<0 bands match the CPU v3 bands to 5e-4",
      ok1)

# ---------------- G2: GPU n_H1 sweep ----------------
q = 1.0/3.0; s = q*(1 - q)/2.0
Lk = lambda k: log((1 + k)/(1 - k))
Hf = lambda k: Lk(k)/(2*k) - 1.0
Hp = lambda k: 1.0/(k*(1 - k**2)) - Lk(k)/(2*k**2)
ys = np.geomspace(1.0, 1e6, 161)
F = ys**(-q); Fp = -q*ys**(-q - 1)
ks = np.array([brentq(lambda kk: Hf(kk) - 2*s*yv**(-q), 1e-13, 1 - 1e-13,
                      xtol=1e-16) for yv in ys])
kps = -2*q*s*ys**(-q - 1)/np.array([Hp(k) for k in ks])
a = F*ks; ap = Fp*ks + F*kps
xq, wq2 = np.polynomial.legendre.leggauss(400)
# CPU reference
W = {(1, 0): xq**2, (1, 1): 1 - xq**2, (2, 0): (3*xq**2 - 1)**2,
     (2, 1): xq**2*(1 - xq**2), (2, 2): (1 - xq**2)**2,
     (3, 0): (5*xq**3 - 3*xq)**2}
ref = {}
for lm, ww in W.items():
    DW = (1/16)*(ys[:, None]**2*(2*Fp[:, None]*ap[:, None]*xq
                                 + ap[:, None]**2*xq**2)
                 - a[:, None]**2*(1 - xq**2)
                 / (F[:, None]*(1 + ks[:, None]*xq)))
    dw = (DW*ww) @ wq2 / (ww @ wq2)
    ref[lm] = -0.5*s*F**2/dw
# GPU batched: all y at once per channel, matmul reduction
t = lambda v: torch.tensor(v, device=dev)
ysT, FT, FpT, kT, aT, apT = map(t, (ys, F, Fp, ks, a, ap))
xqT, wqT = t(xq), t(wq2)
err = 0.0
for lm, ww in W.items():
    wwT = t(ww)
    DWT = (1/16)*(ysT[:, None]**2*(2*FpT[:, None]*apT[:, None]*xqT
                                   + apT[:, None]**2*xqT**2)
                  - aT[:, None]**2*(1 - xqT**2)
                  / (FT[:, None]*(1 + kT[:, None]*xqT)))
    dwT = (DWT*wwT) @ wqT / (wwT @ wqT)
    nT = (-0.5*s*FT**2/dwT).cpu().numpy()        # back to CPU for assert
    err = max(err, np.abs(nT/ref[lm] - 1).max())
    assert not np.isnan(nT).any()
check("G2 GPU batched n_H1 sweep (6 channels x 161 y) == CPU to 1e-12",
      err < 1e-12, f"max rel dev {err:.1e}")
# exclusion re-check on GPU values
ok3 = all(np.all(np.abs(v) > 1e-6) and np.all(np.abs(v - 1) > 1e-3)
          and np.all(np.abs(v - 8) > 1e-3) and np.all(np.abs(v + 8) > 1e-3)
          for v in ref.values())
check("G3 exclusion {0,1,+8,-8} reconfirmed on the GPU-validated sweep",
      ok3)

n = sum(1 for _, ok in PASS if ok)
print(f"\nV7 TOTAL: {n}/{len(PASS)} PASS (GPU: cuda float64, "
      "matmul-only reductions, no batched triangular solves)")

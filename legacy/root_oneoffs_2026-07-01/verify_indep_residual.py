#!/usr/bin/env python3
"""
INDEPENDENT verifier part 3: numerical residuals on the REAL #52 soliton with my OWN
closed-form Einstein engine (independent of whole_metric_3d_core.py's FD pipeline).

Driver: Claude (Opus 4.8, 1M) blind verifier. 2026-06-15. DATA-BLIND.

Method: closed-form G^mu_nu for B=1/A metric depends only on phi, phi', phi''.
Closed-form stress depends on phi, Theta, Theta'.  Generate them with sympy, lambdify,
evaluate on the committed #52 profile (Theta(r),phi(r) from complete_metric_batched).
This shares NOTHING with the committed FD Einstein engine -- it is a fully independent
analytic-G evaluation.  Check: G^t_t-k8 T^t_t ~0; G^r_r-k8 T^r_r O(1) in body, ~0
exterior; convergence with grid resolution; check a couple of (p,kappa8) variations.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, numpy as np, sympy as sp, torch
import complete_metric_batched as cm
torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"

# ---- closed-form G^mu_nu (B=1/A) and stress, as lambdified python ----
r = sp.symbols('r', positive=True)
xi, kap, k8 = sp.symbols('xi kappa kappa8', positive=True)
phi, phip, phipp = sp.symbols('phi phip phipp', real=True)
Th, Thp = sp.symbols('Theta Thp', real=True)

# G^mu_nu for ds^2 = -e^{-2phi}dt^2 + e^{2phi}dr^2 + r^2 dOmega^2, expressed via phi,phi',phi''.
# Derive from scratch here (independent), substituting derivatives as symbols.
phif = sp.Function('phi')(r)
g = sp.diag(-sp.exp(-2*phif), sp.exp(2*phif), r**2, r**2*sp.sin(sp.Symbol('theta'))**2)
gi = g.inv()
thsym = sp.Symbol('theta')
coords = [sp.Symbol('t'), r, thsym, sp.Symbol('psi')]
n = 4
Gam = [[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
for a in range(n):
    for b in range(n):
        for c in range(n):
            s = sum(gi[a, d]*(sp.diff(g[d, b], coords[c])+sp.diff(g[d, c], coords[b])
                    - sp.diff(g[b, c], coords[d])) for d in range(n))
            Gam[a][b][c] = sp.simplify(s/2)
def riem(a, b, c, d):
    s = sp.diff(Gam[a][b][d], coords[c]) - sp.diff(Gam[a][b][c], coords[d])
    for e in range(n):
        s += Gam[a][c][e]*Gam[e][b][d] - Gam[a][d][e]*Gam[e][b][c]
    return s
Ric = sp.Matrix(n, n, lambda b, d: sp.simplify(sum(riem(a, b, a, d) for a in range(n))))
Rs = sp.simplify(sum(gi[i, j]*Ric[i, j] for i in range(n) for j in range(n)))
Gdn = sp.Matrix(n, n, lambda i, j: sp.simplify(Ric[i, j]-sp.Rational(1, 2)*g[i, j]*Rs))
Gmix = sp.simplify(gi*Gdn)
# substitute phi'->phip, phi''->phipp, phi->phi
subs = {sp.Derivative(phif, r, r): phipp, sp.Derivative(phif, r): phip, phif: phi}
Gtt = sp.simplify(Gmix[0, 0].subs(subs))
Grr = sp.simplify(Gmix[1, 1].subs(subs))
Gthth = sp.simplify(Gmix[2, 2].subs(subs))
print("closed-form G^t_t   =", Gtt)
print("closed-form G^r_r   =", Grr)
print("closed-form G^th_th =", Gthth)

# stress (committed, = unit S^3 hedgehog Hilbert stress, verified part 2)
X = sp.exp(-2*phi)*Thp**2; Y = sp.sin(Th)**2/r**2
rho = (xi/2)*(X+2*Y)+(kap/2)*(2*X*Y+Y**2)
prr = (xi/2)*(X-2*Y)+(kap/2)*(2*X*Y-Y**2)
# T^theta_theta for the unit S^3 hedgehog (mixed). Derive via Hilbert quickly:
# p_theta = (xi/2)(X) + (kap/2)(2XY)  (the standard hedgehog: T^th = T^ps = p_t).
# We instead lambdify the canonical committed forms and add p_theta from C-canon (deg1: see below).
fG = sp.lambdify((r, phi, phip, phipp), [Gtt, Grr, Gthth], 'numpy')
fT = sp.lambdify((r, phi, Th, Thp, xi, kap), [-rho, prr], 'numpy')  # T^t_t=-rho, T^r_r=p_r

# ---- the committed #52 profile ----
mat_xi = mat_kap = 1.0
rc = 0.05; SPAN = 14.0; ri = rc + SPAN
P_DEPTH = 0.4; KAP8 = 0.05

def run(N, p=P_DEPTH, kap8=KAP8, label=""):
    rg = torch.linspace(rc, ri, N, device=DEV).unsqueeze(0)
    o = cm.selfconsistent_batched(rg, mat_xi, mat_kap, p=p, kap8=kap8,
                                  iters=160, relax=0.4, tol=1e-11)
    rr = o['r'][0].cpu().numpy(); Thv = o['Th'][0].cpu().numpy(); phiv = o['phi'][0].cpu().numpy()
    # derivatives by central FD (independent of the committed grad_central; same idea, my own)
    Thp = np.gradient(Thv, rr)
    phip = np.gradient(phiv, rr)
    phipp = np.gradient(phip, rr)
    Gt, Gr, Gth = fG(rr, phiv, phip, phipp)
    Ttt, Trr = fT(rr, phiv, Thv, Thp, mat_xi, mat_kap)
    res_tt = Gt - kap8*Ttt
    res_rr = Gr - kap8*Trr
    # interior mask (strip FD edges)
    m = slice(8, -8)
    # body vs exterior by Theta'
    body = np.abs(Thp) > 1e-3
    ext = ~body
    bi = body[m]; ei = ext[m]
    rr_m = rr[m]; rtt = res_tt[m]; rrr = res_rr[m]
    out = dict(N=N,
               max_res_tt=np.max(np.abs(rtt)),
               max_res_rr=np.max(np.abs(rrr)),
               body_res_rr_max=np.max(np.abs(rrr[bi])) if bi.any() else float('nan'),
               body_res_rr_mean=np.mean(np.abs(rrr[bi])) if bi.any() else float('nan'),
               ext_res_rr_max=np.max(np.abs(rrr[ei])) if ei.any() else float('nan'))
    print(f"\n  {label} N={N} p={p} k8={kap8}:")
    print(f"    max|G^t_t - k8 T^t_t| (interior)   = {out['max_res_tt']:.3e}")
    print(f"    max|G^r_r - k8 T^r_r| (interior)   = {out['max_res_rr']:.3e}")
    print(f"    (r,r) residual in BODY  (Theta'!=0): max={out['body_res_rr_max']:.3e} mean={out['body_res_rr_mean']:.3e}")
    print(f"    (r,r) residual in EXTERIOR(Theta'=0): max={out['ext_res_rr_max']:.3e}")
    return out

print("\n" + "="*78)
print("TASK 2: independent numerical residuals on the committed #52 soliton")
print("="*78)
res = [run(N, label="resolution sweep") for N in [600, 900, 1400, 2200]]
print("\n  CONVERGENCE of (r,r) BODY residual with N:")
for o in res:
    print(f"    N={o['N']:5d}: body max|G^r_r-k8 T^r_r| = {o['body_res_rr_max']:.4e}  "
          f"(t,t) max = {o['max_res_tt']:.3e}")
print("  -> if body (r,r) residual does NOT shrink to 0 with N => genuine inconsistency.")

print("\n" + "="*78)
print("Robustness: vary (p, kappa8)")
print("="*78)
for (p, k8v) in [(0.3, 0.05), (0.4, 0.03), (0.5, 0.05)]:
    run(1400, p=p, kap8=k8v, label="variation")

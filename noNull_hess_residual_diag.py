"""Residual diagnostic on the saved 256^3 physical Ritz vectors (Charles directive 2026-07-13).

Distinguishes GENUINE non-convergence (large invariant-subspace residual eta_c) from benign
internal near-degenerate mixing (small eta_c while individual labels rotate). Also sweeps the
FD-HVP step epsilon to exclude finite-difference noise as the residual source.

Uses the EXACT operator from noNull_resolve.py (same grad_noNull, freeproj_at, U(1) deflation,
central-FD HVP). Reports RAW backward error only; no preconditioned-residual substitution.

  V = [v5, v6, v7]  (physical modes, s_TR<0.5): 0.252 doublet (v5,v6) + isolated 0.323 (v7)
  R_c = H V - V (V^T H V)        (invariant-subspace residual, orthonormal V)
  eta_c = ||R_c||_F / (||H V||_F + ||V (V^T H V)||_F)
  raw r_j = ||H v - lam v|| / (||H v|| + |lam|)     [same as the run gate]

Env: RITZ (default noNull_hess_ritz_bw2_s0.npz), CRIT (default noNull_critical_field.npz), HBW=2.
"""
import os, gc, numpy as np, torch
from noNull_energy import energy_noNull, grad_noNull
torch.set_default_dtype(torch.float64); dev = 'cuda' if torch.cuda.is_available() else 'cpu'

RITZ = os.environ.get('RITZ', 'noNull_hess_ritz_bw2_s0.npz')
CRIT = os.environ.get('CRIT', 'noNull_critical_field.npz')
HBW  = int(os.environ.get('HESS_BW', '2'))

dc = np.load(CRIT)
N, L, h, xi, kap = int(dc['N']), float(dc['L']), float(dc['h']), float(dc['xi']), float(dc['kappa'])
n = torch.tensor(dc['n'], device=dev); n = n / n.norm(dim=0, keepdim=True)
print(f"# CRIT={CRIT} N={N} L={L} h={h:.6g} xi={xi} kap={kap}")

# --- exact operator pieces (mirror noNull_resolve.py hess block) ---
def gE(nn): return grad_noNull(nn, h, xi, kap)
def free_mask(w):
    msk = torch.zeros(N, N, N, device=dev); msk[w:-w, w:-w, w:-w] = 1.0; return msk
_FM = free_mask(HBW)
def freeproj_at(nn, v, w=HBW):
    fm = _FM if w == HBW else free_mask(w)
    return (v - (v * nn).sum(0, keepdim=True) * nn) * fm
def ip(a, b): return float((a * b).sum())
u1 = freeproj_at(n, torch.stack([-n[1], n[0], torch.zeros_like(n[0])], 0), HBW)
u1 = u1 / (u1.norm() + 1e-30)
def defl(v): v = freeproj_at(n, v, HBW); return v - ip(v, u1) * u1
def hvp(v, eps): v = defl(v); return defl((gE(n + eps * v) - gE(n - eps * v)) / (2 * eps))

def mgs(cols):                                   # deflation-aware orthonormalization
    out = []
    for c in cols:
        c = defl(c)
        for o in out: c = c - ip(c, o) * o
        nc = float(c.norm())
        if nc > 1e-12: out.append(c / nc)
    return out

def eta_c(Vlist, eps):                            # invariant-subspace residual on orthonormal Vlist
    Vo = mgs(Vlist); k = len(Vo)
    HV = [hvp(v, eps) for v in Vo]
    M = [[ip(Vo[i], HV[j]) for j in range(k)] for i in range(k)]   # V^T H V (Rayleigh, k x k)
    proj = [sum(M[i][j] * Vo[i] for i in range(k)) for j in range(k)]  # (V M)_j = sum_i V_i M_ij
    Rc = [HV[j] - proj[j] for j in range(k)]
    nRc = float(sum(float((r * r).sum()) for r in Rc) ** 0.5)
    nHV = float(sum(float((r * r).sum()) for r in HV) ** 0.5)
    nPr = float(sum(float((r * r).sum()) for r in proj) ** 0.5)
    lam = [M[j][j] / h**3 for j in range(k)]      # diagonal Rayleigh quotients (phys-scaled)
    del HV, proj, Rc; gc.collect(); torch.cuda.empty_cache()
    return nRc / (nHV + nPr + 1e-30), lam

def raw_rj(v, eps):                               # individual backward error (the run gate)
    Hv = hvp(v, eps); lam = ip(v, Hv)
    res = float(defl(Hv - lam * v).norm())
    r = res / (float(Hv.norm()) + abs(lam) + 1e-30)
    lp = lam / h**3
    del Hv; gc.collect(); torch.cuda.empty_cache()
    return r, lp

# --- load physical vectors v5,v6,v7 ---
dr = np.load(RITZ)
Vall = dr['V']; sTR = dr['s_TR']; lam_saved = dr['lam_phys']
phys_idx = [j for j in range(Vall.shape[0]) if sTR[j] < 0.5]
print(f"# RITZ={RITZ} physical indices (s_TR<0.5): {phys_idx}  lam_saved={[round(float(lam_saved[j]),4) for j in phys_idx]}")
v = {j: defl(torch.tensor(Vall[j], device=dev)) for j in phys_idx}
for j in v: v[j] = v[j] / v[j].norm()
del Vall; gc.collect()

# identify doublet (near-equal lam) vs isolated -- by saved lam
lams = {j: float(lam_saved[j]) for j in phys_idx}
srt = sorted(phys_idx, key=lambda j: lams[j])
doublet = srt[:2]; isolated = srt[2:]      # two lowest ~equal = doublet; rest isolated
print(f"# doublet (0.252 pair) = idx {doublet}; isolated = idx {isolated}\n")

for eps in (2e-4, 1e-4, 5e-5):
    print(f"=== eps = {eps:g} ===")
    etaD, lamD = eta_c([v[j] for j in doublet], eps)
    print(f"  doublet  eta_c = {etaD:.3e}   (lam {[round(x,4) for x in lamD]})")
    etaF, lamF = eta_c([v[j] for j in phys_idx], eps)
    print(f"  full V3  eta_c = {etaF:.3e}   (lam {[round(x,4) for x in lamF]})")
    for j in phys_idx:
        r, lp = raw_rj(v[j], eps)
        tag = 'doublet' if j in doublet else 'ISOLATED'
        print(f"    v{j} [{tag}] raw r_j = {r:.3e}  lam = {lp:+.4f}")
    print()
print("# eta_c small + raw r_j large -> benign internal mixing among {v5,v6,v7}.")
print("# eta_c ALSO large -> genuine leakage OUTSIDE the physical subspace (stiff/other) = real non-convergence.")
print("# r_j nearly eps-independent -> not FD noise.")

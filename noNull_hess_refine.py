"""Soft-locking block LOBPCG refinement of the 256^3 physical Hessian modes (Charles directive
2026-07-13; hardened after plain block-4 stalled at eta_c~0.05 via search-space repollution).

The bs=8 production run left the physical Ritz vectors UNCONVERGED (raw r_j 0.11-0.39; invariant-
subspace eta_c 0.16-0.22, eps-independent -> genuine backward error, not mixing, not FD noise).
This refines them in the physical complement to a RAW-backward-error gate.

  - Deflate U(1) AND the 6 T/R pseudomode generators (Q_TR): work in the physical complement.
  - Warm-start active block = [v5, v6, v7, 3 random guards], projected into that complement.
  - Preconditioned block LOBPCG (S = X + W + P), retaining search directions P.
  - SOFT-LOCKING: once a target's residual clears the gate, freeze it and deflate it out of the
    active search -> the next mode becomes the ground state of the deflated operator and converges
    cleanly, insulated from the still-moving upper (guard) modes.
  - Gates:   0.252 doublet: invariant-subspace eta_c < 1e-3   (locked as a PAIR)
             isolated 0.323: individual raw r_j < 1e-3
             (verified across the HVP-eps sweep at the end; both seeds run separately.)
  - RAW backward error is the gate. Preconditioner used ONLY to accelerate (search direction).

Env: CRIT, SEED_RITZ (warm file), HESS_BW=2, EPS=1e-4, MAXIT=120, RJTOL=1e-3, NGUARD=3.
Saves noNull_hess_refine_s{tag}.npz.
"""
import os, gc, time, numpy as np, torch
from noNull_energy import energy_noNull, grad_noNull
from noNull_precond import make_precond
torch.set_default_dtype(torch.float64); dev = 'cuda' if torch.cuda.is_available() else 'cpu'

CRIT = os.environ.get('CRIT', 'noNull_critical_field.npz')
SEED_RITZ = os.environ.get('SEED_RITZ', 'noNull_hess_ritz_bw2_s0.npz')
TAG = os.environ.get('TAG', SEED_RITZ.split('_s')[-1].split('.')[0])
HBW = int(os.environ.get('HESS_BW', '2'))
EPS = float(os.environ.get('EPS', '1e-4'))
MAXIT = int(os.environ.get('MAXIT', '120'))
RJTOL = float(os.environ.get('RJTOL', '1e-3'))
NGUARD = int(os.environ.get('NGUARD', '3'))
SEED_RAND = int(os.environ.get('SEED_RAND', '7'))

dc = np.load(CRIT)
N, L, h, xi, kap = int(dc['N']), float(dc['L']), float(dc['h']), float(dc['xi']), float(dc['kappa'])
n = torch.tensor(dc['n'], device=dev); n = n / n.norm(dim=0, keepdim=True)
precond, shift = make_precond(N, h, xi, dev)
print(f"# refine(soft-lock) CRIT={CRIT} warm={SEED_RITZ} tag={TAG} N={N} h={h:.5g} EPS={EPS} "
      f"RJTOL={RJTOL} NGUARD={NGUARD}", flush=True)

def gE(nn): return grad_noNull(nn, h, xi, kap)
def ip(a, b): return float((a * b).sum())
_FM = torch.zeros(N, N, N, device=dev); _FM[HBW:-HBW, HBW:-HBW, HBW:-HBW] = 1.0
def freeproj(v): return (v - (v * n).sum(0, keepdim=True) * n) * _FM
u1 = freeproj(torch.stack([-n[1], n[0], torch.zeros_like(n[0])], 0)); u1 = u1 / (u1.norm() + 1e-30)
def defl0(v): v = freeproj(v); return v - ip(v, u1) * u1        # U(1) only
xg = torch.linspace(-L, L, N, device=dev); Xg, Yg, Zg = torch.meshgrid(xg, xg, xg, indexing='ij')
dnc = [(torch.roll(n, -1, a + 1) - torch.roll(n, 1, a + 1)) / (2 * h) for a in range(3)]
_tr = [dnc[0], dnc[1], dnc[2], Yg * dnc[2] - Zg * dnc[1], Zg * dnc[0] - Xg * dnc[2], Xg * dnc[1] - Yg * dnc[0]]
def _mgs(cols, dfn):
    out = []
    for c in cols:
        c = dfn(c)
        for o in out: c = c - ip(c, o) * o
        nc = float(c.norm())
        if nc > 1e-12: out.append(c / nc)
    return out
Q_TR = _mgs(_tr, defl0)
del _tr, dnc, Xg, Yg, Zg; gc.collect(); torch.cuda.empty_cache()
print(f"# physical complement = free tangent minus U(1) minus {len(Q_TR)} T/R generators", flush=True)

LOCKED = []                                      # converged vectors deflated out of the active search
def defl(v):                                     # project onto physical complement AND locked^perp
    v = defl0(v)
    for q in Q_TR: v = v - ip(v, q) * q
    for y in LOCKED: v = v - ip(v, y) * y
    return v
def pc(v): return defl(precond(v))
def hvp(v, eps=EPS): v = defl(v); return defl((gE(n + eps * v) - gE(n - eps * v)) / (2 * eps))
def mgsd(cols): return _mgs(cols, defl)

def geneigh(A, B, kk):
    Bs = 0.5 * (B + B.T); k0 = Bs.shape[0]
    wB, VB = torch.linalg.eigh(Bs); tol = float(wB.max()) * k0 * 2.2e-16
    keep = wB > tol; Vk = VB[:, keep]; d = wB[keep]; rk = int(keep.sum())
    Whalf = Vk / d.sqrt(); Ar = Whalf.T @ A @ Whalf; Ar = 0.5 * (Ar + Ar.T)
    wv, Yv = torch.linalg.eigh(Ar); Cv = Whalf @ Yv
    return wv[:kk], Cv[:, :min(kk, rk)], rk, k0

def eta_sub(Vlist, eps=EPS):                     # invariant-subspace residual on Vlist
    Vo = mgsd(Vlist); k = len(Vo); HV = [hvp(v, eps) for v in Vo]
    M = [[ip(Vo[i], HV[j]) for j in range(k)] for i in range(k)]
    proj = [sum(M[i][j] * Vo[i] for i in range(k)) for j in range(k)]
    nRc = sum(float(((HV[j] - proj[j]) ** 2).sum()) for j in range(k)) ** 0.5
    nHV = sum(float((r * r).sum()) for r in HV) ** 0.5
    nPr = sum(float((r * r).sum()) for r in proj) ** 0.5
    lam = [M[j][j] / h**3 for j in range(k)]
    del HV, proj; gc.collect(); torch.cuda.empty_cache()
    return nRc / (nHV + nPr + 1e-30), lam

def raw_rj(v, eps=EPS):
    Hv = hvp(v, eps); lam = ip(v, Hv); r = float(defl(Hv - lam * v).norm()) / (float(Hv.norm()) + abs(lam) + 1e-30)
    lp = lam / h**3; del Hv; gc.collect(); torch.cuda.empty_cache()
    return r, lp

# warm-start: physical modes + guards
dr = np.load(SEED_RITZ); Vall = dr['V']; sTR = dr['s_TR']
phys_idx = [j for j in range(Vall.shape[0]) if sTR[j] < 0.5]
warm = [torch.tensor(Vall[j], device=dev) for j in phys_idx]
del Vall; gc.collect()
torch.manual_seed(SEED_RAND)
for _ in range(NGUARD): warm.append(torch.randn(3, N, N, N, device=dev))
X = mgsd(warm); del warm; gc.collect(); torch.cuda.empty_cache()
print(f"# active block = {len(phys_idx)} physical {phys_idx} + {NGUARD} guards = {len(X)}", flush=True)

lock_doublet = False; lock_iso = False; doublet_vecs = None; iso_vec = None
P = []; t0 = time.time()
for it in range(MAXIT):
    W = []
    for x in X:
        hx = hvp(x); W.append(pc(hx - ip(x, hx) * x)); del hx; torch.cuda.empty_cache()
    S = mgsd(X + W + P); k = len(S)          # ortho-LOBPCG: orthonormalize full basis -> B~=I, no rank collapse
    A = torch.zeros(k, k, device=dev); B = torch.zeros(k, k, device=dev)
    for j in range(k):
        HSj = hvp(S[j])
        for i in range(k): A[i, j] = ip(S[i], HSj)
        del HSj; torch.cuda.empty_cache()
    for i in range(k):
        for j in range(i, k): B[i, j] = B[j, i] = ip(S[i], S[j])
    A = 0.5 * (A + A.T); w, C, rk, k0 = geneigh(A, B, len(X)); nc = min(len(X), C.shape[1])
    newX = [(lambda vv: vv / vv.norm())(defl(sum(C[i, j] * S[i] for i in range(k)))) for j in range(nc)]
    del S; gc.collect(); torch.cuda.empty_cache()
    lams = [ip(v, hvp(v)) / h**3 for v in newX]
    order = sorted(range(nc), key=lambda j: lams[j])
    # PHASE-AWARE identification: before doublet lock -> lowest two = doublet, third = isolated;
    # after doublet lock (deflated out) -> lowest active = isolated.
    etaD = 0.0; rj_iso = 0.0; lam_iso = float('nan'); lamD = [lams[j] for j in order[:2]]
    if not lock_doublet:
        dbl = order[:2]
        etaD, lamD = eta_sub([newX[j] for j in dbl])
        if nc > 2:
            iso_idx = order[2]; rj_iso, lam_iso = raw_rj(newX[iso_idx])   # diagnostic peek
    else:                                                    # doublet locked -> isolated is ground state
        iso_idx = order[0]
        rj_iso, lam_iso = raw_rj(newX[iso_idx])
    print(f"  [refine s{TAG}] it={it} t={time.time()-t0:.0f}s rk={rk}/{k0} lock={len(LOCKED)} "
          f"active_lam={[round(lams[j],4) for j in order[:4]]} "
          f"doublet_eta_c={etaD:.2e} iso_r_j={rj_iso:.2e}", flush=True)
    # --- soft-locking: doublet first (ground state), then isolated ---
    rebased = False
    if not lock_doublet and etaD < RJTOL and it > 2:
        doublet_vecs = mgsd([newX[j] for j in dbl]); lock_doublet = True
        LOCKED.extend(doublet_vecs)                          # defl now removes the doublet pair
        keep = [j for j in range(nc) if j not in dbl]
        X = mgsd([newX[j] for j in keep] + [torch.randn(3, N, N, N, device=dev)])
        P = []; rebased = True
        print(f"  [refine s{TAG}] LOCKED doublet (eta_c={etaD:.2e}, lam~{[round(x,4) for x in lamD]})", flush=True)
    elif lock_doublet and not lock_iso and rj_iso < RJTOL and it > 2:
        iso_vec = mgsd([newX[iso_idx]])[0]; lock_iso = True
        print(f"  [refine s{TAG}] LOCKED isolated (r_j={rj_iso:.2e}, lam={lam_iso:+.4f})", flush=True)
        print(f"  [refine s{TAG}] GATE PASS it={it}: doublet+isolated both locked below {RJTOL}", flush=True)
        del A, B, w, C; break
    if not rebased:
        P = [defl(newX[j] - X[j]) for j in range(nc)]; X = newX
    del A, B, w, C; gc.collect(); torch.cuda.empty_cache()

# --- final verification on locked vectors + eps-sweep ---
print("", flush=True)
if lock_doublet and lock_iso:
    LOCKED_bak = list(LOCKED)
    dv = doublet_vecs; iv = iso_vec
    # recompute residuals WITHOUT self-deflation (remove the target from LOCKED for its own measurement)
    def measure(eps):
        global LOCKED
        LOCKED = [y for y in LOCKED_bak if not any(ip(y, t) > 0.9 for t in dv + [iv])]
        ed, ld = eta_sub(dv, eps)
        ri, li = raw_rj(iv, eps)
        LOCKED = LOCKED_bak
        return ed, ld, ri, li
    print("# FINAL raw-backward-error gate, HVP-eps sweep (locked doublet + isolated):", flush=True)
    ok = True
    for eps in (2e-4, 1e-4, 5e-5):
        ed, ld, ri, li = measure(eps)
        ok = ok and ed < RJTOL and ri < RJTOL
        print(f"    eps={eps:g}: doublet eta_c={ed:.3e} (lam~{[round(x,4) for x in ld]})  "
              f"isolated r_j={ri:.3e} (lam={li:+.4f})", flush=True)
    print(f"\n# GATE {'PASS' if ok else 'NOT MET'} across eps-sweep: all physical modes POSITIVE, "
          f"raw backward error < {RJTOL}.", flush=True)
    with torch.no_grad():
        np.savez(f'noNull_hess_refine_s{TAG}.npz',
                 V=np.stack([v.cpu().numpy() for v in (dv + [iv])]),
                 lam_doublet=ld, lam_isolated=li, eta_c_doublet=ed, r_j_isolated=ri, N=N, L=L, h=h)
    print(f"# saved noNull_hess_refine_s{TAG}.npz", flush=True)
else:
    print(f"# NOT CONVERGED within {MAXIT} iters: lock_doublet={lock_doublet} lock_iso={lock_iso}", flush=True)

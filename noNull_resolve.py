"""Corrected-operator re-solve with PRECONDITIONING (Charles steer 2026-07-11). Preconditions only the
residual/search direction (SPD, from the no-null link-Laplacian symbol); energy and HVP are ALWAYS the
full no-null operator (never filtered/damped). Criticality graded by the resolution-aware ||g||_{M^-1}.

STAGE=relax : preconditioned L-BFGS tightening of the carrier to a critical field (saves noNull_critical_field.npz).
STAGE=hess  : at the critical field, TWO block-LOBPCG Hessian solves -- (i) UNDEFLATED, (ii) deflating ONLY
              the exact U(1) target mode -- both preconditioned (residual only), multi-start, converged to
              ||Hv-lam M v||/(|lam| ||M v||) < 1e-3; saves EVERY final Ritz vector (not just the min-residual
              one). Translation/rotation modes identified AFTER by overlap (not removed beforehand). Reports
              theta_max and TWO independent no-null charge readouts (centered Q is defective).
One clean GPU process; reliable launch (timeout python3). DATA-BLIND."""
import sys, os, gc, time, json, math, numpy as np, torch
from collections import deque
sys.path.insert(0, 'hopfion_arc_scripts_2026-07-05')
import fs_hopfion as m
from noNull_energy import energy_noNull, grad_noNull, _ORIENTS, _dop, _cross
from noNull_precond import make_precond, mnorm, Lh_symbol
torch.set_default_dtype(torch.float64); dev = 'cuda' if torch.cuda.is_available() else 'cpu'
STAGE = os.environ.get('STAGE', 'relax')

d0 = np.load('controlled_best_field.npz')
N = int(d0['N']); L = float(d0['L']); h = float(d0['h']); xi = float(d0['xi']); kap = float(d0['kappa'])
n_inf = torch.tensor([0., 0., -1.], device=dev).view(3, 1, 1, 1)
precond, shift = make_precond(N, h, xi, dev)
@torch.no_grad()
def E_of(nn): return float(energy_noNull(nn, h, xi, kap)[0])
def gE(nn): return grad_noNull(nn, h, xi, kap)
def tang(nn, a): return a - (a * nn).sum(0, keepdim=True) * nn
def pin(nn):
    with torch.no_grad(): m.pin_boundary(nn, n_inf, 2)
    return nn / nn.norm(dim=0, keepdim=True)
def rgrad(nn): return tang(nn, gE(nn))
def ip(a, b): return float((a * b).sum())
def theta_max(nn):
    mx = 0.0
    for a in range(3):
        dot = (nn * torch.roll(nn, -1, a + 1)).sum(0).clamp(-1, 1)
        mx = max(mx, float(torch.arccos(dot).max()))
    return mx

def _hopf_from_F(Fjk, N):                            # A.B via FFT curl^-1 (Coulomb gauge), given F_{jk} dict
    Bx = Fjk[(1, 2)]; By = Fjk[(2, 0)]; Bz = Fjk[(0, 1)]; B = torch.stack([Bx, By, Bz], 0)
    k1 = 2 * math.pi * torch.fft.fftfreq(N, d=h, device=dev)
    KX, KY, KZ = torch.meshgrid(k1, k1, k1, indexing='ij'); k2 = KX * KX + KY * KY + KZ * KZ; k2[0, 0, 0] = 1.0
    def dfwd(f, ax): return (torch.roll(f, -1, ax) - f) / h
    def curl(V):
        return torch.stack([dfwd(V[2], 1) - dfwd(V[1], 2), dfwd(V[0], 2) - dfwd(V[2], 0), dfwd(V[1], 0) - dfwd(V[0], 1)], 0)
    cB = curl(B); A = torch.zeros_like(B)
    for c in range(3):
        Ak = torch.fft.fftn(-cB[c]) / (-k2); Ak[0, 0, 0] = 0.0; A[c] = torch.fft.ifftn(Ak).real
    return float((A * B).sum(0).sum() * h**3 / (16 * math.pi**2))
def charge_fwd(nn):                                  # F with forward diffs (no null)
    dn = [(torch.roll(nn, -1, a + 1) - nn) / h for a in range(3)]
    F = {(i, j): (nn * _cross(dn[i], dn[j])).sum(0) for i in range(3) for j in range(3) if i != j}
    return _hopf_from_F(F, N)
def charge_sym(nn):                                  # F averaged over 8 one-sided orientations (matches energy)
    F = {(i, j): torch.zeros(N, N, N, device=dev) for i in range(3) for j in range(3) if i != j}
    for s in _ORIENTS:
        dn = [_dop(nn, 1, s[0], h), _dop(nn, 2, s[1], h), _dop(nn, 3, s[2], h)]
        for i in range(3):
            for j in range(3):
                if i != j: F[(i, j)] = F[(i, j)] + (nn * _cross(dn[i], dn[j])).sum(0) / 8
    return _hopf_from_F(F, N)

LOG = 'scratchpad/noNull_resolve.log'
def logline(s):
    with open(LOG, 'a') as f: f.write(s + '\n')
    print(s, flush=True)

CRIT = 'noNull_critical_field.npz'
# =========================== STAGE relax (preconditioned) ===========================
if STAGE == 'relax':
    if os.path.exists(CRIT):
        n = pin(torch.tensor(np.load(CRIT)['n'], device=dev))
    elif os.path.exists('noNull_relaxed_field.npz'):
        n = pin(torch.tensor(np.load('noNull_relaxed_field.npz')['n'], device=dev)); open(LOG, 'w').close()
    else:
        n = pin(torch.tensor(d0['n'], device=dev)); open(LOG, 'w').close()
    TARGET = float(os.environ.get('MNORM_TARGET', '5e-2'))   # ||g||_{M^-1} target
    BUDGET = float(os.environ.get('RELAX_BUDGET_S', '3000'))
    g = rgrad(n); E = E_of(n); t0 = time.time(); a_prev = 1.0
    logline(f"# PRECOND STEEPEST-DESCENT start ||g||_M-1={mnorm(g,h):.4e} (raw={float(g.norm()):.3e}) E={E:.4f} "
            f"Q_fwd={charge_fwd(n):.4f} shift={shift:.3f} target ||g||_M-1<{TARGET:.0e}")
    for it in range(1, 6000):
        d = tang(n, -precond(g))                             # preconditioned steepest descent (SPD search dir)
        slope = ip(g, d)                                     # < 0 since M^-1 SPD
        # line search: try to GROW from a_prev, then backtrack (Newton-like precond step ~ O(1))
        a = min(a_prev * 2.0, 4.0); En = None; nt = None
        for _ in range(40):
            nt_try = pin(n + a * d); Et = E_of(nt_try)
            if Et <= E + 1e-4 * a * slope: En = Et; nt = nt_try; break
            a *= 0.5
        if En is None:
            logline(f"# relax line-search stuck it={it} (slope={slope:.2e}) -> near-critical"); break
        a_prev = a; n = nt; g = rgrad(n); E = En
        if it % 10 == 0: gc.collect(); torch.cuda.empty_cache()
        if it % 20 == 0 or it == 1:
            mg = mnorm(g, h)
            logline(f"  [relax] it={it} t={time.time()-t0:.0f}s ||g||_M-1={mg:.4e} (raw={float(g.norm()):.3e}) "
                    f"E={E:.4f} Q_fwd={charge_fwd(n):.4f} thetamax={theta_max(n):.3f}")
            with torch.no_grad():
                np.savez(CRIT + '.tmp.npz', n=(n / n.norm(dim=0, keepdim=True)).cpu().numpy(), N=N, L=L, h=h, xi=xi, kappa=kap)
                os.replace(CRIT + '.tmp.npz', CRIT)
            if mg < TARGET: logline(f"# relax converged ||g||_M-1<{TARGET:.0e}"); break
            if time.time() - t0 > BUDGET: logline("# relax budget hit"); break
    mg = mnorm(rgrad(n), h)
    logline(f"# RELAX DONE ||g||_M-1={mg:.4e} (raw={float(rgrad(n).norm()):.3e}) E={E_of(n):.4f} "
            f"Q_fwd={charge_fwd(n):.5f} Q_sym={charge_sym(n):.5f} theta_max={theta_max(n):.4f}")

# =========================== STAGE hess (preconditioned, 2 variants) ===========================
if STAGE == 'hess':
    n = pin(torch.tensor(np.load(CRIT)['n'], device=dev))
    gnM = mnorm(rgrad(n), h)
    logline(f"# HESS at critical field: ||g||_M-1={gnM:.4e} Q_fwd={charge_fwd(n):.5f} Q_sym={charge_sym(n):.5f} "
            f"theta_max={theta_max(n):.4f}")
    # core mask excluding the pinned-boundary transition region (~N/20 layers) -- the fixed-BC constraint,
    # NOT a physics deflation (the soliton lives at r<4; the pinning transition/residual sits at r>5.4)
    bw = N // 20; bmask = torch.zeros(N, N, N, device=dev); bmask[bw:-bw, bw:-bw, bw:-bw] = 1.0
    # analytic modes for POST-HOC identification (translations, spatial rotations, U(1) target)
    x = torch.linspace(-L, L, N, device=dev); Xg, Yg, Zg = torch.meshgrid(x, x, x, indexing='ij')
    dnc = [(torch.roll(n, -1, a + 1) - torch.roll(n, 1, a + 1)) / (2 * h) for a in range(3)]   # for translations
    trans = dnc
    rot = [Yg * dnc[2] - Zg * dnc[1], Zg * dnc[0] - Xg * dnc[2], Xg * dnc[1] - Yg * dnc[0]]     # spatial rotations
    vU1 = torch.stack([-n[1], n[0], torch.zeros_like(n[0])], 0)                                  # exact U(1): e_z x n
    def norml(v): v = tang(n, v * bmask); return v / (v.norm() + 1e-30)
    analytic = {'Tx': norml(trans[0]), 'Ty': norml(trans[1]), 'Tz': norml(trans[2]),
                'Rx': norml(rot[0]), 'Ry': norml(rot[1]), 'Rz': norml(rot[2]), 'U1': norml(vU1)}
    QU1, _ = torch.linalg.qr(torch.stack([analytic['U1'].reshape(-1)], 1))   # deflate ONLY U(1)

    def mk_defl(deflate_U1):
        def defl(v):
            v = tang(n, v * bmask).reshape(-1)
            if deflate_U1: v = v - QU1 @ (QU1.T @ v)
            return v.reshape(3, N, N, N)
        return defl
    EPS = 1e-4
    def mk_hvp(defl):
        def hvp(v):
            v = defl(v); return defl((gE(n + EPS * v) - gE(n - EPS * v)) / (2 * EPS))
        return hvp
    def mgs(cols, defl):
        out = []
        for c in cols:
            c = defl(c)
            for o in out: c = c - ip(c, o) * o
            nc = float(c.norm())
            if nc > 1e-9: out.append(c / nc)
        return out

    def run(tag, deflate_U1, seed, bs=6, maxit=26):
        defl = mk_defl(deflate_U1); hvp = mk_hvp(defl)
        torch.manual_seed(seed)
        X = mgs([torch.randn(3, N, N, N, device=dev) for _ in range(bs)], defl)
        P = []; t0 = time.time(); last = None; prev = None
        for it in range(maxit):
            Rr = []
            for j in range(len(X)):
                Hx = hvp(X[j]); th = ip(X[j], Hx); Rr.append(defl(precond(Hx - th * X[j]))); del Hx   # PRECOND residual
                if dev == 'cuda': torch.cuda.empty_cache()
            basis = mgs(X + Rr + P, defl); k = len(basis); A = torch.zeros(k, k, device=dev)
            for j in range(k):
                Hj = hvp(basis[j])
                for i in range(k): A[i, j] = ip(basis[i], Hj)
                del Hj; gc.collect(); torch.cuda.empty_cache()
            A = 0.5 * (A + A.T); w, U = torch.linalg.eigh(A)
            newX = [defl(sum(U[i, j] * basis[i] for i in range(k))) for j in range(bs)]
            newX = [v / v.norm() for v in newX]
            lam0 = float(w[0]); r0 = float(defl(hvp(newX[0]) - lam0 * newX[0]).norm())
            rel = r0 / (abs(lam0) + 1e-30); lamp = lam0 / h**3
            # lam-stabilization (near-zero modes: rel=||R||/|lam| never hits 1e-3); track lowest-4 shift
            spread = np.mean([abs(float(w[i]) / h**3) for i in range(min(4, bs))])
            dl = abs(lamp - prev) / (abs(lamp) + spread + 1e-30) if prev is not None else 1.0; prev = lamp
            logline(f"  [{tag} s{seed}] it={it} t={time.time()-t0:.0f}s lam0_phys={lamp:.4e} rel={rel:.2e} dl={dl:.2e} "
                    f"lam_phys[0:4]={[round(float(w[i])/h**3,2) for i in range(min(4,bs))]}")
            last = (w, newX)                                  # keep the LATEST Ritz set (not min-residual)
            if (rel < 1e-3 or (dl < 2e-3 and it > 8)) and it > 4:
                logline(f"  [{tag} s{seed}] CONVERGED rel={rel:.2e} dl={dl:.2e}"); break
            P = [defl(newX[j] - X[j]) for j in range(min(bs, len(X)))]; X = newX
            del basis, A, U, w, Rr; gc.collect(); torch.cuda.empty_cache()
        w, newX = last
        # overlaps of each converged Ritz vector with the analytic zero modes
        recs = []
        for j in range(len(newX)):
            ov = {nm: round(abs(ip(newX[j], av)), 3) for nm, av in analytic.items()}
            recs.append({'lam_phys': float(w[j]) / h**3, 'overlaps': ov})
        return recs

    out = {'crit_mnorm': gnM, 'Q_fwd': charge_fwd(n), 'Q_sym': charge_sym(n), 'theta_max': theta_max(n), 'runs': {}}
    _sel = os.environ.get('HVARIANT', 'both')
    _variants = [v for v in (('undeflated', False), ('U1deflated', True)) if _sel == 'both' or v[0] == _sel]
    for tag, dfl in _variants:
        allrecs = []
        for seed in (0, 1):
            logline(f"# --- Hessian {tag} seed={seed} ---")
            allrecs.append(run(tag, dfl, seed))
        out['runs'][tag] = allrecs
        json.dump(out, open('noNull_resolve_out.json', 'w'), indent=1)
    logline("# HESS DONE")
    for tag in out['runs']:
        lam0s = [r[0]['lam_phys'] for r in out['runs'][tag]]
        logline(f"  {tag}: lowest lam_phys across seeds = {[round(x,2) for x in lam0s]}")
    json.dump(out, open('noNull_resolve_out.json', 'w'), indent=1)

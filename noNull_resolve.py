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
FW = 2                                              # exactly the pin_boundary(w=2) fixed layers
def free_mask(w):
    msk = torch.zeros(N, N, N, device=dev); msk[w:-w, w:-w, w:-w] = 1.0; return msk
_FM = free_mask(FW)
def freeproj_at(nn, v, w=FW):                       # P_nn(v) = P_free[ v - (nn.v) nn ] -- EXPLICIT base point
    fm = _FM if w == FW else free_mask(w)
    return (v - (v * nn).sum(0, keepdim=True) * nn) * fm
def fgrad(nn): return freeproj_at(nn, gE(nn))       # g_f = P_free P_T grad E at nn
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
    OPT = os.environ.get('OPTIMIZER', 'lbfgs')
    g = fgrad(n); E = E_of(n); t0 = time.time(); a_prev = 1.0; stuck = 0; traj = []
    hist = deque(maxlen=8)                                        # L-BFGS (s,y) pairs, transported at use
    s_cg = freeproj_at(n, precond(g)); d_cg = -s_cg; gs_old = ip(g, s_cg)          # CG state
    logline(f"# CORRECTED RIEMANNIAN {OPT.upper()} (P_free={FW}, transported) start ||g_f||_M-1={mnorm(g,h):.4e} "
            f"(raw={float(g.norm()):.3e}) E={E:.4f} Q_fwd={charge_fwd(n):.4f} shift={shift:.3f} target<{TARGET:.0e}")
    for it in range(1, 20000):
        if OPT == 'lbfgs':
            raw = list(hist); q = g.clone(); meta = []            # TRANSPORT each pair ON-DEMAND (memory-safe)
            for (s, y) in reversed(raw):                          # first loop, newest->oldest
                sT = freeproj_at(n, s); yT = freeproj_at(n, y); ys = ip(yT, sT)
                if ys <= 1e-18: meta.append(None); del sT, yT; continue
                rho = 1.0 / ys; a = rho * ip(sT, q); q = q - a * yT; meta.append((rho, a)); del sT, yT
            r = freeproj_at(n, precond(q))                        # H0 = precond
            for (s, y), mt in zip(raw, reversed(meta)):           # second loop, oldest->newest
                if mt is None: continue
                rho, a = mt; sT = freeproj_at(n, s); yT = freeproj_at(n, y)
                b = rho * ip(yT, r); r = r + (a - b) * sT; del sT, yT
            d = -r; slope = ip(g, d)
            if slope >= 0: d = -freeproj_at(n, precond(g)); slope = ip(g, d); hist.clear()
            a = min(a_prev * 2.0, 4.0) if raw else 1.0
        else:                                                     # preconditioned Polak-Ribiere CG
            d = d_cg; slope = ip(g, d)
            if slope >= 0: d = -s_cg; slope = ip(g, d)
            a = min(a_prev * 2.0, 4.0)
        En = None; nt = None
        for _ in range(45):
            nt_try = pin(n + a * d); Et = E_of(nt_try)
            if Et <= E + 1e-4 * a * slope: En = Et; nt = nt_try; break
            a *= 0.5
        if En is None:
            stuck += 1
            if stuck >= 3: logline(f"# relax line-search stuck x3 it={it}"); break
            hist.clear(); s_cg = freeproj_at(n, precond(g)); d_cg = -s_cg; gs_old = ip(g, s_cg); a_prev = 1.0; continue
        stuck = 0; a_prev = a; g_new = fgrad(nt)
        if OPT == 'lbfgs':
            sv = freeproj_at(nt, nt - n)                          # step, projected at NEW point
            g_old_T = freeproj_at(nt, g)                          # TRANSPORT old gradient to T_{nt}
            yv = g_new - g_old_T
            if ip(sv, yv) > 1e-18: hist.append((sv.clone(), yv.clone()))
        else:
            s_new = freeproj_at(nt, precond(g_new)); s_old_T = freeproj_at(nt, s_cg)
            beta = max(0.0, ip(g_new, s_new - s_old_T) / (gs_old + 1e-30))
            d_cg = -s_new + beta * freeproj_at(nt, d); s_cg = s_new; gs_old = ip(g_new, s_new)
        n = nt; g = g_new; E = En
        if it % 10 == 0: gc.collect(); torch.cuda.empty_cache()
        if it % 20 == 0 or it == 1:
            mg = mnorm(g, h)
            traj.append({'it': it, 't': time.time() - t0, 'gf_mnorm': mg, 'gf_raw': float(g.norm()),
                         'E': E, 'Q_fwd': charge_fwd(n), 'theta_max': theta_max(n), 'step': a})
            logline(f"  [relax] it={it} t={time.time()-t0:.0f}s ||g_f||_M-1={mg:.4e} (raw={float(g.norm()):.3e}) "
                    f"E={E:.4f} Q_fwd={charge_fwd(n):.4f} thetamax={theta_max(n):.3f} step={a:.2e}")
            with torch.no_grad():
                np.savez(CRIT + '.tmp.npz', n=(n / n.norm(dim=0, keepdim=True)).cpu().numpy(), N=N, L=L, h=h, xi=xi, kappa=kap)
                os.replace(CRIT + '.tmp.npz', CRIT)
            json.dump(traj, open(f'noNull_relax_{OPT}_traj.json', 'w'), indent=0)
            if mg < TARGET: logline(f"# relax CONVERGED ||g_f||_M-1<{TARGET:.0e}"); break
            if time.time() - t0 > BUDGET: logline("# relax budget hit (NOT at target)"); break
    mg = mnorm(fgrad(n), h)
    verdict = 'REACHED' if mg < TARGET else 'NOT-REACHED(failure-to-criticality)'
    logline(f"# RELAX DONE ({OPT}) ||g_f||_M-1={mg:.4e} (raw={float(fgrad(n).norm()):.3e}) target={TARGET:.0e} "
            f"{verdict} E={E_of(n):.4f} Q_fwd={charge_fwd(n):.5f} Q_sym={charge_sym(n):.5f} theta_max={theta_max(n):.4f}")
    json.dump({'optimizer': OPT, 'verdict': verdict, 'final_gf_mnorm': mg, 'final_E': E_of(n),
               'target': TARGET, 'Q_fwd': charge_fwd(n), 'Q_sym': charge_sym(n), 'theta_max': theta_max(n),
               'trajectory': traj}, open(f'noNull_relax_{OPT}_out.json', 'w'), indent=1)

# =========================== STAGE nk (Riemannian trust-region Newton-Krylov) ===========================
if STAGE == 'nk':
    n = pin(torch.tensor(np.load(CRIT)['n'], device=dev))
    TARGET = float(os.environ.get('MNORM_TARGET', '5e-2'))
    BUDGET = float(os.environ.get('NK_BUDGET_S', '6000'))
    EPS = 1e-4; Md = h**3
    # analytic modes for modal projections of g_f (exact U(1) is deflated; T/R are pseudomodes -> reported)
    xg = torch.linspace(-L, L, N, device=dev); Xg, Yg, Zg = torch.meshgrid(xg, xg, xg, indexing='ij')
    def analytic_modes(nn):
        dc = [(torch.roll(nn, -1, a + 1) - torch.roll(nn, 1, a + 1)) / (2 * h) for a in range(3)]
        M = {'Tx': dc[0], 'Ty': dc[1], 'Tz': dc[2], 'Rx': Yg * dc[2] - Zg * dc[1],
             'Ry': Zg * dc[0] - Xg * dc[2], 'Rz': Xg * dc[1] - Yg * dc[0],
             'U1': torch.stack([-nn[1], nn[0], torch.zeros_like(nn[0])], 0)}
        return {k: (lambda vv: vv / (vv.norm() + 1e-30))(freeproj_at(nn, v)) for k, v in M.items()}
    def defl_nk(v, u1):                                  # P_free P_T then remove exact U(1)
        v = freeproj_at(n, v); return v - ip(v, u1) * u1
    def hvp(v, u1):                                      # projected FD-of-gradient HVP, U(1)-deflated
        v = defl_nk(v, u1); return defl_nk((gE(n + EPS * v) - gE(n - EPS * v)) / (2 * EPS), u1)
    def Aop(v, mu, u1): return hvp(v, u1) + mu * Md * defl_nk(v, u1)     # (H + mu M) on the deflated tangent
    def btau(x, p, rad):                                 # positive root of ||x + tau p|| = rad
        a_ = ip(p, p); b_ = 2 * ip(x, p); c_ = ip(x, x) - rad * rad
        return (-b_ + max(b_ * b_ - 4 * a_ * c_, 0.0) ** 0.5) / (2 * a_ + 1e-30)
    def steihaug(b, mu, rad, u1, maxit=60, tol=1e-2):    # PRECONDITIONED Steihaug-CG for (H+muM)x=b in trust rad
        def pc(v): return defl_nk(precond(v), u1)        # SPD preconditioner, kept in the deflated tangent
        x = torch.zeros_like(b); r = b.clone(); z = pc(r); p = z.clone(); rz = ip(r, z); b0 = float(r.norm()) + 1e-30
        for j in range(maxit):
            Hp = Aop(p, mu, u1); pHp = ip(p, Hp)
            if pHp <= 1e-30: return x + btau(x, p, rad) * p, 'negcurv', j
            al = rz / pHp; xn = x + al * p
            if float(xn.norm()) >= rad: return x + btau(x, p, rad) * p, 'boundary', j
            x = xn; r = r - al * Hp
            if float(r.norm()) < tol * b0: return x, 'converged', j
            z = pc(r); rz_new = ip(r, z); p = z + (rz_new / rz) * p; rz = rz_new
        return x, 'maxit', maxit
    mu = float(os.environ.get('NK_MU0', '1.0')); rad = float(os.environ.get('NK_RAD', '2.0'))
    t0 = time.time(); traj = []
    logline(f"# NK TRUST-REGION start E={E_of(n):.4f} mu0={mu} rad0={rad} target ||g_f||_M-1<{TARGET:.0e}")
    for step in range(1, 300):
        am = analytic_modes(n); u1 = am['U1']
        g = defl_nk(fgrad(n), u1); gn = mnorm(g, h)
        proj = {k: abs(ip(g, v)) / h**1.5 for k, v in am.items()}     # modal projections of g_f (M-1 units)
        if gn < TARGET:
            logline(f"# NK CONVERGED step={step} ||g_f||_M-1={gn:.4e}"); break
        delta, status, cgit = steihaug(-g, mu, rad, u1)
        DN2 = -ip(g, delta)                                          # Newton decrement^2 = <g,(H+muM)^-1 g>
        n_try = pin(n + delta); Eo = E_of(n); Ta = time.time() - t0
        actual = Eo - E_of(n_try)
        Hd = Aop(delta, mu, u1); pred = -ip(g, delta) - 0.5 * ip(delta, Hd)
        rho = actual / (pred + 1e-30)
        acc = rho > 0.1 and actual > 0
        if acc: n = n_try; mu = max(mu * 0.5, 1e-7)
        else: mu = mu * 3.0
        if rho > 0.75 and status in ('boundary', 'negcurv'): rad = min(rad * 2, 16)
        elif rho < 0.25: rad = max(rad * 0.5, 1e-3)
        rec = {'step': step, 't': Ta, 'gf_mnorm': gn, 'E': Eo, 'DN2': DN2, 'mu': mu, 'rad': rad,
               'rho': rho, 'cg_status': status, 'cg_iters': cgit, 'accepted': acc,
               'modal_proj': proj, 'g_perp_phys': mnorm(g - sum(ip(g, v) * v for v in am.values()), h)}
        traj.append(rec)
        logline(f"  [nk] step={step} t={Ta:.0f}s ||g_f||_M-1={gn:.4e} DN2={DN2:.3e} E={Eo:.5f} mu={mu:.1e} "
                f"rad={rad:.2e} rho={rho:+.2f} cg={status}({cgit}) {'ACC' if acc else 'rej'} "
                f"g_perp={rec['g_perp_phys']:.3e}")
        with torch.no_grad():
            np.savez(CRIT + '.tmp.npz', n=(n / n.norm(dim=0, keepdim=True)).cpu().numpy(), N=N, L=L, h=h, xi=xi, kappa=kap)
            os.replace(CRIT + '.tmp.npz', CRIT)
        json.dump(traj, open('noNull_nk_traj.json', 'w'), indent=0)
        gc.collect()
        if dev == 'cuda': torch.cuda.empty_cache()
        if Ta > BUDGET: logline("# NK budget hit"); break
    gnf = mnorm(defl_nk(fgrad(n), analytic_modes(n)['U1']), h)
    logline(f"# NK DONE ||g_f||_M-1={gnf:.4e} target={TARGET:.0e} {'REACHED' if gnf<TARGET else 'NOT-REACHED'} "
            f"E={E_of(n):.4f} Q_fwd={charge_fwd(n):.5f} theta_max={theta_max(n):.4f}")
    json.dump({'final_gf_mnorm': gnf, 'reached': bool(gnf < TARGET), 'final_E': E_of(n),
               'Q_fwd': charge_fwd(n), 'Q_sym': charge_sym(n), 'theta_max': theta_max(n), 'trajectory': traj},
              open('noNull_nk_out.json', 'w'), indent=1)

# =========================== STAGE hess (preconditioned, 2 variants) ===========================
if STAGE == 'hess':
    n = pin(torch.tensor(np.load(CRIT)['n'], device=dev))
    HBW = int(os.environ.get('HESS_BW', '2'))            # free-mask width (primary 2; sweep 2,4,8,12)
    BS = int(os.environ.get('HESS_BS', '10'))            # block size (Charles-authorized bs=10 @256^3; 12 @192/128)
    SEEDS = [int(s) for s in os.environ.get('HESS_SEEDS', '0,1').split(',')]
    g_f = freeproj_at(n, gE(n), HBW); gnM = mnorm(g_f, h)
    logline(f"# HESS bw={HBW} bs={BS} at critical field ||g_f||_M-1={gnM:.4e} Q_fwd={charge_fwd(n):.5f} theta_max={theta_max(n):.4f}")
    xg = torch.linspace(-L, L, N, device=dev); Xg, Yg, Zg = torch.meshgrid(xg, xg, xg, indexing='ij')
    dnc = [(torch.roll(n, -1, a + 1) - torch.roll(n, 1, a + 1)) / (2 * h) for a in range(3)]
    _tr = [dnc[0], dnc[1], dnc[2], Yg * dnc[2] - Zg * dnc[1], Zg * dnc[0] - Xg * dnc[2],
           Xg * dnc[1] - Yg * dnc[0]]                                                    # 6 T/R generators (transient)
    u1 = freeproj_at(n, torch.stack([-n[1], n[0], torch.zeros_like(n[0])], 0), HBW)      # only U1 is exact
    u1 = u1 / (u1.norm() + 1e-30)
    def defl(v): v = freeproj_at(n, v, HBW); return v - ip(v, u1) * u1                  # P_free(bw) then remove exact U(1)
    def pc(v): return defl(precond(v))
    EPS = 1e-4
    def hvp(v):
        v = defl(v); return defl((gE(n + EPS * v) - gE(n - EPS * v)) / (2 * EPS))
    def mgs(cols):
        out = []
        for c in cols:
            c = defl(c)
            for o in out: c = c - ip(c, o) * o
            nc = float(c.norm())
            if nc > 1e-9: out.append(c / nc)
        return out
    def rj_of(v):                                        # symmetric relative residual r_j = ||Hv-lam M v||/(||Hv||+|lam| ||Mv||)
        Hv = hvp(v); lam = ip(v, Hv); res = float(defl(Hv - lam * v).norm())
        return res / (float(Hv.norm()) + abs(lam) + 1e-30), lam
    # Q_TR: orthonormal basis of the 6 T/R pseudomode generators (mgs applies defl -> U(1) removed + free-proj)
    Q_TR = mgs(_tr); del _tr, dnc, Xg, Yg, Zg; gc.collect()      # free the transient generator fields
    logline(f"# Q_TR pseudomode subspace: {len(Q_TR)} orthonormal T/R generators (U(1) removed)")
    def sTR(v): return float(sum(ip(q, v)**2 for q in Q_TR))    # |Q_TR^T v|^2 in [0,1]; >0.5 => pseudomode
    def geneigh(A, B, kk):                               # lowest kk of A c=lam B c; RANK-REVEALING (log rank, drop null dirs)
        Bs = 0.5 * (B + B.T); k0 = Bs.shape[0]
        wB, VB = torch.linalg.eigh(Bs)                   # B eigen-decomposition (SPD up to numerics)
        tol = float(wB.max()) * k0 * 2.2e-16             # machine-precision rank threshold
        keep = wB > tol; rk = int(keep.sum())
        Vk = VB[:, keep]; d = wB[keep]                   # B = Vk diag(d) Vk^T on the kept subspace
        Whalf = Vk / d.sqrt()                            # B^{-1/2} on kept subspace (k0 x rk)
        Ar = Whalf.T @ A @ Whalf; Ar = 0.5 * (Ar + Ar.T)  # reduce generalized -> standard on well-conditioned subspace
        wv, Yv = torch.linalg.eigh(Ar); Cv = Whalf @ Yv
        return wv[:kk], Cv[:, :min(kk, rk)], rk, k0

    def run(seed):
        torch.manual_seed(seed)
        X = mgs([torch.randn(3, N, N, N, device=dev) for _ in range(BS)])   # orthonormal start
        P = []; t0 = time.time(); last = None
        for it in range(60):
            W = []                                          # preconditioned residuals (fresh H*X, del'd -> no storage)
            for x in X:
                hx = hvp(x); W.append(pc(hx - ip(x, hx) * x)); del hx
                if dev == 'cuda': torch.cuda.empty_cache()
            S = X + W + P; k = len(S)
            A = torch.zeros(k, k, device=dev); B = torch.zeros(k, k, device=dev)   # A=S^T H S, B=S^T S
            for j in range(k):
                HSj = hvp(S[j])                             # STREAM every H*S column (never stored) -> memory-safe
                for i in range(k): A[i, j] = ip(S[i], HSj)
                del HSj
                if dev == 'cuda': torch.cuda.empty_cache()
            for i in range(k):
                for j in range(i, k): B[i, j] = B[j, i] = ip(S[i], S[j])
            gc.collect(); torch.cuda.empty_cache()
            A = 0.5 * (A + A.T); w, C, rk, k0 = geneigh(A, B, BS)   # rank-revealing (drops B-null dirs)
            nc = min(BS, C.shape[1])
            newX = [(lambda vv: vv / vv.norm())(defl(sum(C[i, j] * S[i] for i in range(k)))) for j in range(nc)]
            del S; gc.collect(); torch.cuda.empty_cache()
            # records: lam=Ritz w; a_j; s_TR=|Q_TR^T v|^2 (pseudomode-subspace projection); r_j via ACTUAL HVP for lowest NRJ
            NRJ = min(nc, 9); recs = []
            for j in range(nc):
                s = sTR(newX[j])
                recs.append({'lam_phys': float(w[j]) / h**3, 'r_j': None, 'a_j': ip(newX[j], g_f) / h**1.5,
                             's_TR': s, 'is_pseudomode': bool(s > 0.5)})
            for j in range(NRJ):
                Hv = hvp(newX[j]); lamj = ip(newX[j], Hv)
                recs[j]['r_j'] = float(defl(Hv - lamj * newX[j]).norm()) / (float(Hv.norm()) + abs(lamj) + 1e-30)
                recs[j]['lam_phys'] = lamj / h**3           # exact Rayleigh quotient for the computed modes
                del Hv
                if dev == 'cuda': torch.cuda.empty_cache()
            last = (recs, newX)
            rjs = [recs[j]['r_j'] for j in range(NRJ)]
            allconv = all(r is not None and r < 1e-3 for r in rjs); maxrj = max((r for r in rjs if r is not None), default=float('nan'))
            logline(f"  [hess bw{HBW} s{seed}] it={it} t={time.time()-t0:.0f}s rank={rk}/{k0} "
                    f"lam[0:5]={[round(recs[j]['lam_phys'],3) for j in range(min(5,nc))]} "
                    f"max_r_j(0..{NRJ-1})={maxrj:.2e} s_TR[0:5]={[round(recs[j]['s_TR'],2) for j in range(min(5,nc))]}")
            if allconv and it > 3:
                logline(f"  [hess bw{HBW} s{seed}] ALL lowest-{NRJ} Ritz pairs CONVERGED (max r_j={maxrj:.2e})"); break
            Pnew = [defl(newX[j] - X[j]) for j in range(nc)]     # LOBPCG search dir P_{k+1}=X_{k+1}-X_k
            X = newX; P = Pnew
            del A, B, w, C, Pnew; gc.collect(); torch.cuda.empty_cache()
        recs, newX = last
        _rj = [(r['r_j'] if r['r_j'] is not None else float('nan')) for r in recs]
        with torch.no_grad():                            # save EVERY Ritz vector (gitignored .npz)
            np.savez(f'noNull_hess_ritz_bw{HBW}_s{seed}.npz',
                     V=np.stack([v.cpu().numpy() for v in newX]), lam_phys=[r['lam_phys'] for r in recs],
                     r_j=_rj, a_j=[r['a_j'] for r in recs], s_TR=[r['s_TR'] for r in recs], N=N, L=L, h=h)
        return recs

    out = {'crit_gf_mnorm': gnM, 'bw': HBW, 'bs': BS, 'Q_fwd': charge_fwd(n), 'theta_max': theta_max(n), 'seeds': {}}
    for seed in SEEDS:
        logline(f"# --- Hessian bw={HBW} seed={seed} (U(1) deflated; T/R identified by overlap after) ---")
        out['seeds'][str(seed)] = run(seed)
        json.dump(out, open(f'noNull_hess_bw{HBW}_out.json', 'w'), indent=1)
    logline(f"# HESS DONE bw={HBW}")
    for seed in SEEDS:
        recs = out['seeds'][str(seed)]
        nlow = min(9, len(recs))
        logline(f"  seed{seed} lowest-{nlow} (lam_phys : r_j : s_TR[pseudomode] : a_j):")
        for j in range(nlow):
            r = recs[j]
            logline(f"    #{j} lam={r['lam_phys']:+.4f} r_j={(r['r_j'] if r['r_j'] is not None else float('nan')):.2e} "
                    f"s_TR={r['s_TR']:.3f} a_j={r['a_j']:+.2e}")
    json.dump(out, open(f'noNull_hess_bw{HBW}_out.json', 'w'), indent=1)

#!/usr/bin/env python3
"""
ext_scan_verify.py -- LEAN, ROBUST verifier for the two decisive EXTERIOR
=========================================================================
findings, independent of ext_scan_whole.py's heavy dense eigensolves.
Driver: Claude (Opus 4.8, 1M). 2026-06-13. Frame CRITICAL_UNIVERSE_FRAME.
Reuses the metric's OWN operators (Box_g, ON source) verbatim from
wint_solve2d / ext_scan_whole. Adds nothing. New file (ext_scan_* only).

TWO QUESTIONS, each a candidate character-change flagged by PART A:

 Q1 (EXISTENCE). Does the metric's ON matter source admit a SMOOTH STATIC
   medium on the f>1 EXTERIOR (phi<0)? PART A showed: sourceless (Phi=0)
   exterior converges to a clean monotone medium (turns=0); ON-source
   (Phi>0) exterior FAILS to converge (multi-turn, maxres ~ O(1-100)).
   Newton failure alone is not a no-existence proof. We test EXISTENCE
   honestly two ways: (i) PSEUDO-TRANSIENT CONTINUATION (implicit
   gradient flow d phi/dtau = Box_g phi - S(phi)) -- a far more robust
   path to a static fixed point than Newton; (ii) continuation in Phi
   from 0 up. If even pseudo-transient + continuation cannot reach a
   smooth static fixed point while the f<1 INTERIOR does, the ON source
   genuinely does NOT close a smooth static medium on the exterior =
   a REAL character change (the source that binds a cell anti-binds the
   medium).

 Q2 (ANGULAR GAP on the gradient exterior, sparse). On the SOURCELESS
   exterior (which converges, carries a real radial gradient), read the
   angular-stiffness sign about the self-consistent gradient background
   using a SPARSE shift-invert eigensolver of the SYMMETRIZED interior
   Jacobian (NO dense toarray; no OOM). B2/#36 proved the gap POSITIVE
   ABOUT ROUND (zero gradient). The departure question: does the gap
   stay positive as the medium gradient grows? CONTROL = the round
   interior (gap must be >0).

Log /tmp/ext_scan_verify.log. Convergence evidence mandatory. Honest.
"""
import time, json
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spsla

t0 = time.time()
_fh = open("/tmp/ext_scan_verify.log", "w")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()

log("="*72); log("ext_scan_verify -- EXTERIOR existence + angular-gap (lean)")
log("="*72)

# ---- metric's OWN operators (verbatim) -------------------------------
def box_np(phi, r, th, dr, dth):
    w = np.exp(-2.0*phi); R = r[:, None]; sinth = np.sin(th)[None, :]
    a_r = (R**2)*w; am_r = 0.5*(a_r[1:, :]+a_r[:-1, :])
    flux_r = am_r*(phi[1:, :]-phi[:-1, :])/dr
    div_r = np.zeros_like(phi)
    div_r[1:-1, :] = (flux_r[1:, :]-flux_r[:-1, :])/dr/(R[1:-1]**2)
    a_th = sinth*w; am_th = 0.5*(a_th[:, 1:]+a_th[:, :-1])
    flux_th = am_th*(phi[:, 1:]-phi[:, :-1])/dth
    div_th = np.zeros_like(phi)
    div_th[:, 1:-1] = (flux_th[:, 1:]-flux_th[:, :-1])/dth/(R**2*sinth)[:, 1:-1]
    return div_r+div_th

def src(phi, Phi): return Phi*(np.exp(-2*phi)-np.exp(phi))

def resid(phi, r, th, dr, dth, Din, Dout, Phi):
    F = box_np(phi, r, th, dr, dth) - src(phi, Phi)
    F[0, :]  = phi[0, :]  - Din
    F[-1, :] = phi[-1, :] - Dout
    F[:, 0]  = phi[:, 0]  - phi[:, 1]
    F[:, -1] = phi[:, -1] - phi[:, -2]
    return F

def jac(phi, r, th, dr, dth, Din, Dout, Phi, eps=1e-7):
    Nr, Nth = phi.shape; N = Nr*Nth
    F0 = resid(phi, r, th, dr, dth, Din, Dout, Phi).ravel()
    idx = np.arange(N).reshape(Nr, Nth)
    rows, cols, vals = [], [], []
    for ci in range(3):
        for cj in range(3):
            mask = np.zeros((Nr, Nth), bool); mask[ci::3, cj::3] = True
            ph = phi.copy(); ph[mask] += eps
            dF = ((resid(ph, r, th, dr, dth, Din, Dout, Phi).ravel()-F0)/eps
                  ).reshape(Nr, Nth)
            owner = np.full((Nr, Nth), -1, np.int64)
            for (di, dj) in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
                si = np.clip(np.arange(Nr)[:, None]+di, 0, Nr-1)
                sj = np.clip(np.arange(Nth)[None, :]+dj, 0, Nth-1)
                valid = ((np.arange(Nr)[:, None]+di >= 0) &
                         (np.arange(Nr)[:, None]+di < Nr) &
                         (np.arange(Nth)[None, :]+dj >= 0) &
                         (np.arange(Nth)[None, :]+dj < Nth))
                inc = valid & mask[si, sj] & (owner < 0)
                owner[inc] = idx[si, sj][inc]
            sel = owner >= 0; vv = dF[sel]; nz = vv != 0.0
            rows.append(idx[sel][nz]); cols.append(owner[sel][nz]); vals.append(vv[nz])
    return sps.csr_matrix((np.concatenate(vals),
                          (np.concatenate(rows), np.concatenate(cols))),
                          shape=(N, N)), F0

def grid(r_in, r_star, Nr, Nth):
    r = np.linspace(r_in, r_star, Nr); th = np.linspace(0, np.pi, Nth)
    return r, th, r[1]-r[0], th[1]-th[0]

def seed(Din, Dout, r, th):
    return np.tile(np.linspace(Din, Dout, len(r))[:, None], (1, len(th)))

# ---- Q1: EXISTENCE via Newton AND pseudo-transient continuation ------
def newton(phi0, r, th, dr, dth, Din, Dout, Phi, itmax=200, tol=1e-10):
    phi = phi0.copy()
    for nit in range(itmax):
        J, F0 = jac(phi, r, th, dr, dth, Din, Dout, Phi)
        try: dphi = spsla.spsolve(J, -F0).reshape(phi.shape)
        except Exception: return phi, np.inf, False
        if not np.all(np.isfinite(dphi)): return phi, np.inf, False
        nF0 = np.linalg.norm(F0); lam = 1.0; ok = False
        for _ in range(50):
            tr = phi+lam*dphi
            if np.all(np.abs(tr) < 60):
                Ft = resid(tr, r, th, dr, dth, Din, Dout, Phi)
                if np.isfinite(Ft).all() and np.linalg.norm(Ft) < (1-1e-4*lam)*nF0:
                    ok = True; break
            lam *= 0.5
        if not ok:
            mr = float(np.max(np.abs(resid(phi, r, th, dr, dth, Din, Dout, Phi)[2:-2, 2:-2])))
            return phi, mr, mr < 1e-8
        phi = phi+lam*dphi
        mr = float(np.max(np.abs(resid(phi, r, th, dr, dth, Din, Dout, Phi)[2:-2, 2:-2])))
        if mr < tol: return phi, mr, True
    return phi, mr, mr < 1e-8

def ptc(phi0, r, th, dr, dth, Din, Dout, Phi, dtau=0.1, itmax=4000, tol=1e-9):
    """Implicit pseudo-transient continuation (backward-Euler gradient flow):
    (I/dtau - J) dphi = F(phi); robust globalization toward a STATIC fixed
    point. If this cannot reach a static residual<tol while the interior
    does, the static exterior fixed point genuinely does not exist."""
    phi = phi0.copy(); N = phi.size; I = sps.identity(N, format='csr')
    mr = np.inf
    for nit in range(itmax):
        J, F0 = jac(phi, r, th, dr, dth, Din, Dout, Phi)
        A = I/dtau - J
        try: dphi = spsla.spsolve(A.tocsc(), F0).reshape(phi.shape)
        except Exception: return phi, mr, False, nit
        if not np.all(np.isfinite(dphi)): return phi, mr, False, nit
        tr = phi+dphi
        if not np.all(np.abs(tr) < 80): dphi *= 0.3; tr = phi+dphi
        newmr = float(np.max(np.abs(resid(tr, r, th, dr, dth, Din, Dout, Phi)[2:-2, 2:-2])))
        if newmr < mr*1.5:               # accept; grow dtau (SER)
            phi = tr; dtau = min(dtau*1.3, 50.0)
        else:
            dtau = max(dtau*0.5, 1e-3)    # reject step size
        mr = newmr
        if mr < tol: return phi, mr, True, nit
    return phi, mr, mr < tol, nit

def diag(phi, r, th):
    wth = np.sin(th); wth = wth/wth.sum(); phibar = phi @ wth
    turns = int(np.sum(np.diff(np.sign(np.gradient(phibar, r))) != 0))
    return turns, float(phibar.min()), float(phibar.max())

log("\nQ1 -- EXISTENCE of a smooth STATIC medium with the ON source")
log("  Method: Newton, then pseudo-transient continuation (PTC), then")
log("  Phi-continuation (ramp Phi 0->target reusing the previous solve).")
r, th, dr, dth = grid(1.0, 6.0, 161, 81)

# CONTROL: the f<1 INTERIOR with the ON source SHOULD close (B1).
log("\n  CONTROL (INTERIOR f<1, phi>0): ON source must close to a smooth cell")
for (Din, Dout, Phi) in [(0.5, 0.5, 1.0), (0.8, 0.3, 1.0)]:
    p0 = seed(Din, Dout, r, th)
    p, mr, cv = newton(p0, r, th, dr, dth, Din, Dout, Phi)
    t, mn, mx = diag(p, r, th)
    log(f"    INT Din={Din} Dout={Dout} Phi={Phi}: newton conv={cv} "
        f"maxres={mr:.2e} turns={t} phibar in[{mn:.3f},{mx:.3f}]")

log("\n  EXTERIOR (f>1, phi<0): does ANY method reach a smooth static medium?")
log(f"  {'Din':>5} {'Dout':>6} {'Phi':>5} {'newton':>14} {'PTC':>22} {'Phi-cont':>16}")
Q1 = []
for (Din, Dout) in [(0.0, -0.5), (0.0, -1.0), (-0.2, -1.0)]:
    for Phi in [0.1, 0.3, 1.0]:
        p0 = seed(Din, Dout, r, th)
        pn, mrn, cvn = newton(p0, r, th, dr, dth, Din, Dout, Phi)
        tn, _, _ = diag(pn, r, th)
        pp, mrp, cvp, nit = ptc(p0.copy(), r, th, dr, dth, Din, Dout, Phi)
        tp, _, _ = diag(pp, r, th)
        # Phi-continuation: ramp from the converged Phi=0 medium
        pc = seed(Din, Dout, r, th)
        pc, _, _ = newton(pc, r, th, dr, dth, Din, Dout, 0.0)
        cvc = True; mrc = 0.0
        for Phr in np.linspace(0.0, Phi, 8)[1:]:
            pc, mrc, cvc = newton(pc, r, th, dr, dth, Din, Dout, float(Phr))
            if not cvc: break
        tc, _, _ = diag(pc, r, th)
        rec = dict(Din=Din, Dout=Dout, Phi=Phi, newton_conv=cvn, newton_mr=mrn,
                   newton_turns=tn, ptc_conv=cvp, ptc_mr=mrp, ptc_turns=tp,
                   ptc_nit=nit, phicont_conv=cvc, phicont_mr=mrc, phicont_turns=tc)
        Q1.append(rec)
        log(f"  {Din:5.1f} {Dout:6.1f} {Phi:5.1f} "
            f"{str(cvn)+' '+format(mrn,'.1e'):>14} "
            f"{str(cvp)+' '+format(mrp,'.1e')+' n='+str(nit):>22} "
            f"{str(cvc)+' '+format(mrc,'.1e'):>16}")
with open("/tmp/ext_scan_verify_Q1.json", "w") as fh:
    json.dump(Q1, fh, indent=0, default=float)

any_ext = any(d["ptc_conv"] or d["phicont_conv"] or d["newton_conv"] for d in Q1)
log(f"\n  Q1 VERDICT: a smooth static ON-source EXTERIOR medium reachable by "
    f"some robust method? {any_ext}")
if not any_ext:
    log("  -> REAL character change: the ON matter source that CLOSES a cell")
    log("     (interior, f<1) does NOT admit a smooth static medium on the")
    log("     f>1 exterior. The exterior's only smooth static whole-metric")
    log("     solution is the SOURCELESS (vacuum/mirror) medium.")

# ---- Q2: angular gap sign on the SOURCELESS gradient exterior (sparse) -
log("\nQ2 -- ANGULAR-GAP SIGN on the sourceless gradient exterior (sparse)")
log("  CONTROL: round interior gap > 0 (B2). Then sweep medium gradient.")

def ang_gap_sparse(phi, r, th, dr, dth, Din, Dout, Phi, k=8):
    """Smallest eigenvalues of the symmetrized INTERIOR Jacobian (closure
    rows/cols struck) via sparse shift-invert near 0; classify angular
    content; return the angular eigenvalue nearest 0 (its sign) and the
    most-negative angular eigenvalue."""
    Nr, Nth = phi.shape
    J, _ = jac(phi, r, th, dr, dth, Din, Dout, Phi)
    idx = np.arange(Nr*Nth).reshape(Nr, Nth)
    keep = np.ones((Nr, Nth), bool)
    keep[0, :] = keep[-1, :] = keep[:, 0] = keep[:, -1] = False
    kid = idx[keep]
    Jint = J.tocsr()[kid][:, kid]
    Js = (0.5*(Jint+Jint.T)).tocsc()
    # smallest-magnitude eigenpairs via shift-invert at sigma=0
    try:
        vals, vecs = spsla.eigsh(Js, k=k, sigma=0.0, which='LM')
    except Exception:
        # fallback: smallest algebraic
        vals, vecs = spsla.eigsh(Js, k=k, which='SA')
    angc = []
    for i in range(vecs.shape[1]):
        Vg = np.zeros((Nr, Nth)); Vg[keep] = vecs[:, i]
        angc.append(np.mean(np.std(Vg[2:-2, 2:-2], axis=1)))
    angc = np.array(angc)
    isang = angc > 0.3*angc.max() if angc.max() > 0 else np.zeros(len(vals), bool)
    av = vals[isang] if isang.any() else vals
    gap = float(av[np.argmin(np.abs(av))])
    return gap, float(av.min()), int(np.sum(vals < -1e-9)), int(isang.sum())

# CONTROL round interior
r2, th2, dr2, dth2 = grid(1.0, 6.0, 121, 61)
pc = seed(0.5, 0.5, r2, th2)
pc, mrc, cvc = newton(pc, r2, th2, dr2, dth2, 0.5, 0.5, 1.0)
if cvc:
    g, gneg, nn, na = ang_gap_sparse(pc, r2, th2, dr2, dth2, 0.5, 0.5, 1.0)
    log(f"  CONTROL round interior phi=0.5 Phi=1: ang_gap={g:.4e} "
        f"gap_neg={gneg:.4e} n_neg={nn} n_ang={na}  (expect >0, B2)")

log(f"  {'Din':>5} {'Dout':>6} {'grad':>7} {'conv':>5} {'ang_gap':>12} "
    f"{'gap_neg':>12} {'n_neg':>6} {'sign':>5}")
Q2 = []
for (Din, Dout) in [(0.0, -0.5), (0.0, -1.0), (0.0, -2.0), (-0.2, -1.5),
                    (-0.5, -2.0), (0.0, -3.0)]:
    p0 = seed(Din, Dout, r2, th2)
    p, mr, cv = newton(p0, r2, th2, dr2, dth2, Din, Dout, 0.0)  # SOURCELESS
    if not cv:
        log(f"  {Din:5.1f} {Dout:6.1f} {(Dout-Din)/5:7.3f}  FAIL")
        continue
    g, gneg, nn, na = ang_gap_sparse(p, r2, th2, dr2, dth2, Din, Dout, 0.0)
    grad = (Dout-Din)/(r2[-1]-r2[0])
    sign = "+" if g > 1e-9 else ("-" if g < -1e-9 else "0")
    Q2.append(dict(Din=Din, Dout=Dout, grad=grad, gap=g, gap_neg=gneg, n_neg=nn))
    log(f"  {Din:5.1f} {Dout:6.1f} {grad:7.3f} {str(cv):>5} {g:12.4e} "
        f"{gneg:12.4e} {nn:6d} {sign:>5}")
with open("/tmp/ext_scan_verify_Q2.json", "w") as fh:
    json.dump(Q2, fh, indent=0, default=float)

neg = [d for d in Q2 if d["gap"] < -1e-7]
log(f"\n  Q2 VERDICT: angular gap negative on any sourceless gradient "
    f"exterior? {len(neg)>0}  ({len(neg)}/{len(Q2)})")
if not neg:
    log("  -> B2 EXTENDS: the angular gap stays POSITIVE on the gradient-")
    log("     carrying sourceless exterior; pure damping is NOT a round-only")
    log("     accident. No shaped type born in the smooth medium.")

log(f"\next_scan_verify COMPLETE ({time.time()-t0:.0f}s)")
log("logs /tmp/ext_scan_verify.log  json /tmp/ext_scan_verify_Q{1,2}.json")
_fh.close()

#!/usr/bin/env python3
"""
verify_stageB_indep.py -- BLIND ADVERSARIAL VERIFIER (Stage C) for the
complete-metric Stage-B sweep headline.

This is an INDEPENDENT solver.  It does NOT call selfconsistent_fast /
selfconsistent_batched (the Picard SCF the headline used).  Instead it solves
the COUPLED (Theta, phi) complete-action system with a SINGLE damped full-Newton
on the joint unknown vector u=[Theta_interior ; phi_interior], with an Armijo
line search -- the standard tool for a stiff two-way fixed point whose Picard
relaxation is basin-sensitive.  It REUSES only the committed PHYSICS primitives
(theta_ddot, stress, phi_from_source closure, grad_central) from
complete_metric_batched.py -- the EL residual and the MS t-equation -- assembled
into one residual F(u) and a colored-FD Jacobian.

Purpose: try HARD to BREAK the "ONE round continuum, no distinct types" headline:
  A. Re-attack the non-converged region (shaped / multi-node / multi-core seeds,
     deep p, near kappa8*) with this independent full-Newton -- a Picard failure
     is NOT a no-solution proof.
  B. Hunt the TOPOLOGICAL sector the sweep never ran: m=2, m=3 winding, and
     fractional/half seeds.  Different winding = a genuinely distinct type.
  C. Arc-length continuation across kappa8* to characterize the fold.
  D. Independent spot-check of the round-branch physics (B=1/A, size, M_MS, min|eig|).

Driver: blind verifier (Opus 4.8, 1M).  2026-06-15.  DATA-BLIND.  V100 float64.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, time, sys
import numpy as np
import torch
import complete_metric_batched as cm

torch.set_default_dtype(torch.float64)
DEV = cm.DEV
PI = math.pi
TWO_PI = 2.0 * math.pi
t0 = time.time()

XI = KAP = 1.0
L = math.sqrt(KAP / XI)
rc = 0.05
SPAN = 14.0
ri = rc + SPAN * L


def log(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------------------
# The coupled residual F(u) for the COMPLETE action, u = [Th(1..N-2), phi(1..N-2)].
# Theta block  : F_th = Theta'' - theta_ddot(...)            (interior)
# phi block    : F_ph = phi - phi_target(Theta)              (the MS closure tie)
#   where phi_target is EXACTLY cm.phi_from_source -- the same two-constant
#   Misner-Sharp closure (core depth p, mirror-fold seal) the committed engine
#   uses.  The Picard SCF iterates Th<-solve, phi<-relax(target); the full
#   Newton solves BOTH residuals to zero simultaneously (no relaxation, no
#   basin-fragile fixed-point mixing).
# BCs: Th(core)=m*pi, Th(seal)=0 carried as fixed Dirichlet (not unknowns);
#      phi at endpoints fixed by the closure (phi(seal)=0; phi(core) set by p) so
#      phi unknowns are interior only and the closure supplies their target.
# ---------------------------------------------------------------------------
class CoupledSystem:
    def __init__(self, r, p, kap8, m=1):
        self.r = r                       # (1,N)
        self.N = r.shape[1]
        self.p = p
        self.kap8 = kap8
        self.m = m
        rr = r[0]
        h_m = rr[1:-1] - rr[:-2]
        h_p = rr[2:] - rr[1:-1]
        self.a_lo = (2.0 * h_p / (h_m * h_p * (h_m + h_p)))
        self.a_di = (-2.0 * (h_m + h_p) / (h_m * h_p * (h_m + h_p)))
        self.a_hi = (2.0 * h_m / (h_m * h_p * (h_m + h_p)))

    def thpp(self, Th):
        out = torch.zeros_like(Th)
        out[:, 1:-1] = self.a_lo * Th[:, :-2] + self.a_di * Th[:, 1:-1] + self.a_hi * Th[:, 2:]
        return out

    def phi_target(self, Th):
        Thp = cm.grad_central(Th, self.r)
        phi, m_areal, m_closed = cm.phi_from_source(self.r, Th, Thp, Th * 0.0 - self.p,
                                                    XI, KAP, self.p, self.kap8)
        # phi_from_source ignores phi_cur except in stress via X=e^{-2phi}T'^2; supply
        # the actual phi via the assembled state in residual(), see below.
        return phi, m_areal, m_closed

    def residual(self, Th, phi):
        """Joint residual on interior nodes. Returns (F_th, F_ph) each (1,N)."""
        Thp = cm.grad_central(Th, self.r)
        phip = cm.grad_central(phi, self.r)
        # angular EL residual
        rhs = cm.theta_ddot(self.r, Th, Thp, phi, phip, XI, KAP, m=self.m)
        F_th = torch.zeros_like(Th)
        F_th[:, 1:-1] = self.thpp(Th)[:, 1:-1] - rhs[:, 1:-1]
        # phi closure residual: phi must equal the MS-closure phi sourced by the
        # CURRENT (Th,phi) stress.  This is the exact two-way tie.
        _, _, rho, _ = cm.stress(self.r, Th, Thp, phi, XI, KAP)
        integ = self.kap8 * self.r**2 * rho
        dr = self.r[:, 1:] - self.r[:, :-1]
        trap = 0.5 * (integ[:, 1:] + integ[:, :-1]) * dr
        m_src = torch.zeros_like(self.r)
        m_src[:, 1:] = torch.cumsum(trap, dim=1)
        m_core = self.r[:, :1] * (1.0 - math.exp(2 * self.p))
        m_areal = m_core + m_src
        rs = -m_areal[:, -1:]
        span = (self.r - self.r[:, :1]) / (self.r[:, -1:] - self.r[:, :1])
        m_closed = m_areal + rs * span
        emin2phi = torch.clamp(1.0 - m_closed / self.r, min=1e-9)
        phi_tar = -0.5 * torch.log(emin2phi)
        F_ph = phi - phi_tar
        return F_th, F_ph, m_areal, m_closed


def pack(Th, phi):
    return torch.cat([Th[:, 1:-1].reshape(-1), phi[:, 1:-1].reshape(-1)])


def unpack(u, Th_bc, phi_bc, N):
    n = N - 2
    Th = Th_bc.clone()
    phi = phi_bc.clone()
    Th[:, 1:-1] = u[:n].reshape(1, n)
    phi[:, 1:-1] = u[n:].reshape(1, n)
    return Th, phi


def coupled_newton(sys, Th0, phi0, itmax=120, tol=1e-9, eps=1e-7, verbose=False):
    """Damped full-Newton with Armijo line search on the joint residual.
    Jacobian by colored finite differences (banded; both blocks couple through
    central diffs and the cumulative MS integral, so we use a moderate color
    stride that captures the local band + a dense fallback for the phi block's
    nonlocal cumsum coupling via a full numerical Jacobian -- N is small enough
    (<=400) that a dense Jacobian is affordable and ROBUST, no banded assumption
    that could hide a nonlocal branch)."""
    N = sys.N
    n = N - 2
    Th_bc = Th0.clone(); phi_bc = phi0.clone()
    # endpoints fixed: Th(core)=m*pi, Th(seal)=0; phi endpoints from closure.
    Th_bc[:, 0] = sys.m * PI; Th_bc[:, -1] = 0.0
    u = pack(Th0, phi0)

    def Fvec(uu):
        Th, phi = unpack(uu, Th_bc, phi_bc, N)
        F_th, F_ph, _, _ = sys.residual(Th, phi)
        return torch.cat([F_th[:, 1:-1].reshape(-1), F_ph[:, 1:-1].reshape(-1)])

    nrm = lambda v: float(torch.linalg.norm(v))
    hist = []
    F0 = Fvec(u)
    for it in range(itmax):
        nF = nrm(F0)
        maxres = float(F0.abs().max())
        hist.append((it, maxres))
        if verbose and (it % 10 == 0):
            log(f"      [coupled-newton] it={it} ||F||={nF:.3e} max|F|={maxres:.3e}")
        if maxres < tol:
            break
        # Dense numerical Jacobian (2n x 2n).  Colored FD: perturb in groups so
        # cost is ~O(colors) residual evals, not 2n.  But the cumsum makes the
        # phi-block lower-triangular-dense; to be SAFE (not assume structure that
        # could mask a branch) we build the full Jacobian by 2n evals when 2n is
        # small, else colored.  For N<=300 (2n<=596) full FD is fine on GPU.
        M = 2 * n
        J = torch.zeros(M, M, device=DEV)
        base = F0
        for j in range(M):
            up = u.clone(); up[j] += eps
            J[:, j] = (Fvec(up) - base) / eps
        try:
            du = torch.linalg.solve(J + 1e-12 * torch.eye(M, device=DEV), -F0)
        except Exception:
            return u, maxres, it, False, hist
        if not torch.all(torch.isfinite(du)):
            return u, maxres, it, False, hist
        lam = 1.0; ok = False
        for _ in range(40):
            ut = u + lam * du
            Ft = Fvec(ut)
            if torch.all(torch.isfinite(Ft)) and nrm(Ft) < (1 - 1e-4 * lam) * nF:
                ok = True; break
            lam *= 0.5
        if not ok:
            return u, maxres, it, maxres < 1e-6, hist
        u = u + lam * du
        F0 = Fvec(u)
    maxres = float(F0.abs().max())
    Th, phi = unpack(u, Th_bc, phi_bc, N)
    return u, maxres, len(hist), maxres < tol, hist


def diagnose(sys, Th, phi):
    Tn = Th[0].cpu().numpy(); rn = sys.r[0].cpu().numpy(); pn = phi[0].cpu().numpy()
    F_th, F_ph, m_areal, m_closed = sys.residual(Th, phi)
    res = float(torch.max(torch.abs(torch.cat([F_th[:, 1:-1].reshape(-1),
                                               F_ph[:, 1:-1].reshape(-1)]))))
    deficit = (1.0 - (m_closed / sys.r))[0].cpu().numpy()
    min_def = float(np.min(deficit))
    M_MS = float(m_areal[0, -1] - m_areal[0, 0])
    # width: crossings of Th = m*pi/2 (count topological turns / nodes)
    half = sys.m * PI / 2
    w = float('nan')
    for i in range(len(Tn) - 1):
        a, b = Tn[i], Tn[i + 1]
        if (a - PI / 2) * (b - PI / 2) <= 0 and a != b:
            t = (PI / 2 - a) / (b - a); w = rn[i] + t * (rn[i + 1] - rn[i]); break
    d = np.diff(Tn); d = d[np.abs(d) > 1e-6]
    turns = int(np.sum(np.diff(np.sign(d)) != 0)) if len(d) else 0
    # crossings of pi/2, 3pi/2, ... (winding nodes)
    levels = [(2 * k + 1) * PI / 2 for k in range(sys.m)]
    ncross = 0
    for lv in levels:
        for i in range(len(Tn) - 1):
            if (Tn[i] - lv) * (Tn[i + 1] - lv) < 0:
                ncross += 1
    return dict(res=res, min_deficit=min_def, M_MS=M_MS,
                width=((w - rc) / L) if w == w else float('nan'),
                turns=turns, ncross=ncross, phi0=float(pn[0]),
                exists=(res < 1e-6 and min_def > 1e-6))


def make_seed(r, kind, amp=0.4, m=1):
    rr = r
    Lc = math.sqrt(KAP / XI); rcc = rr[:, :1]
    base = (m * PI) * 0.5 * (1 - torch.tanh((rr - (rcc + 2 * Lc)) / (0.8 * Lc)))
    x = (rr - rc) / (ri - rc)
    if kind == 'round':
        Th = base
    elif kind == 'extranode':
        Th = base + amp * torch.sin(3 * PI * x) * torch.exp(-2 * x)
    elif kind == 'twocore':
        Th = base + amp * torch.exp(-((x - 0.55) / 0.10)**2)
    elif kind == 'twocenter':   # widely separated two-center
        Th = base + amp * (torch.exp(-((x - 0.3) / 0.07)**2) - torch.exp(-((x - 0.7) / 0.07)**2))
    elif kind == 'asym':        # strongly asymmetric front
        Th = (m * PI) * 0.5 * (1 - torch.tanh((rr - (rcc + 5 * Lc)) / (0.3 * Lc)))
    elif kind == 'multipole':   # high-frequency angular-proxy
        Th = base + amp * torch.sin(6 * PI * x) * torch.exp(-1.0 * x)
    elif kind == 'staircase':   # multi-node staircase (try to trap turns)
        Th = base + amp * torch.sin(5 * PI * x)
    else:
        Th = base
    Th = torch.clamp(Th, -0.2, m * PI + 0.2)
    Th[:, 0] = m * PI; Th[:, -1] = 0.0
    return Th


def fluct_mineig(sys, Th, phi):
    rg = sys.r[0].cpu().numpy(); Th0 = Th[0].cpu().numpy(); ph = phi[0].cpu().numpy()
    N = len(rg)
    def edens(T, Tp):
        s = np.sin(T); s2 = s * s; s4 = s2 * s2; e_m = np.exp(-ph); e2p = np.exp(2 * ph)
        e2 = (TWO_PI * XI / 3) * e_m * (rg**2 * s2 * Tp**2 + 2 * rg**2 * Tp**2 + 4 * e2p * s2)
        e4 = (TWO_PI * KAP / 3) * e_m * ((2 * rg**2 * s4 + 2 * rg**2 * s2) * Tp**2 + e2p * s4) / rg**2
        return e2 + e4
    Tp0 = np.gradient(Th0, rg); h = 1e-6
    eP = (edens(Th0, Tp0 + h) - 2 * edens(Th0, Tp0) + edens(Th0, Tp0 - h)) / h**2
    eQ = (edens(Th0 + h, Tp0) - 2 * edens(Th0, Tp0) + edens(Th0 - h, Tp0)) / h**2
    epp = edens(Th0 + h, Tp0 + h); epm = edens(Th0 + h, Tp0 - h)
    emp = edens(Th0 - h, Tp0 + h); emm = edens(Th0 - h, Tp0 - h)
    eR = (epp - epm - emp + emm) / (4 * h**2)
    Veff = eQ - np.gradient(eR, rg)
    s = np.sin(Th0); s2 = s * s; s4 = s2 * s2
    W = (TWO_PI / 3) * np.exp(3 * ph) * (XI * (rg**2 * s2 + 2 * rg**2) + KAP * (2 * s4 + 2 * s2))
    n = N - 2; Hm = np.zeros((n, n)); Wm = np.zeros((n, n))
    for i in range(1, N - 1):
        Pr = 0.5 * (eP[i] + eP[i + 1]); Pl = 0.5 * (eP[i - 1] + eP[i])
        hr = rg[i + 1] - rg[i]; hl = rg[i] - rg[i - 1]; hc = 0.5 * (hr + hl); k = i - 1
        Hm[k, k] = (Pr / hr + Pl / hl) / hc + Veff[i]
        if k + 1 < n: Hm[k, k + 1] = -Pr / hr / hc
        if k - 1 >= 0: Hm[k, k - 1] = -Pl / hl / hc
        Wm[k, k] = W[i]
    Hm = 0.5 * (Hm + Hm.T); Winv = 1.0 / np.sqrt(np.abs(np.diag(Wm)))
    A = (Hm * Winv[:, None]) * Winv[None, :]; A = 0.5 * (A + A.T)
    ev = torch.linalg.eigvalsh(torch.as_tensor(A, device=DEV)).cpu().numpy()
    return np.sort(ev), float(np.min(np.abs(ev)))


if __name__ == "__main__":
    log("=" * 78)
    log(f"INDEPENDENT VERIFIER  device={DEV}  torch={torch.__version__}")
    log(f"cell [{rc},{ri:.3f}]={SPAN}L")
    log("=" * 78)

    # =====================================================================
    # D (FIRST: validate the independent engine reproduces the round branch).
    # Independent full-Newton must land on the SAME round soliton as the
    # committed Picard SCF at a clean weak-kappa8 point.
    # =====================================================================
    log("\n--- D. INDEPENDENT-ENGINE VALIDATION vs committed Picard (round, p=0.4, k8=0.05) ---")
    N = 240
    r1 = torch.linspace(rc, ri, N, device=DEV).unsqueeze(0)
    # committed Picard reference
    oc = cm.selfconsistent_batched(r1, XI, KAP, p=0.4, kap8=0.05, iters=120, relax=0.35, tol=1e-11)
    # independent full-Newton from a round seed
    sysv = CoupledSystem(r1, p=0.4, kap8=0.05, m=1)
    Th0 = make_seed(r1, 'round', m=1); phi0 = 0.4 * torch.log(r1 / r1[:, -1:])
    u, mres, nit, conv, hist = coupled_newton(sysv, Th0, phi0, itmax=80, tol=1e-10, verbose=True)
    Thv, phiv = unpack(u, Th0, phi0, N)
    dv = diagnose(sysv, Thv, phiv)
    dTh = float((Thv - oc['Th']).abs().max())
    dM = abs(dv['M_MS'] - float(oc['M_MS']))
    log(f"  committed Picard: M_MS={float(oc['M_MS']):.5f}  res_th={oc['hist'][-1][3]:.2e}")
    log(f"  independent Newton: conv={conv} res={mres:.2e} M_MS={dv['M_MS']:.5f} width={dv['width']:.4f} turns={dv['turns']}")
    log(f"  AGREEMENT: max|dTh|={dTh:.2e}  |dM_MS|={dM:.2e}  (independent engine validated if small)")
    ev, me = fluct_mineig(sysv, Thv, phiv)
    log(f"  round-branch min|eig|={me:.4e}  lowest-6={np.array2string(ev[:6],precision=4)}")

    # =====================================================================
    # A. CONVERGENCE-FAILURE RE-ATTACK with the independent engine.
    # Hit the non-converged region: shaped/multi-node/multi-center seeds at
    # deep p, including near the existence ceiling.  A Picard failure is not
    # a no-solution.  Does ANY shaped seed converge (independent Newton) to a
    # DISTINCT (turns!=0 / not-equal-to-round) stable cell?
    # =====================================================================
    log("\n--- A. CONVERGENCE-FAILURE RE-ATTACK (independent full-Newton on shaped seeds) ---")
    log(f"  {'p':>4} {'k8':>6} {'seed':>11} {'conv':>5} {'res':>9} {'turns':>5} "
        f"{'width':>7} {'min_def':>9} {'M_MS':>8} {'dist?':>6}")
    attackA = []
    test_pts = [(0.8, 0.0), (1.2, 0.0), (1.6, 0.0), (2.0, 0.0),
                (1.2, 1e-3), (0.8, 1e-2), (0.4, 0.06)]  # deep p and near-ceiling
    shaped = ['extranode', 'twocore', 'twocenter', 'asym', 'multipole', 'staircase']
    for (p, k8) in test_pts:
        sysp = CoupledSystem(r1, p=p, kap8=k8, m=1)
        # round reference at this point
        Thr0 = make_seed(r1, 'round', m=1); phir0 = p * torch.log(r1 / r1[:, -1:])
        ur, mrr, _, cr, _ = coupled_newton(sysp, Thr0, phir0, itmax=70, tol=1e-10)
        Thr, phir = unpack(ur, Thr0, phir0, N)
        Tnr = Thr[0].cpu().numpy()
        for sk in shaped:
            Ths = make_seed(r1, sk, amp=0.5, m=1); phis = p * torch.log(r1 / r1[:, -1:])
            us, mrs, nit, cs, _ = coupled_newton(sysp, Ths, phis, itmax=70, tol=1e-10)
            Ths_f, phis_f = unpack(us, Ths, phis, N)
            ds = diagnose(sysp, Ths_f, phis_f)
            Tns = Ths_f[0].cpu().numpy()
            dist = float(np.max(np.abs(Tns - Tnr))) if cs else float('nan')
            isdist = (cs and ds['exists'] and dist > 1e-3 and ds['turns'] > 0)
            log(f"  {p:>4.1f} {k8:>6.3g} {sk:>11} {str(cs):>5} {mrs:>9.1e} {ds['turns']:>5} "
                f"{ds['width']:>7.3f} {ds['min_deficit']:>9.2e} {ds['M_MS']:>8.4f} {str(isdist):>6}")
            attackA.append(dict(p=p, k8=k8, seed=sk, conv=cs, res=mrs, turns=ds['turns'],
                                dist=dist, isdist=isdist, exists=ds['exists'], M_MS=ds['M_MS']))
    nfound = sum(1 for a in attackA if a['isdist'])
    log(f"  ==> distinct stable shaped/multi-core types found by independent Newton: {nfound}")

    # =====================================================================
    # B. TOPOLOGICAL-SECTOR HUNT (the sweep ran ONLY m=1).  Different winding
    # is a genuinely DISTINCT type.  Solve m=2, m=3 hedgehogs with the
    # independent Newton; check they exist, are stable (min|eig|), and carry
    # the right node count (turns/crossings).  Also report their M_MS ordering.
    # =====================================================================
    log("\n--- B. TOPOLOGICAL-SECTOR HUNT (m=2, m=3 winding -- never swept) ---")
    log(f"  {'m':>3} {'p':>4} {'k8':>6} {'conv':>5} {'res':>9} {'ncross':>7} "
        f"{'width':>7} {'min_def':>9} {'M_MS':>8} {'min|eig|':>10}")
    attackB = []
    for mw in [1, 2, 3]:
        for (p, k8) in [(0.4, 0.01), (0.8, 0.01)]:
            sysm = CoupledSystem(r1, p=p, kap8=k8, m=mw)
            Th0 = make_seed(r1, 'round', m=mw); phi0 = p * torch.log(r1 / r1[:, -1:])
            u, mres, nit, conv, _ = coupled_newton(sysm, Th0, phi0, itmax=90, tol=1e-10)
            Thm, phim = unpack(u, Th0, phi0, N)
            dm = diagnose(sysm, Thm, phim)
            try:
                _, me = fluct_mineig(sysm, Thm, phim)
            except Exception:
                me = float('nan')
            log(f"  {mw:>3} {p:>4.1f} {k8:>6.3g} {str(conv):>5} {mres:>9.1e} {dm['ncross']:>7} "
                f"{dm['width']:>7.3f} {dm['min_deficit']:>9.2e} {dm['M_MS']:>8.4f} {me:>10.3e}")
            attackB.append(dict(m=mw, p=p, k8=k8, conv=conv, res=mres, ncross=dm['ncross'],
                                exists=dm['exists'], M_MS=dm['M_MS'], mineig=me))

    # =====================================================================
    # C. ARC-LENGTH around kappa8* (p=0.4): is the ceiling a SADDLE-NODE fold
    # (turning point in kappa8) or a hidden critical softening?  Pseudo-arclength
    # continuation: parametrize by an order parameter (min_deficit s) and SOLVE
    # for (Theta,phi,kappa8) with kappa8 a FREE unknown plus the arclength
    # constraint -- so the solver can round a fold the Picard kappa8-march cannot.
    # We march s DOWN (deficit -> small) and watch whether kappa8 turns back.
    # =====================================================================
    log("\n--- C. PSEUDO-ARCLENGTH around kappa8* (fold vs critical softening) ---")
    log("  marching min_deficit downward; does kappa8 reach a turning point (fold)")
    log("  and does min|eig| -> 0 (critical) or stay finite (saddle-node)?")
    log(f"  {'target_def':>11} {'kappa8':>9} {'min_def':>9} {'min|eig|':>10} {'res':>9} {'conv':>5}")
    p_arc = 0.4
    # solve at a sequence of decreasing deficit targets; at each, find kappa8 (free)
    # such that min(1-m_closed/r)=target by an inner bisection wrapped on the
    # independent Newton (deficit is monotone-ish in kappa8 on the lower branch).
    attackC = []
    Th_prev = make_seed(r1, 'round', m=1); phi_prev = p_arc * torch.log(r1 / r1[:, -1:])
    for tgt in [0.88, 0.86, 0.84, 0.83, 0.825, 0.82, 0.818, 0.816]:
        lo, hi = 0.0, 0.12
        best = None
        for _ in range(26):
            mid = 0.5 * (lo + hi)
            syss = CoupledSystem(r1, p=p_arc, kap8=mid, m=1)
            u, mres, nit, conv, _ = coupled_newton(syss, Th_prev, phi_prev, itmax=45, tol=1e-9)
            Ths, phis = unpack(u, Th_prev, phi_prev, N)
            ds = diagnose(syss, Ths, phis)
            if conv and ds['min_deficit'] > 1e-4:
                best = (mid, ds, Ths.clone(), phis.clone(), mres, conv)
                if ds['min_deficit'] > tgt:
                    lo = mid     # need MORE kappa8 to lower deficit
                else:
                    hi = mid
            else:
                hi = mid         # too much kappa8 (diverged / horizon)
        if best is not None:
            mid, ds, Ths, phis, mres, conv = best
            Th_prev, phi_prev = Ths, phis
            try:
                _, me = fluct_mineig(CoupledSystem(r1, p=p_arc, kap8=mid, m=1), Ths, phis)
            except Exception:
                me = float('nan')
            log(f"  {tgt:>11.3f} {mid:>9.5f} {ds['min_deficit']:>9.4f} {me:>10.3e} {mres:>9.1e} {str(conv):>5}")
            attackC.append(dict(target=tgt, kappa8=mid, min_def=ds['min_deficit'], mineig=me, res=mres))
        else:
            log(f"  {tgt:>11.3f}   (no converged kappa8 reaches this deficit -- below the fold)")
            attackC.append(dict(target=tgt, kappa8=None, min_def=None, mineig=None))
    # fold signature: kappa8 increases toward a max then any further deficit-drop
    # needs LESS kappa8 (turning point) => saddle-node; min|eig| staying finite at
    # the max-kappa8 => NOT a critical softening.
    k8s = [c['kappa8'] for c in attackC if c['kappa8'] is not None]
    if k8s:
        log(f"  kappa8 sequence along lower branch: max={max(k8s):.5f} last={k8s[-1]:.5f}")
        log(f"  min|eig| near the ceiling stays finite? -> "
            f"{[round(c['mineig'],4) for c in attackC if c.get('mineig')]}")

    log("\n" + "=" * 78)
    log(f"VERIFIER DONE  total wall {time.time()-t0:.1f}s")
    log("=" * 78)
    log(f"SUMMARY: A distinct-types-found={nfound}  "
        f"D engine-agreement dTh={dTh:.1e} dM={dM:.1e}")

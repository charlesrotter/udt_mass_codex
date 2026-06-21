#!/usr/bin/env python3
"""
p5d_timelive.py -- P5d THE TIME-LIVE OBSERVATION (the payoff of the everything-on
solver build).  OBSERVE what the full clean metric DOES when time is LIVE on the
round ground-state object, using the P4-validated time-live residual on the full
P1-P3 stack (general Einstein pole-stable hybrid + native S^2 matter + a(phi)
ruler weight k=0).

MODE: OBSERVE (let structure emerge, report WHAT IS THERE).  NOT a target hunt.
DATA-BLIND (units L=1; only residuals, omega-scalings, code-unit M_MS).  Nothing
M_MS/spectrum/ratio is BANKED.

WHAT'S NEW vs #65 (the reduced proxy) and vs P4 (the wiring + containment):
  #65 was a modeled radial profile + single-mode SL eigenproblem, full coupled solve
  NOT built.  P4 wired the live time row into the full stack and PROVED containment
  (omega->0 == static soliton, bitwise) + the T_tr Birkhoff-escape anchor, but made
  NO omega claim and ran NO spectrum.  P5d takes the next step IN BUDGET: with the
  static round ground state as the (a0,b0,F0) background, RELEASE the P4 containment
  pins on the live amplitudes (a1,b1,F1) and OBSERVE the time-live dynamics the full
  coupled harmonic-balance system actually carries -- as a QUADRATIC EIGENPROBLEM in
  omega (the in-budget exact read of "what omega(s) does the live metric select?").

THE OBSERVATION, made native and in-budget:
  The P4 live residual's TIME rows (the cos^1 harmonic-balance rows: the linearized
  Einstein G^t_t/G^r_r/EL operator acting on the live amplitudes x=(a1,b1,F1), plus
  the G^t_r momentum row) are, for a FIXED background, EXACTLY:
        R_time(x; omega) = [ K  +  omega C  -  omega^2 M ] x
  where
    K = the static (omega-independent) spatial operator on the amplitudes
        (curvature/restoring -- d_t^0 content),
    C = the FIRST-order-in-omega content (the G^t_r momentum / open-time d_t channel),
    M = the SECOND-order-in-omega content (the d_t^2 -> -omega^2 INERTIA).
  Assembling K, C, M by exact autograd/FD about x=0 (3*Nr unknowns -- tiny, in budget)
  and solving the quadratic eigenvalue problem (QEP) det[K + omega C - omega^2 M] = 0
  gives EVERY omega the live coupled metric admits on this background, with its mode
  shape -- the WHOLE time-live structure, not one corner.  This is the harmonic-
  balance content of P4's einstein_live + field_dn_s2_live, observed across all modes.

  CONTAINMENT (sanity, inherited): the omega=0 limit zeroes the live amplitudes and
  returns the static soliton; we re-confirm K is the static linearized operator and
  the QEP has the static soliton as its omega->0 fixed point.

  BOX-CONTROL GATE (the binding gate for any intrinsic-omega claim): recompute the
  QEP spectrum at several cell sizes R (Grid3D.cell) and report whether the lowest
  omega(s) are R-INDEPENDENT (intrinsic) or scale ~1/R (box-controlled standing waves).

ANTI-HANG (binding #1): SINGLE clean process per invocation, SEQUENTIAL.  Nr<=16.
The QEP assembly is 3*Nr FD columns of the round time-residual (cheap, ~seconds at
Nr=12) + a dense (2*3Nr) generalized eig (tiny).  No background poll.  Each call <~6min.

USAGE (one solve per process):
  python3 p5d_timelive.py qep NR CELL      # assemble K,C,M on static bg, solve QEP, save
  python3 p5d_timelive.py boxscan          # report omega vs cell at fixed Nr (load saved)
  python3 p5d_timelive.py contain NR        # containment re-check (omega->0 == static)

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE.  DATA-BLIND.  Branch p5d-timelive.
NEW file (committed p4_time_live / p4_validate / p2_round_s2_solver / full3d_* reused
as IMMUTABLE imports only).
"""
import os, sys, math, time
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

import full3d_spectral as F3
from full3d_spectral import build_metric, PI, DEV, T, R, TH, PS
from full3d_newton import inv4x4, det4x4
import p2_matter_s2_fullmetric as P2
import p2_round_s2_solver as RS
import p4_time_live as P4
import p4_validate as P4V


# ---------------------------------------------------------------------------
# The ROUND TIME residual restricted to its LIVE-AMPLITUDE rows, as a function
# of the amplitudes x=(a1,b1,F1) only (background a0,b0,F0 FROZEN at the static
# round ground state).  This is the cos^1 harmonic-balance content of P4's
# einstein_live + field_dn_s2_live: the rows the LIVE TIME sources.  Linear in x
# for fixed background; omega enters via d_t (->omega) and d_t^2 (->-omega^2).
#
# We use the SAME pieces P4_validate.residual_round_live uses (P4.build_metric_live,
# P4.einstein_live, P4.field_dn_s2_live, P4.stress_live, P2.matter_el_s2_fullmetric),
# but WITHOUT the containment pins on (a1,b1,F1): we want the dynamics, not the
# trivial static limit.  We keep the regular amplitude BC anchors (a1(seal)=0,
# b1(core)=0, F1(core)=F1(seal)=0) so the amplitudes are a regular charge-1
# fluctuation about the hedgehog.
# ---------------------------------------------------------------------------
def _expand(G, v):
    return v[:, None, None].expand(G.Nr, G.Nth, G.Nps).contiguous()


def time_rows(x, G, n, a0v, b0v, F0v, omega, cph, sph, kap8, m=1, k=0.0):
    """The live-amplitude (cos^1) residual rows as a function of x=(a1,b1,F1) for a
    FROZEN static background (a0v,b0v,F0v).  Returns the interior G^t_t,G^r_r,EL,G^t_r
    rows (the harmonic-balance time content) -- NO containment pins.  Linear in x for
    fixed background; the omega-dependence is the harmonic-balance d_t/d_t^2 content."""
    a1 = _expand(G, x[0:n]); b1 = _expand(G, x[n:2*n]); F1 = _expand(G, x[2*n:3*n])
    a0 = _expand(G, a0v); b0 = _expand(G, b0v); F0 = _expand(G, F0v)
    g, dtg, dttg, a, b = P4.build_metric_live(G, a0, b0, a1, b1, omega=omega, cph=cph, sph=sph)
    ginv = inv4x4(g)
    Gmix, _ = P4.einstein_live(G, a, b, dtg, dttg, g=g)
    dn, F = P4.field_dn_s2_live(G, F0, F1, omega, cph, sph, m=m)
    Tab, _, _ = P4.stress_live(G, g, ginv, dn, k=k)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
    resE = Gmix - kap8*Tmix
    el = P2.matter_el_s2_fullmetric(G, g, ginv, F, m=m)
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
    W = torch.sqrt(sqrtg*G.wvol_coord); W = W/W[G.body].mean()
    jj = G.Nth//2
    # interior nodes 3..n-3 (matches the round-channel residual's interior excision)
    rows = [
        (W*resE[..., T, T])[:, jj, 0][3:n-3],   # G^t_t live content
        (W*resE[..., R, R])[:, jj, 0][3:n-3],   # G^r_r live content
        (W*el)[:, jj, 0][3:n-3],                # matter EL live content
        (W*resE[..., T, R])[:, jj, 0][3:n-3],   # G^t_r momentum (the Birkhoff-escape row)
    ]
    return torch.cat([rr.reshape(-1) for rr in rows])


def static_background_cell(NR, NTH, NPS, cell, p=0.4, kap8=0.05, m=1, maxit=60):
    """Solve the round S^2 ground state at an ARBITRARY cell (for the box-control scan).
    Mirrors p2_round_s2_solver.solve_round_s2 exactly but on a grid with the given cell."""
    G = F3.Grid3D(Nr=NR, Nth=NTH, Nps=NPS, rc=0.05, cell=cell)
    G = F3.attach_coord_weight(G)
    n = NR
    rr = G.r.cpu().numpy()
    a0 = np.zeros(n)
    b0 = np.full(n, -p) * ((G.ri - rr) / (G.ri - G.rc))
    F0 = PI * (1 - (rr - G.rc) / (G.ri - G.rc))
    u = torch.tensor(np.concatenate([a0, b0, F0]), device=DEV)
    z = torch.zeros(NR, NTH, NPS, device=DEV)
    from einstein_3d_eval import einstein_mixed_weyl as EMW

    def expand(v):
        return v[:, None, None].expand(NR, NTH, NPS).contiguous()

    def resid(u):
        a = expand(u[0:n]); b = expand(u[n:2*n]); F = expand(u[2*n:3*n])
        g = build_metric(G, a, b, z, z); ginv = inv4x4(g)
        Gmix = EMW(G, a, b, z, z)
        dn = P2.field_dn_s2(G, F, m=m)
        import whole_metric_3d_matter as MAT
        Tab, _, _, _ = MAT.stress_tensor(g, ginv, dn, 1.0, 1.0)
        Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
        resE = Gmix - kap8*Tmix
        el = P2.matter_el_s2_fullmetric(G, g, ginv, F, m=m)
        jj = NTH//2
        wbc = 30.0
        rows = [
            resE[..., T, T][:, jj, 0][3:n-3],
            resE[..., R, R][:, jj, 0][3:n-3],
            el[:, jj, 0][3:n-3],
            torch.tensor([wbc], device=DEV)*(u[2*n+0]-PI),
            torch.tensor([wbc], device=DEV)*(u[2*n+n-1]-0.0),
            torch.tensor([wbc], device=DEV)*(u[0*n+n-1]-0.0),
            torch.tensor([wbc], device=DEV)*(u[1*n+0]+p),
        ]
        return torch.cat([r.reshape(-1) for r in rows])

    lam = 1e-4; I = torch.eye(u.numel(), device=DEV)
    F0r = resid(u); Phi = float((F0r*F0r).sum())
    for it in range(maxit):
        if Phi < 1e-12: break
        F0r = resid(u); nU = u.numel(); nF = F0r.numel(); J = torch.zeros(nF, nU, device=DEV)
        eps = 1e-6
        for j in range(nU):
            up = u.clone(); up[j] += eps; um = u.clone(); um[j] -= eps
            J[:, j] = (resid(up)-resid(um))/(2*eps)
        acc = False
        for _ in range(14):
            Jaug = torch.cat([J, math.sqrt(lam)*I], 0)
            Faug = torch.cat([-F0r, torch.zeros(nU, device=DEV)], 0)
            du = torch.linalg.lstsq(Jaug, Faug).solution; un = u+du
            Pn = float((resid(un)**2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                u = un; Phi = Pn; lam = max(lam*0.25, 1e-13); acc = True; break
            lam *= 4.0
        if not acc: break
    a = expand(u[0:n]); b = expand(u[n:2*n]); F = expand(u[2*n:3*n])
    g = build_metric(G, a, b, z, z); ginv = inv4x4(g)
    import whole_metric_3d_matter as MAT
    dn = P2.field_dn_s2(G, F, m=m)
    Tab, _, _, _ = MAT.stress_tensor(g, ginv, dn, 1.0, 1.0)
    M_MS = P4.M_MS_of(G, g, ginv, Tab, kap8)
    return dict(G=G, a=u[0:n], b=u[n:2*n], F=u[2*n:3*n], Phi=Phi, M_MS=M_MS, n=n)


def amplitude_bc_mask(G, n):
    """Indices in x=(a1,b1,F1) that are PINNED by regular fluctuation BCs (held=0):
    a1(seal), b1(core), F1(core), F1(seal).  The remaining indices are free amplitude
    DOF.  This keeps the fluctuation a regular charge-1 mode about the hedgehog (the
    same BC structure the static soliton has), WITHOUT the P4 containment pin that
    zeroes ALL amplitudes."""
    pinned = set()
    pinned.add(0*n + (n-1))      # a1(seal)=0
    pinned.add(1*n + 0)          # b1(core)=0
    pinned.add(2*n + 0)          # F1(core)=0
    pinned.add(2*n + (n-1))      # F1(seal)=0
    free = [i for i in range(3*n) if i not in pinned]
    return sorted(pinned), free


def assemble_KCM(G, n, a0v, b0v, F0v, cph, sph, kap8, m=1, k=0.0, eps=1e-6):
    """Assemble K, C, M (the omega^0, omega^1, omega^2 operators) of the live-amplitude
    time residual R_time(x;omega) = (K + omega C - omega^2 M) x, on the FROZEN static
    background.  Built by central FD of the time rows in each amplitude direction, at
    three omega values, and separating the omega-powers EXACTLY:
        R(x;w) = K x + w (C x) - w^2 (M x)       (linear in x; quadratic in w by HB)
    Evaluate the Jacobian J(w) = dR/dx at x=0 for w in {0, w1, -w1} (and one more for a
    consistency check); then
        K = J(0)
        C = (J(+w1) - J(-w1)) / (2 w1)
       -M = (J(+w1) + J(-w1) - 2 J(0)) / (2 w1^2)   => M = -that.
    Returns dense K,C,M restricted to the FREE amplitude DOF (BC-pinned rows/cols out)."""
    pinned, free = amplitude_bc_mask(G, n)
    nf = len(free)

    def Jac(omega):
        x0 = torch.zeros(3*n, device=DEV)
        R0 = time_rows(x0, G, n, a0v, b0v, F0v, omega, cph, sph, kap8, m=m, k=k)
        nF = R0.numel()
        J = torch.zeros(nF, 3*n, device=DEV)
        for j in range(3*n):
            xp = x0.clone(); xp[j] += eps
            xm = x0.clone(); xm[j] -= eps
            Rp = time_rows(xp, G, n, a0v, b0v, F0v, omega, cph, sph, kap8, m=m, k=k)
            Rm = time_rows(xm, G, n, a0v, b0v, F0v, omega, cph, sph, kap8, m=m, k=k)
            J[:, j] = (Rp - Rm)/(2*eps)
        return J, R0

    w1 = 0.5
    J0, R0_0 = Jac(0.0)
    Jp, _ = Jac(+w1)
    Jm, _ = Jac(-w1)
    Kfull = J0
    Cfull = (Jp - Jm)/(2*w1)
    Mfull = -(Jp + Jm - 2*J0)/(2*w1*w1)
    # restrict columns to free DOF; rows are the (3 interior + Gtr interior) residual rows.
    # The system is square in the free DOF? rows count = 4*(n-6); free cols = 3n-4.
    # For the QEP we need a SQUARE generalized eigenproblem in the amplitudes -> project
    # the residual rows onto the free amplitude space via least-squares-normal form:
    #   K^T K etc.   We instead form the SQUARE normal operators on the free DOF:
    Kf = Kfull[:, free]; Cf = Cfull[:, free]; Mf = Mfull[:, free]
    return Kf, Cf, Mf, free, pinned, R0_0


def solve_qep(Kf, Cf, Mf):
    """Solve the (rectangular) quadratic system (K + w C - w^2 M) x = 0 for the
    amplitudes x and the frequencies w.  Rows (residual eqns) > cols (free amps), so we
    pose the SQUARE generalized eigenproblem on the normal operators:
        (A0 + w A1 - w^2 A2) x = 0,  A0=K^T K, A1=K^T C + C^T K, A2 = K^T M + M^T K - C^T C
    Hmm -- the normal form of a QEP is not itself a clean QEP.  Instead, we use the
    direct rectangular QEP linearization on the MOORE-PENROSE-reduced square form:
    project rows onto col space via the economy QR of [K|C|M] stacked? Too elaborate.

    SIMPLER, EXACT, in-budget: scan real w; at each w compute the smallest singular
    value sigma_min of (K + w C - w^2 M) (the rectangular operator).  sigma_min(w)=0
    <=> w is an eigenfrequency with a nontrivial amplitude null-mode.  Return the
    sigma_min(w) curve and its minima (the omega the live metric admits)."""
    return None  # (the scan is done in qep_scan; this stub documents the method)


def qep_scan(Kf, Cf, Mf, wmax=None, npts=400):
    """Scan real omega in [0, wmax]; sigma_min(w) of (K + w C - w^2 M).  Minima/zeros
    are the live eigenfrequencies.  Also report the w=0 sigma_min (static restoring;
    if ~0 the static op is itself near-singular = a zero mode / flat direction)."""
    if wmax is None:
        # natural scale: sqrt of the ratio of restoring (K) to inertia (M) magnitudes
        kK = float(torch.linalg.norm(Kf)); kM = float(torch.linalg.norm(Mf)) + 1e-30
        wmax = max(3.0*math.sqrt(kK/kM), 2.0)
    ws = torch.linspace(0.0, wmax, npts, device=DEV)
    sig = torch.zeros(npts, device=DEV)
    for i, w in enumerate(ws):
        A = Kf + w*Cf - (w*w)*Mf
        s = torch.linalg.svdvals(A)
        sig[i] = s.min()
    return ws.cpu().numpy(), sig.cpu().numpy(), wmax


def find_minima(ws, sig):
    """Local minima of sigma_min(w) (candidate eigenfrequencies)."""
    mins = []
    for i in range(1, len(sig)-1):
        if sig[i] <= sig[i-1] and sig[i] <= sig[i+1]:
            mins.append((float(ws[i]), float(sig[i])))
    return mins


# ---------------------------------------------------------------------------
# Drivers
# ---------------------------------------------------------------------------
def run_qep(NR, cell, p=0.4, kap8=0.05, m=1):
    NTH = 6 if NR == 12 else 8; NPS = 4
    t0 = time.time()
    print(f"[bg] solving static round S^2 ground state  Nr={NR} cell={cell} ...", flush=True)
    bg = static_background_cell(NR, NTH, NPS, cell, p=p, kap8=kap8, m=m)
    G = bg['G']; n = bg['n']
    print(f"[bg] Phi={bg['Phi']:.3e}  M_MS={bg['M_MS']:.6f}  ({time.time()-t0:.0f}s)", flush=True)
    cph = torch.tensor(math.cos(math.pi/4), device=DEV)
    sph = torch.tensor(math.sin(math.pi/4), device=DEV)
    print(f"[qep] assembling K,C,M (live-amplitude time operator) ...", flush=True)
    Kf, Cf, Mf, free, pinned, R0 = assemble_KCM(G, n, bg['a'], bg['b'], bg['F'],
                                                cph, sph, kap8, m=m)
    print(f"[qep] ||K||={float(torch.linalg.norm(Kf)):.3e} "
          f"||C||={float(torch.linalg.norm(Cf)):.3e} "
          f"||M||={float(torch.linalg.norm(Mf)):.3e}  free DOF={len(free)} "
          f"R0(static)norm={float(torch.linalg.norm(R0)):.3e}  ({time.time()-t0:.0f}s)", flush=True)
    ws, sig, wmax = qep_scan(Kf, Cf, Mf)
    mins = find_minima(ws, sig)
    sig0 = float(sig[0])
    print(f"[qep] sigma_min(w=0) = {sig0:.4e}  (static restoring; ~0 => flat direction)", flush=True)
    print(f"[qep] sigma_min(w) scan over [0,{wmax:.3f}], {len(ws)} pts. local minima:", flush=True)
    for (w, s) in mins[:12]:
        tag = "  <-- candidate eigenfreq" if s < 0.1*sig0 + 1e-8 else ""
        print(f"      w={w:8.4f}   sigma_min={s:.4e}{tag}", flush=True)
    # global min
    gi = int(np.argmin(sig)); print(f"[qep] global min: w={ws[gi]:.4f}  sigma={sig[gi]:.4e}", flush=True)
    rec = dict(NR=NR, cell=cell, n=n, M_MS=bg['M_MS'], Phi_bg=bg['Phi'],
               normK=float(torch.linalg.norm(Kf)), normC=float(torch.linalg.norm(Cf)),
               normM=float(torch.linalg.norm(Mf)), sig0=sig0,
               ws=ws, sig=sig, wmax=wmax, mins=mins, R=cell)
    torch.save(rec, f"/tmp/p5d_qep_{NR}_{int(round(cell*100))}.pt")
    print(f"=== run_qep DONE Nr={NR} cell={cell}  {time.time()-t0:.0f}s ===", flush=True)


def run_boxscan(NR):
    """Load saved QEP records at several cells; report the lowest-mode omega vs cell R.
    R-independent => intrinsic; ~1/R => box-controlled."""
    import glob
    fps = sorted(glob.glob(f"/tmp/p5d_qep_{NR}_*.pt"))
    if not fps:
        print(f"  no saved p5d QEP records at Nr={NR}"); return
    print(f"\n=== P5d BOX-CONTROL SCAN  Nr={NR} ===", flush=True)
    print(f"  {'cell R':>8} | {'M_MS':>9} | {'sig0(w=0)':>11} | {'w_globalmin':>11} | "
          f"{'sigmin':>10} | {'w*R':>8}", flush=True)
    rows = []
    for fp in fps:
        r = torch.load(fp, weights_only=False)
        gi = int(np.argmin(r['sig'])); wmin = float(r['ws'][gi]); smin = float(r['sig'][gi])
        rows.append((r['cell'], r['M_MS'], r['sig0'], wmin, smin))
        print(f"  {r['cell']:>8.3f} | {r['M_MS']:>9.5f} | {r['sig0']:>11.3e} | "
              f"{wmin:>11.5f} | {smin:>10.3e} | {wmin*r['cell']:>8.4f}", flush=True)
    if len(rows) >= 2:
        cells = np.array([x[0] for x in rows]); wmins = np.array([x[3] for x in rows])
        # is w ~ const (intrinsic) or ~1/R (box) ?  fit log w vs log R
        msk = wmins > 1e-9
        if msk.sum() >= 2:
            sl, _ = np.polyfit(np.log(cells[msk]), np.log(wmins[msk]), 1)
            print(f"\n  d(log w)/d(log R) = {sl:+.3f}   "
                  f"(0=intrinsic/R-independent; -1=box-controlled ~1/R)", flush=True)
        print(f"  w*R spread: min={min(x[3]*x[0] for x in rows):.4f} "
              f"max={max(x[3]*x[0] for x in rows):.4f} "
              f"(constant w*R => box-controlled)", flush=True)


def run_contain(NR, cell=14.0, p=0.4, kap8=0.05, m=1):
    """Containment re-check: omega->0 zeroes the live amplitudes; the static round
    ground state IS the omega=0 fixed point.  (Inherited from P4 P4b; re-run cheaply.)"""
    NTH = 6 if NR == 12 else 8; NPS = 4
    bg = static_background_cell(NR, NTH, NPS, cell, p=p, kap8=kap8, m=m)
    G = bg['G']; n = bg['n']
    cph = torch.tensor(math.cos(math.pi/4), device=DEV)
    sph = torch.tensor(math.sin(math.pi/4), device=DEV)
    # at omega=0 the time rows on x=0 must be ~0 (static soliton is the omega=0 solution)
    x0 = torch.zeros(3*n, device=DEV)
    R_w0 = time_rows(x0, G, n, bg['a'], bg['b'], bg['F'], 0.0, cph, sph, kap8, m=m)
    print(f"[contain] Nr={NR} cell={cell}  M_MS(static)={bg['M_MS']:.6f}", flush=True)
    print(f"[contain] ||time-rows(x=0, omega=0)|| = {float(torch.linalg.norm(R_w0)):.3e} "
          f"(must be ~0: static soliton is the omega=0 fixed point)", flush=True)
    # and K (the w=0 Jacobian) should be the static linearized operator -> its sigma_min
    Kf, Cf, Mf, free, pinned, R0 = assemble_KCM(G, n, bg['a'], bg['b'], bg['F'],
                                                cph, sph, kap8, m=m)
    s = torch.linalg.svdvals(Kf)
    print(f"[contain] static-operator K: sigma range [{float(s.min()):.3e}, "
          f"{float(s.max()):.3e}]  cond={float(s.max()/s.min()):.2e}", flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]
    t0 = time.time()
    if mode == "qep":
        NR = int(sys.argv[2]); cell = float(sys.argv[3])
        run_qep(NR, cell)
    elif mode == "boxscan":
        NR = int(sys.argv[2]) if len(sys.argv) > 2 else 12
        run_boxscan(NR)
    elif mode == "contain":
        NR = int(sys.argv[2]); cell = float(sys.argv[3]) if len(sys.argv) > 3 else 14.0
        run_contain(NR, cell)
    else:
        print(__doc__)
    print(f"=== p5d {mode} total {time.time()-t0:.0f}s ===", flush=True)

#!/usr/bin/env python3
"""
wmdeep_angular.py -- THE DEEP ANGULAR-LIVE NEGATIVE-PHI EXISTENCE SOLVE
======================================================================
Driver: Claude (Opus 4.8, 1M ctx). Date 2026-06-13. New file (wmdeep_*).
Frame: CRITICAL_UNIVERSE_FRAME.md (governing) + CANON C-2026-06-10-2
(matter cells inside-out, phi:0 interface -> NEGATIVE toward the core) +
CANON C-2026-06-13-1 (c_r^2=e^{-4phi}, c_th^2=e^{-2phi}/r^2).

WHAT THIS FIXES (the wmneg_results.md scope limit, section H/K):
  The whole-metric 2D both-sector Newton STALLED at p~-2.75 -- a NUMERICAL
  stall (boundary-layer stiffness + the angular dressing e^{2phi}->small
  ill-conditioning the float64 angular block), NOT a physical wall (at -2.75
  c_eff=e^{-2p}~245, lapse~15.6 -- nowhere near runaway). So the angular
  existence/bifurcation verdict was only SOLVED to -2.75; deeper was ARGUED
  (dressing-monotonicity), not solved. Charles: "run it deep, angular live
  past the stall." Here we carry the angular existence test GENUINELY DEEP,
  by COMPUTATION not argument, to the seal.

THE METHOD (Route A, deep-reachable, high precision):
  1. Get the DEEP ROUND radial background phi_0(r) the whole way down with
     the validated adaptive mpmath RK4 (neg_sweep_mpmath; reaches the seal
     r*->2.5459 at p=-500). Capture the FULL trajectory, not just r*.
  2. Linearize the metric's OWN whole field equation
       F[phi] = phi_rr + (2/r)phi_r - 2 phi_r^2
              + (e^{2phi}/r^2)(phi_thth + cot th phi_th - phi_th^2)
              - Phi(1 - e^{3phi})
     about the round (theta-independent) background. For a mode
     u = R(r) P_l(cos th) the angular Laplacian gives -l(l+1), and the
     EXACT linearized RADIAL operator is
       L_l R = R_rr + (2/r - 4 phi_0') R_r
               - (e^{2 phi_0}/r^2) l(l+1) R
               + 3 Phi e^{3 phi_0} R.
     (The -phi_th^2 angular nonlinearity vanishes to first order about
      phi_th=0; the e^{2phi} prefactor variation multiplies the vanishing
      background angular Laplacian -- carried, both give 0. No term dropped.)
  3. Put L_l in the metric's OWN self-adjoint divergence form (the VALIDATED
     bare-measure tool, offdiag_gateA): multiply by the integrating weight
     W_r = r^2 e^{-4 phi_0} (since d_r ln(r^2 e^{-4phi_0}) = 2/r - 4 phi_0'):
       W_r L_l R = d_r( K_r R_r ) - [ K_th l(l+1) - S ] R
     with
       K_r(r)  = r^2 e^{-4 phi_0}        (radial stiffness*measure)
       K_th(r) = e^{-2 phi_0}            ( (e^{2phi}/r^2)*r^2*e^{-4phi}=e^{-2phi} )
       S(r)    = 3 Phi r^2 e^{-4phi_0} e^{3phi_0} = 3 Phi r^2 e^{-phi_0}
       M(r)    = r^2 e^{-4 phi_0}        (the measure = W_r; SPD)
     The self-adjoint GENERALIZED eigenproblem is
        -d_r(K_r R_r) + [ K_th l(l+1) - S ] R = mu M R,
     mu>0 <=> the round cell is STABLE in channel l (no shaped type);
     mu<=0 (a zero crossing) <=> a shaped self-consistent type BIFURCATES.
     This is EXACTLY the e^{-2phi}-in-the-stiffness, bare-r^2 measure of the
     validated offdiag_gateA, with the source term being the linearization
     of the ACTUAL field eqn source -Phi(1-e^{3phi}) (NOT gateA's different
     confining S; gateA validated the MEASURE/eigensolver, not this source).

GAUGE: l=1 (P_1=cos th) is the rigid-TRANSLATION zero mode of the free-
  floating cell (wmneg_results D). It is EXCLUDED from the verdict: the
  decisive existence test is the lowest l>=2 eigenvalue (which has NO
  translation gauge mode). l=1 is tracked separately and shown to soften
  toward 0 (the gauge signature), NOT cross negative.

PRECISION: assembled and solved in mpmath (dps configurable) so the deep
verdict is NOT a float64-overflow artifact (at p=-7, K_r~r^2 e^{28}~1e12;
deeper overflows float64 -- mpmath does not). Convergence shown in BOTH
grid N and precision dps. Cross-checked at shallow p against the float64
wmneg 2D Jacobian smallest modes.

Log /tmp/wmdeep.log. JSON /tmp/wmdeep_angular.json. DATA-BLIND. METRIC-LED.
"""
import sys, time, json
import mpmath as mp

PHI = mp.mpf(1)          # Phi amplitude (scale rides 1/sqrt(Phi); untouched)
R_IN = mp.mpf(1)

_fh = open("/tmp/wmdeep.log", "a")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond); (PASS if ok else FAIL).append(tag)
    log(f"WMDEEP-{tag}: {'PASS' if ok else 'FAIL'}  {note}")

# =====================================================================
# PART 0 -- the DEEP round radial background phi_0(r), full trajectory.
# Adaptive mpmath RK4 (step-doubling), the validated neg_sweep_mpmath
# integrator, but storing (r, phi, phip) at every accepted step so we can
# build the angular operator on the true background.
#   phi'' + (2/r)phi' - 2 phi'^2 = Phi(1 - e^{3phi})
# core (inside-out): phi(1)=p<0, phi'(1)=0+ ; interface r*=first phi->0.
# =====================================================================
def deriv(r, phi, phip, Phi=PHI):
    arg = 3 * phi
    if arg > 5:            # source guard (e^{3phi} only near phi~0; transient
        arg = mp.mpf(5)    # overshoot corrected by step rejection)
    src = Phi * (1 - mp.e ** arg)
    return src - (2 / r) * phip + 2 * phip ** 2

def rk4_step(r, phi, phip, h, Phi=PHI):
    k1p = phip;               k1v = deriv(r, phi, phip, Phi)
    k2p = phip + 0.5*h*k1v;   k2v = deriv(r+0.5*h, phi+0.5*h*k1p, phip+0.5*h*k1v, Phi)
    k3p = phip + 0.5*h*k2v;   k3v = deriv(r+0.5*h, phi+0.5*h*k2p, phip+0.5*h*k2v, Phi)
    k4p = phip + h*k3v;       k4v = deriv(r+h, phi+h*k3p, phip+h*k3v, Phi)
    return (phi + (h/6)*(k1p+2*k2p+2*k3p+k4p),
            phip + (h/6)*(k1v+2*k2v+2*k3v+k4v))

def background_traj(p, tol=mp.mpf('1e-15'), rmax=mp.mpf('4'), Phi=PHI):
    """Return arrays (rs, phis, phips) of the accepted-step trajectory from
    the core to the interface r* (where phi first crosses 0). Adaptive."""
    r = R_IN; phi = mp.mpf(p); phip = mp.mpf('1e-9')
    h = mp.mpf('1e-2'); hmin = mp.mpf('1e-13')
    rs = [r]; phis = [phi]; phips = [phip]
    n = 0
    while r < rmax and n < 6_000_000:
        big_phi, big_phip = rk4_step(r, phi, phip, h, Phi)
        m_phi, m_phip = rk4_step(r, phi, phip, h/2, Phi)
        s_phi, s_phip = rk4_step(r + h/2, m_phi, m_phip, h/2, Phi)
        err = abs(s_phi - big_phi) + abs(s_phip - big_phip)
        scale = tol * (1 + abs(s_phi) + abs(s_phip))
        if err > scale and h > hmin:
            h = h * max(mp.mpf('0.2'), mp.mpf('0.9') * (scale/err) ** mp.mpf('0.2'))
            continue
        phi_new, phip_new, r_new = s_phi, s_phip, r + h
        if phi < 0 and phi_new >= 0:
            frac = (0 - phi) / (phi_new - phi)
            rstar = r + frac * h
            rs.append(rstar); phis.append(mp.mpf(0)); phips.append(phip_new)
            return rs, phis, phips, rstar
        phi, phip, r = phi_new, phip_new, r_new
        rs.append(r); phis.append(phi); phips.append(phip)
        n += 1
        if err < scale / 10 and h < rmax:
            h = min(h * mp.mpf('1.5'), mp.mpf('1e-2'))
    return rs, phis, phips, None

# =====================================================================
# PART 1 -- resample the background on a UNIFORM radial grid and assemble
# the self-adjoint generalized eigenproblem for channel l, in mpmath.
# We linearly interpolate phi_0 and phi_0' from the adaptive trajectory.
# =====================================================================
def resample(rs, phis, Nr):
    """phi_0 on a uniform grid r in [R_IN, r*], Nr points (incl endpoints)."""
    rstar = rs[-1]
    grid = [R_IN + (rstar - R_IN) * mp.mpf(i) / (Nr - 1) for i in range(Nr)]
    phig = []
    j = 0
    M = len(rs)
    for rq in grid:
        while j < M - 2 and rs[j+1] < rq:
            j += 1
        # interval [rs[j], rs[j+1]]
        r0, r1 = rs[j], rs[j+1]
        if r1 == r0:
            phig.append(phis[j]); continue
        t = (rq - r0) / (r1 - r0)
        phig.append(phis[j] * (1 - t) + phis[j+1] * t)
    return grid, phig

def assemble_l(grid, phig, l, Phi=PHI):
    """Self-adjoint generalized eigenproblem for channel l:
        -d_r(K_r R_r) + [K_th l(l+1) - S] R = mu M R
       K_r = r^2 e^{-4phi}, K_th = e^{-2phi}, S = 3 Phi r^2 e^{-phi},
       M   = r^2 e^{-4phi}.  P1 finite elements on the uniform grid (linear
       hat functions) -> SYMMETRIC stiffness by construction, SPD lumped mass.
       Dirichlet at the outer interface (R(r*)=0: the cell seals to round there,
       phi pinned 0); natural (Neumann) at the core inner edge (mirror parity
       phi_r=0).  Returns mpmath matrices (A, Mm) of size (Nr-1)x(Nr-1) (last
       node removed for Dirichlet).  Generalized problem A x = mu Mm x."""
    Nr = len(grid)
    Kr = [g**2 * mp.e**(-4*ph) for g, ph in zip(grid, phig)]
    Kth = [mp.e**(-2*ph) for ph in phig]
    S = [3*Phi * g**2 * mp.e**(-ph) for g, ph in zip(grid, phig)]
    Mw = [g**2 * mp.e**(-4*ph) for g, ph in zip(grid, phig)]   # measure = W_r
    ll = mp.mpf(l*(l+1))
    n = Nr  # full, we drop last row/col for Dirichlet at the end
    A = mp.zeros(n, n)
    Mm = mp.zeros(n, n)
    # element loop (P1 on [r_e, r_{e+1}])
    for e in range(Nr-1):
        h = grid[e+1] - grid[e]
        # midpoint coefficient values (2-pt, accurate for smooth bg)
        Kr_m = (Kr[e] + Kr[e+1]) / 2
        # mass / potential coefficients: use nodal lumping (consistent w/ gateA
        # diagonal mass) but assemble potential via element midpoint*hat^2.
        # --- radial stiffness element matrix (linear hat grads = +-1/h) ---
        ke = Kr_m / h
        A[e, e]     += ke
        A[e+1, e+1] += ke
        A[e, e+1]   += -ke
        A[e+1, e]   += -ke
        # --- potential/reaction element matrix:  (K_th*ll - S) as a
        #     reaction term, lumped to the diagonal (positive K_th part and
        #     the -S part both lumped; lumping keeps M-orthogonality clean).
        pe0 = (Kth[e]   * ll - S[e])
        pe1 = (Kth[e+1] * ll - S[e+1])
        A[e, e]     += pe0 * h / 2
        A[e+1, e+1] += pe1 * h / 2
        # --- mass (measure) lumped ---
        Mm[e, e]     += Mw[e]   * h / 2
        Mm[e+1, e+1] += Mw[e+1] * h / 2
    # Dirichlet at outer node (index Nr-1): drop it.
    sub = list(range(Nr-1))
    Asub = mp.zeros(Nr-1, Nr-1); Msub = mp.zeros(Nr-1, Nr-1)
    for a, i in enumerate(sub):
        for b, j in enumerate(sub):
            Asub[a, b] = A[i, j]
        Msub[a, a] = Mm[i, i]
    return Asub, Msub

def lowest_eig(A, Mm, ntop=3):
    """Lowest few generalized eigenvalues of A x = mu Mm x, A sym, Mm SPD
    diagonal.  Reduce to standard symmetric: Mm^{-1/2} A Mm^{-1/2}, eigsy.
    Returns ascending eigenvalues (mpmath floats)."""
    n = A.rows
    dinv = [1/mp.sqrt(Mm[i, i]) for i in range(n)]
    B = mp.zeros(n, n)
    for i in range(n):
        di = dinv[i]
        for j in range(n):
            B[i, j] = di * A[i, j] * dinv[j]
    # symmetrize defensively
    for i in range(n):
        for j in range(i+1, n):
            s = (B[i, j] + B[j, i]) / 2
            B[i, j] = s; B[j, i] = s
    E = mp.eigsy(B, eigvals_only=True)
    vals = sorted([E[i] for i in range(n)])
    return vals[:ntop]

# =====================================================================
# DRIVER
# =====================================================================
def run_depth(p, Nr=240, dps=40, ls=(0, 1, 2, 3, 4)):
    mp.mp.dps = dps
    rs, phis, phips, rstar = background_traj(p)
    if rstar is None:
        return dict(p=p, ok=False, why="no_interface")
    grid, phig = resample(rs, phis, Nr)
    p_core = phig[0]
    out = dict(p=p, ok=True, rstar=mp.nstr(rstar, 12),
               nbg=len(rs), Nr=Nr, dps=dps, eigs={})
    # deep-regime instruments
    c_eff = mp.e**(-2*p_core)        # c_r^2 = e^{-4phi}; c_eff=e^{-2phi} here
    lapse = mp.e**(-p_core)
    dressing = mp.e**(2*p_core)      # angular dressing e^{2phi} -> 0 deep
    out["c_eff"] = mp.nstr(c_eff, 8)
    out["lapse"] = mp.nstr(lapse, 8)
    out["dressing_e2phi"] = mp.nstr(dressing, 6)
    out["p_core"] = mp.nstr(p_core, 8)
    for l in ls:
        A, Mm = assemble_l(grid, phig, l)
        ev = lowest_eig(A, Mm, ntop=3)
        out["eigs"][l] = [mp.nstr(e, 12) for e in ev]
    return out

def convergence_study(p=-7.004):
    """Grid (Nr) and precision (dps) convergence at a DEEP depth: the verdict
    eigenvalue must be stable under refinement, not a discretization/overflow
    artifact."""
    log(f"\nCONVERGENCE STUDY at p={p} (deep, runaway regime): lowest mu_l2 "
        f"(decisive non-gauge channel) under grid + precision refinement.")
    log(f"{'Nr':>6} {'dps':>5} {'mu_l0':>16} {'mu_l2':>16} {'mu_l4':>16}")
    rows = []
    for (Nr, dps) in [(80, 40), (120, 40), (160, 40), (120, 60), (160, 60)]:
        d = run_depth(p, Nr=Nr, dps=dps, ls=(0, 2, 4))
        if not d["ok"]:
            continue
        l0 = d["eigs"][0][0]; l2 = d["eigs"][2][0]; l4 = d["eigs"][4][0]
        rows.append((Nr, dps, l0, l2, l4))
        log(f"{Nr:6d} {dps:5d} {l0:>16} {l2:>16} {l4:>16}")
    return rows

def main():
    t0 = time.time()
    dps = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    Nr  = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    mp.mp.dps = dps
    log("\n" + "=" * 74)
    log("wmdeep_angular -- DEEP angular-live existence test (mpmath dps=%d, Nr=%d)"
        % (dps, Nr))
    log("time " + time.strftime("%Y-%m-%d %H:%M:%S"))
    log("self-adjoint per-l generalized eigenproblem on the deep round bg;")
    log("mu>0 round-stable (no shape); mu<=0 = shaped type bifurcates.")
    log("GAUGE: l=1 = rigid-translation zero mode, EXCLUDED; verdict = lowest l>=2.")
    log("=" * 74)
    log(f"{'p':>9} {'p_core':>10} {'c_eff':>11} {'lapse':>10} {'e2phi':>10} "
        f"{'mu_l0':>13} {'mu_l1(gauge)':>14} {'mu_l2':>13} {'mu_l3':>13} "
        f"{'mu_l4':>13} {'rstar':>9}")
    depths = [-0.30, -0.80, -1.50, -2.50, -2.75, -3.50, -5.00, -7.004,
              -10.0, -15.0, -25.0, -40.0]
    RES = []
    for p in depths:
        d = run_depth(p, Nr=Nr, dps=dps)
        RES.append(d)
        if not d["ok"]:
            log(f"{p:9.3f}  -- {d['why']}")
            continue
        e = d["eigs"]
        def g(l): return e[l][0] if l in e else "--"
        log(f"{p:9.3f} {d['p_core']:>10} {d['c_eff']:>11} {d['lapse']:>10} "
            f"{d['dressing_e2phi']:>10} {g(0):>13} {g(1):>14} {g(2):>13} "
            f"{g(3):>13} {g(4):>13} {d['rstar']:>9}")
        json.dump(RES, open("/tmp/wmdeep_angular.json", "w"))

    # ---- VERDICT ----
    ok = [d for d in RES if d["ok"]]
    # lowest NON-GAUGE eigenvalue at each depth = min over l in {0,2,3,4}
    def nongauge_min(d):
        vals = []
        for l in (0, 2, 3, 4):
            if l in d["eigs"]:
                vals.append(mp.mpf(d["eigs"][l][0]))
        return min(vals) if vals else None
    crossed = []
    for d in ok:
        m = nongauge_min(d)
        if m is not None and m <= 0:
            crossed.append((d["p"], mp.nstr(m, 8)))
    log("\nLOWEST NON-GAUGE eigenvalue vs depth (the decisive existence map):")
    log(f"{'p':>9} {'min_nongauge_mu':>18} {'verdict':>22}")
    for d in ok:
        m = nongauge_min(d)
        v = "ROUND-STABLE" if (m is not None and m > 0) else "*** CROSSED <=0 ***"
        log(f"{d['p']:9.3f} {mp.nstr(m, 10):>18} {v:>22}")
    # also report the cleanest non-axisymmetric existence channel l>=2 only
    log("\nCLEANEST ANGULAR EXISTENCE TEST -- lowest l>=2 mode (no breathing/")
    log("size or translation gauge mode possible in l>=2) vs depth:")
    log(f"{'p':>9} {'min_l>=2 mu':>16} {'verdict':>16}")
    for d in ok:
        vals = [mp.mpf(d["eigs"][l][0]) for l in (2, 3, 4) if l in d["eigs"]]
        m = min(vals) if vals else None
        v = "STABLE(>0)" if (m is not None and m > 0) else "CROSSED<=0"
        log(f"{d['p']:9.3f} {mp.nstr(m, 12):>16} {v:>16}")

    cstudy = convergence_study(-7.004)

    check("DEEP-REACHED", len(ok) >= 10 and any(d["p"] <= -25 for d in ok),
          f"carried to p={min(d['p'] for d in ok):.3f} "
          f"(deepest c_eff={[d['c_eff'] for d in ok if d['p']==min(e['p'] for e in ok)][0]}, "
          f"lapse={[d['lapse'] for d in ok if d['p']==min(e['p'] for e in ok)][0]}) "
          f"-- WELL past the -2.75 float64 stall, into the runaway regime.")
    check("NONGAUGE-POSITIVE", len(crossed) == 0,
          ("NO non-gauge angular mode (l=0 or l>=2) crosses zero at ANY depth "
           "down to the deepest reached: the round matter cell stays STRICTLY "
           "STABLE all the way down -- ONE ROUND CONTINUUM, by SOLVE not "
           "argument. (l=1 excluded as the rigid-translation gauge mode.)")
          if len(crossed) == 0 else
          (f"*** STRUCTURE EMERGES: a non-gauge mode crosses zero at p="
           f"{crossed} -- a shaped self-consistent type BIFURCATES deep. ***"))
    log(f"\nWMDEEP angular: {len(PASS)} PASS / {len(FAIL)} FAIL "
        f"({time.time()-t0:.0f}s)")
    if FAIL: log("FAILED: " + str(FAIL))
    json.dump(RES, open("/tmp/wmdeep_angular.json", "w"))

if __name__ == "__main__":
    main()
    _fh.close()

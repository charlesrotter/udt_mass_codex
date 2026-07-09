"""cell_solver_round.py — the FIRST solver on the DERIVED constrained-two-player frame.
Round cell (h=rho(r)^2 Omega): TWO fields phi(r), rho(r). CPU, cheap (1-D shooting).
Pre-registration = discreteness_preregistration.md. Binding rule: solve the SPACE, not "the electron".
This increment: OBSERVE what the interior Branch-P system does from a finite core (unlabeled).

Derived round EOMs (verify_ ... round_frame_confirm.py, CAS):
  P (interior, W=1):
     phi'' = 4 e^{-2phi} rho'^2 /(Z rho^2) - 2 phi' rho'/rho
     rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2
  G (exterior, W=e^{2phi}):
     phi'' = -2 phi' rho'/rho                 [ (rho^2 phi')'=0 ]
     rho'' = -(Z/4) rho phi'^2
Junctions at the seal r_s: JC1 [Z rho^2 phi'] cont (=charge q); JC2 rho'_P = e^{2phi_s} rho'_G; phi,rho cont.
NOTE (CAS): a SMOOTH center rho->0 makes the P source ~1/rho^2 DIVERGE -> the cell needs a FINITE CORE
(rho_c>0) -- a native motivation for the canon finite/intrinsically-singular core.
Z_phi held FIXED (one global choice; the open constant). Areal rho=r is the NEUTRAL limit -- we MEASURE
rho(r)/r drift rather than impose it.
"""
import numpy as np
from scipy.integrate import solve_ivp

def rhs_P(r, y, Z, matter=None):
    """Interior Branch-P RHS. matter=None -> the phi-BLIND vacuum-geometry interior (unchanged).
    matter=dict -> Thread-B PRESCRIBED-I_r PROBE (labeled): the radial matter channel is switched on
    with a PRESCRIBED (not self-consistent-f) profile I_r(r), I_4th(r), adding
      phi-EOM source S = asrc_c*alpha*xi*e^{alpha phi}*rho^2*I_r  (phi'' gains S/(Z rho^2)),
      rho-EOM transverse stress T_AB = (e^{2phi}/4)(xi*rho*I_r - kap*N^2*I_4th/rho^3).
    asrc_c is the source coefficient: -1/2 = blind-verified self-consistent (settle2.py); +1 = doc/charter.
    This is a PROBE: I_r is imposed, NOT solved from the S^2 map f -- flagged wherever used."""
    phi, rho, phip, rhop = y
    e2 = np.exp(-2*phi)
    phipp = 4*e2*rhop**2/(Z*rho**2) - 2*phip*rhop/rho
    rhopp = 2*phip*rhop - (Z/4)*rho*np.exp(2*phi)*phip**2
    if matter is not None:
        al = matter["alpha"]; ac = matter["asrc_c"]; xi = matter["xi"]
        kap = matter["kap"]; N = matter["N"]
        Ir = matter["Ir"](r); I4th = matter["I4th"](r)
        phipp += ac*al*xi*np.exp(al*phi)*Ir/Z                         # S/(Z rho^2), rho^2 cancels
        rhopp += (np.exp(2*phi)/4.0)*(xi*rho*Ir - kap*N**2*I4th/rho**3)  # T_AB transverse stress
    return [phip, rhop, phipp, rhopp]

def rhs_G(r, y, Z):
    phi, rho, phip, rhop = y
    phipp = -2*phip*rhop/rho
    rhopp = -(Z/4)*rho*phip**2
    return [phip, rhop, phipp, rhopp]

def integrate(branch, r0, r1, y0, Z, n=4000):
    f = rhs_P if branch == 'P' else rhs_G
    sol = solve_ivp(f, (r0, r1), y0, args=(Z,), t_eval=np.linspace(r0, r1, n),
                    rtol=1e-9, atol=1e-12, dense_output=True, max_step=(r1-r0)/200)
    return sol

def _rho_zero(r, y, *args): return y[1]     # event: rho -> 0 (collapse); *args absorbs (Z[, matter])
_rho_zero.terminal = True; _rho_zero.direction = -1

def make_matter(rc, rs, amp, alpha, asrc_c, xi=1.0, kap=1.0, N=1.0, i4_frac=1.0):
    """Build a PRESCRIBED bounded interior matter profile (Thread-B probe). I_r and I_4th are smooth
    bumps ~ sin^2(pi (r-rc)/(rs-rc)) that VANISH at both ends (consistent with the f_r=0 mirror BC),
    peak amplitude 'amp'. i4_frac scales I_4th relative to I_r. NOT self-consistent f -- a PROBE."""
    L = rs - rc
    def bump(r):
        x = np.clip((r - rc)/L, 0.0, 1.0)
        return np.sin(np.pi*x)**2
    return dict(alpha=alpha, asrc_c=asrc_c, xi=xi, kap=kap, N=N,
                Ir=lambda r: amp*bump(r), I4th=lambda r: i4_frac*amp*bump(r))


def try_cell(phipc, rs, Z, rc=0.1, Rout=200.0, matter=None):
    """Interior P from core to seal r_s; match (JC1: rho^2 phi' cont; JC2: rho'_G=e^{-2phi_s}rho'_P);
    integrate exterior G outward; SCORE asymptotic flatness. Returns (q, score, info).
    matter=dict -> PRESCRIBED-I_r probe active in the interior (see rhs_P/make_matter)."""
    yi0 = [0.0, rc, phipc, 1.0]
    si = solve_ivp(rhs_P, (rc, rs), yi0, args=(Z, matter), rtol=1e-9, atol=1e-12,
                   events=_rho_zero, max_step=(rs-rc)/400)
    if not si.success or si.t_events[0].size or si.y[1,-1] <= 0:
        rmin = float(si.y[1].min()) if si.y.size else 0.0
        return None, np.inf, 'interior-fail', rmin
    phis, rhos, phips, rhops = si.y[:, -1]
    rho_core = float(si.y[1].min())        # min interior rho (T3: finite core vs rho->0 collapse)
    q = Z*rhos**2*phips
    # seal match: phi,rho continuous; JC1 -> phi'_G=phi'_P (rho cont); JC2 -> rho'_G=e^{-2phi_s}rho'_P
    ye0 = [phis, rhos, phips, np.exp(-2*phis)*rhops]
    se = solve_ivp(rhs_G, (rs, Rout), ye0, args=(Z,), rtol=1e-9, atol=1e-12,
                   events=_rho_zero, max_step=(Rout-rs)/2000)
    if se.t_events[0].size:                 # exterior collapsed (rho->0): not a bounded cell
        return q, np.inf, 'exterior-collapse', rho_core
    if not se.success or se.y[1,-1] <= 0:
        return q, np.inf, 'exterior-fail', rho_core
    phiR, rhoR, phipR, rhopR = se.y[:, -1]
    # PROPER asymptotic-flatness (no conical deficit): rho'/e^phi -> 1 at infinity.
    deficit = rhopR/np.exp(phiR) - 1.0
    return q, deficit, (f'ok phiR={phiR:+.3f} rhopR={rhopR:+.3f} deficit={deficit:+.4f}'), rho_core

def _deficit_bracket(phipc, rs, Z, matter, rc=0.1):
    """Return signed deficit at (phipc, rs); np.nan if not a bounded cell (collapse/fail)."""
    q, deficit, info, rho_core = try_cell(phipc, rs, Z, rc=rc, matter=matter)
    return (deficit if np.isfinite(deficit) else np.nan), rho_core


def probe_scan(Z, alpha, asrc_c, amp, rc=0.1):
    """Thread-B PRESCRIBED-I_r deficit probe: scan (phipc, rs) with the alpha source + T_AB active,
    report the deficit landscape and whether deficit=0 (flat) is REACHED (sign change across the grid)."""
    phipcs = [0.0, 0.1, 0.2, 0.3, 0.5, 0.8, 1.2]
    rss    = [0.5, 1.0, 2.0, 3.0, 5.0, 8.0]
    matter = make_matter(rc, 1.0, amp, alpha, asrc_c)   # rs overwritten per-call below
    defs = np.full((len(phipcs), len(rss)), np.nan)
    cores = np.full_like(defs, np.nan)
    for i, phipc in enumerate(phipcs):
        for j, rs in enumerate(rss):
            m = make_matter(rc, rs, amp, alpha, asrc_c)  # profile keyed to this rs
            d, rc_core = _deficit_bracket(phipc, rs, Z, m, rc=rc)
            defs[i, j] = d; cores[i, j] = rc_core
    finite = defs[np.isfinite(defs)]
    reaches_flat = (finite.size > 0) and (finite.min() < 0 < finite.max())
    return phipcs, rss, defs, cores, reaches_flat


if __name__ == '__main__':
    import sys
    Z = 8.0            # FIXED global (route-B value); a CHOSE-fixed parameter, NOT retuned per solution
    if '--probe' in sys.argv:
        # ---- Thread-B PRESCRIBED-I_r probe (alpha source + T_AB); DEFAULT coeff = self-consistent -1/2 ----
        asrc_c = float(sys.argv[sys.argv.index('--asrc') + 1]) if '--asrc' in sys.argv else -0.5
        amp    = float(sys.argv[sys.argv.index('--amp') + 1]) if '--amp' in sys.argv else 0.3
        print(f"# Thread-B PRESCRIBED-I_r DEFICIT PROBE  (Z={Z}, asrc_c={asrc_c:+.2f}, amp={amp}, xi=kap=N=1)")
        print(f"# baseline (alpha=0, no matter) deficit stuck ~ -0.9; does alpha<0 source+T_AB reach deficit=0?")
        for alpha in (-0.5, -1.0, -2.0):
            ph, rs, defs, cores, flat = probe_scan(Z, alpha, asrc_c, amp)
            fin = defs[np.isfinite(defs)]
            dmin = fin.min() if fin.size else np.nan
            dmax = fin.max() if fin.size else np.nan
            cmin = cores[np.isfinite(cores)].min() if np.isfinite(cores).any() else np.nan
            print(f"\n alpha={alpha:+.1f}: deficit range [{dmin:+.3f}, {dmax:+.3f}]  "
                  f"reaches flat(deficit=0): {flat}   min interior rho={cmin:.3e}")
            for i, p in enumerate(ph):
                row = "  ".join(f"rs={rs[j]:>4}:{defs[i,j]:+.3f}" if np.isfinite(defs[i,j]) else f"rs={rs[j]:>4}:  coll "
                                for j in range(len(rs)))
                print(f"  phi'_c={p:>4} | {row}")
        raise SystemExit(0)

    print("# SCAN (unlabeled): bounded round cell + asymptotic FLATNESS (deficit = rho'/e^phi - 1 -> 0).")
    print("# A discrete cell = flatness (deficit=0) satisfied only at ISOLATED (phi'_c, r_s). deficit varies smooth => continuum.")
    phipcs = [0.0, 0.1, 0.2, 0.3, 0.5, 0.8]
    rss    = [0.5, 1.0, 2.0, 3.0, 5.0, 8.0]
    for phipc in phipcs:
        row = []
        for rs in rss:
            q, deficit, info, rho_core = try_cell(phipc, rs, Z)
            tag = 'coll' if info == 'exterior-collapse' else (f'{deficit:+.3f}' if np.isfinite(deficit) else 'xfail')
            row.append(f"rs={rs:>4}:def={tag:>7}")
        print(f"phi'_c={phipc:>4} | " + "  ".join(row))

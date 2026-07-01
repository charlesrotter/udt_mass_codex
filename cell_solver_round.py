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

def rhs_P(r, y, Z):
    phi, rho, phip, rhop = y
    e2 = np.exp(-2*phi)
    phipp = 4*e2*rhop**2/(Z*rho**2) - 2*phip*rhop/rho
    rhopp = 2*phip*rhop - (Z/4)*rho*np.exp(2*phi)*phip**2
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

def _rho_zero(r, y, Z): return y[1]        # event: rho -> 0 (collapse)
_rho_zero.terminal = True; _rho_zero.direction = -1

def try_cell(phipc, rs, Z, rc=0.1, Rout=200.0):
    """Interior P from core to seal r_s; match (JC1: rho^2 phi' cont; JC2: rho'_G=e^{-2phi_s}rho'_P);
    integrate exterior G outward; SCORE asymptotic flatness. Returns (q, score, info)."""
    yi0 = [0.0, rc, phipc, 1.0]
    si = solve_ivp(rhs_P, (rc, rs), yi0, args=(Z,), rtol=1e-9, atol=1e-12,
                   events=_rho_zero, max_step=(rs-rc)/400)
    if not si.success or si.t_events[0].size or si.y[1,-1] <= 0:
        return None, np.inf, 'interior-fail'
    phis, rhos, phips, rhops = si.y[:, -1]
    q = Z*rhos**2*phips
    # seal match: phi,rho continuous; JC1 -> phi'_G=phi'_P (rho cont); JC2 -> rho'_G=e^{-2phi_s}rho'_P
    ye0 = [phis, rhos, phips, np.exp(-2*phis)*rhops]
    se = solve_ivp(rhs_G, (rs, Rout), ye0, args=(Z,), rtol=1e-9, atol=1e-12,
                   events=_rho_zero, max_step=(Rout-rs)/2000)
    if se.t_events[0].size:                 # exterior collapsed (rho->0): not a bounded cell
        return q, np.inf, 'exterior-collapse'
    if not se.success or se.y[1,-1] <= 0:
        return q, np.inf, 'exterior-fail'
    phiR, rhoR, phipR, rhopR = se.y[:, -1]
    # PROPER asymptotic-flatness (no conical deficit): rho'/e^phi -> 1 at infinity.
    deficit = rhopR/np.exp(phiR) - 1.0
    return q, deficit, (f'ok phiR={phiR:+.3f} rhopR={rhopR:+.3f} deficit={deficit:+.4f}')

if __name__ == '__main__':
    Z = 8.0            # FIXED global (route-B value); a CHOSE-fixed parameter, NOT retuned per solution
    print("# SCAN (unlabeled): bounded round cell + asymptotic FLATNESS (deficit = rho'/e^phi - 1 -> 0).")
    print("# A discrete cell = flatness (deficit=0) satisfied only at ISOLATED (phi'_c, r_s). deficit varies smooth => continuum.")
    phipcs = [0.0, 0.1, 0.2, 0.3, 0.5, 0.8]
    rss    = [0.5, 1.0, 2.0, 3.0, 5.0, 8.0]
    for phipc in phipcs:
        row = []
        for rs in rss:
            q, deficit, info = try_cell(phipc, rs, Z)
            tag = 'coll' if info == 'exterior-collapse' else (f'{deficit:+.3f}' if np.isfinite(deficit) else 'xfail')
            row.append(f"rs={rs:>4}:def={tag:>7}")
        print(f"phi'_c={phipc:>4} | " + "  ".join(row))

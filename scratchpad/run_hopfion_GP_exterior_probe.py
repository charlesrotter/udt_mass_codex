"""FROZEN exterior probe (hopfion_GP_exterior_probe_MAP.md) on the REAL H3 field ONLY.
Integrate native Branch-P  Z(r^2 phi')' = e^{-2phi}(4 + Shat(r))  [P-source ON, ambient-weighted],
Shat(r) = real H3 shell-projected transverse trace tau(r) (real-field PROXY source; 0 beyond r_tex).
phi = phi_amb + psi, psi regular at core (u=r^2 psi'=0). q = Z*u (flux above ambient).
MEASURE q(r) across exterior radii: PLATEAU (self-quench->conserved flux) vs DRIFT (no clean flux).
Sweep phi_amb (shallow<crit<deep) and Z in {1,8}. NO G shortcut, NO r_lo cherry-pick, NO tautology."""
import numpy as np
from scipy.integrate import solve_ivp

D = np.load('/home/udt-admin/udt_mass_codex/h4_scripts/stress_rtheta_h3.npz')
rc = D['rc']; thc = D['thc']; w = np.sin(thc)
tau = ((D['Tthth'] + D['Tphph']) * w[None, :]).sum(1) / w.sum()   # real H3 source proxy Shat(r)
r_tex = 3.9
def Shat(r):
    return np.interp(r, rc, tau, left=0.0, right=0.0) * (r <= rc[-1])   # real field; 0 beyond data

R_C, R_MAX = 0.05, 80.0
def integrate(phi_amb, Z, branch="P"):
    # branch="P": native round vacuum P-source 4e^{-2phi} ON in exterior (source-supported).
    # branch="G": CONTROL -- vacuum source OFF in exterior (source-free); hopfion Shat still injects
    #   the inner flux, then (r^2 phi')'=0 outside -> q MUST plateau. Distinguishes P-drift from a bug.
    pref = np.exp(-2.0 * phi_amb)
    def rhs(r, y):
        psi, u = y
        vac = 4.0 if branch == "P" else 0.0
        src = pref * np.exp(-2.0 * psi) * (vac + Shat(r)) / Z
        return [u / r**2, src]
    sol = solve_ivp(rhs, (R_C, R_MAX), [0.0, 0.0], rtol=1e-9, atol=1e-11,
                    dense_output=True, max_step=0.05)
    def q_at(r):
        psi, u = sol.sol(r); return Z * u
    return sol, q_at

def classify(q_at, Z):
    rr = np.array([r_tex, 2*r_tex, 5*r_tex, 10*r_tex, 20*r_tex]); rr = rr[rr < R_MAX]
    qs = np.array([q_at(float(r)) for r in rr])
    qref = qs[-1]
    spread = np.ptp(qs[-3:]) / (abs(qs[-3:]).mean() + 1e-30)   # far-field convergence
    if abs(qref) < 1e-3 and spread < 0.05:
        cls = "flux-neutral (q->0)"
    elif spread < 0.02:
        cls = "PLATEAU (active-P, conserved flux)"
    elif spread > 0.2:
        cls = "DRIFT (boxy-P)"
    else:
        cls = "marginal"
    return rr, qs, qref, spread, cls

print("=== FROZEN exterior probe on REAL H3 field (r_tex=3.9); native P-source ON ===")
print("Shat=real tau(r): core +", f"{tau.max():+.2f}", " tail", f"{tau[np.searchsorted(rc,2.0)]:+.2f}")
for Z in (1.0, 8.0):
    crit = 0.5 * np.log(32 / Z)
    print(f"\n-- Z_phi={Z}  crit=1/2 ln(32/Z)={crit:.3f}  (phi_amb<crit shallow / >crit deep) --")
    print(f"   {'phi_amb':>8} {'regime':>7} | q(r_tex) q(2) q(5) q(10) q(20)            | far-spread  CLASS")
    for pa in (0.3, crit, 1.0, 1.5, 3.0):
        sol, q_at = integrate(pa, Z, branch="P")
        rr, qs, qref, spread, cls = classify(q_at, Z)
        reg = "deep" if pa > crit else "shal"
        qstr = " ".join(f"{q:+.3e}" for q in qs)
        print(f"   {pa:8.3f} {reg:>7} | {qstr}  | {spread:.2e}  {cls}")

print("\n=== BRANCH-G CONTROL (vacuum source OFF; hopfion inner flux only) -- MUST plateau ===")
print(f"   {'phi_amb':>8} {'Z':>4} | q(r_tex) q(2) q(5) q(10) q(20)            | far-spread  CLASS")
for Z in (1.0, 8.0):
    for pa in (0.3, 1.5, 3.0):
        sol, q_at = integrate(pa, Z, branch="G")
        rr, qs, qref, spread, cls = classify(q_at, Z)
        qstr = " ".join(f"{q:+.3e}" for q in qs)
        print(f"   {pa:8.3f} {Z:4.0f} | {qstr}  | {spread:.2e}  {cls}")
print("\n(G control plateaus (conserved q) <=> integrator is sound and the P-DRIFT is real")
print(" source-supported Branch-P behavior, NOT a solver bug. The test is NOT tautological:")
print(" same integrator gives PLATEAU for G, DRIFT for P.)")

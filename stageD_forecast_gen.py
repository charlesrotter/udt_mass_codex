"""stageD_forecast_gen.py — Stage-D frozen forecast from the BANKED quantization-closure law.

PREDICTION GENERATION ONLY. No cell/shooting solves of the field equations are run.
Allowed machinery used:
  - algebra on the potential family A1 m=3 (derivatives of U at rho=1),
  - the universal bottom gamma-system ODE (part of the law's own machinery, Category-A),
  - root-finding on the closure relation.

The chain is a faithful reuse of the blind verifier's own chain in
/home/udt-admin/udt_mass_codex/cascade_bv10_assembly.py (agent a954b5c15ec7ee2ca),
which produced the banked calibration deviations -0.38% (N=8), +0.08% (N=16),
+0.13% (N=22) recorded in ladder_theta0_accumulation_results.md.

LAW (ladder_theta0_accumulation_results.md):
    d*(N) solves  z_c_eff(gamma(d)) = Theta(N)*sqrt(x_c)   [bv10 form; see RHS note]
    gamma(d) = 4*dt(d)^2 / (Z * s1(d)^2 * x_c^2)
    Theta(N) = (N+1)*pi + theta0(N),
    theta0 = z*_eff(gamma) + K*Z*(1-x_c)^2/(3*Theta) + (3/2)*c3*(dt/s1)*Theta
             (self-consistent in Theta),  K = 2 + (15/16)c3^2 - (3/2)c3 + (3/4)c4.
RHS note: the results doc states Theta*sqrt(x_c)/sqrt(1-x_c); the verifier's script
(bv10, the source of the quoted calibration numbers) uses Theta*sqrt(x_c). Both are
computed below; the one reproducing the banked calibration is used for the forecast.

Family (cascade_stageB_results.md): A1 m=3, Z=8, rho_c=1 gauge, below-stuck side.
    U(rho) = 2*rho^3*exp(-a*(rho^2-1)),  a = (3/2)*(1-d)
    s1 = |U''(1)|/4,  dt = U'(1)/4 (= delta-tilde),  c3 = U'''(1)/(12 s1),
    c4 = U''''(1)/(48 s1),  x_c = 1/1101.

Amplitude/charge (ladder_lemmaD_sealing_amplitude_results.md):
    a_seal ~= sqrt(Z)/Theta        (R2 leading form; (|s1|/Q_s)^{1/4} factor <=0.2% needs
                                    a solve for Q_s -> deliberately NOT computed here)
    q = 2*Z*sqrt(|s1|)*(1-x_c)/Theta   (s1 at the predicted d*)
Parity (cascade_stageB_results.md B3, below side): odd N -> rho_s<1, even N -> rho_s>1.
"""
import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
import sympy as sp

XC = 1.0 / 1101.0
SQXC = np.sqrt(XC)
Z = 8.0
M = 3
OUT = "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/bbac881f-5389-456c-bd4a-fa437c66321e/scratchpad"

# ---------------- universal bottom gamma-system (verbatim bv10) ----------------
def rhs(z, y, gamma):
    v, vz, psi, p = y
    return [vz, p*vz - v + 1.0, p, gamma*np.exp(-2.0*psi)*vz*vz - p*p]

def run_bottom(gamma, z_end=400.0):
    ev = lambda z, y, g: y[1]
    ev.direction = 0
    sol = solve_ivp(rhs, (0.0, z_end), [0.0]*4, args=(gamma,), method="DOP853",
                    rtol=1e-11, atol=1e-13, events=[ev], dense_output=True, max_step=0.05)
    zn = sol.t_events[0]; zn = zn[zn > 1e-6]
    offs = zn - np.arange(1, len(zn)+1)*np.pi
    pair = 0.5*(offs[1:] + offs[:-1])
    zz = np.linspace(0.75*z_end, z_end, 100)
    zc = float(np.mean(zz*np.exp(-sol.sol(zz)[2]/2.0)))
    return float(pair[-1]), zc

def build_splines(gg):
    zs, zc = [], []
    for g in gg:
        a, b = run_bottom(g)
        zs.append(a); zc.append(b)
    zstar_f = CubicSpline(gg, zs)
    zc_f = CubicSpline(np.log(gg), np.log(zc))
    return (lambda g: float(zstar_f(g))), (lambda g: float(np.exp(zc_f(np.log(g)))))

# bv10's exact grid (calibration-faithful)
GG_BV10 = np.array([0.4, 0.5, 0.6, 0.688, 0.8, 0.9, 1.0, 1.078, 1.2, 1.4, 1.6, 1.8, 2.0,
                    2.2, 2.334, 2.5, 2.7, 3.0, 3.5, 4.066, 4.5])
# extended grid for the forecast window (gamma ~ d^2 drops below 0.4 near d ~ 1.3e-3)
GG_EXT = np.array([0.10, 0.13, 0.16, 0.20, 0.25, 0.30, 0.35, 0.4, 0.5, 0.6, 0.688, 0.8,
                   0.9, 1.0, 1.078, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.334, 2.5, 2.7, 3.0,
                   3.5, 4.066, 4.5])

# ---------------- family coefficients (exact, sympy; bv10's fam) ----------------
_rho, _d = sp.symbols('rho d', positive=True)
_a = (sp.Rational(M, 2))*(1 - _d)
_U = 2*_rho**M*sp.exp(-_a*(_rho**2 - 1))
_dU_exprs = [sp.diff(_U, _rho, k).subs(_rho, 1) for k in range(5)]
_dU_f = [sp.lambdify(_d, e, "numpy") for e in _dU_exprs]

def fam(d):
    dU = [float(f(d)) for f in _dU_f]
    s1 = abs(dU[2]/4.0)
    dt = dU[1]/4.0
    c3 = dU[3]/(12.0*s1)
    c4 = dU[4]/(48.0*s1)
    return dt, s1, c3, c4

def fam_sympy_check(d):
    """bv10's original per-call sympy path, for a one-point agreement check."""
    a_ = (M/2.0)*(1.0 - d)
    rho = sp.symbols('rho', positive=True)
    U = 2*rho**M*sp.exp(-sp.Float(a_)*(rho**2 - 1))
    dU = [float(sp.diff(U, rho, k).subs(rho, 1)) for k in range(5)]
    return abs(dU[2]/4.0), dU[1]/4.0

# ---------------- theta0 assembly (bv10's assemble) ----------------
def assemble(d, N, zstar_of_gamma, theta0_guess=0.3*np.pi):
    dt, s1, c3, c4 = fam(d)
    dh = dt/s1
    gamma = 4.0*dt*dt/(Z*s1*s1*XC*XC)
    K = 2.0 + (15.0/16.0)*c3*c3 - 1.5*c3 + 0.75*c4
    th0 = theta0_guess
    for _ in range(200):
        Theta = (N+1)*np.pi + th0
        SP_E = K*Z*(1.0-XC)**2/(3.0*Theta)
        SP_d = 1.5*c3*dh*Theta
        th0_new = zstar_of_gamma(gamma) + SP_E + SP_d
        if abs(th0_new - th0) < 1e-14:
            break
        th0 = th0_new
    Theta = (N+1)*np.pi + th0
    return dict(gamma=gamma, theta0=th0, Theta=Theta, s1=s1, dt=dt, c3=c3, c4=c4, K=K)

def closure_res(d, N, zstar_of_gamma, zc_of_gamma, rhs_factor):
    A = assemble(d, N, zstar_of_gamma)
    return zc_of_gamma(A['gamma']) - A['Theta']*SQXC*rhs_factor

def d_star(N, bracket, zstar_of_gamma, zc_of_gamma, rhs_factor=1.0):
    return brentq(closure_res, bracket[0], bracket[1],
                  args=(N, zstar_of_gamma, zc_of_gamma, rhs_factor), xtol=1e-13)

# ---------------- banked pins (cascade_stageB_rungs.json) ----------------
BANKED = {8: 0.0039170433840523145, 16: 0.0026633943318721508, 20: 0.0022843642733540444,
          21: 0.002203947737560068, 22: 0.0021288889609986155}
BANKED_Q = {8: 0.9423556569314924, 22: 0.37967185882682275}

def main():
    # sanity: lambdified fam vs bv10 sympy-Float fam at one point
    s1a, dta = fam(0.003917043)[1], fam(0.003917043)[0]
    s1b, dtb = fam_sympy_check(0.003917043)
    assert abs(s1a/s1b - 1) < 1e-12 and abs(dta/dtb - 1) < 1e-12, "fam mismatch"

    print("=== building bv10-exact splines (calibration) ===")
    zstar_b, zc_b = build_splines(GG_BV10)

    print("\n=== CALIBRATION (bv10-exact grid), RHS = Theta*sqrt(xc) ===")
    calib = {}
    for N in (8, 16, 22):
        dp = d_star(N, (0.5*BANKED[N], 1.6*BANKED[N]), zstar_b, zc_b, 1.0)
        dev = 100*(dp/BANKED[N] - 1)
        calib[N] = dict(d_pred=dp, d_banked=BANKED[N], dev_pct=dev)
        print(f"  N={N:2d}: d_pred={dp:.9f}  banked={BANKED[N]:.9f}  dev={dev:+.2f}%")

    print("\n=== CALIBRATION variant, RHS = Theta*sqrt(xc)/sqrt(1-xc) (doc wording) ===")
    calib_var = {}
    for N in (8, 16, 22):
        dp = d_star(N, (0.5*BANKED[N], 1.6*BANKED[N]), zstar_b, zc_b, 1.0/np.sqrt(1.0-XC))
        dev = 100*(dp/BANKED[N] - 1)
        calib_var[N] = dict(d_pred=dp, dev_pct=dev)
        print(f"  N={N:2d}: d_pred={dp:.9f}  dev={dev:+.2f}%")

    print("\n=== building extended-grid splines (forecast) ===")
    zstar_e, zc_e = build_splines(GG_EXT)
    # soundness: z_end convergence at the small-gamma end
    for g in (0.10, 0.25):
        _, zc400 = run_bottom(g, 400.0)
        _, zc800 = run_bottom(g, 800.0)
        print(f"  z_end conv @gamma={g}: zc(400)={zc400:.6f} zc(800)={zc800:.6f} "
              f"rel={abs(zc800/zc400-1):.2e}")
    # soundness: extended spline reproduces calibration
    calib_ext = {}
    for N in (8, 16, 22):
        dp = d_star(N, (0.5*BANKED[N], 1.6*BANKED[N]), zstar_e, zc_e, 1.0)
        calib_ext[N] = 100*(dp/BANKED[N] - 1)
        print(f"  ext-grid calib N={N:2d}: dev={calib_ext[N]:+.2f}%")

    print("\n=== FORECAST: all N with d*(N) in (1.30e-3, 2.30e-3), extended range ===")
    rows = []
    d_prev = BANKED[20]*1.05
    N = 20
    while True:
        try:
            dp = d_star(N, (0.55*d_prev, 1.02*d_prev), zstar_e, zc_e, 1.0)
        except ValueError:
            print(f"  N={N}: bracket failed, widening")
            dp = d_star(N, (0.4*d_prev, 1.10*d_prev), zstar_e, zc_e, 1.0)
        A = assemble(dp, N, zstar_e)
        a_seal = np.sqrt(Z)/A['Theta']
        q = 2.0*Z*np.sqrt(A['s1'])*(1.0-XC)/A['Theta']
        parity = "rho_s<1" if N % 2 == 1 else "rho_s>1"
        rows.append(dict(N=N, d_star=dp, gamma=A['gamma'], theta0_over_pi=A['theta0']/np.pi,
                         Theta=A['Theta'], a_seal=a_seal, q=q, parity_side=parity,
                         in_window_proper=(1.45e-3 < dp < 2.11e-3),
                         in_extended=(1.30e-3 < dp < 2.30e-3)))
        print(f"  N={N:2d}: d*={dp:.6e} gamma={A['gamma']:.4f} th0={A['theta0']/np.pi:+.4f}pi "
              f"a_seal={a_seal:.5f} q={q:.5f} {parity} "
              f"{'WINDOW' if rows[-1]['in_window_proper'] else ('ext' if rows[-1]['in_extended'] else '-')}")
        if dp < 1.30e-3:
            break
        d_prev = dp
        N += 1
        if N > 60:
            print("  stop guard hit"); break

    # q sanity vs banked (N=8, 22)
    print("\n=== q formula sanity vs banked ===")
    for N in (8, 22):
        A = assemble(BANKED[N], N, zstar_e)
        qpred = 2.0*Z*np.sqrt(A['s1'])*(1.0-XC)/A['Theta']
        print(f"  N={N}: q_pred={qpred:.5f}  banked={BANKED_Q[N]:.5f}  "
              f"dev={100*(qpred/BANKED_Q[N]-1):+.2f}%")
    # d*(20),(21) extra check vs banked
    for N in (20, 21):
        dp = d_star(N, (0.8*BANKED[N], 1.2*BANKED[N]), zstar_e, zc_e, 1.0)
        print(f"  extra: N={N} d_pred={dp:.6e} banked={BANKED[N]:.6e} "
              f"dev={100*(dp/BANKED[N]-1):+.2f}%")

    ext_rows = [r for r in rows if r['in_extended']]
    win_rows = [r for r in rows if r['in_window_proper']]
    print(f"\nExtended-range count: {len(ext_rows)} (N={ext_rows[0]['N']}..{ext_rows[-1]['N']})")
    print(f"Window-proper (1.45e-3, 2.11e-3) count: {len(win_rows)} "
          f"(N={win_rows[0]['N']}..{win_rows[-1]['N']})")

    payload = dict(
        family="A1 m=3, Z=8, rho_c=1 gauge, below-stuck side",
        law="d*(N) solves z_c_eff(gamma(d)) = Theta(N)*sqrt(x_c); gamma=4*dt^2/(Z s1^2 xc^2); Theta=(N+1)pi+theta0(N)",
        rhs_form_used="Theta*sqrt(x_c) (bv10 verifier form; reproduces banked calibration)",
        x_c=XC, Z=Z, m=M,
        calibration_bv10_grid=calib,
        calibration_variant_sqrt1mxc={k: v for k, v in calib_var.items()},
        calibration_extended_grid_devpct=calib_ext,
        q_formula="q = 2*Z*sqrt(|s1|)*(1-x_c)/Theta",
        a_seal_formula="a_seal ~= sqrt(Z)/Theta (R2 leading; (|s1|/Q_s)^{1/4} <=0.2% omitted, needs a solve)",
        parity_rule="below side: odd N -> rho_s<1, even N -> rho_s>1",
        forecast=rows,
        extended_range=[1.30e-3, 2.30e-3],
        window_proper=[1.45e-3, 2.11e-3],
        window_proper_count=len(win_rows),
        extended_count=len(ext_rows),
    )
    with open(f"{OUT}/stageD_frozen_forecast.json", "w") as f:
        json.dump(payload, f, indent=1)
    print(f"\nwrote {OUT}/stageD_frozen_forecast.json")
    return payload

if __name__ == "__main__":
    main()

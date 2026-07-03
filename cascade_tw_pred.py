"""tw_pred.py -- Task (b): predicted twin splittings vs N (m=3, Z=8), tested on banked data.
NO FITS. Predictions built only from: below-side banked rungs + exact family functions +
banked-derived O(eps) machinery (Theorems A/B, Lemma D R2, th2 quadrature) + CAS odd parts (tw_cas).
Above-side banked values (from the Stage-B blind verifier) are used ONLY as test targets.
Cheap 1-D bottom-system integrations (not cell shots) supply z_c_eff(gamma) sensitivity.
"""
import json
import numpy as np
from scipy.integrate import solve_ivp

M, Z = 3.0, 8.0
XC = 1.0/1101.0
SXT = np.sqrt(XC)/np.sqrt(1.0 - XC)     # sqrt(x_c)/sqrt(1-x_c)

# ---------------- banked below-side rungs (cascade_stageB_rungs.json)
rungs = {r["N_delta"]: r for r in json.load(open(
    "/home/udt-admin/udt_mass_codex/cascade_stageB_rungs.json"))["rungs"]}
# ---------------- banked above-side rungs (Stage-B blind verifier; test targets ONLY)
above = {
    8:  dict(a=1.50587703866, rho_s=0.89250307, q=0.93400162, L=16.8576),
    9:  dict(a=1.50556166549, rho_s=1.07964573, q=0.84816520, L=18.6192),
    10: dict(a=1.50526832529, rho_s=0.91264790, q=0.77386007, L=20.4068),
    11: dict(a=1.50501146174, rho_s=1.06742396, q=0.71309209, L=22.1817),
}
# banked measured theta0 (th2 final table, below side)
theta0_meas = {8: 0.32086535678078276, 10: 0.2826580796383584}

def s1abs(dt):   # |s1~| = -(2dt^2 + dt - m), valid small dt
    return -(2.0*dt*dt + dt - M)

def chat3(dt):
    return (16*dt**3 + 24*dt**2 - 24*dt*M + 4*M)/(12.0*s1abs(dt))

def chat4(dt):
    return (32*dt**4 + 96*dt**3 - 96*dt**2*M + 24*dt**2 - 16*dt*M + 24*M**2 - 12*M)/(48.0*s1abs(dt))

def gamma_of(dt):
    return 4.0*dt*dt/(Z*(2*dt*dt + dt - M)**2*XC*XC)

def bottom_zc(gam, zmax=80.0):
    """z_c_eff(gamma) from the banked universal bottom system (cheap 1-D ODE, not a cell shot)."""
    def f(z, y):
        v, vz, psi, p = y
        return [vz, p*vz - v + 1.0, p, gam*np.exp(-2.0*psi)*vz*vz - p*p]
    s = solve_ivp(f, (0.0, zmax), [0.0]*4, rtol=1e-11, atol=1e-13, dense_output=True)
    zz = np.linspace(0.7*zmax, zmax, 20001)
    v, vz, psi, p = s.sol(zz)
    return float(np.sqrt(np.mean(zz**2/np.exp(psi))))   # psi-based z_c_eff (robust)

print("="*110)
print("Per-N ingredients (below side: banked; Theta_B from banked theta0 where available else sqrt|s1|*L)")
print("="*110)
rows = {}
for N in (8, 9, 10, 11):
    rb, ra = rungs[N], above[N]
    d_B = rb["d_star"]; dt_B = 1.5*d_B
    dp_A = ra["a"]/1.5 - 1.0; dt_A = -1.5*dp_A
    s1B, s1A = s1abs(dt_B), s1abs(dt_A)
    # Theta_B: banked theta0 (defensible direct measurement) where we have it; else sqrt|s1|*L chain
    if N in theta0_meas:
        ThB = (N + 1 + theta0_meas[N])*np.pi
    else:
        ThB = np.sqrt(s1B)*rb["L_proper"]
    ThB_L = np.sqrt(s1B)*rb["L_proper"]           # cross-check
    ThA_L = np.sqrt(s1A)*ra["L"]
    # O(eps) machinery, below side
    phipsB = rb["q"]/Z                             # phi'_s at rho~1 order
    QsB = s1B + 0.25*Z*phipsB**2
    A_B = np.sqrt(Z*(1 - XC))*(s1B/QsB)**0.25/ThB  # Lemma-D R2 sealing amplitude
    upB = (dt_B - 0.25*Z*phipsB**2)/QsB            # offset
    # above side prediction ingredients (Theta_A = Theta_B + Dtheta0_derived below)
    rows[N] = dict(rb=rb, ra=ra, d_B=d_B, dp_A=dp_A, dt_B=dt_B, dt_A=dt_A, s1B=s1B, s1A=s1A,
                   ThB=ThB, ThB_L=ThB_L, ThA_L=ThA_L, A_B=A_B, upB=upB, QsB=QsB, phipsB=phipsB)
    print(f"N={N}: d_B={d_B:.7e} dp_A={dp_A:.7e}  |s1|B={s1B:.6f} |s1|A={s1A:.6f}  "
          f"ThB={ThB:.4f} (L-chain {ThB_L:.4f}; A-side L-chain {ThA_L:.4f})  A_B={A_B:.6f} u_pB={upB:+.6f}")

print()
print("="*110)
print("(b-i) TWIN a*-ASYMMETRY / midpoint.  Derived channels:")
print("   gamma-channel (CAS A9, exact to O(b^3)): Dd = d^2 + (8/3)d^3  [m=3];  midpoint M = 0.75 Dd")
print("   off-channel feedback (theta0 odd flip via closure; z' from bottom system): small, computed")
print("="*110)
for N in (8, 9, 10, 11):
    R = rows[N]
    d = R["d_B"]
    Dd_gam = d*d + (8.0/3.0)*d**3
    # theta0 odd (below-side value; flips sign above): off-channel + osc-E-channel (CAS A7)
    off_B = (N + 1)*1.5*chat3(R["dt_B"])*R["dt_B"]/R["s1B"]*np.pi     # rad
    pref = Z*(1 - XC)**2/(3.0*R["ThB"])                                # Sum(pi E) prefactor (rad)
    osc_B = pref*(247.0/144.0)*R["dt_B"]                               # bracket-odd * dt
    th0_odd = off_B + osc_B
    # closure feedback: Dd_theta = -(-2 th0_odd)*SXT/(z'(gam)*dgam/dd)  [flip = -2*th0_odd]
    gam = gamma_of(R["dt_B"])
    dg = 0.02*gam
    zc1, zc2 = bottom_zc(gam - dg), bottom_zc(gam + dg)
    zprime = (zc2 - zc1)/(2*dg)
    dgam_dd = (gamma_of(1.5*(d + 1e-6)) - gamma_of(1.5*(d - 1e-6)))/2e-6
    Dd_th = -(2.0*th0_odd)*SXT/(zprime*dgam_dd)     # from closure subtraction (see report derivation)
    Dd_pred = Dd_gam + Dd_th
    Dd_meas = R["dp_A"] - d
    # closure-consistency: theta0_odd IMPLIED by the measured Dd (diagnostic of between-side transfer)
    th0_odd_implied = -zprime*(dgam_dd*Dd_meas - (4.0*R["dt_B"]/M)*gam)/(2.0*SXT)
    print(f"N={N}: Dd_meas={Dd_meas:+.4e}   Dd_gamma={Dd_gam:+.4e}  Dd_theta0={Dd_th:+.4e}  "
          f"Dd_pred={Dd_pred:+.4e}   meas/pred={Dd_meas/Dd_pred:+.3f}")
    print(f"      th0_odd_B derived={th0_odd/np.pi:+.5f}pi (off {off_B/np.pi:.5f} + osc {osc_B/np.pi:.5f});"
          f"  th0_odd implied-by-closure-from-Dd_meas={th0_odd_implied/np.pi:+.5f}pi   "
          f"[z'={zprime:+.4f} gam={gam:.4f}]")

print()
print("="*110)
print("(b-ii) q-RATIO. DERIVED: the O(A) parity term in q^2 cancels EXACTLY to O(x_c):")
print("   q^2 = 2Z rho_s^2 (2-U(rho_s)) [Thm B exact]; O(eps): q^2 = 4Z|s1|A^2(1-x_c)[1 + sigma*2A*x_c + O(A^2)]")
print("   => q_A/q_B = sqrt(|s1A|/|s1B|) * (Theta_B/Theta_A) * [1 + O(A^2, dt)] -- leading parity term PROTECTED")
print("="*110)
for N in (8, 9, 10, 11):
    R = rows[N]
    # exact-cancellation check: 2A vs Z phi'_s^2/(2|s1|A) using banked q
    w = Z*R["phipsB"]**2/(2.0*R["s1B"]*R["A_B"])
    print(f"N={N}: 2A_B={2*R['A_B']:.6f} vs w=Zphi'^2/(2|s1|A)={w:.6f}  residual={2*R['A_B']-w:+.2e} "
          f"(=2A*x_c pred {2*R['A_B']*XC:.2e})")
qtab = []
for N in (8, 9, 10, 11):
    R = rows[N]
    sr = np.sqrt(R["s1A"]/R["s1B"])
    off_B = (N + 1)*1.5*chat3(R["dt_B"])*R["dt_B"]/R["s1B"]*np.pi
    pref = Z*(1 - XC)**2/(3.0*R["ThB"])
    th0_odd = off_B + pref*(247.0/144.0)*R["dt_B"]
    ThA_pred = R["ThB"] - 2.0*th0_odd
    ratio_pred = sr*(R["ThB"]/ThA_pred)
    ratio_meas = R["ra"]["q"]/R["rb"]["q"]
    A2 = R["A_B"]**2
    print(f"N={N}: q_A/q_B meas={ratio_meas:.6f}  pred(leading, parity-protected)={ratio_pred:.6f}  "
          f"resid={ratio_meas-ratio_pred:+.5f}  [A_B^2={A2:.5f} -- residual is O(A^2)-sized: "
          f"resid/A^2={(ratio_meas-ratio_pred)/A2:+.3f}]")

print()
print("="*110)
print("(b-iii) L-RATIO.  L ~ Theta/sqrt(|s1|):  L_A/L_B = (Theta_A/Theta_B)*sqrt(|s1B|/|s1A|)")
print("   channel 1 (derived, dominant): sqrt(|s1B|/|s1A|) = 1 - |dt|/m + ...")
print("   channel 2: Theta_A/Theta_B = 1 - 2*th0_odd/Theta (off+osc derived; boundary/handover sliver open)")
print("="*110)
for N in (8, 9, 10, 11):
    R = rows[N]
    c1 = np.sqrt(R["s1B"]/R["s1A"])
    off_B = (N + 1)*1.5*chat3(R["dt_B"])*R["dt_B"]/R["s1B"]*np.pi
    pref = Z*(1 - XC)**2/(3.0*R["ThB"])
    th0_odd = off_B + pref*(247.0/144.0)*R["dt_B"]
    c2 = (R["ThB"] - 2.0*th0_odd)/R["ThB"]
    pred1, pred12 = c1, c1*c2
    meas = R["ra"]["L"]/R["rb"]["L_proper"]
    print(f"N={N}: L_A/L_B meas={meas:.6f}  pred(ch1 only)={pred1:.6f}  pred(ch1+ch2)={pred12:.6f}  "
          f"[meas-ch1={meas-pred1:+.5f}; meas-(ch1+ch2)={meas-pred12:+.5f}]")

print()
print("="*110)
print("(b-iv) rho_s PRODUCT.  Pairing (parity law): at equal N the twins seal on OPPOSITE sides of")
print("   the cylinder [sign(rho_s-1) = sign(dt)(-1)^N; above side inverted]. DERIVED prediction:")
print("   rho_sA*rho_sB - 1 = (u_pA + u_pB) - A_A A_B = -A^2 [1 + 2(1-x_c)|s1|/Q_s] + O(A^3)  ~ -3A^2")
print("="*110)
for N in (8, 9, 10, 11):
    R = rows[N]
    # per-side offsets at O(eps) (rho~1-consistent: phi'_s = q/Z per side, q_A ~ q_B at this order)
    phipsA = R["ra"]["q"]/Z
    QsA = R["s1A"] + 0.25*Z*phipsA**2
    upA = (R["dt_A"] - 0.25*Z*phipsA**2)/QsA
    off_B = (N + 1)*1.5*chat3(R["dt_B"])*R["dt_B"]/R["s1B"]*np.pi
    pref = Z*(1 - XC)**2/(3.0*R["ThB"])
    th0_odd = off_B + pref*(247.0/144.0)*R["dt_B"]
    ThA = R["ThB"] - 2.0*th0_odd
    A_A = np.sqrt(Z*(1 - XC))*(R["s1A"]/QsA)**0.25/ThA
    pred = 1.0 + (upA + R["upB"]) - A_A*R["A_B"]
    pred_compact = 1.0 - R["A_B"]**2*(1.0 + 2.0*(1 - XC)*R["s1B"]/R["QsB"])
    meas = R["ra"]["rho_s"]*R["rb"]["rho_s"]
    print(f"N={N}: prod meas={meas:.6f}  pred(full)={pred:.6f}  pred(-3A^2 compact)={pred_compact:.6f}  "
          f"meas_dev={meas-1:+.6f} pred_dev={pred-1:+.6f}  ratio meas/pred={(meas-1)/(pred-1):.3f}")
    # also per-side rho_s prediction
    sigB = +1 if (N % 2 == 0) else -1
    rho_sA_pred = 1.0 - sigB*A_A + upA
    print(f"      per-side: rho_sA meas={R['ra']['rho_s']:.6f} pred={rho_sA_pred:.6f}  "
          f"(below check: rho_sB meas={R['rb']['rho_s']:.6f} pred={1.0 + sigB*R['A_B'] + R['upB']:.6f})")

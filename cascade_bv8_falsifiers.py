"""bv8 falsifiers F1/F2/F3 on banked cascade data. CPU, single process.
F1: seal-energy identity U(rho_s) =?= 2 - q^2/(2 Z rho_s^2), U from the SLICE FORMULA at the
    banked rung a* (Stage B, risefall m=3 Z=8) / p* (Stage C c2, risefall m=3 Z=1). Zero fits.
F2: re-shoot rungs N=5 and N=15 (banked a*); interior extrema amplitude ratios vs the claimed
    e^{phi} envelope AND vs the WKB e^{phi/2} envelope (my independent derivation).
F3: Theorem-A bracket on the SAME trajectories: q_pred = Z*Dphi / int(Phi/q /rho^2) vs banked q.
Total IVP shots: 2.
"""
import json, sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

Z = 8.0
LN1101 = float(np.log(1101.0))
PHI_C = -LN1101

def U_risefall(rho, a, m=3.0):
    return 2.0 * rho**m * np.exp(-a * (rho*rho - 1.0))
def Up_risefall(rho, a, m=3.0):
    return U_risefall(rho, a, m) * (m/rho - 2.0*a*rho)

def rhs(r, y, Zv, a):
    phi, phip, rho, rhop = y
    e2p = np.exp(2.0*phi)
    sigma = 0.25*e2p*Up_risefall(rho, a)
    phipp = 4.0*rhop*rhop/(e2p*Zv*rho*rho) - 2.0*phip*rhop/rho
    rhopp = 2.0*phip*rhop - 0.25*Zv*rho*e2p*phip*phip + sigma
    return [phip, phipp, rhop, rhopp]

SHOTS = 0
def shoot(a, Zv=Z, rtol=1e-10, atol=1e-12, r_max=5e7):
    global SHOTS; SHOTS += 1
    seal = lambda r, y, *aa: y[0]; seal.terminal, seal.direction = True, +1
    coll = lambda r, y, *aa: y[2] - 1e-9; coll.terminal, coll.direction = True, -1
    sol = solve_ivp(rhs, (0.0, r_max), [PHI_C, 0.0, 1.0, 0.0], args=(Zv, a),
                    method="LSODA", rtol=rtol, atol=atol, events=[seal, coll],
                    dense_output=True)
    assert sol.t_events[0].size and not sol.t_events[1].size, "no seal reached"
    r_s = sol.t_events[0][0]
    phi_s, phip_s, rho_s, rhop_s = sol.y_events[0][0]
    return dict(sol=sol, r_s=r_s, rho_s=rho_s, rhop_s=rhop_s, phip_s=phip_s,
                q=Zv*rho_s**2*phip_s)

# =============================================================== F1
print("="*100)
print("F1: seal identity residual  res = U_slice(rho_s; a*) - [2 - q^2/(2 Z rho_s^2)]  (banked values only)")
B = json.load(open("/home/udt-admin/udt_mass_codex/cascade_stageB_rungs.json"))
print("\n-- Stage B (A1 m=3, Z=8), 23 rungs --")
print(f"{'N':>3} {'a*':>14} {'q':>12} {'rho_s':>10} {'U_slice':>14} {'2-q^2/(2Zr^2)':>14} {'residual':>12} {'|res| vs rhop_res*scale':>10}")
worstB = 0.0
for rg in B["rungs"]:
    a = rg["a_star"]; q = rg["q"]; rs = rg["rho_s"]
    Us = U_risefall(rs, a)
    rhsv = 2.0 - q*q/(2.0*Z*rs*rs)
    res = Us - rhsv
    worstB = max(worstB, abs(res))
    print(f"{rg['N_delta']:>3} {a:>14.10f} {q:>12.6f} {rs:>10.6f} {Us:>14.8f} {rhsv:>14.8f} {res:>12.3e}")
print(f"   worst |residual| Stage B: {worstB:.3e}")

C2j = json.load(open("/home/udt-admin/udt_mass_codex/cascade_stageC_c2_A1m3_Z1.json"))
print("\n-- Stage C c2 (A1 m=3, Z=1), rungs --")
worstC = 0.0
for rg in C2j["rungs"]:
    a = rg["p_star"]; q = rg["q"]; rs = rg["rho_s"]
    Us = U_risefall(rs, a)
    rhsv = 2.0 - q*q/(2.0*1.0*rs*rs)
    res = Us - rhsv
    worstC = max(worstC, abs(res))
    print(f"{rg['N_delta']:>3} {a:>14.10f} {q:>12.6f} {rs:>10.6f} {Us:>14.8f} {rhsv:>14.8f} {res:>12.3e}")
print(f"   worst |residual| Stage C c2: {worstC:.3e}")

print("\n-- Claim-B trend check (banked, Stage B): U(rho_s,N) -> 2 ? --")
for rg in B["rungs"]:
    q = rg["q"]; rs = rg["rho_s"]
    print(f"   N={rg['N_delta']:>2}  q={q:9.5f}  rho_s={rs:8.5f}  2-U(rho_s) = q^2/(2Z rho_s^2) = {q*q/(2*Z*rs*rs):.6f}")

print("\n-- Claim-A attack (banked): q(Z=1)/q(Z=8) at equal N, same slice family A1 m=3 --")
qB = {rg["N_delta"]: rg["q"] for rg in B["rungs"]}
qC = {rg["N_delta"]: rg["q"] for rg in C2j["rungs"]}
for N in sorted(set(qB) & set(qC)):
    rat = qC[N]/qB[N]
    print(f"   N={N:>2}  q(Z=1)={qC[N]:9.5f}  q(Z=8)={qB[N]:9.5f}  ratio={rat:8.5f}  (0.125 if bracket Z-free)"
          f"  => B(8)/B(1) = 8*ratio = {8*rat:7.4f}")

# =============================================================== F2 + F3
def analyze(tag, a_star, q_banked, rs_banked, rho_s_banked):
    o = shoot(a_star)
    sol, r_s = o["sol"], o["r_s"]
    print("\n" + "="*100)
    print(f"F2/F3 rung {tag}: a*={a_star:.10f}  re-shot r_s={r_s:.4f} (banked {rs_banked:.4f})  "
          f"rho_s={o['rho_s']:.6f} (banked {rho_s_banked:.6f})  q={o['q']:.8f} (banked {q_banked:.8f})  "
          f"rhop_s={o['rhop_s']:+.2e}")
    # dense grid
    n = 400001
    rr = np.linspace(0.0, r_s, n)
    phi, phip, rho, rhop = sol.sol(rr)
    # interior extrema of rho: sign changes of rhop, refined by brentq on dense output
    f = lambda x: sol.sol(x)[3]
    idx = np.where(np.sign(rhop[1:-1]) * np.sign(rhop[2:]) < 0)[0] + 1
    ext = []
    for i in idx:
        try:
            xr = brentq(f, rr[i], rr[i+1], xtol=1e-12*max(1.0, rr[i]))
        except ValueError:
            continue
        ph, _, rh, _ = sol.sol(xr)
        ext.append((xr, rh - 1.0, ph))
    print(f"   interior extrema found: {len(ext)}")
    # F2 table: successive same-parity extrema (every 2nd)
    print(f"   {'pair':>5} {'r1':>10} {'r2':>10} {'|d1|':>12} {'|d2|':>12} {'measured':>10} "
          f"{'e^dphi':>10} {'e^dphi/2':>10} {'meas/e^dphi':>12} {'meas/e^dphi2':>12}")
    meas_all, pred1_all, pred2_all = [], [], []
    for j in range(len(ext) - 2):
        r1, d1, p1 = ext[j]
        r2, d2, p2 = ext[j + 2]
        if d1 == 0 or np.sign(d1) != np.sign(d2):
            continue
        meas = abs(d2) / abs(d1)
        e1 = np.exp(p2 - p1); e2 = np.exp(0.5*(p2 - p1))
        meas_all.append(meas); pred1_all.append(e1); pred2_all.append(e2)
        print(f"   {j:>5} {r1:>10.2f} {r2:>10.2f} {abs(d1):>12.5e} {abs(d2):>12.5e} {meas:>10.5f} "
              f"{e1:>10.5f} {e2:>10.5f} {meas/e1:>12.5f} {meas/e2:>12.5f}")
    if ext:
        r1, d1, p1 = ext[0]; r2, d2, p2 = ext[-1] if np.sign(ext[-1][1]) == np.sign(d1) else ext[-2]
        cum = abs(d2)/abs(d1); ce1 = np.exp(p2-p1); ce2 = np.exp(0.5*(p2-p1))
        print(f"   CUMULATIVE first->last same-sign extremum: measured={cum:.4f}  "
              f"e^dphi={ce1:.4f}  e^(dphi/2)={ce2:.4f}  meas/e^dphi={cum/ce1:.4f}  meas/e^(dphi/2)={cum/ce2:.4f}")
    ma, p1a, p2a = map(np.asarray, (meas_all, pred1_all, pred2_all))
    print(f"   per-pair geometric means: measured={np.exp(np.mean(np.log(ma))):.5f}  "
          f"e^dphi={np.exp(np.mean(np.log(p1a))):.5f}  e^(dphi/2)={np.exp(np.mean(np.log(p2a))):.5f}")
    print(f"   max |log(meas/e^dphi)| = {np.max(np.abs(np.log(ma/p1a))):.4f}   "
          f"max |log(meas/e^(dphi/2))| = {np.max(np.abs(np.log(ma/p2a))):.4f}")
    # F3: bracket
    Phi = Z * rho**2 * phip
    q_meas = o["q"]
    bracket_hat = np.trapezoid((Phi / q_meas) / rho**2, rr)
    dphi_meas = phi[-1] - phi[0]
    q_pred_pin = Z * LN1101 / bracket_hat
    q_pred_meas = Z * dphi_meas / bracket_hat
    print(f"   F3: bracket int(Phihat/rho^2) = {bracket_hat:.10f}   Dphi_measured = {dphi_meas:.10f} "
          f"(ln1101 = {LN1101:.10f})")
    print(f"       q_pred(pin Dphi=ln1101) = {q_pred_pin:.8f}   q_pred(measured Dphi) = {q_pred_meas:.8f}")
    print(f"       banked q = {q_banked:.8f}   rel diff vs banked: {abs(q_pred_pin-q_banked)/q_banked:.3e} "
          f"(pin) / {abs(q_pred_meas-q_banked)/q_banked:.3e} (meas)")
    print(f"       re-shot q = {q_meas:.8f}   rel diff q_pred(pin) vs re-shot: "
          f"{abs(q_pred_pin-q_meas)/q_meas:.3e}")
    return ext

r5  = [rg for rg in B["rungs"] if rg["N_delta"] == 5][0]
r15 = [rg for rg in B["rungs"] if rg["N_delta"] == 15][0]
analyze("N=5  (Z=8, m=3)", r5["a_star"],  r5["q"],  r5["r_s"],  r5["rho_s"])
analyze("N=15 (Z=8, m=3)", r15["a_star"], r15["q"], r15["r_s"], r15["rho_s"])
print(f"\nTotal IVP shots: {SHOTS}")

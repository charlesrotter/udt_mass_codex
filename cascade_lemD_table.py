"""LEMMA D — numeric test of R1/R2 against ALL banked rungs (no re-shooting, no fits).

R1 (launch-free, from double closure + averaged flux; s1 = |s~1|(d*) exact):
    a_pred = q / ( 2 sqrt(Z (1-x_c)) * (s1 * Q_s)^{1/4} ),   Q_s = s1 + (Z/4) phi_s'^2,
    phi_s' = q/(Z rho_s^2),  x_c = 1/1101.
Banked oscillation amplitude (offset-corrected; parity law banked/verified):
    rho_s - 1 = sign(dt)(-1)^N a_osc + u_p(seal),  u_p = (dt - (Z/4) phi_s'^2)/Q_s
    => a_osc = | rho_s - 1 - u_p |.
R2 (phase law): Theta_implied = sqrt(Z(1-x_c)) (s1/Q_s)^{1/4} / a_osc;
    theta_0 = Theta_implied - (N+1) pi  (the UNDERIVED O(1) launch/onset phase).
Launch factor (route R3, NOT derived — measured): F = a_osc * s1 / (dt * sqrt(1101)).
Family constants dt(d), s1(d): exact (lemD_cas.py S9).
"""
import json
import numpy as np

BASE = "/home/udt-admin/udt_mass_codex/"
XC = 1.0/1101.0
SQ1101 = np.sqrt(1101.0)

def A1(m):
    return (lambda d: m*d/2.0,
            lambda d: -( -(m/2.0)*(m*d**2 + d*m/... ) ))  # placeholder

# exact family constants from CAS (lemD_cas.py S9); s1 returned as |s~1| (positive)
FAM = {
    "c1_A1m2_Z8": (8.0, lambda d: d,        lambda d: -(2*d**2 + d - 2)),
    "c2_A1m3_Z1": (1.0, lambda d: 1.5*d,    lambda d: -(4.5*d**2 + 1.5*d - 3)),
    "c3_A2k3_Z8": (8.0, lambda d: d,        lambda d: -(2*d**2 + 2*d - 3)),
    "c4_A3_Z8":   (8.0, lambda d: -d/(d-2), lambda d: -((3*d**2 + 6*d - 8)/(d**2 - 4*d + 4))),
    "c5_A1m4_Z8": (8.0, lambda d: 2*d,      lambda d: -(8*d**2 + 2*d - 4)),
    "stageB_A1m3_Z8": (8.0, lambda d: 1.5*d, lambda d: -(4.5*d**2 + 1.5*d - 3)),
}

def load():
    rungs = {}
    for c, f in [("c1_A1m2_Z8", "cascade_stageC_c1_A1m2_Z8.json"),
                 ("c2_A1m3_Z1", "cascade_stageC_c2_A1m3_Z1.json"),
                 ("c3_A2k3_Z8", "cascade_stageC_c3_A2k3_Z8.json"),
                 ("c4_A3_Z8",   "cascade_stageC_c4_A3_Z8.json"),
                 ("c5_A1m4_Z8", "cascade_stageC_c5_A1m4_Z8.json")]:
        rungs[c] = json.load(open(BASE + f))["rungs"]
    rungs["stageB_A1m3_Z8"] = json.load(open(BASE + "cascade_stageB_rungs.json"))["rungs"]
    return rungs

def row(combo, r):
    Z, dtf, s1f = FAM[combo]
    N, d, q, rho_s = r["N_delta"], r["d_star"], r["q"], r["rho_s"]
    dt, s1 = dtf(d), s1f(d)
    phps = q/(Z*rho_s**2)
    Qs = s1 + 0.25*Z*phps**2
    up = (dt - 0.25*Z*phps**2)/Qs
    a_osc = abs(rho_s - 1.0 - up)
    a_pred = q/(2.0*np.sqrt(Z*(1.0-XC))*(s1*Qs)**0.25)
    Theta = np.sqrt(Z*(1.0-XC))*(s1/Qs)**0.25/a_osc
    th0 = Theta - (N+1)*np.pi
    F = a_osc*s1/(dt*SQ1101)
    return dict(N=N, d=d, q=q, rho_s=rho_s, s1=s1, dt=dt, a_osc=a_osc,
                a_pred=a_pred, ratio=a_pred/a_osc, absr=abs(rho_s-1.0),
                Theta=Theta, th0_over_pi=th0/np.pi, F=F,
                q_over_sqrt_s1=q/np.sqrt(s1))

rungs = load()
order = ["c1_A1m2_Z8", "c3_A2k3_Z8", "c4_A3_Z8", "c5_A1m4_Z8", "stageB_A1m3_Z8", "c2_A1m3_Z1"]

print("=" * 118)
print("R1 TEST: a_pred = q/(2 sqrt(Z(1-x_c)) (s1*Qs)^{1/4})   vs   a_osc = |rho_s-1-u_p|   (all banked, N=5..11)")
print("=" * 118)
hdr = f"{'combo':<16}{'N':>3}{'d*':>11}{'|s1|':>8}{'q':>10}{'|rho_s-1|':>11}{'a_osc':>10}{'a_pred':>10}{'pred/osc':>10}{'Theta':>9}{'th0/pi':>8}{'F':>8}"
print(hdr)
allr = []
for c in order:
    for r in rungs[c]:
        x = row(c, r)
        if 5 <= x["N"] <= 11:
            allr.append((c, x))
            print(f"{c:<16}{x['N']:>3}{x['d']:>11.3e}{x['s1']:>8.4f}{x['q']:>10.5f}"
                  f"{x['absr']:>11.5f}{x['a_osc']:>10.5f}{x['a_pred']:>10.5f}{x['ratio']:>10.4f}"
                  f"{x['Theta']:>9.3f}{x['th0_over_pi']:>8.3f}{x['F']:>8.4f}")
    print("-" * 118)

ratios = np.array([x["ratio"] for _, x in allr])
print(f"R1 pred/osc over all {len(ratios)} rungs (N=5..11, 5 fam Z=8 + 1 fam Z=1):")
print(f"    mean = {ratios.mean():.4f}   rms dev from 1 = {np.sqrt(np.mean((ratios-1)**2)):.4f}"
      f"   max |dev| = {np.max(np.abs(ratios-1)):.4f}")

print()
print("q ∝ sqrt|s1| at fixed (Z,N) — the derived family-cancellation channel (Z=8 families):")
for N in range(5, 12):
    vals = []
    for c in order[:5]:
        for r in rungs[c]:
            if r["N_delta"] == N:
                vals.append(row(c, r)["q_over_sqrt_s1"])
    if len(vals) >= 4:
        v = np.array(vals)
        print(f"    N={N:>2}: q/sqrt|s1| = {np.array2string(v, precision=4)}   spread = {(v.max()-v.min())/v.mean()*100:.2f}%"
              f"   (raw q spread = {'{:.1f}'.format((max(r['q'] for c in order[:5] for r in rungs[c] if r['N_delta']==N)/min(r['q'] for c in order[:5] for r in rungs[c] if r['N_delta']==N)-1)*100)}%)")

print()
print("Z-SCALING sharp test at N=8 (same family A1m3): a_seal ∝ sqrt(Z) at fixed Theta")
x8 = row("stageB_A1m3_Z8", [r for r in rungs["stageB_A1m3_Z8"] if r["N_delta"] == 8][0])
x1 = row("c2_A1m3_Z1", [r for r in rungs["c2_A1m3_Z1"] if r["N_delta"] == 8][0])
print(f"    banked  a_osc(Z=1)/a_osc(Z=8) = {x1['a_osc']/x8['a_osc']:.4f}")
print(f"    leading R2 (theta0 equal)     = 1/sqrt(8) = {1/np.sqrt(8):.4f}")
print(f"    R2 with measured theta0s      = sqrt(1/8)*Theta8/Theta1 = {np.sqrt(1/8.)*x8['Theta']/x1['Theta']:.4f}")
print(f"    R1 per-Z residuals: Z=8 pred/osc = {x8['ratio']:.4f},  Z=1 pred/osc = {x1['ratio']:.4f}")

print()
print("Leading parameter-free N-law  a_seal ~ sqrt(Z)/((N+1) pi)  [theta_0 -> 0, NOT derived]:")
for c in ["stageB_A1m3_Z8", "c2_A1m3_Z1"]:
    Z = FAM[c][0]
    line = []
    for r in rungs[c]:
        x = row(c, r)
        if 5 <= x["N"] <= 11:
            line.append(f"N={x['N']}: {np.sqrt(Z)/((x['N']+1)*np.pi)/x['a_osc']:.3f}")
    print(f"    {c:<16} pred/osc: " + "  ".join(line))

print()
print("theta_0/pi drift with N (stageB, N=5..22) — the UNDERIVED onset phase:")
line = [(r["N_delta"], row("stageB_A1m3_Z8", r)["th0_over_pi"]) for r in rungs["stageB_A1m3_Z8"] if r["N_delta"] >= 5]
print("    " + "  ".join(f"({n},{t:.3f})" for n, t in line))

print()
print("Launch factor F = a_osc*s1/(dt*sqrt(1101))  (route R3; F=1 would mean naive core-launch WKB transfer):")
for c in order:
    Fv = [f"N={row(c,r)['N']}:{row(c,r)['F']:.3f}" for r in rungs[c] if 5 <= r["N_delta"] <= 11]
    print(f"    {c:<16} " + "  ".join(Fv))

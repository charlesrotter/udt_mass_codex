"""bv9_tables.py -- D4 numeric verification from banked JSONs only (no IVP shots).
Own s~1 evaluation per family at banked p*; q/sqrt|s1| collapse; rho_s-1 prediction; Q_s table.
"""
import json
import numpy as np

REPO = "/home/udt-admin/udt_mass_codex"
XC = 1.0/1101.0
LN1101 = np.log(1101.0)

# --- s~1 = U''(1)/4 (sympy-derived in bv9_cas.py) ---
def s1_A1(m, a): return (8*a*a - 8*a*m - 4*a + 2*m*m - 2*m)/4.0
def s1_A2(k, a): return (2*a*a*k*k - 2*a*k*k - 6*a*k + 4)/4.0
def s1_A3(b):    return (3*b*b - 12*b + 1)/(1+b)**2

def load(f): return json.load(open(f"{REPO}/{f}"))

fams = {}
# stageC combos: rungs carry p_star, N_delta, q, rho_s
for f, name, s1f in [
    ("cascade_stageC_c1_A1m2_Z8.json", "A1m2_Z8", lambda p: s1_A1(2.0, p)),
    ("cascade_stageC_c3_A2k3_Z8.json", "A2k3_Z8", lambda p: s1_A2(3.0, p)),
    ("cascade_stageC_c4_A3_Z8.json",   "A3_Z8",   lambda p: s1_A3(p)),
    ("cascade_stageC_c5_A1m4_Z8.json", "A1m4_Z8", lambda p: s1_A1(4.0, p)),
    ("cascade_stageC_c2_A1m3_Z1.json", "A1m3_Z1", lambda p: s1_A1(3.0, p)),
]:
    d = load(f)
    Z = d["Z"]
    rows = {}
    for rg in d["rungs"]:
        N = rg["N_delta"]
        rows[N] = dict(p=rg["p_star"], q=rg["q"], rho_s=rg["rho_s"], s1=s1f(rg["p_star"]))
    fams[name] = dict(Z=Z, rows=rows)

# stageB = A1 m=3 Z=8 (risefall m=3), a_star column
d = load("cascade_stageB_rungs.json")
rows = {}
for rg in d["rungs"]:
    N = rg["N_delta"]
    rows[N] = dict(p=rg["a_star"], q=rg["q"], rho_s=rg["rho_s"], s1=s1_A1(3.0, rg["a_star"]))
fams["A1m3_Z8"] = dict(Z=8.0, rows=rows)

Z8 = ["A1m2_Z8", "A2k3_Z8", "A3_Z8", "A1m4_Z8", "A1m3_Z8"]

print("="*100)
print("s~1 at banked p* per family (N=5..11) [own symbolic formula]")
print("="*100)
for name in Z8 + ["A1m3_Z1"]:
    F = fams[name]
    line = f"{name:9s}: "
    for N in range(5, 12):
        if N in F["rows"]:
            line += f"N{N}:{F['rows'][N]['s1']:+.5f}  "
    print(line)

print()
print("="*100)
print("D4(i): raw-q spread vs q/sqrt|s1| spread across the FIVE Z=8 families, N=5..11")
print("spread = (max-min)/mean;  also rms/mean in parens")
print("="*100)
print(f"{'N':>3} | {'raw q values':^58} | {'raw spread':>10} | {'collapsed spread':>16}")
for N in range(5, 12):
    qs, qn = [], []
    for name in Z8:
        F = fams[name]
        if N not in F["rows"]:
            continue
        rw = F["rows"][N]
        qs.append(rw["q"])
        qn.append(rw["q"]/np.sqrt(-rw["s1"]))
    qs, qn = np.array(qs), np.array(qn)
    sp_raw = (qs.max()-qs.min())/qs.mean()
    sp_col = (qn.max()-qn.min())/qn.mean()
    rms_raw = qs.std()/qs.mean(); rms_col = qn.std()/qn.mean()
    print(f"{N:>3} | " + " ".join(f"{v:8.5f}" for v in qs) + f" (n={len(qs)}) "
          f"| {100*sp_raw:9.2f}% ({100*rms_raw:.2f}%) | {100*sp_col:9.3f}% ({100*rms_col:.3f}%)")
    print(f"    | q/sqrt|s1|: " + " ".join(f"{v:8.5f}" for v in qn))

print()
print("="*100)
print("D4(iii): Q_s = |s1| + (Z/4) phi'_s^2,  phi'_s = q/(Z rho_s^2)   [banked q, rho_s]")
print("="*100)
for name in Z8 + ["A1m3_Z1"]:
    F = fams[name]; Z = F["Z"]
    line = f"{name:9s}: "
    for N in (5, 8, 11):
        if N in F["rows"]:
            rw = F["rows"][N]
            phps = rw["q"]/(Z*rw["rho_s"]**2)
            Qs = -rw["s1"] + (Z/4.0)*phps**2
            rw["Qs"] = Qs; rw["phps"] = phps
            line += f"N{N}: Qs={Qs:.5f} (|s1|={-rw['s1']:.5f}, corr={100*(Qs/(-rw['s1'])-1):.3f}%)   "
    print(line)
# fill Qs for all N
for name in fams:
    F = fams[name]; Z = F["Z"]
    for N, rw in F["rows"].items():
        phps = rw["q"]/(Z*rw["rho_s"]**2)
        rw["phps"] = phps
        rw["Qs"] = -rw["s1"] + (Z/4.0)*phps**2

print()
print("="*100)
print("D4(ii): fully-derived |rho_s - 1| prediction at N=8:")
print("  pred = sqrt(Z) (1-x_c)^{1/2} (|s1|/Q_s)^{1/4} / [(N+1)pi + theta0]")
print("="*100)
for th0_lab, th0_Z8, th0_Z1 in [("theta0 = 0", 0.0, 0.0),
                                ("theta0 = 0.32pi (Z=8) / 0.25pi (Z=1) [claimed measured]",
                                 0.32*np.pi, 0.25*np.pi)]:
    print(f"--- {th0_lab} ---")
    for name in Z8 + ["A1m3_Z1"]:
        F = fams[name]; Z = F["Z"]
        th0 = th0_Z8 if Z == 8.0 else th0_Z1
        N = 8
        if N not in F["rows"]:
            continue
        rw = F["rows"][N]
        Theta = (N+1)*np.pi + th0
        pred_pure = np.sqrt(Z)*np.sqrt(1-XC)/Theta                     # no family input at all
        pred_corr = pred_pure*(-rw["s1"]/rw["Qs"])**0.25               # with the Q_s correction
        banked = abs(rw["rho_s"]-1.0)
        print(f"  {name:9s} N=8: banked |rho_s-1| = {banked:.5f} | pred(no family input) = {pred_pure:.5f} "
              f"({100*(pred_pure/banked-1):+.2f}%) | pred(with Qs corr) = {pred_corr:.5f} ({100*(pred_corr/banked-1):+.2f}%)")
print()
print("Z-test (no family input, theta0 measured): pred ratio Z8/Z1 =",
      f"{(np.sqrt(8)/(9*np.pi+0.32*np.pi))/(1/(9*np.pi+0.25*np.pi)):.4f}")
b8 = abs(fams['A1m2_Z8']['rows'][8]['rho_s']-1)
b8b = abs(fams['A1m3_Z8']['rows'][8]['rho_s']-1)
b1 = abs(fams['A1m3_Z1']['rows'][8]['rho_s']-1)
print(f"banked ratio (c1 Z8 / c2 Z1) = {b8/b1:.4f};  (stageB Z8 / c2 Z1) = {b8b/b1:.4f}; sqrt(8)={np.sqrt(8):.4f}")

print()
print("="*100)
print("bonus cross-check: q prediction q = 2 Z sqrt|s1| (1-x_c)/Theta at N=8 (theta0 measured)")
print("="*100)
for name in Z8 + ["A1m3_Z1"]:
    F = fams[name]; Z = F["Z"]
    th0 = 0.32*np.pi if Z == 8.0 else 0.25*np.pi
    rw = F["rows"].get(8)
    if rw is None: continue
    Theta = 9*np.pi + th0
    qpred = 2*Z*np.sqrt(-rw["s1"])*(1-XC)/Theta
    print(f"  {name:9s}: banked q = {rw['q']:.5f} | pred = {qpred:.5f} ({100*(qpred/rw['q']-1):+.2f}%)")

# implied theta0 per family per N (from R2 without Qs corr and with)
print()
print("="*100)
print("implied theta0/pi from banked |rho_s-1| via Theta = sqrt(Z(1-x_c))(|s1|/Qs)^{1/4}/|rho_s-1| - (N+1)pi")
print("="*100)
for name in Z8 + ["A1m3_Z1"]:
    F = fams[name]; Z = F["Z"]
    line = f"{name:9s}: "
    for N in range(5, 12):
        rw = F["rows"].get(N)
        if rw is None: continue
        Theta_imp = np.sqrt(Z*(1-XC))*(-rw["s1"]/rw["Qs"])**0.25/abs(rw["rho_s"]-1.0)
        line += f"N{N}:{(Theta_imp-(N+1)*np.pi)/np.pi:+.3f}  "
    print(line)
# implied theta0 from q: Theta = 2 Z sqrt|s1|(1-xc)/q - (N+1)pi
print()
print("implied theta0/pi from banked q via Theta = 2 Z sqrt|s1| (1-x_c)/q")
for name in Z8 + ["A1m3_Z1"]:
    F = fams[name]; Z = F["Z"]
    line = f"{name:9s}: "
    for N in range(5, 12):
        rw = F["rows"].get(N)
        if rw is None: continue
        Theta_imp = 2*Z*np.sqrt(-rw["s1"])*(1-XC)/rw["q"]
        line += f"N{N}:{(Theta_imp-(N+1)*np.pi)/np.pi:+.3f}  "
    print(line)

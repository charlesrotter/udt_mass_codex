#!/usr/bin/env python3
"""M3b Phase-2: in-sample ruler measurement that CLOSES THE FREEZE.
Prereg af9fa75d. Banked DESI + SNe ONLY. ZERO BOSS contact.

r(z) frozen from SNe M3 verified lead (P1, mode B, F-ANCHOR M_B=-19.253+/-0.027):
  inv_n = 0.947 [0.9284, 0.9658]; X_eff = 2086.0 [2059.1, 2113.2] Mpc
  n = 1/inv_n; R_w = n*X_eff; r(z) = R_w*[1 - (1+z)^(-2/n)]

ell measured from the DESI SKY-ROBUST thread (audit grades, commit af9fa75d/2d9933d1):
  PRIMARY = 3 SKY-ROBUST shells; VARIANT = + 2 INCONCLUSIVE.
theta_b in DEGREES -> radians for ell = theta_rad * r(z).
Center error DERIVED: sigma_center = sigma_b(width) / sqrt(dchi2)  [peak-localization].
"""
import json, math
import numpy as np

DEG = math.pi / 180.0

# ---- SNe-frozen r(z) ----
INV_N = 0.947; INV_N_LO = 0.9284; INV_N_HI = 0.9658
XEFF = 2086.0; XEFF_LO = 2059.1; XEFF_HI = 2113.2

def rz(z, inv_n, xeff):
    n = 1.0 / inv_n
    Rw = n * xeff
    return Rw * (1.0 - (1.0 + z) ** (-2.0 / n))

def Rw_of(inv_n, xeff):
    return (1.0 / inv_n) * xeff

# ---- DESI banked per-shell bumps ----
BASE = "/home/udt-admin/udt_mass_codex/udt_xmax_scale_observational_M3_runs_2026-08-07"
with open(f"{BASE}/bao_results_sys.json") as f:   SYS = json.load(f)
with open(f"{BASE}/bao_results_nosys.json") as f: NOSYS = json.load(f)

def shell(data, key):
    for r in data["per_shell"]:
        if r["key"] == key:
            return r
    raise KeyError(key)

# audit-graded fit sets (keys w/o variant suffix)
PRIMARY_KEYS = ["LRG_0.70_0.75", "LRG_1.00_1.05", "QSO_0.95_1.10"]        # SKY-ROBUST
VARIANT_ADD  = ["LRG_0.90_0.95", "QSO_1.10_1.25"]                          # + INCONCLUSIVE
VARIANT_KEYS = PRIMARY_KEYS + VARIANT_ADD

def collect(data, keys, variant):
    out = []
    for k in keys:
        r = shell(data, f"{k}_{variant}")
        b = r["bump"]
        sig_c = b["sigma_b"] / math.sqrt(b["dchi2"])   # DERIVED center error (deg)
        out.append(dict(key=k, zc=r["zc"], theta_deg=b["theta_b"],
                        sigma_width=b["sigma_b"], dchi2=b["dchi2"], sig_c=sig_c))
    return out

def fit_ell(rows, inv_n, xeff):
    """Weighted least-squares single global ruler: theta_deg = (ell/r(z))/DEG."""
    k = np.array([1.0 / (rz(x["zc"], inv_n, xeff)) / DEG for x in rows])  # deg per Mpc
    y = np.array([x["theta_deg"] for x in rows])
    s = np.array([x["sig_c"] for x in rows])
    w = 1.0 / s**2
    ell = np.sum(y * k * w) / np.sum(k * k * w)
    sig_ell_fit = 1.0 / math.sqrt(np.sum(k * k * w))
    pred = ell * k
    chi2 = float(np.sum(((y - pred) / s) ** 2))
    dof = len(rows) - 1
    return ell, sig_ell_fit, chi2, dof, pred

def ell_syst_band(rows, best_ell):
    """Vary (inv_n, X_eff) over interval corners; refit ell each corner."""
    vals = []
    for iv in (INV_N_LO, INV_N, INV_N_HI):
        for xe in (XEFF_LO, XEFF, XEFF_HI):
            e, *_ = fit_ell(rows, iv, xe)
            vals.append(e)
    return min(vals), max(vals)

def report_set(name, data, keys, variant):
    rows = collect(data, keys, variant)
    ell, sfit, chi2, dof, pred = fit_ell(rows, INV_N, XEFF)
    lo_s, hi_s = ell_syst_band(rows, ell)
    Rw = Rw_of(INV_N, XEFF)
    Rw_lo = Rw_of(INV_N_HI, XEFF_LO)   # n=1/inv_n: larger inv_n -> smaller n -> smaller Rw
    Rw_hi = Rw_of(INV_N_LO, XEFF_HI)
    print(f"\n=== {name}  [{variant}]  ({len(rows)} shells) ===")
    print(f"  shells: {[r['key'] for r in rows]}")
    for r, p in zip(rows, pred):
        print(f"    {r['key']:16s} zc={r['zc']:.3f}  theta_obs={r['theta_deg']:.4f}"
              f"  sig_c={r['sig_c']:.4f}  theta_pred={p:.4f}  (dchi2={r['dchi2']:.1f})")
    print(f"  ell = {ell:.3f} Mpc   fit-stat +/- {sfit:.3f}   "
          f"anchor/r(z) band [{lo_s:.3f}, {hi_s:.3f}]")
    tot_lo = min(lo_s, ell - sfit); tot_hi = max(hi_s, ell + sfit)
    print(f"  ell interval (fit+anchor envelope) = [{tot_lo:.3f}, {tot_hi:.3f}] Mpc")
    print(f"  chi2/dof = {chi2:.3f}/{dof} = {chi2/dof:.3f}   (THREADING QUALITY)")
    ellR = ell / Rw
    ellR_lo = tot_lo / Rw_hi; ellR_hi = tot_hi / Rw_lo
    print(f"  R_w = {Rw:.1f} Mpc [{Rw_lo:.1f}, {Rw_hi:.1f}]")
    print(f"  ell/R_w = {ellR:.5f}  [{ellR_lo:.5f}, {ellR_hi:.5f}]  (D3 dimensionless target)")
    print(f"  ell as fraction of R_w = {100*ellR:.3f}%")
    return dict(name=name, variant=variant, rows=rows, ell=ell, sfit=sfit,
                band=(lo_s, hi_s), tot=(tot_lo, tot_hi), chi2=chi2, dof=dof,
                Rw=Rw, ellR=ellR, ellR_int=(ellR_lo, ellR_hi))

print("#"*70)
print("# M3b Phase-2 in-sample ruler fit (freeze). Prereg af9fa75d.")
print(f"# n = 1/inv_n = {1/INV_N:.5f}   R_w = n*X_eff = {Rw_of(INV_N,XEFF):.2f} Mpc")
print("#"*70)

res = {}
res["PRIMARY_sys"]   = report_set("PRIMARY", SYS,   PRIMARY_KEYS, "sys")
res["PRIMARY_nosys"] = report_set("PRIMARY", NOSYS, PRIMARY_KEYS, "nosys")
res["VARIANT_sys"]   = report_set("VARIANT", SYS,   VARIANT_KEYS, "sys")
res["VARIANT_nosys"] = report_set("VARIANT", NOSYS, VARIANT_KEYS, "nosys")

# ---- DRIFT TENSION (PRIMARY sys), quantified in log-theta bins (Delta ln theta = 0.0914) ----
DLN = 0.0914
print("\n" + "="*70)
print("DRIFT TENSION (PRIMARY sys): observed theta drift vs the ruler's ell/r(z) fall")
rows = res["PRIMARY_sys"]["rows"]
ell = res["PRIMARY_sys"]["ell"]
# order by z; use the two LRG SKY-ROBUST anchors (same-tracer, clean z-baseline)
lrg = [r for r in rows if r["key"].startswith("LRG")]
lrg.sort(key=lambda r: r["zc"])
r1, r2 = lrg[0], lrg[1]
th_pred1 = ell / rz(r1["zc"], INV_N, XEFF) / DEG
th_pred2 = ell / rz(r2["zc"], INV_N, XEFF) / DEG
obs_bins  = math.log(r2["theta_deg"]/r1["theta_deg"]) / DLN
pred_bins = math.log(th_pred2/th_pred1) / DLN
print(f"  LRG baseline z={r1['zc']:.3f} -> z={r2['zc']:.3f}")
print(f"    predicted theta: {th_pred1:.4f} -> {th_pred2:.4f}  ({pred_bins:+.2f} bins, ruler FALLS)")
print(f"    observed  theta: {r1['theta_deg']:.4f} -> {r2['theta_deg']:.4f}  ({obs_bins:+.2f} bins)")
print(f"    MISMATCH = observed - predicted = {obs_bins - pred_bins:+.2f} bins (opposite sign = anti-drift)")
# same-z tracer split (QSO vs LRG at zc=1.025): a single ruler forbids two thetas at one z
qso = [r for r in rows if r["key"].startswith("QSO")][0]
lrg_hi = r2
print(f"  SAME-z split at zc=1.025: LRG theta={lrg_hi['theta_deg']:.4f} vs QSO theta={qso['theta_deg']:.4f}"
      f"  -> ratio {lrg_hi['theta_deg']/qso['theta_deg']:.2f}x "
      f"({math.log(lrg_hi['theta_deg']/qso['theta_deg'])/DLN:+.2f} bins) at ONE z (a single ell forbids this)")

# ---- FROZEN BOSS PREDICTION (PRIMARY sys ell) ----
print("\n" + "="*70)
print("FROZEN OUT-OF-SAMPLE PREDICTION: theta_BAO(z) = ell_PRIMARY / r(z)  [degrees]")
ellP = res["PRIMARY_sys"]["ell"]
lo, hi = res["PRIMARY_sys"]["tot"]
print(f"  ell_PRIMARY(sys) = {ellP:.3f} Mpc  interval [{lo:.3f}, {hi:.3f}]")
BOSS_Z = dict(LOWZ=[0.20,0.25,0.30,0.35,0.40], CMASS=[0.45,0.50,0.55,0.60,0.65])
pred_table = {}
for sample, zs in BOSS_Z.items():
    print(f"  --- BOSS {sample} ---")
    for z in zs:
        th   = ellP/rz(z, INV_N, XEFF)/DEG
        th_l = lo /rz(z, INV_N_LO, XEFF_HI)/DEG   # widest r -> smallest theta
        th_h = hi /rz(z, INV_N_HI, XEFF_LO)/DEG
        pred_table[f"{sample}_{z}"] = (th, th_l, th_h)
        print(f"    z={z:.2f}  theta_pred = {th:.4f} deg   [{min(th_l,th_h):.4f}, {max(th_l,th_h):.4f}]")

# machine-check keys
print("\n" + "="*70)
print("MACHINE-CHECK KEYS")
print(json.dumps({
    "n": 1/INV_N, "Rw_Mpc": Rw_of(INV_N,XEFF),
    "ell_PRIMARY_sys": res["PRIMARY_sys"]["ell"],
    "ell_PRIMARY_nosys": res["PRIMARY_nosys"]["ell"],
    "ell_VARIANT_sys": res["VARIANT_sys"]["ell"],
    "ell_VARIANT_nosys": res["VARIANT_nosys"]["ell"],
    "chi2dof_PRIMARY_sys": res["PRIMARY_sys"]["chi2"]/res["PRIMARY_sys"]["dof"],
    "chi2dof_VARIANT_sys": res["VARIANT_sys"]["chi2"]/res["VARIANT_sys"]["dof"],
    "ellR_PRIMARY_sys": res["PRIMARY_sys"]["ellR"],
    "drift_obs_bins": obs_bins, "drift_pred_bins": pred_bins,
}, indent=1))

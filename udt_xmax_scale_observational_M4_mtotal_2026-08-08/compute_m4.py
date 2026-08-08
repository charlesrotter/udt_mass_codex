"""M4: the M_total translation (prereg 2f709b05). Arithmetic only.

Inputs are the M3 CONSOLIDATED SNe numbers (verified leads); every output is
ORDER-OF-MAGNITUDE (the dimensional lead supplies no dimensionless factor)
and carries the anchor premise (M_B = -19.253 +/- 0.027) + the P1 conditional.
"""
import json

# CODATA / astronomical constants
c = 2.99792458e8          # m/s (exact)
G = 6.67430e-11           # m^3 kg^-1 s^-2 (CODATA 2018)
MPC = 3.0856775814913673e22  # m (IAU)
MSUN = 1.98892e30         # kg
KM = 1.0e3

# M3 CONSOLIDATED inputs (mode B anchored, P1; pair-quote caveat carried)
X_eff = {"best": 2086.0, "lo": 2059.1, "hi": 2113.2}   # Mpc
inv_n = {"best": 0.9470, "lo": 0.9284, "hi": 0.9658}   # 1/n

def n_of(inv): return 1.0 / inv

# Measure rows (O2/O3 exact translations, c0=1):
#   areal:  R_w = n * X_eff
#   proper: 2 R_w / (2 - n)   (finite iff n < 2)
#   optical: divergent for n > 1 (the fitted regime) -- reported as such
def rows(xeff, inv):
    n = n_of(inv)
    Rw = n * xeff
    proper = 2.0 * Rw / (2.0 - n)
    return {"areal_Rw_Mpc": Rw, "proper_Mpc": proper, "n": n}

def mtotal_kg(x_mpc):
    return x_mpc * MPC * c * c / G

def fmt(x): return f"{x:.3e}"

out = {"prereg": "2f709b05", "constants": {"c": c, "G": G, "Mpc_m": MPC,
       "Msun_kg": MSUN},
       "labels": ["ORDER-OF-MAGNITUDE (no dimensionless factor)",
                  "ANCHOR: M_B=-19.253+/-0.027 (SH0ES ladder chain)",
                  "P1-conditional (finite-radius power-law wall)",
                  "measure-tagged per no-pin standing"]}

# Best-fit and interval corners. Honest pairing note: X_eff and inv_n are
# correlated (D1); corner-combination OVERSTATES the range -- flagged.
cases = {"best": (X_eff["best"], inv_n["best"]),
         "lo_corner": (X_eff["lo"], inv_n["hi"]),   # small X_eff, small n
         "hi_corner": (X_eff["hi"], inv_n["lo"])}   # large X_eff, large n
table = {}
for k, (xe, iv) in cases.items():
    r = rows(xe, iv)
    entry = {"n": round(r["n"], 4)}
    for row in ("areal_Rw_Mpc", "proper_Mpc"):
        x = r[row]
        m = mtotal_kg(x)
        entry[row] = {"x_Mpc": round(x, 1), "M_kg": fmt(m),
                      "M_Msun": fmt(m / MSUN)}
    entry["optical"] = "DIVERGENT at fitted n>1 (no number; honest dash)"
    table[k] = entry
out["table"] = table
out["corner_caveat"] = ("X_eff and inv_n are correlated (D1); corner "
                        "combinations overstate the interval -- the table "
                        "is a bounding envelope, not a joint CI.")

# D2(a): equivalent local rate (arithmetic of the model form, not a result)
H0_equiv = c / (2.0 * X_eff["best"] * MPC) * MPC / KM   # km/s/Mpc
out["H0_equivalent_km_s_Mpc"] = round(H0_equiv, 2)

# D3 context row (external, model-dependent, no agreement claim)
out["context_LCDM_bookkeeping"] = ("observable-universe mass estimates "
                                   "~1e53-1e54 kg (model-dependent external "
                                   "number; same order; context only)")

print(json.dumps(out, indent=1))
with open("m4_results.json", "w") as f:
    json.dump(out, f, indent=1)

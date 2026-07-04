"""microphysics_E1_probe_pass.py -- E1 cheap probe pass (NO BVP solves) on the E0 ambient tables.

Pre-registration: microphysics_reentry_miniMAP.md (E1: "cheap analytic/probe pass only").
Derived condition set + identities: microphysics_E1_composite_conditions.py (ALL CHECKS PASS)
+ microphysics_E1_composite_closure_results.md. Inputs: microphysics_E0_ambient_tables.json
(blind-verified). Probes (all characterize; none filters):

  P1 per bracket: seal-position bracket sweep -- U_loc(=E_m), rho_loc, gradients, at the even-
      sixth stations + the U=2 interior crossing r* (the geometric-balance station K_geo=0).
  P2 Derrick tax density tau(r) = -pi_rho*rho = 4 e^{-2phi} rho' rho (the embedded-Derrick
      boundary term per K9); near-core slope vs U'(rho_c) (analytic small-r law tau/r -> U'(1)).
  P3 necessary-condition map N_c(r; xi,kap,N) = xi*N + kap*N^2/(2 rho_loc^2) - U_loc  (<= 0
      required for a seal at r, from E_ang >= xi N + kap N^2/(2 rho^2), K12): sign structure
      across position for a bounded (xi,kap) grid; plateau vs wall admissibility.
  P4 core floor rho_c >= N sqrt(kap/(2(2-xi N)))  (from E_ang(core)=2 + K12 bounds).
  P5 rigid-N=1 energy-branch illustration rho_c/rho_p = sqrt((U_loc-xi)/(2-xi)) -- satisfiable
      at every station, then EXCLUDED by the K11 Derrick contradiction (teeth demonstration).
  P6 station-values validity: G_loc = max(|phi'|, |rho'|/rho), eps(r_p) = r_p*G_loc; and the
      linearized ambient back-reaction amplification ||Psi(r_s <- r_station)|| (4x4 fundamental
      matrix of the banked EOMs linearized on the saved profile -- conditioning of using the
      PURE profile as the leading-order bracket; Category-A soundness check).

Anti-hang: single process; linear 4-dim IVPs on saved fields only; bounded everywhere.
"""
import json
import sys
import numpy as np
from scipy.integrate import solve_ivp

sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cascade_stageA_lib import make_A1, make_A3   # banked slice families (CHOSE, per bracket)

D = json.load(open("/home/udt-admin/udt_mass_codex/microphysics_E0_ambient_tables.json"))
OUT = {"stage": "E1 probe pass", "date": "2026-07-03", "brackets": {}}

# bounded probe grids (Category-A conditioning choices -- coverage, not physics):
XI_GRID = np.array([0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 1.9])
KAP_GRID = np.array([0.01, 0.1, 1.0, 10.0])
N_LIST = [1, 2]

for name, b in D["brackets"].items():
    P = b["profiles"]
    rr = np.array(P["r"]); ph = np.array(P["phi"]); php = np.array(P["phip"])
    ro = np.array(P["rho"]); rop = np.array(P["rhop"]); Em = np.array(P["E_m"])
    pirho = np.array(P["pi_rho"]); e2p = np.array(P["exp_2phi"])
    r_s = b["r_s"]; Zv = b["Z"]
    fam = b["family"]
    if fam[0] == "A1":
        Ufun, Upfun, lab = make_A1(fam[1], b["a_reshot"])
    else:
        Ufun, Upfun, lab = make_A3(b["a_reshot"])
    res = {"slice": lab, "Z": Zv, "r_s": r_s}

    # ---------------- P1: U=2 interior crossing r* (wall-side; K_geo=0 balance station)
    dU = Em - 2.0
    # ignore the core fold itself (dU(0)=0 exactly); find the LAST sign change (wall side).
    # Noise floor 1e-12 (Category-A): samples with |U-2| below it (exact zeros / 4e-16
    # machine noise at the fold's geometric refinement points) are excluded from the sign
    # sequence — verifier a50cf068b5ecf05e2 caught 0<->noise transitions being counted as
    # crossings; genuine crossings are counted across the nonzero-magnitude samples only.
    tail = dU[5:]
    kept = np.where(np.abs(tail) > 1e-12)[0]
    sgn = np.sign(tail[kept])
    idx = np.where(np.diff(sgn) != 0)[0]
    r_star = None
    if idx.size:
        i = kept[idx[-1]] + 5
        i2 = kept[idx[-1] + 1] + 5
        # linear interp across the (possibly non-adjacent) bracketing samples
        r_star = rr[i] + (rr[i2] - rr[i]) * (0 - dU[i]) / (dU[i2] - dU[i])
        j = i
        res["r_star_over_rs"] = float(r_star / r_s)
        res["rho_at_rstar"] = float(np.interp(r_star, rr, ro))
        res["phip_at_rstar"] = float(np.interp(r_star, rr, php))
        res["rhop_at_rstar"] = float(np.interp(r_star, rr, rop))
        res["n_sign_changes_U_minus_2"] = int(idx.size)

    # ---------------- P2: Derrick tax density tau = -pi_rho * rho = 4 e^{-2phi} rho' rho
    tau = -pirho * ro
    res["tax"] = {
        "max": float(np.max(tau)), "argmax_r_over_rs": float(rr[np.argmax(tau)] / r_s),
        "min": float(np.min(tau)),
        "tax_over_r_plateau_band": [float(np.median((tau[1:] / rr[1:])[rr[1:] < 0.5 * r_s]))],
        "Uprime_at_rho_c": float(Upfun(1.0)),
        "tau_at_seal": float(tau[-1]),
    }
    # near-core law check: tau/r -> U'(rho_c) (phi-independent; see results doc sec P2)
    mask = (rr > 0.01 * r_s) & (rr < 0.1 * r_s)
    res["tax"]["tax_over_r_nearcore_median"] = float(np.median(tau[mask] / rr[mask]))

    # ---------------- P3 + P4: necessary map and core floor
    grid_report = []
    for N in N_LIST:
        for xi in XI_GRID:
            if xi * N >= 2.0:
                grid_report.append({"N": N, "xi": float(xi), "core": "EXCLUDED (xi*N >= 2)"})
                continue
            for kap in KAP_GRID:
                Nc = xi * N + kap * N**2 / (2.0 * ro**2) - Em     # <= 0 necessary for seal at r
                # exclude the exact core fold point (not a seal candidate: r_p > 0)
                adm = Nc[1:] <= 0
                frac = float(np.mean(adm))
                changes = int(np.sum(np.diff(np.sign(Nc[1:] + 1e-300)) != 0))
                plateau_ok = bool(Nc[1:][rr[1:] < 0.5 * r_s].max() <= 0) if np.any(rr[1:] < 0.5 * r_s) else None
                seal_ok = bool(Nc[-1] <= 0)
                grid_report.append({
                    "N": N, "xi": float(xi), "kap": float(kap),
                    "admissible_fraction": frac, "n_sign_changes": changes,
                    "plateau_admissible": plateau_ok, "outer_seal_admissible": seal_ok,
                    "rho_c_floor": float(N * np.sqrt(kap / (2.0 * (2.0 - xi * N)))),
                })
    res["necessary_map"] = grid_report

    # summary teeth: the seal-station bound on xi*N (kap -> 0 limit) per station class
    res["xiN_bound_plateau"] = float(np.min(Em[(rr > 0.05 * r_s) & (rr < 0.5 * r_s)]))
    res["xiN_bound_at_outer_seal"] = float(Em[-1])

    # ---------------- P5: rigid-N=1 energy-branch (illustration; K11 excludes it)
    st = b["stations"]
    rig = []
    for s in st:
        Uloc = s["E_m"]
        row = {"station": s["station"], "r_over_rs": s["r"] / r_s, "U_loc": Uloc}
        xi0 = 0.5
        if Uloc > xi0:
            row["rhoc_over_rhop_xi0.5"] = float(np.sqrt((Uloc - xi0) / (2.0 - xi0)))
        rig.append(row)
    res["rigid_energy_branch"] = rig

    # ---------------- P6: validity / conditioning
    G = np.maximum(np.abs(php), np.abs(rop) / ro)
    res["G_loc_stations"] = [{"station": s["station"], "r_over_rs": s["r"] / r_s,
                              "G_loc": float(np.interp(s["r"], rr, G))} for s in st]
    res["G_loc_max"] = float(np.max(G))

    OUT["brackets"][name] = res

# ---------------- P6b: linearized back-reaction amplification (bounded: 2 brackets, 3 stations)
def amplification(bname, stations_idx=(1, 3, 5)):
    b = D["brackets"][bname]
    P = b["profiles"]
    rr = np.array(P["r"]); ph = np.array(P["phi"]); php = np.array(P["phip"])
    ro = np.array(P["rho"]); rop = np.array(P["rhop"])
    Zv = b["Z"]; r_s = b["r_s"]
    fam = b["family"]
    Ufun, Upfun, _ = (make_A1(fam[1], b["a_reshot"]) if fam[0] == "A1"
                      else make_A3(b["a_reshot"]))
    h = 1e-7
    Uppfun = lambda x: (Upfun(x + h) - Upfun(x - h)) / (2 * h)

    def Jmat(r):
        p, pp_, q, qp = (np.interp(r, rr, ph), np.interp(r, rr, php),
                         np.interp(r, rr, ro), np.interp(r, rr, rop))
        e2 = np.exp(2 * p); em2 = np.exp(-2 * p)
        J = np.zeros((4, 4))
        # y = (phi, phi', rho, rho'); phi'' = 4 em2 qp^2/(Z q^2) - 2 pp qp / q
        J[0, 1] = 1.0
        J[1, 0] = -8 * em2 * qp**2 / (Zv * q**2)
        J[1, 1] = -2 * qp / q
        J[1, 2] = -8 * em2 * qp**2 / (Zv * q**3) + 2 * pp_ * qp / q**2
        J[1, 3] = 8 * em2 * qp / (Zv * q**2) - 2 * pp_ / q
        # rho'' = 2 pp qp - (Z/4) q e2 pp^2 + (e2/4) U'(q)
        J[2, 3] = 1.0
        J[3, 0] = -(Zv / 2) * q * e2 * pp_**2 + (e2 / 2) * Upfun(q)
        J[3, 1] = 2 * qp - (Zv / 2) * q * e2 * pp_
        J[3, 2] = -(Zv / 4) * e2 * pp_**2 + (e2 / 4) * Uppfun(q)
        J[3, 3] = 2 * pp_
        return J

    out = []
    for k in stations_idx:
        s = b["stations"][k]
        r0 = s["r"]
        def rhslin(r, Y):
            return (Jmat(r) @ Y.reshape(4, 4)).reshape(-1)
        sol = solve_ivp(rhslin, (r0, r_s), np.eye(4).reshape(-1), method="LSODA",
                        rtol=1e-8, atol=1e-10, dense_output=False)
        Psi = sol.y[:, -1].reshape(4, 4)
        out.append({"station": s["station"], "r_over_rs": r0 / r_s,
                    "norm2_Psi": float(np.linalg.norm(Psi, 2)),
                    "success": bool(sol.success)})
    return out

for bname in ("A1 m=3 Z=8", "A3 Z=1"):
    OUT["brackets"][bname]["backreaction_amplification"] = amplification(bname)

# ---------------- report
for name, res in OUT["brackets"].items():
    print(f"\n===== {name}  ({res['slice']}) =====")
    if "r_star_over_rs" in res:
        print(f"  U=2 crossing r*/r_s = {res['r_star_over_rs']:.6f}  rho(r*)={res['rho_at_rstar']:.6f} "
              f" phi'(r*)={res['phip_at_rstar']:.4g}  rho'(r*)={res['rhop_at_rstar']:.4g} "
              f" [{res['n_sign_changes_U_minus_2']} interior sign change(s) of U-2]")
    t = res["tax"]
    print(f"  Derrick tax tau = 4e^-2phi rho' rho: max={t['max']:.4g} at r/r_s={t['argmax_r_over_rs']:.4f}; "
          f"tau(seal)={t['tau_at_seal']:.3g}; near-core tau/r={t['tax_over_r_nearcore_median']:.5g} "
          f"vs U'(rho_c)={t['Uprime_at_rho_c']:.5g}")
    print(f"  xi*N ceilings (kap->0): plateau-min(E_m)={res['xiN_bound_plateau']:.6f}; "
          f"outer-seal E_m={res['xiN_bound_at_outer_seal']:.6f}")
    nmap = [g for g in res["necessary_map"] if "kap" in g]
    n_excl = sum(1 for g in res["necessary_map"] if "core" in g)
    sel = [g for g in nmap if 0 < g["admissible_fraction"] < 1]
    print(f"  necessary map: {len(nmap)} (N,xi,kap) cells + {n_excl} xi*N>=2 exclusions; "
          f"{sum(1 for g in nmap if g['admissible_fraction']==1.0)} fully-admissible, "
          f"{sum(1 for g in nmap if g['admissible_fraction']==0.0)} fully-excluded, "
          f"{len(sel)} position-selective")
    for g in sel[:6]:
        print(f"    N={g['N']} xi={g['xi']} kap={g['kap']}: admissible frac={g['admissible_fraction']:.3f} "
              f"sign-changes={g['n_sign_changes']} plateau={g['plateau_admissible']} seal={g['outer_seal_admissible']} "
              f"rho_c_floor={g['rho_c_floor']:.4f}")
    print("  G_loc at stations: " + ", ".join(f"{g['station']}={g['G_loc']:.3g}" for g in res["G_loc_stations"]))
    if "backreaction_amplification" in res:
        for a in res["backreaction_amplification"]:
            print(f"  back-reaction amplification ||Psi(r_s <- {a['station']})||_2 = {a['norm2_Psi']:.4g} "
                  f"(success={a['success']})")

json.dump(OUT, open("/home/udt-admin/udt_mass_codex/microphysics_E1_probe_results.json", "w"), indent=1)
print("\nwrote microphysics_E1_probe_results.json")

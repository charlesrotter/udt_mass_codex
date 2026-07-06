"""n5d_pilot.py -- the bounded Stage-1 N5d pilot DRIVER (per N5d_solver_build_plan.md sec.8).

Stage-1 regime (frozen hopfion source + LIVE ell=2 shear + EXACT phi, whole cosmic cell):
runs the coupled (phi, rho, u-frozen, a2-shear) cell solve of cell_solver_f2d.py with the ell=2
traceless shear DOF UNFROZEN and sourced by the H3-converged hopfion's transverse stress T^{AB}.

WHAT THIS DRIVER DOES (and does NOT):
  * LOADS the FROZEN hopfion source (h4_scripts/stress_profiles.npz, the ell=2 projection sh2(r)
    of the H3 hopfion prod_an256.npz -- Q=0.99, E=286.5).  If missing / not the H3 hopfion it
    ABORTS with a BLOCKER (a fabricated T^{AB} would be a CHOSE contamination).
  * SEEDS a nonzero shear a2_amp=1e-3 (never exact a2=0: the Jacobian is ill-conditioned there).
  * AMPLITUDE CONTINUATION of the source 0->1 in a few steps, LM-solved (warm-started) at each.
  * runs BOTH shear seal BCs (S-Dir and S-JC2) as separate records (whole-before-slice; sec.4).
  * BOUNDED (binding anti-hang): Nr<=16, Nth=8, LM maxit<=30/step, wall budget <=100 s PER seal-BC;
    if the budget is exceeded it STOPS and marks throughput-limited (it NEVER extends the wall).
  * REPORTS numbers only (no merit filter, no physics verdict): q_raw, Pi_phi, M_readout,
    sign_convention, H_seal, Derrick residual, Jacobian cond, phi node count, reduced-source
    turning-point count, and whether a closed cell (H(r_s)=0 with the shear seal BC) exists.

REUSES ONLY the fenced-clean built solver (cell_solver_f2d + n5d_shear): e^{-2phi} EXACT, native
E^{AB} (NO G=8piT), no branch_operator / branchGP / green_response / X / q~Q_H.  The source is a
FROZEN profile (chose-or-derived: FROZEN, ledgered) registered onto the cell at the SEED length L0
(the frozen-in-lab-frame choice); the coarse coupled solve is category-A conditioning.

CLI:  python3 n5d_pilot.py --Nr 16 --Nth 8 --lmax 2 --maxit 30 --budget 100 [--Nr-fallback 12]
      python3 n5d_pilot.py --Nr 8 --Nth 8 --smoke        # assembly smoke: 1 step, <=2 LM iters, 1 BC
Writes: n5d_pilot_SDir.json, n5d_pilot_SJC2.json, n5d_pilot_report.txt  (smoke: n5d_pilot_smoke.json)
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import json
import time
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

import cell_solver_f2d as cs

HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN_NPZ = os.path.join(HERE, "h4_scripts", "stress_profiles.npz")
HOPFION_NPZ = os.path.join(HERE, "hopfion_arc_scripts_2026-07-05", "prod_an256.npz")

# ---- fixed parameters (ALL tagged; identical to cell_solver_f2d __main__) ----
Z = 8.0    # CHOSE-fixed (Route-A structure carrying Route-B's number; held fixed)
XI = 1.0   # CHOSE-units (repo unit convention)
KAP = 1.0  # CHOSE-units (kap/xi sets the absolute cell scale; ratios are the observables)
N = 1      # DERIVED-topological (winding degree; integer)
PRM = (Z, XI, KAP, N)

A2_SEED = 1e-3                                   # nonzero shear seed (Jacobian ill-conditioned at a2=0)
CONT_AMPS = [0.1, 0.25, 0.5, 0.75, 1.0]         # source-amplitude continuation 0 -> target
H_TOL = 1e-6                                     # |H_seal| threshold for "closed cell"
PHI_TOL = 1e-10                                 # residual threshold for "converged"


# =========================================================================================
# FROZEN SOURCE  (load + provenance-verify; NEVER fabricate)
# =========================================================================================
def load_frozen_source():
    """Return (status_dict, source_rc, source_sh2) or (status_dict, None, None) on BLOCKER.
    source_sh2(r) = the ell=2 (P2-weighted) projection of the hopfion transverse traceless shear
    stress T^{AB}, from the H3-converged hopfion.  Provenance is checked, not assumed."""
    st = {"frozen_npz": FROZEN_NPZ, "hopfion_npz": HOPFION_NPZ}
    if not os.path.exists(FROZEN_NPZ):
        st.update(found=False, blocker="stress_profiles.npz MISSING")
        return st, None, None
    d = np.load(FROZEN_NPZ)
    keys = list(d.keys())
    st.update(found=True, keys=keys)
    if "sh2" not in keys or "rc" not in keys:
        st.update(blocker=f"stress_profiles.npz lacks ell=2 shear key 'sh2'/'rc' (has {keys})")
        return st, None, None
    rc = np.asarray(d["rc"], dtype=float)
    sh2 = np.asarray(d["sh2"], dtype=float)
    # provenance: confirm the underlying hopfion is the real H3-converged one (Q~1, E~286)
    hop = {"exists": os.path.exists(HOPFION_NPZ)}
    if hop["exists"]:
        h = np.load(HOPFION_NPZ)
        hop.update(Q=float(h["Q"]), E=float(h["E"]), E2=float(h["E2"]), E4=float(h["E4"]),
                   Ngrid=int(h["N"]), xi=float(h["xi"]), kappa=float(h["kappa"]))
        # is-the-H3-hopfion sanity: unit Hopf charge, balanced virial (E2~E4), sizable energy
        is_h3 = (abs(hop["Q"] - 1.0) < 0.05) and (abs(hop["E2"] / hop["E4"] - 1.0) < 0.05) and (hop["E"] > 50.0)
        hop["is_h3_hopfion"] = bool(is_h3)
    st.update(hopfion=hop, source_rc_range=[float(rc.min()), float(rc.max())],
              sh2_range=[float(sh2.min()), float(sh2.max())], n_source_pts=int(rc.size))
    return st, rc, sh2


def build_Tshear(ctx, L, amp, source_rc, source_sh2):
    """ell=2 source array on the (Nr,Nth) grid:  Tshear(r,theta) = amp * sh2(r_phys) * P2(mu).
    REGISTRATION B (native pullback, 2026-07-06): the frozen source radial profile is sampled at the
    physical cell nodes r_phys = rc + (L/2)(zeta+1) using the SUPPLIED cell length L (pass the CURRENT
    L, not the seed L0) -- so at L=L0 this reproduces the old registration exactly, and for L!=L0 it
    interpolates at the current physical r (not a fixed zeta-profile).  Source beyond its support is
    clamped to 0 (the hopfion is compact).  NO amplitude Jacobian (interpolation only; 'amp' is the
    continuation factor).  This standalone builds a FIXED array for a given L (diagnostics/tests); the
    SOLVER tracks L live via n5d["src"] (fields() interpolates each residual eval).  Projecting
    Es=Es_geom+Tshear onto P2 gives the ell=2 Galerkin shear equation (E^{AB}=-T^{AB})."""
    r_phys = ctx["rc"] + 0.5 * L * (ctx["zeta"] + 1.0)                    # current-L physical nodes (torch)
    src2 = cs.n5d_shear.source_interp(source_rc, source_sh2, r_phys)      # (Nr,) diff. interp, clamp->0
    P2 = ctx["P2"]                                                        # (Nth,) Legendre P2(mu)
    return amp * src2[:, None] * P2[None, :]                              # (Nr,Nth)


# =========================================================================================
# DIAGNOSTICS  (characterize-only; NO merit filter)
# =========================================================================================
def _sign_changes(arr):
    a = np.asarray(arr, dtype=float)
    s = np.sign(a)
    s = s[s != 0.0]
    if s.size < 2:
        return 0
    return int(np.sum(s[1:] != s[:-1]))


def _turning_points(arr):
    """count local extrema = sign changes of the finite-difference derivative."""
    a = np.asarray(arr, dtype=float)
    if a.size < 3:
        return 0
    d = np.diff(a)
    return _sign_changes(d)


def final_diagnostics(u, ctx, n5d):
    """All scalar readouts + branch labels for a converged/partial vector u (characterize-only)."""
    with torch.no_grad():
        Q = cs.fields(u, ctx, PRM, n5d=n5d)
        phi = Q["phi"].cpu().numpy()
        phip = Q["phip"]
        # reduced radial phi-source RHS = phipp - phi_ode(residual)  (shear-modified; mechanism (i))
        sc = 2.0 / float(Q["L"])
        phipp = sc * sc * (ctx["Dz2"] @ Q["phi"])
        rhs = (phipp - Q["phi_ode"]).cpu().numpy()
        a2 = Q["a2"].cpu().numpy()
        a2p = Q["a2p"]
        Hr = cs.H_of_r(u, ctx, PRM).cpu().numpy()
        ro = cs.readouts(u, ctx, PRM, n5d=n5d)
        Sa, Sb, dS = cs.derrick(u, ctx, PRM)
        cond, smin, smax, nr_, nc_ = cs.jac_condition(u, ctx, PRM, n5d=n5d)
        # shear seal residual value (the load-bearing FREE BC) for the record
        sealbc = n5d.get("sealbc", "off")
        if sealbc == "S-Dir":
            seal_val = float(a2[-1] - float(n5d.get("a2_mirror", 0.0)))
        elif sealbc == "S-JC2":
            seal_val = float(a2p[-1])
        else:
            seal_val = float("nan")
        core_val = float(a2p[0])
    return {
        "q_raw": ro["q_raw"], "Pi_phi": ro["Pi_phi"],
        "sign_convention": ro["sign_convention"], "M_readout": ro["M_readout"],
        "H_seal": float(Hr[-1]), "H_drift_maxmin": float(Hr.max() - Hr.min()),
        "derrick_Sa": Sa, "derrick_Sb": Sb, "derrick_residual": dS,
        "jac_cond": cond, "jac_smin": smin, "jac_shape": [int(nr_), int(nc_)],
        "phi_node_count": _sign_changes(phi),
        "reduced_source_turning_points": _turning_points(rhs),
        "reduced_source_sign_changes": _sign_changes(rhs),
        "shear_core_bc_residual": core_val,
        "shear_seal_bc_residual": seal_val,
        "a2_seal": float(a2[-1]), "a2_peak_abs": float(np.abs(a2).max()),
    }


# =========================================================================================
# ONE SEAL-BC RUN  (nonzero shear seed -> amplitude continuation; bounded budget)
# =========================================================================================
def run_one_bc(sealbc, Nr, Nth, source_rc, source_sh2, maxit, budget,
               amps=CONT_AMPS, a2_mirror=0.0, verbose=False):
    t0 = time.time()
    ctx = cs.make_ctx(Nr, Nth, rc=0.5)
    u = cs.seed_n5d(ctx, a2_amp=A2_SEED)                     # nonzero shear seed (never a2=0)
    _, _, _, _, L0 = cs.unpack(u, ctx, n5d=True)
    L0 = float(L0)                                          # seed length (recorded; NO longer the source anchor)
    steps = []
    throughput_limited = False
    for amp in amps:
        elapsed = time.time() - t0
        remaining = budget - elapsed
        if remaining <= 1.0:
            throughput_limited = True
            break
        # REGISTRATION B: pass the source PROFILE (not a frozen array) so fields() interpolates it at
        # the CURRENT cell L each residual eval -> the source tracks r(zeta)=rc+(L/2)(zeta+1) live.
        n5d = dict(sealbc=sealbc, src=(source_rc, source_sh2, amp), a2_mirror=a2_mirror)
        u, hist = cs.newton_lm_solve(u, ctx, PRM, maxit=maxit, tol=PHI_TOL,
                                     verbose=verbose, time_budget=remaining, n5d=n5d)
        steps.append({"amp": amp, "Phi_start": float(hist[0]), "Phi_final": float(hist[-1]),
                      "iters": len(hist) - 1, "decreased": bool(hist[-1] < hist[0]),
                      "wall_s": round(time.time() - t0, 2)})
        if (time.time() - t0) > budget:
            throughput_limited = True
            break
    # final diagnostics at the last amplitude actually reached (source registered LIVE at the final L)
    last_amp = steps[-1]["amp"] if steps else 0.0
    n5d = dict(sealbc=sealbc, src=(source_rc, source_sh2, last_amp), a2_mirror=a2_mirror)
    diag = final_diagnostics(u, ctx, n5d)
    final_Phi = steps[-1]["Phi_final"] if steps else float("nan")
    converged = bool(final_Phi < 1e-8) if steps else False
    reached_target = bool(last_amp is not None and abs(last_amp - amps[-1]) < 1e-12)
    closed_cell = bool(converged and abs(diag["H_seal"]) < H_TOL and reached_target
                       and abs(diag["shear_seal_bc_residual"]) < 1e-6)
    return {
        "sealbc": sealbc, "Nr": Nr, "Nth": Nth, "lmax": 2, "maxit": maxit, "budget_s": budget,
        "a2_seed": A2_SEED, "a2_mirror": a2_mirror, "continuation_amps": amps,
        "seed_L0": L0, "wall_s": round(time.time() - t0, 2),
        "throughput_limited": throughput_limited,
        "continuation_steps": steps,
        "final_amplitude_reached": last_amp, "reached_target": reached_target,
        "final_Phi": final_Phi, "converged": converged,
        "closed_cell_exists": closed_cell,
        "diagnostics": diag,
        "premise_ledger": {
            "xi": "FREE (probed family)", "kappa": "FREE-units",
            "Z_phi": "CHOSE=8 (Route-A carrying Route-B number)",
            "source": "FROZEN H3-hopfion ell=2 sh2(r) (ledgered)",
            "source_registration": "REGISTRATION B (native pullback): interpolated LIVE at current-L "
                                   "physical r=rc+(L/2)(zeta+1), clamped outside support; no amplitude "
                                   "Jacobian; frame-factor (rho^2/orthonormal-vs-coordinate) OPEN/un-applied",
            "shear_seal_BC": f"CHOSE-provisional ({sealbc}); BOTH run, dependence reported",
            "ell": "SCOPED: ell=2-only pilot (higher-ell = flagged blind-spot)",
            "a2_mirror": "CHOSE=0 (round mirror value for S-Dir)",
        },
        "scope_stamp": "static, Branch P, block-diagonal, ell=2 axisymmetric shear, FROZEN source, "
                       "whole cosmic cell -- a continuum here is B for THIS TILE only; a pin is an "
                       "A-CANDIDATE (needs higher-ell + co-relaxed source + shear-BC-fork survival).",
    }


def _write_json(path, obj):
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=2, default=float)


def _write_report(path, results):
    lines = ["N5d Stage-1 PILOT REPORT  (frozen hopfion source + live ell=2 shear + exact phi)",
             "=" * 78, ""]
    for r in results:
        d = r["diagnostics"]
        lines += [
            f"SEAL BC: {r['sealbc']}   (Nr={r['Nr']} Nth={r['Nth']} lmax={r['lmax']} "
            f"maxit={r['maxit']} budget={r['budget_s']}s)",
            f"  wall={r['wall_s']}s  throughput_limited={r['throughput_limited']}  "
            f"reached_target={r['reached_target']} (amp={r['final_amplitude_reached']})",
            f"  final_Phi={r['final_Phi']:.4e}  converged={r['converged']}  "
            f"CLOSED_CELL_EXISTS={r['closed_cell_exists']}",
            f"  q_raw={d['q_raw']:.4e}  Pi_phi={d['Pi_phi']:.4e}  "
            f"sign_convention={d['sign_convention']:+.0f}  M_readout={d['M_readout']:.4e}",
            f"  H_seal={d['H_seal']:+.4e}  H_drift={d['H_drift_maxmin']:.3e}  "
            f"Derrick_residual={d['derrick_residual']:+.3e}",
            f"  jac_cond={d['jac_cond']:.3e}  jac_shape={d['jac_shape']}",
            f"  phi_node_count={d['phi_node_count']}  "
            f"reduced_source_turning_points={d['reduced_source_turning_points']}  "
            f"(sign_changes={d['reduced_source_sign_changes']})",
            f"  shear_core_bc_res={d['shear_core_bc_residual']:+.3e}  "
            f"shear_seal_bc_res={d['shear_seal_bc_residual']:+.3e}  "
            f"a2_seal={d['a2_seal']:+.4e}  a2_peak|.|={d['a2_peak_abs']:.4e}",
            "  continuation:",
        ]
        for s in r["continuation_steps"]:
            lines.append(f"    amp={s['amp']:.2f}  Phi {s['Phi_start']:.3e}->{s['Phi_final']:.3e}  "
                         f"iters={s['iters']}  wall={s['wall_s']}s")
        lines.append("")
    # BC-fork banking note (sec.4)
    if len(results) == 2:
        cA, cB = results[0]["closed_cell_exists"], results[1]["closed_cell_exists"]
        lines += ["BC-FORK (sec.4 banking rule):",
                  f"  S-Dir closed_cell={cA}   S-JC2 closed_cell={cB}",
                  "  -> if the two DISAGREE the result is CONDITIONAL, not a pin (do NOT bank "
                  "Outcome A unless the branch survives the shear-BC fork or the fork is resolved "
                  "canonically first).", ""]
    lines += [results[0]["scope_stamp"] if results else "", ""]
    with open(path, "w") as fh:
        fh.write("\n".join(lines))


# =========================================================================================
# MAIN
# =========================================================================================
def main():
    import argparse
    ap = argparse.ArgumentParser(description="bounded Stage-1 N5d pilot driver")
    ap.add_argument("--Nr", type=int, default=16)
    ap.add_argument("--Nth", type=int, default=8)
    ap.add_argument("--lmax", type=int, default=2)
    ap.add_argument("--maxit", type=int, default=30)
    ap.add_argument("--budget", type=float, default=100.0)
    ap.add_argument("--Nr-fallback", type=int, default=12, dest="nr_fallback")
    ap.add_argument("--smoke", action="store_true",
                    help="assembly smoke: 1 continuation step, <=2 LM iters, one BC (S-Dir)")
    args = ap.parse_args()

    assert args.Nr <= 24, "anti-hang: Nr capped at 24"
    assert args.lmax == 2, "pilot is ell=2 only"

    st, source_rc, source_sh2 = load_frozen_source()
    blocker = st.get("blocker")
    if blocker is not None:
        out = {"BLOCKER": blocker, "source_status": st}
        _write_json(os.path.join(HERE, "n5d_pilot_report.txt"), out)
        _write_json(os.path.join(HERE, "n5d_pilot_smoke.json" if args.smoke
                                  else "n5d_pilot_BLOCKER.json"), out)
        return

    if args.smoke:
        # assembly smoke: ONE step, <=2 LM iters, one BC -- prove it assembles/steps/records
        r = run_one_bc("S-Dir", args.Nr, args.Nth, source_rc, source_sh2,
                       maxit=2, budget=args.budget, amps=[CONT_AMPS[0]], verbose=True)
        rec = {"MODE": "SMOKE", "source_status": st, "result": r}
        _write_json(os.path.join(HERE, "n5d_pilot_smoke.json"), rec)
        s0 = r["continuation_steps"][0] if r["continuation_steps"] else {}
        print(f"[smoke] assembled + stepped: amp={s0.get('amp')} "
              f"Phi {s0.get('Phi_start'):.4e}->{s0.get('Phi_final'):.4e} "
              f"iters={s0.get('iters')} decreased={s0.get('decreased')} "
              f"cond={r['diagnostics']['jac_cond']:.3e} "
              f"wall={r['wall_s']}s  -> wrote n5d_pilot_smoke.json")
        return

    # ---- FULL bounded pilot: BOTH seal BCs, separate records ----
    results = []
    for sealbc, jpath in (("S-Dir", "n5d_pilot_SDir.json"),
                          ("S-JC2", "n5d_pilot_SJC2.json")):
        r = run_one_bc(sealbc, args.Nr, args.Nth, source_rc, source_sh2,
                       maxit=args.maxit, budget=args.budget, verbose=False)
        r["source_status"] = st
        r["Nr_fallback_if_throughput_limited"] = args.nr_fallback
        _write_json(os.path.join(HERE, jpath), r)
        results.append(r)
    _write_report(os.path.join(HERE, "n5d_pilot_report.txt"), results)


if __name__ == "__main__":
    main()

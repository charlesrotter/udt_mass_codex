#!/usr/bin/env python3
"""M3 V-SNe runner (prereg SS3, commit 523f4aca). Modes A/B/C/D x P1/P2/P3
on real Pantheon+ data with the M2-gated machinery, frozen anchor
M_B = -19.253 +/- 0.027 (SH0ES ladder; F-ANCHOR premise travels).

--dry-run: loads real data, verifies schema / frozen cuts / covariance
subsetting per mode, then STOPS before any fit (M2_GUARD never flipped).
Real mode: flips the guard ONLY via v_sne.authorize_m3(M3_PREREG_COMMIT)
(prereg SS5.4) and runs all modes; SNe results are written and committed
BEFORE any BAO unblinding (prereg SS2).
"""
import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
M2_BUILD = os.path.join(os.path.dirname(HERE),
                        "udt_xmax_scale_observational_M2_build_2026-08-07")
sys.path.insert(0, M2_BUILD)
import v_sne  # noqa: E402

M3_PREREG_COMMIT = "523f4aca"
ANCHOR_M_B, ANCHOR_M_B_ERR = -19.253, 0.027    # frozen (prereg SS3)
D_ZCOLS = ("zCMB", "zHD", "zHEL")              # zCMB primary


def dry_run():
    """Schema/cuts/cov verification only; STOPS before fitting."""
    tab = v_sne.read_pantheon_table()
    n_total = len(np.asarray(tab["zCMB"]))
    out = {"n_rows_file": int(n_total), "frozen_z_cut": v_sne.FROZEN_Z_CUT,
           "anchor": {"M_B": ANCHOR_M_B, "err": ANCHOR_M_B_ERR}, "modes": {}}
    cov_full = v_sne.load_cov()
    out["cov_file_shape"] = list(cov_full.shape)
    for mode, zcol in [("A", "zCMB"), ("B", "zCMB"), ("C", "zCMB")] + \
                      [("D", zc) for zc in D_ZCOLS]:
        md = v_sne.load_mode_data(mode, zcol=zcol, table=tab,
                                  cov_full=cov_full)
        dv = v_sne.DataVector.from_real(md)     # constructed, never fitted
        rec = {"zcol": zcol, "n_after_cuts": int(md.n),
               "calibrators_excluded": True,
               "z_min": float(dv.z.min()), "z_max": float(dv.z.max()),
               "z_cut_ok": bool(dv.z.min() > v_sne.FROZEN_Z_CUT)}
        if md.cov is not None:
            d = np.diag(md.cov)
            rec["cov_subset_shape"] = list(md.cov.shape)
            rec["cov_ok"] = bool(md.cov.shape == (md.n, md.n)
                                 and np.allclose(md.cov, md.cov.T)
                                 and np.all(d > 0))
        else:
            rec["cov_subset_shape"] = None
            rec["cov_ok"] = "n/a (mode C diagonal-only by design)"
        out["modes"][f"{mode}:{zcol}"] = rec
    out["guard_state"] = {"M2_GUARD": v_sne.M2_GUARD,
                          "note": "dry-run never flips the guard"}
    fn = os.path.join(HERE, "sne_dry_run.json")
    with open(fn, "w") as f:
        json.dump(out, f, indent=1)
    for k, v in out["modes"].items():
        print(f"{k}: n={v['n_after_cuts']} zcut_ok={v['z_cut_ok']} "
              f"cov={v['cov_subset_shape']} cov_ok={v['cov_ok']}")
    print(f"DRY-RUN COMPLETE (no fit performed; M2_GUARD={v_sne.M2_GUARD}) "
          f"-> {fn}")
    return out


def real_run():
    """The preregistered real-data run (SS3). Guard flip via SS5.4 only."""
    v_sne.authorize_m3(M3_PREREG_COMMIT)
    t0 = time.time()
    tab = v_sne.read_pantheon_table()
    cov_full = v_sne.load_cov()
    results = {"prereg_commit": M3_PREREG_COMMIT,
               "anchor": {"M_B": ANCHOR_M_B, "err": ANCHOR_M_B_ERR},
               "fits": {}}
    for mode, zcol in [("A", "zCMB"), ("B", "zCMB"), ("C", "zCMB")] + \
                      [("D", zc) for zc in D_ZCOLS]:
        md = v_sne.load_mode_data(mode, zcol=zcol, table=tab,
                                  cov_full=cov_full)
        dv = v_sne.DataVector.from_real(md)
        cc = (v_sne.CovChi2(md.cov) if md.cov is not None else None)
        for profile in v_sne.PROFILES:
            key = f"{mode}:{zcol}:{profile}"
            print(f"[{time.time()-t0:7.0f}s] fitting {key}")
            if mode == "A":
                r = v_sne.fit_mode_A(dv, profile, cc=cc)
            elif mode == "B":
                r = v_sne.fit_mode_B(dv, profile, ANCHOR_M_B,
                                     M_B_err=ANCHOR_M_B_ERR, cc=cc)
            elif mode == "C":
                r = v_sne.fit_mode_C(dv, profile)
            else:
                r = v_sne.fit_mode_D(dv, profile, cc=cc)
            results["fits"][key] = r
    # headline deliverables (prereg SS3): C-vs-A shift; D z-column shifts
    shifts = {"C_minus_A_shape": {}, "D_shifts_shape": {}}
    for p in ("P1", "P3"):
        a = results["fits"][f"A:zCMB:{p}"]["shape"]
        c = results["fits"][f"C:zCMB:{p}"]["shape"]
        shifts["C_minus_A_shape"][p] = {
            "A": a, "C": c, "abs_shift": abs(c - a),
            "note": "quantified BBC-contamination estimate (prereg SS3); "
                    "also the point-of-use note on the banked 0.91"}
        for zc in ("zHD", "zHEL"):
            d = results["fits"][f"D:{zc}:{p}"]["shape"]
            shifts["D_shifts_shape"].setdefault(p, {})[zc] = {
                "zCMB": a, zc: d, "abs_shift": abs(d - a)}
    results["headline_shifts"] = shifts
    with open(os.path.join(HERE, "sne_results.json"), "w") as f:
        json.dump(results, f, indent=1, default=float)
    _write_md(results)
    print("real run complete -> sne_results.json, SNE_RESULTS.md")
    return results


def _write_md(results):
    lines = ["# M3 V-SNe RESULTS (prereg 523f4aca; all leads until blind "
             "results-verifier + Charles)", "",
             f"Anchor (mode B only): M_B = {ANCHOR_M_B} +/- {ANCHOR_M_B_ERR} "
             "(SH0ES ladder; F-ANCHOR premise travels with every absolute "
             "number).", ""]
    for key, r in results["fits"].items():
        lines.append(f"## {key}")
        lines.append(f"- chi2/dof = {r['chi2']:.2f}/{r['ndof']}")
        if r.get("shape") is not None:
            iv = r.get("shape_interval", {})
            one_sided = iv.get("hi_open") or iv.get("lo_open")
            lines.append(
                f"- {r['shape_name']} = {r['shape']:.4g} "
                f"[{iv.get('lo', float('nan')):.4g}, "
                f"{iv.get('hi', float('nan')):.4g}]"
                + (" (ONE-SIDED OPEN interval, honestly marked)"
                   if one_sided else ""))
        if "X_eff_Mpc" in r:
            x = r["X_eff_Mpc"]
            lines.append(f"- X_eff = {x['best']:.1f} Mpc "
                         f"[{x['lo']:.1f}, {x['hi']:.1f}] (anchor premise "
                         "attached; F-ANCHOR)")
        if "R_w_Mpc_at_best_n" in r:
            lines.append(f"- R_w at best n: "
                         f"{r['R_w_Mpc_at_best_n']['value']:.1f} Mpc "
                         "(pair-quote per D1; never marginal-only)")
        if "alpha" in r:
            lines.append(f"- Tripp alpha={r['alpha']:.3f} "
                         f"beta={r['beta']:.3f}")
        lines.append("")
    lines.append("## Headline sensitivity deliverables (prereg SS3)")
    lines.append("```json")
    lines.append(json.dumps(results["headline_shifts"], indent=1,
                            default=float))
    lines.append("```")
    with open(os.path.join(HERE, "SNE_RESULTS.md"), "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="schema/cuts/cov verification only; no fit")
    args = ap.parse_args()
    if args.dry_run:
        dry_run()
    else:
        real_run()

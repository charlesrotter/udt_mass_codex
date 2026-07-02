"""Stage C runner: one combo per invocation. Sweep -> brackets -> Illinois refine -> characterize.
Usage: python3 stageC_run.py <combo_key> [d_lo_frac]
Output: stageC_<combo>.json in scratchpad.
"""
import sys, json, time
import numpy as np
import stageC_lib as L

SCR = "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad"
combo = sys.argv[1]
d_lo_frac = float(sys.argv[2]) if len(sys.argv) > 2 else 0.25
c = L.COMBOS[combo]
t0 = time.time()

d_hi = 1.15 * c["d0_est"]
d_lo = d_lo_frac * c["d0_est"]
rows = L.sweep(combo, d_hi, d_lo, ratio=0.98)
br = L.find_brackets(rows)
print(f"[{combo}] sweep {len(rows)} pts d in [{d_lo:.4e}, {d_hi:.4e}], "
      f"{len(br)} brackets, shots={L.SHOTS}")

# extend downward until >= 9 brackets (bounded: 3 extensions max)
ext = 0
while len(br) < 9 and ext < 3:
    ext += 1
    new_hi = min(r[0] for r in rows)
    new_lo = new_hi * 0.5
    rows += L.sweep(combo, new_hi * 0.999, new_lo, ratio=0.98)
    br = L.find_brackets(rows)
    print(f"[{combo}] extension {ext}: down to {new_lo:.4e}, {len(br)} brackets, shots={L.SHOTS}")

nonseal = [(d, s) for d, f, s in rows if s != "seal"]
rungs = []
for bi, (dh, dl, fh, fl) in enumerate(br):
    if bi >= 12:      # bound: at most 12 rungs refined per combo (need N=0..8)
        break
    d_star, steps = L.refine_root(combo, dh, dl, fh, fl)
    if d_star is None:
        rungs.append({"bracket_index": bi, "d_bracket": [dh, dl], "failed": True,
                      "steps": steps})
        continue
    f, o, U = L.f_of_d(combo, d_star)
    steps += 1
    if o["status"] != "seal":
        rungs.append({"bracket_index": bi, "d_bracket": [dh, dl], "d_star": d_star,
                      "failed": True, "status": o["status"], "steps": steps})
        continue
    ch = L.characterize(o, U, c["Z"])
    ch2 = L.characterize(o, U, c["Z"], npts=200001)   # 2x recheck, no extra shot
    ch["N_delta_recheck200k"] = ch2["N_delta"]
    ch["N_rhop_recheck200k"] = ch2["N_rhop"]
    p_star = c["stuck"] * (1.0 - d_star)
    rung = {"bracket_index": bi, "d_bracket": [dh, dl], "d_star": d_star,
            "p_star": p_star, "refine_steps": steps, **ch}
    rungs.append(rung)
    print(f"[{bi:2d}] p*={p_star:.10f} d={d_star:.6e} steps={steps} "
          f"Nd={ch['N_delta']} Np={ch['N_rhop']} "
          f"(200k: {ch['N_delta_recheck200k']},{ch['N_rhop_recheck200k']}) "
          f"q={ch['q']:.6f} rho_s={ch['rho_s']:.6f} L={ch['L_proper']:.4f} "
          f"chi={ch['chi']:.4f} Hd={ch['H_drift']:.1e}")

json.dump({"combo": combo, "Z": c["Z"], "stuck": c["stuck"], "d0_est": c["d0_est"],
           "rows": rows, "brackets": [list(b) for b in br],
           "nonseal_rows": nonseal,
           "rungs": [{k: v for k, v in r.items() if "profile" not in k} for r in rungs],
           "profiles": [{"bracket_index": r["bracket_index"],
                         "N_delta_profile": r.get("N_delta_profile"),
                         "N_rhop_profile": r.get("N_rhop_profile")} for r in rungs],
           "shots": L.SHOTS, "wall_s": time.time() - t0},
          open(f"{SCR}/stageC_{combo}.json", "w"), indent=1)
print(f"[{combo}] TOTAL shots={L.SHOTS} wall={time.time()-t0:.1f}s nonseal={len(nonseal)}")

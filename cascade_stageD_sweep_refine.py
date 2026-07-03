"""Stage D SURVEY sweep — pass 2 refine. For every pass-1 bracket:
  (a) MULTIPLICITY GUARD: 8x subdivision of the bracket; count interior sign changes
      (hazard 1: dense clusters — a bracket may hold >1 root; any count>1 -> split & recurse);
  (b) METHOD 1: LSODA bisection (origin-solver shooter, cell_solver_universe_T3.miss)
      to bracket width <= 1e-12 in d;
  (c) characterize at d* with the Stage-B graduated-floor counters (100k + 200k dense grids,
      >=2-decade plateau mandatory) — N_delta AND N_rho';
  (d) METHOD 2: independent bv6 chunked-DOP853 shooter + Illinois root finder in a-space
      (cascade_bv6_lib; own event location, own integrator, own graduated-floor counter,
      failed-chunk partial-dense seal scan built in), xtol=1e-11 in a;
  (e) two-method agreement recorded per root (|d1-d2|); a root enters the table only if
      both methods seal and agree.
SINGLE process, bounded. Output: stageD_refine_pass2.json (repo dir).
"""
import sys, json, time
import numpy as np
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import make_risefall_slice, miss, LN1101
from cascade_stageB_common import characterize
import cascade_bv6_lib as bv6

Z, M = 8.0, 3.0
SHOTS = 0

def f_of_d(d):
    global SHOTS
    a = 1.5 * (1.0 - d)
    U, Up, _ = make_risefall_slice(a, m=M)
    SHOTS += 1
    f, o = miss(Z, U, Up, 1.0)
    return (float(f) if np.isfinite(f) else float("nan")), o, U

br = json.load(open("/home/udt-admin/udt_mass_codex/stageD_scan_pass1.json"))["brackets"]
print(f"{len(br)} brackets loaded")

t0 = time.time()
rungs, unresolved, failed_pts = [], [], []

# ---------------- (a) multiplicity guard: recursive split until each bracket holds ONE crossing
work = [(float(hi), float(lo)) for hi, lo in br]   # d descending within each pair
single = []
depth = 0
while work and depth < 6:
    nxt = []
    for d_hi, d_lo in work:
        dd = np.linspace(d_hi, d_lo, 9)
        fs, bad = [], False
        for d in dd:
            f, o, _ = f_of_d(float(d))
            if not np.isfinite(f) or o["status"] != "seal":
                failed_pts.append({"d": float(d), "status": o["status"]})
                bad = True
                break
            fs.append(f)
        if bad:
            unresolved.append({"span": [d_hi, d_lo], "reason": "non-seal point inside bracket"})
            continue
        fs = np.array(fs)
        cross = [(float(dd[i]), float(dd[i+1])) for i in range(8) if fs[i] * fs[i+1] < 0]
        if len(cross) == 1:
            single.append(cross[0])
        elif len(cross) == 0:
            unresolved.append({"span": [d_hi, d_lo],
                               "reason": "sign change lost on subdivision (grazing pair?)",
                               "min_abs_f": float(np.min(np.abs(fs)))})
        else:
            print(f"  CLUSTER: bracket ({d_hi:.6e},{d_lo:.6e}) holds {len(cross)} crossings — splitting")
            nxt.extend(cross)
    work = nxt
    depth += 1
if work:
    for d_hi, d_lo in work:
        unresolved.append({"span": [d_hi, d_lo], "reason": "recursion cap hit"})
print(f"multiplicity guard: {len(single)} single-crossing brackets, "
      f"{len(unresolved)} unresolved, shots={SHOTS}, wall={time.time()-t0:.1f}s")

# ---------------- (b)-(e) per bracket
for bi, (d_hi, d_lo) in enumerate(sorted(single, key=lambda b: -b[0])):
    fhi, _, _ = f_of_d(d_hi)
    flo, _, _ = f_of_d(d_lo)
    if not (np.isfinite(fhi) and np.isfinite(flo)) or fhi * flo > 0:
        unresolved.append({"span": [d_hi, d_lo], "reason": "endpoint re-eval lost bracket"})
        continue
    lo, hi, Fhi = d_lo, d_hi, fhi
    steps = 0
    ok = True
    while (hi - lo) > 1.0e-12 and steps < 45:
        mid = 0.5 * (lo + hi)
        fm, om, Um = f_of_d(mid)
        steps += 1
        if not np.isfinite(fm):
            failed_pts.append({"d": mid, "status": om["status"], "where": f"bisect bracket {bi}"})
            ok = False
            break
        if Fhi * fm < 0:
            lo = mid
        else:
            hi, Fhi = mid, fm
    if not ok:
        unresolved.append({"span": [d_hi, d_lo], "reason": "non-finite miss during bisection"})
        continue
    d_star = 0.5 * (lo + hi)
    width = hi - lo
    fm, om, Um = f_of_d(d_star)
    steps += 1
    if om["status"] != "seal":
        unresolved.append({"span": [d_hi, d_lo], "reason": f"final shot status={om['status']}"})
        continue
    ch = characterize(om, Um, npts=100001)
    ch2 = characterize(om, Um, npts=200001)

    # -------- method 2: bv6 DOP853 chunked + Illinois, in a-space
    a_lo, a_hi = 1.5 * (1.0 - d_hi), 1.5 * (1.0 - d_lo)     # a ascending
    ga, oa = bv6.g_of_a(a_lo, Z=Z, m=M)
    gb, ob = bv6.g_of_a(a_hi, Z=Z, m=M)
    m2 = {"ok": False}
    if np.isfinite(ga) and np.isfinite(gb) and ga * gb < 0:
        a2, g2, w2, out2, nev = bv6.illinois(a_lo, a_hi, ga, gb, xtol=1e-11, maxit=30,
                                             shoot_kw={"Z": Z, "m": M})
        d2 = 1.0 - a2 / 1.5
        diag2 = bv6.diagnose(out2)
        m2 = {"ok": True, "d2": d2, "g2": g2, "illinois_width_a": w2, "nev": nev,
              "N_delta_bv6_1x": diag2["counts"]["1x"]["N_delta"],
              "N_rhop_bv6_1x": diag2["counts"]["1x"]["N_rhop"],
              "N_delta_bv6_2x": diag2["counts"]["2x"]["N_delta"],
              "N_rhop_bv6_2x": diag2["counts"]["2x"]["N_rhop"],
              "rho_s_bv6": diag2["rho_s"], "q_bv6": diag2["q"],
              "d_agree_abs": abs(d2 - d_star)}
    else:
        m2 = {"ok": False, "ga": float(ga), "gb": float(gb),
              "status_a": oa["status"], "status_b": ob["status"]}

    rho_s = ch["rho_s"]
    rung = {"idx": bi, "d_bracket_in": [d_hi, d_lo], "d_star": d_star,
            "bisect_width_d": width, "bisect_steps": steps,
            "a_slice": 1.5 * (1.0 - d_star),
            "residual_miss": float(fm),
            "N_delta": ch["N_delta"], "N_delta_floor_range": ch["N_delta_floor_range"],
            "N_rhop": ch["N_rhop"], "N_rhop_floor_range": ch["N_rhop_floor_range"],
            "N_delta_200k": ch2["N_delta"], "N_rhop_200k": ch2["N_rhop"],
            "N_delta_profile": ch["N_delta_profile"], "N_rhop_profile": ch["N_rhop_profile"],
            "rho_s": rho_s, "a_seal": abs(rho_s - 1.0),
            "rho_s_side": "<1" if rho_s < 1.0 else ">1",
            "q": ch["q"], "r_s": ch["r_s"], "L_proper": ch["L_proper"], "chi": ch["chi"],
            "dphi_dev": ch["dphi_carried"] - LN1101,
            "ms_seal_dev": ch["ms_seal_2m_over_rho"] - 1.0,
            "H_drift": ch["H_drift"],
            "method2": m2}
    rungs.append(rung)
    print(f"[{bi:2d}] d*={d_star:.10e} w={width:.1e} Nd={ch['N_delta']}({ch2['N_delta']}) "
          f"Np={ch['N_rhop']}({ch2['N_rhop']}) rho_s={rho_s:.6f} q={ch['q']:.5f} "
          f"m2ok={m2.get('ok')} dAgree={m2.get('d_agree_abs', float('nan')):.2e} "
          f"NdBV={m2.get('N_delta_bv6_1x')} NpBV={m2.get('N_rhop_bv6_1x')} "
          f"shots={SHOTS}+bv6:{bv6.SHOTS['n']} wall={time.time()-t0:.0f}s", flush=True)

out = {"rungs": [{k: v for k, v in r.items() if "profile" not in k} for r in rungs],
       "profiles": [{"idx": r["idx"], "N_delta_profile": r["N_delta_profile"],
                     "N_rhop_profile": r["N_rhop_profile"]} for r in rungs],
       "unresolved": unresolved, "failed_points": failed_pts,
       "shots_lsoda": SHOTS, "shots_bv6": bv6.SHOTS["n"], "wall_s": time.time() - t0}
json.dump(out, open("/home/udt-admin/udt_mass_codex/stageD_refine_pass2.json", "w"), indent=1)
print(f"\n{len(rungs)} rungs, {len(unresolved)} unresolved, {len(failed_pts)} failed points; "
      f"shots LSODA={SHOTS} bv6={bv6.SHOTS['n']}; wall={time.time()-t0:.1f}s "
      f"-> stageD_refine_pass2.json")

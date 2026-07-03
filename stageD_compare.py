#!/usr/bin/env python3
"""Stage-D comparison: frozen forecast vs blind sweep, per cascade_stageD_prereg.md.

Contract terms implemented verbatim:
- Locations: each found rung within +/-1.0% in d of its predicted d*(N);
  assignment nearest-in-d, injective.
- Count: every N in the hashed forecast's window-proper list present in the
  window proper, none missing, none duplicated (sweep already floor-audited).
- Edge rule: guard-band rungs (outside window proper, inside extended) are
  edge-cases, reported separately, not pass/fail.
- Secondary (characterizing, not pass/fail): a_seal, q, parity side.
- Look-elsewhere: per-prediction band fraction = 2*tol*d_pred / local
  nearest-neighbor spacing of the FOUND set; joint null = product over the
  window-proper predictions.
"""
import json

TOL = 0.010  # +/-1.0%, pinned by Charles in the prereg
WINDOW = (1.45e-3, 2.11e-3)

fc = json.load(open("stageD_frozen_forecast.json"))
sw = json.load(open("stageD_sweep_results_raw.json"))

preds = fc["forecast"]
found = sorted(sw["rungs"], key=lambda r: r["d_star"], reverse=True)

# injective nearest-in-d assignment (greedy by smallest relative distance)
pairs = []
cands = []
for p in preds:
    for r in found:
        rel = (r["d_star"] - p["d_star"]) / p["d_star"]
        cands.append((abs(rel), rel, p, r))
cands.sort(key=lambda t: t[0])
used_p, used_r = set(), set()
for absrel, rel, p, r in cands:
    if p["N"] in used_p or r["idx"] in used_r:
        continue
    used_p.add(p["N"]); used_r.add(r["idx"])
    pairs.append((p, r, rel))
pairs.sort(key=lambda t: t[0]["N"])

rows, misses = [], []
for p, r, rel in pairs:
    hit = abs(rel) <= TOL
    n_match = (r["N_delta"] == p["N"]) and (r["N_rhop"] == p["N"])
    parity_match = r["rho_s_side"] == p["parity_side"].replace("rho_s", "").strip("<>") or None
    # parity: forecast stores 'rho_s>1'/'rho_s<1'; sweep stores side string
    parity_match = (p["parity_side"].endswith(">1") and r["rho_s"] > 1) or \
                   (p["parity_side"].endswith("<1") and r["rho_s"] < 1)
    da = (r["a_seal"] - p["a_seal"]) / p["a_seal"]
    dq = (r["q"] - p["q"]) / p["q"]
    in_win = WINDOW[0] < p["d_star"] < WINDOW[1]
    rows.append(dict(N=p["N"], d_pred=p["d_star"], d_found=r["d_star"],
                     dev_pct=100*rel, hit=hit, N_delta=r["N_delta"], N_rhop=r["N_rhop"],
                     N_label_match=n_match, parity_match=parity_match,
                     a_seal_dev_pct=100*da, q_dev_pct=100*dq, in_window_proper=in_win))
    if not hit or not n_match or not parity_match:
        misses.append(rows[-1])

unmatched_preds = [p["N"] for p in preds if p["N"] not in used_p]
unmatched_found = [r["idx"] for r in found if r["idx"] not in used_r]

# count rule on window proper
win_pred_N = sorted(p["N"] for p in preds if p["in_window_proper"])
win_found = [r for r in found if WINDOW[0] < r["d_star"] < WINDOW[1]]
win_found_N = sorted(r["N_delta"] for r in win_found)
count_pass = (win_found_N == win_pred_N)

# look-elsewhere: local NN spacing from the FOUND set
ds = sorted(r["d_star"] for r in found)
def local_spacing(d):
    gaps = []
    for i, x in enumerate(ds):
        if i > 0: gaps.append((abs(d - (x + ds[i-1]) / 2), x - ds[i-1]))
    gaps.sort()
    return gaps[0][1]
import math
logp = 0.0
le_rows = []
for p in preds:
    if not p["in_window_proper"]:
        continue
    band = 2 * TOL * p["d_star"]
    sp = local_spacing(p["d_star"])
    frac = min(1.0, band / sp)
    le_rows.append((p["N"], band, sp, frac))
    logp += math.log(frac)
joint = math.exp(logp)

loc_hits = sum(1 for x in rows if x["hit"])
win_rows = [x for x in rows if x["in_window_proper"]]
win_hits = sum(1 for x in win_rows if x["hit"])

out = dict(tolerance_pct=100*TOL, window=WINDOW,
           pairs=rows, misses=misses,
           unmatched_predictions=unmatched_preds, unmatched_found=unmatched_found,
           window_pred_N=win_pred_N, window_found_N=win_found_N,
           count_rule_pass=count_pass,
           location_hits_all=f"{loc_hits}/{len(rows)}",
           location_hits_window=f"{win_hits}/{len(win_rows)}",
           worst_dev_pct=max(abs(x["dev_pct"]) for x in rows),
           look_elsewhere_joint_null=joint,
           look_elsewhere_rows=le_rows)
json.dump(out, open("stageD_comparison.json", "w"), indent=1)

print(f"tolerance ±{100*TOL}%  window {WINDOW}")
print(f"{'N':>3} {'d_pred':>12} {'d_found':>14} {'dev%':>8} {'hit':>4} "
      f"{'Nδ':>3} {'Nρ,':>3} {'par':>4} {'aseal%':>7} {'q%':>7} {'win':>4}")
for x in rows:
    print(f"{x['N']:>3} {x['d_pred']:.6e} {x['d_found']:.8e} {x['dev_pct']:>8.3f} "
          f"{str(x['hit']):>4} {x['N_delta']:>3} {x['N_rhop']:>3} "
          f"{str(x['parity_match']):>4} {x['a_seal_dev_pct']:>7.2f} {x['q_dev_pct']:>7.2f} "
          f"{str(x['in_window_proper']):>4}")
print(f"\nunmatched predictions: {unmatched_preds}   unmatched found: {unmatched_found}")
print(f"window-proper predicted N: {win_pred_N}")
print(f"window-proper found N:     {win_found_N}")
print(f"COUNT RULE (exact list match): {count_pass}")
print(f"LOCATION hits: window {win_hits}/{len(win_rows)}, all {loc_hits}/{len(rows)}; "
      f"worst |dev| = {out['worst_dev_pct']:.3f}%")
print(f"look-elsewhere joint uniform-null probability (window proper): {joint:.3e}")

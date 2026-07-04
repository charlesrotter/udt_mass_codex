#!/usr/bin/env python3
"""BLIND VERIFIER independent comparison (stageD_bv_compare.py).
Re-derives the Stage-D comparison from the two committed JSONs ONLY.
Does NOT reuse stageD_compare.py logic: assignment is done by globally
OPTIMAL injective matching (scipy Hungarian on |rel dev|), then cross-checked
against naive sorted-order pairing. All contract arithmetic re-done here.
"""
import json, math, itertools
import numpy as np

TOL = 0.010
WIN_LO, WIN_HI = 1.45e-3, 2.11e-3
GUARD_LO, GUARD_HI = 1.30e-3, 2.30e-3

fc = json.load(open("/home/udt-admin/udt_mass_codex/stageD_frozen_forecast.json"))
sw = json.load(open("/home/udt-admin/udt_mass_codex/stageD_sweep_results_raw.json"))

preds = fc["forecast"]                      # 21 preds N=20..40
found = sorted(sw["rungs"], key=lambda r: r["d_star"])   # ascending d

# ---- optimal injective assignment (minimize total |rel dev|, rel to PREDICTED d)
from scipy.optimize import linear_sum_assignment
P = len(preds); F = len(found)
C = np.full((P, F), 1e9)
for i, p in enumerate(preds):
    for j, r in enumerate(found):
        C[i, j] = abs((r["d_star"] - p["d_star"]) / p["d_star"])
# pad: rectangular OK for linear_sum_assignment
ri, cj = linear_sum_assignment(C)
pairs = [(preds[i], found[j], (found[j]["d_star"] - preds[i]["d_star"]) / preds[i]["d_star"])
         for i, j in zip(ri, cj)]
pairs.sort(key=lambda t: t[0]["N"])
unmatched_preds = [p["N"] for p in preds if p["N"] not in {t[0]["N"] for t in pairs}]

# ---- cross-check: sorted-order pairing (both descending in d) for the 20 lowest-N preds
preds_sorted = sorted(preds, key=lambda p: -p["d_star"])
found_sorted = sorted(found, key=lambda r: -r["d_star"])
order_pairs = list(zip(preds_sorted[:F], found_sorted))
same = all(a["N"] == b[0]["N"] and c["d_star"] == b[1]["d_star"]
           for (a, c), b in zip(order_pairs, sorted(pairs, key=lambda t: -t[0]["d_star"])))
print("optimal assignment == sorted-order pairing:", same)
print("unmatched predictions:", unmatched_preds)

# ---- per-pair contract arithmetic
print(f"\n{'N':>3} {'d_pred':>13} {'d_found':>15} {'dev%':>8} {'hit':>5} "
      f"{'Ndl':>3} {'Nrp':>3} {'Nlbl':>5} {'par':>5} {'winP':>5} {'winF':>5}")
worst = 0.0; worstN = None
loc_fail = []
win_pred_N = []
win_found_ids = []
for p, r, rel in pairs:
    hit = abs(rel) <= TOL
    if abs(rel) > worst: worst, worstN = abs(rel), p["N"]
    nlbl = (r["N_delta"] == p["N"]) and (r["N_rhop"] == p["N"]) \
           and (r["N_delta_200k"] == p["N"]) and (r["N_rhop_200k"] == p["N"]) \
           and (r["method2"]["N_delta_bv6_1x"] == p["N"]) and (r["method2"]["N_rhop_bv6_1x"] == p["N"]) \
           and (r["method2"]["N_delta_bv6_2x"] == p["N"]) and (r["method2"]["N_rhop_bv6_2x"] == p["N"])
    par = (p["parity_side"].endswith(">1") and r["rho_s"] > 1) or \
          (p["parity_side"].endswith("<1") and r["rho_s"] < 1)
    winP = WIN_LO < p["d_star"] < WIN_HI
    winF = WIN_LO < r["d_star"] < WIN_HI
    if winP: win_pred_N.append(p["N"])
    if winF: win_found_ids.append((p["N"], r["N_delta"]))
    if not hit: loc_fail.append(p["N"])
    print(f"{p['N']:>3} {p['d_star']:.7e} {r['d_star']:.9e} {100*rel:>8.4f} {str(hit):>5} "
          f"{r['N_delta']:>3} {r['N_rhop']:>3} {str(nlbl):>5} {str(par):>5} {str(winP):>5} {str(winF):>5}")
    # verify JSON's own in_window_proper flag against arithmetic
    assert p["in_window_proper"] == winP, f"forecast JSON window flag wrong at N={p['N']}"

print(f"\nworst |dev| = {100*worst:.4f}% at N={worstN}; location failures: {loc_fail or 'none'}")

# ---- count rule (window proper): forecast's window list vs found-in-window N labels
win_found_N = sorted(n for _, n in win_found_ids)
win_pred_N = sorted(win_pred_N)
print("window-proper predicted N:", win_pred_N)
print("window-proper FOUND N (by counter label, d_found in window):", win_found_N)
print("consecutive integers, no dup, no gap:",
      win_found_N == list(range(min(win_found_N), max(win_found_N) + 1)))
print("COUNT RULE exact-list match:", win_found_N == win_pred_N)

# edge scrutiny
p35 = [p for p in preds if p["N"] == 35][0]
r35 = [r for r in found if r["N_delta"] == 35][0]
p23 = [p for p in preds if p["N"] == 23][0]
r23 = [r for r in found if r["N_delta"] == 23][0]
print(f"\nEDGES: N=35 pred {p35['d_star']:.6e} (> lo edge by {100*(p35['d_star']/WIN_LO-1):.4f}%), "
      f"found {r35['d_star']:.6e} (> lo edge by {100*(r35['d_star']/WIN_LO-1):.4f}%) -> in-window: {r35['d_star']>WIN_LO}")
print(f"       N=23 pred {p23['d_star']:.6e} (< hi edge by {100*(1-p23['d_star']/WIN_HI):.4f}%), "
      f"found {r23['d_star']:.6e} (< hi edge by {100*(1-r23['d_star']/WIN_HI):.4f}%) -> in-window: {r23['d_star']<WIN_HI}")

# guard-band / edge-rule ledger: found rungs outside window proper but inside guard
guard_found = [r["N_delta"] for r in found if not (WIN_LO < r["d_star"] < WIN_HI)
               and GUARD_LO < r["d_star"] < GUARD_HI]
print("guard-band (edge-case) found rungs:", guard_found)

# ---- look-elsewhere, per contract: per-prediction band 2*tol*d_pred over local NN
# spacing of the FOUND set; product over window-proper predictions
ds = sorted(r["d_star"] for r in found)
gaps = [(0.5 * (a + b), b - a) for a, b in zip(ds, ds[1:])]
def local_sp(d):
    return min(gaps, key=lambda g: abs(d - g[0]))[1]
joint = 1.0
for p in preds:
    if not p["in_window_proper"]:
        continue
    frac = min(1.0, 2 * TOL * p["d_star"] / local_sp(p["d_star"]))
    joint *= frac
print(f"\nlook-elsewhere joint null (window proper, contract method): {joint:.4e}")

# alternative harsher null: fraction of full window covered by each band
joint2 = 1.0
for p in preds:
    if not p["in_window_proper"]:
        continue
    joint2 *= min(1.0, 2 * TOL * p["d_star"] / (WIN_HI - WIN_LO))
print(f"(reference only) naive uniform-over-window null: {joint2:.3e}")

# ---- compare against the committed comparison JSON
cmp_ = json.load(open("/home/udt-admin/udt_mass_codex/stageD_comparison.json"))
print("\ncommitted comparison claims: worst", cmp_["worst_dev_pct"], "count", cmp_["count_rule_pass"],
      "hits", cmp_["location_hits_all"], cmp_["location_hits_window"],
      "LE", cmp_["look_elsewhere_joint_null"], "unmatched", cmp_["unmatched_predictions"], cmp_["unmatched_found"])

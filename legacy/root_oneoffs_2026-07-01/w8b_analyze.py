"""W8 PHASE-B — script 4: CATALOG VERDICT + p_F RATIOS + DATA-BLIND COMPARE.

Reads /tmp/w8b_scan_rows.csv (the persistence scan) and /tmp/w8b_bg.npz
(p_F per member). Produces:
  (i)  DISCRETE vs CONTINUUM verdict: is the stable self-consistent set
       isolated points / thin slices, or an open 2D patch?
  (ii) the catalog members + MS masses (p_F) + RATIOS (static, breather,
       both D_cell forks);
  (iii) kappa-dependence of the catalog/ratios;
  (v)  DATA-BLIND comparison to the wall numbers (done ONLY here, AFTER the
       catalog is fixed; NO tuning).

A scan point (member, gshape, beta, kappa) is a CATALOG MEMBER iff its
breather label is in {RING, BREATHER} AND the run is valid (energy gate).
COLLAPSE/GROW/DISPERSE/UNRESOLVED-STIFF/QUIET are NOT members.

Wall numbers (revealed only in the compare step):
  C_M1=0.977679087638, C_E1=1.93121474779, ratio=1.97530536575
  warped: C_M1=0.936832609588, C_E1=1.81920864981, ratio=1.94187161205

New file. 2026-06-13, W8 PHASE-B.
"""
import sys, csv
import numpy as np

ROWS = "/tmp/w8b_scan_rows.csv"
STABLE = {"RING", "BREATHER"}

def load():
    rows = []
    with open(ROWS) as fh:
        for r in csv.DictReader(fh):
            rows.append(r)
    return rows

def main():
    rows = load()
    breather = [r for r in rows if r["mech"] == "breather"]
    statics = [r for r in rows if r["mech"] == "static"]
    print(f"total breather rows: {len(breather)}  static rows: {len(statics)}")

    # ---- (i) DISCRETE vs CONTINUUM -------------------------------------
    # The stable set lives in (gamma, mult, gshape, beta, kappa). For the
    # DISCRETE/CONTINUUM verdict we ask: at fixed (gshape,beta,sign-of-kappa)
    # do stable cells fill an open (gamma, mult) patch (=> continuum in the
    # cell parameters), and is the stable kappa set an open interval or
    # isolated points?
    stable_rows = [r for r in breather
                   if r["label"] in STABLE and r["valid"] == "1"]
    print(f"\nstable (RING/BREATHER, valid) breather points: "
          f"{len(stable_rows)} / {len(breather)}")

    # kappa-axis structure per member: is stable-kappa an open band?
    from collections import defaultdict
    by_cell = defaultdict(list)   # (member,gshape,beta) -> [(kappa,label)]
    for r in breather:
        key = (r["member"], r["gshape"], r["beta"])
        by_cell[key].append((float(r["kappa"]), r["label"], r["valid"]))
    # classify each cell's kappa structure
    n_neg_stable = n_pos_stable_band = n_isolated = n_none = 0
    for key, lst in by_cell.items():
        lst.sort()
        neg = [l for k, l, v in lst if k < 0]
        pos = [(k, l) for k, l, v in lst if k > 0]
        neg_stable = all(l in STABLE for l in neg) and len(neg) > 0
        pos_stable = [l in STABLE for k, l in pos]
        # open band in positive kappa = >=2 adjacent stable
        adj = any(pos_stable[i] and pos_stable[i+1]
                  for i in range(len(pos_stable)-1))
        nstab = sum(pos_stable)
        if neg_stable:
            n_neg_stable += 1
        if adj:
            n_pos_stable_band += 1
        elif nstab >= 1:
            n_isolated += 1
        if nstab == 0 and not neg_stable:
            n_none += 1
    ncells = len(by_cell)
    print(f"\nKAPPA STRUCTURE across {ncells} cells (member x gshape x beta):")
    print(f"  cells with negative-kappa STABLE (open neg branch): {n_neg_stable}")
    print(f"  cells with positive-kappa OPEN STABLE BAND (>=2 adj): {n_pos_stable_band}")
    print(f"  cells with only ISOLATED positive-kappa stable pts:  {n_isolated}")
    print(f"  cells with NO stable kappa:                          {n_none}")

    # gamma-continuity: among stable cells, does p_F vary continuously in gamma?
    print("\nGAMMA-CONTINUITY of the stable set (p_F vs gamma at a fixed stable kappa):")
    # pick negative kappa = -1.0 (broadly stable) and list stable p_F by gamma
    fixed = defaultdict(list)
    for r in breather:
        if abs(float(r["kappa"]) - (-1.0)) < 1e-6 and r["label"] in STABLE:
            fixed[(r["gshape"], r["beta"])].append(
                (float(r["gamma"]), float(r["mult"]), float(r["pF_seal"]),
                 float(r["pF_weld"])))
    for key, lst in sorted(fixed.items()):
        lst.sort()
        gammas = sorted(set(g for g, m, ps, pw in lst))
        print(f"  gshape={key[0]} beta={key[1]} kappa=-1: stable at gammas "
              f"{gammas}  (n={len(lst)} cells)")

    # ---- (ii) THE CATALOG + p_F + RATIOS -------------------------------
    # The MS mass of a stable cell = p_F. p_F_weld = gamma/2 EXACT;
    # p_F_seal = the deep-endpoint MS charge (weakly c-dependent).
    print("\n" + "="*70)
    print("(ii) CATALOG p_F TABLE (stable cells; MS mass = p_F)")
    print("="*70)
    # collapse over kappa: a (gamma,mult) cell is 'in the catalog' if it is
    # stable for SOME kappa. Its p_F is geometry-fixed (kappa-independent:
    # p_F is read from the formation flow, not from kappa).
    catalog = {}
    for r in breather:
        if r["label"] in STABLE and r["valid"] == "1":
            k = (float(r["gamma"]), float(r["mult"]))
            catalog[k] = (float(r["pF_seal"]), float(r["pF_weld"]))
    print(f"{'gamma':>6} {'mult':>5} {'pF_seal':>9} {'pF_weld(=g/2)':>13}")
    for (g, m), (ps, pw) in sorted(catalog.items()):
        print(f"{g:6.2f} {m:5.2f} {ps:9.5f} {pw:13.4f}")

    # RATIOS: the data-blind falsification quantity. Ratios of p_F across the
    # catalog. Since p_F ~ gamma/2, ratios ~ gamma ratios. Report the set of
    # distinct p_F (by gamma) and their ratios.
    pf_by_gamma_weld = sorted(set(pw for (g, m), (ps, pw) in catalog.items()))
    pf_by_gamma_seal = {}
    for (g, m), (ps, pw) in catalog.items():
        pf_by_gamma_seal.setdefault(g, []).append(ps)
    print("\nDISTINCT p_F (weld, =gamma/2) in catalog:", pf_by_gamma_weld)
    if len(pf_by_gamma_weld) >= 2:
        base = pf_by_gamma_weld[0]
        print("RATIOS to smallest (weld):",
              [round(p/base, 5) for p in pf_by_gamma_weld])
    print("\np_F (seal) spread per gamma (shows c/mult dependence):")
    for g in sorted(pf_by_gamma_seal):
        v = pf_by_gamma_seal[g]
        print(f"  gamma={g}: p_F_seal in [{min(v):.5f},{max(v):.5f}] "
              f"(spread {100*(max(v)-min(v))/np.mean(v):.2f}%)")

    # ---- (v) DATA-BLIND COMPARE (after catalog fixed) ------------------
    print("\n" + "="*70)
    print("(v) DATA-BLIND COMPARISON to the wall numbers (NO tuning)")
    print("="*70)
    C_M1, C_E1 = 0.977679087638, 1.93121474779
    ratio_wall = C_E1 / C_M1  # 1.97530536575
    wC_M1, wC_E1 = 0.936832609588, 1.81920864981
    ratio_warp = wC_E1 / wC_M1
    print(f"wall: C_M1={C_M1} C_E1={C_E1} ratio={ratio_wall:.8f}")
    print(f"warped: ratio={ratio_warp:.8f}")
    print(f"\ncatalog distinct-p_F ratios (weld): {[round(p/pf_by_gamma_weld[0],5) for p in pf_by_gamma_weld]}")
    # the catalog ratios are gamma ratios (0.5,0.75,1,1.5,2) -> 1,1.5,2,3,4
    # honest verdict:
    print("\nHONEST VERDICT (see report).")


if __name__ == "__main__":
    main()

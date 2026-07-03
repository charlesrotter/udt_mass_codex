"""Tolerance sensitivity of the pair: recount Qfree/Qhat/Vhat at tolfac 1e-13..1e-6."""
import numpy as np, json, sys
from bv14_lib import load, assemble, order_free, order_drop, inertia_band

TAGS = ["row1_m3Z8_belowN0", "row2_m3Z8_aboveN0", "row3_m3Z1_fund",
        "row4_m3Z8_belowN15", "row5_m2Z8_fund"]
for tag in TAGS:
    info, arr = load(tag)
    for Mg in (info["M"], 2*info["M"]):
        Q, ix = assemble(info, arr, Mg)
        iu, ib, iv, ia = ix["iu"], ix["ib"], ix["iv"], ix["ia"]
        of = order_free(ix); Qf = Q[np.ix_(of, of)]
        oh = order_drop(ix, {ia, iv[0]}); Qh = Q[np.ix_(oh, oh)]
        ov = np.array(list(iv[1:])); Vh = Q[np.ix_(ov, ov)]
        line = []
        for tf in (1e-13, 1e-10, 1e-8, 1e-6):
            bf = inertia_band(Qf, tolfac=tf); bh = inertia_band(Qh, tolfac=tf)
            bv = inertia_band(Vh, tolfac=tf)
            line.append(f"tol{tf:.0e}: pair=({bh['n_neg']-bv['n_neg']},{bv['n_pos']})"
                        f" z(Qf,Qh,Vh)=({bf['n_zero']},{bh['n_zero']},{bv['n_zero']})"
                        f" hyp={bf['n_neg']==1+bh['n_neg']}")
        print(f"[{tag} M={Mg}] " + " | ".join(line), flush=True)

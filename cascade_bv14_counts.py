"""bv14 production counts per rung: band-LDL slicing at grids M and 2M.
usage: python3 bv14_counts.py <tag> [--cols]   (--cols adds ANCHORED/FIXED pairs)
Outputs bv14_counts_<tag>.json
"""
import numpy as np, json, sys, time, os
from scipy import sparse
import scipy.sparse.linalg as spla
from bv14_lib import (SCR, load, assemble, order_free, order_drop, inertia_band,
                      translation)

tag = sys.argv[1]
do_cols = "--cols" in sys.argv
info, arr = load(tag)
M = info["M"]
out = dict(tag=tag, a=info["a"], m=info["m"], Z=info["Z"], M=M,
           r_s=info["r_s"], rho_s=info["rho_s"], rhop_s=info["rhop_s"], q=info["q"],
           Up1=info["Up1"], two_m_minus_2a=2.0*(info["m"] - 2.0*info["a"]),
           s1=info["s1"], grids={})

for Mg in (M, 2*M):
    t0 = time.time()
    Q, ix = assemble(info, arr, Mg)
    iu, ib, iv, ia = ix["iu"], ix["ib"], ix["iv"], ix["ia"]
    of = order_free(ix); Qf = Q[np.ix_(of, of)]
    oh = order_drop(ix, {ia, iv[0]}); Qh = Q[np.ix_(oh, oh)]
    ov = np.array(list(iv[1:])); Vh = Q[np.ix_(ov, ov)]
    g = {}
    bf = inertia_band(Qf); bh = inertia_band(Qh); bv = inertia_band(Vh)
    g["Qfree"] = (bf["n_neg"], bf["n_zero"], bf["n_pos"])
    g["Qhat"] = (bh["n_neg"], bh["n_zero"], bh["n_pos"])
    g["Vhat"] = (bv["n_neg"], bv["n_zero"], bv["n_pos"])
    g["min_pivots"] = (bf["min_pivot"], bh["min_pivot"], bv["min_pivot"])
    g["pair_FREE"] = (bh["n_neg"] - bv["n_neg"], bv["n_pos"])       # (n_neg(S_u), n_pos(Vhat))
    g["hyperbolic_ok"] = bool(bf["n_neg"] == 1 + bh["n_neg"])
    # translation
    t = translation(info, arr, Mg, ix)
    tf = t[of]
    num = float(t @ (Q @ t)); den = float(t @ t)*ix["h"]
    g["transl_RQ"] = num/den; g["transl_tQt"] = num
    bdefl = inertia_band(Qf, border=tf)
    g["Qfree_deflated"] = (bdefl["n_neg"], bdefl["n_zero"], bdefl["n_pos"])
    g["deflation_drops_nneg_by"] = bf["n_neg"] - bdefl["n_neg"]
    # near-zero spectrum, mass-normalized (lumped h), deflation-by-inspection
    h = ix["h"]
    mass = np.full(ix["dim"], h); mass[iv[0]] *= 0.5; mass[iv[-1]] *= 0.5
    mass[iu[0]] *= 1.0; mass[ib] = 1.0; mass[ia] = 1.0
    Bm = sparse.diags(mass).tocsc()
    try:
        w, V = spla.eigsh(Q.tocsc(), k=16, M=Bm, sigma=0.0, which="LM", mode="normal")
        tB = t*mass
        ovl = np.abs(V.T @ tB) / (np.sqrt(float(t @ tB)) * np.sqrt((V*(mass[:, None]*V)).sum(0)))
        order = np.argsort(np.abs(w))
        g["near0_eigs"] = [float(w[i]) for i in order]
        g["near0_transl_overlap"] = [float(ovl[i]) for i in order]
        itr = order[int(np.argmax([ovl[i] for i in order]))]
        rest = [i for i in order if i != itr]
        g["transl_eig"] = float(w[itr]); g["transl_eig_overlap"] = float(ovl[itr])
        g["smallest_nontransl_eig"] = float(w[rest[0]])
        g["smallest_nontransl_sign"] = int(np.sign(w[rest[0]]))
    except Exception as e:
        g["eigsh_error"] = str(e)
    if do_cols:
        oa = order_drop(ix, {iu[0]}); Qa = Q[np.ix_(oa, oa)]
        oah = order_drop(ix, {iu[0], ia, iv[0]}); Qah = Q[np.ix_(oah, oah)]
        oxf = order_drop(ix, {ia, ib, iv[0]}); Qxf = Q[np.ix_(oxf, oxf)]
        ba = inertia_band(Qa); bah = inertia_band(Qah); bxf = inertia_band(Qxf)
        g["ANCH_Q"] = (ba["n_neg"], ba["n_zero"], ba["n_pos"])
        g["ANCH_Qhat_nneg"] = bah["n_neg"]
        g["pair_ANCH"] = (bah["n_neg"] - bv["n_neg"], bv["n_pos"])
        g["ANCH_hyperbolic_ok"] = bool(ba["n_neg"] == 1 + bah["n_neg"])
        g["FIXED_Qhat_nneg"] = bxf["n_neg"]
        g["pair_FIXED"] = (bxf["n_neg"] - bv["n_neg"], bv["n_pos"])
    g["wall_s"] = round(time.time() - t0, 1)
    out["grids"][str(Mg)] = g
    print(f"[{tag} M={Mg}] {json.dumps(g, default=float)}", flush=True)

with open(os.path.join(SCR, f"bv14_counts_{tag}.json"), "w") as f:
    json.dump(out, f, indent=1, default=float)
print("saved")

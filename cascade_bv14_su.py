"""Explicit S_u + Vhat (dense) at one grid: exact Haynsworth check + S_u edge eigenvalues.
usage: python3 bv14_su.py <tag> <Mg> [ldl]   (ldl: inertia via Bunch-Kaufman, no full spectrum)
"""
import numpy as np, json, sys, time, os
from bv14_lib import SCR, load, assemble, order_drop, order_free, inertia_band, explicit_Su_Vhat

tag, Mg = sys.argv[1], int(sys.argv[2])
use_ldl = "ldl" in sys.argv[3:]
info, arr = load(tag)
t0 = time.time()
Q, ix = assemble(info, arr, Mg)
iu, ib, iv, ia = ix["iu"], ix["ib"], ix["iv"], ix["ia"]
oh = order_drop(ix, {ia, iv[0]}); Qh = Q[np.ix_(oh, oh)]
ov = np.array(list(iv[1:])); Vh_band = Q[np.ix_(ov, ov)]
bh = inertia_band(Qh); bv = inertia_band(Vh_band)
S, _ = explicit_Su_Vhat(Q, ix)
print(f"[{tag} M={Mg}] S_u formed ({time.time()-t0:.0f}s), dim={S.shape[0]}", flush=True)
d = np.sqrt(np.abs(np.diag(S))); d[d == 0] = 1.0
S *= (1.0/d)[:, None]
S *= (1.0/d)[None, :]
Ss = S   # symmetric to rounding; LAPACK routines use one triangle
if use_ldl:
    from scipy.linalg import ldl
    lu, D, perm = ldl(Ss)
    # inertia from D's 1x1/2x2 blocks
    n = D.shape[0]; i = 0; nneg = npos = nzero = 0
    sub = np.diag(D, -1)
    tol = 1e-12
    while i < n:
        if i < n-1 and abs(sub[i]) > 0.0:
            blk = D[i:i+2, i:i+2]
            w2 = np.linalg.eigvalsh(blk)
            for w in w2:
                if w < -tol: nneg += 1
                elif w > tol: npos += 1
                else: nzero += 1
            i += 2
        else:
            w = D[i, i]
            if w < -tol: nneg += 1
            elif w > tol: npos += 1
            else: nzero += 1
            i += 1
    res = dict(n_neg=nneg, n_zero=nzero, n_pos=npos, method="ldl")
    edge = None
else:
    from scipy.linalg import eigvalsh
    w = eigvalsh(Ss)
    tol = 1e-10*np.max(np.abs(w))
    res = dict(n_neg=int(np.sum(w < -tol)), n_zero=int(np.sum(np.abs(w) <= tol)),
               n_pos=int(np.sum(w > tol)), method="eigvalsh", tol=tol)
    edge = [float(x) for x in w[:5]] + [float(x) for x in w[np.argmin(np.abs(w))-2:np.argmin(np.abs(w))+3]]
idroute = bh["n_neg"] - bv["n_neg"]
ok = (res["n_neg"] == idroute) and (bh["n_neg"] == bv["n_neg"] + res["n_neg"])
out = dict(tag=tag, M=Mg, Su_inertia=res, Su_edge_eigs_scaled=edge,
           Qhat_nneg=bh["n_neg"], Vhat=(bv["n_neg"], bv["n_zero"], bv["n_pos"]),
           identity_route_Su_nneg=idroute, haynsworth_exact=bool(ok),
           wall_s=round(time.time()-t0, 1))
print(json.dumps(out, default=float), flush=True)
with open(os.path.join(SCR, f"bv14_su_{tag}_M{Mg}.json"), "w") as f:
    json.dump(out, f, indent=1, default=float)

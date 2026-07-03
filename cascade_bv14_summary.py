"""Final summary: per row/grid, deflated near-zero spectrum (subspace method) + table."""
import numpy as np, json
from scipy import sparse
import scipy.sparse.linalg as spla
from bv14_lib import load, assemble, translation

TAGS = ["row1_m3Z8_belowN0", "row2_m3Z8_aboveN0", "row3_m3Z1_fund",
        "row4_m3Z8_belowN15", "row5_m2Z8_fund"]

for tag in TAGS:
    info, arr = load(tag)
    M = info["M"]
    print(f"\n===== {tag}  (M={M}) =====")
    for Mg in (M, 2*M):
        Q, ix = assemble(info, arr, Mg)
        iu, ib, iv, ia = ix["iu"], ix["ib"], ix["iv"], ix["ia"]
        h = ix["h"]
        mass = np.full(ix["dim"], h); mass[iv[0]] *= 0.5; mass[iv[-1]] *= 0.5
        mass[ib] = 1.0; mass[ia] = 1.0
        Bm = sparse.diags(mass).tocsc()
        w, V = spla.eigsh(Q.tocsc(), k=16, M=Bm, sigma=0.0, which="LM", mode="normal")
        t = translation(info, arr, Mg, ix)
        tB = t*mass
        tnorm = np.sqrt(float(t @ tB))
        c = (V.T @ tB) / tnorm          # components of t-hat in the eigenbasis (Bm-orthonormal V)
        frac = float(np.sum(c**2))      # fraction of t captured by the 16-dim subspace
        # deflate t within span(V): basis of {x in span V : c.x = 0}
        cn = c/np.linalg.norm(c)
        H = np.eye(len(cn)) - 2.0*np.outer(*(lambda u: (u, u))((cn + np.eye(len(cn))[0]*np.sign(cn[0] if cn[0] != 0 else 1.0))/np.linalg.norm(cn + np.eye(len(cn))[0]*np.sign(cn[0] if cn[0] != 0 else 1.0))))
        C = H[:, 1:]                    # columns orthogonal to cn
        wd = np.linalg.eigvalsh(C.T @ np.diag(w) @ C)
        wd = wd[np.argsort(np.abs(wd))]
        rq = float(t @ (Q @ t)) / float(t @ tB)
        print(f"  Mg={Mg}: t-capture in 16-dim near-0 subspace = {frac:.6f}")
        print(f"    mass-RQ(t) = {rq:+.4e}   (bv13-convention RQ = {float(t@(Q@t))/ (float(t@t)*h):+.4e})")
        print(f"    deflated near-0 eigs (|.| sorted, first 6): "
              + " ".join(f"{x:+.3e}" for x in wd[:6]))
        print(f"    smallest deflated eig sign = {int(np.sign(wd[0]))}")

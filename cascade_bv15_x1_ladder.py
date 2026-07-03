"""bv15 X1 ladder: near-zero cluster vs grid, undeflated + two exact projection-deflations.
A = M^{-1/2} Q M^{-1/2} (MC1 lumped mass = the claim's convention).
Deflation DM: project out s = M^{1/2} t (restriction to t^M-perp = {t^T M x = 0}).
Deflation DE: project out s2 = M^{-1/2} t (restriction to {t^T x = 0}, Euclidean-in-x).
Both are exact rank-one projections in A-space; deflated direction shifted to +1 (Woodbury).
Sparse shift-invert (sigma=0) with banded interleaved ordering; k nearest-zero eigenpairs.
"""
import numpy as np, json, sys, os
from scipy import sparse
from scipy.sparse.linalg import splu, eigsh, LinearOperator
import bv15_asm as asm

SCR = os.path.dirname(os.path.abspath(__file__))
K = 14


def near_zero(Ap, sp, defl_vec, k=K, c=1.0):
    n = Ap.shape[0]
    lu = splu(Ap)
    if defl_vec is None:
        w, Y = eigsh(Ap, k=k, sigma=0, which="LM",
                     OPinv=LinearOperator((n, n), matvec=lu.solve), mode="normal")
    else:
        d = defl_vec / np.linalg.norm(defl_vec)
        a = Ap @ d
        Cm = np.array([[float(d @ a) + c, -1.0], [-1.0, 0.0]])
        U = np.column_stack([d, a])
        KU = np.column_stack([lu.solve(U[:, 0]), lu.solve(U[:, 1])])
        S2 = np.linalg.inv(np.linalg.inv(Cm) + U.T @ KU)
        opinv = lambda x: lu.solve(x) - KU @ (S2 @ (KU.T @ x))
        bmv = lambda x: Ap @ x + U @ (Cm @ (U.T @ x))
        w, Y = eigsh(LinearOperator((n, n), matvec=bmv), k=k, sigma=0, which="LM",
                     OPinv=LinearOperator((n, n), matvec=opinv), mode="normal")
    o = np.argsort(w)
    return w[o], Y[:, o], (sp @ Y[:, o])**2   # overlap with M-metric translation unit vec


def run(tag, Ms):
    info, sol = asm.load_bg(tag)
    fn = os.path.join(SCR, f"bv15_x1_ladder_{tag}.json")
    res = json.load(open(fn)) if os.path.exists(fn) else {}
    for M in Ms:
        Q, idx = asm.assemble_Q(info, sol, M)
        Mm = asm.mass(info, idx, "MC1")
        t = asm.translation(idx)
        dM = np.sqrt(Mm.diagonal())
        A = (sparse.diags(1.0/dM) @ Q @ sparse.diags(1.0/dM))
        A = ((A + A.T) * 0.5).tocsr()
        s = dM * t; s /= np.linalg.norm(s)          # M-orth deflation vector
        s2 = t / dM; s2 /= np.linalg.norm(s2)       # Euclidean-in-x deflation vector
        perm = asm.order_interleave(idx)
        Ap = A[perm][:, perm].tocsc()
        sp, s2p = s[perm], s2[perm]
        tq = float(t @ (Q @ t)); tm = float(t @ (Mm @ t))
        wU, YU, ovU = near_zero(Ap, sp, None)
        ovU_E = (s2p @ YU)**2
        wDM, YDM, ovDM = near_zero(Ap, sp, sp)
        wDE, YDE, ovDE = near_zero(Ap, sp, s2p)
        res[str(M)] = dict(h=idx["h"], RQ_t=tq/tm,
                      undefl=wU.tolist(), ovM=ovU.tolist(), ovE=ovU_E.tolist(),
                      deflM=wDM.tolist(), deflM_ov=ovDM.tolist(),
                      deflE=wDE.tolist(), deflE_ov=ovDE.tolist())
        neg = lambda w: [x for x in w if x < 0]
        print(f"[{tag} M={M}] RQ(t)={tq/tm:+.4e}")
        print("   undefl:", " ".join(f"{x:+.3e}" for x in wU))
        print("   ovM   :", " ".join(f"{x:.3f}" for x in ovU))
        print("   deflM :", " ".join(f"{x:+.3e}" for x in wDM), "| neg:", neg(wDM))
        print("   deflE :", " ".join(f"{x:+.3e}" for x in wDE), "| neg:", neg(wDE))
        sys.stdout.flush()
        json.dump(res, open(fn, "w"), indent=1)
    return res


if __name__ == "__main__":
    tag = sys.argv[1]
    Ms = [int(x) for x in sys.argv[2].split(",")]
    run(tag, Ms)

"""bv15 X1 validation gates (dense, small grids; B00).
V1: translation residual ||Q t|| = O(h^2) (assembly + zero-mode check).
V2: exact projection-deflation: spectrum of P A P (0-dir dropped) == spectrum of N^T A N
    (Householder complement basis), dense, to ~1e-11.
V3: sparse Woodbury shift-invert near-zero cluster == dense values (undeflated + deflated).
A = D^{-1/2} Q D^{-1/2} with D = MC1 lumped mass (their convention; X1 adjudication metric).
"""
import numpy as np, json, os
from scipy import sparse
from scipy.linalg import eigh, qr
from scipy.sparse.linalg import splu, eigsh, LinearOperator
import bv15_asm as asm

SCR = os.path.dirname(os.path.abspath(__file__))


def standard_form(Q, Mm, t):
    d = np.sqrt(Mm.diagonal())
    A = sparse.diags(1.0/d) @ Q @ sparse.diags(1.0/d)
    A = ((A + A.T) * 0.5).tocsr()
    s = d * t
    s = s / np.linalg.norm(s)
    return A, s


def dense_near(Aden, s, deflate, win=8):
    if deflate:
        P = np.eye(len(s)) - np.outer(s, s)
        B = P @ Aden @ P
    else:
        B = Aden
    w, Y = eigh(B)
    k = np.argsort(np.abs(w))[:win]
    k = k[np.argsort(w[k])]
    ov = (Y[:, k].T @ s)**2
    return w[k], ov, Y[:, k]


def householder_near(Aden, s, win=8):
    # complement basis via QR of [s | I]
    n = len(s)
    Qf, _ = qr(s.reshape(-1, 1), mode="full")
    N = Qf[:, 1:]
    w = eigh(N.T @ Aden @ N, eigvals_only=True)
    k = np.argsort(np.abs(w))[:win]
    return np.sort(w[k])


def sparse_near(A, s, perm, deflate, k=8, c=1.0):
    n = A.shape[0]
    Ap = A[perm][:, perm].tocsc()
    sp = s[perm]
    lu = splu(Ap)
    if not deflate:
        op = LinearOperator((n, n), matvec=lu.solve)
        w, Y = eigsh(Ap, k=k, sigma=0, which="LM", OPinv=op, mode="normal")
        ov = (Y.T @ sp)**2
        o = np.argsort(w)
        Yb = np.empty_like(Y)
        Yb[perm] = Y
        return w[o], ov[o], Yb[:, o]
    a = Ap @ sp
    sAs = float(sp @ a)
    U = np.column_stack([sp, a])
    Cm = np.array([[sAs + c, -1.0], [-1.0, 0.0]])
    # B = Ap + U Cm U^T ; OPinv via Woodbury with K = Ap
    KU = np.column_stack([lu.solve(U[:, 0]), lu.solve(U[:, 1])])
    S2 = np.linalg.inv(np.linalg.inv(Cm) + U.T @ KU)
    def opinv(x):
        y = lu.solve(x)
        return y - KU @ (S2 @ (KU.T @ x))
    def bmv(x):
        return Ap @ x + U @ (Cm @ (U.T @ x))
    Bop = LinearOperator((n, n), matvec=bmv)
    w, Y = eigsh(Bop, k=k, sigma=0, which="LM", OPinv=LinearOperator((n, n), matvec=opinv),
                 mode="normal")
    ov = (Y.T @ sp)**2
    o = np.argsort(w)
    Yb = np.empty_like(Y)
    Yb[perm] = Y
    return w[o], ov[o], Yb[:, o]


if __name__ == "__main__":
    info, sol = asm.load_bg("B00")
    out = {}
    for M in (100, 200):
        Q, idx = asm.assemble_Q(info, sol, M)
        Mm = asm.mass(info, idx, "MC1")
        t = asm.translation(idx)
        # V1 translation residual (M-scaled): ||Qt|| / ||t||_M
        tn = t / np.sqrt(t @ (Mm @ t))
        res = np.linalg.norm(Q @ tn)
        A, s = standard_form(Q, Mm, t)
        Aden = A.toarray()
        wu, ovu, _ = dense_near(Aden, s, deflate=False)
        wd, ovd, _ = dense_near(Aden, s, deflate=True)
        wh = householder_near(Aden, s)
        # V2: match deflated dense (drop the s-direction zero, ov~1) against householder
        keep = ovd < 0.5
        wd_k = np.sort(wd[keep])
        nh = min(len(wd_k), len(wh))
        # compare the common near-zero sets by nearest matching
        v2 = float(np.max([np.min(np.abs(wh - x)) for x in wd_k[:nh]]))
        perm = asm.order_interleave(idx)
        wsu, ovsu, _ = sparse_near(A, s, perm, deflate=False)
        wsd, ovsd, _ = sparse_near(A, s, perm, deflate=True)
        v3u = float(np.max([np.min(np.abs(wu - x)) for x in wsu]))
        v3d = float(np.max([np.min(np.abs(np.concatenate([wd, [1.0]])) - x)
                            for x in wsd] + [0.0])) if len(wsd) else np.nan
        out[M] = dict(h=idx["h"], Qt_res=float(res),
                      dense_undefl=[float(x) for x in wu], ov_undefl=[float(x) for x in ovu],
                      dense_defl=[float(x) for x in wd], ov_defl=[float(x) for x in ovd],
                      householder=[float(x) for x in wh],
                      V2_maxmismatch=v2,
                      sparse_undefl=[float(x) for x in wsu],
                      sparse_defl=[float(x) for x in wsd],
                      V3_undefl=v3u, V3_defl=v3d)
        print(f"M={M}: Qt_res={res:.3e}  V2={v2:.3e}  V3u={v3u:.3e}  V3d={v3d:.3e}")
        print("  undefl w:", " ".join(f"{x:+.4e}" for x in wu))
        print("  undefl ov:", " ".join(f"{x:.3f}" for x in ovu))
        print("  defl   w:", " ".join(f"{x:+.4e}" for x in wd))
        print("  defl  ov:", " ".join(f"{x:.3f}" for x in ovd))
    r = out[100]["Qt_res"] / out[200]["Qt_res"]
    print(f"V1 order check: Qt_res(M=100)/Qt_res(M=200) = {r:.2f} (expect ~4 for O(h^2))")
    json.dump(out, open(os.path.join(SCR, "bv15_x1_validate.json"), "w"), indent=1)

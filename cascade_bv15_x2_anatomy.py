"""bv15 X2: anatomy of the deflated negative-branch eigenvector under THREE mass conventions.
Generalized x-space solver: pencil (Q, Mm), exact M-orthogonal projection-deflation of the
translation t via Woodbury rank-2 penalty (t made an exact eigenvector with eigenvalue c=1),
shift-invert at sigma=0. Independent code path from the ladder (validated against it at MC1).

Fractions: f_u = u^T Muu u / (x^T M x), f_beta = (Mbb + elimination fold-in) beta^2 / (x^T M x),
etc.; cross-mass terms (consistent mass u-beta coupling) reported separately.
Also: sign(alpha*beta), u(0), v(0) rel to max field, localization landmarks r50/r90 of the
M-weighted field content, and the FIXED-column near-zero window (alpha=beta=0, u_M=0).
"""
import numpy as np, json, sys, os
from scipy import sparse
from scipy.sparse.linalg import splu, eigsh, LinearOperator
import bv15_asm as asm

SCR = os.path.dirname(os.path.abspath(__file__))


def defl_solve(Q, Mm, t, perm, k=6, c=1.0):
    n = Q.shape[0]
    Qp = Q[perm][:, perm].tocsc()
    Mp = Mm[perm][:, perm].tocsr()
    tp = t[perm]
    g = Mp @ tp
    gam = float(tp @ g)
    qt = Qp @ tp
    tQt = float(tp @ qt)
    U = np.column_stack([g, qt])
    C = np.array([[tQt/gam**2 + c/gam, -1.0/gam], [-1.0/gam, 0.0]])
    lu = splu(Qp)
    KU = np.column_stack([lu.solve(U[:, 0]), lu.solve(U[:, 1])])
    S2 = np.linalg.inv(np.linalg.inv(C) + U.T @ KU)
    opinv = lambda x: lu.solve(x) - KU @ (S2 @ (KU.T @ x))
    bmv = lambda x: Qp @ x + U @ (C @ (U.T @ x))
    w, Y = eigsh(LinearOperator((n, n), matvec=bmv), k=k, M=Mp, sigma=0, which="LM",
                 OPinv=LinearOperator((n, n), matvec=opinv), mode="normal")
    o = np.argsort(w)
    Yb = np.empty_like(Y)
    Yb[perm] = Y
    return w[o], Yb[:, o], gam, tp


def anatomy(info, idx, Mm, x, t):
    M = idx["M"]
    iu, ib, iv, ia = idx["iu"], idx["ib"], idx["iv"], idx["ia"]
    xn = x / np.sqrt(x @ (Mm @ x))
    tot = 1.0
    eu = np.zeros_like(xn); eu[iu] = xn[iu]
    ev = np.zeros_like(xn); ev[iv] = xn[iv]
    eb = np.zeros_like(xn); eb[ib] = xn[ib]
    ea = np.zeros_like(xn); ea[ia] = xn[ia]
    f = {}
    f["f_u"] = float(eu @ (Mm @ eu)); f["f_v"] = float(ev @ (Mm @ ev))
    f["f_beta"] = float(eb @ (Mm @ eb)); f["f_alpha"] = float(ea @ (Mm @ ea))
    f["f_cross"] = float(tot - f["f_u"] - f["f_v"] - f["f_beta"] - f["f_alpha"])
    al, be = xn[ia], xn[ib]
    f["alpha"] = float(al); f["beta"] = float(be)
    f["sign_ab"] = float(np.sign(al) * np.sign(be))
    u = xn[iu]; v = xn[iv]
    f["u0_over_umax"] = float(u[0] / np.max(np.abs(u)))
    f["v0_over_vmax"] = float(v[0] / np.max(np.abs(v)))
    f["u_end_over_umax"] = float(u[-1] / np.max(np.abs(u)))
    f["v_end_over_vmax"] = float(v[-1] / np.max(np.abs(v)))
    # localization of field content (lumped weight h per node, both fields combined)
    dens = np.zeros(M + 1)
    dens[:M] += u**2
    dens += v**2
    cum = np.cumsum(dens); cum /= cum[-1]
    rn = idx["rn"]
    f["r50_over_rs"] = float(rn[np.searchsorted(cum, 0.5)] / rn[-1])
    f["r90_over_rs"] = float(rn[np.searchsorted(cum, 0.9)] / rn[-1])
    f["r10_over_rs"] = float(rn[np.searchsorted(cum, 0.1)] / rn[-1])
    f["t_overlap_M"] = float((x @ (Mm @ t))**2 / ((x @ (Mm @ x)) * (t @ (Mm @ t))))
    return f


def fixed_column(info, sol, M):
    """FIXED diagnostic: alpha=beta=0 (=> u_M=0), boundary bilinears drop. Near-zero window."""
    Q, idx = asm.assemble_Q(info, sol, M)
    keep = np.concatenate([idx["iu"], idx["iv"]])
    Qf = Q[keep][:, keep].tocsc()
    Mmf = asm.mass(info, idx, "MC1")[keep][:, keep]
    d = np.sqrt(Mmf.diagonal())
    A = sparse.diags(1.0/d) @ Qf @ sparse.diags(1.0/d)
    A = ((A + A.T)*0.5).tocsc()
    # interleave u,v for band
    Mg = idx["M"]
    o = [0 + Mg]  # v0 (v index offset within keep: after M u's)
    o = []
    for j in range(Mg):
        o += [Mg + j, j]
    o += [2*Mg]
    o = np.array(o)
    Ap = A[o][:, o].tocsc()
    lu = splu(Ap)
    w, _ = eigsh(Ap, k=10, sigma=0, which="LM",
                 OPinv=LinearOperator(Ap.shape, matvec=lu.solve), mode="normal")
    return np.sort(w)


if __name__ == "__main__":
    tag = sys.argv[1]
    Ms = [int(x) for x in sys.argv[2].split(",")]
    info, sol = asm.load_bg(tag)
    out = {}
    for M in Ms:
        Q, idx = asm.assemble_Q(info, sol, M)
        t = asm.translation(idx)
        perm = asm.order_interleave(idx)
        row = {}
        for conv in ("MC1", "MC1b", "MC2", "MC3"):
            Mm = asm.mass(info, idx, conv)
            w, Y, gam, _ = defl_solve(Q, Mm, t, perm)
            # branch selection: the soft branch is the fold-dominated member of the cluster
            fold = []
            for jj in range(len(w)):
                x = Y[:, jj] / np.sqrt(Y[:, jj] @ (Mm @ Y[:, jj]))
                fold.append(Mm[idx["ia"], idx["ia"]]*x[idx["ia"]]**2
                            + Mm[idx["ib"], idx["ib"]]*x[idx["ib"]]**2)
            j = int(np.argmax(fold))
            row[conv] = dict(lam=float(w[j]), cluster=w.tolist(),
                             **anatomy(info, idx, Mm, Y[:, j], t))
            print(f"[{tag} M={M} {conv}] lam={w[j]:+.4e} f_a={row[conv]['f_alpha']:.4f} "
                  f"f_b={row[conv]['f_beta']:.4f} f_u={row[conv]['f_u']:.4f} "
                  f"f_v={row[conv]['f_v']:.4f} fx={row[conv]['f_cross']:+.4f} "
                  f"sgn(ab)={row[conv]['sign_ab']:+.0f} u0={row[conv]['u0_over_umax']:+.2e} "
                  f"v0={row[conv]['v0_over_vmax']:+.2e} r50={row[conv]['r50_over_rs']:.4f}")
            sys.stdout.flush()
        out[str(M)] = row
    wf = fixed_column(info, sol, Ms[-1])
    out["FIXED_near_zero"] = wf.tolist()
    print("FIXED near-zero:", " ".join(f"{x:+.3e}" for x in wf))
    json.dump(out, open(os.path.join(SCR, f"bv15_x2_anatomy_{tag}.json"), "w"), indent=1)

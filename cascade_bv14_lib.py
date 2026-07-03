"""bv14 library: independent P1-FEM/2-pt-Gauss assembly of the verified second-variation
form + banded LDL^T spectrum-slicing inertia (own code, own discretization).

Form (verified operator, stability_operator_results.md):
  Q[u,v,beta,alpha] = int_0^{r_s} [ cku u'^2 + ckv v'^2 + cc1 v u' + cc2 u v'
                                    + cmu u^2 + cmv v^2 ] dr
                      + Lrho_s * beta * v(r_s) + Up(rho_c=1) * alpha * v(0)
  essential odd-fold constraint u(r_s) = -phip_s * beta  (u_M eliminated).
  cku=(Z/2)rho^2, ckv=-2e^{-2phi}, cc1=2Z rho phi', cc2=8 e^{-2phi} rho',
  cmu=-4 e^{-2phi} rho'^2, cmv=(Z/2)phi'^2 - U''(rho)/2.
DOFs (natural order): iu=0..M-1, ib=M, iv=M+1..2M+1, ia=2M+2; dim=2M+3.
"""
import numpy as np, json, os
from scipy import sparse

SCR = os.path.dirname(os.path.abspath(__file__))
G = 0.5/np.sqrt(3.0)   # gauss offsets in xi: 0.5 -+ G
XI = (0.5 - G, 0.5 + G)


def makeU(a, m):
    def U(rho):   return 2.0 * rho**m * np.exp(-a*(rho*rho - 1.0))
    def Up(rho):  return U(rho) * (m/rho - 2.0*a*rho)
    def Upp(rho): return Up(rho)*(m/rho - 2.0*a*rho) + U(rho)*(-m/rho**2 - 2.0*a)
    return U, Up, Upp


def load(tag):
    info = json.load(open(os.path.join(SCR, f"bv14_bg_{tag}.json")))
    arr = np.load(os.path.join(SCR, f"bv14_bg_{tag}.npz"))
    return info, arr


def coeffs(info, phi, phip, rho, rhop):
    Z = info["Z"]
    _, _, Upp = makeU(info["a"], info["m"])
    em2p = np.exp(-2.0*phi)
    return dict(cku=0.5*Z*rho**2, ckv=-2.0*em2p, cc1=2.0*Z*rho*phip,
                cc2=8.0*em2p*rhop, cmu=-4.0*em2p*rhop**2,
                cmv=0.5*Z*phip**2 - 0.5*Upp(rho))


def assemble(info, arr, Mg):
    """Sparse symmetric Q (natural order) via P1 FE, 2-pt Gauss per element."""
    r_s, phip_s = info["r_s"], info["phip_s"]
    h = r_s / Mg
    y = arr[f"g{Mg}_gp_y"]            # 4 x 2Mg  [gp1 elems | gp2 elems]
    dim = 2*Mg + 3
    ib, ia = Mg, 2*Mg + 2
    iv0 = Mg + 1
    # u-side local (l,r) indices & weights (u_M -> -phip_s * beta)
    ul_i = np.arange(Mg);            ul_w = np.ones(Mg)
    ur_i = np.concatenate([np.arange(1, Mg), [ib]])
    ur_w = np.concatenate([np.ones(Mg-1), [-phip_s]])
    vl_i = iv0 + np.arange(Mg);      vr_i = iv0 + np.arange(1, Mg+1)
    one = np.ones(Mg)

    rows, cols, vals = [], [], []
    def add(c, fi, fw, gi, gw):
        # accumulate c*(fw x_fi)(gw x_gi) symmetric
        v = 0.5 * c * fw * gw
        rows.append(fi); cols.append(gi); vals.append(v)
        rows.append(gi); cols.append(fi); vals.append(v)

    for g in range(2):
        xi = XI[g]; w = 0.5*h
        C = coeffs(info, *(y[:, g*Mg:(g+1)*Mg]))
        # shape values at this gauss point:  field = (1-xi)*left + xi*right ; deriv = (r-l)/h
        # cku u'^2
        for (fi, fw, gi, gw, c) in (
            (ul_i, -ul_w/h, ul_i, -ul_w/h, C["cku"]*w),
            (ul_i, -ul_w/h, ur_i,  ur_w/h, 2.0*C["cku"]*w),
            (ur_i,  ur_w/h, ur_i,  ur_w/h, C["cku"]*w),
        ): add(c, fi, fw*one, gi, gw*one)
        # ckv v'^2
        for (fi, fw, gi, gw, c) in (
            (vl_i, -1.0/h, vl_i, -1.0/h, C["ckv"]*w),
            (vl_i, -1.0/h, vr_i,  1.0/h, 2.0*C["ckv"]*w),
            (vr_i,  1.0/h, vr_i,  1.0/h, C["ckv"]*w),
        ): add(c, fi, fw*one, gi, gw*one)
        # cc1 v u'
        for (fi, fw) in ((vl_i, (1-xi)*one), (vr_i, xi*one)):
            for (gi, gw) in ((ul_i, -ul_w/h), (ur_i, ur_w/h)):
                add(C["cc1"]*w, fi, fw, gi, gw)
        # cc2 u v'
        for (fi, fw) in ((ul_i, (1-xi)*ul_w), (ur_i, xi*ur_w)):
            for (gi, gw) in ((vl_i, -one/h), (vr_i, one/h)):
                add(C["cc2"]*w, fi, fw, gi, gw)
        # cmu u^2
        for (fi, fw, gi, gw, c) in (
            (ul_i, (1-xi)*ul_w, ul_i, (1-xi)*ul_w, C["cmu"]*w),
            (ul_i, (1-xi)*ul_w, ur_i,  xi*ur_w,    2.0*C["cmu"]*w),
            (ur_i,  xi*ur_w,    ur_i,  xi*ur_w,    C["cmu"]*w),
        ): add(c, fi, fw, gi, gw)
        # cmv v^2
        for (fi, fw, gi, gw, c) in (
            (vl_i, (1-xi)*one, vl_i, (1-xi)*one, C["cmv"]*w),
            (vl_i, (1-xi)*one, vr_i,  xi*one,    2.0*C["cmv"]*w),
            (vr_i,  xi*one,    vr_i,  xi*one,    C["cmv"]*w),
        ): add(c, fi, fw, gi, gw)

    rows = np.concatenate(rows); cols = np.concatenate(cols); vals = np.concatenate(vals)
    # boundary bilinears
    br = np.array([ib, iv0+Mg, ia, iv0]); bc = np.array([iv0+Mg, ib, iv0, ia])
    bv = np.array([0.5*info["Lrho_s"], 0.5*info["Lrho_s"], 0.5*info["Up1"], 0.5*info["Up1"]])
    rows = np.concatenate([rows, br]); cols = np.concatenate([cols, bc])
    vals = np.concatenate([vals, bv])
    Q = sparse.coo_matrix((vals, (rows, cols)), shape=(dim, dim)).tocsr()
    Q.sum_duplicates()
    idx = dict(iu=np.arange(Mg), ib=ib, iv=iv0+np.arange(Mg+1), ia=ia, h=h, M=Mg, dim=dim)
    return Q, idx


# ---------------------------------------------------------------- orderings / band extraction
def order_free(ix):
    M = ix["M"]; iu, iv, ib, ia = ix["iu"], ix["iv"], ix["ib"], ix["ia"]
    o = [iv[0], ia, iu[0]]
    for j in range(1, M): o += [iv[j], iu[j]]
    o += [iv[M], ib]
    return np.array(o)

def order_drop(ix, drop):
    o = order_free(ix)
    drop = {int(x) for x in drop}
    return np.array([int(i) for i in o if int(i) not in drop])


def to_band(Qsub):
    A = Qsub.tocoo()
    kd = int(np.max(np.abs(A.row - A.col))) if A.nnz else 0
    n = Qsub.shape[0]
    ab = np.zeros((kd+1, n))
    m = A.row >= A.col
    ab[A.row[m]-A.col[m], A.col[m]] += A.data[m]
    return ab, kd, n


def diagscale(Qsub, border=None):
    d = np.sqrt(np.abs(Qsub.diagonal()))
    d[d == 0] = 1.0
    Dinv = sparse.diags(1.0/d)
    Qs = (Dinv @ Qsub @ Dinv).tocsr()
    if border is not None:
        return Qs, border/d
    return Qs


def gersh(Qs):
    return float(np.max(np.abs(Qs).sum(axis=1)))


def band_ldl_count(ab, kd, n, shift, border=None):
    """#negative pivots of LDL^T of (A - shift I)  [+ bordered constraint row if border given].
    Returns (nneg_pivots, min_abs_pivot, corner_sign or None)."""
    a = [ab[k].copy() for k in range(kd+1)]
    a[0] = a[0] - shift
    a = [list(x) for x in a]
    bt = list(border) if border is not None else None
    s_corner = 0.0
    neg = 0; minp = np.inf
    TINY = 1e-320
    for j in range(n):
        d = a[0][j]
        ad = abs(d)
        if ad < minp: minp = ad
        if d < 0.0: neg += 1
        if ad < TINY: d = TINY if d >= 0 else -TINY
        inv = 1.0/d
        kmax = kd if j + kd < n else n - 1 - j
        if bt is not None:
            btj = bt[j]
            s_corner -= btj*btj*inv
        for k1 in range(1, kmax+1):
            c1 = a[k1][j]
            if c1 == 0.0 and (bt is None or bt[j] == 0.0):
                continue
            l1 = c1*inv
            jk = j + k1
            if bt is not None and btj != 0.0:
                bt[jk] -= l1*btj
            if c1 != 0.0:
                for k2 in range(k1, kmax+1):
                    a[k2-k1][jk] -= l1*a[k2][j]
    if border is not None:
        if s_corner < 0.0: neg += 1
        return neg, minp, s_corner
    return neg, minp, None


def inertia_band(Qsub, tolfac=1e-10, border=None):
    """(n_neg, n_zero, n_pos) with |lambda|<=eps zero band on the diag-scaled matrix.
    If border given: inertia of the border-constrained (deflated) form (dim n-1)."""
    if border is not None:
        Qs, ts = diagscale(Qsub, border)
    else:
        Qs = diagscale(Qsub); ts = None
    ab, kd, n = to_band(Qs)
    eps = tolfac * gersh(Qs)
    nlt_m, pm, _ = band_ldl_count(ab, kd, n, -eps, ts)
    nlt_p, pp, _ = band_ldl_count(ab, kd, n, +eps, ts)
    if border is not None:
        nlt_m -= 1; nlt_p -= 1
        n = n - 1
    return dict(n_neg=nlt_m, n_zero=nlt_p - nlt_m, n_pos=n - nlt_p,
                eps=eps, min_pivot=min(pm, pp), n=n)


# ---------------------------------------------------------------- dense reference (validation)
def inertia_dense_eig(A, tolfac=1e-10):
    from scipy.linalg import eigvalsh
    d = np.sqrt(np.abs(np.diag(A))); d[d == 0] = 1.0
    As = A / np.outer(d, d)
    w = eigvalsh(As)
    tol = tolfac * np.max(np.abs(w))
    return dict(n_neg=int(np.sum(w < -tol)), n_zero=int(np.sum(np.abs(w) <= tol)),
                n_pos=int(np.sum(w > tol)), n=A.shape[0])


def explicit_Su_Vhat(Q, ix):
    """Form V-hat (v1..vM tridiag) and S_u = A - B Vhat^{-1} B^T densely (v0=0 convention)."""
    from scipy.linalg import solve_banded
    M = ix["M"]
    uside = list(ix["iu"]) + [ix["ib"]]
    vside = list(ix["iv"][1:])
    Qc = Q.tocsr() if sparse.issparse(Q) else sparse.csr_matrix(Q)
    A = Qc[np.ix_(uside, uside)].toarray()
    Vh = Qc[np.ix_(vside, vside)].tocsr()
    B = Qc[np.ix_(uside, vside)].tocsr()
    # banded solve of tridiagonal Vh
    n = Vh.shape[0]
    abv = np.zeros((3, n))
    abv[1] = Vh.diagonal(0)
    abv[0, 1:] = Vh.diagonal(1)
    abv[2, :-1] = Vh.diagonal(-1)
    X = solve_banded((1, 1), abv, B.toarray().T)
    S = A - B @ X
    S = 0.5*(S + S.T)
    return S, Vh


def translation(info, arr, Mg, ix):
    t = np.zeros(ix["dim"])
    t[ix["iu"]] = -arr[f"g{Mg}_node_phip"][:Mg]
    t[ix["ib"]] = 1.0
    t[ix["iv"]] = -arr[f"g{Mg}_node_rhop"]
    t[ix["ia"]] = 1.0
    return t

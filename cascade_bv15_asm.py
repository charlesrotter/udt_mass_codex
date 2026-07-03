"""bv15 own assembly: P1 FEM with MIDPOINT (1-pt Gauss) quadrature of the verified
second-variation form (stability_operator_results.md; coefficient set as documented):

  Q = int_0^{r_s} [ cku u'^2 + ckv v'^2 + cc1 v u' + cc2 u v' + cmu u^2 + cmv v^2 ] dr
      + Lrho_s * beta * v(r_s) + Up(rho_c) * alpha * v(0),
  essential odd-fold constraint u(r_s) = -phip_s * beta  (u_M eliminated into beta).
  cku=(Z/2)rho^2, ckv=-2e^{-2phi}, cc1=2Z rho phi', cc2=8 e^{-2phi} rho',
  cmu=-4 e^{-2phi} rho'^2, cmv=(Z/2)phi'^2 - U''(rho)/2.

DOF order (natural): u_0..u_{M-1} | beta | v_0..v_M | alpha.  dim = 2M+3.
Quadrature deliberately DIFFERENT from the stage-2/bv14 codes (they used 2-pt Gauss).
Mass conventions:
  MC1 ("theirs"): lumped-h diag; u_0, v_0, v_M get h/2 (trapezoid lumping), interior h;
        alpha, beta weight 1; eliminated u_M carries no mass.
  MC1b: all-node weight h (lumping variant, sensitivity check).
  MC2 ("mine"): consistent P1 mass (tridiag h/6[1,4,1]) for u and v INCLUDING the
        u_M -> -phip_s*beta elimination fold-in; alpha,beta weight 1.
  MC3 ("boundary-Lagrangian weights"): MC2 fields; alpha diag = |Up1|, beta diag += |Lrho_s|.
"""
import numpy as np, pickle, os
from scipy import sparse

SCR = os.path.dirname(os.path.abspath(__file__))


def makeU(a, m):
    def U(rho):   return 2.0 * rho**m * np.exp(-a*(rho*rho - 1.0))
    def Up(rho):  return U(rho) * (m/rho - 2.0*a*rho)
    def Upp(rho): return Up(rho)*(m/rho - 2.0*a*rho) + U(rho)*(-m/rho**2 - 2.0*a)
    return U, Up, Upp


def load_bg(tag):
    d = pickle.load(open(os.path.join(SCR, f"bv15_bg_{tag}.pkl"), "rb"))
    return d["info"], d["sol"]


def grids(info, sol, M):
    r_s = info["r_s"]
    h = r_s / M
    rn = np.linspace(0.0, r_s, M + 1)
    rm = 0.5 * (rn[:-1] + rn[1:])
    yn = sol.sol(rn)   # 4 x (M+1)
    ym = sol.sol(rm)   # 4 x M
    return h, rn, rm, yn, ym


def coeffs(info, y):
    Z = info["Z"]
    _, _, Upp = makeU(info["a"], info["m"])
    phi, phip, rho, rhop = y
    em2p = np.exp(-2.0 * phi)
    return dict(cku=0.5*Z*rho**2, ckv=-2.0*em2p, cc1=2.0*Z*rho*phip,
                cc2=8.0*em2p*rhop, cmu=-4.0*em2p*rhop**2,
                cmv=0.5*Z*phip**2 - 0.5*Upp(rho))


def assemble_Q(info, sol, M):
    """Sparse symmetric Q, midpoint quadrature. Returns Q (csr), idx dict."""
    h, rn, rm, yn, ym = grids(info, sol, M)
    C = coeffs(info, ym)                     # coefficients at element midpoints
    phip_s = info["phip_s"]
    dim = 2*M + 3
    ib, ia, iv0 = M, 2*M + 2, M + 1

    # u DOF index & weight per element endpoint (u_M -> -phip_s * beta)
    uL_i = np.arange(M);  uL_w = np.ones(M)
    uR_i = np.concatenate([np.arange(1, M), [ib]])
    uR_w = np.concatenate([np.ones(M-1), [-phip_s]])
    vL_i = iv0 + np.arange(M); vR_i = iv0 + np.arange(1, M+1)
    one = np.ones(M)

    R, Cc, V = [], [], []
    def add(fi, fw, gi, gw, cf):
        # symmetric accumulate of cf * (fw x_fi) * (gw x_gi), cf per-element incl. h
        val = 0.5 * cf * fw * gw
        R.append(fi); Cc.append(gi); V.append(val)
        R.append(gi); Cc.append(fi); V.append(val)

    # derivative factors and midpoint value factors
    du = [(uL_i, -uL_w/h), (uR_i, uR_w/h)]
    mu = [(uL_i, 0.5*uL_w), (uR_i, 0.5*uR_w)]
    dv = [(vL_i, -one/h), (vR_i, one/h)]
    mv = [(vL_i, 0.5*one), (vR_i, 0.5*one)]

    for (fi, fw) in du:
        for (gi, gw) in du: add(fi, fw*one, gi, gw*one, h*C["cku"])
    for (fi, fw) in dv:
        for (gi, gw) in dv: add(fi, fw, gi, gw, h*C["ckv"])
    for (fi, fw) in mv:
        for (gi, gw) in du: add(fi, fw, gi, gw*one, h*C["cc1"])
    for (fi, fw) in mu:
        for (gi, gw) in dv: add(fi, fw, gi, gw, h*C["cc2"])
    for (fi, fw) in mu:
        for (gi, gw) in mu: add(fi, fw, gi, gw, h*C["cmu"])
    for (fi, fw) in mv:
        for (gi, gw) in mv: add(fi, fw, gi, gw, h*C["cmv"])

    R = np.concatenate(R); Cc = np.concatenate(Cc); V = np.concatenate(V)
    # boundary bilinears (symmetrized halves)
    br = np.array([ib, iv0+M, ia, iv0]); bc = np.array([iv0+M, ib, iv0, ia])
    bv = np.array([0.5*info["Lrho_s"], 0.5*info["Lrho_s"], 0.5*info["Up1"], 0.5*info["Up1"]])
    R = np.concatenate([R, br]); Cc = np.concatenate([Cc, bc]); V = np.concatenate([V, bv])
    Q = sparse.coo_matrix((V, (R, Cc)), shape=(dim, dim)).tocsr()
    Q.sum_duplicates()
    idx = dict(M=M, h=h, dim=dim, iu=np.arange(M), ib=ib, iv=iv0+np.arange(M+1), ia=ia,
               rn=rn, node_phip=yn[1], node_rhop=yn[3])
    return Q, idx


def mass(info, idx, kind):
    M, h = idx["M"], idx["h"]
    dim = idx["dim"]
    ib, ia, iu, iv = idx["ib"], idx["ia"], idx["iu"], idx["iv"]
    phip_s = info["phip_s"]
    if kind in ("MC1", "MC1b"):
        d = np.zeros(dim)
        d[iu] = h; d[iv] = h
        if kind == "MC1":
            d[iu[0]] = 0.5*h; d[iv[0]] = 0.5*h; d[iv[-1]] = 0.5*h
        d[ib] = 1.0; d[ia] = 1.0
        return sparse.diags(d).tocsr()
    # consistent P1: diag 2h/3 interior, h/3 ends; offdiag h/6
    R, C, V = [], [], []
    def sym(i, j, v):
        R.extend([i, j]); C.extend([j, i]); V.extend([0.5*v, 0.5*v])
    # u field incl. eliminated u_M = -phip_s*beta
    ucol = list(iu) + [ib]
    uw = [1.0]*M + [-phip_s]
    for e in range(M):                       # elements 0..M-1, endpoints e,e+1 in ucol
        i, j = ucol[e], ucol[e+1]; wi, wj = uw[e], uw[e+1]
        sym(i, i, (h/3.0)*wi*wi); sym(j, j, (h/3.0)*wj*wj); sym(i, j, 2*(h/6.0)*wi*wj)
    for e in range(M):
        i, j = iv[e], iv[e+1]
        sym(i, i, h/3.0); sym(j, j, h/3.0); sym(i, j, 2*(h/6.0))
    wa, wb = (1.0, 1.0) if kind == "MC2" else (abs(info["Up1"]), abs(info["Lrho_s"]))
    sym(ia, ia, wa); sym(ib, ib, wb)
    Mm = sparse.coo_matrix((V, (R, C)), shape=(dim, dim)).tocsr()
    Mm.sum_duplicates()
    return Mm


def translation(idx):
    t = np.zeros(idx["dim"])
    t[idx["iu"]] = -idx["node_phip"][:idx["M"]]
    t[idx["ib"]] = 1.0
    t[idx["iv"]] = -idx["node_rhop"]
    t[idx["ia"]] = 1.0
    return t


def order_interleave(idx):
    """Bandwidth-reducing permutation: v0, alpha, u0, v1, u1, ..., v_{M-1}, u_{M-1}, vM, beta."""
    M, iu, iv, ib, ia = idx["M"], idx["iu"], idx["iv"], idx["ib"], idx["ia"]
    o = [iv[0], ia, iu[0]]
    for j in range(1, M):
        o += [iv[j], iu[j]]
    o += [iv[M], ib]
    return np.array(o)

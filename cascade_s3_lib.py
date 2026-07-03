"""s3 stage-3 soft-mode identification library.
Backgrounds: cached s2_bg_<tag>.pkl dense interpolants (0 new nonlinear shots).
Assembly: cascade_bv14_lib.py (validated blind-verifier machinery), arrays regenerated
from the pickle interpolant at arbitrary grids in bv14 format.
Mass convention: bv14_counts (lumped h; v0,vM x0.5; alpha,beta weight 1) so eigenvalues
are directly comparable to the banked seed numbers.
"""
import numpy as np, json, os, pickle, sys
from scipy import sparse
import scipy.sparse.linalg as spla

SCR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/udt-admin/udt_mass_codex')
from cascade_bv14_lib import makeU, assemble as bv14_assemble, order_free, order_drop, \
    inertia_band, translation as bv14_translation

GAUSS = 0.5/np.sqrt(3.0)
TAGS = {'B00': 'row1_m3Z8_belowN0', 'SM2': 'row5_m2Z8_fund', 'SZ1': 'row3_m3Z1_fund'}

def load_bg(tag):
    bg = pickle.load(open(os.path.join(SCR, f's2_bg_{tag}.pkl'), 'rb'))
    assert bg['status'] == 'seal'
    return bg

def bg_info(bg):
    """bv14-format info dict from the s2 pickle (EOM-exact Lrho_s)."""
    U, Up, Upp = makeU(bg['a'], bg['m'])
    r_s = bg['r_s']
    return dict(a=bg['a'], m=bg['m'], Z=bg['Z'], r_s=r_s, phip_s=bg['phip_s'],
                rho_s=bg['rho_s'], rhop_s=bg['rhop_s'], q=bg['q'],
                Lrho_s=bg['Lrho_s'], Up1=float(Up(1.0)), Upp1=float(Upp(1.0)))

def gen_arrays(bg, Mg):
    """bv14-format arrays at grid Mg off the dense interpolant."""
    r_s = bg['r_s']; h = r_s/Mg
    mid = (np.arange(Mg) + 0.5)*h
    rg = np.concatenate([mid - GAUSS*h, mid + GAUSS*h])
    rn = np.arange(Mg+1)*h
    yg = bg['sol'].sol(rg); yn = bg['sol'].sol(rn)
    return {f'g{Mg}_gp_y': yg, f'g{Mg}_node_phip': yn[1], f'g{Mg}_node_rhop': yn[3]}

def build(bg, Mg):
    info = bg_info(bg)
    arr = gen_arrays(bg, Mg)
    Q, ix = bv14_assemble(info, arr, Mg)
    t = np.zeros(ix['dim'])
    t[ix['iu']] = -arr[f'g{Mg}_node_phip'][:Mg]
    t[ix['ib']] = 1.0
    t[ix['iv']] = -arr[f'g{Mg}_node_rhop']
    t[ix['ia']] = 1.0
    return Q.tocsc(), ix, t

def mass_vec(ix):
    """bv14_counts mass convention."""
    h = ix['h']
    m = np.full(ix['dim'], h)
    m[ix['iv'][0]] *= 0.5; m[ix['iv'][-1]] *= 0.5
    m[ix['ib']] = 1.0; m[ix['ia']] = 1.0
    return m

def anchored_indices(ix):
    """ANCHORED column: delete u_0 (u(0)=0)."""
    return np.array([i for i in range(ix['dim']) if i != ix['iu'][0]])

def near0_eigs(Q, mass, k=12, v0=None):
    """Undeflated near-zero cluster of Q x = lam W x (shift-invert sigma=0)."""
    W = sparse.diags(mass).tocsc()
    w, V = spla.eigsh(Q, k=k, M=W, sigma=0.0, which='LM', mode='normal', v0=v0)
    o = np.argsort(np.abs(w))
    return w[o], V[:, o]

def deflated_near0(Q, mass, t, k=8, tol=0):
    """Exact translation-projected near-zero cluster: eigenproblem of Q on
    {x: t^T W x = 0} via Sherman-Morrison-corrected shift-invert (sigma=0).
    Returns (eigs sorted by |.|, vecs, diagnostics)."""
    n = Q.shape[0]
    W = mass
    lu = spla.splu(Q)
    Wt = W*t
    z = lu.solve(Wt)
    ztWt = float(Wt @ z)
    tW_norm2 = float(t @ Wt)
    def opinv(b):
        # scipy shift-invert mode applies M to the Lanczos vector BEFORE OPinv:
        # b = W x. Solve Q y + mu W t = b with t^T W y = 0.
        w = lu.solve(b)
        return w - z*(float(Wt @ w)/ztWt)
    OPinv = spla.LinearOperator((n, n), matvec=opinv)
    Wop = sparse.diags(W).tocsc()
    rng = np.random.default_rng(7)
    v0 = rng.standard_normal(n)
    v0 -= t*(float(Wt @ v0)/tW_norm2)
    w, V = spla.eigsh(Q, k=k, M=Wop, sigma=0.0, which='LM', mode='normal',
                      OPinv=OPinv, v0=v0)
    o = np.argsort(np.abs(w))
    w, V = w[o], V[:, o]
    # diagnostics: residual t-content of returned vectors (should be ~0)
    tcont = np.array([abs(float(Wt @ V[:, j]))/np.sqrt(tW_norm2*float(V[:, j] @ (W*V[:, j])))
                      for j in range(V.shape[1])])
    return w, V, dict(t_content=tcont.tolist())

def wdot(x, y, mass):
    return float(x @ (mass*y))

def wnorm(x, mass):
    return np.sqrt(wdot(x, x, mass))

def overlap(x, y, mass):
    return wdot(x, y, mass)/(wnorm(x, mass)*wnorm(y, mass))

# ---------------------------------------------------------------- candidate directions
def dir_homothety(bg, ix):
    """(u,v,alpha,beta) = (-r phi', rho - r rho', 0, r_s) on the grid (bv13 W5iii family)."""
    Mg = ix['M']; h = ix['h']
    rn = np.arange(Mg+1)*h
    y = bg['sol'].sol(rn)
    d = np.zeros(ix['dim'])
    d[ix['iu']] = -rn[:Mg]*y[1][:Mg]
    d[ix['ib']] = bg['r_s']
    d[ix['iv']] = y[2] - rn*y[3]
    d[ix['ia']] = 0.0
    return d

def jac_rhs_factory(bg):
    """Linearized (variational) RHS about the cached background + the d/da inhomogeneity."""
    Z = bg['Z']
    U, Up, Upp = makeU(bg['a'], bg['m'])
    sol = bg['sol'].sol
    def rhs_hom(r, Y):
        phi, phip, rho, rhop = sol(r)
        e2p = np.exp(2.0*phi); em2p = 1.0/e2p
        u, up, v, vp = Y
        # d(phipp): phipp = 4 rhop^2 em2p/(Z rho^2) - 2 phip rhop / rho
        dpp = (-8.0*rhop**2*em2p/(Z*rho**2))*u + (-2.0*rhop/rho)*up \
              + (-8.0*rhop**2*em2p/(Z*rho**3) + 2.0*phip*rhop/rho**2)*v \
              + (8.0*rhop*em2p/(Z*rho**2) - 2.0*phip/rho)*vp
        # d(rhopp): rhopp = 2 phip rhop - (Z/4) rho e2p phip^2 + (e2p/4) Up(rho)
        drr = (-0.5*Z*rho*e2p*phip**2 + 0.5*e2p*Up(rho))*u \
              + (2.0*rhop - 0.5*Z*rho*e2p*phip)*up \
              + (-0.25*Z*e2p*phip**2 + 0.25*e2p*Upp(rho))*v + (2.0*phip)*vp
        return [up, dpp, vp, drr]
    def rhs_a(r, Y):
        base = rhs_hom(r, Y)
        phi, phip, rho, rhop = sol(r)
        e2p = np.exp(2.0*phi)
        # dU'/da = -(rho^2-1) U'(rho) - 2 rho U(rho)
        dUp_da = -(rho*rho - 1.0)*Up(rho) - 2.0*rho*U(rho)
        base[3] += 0.25*e2p*dUp_da
        return base
    return rhs_hom, rhs_a

def integrate_jacobi(bg, kind, rtol=1e-10, atol=1e-12, ledger=None):
    """kind='phic': Y(0)=(1,0,0,0) homogeneous; kind='a': Y(0)=0 with d/da inhomogeneity.
    Dense output for later node sampling. Linear ODE off cached background (not a shot)."""
    from scipy.integrate import solve_ivp
    rhs_hom, rhs_a = jac_rhs_factory(bg)
    f = rhs_hom if kind == 'phic' else rhs_a
    Y0 = [1.0, 0.0, 0.0, 0.0] if kind == 'phic' else [0.0, 0.0, 0.0, 0.0]
    out = solve_ivp(f, (0.0, bg['r_s']), Y0, method='DOP853', rtol=rtol, atol=atol,
                    dense_output=True)
    if ledger is not None:
        ledger.append(dict(kind=f'jacobi_{kind}', tag=bg['tag'], rtol=rtol, atol=atol,
                           nfev=int(out.nfev), success=bool(out.success)))
    assert out.success
    return out

def dir_from_fields(ix, ufun_nodes, vfun_nodes, alpha, beta):
    d = np.zeros(ix['dim'])
    d[ix['iu']] = ufun_nodes[:ix['M']]
    d[ix['ib']] = beta
    d[ix['iv']] = vfun_nodes
    d[ix['ia']] = alpha
    return d

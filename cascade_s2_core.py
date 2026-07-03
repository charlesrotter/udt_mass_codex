"""s2_core.py -- STAGE 2 of the stability filter: labeled inertia decomposition per rung.

OBSERVE MODE. Per stability_filter_miniMAP.md + stability_operator_results.md (verified operator).
Assembly built on the blind verifier's scheme (cascade_bv13_matrices2.py, scheme 2), re-parametrized
for (Z, m, a); translation/continuum validation re-run here before any counts are used.

Conventions (pinned by the stage-1 theorem):
  - v0=0 convention: V^ and S_u defined with v-side = v_1..v_M (v0 consumed by the hyperbolic
    alpha-v0 pair in FREE/ANCHORED). FIXED has no alpha => no hyperbolic step: v0 is kept on the
    Schur KEPT side (exact Haynsworth), flagged; strict v0-deleted diagnostic also computed.
  - Counts are for the ACTION S (energy = -S swaps n_neg <-> n_pos)  [orientation flag, banked].
  - Mass normalization for eigenvalue magnitudes: lumped trapezoid, alpha/beta weight 1
    (CHOSE normalization, flagged; counts are normalization-independent).
NO stability language anywhere in outputs.
"""
import numpy as np, json, os, sys, time, pickle
sys.path.insert(0, '/home/udt-admin/udt_mass_codex')
from cell_solver_universe_T3 import shoot, make_risefall_slice, PHI_C
from scipy.linalg import eigvalsh, eigh, solve, eigh_tridiagonal

SCRATCH = os.path.dirname(os.path.abspath(__file__))
REPO = '/home/udt-admin/udt_mass_codex'

# ---------------------------------------------------------------- rung registry (banked pins)
def load_registry():
    reg = {}
    sb = json.load(open(os.path.join(REPO, 'cascade_stageB_rungs.json')))['rungs']
    for r in sb:
        tag = f"B{r['N_delta']:02d}"
        reg[tag] = dict(tag=tag, side='below', N=r['N_delta'], m=3.0, Z=8.0, a=r['a_star'],
                        banked=dict(r_s=r['r_s'], rho_s=r['rho_s'], q=r['q']), banked_prec=6)
    # above-side rungs (banked by the Stage-B blind verifier; rho_s/q/L only, no banked r_s)
    ab = {8: dict(a=1.50587703866, rho_s=0.89250307, q=0.93400162, L=16.8576),
          9: dict(a=1.50556166549, rho_s=1.07964573, q=0.84816520, L=18.6192),
          10: dict(a=1.50526832529, rho_s=0.91264790, q=0.77386007, L=20.4068),
          11: dict(a=1.50501146174, rho_s=1.06742396, q=0.71309209, L=22.1817)}
    for N, d in ab.items():
        tag = f"A{N:02d}"
        reg[tag] = dict(tag=tag, side='above', N=N, m=3.0, Z=8.0, a=d['a'],
                        banked=dict(rho_s=d['rho_s'], q=d['q'], L=d['L']), banked_prec=6)
    # twin fundamental (banked in twin_ladder_involution_results.md to 4-5 s.f. only -- flagged)
    reg['A00'] = dict(tag='A00', side='above', N=0, m=3.0, Z=8.0, a=1.5099953390,
                      banked=dict(rho_s=0.6190, q=2.2091, L=3.771, r_s=817.5), banked_prec=4)
    # spot rungs (stageC banked, full precision)
    c1 = json.load(open(os.path.join(REPO, 'cascade_stageC_c1_A1m2_Z8.json')))['rungs'][0]
    reg['SM2'] = dict(tag='SM2', side='spot_m2Z8', N=0, m=2.0, Z=8.0, a=c1['p_star'],
                      banked=dict(r_s=c1['r_s'], rho_s=c1['rho_s'], q=c1['q']), banked_prec=6)
    c2 = json.load(open(os.path.join(REPO, 'cascade_stageC_c2_A1m3_Z1.json')))['rungs'][0]
    reg['SZ1'] = dict(tag='SZ1', side='spot_m3Z1', N=0, m=3.0, Z=1.0, a=c2['p_star'],
                      banked=dict(r_s=c2['r_s'], rho_s=c2['rho_s'], q=c2['q']), banked_prec=6)
    return reg

def makeUfns(a, m):
    def U(rho):  return 2.0*rho**m*np.exp(-a*(rho*rho-1.0))
    def Up(rho): return U(rho)*(m/rho - 2.0*a*rho)
    def Upp(rho):return Up(rho)*(m/rho - 2.0*a*rho) + U(rho)*(-m/rho**2 - 2.0*a)
    return U, Up, Upp

# ---------------------------------------------------------------- backgrounds (1 IVP shot, cached)
SHOT_LOG = os.path.join(SCRATCH, 's2_shot_log.json')

def _log_shot(tag):
    log = json.load(open(SHOT_LOG)) if os.path.exists(SHOT_LOG) else []
    log.append(dict(tag=tag, t=time.strftime('%Y-%m-%d %H:%M:%S')))
    json.dump(log, open(SHOT_LOG, 'w'), indent=1)

def get_background(rr):
    """rr = registry entry. Returns bg dict; shoots once and caches (pickle)."""
    pkl = os.path.join(SCRATCH, f"s2_bg_{rr['tag']}.pkl")
    if os.path.exists(pkl):
        return pickle.load(open(pkl, 'rb'))
    U, Up, lab = make_risefall_slice(rr['a'], m=rr['m'])
    _log_shot(rr['tag'])
    o = shoot(rr['Z'], U, Up, 1.0)
    if o['status'] != 'seal':
        bg = dict(status=o['status'], tag=rr['tag'])
        pickle.dump(bg, open(pkl, 'wb')); return bg
    r_s = o['r_s']
    phi_s, phip_s, rho_s, rhop_s = o['sol'].y_events[0][0]
    rrn = np.linspace(0.0, r_s, 200001)
    phi_l = o['sol'].sol(rrn)[0]
    L = float(np.trapezoid(np.exp(phi_l), rrn))
    _, Upf, Uppf = makeUfns(rr['a'], rr['m'])
    bg = dict(status='seal', tag=rr['tag'], a=rr['a'], m=rr['m'], Z=rr['Z'],
              sol=o['sol'], r_s=float(r_s), rho_s=float(rho_s), rhop_s=float(rhop_s),
              phip_s=float(phip_s), q=float(o['q']), H_seal=float(o['H_seal']), L=L,
              Up_c=float(Upf(1.0)), Lrho_s=float(rr['Z']*rho_s*phip_s**2 - Upf(rho_s)))
    pickle.dump(bg, open(pkl, 'wb'))
    return bg

def reproduction_check(rr, bg):
    """Compare measured (r_s, rho_s, q, L) to banked pins at banked precision."""
    out = {}
    tol_pass = 5e-7 if rr['banked_prec'] >= 6 else 5e-4
    tol_marg = 10*tol_pass
    worst = 0.0
    for k, bv in rr['banked'].items():
        mv = bg[k]
        rel = abs(mv - bv)/abs(bv)
        out[k] = dict(banked=bv, measured=float(mv), rel=float(rel))
        worst = max(worst, rel)
    out['verdict'] = ('PASS' if worst < tol_pass else
                      'MARGINAL' if worst < tol_marg else 'FAIL')
    out['worst_rel'] = float(worst); out['tol_pass'] = tol_pass
    return out

# ---------------------------------------------------------------- grids
def rung_M(bg):
    """M >= 800 and >= 40 points per oscillation wavelength lam = 2*pi*e^{-phi}/sqrt|s1| near
    the seal (phi(seal)=0 => e^{-phi}=1). |s1| = m - dt - 2 dt^2, dt = U'(rho_c)/4."""
    dt = bg['Up_c']/4.0
    s1 = bg['m'] - dt - 2.0*dt*dt
    lam = 2.0*np.pi/np.sqrt(s1)
    Mmin = max(800, int(np.ceil(40.0*bg['r_s']/lam)))
    M = 800*int(np.ceil(Mmin/800.0))
    return M, float(lam), float(s1)

# ---------------------------------------------------------------- element data
def element_data(bg, M):
    h = bg['r_s']/M
    rm = (np.arange(M) + 0.5)*h
    rn = np.arange(M+1)*h
    phi_m, phip_m, rho_m, rhop_m = bg['sol'].sol(rm)
    phi_n, phip_n, rho_n, rhop_n = bg['sol'].sol(rn)
    _, Upf, Uppf = makeUfns(bg['a'], bg['m'])
    Z = bg['Z']
    em2p = np.exp(-2.0*phi_m)
    C = dict(h=h,
             cku=0.5*Z*rho_m**2, ckv=-2.0*em2p, cc1=2.0*Z*rho_m*phip_m,
             cc2=8.0*em2p*rhop_m, cmu=-4.0*em2p*rhop_m**2,
             cmv=0.5*Z*phip_m**2 - 0.5*Uppf(rho_m),
             phip_n=phip_n, rhop_n=rhop_n)
    return C

def local_K(C):
    """(M,4,4) local element matrices over [uL,uR,vL,vR]."""
    M = len(C['cku']); h = C['h']
    du = np.array([-1.0, 1.0, 0.0, 0.0]); ub = np.array([0.5, 0.5, 0.0, 0.0])
    dv = np.array([0.0, 0.0, -1.0, 1.0]); vb = np.array([0.0, 0.0, 0.5, 0.5])
    O = lambda x, y: np.outer(x, y)
    B1 = O(du, du); B2 = O(dv, dv); B3 = 0.5*(O(du, vb) + O(vb, du))
    B4 = 0.5*(O(ub, dv) + O(dv, ub)); B5 = O(ub, ub); B6 = O(vb, vb)
    K = (C['cku'][:, None, None]/h*B1 + C['ckv'][:, None, None]/h*B2
         + C['cc1'][:, None, None]*B3 + C['cc2'][:, None, None]*B4
         + C['cmu'][:, None, None]*h*B5 + C['cmv'][:, None, None]*h*B6)
    return K

Lidx = [0, 2]; Ridx = [1, 3]   # (uL,vL), (uR,vR)

def build_blocks(bg, M, column):
    """Block-tridiagonal form. Blocks: 0 (core, incl alpha for FREE/ANCHORED), 1..M-1 = [u_j,v_j],
    M = [beta, v_M] (FREE/ANCHORED) or [v_M] (FIXED). Returns D(list), E(list, E[j] couples j-1->j),
    layout dict."""
    C = element_data(bg, M)
    K = local_K(C)
    h = C['h']; wbeta = -bg['phip_s']
    KLL = K[:, Lidx][:, :, Lidx]; KRR = K[:, Ridx][:, :, Ridx]; KLR = K[:, Lidx][:, :, Ridx]
    D = [None]*(M+1); E = [None]*(M+1)
    # middle blocks
    for j in range(1, M):
        D[j] = KRR[j-1] + KLL[j]
        if j >= 2:
            E[j] = KLR[j-1]
    # block 0
    if column == 'FREE':
        D0 = np.zeros((3, 3)); D0[1:, 1:] = KLL[0]
        D0[0, 2] += 0.5*bg['Up_c']; D0[2, 0] += 0.5*bg['Up_c']
        E1 = np.zeros((3, 2)); E1[1:, :] = KLR[0]
        lay0 = dict(size=3, alpha=0, u0=1, v0=2)
    elif column == 'ANCHORED':
        D0 = np.zeros((2, 2)); D0[1, 1] = KLL[0][1, 1]
        D0[0, 1] += 0.5*bg['Up_c']; D0[1, 0] += 0.5*bg['Up_c']
        E1 = np.zeros((2, 2)); E1[1, :] = KLR[0][1, :]
        lay0 = dict(size=2, alpha=0, u0=None, v0=1)
    elif column == 'FIXED':
        D0 = KLL[0].copy()
        E1 = KLR[0].copy()
        lay0 = dict(size=2, alpha=None, u0=0, v0=1)
    D[0] = D0; E[1] = E1
    # block M
    if column in ('FREE', 'ANCHORED'):
        S = np.diag([wbeta, 1.0])
        DM = S @ KRR[M-1] @ S
        DM[0, 1] += 0.5*bg['Lrho_s']; DM[1, 0] += 0.5*bg['Lrho_s']
        EM = KLR[M-1] @ S
        layM = dict(size=2, beta=0, vM=1)
    else:
        DM = KRR[M-1][1:, 1:].copy()          # v_M only (u_M = 0)
        EM = KLR[M-1][:, 1:].copy()
        layM = dict(size=1, beta=None, vM=0)
    D[M] = DM; E[M] = EM
    layout = dict(column=column, M=M, h=h, lay0=lay0, layM=layM, wbeta=wbeta)
    return D, E, layout, C

def trans_border(bg, layout, C, weighted=True):
    """Translation direction t (per block) and mass-weighted border c = W t.
    t: u_k=-phi'(r_k), beta=1, v_k=-rho'(r_k), alpha=1. W: trapezoid nodes; alpha,beta weight 1."""
    M = layout['M']; h = layout['h']
    phip_n = C['phip_n']; rhop_n = C['rhop_n']
    w = np.full(M+1, h); w[0] = h/2; w[-1] = h/2
    tb = [None]*(M+1); wb = [None]*(M+1)
    l0 = layout['lay0']
    t0 = np.zeros(l0['size']); w0 = np.zeros(l0['size'])
    if l0['alpha'] is not None: t0[l0['alpha']] = 1.0; w0[l0['alpha']] = 1.0
    if l0['u0'] is not None:    t0[l0['u0']] = -phip_n[0]; w0[l0['u0']] = w[0]
    t0[l0['v0']] = -rhop_n[0];  w0[l0['v0']] = w[0]
    tb[0] = t0; wb[0] = w0
    for j in range(1, M):
        tb[j] = np.array([-phip_n[j], -rhop_n[j]])
        wb[j] = np.array([w[j], w[j]])
    lM = layout['layM']
    if lM['beta'] is not None:
        tb[M] = np.array([1.0, -rhop_n[M]]); wb[M] = np.array([1.0, w[M]])
    else:
        tb[M] = np.array([-rhop_n[M]]); wb[M] = np.array([w[M]])
    cb = [t*wv for t, wv in zip(tb, wb)] if weighted else [t.copy() for t in tb]
    return tb, wb, cb

# ---------------------------------------------------------------- O(M) inertia machinery
def block_inertia(D, E, border=None, shift_diag=None):
    """Exact inertia of the block-tridiagonal symmetric matrix by block LDL^T.
    border: optional list of per-block vectors c_j -> also returns inertia of the bordered
    matrix K=[[Q,c],[c^T,0]] (deflated count = n_neg(K)-1). shift_diag: optional per-block
    diagonal weight lists W_j and scalar sigma -> counts for Q - sigma*W."""
    NB = len(D)
    nneg = npos = nzero = 0
    flags = []
    scale = max(float(np.max(np.abs(Dj))) for Dj in D if Dj is not None and Dj.size)
    Dcur = D[0].copy()
    if shift_diag is not None:
        Wl, sig = shift_diag
        Dcur = Dcur - sig*np.diag(Wl[0])
    if border is not None:
        c = border[0].copy(); s_b = 0.0
    for j in range(NB):
        wev = np.linalg.eigvalsh(Dcur)
        tol = 1e-13*scale
        nneg += int((wev < -tol).sum()); npos += int((wev > tol).sum())
        nz = int((np.abs(wev) <= tol).sum())
        if nz:
            nzero += nz
            flags.append(dict(kind='near-singular-pivot', block=j,
                              minabs=float(np.min(np.abs(wev)))))
        elif float(np.min(np.abs(wev))) < 1e-9*scale:
            flags.append(dict(kind='soft-pivot', block=j, minabs=float(np.min(np.abs(wev)))))
        if j < NB - 1:
            Enext = E[j+1]
            X = np.linalg.solve(Dcur, Enext)
            Dn = D[j+1] - Enext.T @ X
            if shift_diag is not None:
                Dn = Dn - sig*np.diag(Wl[j+1])
            if border is not None:
                y = np.linalg.solve(Dcur, c)
                s_b -= float(c @ y)
                c = border[j+1] - Enext.T @ y
            Dcur = Dn
        elif border is not None:
            y = np.linalg.solve(Dcur, c)
            s_b -= float(c @ y)
    out = dict(nneg=nneg, npos=npos, nzero=nzero, flags=flags)
    if border is not None:
        out['border_s'] = s_b
        nnegK = nneg + (1 if s_b < 0 else 0) + nzero*0
        out['nneg_deflated'] = nnegK - 1     # In(K) = In(Q|c-perp) + (1,1)
        out['lam_t_sign'] = int(np.sign(nneg - out['nneg_deflated'])) if True else 0
    return out

def vhat_tridiag_arrays(C, M):
    """V^ in the v0=0 convention: nodes v_1..v_M, tridiagonal (d, e)."""
    h = C['h']
    ckv = C['ckv']; cmv = C['cmv']
    n = M + 1
    d = np.zeros(n); e = np.zeros(n-1)
    d[:-1] += ckv/h + cmv*h/4.0
    d[1:]  += ckv/h + cmv*h/4.0
    e[:]   += -ckv/h + cmv*h/4.0
    return d[1:], e[1:]

def sturm_counts(d, e, shift=0.0):
    n = len(d); nneg = 0; nzero = 0
    piv = d[0] - shift
    if piv < 0: nneg += 1
    if piv == 0: nzero += 1; piv = 1e-300
    for i in range(1, n):
        piv = (d[i] - shift) - e[i-1]**2/piv
        if piv < 0: nneg += 1
        elif piv == 0: nzero += 1; piv = 1e-300
    return nneg, n - nneg - nzero, nzero

def vhat_nearest_eig(d, e):
    """Smallest-|lambda| eigenvalue of tridiagonal V^ (near-singular-V^ monitor)."""
    scale = float(np.max(np.abs(d)) + np.max(np.abs(e)))
    for dlt in np.geomspace(1e-12*scale, scale, 40):
        try:
            w = eigh_tridiagonal(d, e, select='v', select_range=(-dlt, dlt),
                                 eigvals_only=True)
        except Exception:
            continue
        if len(w):
            return float(w[np.argmin(np.abs(w))])
    return None

# ---------------------------------------------------------------- dense route
def blocks_to_dense(D, E, layout):
    M = layout['M']
    sizes = [D[j].shape[0] for j in range(M+1)]
    offs = np.concatenate([[0], np.cumsum(sizes)])
    dim = offs[-1]
    Q = np.zeros((dim, dim))
    for j in range(M+1):
        o = offs[j]; s = sizes[j]
        Q[o:o+s, o:o+s] += D[j]
        if j >= 1:
            op = offs[j-1]; sp = sizes[j-1]
            Q[op:op+sp, o:o+s] += E[j]
            Q[o:o+s, op:op+sp] += E[j].T
    return Q, offs, sizes

def dense_indices(layout, offs):
    """Global dense indices for: alpha, u-list(u_0..u_{M-1}), beta, v-list(v_0..v_M)."""
    M = layout['M']; l0 = layout['lay0']; lM = layout['layM']
    ia = offs[0] + l0['alpha'] if l0['alpha'] is not None else None
    iu = []
    if l0['u0'] is not None: iu.append(offs[0] + l0['u0'])
    iu += [offs[j] + 0 for j in range(1, M)]
    ib = offs[M] + lM['beta'] if lM['beta'] is not None else None
    iv = [offs[0] + l0['v0']] + [offs[j] + 1 for j in range(1, M)] + [offs[M] + lM['vM']]
    return ia, iu, ib, iv

def inertia_eigs(w, tolfac=1e-10):
    tol = tolfac*np.max(np.abs(w))
    return (int((w < -tol).sum()), int((w > tol).sum()), int((np.abs(w) <= tol).sum()))

def inertia_scaled(Q, tolfac=1e-10):
    """bv13's validated inertia tool: symmetric diagonal pre-scaling (equilibrates the e^{2|phi_c|}
    dynamic range so tiny-eigenvalue signs are reliable), then relative-tolerance count."""
    d = np.sqrt(np.abs(np.diag(Q))); d[d == 0] = 1.0
    Qs = Q/np.outer(d, d)
    w = eigvalsh(Qs)
    return inertia_eigs(w, tolfac)

def cperp_basis(c):
    """Orthonormal basis of the c-perp subspace via one Householder reflector."""
    n = len(c)
    w = c.astype(float).copy()
    w[0] += np.sign(c[0] if c[0] != 0 else 1.0)*np.linalg.norm(c)
    w /= np.linalg.norm(w)
    H = np.eye(n) - 2.0*np.outer(w, w)
    return H[:, 1:]

def dense_analysis(bg, M, column):
    """Full dense deliverables at moderate M: counts, identities, S_u/V^ direct, lowest eigs."""
    t0 = time.time()
    D, E, layout, C = build_blocks(bg, M, column)
    Q, offs, sizes = blocks_to_dense(D, E, layout)
    ia, iu, ib, iv = dense_indices(layout, offs)
    dim = Q.shape[0]
    tb, wb, cb = trans_border(bg, layout, C)
    tvec = np.concatenate(tb); wvec = np.concatenate(wb)
    out = dict(M=M, column=column, dim=int(dim))
    # scaled (generalized w/ lumped mass) spectrum
    s = 1.0/np.sqrt(wvec)
    Qs = Q*np.outer(s, s)
    w_all = eigvalsh(Qs)
    out['inertia_full'] = inertia_eigs(w_all)
    near = w_all[np.argsort(np.abs(w_all))[:5]]
    out['near0_full'] = sorted([float(x) for x in near], key=abs)
    # translation data (FREE/ANCHORED)
    if column in ('FREE', 'ANCHORED'):
        tt = tvec/s   # = W^{1/2} t
        rq = float(tt @ Qs @ tt)/float(tt @ tt)
        res = Qs @ tt - rq*tt
        out['translation_RQ'] = rq
        out['translation_relres'] = float(np.linalg.norm(res)/np.linalg.norm(Qs @ tt + 1e-300))
        # identify translation eigenvalue by EIGENVECTOR OVERLAP with t (not RQ proximity:
        # coupling can shift the resolved eigenvalue far from the diagonal RQ expectation)
        cand = np.argsort(np.abs(w_all))[:8]
        i0, i1 = int(cand.min()), int(cand.max())
        wv_sub, vec_sub = eigh(Qs, subset_by_index=(i0, i1))
        tn = tt/np.linalg.norm(tt)
        ovl = np.abs(vec_sub.T @ tn)
        j_t = int(np.argmax(ovl))
        out['translation_eig'] = float(wv_sub[j_t])
        out['translation_overlap'] = float(ovl[j_t])
        i_t = i0 + j_t
        w_defl = np.delete(w_all, i_t)
        out['near0_beyond_translation'] = sorted(
            [float(x) for x in w_defl[np.argsort(np.abs(w_defl))[:3]]], key=abs)
        # EXACT projection deflation (constrain to (Wt)-perp; count invariant under congruence)
        cvec = np.concatenate(cb)
        P = cperp_basis(cvec)
        out['inertia_full_deflated'] = inertia_scaled(P.T @ Q @ P)
        # bordered cross-check (validates the big-M deflation machinery)
        bi = block_inertia(D, E, border=cb)
        out['block_nneg'] = bi['nneg']; out['block_nzero'] = bi['nzero']
        out['block_nneg_deflated'] = bi['nneg_deflated']
        out['block_flags'] = bi['flags']
    else:
        bi = block_inertia(D, E)
        out['block_nneg'] = bi['nneg']; out['block_nzero'] = bi['nzero']
        out['block_flags'] = bi['flags']
    # ---- splits (counts via bv13's diagonal-scaled inertia; congruence-invariant)
    vs = iv[1:]                                    # v_1..v_M  (v0=0 convention)
    if column in ('FREE', 'ANCHORED'):
        us = iu + [ib]
        qhat_idx = [i for i in range(dim) if i != ia and i != iv[0]]
    else:
        us = iu + [iv[0]]                          # FIXED: v0 kept on Schur kept-side (flagged)
        qhat_idx = list(range(dim))
    out['inertia_full_raw'] = inertia_scaled(Q)
    Qhat = Q[np.ix_(qhat_idx, qhat_idx)]
    out['inertia_qhat'] = inertia_scaled(Qhat)
    V = Q[np.ix_(vs, vs)]
    A = Q[np.ix_(us, us)]; B = Q[np.ix_(us, vs)]
    # V^ tridiagonality assert (structure check)
    Voff = np.triu(np.abs(V), 2)
    out['V_tridiag_maxoff'] = float(Voff.max())
    wV = eigvalsh(V)
    out['inertia_V'] = inertia_scaled(V)
    out['V_min_abs_eig'] = float(wV[np.argmin(np.abs(wV))])
    S = A - B @ solve(V, B.T, assume_a='sym')
    wS = eigvalsh(S)
    out['inertia_Su'] = inertia_scaled(S)
    out['Su_low3'] = sorted([float(x) for x in wS[np.argsort(np.abs(wS))[:3]]], key=abs)
    # ---- identity checks (exact matrix theorems)
    nnegF = out['inertia_full_raw'][0]
    nnegH = out['inertia_qhat'][0]
    out['identity_haynsworth'] = bool(nnegH == out['inertia_V'][0] + out['inertia_Su'][0])
    if column in ('FREE', 'ANCHORED'):
        out['identity_hyperbolic'] = bool(nnegF == 1 + nnegH)
    else:
        out['identity_hyperbolic'] = None          # no alpha => no hyperbolic step
        # strict v0-deleted diagnostic for FIXED
        us2 = iu
        A2 = Q[np.ix_(us2, us2)]; B2 = Q[np.ix_(us2, vs)]
        S2 = A2 - B2 @ solve(V, B2.T, assume_a='sym')
        wS2 = eigvalsh(S2)
        out['inertia_Su_v0deleted'] = inertia_eigs(wS2)
    # pair in the pinned convention
    out['pair'] = (out['inertia_Su'][0], out['inertia_V'][1])
    # finite part (split-independent total minus M-proportional Weyl part)
    out['finite_part_nnegQ_minus_nnegV'] = int(nnegF - out['inertia_V'][0])
    # Sturm cross-check of V^ (independent construction)
    d, e = vhat_tridiag_arrays(C, M)
    st = sturm_counts(d, e)
    out['V_sturm'] = st
    out['V_sturm_match'] = bool((st[0], st[1]) == (out['inertia_V'][0], out['inertia_V'][1]))
    out['wall_s'] = round(time.time() - t0, 1)
    return out

def bigM_analysis(bg, M, column):
    """O(M) route at the resolution-required grid: block inertia (+deflation) + Sturm V^."""
    t0 = time.time()
    D, E, layout, C = build_blocks(bg, M, column)
    tb, wb, cb = trans_border(bg, layout, C)
    if column in ('FREE', 'ANCHORED'):
        bi = block_inertia(D, E, border=cb)
        nneg_defl = bi['nneg_deflated']
    else:
        bi = block_inertia(D, E)
        nneg_defl = None
    d, e = vhat_tridiag_arrays(C, M)
    nnegV, nposV, nzV = sturm_counts(d, e)
    vmin = vhat_nearest_eig(d, e)
    out = dict(M=M, column=column, nneg_Q=bi['nneg'], nzero_Q=bi['nzero'],
               block_flags=bi['flags'],
               nneg_V=nnegV, npos_V=nposV, nzero_V=nzV, V_min_abs_eig=vmin)
    if column in ('FREE', 'ANCHORED'):
        # PRIMARY pair = raw route via full form + identities (the banked pinned convention).
        # Deflation is a labeled DIAGNOSTIC: nneg_Q vs nneg_Q_deflated difference = the discrete
        # sign of the translation-resolved near-zero at this grid (the decomposition identity
        # does not commute with deflation; forcing it through would mislabel).
        out['nneg_Q_deflated'] = nneg_defl
        out['translation_resolved_negative'] = int(bi['nneg'] - nneg_defl)
        out['nneg_Su'] = bi['nneg'] - 1 - nnegV                # hyperbolic + Haynsworth
        out['pair'] = (out['nneg_Su'], nposV)
        # translation RQ at this grid (O(h^2) monitor, cheap element sum)
        h = layout['h']
        tvec_blocks = tb
        # Q t via block structure: (Qt)_j = D_j t_j + E_j^T t_{j-1} + E_{j+1} t_{j+1}
        num = 0.0; den = 0.0
        Mn = layout['M']
        for j in range(Mn+1):
            Qt_j = D[j] @ tb[j]
            if j >= 1: Qt_j += E[j].T @ tb[j-1]
            if j < Mn: Qt_j += E[j+1] @ tb[j+1]
            num += float(tb[j] @ Qt_j)
            den += float(tb[j] @ (wb[j]*tb[j]))
        out['translation_RQ'] = num/den
    else:
        out['nneg_Su_haynsworth'] = bi['nneg'] - nnegV
        out['pair'] = (out['nneg_Su_haynsworth'], nposV)
    out['finite_part_nnegQ_minus_nnegV'] = int(bi['nneg'] - nnegV)
    out['wall_s'] = round(time.time() - t0, 1)
    return out

# ---------------------------------------------------------------- per-rung driver
def run_rung(tag, reg=None):
    reg = reg or load_registry()
    rr = reg[tag]
    ck = os.path.join(SCRATCH, f"s2_rung_{tag}.json")
    res = json.load(open(ck)) if os.path.exists(ck) else {}
    bg = get_background(rr)
    if bg['status'] != 'seal':
        res.update(tag=tag, status=bg['status'], SKIPPED=True)
        json.dump(res, open(ck, 'w'), indent=1, default=str); return res
    rep = reproduction_check(rr, bg)
    Mrung, lam, s1 = rung_M(bg)
    res.update(tag=tag, side=rr['side'], N=rr['N'], m=rr['m'], Z=rr['Z'], a=rr['a'],
               status='seal', reproduction=rep,
               r_s=bg['r_s'], rho_s=bg['rho_s'], q=bg['q'], L=bg['L'],
               Up_c=bg['Up_c'], Lrho_s=bg['Lrho_s'], phip_s=bg['phip_s'],
               H_seal=bg['H_seal'], rhop_s=bg['rhop_s'],
               M_rung=Mrung, lam_seal=lam, s1_abs=s1)
    if rep['verdict'] == 'FAIL':
        res['SKIPPED'] = True
        json.dump(res, open(ck, 'w'), indent=1, default=str); return res
    res.setdefault('dense', {}); res.setdefault('bigM', {})
    for col in ('FREE', 'ANCHORED', 'FIXED'):
        for M in (800, 1600):
            key = f"{col}/M{M}"
            if key not in res['dense']:
                res['dense'][key] = dense_analysis(bg, M, col)
                json.dump(res, open(ck, 'w'), indent=1, default=str)
        for M in (Mrung, 2*Mrung):
            key = f"{col}/M{M}"
            if key not in res['bigM']:
                res['bigM'][key] = bigM_analysis(bg, M, col)
                json.dump(res, open(ck, 'w'), indent=1, default=str)
    # grid-stability of the pinned pair
    stab = {}
    for col in ('FREE', 'ANCHORED', 'FIXED'):
        p1 = tuple(res['bigM'][f"{col}/M{Mrung}"]['pair'])
        p2 = tuple(res['bigM'][f"{col}/M{2*Mrung}"]['pair'])
        stab[col] = dict(pair_M=list(p1), pair_2M=list(p2), grid_stable=bool(p1 == p2))
    res['pair_stability'] = stab
    json.dump(res, open(ck, 'w'), indent=1, default=str)
    return res

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'rung':
        r = run_rung(sys.argv[2])
        ps = r.get('pair_stability', {})
        print(json.dumps(dict(tag=r['tag'], reproduction=r.get('reproduction', {}).get('verdict'),
                              M_rung=r.get('M_rung'), pairs={k: v['pair_M'] for k, v in ps.items()},
                              stable={k: v['grid_stable'] for k, v in ps.items()}), default=str))
    elif cmd == 'shoot_only':
        reg = load_registry()
        rr = reg[sys.argv[2]]
        bg = get_background(rr)
        if bg['status'] == 'seal':
            print(sys.argv[2], bg['status'],
                  f"r_s={bg['r_s']:.6f} rho_s={bg['rho_s']:.8f} q={bg['q']:.8f} L={bg['L']:.5f}",
                  json.dumps(reproduction_check(rr, bg)))
        else:
            print(sys.argv[2], bg['status'])

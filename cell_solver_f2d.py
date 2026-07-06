"""cell_solver_f2d.py -- the 2-D finite-mirror cell solver: coupled (phi(r), rho(r), f(r,theta)).

GENERALIZES cell_solver_round.py (1-D phi,rho) by adding the winding matter field f(r,theta).
DERIVED native frame; interior Branch P (W=1); matter is phi-BLIND (undilated radial channel).
BINDING RULE (discreteness_preregistration.md): solve the SPACE, not "the electron". Output
UNLABELED. This module is CODE CONSTRUCTION + a BOUNDED smoke test only -- it does NOT run the
closure-manifold scan (that is a separate, gated run).

Pre-registration / frozen contract: discreteness_preregistration.md (Class A FREE, H=0 build;
AMENDMENT 2026-07-01b). Foundation: f_rtheta_free_field_MAP.md (the exact system, sec.2/sec.9),
f2d_virial_step0_results.md (the H=0 closure + Derrick diagnostic, BLIND-VERIFIED),
round_matter_reduction_results.md (the reduced matter Lagrangian + theta-moments + f-PDE).

================================ THE EXACT SYSTEM ================================
Domain r in [r_c, r_s], theta in [0, pi]. Fields phi(r), rho(r), f(r,theta). Winding degree N.

Geometry (interior P; matter phi-blind, no direct matter source in the phi-EOM):
    phi'' = 4 e^{-2phi} rho'^2 /(Z rho^2)  -  2 phi' rho'/rho
    rho'' = 2 phi' rho'  -  (Z/4) rho e^{2phi} phi'^2  +  (e^{2phi}/4)( xi rho I_r  -  kap N^2 I_4th/rho^3 )
theta-moments of f:
    I_r  (r) = 1/2 INT sin(th) f_r^2 dth
    I_4th(r) = 1/2 INT (sin^2 f / sin th) f_th^2 dth

Matter f-PDE (elliptic, 2-D):
    d_r(A f_r) + d_th(B f_th)  -  (N^2 sin f cos f / sin th)( xi + kap f_r^2 + kap f_th^2/rho^2 ) = 0
    A = xi rho^2 sin th + kap N^2 sin^2 f / sin th ,   B = xi sin th + kap N^2 sin^2 f /(rho^2 sin th)

Boundary conditions:
    poles:  f(r,0)=0, f(r,pi)=pi                            (regularity + degree N; carried by the
                                                             theta background -- see DISCRETIZATION)
    MIRROR ends (BOTH r_c and r_s):  phi'=0, rho'=0, f_r=0  (smooth mirror fold, Class A)
    closure: H(r) == 0  (Step-0 free-boundary transversality; the third scalar condition making the
             closed cell SQUARE: 3 conditions phi'_s=0, rho'_s=0, H=0 vs 3 unknowns phi_c, rho_c, L).
Unknowns: phi_c, rho_c, and the cell LENGTH L = r_s - r_c (r_c fixed as a length reference; the EOMs
are autonomous in r, so only L is physical -- this is why H is conserved and H=0 closes the count).

Conserved radial Hamiltonian (Step-0 V4/V5; monitored + used as the closure row at the seal):
    H(r) = (Z/2)rho^2 phi'^2 - 2 e^{-2phi} rho'^2 - 2
           - (xi/2)rho^2 I_r + (xi/2)(I_th + N^2 I_s) - (kap N^2/2) I_4r + (kap N^2/2) I_4th/rho^2
    (at a mirror point phi'=rho'=f_r=0 -> H = -Lbar = -[2 - (xi/2)(I_th+N^2 I_s) - (kap N^2/2)I_4th/rho^2].)

Derrick integral identity (Step-0 V6; per-solution consistency diagnostic, not a closure):
    S_a := INT[ (Z/2)rho^2 phi'^2 + 2 - 2 e^{-2phi}rho'^2 - (xi/2)(rho^2 I_r + I_th + N^2 I_s) ] dr
    S_b := -(kap N^2/2) INT ( I_4r + I_4th/rho^2 ) dr ,    Derrick: S_a == S_b on any solution.

============================= DISCRETIZATION (method mined from the parts bin) =============================
* Angular: SH-EXACT d/dtheta (method of spectral_sph_exact.py) -- for the AXISYMMETRIC f (m=0 sector)
  the SH-exact operator is the associated-Legendre-of-order-0 = ordinary-Legendre(mu) operator:
      Dth = dSth @ inv(S),  S[i,j]=P_j(mu_i),  dSth[i,j] = -sin(th_i) P_j'(mu_i)  (analytic dP/dth).
  GL-mu interior nodes (never hit the poles) -> the 1/sin(th) factors are evaluated only at interior
  nodes, and theta-integrals map to the GL weights: INT g(th) sin(th) dth = sum_j w_j g_j, and
  INT g(th)/sin(th) dth = sum_j w_j g_j /(1-mu_j^2). NAIVE GL-mu mis-differentiation is avoided by
  using the Legendre-basis operator (exact for band-limited fields; the sin^|m| gotcha).
* MATTER UNKNOWN is the DEVIATION u(r,theta) = f - theta (f = theta + u). The rigid hedgehog f=theta
  is then u=0 (represented EXACTLY: the poles/degree are carried by the theta ramp background, not by
  differentiating the non-band-limited f=theta), and the f-PDE divergences are assembled in EXPANDED
  form (coefficient theta/r-derivatives A_r, B_th taken ANALYTICALLY; only u_r,u_rr,u_th,u_thth come
  from the operators). Consequence: the rigid residual is EXACTLY xi(1-N^2)cos(th) at every node (V1).
* Radial: Chebyshev collocation (method of spectral_cheb.py) on a FIXED reference zeta in [-1,1];
  physical r = r_c + (L/2)(zeta+1), so d/dr = (2/L) D_zeta with L a Newton unknown (free boundary).
* Nonlinear solve: monolithic residual [phi-ODE; rho-ODE; f-PDE; all BCs; H=0], solved by
  Levenberg-Marquardt (Nielsen gain-ratio damping = trust-region line search), Jacobian by torch
  autodiff (jacrev). NOT operator-split (the phi<->rho<->f coupling through e^{2phi} and the moments
  is stiff by construction). Method mined from newton_solve_p1 (p1_residual_general_einstein.py).
This is a FRESH module: it does NOT import the wrong-frame assembly (full3d_*, branch_operator, ...);
only the METHODS above are reproduced.

Provenance of the fixed parameters is tagged CHOSE/THEORY at the top of __main__.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import numpy as np
from numpy.polynomial import legendre as _leg
from scipy.special import roots_legendre
import torch
torch.set_default_dtype(torch.float64)

# N5d off-round transverse (shear) extension -- ADDITIVE; inactive unless n5d config is passed.
# The shear pieces (exact Kcal, sqrt_h, traceless E-row, off-round phi-source correction) live in
# the isolated, unit-tested n5d_shear.py (NO archived operator, e^{-2phi} EXACT).
import n5d_shear


# =========================================================================================
# GRID / OPERATOR CONSTRUCTION (reproduced methods, no imports of the parts-bin modules)
# =========================================================================================
def _cheb(Nr):
    """Chebyshev-Gauss-Lobatto nodes (ASCENDING on [-1,1]) + d/dzeta matrix (Trefethen cheb)."""
    n = Nr - 1
    if n == 0:
        return np.array([0.0]), np.array([[0.0]])
    x = np.cos(np.pi * np.arange(n + 1) / n)          # descending +1..-1
    cc = np.ones(n + 1); cc[0] = 2.0; cc[n] = 2.0
    cc *= (-1.0) ** np.arange(n + 1)
    X = np.tile(x, (n + 1, 1)).T
    dX = X - X.T
    D = np.outer(cc, 1.0 / cc) / (dX + np.eye(n + 1))
    D = D - np.diag(D.sum(axis=1))
    idx = np.arange(n, -1, -1)                        # flip to ascending zeta
    return x[idx], D[np.ix_(idx, idx)]


def _cc_weights(Nr):
    """Clenshaw-Curtis weights on the CGL nodes (ASCENDING), on [-1,1] (for the Derrick radial int)."""
    n = Nr - 1
    if n == 0:
        return np.array([2.0])
    theta = np.pi * np.arange(n + 1) / n
    w = np.zeros(n + 1)
    v = np.ones(n - 1)
    for k in range(1, n // 2 + 1):
        coef = (1.0 if 2 * k == n else 2.0) / (4.0 * k * k - 1.0)
        v -= coef * np.cos(2.0 * k * theta[1:n])
    w[1:n] = (2.0 / n) * v
    w[0] = 1.0 / (n * n - 1 + (n % 2)); w[n] = w[0]
    return w[::-1].copy()


def _sh_exact_dtheta(Nth):
    """SH-exact d/dtheta AND d2/dtheta2 on GL-mu nodes for the m=0 (axisymmetric) sector:
    associated-Legendre of order 0 = ordinary Legendre(mu). Returns theta (ASCENDING), mu, GL
    weights w, Dth, Dthth (each Nth x Nth), EXACT (machine precision) for any field band-limited in
    span{P_0..P_{Nth-1}}. NOTE: Dthth is built from the ANALYTIC d2P/dtheta2, NOT from Dth@Dth --
    composing Dth is inexact because dP/dtheta = -sin(th)dP/dmu carries an extra sin(th) and leaves
    the polynomial-in-mu space (the m=0 sin-theta gotcha, the second-derivative analog of the
    spectral_sph_exact winding gotcha).
      dP/dtheta   = -sin(th) P'(mu)
      d2P/dtheta2 = -cos(th) P'(mu) + sin^2(th) P''(mu)   [mu=cos th]"""
    mu, w = roots_legendre(Nth)                        # mu ascending in (-1,1)
    th = np.arccos(mu)                                 # descending; sort ascending in theta
    order = np.argsort(th)
    mu, w, th = mu[order], w[order], th[order]
    sth = np.sqrt(1.0 - mu ** 2); cth = mu
    S = np.zeros((Nth, Nth)); dSth = np.zeros((Nth, Nth)); dSthth = np.zeros((Nth, Nth))
    for j in range(Nth):
        ej = np.zeros(j + 1); ej[j] = 1.0              # P_j coefficients
        dej = _leg.legder(ej)                          # dP_j/dmu coefficients
        d2ej = _leg.legder(ej, 2)                      # d2P_j/dmu2 coefficients
        S[:, j] = _leg.legval(mu, ej)
        dSth[:, j] = -sth * _leg.legval(mu, dej)       # dP_j/dtheta          (analytic)
        dSthth[:, j] = -cth * _leg.legval(mu, dej) + sth ** 2 * _leg.legval(mu, d2ej)  # d2P/dtheta2
    Sinv = np.linalg.inv(S)
    return th, mu, w, dSth @ Sinv, dSthth @ Sinv


def make_ctx(Nr, Nth, rc=0.5, device="cpu"):
    """Precompute all constant operators/grids as torch tensors. rc = fixed radial length reference
    (CHOSE; the EOMs are autonomous in r so rc is a pure label, only L=r_s-rc is physical)."""
    zeta, Dz = _cheb(Nr)
    Dz2 = Dz @ Dz
    ccw = _cc_weights(Nr)
    th, mu, w, Dth, Dth2 = _sh_exact_dtheta(Nth)       # Dth2 = ANALYTIC d2/dtheta2 (not Dth@Dth)
    tt = lambda a: torch.as_tensor(np.asarray(a), dtype=torch.float64, device=device)
    return dict(
        Nr=Nr, Nth=Nth, rc=float(rc), device=device,
        zeta=tt(zeta), Dz=tt(Dz), Dz2=tt(Dz2), ccw=tt(ccw),
        th=tt(th), mu=tt(mu), w=tt(w),
        DthT=tt(Dth.T), Dth2T=tt(Dth2.T),
        s=tt(np.sin(th)), c=tt(np.cos(th)), s2=tt(1.0 - mu ** 2),   # s2 = sin^2 th = 1-mu^2
        P2=tt(0.5 * (3.0 * mu ** 2 - 1.0)),                        # Legendre P2(mu): the ell=2 shear mode
    )


# =========================================================================================
# PACK / UNPACK  --  base:  u_vec = [ phi(Nr), rho(Nr), u_field(Nr*Nth), L ]
#                   n5d :   u_vec = [ phi(Nr), rho(Nr), u_field(Nr*Nth), a2(Nr), L ]
# The a2(r) (ell=2 shear amplitude) block is INSERTED before L, so the base slices (phi, rho, uf, L)
# are byte-identical -- the extension is ADDITIVE (a2=None recovers the exact base layout).
# =========================================================================================
def pack(phi, rho, ufield, L, a2=None):
    parts = [phi.reshape(-1), rho.reshape(-1), ufield.reshape(-1)]
    if a2 is not None:
        parts.append(a2.reshape(-1))
    parts.append(torch.as_tensor([L], dtype=torch.float64, device=phi.device))
    return torch.cat(parts)


def unpack(v, ctx, n5d=None):
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    phi = v[:Nr]; rho = v[Nr:2 * Nr]
    uf = v[2 * Nr:2 * Nr + Nr * Nth].reshape(Nr, Nth)
    L = v[-1]
    if n5d is None:
        return phi, rho, uf, L
    a2 = v[2 * Nr + Nr * Nth:2 * Nr + Nr * Nth + Nr]        # the ell=2 shear amplitude a2(r)
    return phi, rho, uf, a2, L


# =========================================================================================
# FIELDS + DERIVATIVES + MOMENTS  (the single shared evaluator; torch, jacrev-safe)
# =========================================================================================
def fields(v, ctx, prm, n5d=None):
    """Return a dict of all node-level quantities used by the residual + diagnostics.

    n5d (dict or None): OFF-ROUND shear extension.  When None the base (round-trace) system is
    computed byte-for-byte unchanged.  When a dict, the ell=2 traceless shear a2(r) is live: the
    phi-ODE gains the exact off-round source correction +(1/(5Z))e^{-2phi}a2'^2 (n5d_shear), and
    the shear EL row + its BCs are added by residual().  With a2==0 every base row is identical."""
    Z, XI, KAP, N = prm
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    if n5d is None:
        phi, rho, uf, L = unpack(v, ctx)
    else:
        phi, rho, uf, a2, L = unpack(v, ctx, n5d=n5d)
    Dz, Dz2 = ctx["Dz"], ctx["Dz2"]
    DthT, Dth2T = ctx["DthT"], ctx["Dth2T"]
    s, c, s2, th = ctx["s"], ctx["c"], ctx["s2"], ctx["th"]
    sc = 2.0 / L                                        # d/dr = (2/L) d/dzeta

    # radial derivatives
    phip = sc * (Dz @ phi); phipp = sc * sc * (Dz2 @ phi)
    rhop = sc * (Dz @ rho); rhopp = sc * sc * (Dz2 @ rho)
    ur = sc * (Dz @ uf); urr = sc * sc * (Dz2 @ uf)     # (Nr,Nth)
    # angular derivatives of the DEVIATION u (f = theta + u  ->  f_th = 1 + u_th, f_thth = u_thth)
    uth = uf @ DthT; uthth = uf @ Dth2T

    f = th[None, :] + uf
    sf = torch.sin(f); cf = torch.cos(f); sf2 = sf * sf
    fr = ur; frr = urr
    fth = 1.0 + uth; fthth = uthth
    rho_c = rho[:, None]; rhop_c = rhop[:, None]
    s_r = s[None, :]; c_r = c[None, :]; s2_r = s2[None, :]

    # moments (GL-weight quadrature; INT()sin dth -> sum w, INT()/sin dth -> sum w/(1-mu^2))
    Ir = 0.5 * (ctx["w"][None, :] * fr ** 2).sum(1)
    Ith = 0.5 * (ctx["w"][None, :] * fth ** 2).sum(1)
    Is = 0.5 * (ctx["w"][None, :] * sf2 / s2_r).sum(1)
    I4th = 0.5 * (ctx["w"][None, :] * sf2 * fth ** 2 / s2_r).sum(1)
    I4r = 0.5 * (ctx["w"][None, :] * sf2 * fr ** 2 / s2_r).sum(1)

    # f-PDE coefficients + their EXACT (analytic) coefficient-derivatives (expanded divergence form)
    A = XI * rho_c ** 2 * s_r + KAP * N ** 2 * sf2 / s_r
    B = XI * s_r + KAP * N ** 2 * sf2 / (rho_c ** 2 * s_r)
    Ar = 2.0 * XI * rho_c * rhop_c * s_r + (2.0 * KAP * N ** 2 * sf * cf / s_r) * fr
    Bth = (XI * c_r - KAP * N ** 2 * sf2 * c_r / (rho_c ** 2 * s2_r)
           + (2.0 * KAP * N ** 2 * sf * cf / (rho_c ** 2 * s_r)) * fth)
    rdiv = Ar * fr + A * frr
    thdiv = Bth * fth + B * fthth
    pot = (N ** 2 * sf * cf / s_r) * (XI + KAP * fr ** 2 + KAP * fth ** 2 / rho_c ** 2)
    res_f = rdiv + thdiv - pot

    e2m = torch.exp(-2.0 * phi); e2p = torch.exp(2.0 * phi)
    phi_ode = phipp - (4.0 * e2m * rhop ** 2 / (Z * rho ** 2) - 2.0 * phip * rhop / rho)
    rho_ode = rhopp - (2.0 * phip * rhop - (Z / 4.0) * rho * e2p * phip ** 2
                       + (e2p / 4.0) * (XI * rho * Ir - KAP * N ** 2 * I4th / rho ** 3))

    out = dict(phi=phi, rho=rho, L=L, phip=phip, rhop=rhop, fr=fr,
               e2m=e2m, e2p=e2p, Ir=Ir, Ith=Ith, Is=Is, I4th=I4th, I4r=I4r,
               phi_ode=phi_ode, rho_ode=rho_ode, res_f=res_f)

    # ---------- N5d OFF-ROUND SHEAR (additive; a2==0 leaves every base row unchanged) ----------
    if n5d is not None:
        P2 = ctx["P2"]                                   # (Nth,)  Legendre P2(mu) : the ell=2 mode
        a2p = sc * (Dz @ a2); a2pp = sc * sc * (Dz2 @ a2)   # a2'(r), a2''(r)
        # reconstruct s(r,theta) = a2(r) P2(mu) and its radial derivatives on the grid
        s_field = a2[:, None] * P2[None, :]
        s_r = a2p[:, None] * P2[None, :]
        s_rr = a2pp[:, None] * P2[None, :]
        # traceless geometric E-row (pointwise; sin th supplied by the ell=2 quadrature), n5d_shear
        Es = n5d_shear.EAB_shear_row(rho[:, None], rhop[:, None], phip[:, None],
                                     s_field, s_r, s_rr, e2m=e2m[:, None])   # (Nr,Nth)
        # matter TRACELESS source T^{AB} (FROZEN profile; enters ONLY this h_AB shear row -- phi-BLIND,
        # no direct phi-source).  Two ways to supply it:
        #   n5d["src"]=(source_rc, source_sh2, amp): REGISTRATION B (native pullback) -- the frozen sh2(r)
        #     profile is interpolated LIVE at the CURRENT physical cell coordinate r(zeta)=rc+(L/2)(zeta+1)
        #     (current L, differentiable), NOT frozen at the seed L0.  No amplitude Jacobian (interp only).
        #   n5d["Tshear"]=array: legacy precomputed (Nr,Nth) source (used by tests / diagnostics that pass
        #     a fixed array); NOT L-tracking.  If both absent -> vacuum shear.
        # FRAME-FACTOR LEDGER (open, un-applied): the stored sh2 = <T_thth - T_phph>(l2) is an ORTHONORMAL-
        # frame stress component from the hopfion's flat lab frame.  Whether it equals the cell-frame T_s
        # in E_s + T_s = 0 as-is, or needs a rho^2 / e-based frame conversion, is UNRESOLVED and NOT
        # applied here (amplitude left unchanged; see n5d_source_normalization_audit ledger).
        Tshear = n5d.get("Tshear", None)
        src = n5d.get("src", None)
        if src is not None:
            src_rc, src_sh2, src_amp = src
            r_phys = ctx["rc"] + 0.5 * L * (ctx["zeta"] + 1.0)   # CURRENT L (registration B; differentiable)
            src2 = n5d_shear.source_interp(src_rc, src_sh2, r_phys)   # (Nr,) interp at current physical r
            Tshear = src_amp * src2[:, None] * P2[None, :]           # amp * sh2(r_cur) * P2(mu)
        if Tshear is not None:
            Es = Es + Tshear                              # E^{AB} = -T^{AB}  =>  E_s + T_s = 0
        # ell=2 Galerkin projection: R2(r) = sum_j w_j P2_j (Es[.,j])   (w_j = int dmu incl. sin th)
        shear_res = (ctx["w"][None, :] * P2[None, :] * Es).sum(1)          # (Nr,)
        # EXACT off-round correction to the phi-ODE residual: +(1/(5Z)) e^{-2phi} a2'^2 (vanishes at a2=0)
        phi_ode = phi_ode + n5d_shear.phi_source_offround_correction(rho, a2p, e2m, Z)
        out["phi_ode"] = phi_ode
        out.update(dict(a2=a2, a2p=a2p, a2pp=a2pp, s_field=s_field, s_r=s_r, s_rr=s_rr,
                        Es=Es, shear_res=shear_res))
    return out


def H_of_r(v, ctx, prm):
    """Conserved radial Hamiltonian H(r) at every radial node (should be ~constant on-shell; = 0
    for a closed Class-A cell). Diagnostic + the closure row (at the seal)."""
    Z, XI, KAP, N = prm
    Q = fields(v, ctx, prm)
    rho, phip, rhop, e2m = Q["rho"], Q["phip"], Q["rhop"], Q["e2m"]
    Ir, Ith, Is, I4th, I4r = Q["Ir"], Q["Ith"], Q["Is"], Q["I4th"], Q["I4r"]
    return ((Z / 2.0) * rho ** 2 * phip ** 2 - 2.0 * e2m * rhop ** 2 - 2.0
            - (XI / 2.0) * rho ** 2 * Ir + (XI / 2.0) * (Ith + N ** 2 * Is)
            - (KAP * N ** 2 / 2.0) * I4r + (KAP * N ** 2 / 2.0) * I4th / rho ** 2)


def derrick(v, ctx, prm):
    """Derrick integral identity diagnostic: returns (S_a, S_b, S_a - S_b). Radial integral by
    Clenshaw-Curtis (scaled by L/2). On a true solution S_a == S_b."""
    Z, XI, KAP, N = prm
    Q = fields(v, ctx, prm)
    rho, phip, rhop, e2m = Q["rho"], Q["phip"], Q["rhop"], Q["e2m"]
    Ir, Ith, Is, I4th, I4r = Q["Ir"], Q["Ith"], Q["Is"], Q["I4th"], Q["I4r"]
    dens_a = ((Z / 2.0) * rho ** 2 * phip ** 2 + 2.0 - 2.0 * e2m * rhop ** 2
              - (XI / 2.0) * (rho ** 2 * Ir + Ith + N ** 2 * Is))
    dens_b = -(KAP * N ** 2 / 2.0) * (I4r + I4th / rho ** 2)
    jac = Q["L"] / 2.0                                  # dr = (L/2) dzeta
    Sa = (ctx["ccw"] * dens_a).sum() * jac
    Sb = (ctx["ccw"] * dens_b).sum() * jac
    return float(Sa), float(Sb), float(Sa - Sb)


# =========================================================================================
# READOUTS  --  public charge / MS-mass (NEUTRAL SIGN CONVENTION; §5, Charles-edited 2026-07-06)
# =========================================================================================
# sign_convention: pinned ONCE from the current whole-cell canon (N5b/N2 flux budget
# Pi_phi = Z_phi q = -Z_phi M  =>  M = -q).  NOTE (flagged canon tension): the depth/size node
# phrases M = +q; Gate-8 checks INTERNAL consistency (q_raw, Pi_phi, M_readout all agree with this
# convention), NOT sign-correctness -- the sign fork is a Charles/canon call, not adjudicated here.
SIGN_CONVENTION = -1.0


def readouts(v, ctx, prm, n5d=None):
    """The seal-flux readouts (q_raw, Pi_phi, sign_convention, M_readout).  q_raw is the unambiguous
    raw seal flux integral q = Z_phi rho_s^2 phi'(r_s); NOT q ~ Q_H (an import, forbidden)."""
    Z = prm[0]
    Q = fields(v, ctx, prm, n5d=n5d)
    rho_s = Q["rho"][-1]                                 # rho at the seal
    phi_prime_s = Q["phip"][-1]                          # phi'(r_s) -- FREE seal slope -> OUTPUT q
    q_raw = Z * rho_s ** 2 * phi_prime_s                 # raw seal flux integral (unambiguous)
    Pi_phi = Z * q_raw                                   # Gauss-budget form (§5)
    M_readout = SIGN_CONVENTION * q_raw                  # M = sign_convention * q_raw
    return dict(q_raw=float(q_raw), Pi_phi=float(Pi_phi),
                sign_convention=float(SIGN_CONVENTION), M_readout=float(M_readout))


# =========================================================================================
# THE MONOLITHIC RESIDUAL  ([phi-ODE; rho-ODE; f-PDE; all BCs; H=0]); jacrev-safe (pure torch)
# =========================================================================================
def residual(v, ctx, prm, wbc=1.0, n5d=None):
    """Monolithic residual.  n5d=None -> the base round-trace system (unchanged).  n5d=dict -> the
    off-round shear rows are APPENDED after the base block (base rows keep identical positions, so
    residual(v_base) == residual(v_n5d)[:base_len] whenever the shear amplitude a2==0)."""
    Z, XI, KAP, N = prm
    Q = fields(v, ctx, prm, n5d=n5d)
    phip, rhop, fr = Q["phip"], Q["rhop"], Q["fr"]
    rows = [
        Q["phi_ode"][1:-1],                                       # phi-ODE (interior)
        wbc * phip[[0, -1]],                                      # phi' = 0 mirror (both ends)
        Q["rho_ode"][1:-1],                                       # rho-ODE (interior)
        wbc * rhop[[0, -1]],                                      # rho' = 0 mirror (both ends)
        Q["res_f"][1:-1].reshape(-1),                            # f-PDE (interior r, all theta)
        wbc * fr[0, :], wbc * fr[-1, :],                         # f_r = 0 mirror (both ends, all theta)
    ]
    Hseal = H_of_r(v, ctx, prm)[-1]                               # H = 0 closure (at the seal)
    rows.append((wbc * Hseal).reshape(1))

    if n5d is not None:                                          # ---- N5d shear block (appended) ----
        a2, a2p, shear_res = Q["a2"], Q["a2p"], Q["shear_res"]
        sealbc = n5d.get("sealbc", "off")
        if sealbc == "off":
            rows.append(a2.reshape(-1))                           # frozen: a2 == 0 (Nr rows) -> round
        else:
            core_bc = a2p[[0]]                                    # even core fold: a2'(r_c)=0
            if sealbc == "S-Dir":                                # Dirichlet to the mirror value
                seal_bc = a2[[-1]] - float(n5d.get("a2_mirror", 0.0))
            elif sealbc == "S-JC2":                              # [pi^{AB}]=0 (source-free JC2): a2'(r_s)=0
                seal_bc = a2p[[-1]]
            else:
                raise ValueError(f"unknown sealbc {sealbc!r} (off | S-Dir | S-JC2)")
            rows += [shear_res[1:-1], wbc * core_bc, wbc * seal_bc]  # (Nr-2)+1+1 = Nr shear rows
    return torch.cat([r.reshape(-1) for r in rows])


# =========================================================================================
# SEED  (rigid f=theta background + a SMALL band-limited radial-structure deformation)
# =========================================================================================
def seed(ctx, phi0=0.0, rho0=0.70710678, L0=1.0, amp=0.02):
    """u = amp*(1-mu^2)*cos(pi (zeta+1)/2): (1-mu^2)=sin^2 th vanishes at the poles (degree-safe);
    the radial factor has zero derivative at BOTH ends -> f_r=0 mirror satisfied by the seed, with
    nonzero interior u_r (activates I_r>0). rho0 ~ 1/sqrt(2) (V5 rigid seal illustration; a SEED
    only, not a target). All CHOSE seed values -- Newton relaxes them."""
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    zeta = ctx["zeta"]; mu = ctx["mu"]
    gr = torch.cos(np.pi * (zeta + 1.0) / 2.0)                    # (Nr,)
    uf = amp * (1.0 - mu[None, :] ** 2) * gr[:, None]            # (Nr,Nth)
    phi = torch.full((Nr,), float(phi0), dtype=torch.float64)
    rho = torch.full((Nr,), float(rho0), dtype=torch.float64)
    return pack(phi, rho, uf, float(L0))


def seed_n5d(ctx, a2_amp=0.0, **kw):
    """Base seed with the ell=2 shear amplitude a2(r) appended (a2_amp=0 -> round seed, s=0).
    The shear is seeded SMALL and band-limited; Newton relaxes it (all CHOSE seed values)."""
    Nr = ctx["Nr"]; zeta = ctx["zeta"]
    base = seed(ctx, **kw)
    phi, rho, uf, L = unpack(base, ctx)
    gr = torch.cos(np.pi * (zeta + 1.0) / 2.0)                    # zero-slope at both ends (mirror-safe)
    a2 = a2_amp * gr
    return pack(phi, rho, uf, float(L), a2=a2)


# =========================================================================================
# LEVENBERG-MARQUARDT SOLVE (Nielsen gain-ratio damping = trust-region line search);
# Jacobian by torch.func.jacrev. Method mined from newton_solve_p1 (glm path).
# =========================================================================================
def _col_scale(J, eps=1e-300):
    """CATEGORY-A column scale VECTOR dc so that J @ diag(dc) has ~unit column 2-norms.
    COLUMN scaling only, because for a SQUARE root-finding (Newton/LM) system column scaling is an
    exact change of variables u = diag(dc) y -- the objective Phi=||F||^2 and the fixed point F=0 are
    INVARIANT -- whereas ROW-scaling the least-squares objective reweights the equations and produces
    steps that reduce a *row-weighted* residual instead of the true Phi (empirically it stalled the
    coupled solve).  This scaling in particular lifts the under-scaled L column (col-norm ~1e3 vs the
    field columns ~1e7) found in the N5d conditioning diagnosis.  The huge 2nd-derivative ODE rows are
    handled NOT by row-scaling but by solving the damped step with lstsq (QR/SVD) instead of the normal
    equations J^T J (which would square the condition number)."""
    cn = torch.linalg.norm(J, dim=0).clamp_min(eps)
    return 1.0 / cn


def newton_lm_solve(u0, ctx, prm, wbc=1.0, maxit=30, lam0=1e-3, tol=1e-13,
                    verbose=True, time_budget=110.0, n5d=None, equilibrate=True):
    """LM solve.  equilibrate=True (default, FIX-1): the damped LM step is computed with COLUMN scaling
    (objective-preserving; lifts the under-scaled L column) via a stacked damped least-squares solved by
    lstsq -- this AVOIDS forming the normal equations J^T J (whose condition number is cond(J)^2 ~ 1e30
    and is what made the linear solves rank-deficient), so the huge 2nd-derivative ODE rows no longer
    corrupt the step.  equilibrate=False reproduces the ORIGINAL normal-equations path byte-for-byte.
    In BOTH cases the residual/BCs/source/readouts are UNCHANGED and acceptance/convergence are judged
    on the TRUE unscaled residual Phi=||F||^2 (the linear-model predicted reduction is likewise the
    true-objective one), so FIX-1 changes the numerics of the STEP only, never the physics or the root."""
    import time
    from torch.func import jacrev
    t0 = time.time()
    resfn = lambda uu: residual(uu, ctx, prm, wbc=wbc, n5d=n5d)
    u = u0.detach().clone()
    F = resfn(u); Phi = float((F * F).sum()); hist = [Phi]
    lam = lam0; nu = 2.0
    for it in range(maxit):
        if Phi < tol or (time.time() - t0) > time_budget:
            break
        J = jacrev(resfn)(u).detach()
        F = resfn(u).detach()
        JT = J.transpose(0, 1)
        if equilibrate:
            dc = _col_scale(J)                             # column scale (objective-preserving)
            Jc = J * dc[None, :]                           # unit-ish columns; ROWS keep their true weight
            dHc = (Jc * Jc).sum(0).clamp_min(1e-300)       # diag(Jc^T Jc) ~ 1 (Marquardt col damping)
            zpad = torch.zeros(J.shape[1], dtype=J.dtype, device=J.device)
        else:
            Hm = JT @ J; g = JT @ (-F); dH = torch.diag(Hm)
        accepted = False
        for _try in range(30):
            try:
                if equilibrate:
                    # damped LM step via stacked least-squares (no normal equations => no cond squaring):
                    #   min_dy || [Jc; sqrt(lam) diag(sqrt(dHc))] dy - [-F; 0] ||   (rows UNweighted)
                    aug = torch.cat([Jc, (lam ** 0.5) * torch.diag(dHc.sqrt())], dim=0)
                    rhs = torch.cat([-F, zpad], dim=0)
                    dy = torch.linalg.lstsq(aug, rhs).solution
                    dx = dc * dy                            # unscale the step (exact change of variables)
                else:
                    dx = torch.linalg.solve(Hm + lam * torch.diag(dH), g)
            except Exception:
                lam = min(lam * nu, 1e12); nu *= 2.0; continue
            un = u + dx
            try:
                Fn = resfn(un); Pn = float((Fn * Fn).sum())
            except Exception:
                Pn = float("inf")
            if equilibrate:
                # predicted reduction of the TRUE objective by the linear model at this dx (scale-free)
                pred = Phi - float(((F + J @ dx) ** 2).sum())
            else:
                pred = float((dx * (lam * dH * dx + g)).sum())
            rho_gain = (Phi - Pn) / pred if (pred > 0.0 and math.isfinite(Pn)) else -1.0
            if rho_gain > 0.0:
                u = un; F = Fn.detach(); Phi = Pn
                lam = max(lam * max(1.0 / 3.0, 1.0 - (2.0 * rho_gain - 1.0) ** 3), 1e-14)
                nu = 2.0; accepted = True; break
            lam = min(lam * nu, 1e12); nu *= 2.0
        hist.append(Phi)
        if verbose:
            print(f"  [f2d-lm] it={it:3d} Phi={Phi:.6e} lam={lam:.2e} "
                  f"{'acc' if accepted else 'STALL'}{' [eq]' if equilibrate else ''}", flush=True)
        if not accepted:
            break
    return u.detach(), hist


def jac_condition(u, ctx, prm, wbc=1.0, n5d=None):
    """Report (cond, s_min, s_max, nrows, ncols) of the Jacobian at u (SVD)."""
    from torch.func import jacrev
    J = jacrev(lambda uu: residual(uu, ctx, prm, wbc=wbc, n5d=n5d))(u).detach()
    sv = torch.linalg.svdvals(J)
    return (float(sv[0] / sv[-1]), float(sv[-1]), float(sv[0]), J.shape[0], J.shape[1])


# =========================================================================================
# BOUNDED SMOKE TEST  (the ONLY solve in this module; hard limits per the anti-hang rule)
# =========================================================================================
def _n5d_assembly_preflight(Nr, Nth, prm, sealbc, wbc=1.0):
    """N5d ASSEMBLY-ONLY preflight (NO pilot solve; anti-hang: forward evals only, bounded grid).
    Proves: the coupled residual + shear BCs ASSEMBLE, the system is SQUARE, the Jacobian is finite,
    and the round-limit (a2=0) leaves the base rows unchanged.  The coarse coupled PILOT is GATED
    (do NOT run here) -- see N5d_solver_build_plan.md §8."""
    ctx = make_ctx(Nr, Nth, rc=0.5)
    n5d = dict(sealbc=sealbc)
    u = seed_n5d(ctx, a2_amp=0.0)                                 # round seed (s=0)
    F = residual(u, ctx, prm, wbc=wbc, n5d=n5d)
    ub = seed(ctx); Fb = residual(ub, ctx, prm, wbc=wbc)         # base (no shear) for comparison
    base_len = Fb.numel()
    print(f"[n5d] sealbc={sealbc}: len(u)={u.numel()} len(F)={F.numel()} "
          f"square={u.numel()==F.numel()} all-finite={bool(torch.isfinite(F).all())}")
    print(f"[n5d] base-row match (a2=0): max|F_n5d[:{base_len}] - F_base| = "
          f"{float((F[:base_len]-Fb).abs().max()):.3e}  (expect 0)")
    cond, smin, smax, nr_, nc_ = jac_condition(u, ctx, prm, wbc=wbc, n5d=n5d)
    print(f"[n5d] Jacobian shape=({nr_},{nc_}) cond={cond:.3e} s_min={smin:.3e}")
    ro = readouts(u, ctx, prm, n5d=n5d)
    print(f"[n5d] readouts: q_raw={ro['q_raw']:.4e} Pi_phi={ro['Pi_phi']:.4e} "
          f"sign={ro['sign_convention']:+.0f} M_readout={ro['M_readout']:.4e}")
    print("[n5d] ASSEMBLY-ONLY preflight complete -- the coarse coupled pilot is GATED (not run).")


if __name__ == "__main__":
    import time, argparse
    torch.manual_seed(0)
    ap = argparse.ArgumentParser(description="cell_solver_f2d smoke / N5d assembly preflight")
    ap.add_argument("--n5d", action="store_true", help="N5d shear extension (ASSEMBLY-ONLY here; pilot GATED)")
    ap.add_argument("--Nr", type=int, default=8); ap.add_argument("--Nth", type=int, default=8)
    ap.add_argument("--lmax", type=int, default=2, help="shear angular truncation (pilot: ell=2 only)")
    ap.add_argument("--source", default="none", help="frozen_hopfion | none (pilot source; not run here)")
    ap.add_argument("--sealbc", default="off", choices=["off", "S-Dir", "S-JC2"])
    ap.add_argument("--maxit", type=int, default=30); ap.add_argument("--budget", type=float, default=100.0)
    args = ap.parse_args()

    # ---- fixed parameters (ALL tagged) ----
    Z = 8.0            # CHOSE-fixed (OBS-2: Route-A structure carrying Route-B's number; held fixed)
    XI = 1.0           # CHOSE-units (repo unit convention)
    KAP = 1.0          # CHOSE-units (kap/xi sets the absolute cell scale; ratios are the observables)
    N = 1              # DERIVED-topological (winding degree; integer, fixed per run)
    prm = (Z, XI, KAP, N)

    if args.n5d:
        assert args.Nr <= 24, "anti-hang: Nr capped at 24"
        print("=== cell_solver_f2d N5d ASSEMBLY PREFLIGHT (no pilot solve) ===")
        _n5d_assembly_preflight(args.Nr, args.Nth, prm, args.sealbc)
        raise SystemExit(0)

    Nr, Nth = 8, 8     # BOUNDED smoke-test resolution (HARD anti-hang cap; NOT a converged run)
    wbc = 1.0
    print("=== cell_solver_f2d BOUNDED SMOKE TEST (Nr=8, Nth=8, N=1, Z=8, xi=kap=1) ===")
    print("    goal: residual assembles, Jacobian finite/non-singular, ONE LM step decreases Phi,")
    print("    H(r) and Derrick diagnostics compute.  NOT to find a cell.\n")
    t0 = time.time()

    ctx = make_ctx(Nr, Nth, rc=0.5)
    u0 = seed(ctx)

    F0 = residual(u0, ctx, prm, wbc=wbc)
    Phi0 = float((F0 * F0).sum())
    print(f"seed: len(u)={u0.numel()}  len(F)={F0.numel()}  (square: {u0.numel()==F0.numel()})")
    print(f"seed: Phi0=||F||^2 = {Phi0:.6e}   max|F| = {float(F0.abs().max()):.3e}   "
          f"all-finite: {bool(torch.isfinite(F0).all())}")

    cond, smin, smax, nr_, nc_ = jac_condition(u0, ctx, prm, wbc=wbc)
    print(f"seed Jacobian: shape=({nr_},{nc_})  cond={cond:.3e}  s_min={smin:.3e}  s_max={smax:.3e}")

    H0 = H_of_r(u0, ctx, prm)
    print(f"seed H(r): min={float(H0.min()):+.4e} max={float(H0.max()):+.4e}  "
          f"drift(max-min)={float(H0.max()-H0.min()):.3e}  H(seal)={float(H0[-1]):+.4e}")
    Sa, Sb, dS = derrick(u0, ctx, prm)
    print(f"seed Derrick: S_a={Sa:+.4e} S_b={Sb:+.4e}  S_a-S_b={dS:+.4e} (nonzero off-solution: expected)\n")

    print("LM iterations (bounded maxit=30, wall<120s):")
    u1, hist = newton_lm_solve(u0, ctx, prm, wbc=wbc, maxit=30, verbose=True, time_budget=110.0)

    print(f"\nPhi history: {['%.4e' % h for h in hist]}")
    print(f"ONE-STEP decrease: Phi0={hist[0]:.6e} -> Phi1={hist[1]:.6e}  "
          f"decreased={hist[1] < hist[0]}")
    print(f"final Phi={hist[-1]:.6e}  (iters={len(hist)-1})")
    Hf = H_of_r(u1, ctx, prm)
    print(f"final H(r): drift(max-min)={float(Hf.max()-Hf.min()):.3e}  H(seal)={float(Hf[-1]):+.4e}")
    Sa, Sb, dS = derrick(u1, ctx, prm)
    print(f"final Derrick: S_a={Sa:+.4e} S_b={Sb:+.4e}  S_a-S_b={dS:+.4e}")
    print(f"\nwall time: {time.time()-t0:.1f}s  (budget 120s)")
    print("SMOKE TEST COMPLETE -- no cell claimed; this validates ASSEMBLY + STEP + DIAGNOSTICS only.")

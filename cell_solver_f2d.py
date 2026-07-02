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
    )


# =========================================================================================
# PACK / UNPACK  --  u_vec = [ phi(Nr), rho(Nr), u_field(Nr*Nth), L ]
# =========================================================================================
def pack(phi, rho, ufield, L):
    return torch.cat([phi.reshape(-1), rho.reshape(-1), ufield.reshape(-1),
                      torch.as_tensor([L], dtype=torch.float64, device=phi.device)])


def unpack(v, ctx):
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    phi = v[:Nr]; rho = v[Nr:2 * Nr]
    uf = v[2 * Nr:2 * Nr + Nr * Nth].reshape(Nr, Nth)
    L = v[-1]
    return phi, rho, uf, L


# =========================================================================================
# FIELDS + DERIVATIVES + MOMENTS  (the single shared evaluator; torch, jacrev-safe)
# =========================================================================================
def fields(v, ctx, prm):
    """Return a dict of all node-level quantities used by the residual + diagnostics."""
    Z, XI, KAP, N = prm
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    phi, rho, uf, L = unpack(v, ctx)
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

    return dict(phi=phi, rho=rho, L=L, phip=phip, rhop=rhop, fr=fr,
                e2m=e2m, e2p=e2p, Ir=Ir, Ith=Ith, Is=Is, I4th=I4th, I4r=I4r,
                phi_ode=phi_ode, rho_ode=rho_ode, res_f=res_f)


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
# THE MONOLITHIC RESIDUAL  ([phi-ODE; rho-ODE; f-PDE; all BCs; H=0]); jacrev-safe (pure torch)
# =========================================================================================
def residual(v, ctx, prm, wbc=1.0):
    Z, XI, KAP, N = prm
    Q = fields(v, ctx, prm)
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


# =========================================================================================
# LEVENBERG-MARQUARDT SOLVE (Nielsen gain-ratio damping = trust-region line search);
# Jacobian by torch.func.jacrev. Method mined from newton_solve_p1 (glm path).
# =========================================================================================
def newton_lm_solve(u0, ctx, prm, wbc=1.0, maxit=30, lam0=1e-3, tol=1e-13,
                    verbose=True, time_budget=110.0):
    import time
    from torch.func import jacrev
    t0 = time.time()
    resfn = lambda uu: residual(uu, ctx, prm, wbc=wbc)
    u = u0.detach().clone()
    F = resfn(u); Phi = float((F * F).sum()); hist = [Phi]
    lam = lam0; nu = 2.0
    for it in range(maxit):
        if Phi < tol or (time.time() - t0) > time_budget:
            break
        J = jacrev(resfn)(u).detach()
        F = resfn(u).detach()
        JT = J.transpose(0, 1)
        Hm = JT @ J; g = JT @ (-F); dH = torch.diag(Hm)
        accepted = False
        for _try in range(30):
            try:
                dx = torch.linalg.solve(Hm + lam * torch.diag(dH), g)
            except Exception:
                lam = min(lam * nu, 1e12); nu *= 2.0; continue
            un = u + dx
            try:
                Fn = resfn(un); Pn = float((Fn * Fn).sum())
            except Exception:
                Pn = float("inf")
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
                  f"{'acc' if accepted else 'STALL'}", flush=True)
        if not accepted:
            break
    return u.detach(), hist


def jac_condition(u, ctx, prm, wbc=1.0):
    """Report (cond, s_min, s_max, nrows, ncols) of the Jacobian at u (SVD)."""
    from torch.func import jacrev
    J = jacrev(lambda uu: residual(uu, ctx, prm, wbc=wbc))(u).detach()
    sv = torch.linalg.svdvals(J)
    return (float(sv[0] / sv[-1]), float(sv[-1]), float(sv[0]), J.shape[0], J.shape[1])


# =========================================================================================
# BOUNDED SMOKE TEST  (the ONLY solve in this module; hard limits per the anti-hang rule)
# =========================================================================================
if __name__ == "__main__":
    import time
    torch.manual_seed(0)
    # ---- fixed parameters (ALL tagged) ----
    Z = 8.0            # CHOSE-fixed (OBS-2: Route-A structure carrying Route-B's number; held fixed)
    XI = 1.0           # CHOSE-units (repo unit convention)
    KAP = 1.0          # CHOSE-units (kap/xi sets the absolute cell scale; ratios are the observables)
    N = 1              # DERIVED-topological (winding degree; integer, fixed per run)
    prm = (Z, XI, KAP, N)
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

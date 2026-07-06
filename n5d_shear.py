"""n5d_shear.py -- the off-round transverse (shear) pieces of the N5d extension.

ISOLATED + unit-testable helpers for the shear DOF that cell_solver_f2d.py imports.
Everything here is DERIVED from the NATIVE constrained-two-player action (Branch P,
block-diagonal, phi longitudinal); NO GR G=8piT, NO archived operator, e^{-2phi} EXACT.

Exact provenance (verbatim, CAS-checked in this repo):
  - metric / K_AB / Kcal      : native_field_equations_constrained_two_player_results.md:90-95
  - E^{AB} = -T^{AB} tensor eq : H4_N1_offround_transverse_equation_results.md:19-24
  - Kcal = -2 det(K^A_B)       : H4_N1:57  (=> Kcal = -1/2 e^{-2phi}(a' bt')/(a bt))
  - (a,bt) split, ell, L_bare  : h4_scripts/op_derive2.py  (roots {1,2})

Trace / shear split (round <=> s==0):
    a  = rho^2 e^{ s} = h_thth
    bt = rho^2 e^{-s} = h_psps / sin^2(theta)
    rho^2 = sqrt(a bt)  (areal-volume trace scale, phi-BLIND measure sqrt(h)=rho^2 sin th)
    s     = 1/2 ln(a/bt)  (the TRACELESS shear DOF that N5d unfreezes; round: a=bt=r^2, s=0)

The geometric shear action density is  c sqrt(h) Kcal = c e^{-2phi} ell  with
    ell = -1/2 sin th (a' bt')/sqrt(a b)  (op_derive2:8).
Varying w.r.t. s (delta a = a ds, delta bt = -bt ds; sqrt(h)=rho^2 is s-INDEPENDENT so the
(Z/2)phi'^2 measure and the Gauss-Bonnet R^{(2)} terms drop from the TRACELESS row) gives the
pointwise traceless E-row (CAS-derived + round/linearization-checked, scratch derive_shear.py):
    E_s(r,theta) = - e^{-2phi} [ rho^2 s'' + (2 rho rho' - 2 phi' rho^2) s' ]     (sans sin th area factor)
round s->0 : E_s -> 0 ; round linearization (rho=r, phi const): E_s -> -e^{-2phi}(r^2 s''+2r s'),
and L_bare[r^2 s] = r^2 (r^2 s'' + 2 r s')  => the a-perturbation obeys L_bare (roots {1,2}),
tying the live operator to the certified h4_scripts/lbare_inverse.py.

Category-A note: lbare_precondition wraps the CERTIFIED L_bare BVP inverse (numpy) ONLY as a
linear-response initial guess / TT eigen-index cross-check -- it is NEVER the physics operator
inside the residual (the residual keeps Kcal and e^{-2phi} EXACT).  The buggy green_response is
NOT used.
"""
import torch

torch.set_default_dtype(torch.float64)


# =========================================================================================
# EXACT off-round invariant + measure  (e^{-2phi} kept EXACT; NO Taylor)
# =========================================================================================
def Kcal_offround(a, bt, ap, btp, phi):
    """The EXACT off-round invariant  Kcal = -1/2 e^{-2phi} (a' bt')/(a bt)  (H4_N1:57,70).

    a, bt : the transverse metric functions h_thth and h_psps/sin^2th.
    ap, btp : their radial derivatives a', bt'.
    Round reduction a=bt=r^2, a'=bt'=2r  ->  -1/2 e^{-2phi}(4 r^2)/r^4 = -2 e^{-2phi}/r^2 .
    """
    return -0.5 * torch.exp(-2.0 * phi) * (ap * btp) / (a * bt)


def sqrt_h(a, bt, theta):
    """The phi-BLIND transverse area measure  sqrt(h) = sqrt(a bt) sin(theta)  (native_field:92)."""
    return torch.sqrt(a * bt) * torch.sin(theta)


# =========================================================================================
# The TRACELESS component of E^{AB} = -T^{AB}  (the genuinely-new shear-s equation; H4_N1:19-24,79)
# =========================================================================================
def EAB_shear_row(rho, rhop, phip, s, s_r, s_rr, e2m=None, phi=None):
    """Pointwise TRACELESS geometric E-row  E_s = -e^{-2phi}[rho^2 s'' + (2 rho rho' - 2 phi' rho^2) s'].

    (= the traceless part of E^{AB} = (Z/2)phi'^2 h^{AB} + [1/2 h^{AB}K - 2K^{AC}K_C^B + 2K K^{AB}]
       - d_r pi^{AB}; the pure-trace phi'^2 and 1/2 h K pieces drop from the traceless projection
       because sqrt(h)=rho^2 is s-INDEPENDENT -- verified in derive_shear.py.)
    The sin(theta) area factor is supplied by the ell=2 Galerkin quadrature in the solver, NOT here.
    Round s->0 gives 0.  Provide EITHER e2m=e^{-2phi} OR phi (e2m takes precedence).  e^{-2phi} EXACT.
    """
    if e2m is None:
        if phi is None:
            raise ValueError("EAB_shear_row: supply e2m (=e^{-2phi}) or phi")
        e2m = torch.exp(-2.0 * phi)
    rho2 = rho * rho
    return -e2m * (rho2 * s_rr + (2.0 * rho * rhop - 2.0 * phip * rho2) * s_r)


def source_interp(source_rc, source_sh2, r_phys):
    """Differentiable linear interpolation of the frozen sh2(r) profile at physical radii r_phys.
    torch-differentiable in r_phys (hence in the cell length L) -- this is what makes registration B
    (current-L pullback) live inside the residual: the source is sampled at the CURRENT physical cell
    coordinate r(zeta)=r_c+(L/2)(zeta+1), not frozen at the seed L0.  Clamps to 0 outside the source
    support (the hopfion is compact), matching np.interp(left=0.0, right=0.0).  NO amplitude Jacobian
    (interpolation only); the amplitude/continuation factor is applied by the caller.  source_rc must be
    ascending."""
    rc = torch.as_tensor(source_rc, dtype=torch.float64)
    sh = torch.as_tensor(source_sh2, dtype=torch.float64)
    idx = torch.searchsorted(rc, r_phys).clamp(1, rc.numel() - 1)
    x0 = rc[idx - 1]; x1 = rc[idx]; f0 = sh[idx - 1]; f1 = sh[idx]
    t = (r_phys - x0) / (x1 - x0)                       # differentiable in r_phys (hence L)
    val = f0 + t * (f1 - f0)
    outside = (r_phys < rc[0]) | (r_phys > rc[-1])
    return torch.where(outside, torch.zeros_like(val), val)


def phi_source_offround_correction(rho, a2p, e2m, Z):
    """The ADDITIVE off-round correction to the Branch-P phi-source, from the surface-averaged Kcal
    with s = a2(r) P2(mu):  the phi-ODE residual gains  +(1/(5 Z)) e^{-2phi} a2'^2   (vanishes at a2=0).

    Derivation (derive_shear.py, CAS): <Kcal> = int sqrt(h) Kcal dOmega / int sqrt(h) dOmega with
    int P2^2 dmu = 2/5  =>  RHS of d_r(rho^2 Z phi') = 4 e^{-2phi} rho'^2 - (1/5) rho^2 e^{-2phi} a2'^2 .
    Writing phi'' = RHS/(Z rho^2) - 2 rho' phi'/rho, the a2-piece is -(1/(5 Z)) e^{-2phi} a2'^2 on the
    RHS, i.e. the ODE RESIDUAL (phi'' - RHS) gains +(1/(5 Z)) e^{-2phi} a2'^2 .
    """
    return (1.0 / (5.0 * Z)) * e2m * a2p ** 2


# =========================================================================================
# CATEGORY-A: certified L_bare BVP inverse wrapper (preconditioner + TT eigen-index only)
# =========================================================================================
def lbare_precondition(r, source, f_lo=0.0, f_hi=0.0):
    """Linear-response shear (a-perturbation alpha=rho^2 s) to a given source, via the CERTIFIED
    L_bare two-point BVP inverse (h4_scripts/lbare_inverse.py).  CATEGORY-A (a linear-solver
    technique / initial guess + cross-check) -- NEVER the physics operator in the residual.

    r, source : 1-D numpy arrays on the radial nodes.  Returns the numpy BVP solution.
    """
    import numpy as np
    from h4_scripts.lbare_inverse import lbare_solve_bvp
    return lbare_solve_bvp(np.asarray(r, dtype=float), np.asarray(source, dtype=float),
                           float(f_lo), float(f_hi))


def lbare_tt_eigindex(r):
    """Mechanism-(ii) TT eigen-index: eigenvalues of the certified L_bare interior operator on nodes r
    (h4_scripts/lbare_inverse.build_Lbare).  Round has roots {1,2} (both growing) => NO localized
    decaying mode; a shear-coupled shift could change this.  CATEGORY-A cross-check, not the residual.
    Returns (eigvals, n_decaying_estimate) with n_decaying = count of interior eigenvalues < 0.
    """
    import numpy as np
    from h4_scripts.lbare_inverse import build_Lbare
    L = build_Lbare(np.asarray(r, dtype=float))
    Lint = L[1:-1, 1:-1]
    ev = np.linalg.eigvals(Lint)
    ev = np.sort(ev.real)
    n_dec = int((ev < 0).sum())
    return ev, n_dec

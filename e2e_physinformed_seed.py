"""e2e_physinformed_seed.py -- PHYSICS-INFORMED SEED generator for the embedded-particle composite
solve (E2e, the "fix-the-flaw" continuation of E2d).

THE FLAW (E2d): `cell_solver_composite.seed_comp` sets the cell core to CONTINUITY-FLATS
(phi=phi_loc(r_p), rho=rho_loc(r_p) constant).  A real solution's core sits at the DERIVED even
mirror fold with rho_c pinned by the migrated criticality E_ang(core)=2 (E1, canon C-2026-07-03-3)
-- which is O(1) away from rho_loc (e.g. W1: rho_c=0.183 vs rho_loc~1.0).  That O(1) core offset is
exactly the UNCERTIFIED "combined-cell field axis" the E2d driver folds short on.

THE FIX: build the seed from the DERIVED core:
  * core rho_c = the E_ang(core)=2 criticality value (rigid moments; ledger below),
  * even mirror fold  phi'(0)=rho'(0)=0  (the derived core class, E1 sec.3),
  * interior profile = EITHER a short OUTWARD INTEGRATION of the coupled cell EL from that even-fold
    core (family='integrate'), OR a smooth even-fold blend from (phi_c,rho_c) to the continuity
    values at the seal (family='blend' = "rigid+bulge profile at the correct core depth", E1 P3),
  * a theta bulge in u (the bulge theorem, E1 P3: any closure is a non-perturbative theta object),
  * ambient = the banked E0 profile (IDENTICAL to seed_comp -- the ambient was never the flaw).

DISCIPLINE (critical): this is ONLY a STARTING GUESS (Category-A conditioning).  It NEVER touches
`residual_comp`/`lm_hardened` (byte-identical; git-verified).  Convergence must be to a root of the
TRUE residual; the seed is NEVER an acceptance criterion.  A seed near a NON-solution must fail to
converge, so it cannot manufacture a false positive; every candidate faces the full instrument set
(H_cell, sigma, seed-independence incl. the NON-physics-informed flat seed).

All CHOSE values are reported per call.  Data-blind (no observational numbers; the anchor Delta-phi
lives only in the banked bracket, untouched).
"""
import os, math
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
import cell_solver_composite as C


# =========================================================================================
# Derived core value: rho_c from the migrated criticality E_ang(core)=2 (RIGID moments).
#   rigid carrier f=theta => I_th = I_s = I_4th = 1 (GL-weight identities), so
#   E_ang(core,rigid) = (xi/2)(I_th + N^2 I_s) + (kap N^2/2) I_4th/rho_c^2
#                     = (xi/2)(1 + N^2) + kap N^2 / (2 rho_c^2)  = 2.
#   => rho_c = N sqrt( kap / (2 (2 - (xi/2)(1+N^2))) ).  (DERIVED; the E1-sec.3 core closure.)
# For N=1 this is the E1 U_eff closure rho_c = sqrt(kap/(2(2-xi))).
# =========================================================================================
def derived_rho_c(prm):
    Z, XI, KAP, N = prm
    base = (XI / 2.0) * (1.0 + N ** 2)
    rem = 2.0 - base
    if rem <= 0:
        return None, base            # rigid core criticality has no positive root (ledger flag)
    return float(N * math.sqrt(KAP / (2.0 * rem))), base


def _rigid_moments():
    """(I_r, I_4th) for the rigid carrier f=theta (u=0): I_r=0, I_4th=1 (GL identities)."""
    return 0.0, 1.0


# =========================================================================================
# OUTWARD integration of the coupled cell EL from the even-fold core (RIGID moments).
#   phi'' = 4 e^{-2phi} rho'^2/(Z rho^2) - 2 phi' rho'/rho
#   rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2 + (e^{2phi}/4)(xi rho I_r - kap N^2 I_4th/rho^3)
#   BCs at r=0: phi=phi_c, rho=rho_c, phi'=0, rho'=0  (even mirror fold).
# RK4 on the physical interval [0, r_p]; substeps bounded.  Category-A: a warm-start construction.
# Returns phi(node r), rho(node r) sampled at the cell CGL nodes; None on non-finite blowup.
# =========================================================================================
def outward_core_profile(prm, phi_c, rho_c, r_nodes, r_p, nsub=400):
    Z, XI, KAP, N = prm
    Ir, I4th = _rigid_moments()

    np.seterr(over="ignore", invalid="ignore", divide="ignore")

    def rhs(y):
        phi, php, rho, rhp = y
        phi = max(min(phi, 250.0), -250.0)                 # guard exp overflow (stiff throat)
        e2m = math.exp(-2.0 * phi); e2p = math.exp(2.0 * phi)
        phipp = 4.0 * e2m * rhp ** 2 / (Z * rho ** 2) - 2.0 * php * rhp / rho
        rhopp = (2.0 * php * rhp - (Z / 4.0) * rho * e2p * php ** 2
                 + (e2p / 4.0) * (XI * rho * Ir - KAP * N ** 2 * I4th / rho ** 3))
        return np.array([php, phipp, rhp, rhopp])

    # dense march on [0, r_p], then sample at the (sorted) requested nodes
    r_nodes = np.asarray(r_nodes, dtype=float)
    rmax = max(r_p, float(r_nodes.max()))
    h = rmax / nsub
    y = np.array([phi_c, 0.0, rho_c, 0.0])
    rs = [0.0]; phis = [phi_c]; rhos = [rho_c]
    r = 0.0
    for _ in range(nsub):
        try:
            k1 = rhs(y); k2 = rhs(y + 0.5 * h * k1); k3 = rhs(y + 0.5 * h * k2); k4 = rhs(y + h * k3)
            y = y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        except (OverflowError, FloatingPointError, ZeroDivisionError):
            return None, None            # stiff throat collapse -> caller uses blend fallback
        r += h
        if not np.all(np.isfinite(y)) or y[2] <= 1e-4 or abs(y[0]) > 250.0:
            return None, None            # blew up / rho crossed 0 -> caller uses blend fallback
        rs.append(r); phis.append(y[0]); rhos.append(y[2])
    phi_n = np.interp(r_nodes, rs, phis)
    rho_n = np.interp(r_nodes, rs, rhos)
    return phi_n, rho_n


# =========================================================================================
# Smootherstep even-fold blend s(x): s(0)=0, s(1)=1, s'(0)=s'(1)=0  (mirror at core & seal).
# =========================================================================================
def _smootherstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x ** 3 * (6.0 * x ** 2 - 15.0 * x + 10.0)


# =========================================================================================
# THE PHYSICS-INFORMED SEED.
# =========================================================================================
def physinformed_seed(ctx, bracket, prm, rp0, amp=0.8, family="blend", phi_c_off=0.0,
                      rho_c=None, device="cpu", info=False):
    """Build a physics-informed composite seed.
      family = 'blend'     : even-fold smootherstep from (phi_c, rho_c^derived) to the continuity
                             values (phi_loc, rho_loc) at the seal (E1 P3 rigid+bulge profile).
      family = 'integrate' : short outward RK4 of the coupled cell EL from the even-fold core
                             (falls back to 'blend' if the integration blows up).
      phi_c_off : core-depth offset (phi_c = phi_loc(r_p) + phi_c_off; phi_c is FREE per E1 sec.1,
                  flux law only pins its SIGN monotonically; default 0 = continuity-flat phi).
      rho_c     : override the derived core rho_c (for MMS / seed-family variation); default = derived.
    Ambient block = IDENTICAL to seed_comp (banked E0 profile); only the CELL core is corrected.
    Returns v (torch) [, dict of CHOSE/derived diagnostics]."""
    Nr, Nth, Na = ctx["Nr"], ctx["Nth"], ctx["Na"]
    h = np.asarray(ctx["ha_ld"], dtype=float)
    rsU0 = bracket["r_s"]
    rn_amb = rp0 + (rsU0 - rp0) * h
    phi_a = np.interp(rn_amb, bracket["prof_r"], bracket["prof_phi"])
    rho_a = np.interp(rn_amb, bracket["prof_r"], bracket["prof_rho"])
    phi_loc = float(np.interp(rp0, bracket["prof_r"], bracket["prof_phi"]))
    rho_loc = float(np.interp(rp0, bracket["prof_r"], bracket["prof_rho"]))

    rc_deriv, base = derived_rho_c(prm)
    rc = rho_c if rho_c is not None else (rc_deriv if rc_deriv is not None else rho_loc)
    phi_c = phi_loc + phi_c_off

    # cell radial nodes: r = (r_p/2)(zeta+1)  (concentric reference-interval map)
    zeta = ctx["cell"]["zeta"].cpu().numpy()
    r_cell = 0.5 * rp0 * (zeta + 1.0)
    x = (zeta + 1.0) / 2.0                          # in [0,1], core=0, seal=1

    used = family
    if family == "integrate":
        phi_n, rho_n = outward_core_profile(prm, phi_c, rc, r_cell, rp0)
        if phi_n is None:
            used = "blend(int-fallback)"
    if used.startswith("blend"):
        s = _smootherstep(x)
        rho_n = rc + (rho_loc - rc) * s
        phi_n = phi_c + (phi_loc - phi_c) * s

    # theta bulge in u (the E1 P3 non-perturbative deformation); pole-safe (1-mu^2), even fold at core
    mu = ctx["cell"]["mu"].cpu().numpy()
    uf = amp * (1.0 - mu[None, :] ** 2) * np.sin(np.pi * (zeta[:, None] + 1.0) / 2.0)

    tt = lambda a: torch.as_tensor(np.asarray(a, dtype=float), dtype=torch.float64, device=device)
    v = C.pack_comp(tt(phi_n), tt(rho_n), tt(uf), tt(phi_a), tt(rho_a), rp0, rsU0, device=device)
    if not info:
        return v
    return v, dict(family=used, rho_c_derived=rc_deriv, rho_c_used=rc, base=base,
                   phi_c=phi_c, phi_loc=phi_loc, rho_loc=rho_loc, rp0=rp0, amp=amp,
                   rho_core_offset=abs(rc - rho_loc))


def flat_seed(ctx, bracket, rp0, amp=0.8, device="cpu"):
    """The E2d NON-physics-informed seed (seed_comp): flat continuity cell core.  Kept here as the
    anti-imposition seed-independence family (a converged candidate MUST also be findable from a
    seed that does NOT know the derived core)."""
    return C.seed_comp(ctx, bracket, rp0=rp0, amp=amp, device=device)


def seed_dist(v_a, v_b):
    """max|.| distance between two composite states (numpy longdouble)."""
    a = np.asarray(v_a.detach().cpu().numpy() if torch.is_tensor(v_a) else v_a, dtype=np.longdouble)
    b = np.asarray(v_b.detach().cpu().numpy() if torch.is_tensor(v_b) else v_b, dtype=np.longdouble)
    return float(np.abs(a - b).max())


if __name__ == "__main__":
    # assembly sanity (NO solve): the physics seed assembles, is finite, and sits CLOSER to a
    # derived-core target than the flat seed.
    lab = "A1 m=3 Z=8"
    br = C.load_bracket(lab)
    ctx = C.make_ctx_comp(12, 8, 192, kmap=2.5, device="cpu")
    for nm, N, XI, KAP, frac in [("W1", 1, 0.5, 0.1, 0.5), ("W6", 2, 0.05, 1.0, 0.95),
                                 ("W3", 1, 1.0, 0.1, 0.5)]:
        prm = (br["Z"], XI, KAP, N)
        rp0 = frac * br["r_s"]
        vb, d = physinformed_seed(ctx, br, prm, rp0, amp=0.8, family="blend", info=True)
        vi = physinformed_seed(ctx, br, prm, rp0, amp=0.8, family="integrate")
        vf = flat_seed(ctx, br, rp0, amp=0.8)
        Fb = C.residual_comp(vb, ctx, prm, br)
        print(f"{nm}: rho_c_der={d['rho_c_derived']} used={d['rho_c_used']:.4f} "
              f"rho_loc={d['rho_loc']:.4f}  blend|F|={float(Fb.abs().max()):.2e} "
              f"finite={bool(torch.isfinite(Fb).all())}  "
              f"d(blend,flat)={seed_dist(vb,vf):.3f} d(int,flat)={seed_dist(vi,vf):.3f}")

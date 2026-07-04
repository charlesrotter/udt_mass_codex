"""cell_solver_composite.py -- E2a: the coupled particle-in-universe solver (ONE monolithic
residual for the composite: cell + ambient + BOTH free boundaries).

CONTRACT: microphysics_E2_battle_plan.md (APPROVED AS WRITTEN, Charles 2026-07-03; E2a = build +
verify; the production sweep is E2b and is NOT run here). Conditions are EXACTLY the E1 derived
condition set, microphysics_E1_composite_closure_results.md sec.1 (BANKED, BLIND-VERIFIED).
This module is a NEW OBJECT that IMPORTS the existing banked machinery -- it does NOT fork it:
  * cell block  = cell_solver_f2d.fields/H_of_r/derrick/make_ctx (SH-exact angular, Cheb radial,
    deviation unknown u = f - theta; the banked, harness-verified evaluator; verify_f2d_reduction.py)
  * ambient EOMs = cell_solver_universe_T3.py:18-20 (same formulas, assembled here in collocation
    form; CAS-matched by K0a of microphysics_E1_composite_conditions.py and re-checked discretely
    by verify_composite_reduction.py)
  * slice families = cascade_stageA_lib.make_A1/make_A3 formulas (banked CHOSE families; the torch/
    longdouble ports here are cross-checked against the banked numpy functions in the harness)
  * ambient truth tables = microphysics_E0_ambient_tables.json (banked, blind-verified E0; solver
    output -- NOT observational data; data-blind rule intact).

================================ THE COMPOSITE SYSTEM ================================
Domains (round-static, diagonal, areal, CONCENTRIC -- E1 ledger #1,#2, all CHOSE-cited):
  cell    [0, r_p]     : fields phi(r), rho(r), f(r,theta) = theta + u  (native S^2 L2+L4 carrier,
                         canon C-2026-06-14-1; reduced EOMs = cell_solver_f2d.py:14-44)
  ambient [r_p, r_sU]  : fields phi(r), rho(r)  (potential-only phi-blind L_m = -U(rho), T3 slice
                         family per bracket, slice parameter a* FIXED at the banked bracket value)
  unknowns r_p, r_sU   : BOTH free boundaries are Newton unknowns (fixed reference-interval maps).

CONDITION SET (E1 sec.1, verbatim; every row cited):
  core r=0     : phi' = 0, rho' = 0, f_r(0,theta) = 0        (natural BCs; E1 K1'/K6', DERIVED)
  seal r=r_p   : [phi] = 0, [rho] = 0                        (continuity posture, E1 ledger #9 CHOSE-cited)
                 C1a [pi_phi] = 0  <=> phi'_cell = phi'_amb   (JC1)
                 C1b [pi_rho] = 0  <=> rho'_cell = rho'_amb   (JC2 reduced)
                 C1c f_r(r_p,theta) = 0  for all theta        (one-sided natural BC, DERIVED K1/K1')
                 C2  E_ang(r_p) = U(rho_p)                    (collapsed form, K4; valid WITH C1c)
  fold r=r_sU  : phi = 0 (essential odd pin), rho' = 0, H_amb = 0 (transversality); q = Z rho_s^2 phi'_s
                 is an OUTPUT, never a condition.
  poles        : f(r,0)=0, f(r,pi)=pi  -- carried by the theta-ramp background of the u-deviation
                 representation (inherited from cell_solver_f2d, its banked treatment).
  anchor       : Delta-phi = ln(1101) is applied at BRACKET level only (a* = banked value, FIXED);
                 the composite's Delta-phi = -phi_c floats at O(back-reaction) and is REPORTED,
                 not imposed (E1 sec.4 + ledger #5, CHOSE). anchor_mode='exact' (Delta-phi row,
                 a* freed) is provided for the pure-universe verification mode and as the other
                 branch of the E1 ledger-#5 bookkeeping; default is 'bracket'.

COUNTING (SQUARE; E1 sec.4/sec.8): unknowns 2*Nr + Nr*Nth + 2*Na + 2 == rows
  cell interior 2(Nr-2) + (Nr-2)*Nth ; core BCs 2 + Nth ; C1c Nth ; ambient interior 2(Na-2);
  seal 5 (continuity 2 + C1a + C1b + C2); fold 3 (phi, rho', H_amb).

================================ DISCRETIZATION (Category-A, all conditioning) ================
* cell: EXACTLY the cell_solver_f2d operators (imported): Cheb-Gauss-Lobatto in zeta on [-1,1],
  physical r = (r_p/2)(zeta+1)  [reference-interval map, r_c = 0 concentric], SH-exact theta.
  The cell block is evaluated by PACKING v_cell = [phi_cell, rho_cell, u, L=r_p] and calling
  cell_solver_f2d.fields -- the banked evaluator, byte-identical physics.
* ambient: Cheb-Gauss-Lobatto zeta in [-1,1], physical r = r_p + (r_sU - r_p) * h(zeta) with the
  wall-clustered map h(zeta) = tanh(kmap(1+zeta)/2)/tanh(kmap)  [Category-A grid conditioning;
  kmap=0 -> affine. Default kmap=2.5 chosen by the E2a conditioning study: the outer seal wall
  (E0 dense-table scale, wall width ~ 1/phi'_s) is the resolution-limiting feature].
* Nonlinear solve: monolithic Levenberg-Marquardt with QR/lstsq trust steps on the COLUMN-SCALED
  augmented system [J; sqrt(lam) I] (Category-A: the normal-equations form J^T J stalls at
  cond(J)^2 -- the E2a conditioning study measured cond(J) ~ 1e8-1e11 through the banked ambient
  stiffness ||Psi|| ~ 1e6-2.4e8, E1 sec.5b). Jacobian by torch.func.jacrev (float64, GPU-capable
  with CPU spot-checks); optional EXTENDED-PRECISION (numpy longdouble) residual refinement for
  the pure-universe recovery mode (Category-A numerical technique: float64 residual roundoff,
  amplified by the ambient stiffness, floors a* recovery at ~1e-7 rel; the longdouble residual +
  float64-Jacobian iteration floors it at ~3e-9. Soundness: the two residual paths are
  cross-checked to float64 machine precision in verify_composite_reduction.py).

================================ INSTRUMENTS (battle plan sec. 'verdict instruments') ==========
  * H_amb(r), H_cell(r) profiles + drifts.  H_cell == 0 is NOT imposed anywhere: it is the E1
    sec.2 DERIVED consequence (H_amb(fold)=0 -> conservation -> C2 -> H_cell == 0) and therefore
    a free consistency gate on any true composite solution (must read ~0 there and provably reads
    NONZERO off-solution -- the E0-verifier vacuousness lesson; demonstrated in the harness).
  * matched-Derrick (embedded Pohozaev, E1 K9/P2): on-shell with H == 0,
        S_a - S_b = rho_p pi_rho(r_p) = -4 e^{-2phi_p} rho'_p rho_p  == -tax(r_p).
    Gate value = (S_a - S_b) + 4 e^{-2phi_p} rho'_p rho_p  (0 on-shell; nonzero off-shell).
  * sigma cross-check (armed pass/fail audit): matter-action route vs geometry route on BOTH
    domains + both sides of the seal.  Ambient sigma_ma = (e^{2phi}/4) U'(rho) (D3 potential-only,
    universe_cell_fold_jc_sigma_results.md:75-76); cell sigma_ma = (e^{2phi}/4)(xi rho I_r
    - kap N^2 I_4th / rho^3) (the L2+L4 stress, cell_solver_f2d.py:19).  Geometry route:
    m_MS = (rho/2)(1 - e^{-2phi} rho'^2); eps_geo = m'_MS/(4 pi rho^2 rho') (OFF-SHELL identity,
    derive_universe_einstein_d3.py check 6); sigma_geo from eps (d3 check 5a).  Interior mask
    |rho'| >= 1e-3 max|rho'| (inherited E0 Category-A; the folds are 0/0).
  * tier-a stability instrument = the constraint-reduced (matter-sector, geometry-frozen) ENERGY
    Hessian E_m = INT dr [(xi/2)(rho^2 I_r + I_th + N^2 I_s) + (kap N^2/2)(I_4r + I_4th/rho^2)]
    w.r.t. the u DOF -- NOT the action Hessian.  BANKED MISCLASSIFICATION TRAP: the N=1 build used
    the ACTION Hessian, which is structurally ~90% indefinite even on benign configs and would
    misclassify a genuine cell as unstable (cell_solver_f2d_first_build_results.md:51-66, verifier
    aa88d488); the corrected two-tier formulation with the ENERGY Hessian as tier (a) is banked in
    cell_solver_f2d_N2_results.md:65-104 (S1-S3).  A PD verdict is trustworthy because a
    fixed-background Hessian OVER-counts negatives (gravitating-soliton-stability-test).
  * outputs (characterize, never filter): q (fold), q_p = Z rho_p^2 phi'_p (seal flux, Gauss),
    Delta-phi float vs ln(1101), r_p, r_sU, core depth phi_c, rho_c vs the derived floor.

ANTI-HANG: bounded grids, bounded iterations, single process, no background-poll. GPU (Charles
2026-07-03 addition): dense LM/jacrev linear algebra on the V100 via torch float64 when device=
'cuda'; every GPU run gets CPU spot-checks (harness); NVML warning is benign (banked note);
the banked batched-solve_triangular pitfall is not used anywhere here.

PREMISE LEDGER: inherited UNCHANGED from E1 sec.7 (#1-#17). NEW premises (all Category-A
conditioning, flagged for the E2a report): reference-interval maps + tanh wall map (kmap);
QR/lstsq column-scaled LM; longdouble residual refinement (pure-universe mode); grid sizes;
seed constructions (CHOSE-smoke, reported per run). No new physics premise is introduced.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import json
import math
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

import cell_solver_f2d as F2D                       # banked cell machinery (imported, not forked)

REPO = os.path.dirname(os.path.abspath(__file__))
E0_TABLES = os.path.join(REPO, "microphysics_E0_ambient_tables.json")
LN1101 = math.log(1101.0)                            # anchor magnitude (observational pin, canon)
LN1101_LD = np.log(np.longdouble(1101.0))


# =========================================================================================
# BRACKETS (banked E0 objects; the four pre-committed brackets, guardrail 1)
# =========================================================================================
def load_bracket(label):
    """Load one banked E0 bracket: family, Z, a* (banked; A3 Z=1 was Stage-A budget-cut -> its
    blind-verified fresh value a_reshot is the banked number), dense profiles, banked outputs."""
    with open(E0_TABLES) as fh:
        d = json.load(fh)
    b = d["brackets"][label]
    a_star = b["a_banked"] if b.get("a_banked") is not None else b["a_reshot"]
    return dict(label=label, family=tuple(b["family"]), Z=float(b["Z"]), a_star=float(a_star),
                r_s=float(b["r_s"]), rho_s=float(b["rho_s"]), q=float(b["q"]),
                rho_c=float(b["rho_c"]),
                prof_r=np.array(b["profiles"]["r"]), prof_phi=np.array(b["profiles"]["phi"]),
                prof_rho=np.array(b["profiles"]["rho"]), prof_phip=np.array(b["profiles"]["phip"]),
                prof_rhop=np.array(b["profiles"]["rhop"]))


def make_slice(family, p, xp):
    """T3/Stage-A slice family (CHOSE, banked: cascade_stageA_lib.py:20-36). xp = np or torch.
    A1: U = 2 rho^m exp(-a(rho^2-1));  A3: U = 2 rho^2 (1+b)/(1+b rho^4).  Same formulas as the
    banked numpy functions (cross-checked to machine precision in the harness)."""
    if family[0] == "A1":
        m = family[1]
        def U(rho):  return 2.0 * rho ** m * xp.exp(-p * (rho * rho - 1.0))
        def Up(rho): return (2.0 * rho ** m * xp.exp(-p * (rho * rho - 1.0))) * (m / rho - 2.0 * p * rho)
    elif family[0] == "A3":
        def U(rho):  return 2.0 * rho ** 2 * (1.0 + p) / (1.0 + p * rho ** 4)
        def Up(rho): return 2.0 * (1.0 + p) * (2.0 * rho - 2.0 * p * rho ** 5) / (1.0 + p * rho ** 4) ** 2
    else:
        raise ValueError(f"unknown family {family}")
    return U, Up


# =========================================================================================
# GRIDS / CONTEXT  (cell ctx = the banked f2d ctx; ambient = Cheb + tanh wall map)
# =========================================================================================
def _cheb_ld(Na):
    """Chebyshev-Gauss-Lobatto nodes + d/dzeta in numpy LONGDOUBLE (same construction as
    cell_solver_f2d._cheb = Trefethen cheb with the negative-sum trick; extended precision is a
    Category-A refinement for the pure-universe recovery mode)."""
    n = Na - 1
    x = np.cos(np.pi * np.arange(n + 1, dtype=np.longdouble) / n)
    cc = np.ones(n + 1, dtype=np.longdouble); cc[0] = 2.0; cc[n] = 2.0
    cc *= (-1.0) ** np.arange(n + 1)
    X = np.tile(x, (n + 1, 1)).T
    dX = X - X.T
    D = np.outer(cc, 1.0 / cc) / (dX + np.eye(n + 1, dtype=np.longdouble))
    D = D - np.diag(D.sum(axis=1))
    idx = np.arange(n, -1, -1)
    return x[idx], D[np.ix_(idx, idx)]


def make_ctx_comp(Nr, Nth, Na, kmap=2.5, device="cpu"):
    """Composite context: cell ctx (banked f2d construction, on `device`) + ambient Cheb grid with
    the tanh wall-clustered map h (kmap=0 -> affine).  All Category-A conditioning choices."""
    cell = F2D.make_ctx(Nr, Nth, rc=0.0, device=device)      # rc is a pure label in f2d (unused)
    z_ld, Dz_ld = _cheb_ld(Na)
    k = np.longdouble(kmap)
    if kmap > 0:
        h_ld = np.tanh(k * (z_ld + 1) / 2) / np.tanh(k)
        hp_ld = (k / 2) / np.cosh(k * (z_ld + 1) / 2) ** 2 / np.tanh(k)
    else:
        h_ld = (z_ld + 1) / 2
        hp_ld = 0.5 * np.ones_like(z_ld)
    tt = lambda a: torch.as_tensor(np.asarray(a, dtype=float), dtype=torch.float64, device=device)
    return dict(cell=cell, Nr=Nr, Nth=Nth, Na=Na, kmap=float(kmap), device=device,
                za=tt(z_ld), Da=tt(Dz_ld), ha=tt(h_ld), hpa=tt(hp_ld),
                za_ld=z_ld, Da_ld=Dz_ld, ha_ld=h_ld, hpa_ld=hp_ld)


# =========================================================================================
# AMBIENT BLOCK (backend-generic: torch for the composite/Jacobian, numpy-longdouble for the
# extended-precision pure-universe refinement; SAME formulas, cross-checked in the harness)
# EOMs = cell_solver_universe_T3.py:18-20 (banked; CAS-matched, E1 K0a):
#   phi'' = 4 e^{-2phi} rho'^2/(Z rho^2) - 2 phi' rho'/rho
#   rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2 + (e^{2phi}/4) U'(rho)
# H_amb  = (Z/2) rho^2 phi'^2 - 2 e^{-2phi} rho'^2 - 2 + U(rho)   (T3:119; E1 K2a)
# =========================================================================================
def amb_block(ph, rh, r_lo, r_hi, D, hp, Z, U, Up, xp):
    """Return dict of ambient node quantities. d/dr = D/(L*hp) with L = r_hi - r_lo (the map
    r = r_lo + L*h(zeta)). xp = torch | np (longdouble)."""
    L = r_hi - r_lo
    dd = (lambda f: (D @ f) / (L * hp))
    php = dd(ph); phpp = dd(php)
    rhp = dd(rh); rhpp = dd(rhp)
    e2m = xp.exp(-2.0 * ph); e2p = xp.exp(2.0 * ph)
    r_phi = phpp - (4.0 * e2m * rhp ** 2 / (Z * rh ** 2) - 2.0 * php * rhp / rh)
    r_rho = rhpp - (2.0 * php * rhp - (Z / 4.0) * rh * e2p * php ** 2 + 0.25 * e2p * Up(rh))
    H = (Z / 2.0) * rh ** 2 * php ** 2 - 2.0 * e2m * rhp ** 2 - 2.0 + U(rh)
    return dict(php=php, rhp=rhp, r_phi=r_phi, r_rho=r_rho, H=H, e2p=e2p, e2m=e2m)


# =========================================================================================
# COMPOSITE PACK / UNPACK / RESIDUAL
#   v = [ phi_cell(Nr), rho_cell(Nr), u(Nr*Nth), phi_amb(Na), rho_amb(Na), r_p, r_sU ]
# =========================================================================================
def pack_comp(phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU, device="cpu"):
    sc = lambda x: torch.as_tensor([float(x)], dtype=torch.float64, device=device)
    return torch.cat([phi_c.reshape(-1), rho_c.reshape(-1), uf.reshape(-1),
                      phi_a.reshape(-1), rho_a.reshape(-1), sc(r_p), sc(r_sU)])


def unpack_comp(v, ctx):
    Nr, Nth, Na = ctx["Nr"], ctx["Nth"], ctx["Na"]
    i = 0
    phi_c = v[i:i + Nr]; i += Nr
    rho_c = v[i:i + Nr]; i += Nr
    uf = v[i:i + Nr * Nth].reshape(Nr, Nth); i += Nr * Nth
    phi_a = v[i:i + Na]; i += Na
    rho_a = v[i:i + Na]; i += Na
    return phi_c, rho_c, uf, phi_a, rho_a, v[i], v[i + 1]


def cell_fields(v, ctx, prm):
    """Evaluate the BANKED cell evaluator on the composite state: v_cell = [phi,rho,u,L=r_p]
    (torch.cat keeps autodiff through r_p; f2d.fields uses only L, never rc)."""
    phi_c, rho_c, uf, _, _, r_p, _ = unpack_comp(v, ctx)
    v_cell = torch.cat([phi_c, rho_c, uf.reshape(-1), r_p.reshape(1)])
    return F2D.fields(v_cell, ctx["cell"], prm), v_cell


def E_ang_seal(Q, prm):
    """E_ang(r_p) = (xi/2)(I_th + N^2 I_s) + (kap N^2/2) I_4th/rho^2 at the seal node (E1 sec.0)."""
    Z, XI, KAP, N = prm
    return ((XI / 2.0) * (Q["Ith"][-1] + N ** 2 * Q["Is"][-1])
            + (KAP * N ** 2 / 2.0) * Q["I4th"][-1] / Q["rho"][-1] ** 2)


def residual_comp(v, ctx, prm, bracket, a_star=None):
    """THE monolithic composite residual (SQUARE: 2Nr + Nr*Nth + 2Na + 2 rows). Row order:
    [cell phi-ODE int | cell rho-ODE int | f-PDE int | core phi',rho' | core f_r | seal C1c f_r |
     amb phi-ODE int | amb rho-ODE int | seal [phi],[rho],C1a,C1b,C2 | fold phi, rho', H_amb]."""
    Z, XI, KAP, N = prm
    if a_star is None:
        a_star = bracket["a_star"]                    # bracket-level anchor (E1 ledger #5, CHOSE)
    U, Up = make_slice(bracket["family"], a_star, torch)
    phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = unpack_comp(v, ctx)
    Q, _ = cell_fields(v, ctx, prm)
    A = amb_block(phi_a, rho_a, r_p, r_sU, ctx["Da"], ctx["hpa"], Z, U, Up, torch)
    rows = [
        Q["phi_ode"][1:-1],                           # cell phi-ODE (interior)
        Q["rho_ode"][1:-1],                           # cell rho-ODE (interior)
        Q["res_f"][1:-1].reshape(-1),                # f-PDE (interior r, all theta)
        Q["phip"][0].reshape(1),                      # core natural phi'(0)=0
        Q["rhop"][0].reshape(1),                      # core natural rho'(0)=0
        Q["fr"][0, :],                                # core natural f_r(0,theta)=0
        Q["fr"][-1, :],                               # C1c: f_r(r_p,theta)=0 (DERIVED, K1')
        A["r_phi"][1:-1],                             # ambient phi-ODE (interior)
        A["r_rho"][1:-1],                             # ambient rho-ODE (interior)
        (Q["phi"][-1] - phi_a[0]).reshape(1),         # [phi]=0 (continuity posture, ledger #9)
        (Q["rho"][-1] - rho_a[0]).reshape(1),         # [rho]=0
        (Q["phip"][-1] - A["php"][0]).reshape(1),     # C1a [pi_phi]=0 (shared Z,rho,phi => phi' match)
        (Q["rhop"][-1] - A["rhp"][0]).reshape(1),     # C1b [pi_rho]=0
        (E_ang_seal(Q, prm) - U(rho_a[0])).reshape(1),# C2 collapsed (K4)
        phi_a[-1].reshape(1),                         # fold odd pin phi(r_sU)=0
        A["rhp"][-1].reshape(1),                      # fold rho'(r_sU)=0
        A["H"][-1].reshape(1),                        # fold transversality H_amb(r_sU)=0
    ]
    return torch.cat([r.reshape(-1) for r in rows])


# =========================================================================================
# PURE-UNIVERSE MODE (carrier off, cell domain removed; the criterion-2 recovery object).
# Unknowns w = [phi(Na), rho(Na), r_sU, a]; SQUARE 2Na+2:
#   interior ODEs 2(Na-2); core fold phi'=rho'=0; anchor phi(0)=-ln1101 (the pure cell's pin);
#   critical closure U(rho(0)) = 2 (THEORY: transversality closure -- rho_c = 1 must EMERGE);
#   fold phi=0, rho'=0.  H_amb(fold) is NOT imposed (it is implied: H(0) = U(rho_c)-2 = 0 +
#   conservation) -- it is a free gate here, exactly the non-vacuousness the harness checks.
# =========================================================================================
def residual_pure(w, ctx, bracket, xp):
    Na = ctx["Na"]
    Z = bracket["Z"] if xp is torch else np.longdouble(bracket["Z"])
    D = ctx["Da"] if xp is torch else ctx["Da_ld"]
    hp = ctx["hpa"] if xp is torch else ctx["hpa_ld"]
    ph = w[:Na]; rh = w[Na:2 * Na]; r_sU = w[2 * Na]; a = w[2 * Na + 1]
    U, Up = make_slice(bracket["family"], a, xp)
    zero = r_sU * 0.0
    A = amb_block(ph, rh, zero, r_sU, D, hp, Z, U, Up, xp)
    anchor = ph[0] + (LN1101 if xp is torch else LN1101_LD)
    if xp is torch:
        rows = [A["r_phi"][1:-1], A["r_rho"][1:-1],
                A["php"][0].reshape(1), A["rhp"][0].reshape(1),
                anchor.reshape(1), (U(rh[0]) - 2.0).reshape(1),
                ph[-1].reshape(1), A["rhp"][-1].reshape(1)]
        return torch.cat(rows)
    return np.concatenate([A["r_phi"][1:-1], A["r_rho"][1:-1],
                           A["php"][0:1], A["rhp"][0:1],
                           [anchor], [U(rh[0]) - 2.0], ph[-1:], A["rhp"][-1:]])


def seed_pure(ctx, bracket, a_pert=1e-3):
    """Seed from the banked E0 dense profile (linear interp onto the mapped grid) with a* DELIBERATELY
    perturbed by a_pert rel -- the recovery must PULL a* back (attraction, not mere holding)."""
    h = np.asarray(ctx["ha_ld"], dtype=float)
    rn = bracket["r_s"] * h
    ph = np.interp(rn, bracket["prof_r"], bracket["prof_phi"])
    rh = np.interp(rn, bracket["prof_r"], bracket["prof_rho"])
    return np.concatenate([ph, rh, [bracket["r_s"]], [bracket["a_star"] * (1.0 + a_pert)]]
                          ).astype(np.longdouble)


# =========================================================================================
# LM DRIVER (Category-A; QR/lstsq trust steps on the column-scaled augmented system; optional
# extended-precision residual path). Anti-hang: maxit + wall-clock budget, single process.
# =========================================================================================
def lm_qr(resfn_t, w0, maxit=60, lam0=1e-6, tol=1e-24, time_budget=300.0, resfn_hp=None,
          device="cpu", verbose=False, hist_out=None):
    """resfn_t : torch residual (float64, on `device`) -- used for the Jacobian (jacrev) and, if
    resfn_hp is None, for the residual too.  resfn_hp : optional numpy-longdouble residual (same
    formulas) -- when given, w lives in longdouble and Phi is evaluated in extended precision.
    Returns (w_final [np.longdouble], info dict)."""
    import time
    from torch.func import jacrev
    t0 = time.time()
    w = np.asarray(w0, dtype=np.longdouble).copy()
    n = w.size
    evalF = (lambda ww: resfn_hp(ww)) if resfn_hp is not None else \
            (lambda ww: resfn_t(torch.as_tensor(ww.astype(float), device=device)
                                ).detach().cpu().numpy().astype(np.longdouble))
    F = evalF(w); Phi = float((F * F).sum())
    lam = lam0; nit = 0; hist = [Phi]
    for it in range(maxit):
        nit = it + 1
        if Phi < tol or (time.time() - t0) > time_budget:
            break
        wt = torch.as_tensor(w.astype(float), device=device)
        J = jacrev(resfn_t)(wt).detach()
        colscale = J.abs().amax(dim=0).clamp(min=1e-30)
        Js = J / colscale
        Ft = torch.as_tensor(F.astype(float), device=device)
        eye = torch.eye(n, dtype=torch.float64, device=device)
        zer = torch.zeros(n, dtype=torch.float64, device=device)
        accepted = False
        for _try in range(40):
            Aug = torch.cat([Js, math.sqrt(lam) * eye], 0)
            rhs = torch.cat([-Ft, zer])
            dxs = torch.linalg.lstsq(Aug, rhs.unsqueeze(1)).solution.squeeze(1)
            dx = (dxs / colscale).cpu().numpy().astype(np.longdouble)
            wn = w + dx
            try:
                Fn = evalF(wn); Pn = float((Fn * Fn).sum())
            except Exception:
                Pn = float("inf")
            if math.isfinite(Pn) and Pn < Phi:
                w = wn; F = Fn; Phi = Pn
                lam = max(lam / 3.0, 1e-18); accepted = True
                break
            lam = min(lam * 2.0, 1e10)
        hist.append(Phi)
        if verbose:
            print(f"  [lm-qr] it={it:3d} Phi={Phi:.6e} lam={lam:.2e} "
                  f"{'acc' if accepted else 'STALL'}", flush=True)
        if not accepted:
            break
    if hist_out is not None:
        hist_out.extend(hist)
    return w, dict(Phi=Phi, iters=nit, hist=hist, wall=time.time() - t0)


def solve_pure_universe(label, Na=288, kmap=2.5, a_pert=1e-3, maxit=140, device="cpu",
                        time_budget=300.0, verbose=False):
    """Criterion-2 recovery: pure-universe limit of the composite machinery on one bracket.
    Returns dict with recovered a*, r_sU, q, rho_s + gates (H drift, H(fold)) + banked deltas."""
    bracket = load_bracket(label)
    ctx = make_ctx_comp(4, 4, Na, kmap=kmap, device=device)   # cell ctx unused in this mode
    w0 = seed_pure(ctx, bracket, a_pert=a_pert)
    res_t = lambda ww: residual_pure(ww, ctx, bracket, torch)
    res_hp = lambda ww: residual_pure(ww, ctx, bracket, np)
    w, info = lm_qr(res_t, w0, maxit=maxit, resfn_hp=res_hp, device=device,
                    time_budget=time_budget, verbose=verbose)
    Na_ = ctx["Na"]
    ph = w[:Na_]; rh = w[Na_:2 * Na_]; r_sU = float(w[2 * Na_]); a_rec = float(w[2 * Na_ + 1])
    Z = np.longdouble(bracket["Z"])
    U, Up = make_slice(bracket["family"], w[2 * Na_ + 1], np)
    A = amb_block(ph, rh, np.longdouble(0.0), w[2 * Na_], ctx["Da_ld"], ctx["hpa_ld"],
                  Z, U, Up, np)
    q = float(Z * rh[-1] ** 2 * A["php"][-1])
    return dict(label=label, Na=Na_, kmap=kmap, Phi=info["Phi"], iters=info["iters"],
                wall=info["wall"],
                a_rec=a_rec, a_banked=bracket["a_star"],
                a_rel_err=(a_rec - bracket["a_star"]) / bracket["a_star"],
                r_sU=r_sU, r_s_banked=bracket["r_s"], dr_s=r_sU - bracket["r_s"],
                q=q, q_banked=bracket["q"], dq=q - bracket["q"],
                rho_s=float(rh[-1]), rho_s_banked=bracket["rho_s"],
                drho_s=float(rh[-1]) - bracket["rho_s"],
                rho_c=float(rh[0]),                       # must EMERGE ~= 1 (not imposed)
                H_drift=float(np.abs(A["H"]).max()),      # free gate (H not imposed in this mode)
                H_fold=float(A["H"][-1]),
                w=w, ctx=ctx, bracket=bracket)


# =========================================================================================
# GATES / INSTRUMENTS  (characterize, never filter; provenance+honesty only)
# =========================================================================================
def gates_comp(v, ctx, prm, bracket, a_star=None):
    """Full instrument set on a composite state (any state -- gates must read ~0 only on true
    solutions and NONZERO off them; the harness demonstrates both directions)."""
    Z, XI, KAP, N = prm
    if a_star is None:
        a_star = bracket["a_star"]
    U, Up = make_slice(bracket["family"], a_star, torch)
    phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = unpack_comp(v, ctx)
    Q, v_cell = cell_fields(v, ctx, prm)
    A = amb_block(phi_a, rho_a, r_p, r_sU, ctx["Da"], ctx["hpa"], Z, U, Up, torch)
    Hc = F2D.H_of_r(v_cell, ctx["cell"], prm)             # H_cell(r) -- the ==0 consistency gate
    Sa, Sb, dS = F2D.derrick(v_cell, ctx["cell"], prm)
    tax = float(4.0 * torch.exp(-2.0 * Q["phi"][-1]) * Q["rhop"][-1] * Q["rho"][-1])
    sig_cell = sigma_two_route_cell(v, ctx, prm)
    sig_amb = sigma_two_route_amb(v, ctx, prm, bracket, a_star)
    return dict(
        H_cell_max=float(Hc.abs().max()), H_cell_seal=float(Hc[-1]),
        H_cell_drift=float(Hc.max() - Hc.min()),
        H_amb_max=float(A["H"].abs().max()), H_amb_seal=float(A["H"][0]),
        H_amb_drift=float(A["H"].max() - A["H"].min()),
        derrick_Sa=Sa, derrick_Sb=Sb,
        matched_derrick_gate=dS + tax,                    # (Sa-Sb) + 4 e^{-2phi_p} rho'_p rho_p
        tax=tax,
        sigma_cell=sig_cell, sigma_amb=sig_amb,
        E_ang_core=float((XI / 2.0) * (Q["Ith"][0] + N ** 2 * Q["Is"][0])
                         + (KAP * N ** 2 / 2.0) * Q["I4th"][0] / Q["rho"][0] ** 2),
        E_ang_seal=float(E_ang_seal(Q, prm)),
        q_fold=float(Z * rho_a[-1] ** 2 * A["php"][-1]),
        q_seal=float(Z * rho_a[0] ** 2 * A["php"][0]),
        dphi_float=float(-phi_c[0]),                      # composite Delta-phi (REPORTED, ledger #5)
        dphi_anchor_gap=float(-phi_c[0]) - LN1101,
        r_p=float(r_p), r_sU=float(r_sU),
        phi_core=float(phi_c[0]), rho_core=float(rho_c[0]),
        rho_c_floor=float(N * math.sqrt(KAP / (2.0 * (2.0 - XI * N)))) if XI * N < 2 else float("nan"),
    )


def _sigma_geo_from_profile(rr, phi, phip, rho, rhop, D_over_L, Z):
    """Geometry-route sigma on one domain (torch). m_MS=(rho/2)(1-e^{-2phi}rho'^2); m'_MS by the
    domain's spectral derivative; eps = m'/(4 pi rho^2 rho'); sigma from eps (d3 check 5a).
    Returns (sigma_geo, mask) -- mask excludes |rho'| < 1e-3 max (0/0 folds; E0 Category-A)."""
    e2m = torch.exp(-2.0 * phi); e2p = torch.exp(2.0 * phi)
    mMS = 0.5 * rho * (1.0 - e2m * rhop ** 2)
    mp = D_over_L(mMS)
    eps = mp / (4.0 * math.pi * rho ** 2 * rhop)
    sig = 0.5 * rho * e2p * (1.0 / rho ** 2 - e2m * (rhop ** 2 / rho ** 2 + 2.0 * phip * rhop / rho)
                             + 0.5 * Z * phip ** 2 - 8.0 * math.pi * eps)
    mask = rhop.abs() >= 1e-3 * rhop.abs().max()
    return sig, mask


def sigma_two_route_cell(v, ctx, prm):
    """sigma cross-check, CELL domain: matter route = (e^{2phi}/4)(xi rho I_r - kap N^2 I_4th/rho^3)
    (the L2+L4 stress, f2d rho-EOM source) vs geometry route from the profile."""
    Z, XI, KAP, N = prm
    Q, v_cell = cell_fields(v, ctx, prm)
    r_p = v[-2]
    Dc = ctx["cell"]["Dz"]
    dd = lambda f: (2.0 / r_p) * (Dc @ f)
    sig_ma = 0.25 * Q["e2p"] * (XI * Q["rho"] * Q["Ir"] - KAP * N ** 2 * Q["I4th"] / Q["rho"] ** 3)
    sig_geo, mask = _sigma_geo_from_profile(None, Q["phi"], Q["phip"], Q["rho"], Q["rhop"], dd, Z)
    scale = float(sig_ma.abs().max().clamp(min=1e-300))
    rel = ((sig_geo - sig_ma).abs() / scale)[mask]
    return dict(max_rel=float(rel.max()) if rel.numel() else float("nan"),
                n_masked=int(mask.sum()),
                seal_ma=float(sig_ma[-1]), seal_geo=float(sig_geo[-1]), scale=scale)


def sigma_two_route_amb(v, ctx, prm, bracket, a_star=None):
    """sigma cross-check, AMBIENT domain: matter route = (e^{2phi}/4) U'(rho) (D3 potential-only)
    vs geometry route from the profile."""
    Z = prm[0]
    if a_star is None:
        a_star = bracket["a_star"]
    U, Up = make_slice(bracket["family"], a_star, torch)
    _, _, _, phi_a, rho_a, r_p, r_sU = unpack_comp(v, ctx)
    L = r_sU - r_p
    dd = lambda f: (ctx["Da"] @ f) / (L * ctx["hpa"])
    php = dd(phi_a); rhp = dd(rho_a)
    sig_ma = 0.25 * torch.exp(2.0 * phi_a) * Up(rho_a)
    sig_geo, mask = _sigma_geo_from_profile(None, phi_a, php, rho_a, rhp, dd, Z)
    scale = float(sig_ma.abs().max().clamp(min=1e-300))
    rel = ((sig_geo - sig_ma).abs() / scale)[mask]
    return dict(max_rel=float(rel.max()) if rel.numel() else float("nan"),
                n_masked=int(mask.sum()),
                seal_ma=float(sig_ma[0]), seal_geo=float(sig_geo[0]), scale=scale)


def energy_hessian_tier_a(v, ctx, prm):
    """Tier-(a) stability instrument: the constraint-reduced (matter-sector, geometry-frozen)
    ENERGY Hessian -- E_m = INT dr [(xi/2)(rho^2 I_r + I_th + N^2 I_s) + (kap N^2/2)(I_4r +
    I_4th/rho^2)] w.r.t. the u DOF only.  This is deliberately NOT the action Hessian: the action
    Hessian is structurally ~90% indefinite on benign configs and misclassifies (BANKED:
    cell_solver_f2d_first_build_results.md:51-66 verifier aa88d488; corrected formulation banked
    cell_solver_f2d_N2_results.md:65-104 S1-S3).  PD => stable is trustworthy (fixed-background
    Hessians OVER-count negatives; gravitating-soliton-stability-test).  Returns eigenvalues."""
    Z, XI, KAP, N = prm
    phi_c, rho_c, uf, _, _, r_p, _ = unpack_comp(v, ctx)
    phi_f = phi_c.detach(); rho_f = rho_c.detach(); rp_f = r_p.detach()
    ccw = ctx["cell"]["ccw"]

    def E_m(u_flat):
        v_cell = torch.cat([phi_f, rho_f, u_flat, rp_f.reshape(1)])
        Q = F2D.fields(v_cell, ctx["cell"], prm)
        dens = ((XI / 2.0) * (Q["rho"] ** 2 * Q["Ir"] + Q["Ith"] + N ** 2 * Q["Is"])
                + (KAP * N ** 2 / 2.0) * (Q["I4r"] + Q["I4th"] / Q["rho"] ** 2))
        return (ccw * dens).sum() * (rp_f / 2.0)

    H = torch.func.hessian(E_m)(uf.reshape(-1).detach())
    H = 0.5 * (H + H.T)
    return torch.linalg.eigvalsh(H)


# =========================================================================================
# COMPOSITE SEED  (rigid + bulge perturbation; all values CHOSE-smoke, reported per run)
# =========================================================================================
def seed_comp(ctx, bracket, rp0, amp=0.5, rho_cell0=None, device="cpu"):
    """Ambient: banked E0 profile interpolated onto [rp0, r_s_banked] (mapped grid).  Cell: flat
    phi = phi_loc(rp0), rho = rho_loc(rp0) (continuity-consistent flats), u = rigid + bulge
    amp*(1-mu^2)*sin(pi(zeta+1)/2) (pole-safe; f_r=0 NOT pre-imposed at the seal -- Newton owns
    C1c).  The bulge theorem (E1 P3) says any solution is non-perturbative in theta: amp is a
    genuine coverage knob (CHOSE-smoke)."""
    Nr, Nth, Na = ctx["Nr"], ctx["Nth"], ctx["Na"]
    h = np.asarray(ctx["ha_ld"], dtype=float)
    rsU0 = bracket["r_s"]
    rn = rp0 + (rsU0 - rp0) * h
    phi_a = np.interp(rn, bracket["prof_r"], bracket["prof_phi"])
    rho_a = np.interp(rn, bracket["prof_r"], bracket["prof_rho"])
    phi_loc = float(np.interp(rp0, bracket["prof_r"], bracket["prof_phi"]))
    rho_loc = float(np.interp(rp0, bracket["prof_r"], bracket["prof_rho"]))
    if rho_cell0 is None:
        rho_cell0 = rho_loc
    zeta = ctx["cell"]["zeta"].cpu().numpy(); mu = ctx["cell"]["mu"].cpu().numpy()
    uf = amp * (1.0 - mu[None, :] ** 2) * np.sin(np.pi * (zeta[:, None] + 1.0) / 2.0)
    tt = lambda a: torch.as_tensor(np.asarray(a, dtype=float), dtype=torch.float64, device=device)
    return pack_comp(tt(np.full(Nr, phi_loc)), tt(np.full(Nr, rho_cell0)), tt(uf),
                     tt(phi_a), tt(rho_a), rp0, rsU0, device=device)


if __name__ == "__main__":
    # assembly sanity only (NO solve; the harness + smoke script own everything heavier)
    lab = "A1 m=3 Z=8"
    br = load_bracket(lab)
    ctx = make_ctx_comp(8, 8, 48, kmap=2.5)
    prm = (br["Z"], 0.5, 0.1, 1)
    v0 = seed_comp(ctx, br, rp0=100.0, amp=0.5)
    F = residual_comp(v0, ctx, prm, br)
    print(f"composite assembly: unknowns={v0.numel()} rows={F.numel()} square={v0.numel()==F.numel()}"
          f" all-finite={bool(torch.isfinite(F).all())} maxabs={float(F.abs().max()):.3e}")

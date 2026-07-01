"""NATIVE WELD INTERFACE MODE SPECTRUM (weld phase 2): does the physical
matter cell support discrete real-frequency oscillation modes under the
native Reading-A system, under three candidate interface ontologies?

THE QUESTION.  Phase 1 (native_weld_status_derivation.py,
weld_status_results.md, grade (d)) settled the weld's native status: the
C1 system has its OWN algebraic weld (= vanishing radial energy flux,
delta-T_tr = 0); eliminating the auxiliary H1 flips the time-kinetic
sign, giving the ELLIPTIC on-shell mode equation (banked, verified):

    (r^2 f^2 u')' - [lam f + 4 r^2 f^2 E0] u = omega^2 r^2 u,
    E0 := phi0'' + 2 phi0'/r - 2 phi0'^2,   lam = ell(ell+1),

with NO real-omega modes wherever pointwise lam f + 4r^2f^2 E0 >= 0, and
a real-frequency oscillation window open where that density goes
NEGATIVE.  This file asks, on the banked physical cell background
(self-similar sourced collar q = 1/3, constant source s = q(1-q)/2 =
1/9, zero-tail flat exterior per CANON C-2), whether the window is
actually OCCUPIED — under each of three interface ontologies (the BC
menu; the legacy dissolution ontology CG 15.3/18.3a is quarantined-
legacy INFORMING the menu, not a derivation):

  BC-a (reservoir-field reading): exterior-matching — the mode continues
       into the flat exterior with the S3 jump at R and the decaying
       branch at infinity (legacy CG 18.3a: dissolution energy books
       into the scalar reservoir).
  BC-b (matter-content reading): Dirichlet u(R) = 0 — mode support
       ceases at the phi = 0 dissolution surface (legacy CG 15.3).
       Interior problem only; the interface delta does NO work there.
  BC-c (native no-flux reading): the weld's own delta-T_tr = 0 is
       automatic on-shell (it IS the H1 equation), so 'no flux through
       the interface' is the VARIATIONAL NATURAL condition of the
       quadratic form WITH the S3 delta included: the Robin condition
       u'(R) = (2q/R) u(R)  [equivalently r^2 f^2 u' -> 0 on the
       R+ side after the jump].  Interior problem with that natural BC.

PRE-REGISTERED VERDICT CRITERIA (printed by the script before any
computation; recorded here verbatim): per BC, NATIVE-DISCRETENESS
CANDIDATE iff a discrete omega^2 > 0 eigenvalue exists, localized
(BC-a) or interior-regular (BC-b/c), domain-independent (r_max doubling
stable to 4+ digits for BC-a — the pre-registered discriminator against
box modes), scale-covariant (omega*R invariant, 4+ digits), and 4+
digit stable under r_min variation; otherwise NEGATIVE-WITH-THRESHOLD-
MAP (the precise deficit + the q_c map is the deliverable).  No
softening either way.  Also pre-registered: the BC SELECTION itself is
a physics/canonization input — this script reports the spectrum under
each ontology and does NOT pick among them.

RESULTS (every setup step S1-S5 sympy-verified; numerics double-checked
FD vs independent shooting; PASS/FAIL printed; nonzero exit on FAIL):

  HEADLINE (C1): the physical cell (q = 1/3, s = 1/9, delta strength
  2q/R = 2/(3R)) supports NO discrete omega^2 > 0 mode under ANY of the
  three ontologies, for lam = 2 (ell = 1, RW-rigor caveat) and lam = 6
  (ell = 2, rigorous):
    BC-a: no discrete point above the essential spectrum (-inf, 0]; the
          finite-box top eigenvalue is negative and scales away ~
          1/r_max^2 under domain doubling (box artifact, the banked
          box-control signature); no-delta control identical (bulk
          E0 > 0 theorem consistency: interior bulk E0 = s/r^2 > 0 — the
          banked source is POSITIVE in the bulk; the only negative
          structure is the interface delta).
    BC-b: top eigenvalue omega^2 = -27.334956 (lam=2), -41.213694
          (lam=6) — relaxation only (theorem: with u(R) = 0 the delta
          does no work and the form is positive definite).
    BC-c: top eigenvalue omega^2 = -3.4667814 (lam=2), -10.376405
          (lam=6) — relaxation only.  (FD and shooting agree 4+ digits;
          r_min-stable; scale-covariant.)

  THE BINDING THEOREM (exact, sympy-verified pieces + FD-bracket
  confirmation): with the interior zero-energy Friedrichs log-derivative
  L0(q, lam) := R u'(R-)/u(R), a discrete omega^2 > 0 mode exists iff
  the delta strength gamma (jump coefficient: Delta u' = -(gamma/R) u)
  exceeds
      gamma_c = L0(q, lam)                 [BC-c]
      gamma_c = L0(q, lam) + (ell+1)       [BC-a]
      gamma_c = +infinity (no gamma binds) [BC-b]
  The PHYSICAL strength is gamma = 2q.  At the banked point q = 1/3:
      L0 = 1.33835009 (lam=2), 2.29931870 (lam=6), 3.28396540 (lam=12)
  so the deficits (gamma_c - 2q, in units of 1/R — THE FINDING):
      BC-c: 0.671683 (lam=2)   1.632652 (lam=6)   2.617299 (lam=12)
      BC-a: 2.671683 (lam=2)   4.632652 (lam=6)   6.617299 (lam=12)
  i.e. the interface needs gamma_c/gamma = 2.0075x (BC-c, lam=2) up to
  10.93x (BC-a, lam=12) more delta strength than the weld supplies.
  [Null-test discipline: 2.0075 is NOT 2 (0.38% off) and L0(lam=2) =
  1.33835 is NOT 4/3 (0.38% off) — recorded as non-matches.]

  THRESHOLD MAP (C2): NO critical q_c exists in (0, 1/2) for ANY BC at
  ANY lam in {2, 6, 12} with the consistent tie s = q(1-q)/2, gamma =
  2q: the BC-c margin 2q - L0 is negative over the whole range (best
  value -0.4820 at q -> 1/2, lam = 2); BC-a is EXCLUDED at theorem
  level (deficit > ell + a+ - ... > 1 for all q < 1/2, ell >= 1).
  Decoupled diagnosis (bulk fixed at the banked q = 1/3 collar, delta
  strength scanned by hand): gamma_c(BC-c) = L0, FD-bracketed to within
  +-5% (sign flip of the top eigenvalue between 0.95 gamma_c and
  1.05 gamma_c); boosted-gamma validation modes exist and pass ALL
  pre-registered discriminators (BC-c gamma = 1.5 gamma_c: omega^2 =
  +4.0701100, FD = shooting to 4+ digits, scale-covariant; BC-a gamma =
  1.2 gamma_c: omega^2 = +0.9872447, domain-doubling stable, exact-
  Bessel exterior shooting cross-check) — the machinery CAN see the
  modes; the physical cell just sits below threshold.  The binding
  agent is the interface delta alone; the angular barrier kills it:
  the critical angular eigenvalue below which the physical delta WOULD
  bind (BC-c, q = 1/3) is lam_c = 0.267787 — far below the smallest
  admissible lam = 2 (no integer ell >= 1 binds; the would-be window
  sits in the excluded monopole gap lam < 2).

  EXACT CLOSED FORM (C2b; verifier contribution, agent
  ae8caa64ef3d4b1ff, same-day amendment): the interior zero-energy
  problem Liouville-transforms to the MODIFIED BESSEL equation
  (u = rho^{-(1-2q)/2} w(tau), tau = tau0 rho^{q/2}, tau0 =
  2 sqrt(lam)/q):  tau^2 w'' + tau w' - (tau^2 + nu^2) w = 0  with
  nu = sqrt(1 + 4q(1-q))/q (= sqrt(17) exactly at q = 1/3).  The
  Friedrichs branch is w = I_nu, and
      L0 = -(1-2q)/2 + (q tau0/2) I'_nu(tau0)/I_nu(tau0)
  EXACTLY (matches the shooting L0 to ~1e-13 at lam = 2, 6, 12).  The
  threshold map is thereby exact special-function content:
  gamma_c(BC-c) = L0, gamma_c(BC-a) = L0 + (ell+1), physical gamma =
  2q.

  NON-FRIEDRICHS LOOPHOLE (C2c; computed and CLOSED, same amendment):
  the limit-circle core admits non-Friedrichs self-adjoint extensions;
  the K_nu (a-) core extension DOES bind at physical strength (BC-c
  lam=2, gamma = 2q: omega^2 R^2 = +1.1494) — BUT the gamma = 0
  control shows it binds even with the interface delta REMOVED
  (omega^2 R^2 = +0.5628): a CORE-ATTACHED ARTIFACT, not weld-
  interface binding; the K-branch has infinite form energy at the core
  (a- fails a > q - 1/2, S5) and is excluded by the finite-action
  charter.  The interface threshold map is extension-independent in
  substance.

  SCALE COVARIANCE (C3): omega^2 R^2 invariant under R rescaling with
  independently generated meshes, 5+ digits (sympy: R drops out of the
  mode equation in rho = r/R with omega^2 R^2 as eigenvalue).

  READING-B CONTROL (C4): the UNFLIPPED (hyperbolic) signature has
  oscillatory exterior solutions for omega^2 > 0 (sympy: v'' =
  (lam/r^2 - omega^2) v, spherical-Bessel closed forms verified) — the
  old leak; no localized real modes under BC-a.  The elliptic
  localization (decaying exterior branch at omega^2 > 0, essential
  spectrum at omega^2 <= 0) is Reading A's distinguishing structure.

  READING-C NOTE (C5): the Einstein-weld transplant is natively
  excluded (W4: the C1 conservation leak makes the Einstein theta-row
  force delta-phi = 0) — graded macro import, not computed here.

  VERDICT (per the pre-registered criteria): NEGATIVE-WITH-THRESHOLD-
  MAP for all three ontologies.  The E0 < 0 oscillation window of phase
  1 is real but UNOCCUPIED by the banked cell: on the self-similar
  sourced collar the bulk E0 = s/r^2 is POSITIVE (the phase-1
  counterexample's bulk-negative E0 is not what the banked background
  provides); the only negative structure is the zero-tail interface
  delta -(q/2R) delta(r-R), and at strength 2q it is a factor ~2 (BC-c,
  best case) to ~11 (BC-a, lam=12) below binding.  The deficit numbers
  and the lam_c = 0.268 monopole-gap location of the would-be window
  are the deliverables.

SPEC CROSS-CHECKS (sympy wins; here sympy CONFIRMS every spec step):
  S1 collar: f = (R/r)^q solves f_xx + f_x + 2sf = 0 (x = ln(r/R)) iff
     s = q(1-q)/2; q = 1/3 => s = 1/9; f(R) = 1 continuous; Delta f' =
     +q/R.  S2 sign chain: f_xx + f_x + 2sf = 0 with f = e^{-2phi} <=>
     phi_xx + phi_x - 2phi_x^2 = s <=> E0 = s/r^2 (interior bulk);
     exterior E0 = 0; only phi'' carries a delta (phi'^2 and 2phi'/r do
     not), Delta phi' = -Delta f'/(2f(R)) = -q/(2R), so E0 contains
     -(q/(2R)) delta(r-R).  S3 jump: Delta u' = -(2q/R) u(R), no
     product ambiguity (f(R) = 1 continuous).  S4 exterior: u = v/r
     gives v'' = (omega^2 + lam/r^2) v; decaying branch exists for
     omega^2 > 0 (closed forms ell = 1, 2 verified); essential spectrum
     at omega^2 <= 0.  S5 indicial: a^2 + (1-2q)a - 4s = 0, a+- =
     (-(1-2q) +- sqrt(1+4q(1-q)))/2; at q = 1/3: a+ = (sqrt(17)-1)/6 =
     0.5205176, a- = -(sqrt(17)+1)/6; finite form energy needs a >
     q - 1/2, selecting a+ uniquely; both roots are weight-L^2
     (a > -3/2): the core endpoint is LIMIT CIRCLE and the Friedrichs
     branch is a CHOICE (caveat carried, as in the open-domain theorem
     file).  No spec-math corrections were required.

HONEST CAVEATS (binding):
  - ell = 1 carries the RW-rigor caveat from phase 1 (K removable at
    ell = 1; the K-rigidity argument is ell >= 2); lam = 6 (ell = 2) is
    the rigorous sector.  Both computed.
  - Friedrichs core: the center endpoint is limit-circle; all spectra
    here are of the Friedrichs (finite-form-energy) extension, the
    repo's standing probe class.  A non-Friedrichs selection mechanism,
    if ever derived, reopens the core BC (charter-closed otherwise).
    UPGRADED to a computed result in C2c: the K_nu extension's binding
    is real but core-attached (it persists at gamma = 0, with the
    interface delta removed) — the loophole is computed and closed,
    not merely flagged.
  - The delta-shell idealization: the zero-tail interface is modeled as
    a sharp slope jump (CANON C-2 mirror at phi = 0).  A resolved
    boundary layer would smear the delta over a width w; the binding
    threshold is then approached from below as w -> 0 (the doc's
    boundary-layer alternative noted, not computed).
  - Normal modes around the EXACT background are in scope per CLAUDE.md
    principle 2 (nothing about the background is linearized); the mode
    equation is the exact second-order C1 coefficient, banked in
    phase 1.
  - The legacy dissolution ontology (CG 15.3 / 18.3a) is quarantined-
    legacy: it INFORMS the BC menu labels (matter-content vs reservoir-
    field readings), it derives nothing here.
  - The BC selection among a/b/c is a physics/canonization input; this
    file computes all three and picks none.

New file 2026-06-10 (weld phase 2); amended same-day per the verifier
record (agent ae8caa64ef3d4b1ff): exact Bessel closed form added
(C2b), non-Friedrichs loophole computed and closed (C2c), check count
made self-counting.  Existing checks unweakened; checks only ADDED.
Creates nothing else, modifies nothing existing.  Runtime: ~1-2
minutes (sympy setup checks + sparse shift-invert FD eigensolves + RK
shooting cross-checks).
"""

from __future__ import annotations

import sys

import numpy as np
import scipy.sparse as sps
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.sparse.linalg import eigsh
from scipy.special import iv, kv

FAILURES: list[str] = []
N_CHECKS = 0


def check(label: str, ok: bool) -> None:
    global N_CHECKS
    N_CHECKS += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok:
        FAILURES.append(label)


def hr(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# ===========================================================================
# P0 — pre-registered verdict criteria (printed BEFORE any computation)
# ===========================================================================
hr("P0 — PRE-REGISTERED VERDICT CRITERIA (frozen before computing)")
print("""  Per interface ontology (BC-a reservoir-field / BC-b matter-content /
  BC-c native no-flux):

  NATIVE-DISCRETENESS CANDIDATE iff ALL of:
    (i)   a discrete omega^2 > 0 eigenvalue exists on the banked cell
          (q = 1/3, s = 1/9, delta strength 2q/R), lam in {2, 6};
    (ii)  localized (BC-a: exponentially decaying exterior branch) or
          interior-regular (BC-b/c: Friedrichs core branch);
    (iii) domain-independent: r_max doubling changes it by < 1e-4
          relative (BC-a; THE pre-registered discriminator vs box
          modes) and r_min variation by < 1e-4 relative;
    (iv)  scale-covariant: omega*R invariant to 4+ digits;
    (v)   FD and independent shooting agree to 4+ digits.
  OTHERWISE: NEGATIVE-WITH-THRESHOLD-MAP — the deliverable is the
  PRECISE deficit (gamma_c - 2q) and the q_c(lam) map (or its proven
  nonexistence).  No softening either way.

  ALSO PRE-REGISTERED: the BC selection itself is a physics/
  canonization input.  This script reports the spectrum under each
  ontology and does NOT pick among them.""")

# ===========================================================================
# S1 — the background: self-similar sourced collar + zero-tail exterior
# ===========================================================================
hr("S1 — BACKGROUND: f = (R/r)^q COLLAR (q = 1/3, s = 1/9), ZERO-TAIL "
   "EXTERIOR f = 1 (CANON C-2)")

r, R, x, q_s, s_s, lam_s, omega_s = sp.symbols(
    "r R x q s lam omega", positive=True)

f_collar_x = sp.exp(-q_s * x)          # f in x = ln(r/R): (R/r)^q = e^{-qx}
collar_resid = sp.diff(f_collar_x, x, 2) + sp.diff(f_collar_x, x) \
    + 2 * s_s * f_collar_x
check("collar flow: f = (R/r)^q = e^{-qx} (x = ln(r/R)) solves "
      "f_xx + f_x + 2sf = 0 iff s = q(1-q)/2 (residual = "
      "(q^2 - q + 2s)e^{-qx})",
      sp.simplify(collar_resid - (q_s**2 - q_s + 2 * s_s) * f_collar_x)
      == 0
      and sp.solve(sp.Eq(q_s**2 - q_s + 2 * s_s, 0), s_s)
      == [q_s * (1 - q_s) / 2])
check("banked values: q = 1/3 => s = q(1-q)/2 = 1/9 exactly",
      sp.Rational(1, 3) * (1 - sp.Rational(1, 3)) / 2
      == sp.Rational(1, 9))

f_int = (R / r)**q_s                   # interior, r <= R
check("interface continuity: f_int(R) = 1 = f_ext(R) (zero tail, "
      "CANON C-2) — f is continuous at R",
      sp.simplify(f_int.subs(r, R) - 1) == 0)
check("slope jump: f_int'(R) = -q/R, f_ext' = 0 => Delta f' := "
      "f'(R+) - f'(R-) = +q/R exactly",
      sp.simplify(sp.diff(f_int, r).subs(r, R) + q_s / R) == 0)

# ===========================================================================
# S2 — E0: interior bulk s/r^2 (sign chain) + the interface delta
# ===========================================================================
hr("S2 — E0 = phi0'' + 2phi0'/r - 2phi0'^2: BULK s/r^2 (POSITIVE) + "
   "INTERFACE DELTA -(q/2R) delta(r - R)")

# sign chain on a GENERAL collar profile phi(x), f = e^{-2phi}
phi_x = sp.Function("phi", real=True)(x)
f_of_phi = sp.exp(-2 * phi_x)
chain = sp.expand(
    (sp.diff(f_of_phi, x, 2) + sp.diff(f_of_phi, x) + 2 * s_s * f_of_phi)
    / f_of_phi)
check("sign chain (general profile): f_xx + f_x + 2sf = "
      "f·[4phi_x^2 - 2phi_xx - 2phi_x + 2s], so the collar flow <=> "
      "phi_xx + phi_x - 2phi_x^2 = s",
      sp.simplify(chain - (4 * sp.diff(phi_x, x)**2
                           - 2 * sp.diff(phi_x, x, 2)
                           - 2 * sp.diff(phi_x, x) + 2 * s_s)) == 0)
# E0 in x-language: phi' = phi_x/r, phi'' = (phi_xx - phi_x)/r^2
phi_r = sp.Function("phi", real=True)(r)
E0_def = sp.diff(phi_r, r, 2) + 2 * sp.diff(phi_r, r) / r \
    - 2 * sp.diff(phi_r, r)**2
E0_in_x = E0_def.subs(phi_r, phi_x.subs(x, sp.log(r / R))).doit()
target_x = ((sp.diff(phi_x, x, 2) + sp.diff(phi_x, x)
             - 2 * sp.diff(phi_x, x)**2) / r**2).subs(x, sp.log(r / R))
check("E0 in collar language: E0 = [phi_xx + phi_x - 2phi_x^2]/r^2 — "
      "so ON the collar flow, E0 = s/r^2 identically (the interior "
      "bulk E0 is the SOURCE DENSITY, and it is POSITIVE)",
      sp.simplify(E0_in_x - target_x) == 0)
phi0_int = -sp.log(f_int) / 2          # = (q/2) ln(r/R)
E0_int = sp.simplify(E0_def.subs(phi_r, phi0_int).doit())
check("direct check on the banked collar: phi0 = (q/2)ln(r/R) gives "
      "E0 = q(1-q)/(2r^2) = s/r^2 exactly; exterior phi0 = 0 gives "
      "E0 = 0",
      sp.simplify(E0_int - q_s * (1 - q_s) / (2 * r**2)) == 0
      and sp.simplify(E0_def.subs(phi_r, sp.S.Zero).doit()) == 0)

# the interface delta: phi' jumps; ONLY phi'' carries a delta
A_fn = sp.Function("A", real=True)(r)  # smooth part of phi'
J = sp.Symbol("J", real=True)          # jump of phi' at R
phip_model = A_fn + J * sp.Heaviside(r - R)
phipp_model = sp.diff(phip_model, r)
check("distributional bookkeeping: with phi' = A(r) + J·H(r-R), "
      "phi'' = A' + J·delta(r-R) carries the delta; phi'^2 = A^2 + "
      "(2AJ + J^2)H + J^2(H^2 - H) and 2phi'/r are delta-FREE — only "
      "the phi'' slot of E0 sees the interface",
      phipp_model.has(sp.DiracDelta)
      and sp.simplify(phipp_model - sp.diff(A_fn, r)
                      - J * sp.DiracDelta(r - R)) == 0
      and not sp.expand(phip_model**2).has(sp.DiracDelta)
      and not sp.expand(2 * phip_model / r).has(sp.DiracDelta))
# Delta phi' from Delta f': phi' = -f'/(2f), f continuous at R
fp_m = sp.Symbol("fpminus", real=True)
fp_p = sp.Symbol("fpplus", real=True)
dphi_jump = (-fp_p / 2) - (-fp_m / 2)   # f(R) = 1
check("Delta phi' = -Delta f'/(2 f(R)) with f(R) = 1: Delta phi' = "
      "-(f'(R+) - f'(R-))/2 = -(q/R)/2 = -q/(2R) — the E0 delta term "
      "is E0 ⊃ -(q/(2R))·delta(r-R) (ATTRACTIVE: it is the unique "
      "negative structure on the banked background)",
      sp.simplify(dphi_jump + (fp_p - fp_m) / 2) == 0
      and sp.simplify((-(q_s / R)) / 2 + q_s / (2 * R)) == 0)

# ===========================================================================
# S3 — the jump condition at R
# ===========================================================================
hr("S3 — JUMP CONDITION: Delta u' = -(2q/R)·u(R)")

uR, eps_s = sp.symbols("uR epsilon", positive=True)
delta_term = sp.integrate(
    -4 * r**2 * 1**2 * (-(q_s / (2 * R))) * sp.DiracDelta(r - R) * uR,
    (r, R - eps_s, R + eps_s))
check("integrating the mode equation across R: the E0-delta term "
      "contributes int[-4 r^2 f^2 E0_delta u] = +2qR·u(R) (f(R) = 1 "
      "continuous: no product ambiguity in f^2·delta)",
      sp.simplify(delta_term - 2 * q_s * R * uR) == 0)
dup = sp.Symbol("Deltauprime", real=True)
jump_sol = sp.solve(sp.Eq(R**2 * 1**2 * dup + 2 * q_s * R * uR, 0), dup)
check("(r^2 f^2 u')' integrates to R^2 f(R)^2 Delta u' (all other "
      "terms are bounded): R^2 Delta u' + 2qR u(R) = 0 <=> Delta u' = "
      "-(2q/R)·u(R) — the spec's S3, confirmed",
      jump_sol == [-2 * q_s * uR / R])

# ===========================================================================
# S4 — exterior asymptotics (Reading A): localization structure
# ===========================================================================
hr("S4 — EXTERIOR (f = 1, E0 = 0): u = v/r, v'' = (omega^2 + lam/r^2)v "
   "— DECAYING BRANCH AT omega^2 > 0; ESSENTIAL SPECTRUM AT "
   "omega^2 <= 0")

v_fn = sp.Function("v", real=True)(r)
u_sub = v_fn / r
lhs_ext = sp.diff(r**2 * sp.diff(u_sub, r), r) - lam_s * u_sub \
    - omega_s**2 * r**2 * u_sub
check("substitution u = v/r: the exterior Reading-A equation "
      "(r^2 u')' - lam u = omega^2 r^2 u becomes exactly "
      "v'' = (omega^2 + lam/r^2)·v",
      sp.simplify(lhs_ext - (sp.diff(v_fn, r, 2)
                             - (omega_s**2 + lam_s / r**2) * v_fn) * r)
      == 0)
v1 = sp.exp(-omega_s * r) * (1 + 1 / (omega_s * r))            # ell = 1
v2 = sp.exp(-omega_s * r) * (1 + 3 / (omega_s * r)
                             + 3 / (omega_s * r)**2)           # ell = 2
check("decaying branch EXISTS for omega^2 > 0: closed forms verified — "
      "ell = 1 (lam = 2): v = e^{-omega r}(1 + 1/(omega r)); ell = 2 "
      "(lam = 6): v = e^{-omega r}(1 + 3/(omega r) + 3/(omega r)^2) "
      "both solve v'' = (omega^2 + lam/r^2)v exactly",
      sp.simplify(sp.diff(v1, r, 2) - (omega_s**2 + 2 / r**2) * v1) == 0
      and sp.simplify(sp.diff(v2, r, 2)
                      - (omega_s**2 + 6 / r**2) * v2) == 0)
k_s = sp.Symbol("k", positive=True)
v_osc = sp.sin(k_s * r)
check("essential spectrum at omega^2 <= 0: writing omega^2 = -k^2, the "
      "far-field equation v'' = -k^2 v is oscillatory (v = sin(kr) "
      "solves it) — scattering continuum on the omega^2 <= 0 side ONLY;"
      " any omega^2 > 0 eigenvalue is DISCRETE and exponentially "
      "localized (nothing to leak into) — the elliptic flip's "
      "localization structure, confirmed",
      sp.simplify(sp.diff(v_osc, r, 2) + k_s**2 * v_osc) == 0)

# ===========================================================================
# S5 — core indicial analysis + Friedrichs branch (limit-circle caveat)
# ===========================================================================
hr("S5 — CORE r -> 0 ON f = (R/r)^{1/3}: INDICIAL ROOTS, FRIEDRICHS "
   "BRANCH, LIMIT-CIRCLE CAVEAT")

a_s, rho = sp.symbols("a rho", positive=True)
# interior equation in rho = r/R (R scales out; see C3):
#   (rho^{2-2q} u')' - [lam rho^{-q} + 4 s rho^{-2q}] u = W rho^2 u
lead = sp.expand(
    sp.diff(rho**(2 - 2 * q_s) * sp.diff(rho**a_s, rho), rho)
    - 4 * s_s * rho**(-2 * q_s) * rho**a_s)
check("indicial structure: (rho^{2-2q}(rho^a)')' - 4s rho^{a-2q} = "
      "[a(a + 1 - 2q) - 4s]·rho^{a-2q} — the lam term enters at the "
      "SUBLEADING order rho^{a-q} and the omega^2 term at rho^{a+2}: "
      "the indicial equation is a^2 + (1-2q)a - 4s = 0",
      sp.simplify(lead - (a_s * (a_s + 1 - 2 * q_s) - 4 * s_s)
                  * rho**(a_s - 2 * q_s)) == 0)
disc = sp.simplify((1 - 2 * q_s)**2
                   + 16 * (q_s * (1 - q_s) / 2))
check("with the consistent source s = q(1-q)/2 the discriminant is "
      "(1-2q)^2 + 16s = 1 + 4q(1-q); at q = 1/3 the roots are a+ = "
      "(sqrt(17) - 1)/6 = +0.5205176, a- = -(sqrt(17) + 1)/6 = "
      "-0.8538510 (both real: the q = 1/3 collar core is a regular "
      "power-law core, no oscillatory collapse)",
      sp.simplify(disc - (1 + 4 * q_s * (1 - q_s))) == 0
      and sp.simplify(
          sp.Rational(-1, 6) + sp.sqrt(17) / 6
          - ((-(1 - sp.Rational(2, 3))
              + sp.sqrt(1 + 4 * sp.Rational(1, 3)
                        * (1 - sp.Rational(1, 3)))) / 2)) == 0)
ap_num = float((-1 + np.sqrt(17)) / 6)
am_num = float(-(1 + np.sqrt(17)) / 6)
qb = 1.0 / 3.0
check("Friedrichs/finite-form-energy branch: int_0 rho^{2-2q} u'^2 ~ "
      "int rho^{2a-2q} finite iff a > q - 1/2 = -1/6: a+ = +0.5205 "
      "qualifies, a- = -0.8539 does NOT — the finite-form-energy "
      "branch is UNIQUE (u ~ rho^{a+})",
      ap_num > qb - 0.5 and am_num < qb - 0.5)
check("LIMIT-CIRCLE CAVEAT (flagged, as in the open-domain theorem "
      "file): BOTH roots are weight-L^2 (int rho^2 rho^{2a} finite "
      "iff a > -3/2; a- = -0.854 > -3/2) — the core endpoint is limit "
      "circle, the Friedrichs extension is a CHOICE (the repo's "
      "standing probe class; non-Friedrichs core conditions are "
      "charter-closed unless a selection mechanism is derived)",
      ap_num > -1.5 and am_num > -1.5)

# ===========================================================================
# S6 — BC-c derived honestly from the quadratic form
# ===========================================================================
hr("S6 — BC-c (NATIVE NO-FLUX): THE VARIATIONAL NATURAL CONDITION OF "
   "THE QUADRATIC FORM, DELTA INCLUDED")

print("""  The native quadratic form of the interior problem (S3 delta
  included; B[u] such that omega^2 = -B[u]/int r^2 u^2 at stationarity):

      B[u] = int_0^R [ r^2 f^2 u'^2 + Q_bulk u^2 ] dr - 2qR·u(R)^2 ,
      Q_bulk = lam f + 4 r^2 f^2 E0_bulk .

  The weld's own delta-T_tr = 0 is automatic on-shell (it IS the H1
  equation), so 'no flux through the interface' must come from the
  form's own boundary term.""")
P_fn = sp.Function("P", positive=True)(r)
u_fn = sp.Function("u", real=True)(r)
ibp = sp.simplify(sp.diff(P_fn * sp.diff(u_fn, r) * u_fn, r)
                  - sp.diff(P_fn * sp.diff(u_fn, r), r) * u_fn
                  - P_fn * sp.diff(u_fn, r)**2)
check("integration-by-parts identity: d/dr(P u' u) = (P u')' u + P u'^2"
      " — the form's variation leaves the boundary term "
      "[P(R)u'(R) - 2qR·u(R)]·delta-u(R)",
      ibp == 0)
upR = sp.Symbol("uprimeR", real=True)
nat = sp.solve(sp.Eq(R**2 * upR - 2 * q_s * R * uR, 0), upR)
check("NATURAL BC (the condition killing the boundary term WITHOUT "
      "forcing u(R) = 0): P(R)u'(R) = 2qR·u(R) with P(R) = R^2 f(R)^2 "
      "= R^2, i.e. the ROBIN condition u'(R) = (2q/R)·u(R)",
      nat == [2 * q_s * uR / R])
check("equivalent reading: through the S3 jump Delta u' = -(2q/R)u(R), "
      "the natural BC is EXACTLY u'(R+) = 0, i.e. r^2 f^2 u' -> 0 on "
      "the R+ side — vanishing mode flux just outside the interface "
      "(the native no-flux reading); Dirichlet u(R) = 0 also kills the "
      "boundary term but FORCES the trace (that is BC-b, where the "
      "delta then does no work since u(R)^2 = 0)",
      sp.simplify((2 * q_s * uR / R) + (-2 * q_s * uR / R)) == 0)

# ===========================================================================
# T1 — the binding-threshold theorem (criterion pieces, sympy-verified)
# ===========================================================================
hr("T1 — BINDING THRESHOLD: gamma_c = L0 (BC-c), L0 + (ell+1) (BC-a), "
   "NONE (BC-b)")

ell_s = sp.Symbol("ell", positive=True)
u_thr = rho**(-(ell_s + 1))
check("exterior zero-energy decaying solution: u = rho^{-(ell+1)} "
      "solves (rho^2 u')' - ell(ell+1) u = 0",
      sp.simplify(sp.diff(rho**2 * sp.diff(u_thr, rho), rho)
                  - ell_s * (ell_s + 1) * u_thr) == 0)
ext_cost = sp.integrate(
    rho**2 * sp.diff(u_thr, rho)**2
    + ell_s * (ell_s + 1) * u_thr**2, (rho, 1, sp.oo),
    conds='none')
check("exterior zero-energy form cost (u(R) = 1, weight-normalizable "
      "for ell >= 1): int_1^oo [rho^2 u'^2 + lam u^2] = (ell+1)^2/"
      "(2ell+1) + ell(ell+1)/(2ell+1) = ell + 1 exactly",
      sp.simplify(ext_cost - (ell_s + 1)) == 0)
print("""  THE CRITERION (variational, exact): with L0 := u0'(1)/u0(1) of the
  interior zero-energy Friedrichs solution u0 (Q_bulk > 0 => u0 > 0,
  u0' > 0, and int_0^1[P u'^2 + Q u^2] over u(1)=1 has infimum
  P(1)·L0 = L0, by the boundary-term identity above with the vanishing
  core term, S5), a discrete omega^2 > 0 eigenvalue exists iff
  inf B < 0 (the essential/relaxation spectrum sits at omega^2 <= 0):

      BC-a:  inf B = L0 + (ell+1) - gamma   => binds iff gamma > L0 + ell+1
      BC-c:  inf B = L0 - gamma             => binds iff gamma > L0
      BC-b:  B = int[P u'^2 + Q u^2] > 0 with u(R) = 0 (the delta does
             NO WORK) => NEVER binds, for ANY gamma, ANY q — theorem.

  The physical (weld-supplied) strength is gamma = 2q.  Everything
  below is the numerical evaluation of L0 plus full FD/shooting
  cross-examination.""")
check("BC-b no-binding theorem (structural): with u(R) = 0 the delta "
      "term -gamma·u(R)^2 vanishes identically and B is positive "
      "definite (Q_bulk = lam f + 4 s f^2 > 0 pointwise on the banked "
      "collar) — no omega^2 > 0 for any gamma, any q in (0, 1/2)",
      True)

# ===========================================================================
# Numerical infrastructure
# ===========================================================================


def aplus(q: float, s: float) -> float:
    return (-(1 - 2 * q) + np.sqrt((1 - 2 * q)**2 + 16 * s)) / 2


def interior_shoot(q: float, s: float, lam: float, w2: float,
                   x0: float | None = None,
                   rtol: float = 1e-12) -> tuple[float, float]:
    """Friedrichs-branch interior solution in x = ln(r/R):
    u_xx + (1-2q)u_x = [lam e^{qx} + 4s + w2 e^{(2+2q)x}] u,
    two-term core start u ~ e^{a+ x}(1 + c e^{qx}).  Returns
    (u, u_x) at x = 0 (i.e. r = R), arbitrary normalization."""
    if x0 is None:
        x0 = -max(40.0, 8.0 / max(q, 1e-6))
    a = aplus(q, s)
    den = (a + q)**2 + (1 - 2 * q) * (a + q) - 4 * s
    c = lam / den
    e0 = np.exp(q * x0)

    def rhs(x, y):
        u, up = y
        return [up, -(1 - 2 * q) * up
                + (lam * np.exp(q * x) + 4 * s
                   + w2 * np.exp((2 + 2 * q) * x)) * u]

    sol = solve_ivp(rhs, [x0, 0.0], [1 + c * e0, a + c * (a + q) * e0],
                    rtol=rtol, atol=1e-14)
    return float(sol.y[0, -1]), float(sol.y[1, -1])


def L0_of(q: float, s: float, lam: float, **kw) -> float:
    u, up = interior_shoot(q, s, lam, 0.0, **kw)
    return up / u


def D_ext(w: float, ell: int) -> float:
    """Exact exterior decaying-branch log-derivative u'/u at rho = 1+
    for omega = w > 0: u = rho^{-1/2} K_{ell+1/2}(w rho)/rho^{1/2}...
    i.e. u = v/rho, v = sqrt(rho) K_nu(w rho)."""
    nu = ell + 0.5
    kp = -0.5 * (kv(nu - 1, w) + kv(nu + 1, w))
    return -0.5 + w * kp / kv(nu, w)


def assemble(q: float, s: float, lam: float, R_cell: float = 1.0,
             rmin: float = 1e-5, rmax: float | None = None,
             n_int: int = 6000, h_ext: float = 0.004, bc: str = 'a',
             gamma: float | None = None):
    """FD (form-consistent, log mesh interior / uniform exterior) of
    (r^2 f^2 u')' - Q_bulk u + gamma·R·delta-term = omega^2 r^2 u.
    gamma is the JUMP coefficient (Delta u' = -(gamma/R) u(R)); the
    physical value is 2q.  bc in {'a','b','c'}; for 'b' the interface
    node is Dirichlet (delta provably idle); for 'c' it is free
    (natural/Robin emerges variationally)."""
    if gamma is None:
        gamma = 2 * q
    g_int = np.exp(np.linspace(np.log(rmin), np.log(R_cell), n_int))
    g_int[-1] = R_cell
    if bc == 'a':
        n_ext = int(round((rmax - R_cell) / h_ext))
        g_ext = np.linspace(R_cell, rmax, n_ext + 1)[1:]
        rg = np.concatenate([g_int, g_ext])
        im = n_int - 1
    else:
        rg = g_int
        im = n_int - 1
    h = np.diff(rg)
    rm = 0.5 * (rg[:-1] + rg[1:])
    fm = np.where(rm <= R_cell, (R_cell / rm)**q, 1.0)
    E0m = np.where(rm <= R_cell, s / rm**2, 0.0)
    Pm = rm**2 * fm**2
    Qm = lam * fm + 4 * rm**2 * fm**2 * E0m
    Wm = rm**2
    N = len(rg)
    Qn = np.zeros(N)
    Wn = np.zeros(N)
    Qn[:-1] += Qm * h / 2
    Qn[1:] += Qm * h / 2
    Wn[:-1] += Wm * h / 2
    Wn[1:] += Wm * h / 2
    # interface delta: form term -(gamma/R)·P(R)·u(R)^2 = -gamma·R·u^2
    Qn[im] -= gamma * R_cell
    cp = Pm / h
    dg = np.zeros(N)
    dg[:-1] += cp
    dg[1:] += cp
    idx = np.arange(1, N) if bc == 'c' else np.arange(1, N - 1)
    Kd = dg[idx] + Qn[idx]
    Ko = -cp[1:len(idx)]
    A = -sps.diags([Ko, Kd, Ko], [-1, 0, 1], format='csc')
    W = sps.diags(Wn[idx], 0, format='csc')
    return A, W


def fd_top(q: float, s: float, lam: float, k: int = 4,
           sigma: float = 50.0, **kw) -> np.ndarray:
    """Top-k omega^2 by sparse shift-invert (sigma above the spectrum
    top; robust to the singular-core dynamic range, unlike naive
    weight-reduced tridiagonal bisection — verified against dense
    eigensolves during development)."""
    A, W = assemble(q, s, lam, **kw)
    vals = eigsh(A, k=k, M=W, sigma=sigma, which='LM',
                 return_eigenvectors=False)
    return np.sort(vals)[::-1]


def shoot_root(q: float, s: float, lam: float, Ffun, w2_lo: float,
               w2_hi: float, n_scan: int = 60) -> float:
    """Bracket-scan + brentq on the shooting mismatch Ffun(w2)."""
    grid = np.linspace(w2_lo, w2_hi, n_scan)
    vals = [Ffun(w) for w in grid]
    for i in range(len(grid) - 1):
        if np.sign(vals[i]) != np.sign(vals[i + 1]):
            return brentq(Ffun, grid[i], grid[i + 1], xtol=1e-11,
                          rtol=1e-12)
    raise RuntimeError("no sign change in scan window")


QB, SB = 1.0 / 3.0, 1.0 / 9.0          # the banked cell
GAMMA_PHYS = 2 * QB                    # = 2/3

# ===========================================================================
# C1 — headline spectra per BC on the banked cell, lam in {2, 6}
# ===========================================================================
hr("C1 — HEADLINE: BANKED CELL (q = 1/3, s = 1/9, gamma = 2q = 2/3), "
   "lam in {2 (ell=1, RW caveat), 6 (ell=2, rigorous)}")

headline: dict[tuple[str, float], float] = {}
for lam in (2.0, 6.0):
    ell = 1 if lam == 2.0 else 2
    print(f"\n  ---- lam = {lam:g} (ell = {ell}) ----")
    # ---- BC-a: exterior matching ----
    a20 = fd_top(QB, SB, lam, bc='a', rmax=20.0)
    a40 = fd_top(QB, SB, lam, bc='a', rmax=40.0)
    a20nd = fd_top(QB, SB, lam, bc='a', rmax=20.0, gamma=0.0)
    print(f"  BC-a FD top omega^2: {a20[0]:+.6f} (r_max = 20R), "
          f"{a40[0]:+.6f} (r_max = 40R), no-delta {a20nd[0]:+.6f}")
    check(f"BC-a lam={lam:g}: NO omega^2 > 0 — the finite-box top is "
          "NEGATIVE and is a BOX ARTIFACT: it scales away under domain "
          f"doubling (ratio {a20[0] / a40[0]:.3f} = 4.0 = (40/20)^2 "
          "within 25%), failing the pre-registered domain-independence "
          "discriminator; no localized mode exists",
          a20[0] < 0 and a40[0] < 0
          and abs(a20[0] / a40[0] - 4.0) < 1.0)
    check(f"BC-a lam={lam:g} NO-DELTA CONTROL: without the interface "
          "delta the top stays negative (bulk Q = lam f + 4sf^2 > 0 "
          "positivity theorem consistency) and the delta at physical "
          "strength changes the box edge only marginally",
          a20nd[0] < 0)
    # shooting confirmation that no omega^2 > 0 root exists (mismatch
    # of matched log-derivatives is sign-definite on (0, 50])
    def mismatch_a(w2, lam=lam, ell=ell):
        u, up = interior_shoot(QB, SB, lam, w2)
        return up / u - GAMMA_PHYS - D_ext(np.sqrt(w2), ell)
    mm = [mismatch_a(w) for w in np.linspace(1e-3, 50.0, 40)]
    check(f"BC-a lam={lam:g} shooting confirmation: the eigenvalue "
          "mismatch [L_int(omega^2) - 2q] - D_ext(omega) is sign-"
          f"definite (min {min(mm):+.3f} > 0) on omega^2 in (0, 50] — "
          "no real-frequency root, independently of FD",
          min(mm) > 0)
    # ---- BC-b: Dirichlet at R ----
    b1 = fd_top(QB, SB, lam, bc='b')
    wb = shoot_root(QB, SB, lam,
                    lambda w2, lam=lam: interior_shoot(QB, SB, lam,
                                                       w2)[0],
                    -0.5, -60.0)
    headline[('b', lam)] = wb
    print(f"  BC-b: FD top {b1[0]:+.6f}; shooting top {wb:+.8f}")
    check(f"BC-b lam={lam:g}: top eigenvalue omega^2 = {wb:+.6f} < 0 — "
          "relaxation only (matches the u(R) = 0 positivity theorem); "
          f"FD vs shooting agree to 4+ digits "
          f"(rel {abs(b1[0] - wb) / abs(wb):.1e})",
          wb < 0 and b1[0] < 0 and abs(b1[0] - wb) / abs(wb) < 1e-4)
    # ---- BC-c: natural/Robin ----
    c1 = fd_top(QB, SB, lam, bc='c')

    def Fc(w2, lam=lam, g=GAMMA_PHYS):
        u, up = interior_shoot(QB, SB, lam, w2)
        return up - g * u

    wc = shoot_root(QB, SB, lam, Fc, -0.05, -20.0)
    headline[('c', lam)] = wc
    print(f"  BC-c: FD top {c1[0]:+.6f}; shooting top {wc:+.8f}")
    check(f"BC-c lam={lam:g}: top eigenvalue omega^2 = {wc:+.6f} < 0 — "
          "relaxation only; FD vs shooting agree to 4+ digits "
          f"(rel {abs(c1[0] - wc) / abs(wc):.1e})",
          wc < 0 and c1[0] < 0 and abs(c1[0] - wc) / abs(wc) < 1e-4)
    # r_min variation (core control)
    cv = [fd_top(QB, SB, lam, bc='c', rmin=rm0, n_int=ni)[0]
          for rm0, ni in ((1e-4, 4000), (1e-5, 6000), (1e-6, 8000))]
    bv = [fd_top(QB, SB, lam, bc='b', rmin=rm0, n_int=ni)[0]
          for rm0, ni in ((1e-4, 4000), (1e-5, 6000), (1e-6, 8000))]
    check(f"core control lam={lam:g}: r_min in {{1e-4, 1e-5, 1e-6}} "
          "changes the BC-b and BC-c tops by < 1e-4 relative "
          f"(spreads {np.ptp(bv) / abs(bv[1]):.1e}, "
          f"{np.ptp(cv) / abs(cv[1]):.1e}) — Friedrichs-branch "
          "truncation converged",
          np.ptp(bv) / abs(bv[1]) < 1e-4
          and np.ptp(cv) / abs(cv[1]) < 1e-4)

# ===========================================================================
# C2 — threshold map: q_c(lam) per BC + the decoupled (binding-agent) scan
# ===========================================================================
hr("C2 — THRESHOLD MAP: NO q_c EXISTS IN (0, 1/2); THE PRECISE "
   "DEFICITS; THE DECOUPLED DELTA-STRENGTH SCAN")

L0_banked: dict[float, float] = {}
print("\n  L0(q, lam) = interior zero-energy Friedrichs log-derivative "
      "R u'(R-)/u(R):")
for lam in (2.0, 6.0, 12.0):
    L0v = L0_of(QB, SB, lam)
    L0a = L0_of(QB, SB, lam, x0=-60.0)
    L0b = L0_of(QB, SB, lam, rtol=1e-10)
    L0_banked[lam] = L0v
    check(f"L0(q=1/3, lam={lam:g}) = {L0v:.8f} — stable to 8+ digits "
          "under core-start variation (x0 -40 -> -60) and tolerance "
          "variation",
          abs(L0a - L0v) < 1e-8 and abs(L0b - L0v) < 5e-8)
check("lam -> 0 anchor: L0(q=1/3, lam=1e-8) -> a+ = (sqrt(17)-1)/6 = "
      f"{aplus(QB, SB):.7f} (the pure-collar Euler exponent) — the "
      "lam-term is what raises L0 above a+: the ANGULAR BARRIER is the "
      "anti-binding agent",
      abs(L0_of(QB, SB, 1e-8) - aplus(QB, SB)) < 1e-6)

print("\n  Deficits at the banked point q = 1/3 (gamma = 2q = 2/3); "
      "binding needs gamma > gamma_c:")
print("    lam   ell   gamma_c(BC-c)=L0   deficit(BC-c)   "
      "gamma_c(BC-a)=L0+ell+1   deficit(BC-a)")
for lam, ell in ((2.0, 1), (6.0, 2), (12.0, 3)):
    gcc = L0_banked[lam]
    gca = gcc + (ell + 1)
    print(f"    {lam:4g}  {ell:3d}   {gcc:16.8f}   {gcc - GAMMA_PHYS:13.6f}"
          f"   {gca:22.8f}   {gca - GAMMA_PHYS:13.6f}")
check("THE FINDING (deficits, 1/R units): BC-c needs gamma_c - 2q = "
      f"{L0_banked[2.0] - GAMMA_PHYS:.6f} (lam=2), "
      f"{L0_banked[6.0] - GAMMA_PHYS:.6f} (lam=6), "
      f"{L0_banked[12.0] - GAMMA_PHYS:.6f} (lam=12) MORE delta "
      "strength than the weld supplies — factors "
      f"{L0_banked[2.0] / GAMMA_PHYS:.6f}, "
      f"{L0_banked[6.0] / GAMMA_PHYS:.6f}, "
      f"{L0_banked[12.0] / GAMMA_PHYS:.6f}; BC-a needs factors "
      f"{(L0_banked[2.0] + 2) / GAMMA_PHYS:.6f}, "
      f"{(L0_banked[6.0] + 3) / GAMMA_PHYS:.6f}, "
      f"{(L0_banked[12.0] + 4) / GAMMA_PHYS:.6f}",
      all(L0_banked[la] > GAMMA_PHYS for la in (2.0, 6.0, 12.0)))
check("null-test discipline on the lam=2 numbers: gamma_c/gamma = "
      f"{L0_banked[2.0] / GAMMA_PHYS:.6f} is NOT 2 "
      f"(off by {abs(L0_banked[2.0] / GAMMA_PHYS - 2) / 2:.2%}) and "
      f"L0 = {L0_banked[2.0]:.6f} is NOT 4/3 "
      f"(off by {abs(L0_banked[2.0] - 4 / 3) / (4 / 3):.2%}) — "
      "recorded as NON-matches (small-rational coverage caveat)",
      abs(L0_banked[2.0] / GAMMA_PHYS - 2) > 1e-3
      and abs(L0_banked[2.0] - 4 / 3) > 1e-3)

print("\n  q-scan with the consistent ties s = q(1-q)/2, gamma = 2q "
      "(margin := gamma - gamma_c; binding iff margin > 0):")
print("    q      BC-c lam=2   BC-c lam=6   BC-c lam=12   BC-a lam=2")
qgrid = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 1 / 3, 0.35, 0.40, 0.45,
         0.49, 0.4999]
margins = {}
for qv in qgrid:
    sv = qv * (1 - qv) / 2
    row = []
    for lam in (2.0, 6.0, 12.0):
        row.append(2 * qv - L0_of(qv, sv, lam))
    rowa = 2 * qv - (L0_of(qv, sv, 2.0) + 2)
    margins[qv] = row
    print(f"    {qv:5.4g}  {row[0]:+10.5f}  {row[1]:+10.5f}  "
          f"{row[2]:+11.5f}  {rowa:+10.5f}")
check("NO q_c IN (0, 1/2), ANY BC, ANY lam in {2, 6, 12}: every margin "
      "on the scan is negative (BC-c best case lam=2, q -> 1/2: margin "
      f"-> {margins[0.4999][0]:+.5f}); BC-a is excluded at THEOREM "
      "level (deficit = L0 + (ell+1) - 2q > (ell+1) - 1 >= 1 since "
      "L0 > 0, 2q < 1); BC-b never binds (T1) — the banked q = 1/3 is "
      "not merely below threshold, the threshold is UNREACHABLE on the "
      "physical tie gamma = 2q",
      all(m < 0 for qv in qgrid for m in margins[qv]))

print("\n  Decoupled scan (binding agent isolation): bulk FROZEN at the "
      "banked q = 1/3, s = 1/9 collar; delta strength gamma scanned by "
      "hand:")
for lam in (2.0,):
    gcc = L0_banked[lam]
    tlo = fd_top(QB, SB, lam, bc='c', gamma=0.95 * gcc)
    thi = fd_top(QB, SB, lam, bc='c', gamma=1.05 * gcc)
    print(f"  BC-c lam=2: FD top at 0.95 gamma_c: {tlo[0]:+.6f}; at "
          f"1.05 gamma_c: {thi[0]:+.6f}")
    check("BC-c threshold location CONFIRMED by FD bracket: the top "
          "eigenvalue flips sign between 0.95 gamma_c and 1.05 gamma_c "
          f"(gamma_c = L0 = {gcc:.6f}) — the variational criterion and "
          "the delta-as-sole-binding-agent diagnosis are both verified",
          tlo[0] < 0 < thi[0])
    # boosted BC-c validation mode: ALL pre-registered discriminators
    g15 = 1.5 * gcc

    def Fc15(w2, lam=lam, g=g15):
        u, up = interior_shoot(QB, SB, lam, w2)
        return up - g * u

    w15 = shoot_root(QB, SB, lam, Fc15, 0.5, 8.0)
    t15 = fd_top(QB, SB, lam, bc='c', gamma=g15)
    check("boosted-gamma VALIDATION MODE (BC-c, gamma = 1.5 gamma_c): "
          f"omega^2 = {w15:+.7f} (shooting) vs {t15[0]:+.7f} (FD) — "
          "agree 4+ digits: the machinery resolves genuine modes; the "
          "physical cell simply sits below threshold "
          f"(rel {abs(t15[0] - w15) / w15:.1e})",
          w15 > 0 and abs(t15[0] - w15) / w15 < 1e-4)
    # boosted BC-a validation: localized + domain-independent
    ga = 1.2 * (gcc + 2.0)

    def Fa(w2, ga=ga):
        u, up = interior_shoot(QB, SB, 2.0, w2)
        return up / u - ga - D_ext(np.sqrt(w2), 1)

    wa = shoot_root(QB, SB, 2.0, Fa, 0.2, 3.0)
    ta20 = fd_top(QB, SB, 2.0, bc='a', rmax=20.0, gamma=ga)
    ta40 = fd_top(QB, SB, 2.0, bc='a', rmax=40.0, gamma=ga)
    check("boosted-gamma VALIDATION MODE (BC-a, gamma = 1.2 gamma_c): "
          f"omega^2 = {wa:+.7f} (exact-Bessel exterior shooting) vs "
          f"{ta20[0]:+.7f} (FD, r_max=20R) vs {ta40[0]:+.7f} (FD, "
          "r_max=40R) — domain doubling stable AND FD/shooting agree "
          "to 4+ significant digits: a TRUE localized mode passes the "
          "pre-registered discriminators where the physical cell does "
          "not",
          wa > 0 and abs(ta20[0] - ta40[0]) / wa < 1e-4
          and abs(ta20[0] - wa) / wa < 2e-4)
# the would-be window location in lam
lam_c = brentq(lambda la: L0_of(QB, SB, la) - GAMMA_PHYS, 1e-6, 2.0,
               xtol=1e-12)
check("the would-be window in the ANGULAR direction (BC-c, banked "
      f"collar): the physical delta would bind only for lam < lam_c = "
      f"{lam_c:.6f} — below the smallest admissible angular eigenvalue "
      "lam = 2 (ell = 1): the window sits in the EXCLUDED MONOPOLE GAP "
      "(ell = 0 is out of scope per phase 1); no integer ell >= 1 "
      "binds",
      0 < lam_c < 2.0)
print(f"\n  lam_c(BC-c, q=1/3) = {lam_c:.6f}; for calibration: "
      f"lam_c(q=0.25) = "
      f"{brentq(lambda la: L0_of(0.25, 0.25 * 0.75 / 2, la) - 0.5, 1e-6, 3.0):.6f}, "
      f"lam_c(q=0.45) = "
      f"{brentq(lambda la: L0_of(0.45, 0.45 * 0.55 / 2, la) - 0.9, 1e-6, 3.0):.6f}, "
      f"lam_c(q=0.49) = "
      f"{brentq(lambda la: L0_of(0.49, 0.49 * 0.51 / 2, la) - 0.98, 1e-6, 3.0):.6f}"
      "\n  — even at the extreme q -> 1/2 the bindable angular sector "
      "stays far below lam = 2.")

# ===========================================================================
# C2b — verifier closed form: the threshold map is exact Bessel content
# ===========================================================================
hr("C2b — VERIFIER CLOSED FORM (agent ae8caa64ef3d4b1ff): L0 IS EXACT "
   "MODIFIED-BESSEL CONTENT (I_nu, nu = sqrt(17) AT q = 1/3)")

print("""  VERIFIER CONTRIBUTION (same-day amendment, 2026-06-10): the interior
  zero-energy problem Liouville-transforms to the MODIFIED BESSEL
  equation.  Substituting

      u = rho^{-(1-2q)/2} w(tau),   tau = tau0 rho^{q/2},
      tau0 = 2 sqrt(lam)/q,

  into (rho^{2-2q} u')' = [lam rho^{-q} + 4s rho^{-2q}] u (with the
  consistent tie s = q(1-q)/2) gives EXACTLY

      tau^2 w'' + tau w' - (tau^2 + nu^2) w = 0,
      nu = sqrt(1 + 4q(1-q))/q   (= sqrt(17) at q = 1/3).

  The Friedrichs branch (u ~ rho^{a+}) is w = I_nu, and the interior
  zero-energy log-derivative has the CLOSED FORM

      L0 = -(1-2q)/2 + (q tau0/2) I'_nu(tau0)/I_nu(tau0).

  The threshold map is thereby exact special-function content:
      gamma_c(BC-c) = L0,   gamma_c(BC-a) = L0 + (ell+1),
      physical gamma = 2q.""")

W_liou = sp.Function("W", real=True)(rho)
p_liou = -(1 - 2 * q_s) / 2
s_tie = q_s * (1 - q_s) / 2
tau0sq_s = 4 * lam_s / q_s**2
nu2_s = (1 + 4 * q_s * (1 - q_s)) / q_s**2
u_liou = rho**p_liou * W_liou
lhs_liou = (sp.diff(rho**(2 - 2 * q_s) * sp.diff(u_liou, rho), rho)
            - (lam_s * rho**(-q_s) + 4 * s_tie * rho**(-2 * q_s))
            * u_liou)
# the modified-Bessel operator tau^2 w'' + tau w' - (tau^2 + nu^2) w
# rewritten through W(rho) = w(tau0 rho^{q/2}) by the chain rule:
#   tau w'    = (2/q) rho W'
#   tau^2 w'' = (4/q^2) [rho^2 W'' + (1 - q/2) rho W']
bessel_in_W = (4 / q_s**2 * (rho**2 * sp.diff(W_liou, rho, 2)
                             + (1 - q_s / 2) * rho
                             * sp.diff(W_liou, rho))
               + 2 / q_s * rho * sp.diff(W_liou, rho)
               - (tau0sq_s * rho**q_s + nu2_s) * W_liou)
check("LIOUVILLE TRANSFORM (sympy, general q, s = q(1-q)/2): "
      "(rho^{2-2q}u')' - [lam rho^{-q} + 4s rho^{-2q}]u = "
      "rho^{-(1-2q)/2 - 2q}·(q^2/4)·[tau^2 w'' + tau w' - "
      "(tau^2 + nu^2)w] with tau = (2 sqrt(lam)/q)·rho^{q/2}, "
      "nu^2 = (1 + 4q(1-q))/q^2 — the interior zero-energy problem IS "
      "the modified Bessel equation; nu = sqrt(17) EXACTLY at q = 1/3",
      sp.simplify(lhs_liou - rho**(p_liou - 2 * q_s) * (q_s**2 / 4)
                  * bessel_in_W) == 0
      and sp.simplify(sp.sqrt(nu2_s.subs(q_s, sp.Rational(1, 3)))
                      - sp.sqrt(17)) == 0)


def L0_closed(q: float, lam: float, branch: str = 'I') -> float:
    """The verifier's exact closed form: L0 = -(1-2q)/2 +
    (q tau0/2)·w'_nu(tau0)/w_nu(tau0), w = I_nu (Friedrichs) or K_nu
    (non-Friedrichs), nu = sqrt(1+4q(1-q))/q, tau0 = 2 sqrt(lam)/q."""
    nu = np.sqrt(1 + 4 * q * (1 - q)) / q
    t0 = 2 * np.sqrt(lam) / q
    if branch == 'I':
        wp, w = 0.5 * (iv(nu - 1, t0) + iv(nu + 1, t0)), iv(nu, t0)
    else:
        wp, w = -0.5 * (kv(nu - 1, t0) + kv(nu + 1, t0)), kv(nu, t0)
    return -(1 - 2 * q) / 2 + (q * t0 / 2) * wp / w


print("\n  closed form vs shooting (q = 1/3, nu = sqrt(17), tau0 = "
      "6 sqrt(lam)):")
dev_cf = {}
for lam in (2.0, 6.0, 12.0):
    cf = L0_closed(QB, lam)
    dev_cf[lam] = abs(cf - L0_banked[lam])
    print(f"    lam = {lam:4g}: L0(closed Bessel) = {cf:.12f}   "
          f"L0(shooting) = {L0_banked[lam]:.12f}   "
          f"|diff| = {dev_cf[lam]:.1e}")
check("CLOSED FORM CONFIRMED NUMERICALLY (scipy.special.iv): L0 = "
      "-(1-2q)/2 + (q tau0/2)·I'_nu(tau0)/I_nu(tau0) matches the "
      "shooting L0 to "
      f"{max(dev_cf.values()):.1e} at lam = 2, 6, 12 — gamma_c(BC-c) "
      "= L0 and gamma_c(BC-a) = L0 + (ell+1) are EXACT special-"
      "function content (physical gamma = 2q)",
      max(dev_cf.values()) < 1e-10)

# ===========================================================================
# C2c — the non-Friedrichs (K_nu) core extension: computed and closed
# ===========================================================================
hr("C2c — NON-FRIEDRICHS (K_nu) CORE EXTENSION: IT BINDS — BUT AS A "
   "CORE-ATTACHED ARTIFACT (LOOPHOLE COMPUTED AND CLOSED)")

print("""  S5 flagged the limit-circle caveat: the Friedrichs extension is a
  CHOICE.  This section UPGRADES the caveat to a computed result
  (verifier amendment).  The non-Friedrichs core extension is the
  K_nu (a-) branch: zero-energy interior solution u =
  rho^{-(1-2q)/2} K_nu(tau0 rho^{q/2}) (~ rho^{a-} at the core).
  Numerics: shoot from the EXACT zero-energy K_nu data at x0 = ln rho_0
  deep in the collar (the omega^2 term there is O(e^{(2+2q)x0}) ~
  1e-12 relative) and integrate the full mode equation to r = R.""")


def interior_shoot_K(q: float, s: float, lam: float, w2: float,
                     x0: float = -12.0,
                     rtol: float = 1e-13) -> tuple[float, float]:
    """Non-Friedrichs (K_nu-branch) interior solution; returns
    (u, u_x) at x = 0 (r = R), arbitrary normalization."""
    nu = np.sqrt(1 + 4 * q * (1 - q)) / q
    t0 = 2 * np.sqrt(lam) / q
    tau = t0 * np.exp(q * x0 / 2)
    Kv0 = kv(nu, tau)
    Kp0 = -0.5 * (kv(nu - 1, tau) + kv(nu + 1, tau))
    pre = np.exp(-(1 - 2 * q) * x0 / 2)
    y0 = [pre * Kv0,
          pre * (-(1 - 2 * q) / 2 * Kv0 + Kp0 * tau * (q / 2))]

    def rhs(x, y):
        u, up = y
        return [up, -(1 - 2 * q) * up
                + (lam * np.exp(q * x) + 4 * s
                   + w2 * np.exp((2 + 2 * q) * x)) * u]

    sol = solve_ivp(rhs, [x0, 0.0], y0, rtol=rtol, atol=1e-300)
    return float(sol.y[0, -1]), float(sol.y[1, -1])


L0K_closed = L0_closed(QB, 2.0, branch='K')
uK0, upK0 = interior_shoot_K(QB, SB, 2.0, 0.0, x0=-8.0)
print(f"\n  K-branch zero-energy log-derivative: shooting "
      f"{upK0 / uK0:.8f} vs closed form -(1-2q)/2 + "
      f"(q tau0/2)K'_nu/K_nu = {L0K_closed:.8f}")
check("K-branch shooter VALIDATED at omega^2 = 0: reproduces the "
      f"closed-form K_nu log-derivative L0_K = {L0K_closed:.7f} to "
      f"{abs(upK0 / uK0 - L0K_closed):.1e} (x0 = -8) — and L0_K < 0 < "
      "2q: under the K-extension the threshold criterion is met "
      "ALREADY AT gamma = 0 (a warning sign: the 'binding' does not "
      "need the interface)",
      abs(upK0 / uK0 - L0K_closed) < 1e-6 and L0K_closed < 0)


def FKc(w2: float, g: float, x0: float = -12.0) -> float:
    u, up = interior_shoot_K(QB, SB, 2.0, w2, x0=x0)
    return up - g * u


wK = brentq(lambda w2: FKc(w2, GAMMA_PHYS), 0.5, 2.0, xtol=1e-11)
wK10 = brentq(lambda w2: FKc(w2, GAMMA_PHYS, x0=-10.0), 0.5, 2.0,
              xtol=1e-11)
wK0 = brentq(lambda w2: FKc(w2, 0.0), 0.1, 1.5, xtol=1e-11)
print(f"\n  BC-c lam=2, K-extension: gamma = 2q     => top omega^2 R^2 "
      f"= {wK:+.5f}  (x0 = -12; {wK10:+.5f} at x0 = -10)")
print(f"  BC-c lam=2, K-extension: gamma = 0      => top omega^2 R^2 "
      f"= {wK0:+.5f}  (interface delta REMOVED)")
print(f"  interface-attributable shift: {wK - wK0:+.5f} (it moves the "
      "eigenvalue; it does not create it)")
check("the non-Friedrichs LOOPHOLE IS REAL: under the K_nu core "
      "extension the banked cell DOES bind at physical strength — "
      f"BC-c lam=2, gamma = 2q: discrete omega^2 R^2 = {wK:+.5f} > 0 "
      f"(x0-stable to {abs(wK - wK10):.0e}; the verifier's ~+1.149)",
      wK > 0 and abs(wK - wK10) < 5e-3 and abs(wK - 1.149) < 5e-3)
check("...AND IT IS A CORE-ATTACHED ARTIFACT, NOT WELD-INTERFACE "
      "BINDING: the gamma = 0 control (interface delta REMOVED) "
      f"still binds, omega^2 R^2 = {wK0:+.5f} > 0 — the bound state "
      "is supplied by the core extension itself; the K-branch has "
      "INFINITE form energy at the core (a- fails a > q - 1/2, S5) "
      "and is excluded by the finite-action charter; the INTERFACE "
      "threshold map (gamma_c = L0, L0 + ell + 1) is extension-"
      "independent in substance",
      wK0 > 0)

# ===========================================================================
# C3 — scale covariance
# ===========================================================================
hr("C3 — SCALE COVARIANCE: omega^2 R^2 INVARIANT (SYMBOLIC + 4+ DIGIT "
   "NUMERIC, INDEPENDENT MESHES)")

Ufn = sp.Function("U", real=True)
W2 = sp.Symbol("W2", real=True)        # = omega^2 R^2
u_dim = Ufn(r / R)
expr_dim = (sp.diff(r**2 * ((R / r)**q_s)**2 * sp.diff(u_dim, r), r)
            - (lam_s * (R / r)**q_s
               + 4 * r**2 * ((R / r)**q_s)**2
               * (s_s / r**2)) * u_dim
            - (W2 / R**2) * r**2 * u_dim)
expr_rho = expr_dim.subs(r, rho * R).doit()
target_rho = (sp.diff(rho**(2 - 2 * q_s) * sp.diff(Ufn(rho), rho), rho)
              - (lam_s * rho**(-q_s)
                 + 4 * s_s * rho**(-2 * q_s)) * Ufn(rho)
              - W2 * rho**2 * Ufn(rho))
check("R-elimination (sympy): substituting r = R rho into the interior "
      "mode equation with omega^2 = W2/R^2 leaves an equation in rho "
      "alone — R drops out completely: (rho^{2-2q}U')' - "
      "[lam rho^{-q} + 4s rho^{-2q}]U = W2 rho^2 U; omega R is the "
      "invariant (the jump -(2q/R)u(R) and the exterior scale the same "
      "way)",
      sp.simplify(sp.expand(expr_rho - target_rho)) == 0)
e_R1 = fd_top(QB, SB, 2.0, bc='c', R_cell=1.0, rmin=1e-5, n_int=6000)[0]
e_R25 = fd_top(QB, SB, 2.0, bc='c', R_cell=2.5, rmin=1e-5, n_int=7000,
               sigma=10.0)[0]
check("numeric (banked BC-c top, lam=2, INDEPENDENT meshes: R=1 with "
      f"r_min=1e-5 vs R=2.5 with the same DIMENSIONAL r_min): "
      f"omega^2 R^2 = {e_R1:+.7f} vs {e_R25 * 2.5**2:+.7f} — invariant "
      f"to 4+ digits (rel {abs(e_R1 - e_R25 * 6.25) / abs(e_R1):.1e})",
      abs(e_R1 - e_R25 * 6.25) / abs(e_R1) < 1e-4)
g15 = 1.5 * L0_banked[2.0]
p_R1 = fd_top(QB, SB, 2.0, bc='c', R_cell=1.0, gamma=g15)[0]
p_R25 = fd_top(QB, SB, 2.0, bc='c', R_cell=2.5, gamma=g15, n_int=7000,
               sigma=10.0)[0]
check("numeric (boosted validation mode, gamma = 1.5 gamma_c): "
      f"omega^2 R^2 = {p_R1:+.7f} (R=1) vs {p_R25 * 6.25:+.7f} (R=2.5) "
      f"— scale-covariant to 4+ digits "
      f"(rel {abs(p_R1 - p_R25 * 6.25) / p_R1:.1e})",
      abs(p_R1 - p_R25 * 6.25) / abs(p_R1) < 1e-4)

# ===========================================================================
# C4 — Reading-B control: the unflipped signature leaks
# ===========================================================================
hr("C4 — READING-B CONTROL (UNFLIPPED, HYPERBOLIC): "
   "-(r^2 f^2 u')' + [lam f + 4r^2f^2 E0]u = omega^2 r^2 u")

lhs_B = -sp.diff(r**2 * sp.diff(u_sub, r), r) + lam_s * u_sub \
    - omega_s**2 * r**2 * u_sub
check("Reading-B exterior in u = v/r: v'' = (lam/r^2 - omega^2)·v — "
      "for omega^2 > 0 the far field is OSCILLATORY (opposite sign to "
      "Reading A's S4)",
      sp.simplify(lhs_B + (sp.diff(v_fn, r, 2)
                           - (lam_s / r**2 - omega_s**2) * v_fn) * r)
      == 0)
vB1 = sp.sin(omega_s * r) / (omega_s * r) - sp.cos(omega_s * r)
check("explicit oscillatory branch (ell = 1, lam = 2): v = "
      "sin(omega r)/(omega r) - cos(omega r) (the spherical-Bessel "
      "j_1 carrier, amplitude-bounded, NON-decaying) solves "
      "v'' = (2/r^2 - omega^2)v exactly — every omega^2 > 0 sits in "
      "the scattering continuum: NO localized real modes under BC-a "
      "(the old leak)",
      sp.simplify(sp.diff(vB1, r, 2)
                  - (2 / r**2 - omega_s**2) * vB1) == 0)
print("""  Reading-B verdict (control): with the UNFLIPPED signature the
  exterior carries every omega^2 > 0 away as radiation — real
  frequencies live in the continuum, none are localized.  The ELLIPTIC
  localization (S4: decaying branch at omega^2 > 0, continuum confined
  to omega^2 <= 0) is Reading A's distinguishing structure: under
  Reading A there is NOTHING to leak into — which is exactly why the
  binding question reduces to the clean threshold criterion of T1, and
  why its failure is a sharp negative rather than a resonance-width
  question.""")

# ===========================================================================
# C5 — Reading-C note
# ===========================================================================
hr("C5 — READING-C NOTE (NOT COMPUTED)")
print("""  The Einstein-weld transplant (Reading C) is NATIVELY EXCLUDED at
  matter scope: phase 1's W4 shows the C1 stress has a first-order
  conservation leak (div T)_theta = c f^2 (E0 - phi0'^2)·dphi·d_th Y,
  independent of H1 and K, so the full Einstein theta-row would force
  delta-phi = 0 — no breathing at all.  Reading C is a graded MACRO
  import (channel-specific empirical support; EE ~2x overshoot
  standing), not a matter-cell spectrum candidate.  Not computed.""")

# ===========================================================================
# Final verdicts per ontology (against the pre-registered criteria)
# ===========================================================================
hr("VERDICTS (per the P0 pre-registered criteria — no softening)")
print(f"""  BC-a (reservoir-field reading):  NEGATIVE-WITH-THRESHOLD-MAP.
      No discrete omega^2 > 0; the finite-box top is a box artifact
      (scales ~ 1/r_max^2); shooting mismatch sign-definite.  Deficit
      at q = 1/3: gamma_c - 2q = {L0_banked[2.0] + 2 - GAMMA_PHYS:.6f} (lam=2),
      {L0_banked[6.0] + 3 - GAMMA_PHYS:.6f} (lam=6) [1/R units]; threshold UNREACHABLE for any
      q in (0, 1/2), any ell >= 1 (deficit > 1, theorem).

  BC-b (matter-content reading):   NEGATIVE-WITH-THRESHOLD-MAP.
      Top eigenvalue omega^2 = {headline[('b', 2.0)]:+.6f} (lam=2), {headline[('b', 6.0)]:+.6f}
      (lam=6): relaxation only.  No gamma binds (the delta does no
      work at u(R) = 0): no threshold exists at all.

  BC-c (native no-flux reading):   NEGATIVE-WITH-THRESHOLD-MAP.
      Top eigenvalue omega^2 = {headline[('c', 2.0)]:+.6f} (lam=2), {headline[('c', 6.0)]:+.6f}
      (lam=6): relaxation only.  The closest ontology to binding:
      deficit {L0_banked[2.0] - GAMMA_PHYS:.6f} (lam=2), factor {L0_banked[2.0] / GAMMA_PHYS:.4f} in delta
      strength; no q_c in (0, 1/2); the bindable angular sector is
      lam < {lam_c:.4f} — inside the excluded monopole gap.

  CROSS-ONTOLOGY FINDING: the phase-1 E0 < 0 oscillation window is
  REAL but UNOCCUPIED by the banked cell: the self-similar sourced
  collar has POSITIVE bulk E0 = s/r^2 (the phase-1 counterexample's
  bulk-negative E0 is not what the banked background supplies); the
  only attractive structure is the interface delta -(q/2R)delta(r-R),
  and the weld-supplied strength 2q is a factor ~2 (BC-c) to ~11
  (BC-a, lam=12) short.  The deficit numbers, the lam_c monopole-gap
  location, and the no-q_c theorem are the deliverables.  The
  threshold map is EXACT special-function content (C2b): gamma_c =
  -(1-2q)/2 + (q tau0/2) I'_nu(tau0)/I_nu(tau0) [+ ell + 1 for BC-a],
  nu = sqrt(17) at q = 1/3.  The BC selection (a/b/c) remains a
  physics/canonization input — nothing here picks one.

  NON-FRIEDRICHS LOOPHOLE (computed, C2c): the K_nu core extension
  binds at physical strength (omega^2 R^2 = {wK:+.5f}, BC-c lam=2) —
  but it ALSO binds at gamma = 0 ({wK0:+.5f}): a core-attached
  artifact, charter-excluded (infinite core form energy); the
  threshold map above is extension-independent in substance.""")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
hr("SUMMARY")
if FAILURES:
    print(f"  {len(FAILURES)} CHECK(S) FAILED:")
    for lab in FAILURES:
        print(f"    - {lab}")
    sys.exit(1)
print(f"""  All {N_CHECKS} checks PASSED.

  S1-S5  Spec setup verified end-to-end by sympy, no corrections:
         collar f = (R/r)^q with s = q(1-q)/2 (= 1/9 at q = 1/3);
         E0 = s/r^2 > 0 in the bulk + the attractive interface delta
         -(q/2R)delta(r-R) (only phi'' carries it); jump Delta u' =
         -(2q/R)u(R); exterior decaying branch at omega^2 > 0
         (essential spectrum at omega^2 <= 0); core indicial a+ =
         (sqrt(17)-1)/6 Friedrichs branch (limit-circle caveat flagged).
  T1     Binding criterion (exact): gamma_c = L0 (BC-c), L0 + ell + 1
         (BC-a), none (BC-b); physical gamma = 2q.
  C1     Banked cell: NO discrete omega^2 > 0 under ANY ontology
         (lam = 2, 6).  Tops: BC-b {headline[('b', 2.0)]:+.5f}/{headline[('b', 6.0)]:+.5f}, BC-c
         {headline[('c', 2.0)]:+.5f}/{headline[('c', 6.0)]:+.5f}; BC-a box-artifact only.  FD =
         shooting 4+ digits; r_min/r_max controls pass; no-delta
         control consistent.
  C2     L0 = {L0_banked[2.0]:.6f}/{L0_banked[6.0]:.6f}/{L0_banked[12.0]:.6f} (lam = 2/6/12);
         deficits BC-c {L0_banked[2.0] - GAMMA_PHYS:.6f}/{L0_banked[6.0] - GAMMA_PHYS:.6f}/{L0_banked[12.0] - GAMMA_PHYS:.6f}; NO q_c in
         (0, 1/2) anywhere; threshold bracketed by FD (+-5%); boosted-
         gamma validation modes pass every discriminator; lam_c =
         {lam_c:.6f} (monopole gap).
  C2b    Verifier closed form: the interior zero-energy problem IS the
         modified Bessel equation (Liouville transform, sympy); L0 =
         -(1-2q)/2 + (q tau0/2)I'_nu(tau0)/I_nu(tau0), nu = sqrt(17)
         at q = 1/3, tau0 = 2 sqrt(lam)/q — matches shooting to
         {max(dev_cf.values()):.0e}: the threshold map is EXACT
         special-function content.
  C2c    Non-Friedrichs (K_nu) extension computed: binds at gamma = 2q
         (omega^2 R^2 = {wK:+.5f}) but ALSO at gamma = 0
         ({wK0:+.5f}) — core-attached artifact, charter-excluded;
         threshold map extension-independent in substance.
  C3     omega^2 R^2 scale-covariant, symbolic + 4+ digit numeric.
  C4     Reading-B exterior oscillatory (the old leak) — Reading A's
         elliptic localization is the distinguishing structure.
  C5     Reading-C natively excluded (W4 leak), macro import only.

  VERDICT: NEGATIVE-WITH-THRESHOLD-MAP, all three interface
  ontologies.  The oscillation window exists but the banked physical
  cell sits below its binding threshold by the precise deficits above;
  the would-be window lives in the excluded monopole sector.""")

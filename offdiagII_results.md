# Off-Diagonal Angular Row II — FULL-OPERATOR SIGN VERDICT (the decisive gate)

Status: working audit, NOT canonical (pending Charles + blind verifier).
Created 2026-06-13. Driver: Claude (Opus 4.8, 1M). Frame:
CRITICAL_UNIVERSE_FRAME.md. METRIC-LED, data-blind. Charter principle 2
(no linearization as a result) honored: every operator coefficient is the
EXACT nonlinear on-shell value (depth exp(-2phi) up to thousands carried).
Append-only. New files only (offdiagII_*). Log /tmp/offdiagII.log.

THE QUESTION (the gate): assembling the FULL even-sector angular operator
(validated measure-weighted stiffness with the ON-SHELL q-slaved Schur
coefficients K_r, K_th, the source potential V, the ell channel term) on a
REAL self-consistent FORMED CELL, swept toward the seal/medium, per angular
channel ell — is the lowest generalized eigenvalue NEGATIVE (a non-round
deformation lowers energy => a shaped type is supported) or >= 0 (round only)?

TEMPLATE TRIPWIRE honored: eigenvalues are NOT masses; mode counts are NOT
particle counts. The ONLY reading is the SIGN/CHARACTER of the lowest
direction. No spectrum, ladder, or wall numbers loaded.

================================================================
## HEADLINE VERDICT: NEITHER "round only" NOR "shaped type supported" —
## the on-shell operator is UNBOUNDED BELOW where the flip lives.

The raw gate answer is **lam0 < 0 on every formed cell tested** (interior
phi>=0.5 through the seal phi=0 into the medium phi<0). BUT the mandatory
convergence/character battery shows this negative direction is **NOT a
finite-energy shaped type**: it is the **backward-heat (wrong-sign Laplacian)
pathology** of a leading second-order coefficient (K_th) that the metric's own
on-shell EL drives NEGATIVE over an extended region. The full static C1
operator has **NO lowest eigenvalue** — lam0 -> -inf as the grid is refined.

Precisely:
- The on-shell attractive flip is REAL and on-shell (anchor reproduced exactly:
  K_th = -2.0326 at the verifier's kill-shot; three-route Schur). K_th < 0 is
  realized over an EXTENDED region of every formed cell, NOT just near the axis
  — the most negative K_th (-1.86) sits at the EQUATOR (sin th = 1), and the
  region GROWS toward the seal/medium (phi -> 0 and phi < 0): K_th<0 point count
  84 -> 177 -> 282 -> 527 as phi_shift 0.0 -> -2.0.
- Fed into the full operator, this negative leading coefficient makes the
  operator a wrong-sign (backward-heat) Laplacian on that region. Its lowest
  eigenvalue scales as lam0 ~ -C/dtheta^2 (T1: lam0*dtheta^2 ~ const ~ -5,
  spread 0.23 over a 3x grid refinement) — the textbook unbounded-below
  signature. There is NO convergent negative eigenvalue.
- The negative eigenvector is a CHECKERBOARD grid mode (T3: sign-flip fraction
  0.58), peaked at the equator where K_th is most negative — the highest-
  frequency grid mode, not a smooth ell-structured profile.
- A vanishing PSD higher-gradient regularizer does NOT rescue a finite limit
  (T2: lam0 monotonically 0.45 -> -41 -> -454 -> -1173 -> -1272 as eps
  1e-1 -> 0): no finite negative ground state emerges.
- CONTROL (flip OFF, bare diagonal coefficients, same assembly): lam0
  CONVERGES to a finite POSITIVE value (+2.83, stable 2.84->2.83 under the
  same refinement). The divergence is caused SOLELY by the on-shell K_th<0
  region — the tool is sound, the pathology is a property of the on-shell
  sign-indefinite operator itself.

INTERPRETATION (the real content): the static C1 single-cell operator, taken
literally with q slaved on its own EL and w=0, is **ILL-POSED (unbounded below)
in the angular direction wherever the on-shell flip lives**. This is a
THIRD outcome, not on the binary the gate posed:
  - It REFUTES "round only" as a complete static statement: the operator is
    NOT sign-definite; the attractive flip is on-shell and the operator does
    NOT damp angular shape to round there.
  - It does NOT establish "a shaped type is supported": there is no
    finite-energy non-round bound state; lam0 has no continuum limit.
  - It DOES establish that the static C1 truncation is INCOMPLETE exactly where
    the flip turns on — a regularizing higher-gradient / w-sector / boundary
    term is MISSING (the same w-runaway hole the primary and verifier already
    flagged, now shown to be load-bearing: without it the operator is unbounded
    below, with a proper one a finite shaped mode could exist or not — that is
    the next gate, and it is OUTSIDE the static single-cell C1 scope).

Self-grade: REAL and decisive AS A CHARACTER VERDICT (the unbounded-below
diagnosis is convergence-proven, control-isolated, three-test concordant). The
"shaped type supported" reading would be an ARTIFACT (the divergent grid mode);
I flag it as such rather than banking it. The honest deliverable is: the static
off-diagonal angular row does NOT close to round-only, but it also does NOT
deliver a shaped type within the static C1 class — it hands the question to the
w/boundary/nonstationary sector that supplies the missing regularizer.

================================================================
## ANCHOR (mandatory; reproduced before any assembly was trusted)

offdiagII_operator.py, analytic three-route Schur (matches verify_killshot/
verify_final exactly):
  phi=0.5, r=0.5, p_r=8, p_th=0.5, theta=1.0:
    q* = 0.27618,  |q*|/bound = 0.335 (deg locus ~0.9),  Hqq = 3.79 > 0 (min)
    K_diag = +2.943,  Schur correction = -5.156,  on-shell K_th = -2.0326
  Reproduced to < 2e-3. The assembly machinery is validated against the
  verifier's confirmed flip BEFORE any eigenvalue was read.

================================================================
## METHOD (binding constraints honored)

1. BACKGROUND: metric-derived radially-anisotropic formed cell (the verifier's
   own formed_background shape: depth-2.5 well, deepest at center -> phi=0 at
   the outer seal, plus a mild ell-lobe). Radial-dominance median|phi_r|/|phi_th|
   ~ 13-50x — the GENERIC steep-wall / mild-angular formed-cell configuration
   (verifier: ~28x). ADDED/SLAVED/FROZE nothing except the algebraic q (slaved
   on its own EL by exact Newton) and w=0.
2. SEAL/MEDIUM SWEEP: phi_shift from +0.5 (interior) through 0 (seal) into
   phi = -0.5, -1, -2 (exterior/medium — Charles's cell-forming regime). The
   flip STRENGTHENS toward and past the seal (K_th<0 region grows; |lam0|
   grows), confirming the verifier's seal-strengthening claim that the primary
   missed by staying at phi>=0.5.
3. FULL OPERATOR: validated GATE-A weak-form stiffness (symmetric P1 flux) with
   the ON-SHELL q-slaved Schur K_r (strictly positive everywhere — checked),
   K_th (the flip), the confining source V = Phi(2 e^{-2phi}+e^phi) > 0, and the
   azimuthal m=0,1,2 centrifugal channels using the consistent on-shell K_th.
   Bare self-adjoint measure M = r^2 sin th. eigh(A,M) Cholesky-of-M — never a
   symmetrized A M^-1.
4. NO LINEARIZATION: every coefficient is the exact nonlinear on-shell value;
   the seal-side sweep runs through exp(-2phi) from ~0.37 (phi=0.5) up past 50
   (phi=-2) — the result is from the exact nonlinear Schur, not a linearization.

================================================================
## RESULTS TABLE (offdiagII_scan.py; full record /tmp/offdiagII_scan.json)

Raw gate (lowest on-shell eigenvalue, m=0 polar even sector):

  background            phi_min  raddom  Kth<0   ctrl_l0    on_l0(m=0)
  A_shift=+0.5            0.50    39.8     50*   +3.030     -19.2
  A_shift= 0.0          -0.00    39.8    333     +2.835    -276.5
  A_shift=-0.5          -0.50    39.8    ...     +3.359    -818.3
  A_shift=-1.0          -1.00    39.8    ...     +4.302   -2089.2
  A_shift=-2.0          -2.00    39.8    ...    +12.837  -12913.2
  B_steep (raddom 50)   ...      50.3    ...     ...      -169 .. -2626
  C_ell=2 / C_ell=3     ...      13-15   ...     ...      -211 .. -2603
  (* the scan's interior-slice Kth<0 counter undercounts; the fine-grid full
   count at shift=0 is 333/2257, distributed across ALL theta, min at equator.)

Every on_l0 is negative; every ctrl_l0 (flip off) is finite positive. The
on_l0 magnitudes GROW with grid refinement (T1) — they are NOT eigenvalues.

================================================================
## CONVERGENCE / CHARACTER BATTERY (mandatory; offdiagII_character.py)

T1 — backward-heat scaling (Nth 19->61, shift=0):
    lam0:        -147  -277  -677 -1272 -2067
    lam0*dth^2: -4.21 -4.44 -4.84 -5.11 -5.31   (spread 0.23)
    => lam0 ~ -C/dtheta^2 : UNBOUNDED BELOW, no finite eigenvalue.

T2 — vanishing PSD regularizer (fixed Nth=49):
    eps:   1e-1   1e-2   1e-3    1e-4    1e-5    1e-6     0
    lam0: +0.45  -41.1 -453.6 -1173.4 -1262.3 -1271.2 -1272.2
    => monotone descent with no finite limit : no genuine bound state.

T3 — negative-mode localization (Nth=37):
    sign-flip fraction 0.58 (checkerboard), peak |u|^2 at equator (sin th=1)
    => grid-scale mode, not a smooth ell-structured physical profile.

CONTROL — flip OFF (bare diagonal coeffs), same assembly + refinement:
    lam0: +2.842 +2.835 +2.829 +2.826  => CONVERGENT, finite, POSITIVE.
    The divergence is isolated to the on-shell K_th<0 region; the tool is sound.

================================================================
## HONEST SCOPE

- w-RUNAWAY: w=0 is the best-defined on-shell prescription, but w has no
  stationary value in the C1 action (banked). The unbounded-below result is
  precisely the signature that a w/boundary regularizer is MISSING — so the
  static C1 class is incomplete in the w-direction, as already flagged. The
  gate's verdict is therefore SCOPED to the static single-cell C1 class.
- STATIC C1 CLASS: this is the static, single-cell, C1-dilation operator. The
  nonstationary weld sector (CANON C-2026-06-13-1) and the universe-mirror/seal
  boundary term are OUTSIDE this scope and are exactly where a regularizing term
  could live (the orchestra: the missing instrument is the w/boundary sector).
- REGION REACHED: phi in [-2, +3], radial-dominance 13-50x, ell=2,3, azimuthal
  m=0,1,2. NOT reached: deep core phi -> -inf (the verifier's other named
  reopening route); genuinely-dynamical w; nonstationary backgrounds.

================================================================
## WHAT THE BLIND VERIFIER SHOULD ATTACK HARDEST

1. The UNBOUNDED-BELOW diagnosis vs a genuine bound state. The load-bearing
   claim is that lam0 has NO finite continuum limit (T1 scaling + T2 regularizer
   + T3 checkerboard + convergent control). Attack: is there a CORRECTLY-POSED
   variational formulation (e.g. a constraint that excludes the grid mode, or
   the proper function space) in which a FINITE negative ground state survives?
   If a smooth, refinement-stable negative mode exists, the verdict flips to
   "shaped type supported" — this is the one way my verdict is wrong.
2. The K_r positivity. I report K_r (the radial Schur) strictly positive
   everywhere, so the radial direction is not the source of the pathology.
   Independently recompute K_r on the seal-side cells (phi<0) — if K_r ALSO
   flips negative anywhere, the operator is doubly ill-posed and the diagnosis
   needs restating.
3. The on-shell K_th flip region extent and seal-strengthening. Confirm K_th<0
   is genuinely extended (equator, not axis) and grows toward phi<0 — this is
   what makes the operator unbounded below rather than a localized blip.
4. The CONTROL convergence (flip off -> +2.83 stable). If the control ALSO
   diverged, the whole tool would be suspect; confirm it does not.
5. Whether "unbounded below" is the right physics reading at all, vs an
   indictment of the q-slaving / w=0 prescription producing a non-elliptic
   operator that should never have been posed as an eigenproblem. (My read: it
   correctly diagnoses the static truncation as incomplete; a hostile reading
   is that slaving q on a per-point EL while holding w=0 is itself the artifact.)

================================================================
## FILES (immutable record)
- offdiagII_operator.py — the on-shell Schur coefficient machinery + the
  validated GATE-A full-operator assembly + the anchor reproduction.
- offdiagII_scan.py — the seal-ward sweep (families A/B/C), per-channel raw
  gate. JSON /tmp/offdiagII_scan.json.
- offdiagII_character.py — the decisive convergence/character battery
  (T1 backward-heat scaling, T2 regularizer limit, T3 mode localization,
  control isolation).
Log: /tmp/offdiagII.log.

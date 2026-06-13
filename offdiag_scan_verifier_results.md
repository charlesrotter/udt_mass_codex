# Off-Diagonal Angular Row — BLIND ADVERSARIAL VERIFIER RESULTS

Status: blind adversarial verifier pass on offdiag_scan_results.md.
NOT canonical (Charles canonizes). Append-only. New file.
Verifier: Claude (Opus 4.8, 1M), agent id `offdiag-verify-2026-06-13`.
Date: 2026-06-13. Frame: CRITICAL_UNIVERSE_FRAME.md.
Independent machinery: my OWN sympy second-variation + numpy probes
(NOT a re-run of the challenger's scripts). Log /tmp/offdiag_verify.log.
Hypothesis discipline honored: this result CONFIRMS the standing picture
(no vibration spectrum / round-only); per the charter I aimed HARDEST at
showing the attractive flip IS on-shell real — and it is.

================================================================
## VERDICT: PARTIALLY-CONFIRMED (SCOPED) — the headline is REFUTED as stated

The two infrastructure sub-claims (GATE A measure; w-runaway / q,w
algebraic) are INDEPENDENTLY CONFIRMED. But the LOAD-BEARING physical
headline — "on-shell the angular operator is SIGN-DEFINITE (round only);
the flip lives ONLY at the metric-degeneracy locus, which formed cells
never approach" — is **REFUTED**. With q slaved EXACTLY by the metric's
OWN algebraic EL and w=0 (the challenger's own on-shell prescription),
the on-shell angular stiffness K_th goes **NEGATIVE** at field
configurations that are (a) INSIDE the challenger's own claimed-safe
range phi in [0.5,4.0], (b) FAR from the degeneracy locus
(|q*|/bound ~ 0.01–0.34, not the ~0.9 the challenger asserted is
required), and (c) REALIZED ON A FORMED CELL'S OUTER WALL. The challenger
missed it because its decisive probe (offdiag_kth_probe.py) sampled
gradient ratios only up to pr/pth = 3x; the flip turns on for
RADIAL-DOMINANT anisotropy pr/pth >~ 6–16x, which is the GENERIC
formed-cell configuration (steep radial well wall + mild angular
structure), not a hostile corner.

SURVIVING STATEMENT (what is actually true):
- The self-adjoint measure is M = r^2 sin th (bare); e^{-2phi} lives in
  the stiffness. (CONFIRMED — the ~18000 negatives were a real
  double-count.)
- q, w are algebraic; w is a genuine runaway with no on-shell value in
  the C1 dilation action. (CONFIRMED.)
- With q slaved on its own EL, the on-shell angular operator is NOT
  sign-definite: a RADIAL-DOMINANT phi-gradient drives the q-Schur
  response large enough to flip K_th attractive at modest off-diagonal
  amplitude — well off the degeneracy locus. "Round only" is NOT
  established on-shell.

================================================================
## (1) IS THE MEASURE RIGHT? — YES (KILL-SHOT A confirmed)

Independent sympy (verify_measure3.py, verify_selfadjoint.py). The C1
dilation kinetic density on the diagonal areal slice is, EXACTLY:

    L_kin = e^{-4phi} r^2 sin th * phi_r^2  +  e^{-2phi} sin th * phi_th^2

This factors uniquely as [K_r phi_r^2 + K_th phi_th^2] * W with a SINGLE
weight W = r^2 sin th (bare), K_r = e^{-4phi}, K_th = e^{-2phi}/r^2
(cr/(K_r W) = 1, cth/(K_th W) = 1 exactly). The EL operator's principal
parts (coeff phi_rr = -2 W K_r; coeff phi_thth = -2 W K_th) match the
divergence form (1/W)[-d_r(W K_r d_r) - d_th(W K_th d_th)] under this same
W — i.e. the operator IS self-adjoint in <f,g> = INT f g W. Putting
e^{-2phi} in the MEASURE (W' = e^{-2phi} r^2 sin th) would NOT factor
consistently. The measure is correct; GATE A's flat-PSD recovery and zero
control-negatives are real. The verdict does NOT invert here.

================================================================
## (2) IS "ROUND ONLY" ESTABLISHED ON-SHELL? — NO. The flip is on-shell.

### w-runaway (KILL-SHOT B): CONFIRMED, but it does NOT establish round-only.
Independent sympy (verify_qw_el.py, verify_w_runaway.py): EL[q], EL[w] are
purely algebraic (no q,w derivatives at any order); tadpoles reproduce the
challenger's exactly. L(w) has dL/dw < 0 for all w, decays monotonically to
a finite asymptote, and sp.solve(dL/dw = 0, w) returns the EMPTY set — w is
a genuine runaway. The challenger's reading (i) — "w has no native value,
so the flip needs an import" — is half right: w indeed has no stationary
value. But that does NOT license w=0 as "the" on-shell choice; it is the
charter-permitted ALTERNATIVE reading (ii): the static problem is
INCOMPLETE in the w-direction. Crucially, the round-only verdict does NOT
hinge on w: even with w=0 (the challenger's own choice) the q-channel alone
flips K_th, below.

### q-slaved on-shell K_th (KILL-SHOTS C/D): the flip is REAL on-shell.
Independent sympy Schur reduction (verify_kth.py, verify_decomp2.py,
verify_killshot.py, verify_final.py). With q slaved exactly on dL0/dq = 0
(w = 0), the total on-shell angular stiffness is the Schur complement
K_th = (Hpp - Hpq^2/Hqq)/W. The diagonal piece Hpp/W ~ +2 e^{-2phi}/r^2 is
always positive, but the q-Schur correction -Hpq^2/Hqq/W is negative and,
for radial-dominant gradients, DOMINATES.

CLEAN KILL-SHOT POINT (phi = 0.5 = challenger's OWN lower bound,
r = 0.5, pr = 8, pth = 0.5):
    q* = 0.27618,   |q*|/bound = 0.335   (degeneracy needs ~0.9)
    Hqq = 3.79 > 0  (q* is a genuine MINIMUM, not a saddle)
    K_diag = +2.943,  Schur correction = -5.156,  K_th = -2.033
  THREE independent routes agree to 4 sig figs:
    analytic Schur = -2.0326 ; independent FD (re-slaved q*) = -2.0326 ;
    det(2x2 (pth,q) Hessian)/Hqq/W = -2.0326.
  h-stable (1e-3..1e-5). This is PHYSICS, not a grid/measure artifact.

This point is INSIDE phi in [0.5,4.0] and at |q*|/bound = 0.34 — NOT the
degeneracy locus. The challenger's claim that K_th flips ONLY at
|q*| -> r e^{phi} is FALSE.

### Why the challenger missed it.
Reproducing the EXACT probe grid of offdiag_kth_probe.py (phi in
{0.5,1,2,3,4}, r in {0.4,0.8}, (pr,pth) in {(0,0),(1,0),(0,1),(1,1),
(2,2),(3,1),(1,3)}) gives K_th > 0 at every point — I reproduce the
challenger's positive result EXACTLY. The grid's maximum radial dominance
is (3,1) = 3x. Sweeping pr/pth at phi=0.5, r=0.4: the flip turns on between
pr/pth = 3x (K = +7.4) and pr/pth >~ 6x (K < 0). The challenger's grid
simply never entered the radial-dominant region where the flip lives.

### It is REALIZED on a formed cell.
verify_formed2.py: a formed cell (depth 2.5, mild ell=2 lobe, the
challenger's own formed_background shape) has |phi_r|max ~ 6, |phi_th|max
~ 0.2 — radial-dominant by ~28x, the GENERIC well-wall configuration. The
analytic on-shell Schur K_th is NEGATIVE at ~108 interior points with
|phi_th| > 0.02 and |q*|/bound < 0.7; the outer-wall band (r ~ 0.89,
phi ~ 0.62, pr ~ -5.5, pth ~ -0.04) gives K_th ~ -0.04 to -0.06 at
|q*|/bound ~ 0.01-0.02 — FAR from degeneracy. (Magnitude is small because
the lobe is mild, so phi_th is tiny; it is nonzero and the sign is robust
across the analytic/FD/det routes.) The flip is the GENERIC formed-cell
behavior at the wall, not a corner the metric avoids.

================================================================
## (3) IS THE REOPENING ROUTE LIVE? — YES, and wider than scoped.

The challenger scoped the one reopening route to the degeneracy locus
reachable only by deep-core / nonstationary / welded cells OUTSIDE the
static single-cell class. My finding makes the reopening route LIVE
WITHIN the static single-cell class itself:

- The flip does NOT require the degeneracy locus. It requires
  RADIAL-DOMINANT phi-gradient (pr/pth >~ 6-16x) at modest |q*|, which is
  exactly the formed-cell wall.
- It strengthens toward the SEAL and EXTERIOR (phi -> 0 and phi < 0):
  K_th is more negative at phi = 0, -0.5, -2 (exterior/medium — Charles's
  cell-forming regime per the exterior-field memory). The challenger
  tested only phi >= 0.5 (cell interior) and so never saw the
  seal/exterior strengthening.
- The deep-core (phi -> -inf) and nonstationary (CANON C-2026-06-13-1)
  routes the challenger named are ALSO live and now over-determined: the
  flip is already present in the shallow static class.

================================================================
## REGISTRY CONSEQUENCES (the named re-grade)

The angular_completeness suspensions (#1/#2/#3/#5 ell>=2, the
DIAGONAL-CLASS premise) were up for re-grade on self-consistent
backgrounds. This verifier pass finds:

- They should REMAIN SUSPENDED / CONDITIONS-CHANGED, NOT reinstated. The
  challenger's attempted re-grade ("flip is off-shell, reinstate
  round-only") does NOT hold: on a self-consistent background with q
  slaved on the metric's own EL, the attractive angular flip SURVIVES at
  formed-cell field strengths away from the degeneracy locus.
- The angular_completeness CALIBRATION ("formed maps scheme-conditional;
  decisive test is q,w-on self-consistent backgrounds") is VINDICATED: the
  decisive test, run honestly, shows the flip IS on-shell.
- What IS newly banked (challenger's correct contributions): the bare
  measure M = r^2 sin th; the w-runaway (w not slaveable in the C1 action
  alone); the q-only slaving as legitimate. These survive.

OPEN / NOT closed by this pass:
- Whether the attractive K_th, fed into the full GATE-A generalized
  eigenproblem on a formed cell, produces a genuine sign-INDEFINITE
  operator (a supported shaped type) or is dominated by the confining
  potential V over the cell as a whole. I verified the COEFFICIENT K_th
  flips; the full-operator eigenvalue verdict on a self-consistent cell is
  the next gate and is NOT settled here. (The challenger's own
  selfconsistent assembler conflated this with measure artifacts; a clean
  re-run is owed.)
- The w-sector remains genuinely incomplete (runaway): a native confining
  contribution (seal boundary term / nonstationary / mirror closure) could
  make w dynamical and further reopen — unchanged from the challenger's
  honest scope.

================================================================
## STRONGEST POINT FOR / AGAINST THE NEGATIVE

FOR the negative (round-only): the measure is genuinely correct, the
control negatives were a real double-count, and on the SYMMETRIC /
mild-gradient interior the on-shell stiffness IS positive — the challenger
reproduced cleanly. If formed cells were gradient-isotropic, round-only
would hold.

AGAINST the negative (decisive): formed cells are NOT gradient-isotropic —
the radial well wall is steep while angular structure is mild, exactly the
pr/pth >> 1 regime where the q-Schur response flips K_th attractive. The
flip is on-shell (q slaved on the metric's own EL), three-route robust,
away from degeneracy, inside the claimed range, and present on a formed
cell. The headline overgeneralized from an under-sampled probe grid.

================================================================
## FILES (this verifier; immutable)
- /tmp/verify_measure3.py, /tmp/verify_selfadjoint.py — measure (A).
- /tmp/verify_qw_el.py, /tmp/verify_w_runaway.py — q,w algebraic + runaway (B).
- /tmp/verify_kth.py, /tmp/verify_decomp2.py — on-shell K_th decomposition.
- /tmp/verify_seal.py, /tmp/verify_flipmap.py — the (phi, anisotropy) flip map.
- /tmp/verify_killshot.py, /tmp/verify_final.py — the clean 3-route kill-shot.
- /tmp/verify_formed2.py — flip realized on a formed cell wall.
- /tmp/verify_reproduce.py — reproduces challenger's positive grid + shows the gap.
Log: /tmp/offdiag_verify.log.

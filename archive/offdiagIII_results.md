# Off-Diagonal Angular Row III — THE COMPLETION GATE (anti-invention)

Status: working audit, NOT canonical (pending Charles + blind verifier).
Created 2026-06-13. Driver: Claude (Opus 4.8, 1M). Frame:
CRITICAL_UNIVERSE_FRAME.md. METRIC-LED, data-blind. THE CENTRAL DISCIPLINE:
ANTI-INVENTION (charter principle 1) — no regularizer/stiffness term may be
ADDED because it would help; any completion must be UNCOVERED in the metric's
OWN action as a term the static single-cell C1 truncation DROPPED. Charter
principle 2 honored (every coefficient is the exact nonlinear on-shell value;
depth e^{-2phi} carried). Append-only. New files only (offdiagIII_*).
Log /tmp/offdiagIII.log.

THE GATE (the decisive sub-question continuing #38): DOES THE METRIC'S OWN
ACTION CONTAIN A NATIVE TERM — dropped by the static single-cell C1
second-order truncation — THAT (a) is active where K_th<0 and (b) BOUNDS THE
OPERATOR BELOW? A wrong-sign 2nd-order coefficient is unbounded regardless of
any potential V, so the bounding term must be HIGHER-DERIVATIVE (e.g. a
positive biharmonic-like +( d_th^2 v)^2) or an equivalent native mechanism.

TEMPLATE/INVENTION TRIPWIRES honored: the verdict is BOUNDEDNESS + sign
CHARACTER (does a FINITE non-round shaped type exist), NOT a mode count, NOT a
frequency ladder, NOT masses. No wall numbers loaded. Every term tested as a
candidate is the metric's OWN previously-dropped term, with provenance; no
by-hand stiffness/regularizer was banked (the W2–W8 dead end — flagged where
the empirics show it is the ONLY thing that would work).

================================================================
## HEADLINE VERDICT (STEP 3): THE METRIC SUPPLIES NO NATIVE BOUNDING TERM
## IN THE STATIC SINGLE-CELL C1 CLASS. The completion is NOT here.

The metric's own action — pure dilation-kinetic
`S_phi = -(c/2) INT e^{-2phi}(d phi)^2 sqrt(-g4)` PLUS the algebraic ON
potential `-Phi((1/2)e^{-2phi}+e^{phi})sqrt(-g4)` (UDT_REBUILD.md §1; the
metric IS phi, B=1/A makes the Einstein source tautological, so there is NO
independent Einstein-Hilbert R term to mine) — contains NO native
higher-derivative (or equivalent) term, dropped by the static single-cell C1
truncation, that bounds the wrong-sign angular operator below where the
on-shell flip (K_th<0) lives. Each of the four NAMED suspects was DERIVED, not
asserted, and each FAILS to bound — for a structural, provenance-clear reason:

- **(i) w (sphere-shape g_thth AND time-theta g_ttheta) gradient/higher-deriv:
  ABSENT.** The density carries NO derivative of w (or q) at ANY order — both
  off-diagonal/shape fields enter ONLY ALGEBRAICALLY through g^{ab} and
  sqrt(-g) (`L.has(d w)=False`, derivative order of the density = 1, carried
  by phi alone). A field absent from L as a gradient cannot supply ANY
  gradient/biharmonic term at ANY order of fluctuation expansion (expansion
  differentiates in the FIELD; it cannot manufacture a coordinate-derivative
  the density lacks). The "cubic-order w" entry of angular_completeness is,
  made precise (eps^3 expansion), an ALGEBRAIC cubic COUPLING dw·{...}, not a
  kinetic term. w is a STIFF ALGEBRAIC (mass) direction: at the static
  stationary point w=0, L is even in w, L_ww=+16.18>0, and L_pw=L_qw=0, so the
  joint (q,w) Schur EQUALS the q-only Schur EXACTLY (K_th=-2.03256) — the
  w-Schur correction is EXACTLY ZERO, not merely bounded. NO bounding term.
- **(ii) the phi-angular cross coupling d_pr×d_pth ~ phi0_r phi0_th: PRESENT
  but 2nd-ORDER.** It multiplies (d_r u)(d_th u) — a first×first derivative
  product, derivative order 2. It modifies the principal SYMBOL at the SAME
  order as the pathology (indeed it is part of WHY K_th flips: the radial
  gradient enters K_th through exactly this q-channel cross-response). A
  2nd-order term CANNOT bound a wrong-sign 2nd-order Laplacian. NOT bounding.
- **(iii) curvature / EH-remainder (Kretschmann-type): ABSENT from the
  action.** The density is FIRST-ORDER in field gradients (highest derivative
  order = 1), so its EL is at most SECOND-ORDER and there is NO native
  higher-derivative term. The metric IS phi; the Einstein tensor is
  tautological (B=1/A ⇒ G^t_t=G^r_r). Introducing an independent
  sqrt(-g)R / R^2 / Kretschmann term to mine a biharmonic would be an IMPORT,
  forbidden by principle 1. NOT available.
- **(iv) the seal area-form (#36): a BOUNDARY datum only — NOT a bulk
  regularizer.** #36 is an EXACT boundary transgression
  `d ln f ^ omega_H1 = d[(ln f)omega_H1]`, "invisible to the bulk EL" (its own
  words); by Stokes it contributes ZERO to the bulk operator. Numerically, the
  unbounded-below divergence is driven by HIGH-FREQUENCY INTERIOR modes that
  vanish at the endpoints, so even the MAXIMAL boundary term (Dirichlet,
  alpha→inf) leaves lam0 bit-identical → -inf. A pure BC cannot bound a bulk
  wrong-sign Laplacian. (#37 confirms the area form is sigma-even, EXACT, adds
  no bulk higher-derivative structure.) NOT bounding.

CONSEQUENCE (the domino, NOT a failure): the static single-cell C1 class
genuinely CANNOT host the completion. The off-diagonal angular row is HANDED,
cleanly and for a derived reason, to the CLOSED-CELL (#36/#37 as the WHOLE,
with both seals live and the matter-cell core closure) and NONSTATIONARY
(CANON C-2026-06-13-1, the propagating phi-angular sector) WHOLE. This is a
real result: it converts #38's "incomplete, a regularizer is missing" into the
SHARP statement that the missing regularizer is NOT a previously-dropped static
single-cell term — the completion requires LEAVING the static single-cell
class (a genuine c_r^2/c_th^2 wave term from C-2026-06-13-1, or the
two-seal/core closure of #37). It is NOT a license to invent a stiffness term.

================================================================
## STEP 1 — THE DERIVATION (anti-invention; offdiagIII_derive.py)

ANCHOR (my own machinery, reproduced before any suspect claim trusted):
phi=0.5, r=0.5, pr=8, pth=0.5, theta=1.0 → q*=0.27618, Hqq=3.7915>0,
on-shell K_th = -2.03257 (target -2.0326, <2e-3). The on-shell wrong-sign flip
is real (build on #38).

THE ACTION'S DERIVATIVE CONTENT (the decisive structural fact). Building the
full density with phi, q, w (BOTH w=sphere-shape g_thth=r^2 e^{2w} AND
w=time-theta g_ttheta carried, independently) as functions:
- highest derivative order present in the density = **1** (phi-gradients only);
- `L.has(d_r w)=False`, `L.has(d_th w)=False`, same for q — at ALL orders.
So the EL is at most 2nd-order, there is NO native higher-derivative term, and
neither off-diagonal field carries a gradient. This single fact closes
suspects (i) and (iii) at the level of the action itself.

THE TWO "w" FIELDS (a corpus naming collision, both checked). angular_
completeness / offdiag_qw_derive use w = SPHERE-SHAPE (g_thth); the offdiagII
verifier (v4_joint_qw) used w = TIME-THETA (g_ttheta). I checked BOTH:
- sphere-shape w: algebraic, no gradient (confirmed; cubic coupling only).
- time-theta w: at pt=0 (static) dL/dw is ODD in w, vanishes EXACTLY at w=0,
  L_ww=+16.18>0 ⇒ w=0 IS the static stationary point (a genuine minimum), and
  L_pw=L_qw=0 there ⇒ joint (q,w) Schur = q-only Schur = -2.03256 EXACTLY.
Both confirm: w is a stiff algebraic mass, contributing a BOUNDED (here EXACTLY
ZERO) Schur shift — never a higher-derivative bounding term. (v4_joint_qw.py
re-run reproduces L_pp=0.657, L_pq=-2.028, L_pw=0, L_qq=3.79, L_ww=16.18,
L_qw=0, detH=61.4, K_th_joint=K_th_qonly=-2.03256.)

CUBIC-ORDER w EXPANSION (/tmp/offdiagIII_wcubic.py, subagent a84aebb7):
eps^3 expansion about a formed background — every dw term at orders 1,2,3 has
ZERO dw-derivative atoms; dw appears only undifferentiated. L1 = the banked
tadpole -2 dw e^{-2phi0}|sin th| phi0_th^2 (spherical-vanishing); L2 dw^2
coeff = +2 e^{-2phi0}|sin th| phi0_th^2 ≥ 0 (the algebraic mass); L3 = dw ×
algebraic. NO higher-derivative term, confirming (i) to cubic order.

================================================================
## STEP 1 — EMPIRICAL CLOSURE (GPU torch float64; offdiagIII_converge.py)

(A) #38 reproduced in my OWN tool on the on-shell K_th<0 wall slice (bare
measure M=sin th, P1 stiffness, generalized eigvalsh via explicit Cholesky-of-M
inverse per the CLAUDE.md broadcast pitfall):
    Nth   Kth_min   lam0_on   lam0*dth^2   lam0_ctrl
     33   -0.274   -120.99    -1.0931      ~0
     65   -0.274   -484.75    -1.0949      ~0
    129   -0.274  -1940.03    -1.0954      ~0
    257   -0.274  -7761.20    -1.0956      ~0
    513   -0.274 -31045.89    -1.0956      ~0
lam0 ~ -C/dth^2 (UNBOUNDED BELOW, #38 reproduced); the flip-off control
converges finite. Baseline confirmed.

(B) EACH native previously-dropped candidate FAILS to bound (nothing invented):
- (iv) seal/boundary, alpha=0/1e2/1e8 (Dirichlet): lam0(65,129,257) =
  [-484.7, -1940.0, -7761.2] IDENTICALLY — boundary term does not touch the
  interior divergence.
- (ii) native 2nd-order cross term, read as over-generously +|cross|: lam0 =
  [-459.7, -1839.7, -7359.9] — still diverging (same-order, cannot bound).
- (i) the REAL w-Schur shift = 0 (L_pw=L_qw=0): leaves the on-shell row
  untouched → diverges. (A demonstrative +1/+3 UNIFORM shift DOES converge it —
  but that uniform stiffness is exactly the FORBIDDEN W2–W8 import, NOT what
  the bounded w-Schur supplies. This is the anti-invention point made
  empirical: the ONLY thing that bounds the operator is a by-hand uniform
  stiffness term the metric does not contain.)

================================================================
## SELF-GRADE (real vs artifact) + WHAT THE BLIND VERIFIER SHOULD ATTACK

Self-grade: REAL and decisive as an ANTI-INVENTION verdict. The load-bearing
facts are structural and provenance-clean: (1) the action is first-order in
gradients (no native higher-derivative term — verifiable by inspection of the
density's derivative atoms); (2) both off-diagonal/shape "w" fields are
algebraic (no gradient at any order); (3) #36 is a bulk-invisible boundary
transgression (Dirichlet doesn't bound the bulk — numerically shown
basis-independently here and by the seal subagent). The verdict CONFIRMS the
standing picture (the completion lives in the closed/nonstationary WHOLE, per
CRITICAL_UNIVERSE_FRAME and C-2026-06-13-1), so per hypothesis discipline I
aimed hardest at finding a native bounding term that would REOPEN the static
class — and found none.

INVENTION TEMPTATIONS RESISTED (flagged honestly): (a) the empirics show a
uniform +1 K_th shift converges the operator — it would have been an "evil
genie" easiest-response to bank a "stiffness completion." REFUSED: it is the
banked-dead W2–W8 by-hand stiffness, not a native term. (b) The temptation to
read the seal #36 as a bulk regularizer (it is named in the registry as the
home of the completion) — REFUSED after the Stokes argument + the
Dirichlet-doesn't-bound numeric. (c) The temptation to add an R^2/Kretschmann
term "because GR has one" — REFUSED: the metric IS phi, there is no independent
EH term; that is an IMPORT.

ATTACK HARDEST HERE (for the blind verifier):
1. **The "no native higher-derivative term" claim hinges on the ACTION being
   exactly the pure dilation-kinetic + algebraic potential.** If the TRUE UDT
   action carries any term with a SECOND field-derivative (a genuine
   sqrt(-g)R that does NOT reduce to the C1 kinetic via B=1/A; a Gibbons-
   Hawking-type term that is NOT a pure boundary; a higher dilation-gradient
   term e^{-2phi}(Box phi)^2), the verdict could flip. Independently confirm
   the density is first-order in gradients and that B=1/A genuinely makes the
   Einstein sector tautological (no independent 2nd-derivative term).
2. **The two-w distinction.** Confirm BOTH the sphere-shape and the time-theta
   w are algebraic, and that NEITHER, properly carried, adds a gradient term.
   Attack whether a THIRD off-diagonal/shape component (e.g. a g_rphi or a
   genuinely-time-dependent w in the NONSTATIONARY sector) carries a kinetic
   term — that is exactly the handoff target, so finding one there CONFIRMS the
   handoff rather than refuting the verdict; finding one IN STATICS would
   refute it.
3. **The bulk-invisibility of #36.** Confirm by Stokes that the exact
   transgression contributes zero to the bulk EL, and that the
   Dirichlet-limit numeric (boundary term leaves lam0 → -inf) is right. The
   one way (iv) is wrong: if omega_H1 enters the BULK leading coefficient as a
   positive curvature weight (not a boundary term), it could bound — argue
   from #37 (sigma-even, EXACT) that it does not.
4. **Whether STEP 3 over-concludes.** The honest scope is: NO native bounding
   term EXISTS IN THE STATIC SINGLE-CELL C1 CLASS. It does NOT claim the
   nonstationary/closed WHOLE lacks one (the c_r^2, c_th^2 wave term of
   C-2026-06-13-1 is a genuine 2nd-time-derivative term outside this scope and
   is the natural next gate). Confirm the verdict is correctly scoped and not
   inflated to an absolute no-go.

================================================================
## SCOPE / PREMISE SET (for NEGATIVES_REGISTRY)

Background: static, single-cell, C1-dilation, formed cell (radial-dominant
wall). Action: pure dilation-kinetic + algebraic ON potential (the metric IS
phi; no independent EH term). Reduction: q slaved on dL0/dq=0 (its own EL),
w=0 (the static stationary point; both sphere-shape and time-theta w checked,
each algebraic/stiff). Region: the on-shell K_th<0 wall slice, phi in [-2,+3].
NOT reached / explicitly handed off: the NONSTATIONARY sector (C-2026-06-13-1,
where a genuine 2nd-time-derivative wave term lives) and the CLOSED two-seal /
core-closure WHOLE (#36/#37). If a native bounding term is later found there,
this "no static-single-cell completion" loses no authority (it was scoped to
statics) — it POINTS to where the completion must be.

================================================================
## FILES (immutable record)
- offdiagIII_derive.py — STEP 1: the four-suspect derivation from the metric's
  own action; anchor reproduction; the density-derivative-order fact; the two-w
  check; the 2nd-order cross-term order; #36 bulk-invisibility statement.
- offdiagIII_converge.py — STEP-1 empirical closure (GPU torch float64): #38
  divergence reproduced; each native candidate (boundary/Dirichlet, real
  w-Schur, 2nd-order cross) shown NOT to bound; the forbidden uniform-stiffness
  shown to be the only cure.
- offdiagIII_wcubic.py (subagent a84aebb7; copied into repo) — eps^3
  w-expansion: no w-derivative at any order; cubic coupling algebraic; L_ww>0.
- offdiagIII_sealbound.py (subagent a8c6685b; copied into repo) — #36 boundary
  term vs bulk: Dirichlet (alpha→inf) leaves lam0 → -inf, basis-independent
  (P1 FEM + sine Galerkin).
- /tmp/v4_joint_qw.py (prior offdiagII verifier, re-run) — time-theta w static
  stationarity, joint (q,w) Schur = q-only.
Log: /tmp/offdiagIII.log.

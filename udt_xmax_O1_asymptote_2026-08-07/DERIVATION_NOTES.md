# O1 — the lambda_t -> 0 boundary + the asymptote theorem (exact derivation notes)

Date 2026-08-07 | branch grok | MODE OBSERVE | Status: **LEAD / UNBANKED** (two adversarial
reviews owed per the frozen contract before any banking). Contract: `PREREGISTRATION.md`.
Script: `derive_o1.py` (exact sympy 1.13.1, CPU, float-free; 47 machine checks, output in
`run_output.txt`). Not committed.

## Ground (cited at source; no code imported)
- `udt_complete_pair_phi_orchestra_audit_2026-08-05/EXACT_DERIVATION.md`: comparison arrow
  A "typed INVERTIBLE" (sec.2 — constitutive, load-bearing below); strain C_A = A^dag A,
  A^dag = g_p^{-1} A^T g_q; conjugacy data endpoint-frame invariant (C_A -> L_p C_A L_p^{-1});
  delta_t = -(1/2) log(lambda_timelike), regular-stratum extractor (sec.3); reversal
  delta_t(A^{-1}) = -delta_t(A) (sec.3); cocycle laws are the REQUIRED type of a physical
  depth (sec.6), NOT a banked theorem that delta_t is a cocycle on all arrows.
- `udt_ceff_profile_binding_test_2026-08-06/DERIVATION_NOTES.md`: lambda_t = e^{-2 Delta phi}
  on the reciprocal subgroup; c_eff = c_E * lambda_t identity; 4-slot strain diag structure;
  mixing witness (sec.4 of the audit) changes lambda_t.
- `udt_mixing_channel_lane_2026-08-06/DERIVATION_NOTES.md`: mu = invariant reciprocal-lock
  defect, lambda_t*lambda_radial = 1 IFF mu = 0, scoped s != r; clock-screen block charpoly
  (verification-corrected constant term s^2/r^2); elliptic window; additivity defect at mu != 0.

## Q1 — the wall as an object (mu = 0 stratum; strain diag(lambda_t, 1/lambda_t, s^2, s^2))

All statements machine-checked in `derive_o1.py` (Q1_* keys).

**(a) Invariants as lambda_t -> 0+ (reciprocal tie lambda_r = 1/lambda_t):**
- e1 (trace), e2, e3 all DIVERGE (each carries a 1/lambda_t term)   [Q1_limit_e1..e3 = oo]
- e4 = det C_A = s^4 stays FINITE and NONZERO                        [Q1_limit_e4 = s^4]
- lambda_t itself (the causally-labeled root, invariant on the regular stratum) -> 0;
  the extractor delta_t = -(1/2) log lambda_t -> +infinity.
So the wall is NOT a singular degeneration of the strain (det survives); three of the four
char-poly coefficients blow up through the reciprocal partner.

**(b) Arrow invertibility / does the limit exist in the arrow space?** Along the reciprocal
path D_r = diag(1/r, r, 1, 1), lambda_t = 1/r^2 -> 0 means r -> infinity:
- det A = 1 for ALL r (invertibility never degrades)                 [Q1_detA_along_path]
- det C_A = 1 for ALL r                                              [Q1_detC_along_path]
- but the radial entry r -> infinity                                 [Q1_arrow_entry_r_limit = oo]
The family stays invertible at every point, yet has NO limit in the space of finite matrices:
the wall is not an arrow, and (on this stratum) not even a finite-matrix boundary point of the
arrow space. It exists only as an IDEAL point (escape to infinity) — exactly the structure of
the SR boost family as v -> c (gamma -> infinity, matrices diverge).
In the PROJECTIVE closure the limit DOES exist and is characterizable: C/trace ->
diag(0,1,0,0), a RANK-1 projective strain concentrated on the radial-partner eigenline
[Q1_projective_limit_strain, rank = 1].

**(c) Eigenline fate.** The timelike eigenline e_0 is an eigenvector of C for EVERY r
(eta(e_0,e_0) = -1) and survives to the boundary — in the projective limit it survives as the
KERNEL direction of the rank-1 limit strain [Q1_e0_eigvec_all_r; Q1_timelike_e0_in_kernel].
The causal labeling never fails on the way to the wall; what fails AT the wall is positivity
of the labeled eigenvalue (lambda_t = 0 is outside the regular stratum's lambda > 0 demand).

**(d) What the wall IS (orchestra-natively).** Two distinct faces bound the regular stratum:
- the SINGULAR face: det A -> 0, finite matrices, lambda_t = 0 attained — but these are not
  comparison arrows (invertibility is constitutive of the banked arrow type / groupoid);
- the IDEAL face: entries diverge, det bounded away from 0, lambda_t -> 0 asymptotically.
THE RECIPROCAL TIE CLOSES THE SINGULAR FACE ON THE LOCK: lambda_t * lambda_r = 1 forces the
partner to blow up, so det C cannot -> 0 through lambda_t; the only route to the wall on the
mu = 0 stratum is escape to infinity. The wall is a BOUNDARY STRATUM OF THE (projective)
CLOSURE, never an element of the comparison groupoid: this is the exact algebraic content of
"gamma-type asymptote" — same structure as SR's v = c (LEAD; scoped to the mu = 0 stratum).

## Q2 — the asymptote theorem, content honestly located

### (a) EXACT ADDITIVITY — scope (banked + derived)
- Banked: reciprocal collinear subgroup D_{r1} D_{r2} = D_{r1 r2} (audit sec.3 reduction);
  mixing lane banked additivity EXACT at mu=0 for the diagonal family, BROKEN at mu!=0
  (defect witness ~0.0121). The audit's sec.6 cocycle law is the REQUIRED TYPE of a physical
  depth, not a banked theorem for delta_t on all arrows — scope matters.
- Machine re-verified here: collinear group law + additivity exact [Q2a_collinear_*].
- NEW (derived): additivity is exact on the LARGER full-diagonal subgroup — reciprocal
  squeezes along DIFFERENT SPATIAL AXES commute and the timelike eigenvalue FACTORIZES:
  lambda_t = e^{-2(p+q)} exactly for a 0-1 squeeze composed with a 0-2 squeeze
  [Q2a_multiaxis_*]. Likewise a SPATIAL-ROTATION twist of the second leg's axis leaves e_0 a
  shared eigenvector: exact additivity for ANY axis angle theta (general symbolic theta)
  [Q2a_rotation_twist_e0_eigvec]. Spatial-axis non-collinearity does NOT break additivity.

### (b) THE NON-COLLINEAR COMPOSITION LAW (the substantive leg) — INEQUALITY REVERSES
The twist that matters is a relative BOOST between the frames in which each leg is reciprocal
(the legs' timelike eigenlines differ by rapidity w) — not a spatial rotation. In the 2x2
Lorentzian block (legs: P1 depth p; B = L_w D_q L_w^{-1} depth q [Q2b_legB_charpoly_no_w —
the twist does not change leg B's own depth]; composite arrow B o P1):

    cosh(2 delta_comp) = cosh(2(p+q)) + 2 sinh^2(w) sinh(2p) sinh(2q),  det C = 1
    [Q2b_TRACE_LAW_cosh2delta = True, exact symbolic; Q2b_det_CM = 1]

- SAME-SIGN legs (p,q > 0): the correction is >= 0, POSITIVE for w != 0
  [Q2b_correction_positive_offcollinear] => delta_comp >= p + q: **SUPER-additive.**
  Equality IFF w = 0 (collinear) or a leg depth vanishes [Q2b_correction_zero_at_w0].
- The composite depth is UNBOUNDED in the twist at FIXED leg depths: as w -> infinity,
  cosh(2 delta_comp) -> infinity [Q2b_limit_w_inf_same_sign; sign factor
  (e^{4p}-1)(e^{2q}-e^{-2q}) > 0]. TWO finite-depth legs approach the wall arbitrarily
  closely as their relative twist grows.
- Exact rational witness (e^p = e^q = 2, cosh w = 5/4): half-trace = 6137/512 > 257/32
  (the collinear value), lambda_t < 1/16 = e^{-2(p+q)}, and the small-eigenvalue eigenline
  IS eta-timelike (labeling verified, not assumed) [Q2b_witness_*].
- 3D out-of-plane check (0-2 boost twist on 0-1 squeezes, exact rationals): all composite
  strain roots real positive, lambda_t < 1/16, min root's eigenline eta-timelike
  [Q2b3_*]. Pocket hunt over rotation/boost twist combinations: rotation-only = EXACTLY
  additive; every combination containing a boost = SUPER-additive; NO sub-additive pocket
  found at the sampled points [POCKET_*].
- OPPOSITE-SIGN legs: cosh(2 delta) = cosh(2(p-q)) - 2 sinh^2 w sinh 2p sinh 2q
  [Q2b_TRACE_LAW_opposite_sign]: large twist drives the composite OFF the regular stratum —
  elliptic window (|tr|/2 < 1: complex unit-modulus pair, no real depth; witness 287/512)
  or negative-real branch (tr/2 < -1; witness -1513/512) [ESC_elliptic/negative_exit]. In
  both exits det C = 1 != 0: lambda_t = 0 is never crossed; the extractor's DOMAIN is left.

**The prompt's/SR's conjectured inequality delta_comp <= p + q is REFUTED in this matrix
setting.** The law has EXACTLY the law-of-cosines FORM of SR rapidity composition
(cosh w_tot = cosh w1 cosh w2 + (n1.n2) sinh w1 sinh w2), but the relative-orientation
factor lives in a NON-COMPACT group: SR's rotation factor n1.n2 = cos(theta) <= 1 gives
sub-additivity; here the factor 1 + 2 sinh^2(w) (at the cosh-product normalization) is >= 1
and UNBOUNDED, giving super-additivity. The SR parallel is exact in FORM, loose in
MECHANISM: compact twist (SR) caps the composite; non-compact twist (strain groupoid)
amplifies it. Depth composes with a reverse-triangle (Lorentzian/timelike) character, fitting
delta_t being the TIMELIKE strain readout. (F-STEER discharge: the steered-for sub-additive
mechanism is the one thing the algebra refuses; see (c) for what survives.)

### (c) THE THEOREM (corrected statement, honest scope)
For ANY finite chain A_n o ... o A_1 of comparison arrows (each typed INVERTIBLE per the
banked definition, each with finite entries):
1. the composite is a finite product of finite invertible matrices, hence itself a finite
   invertible matrix; det C != 0; NO eigenvalue is 0 and none is infinite;
2. therefore IF the composite lies on the regular stratum, lambda_t > 0 STRICTLY and
   delta_comp is FINITE: the wall (delta = infinity) is NEVER ATTAINED by finite composition;
3. if the composite leaves the regular stratum (elliptic/negative exits above), delta_t is
   UNDEFINED there, not infinite — still not the wall;
4. BOTH ENDS: by the banked reversal delta_t(A^{-1}) = -delta_t(A) [re-verified,
   Q1_reversal_lambda_t = r^2], lambda_t -> infinity (delta -> -infinity, the
   c_eff -> infinity small extreme via c_eff = c_E * lambda_t) is the SAME statement under
   A -> A^{-1}: equally unattainable.
BUT the prereg's quantitative floor "lambda_t >= e^{-2 sum D_i}" holds ONLY on the exact-
additivity subgroup (full-diagonal/collinear + spatial-rotation twists). On boost-twisted
chains it FAILS: there is NO uniform lower bound on lambda_t in terms of leg depths alone —
two depth-D legs reach past e^{-4D} arbitrarily far as twist grows. Unreachability survives;
the SR-style sum-bound mechanism does not.

### (d) THE ESCAPE HUNT (F-STEER discharge — genuinely hunted for O1-REACHABLE)
Attempted routes to lambda_t = 0 from finite legs:
1. SINGULAR ARROW, one step: A = diag(0,2,1) gives strain diag(0,1,4) — lambda_t = 0
   ATTAINED at finite entries [ESC_singular_strain]. But det A = 0: not invertible, hence
   NOT in the banked arrow set ("typed invertible comparison arrow", audit sec.2; inverses
   are constitutive of the groupoid and of the reversal law). **The theorem's scope must and
   does exclude singular arrows EXPLICITLY.** If a future completion admits degenerate/limit
   arrows (e.g. an actual horizon comparison), the theorem does NOT cover them — honest scope
   edge, stated.
2. FINITE CHAIN of invertible legs: det multiplicativity forbids det -> 0; finite products
   of finite matrices forbid entry blow-up. No finite chain attains lambda_t = 0. (This leg
   is definitional — see (e).)
3. UNIPOTENT/MIXING LEG (mu != 0): CANNOT even approach the wall in the mu-direction — see
   Q3 below: exact positive floor lambda_t >= s^2/(1 + r^2 s^2) at fixed (r,s).
4. OPPOSITE-SIGN + LARGE TWIST: exits the regular stratum (elliptic/negative) with
   det C = 1; lambda_t = 0 never crossed; depth becomes UNDEFINED, not infinite.
5. NULL/DEGENERATE-METRIC LEG: the banked formalism fixes nondegenerate endpoint metrics
   (g = eta in orthonormal coframes); a degenerate-g comparison is outside the banked
   objects — not available as an escape within scope.
NO reachable construction found within the banked arrow set. The closest thing to an escape
is quantitative, not topological: super-additivity + unbounded twist amplification mean the
wall is approached ARBITRARILY FAST (already at chain length 2), but never attained.

### (e) ANTI-TAUTOLOGY LEDGER (where the content lives)
- DEFINITIONAL: step (c)1-2 ("finite products of invertibles are invertible; det != 0 =>
  lambda_t != 0"); the reversal corollary GIVEN the banked reversal law. Alone, these would
  make O1 a definitional corollary (F-TRIVIAL would bite).
- SUBSTANTIVE (derived here, exact):
  S1. The additivity SCOPE: exact on the full-diagonal subgroup INCLUDING different spatial
      axes and arbitrary spatial-rotation twists (larger than the banked collinear scope);
      broken by boost twist and by mixing (banked).
  S2. The composition LAW: cosh(2 delta) = cosh(2(p+q)) + 2 sinh^2(w) sinh(2p) sinh(2q) —
      law-of-cosines form, NON-COMPACT twist factor, inequality REVERSED vs SR
      (super-additive), equality iff collinear; no uniform depth floor from leg depths.
  S3. The boundary characterization (Q1): two-face structure; the reciprocal tie closes the
      singular face; wall = ideal boundary point; rank-1 projective limit with the timelike
      eigenline as kernel.
  S4. The scope fact: singular arrows attain the wall trivially and are excluded exactly by
      the banked invertible typing — the unreachability theorem is ABOUT the groupoid.
  S5. The stratum-exit taxonomy: elliptic/negative exits exist (det != 0) — the extractor
      can lose its domain, which is a different failure than reaching the wall.

## Q3 — the mu corner (noted only, NOT pursued)
On the mixing stratum (s != r scope per the final blind verification), the clock-screen block
of C_A has trace T = 1/r^2 + s^2 - mu^2 and det d = s^2/r^2 (mu-independent). The tie
generalizes: lambda_t * lambda_partner = s^2/r^2, so at bounded (r,s) a genuine lambda_t -> 0
still forces partner blow-up (degeneration character unchanged in that respect). But the
mu-DIRECTION itself cannot reach the wall at all: mu only LOWERS the trace, and on the
real-spectrum window lambda_t = d/lambda_max >= d/T >= s^2/(1 + r^2 s^2) > 0 — an exact
positive floor [ESC_mu_block_sum_prod, ESC_mu_floor_identity, ESC_mu_floor_holds_on_samples].
Increasing |mu| degenerates through the ELLIPTIC transition (complex spectrum, depth
undefined) BEFORE lambda_t can approach 0: on the mu-stratum the degeneration changes
character from asymptotic-ideal (the wall) to elliptic-domain-loss. Held with the
discretization seed; nothing further pursued.

## LANDED OUTCOME CLASS (per the frozen contract)
**O1-CONDITIONAL** (the prereg's own marker: "the general inequality fails or reverses —
report the exact boundary of validity"), with strong O1-MIXED structure findings (Q1):
- UNREACHABILITY HOLDS on the honest scope: within the banked groupoid of typed INVERTIBLE
  comparison arrows, no finite chain of finite-depth legs attains lambda_t = 0 (nor, by
  reversal, lambda_t = infinity — both extremes, one statement). The wall is a boundary
  stratum of the closure (ideal on the lock; singular off it), never an arrow.
- BUT the SR sum-bound mechanism steered for is REFUTED: the general-chain inequality
  REVERSES (super-additive under boost twist; exact law S2); the quantitative floor
  lambda_t >= e^{-2 sum D_i} holds ONLY on the exact-additivity (full-diagonal + rotation)
  subgroup; there is NO uniform floor on twisted chains.
- The gamma-asymptote READING survives — the wall is approached, never attained, and the
  approach is even FASTER than rapidity-sum — but its mechanism is groupoid invertibility +
  the reciprocal tie closing the singular face, NOT sub-additive rapidity budgeting.
SINGLE LOAD-BEARING STEP: the exact composite trace law (S2) with its NON-COMPACT twist
factor — it simultaneously kills the steered-for inequality, relocates the theorem's content
onto invertibility + the tie (S3/S4), and survives every escape attempt (d).
F-SCOPE/F-PIN respected: no x_max value, no law, no separation measure, scale-free
throughout. LEAD / UNBANKED: two same-session adversarial reviews owed before any banking.

## CONSOLIDATED (2026-08-07, both reviews in): O1-CONDITIONAL SUSTAINED — AMENDED (nothing broken)

Files: ADVERSARIAL_REVIEW_1_algebra.md (SUSTAINED-AMENDED; full independent recompute, no probe code
opened) + ADVERSARIAL_REVIEW_2_scope.md (AMENDED; independent recompute incl. closing the
witness-only labeling gap). The two reviews INDEPENDENTLY found the same load-bearing addition (the
infinite-chain witness). Amendments applied here; the theorem statement below supersedes Q2(c).

**THE THEOREM (amended, honest scope):** Within the banked groupoid of typed INVERTIBLE Lorentz
comparison arrows, NO FINITE CHAIN of comparisons attains the lambda_t -> 0 wall; on the mu=0
locked stratum this is substantive (the derived reciprocal tie det C = s^4 closes the singular
face — the only approach is escape to infinity, the ideal-point v->c structure); off-lock and
without the invertibility typing it is a TYPING fact (a singular arrow attains the wall in one
step). By banked reversal the same statement covers lambda_t -> infinity (the c_eff -> infinity
small extreme). **LOAD-BEARING QUANTIFIER: finite chain LENGTH — not total depth.** There is NO
budget protection: an INFINITE chain with SUMMABLE leg depths (total < 1) and growing non-compact
twists ACCUMULATES to the wall (R1: lambda_t ~ 4e-84 by n=10, every truncation regular and
timelike-labeled; R2: independent witness, total budget ~0.85). In SR, summable rapidities stay
bounded away from c — HERE THEY DO NOT. The SR parallel: FORM survives (asymptote-yes hard-bound-no,
ideal boundary, both ends, law-of-cosines composition), the BUDGET MECHANISM died.

**THE PARTITION THEOREM (R1, resolves the additivity-vs-superadditivity tension exactly):**
composition is depth-ADDITIVE iff the inter-leg twist STABILIZES the timelike eigenline (compact
spatial rotations); ANY non-compact twist component (relative boost OR null/parabolic rotation)
gives STRICT super-additivity — parabolic twists growing as n^4 sinh(2p) sinh(2q) (new tile; the
probe skipped parabolics). 1500 verified-Lorentz random twists: zero sub-additive pockets.
SCOPE EDGE (named): non-Lorentz "twists" DO produce sub-additivity — the Lorentz typing of legs is
load-bearing. **Anti-hunch datum (scoped, kinematic-composition only, mu=0):** the PURE ANGULAR
(spatial-rotation) sector composes exactly additively; the enhancement lives in the non-compact
channels — at this layer this cuts AGAINST reading super-additivity as the phi-angular interaction.

**THE WALL (Q1, amended):** a FAMILY of ideal boundary points (rank-1 with the timelike eigenline
as kernel when the screen strain is subdominant; rank-3 if the screen co-diverges — R2's check);
det A = det C = 1 all along; e1-e3 diverge, e4 = s^4 pinned; the causal labeling survives to the
wall (no collision/complexification anywhere on the twist family — R1 closed this gap generally).

**Q3 (strengthened, R1):** along the mu-direction lambda_min monotonically INCREASES toward s/r —
the mixing direction moves AWAY from the wall before degenerating (near exit elliptic; far exit
negative-real; same conclusion). Mixing is wall-protective at this layer.

**STATUS: verified LEAD (same-session reviews; the external bar travels).** Four-check:
preregistered; bounded scope stated (mu=0 stratum + typed groupoid + finite chains, each named as
load-bearing); blind-verified on the load-bearing steps by two independent recomputes; premises
audited (typing = CHOSE at source, honestly carried). Outcome class O1-CONDITIONAL per the prereg's
own bin (the inequality REVERSED) — conditional in MECHANISM, not in conclusion. Headline sentence
(R2, adopted): "The wall really can't be reached — but not because depths add up too slowly like
speeds in relativity: the wall simply isn't a member of the comparison family, and on the locked
stratum the reciprocity tie slams that door — while twisting between legs lets even shallow
comparisons race arbitrarily close, with no budget holding them back."

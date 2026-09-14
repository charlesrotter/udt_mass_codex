# Blind adversarial verifier report — P4 Route B Stage 1

Verifier: blind adversarial agent (zero-context framing; same-session-spawned — the
not-a-hosted-external-model caveat travels per the prereg §6 method note).
Date: 2026-07-28. Worktree: `p4-routeB`. Framing: ADJUDICATE between competing
readings, never confirm the author's read. No production file was edited. Preserved
artifacts: `INDEPENDENT_REDERIVE.py`, `INDEPENDENT_STDOUT.txt` (this package).

## My setup (stated per duty 2a)

- My own so(1,3) basis: the covariant generators `(M_ab)^mu_nu = delta^mu_a eta_{b nu}
  − delta^mu_b eta_{a nu}`, pairs (0,1),(0,2),(0,3),(1,2),(1,3),(2,3) — constructed from
  the defining formula, not copied from the production E-matrix sums. Verified: all six
  satisfy `lam^T eta + eta lam = 0`, rank 6, and span the SAME 6-dim algebra as the
  production basis (`A2_same_algebra_as_production`) — so both scripts compute the same
  action.
- Action adjudication: with the coframe a COLUMN of one-forms, extension `e → exp(φX)e`
  and gauge `e → Le` both left-acting, the induced action on X is FORCED to be the
  pointwise adjoint `X → LXL⁻¹` (`L exp(φX) L⁻¹ = exp(φ LXL⁻¹)` is an exact similarity
  identity; no inhomogeneous/connection term can enter because the extension map contains
  no derivative of L). The production representation setup is NOT ambiguous and NOT
  wrong-sided. A side/sign flip (`δX = [X,λ]`) would leave every stabilizer dimension
  unchanged (identical nullspaces), so no finding hides there.
- My own stabilizer machinery: coefficient extraction per monomial in the extension
  parameters, own linear-system nullspace over the gauge coefficients, with a
  nonlinearity guard.
- Rerun record (duty 1): `python3 derive_routeB_stage1.py` → exit 0, runtime < 1 s,
  stdout BYTE-IDENTICAL to `DERIVATION_STDOUT.txt`, deterministic across two runs;
  `DERIVATION_RESULT.json` on disk equals the JSON block embedded in the stdout file;
  47/47 checks, `all_pass: true`, sympy 1.13.1. Prereg is committed; deliverables were
  uncommitted at verification time (correct verifier-before-record order).
- Independent rerun record (duty 2): `INDEPENDENT_REDERIVE.py` → 44 checks, ALL PASS,
  exit 0, deterministic across two runs. (One intermediate run failed on MY OWN check's
  expected solution shape — sympy returned `{A: D, B: −K21}` instead of `{D: A, K21: −B}`
  for the same solution set; fixed by substitute-back verification. Production is not
  implicated; recorded for honesty.)

## Duty 2 — independent rederivation: adjudications

**2(a) Stabilizer chain — CONFIRMED.** With my own basis and solver: upper-right-zero
preserved exactly by span(M01, M23) = so(1,1)⊕so(2), dim 2 (and [M01,M23]=0, a true
direct sum); adding fixed H cuts to span(M23), dim 1; adding the triangular chart
condition cuts to {0}. The obstruction entry is `d − a` exactly (the production's
corrected sign is RIGHT for R23 = E23−E32; its recorded first-run F-C failure was real
and honestly banked). Per-stratum: E04 dim 1, E05 full-K dim 1, E05 triangular dim 0,
E06 dim 1; the so(2)-fixed set of the 7-parameter triangular class is exactly the
isotropic line; centralizer dims of `diag(−1,+1,λ,λ)` are 1/3/3/1 (generic/+1/−1/0).
The det-one (trace) condition is invariant under the FULL algebra — in fact under any
λ whatsoever (trace of a commutator). All claimed dimensions are correct.

**2(b) E08/C-block cocycle — CONFIRMED.** I derived `M(φ) = ∫₀^φ e^{tH}dt =
diag(1−e^{−φ}, e^{φ}−1)` by my own integration, verified the closed form solves the
defining ODE with F(0)=I, and spot-checked against sympy's exact 4×4 matrix
exponential at φ=1, C=[[2,3],[5,7]]. My own two-segment multiply gives exactly
`σ_tot = σ₁ + e^{−φ₁}σ₂` (and the full-C law `C₂M(φ₂)e^{φ₁H} + C₁M(φ₁)`,
clock-channel weight e^{−φ₁}, ruler channel e^{+φ₁}), associativity with path-ordered
weights, and the history-dependence witness `sbar(T/2,T/2) − sbar(T,0) =
(s₂−s₁)e^{−T/2}(1−e^{−T/2})/(1−e^{−T})`, verified nonzero at an exact witness point.
The composition-order convention (segment 1 then 2 = g₂·g₁ under left action) is
consistent with the stated representation.

**2(c) T4 plane facts — CONFIRMED, including the sign audit against the source
package.** Using the metric readout convention of
`udt_founded_phi_complete_coframe_extension_audit_2026-07-25/derive_extension_class.py`
(g = (diag(c,1,1,1)·Λ)^T η (diag(c,1,1,1)·Λ); calibration on the clock slot only): a
generator entry m gives metric factor e^{2mφ}; the E07 record
diag(e^{−2kφ}, e^{+2kφ}) is reproduced from (a,d)=(−k,+k) with signs intact;
`√|det g| = c·e^{(a+d)φ}` so the native 4D chart volume exponent is a+d with the base
pair contributing (−1)+(+1)=0 exactly; φ-blindness holds iff a+d=0; the parametrization
k ↦ (−k,+k) is onto the anti-diagonal, so E07 line = det-one line = 4D volume-blind
line is a genuine three-name coincidence; (a,d) = (λ−k, λ+k) is an exact orthogonal
decomposition — the MAP's "E07 k = joint-audit λ" is correctly resolved as a
decomposition, not an identity. I also verified the λ-normalizations MATCH across the
banked records (X_λ = diag(−1,+1,λ,λ) verbatim in the 07-27 and 07-28 records; the
rank-closure metric carries e^{2λφ} on the screen, consistent with m→e^{2mφ}), so the
seat identification does not conflate normalizations.

**2(d) Spot checks — 7 additional production claims CONFIRMED** with independent
constructions: bracket block formula (zero base block; triangular bracket-stability;
non-abelian witness), L8 Lie-algebra closure, the total-φ=0 non-closure witness
(base=I, screen≠I, base=I forces identity in the class), the diagonal φ-weighted-mean
modulus and abelianness, det M(φ)=0 iff φ=0, the E08 finite form as an exponential,
and so(1,3) perfectness (bracket span rank 6).

## Duty 3 — F-D quantifier hunt

Hunted every unique/forced/invariant/unconstrained statement in EXACT_DERIVATION.md and
the TSV. Results (details under findings):

- **CAUGHT (the one real slip):** "the E07/k direction is currently UNCONSTRAINED by
  every supplied-reduction gate" (§4 end), "currently UNCONSTRAINED by every banked
  gate" (§7 L2), and TSV row E07/C3 scope "no supplied reduction currently constrains
  k" — scope WIDER than the bank shows. See finding CR-1.
- "the unique stratum condition covariant under all of so(1,3)": true over the
  package's OWN stratum/chart condition list (each alternative's stabilizer computed
  smaller), but the wide reading is false — ANY spectral function of X is fully
  covariant; I verified δ(det X) = 0, so det X = −ad is another fully covariant
  function on the class. Needs the explicit quantifier. See N-3.
- E06 "unique closed one-parameter subgroup": properly F-D-guarded in-row (uniqueness
  quantified over the closure property); no slip.
- Reverse hunt (over-hedged): "no stratum with ≥2 members is closed at total φ=0" is
  claimed fully generally and IS fully general — the quoted witness lives in E05, but
  the base=I argument is member-independent and per-stratum witnesses exist (I
  constructed the E03-internal one exactly: det-one members (a,d)=(1,−1),(−1,1) give
  diag(1,1,e^{2φ},e^{−2φ})). Correctly not over-hedged; but the TSV E03/C2 cell text is
  garbled (N-5). The T5 "forces" cells are correctly scope-stamped conditional.

## Duty 4 — bank-consistency audit

**(i) No unconditional elimination — VERIFIED.** The ledger contains zero FORCED-OUT
statuses (census: 14 CONDITIONAL, 15 SURVIVES_WITH_MODULI, 1 UNCONSTRAINED, 2
NOT_WELL_POSED_POINTWISE); the prose claims "L1 elimination by C1/C2 alone: NONE".
F-A cannot fire and did not.

**(ii) "no banked gate reaches k≠0" — ADJUDICATION: the NARROW claim is TRUE, the
BROAD phrasing is FALSE.** I checked all four cited banked records. No banked fact
pins k to any nonzero value — verified. BUT the 07-27 extension-selector record's
full-class solves (EXACT_DERIVATION §4 there) give: supplied SO(3) →
K = diag(+1,+1); supplied SO+(1,2) → K = diag(−1,−1); supplied twisted swap F →
(c00,c01,c10,c11,k00,k10,k11) = (−a,+a,−b,+b,0,0,0), i.e. K = 0 entirely. Each of
these supplied gates therefore DOES constrain the k direction — it conditionally
forces k = 0. The package's own T5 table knows this ("only its origin survives the
swap gate"), so the §4/§7/TSV-row-28 "unconstrained by every gate" wording is an
internal inconsistency and a scope slip, not a wrong theorem. See CR-1.

**(iii) V_q reconciliation — ADJUDICATION: correct honest scoping.** The banked V_q
is derived on the registered stationary twisted family whose screen isotropy is baked
into the registration (`g = −e^{−2φ}τ² + R²e^{2φ}σ₃² + R²e^{2λφ}(σ₁²+σ₂²)`), giving
`det q = R⁶e^{2(1+2λ)φ}` — exactly the package's "2 screen legs at λ + 1 fibre leg at
ruler weight +1". No banked orbit-volume formula exists for a≠d; the two functionals
(1+2λ on the 3D orbit vs a+d on the 4D chart) and their blind loci (−1/2 vs 0) are
kept separate at every occurrence I could find (pin table, TSV row 32, script note,
§7). No missed translation is banked: a naive algebraic extension (orbit exponent
1+a+d) is trivially writable, but its prerequisites (the unique-K certification, the
registered family itself) exist only for the isotropic registration — importing it
would have been an unbanked adoption, and the package was right to refuse. No
conflation found elsewhere. Wording nit: "NOT-TRANSLATABLE" is glossed in-row as
absence-of-banked-formula; "NOT-TRANSLATED (no banked formula)" would be more precise
(N-6).

## Duty 5 — load-bearing premise, attacked

**The premise I judge most load-bearing for the L1/L2 re-tag:** the induced-action
identification — that the gauge group acts on the extension generator by the pointwise
adjoint `X → LXL⁻¹` in the defining representation, with no inhomogeneous term and no
side ambiguity. ALL of T1 (the split-relativity that drives L1's "well-posed only
given a supplied split", the chart-section verdicts, the so(2)-invariant content
(λ,|k|) that IS the L2 re-tag) rides on this single identification.

Attack outcome: **premise SURVIVES.** (1) The adjoint law is forced by the algebra of
two left actions on the same coframe column composed with a pointwise algebraic map —
an inhomogeneous term would require the extension map to differentiate L, which it
does not. (2) The wrong-side variant `δX = [X,λ]` has identical nullspaces, so every
claimed stabilizer dimension is side-invariant — no finding can hide in the
convention. (3) Cross-record normalization: X_λ = diag(−1,+1,λ,λ) appears verbatim in
both the 07-27 and 07-28 banked records; the E07 generator diag(−1,+1,−k,+k)
reproduces the banked screen metric diag(e^{−2kφ}, e^{+2kφ}) under the source
package's own readout convention — so the (λ,k)-plane synthesis mixes no incompatible
normalizations. The one residual exposure is inherited and declared: everything is
scoped to the registered pointwise one-parameter class (scope stamps present).

## Duty 6 — prereg compliance

- Targets: T1–T4 mechanized in the script, T5 delivered as the cited assembly table,
  T6 delivered as EXACT_DERIVATION §7 — all six delivered as preregistered.
  `AUDIT_REPORT.md` is still owed (correctly sequenced after this verifier pass).
- Ceiling (§5): NOT exceeded anywhere. No supplied reduction adopted, no physics
  selected, no response one-form/action claims, no unconditional elimination; the
  strongest statements are covariance/closure typings within the stamped scopes; O2/O3
  outcome honestly declared.
- Ledger vocabulary: VIOLATION — `NOT_WELL_POSED_POINTWISE` (rows: diagonal-subfamily
  C1, E07-line C1) is not in the frozen §2 vocabulary. See CR-2.
- Falsifier review (§6) is accurate as far as it goes; F-D "none found by the author"
  is now superseded by CR-1 (the verifier's hunt, as the prereg itself anticipated).
- Interrogation declaration honored: the deliverable is a survival/typing ledger, not
  a verdict for any stratum; observing, not targeting.

## Findings (graded)

- **CR-1 (CORRECTION-REQUIRED, quantifier scope / F-D):** Replace the three overbroad
  "k is UNCONSTRAINED by every supplied-reduction/banked gate" statements
  (EXACT_DERIVATION §4 last paragraph; §7 L2 bullet; TSV row E07-line/C3 scope stamp)
  with the bank-accurate statement: "no banked gate pins any k ≠ 0; absent supplied
  structure k is unconstrained; under each cited supplied reduction (SO(3), SO+(1,2),
  twisted swap) k is conditionally forced to 0 (07-27 full-class solves; cf. this
  package's own T5 E07 row)." The E07/C3 ledger status should read
  CONDITIONAL/UNCONSTRAINED-UNCONDITIONALLY rather than bare UNCONSTRAINED. The slip
  overstates freedom, not forcing — it creates no false elimination and no false
  selection — and the correct content already appears in the package's T5 table, so
  this is wording harmonization, not a broken theorem. L1/L2 re-tag verdicts are
  unaffected.
- **CR-2 (CORRECTION-REQUIRED, prereg vocabulary):** `NOT_WELL_POSED_POINTWISE`
  (2 ledger rows) is outside the preregistered status vocabulary. Either re-map those
  rows to CONDITIONAL with the not-well-posed identity kept in the forcing column, or
  record the vocabulary extension explicitly in the correction layer. The content
  itself is honest (strictly weaker than any elimination).
- **N-3 (NOTE):** "the unique stratum condition covariant under all of so(1,3)"
  needs its quantifier made explicit ("unique among this package's stratum/chart
  conditions"): any spectral function of X is fully covariant under the adjoint
  action (verified: δ(det X) = 0, so det X = −ad is another fully covariant function
  on the class). True as scoped; false in the widest reading.
- **N-4 (NOTE, scope):** the so(2)-fixed-set statement ("exactly the isotropic line")
  is triangular-chart-scoped: on the chart-free full-K class — the very home the
  package recommends for covariant statements — the fixed set is the 2-modulus family
  {a=d, k21=−b, C=0} (isotropic + screen-rotation direction; verified). The sentence
  itself is correctly scoped ("of the whole 7-parameter class"), but the T5 SO(2)
  column and the banked-row cross-check should carry the chart stamp.
- **N-5 (NOTE, text defect):** TSV E03/C2 cell contains garbled/truncated text
  `"(1,0,-1,0),(0,0,..."`. The intended claim is right — an E03-internal total-φ=0
  witness exists (constructed exactly in `INDEPENDENT_REDERIVE.py`,
  `E3_E03_internal_witness`). Repair the cell.
- **N-6 (NOTE, wording):** pin-table "NOT-TRANSLATABLE off a=d" — the row's own
  parenthetical correctly glosses this as "no banked formula"; prefer
  "NOT-TRANSLATED" to foreclose the impossibility reading.
- **N-7 (NOTE):** `T4_conditional_pins_on_isotropic_line`'s algebraic content is
  trivial (k=0 at a=d by definition); the load-bearing content is the bank audit,
  adjudicated separately above (narrow claim verified, broad wording = CR-1).
- **Positive note:** the in-run F-C sign failure (a−d vs d−a) was real, the corrected
  sign is right in my independent basis, and the honesty note is accurate.

## Verdict

VERDICT: PASS_WITH_CORRECTIONS (CR-1: harmonize the three overbroad "k unconstrained
by every gate" statements + E07/C3 status to the bank-accurate conditional form;
CR-2: resolve the NOT_WELL_POSED_POINTWISE out-of-vocabulary ledger status).

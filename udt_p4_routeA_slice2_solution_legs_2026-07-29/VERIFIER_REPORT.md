# BLIND VERIFIER REPORT — P4 Route A Slice 2 (solution-touching legs)

Verifier: blind adversarial verifier, **same-session-spawned** (zero package context at
start; not a hosted external model — this caveat travels with the verdict). Date:
2026-07-29. Contract adjudicated against: `PREREGISTRATION.md` at ef35a67 (BOOTSTRAP-LENS
frame §2 treated as binding). Independent artifacts: `VERIFIER_INDEPENDENT_CHECK.py` +
`VERIFIER_INDEPENDENT_STDOUT.txt` (21/21 own-construction checks, exit 0).

## VERDICT: **PASS-WITH-REQUIRED-AMENDMENTS** (two; both F-D3-class stamps — no claim
refuted, no falsifier fired, all load-bearing mathematics independently confirmed)

---

## 1. Rerun / contract-first / determinism

- Contract-first CONFIRMED in git: PREREGISTRATION.md committed at ef35a67 (2026-07-29
  11:38) — the only file in that commit; all derivation artifacts created 11:56–11:58.
- `python3 derive_routeA_slice2.py`: exit 0, 36/36, run TWICE — both reruns byte-identical
  to the shipped `DERIVATION_STDOUT.txt`. Deterministic confirmed.
- Script audit: exact SymPy only; no floats, no randomness, no network, no numeric solvers
  (sp.solve used on one linear equation; all instantiations rational/symbolic), single
  process. JSON matches the CHECKS list (36 = 28 substantive + 8 guards, 0 failed, OD1).
- Guard-split audit: all 8 guard rows are `True`-condition recording/citation/definitional
  rows, correctly labeled `[guard]` in stdout and JSON. Two honesty notes (N1, N2 below):
  one substantive check is a duplicate boolean and one is zero-by-construction; the split
  is not inflated in the load-bearing direction (the well/tie/quadrature/closure checks
  are all genuine computations).

## 2. Independent re-derivation (own constructions; 21/21 PASS)

**(a) The emergent nodeless well — attacked hardest.** Re-derived the GEN-QUAD tuple by an
independent route (function-based Euler–Lagrange on x, not the package's jet machinery):
exact match. The closed-form family e^{a_F p0} = w = (a_F²E0/2)x² + w1x + w0, f′ = c_f/w,
h′ = c_h/w verified zero-residual with a_F a FREE REAL symbol (the package script's
`positive=True` declaration is NOT load-bearing — verified at a_F < 0) and c_f, c_h of any
sign. disc(w) = −a_F²c² and 2w0E0 = sum of three squares re-verified sign-free ⟹ E0 ≥ 0
forced on the real family, w rootless for c ≠ 0 (globally regular, nodeless), E0 = 0 iff
constants — all genuinely forced by the equations ON THIS REPRESENTATIVE; the
CHOSE(representative) tag and "not a cell census" stamp are prominent and travel
(the well is a property of GEN-QUAD's atlas, honestly scoped, not passed off as the
cell's). Exhaustiveness: I constructed the EXPLICIT global inverse of the
parameter→initial-data map ((w0,w1,c_f,c_h) = (e^{aP0}, ae^{aP0}P1, e^{aP0}F1, e^{aP0}H1))
— stronger than the package's rank-6 spot check and confirming it; with Picard
(Category-A, correctly stamped) the local field-sector space is exactly the 6-dim
initial-data manifold; the "locally exhaustive" claim is correctly scoped (field sector,
representative family, local-in-x, w > 0 extension governed — limits (i)/(iv)). Both
quadratures re-verified by differentiation. **One genuine defect found — sign(a_F) shape:
see REQUIRED AMENDMENT A1.**

**(b) The background tie 2E0·I_p = 0.** Re-derived: for both P1 instances a_F′ = 2, so
∂λ(W_F L̃₀) = 2p0·W_F L̃₀ exactly; on-shell W_F L̃₀ ≡ E0 (verified identically constant on
the closed form), giving the integrated BASE-branch row 2E0·I_p = 0. The a_M-cancellation
is genuine GIVEN the banked Stage-3 generated construction R_μ = W_M⁻¹∂_μ(W_F L̃) (verified
present in the Stage-3 bank; the in-script `row_integrand` check is zero by construction —
note N2). I_p's closed form re-verified against direct sympy integration at the witness.
NONEMPTINESS at every background: CONFIRMED and STRENGTHENED — my own legs at SYMBOLIC ℓ
and BOTH signs of a_F (w ≤ 5/8 on the cell vs w ≥ 2, E0 > 0 throughout the connecting
path) prove the I_p = 0 root with E0 > 0 exists at every a_F ≠ 0, ℓ background; the
package's own exhibited legs cover only (a_F, ℓ) = (1, 1) — see REQUIRED AMENDMENT A2.
Continuity/monotonicity legs correctly stamped Category-A. **P2-side ABSENCE: genuinely
derived**, not assumed — on P2 the branch definition is a_F ≡ 0 with a_F′ = 0, so the
generated λ-slot ∂λ(1·L̃₀) vanishes identically; and it is exactly the a_F′ = 0
degeneration of the P1 tie at the banked blindness loci (λ = 0, λ = −1/2) — re-verified.
Pairing-relativity reading ADJUDICATED CLEAN: stated as observation, FOR (tie emerges
unforced on anchored pairings) and AGAINST-universality (absent under P2) both recorded;
no promotion of the anchored branches (F-D1 clean), P2 result reported not suppressed
(F-D8 clean both directions).

**(c) The M instantiation stamp.** M = 2ℓE0 carries the CHOSE/CONDITIONAL (banked mass
rows OPEN) tag at EVERY use found: script TD2 detail, EXACT_DERIVATION §0 premise ledger +
§3 + limits (iii), both ledger R5 strings, SLICE2B_SURFACE §3. No silent upgrade: the lens
classes rest on solution existence, and the self-consistent locus derives from the λ-row
(E0 via the pairing structure), not from the R5 M-instantiation. ρ = M/V: V, M, ρ
re-integrated by me on the SAME closed-form member — F-D6 confirmed clean.

**(d) Pairing-branch independence.** Zero-set/pairing theorem re-verified (e^{a_F p0}
exactly invertible and positive; W1's zero set = affine atlas weight-independently, while
its Helmholtz-(ii) self-defect −2a_F p1 e^{a_F p0} moves its CELL membership — the
theorem's "membership moves, zero set doesn't" instance confirmed). α, 𝔠, c_E absence
re-checked on my own tuple; the L8/α-ACTIVE branch: the generated member's α-slot is
W_M⁻¹∂α(W_F L̃₀) = 0, so the extra row is vacuous — the atlas is genuinely untouched
(recorded as zero/retained, not omitted). a_M-independence: the W_M cancellation (b).
BR-B role-only: cited to the bank (banked PROVEN pointwise branch-independent) —
consistent. Scope correctly stamped "named representatives, NOT a cell-general claim".
No hidden branch dependence found.

**(e) W3 / ω.** W3 = (p1,0,0): f/bh rows identically zero ⟹ {p0 const} × f, bh arbitrary
— per-member DEGENERATE, recorded without gloss and correctly reconciled with the
Stage-3 DETERMINED-TYPE (generic-member) typing. ω: the single nonvacuous row
k10·∫e^{a_M p0}dx = 0 with positive integrand forces k10 = 0 for EVERY a_M — the zero set
{k10 = 0} × fields free, a_M-independent, honestly recorded.

**(f) KMOD0.** Stratum identity −2k10·r_tf + m00c10 + m01c11 − m10c00 − m11c01
recomputed from my own [L23, X] build — matches the banked Stage-2 identity; all reps
satisfy it identically (field-sector members r_tf = M = 0; ω's r_sh does not enter).
Gauge tangent (δλ, δk_mod, δk10, δC) = (0, k10, 0, J·C) confirmed; GEN-QUAD components
(k10, C)-independent; ω's zero set invariant and on-stratum. Quotient carried exactly.

**(g) Route C cross-check.** Own parse of the banked `EH_ODE_SYSTEM_FULL.txt` (7 rows,
verified autonomous — no bare x — so the package's t-substitution was valid); my own
substitution with EXPLICIT x-dependence (p0 const, f const, bh = (Ax+B)², Λ = 0) kills
all seven rows identically in (x, A, B, α, λ, c_E). GR-as-reference stamps present and
honest ("OBSERVATION only; the restricted-EH G3 tile stays un-run"; CONDITIONAL stamps
travel). No adoption.

**(h) NV NOT-DERIVABLE-AT-SLICE-2.** Genuine derivational absence: a nonvariational
member has no generated Lagrangian, hence no first-integral energy; adopting a mass
functional would be an import (G09/F-D7-adjacent, correctly refused). Reported
explicitly per F-D8 (not silently skipped: it appears in the TD3 UNDETERMINED class, the
TD5 record, all NV ledger rows, and SLICE2B §1.2 with both allowed continuations —
derive-from-banked-structure or bank structurally OPEN). Typed to Slice-2b. Honest.

## 3. Falsifier hunts

- **F-D3 (hunted first, code + both prose docs + ledger + JSON):** every works/all/none/
  fails claim I could find carries cell + fork-branch + stratum + background stamps, and
  the representative-sub-family stamp is ubiquitous — EXCEPT the two sites in the
  amendments below (a_F-sign stamp missing on the "well/single minimum" language; the
  "every a_F ≠ 0 background" nonemptiness claim exceeding its exhibited witnesses).
- **F-D1:** clean. "Emergent/observed, not imposed" language stays observational; no
  member ranked or preferred; ceiling respected; SLICE2B §3 explicitly de-decides.
- **F-D2:** trivially clean — no elimination anywhere (lens FAILS row: NONE); confirmed.
- **F-D4:** Stage-3/Stage-2 facts recomputed independently (K₄/X footing, k_mod = 0
  identity, W1 defect, W2′ field-only H4(λ) failure, W3 all-branch NV, blindness loci,
  20-cell READY bin, DETERMINED-TYPE 3+7) — no contradiction.
- **F-D5:** none; 36/36 twice, byte-identical.
- **F-D6:** clean (verified by my own same-member integration).
- **F-D7:** clean — no carrier, no source rows; gate 2 in carrier-free typed form only.
- **F-D8 both directions:** clean — no bootstrap in any definition/filter/crown (R14 a
  diagnostic column only); every LE representative's locus computed and reported (incl.
  the degenerate P2 all-backgrounds report); NV absence reported with its reason.

## 4. Contract compliance

TD1–TD6 all addressed at full declared scope; scope ladder UNUSED (consistent with
content — all 20 cells, NV duties present, forks carried as labeled branches per the
Stage-3 must-decide list); the representative-sub-family clause used exactly as
pre-authorized, WITH stamps (script docstring, MD header block, ledger preamble, per-claim
scopes) — not a silent narrowing; ceiling respected (no law crowned; bootstrap explicitly
left to Charles, evidence recorded both ways). `AUDIT_REPORT.md` is still owed before
commit (method §6 step 5 — post-verification; noted, not a violation at this stage).

## 5. REQUIRED AMENDMENTS (both F-D3-class stamp repairs; no computation changes)

**A1 — sign(a_F) stamp on the "well" language.** p0″(vertex) = 8A²/(a_F³c²) has the SIGN
of a_F (verified: `V_shape_sign_of_aF`). On the anchored branches the explored background
range includes a_F < 0 (P1-4D: λ < 0; P1-triad: λ < −1/2), where the depth profile is a
single-MAXIMUM bump, not a well. Nodelessness, global regularity, disc ≤ 0, and E0 ≥ 0
are sign-free (verified). Repair: stamp every "well / single minimum" site —
EXACT_DERIVATION §2.1 ("a symmetric well in the anchored depth with a single minimum" →
also "symmetric" means about its vertex, not the cell center), §2.1 background-transition
bullet, §2.2/2.3 "well atlas" mentions, the TD3 lens table, the ledger's `well family`
label, SLICE2B §2 "nodeless-well" — as "well (single minimum of p0) for a_F > 0 /
inverted (single maximum) for a_F < 0; nodeless and regular for both signs", or rename
the family shape-neutrally (e.g. "nodeless quadratic-w family").

**A2 — the locus-nonemptiness witnesses do not cover the claimed scope.** The claim
"nonempty nonconstant at every a_F ≠ 0 background" (script detail, EXACT_DERIVATION §3,
ledger self_consistent_locus column) is exhibited only at (a_F, ℓ) = (1, 1); those legs do
not transfer (leg A's bound fails at ℓ > √3 with the same parameters; the stated
implication "w ≤ 5/8 < 1 ⟹ I_p < 0" flips for a_F < 0). The claim itself is TRUE — my
`V_locus_legs_sign±` checks prove it with symbolic-ℓ legs at both signs of a_F (E0 > 0
along the whole connecting path) — so this is a proof-coverage gap, not an error. Repair:
add the general-(a_F, ℓ), both-signs legs to the derivation script (or cite the verifier
checks) and reword the §3 sign-leg sentence to carry its (a_F, ℓ) witness stamp.

## 6. Notes (not required)

- N1: `TD1_LE_E0zero_constants_only` re-tests the identical boolean (`sum_sq == 0`)
  already inside `TD1_LE_disc_E0_sign_structure` — a corollary-recording row counted
  substantive (split 28/8 otherwise honest).
- N2: `row_integrand` in TD2 is zero by construction (R_λ is DEFINED as W_M⁻¹∂λ(W_F L̃₀));
  the real footing is the banked Stage-3 generated construction — the citation is sound,
  the in-script check adds no computation.
- N3: the "self-consistent locus" column instantiates prereg §2c AS the member's own
  integrated λ-row zero locus — the only derivable tie given banked G12 (no derived
  bootstrap→local map); ρ = M/V is separately computed and reported. Defensible and
  stated in §4's FOR bullet; a one-line explicit note in §3 would remove any reading
  ambiguity.
- N4: dead code `legA_ok` in `derive_routeA_slice2.py` (computed, unused) — cosmetic.

*Blind verifier, same-session-spawned; not a hosted external model. 2026-07-29.*

---

# AMENDMENT CLOSURE (same verifier, second pass — attack framing retained)

Date: 2026-07-29. Adjudicating the A1/A2 implementation + CORRECTION_LAYER.md +
AUDIT_REPORT.md. Blind verifier, same-session-spawned; not a hosted external model.

## VERDICT: **CLOSED**

## Findings per duty

1. **Rerun:** exit 0, 41/41 = 33 substantive + 8 guards; run twice more by the verifier —
   byte-identical to each other and to the shipped `DERIVATION_STDOUT.txt`; the three
   sha256 values recorded in CORRECTION_LAYER §3 (JSON 1871e1e2…, ledger afad4124…,
   stdout 22905d5e…) all reproduce exactly. The 36 pre-amendment checks: names and
   PASS/FAIL identical to the pre-amendment run (line-diffed); their BOOLEAN pass
   conditions verified unchanged in-code (all key condition expressions grep-confirmed
   byte-identical: Helmholtz families, disc/sum-of-squares, rank-6, k_mod0 identity,
   λ-row, EH 7-row, ledger-20); exactly 4 substantive + 1 guard detail strings restated
   with stamps, as declared. The 5 new checks are genuine zero-residual computations,
   correctly counted SUBSTANTIVE, and adopt my derivations faithfully:
   `A1_well_zero_residual_signfree` (free REAL nonzero a_F, c_f/c_h any sign),
   `A1_vertex_curvature_sign_of_aF` (p0″(vertex) = 8A²/(a_F³c²), instantiated both
   signs — matches my formula), `A1_bump_instance_regular_nodeless` (a_F = −1,
   w = x²/2 + 1, disc = −2 — independently re-verified sound), and
   `A2_locus_legs_general_sign_pos/_neg` (structurally identical to my
   `V_locus_legs_sign±`: symbolic (|a_F|, ℓ), legs w ≤ 5/8 vs w ≥ 2, E0 > 0 proven
   symbolically, Category-A steps named).
2. **A1 stamp installation — CONFIRMED at every site I listed:** EXACT_DERIVATION §1
   T0 visible instance, §2.1 (sign-FREE bullet split from a new "Shape is
   sign(a_F)-scoped" bullet; "symmetric" = about the VERTEX), §2.1 background-transition
   bullet (quadratic-w vs affine + the WELL↔BUMP flip as a second sign-scoped facet),
   §2.3 W2-fs, §4 lens table, limits (viii); the ledger's 10 quadratic-w rows renamed
   shape-neutrally ("nodeless quadratic-w family") with the full in-row A1 stamp;
   SLICE2B §2. Regularity/nodelessness/E0 ≥ 0 correctly kept SIGN-FREE everywhere
   checked. **No F-D1 creep** in the new wording: "OBSERVED EMERGENT STRUCTURE —
   observation only, nothing adopted" framing holds; nothing promoted; the a_F < 0
   range explicitly located inside the explored background (λ < 0 / λ < −1/2).
3. **A2 — CONFIRMED:** the general legs match my V_locus_legs_sign± exactly (same
   targets, same parameter realizations, same E0 > 0 path argument, both signs); the
   (a_F, ℓ) = (1, 1) legs now carry an explicit witness stamp in the script detail, the
   MD §3, and the ledger's self_consistent_locus column; the old sign-leg implication
   is restated with its a_F-sign-dependence named; log-monotonicity/integral-sign/
   continuity remain named Category-A.
4. **CORRECTION_LAYER did-NOT-change list — VERIFIED by comparison:** OD1 unchanged
   (JSON); all atlas closed forms unchanged (pass conditions byte-identical; the
   tie/pairing-relativity checks TD2_lambda_row/TD2_P2 absent from the stdout diff =
   untouched); lens tallies: zero eliminations, no class membership moved (the TD3
   record differs only by the sign-stamp wording); KMOD0 quotient and fork-independence
   checks byte-identical; F-D records changed only by the F-D3 two-repair memorial.
   The fourth-catch claim is consistent with the banked Stage-3 record ("THIRD catch"
   at 21d589c). The §1 pre-amendment-claims list matches what I actually found.
5. **AUDIT_REPORT.md — FAITHFUL:** contract-first, 21/21 independent checks, both
   strengthenings credited (explicit global inverse; symbolic both-signs legs), A1/A2
   disposition accurate ("no claim refuted, no computation touched"), the bootstrap
   pair recorded exactly as observation (STRENGTHENED-AS-HYPOTHESIS via the emergent
   tie / WEAKENED-AS-UNIVERSAL via the P2 absence — limit 7; nothing settled, ceiling
   respected), M-stamp and NV-honesty limits carried, verifier caveat travels.
   N1/N2 recorded (CORRECTION_LAYER §2 — not-required notes, acceptable as recorded);
   N4 done (dead code removed; only the JSON amendments note references it).

## Residual notes (non-blocking, no amendment required)

- R1 (cosmetic): the ledger's W2-fs representative LABEL still reads "W2-fs (well tuple
  at aF=2lam; …)" — a shape word inside a family NAME; the adjacent solution-space
  column carries the full A1 sign stamp, so no reader can take the unstamped meaning.
  Check identifiers (`TD1_LE_well_*`, `A1_well_*`) likewise retain "well" as names —
  correctly left stable for comparability.
- N1 stands as recorded (TD1_LE_E0zero_constants_only remains a duplicate-boolean
  corollary row counted substantive; split now 33/8, honest).

*Blind verifier closure pass, 2026-07-29. Nothing committed by the verifier.*

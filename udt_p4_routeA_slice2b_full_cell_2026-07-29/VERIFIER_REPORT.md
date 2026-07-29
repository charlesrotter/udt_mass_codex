# BLIND VERIFIER REPORT — P4 Route A Slice 2b (full-cell generality + branched mass legs)

Date: 2026-07-29. Verifier: blind adversarial verifier, **same-session-spawned** (zero
package context at start; **caveat: not a hosted external model** — spawned from the same
session per house method §6(3); the caveat travels with this record). Independent script:
`VERIFIER_INDEPENDENT_CHECK.py` (own jet machinery, own solution construction from the
reduced energy ODE, own survivor-set logic; 26/26 pass, exit 0; preserved) +
`VERIFIER_INDEPENDENT_STDOUT_2B.txt` if regenerated. Adjudication stance: attack the
"exactly/only/all/none/robust" quantifiers first (F-E3, fifth-catch watch), then
F-E1/F-E2/F-E4/F-E5 and the inherited F-D set.

## VERDICT: **PASS-WITH-REQUIRED-AMENDMENTS** (4 amendments; none touches a computed law)

Every load-bearing mathematical claim survived independent re-derivation — several with
STRONGER grounding than the package states (below). The amendments are two scope/typing
defects (one of them exactly the named F-E3 class — the fifth catch), one record-honesty
gap, and one check-bookkeeping overcount. No refutation.

## Duty 1 — rerun and contract-first: CLEAN

- `PREREGISTRATION.md` committed ALONE at 5ac0de8 (2026-07-29 12:41), all artifacts
  timestamped 13:01–13:04, working-tree prereg byte-identical to the commit
  (`git diff 5ac0de8` empty). Contract-first VERIFIED in git. R1/R2 rulings and the
  bootstrap-lens frame present in the frozen contract.
- Rerun: exit 0, **35/35 = 27 substantive + 8 guards** (split audited against the JSON
  `kind` fields and the in-script `CITATION_GUARDS` set — the 8 guard names match the
  [guard] labels in prose; but see Amendment A4 on two thin "substantive" checks).
- Stdout byte-identical to `DERIVATION_STDOUT.txt`; regenerated
  `routeA_slice2b_results.json` / `FULL_CELL_ATLAS_LEDGER.tsv` / `DIVERGENCE_MAPS.tsv`
  byte-identical (sha256). Ledger = 20 rows × 14 columns exactly. Purity scan: no floats/
  evalf/nsolve/random/numpy in the derivation script. Runtime minutes — scope-ladder
  non-use consistent.

## Duty 2 — independent re-derivations (own constructions)

**(a) Bookkeeping divergence theorem — ATTACKED HARDEST; HOLDS, with stronger grounding.**
I re-derived the quadratic-class atlas by SOLVING, not substituting: the f/h rows force
(f′,h′) = G⁻¹c/w; the conserved energy gives w′² = (2a²/g_p)(E0·w − qc/2); differentiating
gives w″ = a²E0/g_p on every nonconstant solution — i.e. **w is EXACTLY quadratic: the
atlas is EXHAUSTIVE on the class** (6 params = the Picard data count). This exhaustiveness
argument (which the package leaves implicit under its Picard citation) is what grounds
every "exactly/only" survivor quantifier — verified, not just asserted. The p-row uniquely
FORCES A = a²E0/(2g_p) with the stated E0 (solved, single root). POINTWISE survivors =
{E0 = 0} exactly (own logic: E0 = 0 directly, or p0 ≡ 0 ⇒ A = 0 ⇒ E0 = 0), including the
indefinite stratum: definite ⇒ constants only (sum-of-squares solve returns exactly
w1 = c_f = c_h = 0); indefinite ⇒ the nonconstant affine member w = x+2 with E0 = 0
verified as an exact solution. STRICTNESS of the inclusion: I certified the massive
I_p = 0 locus nonempty INDEPENDENTLY of the banked-A2 citation — exact closed-form
I_p with certified sign change (I_p(c=1) ≈ −0.858 < 0 < I_p(c=6) ≈ +2.773, both E0 > 0;
50-digit sign certification, verifier-side) ⇒ a massive integrated survivor exists ⇒ the
tie's massive branch exists ONLY on the INTEGRATED side, on the quadratic class. The
mass-branch robustness of the tie's zero locus (all four masses ∝ E0 or E0·V, V > 0)
re-checked. **But see Amendment A1: the LEDGER columns state these survivor sets without
their quadratic-class stamp.**

**(b) Mass-branch identities — ALL HOLD.** (i) M-DENS-proper = ∫(E0/w)·w dx = 2ℓE0 =
M-GEN identically (re-derived). (ii) M-WALL: own by-parts/wall-momentum construction —
π_f = c_f, π_h = c_h exactly (p-slot the ONLY nonvacuous wall-difference slot, derived on
the class), [π_p] = g_p[w′]/a = 2aℓE0 = a_F·M-GEN with g_p and G cancelling; the
canon-parity trace-functional caveat is present and stamped in the availability table AND
the ledger M-WALL column. At a_F = 0 I DERIVED the result the package's check only
tautologizes (A4): the Euler rows at a_F = 0 force u″ = 0 (affine atlas), p1 const,
M-WALL ≡ 0 while M-GEN free. (iii) coord law: M-DENS-coord − M-GEN = E0(V − 2ℓ),
V = (2/3)Aℓ³ + 2w0ℓ — exact, the 2(w0−1)ℓ term present and correct. **But see Amendment
A3: no record of the claimed self-caught dropped term exists anywhere in the package.**
(iv) Consensus witness: w = (3/2)x² + 1/2 at a_F = 1, ℓ = 1 is an exact solution with
E0 = 3, V = 2, all four readings = 6 (verified); its off-survivor stamp verified STRONGER
than the Jensen citation: exact quadrature I_p = −4 + log 4 + 4√3π/9 ≈ −0.195 ≠ 0
(closed form), and E0 = 3 ≠ 0 excludes it pointwise. No OE3 promotion language found;
"OE3-flavored observation, NOT a promotion" carried everywhere the witness appears.

**(c) Definiteness scoping / F-D4 adjudication: REFINEMENT, not contradiction.** Both
indefinite witnesses re-derived exactly (E0 = −2, w = 1−x², nodes ±1; E0 = 0, w = x+2
nonconstant); disc = −(a²/g_p)·cᵀG⁻¹c own-algebra exact; definite instance E0 ≥ 0,
disc ≤ 0 (congruence extension is legitimate Category-A). The Slice-2 bank's own words:
"Every 'solution space' claim below is scoped to its representative family; NONE is a
cell" (EXACT_DERIVATION.md §TD1 preamble), "SCOPE: GEN-QUAD representative, a_F ≠ 0
branches, BASE branch" on the E0 ≥ 0/nodelessness claim, and "representatives — NOT a
cell-general claim." **RULING: the Slice-2b definiteness-scoping REFINES a rep-scoped
banked claim; F-D4 does NOT fire. The banked CHOSE(representative) stamp did its job.**

**(d) The two arbitrary-member theorems — HOLD.** Energy first integral: own machinery,
zero residual with arbitrary L̃. Shift-current non-extension: I derived the exact failure
law Dx(π_f) = ∂S/∂f0 − E_f(S) identically, so the current is conserved on-shell IFF
∂L̃/∂f0 = 0 — the claim's "exist exactly on the sub-class" is the precise statement; a
member-universal counterterm is impossible (the defect W_F∂L̃/∂f0 is member-arbitrary).
Leading-symbol dichotomy: ∂E_a/∂u_b″ = −W_F·Hess re-derived; pairing-independence rides
only on W_F > 0 (banked T0).

**(e) NV re-grades.** W1 Helmholtz defect −2a_F p1 W_F re-derived; p1, f1, h1 each
conserved on the affine atlas (verified). W2-fs: E0 = e^{2λp0}L̃0 conserved on-shell
(verified); its provenance is genuine — the banked Slice-2 record says W2-fs is "the
IDENTICAL tuple to GEN-QUAD at a_F = 2λ", so the energy is the TUPLE'S OWN (a generated
tuple that is NV only pairing-relatively): **M-GEN-eq is derived-typed, not an invented
kernel — F-E2 does not fire on W2-fs.** M-WALL = 0 on zero-declared walls carries its
"artifact of the declaration" stamp in prose, ledger, and map (verified present). **But
the W1 refusal is INCONSISTENT with the W2-fs grant — Amendment A2.**

**(f) Full-cell extension.** Closed form re-derived fully symbolically AND at an own
sub-instance (g_p = 2, G = diag(1,3), a_F = −2, negative branch): zero residual. The
stated obstructions (p-mixed weight anisotropy; Liouville-class; NV universality) are
honest boundaries — the TE1 theorems demonstrably cover those members (arbitrary-L̃
proofs), and the obstruction row is guard-labeled, not counted as computation.

## Duty 3 — falsifier hunts

- **F-E3 (FIRST; the named class): ONE CATCH — Amendment A1** (ledger columns missing the
  quadratic-class stamp on the R2-survivor and tie-status claims). All other
  exactly/only/all/none/robust claims audited: each carries its stamps in prose and maps;
  the three danger spots the derivation itself flags (M-WALL parity caveat, M-GEN-eq
  sub-branch label, consensus off-survivor stamp) were each hunted — the first and third
  are clean and verified; the second yields Amendment A2.
- **F-E1: clean.** No mass branch called natural/correct/physical; disagreements mapped,
  none resolved; the calibration and consensus rows use the prereg's own contract
  language; the sign-divergence row ("wall reading assigns negative mass") is labeled
  observation.
- **F-E2: clean** (five definitions, each with banked provenance; W2-fs adjudicated
  above; the W1 refusal is itself an F-E2-respecting refusal — the problem is its
  asymmetry, not an invention).
- **F-E4: clean.** Every tie quote carries INTEGRATED-branch; the pointwise analog is
  computed separately, never conflated.
- **F-E5: clean.** NEXT_SURFACE frames R1/R2 as "Charles's calls, later"; "the R2 fork is
  now a MASS question" is a computed map statement (only INTEGRATED admits massive
  self-consistent members — a theorem on the quadratic class), not a nudge; no
  recommendation language.
- **Inherited F-D1/D6/D7/D8: clean.** No crowning (massive-branch language stays
  survivor-set description); carrier closure rows typed OUT, never instantiated (G09);
  R5 triples on one solution per branch; tie observations lens-clean ("observation only,
  settling is Charles's").

## Duty 4 — contract compliance: CLEAN

TE1–TE6 each delivered as frozen (TE4 per its filled/typed clause; TE1's obstruction
statements are the prereg's honest-boundary clause). Scope ladder unused — consistent
(minutes of CPU, full declared scope present). Ceiling respected: no law crowned, no mass
rule promoted, no fork decided, no bootstrap settlement, no carrier. OE1 is the correct
outcome class (no elimination, no OE4 halt; OE3-flavored rows correctly kept INSIDE the
map). `AUDIT_REPORT.md` (a prereg deliverable) is still owed at the post-verifier step —
due before commit, not an amendment.

## REQUIRED AMENDMENTS

- **A1 (F-E3 — the FIFTH catch of the named scope class; ledger only).** In
  `FULL_CELL_ATLAS_LEDGER.tsv`, the anchored-LE rows' `R2_INTEGRATED_survivors`
  ("{E0 = 0} UNION {I_p = 0 ...}"), `R2_POINTWISE_survivors` ("{E0 = 0} ONLY (exact ...)"),
  and `tie_status` ("tie = 2 E0 I_p = 0 present ...") columns state quadratic-class
  characterizations WITHOUT an in-column "quadratic class" stamp. Read cell-generally
  they are FALSE: for a non-quadratic member the λ-row is a_F′·∫p0·W_F L̃ dx (nonconstant
  integrand ≠ E0), and the survivor sets are NOT characterized. The prose
  (EXACT_DERIVATION.md §2) and DIVERGENCE_MAPS.tsv rows carry the stamp; the ledger
  columns must too (add "quadratic class; beyond it: row = a_F′∫p0 W_F L̃, survivors
  uncharacterized (typed)" or equivalent).
- **A2 (M-GEN-eq availability asymmetry — TE2_NV_regrade_per_branch + availability
  table + ledger NV M_GEN column + DIVERGENCE_MAPS NV-availability row).** The W2-fs
  grant rests on: the tuple IS a generated tuple under a DIFFERENT enumerated pairing
  (anchored, a_F = 2λ), so its energy is the tuple's own. W1 satisfies the SAME
  principle: the banked record ("W1 = (p2, f2, h2) ... LE at a_F = 0") makes W1's tuple
  the weight-free generated tuple (generator −L̃0, unique up to null Lagrangians, which
  do not shift the energy), giving the same-provenance first integral L̃0 conserved on
  the affine atlas (verified). The availability table's restriction to "coincide with an
  ANCHORED generated tuple" has no stated derivation, and the W1 refusal reason
  ("conserved 1-jets exist but none structure-selected") ignores the selector that DOES
  exist — the a_F = 0 generator, exactly parallel to W2-fs's a_F = 2λ generator. FIX
  (either way, labeled): extend M-GEN-eq to W1-class (DETERMINED-under-M-GEN-eq via its
  weight-free generator, value ±2ℓL̃0 per the generator's sign convention, member
  staying NV under P1 — stamped), OR refuse it for BOTH and re-grade W2-fs back, OR
  derive and state the discriminator that legitimizes anchored-only. Decision-relevant
  for Charles's R1 fork; must not ship asymmetric.
- **A3 (record honesty).** The dispatch to this verifier states the derivation
  SELF-CAUGHT a dropped term in the M-DENS-coord law (the E0(V − 2ℓ) leg). NO record of
  any such catch exists in the package (grep: no "caught/corrected/dropped" in script,
  prose, stdout, or JSON). The shipped law is verified CORRECT (including the 2(w0−1)ℓ
  term). House precedent memorializes catches (the F-S3/F-E3 catch records). Either
  memorialize the catch in EXACT_DERIVATION.md (what was dropped, how caught) or strike
  the claim from the handoff — an unrecorded catch and an over-claimed catch are both
  honesty defects.
- **A4 (check bookkeeping, minor).** `TE2_MWALL_P2_zero` is TAUTOLOGICAL as coded (first
  conjunct subtracts an expression from itself; second conjunct compares identical
  expressions at a_r = 1) yet counts SUBSTANTIVE; the claim itself is true — my
  independent derivation establishes it (Euler rows at a_F = 0 force the affine atlas)
  — but the check computes nothing. `TE3_tie_fate_map`'s computational content is
  likewise thin (two trivial solves + one reused identity). Strengthen both or re-tag;
  the honest substantive count is ~25-26, not 27. (`masses_vanish` is computed and
  unused — cosmetic.)

## What survived attack (for the record)

The load-bearing structure is SOLID: atlas exhaustiveness (proved here via the energy
ODE — recommend adding it to EXACT_DERIVATION.md, it is one line and closes the
"exactly" quantifiers' only gap), both survivor sets, strict inclusion with an
independent existence certificate, all four mass laws and their divergence loci, the
consensus witness with exact off-survivor closed form I_p = −4 + log 4 + 4√3π/9, the
definiteness scoping with both witnesses, F-D4 = REFINEMENT, the two arbitrary-member
theorems, and the full falsifier discipline outside A1/A2.

— blind verifier (same-session-spawned; not a hosted external model), 2026-07-29

---

# AMENDMENT CLOSURE (same verifier, second round)

Date: 2026-07-29. Same blind verifier (same-session-spawned; not a hosted external
model). Stance: attack the amendment pass, not confirm it.

## VERDICT: **CLOSED**

All four required amendments implemented as specified, check-backed, with nothing
weakened and nothing new smuggled. Adjudication per item:

1. **Rerun/determinism/purity: CLEAN.** 39/39, exit 0; stdout and all regenerated
   outputs byte-identical to the shipped files (sha256 match the CORRECTION_LAYER §3.5
   values); split 31 substantive + 8 guards audited against the JSON `kind` fields
   (the 8 guard names unchanged; the 4 new checks all substantive and genuinely
   computed). Purity scan clean — the only "evalf" hits are prose saying "evalf-free".
   Repo harness re-run: 70 passed / 1 xfailed (claim confirmed).
2. **The exact sign chains: VALID AND SUFFICIENT (attacked line by line).**
   (a) `ADOPTED_Ip_signchange_exact`: I_p(c=1) = pi - 4 exactly (machine-checked
   closed form); pi <= 22/7 < 4 by the Dalzell integral (machine-checked identity
   22/7 - pi = integral of a manifestly nonnegative integrand) — valid. I_p(c=6) =
   2 log(37/2) - 4 + (2/3) atan 6 exactly (machine-checked); positivity via
   e < 65/24 + 1/100 = 1631/600 < 11/4: the tail bound sum_{k>=5} 1/k! <
   (1/120)·sum(1/6)^j = 1/100 is a valid geometric majorant (term ratios 1/6, 1/7, ...
   <= 1/6), so e^2 < 121/16 < 37/2 and log(37/2) > 2 — valid and sufficient; atan 6 > 0
   trivial. E0 = 1 and 36 on the family, connected with E0 > 0: the sign-change
   existence certificate stands exactly. (b) `ADOPTED_consensus_Ip_closed_form`:
   I_p = -4 + log 4 + 4 sqrt(3) pi/9 machine-checked; negativity via log 4 < 7/5
   (partial sum sum_{k<=5}(7/5)^k/k! > 4, rational-verified, positive series),
   sqrt(3) < 26/15 (676/225 > 3), pi < 22/7; the bound 7/5 + 2288/945 = 3611/945 < 4
   is exact rational arithmetic and all factors positive (monotone substitution valid).
   Both replacements are STRONGER than my evalf(50) certifications. (c) The adopted
   exhaustiveness check faithfully encodes my energy-ODE argument (three zero-residual
   identities: E-form on the class, ODE = energy conservation, d/dx factorization).
3. **A1: CLOSED.** All six anchored-LE ledger rows now open the R2-survivor and
   tie-status columns with "QUADRATIC CLASS (A1 stamp):" and close with the correct
   beyond-class row form (a_F'∫p0·W_F L̃ / pointwise analog, "no E0 factorization") and
   UNCHARACTERIZED (typed) — the exact fix required. Fifth catch memorialized in
   EXACT_DERIVATION §7 and AUDIT_REPORT with the per-artifact-drift diagnosis (accurate)
   and standing corrective.
4. **A2: CLOSED — the null-Lagrangian check is GENUINE; W3 refusal basis CORRECT; no
   promotion creep.** (a) `A2_W1_MGENeq_extension` machine-checks: W1 = Euler(-L̃0)
   component-exact; the energy of the autonomous jet-local null Lagrangian Dx(g(0-jets))
   is IDENTICALLY zero (a real zero-residual identity — and within first-order
   autonomous generators, null Lagrangians ARE exactly Dx g(u) + const, Category-A;
   the additive-constant energy shift is explicitly carved out as the shared
   normalization convention — honest); orientation flip machine-checked
   (Euler(+L̃0)_p = -p2). (b) W3 refusal: I verified independently that NO first-order
   generator can produce (p1, 0, 0) — for L linear in p1 (forced: no p2 allowed),
   E_p(L) = b_p0 - a_f0 f1 - a_h0 h1 can never contain p1 — the stated basis ("no
   generated-tuple identity in banked structure") is correct and in fact provably
   unfixable at jet <= 1. (c) Language: availability statements only, ±2ℓL̃0 sign
   labeled, [DECISION-RELEVANT-R1] flagged in check, ledger, map row, NEXT_SURFACE
   leg (c), and AUDIT_REPORT; "whether M-GEN-eq is admitted at all is Charles's call"
   — no promotion creep found. OBSERVATION (not a defect, for Charles's desk): at the
   BANKED orientation W1 = +(p2, f2, h2) the derived energy is -L̃0, so the
   banked-orientation value is M = -2ℓL̃0 (nonpositive); the ± honestly reflects the
   presentation/orientation freedom that equally rides the W2-fs grant (whose banked
   R_LE presentation quietly fixes the + sign there) — the labeled-sub-choice framing
   is the correct treatment.
5. **A3: CLOSED.** The withdrawal (CORRECTION_LAYER §A3) is the honest resolution:
   strike + dispatch-vs-record process-defect log, explicitly refusing a retroactive
   memorial; the law's correctness (verifier-confirmed) recorded. Package-wide grep:
   the only surviving "self-caught" strings are the withdrawal/process-record entries
   themselves (script banner, JSON amendments block, EXACT_DERIVATION banner/§7) — all
   describe the claim AS withdrawn; no assertive instance survives.
6. **A4: CLOSED.** `TE2_MWALL_P2_zero` now derivation-backed (Euler rows at a_F = 0
   solved to the affine atlas, unique; pi_p constancy and energy conservation
   machine-checked — matches my V_MWALL_P2_zero_derived); `TE3_tie_fate_map` now
   computes the mass-zero solves under declared assumptions plus four zero-residual
   nonzero-factor row rewrites; `masses_vanish` gone; the honest split restated in
   script, stdout, JSON, EXACT_DERIVATION, CORRECTION_LAYER, AUDIT_REPORT.
7. **Did-NOT-change list: VERIFIED by comparison.** OE1 unchanged (JSON); both TE1
   theorems and their check names/details intact; the closed-form atlas, both survivor
   sets, strict inclusion, all four mass identities, the F-D4 REFINEMENT ruling, and
   the 20x14 + 15 map structure all match my round-1 adjudicated content (the only
   content deltas are the A1 stamps, the A2 NV column/row, and the A4 check recodings
   — exactly as listed). The exhaustiveness upgrade is a strengthening with survivor
   sets unchanged, as claimed.
8. **AUDIT_REPORT: FAITHFUL.** 26/26 credited; the three adopted proofs attributed;
   A1-A4 dispositions accurate; fifth catch + process defect memorialized; verifier
   caveat carried; grade VERIFIED-WITH-AMENDMENT; no fork nudge (the R2 stakes are
   stated as map facts; forks and the M-GEN-eq admission expressly Charles's). It
   correctly records that same-verifier closure was owed — this section discharges it.

No OPEN items; no NEW-DEFECT. The package is closure-adjudicated from this verifier's
side; banking remains the driver's step (nothing committed by me).

— blind verifier (same-session-spawned; not a hosted external model), 2026-07-29

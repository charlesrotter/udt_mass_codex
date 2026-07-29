# BLIND VERIFIER REPORT — P4 Route A Stage 2 (pointwise reduction ℛ_PW)

Verifier: blind adversarial verifier, **same-session-spawned** (zero-context framing;
**not a hosted external model** — the standing caveat travels). Date: 2026-07-29.
Target: `udt_p4_routeA_stage2_pointwise_reduction_2026-07-29/`; binding contract
`PREREGISTRATION.md` @ b741add. Independent script:
`VERIFIER_INDEPENDENT_CHECK.py` (this package; all 33 checks pass, exit 0 — including
the adversarial counter-computation of §2b below).

## VERDICT: **PASS-WITH-REQUIRED-AMENDMENTS**

The rerun, the anchored-exponent condition, the character-module bases, the slot
algebra, the located objects, the jet-3/4 typing, the falsifier hygiene (F-B1..F-B6
prose+code), and the contract compliance (TB1–TB6, ceiling, no gate run) all
VERIFIED. **One load-bearing claim is REFUTED AS STATED and must be amended: the
R7(b) Noether-vacuity claim** (`PW2_R7b_noether_pointwise_vacuous` + EXACT_DERIVATION
§2 + the STAGE3_HANDOFF gate-1/gate-4 notes). The refutation does NOT overturn OB1
(nonemptiness survives — the ω-shape witness satisfies the corrected identity); it
makes the published parametrization a strict SUPERSET of the true ℛ_PW on a
codimension-1 stratum of the moduli.

## 1. Rerun / contract-first (duty 1) — PASS

- Contract-first CONFIRMED in git: `PREREGISTRATION.md` committed alone at b741add
  (2026-07-29 00:52) before any derivation artifact existed (artifacts untracked,
  written 01:06–01:08).
- `python3 derive_routeA_stage2.py`: exit 0, 53/53, < 1 s. All three outputs
  (`routeA_stage2_results.json`, `RESIDUAL_SPACE_LEDGER.tsv`, stdout vs
  `DERIVATION_STDOUT.txt`) regenerated **byte-identical** (mtimes confirm actual
  overwrite). Exact SymPy only; imports clean (no floats/randomness/network); ledger
  = 41 data rows + 2 header lines.

## 2. Independent re-derivation (duty 2)

**(a) Anchored-exponent condition — VERIFIED (own derivation, stronger than the
package's).** I re-derived the anchoring from the banked shift-with-absorption orbit
(φ, c_E) ↦ (φ+s, c_E·e^s) by the orbit-space argument: (φ, c_E) ↔ (φ, Q) is an
invertible change of variables (c_E > 0), the shift is transitive on the φ-line and
trivial on Q, and for a GENERAL smooth F(φ, Q), d/ds F(φ+s, Q)|₀ = F_φ — so
invariance ⟺ no bare-φ argument, i.e. zero-jet dependence factors through Q exactly
(`VB_*`). This is stronger than the package's power-family check (which only proves
p = q within c_E^p e^{−qφ}); the general exclusion IS forced by shift-equivariance +
the banked D3 absorption alone — no extra assumption from the mirror-tension (V8)
resolution is smuggled (V8 is used only, and correctly, to route anchored-φ WALL data
through supplied slots). φ-jets evade anchoring and are correctly included as
shift-invariant blocks (all orders, `VB_jets_shift_invariant`); φ-differences
φ(x)−φ(y) are bilocal — outside the pointwise alphabet by scope, and excluded upstream
by Stage-1 J04/R1 provenance. Handled.

**(b) Noether-vacuity claim — COMPUTATION CORRECT, INTERPRETATION REFUTED AS
STATED.** The class-wide computation is right: the system "[B,X] tangent to the class
for EVERY class member" has rank 6, nullspace empty
(`VC_classwide_stabilizer_trivial_recomputed`). But the inference "⟹ NO continuous
gauge direction tangent to the registered-chart configuration space ⟹ pointwise
Noether identity set EMPTY" conflates the class-wide stabilizer with the POINTWISE
(per-member) tangency stabilizer. Counter-computation (`VC_*`, `VH_*`, all exact):

- At a generic member the pointwise stabilizer is trivial (rank 6) — the claim holds
  GENERICALLY.
- **On the codimension-ONE stratum k_mod = 0** (k00 = k11, any λ, k10, C) the rank
  drops to 5 and the nullspace is span(L23), the screen rotation:
  **[L23, X]|_{k_mod=0} = [[0,0],[J·C, k10·diag(1,−1)]] ≠ 0** for (k10, C) ≠ 0 —
  a nonzero infinitesimal local-Lorentz motion TANGENT to the registered class
  (δλ = δk10 = 0, δk_mod = −k10, δC = J·C). Route B's finite-residual enumeration
  (= K₄) is unaffected — the finite orbit exits the class (S·E21·S⁻¹ has entry
  −sin²θ in the forbidden (2,3) slot) — but R7(b) is an infinitesimal identity, and
  Stage-1's R7(b) reads "⟨𝓡, δ_gauge𝒳⟩ ≡ 0 identically for gauge directions — PW as
  an identity". On the stratum that identity set is NOT empty; its moduli-sector form
  is exactly
  **−2·k10·r_tf + m00·c10 + m01·c11 − m10·c00 − m11·c01 (+ field-sector terms) = 0
  at k_mod = 0** (`VH_stratum_identity_form`), and it is K₄-consistent (every term
  χ_a-graded).
- **The package's own nonemptiness witness violates it:** the "unit trace-free screen
  kernel with R_kmod = 2" (r_tf = 1, all other components — field components
  included — zero) pairs to −2·k10 ≠ 0 with this gauge direction
  (`VH_witness_member_violates`; robust to any field-sector completion because the
  witness's field components vanish). So ℛ_PW **as parametrized contains members not
  well-defined on the quotient**: the published parametrization is a strict superset
  of the true ℛ_PW.
- Further higher-codimension degeneration strata exist (e.g. C = 0 with
  λ∓k_mod ∈ {±1}: base-block eigenvalue resonance, rank 5 —
  `VC_resonance_locus_C0_a_eq_m1`); an exhaustive stratum enumeration is owed by the
  amendment.
- **OB1 SURVIVES:** the ω-shape witness (r_sh = k10, all else 0) satisfies the
  stratum identity (tr(E21ᵀ·diag(1,−1)) = 0, checked), so nonemptiness and the
  character-sector exhibits stand after correction.
- Scope note: the same generic-only gloss sits in the BANK — Stage-1
  POSED_INVERSE_PROBLEM §1.4 "on the registered chart, mod nothing continuous — the
  quotient is discrete K₄" and the Route B T1 headline. The Route B COMPUTATION is
  correct (class-wide); the per-stratum reading was never checked upstream. Flag for
  the driver to route to the registry.

**(c) Character-module bases — VERIFIED, with an all-degree proof of my own.**
Independent code (different algorithm), generation checked exhaustively to **degree
8** (exceeds the package's 6) for the invariant ring (11 generators) and all three
modules (`VD_*`). All-degree closure proven by my own Davenport-style argument: the
parity case split (χ_a: e odd ⟹ divide k10, e even ⟹ p+q and r+s both odd ⟹ divide a
c_b·c_c pair; χ_b/χ_c mirrored; invariant-ring indecomposables have degree ≤ 3 since
the Davenport constant of (ℤ/2)² is 3) verified on every monomial
(`VD_all_degree_case_split_verified`). Ranks 1/5/4/4 confirmed; minimality confirmed
(each class's degree ≤ 2 monomials are exactly its generators; the invariant ring
starts at degree 2); syzygy I1·(c00c01) − I8·k10 = 0 reproduced. "Generically rank 1"
is stated WITH its degeneration loci (the K₄-fixed strata) in both code detail and
prose — compliant.

**(d) Slot uniqueness — VERIFIED, one convention note.** Gram of {I₂, diag(−1,1),
E21} = diag(2,2,1), nondegenerate; E12 null against all three; component pairings
(2r_tr, 2r_tf, r_sh) reproduced (`VE_*`). Cross-check against the Route B physical
tangent T = [[2I₂,Cᵀ],[C,K+Kᵀ]]: pairing against δ(K+Kᵀ) gives (4r_tr, 4r_tf,
r_sh + r_nl) — an invertible reparametrization of the SAME component space, so the
parametrization is convention-independent; but "E12 is a null unpaired slot" is true
only in the chart-δK pairing convention (against the physical δ(K+Kᵀ), the symmetric
E12+E21 combination pairs). Minor amendment A3.

**(e) Branch independence — GENUINE BUT INFORMAL; accepted.** BR-B and BR-C carry
real structural arguments (wall data enter as supplied arguments in both forks so the
pointwise component expressions are identical, only the equation-vs-condition ROLE
differs = WS; 𝔠 is discrete in both forks and enters only as an argument slot, no
infinitesimal direction, difference = GC). These are proofs-by-construction-
inspection, not zero-residual computations — no computation could carry them; graded
genuine. BR-M and BR-CE correctly stamped TYPED/NOT-EXHAUSTED in ledger, JSON, and
prose. No silent fork freeze found.

**(f) Located objects — VERIFIED.** EH: the banked Route C restricted system's jet
signatures independently re-read from `routeC_stage1_results.json` — max jet 2 across
all seven components (`VF_EH_jets_le2`); φ-dependence via seat exponentials
e^{aφ} = (c_E/Q)^a is anchored (`VF_seat_exponentials_anchored`); trivial-character
moduli dependence (λ) checked; (k10,C)-independence on the diagonal presentation ⟹
J06-retained classification for k10/C is correct. Bach: max jet 4 with 3rd/4th jets
present (`VF_Bach_jets_34`) — correctly OUTSIDE jet ≤ 2, INSIDE the typed extension;
not smuggled in or out. Exclusions: character-mismatch, absolute-φ, pure-trace-kernel,
restrict-then-vary each backed by an exact computed witness (verified); fitted-global
is a definition-level provenance audit (string scan) — honest as labeled, since the
exclusion is by type, not computable.

**(g) Jet-3/4 order-independence — HOLDS.** Attack surface checked: K₄ substitutions
touch only {k10, C} — disjoint from field jets at every order; shifts leave all jets
(n = 1..4 checked, argument order-blind) inert; R8 is jet-level TYPING (declare the
grade, compute D𝓡) and acts identically at any declared grade; R12/J14, J01/J02,
R1/R13/J12 are order-blind typings. No PW requirement acts differently on 3rd/4th
jets. The one order-sensitive surface (wall-slot DEPTH grows with N) is already
carried as example-typed/NOT-EXHAUSTED (Route C TC5) — compliant. NOTE: amendment A1's
stratum identities are themselves order-independent (the gauge direction is
moduli-sector), so the corrected structure remains order-independent.

## 3. Prose falsifier hunts (duty 3)

- **F-B1 — CLEAN.** Located-object language stays observational throughout
  (EXACT_DERIVATION §5 "OBSERVATIONS ONLY"; handoff §5 "carrying no precedence");
  no member selected/privileged; no ranking of families in STAGE3_HANDOFF; no WS/GC
  gate run.
- **F-B2 — CLEAN.** Six branches labeled; BR-B/BR-C independence argued (see 2e);
  BR-M/BR-CE typed.
- **F-B3 — CLEAN.** Every exhaustive claim carries the jet ≤ 2 + presentation +
  polynomial-in-moduli stamp (ledger header, JSON scope_stamps, MD standing stamps);
  structural vs exhaustive kept separate. (Amendment A1 adds one more stamp:
  "parametrization exact OFF the degeneration strata; stratum identities on them.")
- **F-B4 — CLEAN as to usage; one upstream flag.** A1-amended character-matched rule
  and A3-amended narrowed channel class used correctly throughout (slot theorem
  stated in its narrowed form with the tr(X²) counter-channel routing); Route B/C
  banked facts recomputed and matched. The §2b finding indicts a BANK
  interpretation-layer sentence (Stage-1 §1.4; Route B T1 gloss), not Stage 2's use
  of it — routed upstream via A1(v).
- **F-B6 — CLEAN.** Every equivariant space carries an exhibited basis with
  generation, minimality, syzygies (independently reproved here to degree 8 +
  all-degree).

## 4. Contract compliance (duty 4) — PASS

TB1 (§1, alphabet + zero-residual grading), TB2 (§2, bases computed), TB3 (§3, slot
algebra + J06 branches per family, none chosen), TB4 (§4 + ledger, parametrization +
fork table + jet-3/4 typing), TB5 (§5, OB1 verdict + locations + exclusions), TB6
(STAGE3_HANDOFF, a handle not a launch) — all addressed. Limits-that-travel stated
(§6). No WS/GC gate run. Maximum-conclusion ceiling respected (no member selected, no
full-ℛ verdict, no action, no physics).

## 5. REQUIRED AMENDMENTS (exact)

- **A1 (substantive — the §2b refutation).**
  (i) Restate `PW2_R7b_noether_pointwise_vacuous` + EXACT_DERIVATION §2: "the
  pointwise stabilizer is trivial at GENERIC members; on the k_mod = 0 stratum
  (codim 1) the screen rotation gives the class-tangent gauge direction
  (δk_mod, δC) = (−k10, J·C), and R7(b) imposes the nontrivial pointwise identity
  −2k10·r_tf + m00c10 + m01c11 − m10c00 − m11c01 (+ field-sector terms, to be
  derived) = 0 there; further higher-codim resonance strata (C = 0, λ∓k_mod ∈ {±1})
  exist and owe an exhaustive enumeration."
  (ii) Add the stratum identity to the §4 parametrization and the ledger conditions
  column (R_kmod, R_C rows): as published, ℛ_PW is a strict SUPERSET of the true
  residual space on the stratum.
  (iii) Replace or scope the r_tf = 1 constant-kernel nonemptiness witness (it
  violates the identity at k_mod = 0, k10 ≠ 0); the ω-shape witness stands, so OB1
  is unaffected.
  (iv) Correct STAGE3_HANDOFF gate-1/gate-4 notes: gate 1 must NOT assume "no
  continuous chart-gauge identities" — that holds only off the degeneration strata;
  on them explicit stratum identities exist (still not Bianchi-TYPE differential
  identities — that warning stands).
  (v) Route upstream: flag Stage-1 POSED_INVERSE_PROBLEM §1.4 ("mod nothing
  continuous") and the Route B T1 headline gloss as generic-only statements
  (registry/CONDITIONS-CHANGED style note; the Route B computation itself is
  correct).
- **A2 (minor — labeling).** The "53/53 zero-residual checks" headline overcounts:
  ~8 checks are bookkeeping/citation guards, not residual computations
  (`PW4_R2_census_component_coverage` compares a list to its own copy;
  `PW5_obs_Bach_form_typed_class_only` = `4 > 2`; `PW5_obs_EH_form_lands_in_jet2_class`
  includes `2 <= 2`; `PW4_R13_no_global_entries_in_alphabet` is a string scan;
  `PW1_bare_phi_excluded` is trivially true as coded). Each is honestly described in
  its detail string and the cited content is genuinely banked (I verified the Route C
  jet signatures independently), but the headline should distinguish computational
  checks from citation guards.
- **A3 (minor — convention note).** "E12 is a null unpaired slot" is a chart-δK
  pairing-convention statement; against the physical tangent δ(K+Kᵀ) the symmetric
  E12+E21 combination pairs (component space isomorphic either way). Add the note
  where the null slot is introduced (§3).

## 6. Bottom line for the driver

Structure verified end-to-end; OB1 stands; no selection, no imposition, stamps clean.
One real hole: the Noether-vacuity claim is a GENERIC-stratum truth stated as
unqualified — on the codim-1 k_mod = 0 stratum a continuous gauge direction is
tangent to the registered chart, it induces an exact, K₄-consistent pointwise
identity, the published parametrization misses it, and one of the two exhibited
nonemptiness witnesses violates it. Fix per A1 (and note the new stratum identity is
itself a POSITIVE structural finding: the first nontrivial pointwise Noether content
of the response problem, tying r_tf to the mixing kernel on the reciprocal-isotropy
locus). Not committed by the verifier.

---

# AMENDMENT CLOSURE (same blind verifier, 2026-07-29; same-session-spawned, not a hosted external model)

Closure probe: `VERIFIER_CLOSURE_PROBE.py` (this package; runs clean, prints the
counter-computation of §C3 below).

## VERDICT: **NEW-DEFECT** (scoped to one A1-extension headline claim; everything else CLOSED)

## C1. Rerun — CLOSED
67/67, exit 0, deterministic: all three outputs byte-identical across rerun; split =
59 substantive + 8 citation guards, reported consistently in stdout, JSON,
EXACT_DERIVATION and AUDIT_REPORT. Count reconciliation verified: 53 pre-amendment
− 1 replaced (R7(b) vacuity → `PW2_R7b_noether_generic_vacuous_stratum_identities`)
+ 13 `A1_*` + 1 `A3_*` + 1 restated = 67; 8 guards relabeled `[guard]`, content
unchanged; 40 survivors byte-equal; 4 survivors (`PW2_registered_stabilizer_trivial`,
`PW3_screen_pairing_basis_unique`, `PW4_jet34_extension_is_alphabet_only`,
`PW5_verdict_nonempty_OB1`) carry added annotation text — and `PW5_verdict` a
STRENGTHENED condition — with underlying math unchanged.

## C2. A1 core and extensions (a), (b), (d) — CLOSED (independently verified)
- R7(b) restated correctly as generic-vacuity + the exact k_mod = 0 identity
  (−2k10·r_tf + m00c10 + m01c11 − m10c00 − m11c01 = 0, χ_a-graded, K₄-consistent,
  r_tr/r_sh/r_nl drop out — the r_nl-independence is a genuine strengthening);
  ledger carries the STRATUM-IDENTITY constraint rows; old r_tf = 1 witness
  correctly scoped off-stratum with its violation as a check.
- (a) Minor divisibility VERIFIED independently (own `sp.rem` in the full polynomial
  ring): exactly 36 nonzero 6×6 minors, every one divisible by (k00 − k11); the
  obstruction [L23,X](2,3) = k11 − k00 = 2k_mod confirmed. The all-member proof is
  genuine.
- (b) Gröbner confinement VERIFIED independently (own basis, grevlex over all 7
  moduli): (k00²−1)(k00−k11)(k11²−1) reduces to 0 mod the minor ideal — a genuinely
  exhaustive, fully symbolic NECESSARY-condition confinement (not sampled). Attack
  check: bare (k00−k11) is NOT in the ideal, so the resonance components are real.
- (d) New witness (r_tf, m00) = (c01c10, 2k10·c01): identity satisfied identically,
  characters correct (c01c10 = I7 trivial; k10c01 = listed χ_b generator),
  R_kmod = 2c01c10 ≢ 0 — the k_mod-determined branch stays nonempty on-stratum.
  It also vanishes on the C≠0 defect stratum of §C3 (survives the new cut).

## C3. A1 extension (c) — **NEW-DEFECT: "the ONLY genuine new cut is the k_mod = 0 identity" is REFUTED**
The auto-satisfaction COMPUTATION is correct as computed (every χ_b/χ_c generator
vanishes at C = 0), and it DOES lean on the polynomial/formal stamp (coefficient
regularity at C = 0) — the stamp travels in the check message, adequate. But the
argument covers ONLY the four NAMED C = 0 strata, while the resonance rank-drop
locus has substantial **C ≠ 0 sub-varieties** whose identities are NOT
auto-satisfied. Counter-computation (`VERIFIER_CLOSURE_PROBE.py` P3/P5):
- Solving the k00 = −1 slice of the minor ideal gives 7 solution branches, including
  {c00 = c01 = 0, c10, c11 free} and {k11 = 1, c10 = −c00k10/2, c11 = −c01k10/2}
  (fully generic C ≠ 0).
- On the stratum **{λ−k_mod = −1 (k00 = −1), c00 = c01 = 0}** (codim 3, K₄-stable)
  the pointwise nullspace is 1-dim (the mixed generator L02), tangent, with the
  exact identity **−c10·r_sh − k10·m10 = 0** (note it cuts the SHEAR slot, unlike
  the named C = 0 identities).
- The character-matched polynomial member R_c10 = c10 (a listed χ_c generator × 1)
  pairs to −c10·k10 ≢ 0 there — a GENUINE further cut, not auto-satisfied. The
  ω-shape witness (r_sh = k10) ALSO pairs to −c10·k10 ≢ 0 on this sub-stratum.
- OB1 is NOT threatened: field-sector members (e.g. R_φ = Q, all moduli components
  zero) pair to zero with every gauge direction, and the corrected trace-free
  witness vanishes on the found strata.

REQUIRED FIX (exact): (i) restate the headline everywhere it appears — correct
statement: "k_mod = 0 is the only CODIMENSION-1 genuine cut; the resonance
rank-drop locus consists of higher-codim sub-varieties, generically with C ≠ 0,
whose identities ARE further genuine cuts (counter-example stratum and identity
above); the four NAMED C = 0 strata identities are auto-satisfied in the declared
class." Occurrences: EXACT_DERIVATION §0 line ~35 hedged version OK, §2 "so the
ONLY genuine new cut…" (line ~161) NOT OK; ledger header "resonance =
auto-satisfied in the declared class"; STAGE3_HANDOFF gate-1 row "resonance
strata: auto-satisfied in the declared class"; AUDIT_REPORT line ~154; JSON
`resonance_note`, verdict statement, scope-stamp entry, and the
`A1_resonance_identities_auto_satisfied_in_class` detail string. (ii) Re-scope the
ω witness (valid ON k_mod = 0; violates the C ≠ 0 resonance identities — per-witness
stratum stamps, with a field-sector member carrying all-strata nonemptiness).
(iii) Either enumerate the full rank-drop variety (primary decomposition of the
minor ideal; the k00 = −1 slice is done in the probe) with per-branch identities,
or stamp the C ≠ 0 branches NOT-ENUMERATED **with the counter-example recorded** —
the uniqueness headline must go either way.

## C4. A2 / A3 — CLOSED
A2: the 8-guard set matches the checks I flagged (list-copy equality, trivial
arithmetic, string scans, dict compares); classification honest and conservative
(PW5_obs_EH has one real subcheck yet is classed guard); counts stated everywhere
they appear. A3: `A3_pairing_convention_isomorphic` reproduces my VE finding exactly
((4r_tr, 4r_tf, r_sh+r_nl) against δ(K+Kᵀ)); the null-slot statement now carries its
chart-δK convention note in code, prose and ledger.

## C5. STAGE3_HANDOFF — CLOSED except the C3 phrase
Gates 1/2/4 carry the strata; the no-Bianchi-TYPE warning is retained with the
correct algebraic-vs-differential distinction; §1/§2 carry the cut and the
r_tf–mixing tie. The gate-1 row's "resonance strata: auto-satisfied" inherits the
C3 defect — fix with C3(i).

## C6. CORRECTION_LAYER / AUDIT_REPORT — CLOSED with one wording nit
The did-NOT-change list is accurate in substance (OB1, alphabet, modules, slot
math, located objects, branch stamps, order-independence all indeed untouched —
verified by check-level diff). Nit: "All 52 surviving original checks — names,
math, and results byte-equivalent" — 4 of them carry added annotation text and
PW5_verdict a strengthened condition (math/results unchanged); say so. AUDIT_REPORT
represents the verifier findings faithfully (33/33, the refutation-as-stated, the
anchoring-provenance upgrade credited, A1–A3), except its line ~154 inherits the C3
phrase.

## C7. UPSTREAM_PRECISION_FLAG — ENDORSED (both edits), one consistency note
Both proposed edits are the RIGHT precision notes and correctly scoped: they fix
exactly the two class-wide-vs-per-member glosses my report flagged (Stage-1 §1.4
"mod nothing continuous"; Route B T1 registered-class bullet), leave every upstream
COMPUTATION untouched, preserve the finite-orbit/K₄-exhaustiveness distinction
(correctly noting only the INFINITESIMAL tangency jumps), and route application to
the driver as visible edits. Edit 2b's leave-the-frozen-JSON option is sensible.
Consistency note: after the C3 fix, the flag's "eigenvalue resonances λ∓k_mod ∈
{±1}" phrasing should not imply the named C = 0 strata exhaust the resonance
content (cite the corrected statement).

## Closure bottom line
A1 core adopted faithfully and extended with genuine, independently verified
mathematics (all-member minors, Gröbner confinement, named-strata identities, new
witness). One inference overreached — the same error CLASS as the original
refutation (a stratum-blind uniqueness gloss), one level down: "only genuine cut =
k_mod = 0" fails on C ≠ 0 resonance sub-varieties, counter-computation above.
Fix per C3; everything else closed. Not committed by the verifier.

---

# ROUND-2 CLOSURE (same blind verifier, 2026-07-29; same-session-spawned, not a hosted external model)

## VERDICT: **CLOSED** (two non-gating precision notes; item-6 adjudication below)

## R1. Rerun — CLOSED
75/75, exit 0 = 67 substantive + 8 citation guards; byte-identical outputs across
rerun (stdout, JSON, ledger). Accounting: 67 round-1 checks + 8 `A1R2_*`. The
`A1R2_*` block adopts my closure probe faithfully — I re-verified against my own
round-1 computations: the L02 nullspace and tangency, chart reading
(δk10, δc10) = (−c10, −k10), the shear identity −c10·r_sh − k10·m10 = 0 with all
other slots dropping out, its χ_b grading (c10·r_sh = χ_c×χ_a; k10·m10 = χ_a×χ_c;
g·L02·g = χ_b(g)·L02 — signs independently confirmed), K₄-stability of the stratum,
the R_c10 = c10 genuine-cut demonstration, the ω violation, the corrected witness's
vanishing/survival, and the concrete C ≠ 0 rank-5 point.

## R2. C3 statement installation — CLOSED
The corrected cut statement (k_mod = 0 the only CODIMENSION-1 cut; C ≠ 0
sub-varieties = further genuine cuts with the derived shear example; four named
C = 0 strata auto-satisfied; deeper stratification TYPED-NOT-EXHAUSTED) is installed
at all occurrences from my fix list: EXACT_DERIVATION §0 + §2 (R2-CORRECTED bullets),
ledger header (shear row referenced), STAGE3_HANDOFF §1 + gate rows 1/2/4,
AUDIT_REPORT, JSON (resonance content, verdict statement, scope stamps,
`A1_resonance_identities_auto_satisfied_in_class` detail R2-corrected in place).
Remaining old-phrase hits are exclusively quotations inside defect records
(AUDIT_REPORT, EXACT_DERIVATION defect narration, CORRECTION_LAYER §5, JSON F-B3
record, this report) — verified by grep.

## R3. Witness re-scoping — CLOSED
`PW5_verdict_nonempty_OB1` now carries per-witness stratum stamps AND embodies them
as strengthened conditions: sat_omega (k_mod = 0), sat_corr + surv_corr_r2 (the
corrected witness on both the k_mod = 0 stratum and the found C ≠ 0 stratum), and
the all-strata field-sector coverage (every derived stratum pairing verified
moduli-sector-only and vanishing at zero moduli components). The ω witness is
correctly demoted to k_mod = 0-only; the constant kernel stays off-k_mod = 0; the
field-sector member is the all-strata OB1 carrier. The all-strata argument is
legitimately census-independent (gauge motions act on X only on the registered
stationary presentation — with the general-arenas TYPED stamp carried).

## R4. Nit + upstream flag — CLOSED
The byte-equivalence wording is corrected to the precise 40/8/4 accounting
(CORRECTION_LAYER §4/§6). UPSTREAM_PRECISION_FLAG now phrases the resonance locus as
carrying BOTH the named C = 0 strata AND C ≠ 0 sub-varieties with further cuts, with
an explicit "do NOT exhaust the resonance content" clause in the proposed edit text —
my consistency note applied; both proposed edits remain correctly scoped (glosses
only, computations untouched) and remain ENDORSED.

## R5. Records — CLOSED
CORRECTION_LAYER §5 is a faithful round-2 record (defect, provenance with my pattern
note adopted, changes, rerun record). AUDIT_REPORT carries the two-round grade, the
C1–C7 closure record, both F-B3-class scope slips named as such, and quotes the
pattern note accurately. STAGE3_HANDOFF gate rows 1/2/4 carry the not-yet-enumerated
deeper sub-varieties with the per-candidate contact rule ("stratum contact requires
the per-branch identity computation, method recorded") — exactly the right burden
placement.

## Precision notes (non-gating; no amendment required, recommended wording)
- **N1 ("7 solution branches"):** the count is a raw sp.solve-output census of the
  k00 = −1 slice and contains nested/duplicate branches (e.g. {c00=0, k11=−1} ⊂
  {k11=−1}; {c01=0, c10=−c00k10/2, c11=0, k11=1} ⊂ {c10=−c00k10/2, c11=−c01k10/2,
  k11=1}; and the {k11=−1} branch is the k_mod = 0 intersection, not new resonance
  content) — it is NOT an irreducible-component count (that is smaller, ~4). No
  downstream claim rides on "7"; the load-bearing existence claims (the two named
  C ≠ 0 branches + the rank-5 point) are independently verified. A parenthetical
  "(raw solve-output branches, with containments; not an irreducible-component
  census)" would immunize it.
- **N2:** the "OBSERVATION (A1…)" paragraph's cross-thread note still names only the
  screen rotation; with R2 the resonance gauge directions include mixed base–screen
  boosts — harmless as written (it describes the k_mod = 0 identity only), noted for
  completeness.

## R6. Item-6 adjudication (explicit): TYPED-NOT-EXHAUSTED **IS an honest resting point for the bank** — the full deeper census is NOT required first
Grounds: (1) the codimension-1 layer is closed by an actual PROOF (the Gröbner
minor-ideal confinement — every rank-drop point lies in k_mod = 0 or the resonance
hypersurfaces), so the stamp fences a bounded, exactly-confined, measure-zero
region, not an unknown; (2) the banked verdict (OB1 + the parametrization-with-cuts)
is proven INDEPENDENT of the missing census by a stratum-blind argument (the
field-sector all-strata carrier, `A1R2_field_sector_members_carry_all_strata` — no
future stratum discovery can empty ℛ_PW); (3) the derivation method for any deeper
branch is mechanical, demonstrated on a worked example, and embodied as
zero-residual checks — and the handoff's per-candidate contact rule places the
remaining burden exactly where and when it binds (a Stage-3 candidate touching the
resonance locus must derive its branch identities); (4) this matches the program's
established honest-partial practice (jet-3/4, BR-M/BR-CE, wall depth — all banked
TYPED-NOT-EXHAUSTED). Conditions (both already in the banked text, must stay): the
stamp travels with every citation of "the parametrization", and the gate rows keep
the per-candidate stratum-contact requirement. RECOMMENDATION (not a gate): given
that BOTH defects in this package were stratum-blind glosses, the full deeper census
(primary decomposition of the minor ideal per resonance hypersurface + per-branch
nullspace/pairing — bounded, mechanical) is a natural small follow-up tile, and
should be REQUIRED before any Stage-3 candidate that actually contacts the resonance
locus is adjudicated — but banking THIS package does not wait on it.

## Round-2 bottom line
All C3 fixes installed and check-backed; my counter-computation adopted faithfully
and correctly extended (χ_b grading, K₄ consistency, per-witness stamps, all-strata
carrier); records faithful; upstream flag corrected and endorsed. CLOSED. The
four-check may proceed with the item-6 adjudication above. Not committed by the
verifier.

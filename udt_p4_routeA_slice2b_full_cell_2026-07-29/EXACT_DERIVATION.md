# P4 Route A Slice 2b — exact derivation record: full-cell generality + the branched mass legs (TE1–TE6)

Date: 2026-07-29. Branch: grok. Contract: `PREREGISTRATION.md` (frozen before this
derivation; Charles's rulings **R1** — mass = LABELED candidate-definition branches
derived-typed from banked structure only, NO branch promoted — and **R2** — moduli
bookkeeping carried BOTH ways, INTEGRATED vs POINTWISE, divergence map first-class; the
BOOTSTRAP-LENS frame governs in full). Script: `derive_routeA_slice2b.py` — **39/39
checks, exit 0 = 31 SUBSTANTIVE zero-residual exact-SymPy checks + 8 CITATION GUARDS**
(guards = definitional-unpacking / recording-table / typing rows, labeled `[guard]`
in-script and in the JSON, never counted as residual computations), deterministic (no
floats, no randomness, no network, no numeric solvers, no GPU; stdout byte-identical
across reruns — verified ×3 post-amendment), single CPU process, well under budget
(**FULL DECLARED SCOPE — no scope-ladder reduction taken**; TE4 is delivered per its own
filled-where-determined / typed-where-not clause; the TE1 obstruction statements are the
prereg's honest-boundary clause, not reductions). Outputs: `routeA_slice2b_results.json`,
`DERIVATION_STDOUT.txt`, `FULL_CELL_ATLAS_LEDGER.tsv` (20 cells), `DIVERGENCE_MAPS.tsv`
(15 rows), `NEXT_SURFACE.md`. Every check named in `monospace` below is one of the 39.

**AMENDMENT BANNER (2026-07-29, per `VERIFIER_REPORT.md` verdict
PASS-WITH-REQUIRED-AMENDMENTS; full record = `CORRECTION_LAYER.md`):** A1 — the ledger
`R2_INTEGRATED_survivors` / `R2_POINTWISE_survivors` / `tie_status` columns now carry
their in-column **QUADRATIC CLASS** stamp (the FIFTH catch of the named F-E3 scope
class); A2 — **M-GEN-eq extended EVEN-HANDEDLY to the W1 class** (weight-free a_F = 0
generator; verifier derivation adopted as `A2_W1_MGENeq_extension`; **DECISION-RELEVANT
for Charles's R1 fork**); A3 — the dispatch's unsubstantiated "self-caught dropped term"
claim on the M-DENS-coord law is **WITHDRAWN** (`CORRECTION_LAYER.md` §A3; the shipped
law itself is verifier-confirmed correct); A4 — `TE2_MWALL_P2_zero` re-coded
derivation-backed, `TE3_tie_fate_map` strengthened, dead code removed, honest split
restated (31 substantive, up from an over-counted 27). Verifier strengthenings ADOPTED
(credited): the atlas-exhaustiveness energy-ODE argument, the exact I_p sign-change
certificate, and the exact consensus-witness closed form. The pre-amendment 35 checks
all survive with their mathematics unchanged; no computed law was touched.

**Slice-2b boundary (binding, carried on every statement):** NO candidate crowned, NO mass
rule promoted or called natural/correct/physical (F-E1); NO invented mass functional or
kernel — every branch below carries its banked-provenance stamp (F-E2); every claim
carries cell + pairing + mass-branch + bookkeeping-branch + stratum + BACKGROUND stamps
(F-E3 — the NAMED class, four prior catches); no Slice-2 result quoted branch-free — the
banked tie is INTEGRATED-branch (F-E4); no R1/R2 fork or pairing supply pre-decided
(F-E5); the inherited F-D1..F-D8 travel in full (no elimination — F-D2 never engaged; R5
triples one-solution only — F-D6; no carrier — F-D7/G09; bootstrap neither imposed nor
suppressed — F-D8).

**Standing scope stamps (travel with every statement):** jet ≤ 2, registered stationary
one-parameter presentation (fields (φ, f, bh), jets p/f/h 0..2), registered positive
triangular chart, BASE arena (moduli constant; the POINTWISE column is **Charles's R2
branch read on that arena, labeled** — BR-M's moduli→fields fork stays typed
NOT-EXHAUSTED upstream and is NOT entered), enumerated pairing branches (P1-4D a_F = 2λ;
P1-triad a_F = 1+2λ; P2 a_F = 0; P3-bulkP2 / P3-bulkP1 = declared bulk + wall blocks),
READY bin only (RES-CNEQ0 CENSUS-REQUIRED; 4th-order EXTENSION-REQUIRED; carriers
G09/F-D7 out; time-live out). "Quadratic class" below = the fiberwise-quadratic p-unmixed
LE class (its exact definition in §1.2).

---

## 0. Premises (chose or derived — stamped)

| Premise | Tag |
|---|---|
| Slice-2 atlas (GEN-QUAD closed form, affine atlas, ω stratum, W3 degeneracy, A1 sign stamp, A2 legs, tie 2E0·I_p=0 INTEGRATED-branch, NV UNDETERMINED reason, M = 2ℓE0 CHOSE stamp) | DERIVED input (banked d110fe0; recomputed as consistency `S0_genquad_footing_recomputed`) |
| Stage-3 gate-cut map, pairing branches, TC3 gate-5 wall census (N=2 by-parts, parity kill, NV no-forced-slots), anchored-log iff | DERIVED input (banked 21d589c; the by-parts identity re-derived full-cell in `TE2_MWALL_theta2_and_pslot`) |
| Stage-2 ℛ_PW, k_mod = 0 identity, BR-M typed NOT-EXHAUSTED | DERIVED input (banked 2c0e7cc; identity reused in `TE4_kmod0_identity_fullcell`) |
| Stage-1 R5 same-solution rule, §1.5 pairings, J07–J11 | DERIVED input (banked) |
| Closure-identity rows ρ+S=2ρ₄ vs ρ+p_∥=2(ρ2_∥+ρ4_∥) kept SEPARATE; both G09-carrier-gated | DERIVED input (adjudication bank); typed OUT here, never instantiated (F-D7) |
| Proper-density sense (density per unit branch volume) | THEORY-cite (WR-L / Xmax / proper-density canon lineage, C-2026-07-09-1) — used as ONE labeled M-DENS sub-sense |
| Mass-branch DEFINITIONS M-GEN / M-GEN-eq / M-WALL / M-DENS-coord / M-DENS-proper | **LABELED BRANCHES (R1)** — availability DERIVED per cell from banked structure (§3.1); the p-slot selection inside M-WALL is DERIVED on the quadratic class, a LABELED sub-choice beyond it; none promoted |
| INTEGRATED vs POINTWISE moduli reading | **LABELED BRANCHES (R2)** — both carried; neither adopted |
| Mirror parity instance ε_φ = −1; f/bh parities | THEORY-cite (canon) / SUPPLIED, tagged |
| Cell half-length ℓ, anchor c_E, seat λ, retained moduli, 𝔠 | FREE explored BACKGROUND coordinates (bootstrap-lens §2a) |
| Picard uniqueness; constant-congruence diagonalization of the (f,h) block; log-monotonicity / integral positivity; **Jensen's inequality (log strictly concave)** | Category-A (cited calculus/linear algebra, named where used) |
| SymPy exact, CPU, single process | Category-A conditioning |

## 1. TE1 — full-cell generality (beyond the representatives)

### 1.1 The two cell-general theorems (arbitrary member, exact)

- **Energy first integral** (`TE1_general_energy_first_integral`): for the ARBITRARY
  generating density L̃(p0, p1, f0, f1, h0, h1) — the LE cell's whole census scope at
  jet ≤ 2 — and S = W_F L̃, the energy E := Σ_a u_a′ ∂S/∂u_a′ − S obeys
  Dx(E) = −Σ_a u_a′ E_a(S) IDENTICALLY (zero residual with L̃ an arbitrary SymPy
  Function): **every LE-cell member has the exact energy first integral** — the Slice-2
  representative structure extended to the full cell. The f/h SHIFT currents do NOT
  extend (they exist exactly on the sub-class ∂L̃/∂f0 = ∂L̃/∂h0 = 0): the general member
  has ONE guaranteed first integral, not three.
- **Determinedness dichotomy** (`TE1_general_leading_symbol_dichotomy`):
  ∂E_a/∂u_b″ = −W_F Hess_{u′}(L̃)_ab identically, and W_F > 0 (banked T0), so
  **solved-form u″ = F(u, u′) iff det Hess_{u′}(L̃) ≠ 0 — pairing-independent**; there
  (Picard, Category-A) the LOCAL solution space is EXACTLY the 6-dim initial-data
  manifold: the banked rank-6 exhaustiveness extended from the representative to EVERY
  nondegenerate-Hessian member. The degenerate stratum is POPULATED in the LE cell too
  (`TE1_degenerate_LE_instance`: L̃ = p1²/2 — f/bh rows vanish identically,
  underdetermined, the LE analog of W3).

### 1.2 The exact closed-form atlas on the fiberwise-quadratic p-unmixed class

(`TE1_quadratic_class_closed_form`) For L̃ = g_p p1²/2 + (f1,h1)·G_fh·(f1,h1)ᵀ/2
(constant g_p ≠ 0, det G_fh ≠ 0 — extends GEN-QUAD = the g_p = 1, G_fh = I instance):

    e^{a_F p0} = w(x) = A x² + w1 x + w0 ,  A = a_F² E0/(2 g_p) ,
    (f′, h′) = G_fh^{-1}(c_f, c_h)/w ,  E0 = (g_p w1²/a_F² + cᵀG_fh^{-1}c)/(2 w0) ,

zero residual in all three equations at free real a_F of both signs and arbitrary real
(g_f, g_h, g_x); E(solution) = E0 exactly. 6 parameters × retained moduli × background.

- **The atlas is EXHAUSTIVE on the class** (`ADOPTED_atlas_exhaustive_energy_ODE` —
  verifier-derived, adopted, credited): on the class the conserved TE1 energy reads
  g_p w′²/(2a_F²w) + cᵀG_fh⁻¹c/(2w) = E0, i.e. w′² = (2a_F²/g_p)(E0·w − cᵀG⁻¹c/2);
  differentiating gives 2w′(w″ − a_F²E0/g_p) = 0 identically, so **every nonconstant
  solution has w″ = a_F²E0/g_p constant — w is EXACTLY quadratic** (constants = the
  w′ ≡ 0 stratum; 6 parameters = the Picard data count). This one-line argument closes
  the quantifier gap under every "exactly/only" survivor claim below.

- **The banked emergent sign structure is DEFINITENESS-SCOPED — a full-cell finding**
  (`TE1_definiteness_scoped_sign_structure`): disc(w) = −(a_F²/g_p)·cᵀG_fh^{-1}c
  exactly. On the POSITIVE-DEFINITE sub-class (g_p > 0, G_fh ≻ 0; diagonal-positive
  instance proven, general case by constant congruence — Category-A): E0 ≥ 0 and
  disc ≤ 0 (nodeless, regular) — the banked GEN-QUAD emergence (incl. the A1 well/bump
  law) is the G = I instance and carries to the whole definite class. On the INDEFINITE
  sub-class it FAILS: `TE1_indefinite_noded_witness` (G_fh = diag(−1,1), a_F = 1:
  E0 = −2 < 0, w = 1 − x², disc = +4, nodes at x = ±1 — regular iff ℓ < 1) and
  `TE1_indefinite_E0zero_nonconstant_witness` (E0 = 0 with NONCONSTANT w = x + 2 —
  at full cell the E0 = 0 stratum is NOT just the constants). No member excluded
  (characterize, not filter).
- **Honest generality boundary** (`TE1_pmixed_and_nonquadratic_obstruction` [guard],
  stamped, not silently narrowed): p-MIXED quadratic members — the w-substitution no
  longer linearizes the p-row (weight anisotropy); non-quadratic members —
  Liouville-class, no closed form in general. The TE1 theorems (§1.1) still cover ALL
  these members exactly; what is not obtained is a closed-form atlas beyond the
  quadratic class.
- **NV cells** (`TE1_NV_fullcell_structure`): the general member is an arbitrary
  component tuple; its zero set realizes an essentially arbitrary 2nd-order system
  (universality obstruction): the determinedness dichotomy (pairing-independent) is the
  complete cell-general theorem; W1 (leading symbol W_F·Id, affine atlas) and W3
  (degenerate) recomputed as the instance legs.
- **KMOD0 at full cell** (`TE4_kmod0_identity_fullcell`): the banked stratum identity is
  a single linear relation on screen/mixing components (solvable for m00 wherever
  c10 ≠ 0 — codim-1 on the screen-carrying sub-census) and IDENTICALLY VACUOUS on the
  field-sector sub-census (r_tf = M = 0), which contains every member used in the mass
  legs: those KMOD0 atlases are the GENERIC ones at k_mod = 0, uncut — now cell-general
  on that sub-census; L23 quotient carried (banked).

## 2. R2 — the bookkeeping branches (both ways; divergence computed)

- **Inclusion** (`R2_survivor_inclusion_theorem` [guard]): POINTWISE survivors ⊆
  INTEGRATED survivors in every cell (integral of zero). Divergence = where strict.
- **Full-cell tie theorem** (`R2_general_lambda_row_aFprime_control`): for the ARBITRARY
  λ-independent LE member, ∂λ(W_F L̃) = a_F′(λ)·p0·(W_F L̃) identically — INTEGRATED row
  = a_F′ ∫p0 W_F L̃ dx, POINTWISE row = a_F′ p0 W_F L̃; both IDENTICALLY ABSENT iff
  a_F′ = 0: **the banked pairing-relativity of the background tie is FULL-CELL general,
  on both bookkeeping branches** (λ-dependent L̃: extra ∫W_F ∂λL̃ term, typed).
- **INTEGRATED survivors, quadratic class** (`R2_quadclass_integrated_survivors`):
  W_F L̃ = E0 on-shell, a_F′ = 2 (both P1 instances) ⇒ row = **2E0·I_p = 0** — the
  banked tie recovered as the (g_p, G_fh)-independent full-class law [INTEGRATED-branch,
  F-E4]. Survivors = {E0 = 0} ∪ {I_p = 0}; the massive I_p = 0 locus nonempty at every
  a_F ≠ 0 background (banked A2 + Category-A, cited — and now ALSO certified in-package
  exactly: `ADOPTED_Ip_signchange_exact`, evalf-free — I_p(c=1) = π − 4 < 0 by the
  Dalzell integral π < 22/7; I_p(c=6) = 2log(37/2) − 4 + (2/3)atan 6 > 0 by exact
  rational bounds on e; both E0 > 0; continuity gives the massive root).
- **POINTWISE survivors, quadratic class** (`R2_quadclass_pointwise_survivors`):
  2E0·p0(x) = 0 at every x forces **E0 = 0 exactly** (either directly, or p0 ≡ 0 ⇒
  w ≡ 1 ⇒ A = 0 ⇒ E0 = 0; zero residual). Survivors = {E0 = 0}: constants on the
  definite sub-class (banked sum-of-squares); PLUS nonconstant affine-w members on the
  indefinite sub-class (§1.2 witness). **The massive integrated locus {I_p = 0, E0 ≠ 0}
  does NOT survive pointwise: the inclusion is STRICT on P1-side LE cells.**
- **Convergence rows** (`R2_omega_convergence_P2_vacuity`): ω's k10-row — both branches
  force exactly {k10 = 0} (agree); P2-side λ-row — identically zero both ways (agree,
  vacuous, reported); NV reps — zero moduli slots, both vacuous (general NV: inclusion
  holds, strictness member-dependent, typed).

## 3. TE2 — the branched mass legs (R1)

### 3.1 Availability, derived-typed (per cell; `TE2_mass_branch_availability_table` [guard])

| Branch | Provenance (banked) | LE cells | NV cells |
|---|---|---|---|
| **M-GEN** | the TE1 first integral (= the Slice-2 CHOSE instantiation, now labeled) | AVAILABLE: M-GEN = 2ℓE for EVERY member (`TE2_MGEN_general_value`) | NOT AVAILABLE (defect obstructs generator — re-derived) |
| **M-GEN-eq** (labeled sub-branch) | the TUPLE'S OWN autonomy first integral, where the tuple coincides with a generated tuple of the ENUMERATED weight menu (banked tuple identities; **A2**: the earlier anchored-only restriction had no stated derivation and is removed — even-handed) | (coincides with M-GEN) | AVAILABLE for W2-fs-class (anchored a_F = 2λ generator) **AND — A2 — for W1-class** (weight-free a_F = 0 generator: W1 = Euler(−L̃0) exactly, `A2_W1_MGENeq_extension`; M = ±2ℓL̃0, orientation-sign labeled; **DECISION-RELEVANT-R1**); NOT for W3 (no generated-tuple identity in banked structure — a refusal, not an invented discriminator) |
| **M-WALL** | TC3 gate-5 N=2 by-parts census; the identity re-derived at ARBITRARY member (`TE2_MWALL_theta2_and_pslot`) | AVAILABLE: [π_p] across the cell; on the quadratic class the p-slot is the ONLY nonvacuous wall-difference slot (π_f, π_h conserved — DERIVED, not chosen); beyond, p-slot = labeled sub-choice. Canon-parity caveat: the v_p SLOT is parity-killed, so M-WALL is a TRACE functional there, not a paired boundary charge (stamped) | = member's OWN declared R_wall: banked reps declare zero ⇒ M-WALL = 0 (trivially determined — an artifact of the declaration, stamped); nonzero-wall NV members typed OPEN |
| **M-DENS-coord / M-DENS-proper** | R5 triple's V (branch volume, THEORY) + the two banked density senses (registered-chart E0dens vs proper per-branch-volume, WR-L lineage) — kept separate | AVAILABLE (E0dens derived) | NOT AVAILABLE (no derived density) |
| carrier closure rows ρ+S=2ρ₄ / ρ+p_∥ | adjudication bank | **G09-carrier-gated: typed OUT, kept separate, never merged** | same |

### 3.2 Values and laws (quadratic class; every row branch-labeled)

- **M-GEN = 2ℓE** for every LE member (E constant on-shell — full generality); = 2ℓE0 on
  the quadratic class. NOT sign-definite at full cell (definiteness-scoped; E0 = −2
  witness).
- **M-WALL = [π_p] = 2a_F ℓE0 = a_F · M-GEN** exactly on the whole quadratic class
  (g_p and G_fh cancel) (`TE2_MWALL_theta2_and_pslot`); at a_F = 0 (P2 side)
  **M-WALL ≡ 0 on the affine atlas while M-GEN = 2ℓE0 is free** (`TE2_MWALL_P2_zero` —
  A4: now DERIVATION-BACKED, the affine atlas u″ = 0 forced by the a_F = 0 Euler rows
  themselves; the verifier's derivation adopted, replacing a tautological coding).
- **M-DENS-proper ≡ M-GEN identically** — ∫(E0dens/W_F)·W_F dx = ∫E0dens dx: the
  proper-density sense REPRODUCES the generated-energy branch exactly — **the
  cross-branch calibration observation** (`TE2_MDENS_proper_calibration`).
- **M-DENS-coord = E0·V**, and **M-DENS-coord − M-GEN = E0·(V − 2ℓ)** exactly, with
  V − 2ℓ = (2/3)Aℓ³ + 2(w0 − 1)ℓ (`TE2_MDENS_coord_divergence`): zero iff E0 = 0 or
  V = 2ℓ (a SOLUTION locus; on the P2 side V = 2ℓ identically — agreement). On the
  integrated tie locus {I_p = 0, E0 > 0, nonconstant}: ∫log w = 0 ⇒ V > 2ℓ STRICTLY
  (Jensen, named Category-A) — the coord sense strictly exceeds M-GEN on every massive
  self-consistent definite member.
- **NV re-grade per branch** (`TE2_NV_regrade_per_branch` + `A2_W1_MGENeq_extension`):
  W1-class (P1-side NV) — M-GEN proper STILL-UNDETERMINED (the Helmholtz defect
  obstructs a generator under the cell's own anchored pairing, re-derived; p1, f1, h1
  each conserved), **DETERMINED-under-M-GEN-eq (A2, even-handed with the W2-fs grant):
  the W1 tuple IS the weight-free a_F = 0 generated tuple Euler(−L̃0) exactly (banked
  identity), its energy −L̃0 is conserved on the affine atlas, generator unique up to
  null Lagrangians (energy-neutral, zero residual) — M = ±2ℓL̃0, sign per tuple
  orientation (labeled sub-choice); the member stays NV under P1 (stamped); flagged
  DECISION-RELEVANT-R1** — the earlier refusal reason ("conserved 1-jets exist but none
  structure-selected") undercounted banked structure: the a_F = 0 generator IS the
  selector, exactly parallel to W2-fs's a_F = 2λ generator (verifier catch, A2);
  M-WALL DETERMINED = 0 (trivial), M-DENS STILL-UNDETERMINED.
  W2-fs-class (P2-side NV) — DETERMINED-under-**M-GEN-eq**:
  M = 2ℓE0 on the quadratic-w atlas (tuple-autonomy first integral, banked provenance;
  the member stays NV under P2 — stamped), M-WALL = 0, M-DENS STILL-UNDETERMINED. W3 —
  M-WALL = 0; rest undetermined. Each verdict branch-labeled; none promoted.
- **R5 triples re-run per branch on ONE solution** (`TE2_R5_triples_rerun`, F-D6):
  closure ρV = M exact in every branch; M-WALL's ρ is NEGATIVE for a_F < 0 on definite
  members (branch-labeled); NV under M-WALL: (V, 0, 0), closure trivial.

## 4. TE3 — the three divergence maps (deliverable: `DIVERGENCE_MAPS.tsv`, 15 rows)

**(a) Mass-branch map** (`TE3_massbranch_divergence_map`, `TE3_sign_divergence_aFneg`,
`TE3_allfour_agreement_witness`): M-DENS-proper ≡ M-GEN (agreement everywhere — the
calibration); M-WALL − M-GEN = 2ℓE0(a_F − 1) — agreement exactly on {E0 = 0} ∪
{a_F = 1} (a BACKGROUND locus: P1-4D λ = 1/2, P1-triad λ = 0); M-DENS-coord − M-GEN =
E0(V − 2ℓ) — agreement on {E0 = 0} ∪ {V = 2ℓ}; P2 side: M-WALL ≡ 0 (maximal divergence)
while both M-DENS senses agree with M-GEN. SIGN: on the definite bump side (a_F < 0, A1
stamp) M-WALL ≤ 0 ≤ M-GEN — the wall reading assigns negative mass to every definite
bump-side member with E0 > 0. ALL-FOUR agreement locus = {E0 = 0} ∪ ({a_F = 1} ∩
{V = 2ℓ}): a **nonzero-mass consensus point EXISTS** — exact witness w = (3/2)x² + 1/2
at a_F = 1, ℓ = 1 with E0 = 3 and all four readings = 6 — but it lies OFF the integrated
moduli-row survivor set (Jensen strict ⇒ I_p < 0 there; now ALSO by exact quadrature:
**I_p(witness) = −4 + log 4 + 4√3π/9 exactly, certified < 0** by an exact rational chain
— `ADOPTED_consensus_Ip_closed_form`, verifier-derived, adopted, credited) and off the
pointwise one (E0 = 3 ≠ 0): OE3-flavored observation, NOT a promotion.

**(b) Bookkeeping map** (`TE3_bookkeeping_divergence_map` [guard]): STRICT on P1-side LE
cells — the fork decides whether ANY massive self-consistent member exists (under every
mass branch); agreement on ω-rows, P2-side rows, zero-moduli NV reps; general NV typed.

**(c) Tie fate** (`TE3_tie_fate_map` — A4-strengthened: mass-zero solves under the
declared assumptions + zero-residual nonzero-factor rewrites of the row through each
branch mass; bootstrap observation only, per lens):
INTEGRATED × every mass branch — the tie reads (branch mass)·I_p = 0 up to nonzero
factors; its zero locus is MASS-BRANCH-ROBUST (each of the four masses vanishes iff
E0 = 0), and its nontrivial branch {I_p = 0, E0 ≠ 0} carries NONZERO mass under all four
readings simultaneously: **the bootstrap-shaped tie couples MASS ITSELF to the background
seat, whichever labeled definition is used.** POINTWISE × every mass branch — the analog
forces E0 = 0: every pointwise survivor is MASSLESS under all four readings; the tie's
massive branch exists ONLY on the INTEGRATED side (the banked F-E4 stamp made
structural). P2 side (a_F′ = 0) — no tie, no analog, either branch (full-cell general by
§2). Settling is Charles's.

## 5. TE4 — wall/corner/completion structure (filled vs typed)

- **FILLED** (the solutions determine it): wall traces in exact closed form (w, w′, atan
  f/h traces; canon-parity witness re-cut at the g = I point) —
  `TE4_wall_traces_and_parity`; **J09** — the node/type-changing locus = the real-root
  set of w: vacuous on the definite class (disc < 0), explicit node radii
  x = (−w1 ± √disc)/(2A) with the per-member exclusion statement at disc > 0 —
  `TE4_J09_node_locus`; the KMOD0 identity structure (§1.2, cell-general on the
  field-sector census).
- **TYPED** (`TE4_completion_typing_record` [guard]): J07/J11 transition data
  NEEDS-TRANSITION-DATA (no chart overlap in the one-parameter presentation; F-S7 flag
  inherited); J08/L4 — components 𝔠-free, completion enters only via gate-6 periods,
  NEEDS-COMPLETION-DATA, **L4 carried both ways**; J10 — banked equivariance + L23
  quotient carried; corners TYPED-ONLY (codim-2); P3 wall blocks — the varied-fork cut
  COUNT per parity-surviving slot is determined (canon ε_φ = −1 kills the v_p slot), the
  cut LOCUS needs the free (unenumerated) wall-density data: typed OPEN at the DATA
  level, not the structure level.

## 6. TE5 — the composite map

`FULL_CELL_ATLAS_LEDGER.tsv`: 20 READY composite cells (5 branches × {GENERIC, KMOD0} ×
{LE, NV}) × (full-cell solution structure + obstruction, four labeled mass columns, both
R2 survivor columns, tie status, TE4 wall/completion, background stamps)
(`TE5_ledgers_written` [guard]). The pairing × mass-branch × bookkeeping-branch ×
background crossing is carried inside the columns (the mass functionals are
R2-independent; their SURVIVOR domains are not — stamped per column).

## 7. Outcome and falsifier record (derivation-side)

**Outcome class: OE1** — the composite map populated across all branch combinations; no
cell emptied (OE2 not triggered — no elimination, F-D2 never engaged); OE3-FLAVORED
convergence rows recorded INSIDE the map as observations (M-DENS-proper ≡ M-GEN
calibration; ω-row R2 agreement; the all-four nonzero-mass consensus witness at
{a_F = 1, V = 2ℓ} — off both R2 survivor sets), none promoted; no structural
inconsistency inside any branch combination (OE4 not triggered).

- **F-E1 clean** — every mass number/law above carries its branch label; the
  disagreements are mapped, none resolved; no branch called natural/correct/physical
  (verifier-hunted, clean; the A2 extension adds a labeled sub-branch verdict, not a
  promotion).
- **F-E2 clean** — five labeled definitions, each with a banked-provenance stamp
  (§3.1); the Tonti/integrating-factor door stayed shut. **A2 adjudication:** the
  original W1 refusal was itself F-E2-respecting, but ASYMMETRIC — the availability
  table's anchored-only restriction had no stated derivation while W1 satisfies the
  SAME banked principle that granted W2-fs; fixed even-handedly by EXTENDING (nothing
  invented: the weight-free generator is banked structure), not by inventing a
  discriminator.
- **F-E3: ONE catch fired post-derivation — the FIFTH of the named scope class —
  and is cured (A1).** The ledger's `R2_INTEGRATED_survivors` / `R2_POINTWISE_survivors`
  / `tie_status` columns stated quadratic-class characterizations WITHOUT the in-column
  "quadratic class" stamp — read cell-generally they were FALSE (the general member's
  λ-row is a_F′∫p0·W_F L̃ dx, survivors uncharacterized). Prose and DIVERGENCE_MAPS
  carried the stamp; the ledger columns now do too, plus the beyond-class row form and
  UNCHARACTERIZED typing. Caught by the verifier's pre-registered first hunt (the
  mechanism worked a fifth time). All other exactly/only/all/none/robust claims carry
  their stamps (verifier-audited).
- **F-E4 clean** — the tie is quoted INTEGRATED-branch throughout; its pointwise analog
  is computed, not conflated.
- **F-E5 clean** — R1/R2 forks and the pairing supply left open; the branch-collapse
  items are QUESTIONS in `NEXT_SURFACE.md`.
- **F-D1..F-D8 clean** — no crowning; no elimination; banked facts recomputed as
  consistency only (one banked-claim REFINEMENT, not a contradiction: the Slice-2
  emergent E0 ≥ 0 / nodelessness was rep-scoped by its own stamp, and is here shown
  DEFINITENESS-scoped at full cell — the banked stamp did its job); every R5 triple on
  one solution; no carrier (closure-identity rows typed OUT); self-consistent loci
  computed and reported per branch or reported undetermined with the reason.
- **F-D5 none** — 39/39, exit 0; deterministic rerun byte-identical ×3 (post-amendment).
- **Amendment/process record (A3, A4):** the derivation dispatch claimed a self-caught
  dropped term in the M-DENS-coord law; NO package record substantiates it; the shipped
  law is verifier-confirmed correct — the unsubstantiated claim is WITHDRAWN
  (`CORRECTION_LAYER.md` §A3, a dispatch-vs-record process defect, logged). A4: two
  checks were thinner than their "substantive" tag (one tautological, one near-trivial);
  both are now genuinely computed and the honest split is restated (31 substantive +
  8 guards).

**Limits that travel:** (i) the closed-form atlas is exact on the fiberwise-quadratic
p-unmixed class; beyond it the full-cell content is the two TE1 theorems + obstruction
statements (honest boundary, stamped); (ii) all statements at jet ≤ 2, BASE arena,
stationary presentation, enumerated branches, READY bin; (iii) the POINTWISE column is
Charles's R2 branch on the BASE arena — BR-M's field fork stays NOT-EXHAUSTED; (iv) the
M-WALL p-slot selection is derived only on the quadratic class (labeled sub-choice
beyond); the canon-parity trace-functional caveat travels; (v) named Category-A steps:
Picard, constant congruence, log-monotonicity/integral positivity (banked A2 reuse), and
Jensen (strict concavity of log) in the V > 2ℓ leg (the consensus-witness off-survivor
stamp no longer rides Jensen alone — exact quadrature certificate in-package); (vi) the
banked A2 nonemptiness of the I_p = 0 locus is cited where used AND now certified
in-package at the a_F = 1 background (`ADOPTED_Ip_signchange_exact`; the general-
background claim still rides banked A2); (vii) NV masses: determinations are
trivial-zero (M-WALL, zero-declared walls) or sub-branch-labeled (M-GEN-eq — now BOTH
witness classes, W2-fs = 2ℓE0 and W1 = ±2ℓL̃0 orientation-labeled, A2); nonzero-wall NV
members, P3 wall-density data, resonance cells, 4th-order class, carriers, time-live:
untouched (typed); (viii) the ledger R2-survivor and tie-status columns are QUADRATIC-
CLASS-scoped in-column (A1) — beyond the class the λ-row is a_F′∫p0·W_F L̃ dx and the
survivor sets are UNCHARACTERIZED (typed, honest boundary); (ix) the M-GEN-eq(W1) sign
is a labeled orientation sub-choice (±W1, same zero set), and the additive-constant
normalization convention is shared with the W2-fs grant (labeled, even-handed) — whether
M-GEN-eq enters the R1 menu at all is Charles's call (DECISION-RELEVANT-R1).

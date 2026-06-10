# mass_emergence_canonical_geometry.md

> **⚠ STATUS: RE-AUDIT IN PROGRESS — NOT CANONICAL until complete.** This document re-derives the UDT
> matter/mass-emergence sector from the ground up, with **nothing taken as given** (the session-5
> paradigm shift is large enough that ALL prior work — including CG's matter section and every session-5
> landing — is suspect until re-graded here). It does NOT edit `udt_canonical_geometry.md` (CG stays
> intact). If this re-audit survives, it may supersede CG's matter section later with Charles's sign-off;
> if it does not, it documents exactly why. **Goal: determine whether the hadron/mass sector was arrived
> at honestly or is built on sand — strengthen OR disprove, slowly and methodically, piece by piece.**
> Started 2026-06-07 (session-5 close).
>
> **★ STATUS (session-6 close): §0–§4 FIRST-PASS GRADED — verdict: NO unfittable quantitative prediction
> survives (floor fitted; skeleton real ALGEBRA but physics-identification conditional; charges/masses
> labels/dense-fits; no assembly mechanism; no spectrum prediction). §5 (pion RPA) = NOT STARTED.** This doc
> is now the **GUIDING DOC for the rebuild** (`UDT_REBUILD.md`, Parts A–F): all new rebuild work is graded
> AGAINST these §0–§4 verdicts, NOT against CG's "parameter-free"/"DERIVED" labels (a session-6 drift Charles
> caught — the corpus's "parameter-free" = free of φ₀/μ/r* only; masses still ride the Fock import + dense fits).
>
> **★ STATUS (session-7 close, 2026-06-08): the §0–§4 grades STAND (no change). Session-7 work lives in
> `UDT_REBUILD.md` Parts G–J and REINFORCES this doc's verdict, it does not soften it:** (a) A & B BANKED as
> postulates — all algebraic derive-B routes CLOSED (Part G/H); (b) the **§10.5 two-sector seam RESOLVED
> structurally** — one definitional positional-dilation geometry across macro+micro, matter = the exact φ→−φ
> *inside-out* region (Parts I/J, verified); (c) **mass emergence**: a *scaffold-free* spinor-binding mechanism
> exists (free-magnitude inside-out pocket, NO floor, NO wall, smooth onset) — but it does **NOT pin any mass**
> (lepton ratios not reproduced; Koide Q≈1/3 not 2/3; φ-depth ladder = right exponential mechanism, unpinned
> spacings) → **CONSISTENT with "no unfittable prediction survives"; the masses stay parameterized.** §5 (pion
> RPA) still NOT STARTED. The CALIBRATED STATUS (unification = structural/verified; mass-origin = NOT established)
> is recorded in UDT_REBUILD Part J. New derive-B lead: a TOPOLOGICAL/index route (gut, not started).

## ★ SELF-HARDENING PROTOCOL (BINDING — re-read in full before EVERY edit, every session)
This document is engineered to get HARDER to satisfy over time, never softer. The failure mode it exists
to prevent is multi-session drift: grades quietly inflating, caveats eroding, the optimistic narrative
creeping back. The following are INVARIANTS, not suggestions. A session that violates them is corrupting
the record; a later session that spots a violation MUST repair it.

1. **NOTHING IS EVER "GIVEN".** No claim, parameter, or prior result is exempt from grading — including
   ones an earlier session (or CG) marked [DERIVED]. If asked to justify a [DERIVED] and you cannot
   re-derive it here and now, DOWNGRADE it. "It was settled before" is not a defense. (But re-derivation is
   EVENT-TRIGGERED, not a per-session ritual — see §9; valid recorded provenance stands until challenged.)
2. **THE RATCHET (burden of proof is always on the UPGRADE).** A grade may move DOWN (toward [ASSERTION])
   freely, no ceremony. A grade may move UP (toward [DERIVED]) ONLY if, in the SAME edit, you append on the
   line: (a) the explicit derivation/audit justifying it, (b) a recorded blind adversarial-verifier pass
   (date + agent id + verdict), (c) which of the 7 audits it cleared. **A bare upgrade with no recorded
   evidence is FORBIDDEN; any session seeing one MUST downgrade it on sight.**
3. **[DERIVED] IS RARE AND SACRED.** It requires ALL of: follows from metric+axioms, zero free input,
   survived all 7 audits, verifier-confirmed, provenance on the line. Missing any one ⇒ it is NOT [DERIVED].
   **When in doubt, it is [ASSERTION].**
4. **NEGATIVES ARE APPEND-ONLY.** Recorded caveats, null-test results, "ruled out", and failure reasons are
   NEVER deleted or softened. They may only be (a) added to, or (b) explicitly retracted WITH a recorded
   reason + verifier — the retraction itself logged in the CHANGELOG, never silent. A caveat that vanished
   without a logged retraction is tampering; RESTORE it from git history.
5. **NO NARRATIVE / NO COMPRESSION.** Banned verbatim anywhere in this doc: "reduces to a single X",
   "this unifies", "everything rests on", "the one thing", "the key to", and kin. Claims + grades +
   provenance only. Any synthesis is written ONCE, LAST, only if earned, and is itself graded.
6. **EVERY EDIT LOGS.** Append to the CHANGELOG (bottom): date / session / section / what changed /
   grade before→after / evidence. Git diff + this log make any weakening conspicuous and reversible.
7. **CANONIZATION IS CHARLES'S CALL ALONE.** No instance may remove the "NOT CANONICAL" header, declare a
   section "done", or promote this doc. Only Charles does that.
8. **WHEN UNSURE, HARDEN.** Every ambiguity resolves toward the more skeptical grade, the preserved caveat,
   the re-derivation. Err toward disproof, never toward belief.
9. **BOUNDED COST — harder to FOOL, not harder to USE (re-derivation is EVENT-TRIGGERED, not periodic).**
   A grade once recorded WITH valid evidence on the line (derivation + verifier + audits) is the durable
   result: it STANDS and is NOT re-proven each session. Re-derive a standing [DERIVED] ONLY when (a) it is
   specifically challenged, (b) a claim it depends on is downgraded/changed (propagate the cascade — bounded
   by the dependency graph, a one-time cost when a foundation moves, not recurring), or (c) you are about to
   build directly on it. Per-claim work is paid ONCE; the doc grows linearly; per-session effort stays bounded
   to the CURRENT frontier section + a cheap re-read of this protocol. (No loophole: §9 exempts only claims
   that ALREADY meet §2/§3 with recorded evidence — missing/invalid provenance still forces downgrade.)

## Grading vocabulary (every load-bearing claim carries one or a combination, INLINE)
- **[DERIVED]** — follows from the metric + the two axioms with no free input, AND has survived all 7
  audits below, AND is verifier-confirmed with provenance ON THE LINE (Self-Hardening Protocol §2–§3).
  The only tag that means "real"; rare and sacred; never asserted, only earned.
- **[INPUT]** — an honest external given, named as such (e.g. the electron-mass anchor mₑ).
- **[ANSATZ]** — a posited form/assignment not yet derived. Each must be ELIMINATED or PROVEN NECESSARY
  (subject to modification if a serious blocker appears).
- **[ASSERTION]** — claimed without derivation OR check. These are the primary hunt; must be resolved.
- **[FITTED]** — tuned to data / a convention chosen to match (e.g. possibly C, r*).
- **[IMPORT]** — SM/QFT/nuclear scaffolding used as a crutch (judged by UDT's own axioms, not SM norms).

Deliverable per piece + overall: **what fraction of the LOAD-BEARING claims survive as [DERIVED] vs
collapse to [ASSERTION]/[FITTED]/[IMPORT]?**

## The 7 audits (applied to EVERY section before it is allowed to stand)
1. Non-UDT imports of all kinds, at all levels.
2. Linearization / approximation (controlled? quantified? or hidden?).
3. Missing functions the metric produces (what was omitted that the metric actually gives?).
4. Other-sector inclusion (UDT Maxwell §11, breathing/scalar, spin connection, §19.9.8 exchange, …).
5. What does the metric itself SAY about how to construct this (vs an imposed SM picture)?
6. Math errors (independently recompute).
7. Potential for different models (was the chosen construction the only one, or one of many?).

## Ground rules (agreed session-5)
- Foundation-UP, ONE section fully graded before the next; no advancing on an ungraded floor.
- The CG matter-section copy (when imported as structure) is **structure-only**: every copied line starts
  UNGRADED and must earn its tag; nothing preserved as true because CG says so.
- The document IS the audit vehicle; prior landings are SOURCE/PROVENANCE, re-graded & superseded here as
  each section is written (no second pass, no new pile of landings).
- **NO synthesis / narrative / "this unifies" / "rests on a single X" sections** until the very end — and
  only if earned. Graded claims + provenance only. (Guard against the session-5 narrative-compression bug.)
- Run a blind adversarial verifier on each section's closure (esp. anything graded [DERIVED]).

---

## SECTION PLAN (foundation-up) — §0–§4 FIRST-PASS GRADED (session-6); (5) pion NOT STARTED (deferred build)

### (0) Parameters and the scale C — *the floor; audit first, try to BREAK it*
Scope: φ₀=−cos(π/5), μ²=π/3, r*=6.9875, the calibration C=4π²mₑr*, the vacuum ODE (J'=r²μ²φ, φ'=Je^{2φ}/r²),
the Form-T Dirac operator, and the Diophantine selection (j=½, ℓ=1, |κ_max|=3). Central question: are these
a-priori, or fitted/circular? (Known red flag to confront head-on: the corpus's own audits call C/r*=4π²mₑ
a "free convention" and r*=7−1/80 "defined from source=1/4, circular" — LANDING_D-ANCHOR-4-UNIFY-1,
CONSILIENCE_AUDIT, RETRACTION_third_axiom_irreducible, SESSION_CONSOLIDATED_EDITS.) If the scale is [FITTED],
say so plainly and trace what downstream is absolute vs ratio/structural.
STATUS: **FIRST-PASS GRADED (session-6, 2026-06-07). NOT canonical** (per Protocol §7 only Charles canonizes).

**Closure result: 0 of the 4 floor parameters reach [DERIVED].** Each reaches its *value* only via an asserted
step, a chosen boundary condition, a target-tuned definition, or an external input + convention. Verified by a
blind adversarial verifier instructed to DEFEND all four as hard as possible (Agent `ae094fea6c5b24c13`,
2026-06-07): it independently confirmed every downgrade below with file:line evidence and overturned none, adding
corroboration (⟨G⟩=2/π=0.637 ≠ cos(π/5)=0.809 numerically; a second conflicting calibration C=3m_π/(2√2);
C exact only to 1.5%). Cleared audits 1–7 on the closure (no import smuggled into the *downgrades*; recomputed
the sphere integral and the |φ₀|-cancellation independently).

**The four load-bearing parameters:**
- **φ₀ = −cos(π/5) = −0.809 — [INPUT]+[FITTED].** It is a *boundary condition*, not a derived value: the metric's
  exact vacuum classification (CG §8.1.5, line 816) admits EVERY φ₀<0 (global monotone vacuum), and the emergence
  scan confirms Dirac modes exist at all negative φ₀ (CG:2436). Nothing in metric+axioms selects −0.809. Three
  *competing* justifications are offered for the value (the tell of a number seeking a home): (a) "⟨G⟩=2/π
  (geometric)" (CG:2285/2814) — but 2/π=0.637 ≠ cos(π/5)=0.809, so this is asserted not computed; (b) pentagon /
  φ_gold/2 via the Diophantine triple (CG:1898/2835) — a clean-form tie, conditional on |κmax|=3 (deferred to §1);
  (c) the value alone reproduces the meson eigenvalue-ratio spread 1:5.6:7.3:8.9 (CG:2436) — an explicit FIT to the
  physical meson spectrum. CG itself reframes φ₀ down to "the central-depth boundary condition … not a dynamical
  attractor" (CG:2436). cos(π/5) is a clean-form re-encoding of ~0.809; not forced.
- **μ² = π/3 — [ASSERTION]** (contains a [DERIVED] sub-fact). ⟨cos²θ⟩_S² = 1/3 IS a genuine parameter-free sphere
  integral [DERIVED] (CG:2191; = Vol(B³)/Area(S²)). But the load-bearing step μ² = π × ⟨cos²θ⟩ — multiplying by π,
  named "the angular half-period" — is **asserted, never derived from the scalar action S_φ**: it appears only at
  CG:2195, with no Klein-Gordon/action derivation anywhere in the document (verifier searched the whole file). And
  the value is data-validated: CG:2201 — "at this value, all meson eigenvalue ratios are within 1.8% … vs 55%
  failures at the old fitted μ=1.020." 4μ²=4π/3=Vol(B³) (CG:2199) is a consistency identity, not the derivation
  (CONSILIENCE_AUDIT:107). So: real sphere integral, asserted ×π closure, checked against meson ratios.
- **r* = 6.9875 = 7 − 1/80 — [FITTED]/CIRCULAR.** Defined as the domain size where the Dirac ground state hits
  E₁ = 2√2/3 (CG:2185). CG admits the circularity: "E₁ = 2√2/3 is **exact by construction**: r* is defined as the
  domain size that realizes this algebraic value … a **tuned-to-target identity, not an independent prediction**"
  (CG:2831). The "7−1/80" closed form is itself circular — the correction Δr* = (E₁^alg−E₁(7))/|dE₁/dr*| has |φ₀|
  in numerator and denominator and cancels trivially to source²/5 (CG:2851–2855); CONSILIENCE_AUDIT:134 calls it
  "defined from source=1/4 (circular)." And it is **anchor-dependent**: proton-anchoring gives r*=7.042 (CG §17.3,
  line 2863), not 6.9875. The closure integer 7=2|κmax|+1 is structural (conditional on |κmax|=3, deferred to §1);
  the 1/80 correction is a fit to the chosen target eigenvalue.
- **C = 4π²·mₑ·r* — [INPUT]+[FITTED].** mₑ is an explicit external mass anchor (CG:21, "Sets the absolute scale").
  An absolute MeV scale cannot come from dimensionless metric+axioms without one dimensionful import — so an [INPUT]
  here is structurally unavoidable and honest. The "4π²" prefactor is a **free convention**: LANDING_D-ANCHOR-4-UNIFY-1:25,38
  — "chosen prefactor … a free convention absorbing the mismatch" between the genuine structural angular coefficient
  (2/3, target-blind) and the formula's anchor value (1/4); the three "4"s do NOT share an operator-level origin
  (numerical coincidence at the cherry-picked triple). Not even exact: C/r*=4π²mₑ holds to 1.5% (CG:2513), and a
  *different* C=3m_π/(2√2) is carried from pion-anchoring (CG:2511).

**[DERIVED] sub-facts that survive (the real, partial, mostly-dimensionless content underneath the fitted values):**
- **⟨cos²θ⟩_S² = 1/3** [DERIVED] — sphere integral, metric's angular part (CG:2191; recomputed by verifier).
- **Vacuum classification by sign(φ₀)** [DERIVED] — φ₀<0 ⟹ global, monotone, never re-enters φ>0 (CG §8.1.5
  theorem, line 816). Real, but selects a *branch*, not a value.
- **source(κ=−1) = ∫(G²−F²)e^{2φ}r²dr ≈ 0.250 ± 0.001, CV~1e-4 across μ∈[0.95,1.10]** [DERIVED] as a *stable
  eigenfunction integral* (CG:2802) — genuinely the corpus's most robust structural number. But "= exactly 1/4"
  is a [FITTED] clean-form rounding (measured 0.2503–0.2514, slightly above 1/4) and is weight-dependent
  (CONSILIENCE_AUDIT: "spans 0.06–17 over weights").
- **r*/r_b ≈ φ_gold** (1.616 vs 1.618, 0.09–0.12%, CV 0.003) [DERIVED] as a *stable dimensionless ratio* (CG:2806);
  the "= φ_gold exactly" is a 0.1% match, not an identity.

**Downstream trace (absolute vs ratio/structural) — the §0 deliverable:** the entire ABSOLUTE MeV scale rides on
C, which is [INPUT]+[FITTED]; therefore EVERY absolute mass in the framework is scale-fitted (carries mₑ + the 4π²
convention) and cannot be a zero-free-input prediction. What can still be real is **dimensionless / ratio /
structural** content: stable eigenfunction integrals (source≈1/4), stable ratios (r*/r_b≈φ_gold), sphere integrals
(⟨cos²θ⟩=1/3), and parameter-free mass *ratios* (6π⁵, 20π³/3 — flagged separately by the banked dense-(rational)·π^odd
rule; graded in §2/§4, not here). **The floor does NOT stand as derived; it stands as one honest input (mₑ) + a
fitted scale (C, r*) + a fitted/asserted shape (φ₀, μ²), with a thin layer of genuinely structural dimensionless
facts underneath.** This is the foundation every later section inherits; sections (1)–(5) must be read as conditional
on a FITTED absolute scale.

### (1) The quark REPRESENTATION skeleton
Scope: the 6 κ-channels, the parity-block split {−1,+2,−3}/{+1,−2,+3}, su(3) rep (3⊕5; the Casimir-4/3
framing already flagged vacuous), color=m_ℓ / N_c=2ℓ+1, the ε_abc singlet, the bridge values B₁=1/18,B₃=1/8.
Re-audit the "genuine/unfittable" claim against all 7.
STATUS: **FIRST-PASS GRADED (session-6, 2026-06-07). NOT canonical** (Protocol §7).

**Closure result: §1 is the first section with genuine [DERIVED] content — but ONLY the dimensionless
representation theory, and ALL of the *physical* quark identification is conditional on one [ANSATZ]
(rank-2) + one [INPUT] (j=½).** I re-verified every structural claim independently with
`da_reaudit_s1_skeleton.py` (6 tests, all pass, random-matrix controls included), NOT trusting the prior
landing. Closure cross-checked by a blind adversarial verifier instructed to attack the [DERIVED] grades
AND to defend rank-2 as forced (Agent `a4fe441624990c66d`, 2026-06-07): it confirmed all four grades with
no over/under-grading, and strengthened two of them (below). Audits 1–7 applied; the pivotal ones are
#5 (what the metric says), #7 (was this the only construction?), #1 (imports).

**[DERIVED] — pure SO(3)/su(3) representation theory of the ℓ=1 (3-dim) operator space (no SM import,
recomputed from scratch):**
- **8 = (2ℓ+1)²−1 = 3⊕5 only at ℓ=1.** The traceless operators on the 3-dim ℓ=1 multiplet form su(3),
  decomposing under SO(3) as rank-1(3)⊕rank-2(5), with cross-rank trace-orthogonality Tr(T⁽¹⁾T⁽²⁾)=0
  exact, and the span filling all 8 generators. 8=3+5 holds ONLY at ℓ=1 (ℓ=2→24, ℓ=3→48). [DERIVED]
  (da_reaudit_s1_skeleton.py TEST 2; verifier rebuilt independently, rank 8, max cross-rank trace 0).
  *This is the honest statement of "the su(3)" — it is the operator algebra on ℂ³, NOT "QCD color"
  (see labels below).*
- **ε_abc color-singlet, multiplicity 1, and N=3-specific.** Exactly one totally-antisymmetric SO(3)
  singlet in 1⊗1⊗1 (three ℓ=1), = ε_abc (J²=0 to 1e-16); and V⊗V⊗V has a totally-antisymmetric singlet
  iff dim Λ³V = C(N,3) = 1 iff **N=3**. Three spin-½ give **ZERO** singlets. [DERIVED] (TEST 4; verifier
  checked N=1..7, only N=3→1). **★ SHARPER than LANDING_D-QUARK-CONSOLIDATE**, which hedged "single-singlet
  is generic — 2⊗2⊗2 also has one": that hedge is WRONG under the SO(3)/spin reading (three spin-½ → 0
  singlets). The ε singlet is genuinely tied to N_c=3=(2ℓ+1), not generic. (Append-only correction logged.)
- **Bridge closed forms B₁=1/(2(2ℓ+1)²)=1/18, B₃=1/(2(2j+1)²)=1/8, ratio 9/4=(2ℓ+1)²/(2j+1)².** Exact
  multiplicity arithmetic given (ℓ,j). [DERIVED] as *multiplicity expressions* (TEST 6). CAVEAT: their
  IDENTIFICATION with the eigensolver source integrals (0.05567, 0.12494 at 0.2%/0.05%, LANDING) is a
  separate physical claim, re-graded in §3, NOT [DERIVED] here. Naming 9/4 "α_s/α_EM" is a §2 label.

**[INPUT]:**
- **j = ½** (spin-½ fermion) — the seed. Given j=½, the Diophantine (2j+1)²(2ℓ+1)(2|κmax|+1) =
  C(2ℓ+2|κmax|+1, 2ℓ+1) has the UNIQUE solution (j,ℓ,|κmax|)=(½,1,3) → 6 κ-channels (TEST 5, scanned
  ℓ∈0..6, K∈1..8: only (1,3,84)). The uniqueness is [DERIVED] conditional on the j=½ [INPUT]. (The
  link 84→pion mass is dense-fit and lives in §4/§5, NOT here.)

**[ANSATZ] — THE PIVOTAL GRADE (must be eliminated-or-proven-necessary; it is NOT proven necessary):**
- **Identifying the quark/strong sector with the rank-2 spherical tensor T_ij=r_ir_j−δ_ij/3.** cr187 §4
  itself titles this "**the rank-2 tensor HYPOTHESIS**" / "the next natural operator after the vector"; §15
  "if the matrix elements do not decompose, the rank-2 hypothesis fails." The metric provides a whole TOWER
  of spherical-tensor operators (rank-1 r̂ = the lepton sector §13.3, rank-2, rank-3, …); **nothing forces
  rank-2.** The "parity-block split" {−1,+2,−3}(even ℓ)/{+1,−2,+3}(odd ℓ) is *dynamically decoupled* ONLY
  because rank-2 is parity-even (rank-1 r̂ is parity-odd and connects the blocks; cr188's own ±κ block test
  prints "NOT block diagonal" — the real partition is ℓ-parity). So the entire quark CHANNEL STRUCTURE is
  downstream of this ansatz. **★ The one in-corpus "derivation" of rank-2 — §19.8b.2 "the mass term ψ̄ψ is
  a rank-2 bilinear, so the coefficient is multiplicity²" — is a CONFLATION** (verifier, attack succeeded):
  ψ̄ψ being a 2-index object in the 4-component Dirac-spinor space has nothing to do with selecting the
  rank-2 spherical tensor Y₂ as the *angular coupling* operator. Two different index spaces merged by the
  word "rank-2." Inconsistent internally too: cr186 §5a derives the same 2π² from RANK-1 bridge ratios.
  cr186 Step 10 (the corpus's own script): "CG §19.8b.5 status 'DERIVED' is **PREMATURE**." → rank-2 is
  posited, not derived. [ANSATZ].

**[ASSERTION] / vacuous (banked — never cite as evidence):**
- **Casimir C₂ = 4/3.** ΣT_a²=(4/3)I holds for ANY orthonormal su(3) basis — reproduced with RANDOM
  traceless-Hermitian generators to machine precision (TEST 3); fixed by N=3 + the normalization choice.
  CG §18.6's "Verified to machine precision <10⁻¹⁶" + "closure" is vacuous dressing. **Strengthened by the
  verifier:** cr194_casimir's *inverse-metric* route actually gives **8/3**, and only the separate
  Gram-Schmidt route gives 4/3 — i.e. 4/3 is a chosen-normalization artifact, not an eigenvalue. [ASSERTION].

**[INPUT]/[LABEL] (deferred to §2, listed here for completeness — NOT graded [DERIVED]):** electric
charges Q_u,Q_d; "color" as a gauge DOF; flavor/generation masses. cr195 §6.3 (corpus's own): "the spin
connection generates SO(3,1) (Lorentz), NOT SU(3) (color)"; local gauge color force is **conceded NOT
derived** — su(3) here is GLOBAL kinematics only. So "su(3) **color**" adds a physics label to the genuine
operator-algebra fact.

**Net §1 (the §1 deliverable):** the dimensionless REPRESENTATION skeleton is genuinely [DERIVED] (the
ℓ=1 8=3⊕5 su(3), the N=3-specific ε singlet, the bridge multiplicity arithmetic, the unique Diophantine
triple) — this is REAL, unfittable, ℓ=1-specific group theory, consistent with §0's verdict that only
dimensionless/structural content survives. BUT it is a skeleton of *operators on a 3-dim space*, and its
identification with PHYSICAL quarks/color/strong-force rests on (i) the j=½ [INPUT], (ii) the rank-2
[ANSATZ] (unforced; the sole in-corpus "derivation" is a rank-conflation), and (iii) free [LABEL]s
(charge, color-as-gauge, flavor mass) graded in §2. The "genuine/unfittable" claim survives for the
algebra; it does NOT survive for "these are quarks." Build §2/§3 only on the [DERIVED] algebra, flagging
the rank-2 ansatz wherever the parity-block channel structure is used.

### (2) The charge / mass LABELS
Scope: Q_u/Q_d, current masses 4mₑ/9mₑ, generation ratios (2π²,…). Phase-1 graded these fits — verify
rigorously and tag.
STATUS: **FIRST-PASS GRADED (session-6, 2026-06-07). NOT canonical** (Protocol §7).

**Closure result: §2 adds NO new [DERIVED] physics on top of the §1 skeleton.** Every genuine NUMBER here
(2/3, 4, 9, 9/4) is just §1's multiplicity arithmetic re-used; every PHYSICS NAME (electric charge, quark
mass, generation ratio) is a free [LABEL]/[FITTED] on top. Verified by a rigorous null test
(`da_reaudit_s2_labels.py`) + a blind adversarial verifier instructed to RESCUE the claims (Agent
`a78184b1ece5a9429`, 2026-06-07) — it overturned nothing and surfaced corpus self-concessions I did not have.

- **Generation mass ratios 2π², 6π⁴, 9π²/2, 14π² — [FITTED] (DROP as predictions).** NULL TEST (da_reaudit_s2_labels.py):
  the (rational)·π^k family is DENSE — a RANDOM target in [10,600] is hit within 1% by a simple form with
  **P=0.98** (within 2%: P=1.00). The four "matches" carry essentially zero evidential weight. The four
  "sector factors" {1, 3π², 9/4, 7} are heterogeneous in kind (bare number / π² / rational / bare number) =
  per-transition post-hoc assignment, NOT one operator evaluated at n. **★ Corpus self-convicts (verifier):**
  cr189 §15 — sector factors "(1,3,9/4,7) … **MATCHED, not derived**"; selection-rule + up/down assignment
  "OPEN"; §9.1 — the factor that should be 7 comes out **7.375 from the actual rank-2 matrix (5% off)**, so
  the factors do NOT even reproduce from the operator they're attributed to. The base 2π² is itself an
  asserted product (cr186:273 "the PRESCRIPTION … is an ASSERTION, no operator equation forces this product").
  **★ Internal contradiction:** CG §19.8b header "Status: CANDIDATE — coefficients found by SEARCHING quantum
  number combinations" (CG:3670) vs §19.8b.5 "Status upgraded to DERIVED" (CG:3719) vs §19.8b.6 "CLOSED" —
  unreconciled within one section; cr186:709 calls the "DERIVED" upgrade **PREMATURE**; validated_results:2287
  says "ADVANCED CANDIDATE … complete operator derivation OPEN." The DERIVED/CLOSED labels are unjustified.
- **Electric charges Q_u=+2/3, Q_d=−1/3 — [LABEL] on a real multiplicity number.** The NUMBER 2/3 =
  (2j+1)/(2ℓ+1) is genuine (§1 arithmetic), but "charge := √(B₁/B₃)" is a **tautology** — B₁∝1/(2ℓ+1)²,
  B₃∝1/(2j+1)², so √(B₁/B₃)=(2j+1)/(2ℓ+1) just cancels the defining squares (validated_results:2459-2461).
  No operator equation forces charge=this ratio: cr193's H1–H3 **FAIL** (physical pair-production couplings
  give 1.0/1.50/2.23, not 1/9·4/9), H4 gives |Q|=1/3 for **BOTH** blocks (can't distinguish u/d), only the
  constructed H5=tautology "passes"; up/down block assignment + sign are admittedly conventional
  (cr193:1368). cr192 itself: "the UDT EM coupling ratios are **NOT** the SM quark charges." → [LABEL].
- **Base masses 4mₑ=(2j+1)², 9mₑ=(2ℓ+1)² — FORM [FITTED]/conflation; MATCH [UNFALSIFIABLE].** The FORM
  (multiplicity²) is exact arithmetic, but its justification "mass coeff = multiplicity² because ψ̄ψ is a
  rank-2 bilinear" (CG:3695) is the SAME Dirac-spinor-index ↔ spherical-tensor-rank **conflation** as §1's
  rank-2 ansatz; cr186:694 concedes "No operator equation directly produces m_quark=(multiplicity)²×mₑ …
  this is pattern-matching." The MATCH to MS-bar u,d is **retracted by the corpus itself**: CG §19.8b.6
  (line ~3731) — comparing 4mₑ to an MS-bar extraction "was a **mirage** … model-dependent theoretical
  construct"; with ~10-20% scheme uncertainty it cannot be falsified → not evidence.

**Append-only refinement to §1 (N_c=3):** the number 3 = (2ℓ+1) = parity-block size is genuinely forced
[DERIVED], BUT the 3 channels are **non-degenerate** (distinct κ/ℓ), so identifying them with 3 *identical*
QCD color copies is unjustified — cr192 §7.3 "**Identical Copies Problem**." So "N_c=3" is a [DERIVED]
integer wearing a [LABEL] ("3 identical colors"); the color *interpretation* is not forced.

**Net §2 (deliverable):** §2 contains zero new derived physics. It is the layer where SM particle-names are
attached to §1's dimensionless skeleton: the charges are labels (magnitude via tautology, assignment
conventional), the generation masses are dense π-fits the corpus admits are "searched" and that don't even
reproduce from the operator (7→7.375), and the base-mass match is corpus-retracted as unfalsifiable. This
fully confirms Phase-1's "all fits," now rigorously null-tested + verifier-corroborated. Consistent with §0
(absolute scale fitted) and §1 (algebra real, physics-identification conditional).

### (3) ASSEMBLY: confinement-by-projection vs binding
Scope: color-singlet projection (angular averaging), the claim "assembly=projection NOT binding" (currently
an [ASSERTION] inferred from absence of binding), the ruled-out binding routes.
STATUS: **FIRST-PASS GRADED (session-6, 2026-06-07). NOT canonical** (Protocol §7).

**Closure result: §3 has NO derived multi-quark assembly/binding/confinement mechanism.** What survives is
(i) a kinematic SELECTION identity (exact, = §1's ε singlet re-used), and (ii) a robust NEGATIVE (the
dilaton does not bind). The session-5 "assembly = projection, NOT binding" is an [ASSERTION] that conflates
*observability* with *confinement* and leans on a *null-rejected* mass law. Verified by a blind adversarial
verifier instructed to RESCUE the claims (Agent `a63df520fde00cf75`, 2026-06-07); it overturned nothing and
caught an internal contradiction in CG/cr194.

- **"Confinement = color-singlet angular projection" — [ASSERTION] / OBSERVABILITY-ONLY (conflation).** The
  projection IS exact, but only as a SELECTION/observability rule: only rotationally-invariant (ℓ=0)
  combinations survive angular integration of observables (Σ_m|Y_{1m}|²=3/4π constant to 2e-16; ε_abc the
  unique singlet — this is just §1's [DERIVED] ε singlet + the angular integral). That is NOT confinement.
  **Confinement** = colored states cost large/rising energy; the projection only says they "average to zero"
  in observables. **★ The corpus concedes the dynamical confinement is NOT derived, and contradicts itself:**
  cr194:151/280 assert "Confinement is geometric … this is exact" / list confinement as "Established", while
  the SAME file's honest sections say cr194:217 "the angular averaging argument for confinement is
  QUALITATIVE … a quantitative derivation would show the potential rises with separation [not done]" and
  cr194:289 "confining potential NOT derived"; cr192:247 "qualitative, not quantitative … would require
  showing only angular singlets have finite-energy solutions" (open task, cr192:309). The "exact" attaches
  to the trivial angular identity, not to confinement. → [ASSERTION] (observability is [DERIVED]; calling it
  confinement is unforced over-reach). Same conflation pattern as §1 (rank) and §2 (bilinear).
- **"Baryon mass = constituent SUM" — [NULL-REJECTED].** The clean anchor 2π⁵mₑ=312.8 MeV is rejected by a
  target-blind null scan: octet/decuplet prefer m_q≈370 MeV (RMS 1.2%) over 313 (RMS 7.8%, ~6× worse)
  (LANDING_D-BARYON-CONSTITUENT:31). And "proton = N_c×constituent" is retracted: 2π⁵=6π⁵/3 is just proton/3
  with a trivial 6=(2j+1)(2ℓ+1)=2×3 relabel (the (2ℓ+1) plays no color role) (D-CONSTITUENT-INDEP:5-17).
  No derived constituent-sum mass law exists.
- **"Assembly = projection, NOT binding" — [ASSERTION-FROM-ABSENCE].** The reframe is "every binding search
  found ~zero binding ⟹ nothing to bind ⟹ assembly is projection+sum" (D-BARYON-CONSTITUENT:46-47, "the
  absence of binding is the model working, not failing") — a reinterpretation of a null, not a positive
  derivation. It is entangled with, and "confirmed" by, the very constituent-sum that is null-rejected above
  (cannot rescue this without that). And the absence itself is partly artifactual: D-BARYON-AUDIT retracts
  "route closed" — the binding tests ran the one same-κ config CG §8.6 GUARANTEES repels (a tautology) and
  OMITTED the §19.9.8 three-exchange sector the metric actually uses for hadronic binding. → [ASSERTION].
- **"The dilaton is NOT the inter-quark binder" — [DERIVED-NEGATIVE] (robust; scope = one channel).** The
  screening length 1/μ=√(3/π)=0.977 ≪ cavity r*=6.99 (μr*=7.15, e^{−μr*}=7.8e-4), and the self-consistent
  scalar mean-field anti-binds in EVERY config: same-κ +2.878%→+1.953%, cross-κ{−1,+2,−3}+1.569%, +Coulomb
  +1.808% (D-BARYON-CROSSK:19, validated solve reproducing D-BARYON-3F). ROBUST to §0's fitted inputs: μ²
  would have to be wrong by ~51× to close the O(1)≪O(7) hierarchy (verifier). This is a genuine negative.
  CAVEAT (append-only): it kills only the DILATON channel; Coulomb is unscreened and the σ/ω three-exchange
  is untested — so "nothing binds" is NOT established, only "the scalar dilaton mean-field doesn't."

**Single-mode cavity confinement (the one real positive nearby, but NOT color-confinement):** the §0-[DERIVED]
vacuum branch (φ→−∞ outward ⇒ e^{2φ}→∞) plus the Neumann BC at r* makes a finite cavity, so single Dirac
modes have a DISCRETE GeV-scale spectrum. Real — but (i) the SCALE is the fitted C (§0), (ii) the hard wall
is the fitted r* domain, and (iii) it is SINGLE-MODE confinement, not a derived COLOR confinement of
assembled quarks. Naming it "color confinement" is a [LABEL].

**Net §3 (deliverable):** there is no derived assembly, binding, or color-confinement mechanism. The genuine
content is: (a) the exact kinematic singlet SELECTION rule (= §1's ε singlet, an observability statement);
(b) the robust NEGATIVE that the dilaton scalar field does not bind quarks; (c) single-mode cavity
confinement at the fitted scale. Under CR-191 ontology-(ii) the baryon is plausibly a SINGLE geometric mode
("3 quarks assembling" being the SM premise the ontology rejects) — in which case §3's assembly question
DISSOLVES rather than resolves: there is nothing to assemble, and equally nothing derived about assembly.
Consistent with §1/§2 (quarks = real labels on a real single mode, not assemblable derived constituents).

### (4) The SPECTRUM
Scope: κ-ladder, the sparse-meson match (p~1e-4 but one fitted scale + J^PC issues), the breathing scalars,
the half-integer-j-vs-integer-J problem, the density artifact.
STATUS: **FIRST-PASS GRADED (session-6, 2026-06-07). NOT canonical** (Protocol §7).

**Closure result — the DECISIVE verdict of the audit: NO genuinely unfittable, falsifiable, parameter-free
hadron-spectrum prediction survives.** The geometric channel structure sets the right overall SCALE
(everything O(C), lowest mode ≈ pion ≈133 MeV) — but the scale is fitted (C, §0), the ratio structure is
fitted (φ₀, §0 + the circularity below), the statistics are wrong (half-integer j), and J^PC/selection is
absent. Verified by a blind adversarial verifier instructed to RESCUE any surviving prediction and to attack
the circularity (Agent `afe5fa689d474921a`, 2026-06-07): verdict NONE-SURVIVES; circularity REAL; p INFLATED;
it could not rescue even the one parameter-free-flagged hadron mass (6π⁵).

- **Single-mode meson identification (CR-191 "meson = E_n(κ)×C") — [INVALID] / WRONG STATISTICS.** A single
  κ-channel Dirac mode has half-integer j = |κ|−½ (κ=−1→½, +2→3/2, −3→5/2, da_reaudit_s4_spectrum.py); a meson
  has INTEGER J. So a single κ-mode CANNOT be a meson; the mass-match is between wrong-type objects
  (D-MESON-JPC-1:11-14, conceded). [DERIVED-NEGATIVE].
- **The sparse-meson "p~1e-4" ratio match — [FITTED]/INFLATED (CIRCULAR).** Claimed parameter-free ("only
  ratios enter"). **★ But it is circular:** the eigenvalue ratios are produced at φ₀=−cos(π/5), and CG:2436
  (emergence scan) shows the ratios "change DRAMATICALLY with φ₀" and that φ₀=−0.809 was SELECTED precisely
  because "at φ₀=−0.809, ratios spread to 1:5.6:7.3:8.9, matching the physical meson spectrum." So φ₀ was
  tuned to the meson ratios, then the ratio-match is presented as a prediction — φ₀ is a fitted shape
  parameter (§0), and the ratios are NOT φ₀-invariant (corpus: E₂/E₁=3φ_gold/I₂ is "μ-DEPENDENT — an anchor,
  not a prediction", CG:2877). On top of that: (i) one fitted overall scale C (razor min, ~1% from best-fit
  142, D-MESON-SPECTRUM-BLIND:28-31); (ii) the dense region >1.1 GeV is a density artifact (p=0.18); (iii)
  wrong statistics (above); (iv) σ/f₀(500) omitted; (v) a spurious mode (752 vs ρ775). The "p<0.0001" was
  driven entirely by ~5 sparse states against a too-generous "random ladder" null that charges nothing for
  the φ₀-pretuning or the scale calibration. → a weak SCALE signal, NOT a parameter-free prediction.
- **m_p/m_e = 6π⁵ — [FITTED]/dense (re-grades the handoff's "proton derived").** The one parameter-free-flagged
  HADRON mass, so the most dangerous candidate. It fails: the (rational)·π^k family is DENSE (~6300 simple
  forms; a sub-0.1% form for the proton is expected by counting, D-LEDGER:23-28); 84 is forced only GIVEN
  the closure condition and the closure→mass LINK is the cheap step (D-84-1); 6π⁵ rides the Fock/quantization
  IMPORT π-ladder (D-BARYON-DIAGNOSIS:43-47, [[dont-use-fock-as-yardstick]]); and the clean unfittable channel
  E₁·C DISAGREES with the 6π⁵ route by 1.5% (D-LEDGER:31). → 6π⁵ is a selected label among near-degenerate
  dense fits, NOT a parameter-free prediction. (The handoff's "proton 6π⁵ derived" is downgraded here.)
- **Breathing scalars (σ=519≈f₀(500), 1394≈f₀(1370)) — [PARTIAL]/weak (the best item, still not a sharp
  prediction).** A genuine ODE eigenvalue with CORRECT statistics (boson 0⁺⁺) — the strongest physics object
  in the spectrum. But σ=519 lands inside the PDG's BROADEST pole (f₀(500): 400–550 MeV, width ~500), so it
  carries little falsifying weight; the tower also predicts a spurious scalar at 889 (no partner, 9% off);
  and it still rides the fitted scale C. Suggestive, not a sharp falsifiable prediction.
- **Baryon spectrum (CG §14) — [INVALID] / shopped (statistically void as a result).** Uniform-ladder
  p≈0.2 (CG:2442 itself: "not uniquely determined predictions"); two pairs SHARE an eigenvalue; the strict
  no-shop pure-ordering test fails (baryons RMS 72%, null p=0.998 — random nearly always beats it); wrong
  shape (ladder spans factor ~9, baryons ~1.8). D-RATIOS / D-BARYON-DIAGNOSIS. The arithmetic runs; the
  result carries no evidential weight. [INVALID].

**Net §4 (the decisive deliverable):** after the fitted floor (§0), the real-but-conditional skeleton (§1),
the label layer (§2), and the absent assembly mechanism (§3), the spectrum yields NO genuinely unfittable
mass / ratio / J^PC prediction. Every quantitative hadron "prediction" reduces to: one fitted scale C + a
fitted shape φ₀ (to which the ratios are circularly tuned) + dense (rational)·π^k accommodations + a partly-
imported π-ladder. What is REAL is qualitative/structural: the geometric channel structure sets the correct
SCALE and ordering-of-magnitude of the lightest hadrons, and the breathing-scalar eigenvalues are genuine
(if broad-pole) boson modes. The meson spectrum's true bottleneck is the chiral (pion-lightness) mechanism,
absent at r*=6.99 — which gates both the pion and the q̄q spectrum and is the §5 open item.

### (5) The PION
Scope: 0⁻ = ψ̄γ₅ψ=2GF bilinear (present); lightness — single-particle Goldstone ruled out; the q̄q RPA
collective mode (unbuilt). STATUS: NOT STARTED.

---
## Provenance (session-5 landings, to be re-graded into the sections above, NOT trusted)
D-QUARK-CONSOLIDATE, D-BARYON-MULTICENTER-1/2, D-BARYON-AUDIT, D-BARYON-CROSSK, D-BARYON-CONSTITUENT,
D-CONSTITUENT-INDEP, D-PION-0MINUS-1, D-MESON-SPECTRUM-BLIND, D-MESON-JPC-1, D-PION-CHIRAL-1/2,
D-MASSIVE-DIRAC-1; plus CG matter sections (§4 Dirac, §8.5 coupling, §11 Maxwell, §13 angular masses,
§14 spectrum [shopped], §19.9 nuclear). All [UNGRADED] until pulled in.

---
## CHANGELOG (append-only; every edit logs date / session / section / change / grade before→after / evidence)
Per Self-Hardening Protocol §6. This log + git diff are the tamper-evidence: any grade that rose without a
matching entry recording its derivation + verifier is invalid and must be downgraded.
- **2026-06-07 / session-5 close / ALL** — Document created (scaffold only): status header, Self-Hardening
  Protocol, grading vocabulary, 7 audits, ground rules, foundation-up section plan (0)–(5), provenance list.
  NO claims graded yet (every section STATUS: NOT STARTED; all prior work [UNGRADED]). Next session: begin
  §(0) params+C, try to break the floor. Evidence: n/a (no grades asserted).
- **2026-06-07 / session-5 close / Self-Hardening Protocol** — Added invariant §9 (BOUNDED COST:
  re-derivation is event-triggered not periodic; recorded provenance stands; per-session cost bounded to the
  current frontier — "harder to fool, not harder to use") + cross-ref in §1. Reason: prevent a misreading of
  §1 that would make per-session effort grow with the accumulated corpus (Charles flagged the possibility).
  No grade changes. Evidence: n/a (protocol clarification, not a claim).
- **2026-06-07 / session-6 / §(0) Parameters and scale C** — FIRST-PASS GRADED (tried to break the floor).
  Grades recorded: φ₀=−cos(π/5) → **[INPUT]+[FITTED]** (boundary condition; metric admits all φ₀<0 per CG §8.1.5;
  value selected to match meson eigenvalue-ratio spread, CG:2436; ⟨G⟩=2/π justification fails numerically).
  μ²=π/3 → **[ASSERTION]** (⟨cos²θ⟩=1/3 is [DERIVED] sphere geometry, but the ×π "angular half-period" closure
  is asserted at CG:2195 with no scalar-action derivation; value data-validated against meson ratios, CG:2201).
  r*=6.9875 → **[FITTED]/CIRCULAR** (defined as where E₁=2√2/3, "exact by construction … tuned-to-target identity"
  CG:2831; 7−1/80 form circular, |φ₀| cancels trivially; anchor-dependent, =7.042 proton-anchored CG:2863).
  C=4π²mₑr* → **[INPUT]+[FITTED]** (mₑ external anchor CG:21; 4π² a "free convention" per LANDING_D-ANCHOR-4-UNIFY-1:25,38;
  exact only to 1.5% CG:2513). Surviving [DERIVED] sub-facts: ⟨cos²θ⟩=1/3; vacuum classification by sign(φ₀);
  source≈0.250±0.001 stable integral (but "=1/4" is fitted rounding); r*/r_b≈φ_gold stable ratio (0.1% match, not
  identity). Net: 0/4 floor params [DERIVED]; absolute scale is fitted ⇒ all absolute masses scale-fitted; only
  dimensionless/ratio/structural content can be real. Grade direction = all DOWNWARD (ratchet-free per Protocol §2),
  but recorded with derivation + verifier anyway. **Evidence:** blind adversarial verifier Agent `ae094fea6c5b24c13`
  (2026-06-07), instructed to DEFEND all four as DERIVED — confirmed every downgrade independently, overturned none,
  added corroboration; cleared audits 1–7 on the closure. Sources cited inline in §(0).
- **2026-06-07 / session-6 / §(1) Quark representation skeleton** — FIRST-PASS GRADED. First section with
  genuine [DERIVED] content, but only the dimensionless rep theory; physical-quark identification is
  conditional. Grades: [DERIVED] (recomputed from scratch, da_reaudit_s1_skeleton.py 6 tests + random
  controls) — the ℓ=1 8=(2ℓ+1)²−1=3⊕5 su(3) operator algebra w/ exact cross-rank orthogonality (only at
  ℓ=1); the ε_abc singlet (mult 1, N=3-specific, three spin-½→ZERO); bridge multiplicity forms
  B₁=1/18,B₃=1/8, ratio 9/4. [INPUT]: j=½ (→ unique Diophantine (½,1,3), 6 channels). **[ANSATZ] (pivotal):
  rank-2 = the quark/strong operator** — cr187 self-titles it "the rank-2 HYPOTHESIS"; metric provides a
  tower, nothing forces rank-2; the parity-block split is downstream of it; the one in-corpus "derivation"
  (§19.8b.2 "ψ̄ψ is rank-2 bilinear") is a Dirac-index↔spherical-tensor-rank CONFLATION (verifier); cr186
  Step 10 calls §19.8b.5 "DERIVED" **PREMATURE**. [ASSERTION]/vacuous: Casimir=4/3 (holds for random su(3)
  bases; inverse-metric route gives 8/3 — normalization artifact). [LABEL] (→§2): charges, color-as-gauge
  (cr195 §6.3: spin connection gives SO(3,1) NOT SU(3); local gauge color conceded NOT derived), flavor
  masses. **★ Sharpening logged (append-only):** LANDING_D-QUARK-CONSOLIDATE's hedge "ε singlet is generic,
  2⊗2⊗2 also has one" is WRONG (three spin-½ → 0 singlets); ε singlet is N=3-specific. Net: the *algebra*
  is real+unfittable; "these are quarks" rests on j=½ [INPUT] + rank-2 [ANSATZ] + free labels. Grades mixed
  direction; the [DERIVED] ones recorded with derivation + verifier on the line per Protocol §2. **Evidence:**
  da_reaudit_s1_skeleton.py (committed) + blind adversarial verifier Agent `a4fe441624990c66d` (2026-06-07,
  tasked to attack [DERIVED] and defend rank-2) — confirmed all 4 grades, no over/under-grading. Cited inline.
- **2026-06-07 / session-6 / §(2) Charge/mass labels** — FIRST-PASS GRADED. Zero new [DERIVED] physics;
  every genuine number is §1 multiplicity arithmetic re-used, every physics name is a free label/fit.
  Grades: generation ratios 2π²/6π⁴/9π²/2/14π² → **[FITTED], DROP** (null test da_reaudit_s2_labels.py:
  random target in [10,600] hit within 1% w.p. 0.98 — family dense, zero evidential weight; cr189 §15
  "MATCHED not derived"; §9.1 the "7" factor is really 7.375 from the actual matrix; CG header "found by
  SEARCHING" contradicts §19.8b.5 "DERIVED"; cr186:709 "PREMATURE"). Charges Q_u=2/3 → **[LABEL]**
  (√(B₁/B₃) tautology undoes defining squares; cr193 H1–H4 fail, H4 gives |Q|=1/3 for both blocks, only
  constructed-H5 passes; up/down + sign conventional; cr192 "NOT the SM quark charges"). Base-mass FORM
  4/9 mₑ → **[FITTED]/conflation** (multiplicity² justified via the §1 rank-2-bilinear conflation; cr186:694
  "pattern-matching, no operator equation"); base-mass MATCH → **[UNFALSIFIABLE]** (CG §19.8b.6 self-retracts
  the MS-bar comparison as "a mirage … model-dependent"). **Append-only refinement to §1:** N_c=3=(2ℓ+1) is
  a [DERIVED] integer but the 3 channels are NON-degenerate ⇒ "3 identical colors" is a [LABEL] (cr192 §7.3
  "Identical Copies Problem"). All grades downward/confirmatory (ratchet-free). **Evidence:**
  da_reaudit_s2_labels.py (committed) + blind adversarial verifier Agent `a78184b1ece5a9429` (2026-06-07,
  tasked to RESCUE the claims) — overturned nothing, added corpus self-concessions. Cited inline in §(2).
- **2026-06-07 / session-6 / §(3) Assembly: confinement-by-projection vs binding** — FIRST-PASS GRADED.
  No derived multi-quark assembly/binding/confinement mechanism. Grades: "confinement = angular projection"
  → **[ASSERTION]/OBSERVABILITY-ONLY** (the projection is exact angular algebra = a SELECTION/observability
  rule = §1's ε singlet; NOT confinement; corpus concedes "confining potential NOT derived" cr194:289/217,
  cr192:247, and CONTRADICTS itself at cr194:151/280 "exact/Established"). "Baryon mass = constituent SUM"
  → **[NULL-REJECTED]** (anchor 2π⁵mₑ=313 rejected, octet/decuplet prefer ~370, RMS 7.8% vs 1.2%,
  D-BARYON-CONSTITUENT:31; "proton=N_c×constituent" retracted, D-CONSTITUENT-INDEP:5). "Assembly=projection
  NOT binding" → **[ASSERTION-FROM-ABSENCE]** (null reinterpreted as feature, D-BARYON-CONSTITUENT:47;
  entangled with the null-rejected sum; absence partly artifactual — D-BARYON-AUDIT: tested the same-κ config
  §8.6 guarantees repels, omitted §19.9.8 three-exchange). "Dilaton NOT the binder" → **[DERIVED-NEGATIVE]**
  (robust: 1/μ=√(3/π)=0.977≪r*=6.99, μr*=7.15; anti-binds all configs, D-BARYON-CROSSK:19; survives §0 fits
  — μ² would need a 51× error; scope = dilaton channel only, Coulomb+σ/ω untested). Single-mode cavity
  confinement is real but single-mode + fitted scale, NOT color confinement ([LABEL]). Under ontology-(ii)
  the assembly question DISSOLVES (single mode, nothing to assemble). All grades downward/confirmatory
  (ratchet-free); negatives preserved append-only. **Evidence:** screening arithmetic re-confirmed +
  blind adversarial verifier Agent `a63df520fde00cf75` (2026-06-07, tasked to RESCUE) — overturned nothing,
  caught the cr194 internal contradiction. Cited inline in §(3).
- **2026-06-07 / session-6 / §(4) The spectrum — DECISIVE** — FIRST-PASS GRADED. Verdict: NO genuinely
  unfittable, falsifiable, parameter-free hadron-spectrum prediction survives. Grades: single-mode meson id
  → **[INVALID]/wrong-statistics** (j=|κ|−½ half-integer ≠ integer J; D-MESON-JPC-1 conceded). Sparse-meson
  "p~1e-4" → **[FITTED]/INFLATED/CIRCULAR** (φ₀ was SELECTED to make the eigenvalue ratios match mesons,
  CG:2436 "ratios change dramatically with φ₀"; ratios φ₀-dependent CG:2877; +fitted scale C razor; +density
  artifact p=0.18 >1.1GeV; +wrong stats; +σ omitted; +spurious mode). m_p/m_e=6π⁵ → **[FITTED]/dense**
  (dense (rational)·π^k family ~6300 forms, D-LEDGER; rides Fock import D-BARYON-DIAGNOSIS; clean E₁·C channel
  disagrees 1.5% — **downgrades the handoff's "proton 6π⁵ derived"**). Breathing scalars σ=519≈f₀(500) →
  **[PARTIAL]/weak** (genuine 0⁺⁺ eigenvalue but into PDG's broadest pole + spurious 889 + fitted scale).
  Baryon spectrum CG §14 → **[INVALID]/shopped** (uniform-ladder p≈0.2, shared eigenvalues, no-shop RMS 72%
  null p=0.998, wrong shape; D-RATIOS/D-BARYON-DIAGNOSIS; CG:2442 "not uniquely determined"). Net: every
  quantitative hadron prediction = fitted C + fitted φ₀ (ratios circularly tuned) + dense π-fits + imported
  π-ladder; only the SCALE and the breathing eigenvalues are real-ish. Bottleneck = chiral mechanism (→§5).
  All grades downward (ratchet-free); negatives append-only. **Evidence:** da_reaudit_s4_spectrum.py
  (committed) + blind adversarial verifier Agent `afe5fa689d474921a` (2026-06-07, tasked to RESCUE + attack
  the circularity) — NONE-SURVIVES, circularity REAL, p INFLATED. Cited inline in §(4).
- **2026-06-07 / session-6 / §(0)+§(2)+§(4) ANCHOR-ALLOWED RE-CHECK** — Re-ran the matter-sector negatives vs
  BOTH udt_active_results.md + udt_validated_results.md with a mass anchor (mₑ) ALLOWED (Charles). No §240-style
  rescue found; §0–§4 verdict holds (triangulated: this audit + corpus's own gap registry + the re-check).
  REFINEMENTS (grades rise, evidence on line per §2): in §(0), C=4π²mₑr* — the **4π² is FORCED** given mₑ by the
  electron's derived A_e=1/(2j+1)²=1/4 (VR:2451), NOT a "free convention" as graded earlier (that entry refined).
  In §(4)/§(2): the lepton-ratio **rational prefactors (6, 20/3) are [DERIVED]** (r̂ coupling CG:2203 + selection
  rule (n−1)(n−2)=0 CG:2230); the **π-powers are [IMPORT]** (CG:2245 retraction; D-PI-POWER-ORIGIN OPEN CG:4538);
  **charges = clean multiplicity [LABEL]** (not "tautology/fitted"). Shape params φ₀/μ²/r* still asserted/circular
  (anchor doesn't rescue dimensionless shape params); meson/σ ratios φ₀-circular. Full ledger in UDT_REBUILD.md.
  Evidence: Agents a3b922397042f0b86 + a4dbe87119123486a (both docs end-to-end). No grade rose without evidence.
- **2026-06-08 / session-7 / ALL (pointer entry — §0–§4 grades UNCHANGED)** — Session-7 worked in
  `UDT_REBUILD.md` Parts G–J; nothing here re-graded; this entry logs the cross-reference + confirms the §0–§4
  verdict is REINFORCED, not softened. (a) **A & B BANKED as postulates** — all four ALGEBRAIC derive-B attempts
  CLOSED (ℓ-reach, spin-2-ceiling, Diophantine-form D-A3-2, ℓ(2ℓ+1) lemma), all failing on the SAME
  boson↔fermion/single-↔multi-body category gap (UDT_REBUILD Parts G/H + CHANGELOG; blind verifiers
  ac482b602fb2545ad, a1f5253c4b3e718bd, ae3c4a2b2fe15f6e4). (b) **§10.5 two-sector seam RESOLVED structurally** —
  Part I (`da_seam_einstein.py`, verifier a4d14234d9369317c): B=1/A ⟹ G^t_t=G^r_r ⟹ the positional-dilation metric
  is DEFINITIONAL (not matter-sourced) at any scale; Part J (Charles): same metric is the MACRO mechanism too →
  one definitional geometry across macro+micro, matter = the exact φ→−φ **inside-out** (φ<0) region. Verified;
  scale+empirical quarantined to cosmology (Charles's domain). (c) **MASS EMERGENCE (relevant here):** a
  scaffold-free spinor-binding mechanism EXISTS — a free-magnitude inside-out pocket (NO floor μ²/φ₀, NO wall)
  binds the Dirac spinor with smooth onset (`da_option1_well.py`) — BUT it does **NOT pin any mass**: lepton
  ratios (207/3477) not reproduced as a radial tower (Koide Q≈1/3, not 2/3, `da_leptons_pocket.py`); the φ-depth
  ladder is the right *exponential* mechanism but the spacings are unpinned (`da_lepton_ladder.py`). **⟹ CONSISTENT
  with §(4)'s "NO genuinely-derived spectrum"; masses stay parameterized; nothing here upgrades.** §5 pion RPA
  still NOT STARTED. CALIBRATED STATUS (unification = structural/verified; mass-origin = NOT established) recorded
  in UDT_REBUILD Part J. New derive-B lead (gut, not started): a TOPOLOGICAL/index route on the inside-out region.
  No grade rose. Evidence: UDT_REBUILD.md Parts G–J + listed verifiers/scripts.

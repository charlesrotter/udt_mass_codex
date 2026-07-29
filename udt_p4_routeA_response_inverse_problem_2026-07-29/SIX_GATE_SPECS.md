# P4 Route A Stage 1 — SIX-GATE SPECIFICATIONS (TA5; specs ONLY, no gate is run)

Date: 2026-07-29. Contract: `PREREGISTRATION.md`. These are executable pass/fail
specifications of the six-gate sequence (MAP Route A: same-solution closure → sector
selection → Helmholtz → gauge/Noether → boundary differentiability → periods) as it
applies to a candidate response 𝓡 ON THE TYPED DOMAIN of `POSED_INVERSE_PROBLEM.md`.
**No candidate exists at Stage 1; running any gate here would be F-A1. None is run.**
**AMENDED 2026-07-29 per `VERIFIER_REPORT.md` (A2/A4):** gate 2's FAIL clause and gate
4's step 2 corrected from "bare-linear dependence" to "character-MISMATCHED dependence"
(the old wording would wrongly fail legitimate candidate shapes such as d(k10²), whose
R_k10 component is bare-k10-linear yet K₄-invariant as a one-form); gate 6 carries the
K₄-torsion-period scope note. Amendment record: `CORRECTION_LAYER.md`.

Common input to every gate — a CANDIDATE DECLARATION, which must state (else the gate
is not executable and the candidate is REJECTED-AS-UNDECLARED, which is a completeness
failure, not a physics verdict):

    (D1) the component list over the census (every census row covered; forks resolved
         EXPLICITLY and ledgered — resolving a fork silently = F-A2);
    (D2) the jet order N of each component;
    (D3) the declared pairing (P1/P2/P3 of §1.5) with its supplied structures tagged
         (volume functional / dual class / stratum trace maps);
    (D4) the domain declaration on null/type-changing strata (J09);
    (D5) the completion-fork stance (L4) and boundary-data stance (varied vs held).

Gate discipline (binding): every gate checks PROVENANCE and HONESTY (is the structure
present, declared, consistent) — NEVER MERIT (is the answer the expected shape). A FAIL
routes to the recorded failure class; it is a classification, not a suppression.

---

## Gate 1 — SAME-SOLUTION CLOSURE (structural compatibility)

**Question.** Do the candidate's component equations close on ONE
metric–matter–boundary solution structure, avoiding the three TYPED failure modes of
the 28+12 negative map (local-without-selection; global-without-local-source;
conditional-branch-without-solder)?

**Procedure.**
1. Enumerate the zero-set system {R_i = 0} over the declared components (D1).
2. Check every census direction has either an equation or an explicitly retained
   modulus (no silent freeze; J06-else-branch allowed and reported).
3. Compute the formal compatibility identities of the system (the generalized
   Bianchi/Noether identities from gate-4 equivariance must be CONSISTENT with the
   component count: overdetermination beyond the gauge identities must be resolved by
   explicit integrability conditions, not discarded equations).
4. Classify against the three failure modes: (a) local equations present but moduli
   selection absent AND not retained → local-without-selection; (b) completion data
   constrained but no local source equation → global-without-local-source; (c)
   conditional branches used without solder maps between them (cross-branch splices
   are forbidden — Route B C3) → conditional-branch-without-solder.

**PASS:** all census directions covered (equation or retained modulus); compatibility
identities close; none of the three typed failure modes present.
**FAIL:** any typed failure mode present → record WHICH, with the witness component.
Existence of solutions is NOT this gate (that is Stage-2+ / J15 reporting).

## Gate 2 — SECTOR SELECTION (screen/moduli slots; requirement 4 + J06)

**Question.** Does the candidate's screen sector carry the structure that CAN determine
(or honestly retain) the two-scalar seat and mixing moduli?

**Procedure.**
1. Decompose the screen-sector components on the seat: r_tr·I₂ + r_tf·diag(−1,1) +
   mixing slots (`B2_screen_trace_tracefree_decomposition`).
2. Compute the pairing of each moduli direction (∂λ, ∂k_mod, ∂k10, ∂C) with the
   candidate's components.
3. Apply the exact theorem (F-RA2): if the screen sector factors through trace/volume/
   density channels only, its k_mod-pairing is IDENTICALLY zero (`B3_*`) — the
   candidate then CANNOT be in J06's "determined" branch for k_mod.
4. Check the J06 disjunction: each modulus is (i) determined by a nonzero pairing, or
   (ii) explicitly retained and reported as residual. Check K₄ character-matching of
   the moduli dependence (A1-amended: each component carries the K₄ character of its
   paired direction — `A6_*`; components along K₄-invariant directions factor through
   the `A4_*` invariants).

**PASS:** J06 disjunction holds for every modulus with the branch recorded; moduli
dependence K₄ character-matched; no J13 discriminator slot silently deleted.
**FAIL:** any modulus neither determined nor retained (the named false pass "spectator
screen isotropy or trace zero assumed"), or character-MISMATCHED moduli dependence (a
component whose K₄ character differs from that of its paired direction — A2-amended;
bare-k10-linear dependence in R_k10 is character-matched and LEGITIMATE, e.g. the
d(k10²) shape). Record per-modulus.

## Gate 3 — HELMHOLTZ (variationality as a TESTABLE property; F-A3)

**Question.** Is 𝓡 locally exact (𝓡 = δS) — i.e., does the L6 fork resolve to the
variational branch FOR THIS CANDIDATE?

**Procedure.**
1. Compute the formal Fréchet derivative D𝓡 componentwise at declared jet order N.
2. Test self-adjointness of D𝓡 with respect to the DECLARED pairing (D3) — the
   Helmholtz conditions at jet level (pairing-relative: a candidate self-adjoint under
   P3 need not be under bare P1; the declaration governs).
3. If self-adjoint: record LOCALLY-EXACT (an action density exists locally; its global
   existence goes to gates 5–6).
4. If not: record NONVARIATIONAL — this is a CLASSIFICATION into the L6 nonvariational
   branch, NOT a failure/elimination (demanding exactness = F-A3).

**PASS/OUTCOME:** either stamp (LOCALLY-EXACT / NONVARIATIONAL) is a pass of the GATE
(the gate's job is to decide the fork honestly). **FAIL** only if the candidate's
declaration makes the test uncomputable (undeclared pairing or jet order).

## Gate 4 — GAUGE/NOETHER (requirement 7 + J10 on the exact quotient)

**Question.** Is 𝓡 equivariant on the quotient, with the forced identities holding
OFF-SHELL?

**Procedure.**
1. Connected part: verify components transform contragradiently to the tangent
   transport T ↦ Λ⁻ᵀTΛ⁻¹ (`T2_*`) under local Lorentz; equivalently
   𝓡(Λ·𝒳)[Λ·δ𝒳] = 𝓡(𝒳)[δ𝒳].
2. Discrete residual: verify well-definedness on the K₄ quotient via CHARACTER-MATCHED
   RELATIVE INVARIANCE (A2-amended): every component transforms with the K₄ character
   of its paired direction (component character × direction character = trivial —
   `A3_*`, `A6_*`); components along K₄-invariant directions (δφ, base data, δλ,
   δk_mod, boundary data) must factor verbatim through the exact invariants (`A4_*`);
   a character-MISMATCHED component → FAIL (bare-linearity alone is NOT a failure:
   ω = k10·dk10 is K₄-invariant).
3. Noether identities: ⟨𝓡, δ_gauge𝒳⟩ ≡ 0 identically (off-shell) for every gauge
   direction; record the resulting differential identities (Bianchi-type) and check
   them against gate 1's compatibility count.
4. Guard (J10 false pass): equivariance of the FAMILY must not be reported as unique
   selection of a member; no fixed preferred plane may be smuggled (none exists —
   `A5_*`).

**PASS:** 1–3 hold identically (zero residual), 4 clean. **FAIL:** any residual
nonzero → record the violating component and group element/direction.

## Gate 5 — BOUNDARY DIFFERENTIABILITY (requirement 6 on the finite cell)

**Question.** Is the total pairing differentiable on the stratified finite cell — no
unpaired boundary/corner jets — under the mirrored-cell structure?

**Procedure.**
1. From the declared jet order N, enumerate the wall jet slots (the wall's jet depth
   is N-dependent: e.g. 1-jet wall for 2nd-order candidates vs 2-jet wall +
   3rd-derivative momenta for 4th-order — Route C TC5, cited as EXAMPLES).
2. Vary: compute ⟨𝓡, δ𝒳⟩ including all wall/corner terms per the declared boundary
   fork (D5). If boundary data are varied: every wall jet slot must be paired by a
   declared R_∂ component; corners by R_corner (the seal VALUE alone is insufficient —
   requirement 6).
3. Check compatibility with the mirrored parity (CANON C-2026-06-10-2) and the
   seal-involution sector split (C-2026-07-04-1): static-sector components use the
   spatial mirror φ→−φ data; time-on components the temporal mirror — a candidate
   whose wall terms cross the sector split is recorded as a parity violation.
4. If boundary data are held (D5 fork ii): the same enumeration runs as consistency
   conditions on the held data.

**PASS:** zero unpaired jet terms on every stratum; parity/sector-split respected.
**FAIL:** any unpaired slot or parity violation → record stratum + jet slot.

## Gate 6 — PERIODS (requirement 9; global exactness / holonomy control)

**Question.** Are the global obstructions controlled?

**Procedure.**
1. Enumerate the nontrivial cycles of 𝒟 for this candidate's declaration: completion-
   class cycles (fork L4 over-the-class), K₄-orbifold cycles in the moduli factor,
   J07/J11 cocycle loops (the E08-type twisted-cocycle holonomy — Route B T3).
2. If gate 3 stamped LOCALLY-EXACT: compute the periods of 𝓡 over each cycle; PASS
   requires each period to vanish or be EXPLICITLY quantized (with its quantum
   reported — quantization is a report, not a merit judgment).
3. If gate 3 stamped NONVARIATIONAL: compute the corresponding holonomy/monodromy of
   the closure data over the same cycles; PASS requires it trivial or CLASSIFIED
   (J11's pass condition).

**PASS:** every cycle's obstruction vanishing/quantized/classified and reported.
**FAIL:** any uncontrolled period/holonomy → record the cycle.

Scope note (A4-amended): the K₄-orbifold-cycle period condition in step 2 is VACUOUS
for closed one-forms (torsion classes: 2·period = period over γ² = 0, so periods vanish
automatically — verifier `V8_clash2_torsion_periods_vacuous`); for those cycles the
gate's live content is the step-3 holonomy reading and the non-torsion cycles.

---

## Sequence discipline

Gates run in the stated order; a gate-k FAIL stops the sequence for that candidate with
the failure class recorded (gates k+1… are then untested, stamped as such — an
untested gate is never reported as passed). ALL outcomes (including a candidate
failing every gate, and gate 3's NONVARIATIONAL stamp) are first-class records for
J15's uniqueness-or-residual-family report. No gate outcome is a physics selection;
physics adjudication stays with Charles (authority boundary, contract §5).

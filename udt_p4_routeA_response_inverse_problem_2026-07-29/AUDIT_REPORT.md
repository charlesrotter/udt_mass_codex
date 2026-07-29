# P4 Route A Stage 1 — AUDIT REPORT (the posed response inverse problem, TA1–TA6)

Date: 2026-07-29. Branch: `grok`. Preregistration (`PREREGISTRATION.md`) committed at
940c8fe BEFORE the derivation artifacts existed (contract-first confirmed in git by the
verifier). CPU-only exact-SymPy derivation; no solve, no GPU, no candidate, no
canonization, no physics selected.

**GRADE: VERIFIED-WITH-AMENDMENT** — blind adversarial pass (zero-context-framed,
same-session-spawned agent, **not a hosted external model**; caveat travels) returned
**PASS-WITH-REQUIRED-AMENDMENTS** with four amendments (A1: the F-RA1 K₄ component
clause was a false universal quantifier — corrected to character-matched RELATIVE
invariance; A2: the gate-2/gate-4 failure wording would have wrongly failed legitimate
candidates — corrected to character-MISMATCHED dependence; A3: the F-RA2 channel-class
quantifier was false as written — narrowed to the exactly-proven class with the slot
theorem; A4: two clash-scan omissions recorded with resolutions), all applied and
check-backed (`CORRECTION_LAYER.md`; six new zero-residual checks `A6_*`/`B5_*`; rerun
**40/40, exit 0**, deterministic). The core forced statements all SURVIVE independent
re-derivation — the two slips were precision/quantifier errors with well-defined
correct restatements, not load-bearing collapses.

## Result first — the POSED PROBLEM is the principal deliverable, ready for Stage 2

Stage 1 delivers the inverse problem Stage 2 will attack, fully typed and
requirement-formalized, with candidate-free forced structure banked:

- **The typed variation domain 𝒟** (`POSED_INVERSE_PROBLEM.md` §1 +
  `VARIATION_DOMAIN_CENSUS.tsv`, 16 rows): fields (φ; base data), carried moduli
  (λ, k_mod, k10, C) modulo the EXACT K₄ residual, boundary/corner strata of the
  finite cell, completion label — every fork typed BOTH ways, none chosen; tangent
  object identified (T = [[2I₂, Cᵀ],[C, K+Kᵀ]], bilinear transport); the three
  pairing structures (P1/P2/P3) enumerated, NONE adopted.
- **The most general response object 𝓡** (§2): component structure over the census;
  jet-order grading as a declared slot; the L6 fork formalized BOTH ways (Helmholtz as
  a testable gate property, nonvariational case fully in scope).
- **The fifteen requirements formalized** (§3): exact conditions on 𝓡, classified
  **8 POINTWISE / 2 WHOLE-SOLUTION / 4 GLOBAL-COMPLETION** (+ J01–J15 instantiated
  per-row) — verifier-recounted correct.
- **Six executable gate specifications** (`SIX_GATE_SPECS.md`): same-solution closure
  → sector selection → Helmholtz → gauge/Noether → boundary differentiability →
  periods, each a testable pass/fail procedure on a candidate declaration. **No gate
  run; no candidate exists** (F-A1 clean).

**Outcome class: OA1/OA2 MIXED** (verifier-adjudicated as standing with the
amendments): nontrivial candidate-free forced structure exists (F-RA1/F-RA2/F-RA3);
the G01 item is near-null pointwise (F-RA4); most requirement content is
whole-solution/global — the typed problem statement is itself the main deliverable.
**No OA3**: no requirement clash; the one new tension found (below) is
resolution-recorded.

## Target outcomes

| Target | Outcome |
|---|---|
| TA1 census | PASS — 16 rows, every object tagged VARIED / CARRIED-MODULUS (with B-banked quotient) / SUPPLIED / OPEN-FORK; all forks typed both ways with consequences; verifier F-A2 hunt CLEAN; rows 13–14 wording A1-amended (character-matched rule) |
| TA2 domain typing | PASS — 𝒟 typed with the exact K₄ orbifold moduli factor, finite-cell strata, three-gaps placement, tangent object; L7 pairing structures enumerated-not-adopted |
| TA3 general response object | PASS — component structure over the census; jet grading as slot; L6 both ways (F-A3 clean); the §2.4 inverse problem posed, not solved |
| TA4 requirements formalized | PASS — 15 exact conditions + J01–J15 rows; classification 8 PW / 2 WS / 4 GC verifier-recounted; R4 row A3-amended; sampled rows (R4/R8/R12/R5/R9) verifier-confirmed faithful |
| TA5 gate specs | PASS (specs only; none run) — six executable procedures with candidate-declaration inputs; gate 2 FAIL + gate 4 step 2 A2-amended; gate 6 torsion-vacuity scope note added |
| TA6 forced structure | **OA1/OA2 MIXED** — F-RA1/F-RA2 forced in AMENDED form, F-RA3 forced, F-RA4 near-null; all four independently re-derived by the verifier; 40/40 zero-residual checks |

## The four forced items (CORRECTED statements; scope stamps travel)

- **F-RA1 (A1-AMENDED) [POINTWISE — registered chart, one-parameter, off-shell; J07/J11
  untouched].** No Lorentz-invariant member exists in the class (scalar-only so(1,3)
  commutant + founded non-scalar H): the response is forced to be an EQUIVARIANT
  FAMILY, components contragredient to T ↦ Λ⁻ᵀTΛ⁻¹. On the K₄ quotient the forced rule
  is **character-matched RELATIVE invariance per component**: R_v transforms with the
  K₄ character of its paired direction dv; verbatim factoring through the exact
  invariants (a verifier-PROVEN generating set of the full invariant ring) holds
  exactly for components along K₄-invariant directions; R_k10 is χ_a-relative, R_C
  components χ_b/χ_c-relative; character MISMATCH (not bare-linearity) is the failure
  mode. Counterexample on record: ω = k10·dk10 = ½d(k10²).
- **F-RA2 (A3-AMENDED) [POINTWISE on the seat; moduli-VALUE selection untouched —
  07-26 rank zero respected].** Functionals of tr X (first trace) and of det e^{φX}
  are k_mod-blind — NOT every trace/volume/density channel (counter-channel: tr(X²)
  pairs, ∂/∂k_mod = 4k_mod). The exact slot theorem ⟨r_tr·I₂, diag(−1,1)⟩ ≡ 0 holds:
  any k_mod-pairing routes through the trace-free part (d(tr X²)'s does so exactly).
  J06's "determined" branch for k_mod is reachable ONLY with the trace-free screen
  slot k_mod·diag(−1,1) (and/or mixing slots): SLOT PRESENCE forced, no value demanded.
- **F-RA3 [STRUCTURAL/DEFINITIONAL; exact witness].** The response must be defined on
  the FULL typed domain with components along every census direction; restrictions are
  pullbacks AFTER definition (vary-then-restrict); restrict-then-vary is inequivalent
  (witness: restricted critical point (0,0) vs true zero set {(0,−1/2)}, normal
  residual exactly 1). J14's off-shell/on-shell separation is built into the TYPE.
  (Unchanged; verifier-confirmed by own solves.)
- **F-RA4 [POINTWISE; near-null — the OA2 item].** G01 forces ONLY shift-equivariance
  of the φ-dependence (shifts act by left group translation, absorbable into c_E; no
  component may depend on an absolute φ zero-point); nothing further pointwise — the
  every-scalar-f witness blocks functional-form selection. (Unchanged; the verifier
  attempted further forcing and found none.)

## Clash-scan record (A4)

- **Mirror-vs-shift tension (verifier construction; now recorded §3.2):** the φ=0
  mirror/seal interface anchors an absolute φ zero-point; mirror and shift do not
  commute. RESOLUTION (typed, not decided): the interface is SUPPLIED structure whose
  anchor is absorbable into c_E — components may use anchored φ only through
  supplied-structure slots. Not a requirement clash; a Stage-2 candidate checkpoint.
- **K₄-torsion-period vacuity:** the gate-6/R9 period condition on K₄-orbifold cycles
  is vacuous for closed one-forms (2·period = 0); scope note added to gate 6.

## Falsifier record

**F-A1..F-A6: none fired in the final record.** F-A1 (candidate smuggle): NOT FIRED —
EH/Bach/CM0-C appear only as cited jet-order examples / recorded exclusion; no gate
run; pairings enumerated, none adopted (verifier prose hunt CLEAN). F-A2 (census
freeze): NOT FIRED — all 16 rows fork-typed both ways; no modulus fixed (verifier
CLEAN). F-A3 (L6 imposition): NOT FIRED — NONVARIATIONAL is a pass-classification at
gate 3 (verifier CLEAN). F-A4 (bank contradiction): NOT FIRED — every recomputed
banked fact matched Route B/C verbatim (verifier CLEAN). F-A5 (symbolic failure): NOT
FIRED — 40/40, exit 0 (pre-amendment 34/34). F-A6 (quantifier/scope slip): **TWO
F-A6-class slips were caught by the verifier** — the F-RA1 component quantifier and
the F-RA2 channel quantifier, both false as universally stated, both with exact
counterexamples — **amended** (A1/A3) with the counterexamples embodied as
zero-residual checks; the gate-spec infection cured (A2). All other forced statements
carried correct scope stamps.

## LIMITS THAT TRAVEL

1. **Registered chart.** All pointwise statements are registered-positive-triangular-
   chart, one-parameter, off-shell statements on the Route B E02 footing; the K₄
   residual is the chart's exact discrete gauge.
2. **Pointwise scope on the forced items.** F-RA1/F-RA2/F-RA4 are POINTWISE-scoped
   (F-RA3 definitional); the global assignment (J07/J11), whole-solution selection,
   and moduli VALUES are untouched.
3. **Forks typed, not decided.** Const-vs-field moduli, α active-vs-frozen,
   boundary varied-vs-held, completion within-vs-over, c_E promotion, pairing
   P1/P2/P3, L6 variational-vs-not: ALL open; any Stage-2 candidate must declare and
   ledger its stances (gate input D1–D5).
4. **No candidate; no existence/uniqueness verdict.** Stage 1 ends at the posed
   problem + forced structure. Whether the response space ℛ is empty, a point, or a
   family is Stage 2's question — the pre-committed ceiling was respected
   (verifier-confirmed).
5. **No physics.** No action, no equations of motion, no modulus value, no mass, no
   canonization; physics adjudication stays with Charles.
6. **Verifier caveat.** The blind verifier is same-session-spawned, not a hosted
   external model.

## Evidence

`derive_routeA_stage1.py`: **40/40** zero-residual exact-SymPy checks (34 original +
3 `A6_*` from A1 + 3 `B5_*` from A3), exit 0, < 5 s single CPU process, deterministic
(JSON and stdout byte-identical across reruns, JSON sha256 e56025cb…01f6; no floats/
randomness/network). `routeA_stage1_results.json` (amendments field added),
`DERIVATION_STDOUT.txt` — regenerated post-amendment. `POSED_INVERSE_PROBLEM.md`
(A1/A3/A4-amended), `SIX_GATE_SPECS.md` (A2/A4-amended),
`VARIATION_DOMAIN_CENSUS.tsv` (rows 13–14 A1-amended), `EXACT_DERIVATION.md`
(A1/A3-amended), `CORRECTION_LAYER.md` (the amendment record).

## Verifier record

Blind adversarial pass, 2026-07-29 (zero-context framing; same-session-spawned; **not
a hosted external model** — caveat travels). Independent artifacts preserved
in-package (`VERIFIER_INDEPENDENT_CHECK.py`): **31/31 independent checks, exit 0**,
all own constructions — stacked-Kronecker commutant operator (rank 15, nullspace =
span{I}), character-theoretic invariant ring, actual matrix exponential, own solves,
counterexample constructions. **Contract-first VERIFIED in git** (PREREGISTRATION.md
sole file of commit 940c8fe; artifacts later-stamped). Byte-identical rerun twice
(pre-amendment 34/34; JSON sha256 match; stdout byte-for-byte). **The generation
direction PROVEN by the verifier** (the 11 invariants generate the full invariant
ring: character/parity argument + exhaustive degree-≤6 factorization — a strengthening
the package now cites). **Two quantifier catches** (the F-RA1 component clause, the
F-RA2 channel clause) with exact counterexamples (ω = k10·dk10; tr(X²)) → **A1–A4
required**, all applied and check-backed this pass (rerun 40/40, exit 0;
`CORRECTION_LAYER.md`). Prose falsifier hunts F-A1/F-A2/F-A3/F-A4 CLEAN; TA4
classification audit correct; clash-scan adequacy probed with three own constructions
(one real unscanned tension → A4). Outcome-claim adjudication (§7): with A1–A4
applied, OA1/OA2 MIXED stands; no candidate, action, modulus value, or physics
selected anywhere in the package.

## NEXT-STAGE HANDLE (stated as a handle — NOT launched)

Stage 2 attacks the **response-space existence/uniqueness question on the posed
problem**: characterize ℛ = {𝓡 satisfying R1–R15 on the typed domain 𝒟} — empty /
point / family-with-moduli all first-class outcomes (J15 reporting discipline) — with
any candidate entering ONLY through a full declaration (D1–D5) and the six amended
gates, run in sequence. Requires its own preregistration and Charles's go; nothing is
launched by this report.

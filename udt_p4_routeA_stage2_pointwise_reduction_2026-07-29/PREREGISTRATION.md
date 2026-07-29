# P4 ROUTE A — STAGE 2 PREREGISTRATION: the pointwise reduction of the response space (frozen before derivation)

Date: 2026-07-29. Branch: grok. Authorized: Charles launched Route A Stage 2 (2026-07-29), on
the banked Stage-1 posed problem (`udt_p4_routeA_response_inverse_problem_2026-07-29/`,
b5aac4a). DERIVE authority: Stage 2 ONLY — impose the POINTWISE-decidable requirements exactly
and derive the residual space ℛ_PW. NO member of ℛ_PW selected or privileged, NO whole-solution
or global gate run, NO action, NO equations of motion adopted, NO physics. Committed BEFORE the
derivation runs; no retuning after.

## 0. Interrogation declaration

METRIC-LED and OBSERVING. The question is "what EXACTLY survives the eight pointwise
requirements — empty, or a parametrized space, and of what structure?" — not "show a response
exists" and not "kill the space." Emptiness and non-emptiness are both first-class (OB classes
§5); locating KNOWN objects (Einstein/Bach forms) inside the parametrization, if they land
there, is legitimate CHARACTERIZATION (an observation, recorded as such) — never a selection.

## 1. The frozen question and its banked footing

Stage 1 posed: ℛ = { 𝓡 as in POSED_INVERSE_PROBLEM §2 | 𝓡 satisfies R1–R15 } — empty, point,
or family? (POSED_INVERSE_PROBLEM.md §2.4.) Stage 2 computes the POINTWISE layer exactly:

    ℛ_PW = { 𝓡 | 𝓡 satisfies the PW-class requirements: R1, R2, R4, R7(a,b-identities),
             R8, R10, R12, R13 + the PW J-rows J01–J06(slot), J10, J12, J13(slot), J14 } ,

with the WS/GC requirements (R5, R14; R3, R6, R9, R15; J07–J09, J11, J13-completion, J15)
NOT imposed — they are Stage 3's gates acting ON ℛ_PW.

Banked inputs (never re-derived, never adopted): the Stage-1 bank — typed domain, census (16
objects, forks typed both ways), general response object, the four forced items in their
A1/A3-AMENDED form (equivariant family + CHARACTER-MATCHED relative K₄ invariance per component,
with the 11-invariant PROVEN generating set; trace-free screen slot forced for k_mod sensitivity
with the NARROWED channel class; full-domain-before-restriction as type property; G01 ⇒
shift-equivariance only) — plus the Route B bank (E02 footing, two-scalar seat, exact K₄ with
its actions, forcing table) and the Route C bank (jet spread cited as examples only).

## 2. Declared scope (chose-or-derived, out loud)

- **Jet order (Category-A bounded scope, stamp travels — NOT a freeze):** structural results
  derived ORDER-INDEPENDENTLY wherever the argument permits (equivariance, character rule,
  slot structure, provenance grading are order-blind); the EXHAUSTIVE parametrization is
  computed at jet order ≤ 2 in the varied fields (the EH-side of the banked spread); the
  3rd/4th-jet case (Bach-side) is TYPED structurally (which new component shapes appear, why
  the method extends) and stamped NOT-EXHAUSTED. Conflating the two = falsifier F-B3.
- **Fork branches carried, not chosen:** the census forks (moduli constants-vs-fields; α active
  vs frozen; boundary varied-vs-held; completion class) are carried as explicit BRANCHES of the
  parametrization where they change the PW answer, or shown branch-independent (proven, not
  assumed). Silently working in one branch = F-B2.
- **Chart/gauge:** registered chart + local-Lorentz equivariance + exact K₄ (THEORY/DERIVED,
  Route B bank). Components are classified by their K₄ character per the amended rule.
- **Building blocks:** admitted by R1/R13/J12/J04 — census objects, their jets, and banked
  derived structure only; each block's shift-equivariance and K₄ character tabulated.

## 3. Frozen targets

- **TB1 (building-block basis).** The exact table of pointwise building blocks admitted by
  provenance (R1/R13/J12) with J04 shift-equivariance: every block with its census source, its
  behavior under the shift, its local-Lorentz type, and its K₄ character. Zero-residual checks
  for every graded assignment. (This is the alphabet the components may be written in.)
- **TB2 (equivariance reduction).** Solve R7(a)/J10 exactly: for each component type of 𝓡
  (field components R_φ, R_f, R_bh[, R_α]; moduli components R_λ, R_kmod, R_k10, R_C; wall and
  corner slots), derive the exact space of contragredient-equivariant, character-matched maps
  from the TB1 alphabet — computed (basis exhibited per type and grade), not asserted. The
  Noether identity sub-part R7(b) imposed as componentwise identities.
- **TB3 (slot/seat reduction).** Impose R4/J06 exactly on the screen sector: the decomposition
  r_tr·I₂ + r_tf·diag(−1,1) + mixing slots with the forced-slot theorem carried in its
  narrowed form; the exact parametrization of the (λ, k_mod, k10, C) component block consistent
  with the character rule and the slot theorem; the J06 determined-vs-retained branch structure
  made explicit PER FAMILY (no branch chosen).
- **TB4 (the residual space ℛ_PW at the declared scope).** The exhaustive exact parametrization
  at jet ≤ 2: generators, relations, dimension per grade, fork-branch dependence; the R12/J14
  and R8 typing conditions verified on the parametrized family; the 3rd/4th-jet structural
  typing with its NOT-EXHAUSTED stamp.
- **TB5 (the pointwise verdict).** Is ℛ_PW empty at the declared scope? If NONEMPTY: the
  parametrization IS the deliverable; additionally RECORD (observation, not selection) which
  known objects land inside it (the EH-form? the Bach-form? the Stage-1 counterexample shapes?)
  and which banked no-go structures are excluded by which PW requirement. If EMPTY at jet ≤ 2:
  determine whether the emptiness argument is order-independent (⇒ OB3, halt and route to
  Charles) or order-bounded (⇒ OB2, typed).
- **TB6 (the Stage-3 handoff surface).** The exact statement of what the WS/GC gates must
  decide ON ℛ_PW: which moduli-determination branches (J06) remain open per family; which
  parameters the six gate specs (banked) would test; what completion/boundary data each family
  requires (typed per J07/J08 — the cocycle-law type cited, not filled). Stated as a handle,
  NOT launched.

Deliverables: `derive_routeA_stage2.py` (exact SymPy, zero-residual checks, deterministic,
JSON + stdout, exit nonzero on failure), `RESIDUAL_SPACE_LEDGER.tsv` (component type × grade ×
fork-branch → basis/dimension/conditions), `EXACT_DERIVATION.md` (TB1–TB6),
`STAGE3_HANDOFF.md` (TB6), `AUDIT_REPORT.md`, blind-verifier record + preserved independent
script.

## 4. Falsifiers (frozen)

- **F-B1 (candidate smuggle / selection).** Any member of ℛ_PW selected, privileged, or
  described as "the natural/physical one"; any WS/GC gate run on a member. Locating known
  objects in the parametrization is allowed AS OBSERVATION with the recording rule of TB5.
  Fires → the contaminated deliverable is VOID.
- **F-B2 (silent fork freeze).** Any census fork worked in one branch without either carrying
  the branch label or proving branch-independence. Fires → drift flag; branch or prove.
- **F-B3 (jet-order slip).** Any jet ≤ 2 exhaustive result stated without its scope stamp, or
  structural (order-independent) and exhaustive (order-bounded) claims conflated. Fires →
  restate with stamps or void.
- **F-B4 (bank contradiction).** Any statement contradicting the Stage-1 amended forced items
  (using verbatim invariance where the character rule applies; using the pre-A3 channel class),
  the Route B bank, or the Route C bank. Fires → halt, audit before recording.
- **F-B5 (symbolic failure).** Any zero-residual check fails → recorded as-is; exit nonzero;
  no massaging.
- **F-B6 (equivariance by fiat).** Any equivariant-space claim without the exhibited basis
  computation (per type, per grade). The verifier hunts every TB2 space for an assumed-not-
  derived basis.

## 5. Outcome classes and pre-committed ceiling

OB1: ℛ_PW nonempty — the exact parametrization (generators/relations/dimensions per grade and
branch) is the deliverable; known-object locations recorded as observations. OB2: ℛ_PW empty at
jet ≤ 2 but not order-independently — the exact order-bounded obstruction is the deliverable,
typed for higher order. OB3: ℛ_PW empty by an ORDER-INDEPENDENT argument — a major finding
about the requirement set (the postulates under-determine no object at all pointwise); halt
further structure, document exactly, route to Charles. ALL THREE are first-class.

**Maximum-conclusion ceiling (pre-committed):** the strongest bankable statement is "ℛ_PW at
the declared scope is [empty per OB2/OB3 with the exact obstruction | parametrized exactly as
X], fork-branch dependence Y, known objects located at Z (observation), Stage-3 surface W" —
scoped to the registered chart, the declared jet scope, and the carried branches. NO member
selected, NO existence/uniqueness verdict on the FULL ℛ (that needs Stage 3's WS/GC gates), NO
action, NO equations of motion, NO physics — regardless of what the algebra shows.

## 6. Method (same machinery as Stages B/C/A1)

(1) This preregistration committed first. (2) Derivation agent writes the deliverables into the
package; every reduction step (TB1 grading, TB2 bases, TB3 slot algebra, TB4 parametrization,
TB5 verdict computations) is a zero-residual exact-SymPy check; deterministic output. (3) Blind
adversarial verifier (zero-context framing; same-session-spawned — the not-a-hosted-external-
model caveat travels): independent re-derivation of the TB2 equivariant bases and the TB5
verdict, F-B1/F-B2/F-B3/F-B6 hunts across code AND prose, byte-identical rerun, verdict framed
as ADJUDICATE not confirm. (4) Amendments + SAME-verifier closure adjudication. (5)
AUDIT_REPORT.md banks grade + target-outcome table + limits-that-travel + verifier record;
four-check before commit. Anti-hang: pure symbolic CPU; no GPU; no numeric solves; single clean
process; bounded (< 45 min CPU total; if the jet ≤ 2 exhaustion still exceeds budget, reduce to
the diagonal/no-mixing sub-block FIRST, stamp THROUGHPUT-LIMITED, and report the honest
partial — never hang).

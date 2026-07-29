# P4 ROUTE A — STAGE 1 PREREGISTRATION: census, domain typing, and the posed response inverse problem (frozen before derivation)

Date: 2026-07-29. Branch: grok. Authorized: Charles cleared the P4 MAP (B→A staged, C parallel;
2026-07-28) and ordered Route A Stage 1 launched (2026-07-29). Prerequisite delivered: Route B
Stage 1 BANKED (da301b1; VERIFIED-WITH-AMENDMENT; independently replicated with full concordance
on branch p4-routeB — the grok bank rules). DERIVE authority: Route A Stage 1 ONLY — census,
typing, problem-posing, and requirement-forced structure. NO candidate response selected or
privileged, NO action, NO equations of motion, NO lambda/moduli adoption, NO physics. Committed
BEFORE the derivation runs; no retuning after.

## 0. Interrogation declaration

METRIC-LED and OBSERVING. The question is "what IS the configuration space UDT varies over, what
is the most general response object on it, and what do the fifteen audited requirements ALREADY
force about that object before any candidate exists?" — not "construct the response" and not
"show the space is nonempty/unique." Outcome classes OA1/OA2/OA3 (§5) are all first-class,
including the possibility that the requirement set is over-constrained (an inconsistency would be
a major finding routed to Charles, not a failure).

## 1. The frozen question and its banked footing

The missing object (07-24/25/26/28 closure records, quoted in the MAP): "a metric-native
off-shell global-local response one-form on the complete field and finite-cell boundary
configuration space" — the thing whose zeros ARE the field equations. An action, if any, is
downstream (exists only if the response passes Helmholtz/self-adjointness, boundary
integrability, gauge compatibility, period control).

Banked footing this stage stands on (inputs, never re-derived):

- **Route B bank** (`udt_p4_routeB_extension_selection_2026-07-28/`): the full 7-parameter E02
  extension family survives all four constraint layers; L1/L2 are MODULUS-CARRIED; the
  transverse seat is TWO scalars (λ isotropic, k_mod reciprocal-in-screen; the MAP's "E07 k = λ"
  is refuted); carried moduli (λ, k_mod, k10, C) read modulo the EXACT Klein four-group residual;
  conditional descent gates conditional on supplied structure only.
- **Route C bank** (`udt_p4_routeC_shared_static_sector_2026-07-28/`, registry #78): the
  (C2/Bach, EH+Λ) pair shares no exact static sector on the registered domain — no shortcut
  through "the conditional actions agree where it matters" exists for that pair.
- The fifteen requirements (MAP §2, per-item sources = the banked packages; J01–J15 =
  `udt_joint_selector_provenance_audit_2026-07-28/JOINT_OPERATION_OBLIGATIONS.tsv`).
- The three-gap decomposition; the 28+12 typed negative map; the finite-cell canon (mirrored
  cells, CANON); the extension-gate precedence (requirement 10: coframe extension FIRST — honored
  by construction, since the domain is B's E02 footing).

## 2. Frozen targets

- **TA1 (the census — L3 discharged as a deliverable, not a choice).** The exact configuration
  space: every object classified as VARIED FIELD / CARRIED MODULUS (with its B-banked quotient) /
  SUPPLIED STRUCTURE (with its conditionality) / OPEN-FORK ENTRY. Must explicitly cover: the
  depth field φ (equivalently u); the base data (c_E, α, f, b / q_B); the angular-generator and
  mixing moduli (λ, k_mod, k10, C — constants vs promoted to fields: BOTH options typed with
  their consequences, neither chosen); boundary/corner data of the finite cell; the completion
  class (L4: vary within one FC family vs over the class — typed, not chosen); the twist seat
  (L8: α active vs frozen — typed both ways, the two banked twist-adjacent observations cited as
  observations only). Every entry tagged; silent freezes = falsifier F-A2.
- **TA2 (domain typing).** The mathematical type of the configuration space after the
  local-Lorentz quotient (E11 equivariance; scalar-only centralizer and the K₄ residual from B
  applied to the QUOTIENT structure, not re-derived); where the boundary/corner strata sit
  (finite-cell canon; requirement 6); where the three gaps live as explicit moduli directions;
  what a tangent vector to the domain IS (the object the response pairs with) — this TYPES the
  L7 pairing question: enumerate the pairing structures available on the typed domain
  (metric-induced / duality-natural / boundary-extended), each with what it requires, NONE
  adopted.
- **TA3 (the general response object).** The most general form of a metric-native off-shell
  response one-form on the typed domain: component structure over the census; locality grading
  by jet order (with the C-vs-EH jet-order split from the C bank cited as the known spread);
  bulk + boundary + corner slots (requirement 6); the L6 fork formalized BOTH ways — the exact
  (variational) subcase characterized via the Helmholtz condition as a TESTABLE property
  (requirement 8), and the general nonvariational case kept fully in scope (the closure audit
  deliberately phrased the object as a RESPONSE; CM0-C exclusion recorded in C). Demanding
  exactness = falsifier F-A3.
- **TA4 (requirements formalized).** Each of the fifteen requirements translated into an exact
  mathematical condition on the response object over the typed domain, and classified:
  POINTWISE-DECIDABLE / WHOLE-SOLUTION / GLOBAL-COMPLETION — with the J01–J15 rows instantiated
  (J06's transverse/mixing selection stated on the TWO-scalar seat; J10 equivariance stated with
  the exact gauge group + K₄ residual; J14's off-shell/on-shell separation built into the
  object's definition). Requirement 4 (trace-free anisotropic screen response) made exact on the
  banked seat decomposition.
- **TA5 (the six-gate sequence instantiated).** The exact executable specification of each gate
  (same-solution closure → sector selection → Helmholtz → gauge/Noether → boundary
  differentiability → periods) as it applies to a candidate response ON THIS TYPED DOMAIN —
  written as testable procedures with pass/fail conditions. NO gate is RUN in Stage 1 (there is
  no candidate; running gates on a smuggled candidate = F-A1).
- **TA6 (requirement-forced structure — the bounded derivation).** What requirements 1–15
  ALREADY force about the response's component structure at the pointwise level, candidate-free,
  each forced statement a zero-residual check: at minimum (a) what J10 equivariance +
  the scalar-only-centralizer/K₄ facts force on the response's covariance type; (b) what
  requirement 4 + J06 force on the screen-sector components over the two-scalar seat; (c) what
  requirement 12 (restrict-then-vary FORBIDDEN) + J14 force structurally (domain-before-
  restriction ordering as a property of the object, not a practice); (d) what the additive-depth
  composition law (G01) forces on the response's φ-dependence at the pointwise level, if
  anything — reported as-is if nothing. Each item's scope stamp (pointwise vs global) mandatory;
  conflation = F-A6.

Deliverables: `derive_routeA_stage1.py` (exact SymPy where derivations occur — TA6 and any TA2/
TA4 identities; zero-residual checks; JSON + stdout; deterministic; exit nonzero on failure),
`VARIATION_DOMAIN_CENSUS.tsv` (TA1, one row per object, tags + quotients + fork entries),
`POSED_INVERSE_PROBLEM.md` (TA2+TA3+TA4: the typed domain, the general response object, the
fifteen formalized conditions — the document Stage 2 will attack), `SIX_GATE_SPECS.md` (TA5),
`EXACT_DERIVATION.md` (TA6 + all derived identities), `AUDIT_REPORT.md`, blind-verifier record +
preserved independent script.

## 3. Falsifiers (frozen)

- **F-A1 (candidate smuggle).** Any specific response/action selected, privileged, or used as
  "the natural form" (incl. EH/Bach/CM0-C forms entering as anything but cited jet-order
  examples), or any gate RUN on a candidate. Fires → the contaminated deliverable is VOID.
- **F-A2 (census freeze).** Any DOF or modulus silently frozen or fixed (λ, k_mod, k10, C, α,
  completion class, boundary data). Fires → drift flag; free it or ledger it explicitly.
- **F-A3 (L6 imposition).** Variationality/Helmholtz demanded as a filter on the object's
  definition rather than formalized as a testable gate property. Fires → the definition is VOID
  (imported least-action reflex).
- **F-A4 (bank contradiction).** Any statement contradicting the B bank (7-param survival,
  two-scalar seat, K₄ exactness, rank-zero pointwise set), the C bank (#78), or the joint-
  selector no-go structure. Fires → halt, audit before anything is recorded.
- **F-A5 (symbolic failure).** Any zero-residual check fails → recorded as-is; exit nonzero; no
  massaging.
- **F-A6 (quantifier/scope slip).** Pointwise-forced conflated with globally-forced;
  subfamily-forced stated as domain-forced; "the response must" without its scope stamp.
  Verifier hunts every forced statement.

## 4. Premise ledger (chose or derived — each tagged)

| Premise | Tag |
|---|---|
| E02 moduli-carrying footing (7 params; two-scalar seat; K₄ quotient) | DERIVED (Route B bank da301b1; replication-stable) |
| Fifteen requirements as the constraint set | THEORY (MAP §2; per-item banked sources; J TSV) |
| Response one-form as the object's type (not an action) | THEORY (closure-audit localization; L6 fork carried BOTH ways inside it) |
| Finite-cell boundary/corner structure | CANON (mirrored finite cells) + THEORY (requirement 6) |
| Local-Lorentz quotient handling = equivariance | DERIVED (07-26 correction; B bank) |
| Registered positive triangular chart | THEORY (E02 registration; B's T1 covariance stratification cited where chart-dependence matters) |
| Census/completion/twist entries | OPEN-FORK — typed both ways in TA1, NEVER chosen here |
| SymPy/CPU, bounded, single process, no GPU | Category-A conditioning (soundness only) |
| NO candidate, action, EOM, physics, adoption | EXCLUDED (authority boundary — unchanged) |

## 5. Outcome classes and pre-committed ceiling

OA1: the requirements force nontrivial candidate-free structure on the response (the forced
identities bank, each scoped). OA2: the requirements are largely non-restrictive at the
pointwise level — the honest finding is that the inverse problem's content is global/whole-
solution, and the typed problem statement IS the deliverable. OA3: an inconsistency or
over-constraint among the fifteen requirements surfaces — halt derivation of further structure,
document the clash exactly, route to Charles (a finding about the requirement set itself).
ALL THREE are first-class.

**Maximum-conclusion ceiling (pre-committed):** the strongest bankable statement is "the
variation domain is typed as X (census attached); the general response object has form Y; the
fifteen requirements formalize to Z with classification; requirements force W at the pointwise
level, scoped" — plus, in OA3, "requirements i and j clash on the typed domain, exactly thus."
NO candidate response, NO existence/uniqueness/emptiness verdict on the response space (that is
Stage 2+), NO action, NO equations of motion, NO physics — regardless of what the formalization
shows.

## 6. Method (same machinery as Routes B/C)

(1) This preregistration committed first. (2) Derivation agent writes the deliverables into the
package; every derived identity (TA6, and TA2/TA4 identities) is a zero-residual exact-SymPy
check; the typing/formalization documents cite banked sources per claim; deterministic output.
(3) Blind adversarial verifier (zero-context framing; same-session-spawned — the
not-a-hosted-external-model caveat travels): independent re-derivation of every TA6 forced
statement, F-A1/F-A2/F-A3/F-A6 hunts across ALL documents (incl. the prose ones — a candidate
smuggle or census freeze in prose is as void as in code), byte-identical rerun, verdict framed
as ADJUDICATE not confirm. (4) Amendments + SAME-verifier closure adjudication (the B/C process
note). (5) AUDIT_REPORT.md banks grade + target-outcome table + limits-that-travel + verifier
record; four-check before commit. Anti-hang: pure symbolic CPU; no GPU; no numeric solves;
single clean process; bounded (< 30 min CPU total; reduce and stamp THROUGHPUT-LIMITED rather
than hang).

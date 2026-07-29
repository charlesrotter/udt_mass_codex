# P4 ROUTE A — STAGE 3 (SLICE 1) PREREGISTRATION: the candidate-free gate cuts on ℛ_PW (frozen before derivation)

Date: 2026-07-29. Branch: grok. Authorized: Charles's standing go for Stage 3 (2026-07-29,
recorded at 0ce9548), launch-gated on the Stage-2 bank — now satisfied (2c0e7cc). DERIVE
authority: Slice 1 ONLY — the candidate-free (typing/partition) parts of the WS/GC gates acting
on the banked residual space ℛ_PW. NO member of ℛ_PW selected or privileged, NO solutions of
𝓡=0 computed, NO completion class chosen, NO action adopted, NO physics. Committed BEFORE the
derivation runs; no retuning after.

## 0. Interrogation declaration

METRIC-LED and OBSERVING. The question is "how do the gates PARTITION the parametrized space —
which sub-families pass, fail, or split, per gate, per pairing branch, per stratum?" — not
"find the surviving candidate." The L6 response-vs-action fork is NOT decided here: gate 3
turns it into a COMPUTED PARTITION of ℛ_PW (locally-exact vs nonvariational members, per
declared pairing), with both cells first-class. An empty cell in ANY partition (e.g. no
Helmholtz-exact member under any enumerated pairing) is a first-class finding, not a failure.

## 1. The frozen question and its banked footing

Inputs (banked, never re-derived; every use carries the source's own stamps):
- **ℛ_PW** (`udt_p4_routeA_stage2_pointwise_reduction_2026-07-29/`, 2c0e7cc): the stratified
  parametrization — character-matched modules over the anchored alphabet; generic stratum
  identity-free; the exhaustive codim-1 cut at k_mod=0; deeper C≠0 cuts typed-not-exhausted;
  the witness table; STAGE3_HANDOFF.md is the binding input surface.
- **The six gate specs** (`udt_p4_routeA_response_inverse_problem_2026-07-29/SIX_GATE_SPECS.md`,
  as amended: character-mismatch failure conditions; strata carried; torsion-vacuity note).
- **The GR-analog shortlist** (`udt_gr_analog_reconnaissance_2026-07-29/`, b198113) — machines
  used as METHOD under the lane clause: pairing-relative Helmholtz (bicomplex; VERIFIED row);
  wall/corner jet-slot bookkeeping (VERIFIED); integrability-complex typing (VERIFIED);
  twisted-cocycle holonomy (its underlying twisted-H¹ row is MODEL-KNOWLEDGE — see F-S7).
- The requirement classifications (R3/R6/R9/R15 GC; R5/R14 WS; the J-rows) from the banked
  posed problem.

## 2. Slice boundary (chose-or-derived, out loud)

- **IN Slice 1 (candidate-free — computable on the parametrization):**
  - **G3 (Helmholtz partition).** For each enumerated pairing (P1 constrained-volume / P2
    declared-dual / P3 stratum-trace — banked enumeration, NONE adopted): partition ℛ_PW into
    LOCALLY-EXACT vs NONVARIATIONAL members via the pairing-relative self-adjointness
    condition at jet ≤ 2 (the banked exhaustive layer). Pairing-dependence of the partition is
    itself a deliverable (Route B T4 volume-blindness loci cited).
  - **G1-typing (integrability complex).** The compatibility-complex structure of {R_i = 0}
    over the parametrized family: generic stratum (no identities — the determined regime) AND
    carrying the k_mod=0 identity (the constrained regime); NO Bianchi-type identity assumed
    (banked input). Typing only — no solution existence claimed.
  - **G5-typing (wall/corner slot census).** Per jet order (≤ 2 exhaustive; 3/4 typed), the
    unpaired-slot bookkeeping on the mirrored finite cell (parity + sector split + anchored-φ
    rule): which sub-families CAN pair every wall/corner slot from their own components, which
    require boundary data of a type the census forbids. The counterterm move is NOT available
    (Category-B; banked). Route C TC5 anchors the known instances.
  - **G6-typing (holonomy/periods).** The type-level classification of period/holonomy
    obligations for the closure data (the banked two-sided twisted cocycle; K₄-torsion
    vacuity note carried); classification of WHAT gate 6 would test per sub-family — no
    period computed on a solution.
- **OUT of Slice 1 (= the Slice-2 surface, typed at the end, not run):** gate 2 (sector
  selection — needs sources/sectors), the WS requirements R5/R14 and gate 1's on-shell
  closure leg (need solutions of 𝓡 = 0), gate 4's current-conservation leg, any completion-
  class commitment (L4 fork stays open), any boundary-data choice (BR-B fork stays open).
- **RESONANCE RULE (inherited, binding):** any adjudication SPECIFIC to a sub-family
  contacting the resonance locus (λ∓k_mod ∈ {±1} beyond the codim-1 stratum's banked
  identity) is DEFERRED — marked CENSUS-REQUIRED — until the queued deeper-census tile runs.
  Generic-stratum and k_mod=0-stratum adjudications proceed (their identity content is banked
  and exhaustive at codim 1).

## 3. Frozen targets

- **TC1 (the Helmholtz partition).** The exact partition of ℛ_PW per pairing branch, with
  generators/conditions for each cell; the pairing-dependence map; the EH-form's and ω-shape's
  cell locations recorded as observations (F-S1 discipline). If a cell is EMPTY under every
  enumerated pairing, that emptiness is stated with its exact obstruction.
- **TC2 (the integrability typing).** The compatibility-complex type of the family: generic
  (determined) regime vs the k_mod=0 constrained regime; what gate 1's on-shell leg would
  need per cell (typed).
- **TC3 (the boundary census).** The slot-pairing partition: sub-families that self-pair all
  wall/corner slots at jet ≤ 2 vs those structurally unable; the 3/4-jet typing; the mirrored-
  parity constraints made explicit per cell.
- **TC4 (the period typing).** Per cell: the period/holonomy obligations gate 6 would impose,
  classified (vanishing-by-torsion / quantization-typed / needs-completion-data).
- **TC5 (the joint gate-cut map).** The composite partition of ℛ_PW by (G3-cell × G1-type ×
  G5-status × G6-type), per pairing branch and stratum — THE deliverable. Every cell carries:
  its parametrization, its open forks, its CENSUS-REQUIRED flags, and what Slice 2 must
  decide on it.
- **TC6 (the Slice-2 surface).** The exact statement of the remaining work per surviving
  cell: the WS legs, gate 2, the completion/boundary forks, with cost-shape estimates. A
  handle, NOT a launch.

Deliverables: `derive_routeA_stage3.py` (exact SymPy, zero-residual checks, deterministic,
JSON + stdout, exit nonzero on failure), `GATE_CUT_LEDGER.tsv` (cell × gate × pairing ×
stratum → status + conditions), `EXACT_DERIVATION.md`, `SLICE2_SURFACE.md`, `AUDIT_REPORT.md`,
blind-verifier record + preserved independent script.

## 4. Falsifiers (frozen)

- **F-S1 (selection).** Any member/cell selected, privileged, ranked, or called natural/
  physical; known-object locations are observations only. Fires → contaminated deliverable VOID.
- **F-S2 (pairing chosen).** Any G3 result stated without its pairing-branch label, or a
  pairing silently adopted. Run per branch or prove branch-independence. Fires → restate/void.
- **F-S3 (stratum-blind gloss — the NAMED recurring error class, two prior catches).** Any
  "only / all / none / exhaustive / vacuous / empty" claim without its stratum scope stamp.
  The verifier hunts these FIRST, on every partition statement. Fires → restate with scope
  or void.
- **F-S4 (bank contradiction).** Contradicting the Stage-2 stratified parametrization (incl.
  its amended cut structure), the gate specs as amended, Routes B/C, or the resonance rule.
  Fires → halt, audit.
- **F-S5 (symbolic failure).** Recorded as-is; exit nonzero; no massaging.
- **F-S6 (WS smuggle).** Any solution-dependent conclusion (existence of solutions, on-shell
  closure, current conservation, mass/volume/density values) claimed from typing-level
  computation. Fires → claim VOID (it belongs to Slice 2).
- **F-S7 (MODEL-KNOWLEDGE reliance).** The twisted-H¹ analog row is MODEL-KNOWLEDGE: it may
  guide method but may NOT underpin a banked G6 claim without prior source verification. Any
  G6 statement leaning on it carries the flag or is void.

## 5. Outcome classes and pre-committed ceiling

OS1 (expected): the joint gate-cut map — a partition with populated cells, per pairing and
stratum, forks carried. OS2: some gate EMPTIES ℛ_PW under all pairing branches at the declared
scope — a major structural finding (e.g. "no pointwise-admissible response can pair its own
boundary slots"); halt further cutting, document the obstruction exactly, route to Charles.
OS3: the cuts collapse ℛ_PW to a rigid low-parameter subfamily — reported exactly, NOT
promoted (selection is Charles's, and Slice 2's WS legs are still undischarged). ALL are
first-class.

**Maximum-conclusion ceiling (pre-committed):** the strongest bankable statement is "the gates
partition ℛ_PW as [map], per pairing branch and stratum, with [cells] CENSUS-REQUIRED and
[forks] open; the L6 fork is now the computed partition [X]" — NO member selected, NO
existence/uniqueness verdict on full ℛ (Slice 2 + the WS legs remain), NO action, NO physics,
regardless of what the algebra shows.

## 6. Method (same machinery as Stages 1/2)

(1) This preregistration committed first. (2) Derivation agent writes the deliverables; every
partition condition and cut is a zero-residual exact-SymPy check; deterministic. (3) Blind
adversarial verifier (zero-context; same-session-spawned caveat travels): independent
re-derivation of the G3 partition and at least one G5 census cell, F-S1/F-S2/F-S3/F-S6 hunts
across code AND prose (F-S3 first), byte-identical rerun, ADJUDICATE framing. (4) Amendments +
SAME-verifier closure (multi-round if needed — the Stage-2 precedent). (5) AUDIT_REPORT.md +
four-check before commit. Anti-hang: pure symbolic CPU, single process, no GPU, bounded
(< 45 min total; reduce per the declared scope ladder — drop 3/4-jet typing first, then the
P3 pairing branch, stamping THROUGHPUT-LIMITED — never hang).

# P4 cold adversarial review — frozen execution contract

Date: 2026-08-01  
Base: `2e93a621aeeee0a0844543068363d0ba94094357` (exact post-A3 `grok` tip)  
Branch: `codex/p4-cold-adversarial-review-2026-08-01`  
Authorization: Charles, current session: “launch the cold adversarial P4 review.”

Status: **PREREGISTERED BEFORE REVIEWER CONTENT INSPECTION OR OUTCOME WORK**. This contract turns
`P4_COLD_ADVERSARIAL_REVIEW_SUGGESTION_2026-08-01.md` into a bounded execution. It authorizes only
a cold evidence regrade. It does not authorize T4, a new derivation, physics adoption, canonization,
GPU work, a response law, carrier, source, boundary, mass interpretation, or branch selection.

## 1. Observing, not targeting

Whole question: does the accumulated P4 evidence through A3 support its banked, premise-scoped
claims when a fresh reviewer reconstructs provenance, quantifiers, algebra, independence, and
scope without being told which claims should survive?

This is **metric-led evidence auditing**, not a search for mass, particles, integers, or a preferred
law. `RETAINED`, `NARROWED`, `CONTRADICTED`, and `OPEN` are equally acceptable. The reviewer must
attack claims favorable to the standing UDT picture at least as hard as negative claims.

## 2. Frozen scope

`build_preregistration.py` mechanically freezes:

- all 29 package-headline bundles, rows 0–28 of `P4_ARC_SUMMARY_2026-07-31.md`;
- the eight cross-cutting questions in the cold-review suggestion;
- every tracked file under those 29 package directories;
- current premise/control sources and the explicitly named nuclear-scoping material.

The resulting `FROZEN_REVIEW_UNITS.tsv`, `SOURCE_INVENTORY.tsv`, `SOURCE_MANIFEST.sha256`, and
`PREREG_SNAPSHOT.json` are immutable review inputs. A package-headline bundle may contain several
clauses; the reviewer must split every load-bearing clause into separately graded rows. It may add
a missed claim only as `DISCOVERED_LOAD_BEARING_CLAIM`, with source and reason. Generated review
records may not change selection or scope.

Excluded: pre-P4 material unless directly cited by a frozen P4 source; empirical fitting; GPU or
long numerical solves; new mechanisms; changes to existing evidence, controls, registries, scripts,
data, manifests, or research artifacts.

## 3. Premise ledger for this review

- Review base, source bytes, bank commits: **pinned-by-THEORY** (Git and frozen inventory).
- Claim set: **pinned-by-THEORY** (current P4 summary plus the eight authorized questions).
- Algebraic method/basis: **free-and-explored**, but every recomputation must state whether it is
  genuinely independent, same-code regression, manual proof, symbolic re-expression, or unrun.
- Physical values, boundary conditions, signs, charts, sources, carriers, actions, postures,
  censuses, topology forks, and response laws: **not chosen by this review**. The reviewer carries
  the exact source stamp or flags the claim.
- Acceptance criteria: provenance, internal consistency, mathematical validity, scope fidelity,
  and reproducibility only. No expected physical shape or favored outcome is an acceptance gate.

## 4. Mandatory attack layers

1. **Provenance and quantifiers.** Audit response alphabet, variation domain, pairing, wall posture,
   census, topology, lock/spatial readings, fixed-vs-family quantifiers, and every conditional mass
   definition. Explicitly distinguish `DERIVED`, `CHOSE`, `WORKING`, `OPEN`, `CONDITIONAL`,
   `POSIT`, and `OBSERVED`.
2. **Independent algebra.** Recompute every load-bearing identity using a different route where
   practical. Mandatory named clusters: inverse-domain/response parametrization; Noether cut;
   seam/wall coefficients; period and real-vs-circle statements; absorption/dichotomy stability;
   time-live embeddings; angular reading/mode claims; A3 cap, Hopf, holonomy, and C1 recovery.
3. **Independence map.** Identify shared parsers, source tuples, generated ledgers, symbolic
   expressions, inherited assumptions, and any verifier that merely checks its own producer.
4. **Completeness.** For every claim record what fields, action terms, equations, domain, boundary,
   topology, dynamical character, branches, stability, and regime it covers or drops. A bounded
   tile cannot become a whole-theory verdict.
5. **Regrade.** Exactly one of `RETAINED`, `NARROWED`, `CONTRADICTED`, or `OPEN`, with a precise
   replacement sentence. No silent strengthening.

## 5. Required outputs

- `MECHANICAL_CLAIM_REGRADES.tsv`: one row per exploded load-bearing claim, including every frozen
  package unit and all discovered claims.
- `PREMISE_QUANTIFIER_AUDIT.tsv`.
- `INDEPENDENT_RECOMPUTATION_LEDGER.tsv` with commands/methods, outputs, residuals, and evidence.
- `SHARED_CODE_CIRCULARITY_MAP.tsv`.
- `COMPLETENESS_MAP.md` applying all ten completeness criteria.
- reviewer-built runnable CPU/symbolic scripts and raw stdout/stderr.
- `REVIEW_RESULTS.json`, `AUDIT_REPORT.md`, and `REVIEW_MANIFEST.sha256`.
- one smallest justified next step, or `STOP_REPAIR_FIRST`.

Every output must be written only under this review package. Existing evidence is read-only.

## 6. Falsifiers and fail-closed gates

- F1: wrong base, altered frozen source, missing/duplicate review unit, or missing package row.
- F2: any headline bundle not exploded until every load-bearing clause is graded.
- F3: a conclusion whose premise stack is weaker than its source.
- F4: fixed-family/fixed-metric or existence/universality quantifier substitution.
- F5: same-code replay labeled independent; tautological digest/copy checks; unexercised guards.
- F6: a conditional definition narrated as physical mass, law, carrier, source, or dynamics.
- F7: compact-circle/integer conclusions imported from topology not owned by the tested domain.
- F8: dropped fields, sectors, branches, boundaries, or limits hidden rather than recorded.
- F9: nuclear/SEMF comparison promoted above `CONSISTENCY-DEMO` without new independent evidence.
- F10: edits outside the review package, GPU work, or new science.

Any F1/F2/F10 event halts. Other unresolved events force `NARROWED`, `OPEN`, or
`STOP_REPAIR_FIRST`, never an optimistic pass.

Catch-proofs required from the final verifier: missing unit; duplicate unit; source-byte mutation;
quantifier weakening; false-independent label; missing premise stamp; and an edit outside package.

## 7. Isolation and verification pipeline

The primary reviewer must be a fresh zero-context agent pointed first to this preregistration. It
must not read `LIVE.md` or `HANDOFF.md` before the frozen inputs and must receive no summary of the
expected result. CPU only. Its return remains unbanked until a second fresh adversarial verifier
checks coverage, independent recomputations, catch-proofs, source immutability, and the maximum
conclusion. Required amendments return to the original reviewer, then to the same verifier until
closed. Driver four-check, premise verifier, manifests, tests, and clean-tree audit follow.

## 8. Maximum conclusion

A claim-by-claim cold regrade of P4 through A3, plus the smallest justified next step. The review
may say the architecture is sound, requires narrowing, contains contradictions, or must be repaired.
It cannot supply affirmative new UDT physics, select a law or branch, or canonize anything.


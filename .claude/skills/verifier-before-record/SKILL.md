---
name: verifier-before-record
description: Use before promoting any scientific result or claiming a synthesis is reviewed; labeled draft checkpoints remain recoverable without scientific promotion.
---

# Verifier-before-record (binding)

Every scientific result gets a blind adversarial verifier pass, recorded with the reviewer's
identity and date, before promotion or an accepted-result commit. Negative scientific results are
first-class and receive the same scrutiny.

A draft, failed attempt, incomplete explanation, or candidate synthesis may be saved in a clearly
labeled checkpoint before review. The checkpoint must identify its source snapshot, scope,
limitations, and review state; it does not promote science, alter registry grades, or silently become
an accepted dependency. Calling a synthesis `FIDELITY_REVIEWED` still requires a real separate-context
review proportional to what the synthesis changed.

## A clean blind pass requires
- FRESH ZERO-CONTEXT instance (no conversation history). For load-bearing / native-vs-import /
  "must-quantize"-class verdicts, use a fresh instance and/or a different model family (P4) — a
  same-context same-model subagent shares blind spots.
- ADVERSARIAL stance: try to BREAK the claim, not confirm it. Default to skepticism; concede
  only what cannot be refuted.
- INDEPENDENTLY RE-RUN the key computation/tests; report the real numbers vs the claim.
- Hunt FALSE PASSES: tautologies, vacuous asserts, loose tolerances that would pass a broken
  result, circular references, a check that secretly reuses the thing it tests.
- For a test harness: REDO the catch-proof (reintroduce each bug, confirm the matching test
  goes RED). An untested guard is decoration.
- Verdict: VERIFIED / VERIFIED-WITH-CAVEATS / REFUTED, with concrete reasons. Distinguish
  "PROVEN to machine precision" from "CONSISTENCY-checked / REGRESSION-locked."
- Leave the repo EXACTLY as found (restore scratch edits; note UNTRACKED files won't
  `git checkout` back — back them up manually).

## Fidelity review for an accepted-source synthesis

- Check the actual source versions, definitions, premises, domains, labels, and logical seams.
- Ask whether the explanation strengthens a theorem, hides a premise, changes an object, or skips a
  necessary connection; report the exact defective step and strongest surviving statement.
- Re-run only the underlying checks made load-bearing by the editorial change. Record what was not
  replayed; do not pretend a bounded fidelity review re-proved every source package.
- A review verdict applies to the synthesis. It does not upgrade source evidence, adopt a premise,
  establish empirical truth, or confer canonical status.

## Cross-model escalation (load-bearing calls — P4)
For NATIVE-vs-IMPORT classifications, "must-quantize"-class verdicts, and CANON candidates, ALSO
run a verifier on a DIFFERENT Claude tier (Agent `model=` param, e.g. driver=opus -> sonnet), fresh
zero-context, pointed at the source docs NOT the prior verdict. Log the cross-model agent's
id+model+verdict; a DISAGREEMENT is resolved or escalated to Charles, NEVER dropped — and if it
refines a classification, update the source-of-truth. Protocol = `CROSS_MODEL_VERIFY.md`.

## Aim
Aim verifiers HARDEST at results that CONFIRM the standing hypothesis (hypothesis discipline:
"find what's real, not what confirms priors"). Record caveats; CLOSE or explicitly SCOPE them
before banking. Pre-register falsification contracts before the test runs; no retuning after.

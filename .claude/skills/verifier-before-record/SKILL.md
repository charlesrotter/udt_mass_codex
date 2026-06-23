---
name: verifier-before-record
description: Use before committing or recording ANY result (positive OR negative). Defines what a clean blind adversarial verifier pass requires; binding repo discipline.
---

# Verifier-before-record (binding)

Every result gets a BLIND ADVERSARIAL verifier pass, recorded in its results doc with the
verifier's agent id + date, BEFORE commit. Negative results are first-class — they get the
same pass.

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

## Aim
Aim verifiers HARDEST at results that CONFIRM the standing hypothesis (hypothesis discipline:
"find what's real, not what confirms priors"). Record caveats; CLOSE or explicitly SCOPE them
before banking. Pre-register falsification contracts before the test runs; no retuning after.

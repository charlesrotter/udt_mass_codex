# Fresh Adversarial Review — Semantics and Causal Interpretation

Date: 2026-07-19  
Review contexts: `/root/copresence_conceptual_adversary`, then
`/root/copresence_final_semantic_review`  
Mode: fresh zero-context, read-only, CPU-only

## Initial verdict

`PASS-WITH-CAVEATS`

The reviewer accepted the central negative and conditional conclusions but required:

- type-correct whole-solution notation `S=(M_S,g,Phi,...)` with events in `M_S`;
- “causal partition” demotion to lay shorthand for event-relative reachability;
- separation of static-chart coordinate time, null proper time, and detector-clock time;
- treatment of both boundary retuning and localized intervention as counterfactual comparisons between
  solutions with different held-fixed data;
- conditional, not affirmative, source/star/signal language;
- removal of physical-calibration and UDT-uniqueness leakage;
- correction of C11 to `DERIVED` insufficiency and C19 to `REJECTED_AS_INFERENCE` uniqueness;
- stronger variable-lapse, principal-symbol, and zero-set checks.

## Final-review break tests

After those corrections, a second fresh context found three remaining failures:

1. the report reused `S` as both whole solution and source event;
2. the executable called the star candidate an “observed emission event” without the conditional
   signal-coupling premise;
3. the verifier did not read the lay tree or premise ledger and falsely passed disposable-copy
   mutations that made the star signal unconditional or made only one counterfactual side explicit.

The reviewer reproduced the then-current derivation and verifier byte-identically at 23/23, 30/30,
and 29/29 before demonstrating those false passes.

## Applied correction

- The remote source event is now `R_src`; `S` remains the whole solution only.
- The executable check is named `candidate_star_emission_offset_is_null_related` and its source comment
  carries the signal-follows-characteristic condition.
- The verifier now reads and hashes the lay tree and premise ledger, requires the conditional star
  language and both-counterfactual statement, and exercises RED mutations for each.
- The verifier also binds the post-prereg correction, transcript result hash, requirements, and
  repository-gate script.

## Closure replay

`PASS`. The same final reviewer independently replayed copied scripts at 23/23 derivation, 30/30
verification, and 35/35 catches. Disposable-copy mutations of the lay signal conditional,
counterfactual symmetry, and premise-ledger scalar promotion all failed as required. The 16-entry
package manifest replayed completely. No source file was modified by the reviewer.

# External-review correction preregistration

Date: 2026-08-11  
Base result preregistration commit: `09056c83`  
External reviewer: Codex `gpt-5.4`, sealed read-only 37-file intake

## Trigger

The cold review returned `VERIFIED_AFTER_SPECIFIED_CORRECTIONS`. It reproduced the scientific
landing and exact source/family/query counts, but found three evidence-labeling defects:

1. `verify_cmb_query_map_independent.py` independently checks saved-artifact consistency without
   importing the renderer, but it does not independently derive semantic ownership from the
   sixteen source texts.
2. `run_catch_proofs.py` imports that validator, so its ten exercised mutations are fail-closed
   artifact guards rather than an independent second proof.
3. `derive_cmb_query_map.py` is a deterministic renderer of preregistered, source-audited semantic
   judgments, not an algorithm that derives those judgments from natural-language sources.

The reviewer also correctly did not run the repository-wide gate script from inside the sealed
intake, because doing so would have exceeded the authorized 37-file boundary.

## Frozen scientific content

The following may not change during this correction:

- the exact sixteen-source universe and every source SHA-256;
- the `F00`--`F17` universe, ordering, and family classifications;
- all 14 query-layer rows and all four observable-channel rows;
- the spectrum-versus-power counterexample;
- the counts `10,080` C0 roots and `15,420` C1 matrix elements;
- the conclusion that no family in the bounded universe owns a complete physical CMB realization;
- the next proposed F01/F02 common-query Jacobi calculation and its pre-eigensolve stop boundary.

## Authorized correction

Only the evidence descriptions and corresponding machine-readable metadata may change:

- relabel the local verifier as an artifact-consistency verifier;
- relabel the ten mutations as catch proofs of that validator;
- identify the production script as a deterministic renderer;
- record the cold review as the independent semantic source audit;
- update the audit report, exact derivation, dispatch/readme references, and generated JSON names or
  fields needed to carry those labels honestly;
- preserve the raw external verdict and add an adjudication record.

The existing preregistration remains immutable historical evidence. This correction layer must not
silently rewrite what was originally promised.

## Certification contract

The correction is accepted only if:

1. all frozen source hashes and all scientific tables remain byte-identical;
2. the artifact-consistency verifier still passes `21/21`;
3. the validator catch proofs still pass `10/10`;
4. the exact spectrum/power countermodel still passes `6/6`;
5. the external semantic review and this adjudication are both preserved;
6. repository tests, current premises, six frozen manifests, current paths, links/frontier, and
   protected-untracked metadata gates replay successfully;
7. no protected file is opened, modified, staged, or included.

## Maximum conclusion

At most `VERIFIED_AFTER_SPECIFIED_CORRECTIONS`: within the frozen sixteen-source/F00--F17 universe,
the CMB observation-query architecture and ownership census survive independent semantic review,
while the local machine checks certify artifact consistency rather than semantic derivation.


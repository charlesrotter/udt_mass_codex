# G261 fresh external adversarial review

Reviewer: external Codex `gpt-5.4`, high reasoning

Disposition: `ACCEPT_WITH_REPAIRS`

## Reviewer return

I verified all 29 entries in `/intake/REVIEW_MANIFEST.tsv`: every declared SHA-256 and byte count
matched on disk. I then copied the intake to `/return/work`, reran the four registered commands from
the G261 package, and the regenerated outputs matched the packaged outputs byte-for-byte.

### Defects

1. The production “derivation” is not premise-driven; it is a hard-coded classification emitter.
   `derive_w4_ownership.py` literalizes the ownership table, witnesses, landing, and remaining-
   premise type without reading `founding.md`, the ledgers, or the G259/G260 sources. The 257-case
   loop checks only signature/determinant algebra.
2. The “independent verification” is only artifact-independent, not logically independent.
   `verify_independent.py` hard-codes the same ten classifications and final landing, while the
   seven separators are literal boolean tuples. `EVIDENCE_GATES.md` overstates what it proves.
3. The hostile-mutation evidence is overstated. `run_catch_proofs.py` only reads
   `DERIVATION_RESULT.json` and confirms conservative labels are already present. No mutations are
   generated or applied, so “10/10 hostile catches” must be downgraded to regression consistency.
4. The Levi-Civita item needs stricter typing. W4 says only that one metric supplies clocks, rulers,
   free fall, and null propagation, and explicitly does not select locality/order/equations. The
   package prose correctly adds “with the already supplied Lorentz-metric/Levi-Civita geometry,” so
   the machine classification must preserve that qualifier instead of plain `DERIVED_FROM_W4`.

### Strongest bounded landing

The bounded substantive landing is still supportable: W4 supports one universally coupled physical
metric and, with the pre-existing Lorentz/torsion-free/metric-compatible geometry, local inertial,
free-fall, and null semantics; it does not alter the F1--F4 metric formula, and it does not derive
the G259 operator class.

Premise/type corrections:

- W4 remains `WORKING/POSIT_NOT_CANON`.
- The Levi-Civita conclusion is derived from W4 plus existing metric geometry, not W4 alone.
- “One dynamics-generator premise remains” is acceptable only as one broad remaining premise
  family, not one uniquely identified mechanism.

### Independence audit

Packaging independence passed narrowly: no production imports, no production-result reads,
manifest integrity passed, and reruns were deterministic. Epistemic independence did not pass
strongly: the scripts did not reconstruct the landing from frozen premise strings or source
documents, and the hostile harness did not perform actual hostile mutations.

The remaining type
`NONIDENTITY_DYNAMICS_GENERATOR_SELECTING_A_PROPER_SUBSPACE_OF_COMPLETE_METRICS` is justified as a
coarse family-level remainder. It is not a uniquely minimal specific premise because local,
nonlocal, variational, source-coupled, and globally relational realizations remain open.

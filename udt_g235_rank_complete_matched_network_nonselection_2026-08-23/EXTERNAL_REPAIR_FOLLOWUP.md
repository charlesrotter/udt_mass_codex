G235_REPAIRS_ACCEPTED__NO_CANDIDATE_RETAINED

- Repair 1: `SEALED_SOURCES/` contains all 9 manifest paths, and the verifier resolves a
  package-local source root with containment and hash checks. `verify_package.py` returned
  `all_pass: true`, including every source-containment and source-hash check.
- Repair 2: Both executables expose registered `--no-write` modes. The reviewer ran both; frozen
  SHA-256s for `DERIVATION_RESULT.json`, `INDEPENDENT_VERIFICATION.json`, and
  `NETWORK_TWIN_ATLAS.tsv` were unchanged, and direct recomputation matched all frozen artifacts.
- Repair 3: The independent replay instantiates all six ruler pairs per sampled node for both
  profiles, records six constructed clock entries, and checks both conditions explicitly. Frozen
  output records both strengthened checks as true.
- Repair 4: The production common-clock test compares six constructed `clock_entries` instead of a
  tautology. Frozen evidence records the check as true for `b=0` and `b=7`.
- Repair 5: Both production and independent two-chart screen-overlap checks are explicit and true.
- Repair 6: The preregistered candidate and twins remain `b=0` and `b=7`, the separator remains
  `560/81`, both twins remain accepted by the candidate, and the existential quantifier and bounded
  conclusion ceiling are unchanged.
- Scientific landing changed: no. Production remains bounded `...__NO_CANDIDATE`; independent
  replay remains `INDEPENDENT_CONFIRMATION__NO_CANDIDATE`.

Ephemeral absolute intake links in the raw response were omitted because they do not survive intake
teardown; the verdict and scientific repair evidence above are unchanged.

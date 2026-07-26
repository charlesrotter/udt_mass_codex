# Independent review

The independent verifier is a standard-library reconstruction.  It does not
import the production generator.  It independently:

- checks the frozen preregistration, amendment, and append-only correction;
- hashes all 21 sources against the frozen base;
- recomputes 256 cap determinants and eight monodromy determinants;
- reconstructs exact completion/readout coverage and source-table inheritance;
- regression-checks the authored R06 and R10 completion dictionaries against
  deterministic outputs; their independent semantic gate is the separate
  source-first adversarial review, not this duplicated dictionary check;
- checks FC10/FC11 fail-closed behavior, all schema partitions, relation
  classes, graph endpoints, selector coverage, and the authority boundary;
- applies all 22 preregistered corruptions and requires every one to fail.

The initial adversarial model review found the source-hash, transport,
holonomy, R11, schema, relation-label, and dependency defects listed in
`ADVERSARIAL_CORRECTION.md`.  The package was not banked until those defects
were corrected and re-audited.

The final source-first re-audit returned **PASS**: all 204 rows retain zero
complete metric witnesses; FC10 ambient Levi-Civita transport is separated
from projector-rank transition; FC11/R11 is fail-closed; lattice, `S`, and `H`
dependencies are distinct; every schema totals seventeen; and physical
closure remains zero.

Final machine-readable results are in `INDEPENDENT_RESULT.json` and
`CATCH_PROOFS.tsv`.

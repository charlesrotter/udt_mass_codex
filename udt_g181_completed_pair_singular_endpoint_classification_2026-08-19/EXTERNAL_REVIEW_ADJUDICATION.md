# G181 external-review adjudication

Date: 2026-08-19

## Verdict

`G181_REQUIRES_REPAIR`

The fresh external reviewer found no refutation of the bounded geometry. It accepted the generic
determinant and completed-coordinate algebra, integrable-density accessibility criterion,
retained-chart regular endpoint criterion, density-limit counterexamples, one-sided stall versus
two-sided cusp distinction, power-law and oscillatory census, and primary zero-complete-tangent
classification.

It independently reproduced the 20,000-family standard-library replay, all sealed source hashes,
scope verification, package verification, and the banked catch JSON.

## Evidence defects

1. The sealed production script imported SymPy, which was absent from the isolated runtime. The
   production derivation therefore did not replay self-containedly.
2. The reported 33 mutation catches overstated the evidence. Several were tautologies or
   string/metadata checks rather than executable mutations capable of making a correct invariant
   fail.

These defects block acceptance as packaged. They do not constitute a mathematical counterexample.

## Registered local repair status

The preregistered repair is now implemented locally. The production replay is dependency-free;
the independent census uses 20,000 rational-exponent families including 16,575 noninteger cases;
28 executable mutants and six separate semantic guards pass; and the package verifier executes all
three scripts under isolated read-only Python.

The first recovery process ended before returning a verdict. A second overlong review returned
`G181_REPAIR_INCOMPLETE` without identifying a failed repair after all displayed checks passed. A
fresh concise recovery review then independently hashed the intake before and after every replay,
reran both verifiers and all three scripts, checked imports and exact populations, and returned
`G181_REPAIR_ACCEPTED`. The accepted repair-only verdict supersedes the local-pending status while
preserving the earlier incomplete attempt as evidence.

## Retained boundary

The theorem remains only a one-sided supplied-family endpoint classification. Physical family
selection, two-sided immersion carry, null/cut/focal/topology-changing strata, global completion,
non-scalar transport, metric-space distance, numerical `X_max`, dynamics, and observations remain
open.

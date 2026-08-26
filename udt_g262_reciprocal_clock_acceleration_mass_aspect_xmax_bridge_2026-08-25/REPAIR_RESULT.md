# G262 external-review repair result

Date: 2026-08-25

Preregistered at commit `91448643` before implementation.

## R1 — pre-existing raw wall lapse flux: implemented

The report, exact derivation, lay report, ownership atlas, status ledger, mutation harness, and
package verifier now retain the sealed WR-L result

\[
\Phi_{\rm wall}=-2\pi X
\]

as `DERIVED_METRIC_LIMIT_PREEXISTING` on the supplied `f=1-r/X` representative. Every surface also
retains the negative ownership result: this is not native mass or a normalized charge, does not
identify `X` with global `Xmax`, and cannot be promoted without a complete action or generator,
normalization, reference, orientation, and boundary prescription.

Two new applied mutations fail closed when the flux is omitted or promoted to mass. The repaired
harness catches 12/12 mutations.

## R2 — external replay scope: implemented

The report, evidence gates, run record, and transmission record now disclose that the external
reviewer successfully reran the dependency-free exact-Fraction replay, mutation harness, and
package verifier, but could not rerun the SymPy production derivation because SymPy was absent in
its isolated runtime.

## Scientific landing

Unchanged:

```text
ONE_METRIC_STATE_HIERARCHY_DERIVED
__COVECTOR_ENERGY_PAIRING_CONDITIONAL
__LOCAL_REST_MASS_PHYSICAL_TOTAL_MASS_XMAX_VALUE_AND_HISTORY_LAW_OPEN
```

No source, physical mass, normalized charge, numerical/global `Xmax`, or history equation was
added.

## Repair-only adjudication

Fresh isolated `gpt-5.4` follow-up returned `ACCEPT_REPAIR`: no remaining defect within R1/R2 and
the bounded scientific landing is unchanged.

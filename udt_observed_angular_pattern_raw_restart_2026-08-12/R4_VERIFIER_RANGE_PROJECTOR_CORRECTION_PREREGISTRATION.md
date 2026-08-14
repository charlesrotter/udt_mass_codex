# R4 verifier range-projector correction — preregistration

Date: 2026-08-14
Status: `PREREGISTERED_AFTER_SECOND_VERIFIER_FAILURE__BEFORE_RERUN`

## Second return

The batched independent replay completed all relation and lag checks in about two seconds, then
passed the first cap records under the first correction and stopped at:

```text
record: CMASS / factor 1 / group 3 / W0_UNIT / NSIDE 4
metric: unresolved_fraction
saved production value:       0.13478250566218353
independent SciPy-eigh value: 0.13478250581101614
absolute difference:          1.4883261283409337e-10
positive condition:           32573519.924816128
```

No verification result file was written and no R4 structure was interpreted.

## Diagnosis

`range_fraction` and `unresolved_fraction` are formed from the same thresholded eigenspace projector
as `range_quadratic_per_rank`. The first correction incorrectly named only the quadratic as
condition-sensitive. On this record,

```text
2048 * eps_float64 * positive_condition = 1.481272189485759e-5,
```

which is far larger than the observed `1.49e-10` projector discrepancy. The fixed general tolerance
was therefore not type-correct for these two fields.

## Frozen second correction

Apply the already registered condition-aware scale

```text
projector_bound = max(3e-10, 2048 * eps_float64 * positive_condition)
```

to all three thresholded-range fields:

- `range_fraction`;
- `unresolved_fraction`;
- `range_quadratic_per_rank`.

Use it as both relative tolerance and, for the dimensionless fractions, absolute tolerance. Keep
every other cap field at `rtol=3e-10`, `atol=3e-12`. Record the largest realized projector
difference and largest allowed condition-aware bound.

This correction changes only the independent comparison semantics for numerically ill-conditioned
range projectors. It changes no production output, rank threshold, relation, physical premise,
count, or conclusion. Large condition numbers remain visible evidence and limit precision; they are
not repaired or filtered.

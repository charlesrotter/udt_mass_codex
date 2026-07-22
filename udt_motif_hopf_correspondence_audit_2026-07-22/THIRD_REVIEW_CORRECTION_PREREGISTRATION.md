# Third-review certification correction preregistration

Date: 2026-07-22

The third fresh review returned `FAIL` for package certification while independently preserving the
registered scientific maximum and `LEAD` status. The failure is accepted before any correction:
the verifier enforced only accounting identities, so a coordinated mutation could replace the
observed point census and the `63,438 + 50` edge split with fabricated values that retained the same
totals.

## Frozen correction scope

No scientific calculation, atlas row, premise, status, or maximum conclusion may change. The
correction is limited to fail-closed validation and its bookkeeping records.

The corrected validator must require exactly:

- point census `67,396 BOTH_CLASSIFIED`, `33 ONE_SIDED_UNCERTAIN`, and `27 BOTH_UNCERTAIN`;
- `60` uncertainty-bearing point comparisons;
- edge census `63,488 possible = 63,438 eligible + 50 skipped`;
- the sole skip reason
  `ORIGINAL_EDGE_UNMATCHED+TRANSFORMED_EDGE_UNMATCHED = 50`;
- nonnegative finite numerical residuals and a positive finite sampled Jacobian determinant;
- exact frozen `hopf_seed` source path, hash, function, device, dtype, sample count, and sample seed.

## Required exercised catches

In addition to the existing 23 catches, reject at least:

1. a coordinated redistribution of the point-status census;
2. a coordinated replacement of the eligible/skipped edge split and skip vocabulary;
3. negative residuals or a non-finite determinant;
4. a fabricated seed source path;
5. a negative point-status count.

The package verifier must independently lock the exact point and edge censuses and the expanded
catch count. A temporary-mirror corruption matching the third review's attack must fail.

## Maximum allowed conclusion

Unchanged:

`OBSERVED_BOUNDED_REGISTERED-CHART_SAMPLED_MOTIF_AND_FROBENIUS_CENSUS`

plus

`EXACT_CONDITIONAL_RECIPROCAL-TORIC/HOPF-SEED_COMPATIBILITY_WITNESS`.

The correspondence remains `LEAD`. This correction cannot promote continuous transport, global
topology, a physical chart, toric/circle-action selection, carrier emergence, action, dynamics,
stability, source, or mass.

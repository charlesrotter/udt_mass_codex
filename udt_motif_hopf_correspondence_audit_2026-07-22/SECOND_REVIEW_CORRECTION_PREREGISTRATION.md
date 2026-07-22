# Second-review correction preregistration

Date: 2026-07-22

The second fresh review returned `FAIL` for package certification while explicitly retaining the
scientific maximum and overall `LEAD` status. Its raw return and complete transcript are preserved.
This correction is verification engineering, not a new scientific search, and cannot strengthen the
maximum conclusion.

## Accepted blockers

1. The edge-assignment test reused one Jacobian along a path. Nonzero stored second/third map jets
   made the pointwise geometry test nonlinear, but the edge test was only a fixed component-frame
   transformation.
2. Sixty uncertainty-bearing point comparisons and 50 ineligible transition-edge comparisons were
   omitted from the correction result instead of retained and counted.
3. Six independently corrupted load-bearing result fields survived `validate_result`: edge count,
   intrinsic covariance residual, sampled-path status, symbolic angular gap, seed source hash, and
   seed sample count.

## Registered repair

For each stored `(J,K,L)` transform, define the zero-constant cubic polynomial coordinate map

```text
x(y) = J y + (1/2) K[y,y] + (1/6) L[y,y,y].
```

At every path node, solve `x(y)=x_node`, evaluate the node-dependent Jacobian and second derivative,
and transform the complete metric/phi two-jet. Record maximum inverse-map residual and minimum
absolute Jacobian determinant. This is a newly explicit global-polynomial interpretation of the
stored jets, not a claim that the frozen parent selected a physical chart.

The result must contain:

- all `64*17*31*2 = 67,456` point comparisons;
- a mutually exclusive point-status census: both classified, one-sided uncertain, both uncertain;
- every non-uncertain classification discordance;
- all `64*16*31*2 = 63,488` possible edge comparisons split into tested and skipped;
- every skipped-edge reason and zero silent `continue` accounting;
- every tested-edge transport discordance;
- pointwise tensor/projector residuals under the node-dependent maps.

The validator must enforce all preceding coverage identities and thresholds. It must also enforce:

- intrinsic-object and projector residuals `<=1e-8`;
- exact sampled-path nonpromotion text;
- exact metric-derived angular-gap, connection, and unit-limit records;
- frozen `hopf_seed` source SHA-256, CPU float64 execution, deterministic seed, exactly 1,000
  samples, and residual `<=1e-12`;
- complete construction provenance and direct source lineage; and
- the unchanged maximum and overall `LEAD` status.

Mutation catches must include the six escaped mutations, missing uncertainty counts, missing skipped
edges, and replacement of the node-dependent polynomial-map interpretation with a fixed Jacobian.

## Known review probe

The second reviewer independently applied this cubic-polynomial interpretation after finding the
defect and observed zero discordances on the eligible edges. That post-review outcome is known and
cannot be presented as outcome-blind. The package implementation must nevertheless recompute it from
scratch, retain every excluded/uncertain case, and survive another fresh audit before certification.

## Maximum conclusion

Unchanged:

`OBSERVED_BOUNDED_REGISTERED-CHART_SAMPLED_MOTIF_AND_FROBENIUS_CENSUS`

plus

`EXACT_CONDITIONAL_RECIPROCAL-TORIC/HOPF-SEED_COMPATIBILITY_WITNESS`.

The proposed motif-to-Hopf correspondence remains a `LEAD`. No continuous/global continuation,
physical chart, toric/circle selection, cap, carrier, action, dynamics, stability, source, or mass is
derived.


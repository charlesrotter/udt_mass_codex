# G170 audit report — endpoint-relative bidirectional pair response

Date: 2026-08-19
Grade: `VERIFIED_WITH_CAVEATS__ENDPOINT_RELATIVE_THEOREM__CONSISTENT_CALIBRATION_CLASS__CROSS_QUERY_CARRY_OPEN`

## Primary landing after fresh review

```text
ENDPOINT_RELATIVE_REPAIR_VALID_BUT_CALIBRATION_CARRY_STILL_LOAD_BEARING
```

## Result first

The fresh external reviewer confirmed that the apparent G169 reversal gap came from applying the
terminal scalar at each endpoint as though
each value were already the directed pair depth. The original 2026-08-09 reciprocal-`c_E` theorem
had already derived the correct two-endpoint rule:

\[
\delta_{AB}
=\frac12\log\frac{L_B/T_B}{L_A/T_A}
=\Phi_B-\Phi_A.
\]

Consequently, swapping the same two endpoint readouts forces

\[
\delta_{BA}=-\delta_{AB},
\qquad
q_{BA}=q_{AB}^{-1},
\qquad
\chi_{BA}=-\chi_{AB}.
\]

No co-presence premise, separately supplied negative depth, path, `X_max`, or observational input
is used.

The theorem is scoped to endpoints on one consistently calibrated pair surface, or an equivalent
endpoint family with explicitly matched reciprocal calibration carry. Independent reciprocal
recalibrations remain different inputs and shift the candidate cross-family depth by `c_B-c_A`.

## G169 regrade

G169's flat surface witness has

\[
\Phi_A=\Phi_B=\frac14\log(1+a^2).
\]

It therefore gives \(\delta_{AB}=\delta_{BA}=0\). The witness disproves treating one endpoint's
nonzero reciprocal density as the arrow depth, but it is not a counterexample to endpoint-relative
reversal.

G169 remains correct that ordinary surface orientation reversal does not negate a local terminal
density. Its stronger implication—that an independently supplied inverse scalar is needed—does not
survive restoration of the original endpoint-relative rule.

## Metric and orchestra

The endpoint readouts are computed only after the G167 pullbacks are complete. Two exact nonradial
endpoint witnesses retain live shift and angular Gram terms. Both angular sectors change their
terminal ratios, and the relative squared ratio reverses exactly. Independent common endpoint
scales cancel.

Thus the current bounded chain is:

```text
primary metric
  -> supplied endpoint pair germs
  -> full endpoint pullbacks h_A,h_B, including angular Gram
  -> terminal endpoint ratios q_A,q_B
  -> q_AB=q_B/q_A
  -> delta_AB=-(1/2)log(q_AB).
```

The observers and endpoint data are arguments of this calculation. They are not an additional
physical law the metric must select. This evaluator statement does not select which endpoints form
one experiment and does not derive cross-query calibration carry.

## Exact evidence

- preregistered and pushed at `f9a6d1e6` before outcome algebra;
- 12/12 frozen source hashes pass;
- production symbolic/source checks: 40/40;
- independent standard-library `Fraction` checks: 21,600/21,600;
- 1,200/1,200 independent live-shift channel trials;
- 1,200/1,200 independent regular nonradial angular trials; all retain nonzero pair shift and
  angular modification of the readout;
- mutation catches: 13/13;
- fresh external review returned
  `ENDPOINT_RELATIVE_REPAIR_VALID_BUT_CALIBRATION_CARRY_STILL_LOAD_BEARING`;
- the review independently confirmed the mathematical repair and required a calibration-domain
  clarification plus a self-contained sealed replay;
- the calibration repair passed follow-up without a finding;
- that follow-up found that SymPy was unavailable in the minimal sealed sandbox, so the sealed
  replay is now standard-library-only and the SymPy controller remains an outer gate;
- the next follow-up successfully ran the standard-library replay but required explicit `-S`
  propagation to its child processes; that sole mechanical repair is implemented;
- the final mechanical reviewer reproduced the sealed replay with both child `no_site` flags true,
  found no in-scope defect, and retained the consistent-calibration theorem unchanged;
- repository premise and regression gates must be rerun after final package assembly.

## Scope and remaining open work

Derived in this bounded arena:

- terminal endpoint reciprocal densities from the complete calibrated pair metrics;
- their endpoint-relative scalar depth inside one consistently carried reciprocal calibration
  class;
- reversal by endpoint swap;
- matched scalar composition on shared calibration states;
- common-scale cancellation;
- inclusion of the primary metric's angular Gram before relative readout.

Not derived here:

- a positive metric-space distance or identity-of-indiscernibles;
- full non-scalar carry, connection, holonomy, or arbitrary triangle closure;
- cross-query reciprocal calibration carry;
- event selection, general ambient/time-live extension, global completion, `X_max`, action, source,
  matter, observations, or signalling.

## Maximum conclusion

The primary reciprocal scalar no longer has an inverse-ownership gap once it is computed as the
already-derived difference of two endpoint densities in one consistently calibrated pair
calculation. Cross-query reciprocal calibration and the full non-scalar carry remain load-bearing
open structures. The result is `VERIFIED_WITH_CAVEATS`: the endpoint-relative theorem and its
mechanical evidence are closed in the stated bounded arena, while cross-query reciprocal
calibration and full non-scalar carry remain open.

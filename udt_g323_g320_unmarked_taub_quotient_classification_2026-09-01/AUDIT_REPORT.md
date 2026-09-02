# G323 internal audit report

Date: 2026-09-01; repaired 2026-09-02
Status: `EXTERNALLY_ACCEPTED_AFTER_REPAIRS`

## Result

```text
REGISTERED_G320_PROFILES_EMBED_AS_CAUCHY_GRAPHS_IN_ONE_LOCAL_RICCI_FLAT_TAUB_FORM
__INTEGER_MODES_HAVE_STRICTLY_DISTINCT_COMPACT_LATTICE_MODULI_AND_THUS_DISTINCT_UNMARKED_QUOTIENTS
__OPPOSITE_K_SIGNS_ARE_ONE_TIME_UNORIENTED_METRIC_WITH_OPPOSITE_TIME_ORIENTATIONS
__NO_OCCUPANCY_SELECTION
```

## Findings

1. Every registered G320 profile and sign embeds with its complete first and second fundamental
   forms in the explicit local metric `-R/mu dR^2 + mu/R dX^2 + R^2(dy^2+dz^2)`.
2. Direct tensor calculation gives `Ric=0` and Kretschmann scalar `12 mu^2/R^6`.
3. Thus the arbitrary profile is locally a refoliation/Cauchy-graph freedom in this LRS slice.
4. A degree/winding plus zero-integral argument proves that compact injectivity forces the global
   `X` period. The invariant lattice-intersection/projected-covolume definition of `Q_X` survives
   local parameter rescalings, basis changes, and nonsplit lattice presentations.
5. `L_X(n)` is strictly increasing for every positive integer mode. The registered `n=1` and
   `n=2` explicit globally hyperbolic Taub quotients are therefore inequivalent even after the
   initial marking is forgotten. Equality of either explicit quotient with its G322 MGHD is open.
6. Opposite `K` signs give the same time-unoriented metric quotient and opposite time orientations.
   The nonzero timelike gradient of the Kretschmann scalar forbids an orientation-preserving
   identification between those orientations.
7. The result classifies the diagnostic family. It selects no physical datum, topology, quotient,
   orientation, scale, or universe.
8. The provisional field equation, UDT metric, reciprocal kernel, angular cancellation, and
   observational interfaces are unchanged.

## Raw gates

- production: 78 assertions; maximum pullback error `8.882e-15`; maximum extrinsic error
  `9.992e-16`;
- independent: 33 assertions with different controls; maximum pullback error `2.665e-15` and
  maximum extrinsic error `1.224e-10`;
- independent Ricci residuals: `4.44e-16` to `1.14e-13` after the documented failed-closed repair;
- hostile mutations: 13/13 caught;
- finite production periods: `6.5545166850`, `6.6232264275`, `6.7354404967`, `6.8880830208`.
- exact 305-row premise registry and startup guards: repository-side pass, recorded as an external
  attestation rather than replayable evidence in the first sealed intake;
- full repository suite: repository-side `217 passed, 1 xfailed`, likewise an external attestation.
- fresh external review: `G323_REPAIRABLE_DEFECTS__BOUNDED_LANDING_RETAINED`;
- repair-only external follow-up:
  `G323_REPAIRS_ACCEPTED__BOUNDED_EXPLICIT_QUOTIENT_LANDING_RETAINED`.

## Boundary

This does not cover the full G319 moduli space, non-LRS data, `d` or `Lambda` nonzero, `B=0`
crossings, matter/source sectors, stability, physical topology/occupancy, an observational scale,
or full UDT. The explicit quotient is a globally hyperbolic development. Equality with the G322
MGHD is not proved and remains open.

Repairs R1--R4 and the retained bounded landing were accepted by the repair-only external follow-up.

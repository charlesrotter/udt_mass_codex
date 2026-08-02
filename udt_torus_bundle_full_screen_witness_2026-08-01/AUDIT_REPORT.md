# FC07 complete full-screen witness audit

Date: 2026-08-01  
Status: **VERIFIED-WITH-CAVEATS — exact bounded off-shell construction**

## Result first

The prior transition schemas are now realized by actual complete metrics in a second registered
completion class.

All eight registered `GL(2,Z)` controls admit smooth, nondegenerate, Lorentzian geodesically
complete mapping-torus metrics with the full three-mode positive screen. Their endpoint screen
metrics obey the exact congruence law, and the flat interpolation makes every transformed seam jet
match.

The result has three important refinements:

1. The eight frozen monodromy presentations give only **seven metric-level endpoint-congruence
   fibers**. Identity and minus identity remain globally different monodromies, but the quadratic metric readout makes
   their local congruence maps identical.
2. Six determinant-plus-one cases admit global oriented coframes for the constructed metrics. The
   two determinant-minus-one cases are smooth complete nonorientable metrics with local coframes
   joined by reflection; they overlap the registered FC09 class.
3. Six monodromies allow a constant-screen subfamily. Parabolic and hyperbolic monodromy have no
   invariant positive screen, so within the chosen block/lattice presentation they force the
   angular screen metric to vary somewhere around the global base circle.

The screen projector descends globally and remains integrable in every witness. In the two forced-
variation classes it cannot be parallel everywhere because the varying screen produces exact
connection mixing. This is global geometric structure, not physical time evolution.

## Why this matters

The preceding audit found precise blueprints for global-to-local compatibility. This package builds
the first second-completion family from those blueprints. The global completion is no longer merely
a label or seam formula: it is carried by a smooth complete four-metric.

It also shows that the metric readout can forget some global information. Distinct global
monodromies can induce the same local metric fiber, so any future bootstrap return cannot assume a
one-to-one map from local metric data back to global topology.

## Exact scope

This is an existence family inside a chosen exact block extension with constant `phi`, zero shift,
and no pair-screen cross block. Those are surfaced bounded controls. The full positive screen is
free, all eight registered monodromy controls are retained, and no branch is ranked by merit.

The construction is off shell. It supplies no native equation, action, source, carrier, density,
bootstrap return, physical boundary, stability result, matter interpretation, or completion
selector. It does not exhaust the infinite `GL(2,Z)` family.

## Verification

- Production: 116 exact symbolic/rational checks.
- Independent stdlib reconstruction: 302 checks without importing the production script; malformed
  source-anchor rows fail closed.
- Semantic verifier: 33/33 attempted omissions and overclaims fail closed.
- The load-bearing completeness argument is the compact-mapping-torus/Hopf-Rinow theorem plus the
  exact constant-lapse product splitting of the geodesic equations.
- Sixteen exact lattice-basis controls confirm covariance of the endpoint law. The seven count is
  not a conjugacy or infinite-family classification.

Fresh zero-context agent `/root/fc07_cold_adversary` independently returned
`VERIFIED-WITH-CAVEATS` after requiring the source-anchor, orientation, seam-convention,
representative-scope, stale-capture, and topology-wording repairs. Repository gates and the final
package manifest are recorded separately.

## Maximum conclusion

`COMPLETE_OFFSHELL_FC07_METRIC_WITNESSES_EXIST_FOR_THE_EIGHT_FROZEN_CONTROLS_IN_THE_CHOSEN_CONSTANT_DEPTH_BLOCK_EXTENSION__SEVEN_FROZEN_ENDPOINT_CONGRUENCE_OPERATOR_CLASSES__NO_EXTENSION_OR_MONODROMY_SELECTION_DYNAMICS_STABILITY_BOOTSTRAP_RESPONSE_PROJECTOR_OR_MATTER_CLAIM`.

# FC07 torus-bundle full-screen witness — preregistration

Date: 2026-08-01  
Base: `06858a8e4f9fedfe3921b8083748193f24f945de`  
Mode: CPU-only exact construction and bounded sampling; metric-led; no field equation or solve

## Whole question

Does the already registered `FC07_PERIODIC_TORUS_BUNDLE` completion class admit an actual smooth,
complete, nondegenerate off-shell UDT metric with a general positive-definite two-dimensional
screen whose endpoint data realize the mapping-torus transition/jet fiber throughout the quotient?

This tests whether the preceding parametric `Graph(M)` and transformed-jet schemas can be promoted
to realized complete **off-shell metric witnesses** in one second completion class. It does not ask
which completion or monodromy is physical.

## Bounded construction class

Retain all eight registered `GL(2,Z)` monodromy witnesses. On a fundamental domain
`s in [0,1]`, glue

```text
(1,y) ~ (0,M y),       y in T2.
```

Use the founded reciprocal clock/ruler scaling with constant depth only as an isolating control:

```text
g = -c_E^2 exp(-2 phi0) dt^2 + L^2 exp(2 phi0) ds^2 + dy^T h(s) dy,
```

where `c_E>0`, `L>0`, and finite `phi0` remain symbolic. Let `h0` range over every positive-
definite symmetric `2 x 2` matrix and require

```text
h1 = M^T h0 M.
```

Use any smooth flat endpoint switch `chi(s)` with `chi(0)=0`, `chi(1)=1`, and every positive-order
endpoint derivative zero, and test the constructive family

```text
h(s) = (1-chi(s)) h0 + chi(s) h1.
```

The interpolation is a construction device, not a physical weighting or action.

## Before-work premise ledger

- **Question:** observing whether registered completion data are realizable; not targeting a
  particle, mass, spectrum, preferred topology, or selector.
- **Completion class FC07:** `pinned-by-THEORY` as a registered mathematical branch; explicitly not
  pinned as the physical cell.
- **All eight monodromies:** `free-and-explored` within the frozen witness registry; none preferred.
- **General screen `h0`:** `free-and-explored` over the full positive-definite cone.
- **Constant `phi0`, no shift, no clock-screen mixing:** `pinned-by-HABIT` bounded control choices.
  A positive witness is existential only; any negative is invalid outside this slice.
- **Positive `c_E,L` and finite `phi0`:** symbolic calibration/domain conditions, no numerical pin.
- **Flat switch:** category-A smooth gluing construction. Its detailed shape has no physical status.
- **No action, variation, field equation, source, carrier, density, bootstrap return, stability
  test, or desired filter:** entered.

## Certification gates

A monodromy row earns `COMPLETE_OFFSHELL_METRIC_WITNESS` only if all hold:

1. `det(M)=+-1` and the stated gluing defines the registered mapping-torus class;
2. `h1=M^T h0 M` is positive definite for every positive-definite `h0`;
3. the entire interpolation remains positive definite for `0<=chi<=1`;
4. all transformed metric jets match at the seam;
5. a smooth local screen coframe exists and its seam relation is explicitly typed, including its
   possible `O(2)` gauge factor;
6. the spatial quotient is compact and Riemannian complete;
7. the constant-lapse Lorentzian product is geodesically complete, with the proof stated;
8. no source is promoted from registered/conditional branch to physical completion.

The audit must separately count metric-level congruence fibers and coframe presentations. It must
not claim eight distinct metric fibers if central sign or screen gauge makes any coincide.

## Falsification and maximum conclusion

- Any loss of positive definiteness, seam smoothness, nondegeneracy, compactness, or completeness
  blocks the corresponding witness.
- If only a local fundamental-domain metric exists, return `LOCAL_ONLY_NOT_COMPLETE`.
- If the metric descends but the coframe requires transition gauge, report that gauge rather than
  calling the coframe globally single-valued.
- If different `M` collapse at the metric level, retain the equivalence classes.
- A witness may realize compatibility schemas but cannot select `M`, FC07, a physical boundary,
  dynamics, stability, or matter.

Maximum conclusion:

```text
FC07_COMPLETE_OFFSHELL_FULL_SCREEN_WITNESS_FAMILY_EXISTS
WITH_EXACT_TRANSITION_AND_JET_DESCENT
NO_PHYSICAL_SELECTION_DYNAMICS_STABILITY_OR_BOOTSTRAP
```

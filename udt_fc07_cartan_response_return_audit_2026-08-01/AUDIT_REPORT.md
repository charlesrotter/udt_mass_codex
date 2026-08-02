# FC07 Cartan, intrinsic-response, and return-channel audit

Date: 2026-08-01  
Grade: **VERIFIED-WITH-CAVEATS**

## Result first

The complete FC07 metrics contain a real, stratified global-to-local geometric channel.

For every nonconstant registered screen interpolation, unimodularity forces the screen-change
matrix to be indefinite and full rank. The resulting rank-one projector response is therefore
nonzero at every cell-interior point. This is initially a bundle-relative statement.

In three varying classes—order-four, order-six, and hyperbolic—the completed spatial manifold has
`b1=1`. Its unique harmonic one-form line, together with the curvature-selected timelike line,
makes the ruler projector metric-intrinsic on the registered product. The normalized harmonic form
at each point depends on an integral over the whole cell. This is an explicit nonidentity
global-completion-to-local-geometry map.

Among the two frozen classes where variation is unavoidable, hyperbolic has this unique harmonic
line; parabolic has `b1=2` and retains a genuine line-selection ambiguity. This is a structural
intersection, not a physical ranking.

Constant-screen strata reveal the observer-covariant companion result. Minus-identity, order-four,
and order-six holonomy select the whole Lorentzian reciprocal two-plane while leaving its
clock/ruler axes free. No preferred observer is introduced.

## What was derived

- the full arbitrary-screen two-jet Cartan/Levi-Civita connection;
- complete Riemann, Ricci, scalar, curvature-nullity, and shape-operator formulas;
- an exact theorem that every nonconstant unimodular two-screen endpoint interpolation has
  `det(K)<0` throughout its interior;
- the full rank-one relative response `Omega_rel`, not one selected component;
- six nonzero generic response controls and two flat zero controls;
- four unique-`H1` completions, three of them varying in the generic witness;
- one forced-varying unique-`H1` row in the frozen set: hyperbolic;
- three constant-screen holonomy-fixed reciprocal planes with no selected axes; and
- explicit bootstrap and `X_max` failure gates.

## Why this matters

Earlier complete witnesses showed that global joins constrain local metric profiles. This audit
adds the next strut: on specified strata the completed metric can solve a global harmonic problem
and return a locally varying line/projector field. That is the type of communication a bootstrap
architecture needs.

The result does not yet close the loop. It supplies neither a native equation requiring this field
nor feedback from local admissibility/matter to the global completion. It therefore cannot yet
repair, select, or invalidate a mass branch.

## Scope and negatives retained

- The complete metrics are off shell and use constant `phi`, zero shift, zero pair-screen mixing,
  and the chosen block interpolation.
- The response is metric-intrinsic only on the exact selection strata; elsewhere it remains
  bundle-relative, set-valued, degenerate, or absent.
- Constant invariant screens and both nonorientable cases remain in the atlas.
- The midpoint isotropy is a selected symmetric-interpolation property, not a UDT law.
- That isotropic curvature selects the timelike nullity line but cannot itself select a ruler; the
  global harmonic gate is independently load-bearing.
- No action, carrier, source, density, stability condition, matter label, completion choice, or
  physical branch was introduced.
- The harmonic realization emerged inside the preregistered broad C06 return-channel class rather
  than being named in advance; this disclosure and the absence of a fresh external semantic review
  keep the grade caveated.

## Evidence

- preregistration `45ebc7e`;
- 23 source identities frozen at `f9fb990`;
- SymPy 1.13.1 production derivation: 69 exact checks;
- independent standard-library `Fraction` implementation: 155 checks, including four direct
  second-jet coordinate-Riemann reconstructions and sixteen basis-covariance controls;
- 25/25 semantic mutation catches;
- all eight monodromies, seven metric-readout classes, six constant-screen subfamilies, two forced
  varying classes, and both orientation strata retained.

## Maximum conclusion

```text
FC07_FULL_SCREEN_CARTAN_AND_CURVATURE_DERIVED__ALL_NONCONSTANT_REGISTERED_INTERPOLATIONS_HAVE_NONZERO_BUNDLE_RELATIVE_PROJECTOR_RESPONSE__THREE_VARYING_UNIQUE_H1_CLASSES_HAVE_A_METRIC_INTRINSIC_GLOBAL_HARMONIC_RULER_CHANNEL__ONE_FORCED_HYPERBOLIC_INSTANCE__THREE_CONSTANT_SUBFAMILIES_HAVE_A_HOLONOMY_FIXED_RECIPROCAL_PLANE_WITHOUT_SELECTED_AXES__NO_UNIVERSAL_PROJECTOR_BOOTSTRAP_CLOSURE_XMAX_SELECTION_DYNAMICS_OR_MATTER
```

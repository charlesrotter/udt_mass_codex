# G176 preregistration — completed-pair Dual Reciprocity consolidation

Date: 2026-08-19
Mode: metric-led exact algebra and type consolidation
Frozen source commit: `76ac6bb2`

## Question

Given Charles's provisional clarification that Dual Reciprocity applies after all complete-pair
metric contributions enter, does the completed physical observer-pair pullback uniquely inherit
the determinant-one reciprocal normalization, or does a residual calibrated-ruler ambiguity remain
inside the physical scalar kernel?

## Preregistered primary landings

Exactly one will be selected:

1. `COMPLETED_PAIR_DUAL_RECIPROCITY_UNIQUELY_FIXES_RECIPROCAL_RULER__ARBITRARY_CALIBRATIONS_ARE_CONTROL_QUERIES`:
   on every regular completed pair, `T L=1` is equivalent to the unique positive auxiliary ruler
   density `m=T L_sigma=sqrt(-det h_sigma)`; in the G173 static family this is
   `m^2=exp(-2 phi) H` and `Phi=phi`.
2. `COMPLETE_PAIR_CONTRIBUTIONS_OBSTRUCT_DETERMINANT_ONE_DESCENT`: angular, screen, mixing, or shift
   data prevent a regular covariant reciprocal normalization on at least one declared stratum.
3. `RESIDUAL_PHYSICAL_CALIBRATION_FAMILY_SURVIVES_RECIPROCITY`: two non-constant, inequivalent
   positive ruler densities satisfy the same completed-pair reciprocal condition.
4. `TYPE_OR_REGULARITY_FAILURE`: the proposed normalization changes the supplied pair image or
   leaves the regular Lorentzian rank-two stratum.

## Exact derivation contract

1. Start from the generic regular calibrated auxiliary pair metric
   `h_sigma=-T^2(dy0+beta dsigma)^2+L_sigma^2 dsigma^2`, with `T,L_sigma>0`.
2. Under `ds=m dsigma`, derive every transformed component, determinant, terminal `T,L,beta`, and
   reciprocal scalar without setting `beta=0`.
3. Prove or refute the iff theorem
   `T L=1 <=> -det(h_s)=1 <=> m=T L_sigma=sqrt(-det h_sigma)` for positive `m`.
4. Prove uniqueness and auxiliary-reparameterization covariance, including orientation reversal.
5. Specialize only afterward to `T=exp(-phi)` and
   `L_sigma^2=H=exp(2phi)v^2+r^2 b2`; test pure radial recovery and regular angular turns.
6. Track where the orchestra remains: all complete contributions enter `T,L_sigma,beta` before
   reciprocal normalization; spatial-only enlargement changes the ruler map, clock-side change
   changes `Phi=-log T`, and shift/non-scalar channels are retained.
7. Reclassify G173--G175 alternatives as controls without rewriting their historical results.
8. Do not claim that the bare metric selects events, the pair germ, or a global relation family.

## Bounded scope and omitted sectors

- generic local regular Lorentzian rank-two pair metric: full exact algebra;
- G173 static spherical turning family: bounded specialization;
- complete `3+1` histories: only through their supplied pair pullback;
- omitted: event/germ selection, coincidence, null/degenerate/cut/focal/singular/topology-changing
  strata, paths, connections, Jacobi/holonomy transport, global completion, dimensionful distance,
  numerical `X_max`, observations, radiative transfer, dynamics, action, source, matter, bootstrap,
  mass, and signalling.

## Certification and falsification contract

- exact symbolic derivation for generic nonzero shift;
- independent standard-library rational replay over at least 20,000 regular metrics and auxiliary
  reparameterizations;
- static radial and angular-turn witnesses;
- at least 16 semantic/mutation catches, including post-processing the orchestra, selecting event
  pairs, erasing shift, reviving arbitrary calibrated curves as rival kernels, and globalizing the
  local theorem;
- all nine frozen source hashes verified at commit `76ac6bb2`;
- current premise verifier and full repository regression suite pass;
- fresh independent/adversarial review before any stronger than `VERIFIED_WITH_CAVEATS` grade.

Landing 1 is falsified by one regular completed pair admitting two positive non-constant ruler
densities with `T L=1`, or by one declared complete contribution that cannot be included before the
normalization. Landings 2--4 are falsified by a generic covariant iff proof plus independent replay.

## Maximum conclusion

At most G176 may close the scalar normalization type on supplied regular completed physical UDT
pairs under the provisionally adopted clarification. It cannot select which pairs are realized or
derive any global, observational, source, action, matter, or signalling law.

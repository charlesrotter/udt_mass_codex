# G180 preregistration — completed-pair smooth-family descent

Date: 2026-08-19
Mode: metric-led exact one-dimensional descent, primary-metric specialization, and independent
finite-dimensional replay
Frozen source commit: `94a85956`

## Whole question and bounded regime

Does the G176--G179 completed-pair kernel glue pointwise into one smooth physical ruler coordinate
on every supplied connected smooth regular pair family, without an extra scalar, carry rule,
profile, or `X_max` input?

Let a supplied auxiliary pair metric vary smoothly on a connected interval `I`:

```text
h_sigma(sigma)=[[h00,h01],[h01,h11]],
h00<0, det(h_sigma)<0.
```

The primary specialization is the declared static-spherical metric pulled back to a supplied
time-orthogonal sphere curve with arbitrary smooth radial and angular motion. Turning and
pure-angular points are included whenever the complete spatial tangent remains nonzero.

## Preregistered primary landings

Exactly one will be selected:

1. `COMPLETED_PAIR_SMOOTH_FAMILY_DESCENT__ORCHESTRA_ENTERS_THE_PHYSICAL_TAPE_MAP`:
   `m=sqrt(-det h_sigma)` is a smooth positive density, its integral defines one completed ruler
   coordinate up to origin and orientation, `det h_s=-1`, and no extra scalar is required. In the
   primary time-orthogonal family, angular motion changes `ds/dsigma` and therefore `r(sigma(s))`,
   while completed depth remains `Phi=phi(r(s))`.
2. `LOCAL_COMPLETED_DENSITY_FAILS_TO_GLUE`: a supplied smooth regular connected family has no
   lawful completed ruler coordinate even locally or interval-wide.
3. `ACTIVE_FAMILY_CHANNEL_REQUIRES_AN_EXTRA_SCALAR_OR_CARRY`: after the full pullback and local
   reciprocal normalization, additional pair-family data are required for scalar descent.
4. `REGULARITY_OR_COVARIANCE_FAILURE`: the result fails a lawful family reparameterization,
   orientation, turning-point, shift, or exact derivative control.

## Exact derivation contract

1. Prove from smoothness and `-det h_sigma>0` that
   `m=sqrt(-det h_sigma)` is smooth and positive and that
   `s(sigma)=s0+integral m(u)du` is a smooth monotone coordinate on `I`.
2. Transform the full shifted pair metric under `ds=m dsigma`; require exactly
   `det h_s=-1`, `T_s L_s=1`, `Phi=-1/2 log(-h00)`, and retained
   `beta_s=beta/m`.
3. Prove orientation-preserving auxiliary reparameterization covariance and distinguish the
   positive density from the oriented ruler one-form. Do not call auxiliary reversal observer-pair
   reversal.
4. Specialize to
   `F(x0,sigma)=(x0,r(sigma),gamma(sigma))` in the primary metric. With
   `v=dr/dsigma` and `b2=|dgamma/dsigma|^2`, derive or refute

   ```text
   H=exp(2phi)v^2+r^2 b2,
   m^2=exp(-2phi)H=v^2+exp(-2phi)r^2 b2,
   h_s=diag(-exp(-2phi),exp(2phi)),
   Phi=phi.
   ```

5. Show precisely how the orchestra survives: it changes the completed tape map `s(sigma)` and
   hence the history `r(s)` and `Phi(s)=phi(r(s))`; it is not appended to `Phi` afterward.
6. Include radial, angular-turn, pure-angular, nonzero-shift generic, and smooth center-limit
   controls. The zero spatial-tangent point is a declared excluded degeneracy, not a negative.
7. Verify the exact derivative identities
   `ds/dsigma=m`, `dPhi/dsigma=-dot(h00)/(2h00)`, and, where inversion is regular,
   `dPhi/ds=(dPhi/dsigma)/m`. These are kinematics, not dynamics.
8. Prove same-family endpoint difference, reversal, and telescoping from the completed scalar
   values. Do not impose closure across independently supplied pair families.
9. Run an independent standard-library replay over at least 20,000 smooth regular algebraic jets
   and primary radial/angular controls, with exact arithmetic wherever possible.
10. Include mutation catches for restoring G172's arbitrary-coordinate scalar as the completed
    depth, deleting the angular contribution from `m`, bolting it onto `Phi`, importing G142--G160,
    using `X_max`, fitting observations, selecting a family, or calling the chain rule dynamics.

## Values, choices, omissions, and premise stamps

- Lorentz signature, pullback, smoothness, and regularity inequalities: `pinned-by-THEORY` in the
  bounded metric arena.
- Completed-pair Dual Reciprocity: `WORKING_FOUNDATIONAL_CLARIFICATION`, not canon.
- Primary static-spherical metric and supplied smooth pair family: `CONDITIONAL`.
- Family shapes and algebraic witnesses: `free-and-explored`; none is selected as physical.
- `c_E`: `OBSERVED` calibration anchor; dimension-matched coordinates may set its numerical value
  to one.
- Inactive: G142--G160 carry/score scaffolds, `X_max`, fits, radiative transfer, dynamics, action,
  source, matter, bootstrap, co-presence, and signalling.
- Omitted: physical event/germ population, cross-family matching, multidimensional/global
  completion, loops and non-scalar transport, null/degenerate strata, and observations.

## Certification and falsification contract

- preregistration and exact source hashes banked before outcome code;
- generic smooth-family proof plus exact primary-metric specialization;
- independent implementation sharing no production functions;
- at least 20,000 independent regular controls and at least 20 semantic/mutation catches;
- exact residuals for algebraic gates and controlled tolerances only for numerical quadrature;
- current premise verifier and full repository regression suite pass;
- fresh adversarial review required before promotion beyond `VERIFIED_WITH_CAVEATS`.

Landing 1 is falsified by one declared smooth connected regular family whose local reciprocal
density cannot integrate to the calibrated determinant-one tape, by one lawful reparameterization
that changes the completed result, or by one primary angular/turning family requiring an extra
post-readout scalar.

## Maximum conclusion

At most G180 may derive interval-wide smooth descent of the already accepted local completed-pair
kernel and show that the primary angular orchestra changes the completed tape map rather than
adding a scalar correction. It cannot select a physical family, derive a global universe or
`X_max`, close non-scalar transport, or validate observations or dynamics.

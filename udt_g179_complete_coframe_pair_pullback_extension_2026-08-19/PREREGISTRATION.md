# G179 preregistration — complete-coframe completed-pair extension

Date: 2026-08-19
Mode: metric-led exact algebra, covariance, and independent finite-dimensional replay
Frozen source commit: `7c782014`

## Whole question

Does the G176--G178 completed-pair Dual Reciprocity theorem extend without an extra scalar,
coefficient, profile, or post-processing term from the primary static-spherical slice to an
arbitrary supplied smooth complete Lorentz coframe and supplied regular rank-two observer-pair
germ?

The bounded domain is local and pointwise. Write

```text
g = E^T eta_4 E,               E in GL(4,R),
h = J^T g J,                   rank(J)=2,
h00<0,                         det(h)<0.
```

The lower-block complete chart `E=[[B,0],[Q S,Q]]`, `J=[Y;Z]` will be tested as an explicit
specialization with every `B,Q,S,Y,Z` sector active. It is not assumed to be the only coframe
presentation.

## Preregistered primary landings

Exactly one will be selected:

1. `GENERAL_COMPLETE_COFRAME_PULLBACK_EXTENDS_COMPLETED_PAIR_KERNEL_WITHOUT_EXTRA_SCALAR`:
   after the full pullback, completed-pair Dual Reciprocity uniquely gives
   `m=sqrt(-det h)`, `Phi=-1/2 log(-h00)`, and the calibrated determinant `-1`; all active
   complete-coframe channels enter only through `h` before normalization.
2. `COMPLETE_COFRAME_EXTENSION_IS_CHART_OR_SECTOR_DEPENDENT`: one declared nonspherical,
   screen, mixing, shift, time-live, or singular-`Y` regular witness cannot be represented by the
   same theorem.
3. `ACTIVE_COMPLETE_CHANNEL_LEAVES_AN_ADDITIONAL_SCALAR_OR_COEFFICIENT`: after forming `h`, a
   regular witness requires information not contained in `h00`, `h01`, and `h11` to impose Dual
   Reciprocity.
4. `COVARIANCE_OR_REGULARITY_FAILURE`: the proposed extension fails ambient coframe gauge,
   ambient coordinate covariance, lawful auxiliary-ruler reparameterization, or rank-two
   regularity.

## Exact derivation contract

1. Begin with arbitrary invertible `E`, Lorentz signature `eta_4=diag(-1,1,1,1)`, and arbitrary
   rank-two `J`; form `h=J^T E^T eta_4 E J` before any terminal readout.
2. On `h00<0`, `det(h)<0`, reconstruct the unique positive shifted decomposition
   `T^2=-h00`, `beta=h01/h00`, and `L_sigma^2=h11-h01^2/h00`.
3. Apply only the G176 working completed-pair clarification `T L_s=1` under
   `ds=m dsigma`; prove or refute the unique positive result
   `m=T L_sigma=sqrt(-det h)` and `Phi=-log T=-1/2 log(-h00)`.
4. Prove ambient Lorentz-coframe gauge invariance under `E -> Lambda E`,
   `Lambda^T eta_4 Lambda=eta_4`, and ambient coordinate covariance under the matched changes of
   `E` and `J` that leave `EJ` invariant.
5. Recheck positive auxiliary-ruler reparameterization and spatial orientation reversal as a
   density/oriented-one-form statement. Do not conflate this with observer-pair reversal.
6. Specialize exactly to `E=[[B,0],[Q S,Q]]`, `J=[Y;Z]` and recover
   `h=Y^T B^T eta_2 B Y+(S Y+Z)^T Q^T Q(S Y+Z)`.
7. Supply exact regular witnesses with nonspherical `Q`, all four entries of `S`, nonzero `Z`,
   nonzero terminal shift, and a regular singular-`Y` case. Vary each `B,Q,S,Y,Z` sector
   independently and require at least one generic nonzero effect on `h`, `m`, or `Phi` according to
   its tensor location; no sector may be reinserted after the readout.
8. For a supplied smooth parameter family, verify the pointwise identity and the kinematic chain
   rule `dot h=dot J^T g J+J^T dot g J+J^T g dot J`. This is query-live kinematics, not dynamics or
   an equation of motion.
9. Run an independent standard-library exact-rational replay over at least 20,000 nonsingular
   complete-coframe/pair witnesses and lawful coordinate/gauge/reparameterization controls.
10. Include mutation catches for deleting `Q`, deleting or scalarizing `S`, freezing `J`, erasing
    shift, using a post-readout orchestra term, importing `X_max`, selecting events, globalizing
    the theorem, or treating pair-coordinate reversal as observer reversal.

## Values, choices, omissions, and premise stamps

- Lorentz signature and regularity inequalities: `pinned-by-THEORY` for this bounded metric arena.
- Complete coframe chart and supplied rank-two germ: `CONDITIONAL`; free generic witnesses are
  `free-and-explored` and are not claimed as physical histories.
- Completed-pair application of Dual Reciprocity: `WORKING_FOUNDATIONAL_CLARIFICATION`, explicitly
  adopted by Charles and externally accepted only within its stated bounds.
- `c_E`: `OBSERVED` calibration anchor; dimension-matched units may set its numerical coordinate
  value to one without changing the theorem.
- No sign, boundary, source, carrier, action, profile, `X_max`, bootstrap, radiative-transfer,
  observational, or fitted parameter is active.
- Omitted: event/germ realization, coincidence and null/degenerate strata, cut/focal loci, global
  topology and completion, path/connection/Jacobi/holonomy outputs, observations, dynamics, action,
  source, matter, mass, bootstrap, and signalling.

## Certification and falsification contract

- preregistration and exact source hashes banked before outcome computation;
- symbolic derivation from both arbitrary `E,J` and the complete block chart;
- independent exact-rational implementation sharing no production functions;
- generic full-sector, singular-`Y`, shift, covariance, orientation, and time-live controls;
- raw algebraic residuals exactly zero; no tolerance-substituted certification;
- current premise verifier and full repository regression suite pass;
- at least 20 semantic/mutation catches;
- a later fresh adversarial review is required before promotion beyond
  `VERIFIED_WITH_CAVEATS`.

Landing 1 is falsified by one declared regular complete-coframe witness for which the full pullback
does not feed the same unique density and scalar formula, or by one lawful gauge/coordinate change
that changes the result. Landings 2--4 are falsified by the generic proof plus independent full-
sector replay.

## Maximum conclusion

At most G179 may establish a local complete-coframe extension of the accepted scalar kernel on
supplied regular completed observer-pair germs, conditional on the working clarification. It cannot
select events or germs, prove a global UDT history or `X_max`, collapse non-scalar transport to the
scalar kernel, or validate SNe, BAO, CMB, radiative transfer, matter, source, action, or dynamics.

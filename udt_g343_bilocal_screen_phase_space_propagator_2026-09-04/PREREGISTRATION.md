# G343 preregistration — bilocal screen phase-space propagation

Date: 2026-09-04
Outcome status: analytic, computational, and independent-replay outcomes unseen

## Frozen question and inputs

Freeze the exact G341/G342 metric, regular component `T>0`, normal-observer null congruence, the
G341 parallel quotient-screen basis, all projective directions `rho in [0,1]`, arbitrary positive
endpoint triples, one arbitrary positive-time reference event `T_*`, one positive reference
frequency `nu=(dT/ds)|T_*` held fixed along each ray, and every supplied compact-lattice lift. The
regular chart is `rho=T_*^2/(T_*^2+lambda^2)` and may never be formed by adding unlike dimensionful
momentum components. Endpoint order is free: future propagation has `T_1>T_0`, while algebraic
reversal is tested for both orders. Changing `T_*` must be tested as a coordinate/gauge change, not
treated as a different ray or physical scale.

No luminosity, electromagnetic transfer, source spectrum, detector, observed distance, radar
choice, route population, topology selection, matter model, scale, `X_max`, stability criterion,
or canon claim may enter.

## Preregistered primary alternatives

1. `A__FULL_BILOCAL_PHASE_SPACE_PROPAGATOR_CLOSES__EXACT_COMPOSITION_SYMPLECTICITY_AND_TYPED_RECIPROCITY`:
   all four blocks are regular for every positive endpoint pair and projective direction; the map
   composes exactly in one affine gauge, preserves the screen Wronskian, reverses by matrix inverse,
   and separately source-normalized endpoint maps obey a derived frequency-rescaling conjugation.
2. `B__BILOCAL_PROPAGATOR_CLOSES_BUT_ONLY_A_CONFORMAL_WRONSKIAN_OR_RESTRICTED_RECIPROCITY_SURVIVES`:
   the metric gives a complete map, but a nontrivial common factor or restricted direction/domain
   prevents exact canonical symplecticity or the proposed endpoint-normalization law.
3. `C__G342_VERTEX_MAP_DOES_NOT_EXTEND_TO_A_GLOBAL_BILOCAL_FUNDAMENTAL_MAP`:
   a missed screen-basis, affine-gauge, endpoint, or principal-chart defect breaks composition,
   reversal, or rank on a regular ray.
4. `D__ONLY_NUMERICAL_OR_LOCAL_PHASE_SPACE_PROPAGATION_IS_CERTIFIED`:
   bounded integration succeeds but exact formulas or global endpoint/direction proofs fail.

## Preregistered secondary alternatives

- composition: `C1__EXACT_GROUPoid_COMPOSITION_ON_EACH_FIXED_LIFT` or
  `C2__COMPOSITION_REQUIRES_UNOWNED_PATH_OR_ENDPOINT_DATA`;
- Wronskian: `W1__EXACT_CANONICAL_SYMPLECTIC` or `W2__ONLY_CONFORMALLY_SYMPLECTIC`;
- reversal: `R1__COMMON_AFFINE_INVERSE_AND_SOURCE_NORMALIZED_FREQUENCY_FACTOR` or
  `R2__BARE_OR_TYPED_ENDPOINT_RECIPROCITY_FAILS`;
- principal limits: `P1__BOTH_LIMITS_REGULAR_AND_LONGITUDINAL_LIMIT_IS_FREE_PROPAGATION` or
  `P2__ONE_LIMIT_LOSES_A_PHASE_SPACE_DIRECTION`;
- quotient: `Q1__EACH_LIFT_RETAINS_A_SEPARATE_PROPAGATOR_AND_COMPOSES_ONLY_ALONG_ITS_OWN_RAY` or
  `Q2__QUOTIENT_IDENTIFICATION_CHANGES_THE_PER_LIFT_MAP`.

## Required derivation and evidence

1. Rebuild the fixed-affine ray and metric tidal matrix in the regular `rho` chart. Derive two
   nonvanishing scalar Jacobi solutions, their bilocal integral kernels, and all `A,B,C,D` blocks.
   Do not define the tide from the proposed propagator.
2. Prove algebraically that each scalar block has unit Wronskian and that the assembled `4 x 4`
   matrix obeys `M^T J M=J`. Prove composition from a common fundamental basis, then test it directly.
3. Prove common-affine endpoint reversal `M(T_0,T_1)=M(T_1,T_0)^{-1}` and the antisymmetry of the
   bilocal position block. Derive, rather than posit, the conjugation and frequency factor produced
   when each endpoint resets emitted frequency to one.
4. Recover G342's two source-normalized vertex widths and both principal limits exactly. Any
   singularity or unexplained normalization mismatch selects `C` or `D`.
5. Prove and test reference-event covariance by changing `T_*`, converting `rho` and `nu` through
   the same invariant `lambda` and affine tangent, and recovering the identical `4 x 4` map.
6. Production must cover at least 6,000 checks over logarithmically distributed endpoint triples,
   reference events, direction values including both axes and near-axis cases, and affine gauges.
   Independent code
   may not import production or G341/G342 implementation and must use direct first-order Jacobi
   integration plus an implementation-distinct fundamental-matrix route for at least 2,500 checks.
7. Raw double-precision relative tolerance is `5e-9` for quadrature identities and `2e-7` for the
   independent ODE route. Exact algebraic identities are required where available.
8. Hostile mutations must catch at least: hidden `T_*=1` scale, independently renormalized
   intermediate affine gauges,
   wrong composition order, reversal without inversion, wrong bilocal `B` sign, swapped `A/D`,
   curvature sign flip, injected screen mixing, broken Wronskian, lost longitudinal limit, lost
   transverse limit, deleted compact path label, and promotion to luminosity/distance/scale.
9. Every script must run with `python3 -S`, support `UDT_NO_WRITE=1`, and preserve evidence bytes in
   no-write mode.

## Premise and completeness gate

This is one exact-spacetime, one-observer-congruence, one-null-ray-family tile. The complete two-screen
linear Jacobi phase space is live; no screen component is frozen. Generic G332 developments,
perturbed metrics, accelerated observers, nonlinear congruence behavior, physical branch population,
matter, and radiative transfer are omitted and remain capable of carrying additional structure.
The computation characterizes all endpoint orders and directions in this tile; it does not filter
solutions by desired optical behavior.

## Maximum conclusion

The maximum allowed landing is an exact, independently checked bilocal geometric phase-space
classification on the supplied G341/G342 spacetime and supplied labelled null rays. No result may be
called a luminosity prediction, physical distance, selected signal path, generic UDT spacetime,
physical scale, `X_max`, stability theorem, or canon.

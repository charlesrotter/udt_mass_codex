# F01/F02 observer-sky Jacobi controls — preregistration

Date: 2026-08-11  
Base commit: `0634b7f801253fc105d374c4c160dbbe19f5b9de`  
Mode: metric-led; bounded exact/CPU algebra; no eigensolve or fit

## Whole question

For one identical, explicitly typed observer-sky comparison query, what local screen Jacobi map is
returned by the round zero-mixing F01 control and by the round axis-regular mixing-on F02 control?
Which of the two historical affine angular-projection freedoms is replaced by metric geometry at
the first nontrivial local order, and which remains query-, profile-, boundary-, or source-owned?

This is a control comparison. F01 and F02 are not candidate universes and will not be ranked.

## Frozen geometry universe

Exactly two stationary local control families are admitted:

```text
F01: ds^2=-A(r)dt^2+dr^2/A(r)+r^2[dtheta^2+sin^2(theta)dpsi^2]

F02: ds^2=-A(r)dt^2+dr^2/A(r)+r^2[dtheta^2+sin^2(theta)dpsi^2]
          +2h(r)sin^2(theta)dt dpsi.
```

Assume only the regular Lorentzian stratum `r>0`, `A>0`, and
`D=A r^2+h^2 sin^2(theta)>0`. The local jets of `A` and `h` are
`free-and-explored` symbolic data. No P1 SNe pair profile is copied into `A`; no wall, global
profile, source, population, bootstrap value, or field equation is supplied.

## Identical observer-sky query Qsky

At a regular equatorial event `p=(t0,r0,pi/2,psi0)`, choose the stationary unit observer
`u=A^(-1/2) partial_t`, the outward unit radial direction `n=A^(1/2) partial_r`, and the oriented
orthonormal screen `(E_theta,E_psi)` obtained from the metric by Gram orthogonalization in the
`theta` and `t-psi` planes. Let `k=u+n` be the future/outward null comparison direction.

The metric defines the affinely parameterized null geodesic `gamma` with initial data `(p,k)`.
Parallel transport the screen along `gamma`. Define two query-owned Jacobi fields by

```text
J_B(0)=0,
nabla_k J_B(0)=E_B,
nabla_k nabla_k J_B+R(J_B,k)k=0.
```

The screen Jacobi matrix is `mathcal_D_AB(s)=g(E_A,J_B)`. With the declared curvature convention,

```text
mathcal_D(0)=0,
mathcal_D'(0)=I,
mathcal_D(s)=s I-(s^3/6) mathcal_T(0)+O(s^4),
mathcal_T_AB=g(E_A,R(E_B,k)k).
```

This is an inter-observer/celestial-screen comparison query. The null generator is geometric query
data; it is not being interpreted as local material signalling in the co-present framing.

## Premise stamps

- `c_E`: `OBSERVED` local clock/ruler calibration. Algebra may use units `c_E=1`; dimensions must
  be restorable and no local variable speed is inferred.
- F01: `CHOSE` round, zero-mixing control.
- F02: `CHOSE` conditional round, axis-regular mixing-on control.
- stationary observer, equatorial event, radial initial direction, outward sign, and screen
  orientation: `CHOSE` query controls, held identical by construction.
- geodesic/Jacobi construction: `DERIVED` from each supplied metric and the declared initial query.
- `A(r)`, `h(r)` and local jets: `free-and-explored`; no fitted or preferred numerical profile.
- P1 SNe result: `CONDITIONAL` low-redshift pair-compatibility anchor only; inactive in the local
  coefficient derivation.
- `c_eff^(pair)`: `CONDITIONAL` inter-observer terminal readout; not used as a local propagation
  law.
- `X_max`: `WORKING` pair asymptotic guard; inactive locally.
- co-presence: `POSIT` interpretation; not a signalling mechanism.
- action, source, bootstrap, mode population, polarization source, and physical CMB query:
  `OPEN` and inactive.

## Required calculation

1. Derive the exact equatorial tetrad and prove it is orthonormal in both controls.
2. Derive the exact local optical/Jacobi tidal matrix `mathcal_T` for F02.
3. Take the exact `h -> 0` limit and compare it with an independently derived F01 result.
4. Classify trace (area focusing), trace-free symmetric part (shear), and antisymmetric/rotation
   content at the registered local order.
5. State which terms depend on local profile jets and which are fixed by the round/angular or mixing
   structure.
6. Preserve degeneracies and special subloci; do not discard them because they simplify or fail to
   resemble a desired sky.

## Certification and falsification

The package fails closed if:

1. F01/F02 source formulas or frozen source hashes change;
2. the query differs between F01 and F02 except for metric-derived orthonormalization;
3. `h`, its derivatives, or complete `t-psi` mixing are silently zeroed in F02;
4. the F02 result does not reduce exactly to the independently derived F01 result at `h=0`;
5. the tetrad, null condition, Riemann symmetries, screen symmetry, or Jacobi initial conditions fail;
6. a local Taylor coefficient is promoted to a finite-distance map without integrating a supplied
   global profile;
7. a screen map is promoted to nonzero TT power without a source/state covariance;
8. an `SO(2)` screen-basis rotation is claimed to change scalar TT by itself;
9. the calculation infers local signalling, selects F01/F02, imports P1 as a centered lapse, or
   activates `X_max` as a local wall;
10. the production and independent checks share the load-bearing curvature implementation.

Certification requires exact symbolic production algebra, a separately implemented independent
control for the load-bearing F01 limit and selected F02 substitutions, exercised catch-proofs,
repository gates, and fresh adversarial semantic review before a scientific verdict is banked.

## Allowed landings

Exactly one primary landing will be used:

1. `LOCAL_SKY_MAP_GEOMETRY_DISTINGUISHES_F01_F02_WITH_PROFILE_REMAINDER`;
2. `LOCAL_SKY_MAP_IDENTICAL_AT_REGISTERED_ORDER`;
3. `QUERY_OWNS_ONLY_FORMAL_JACOBI_OPERATOR_WITHOUT_EVALUABLE_CONTROL`;
4. `TYPE_OR_REGULARITY_FAILURE`;
5. `ALGEBRAICALLY_OR_NUMERICALLY_UNRESOLVED`.

Maximum conclusion: a local, two-control, preregistered screen-Jacobi classification and an exact
account of which affine projection freedoms geometry does or does not remove. No CMB prediction,
screen selection, finite-distance angular scale, source/population law, polarization prediction,
FD2 restart, action, bootstrap result, local signal law, `X_max` value, or native dynamics follows.


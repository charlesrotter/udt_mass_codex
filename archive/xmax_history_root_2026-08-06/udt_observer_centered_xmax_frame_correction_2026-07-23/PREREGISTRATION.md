# Observer-centered Xmax/frame correction — preregistration

Date: 2026-07-23

Base: `0e16bea8a1e26b4250d55d551b3ca34a6f43a659`

Compute: bounded CPU-only exact algebra.

## Reason for correction

The frozen parent package
`udt_wrl_xmax_lightcone_frame_audit_2026-07-23/` treated curves with
changing WR-L areal coordinate `r` as inward/outward physical observers
relative to one fixed spherical center. Charles corrected that
interpretation:

1. there is no preferred inertial observational frame;
2. an observer does not physically move inward or outward relative to an
   absolute cosmic center;
3. each inertial observer owns an equivalent centered observational frame;
4. inertial frame changes preserve the light-cone structure; and
5. acceleration, not uniform relative motion, is the only presently
   admitted trigger for a changed within-frame connection/light-cone
   presentation.

The parent algebra is preserved as historical evidence. Its physical
observer and crossing language is to be regraded, not silently edited.

## Whole question

For the recorded WR-L branch

```text
A(r)=1-r/X,
ds2=-A c_E^2 dt2+A^-1 dr2+r2 dOmega2,
0<r<X,
```

determine:

1. what the metric derives for the relational clock/ruler asymptote in
   one observer-centered chart;
2. whether the regular continuation through `A=0` is an admissible
   continuation of that same clock/ruler polarization;
3. whether two distinct observer-centered WR-L charts can be ordinary
   overlapping coordinate charts of the same tensor geometry;
4. what inertial coframe equivalence derives locally;
5. what a time/space-dependent coframe change does to connection,
   curvature, and the invariant cone; and
6. which additional observer-composition or acceleration-response law
   remains missing.

## Observing or targeting

`OBSERVING`. No desired hard edge, GR horizon, particle, action, carrier,
source, or Hopf result is targeted.

## Scope

Covered:

- the exact static/spherical WR-L tensor branch on `0<r<X`;
- its centered clock/ruler polarization;
- exact scalar invariants;
- local radial orthonormal coframes;
- constant and smooth local `SO+(1,1)` frame changes;
- the regular ingoing chart as a test of manifold extendibility;
- the logical status of observer-centered recentering.

Not covered:

- a complete observer-indexed UDT metric or composition law;
- a law converting acceleration into a new physical metric solution;
- matter motion, signalling, sources, action, mass dynamics, or force;
- global topology, quotient, seam, angular completion, or a second cell;
- time-live field equations;
- selection or numerical evaluation of `Xmax`;
- native matter mass at the asymptote;
- the carrier or Hopf sector.

## Premise classification

Every premise is registered in `PREMISE_LEDGER.tsv`.

In particular:

- `c_E` is the measured ordinary-regime clock/length anchor;
- no preferred macroscopic inertial observational frame is
  `OWNER_LOCKED`;
- common `Xmax` remains an owner working frame premise/global-output
  expectation, not a derived numerical scale;
- `r` is a nonnegative observer-centered separation/depth coordinate,
  not an absolute signed position;
- the WR-L profile is `DERIVED_CONDITIONAL_WRL`;
- the fixed clock/ruler polarization is tested explicitly rather than
  silently inherited beyond `A=0`;
- no GR field equation, equivalence principle, or imported observer
  mechanics is used.

## Preregistered derivations

### D1 — centered clock/ruler admissibility

Compute the signs and limits of

```text
g_tt=-A c_E^2,
g_rr=A^-1,
theta0=sqrt(A)c_E dt,
theta1=dr/sqrt(A).
```

The same centered clock/ruler interpretation is admissible only while
`A>0`. Test whether `A<0` swaps the time and ruler roles.

### D2 — relational asymptote

Recompute

```text
d tau_rel/dt=sqrt(A),
d ell/dr=1/sqrt(A),
dr_star/dr=1/A,
phi=-log(A)/2.
```

These are relational chart statements. Do not call their users
“stationary observers.”

### D3 — manifold continuation versus observer continuation

Recompute the regular ingoing radial form

```text
ds2_rad=-A dv2+2 dv dr.
```

Classify any causal curve in that extension only as a mathematical
manifold curve unless an observer-centered chart/composition map is also
supplied.

### D4 — distinct-center compatibility

Compute exact scalar invariants, including

```text
R=6/(X r),
K=8/(X^2 r^2).
```

If two distinct observer-centered charts are charts of the same tensor
geometry on an overlap, scalar invariance requires their radial labels to
agree pointwise. Test whether this permits a genuine recentering.

### D5 — local inertial and accelerated coframes

Derive the connected radial orthonormal frame group from metric
preservation. For smooth local rapidity `eta`, recompute the connection
transformation and curvature. Distinguish:

- a constant local inertial-frame basis change;
- a varying/accelerated coframe presentation;
- a physical acceleration-induced change of the metric.

Only the first two are available from the recorded metric.

### D6 — parent regrade

Regrade every load-bearing parent statement containing:

```text
static observer
moving observer
crossing observer
universal crossability
frame-invariant X sphere
angular obstruction to reciprocity
acceleration warps curvature
```

Exact algebra may survive while physical interpretation is withdrawn.

## Falsification and certification

The proposed centered-chart incompatibility is false if an explicit
nontrivial recentering diffeomorphism preserves all scalar invariants of
the WR-L metric on an overlap.

The fixed-polarization edge claim is false if the same `t`-clock and
`r`-ruler roles remain respectively timelike and spacelike through
`A=0`.

The physical-crossing withdrawal is false if the parent crossing witness
already supplies two equivalent observer-centered charts and their
complete transition law.

The pure-frame acceleration result is false if a smooth Lorentz coframe
change alters an invariant curvature scalar or the invariant null cone.

Certification requires:

1. exact symbolic or rational checks;
2. an independent implementation that does not import the production
   module;
3. semantic catch-proofs rejecting physical crossing language,
   preferred-center language, derived common `Xmax`, and native mass
   closure;
4. source-hash verification;
5. all repository, frozen-package, current-path, frontier, test, and
   dirty-checkout gates.

## Maximum allowed conclusion

```text
THE_WRL_ALGEBRA_DERIVES_A_CENTERED_RELATIONAL_CLOCK_RULER_ASYMPTOTE_AT_A_ZERO_AND_NO_ADMISSIBLE_CONTINUATION_PRESERVING_THE_SAME_CLOCK_RULER_POLARIZATION;THE_REGULAR_INGOING_EXTENSION_PROVES_ONLY_MANIFOLD_EXTENDIBILITY_NOT_A_PHYSICAL_OBSERVER_CROSSING;DISTINCT_OBSERVER_CENTERS_CANNOT_BE_STANDARD_OVERLAPPING_COORDINATE_CHARTS_OF_THE_SAME_NONHOMOGENEOUS_WRL_TENSOR_GEOMETRY;LOCAL_INERTIAL_FRAME_EQUIVALENCE_IS_DERIVED_BUT_GLOBAL_OBSERVER_RECENTERING_AND_COMMON_XMAX_REQUIRE_AN_OBSERVER_INDEXED_COMPOSITION_LAW_OR_COMPLETE_METRIC_NOT_YET_DERIVED;A_VARYING_COFRAME_CHANGES_CONNECTION_COMPONENTS_BUT_NOT_INVARIANT_CURVATURE_OR_CONES_WITHOUT_A_PHYSICAL_METRIC_RESPONSE_LAW
```

Maximum grade: `VERIFIED-WITH-CAVEATS`.

No canonization, navigation edit, GPU work, physics mechanism, action,
carrier, source, mass closure, or repository reorganization is authorized.

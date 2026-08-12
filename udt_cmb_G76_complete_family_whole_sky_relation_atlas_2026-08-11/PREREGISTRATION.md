# G76 preregistration — complete-family whole-sky relation atlas

Date: 2026-08-11

Base: `122d1aee624b133438e4cb0ef06d57c1e5397954`

Status before computation: not run; no G75 whole-sky response inspected.

## Whole question

For every one of the `591` profiles in the externally verified G75 stationary axial control
family, what complete initial-direction-sphere relation is produced by the metric between the
registered observer sphere `x=1/4` and the first outward crossing of the registered comparison
sphere `x=1`?

The calculation will characterize crossing, branch/turn behavior, signed angular area, local
angular singular values, orientation, and sampled critical approach. It will not seek a desired
CMB pattern, rank profiles, populate a source, or fit observations.

This is metric-led solution-space mapping, not template-led CMB fitting.

## Frozen metric and exact variable-profile Hamiltonian

Use dimensionless `R=c_E=1` coordinates only for this scale-neutral angular relation. The supplied
stationary axial metric is

```text
ds^2 = -A dt^2 + dx^2/A + x^2(dtheta^2 + sin^2(theta)dpsi^2)
       + 2 h(x) sin^2(theta) dt dpsi,
A=1+a x^2,
h=x^2 q(x^2).
```

In Cartesian spatial coordinates `X=(X,Y,Z)`, put

```text
s = X.X,
rho2 = X^2+Y^2,
Lz = X pY-Y pX,
q = q(s),
B = 1+a s+q^2 rho2,
E = p_t-q Lz.
```

The metric inverse must be independently reconstructed before trajectory inspection. The proposed
exact null Hamiltonian is

```text
H = 1/2 [p.p + a(X.p)^2 - E^2/B].
```

The variable-profile terms must remain live. With `dq=2 q_s X`,

```text
dB = 2a X + 2q rho2 dq + 2q^2(X,Y,0),
dLz = (pY,-pX,0),
dX/dlambda = p + a(X.p)X + (E/B)q(-Y,X,0),
dp/dlambda = -a(X.p)p - (E/B)(Lz dq+q dLz) - (E^2/(2B^2))dB,
dt/dlambda = -E/B.
```

No constant-`q` substitution is allowed. The `q_s` terms are load-bearing.

## Frozen candidate universe

- All `591/591` rows of G75 `PROFILE_ATLAS.tsv` are included.
- All `49` shape rays, all four amplitudes, all three lapse controls, and all three zero controls
  are retained.
- No representative reduction, response-based pruning, or post-outcome retuning is allowed.
- The globally reflected partner `q -> -q` is retained analytically through `psi -> -psi`; a
  preregistered numerical reflection audit will use all nonzero rows at a coarser mesh without
  treating the orientation partner as a separately selected physical universe.

## Frozen observer query

- observer position: Cartesian `(x,y,z)=(1/4,0,0)`;
- initial directions: the complete unit sphere in the metric-orthonormal observer frame;
- endpoint: first outward crossing of `|X|=1`;
- path: full four-coordinate future null Hamiltonian flow;
- affine cap: `4`;
- no path is discarded for turning, missing the endpoint, orientation reversal, or small angular
  area. Those outcomes are classifications.

This exactly preserves the G74 control query. It is not last scattering, `X_max`, a finite-cell
seal, a local signalling experiment, or a selected physical observer.

## Frozen numerical census

Production uses vectorized CPU `float64` RK4 with checkpoint/restart by profile:

- icosphere levels `2,3,4` (`162,642,2562` initial directions);
- `1024` steps at all levels;
- an additional `512`-step level-4 pass;
- every one of the `591` profiles;
- a coarse level-3 reflected-partner audit for every nonzero profile.

These are numeric controls, not physics. Runtime is not a scientific acceptance criterion. If the
full census is interrupted, resume from checkpoints; do not reduce the family after seeing partial
responses.

## Output invariants and classifications

For every profile and mesh level record:

- endpoint directions and crossing mask;
- endpoint coordinate time and affine parameter;
- Hamiltonian backward error;
- missing/active directions and turning evidence;
- signed spherical triangle-area ratios and degree estimate;
- minimum/maximum signed area ratio;
- negative-face counts;
- absolute-area counts below `1e-2`, `1e-3`, and `1e-4` (diagnostic thresholds only);
- per-face intrinsic tangent-map singular values and their ratio where numerically defined;
- local orientation sign.

The endpoint-map singular values characterize angular scale and shear using the round metrics on
the input and output direction spheres. They do not provide G72's path-carried polar rotation.
Physical screen transport and source/population response remain open.

Allowed sampled classes are descriptive, not filters:

- `SAMPLED_COMPLETE_ORIENTATION_PRESERVING`;
- `SAMPLED_ORIENTATION_REVERSING_OR_FOLD_CANDIDATE`;
- `SAMPLED_MISSING_OR_MULTIBRANCH_CANDIDATE`;
- `NUMERICALLY_UNRESOLVED`.

## Independent equation and regression controls

Before interpreting G75 outcomes:

1. SymPy must invert the declared Cartesian metric and reproduce the registered Hamiltonian.
2. SymPy differentiation of `H` at preregistered rational/random control points must agree with
   the hand-coded variable-`q` RHS.
3. `q=constant` rows must reproduce the G74 production endpoints and summaries within the frozen
   numerical thresholds.
4. All three `q=0` rows must reproduce the exact F01 degree-one map.
5. The numerical `q -> -q` relation must match the exact `psi -> -psi` reflection on the registered
   coarse census.

The fresh adversarial verifier must independently reconstruct the variable-profile terms and rerun
at least one row from each of the eight exact G75 strata, including both lapse extremes and both
amplitude extremes across the selected verifier panel.

## Certification thresholds

Thresholds are frozen before response inspection:

- level-4 endpoint chord difference, `512` versus `1024` steps: `<=5e-5` for a resolved row;
- level-3 to level-4 degree drift: `<=5e-4` for a resolved row;
- maximum absolute Hamiltonian drift: `<=1e-6` for a resolved row;
- F01 endpoint chord error from the identity sky map: `<=2e-6`;
- constant-profile G74 endpoint replay: `<=5e-6`;
- reflected-partner endpoint/reflection error: `<=2e-5`.

Exceeding a threshold yields `NUMERICALLY_UNRESOLVED`; it does not remove the row or become a
physical negative. No threshold may be relaxed after inspection.

## Allowed landings

- `COMPLETE_FROZEN_FAMILY_SAMPLED_REGULAR`;
- `MIXED_SAMPLED_GLOBAL_RELATION_CLASSES`;
- `CRITICAL_OR_MULTIBRANCH_CANDIDATES_PRESENT`;
- `NUMERICALLY_UNRESOLVED_FAMILY`;
- `TYPE_OR_IMPLEMENTATION_FAILURE`.

## Maximum allowed conclusion

At most, G76 may classify the sampled whole-sky endpoint relation and intrinsic angular distortion
for the complete frozen G75 family under this supplied stationary observer query. It cannot select
the physical profile, source, CMB endpoint, universe size, `R`, `X_max`, bootstrap state, action,
matter source, TT/TE/EE/BB spectrum, polarization, local signal law, or generic complete metric.

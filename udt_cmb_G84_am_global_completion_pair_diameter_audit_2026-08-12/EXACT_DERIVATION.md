# G84 exact derivation — AM spatial completion and observer-patch asymptote

## 1. Scope and metric

The frozen stationary axial `AM` control family is

```text
ds^2/R^2 = -A(x) dτ^2 + dx^2/A(x)
            + x^2(dθ^2+sin(θ)^2 dψ^2)
            + 2 h(x) sin(θ)^2 dτ dψ,
A(x)=1-x^2/4,
h(x)=x^2 q(x^2),
τ=c_E t/R.
```

All `197` exact AM controls are retained. Their G75 authority stops at `x=1`; everything below
that uses `x>1` is a transparent `FREE_AND_EXPLORED` continuation. `R` remains symbolic and
unselected.

## 2. The spatial geometry hidden by the areal-radius chart

Set

```text
x = 2 sin(χ).
```

On either monotone chart branch,

```text
A = cos(χ)^2,
dx^2/A = 4 dχ^2.
```

Therefore every AM profile has the same intrinsic spatial metric

```text
dℓ^2 = 4R^2[dχ^2+sin(χ)^2 dΩ^2].
```

The minimal doubled, simply connected spatial completion candidate `0<=χ<=π` is the round
three-sphere of radius `2R`. The local continuation does not uniquely select this topology; smooth
quotients or other global identifications require a separate global-completion rule.
This follows directly from the Euclidean embedding

```text
Y=(2R cosχ, 2R sinχ n),  n in S^2.
```

Consequently,

```text
sectional curvature = 1/(4R^2),
scalar curvature    = 3/(2R^2),
injectivity radius  = 2πR,
spatial diameter    = 2πR.
```

For embedded points `Y_p,Y_q`, the exact completed spatial distance is

```text
d_S3(p,q) = 2R arccos[(Y_p·Y_q)/(4R^2)].
```

The map `x=2sinχ` is two-to-one off its maximum on the doubled sphere. Thus `x=2` is the equator,
not the antipode and not the spatial diameter. A north-pole observer reaches that equator after
proper radial distance `πR`; its antipode is `2πR` away.

This derives an intrinsic spatial completion candidate. It does not make that spatial distance the
physical UDT observer-pair separation.

## 3. Zero-mixing spacetime extension

For the single zero-mixing row, the full continued metric is

```text
ds^2/R^2 = -cos(χ)^2 dτ^2
            +4[dχ^2+sin(χ)^2dΩ^2].
```

It is the static presentation of the smooth constant-curvature Lorentzian hyperboloid

```text
-X0^2+X1^2+X2^2+X3^2+X4^2 = 4R^2
```

under

```text
X0 = 2R cosχ sinh(τ/2),
X4 = 2R cosχ cosh(τ/2),
(X1,X2,X3) = 2R sinχ n.
```

Direct pullback returns the displayed metric. The static coordinates cover two static regions and
collapse at the bifurcation sphere; additional time-live charts cover the remaining hyperboloid.
Thus the lapse zero is a stationary-chart horizon, not a material edge or manifold boundary.

The hyperboloid is homogeneous. Algebraically, its isometry group acts transitively on oriented
timelike two-planes through the embedding origin, hence on the corresponding central timelike
geodesic observer frames. Each such observer admits an equivalent recentered static patch.
This establishes frame sharing only for that geodesic-observer isometry orbit, not for arbitrary
accelerated observers or nonzero-mixing profiles.

## 4. Recentered stationary pair law on the zero-mixing branch

Let `s` be outward spatial proper distance on one recentered static slice from its central geodesic
observer. Since `s=2Rχ`, the stationary lapse is

```text
A(s)=cos[s/(2R)]^2,       0<=s<πR.
```

With the receiver normalized at the patch center, the G79/G83 Killing-observer depth and terminal
reciprocal readout become

```text
φ(s) = -log cos[s/(2R)],
c_eff(s)/c_E = exp[-2φ(s)] = cos[s/(2R)]^2.
```

Therefore

```text
s -> πR from below  =>  φ -> +infinity,
                         c_eff/c_E -> 0.
```

Every central geodesic observer in the isometry orbit receives the same stationary-patch limit
`πR`. This is the first exact frame-shared recentered asymptote in the current branch record.
Its exact status is

```text
DERIVED_CONDITIONAL_ZERO_MIXING_CONSTANT_CURVATURE_GEODESIC_OBSERVER_CLASS.
```

It is not yet physical `X_max`: zero mixing is one control, `R` is unselected, arbitrary
accelerated observers are not covered, and the physical pair-separation operator has not been
identified with this static-patch distance.

## 5. Why stationary depth is not global spatial distance

The completed spatial sphere and the observer-patch law are related but not identical:

1. North pole to equator has `d_S3=πR` and divergent stationary depth.
2. Entirely within the north static patch, take two observers at `χ=π/4` separated by angular
   angle `γ`. They have identical lapse and hence zero endpoint lapse-depth, while
   `d_S3/R=2 arccos[(1+cosγ)/2]` ranges continuously from zero to `π`. This avoids treating the
   opposite static patch as one future-directed stationary pair query.
3. Pairs lying within the equatorial two-sphere can have spatial distances ranging from zero to
   `2πR`, while the original stationary observer congruence becomes null there.

Thus no single-valued function `φ=f(d_S3)` exists even within one regular static patch of the
minimal completed spatial sphere. The candidate
`πR` is an observer-patch accessibility scale, not the global spatial diameter. If it becomes
physical `X_max`, then the missing UDT separation type cannot be unrestricted spatial geodesic
distance on the completed slice.

This resolves G83's receiver-dependent one-sided lengths only in the central-geodesic recentered
class. A receiver held at fixed nonzero radius is accelerated and is not silently promoted into
that class.

## 6. Complete nonzero-mixing continuation

In `χ`, the complete continued metric is

```text
ds^2/R^2 = -cos(χ)^2 dτ^2
            +4[dχ^2+sin(χ)^2dΩ^2]
            +2h(χ)sin(θ)^2dτdψ,
h(χ)=4sin(χ)^2 q(4sin(χ)^2).
```

At the equator, the `τ-ψ` block has determinant

```text
-h(π/2)^2 sin(θ)^4.
```

It is Lorentzian away from the axial fixed points when `h(π/2)!=0`. At either axial fixed point,
the axial Killing vector vanishes, the mixing one-form vanishes, and `g(∂τ,·)=0`; the analytic
`χ` continuation is genuinely degenerate there. A corotating redefinition cannot remove this
fixed-point kernel because adding the vanishing axial generator leaves `∂τ` unchanged on the axis.

Direct exact evaluation of every frozen AM polynomial at `s=x^2=4` gives:

```text
q(4)=0:     1 row, the zero-mixing control;
q(4)!=0: 196 rows.
```

Hence all 196 nonzero-mixing continuations are obstructed within this standard smooth,
stationary, axial, doubled/bifurcate extension class. This is not a generic no-go. A different
time-live completion, symmetry reduction, branch topology, or metric evolution could change the
extension problem, and none is supplied here.

## 7. Exact landing

```text
ZERO_MIXING_BRANCH_HAS_CONDITIONAL_FRAME_SHARED_RECENTERED_ASYMPTOTE
__NONZERO_MIXED_COMPLETION_OPEN
```

Maximum package conclusion:

`BOUNDED_AM_SPATIAL_COMPLETION_AND_STATIONARY_DEPTH_COMPATIBILITY_ATLAS`.

No physical profile, numerical `R`/`X_max`, generic observer theorem, CMB result, source, action,
matter law, bootstrap closure, boundary functional, local-signalling law, or time-live dynamics is
derived.

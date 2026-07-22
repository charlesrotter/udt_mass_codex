# UDT clock-anchor, scale-map, and threading audit

Date: 2026-07-22

Base: `e4075a05e6f64714e732f375641bd73447d3559c`

Preregistration commit: `c0da3e7bd847de458ed25fbd4e7f6afb3cd11047`

Mode: exact CPU metric algebra and source audit; no action, EOM, ODE/PDE, GPU, carrier, source,
boundary selection, physical-scale insertion, or navigation edit

Grade: `VERIFIED-WITH-CAVEATS`; independent standard-library rational tensor reconstruction passes,
while no fresh external-model semantic review was authorized

## Result first

Keeping the observed finite `c_E` explicit in the complete positive-`X` spherical areal form,

```text
h = -c_E^2 F(t,R)^2 X(t,R) dt^2 + X(t,R)^(-1)dR^2,
```

separates three exact objects:

```text
d tau/dt       = F sqrt(X),
d ell/dR       = 1/sqrt(X),
|dR/dt|_null   = c_E F X.
```

Comparing the orthonormal spatial component with the stationary local-frame clock component on the
metric-null differential,

```text
d ell/d tau_ref = c_E.
```

Thus `c_E` is the local dimensional metric conversion between the stationary frame's clock and
ruler components. `F` and `X` cancel in that relation. `d tau_ref` is not proper time along a null
curve—the latter is zero. `F` and `X` instead control the selected-coordinate and remote-comparison
readouts. This is compatible with a co-present ontology in which no foundational carrier is
presumed to traverse an external time. It does not derive a material propagation, detector
response, or instantaneous-access law.

## Reciprocity and the surviving threading factor

The reciprocal modulation itself obeys

```text
sqrt(X) × 1/sqrt(X) = 1.
```

The orbit-block determinant is instead

```text
det(h_tR) = -c_E^2 F^2.
```

One might set this determinant to `-c_E^2` and obtain `F=1`. That is not an invariant derivation. A
passive time relabeling `dt=s(t)dt_new` sends `F` to `sF` and the determinant to `s^2` times itself.
The condition fixes a synchronization/coordinate normalization.

A time-only multiplier can be absorbed locally in this way, but the radial content cannot. For the
static areal congruence with lapse `N=F sqrt(X)`, the acceleration one-form is

```text
a_R = partial_R log N
    = partial_R log F + (1/2) partial_R log X.
```

The `partial_R log F` term survives a time-only relabeling and changes curvature. Consequently `F`
is not wholly coordinate gauge.

## Complete static spherical curvature control

For

```text
g = -c_E^2 N(R)^2dt^2 + X(R)^(-1)dR^2 + R^2dOmega^2,
```

direct coordinate Riemann reconstruction gives the four independent orthonormal motifs

```text
clock–radial:   X N''/N + X' N'/(2N),
clock–angular:  X N'/(R N),
radial–angular: -X'/(2R),
angular:        (1-X)/R^2.
```

The exact Kretschmann invariant is

```text
K = 4[clock-radial^2
      +2 clock-angular^2
      +2 radial-angular^2
      +angular^2].
```

This positive sum supplies the endpoint certification without an action or field equation.

For `C^2` Taylor data at a bounded-curvature spherical areal center it requires

```text
X(0)=1,
X'(0)=0,
0<N(0)<infinity,
N'(0)=0.
```

The remaining second derivatives determine finite center curvature.

### Inner radial-clock divergence

At the balanced control `X=1`, take `F=N=R^(-q)` with `q>0`. Then

```text
K = 4 q^2 (q^2+2q+3)/R^4,
```

which diverges. If instead `X=R^(-p)` with `p>0`, the angular term alone gives

```text
K >= 4(R^p-1)^2/R^(2p+4).
```

Therefore an infinite radial clock factor or reciprocal scalar is curvature-singular when physical
smallness is identified with a regular spherical areal center. This conclusion does not cover a
nonspherical, noncentral, toric/Hopf, throat, quotient, or otherwise different intrinsic small-scale
limit. Nor has the repository derived a map from subnuclear separation to `R->0`.

## Finite-cell and bootstrap ownership of `F`

Let `y=R/X_max` and consider the positive deformation

```text
F_epsilon = exp[epsilon y^3(1-y)^3].
```

At `R=0` and `R=X_max`, `F_epsilon=1` and its first two radial derivatives vanish, exactly matching
the undeformed control through the curvature-relevant endpoint jets. With fixed
`X=1-R/X_max`, the clock–radial curvature difference at the half-cell is

```text
-3 epsilon/(16 X_max^2).
```

Thus endpoint and seal data do not determine the interior threading even when second jets are held
fixed. The counterfamily is bounded evidence against that implication, not a complete UDT universe.

Source adjudication also finds:

- pair Reciprocity owns the inverse `X` modulation, not `F`;
- macro observer reciprocity requires tensor covariance, not identical coordinate `F`;
- CSN treats the pre-scale common factor as calibration rather than selecting a representative;
- registered bootstrap is on-shell admissibility and supplies no operational input/map/output
  relation for `F`; and
- the clock–curvature equation could constrain lapse only as its already recorded conditional
  post-scale premise. It is not current native authority.

## Outer endpoint classification

Write near an endpoint

```text
X ~ delta^p,
F ~ delta^q,
p>0.
```

Then

```text
clock factor             ~ delta^(q+p/2),
coordinate slope/c_E     ~ delta^(q+p),
radial ruler factor      ~ delta^(-p/2).
```

Both the clock factor and coordinate slope vanish when `q>-p/2`. The WR-L control has `p=1,q=0`
and lies in this class. Other `F` asymptotics can produce finite or divergent clock factors even
while the coordinate slope vanishes. Therefore “time and effective speed approach zero at
`X_max`” is a coherent conditional class, not a consequence of `X->0` alone.

No endpoint is identified here with the physical CMB, universe boundary, or selected `X_max`.

## Absolute scale and regime map

The independent dimension matrix for `(c_E,G_obs,M,L)` has rank three and the single null generator

```text
(-2,1,1,-1),
```

corresponding to

```text
G_obs M/(c_E^2 L).
```

There is no nonzero dimensionless or absolute-scale monomial made from `c_E` and `G_obs` alone.
They calibrate mass per length but do not select an absolute length, mass, `X_max`, or a map from
dimensionless metric depth to terrestrial/cosmological/subnuclear regimes.

Keeping `c_E` visible therefore corrects the semantics without closing the scale problem.

## Evidence and verification

Fifteen exact post-firewall sources are frozen in `SOURCE_LINEAGE.tsv`. The production SymPy route
passes 24/24 exact checks. A separate standard-library `Fraction` implementation independently
rebuilds a generic metric two-jet and complete coordinate Riemann tensor, matches all four curvature
motifs and `K`, checks the local `c_E` cancellation, center limits, both divergent controls,
endpoint-flat deformation, and dimensional rank. It passes 18/18 exact checks and 18/18 exercised
corruption catches.

## Four evidence gates

1. **Preregistered:** yes; commit `c0da3e7` precedes production algebra and adjudication.
2. **Full or bounded:** complete for the positive-`X` orthogonal areal clock/ruler readouts,
   arbitrary static spherical `N(R),X(R)` curvature, endpoint power classes, and the enumerated
   registered selectors. General time-live curvature and nonspherical intrinsic small-scale limits
   remain outside it.
3. **Independently verified:** yes for the load-bearing metric, curvature, endpoint, scale, source,
   and ledger claims. No fresh external-model semantic review was authorized.
4. **Premises audited:** `c_E`, inverse conversion, co-presence, Reciprocity, observer covariance,
   CSN, finite cell, seal, bootstrap, WR-L, clock curvature, scale, micro mapping, action, matter,
   and topology limits are explicit.

## Stop line

No carrier, operational signal law, action, source, boundary functional, density, mass, `X_max`,
physical micro scale, topology, ODE/PDE, GPU run, canon, or navigation change is selected.

Maximum conclusion:

```text
C_E IS THE EXPLICIT LOCAL METRIC CLOCK–LENGTH ANCHOR;
F AND X CONTROL DISTINCT REMOTE/CURRENT-COORDINATE READOUTS;
CURRENT RECIPROCITY, CSN, FINITE-CELL, SEAL, AND BOOTSTRAP DO NOT FIX F OR THE SCALE MAP;
OUTER FREEZE IS A CONDITIONAL COMBINED-ASYMPTOTIC CLASS;
INNER INFINITY IS SINGULAR AT A REGULAR SPHERICAL AREAL CENTER BUT REMAINS OPEN IN NONCENTRAL GEOMETRY.
```

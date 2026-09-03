# G337 exact derivation — inherited third response on double silence

Date: 2026-09-03
Grade: `DERIVED_CONDITIONAL_BOUNDED__INDEPENDENTLY_VERIFIED__PENDING_EXTERNAL_REVIEW`

## 1. Landing

```text
G337_FULL_INITIAL_FIELDS_OWN_INHERITED_DOUBLE_SILENT_THIRD_JET
__POINTWISE_R_B_C_LAMBDA_MU_TUPLE_DOES_NOT
__SPATIAL_JETS_SURVIVE
__BOTH_STRICT_ROOTS_AND_NONZERO_HOMOGENEOUS_RESPONSE_RETAINED
__NO_FINITE_TIME_STABILITY_OR_HISTORY_SELECTION
```

This theorem is conditional on the owner-provisional Universal Reciprocity/DDR and G312 premises
inside their bounded regular metric-only vacuum arena. It is not a derivation of those premises.

## 2. Exact third-jet identity

Use the G315 Gaussian-normal convention

```text
n gamma = -2K,
F := nK = Ric3 + tau K - 2B - Lambda gamma,
B := K gamma^{-1} K,
tau := tr_gamma K.
```

For the inherited Lie-carried unit direction `v`, let

```text
q0 := (1/2)n[gamma(v,v)] = -K(v,v),
s1 := (1/2)n^2[gamma(v,v)] = -F(v,v),
s2 := (1/2)n^3[gamma(v,v)] = -(nF)(v,v).
```

On exact double silence, `K(v,v)=F(v,v)=0`. Differentiating the active equation makes the
`(n tau)K`, `tau F`, and `Lambda n gamma` contractions vanish. Therefore

```text
s2 = -(n Ric3)(v,v) + 2(nB)(v,v),

nB = F gamma^{-1} K + K gamma^{-1} F
     + 2 K gamma^{-1} K gamma^{-1} K.
```

The last term is forced by

```text
n(gamma^{-1}) = 2 gamma^{-1} K gamma^{-1}.
```

For `h=n gamma=-2K`, the uncommuted covariant Ricci variation is

```text
(n Ric3)_ij
 = -D^k D_i K_kj - D^k D_j K_ki
   + D^k D_k K_ij + D_i D_j tau.
```

This expression deliberately retains the spatial derivatives and their connection terms. The
momentum constraint cannot be substituted as though covariant derivatives commuted.

## 3. Ownership result

The displayed identity uses only the complete smooth initial fields `(gamma,K)`, their spatial
derivatives, the connected constant `Lambda`, and the already active conditional equation.
Consequently the inherited initial third normal jet is fixed by the complete initial fields.

It is not fixed by the compressed pointwise tuple `(R,b,C,Lambda,mu)`. That tuple records values at
one event but not the required neighboring spatial derivatives. The surviving spatial jets are
not an imported mechanism: they were already part of the supplied fields.

## 4. Exact pointwise twins

Take

```text
R = 319/200,  mu = 16/25,  |b| = 1,
C = b(1-2mu) = -7b/25,
Lambda = R/2 - 2b^2 mu + 3b^2 mu^2.
```

Two positive-weight G331 geometries realize this same tuple at interior points:

```text
(w1,w2,x) = (1/4,1/2,1438/1919),
(w1,w2,x) = (1/3,1/2,4071/6157).
```

Their invariant squared curvature gradients differ:

```text
|dR|^2 = 663665041/48000000,
|dR|^2 = 8714316107/1296000000.
```

Thus these are genuinely different spatial germs, not a coordinate relabeling hidden by the five
labels. For the radial-horizontal/weighted-Reeb direction with the same `mu`, their third responses
are

```text
b=-1:  -11982281327/699840000,
       -207122235829/18895680000;

b=+1:  +11982281327/699840000,
       +207122235829/18895680000.
```

The responses differ within each branch although the pointwise tuple is identical. This is an
exact counterexample to pointwise-tuple ownership.

## 5. Homogeneous control and branch reversal

For the equal-weight member `w1=w2=719/1600`, `R=319/200` is constant and the spatial derivative
terms reduce exactly. On the complete strict double-silent surface,

```text
s2 = 8 b mu.
```

At `mu=16/25`, this is `-128/25` on the negative root and `+128/25` on the positive root. Hence
double silence through second order does not imply continued silence. Reversing the complete G332
root reverses the inherited third response. This control does not prove that every inhomogeneous
datum is nonzero or select a preferred sign.

## 6. Completed finite-boost readout

For a fixed finite boost `z`, no new carry is required. The third pair-metric jet is

```text
2 s2 [[sinh(z)^2, sinh(z)cosh(z)],
      [sinh(z)cosh(z), cosh(z)^2]].
```

The corresponding terminal scalar third jet is `s2 sinh(z)^2`. At zero boost that scalar remains
blind even when the completed spatial pair metric has nonzero third response. The terminal scalar
is therefore not promoted to the complete pair response.

## 7. Evidence and boundary

The production executable differentiates the exact coordinate metric with a time dual number. The
independent executable instead evaluates the uncommuted covariant Ricci-variation formula and
imports no production code or result. Both use exact rational arithmetic. They agree on both
pointwise twins, both roots, and the homogeneous formula.

This is an initial inherited third-jet theorem. It does not establish arbitrary higher direction
or pair-frame carry, observer-time conversion, explicit positive-time evolution, finite/global
persistence, stability, physical germ population, occupancy, topology, matter, mass, observations,
scale, `X_max`, or canon. The metric and reciprocal kernel are unchanged.

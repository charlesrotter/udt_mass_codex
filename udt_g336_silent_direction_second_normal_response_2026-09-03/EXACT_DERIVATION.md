# G336 exact derivation — second normal response on the silent set

Date: 2026-09-03
Status: `DERIVED_CONDITIONAL_BOUNDED__EXTERNALLY_ACCEPTED_AFTER_PREREGISTERED_REPAIRS`

## 1. Bounded landing

```text
G336_INHERITED_SILENT_SECOND_JET_IS_EXACT_BUT_SIGN_INDEFINITE
__INTERIOR_CLASSIFICATION_DEPENDS_ON_DIRECTION_CARRY
__STRICT_HORIZONTAL_ENDPOINT_IS_POSITIVE_AND_CARRY_INDEPENDENT
__VERTICAL_ENDPOINT_IS_BRANCH_MEETING_BOUNDARY
__DOUBLE_SILENT_STRATUM_REQUIRES_HIGHER_JET
```

G336 computes the next initial normal derivative precisely where G335's first response vanishes.
It is an initial-jet classification in the owner-provisional bounded vacuum arena. It is not a
finite-time development, stability result, physical-germ selector, or cosmological prediction.

The candidate reduced formula was seen during exploratory mapping before preregistration. That
fact is disclosed in `EXPLORATORY_MAP_NOTE.md`; the registered production and independent evidence
are confirmatory rather than a blind discovery.

## 2. Inputs and conventions

G332 supplies

```text
K = ((C-b)/2) gamma + b eta tensor eta,
(b+C)^2 = 2(R+2C^2-2Lambda).
```

The G333 rate endomorphism is `H=-K^sharp`. For a unit direction `v`, put

```text
mu = gamma(v,xi)^2,
q0 = gamma(Hv,v) = (b-C)/2-b mu.
```

G336 restricts to the complete first-order-silent set `q0=0`. Since `b=0` would then force
`C=0` and make the G332 strict radicand vanish, every strict silent datum has `b!=0` and

```text
C = b(1-2mu).
```

The radicand on this set is

```text
(b+C)^2 = 4b^2(1-mu)^2.
```

It is strictly positive for `0<=mu<1` and vanishes at `mu=1`. Thus the vertical endpoint is a
branch-meeting closure boundary, not a member of the strict two-branch family. This scope error in
the original preregistration was caught before external transmission and is registered in
`PREREGISTRATION_SCOPE_REPAIR.md`.

The future-normal sign convention is `K=-(1/2)L_n gamma`. In unit-lapse, zero-shift Gaussian
presentation the active conditional equation gives

```text
n K_ij = Ric3_ij + tau K_ij - 2 K_i^k K_kj - Lambda gamma_ij.
```

Gaussian normal coordinates are a presentation control. The equation remains conditional on the
owner-provisional Universal Reciprocity/DDR and G312 premises; it has not become canon.

## 3. Three-dimensional Ricci input

G331's weighted-contact family has a unit Killing eigenline `xi` with

```text
Ric3^sharp xi = 2 xi,
Ric3^sharp|horizontal = (R-2)/2 I.
```

Consequently every unit direction obeys

```text
Ric3(v,v) = (R-2)/2 + (6-R)mu/2.
```

Production independently reconstructs the weighted metric, inverse, Christoffels, Ricci tensor,
and scalar curvature in exact rational coordinates at equal- and unequal-weight controls. Every
sample agrees componentwise with this projector formula. The all-positive-weight statement is the
analytic G331 identity; samples do not replace it.

## 4. Inherited Lie-carry second jet

Let `[n,v]=0` at the initial slice, exactly the inherited G333/G334 germ convention. Then

```text
s1 := (1/2)n^2[gamma(v,v)] = -nK(v,v).
```

The `tau K(v,v)` term vanishes on the silent set because `K(v,v)=-q0=0`. Therefore

```text
s1 = Lambda - Ric3(v,v) + 2 K_i^k K_kj v^i v^j.
```

At silence the horizontal and vertical eigenvalues of `K^sharp` reduce to

```text
k_horizontal = -b mu,
k_vertical   =  b(1-mu),
```

so

```text
K^2(v,v) = b^2 mu(1-mu).
```

Substituting `C=b(1-2mu)` into the G332 constraint gives

```text
Lambda = R/2 - 2b^2 mu + 3b^2 mu^2.
```

The full ADM expression consequently has the two exactly equivalent reductions

```text
s1 = 1 + (Lambda-3)mu + 3b^2 mu^2(1-mu)
   = 1 + (R-6)mu/2 + b^2 mu^2.
```

No curvature term or nonlinear `K^2` term has been discarded.

## 5. Sign strata and double silence

For the strict interior `0<mu<1`, the inherited second jet vanishes exactly on

```text
b^2 = ((6-R)mu-2)/(2mu^2),
```

whenever the right side is positive and the other strict G332 conditions hold. Above and below
that surface the sign changes. Thus the active equation does not force one universal second-order
turn-on direction.

An exact lawful triplet occurs in the equal-weight `w1=w2=1/4` metric, for which direct coordinate
reconstruction gives `R=0`. Set `C=0`, `mu=1/2`. Then:

| `b^2` | `Lambda` | `s1` | sign |
| ---: | ---: | ---: | --- |
| 1 | -1/4 | -1/4 | negative |
| 2 | -1/2 | 0 | double-silent |
| 4 | -1 | 1/2 | positive |

Both roots `b=+sqrt(b^2)` and `b=-sqrt(b^2)` are retained. The exact double-silent member makes a
third normal jet the next unresolved local question; it is not rejected as unphysical.

At the horizontal endpoint `mu=0`, silence gives `C=b` and

```text
s1=1.
```

At the vertical closure boundary `mu=1`, silence gives `C=-b` and

```text
s1 = R/2-2+b^2 = Lambda-2.
```

This boundary identity may be positive, zero, or negative, but it is not counted as a lawful strict
two-branch G332 datum.

## 6. Complete finite-boost pair matrix

For fixed finite rapidity `z`, boost the initial orthonormal pair by

```text
U = cosh(z)n+sinh(z)v,
S = sinh(z)n+cosh(z)v.
```

With the same inherited carry and `q0=0`, only the spatial entry has a nonzero second metric jet:

```text
n^2 h_pair = 2s1 [[sinh(z)^2, sinh(z)cosh(z)],
                   [sinh(z)cosh(z), cosh(z)^2]].
```

For `Phi=-(1/2)log(-h00)`, the first derivative vanishes and

```text
n^2 Phi = s1 sinh(z)^2.
```

Thus zero boost remains terminal-scalar blind even when the spatial second response is nonzero.
The pair matrix, not `Phi` alone, retains the complete registered response.

## 7. Exact carry boundary

The inherited formula is not an all-carry scalar. Let a unit direction vary smoothly and define
`W=nabla_n v` at the initial event. At silence, first-order preservation of unit norm is
`gamma(W,v)=0`. The derivative of the instantaneous directional strain

```text
q = gamma(Hv,v)
```

is

```text
nq(W) = nq(Lie) + 2 gamma(Hv,W-Hv),
```

because inherited Lie carry has `[n,v]=0`, hence `W=Hv` in Gaussian presentation.

On the silent set,

```text
|Hv|^2 = b^2 mu(1-mu).
```

For every strict interior direction this is positive and `Hv` is perpendicular to `v`. Choosing
`W=k Hv` preserves unit norm to first order and can make `nq(W)` negative, zero, or positive.
Therefore the inherited sign classification is genuinely carry-dependent in the interior.

At the strict horizontal endpoint, silence makes `Hv=0`; the first-carry correction vanishes and
`s1=1`. The same algebraic carry cancellation occurs at the vertical closure boundary, but that
boundary is outside the strict family. Arbitrary pair-frame second carry and acceleration were not
classified.

This distinction prevents a category error: `s1` is one-half the second metric-length jet only for
the declared inherited Lie carry. For another unit-direction carry, the displayed `nq(W)` is the
derivative of the normalized directional strain, not the second derivative of the identically
unit norm `gamma(v,v)=1`.

## 8. Evidence

`derive_silent_second_response.py` uses exact rational arithmetic, direct coordinate curvature,
ADM tensor algebra, both branches, every analytic silent stratum, and all finite boosts
analytically. It passes 48,375 checks over 576 strict silent controls, 48 vertical-boundary
controls, 9,792 strict boost cases, and 816 boundary boost controls.

`verify_silent_second_response_independent.py` imports no production code and reads no production
result. It uses 480 randomized rotated bases, a direct ADM matrix reconstruction, a centered metric
second jet, finite boosts, and independent carry controls. It passes 3,860 checks.

`run_catch_proofs.py` catches 14 algebraic, carry, endpoint, and scope mutations.
Fresh external adversarial review retained the complete bounded mathematics and requested only the
registered R2 wording repair that restricts the zero-surface statement to `0<mu<1`. Repair-only
follow-up independently accepted R2 and the unchanged bounded scientific landing.

## 9. Exact boundary

G336 does not derive a finite-time G332 spacetime, stability, occupancy, topology, matter or mass,
an observational prediction, a physical scale, `X_max`, or canon. It sharpens the local response
census and identifies the double-silent and carry boundaries. The metric, kernel, angular sector,
and active owner-provisional evolution equation are unchanged.

# G333 exact derivation — metric-native initial pair response

Date: 2026-09-03

Historical production status before fresh external review:
`DERIVED_CONDITIONAL_BOUNDED_PENDING_EXTERNAL_REVIEW`.

## 1. Inputs and convention

On the strict G332 branch, let `gamma` be a smooth compact spatial metric with a global unit
Killing field `xi`. Write `eta=gamma(xi,.)` and let

```text
P = xi tensor eta
```

be the orthogonal rank-one projector onto the line spanned by `xi`. G332 constructs

```text
b = -C +/- sqrt(2[R+2C^2-2Lambda]),
K = ((C-b)/2) gamma + b eta tensor eta.
```

The two square-root signs are both retained, and the radicand is strictly positive. The G315 sign
convention is

```text
K = -(1/2) L_n gamma,
```

for the future unit normal `n`. Define the spatial rate endomorphism

```text
H = (1/2) gamma^{-1} L_n gamma = -K^sharp.
```

When two vector arguments are displayed, the notation is explicitly the metric contraction

```text
H(v,v) := gamma(Hv,v) = (1/2)(L_n gamma)(v,v).
```

It is not an endomorphism being evaluated on two arguments.

This is a first-normal-jet calculation. Unit lapse and zero shift are used only as a Gaussian
coordinate presentation of the geometric normal derivative.

## 2. Exact two-plane-plus-line response

Put `a=(C-b)/2`. Since `P^2=P`,

```text
K^sharp = a I + b P,
H       = -a I - b P.
```

Therefore the rate on the two-plane orthogonal to `xi` and the rate along `xi` are

```text
H_horizontal = (b-C)/2,
H_vertical   = -(C+b)/2.
```

Their exact difference is

```text
H_vertical-H_horizontal = -b.
```

Thus the response is common only on the special sub-stratum `b=0`. The complete G332 family has a
genuine two-plane-plus-line channel; no orbit period or fibre normalization occurs in it.

The trace and mean rate are

```text
tr(H)  = (b-3C)/2,
bar(H) = tr(H)/3 = -C/2+b/6.
```

The trace-free part `A=H-bar(H)I` has eigenvalues

```text
(b/3, b/3, -2b/3)
```

and exact squared norm

```text
|A|^2 = 2b^2/3.
```

This cleanly separates a common volume response from a directional shape response.

## 3. Every local separation direction

For any unit spatial direction `v`, define the invariant number

```text
mu = gamma(v,xi)^2,       0 <= mu <= 1.
```

Then

```text
gamma(Hv,v) = (b-C)/2 - b mu.
```

This covers every unit direction, not just the horizontal and vertical endpoints. Changing a
direction from `v` to `w` changes its instantaneous logarithmic length rate by

```text
gamma(Hv,v)-gamma(Hw,w) = -b(mu_v-mu_w).
```

The G332 constraint relation

```text
(b+C)^2 = 2(R+2C^2-2Lambda)
```

makes the interlock explicit: after `C`, `Lambda`, and a square-root branch are supplied, the
spatial scalar curvature fixes `b` pointwise, and `b` fixes the initial directional response. In
the unequal-weight G331/G332 controls, `R` and therefore generally `b` vary over the slice. In the
equal-weight control `R` is constant. This is a curvature-to-first-response statement, not a
selection of the free constant, branch, datum, or physical history.

The Hamiltonian identity remains exact:

```text
R + (tr K)^2 - |K|^2 = 2 Lambda.
```

Both algebraic branches were retained in production and independent verification.

## 4. What the complete pair germ reads

Choose a local Gaussian normal extension of the initial slice. For an arbitrary extension of a
unit initial direction `v`, tensor differentiation gives the theorem-level identity

```text
n[gamma(v,v)] = (L_n gamma)(v,v) + 2 gamma(L_n v,v),
```

where `L_n v=[n,v]`. The reduced pair formula therefore requires the declared Lie-transported
extension `[n,v]=L_n v=0` at the evaluation point. This transport is a calculation convention, not
additional physical data. For the supplied two-dimensional germ spanned by `n` and `v`, the pair
metric at the slice then has

```text
h00 = -1,   h01 = 0,   h11 = 1.
```

Its first normal jet is

```text
n(h00)=0,
n(h11)=(L_n gamma)(v,v)=2 gamma(Hv,v).
```

Consequently the instantaneous logarithmic rate of proper spatial length is

```text
(1/2)n(log h11)=gamma(Hv,v)=(b-C)/2-b mu.
```

The terminal reciprocal scalar for this calibrated germ is

```text
Phi = -(1/2) log(-h00),
```

so `n(Phi)=0` in this Gaussian normal presentation. Horizontal and vertical directions can
therefore have the same terminal-scalar first jet and different spatial-length first jets. The
complete pair pullback contains more of this first response than that single terminal scalar.

This is deliberately narrow. It does not say that every physical pair germ has zero clock
response, that `Phi` is generally blind to dynamics, or that spatial strain is an additional law.
Other timelike, oblique, null, accelerated, shifted, or screen-mixed germs can place different
metric information into `h00`, `h01`, and `h11`. They remain a later extension.

## 5. Why Hopf is not load-bearing

Every formula above uses only local `(gamma,K,n,v)` data and the invariant decomposition already
present in the G332 construction. It does not use whether an integral curve of `xi` closes, is
dense on a torus, or belongs to a Hopf fibration. Rational and irrational G331 weight ratios obey
the same response formula.

Thus G333 neither confirms nor rejects the older Hopf-stability lane. It shows that the metric and
its lawful first jet already supply a response question that is logically prior to topology.

## 6. Evidence and exact boundary

`derive_initial_pair_response.py` uses exact rational and quadratic-extension arithmetic over 360
cases, all five registered directional overlaps, both branches, both signs of `C`, three values of
`Lambda`, and equal/unequal-weight scalar-curvature controls. It passes 6,882 checks.

`verify_initial_pair_response_independent.py` does not import production code or read its result.
It gives an implementation-distinct rotated-matrix and centered-first-jet confirmation on
representative directions. It is not a second continuum symbolic proof; the exact analytic
all-`mu` proof is carried by the production derivation. The independent implementation passes 146
checks.

`run_catch_proofs.py` catches nine preregistered scientific mutations, in addition to baseline and
scope controls.

Maximum conclusion:

```text
G332_METRIC_NATIVE_FIRST_RESPONSE_IS_COMMON_PLUS_DIRECTIONAL
__COMPLETE_NORMAL_SPATIAL_PAIR_PULLBACK_EXCEEDS_ITS_TERMINAL_SCALAR
__FIRST_JET_ONLY_NO_HOPF_SELECTION_OR_STABILITY
```

The production artifact retains its historical pre-review grade. After fresh review and accepted
preregistered repairs, the package grade is
`DERIVED_CONDITIONAL_BOUNDED__EXTERNALLY_ACCEPTED_AFTER_PREREGISTERED_REPAIRS`. It is not a finite-time
development, stability theorem, topology selector, physical occupancy rule, matter/mass law,
observational prediction, absolute scale, physical `X_max`, or canon.

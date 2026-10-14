# Explorer A — initial source-first reconstruction

Status: frozen initial analytic candidate before old/sibling argument exposure.
Not reviewed; not adoption, canon or a registry regrade. Source snapshot,
permitted sections, full-file hashes, inherited startup and limited staged
exposure are recorded in `INITIAL_APPROACH.md` and incorporated here. No new
scientific source was opened between that approach and this reconstruction.

## 1. Start from what a clock comparison measures

Let A and B be specified future-timelike worldlines with ordinary metric proper
times `τ_A, τ_B`. Restrict to a smooth causal branch on which emitted pulses
from A have unique receptions on B. The future transfer map is

`τ_B = F_AB(τ_A)`, with `F_AB' > 0`.

For equal proper emission periods, the instantaneous received tick rate
relative to the emission clock rate is

`R_AB = dτ_A/dτ_B = 1/F_AB'(τ_A)`.

Thus A appears slower to B through signals precisely when `0<R_AB<1`.
This is a definition of the actual idealized measurement, not a formula for
its value. It requires the worldlines, causal signal path and event pairing.
It separates a propagation delay from the derivative of that delay.

The reverse experiment has another future map `τ_A = F_BA(τ_B)`.
It is not generally `F_AB^{-1}`: inversion maps a reception back to its earlier
emission, while the reverse experiment emits anew and arrives later. Therefore
mutual slowing is the pair of inequalities `R_AB<1` and `R_BA<1`, not merely
an inversion symmetry. The packet supplies no general `F_AB` or `F_BA`.

## 2. What has and has not selected the metric

The owner statements express a physical program and intended observation;
they do not contain equations selecting the supplied static spherical branch.
Even within the already restricted static diagonal spherical areal family,

`ds² = -A(r)c_E²dt² + B(r)dr² + r²dΩ²`, `A,B>0`,

there are two positive functions. The benchmark additionally imposes
`A B = 1`, using `A=exp(-2φ)` and `B=exp(2φ)`. Writing a positive function as
an exponential is a parametrization. Requiring the other independent metric
coefficient to be its reciprocal is an additional restriction in areal radius.

A radial coordinate change `dρ = sqrt(A B) dr` can locally arrange reciprocal
time/radial coefficients, but then the angular term is `r(ρ)²dΩ²`, not generally
`ρ²dΩ²`. It does not establish both reciprocity and the supplied areal form.
A constant rescaling of time only rescales `A B` by a constant; it cannot
remove arbitrary radial dependence. The owner words, as supplied, do not
identify this radial relation, staticity, a center, or the profile `φ(r)`.

This is an explicit unfilled derivation, not a theorem that no metric can
satisfy the words. It does not require all cosmological initial data or all
free constants to be uniquely fixed before useful consequences can be derived.

## 3. Exact local consequences when the benchmark is supplied

For a static observer and a radial displacement on a static slice, set

`a(r)=dτ/dt=exp(-φ(r))`, `b(r)=dℓ/dr=exp(φ(r))`.

Positive roots and the chosen chart give `a b=1`. Radial null propagation gives

`|dr/dt| = c_E sqrt(A/B) = c_E exp(-2φ)`,

and conversion to the static observer's local radial ruler and clock gives

`|dℓ/dτ| = (b/a)|dr/dt| = c_E`.

The coordinate speed varies with `φ`; the local orthonormal null speed is the
calibration `c_E`. These are different objects. An algebraic conditional ratio
is not automatically either one.

For this supplied positive reciprocal pair, choosing the normalized contrast

`K=(b-a)/(b+a)`

gives exactly `K=tanh(φ)`. This follows from the definitions and the elementary
exponential identity. For finite real `φ`, `|K|<1`; exchanging `a,b` changes the
sign. If instead one contrasts the metric coefficients, the same construction
gives `(B-A)/(B+A)=tanh(2φ)`. If one uses only `b/a`, the result is `exp(2φ)`.
The phrase “reciprocal identity” alone does not choose the normalized contrast,
the square-root factors or the depth convention. No physical signal or clock
readout has yet been identified with `K`.

Further, `a,b` at one point compare proper increments with particular chart
increments; their being reciprocal does not turn them into the two received
tick rates of separated observers. In a generic chart even their product is a
different number. Time/radial normalization and areal radius belong in any
claim that this local branch algebra supplies a physical pair.

An “underlying infinite c” is not a second parameter appearing in the given
finite Lorentz metric. The packet supplies no operational mapping from that
counterfactual description to `K`, `c_E`, or a global depth. No physical claim
about its necessity or impossibility follows from this absence alone.

## 4. Exact static two-clock experiment

Choose fixed radii `r_A<r_B` in one regular interval, fixed angles, and the same
radial path for repeated pulses. This is a free-and-explored preparation; the
clocks generally need support/acceleration and are not asserted geodesic.
Assume ideal pulses follow the future radial null curves. Finite smooth `φ`
on the compact interval makes the coordinate transit time finite:

`T_AB = (1/c_E) ∫[r_A,r_B] exp(2φ(r)) dr`.

Staticity makes this delay independent of emission time. Thus
`t_B=t_A+T_AB`, `dt_B/dt_A=1`. Since `dτ_i=a_i dt_i`,

`R_AB = a_A/a_B = exp(φ_B-φ_A)`.

For the future B-to-A experiment, the same argument gives

`R_BA = a_B/a_A = exp(φ_A-φ_B)`, hence `R_AB R_BA=1`.

Both cannot be strictly below one. Equal endpoint lapse gives both equal to
one even when `T_AB>0` and the geometric distance is positive. This calculation
also holds for positive general static `A,B`: the travel time contains
`sqrt(B/A)`, while the received-rate ratio contains endpoint `sqrt(A)` only.
Consequently the reciprocal coefficient restriction `A B=1` is neither what
creates this static rate reciprocity nor what turns it into mutual slowing.

The inverse-map distinction has not been erased: with proper-time origins
chosen conveniently, `F_AB(τ_A)=(a_B/a_A)τ_A+a_B T` and
`F_BA(τ_B)=(a_A/a_B)τ_B+a_A T`. They have inverse slopes but positive causal
delays; the algebraic inverse has the opposite delay. A round trip advances
A's time by `2a_A T`.

This refutes only the implication “the supplied metric with stationary
observers and ordinary null-clock readout automatically yields strict mutual
slowing.” It is not a no-go for all moving observers, time-dependent geometries,
or the entire founding program. The correct failed join is from local
reciprocal factors to the asserted physical two-clock comparison without
specifying the preparation and proving the readout map.

## 5. A retained alternative: two future maps can both slow clocks

To check that the preceding limit is substantive, consider the explicit flat
metric `ds²=-c_E²dt²+dx²` and inertial worldlines `x_A=-vt`, `x_B=vt`,
`0<v<c_E`, restricted to `t>0`. This is a mathematical SR control, not a native
positional-dilation model. A pulse sent from A at `t_e` follows
`x=-v t_e+c_E(t-t_e)` and meets B at

`t_r=[(c_E+v)/(c_E-v)]t_e`.

Both clocks have `dτ=sqrt(1-v²/c_E²)dt`, so

`R_AB=(c_E-v)/(c_E+v)<1`.

Reflection symmetry gives the same `R_BA<1` for a new future pulse in the other
direction. Their product is below one, unlike the stationary benchmark. The
relative-motion preparation supplies the effect; neither a positional law nor
the supplied kernel was derived. This witness prevents “reciprocal maps cannot
both redshift” from being asserted universally and identifies worldline/path
selection as load-bearing information.

There is an informative extension before any new physical adoption: in any
radial time-dependent diagonal metric write null coordinate flight time as
`t_r=t_e+T(t_e)` between prescribed worldlines. Then the proper-time transfer
is governed by endpoint clock factors and `1+T'(t_e)` (with worldline motion
included in those factors and in `T`). A constant delay does not redshift ticks;
changing transit time can. A founding positional explanation needs to derive
this derivative or an equivalent invariant signal transfer, rather than only
the existence of finite travel time. This is a diagnostic decomposition, not
an imported dynamics or a proposed replacement metric.

## 6. Initial dependency verdict and next useful comparison

| Link | Initial result | Exact remaining condition |
| --- | --- | --- |
| Owner words → supplied metric | Not reconstructed | Need an argument selecting the branch restrictions, or explicitly admit them as branch inputs |
| Supplied metric → reciprocal local factors | Exact on the declared chart and regular static branch | Local lapse/stretch interpretation and calibration |
| Reciprocal factors → tanh contrast | Exact after defining the normalized contrast and depth | The contrast definition is not fixed by the owner words alone |
| Local contrast → physical two-clock comparison | Not established; automatic stationary mutual-slowing version fails | Worldlines, linked events, signal law/path and readout identification |
| One experiment inverted → reverse future experiment | Invalid in general | Separate future maps; even equal inverse slopes do not equate maps |
| Static failure → whole-founding-program no-go | Does not follow | Moving-clock control already defeats the unrestricted inference |

The source-limited initial finding is a surviving conditional algebra with an
unfilled selection/readout chain. It is worth comparing exact prior sources
next: they may contain an independent operational definition or additional
premise that repairs a missing link. A later adopted premise remains distinct
from proof that the original owner words imply it. The next comparison must
test the strongest favorable reconstruction as well as the adverse result.

No numerical check has been used. Direct hand derivations above provide exact
substitution anchors, not independent-review certification. Initial alternatives
and this edition stay preserved through the forthcoming comparison and review.

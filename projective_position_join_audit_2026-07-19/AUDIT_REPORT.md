# Projective-position join and two-depth audit

Date: 2026-07-19

Base: `85f94e10324d5c56f81d335b524afc700435d4c9`

Status: `VERIFIED-WITH-CAVEATS`; exact bounded kinematic/readout audit, not canonization

## Result first

The normalized imbalance is already almost derived—but one physical identification is still absent.

UDT Reciprocity and CSN give the positive projective ray

\[
 [u:v]=[e^{-\phi}:e^{+\phi}].
\]

If physical signed position is required to be a first-degree fractional-linear coordinate of that
ray, with the reciprocal axes at `-1,+1` and the neutral ray at `0`, then the coordinate is unique:

\[
 \boxed{
 \xi=\frac{v-u}{v+u}
 =\frac{r-1}{r+1}
 =\tanh\phi,\qquad r=\frac vu.
 }
\]

The fractional composition law then follows exactly. This part is genuinely downstream once the
anchored projective readout class is supplied.

But current UDT does not yet require physical position to be that first-degree projective readout.
The exact family

\[
 f_\epsilon(\xi)
 =\xi+\epsilon\xi(1-\xi^2),
 \qquad -1<\epsilon<\frac12,
\]

is smooth, increasing, odd, fixes `-1,0,+1`, respects CSN, shares the same `X_max`, and inherits exact
identity, reversal, associativity, and closure by conjugating additive depth. Every member uses the
same complete `phi` coframe. Nonzero members are not the normalized imbalance and do not obey the
original fractional-linear law in their display coordinate.

A stronger companion family

\[
 g_\epsilon(\xi)=\xi+\epsilon\xi^3(1-\xi^2)
\]

also satisfies `g_epsilon'(0)=1`. Thus even silently matching the local slope at the neutral point
does not select `tanh`.

The projective-position join therefore remains `OPEN`. The smallest absent statement is now exact:

> **Physical signed position is the first-degree anchored projective readout of the reciprocal CSN
> ray.**

This audit identifies that selector but does not adopt it.

The two meanings of depth advance further. If the absolute static field and observer calibration use
the same reciprocal representation, then

\[
 \boxed{
 \phi_{\rm rel}(P;O)=\Phi(P)-\Phi(O).
 }
\]

This is `DERIVED_CONDITIONAL` in that shared representation. Since the physical static seal satisfies
`Phi(S)=0`, an observer sees

\[
 \phi_{\rm rel}(S;O)=-\Phi(O),
 \qquad
 \xi_{\rm rel}(S;O)=-\tanh\Phi(O).
\]

The seal is therefore generally neither the observer's relative zero nor the `X_max` endpoint. The
relative and absolute uses of phi are compatible as a difference map, but they are not the same
zero-bearing object.

## Lay interpretation

UDT gives us two reciprocal readings—one clock-like and one ruler-like. It also says their common
magnification is merely calibration. What remains physically meaningful is their ratio, or
projective ray.

Taking “ruler minus clock, divided by ruler plus clock” gives a beautiful bounded number:

\[
 \frac{v-u}{v+u}=\tanh\phi.
\]

It is the simplest symmetric display and the unique fractional-linear one with the desired three
anchors. But simplicity is not necessity. One can smoothly bend the markings between the center and
the endpoints without changing the reciprocal geometry, the endpoint, or how the underlying depth
composes. The complete metric continues to use `dphi`, so it does not notice which set of bounded
labels was painted on top.

That is what the counterfamily proves. UDT has derived the projective object, but not yet the rule
saying that this particular chart is operational distance.

The seal question becomes cleaner too. The absolute field is like elevation measured from a fixed
physical boundary. Relative depth is the elevation difference between an event and an observer.
Moving the observer changes that difference without moving the physical boundary or changing where
the absolute field is zero.

## What is genuinely derived

### Reciprocal CSN ray

The determinant-one reciprocal pair is

\[
 D(\phi)=\operatorname{diag}(e^{-\phi},e^{+\phi}).
\]

CSN quotients `(u,v)` by simultaneous positive rescaling. Therefore the local reciprocal datum is the
positive projective ray, equivalently

\[
 r=\frac vu=e^{2\phi}.
\]

Exchange `u<->v` sends `r->1/r` and `phi->-phi`. This is
`DERIVED_IN_DECLARED_DUAL_REPRESENTATION`.

### Anchored first-degree projective coordinate

Let

\[
 F(r)=\frac{ar+b}{cr+d}.
\]

Demand

\[
 F(0)=-1,qquad F(1)=0,qquad F(\infty)=+1.
\]

After removing the irrelevant common coefficient scale, these three equations uniquely give

\[
 a=c=d=1,qquad b=-1.
\]

Hence

\[
 F(r)=\frac{r-1}{r+1}=\tanh\phi.
\]

Multiplication of `r` then gives

\[
 \xi_1\oplus\xi_2
 =\frac{\xi_1+\xi_2}{1+\xi_1\xi_2}.
\]

This is an exact uniqueness theorem inside the first-degree fractional-linear class. It is not an
unrestricted position theorem.

## The complete counterfamily

For

\[
 f_\epsilon(\xi)=\xi+\epsilon\xi(1-\xi^2),
\]

the derivative is

\[
 f_\epsilon'(\xi)=1+\epsilon(1-3\xi^2).
\]

On `[-1,1]`, its minimum is `1+epsilon` when epsilon is negative and `1-2epsilon` when epsilon is
nonnegative. It is therefore strictly positive for the registered interval

\[
 -1<\epsilon<\frac12.
\]

Every member is a smooth increasing odd bijection of the bounded interval and fixes all three
anchors. Composing it with the CSN-invariant `xi` preserves CSN. Reciprocal exchange remains sign
reversal. Defining

\[
 x_\epsilon(\phi)=X_{\max}f_\epsilon(\tanh\phi)
\]

preserves the same unattainable endpoints.

The induced composition law is

\[
 x_\epsilon(\phi_1)\oplus_\epsilon x_\epsilon(\phi_2)
 :=x_\epsilon(\phi_1+\phi_2).
\]

It is associative and has the same identity and inverse because it is a conjugate representation of
the additive depth group. At the exact witness `epsilon=1/4`, base coordinates `xi1=1/3` and
`xi2=1/5`, composing before and after the nonlinear display differs by `-45/29728`. Thus the
nonprojective display does not accidentally obey the original Mobius formula.

The companion `g_epsilon` fixes the neutral derivative as well. Its derivative correction is
`epsilon(3xi^2-5xi^4)`, whose bounded range keeps the map increasing on the same registered epsilon
interval. Local neutral calibration therefore cannot rescue unrestricted uniqueness.

## Why the complete coframe does not select the chart

The exact frame action remains

\[
 D(\phi-\beta)=D(\phi)D(-\beta).
\]

Every bounded display merely inherits

\[
 x_\epsilon'
 =X_{\max}f_\epsilon\left(
 \frac{\xi-\tanh\beta}{1-\xi\tanh\beta}
 \right).
\]

The spatial depth coframe is the already-selected conditional object `L dphi`, not `dx_epsilon`.
For every candidate,

\[
 Ld\phi
 =\frac{L\,dx_\epsilon}
 {X_{\max}f_\epsilon'(\xi)(1-\xi^2)}.
\]

Keeping the exact Jacobian reproduces the same coframe. Consequently the static, dynamic, and
accelerating full-frame results are all insensitive to `epsilon`. Complete-coframe covariance
cannot choose a display that is not itself part of the coframe premise.

This also clarifies why the earlier `dx` coframe failed: treating a bounded display differential as
the fundamental reciprocal ruler is a different—and inconsistent in that tested family—slot
identification. It does not follow that one particular bounded display is therefore physical.

## The absolute and observer-relative depths

Let the absolute static reciprocal field be represented by `D(Phi(P))`. Calibrating it relative to
an observer at `O` gives

\[
 D(\Phi(P))D(\Phi(O))^{-1}
 =D(\Phi(P)-\Phi(O)).
\]

Thus

\[
 \phi_{\rm rel}(P;O)=\Phi(P)-\Phi(O)
\]

inside this shared reciprocal representation. Intermediate comparisons telescope exactly:

\[
 [\Phi(P)-\Phi(Q)]+[\Phi(Q)-\Phi(O)]
 =\Phi(P)-\Phi(O).
\]

The observer is at relative zero because `phi_rel(O;O)=0`. The physical seal remains at absolute
zero because `Phi(S)=0`. Those facts coexist without moving the seal.

This is not an unconditional global theorem. It assumes that the absolute static field and observer
calibration use the same reciprocal exponential representation. It does not derive a complete
time-live absolute scalar, how every field transforms at the seal, or the differentiable boundary
action.

## Why finite-cell and bootstrap data do not select the readout

The finite-cell canon fixes static absolute-field parity and `Phi=0` at the seal. Every
`f_epsilon` member can use the same absolute field and the same relative difference. The seal data do
not mention a first-degree projective coordinate, an operational position measure, or the reciprocal
axes as physical boundaries.

Likewise, the current global bootstrap says that realized matter-bearing universes are complete
self-consistent solutions in a narrow proper-density window. Smoothly relabeling the same reciprocal
ray changes neither the metric, proper volume, total mass, density, nor boundary. Therefore the
qualitative bootstrap statement cannot distinguish epsilon. A future derived bootstrap functional
could do so only if it contains an independently justified operational position or boundary measure;
inserting the desired readout would be circular.

The same applies to `X_max`: every candidate shares the endpoints `+-X_max`. A bound does not choose
the markings inside the interval.

## Adjudication and next conceptual gate

- `DERIVED_IN_DECLARED_DUAL_REPRESENTATION`: the reciprocal CSN projective ray.
- `DERIVED_IN_CLASS`: normalized imbalance as the unique three-anchor first-degree projective chart.
- `OPEN`: the physical projective-position join.
- `REFUTED_AS_UNCONDITIONAL`: current UDT premises uniquely force `x=X_max tanh(phi)`.
- `DERIVED_CONDITIONAL`: `phi_rel(P;O)=Phi(P)-Phi(O)` in the shared static reciprocal
  representation.
- `REFUTED_GENERIC_IDENTIFICATION`: the fixed seal is every observer's relative zero or the `X_max`
  endpoint.
- `ABSENT / IDENTIFIED NOT ADOPTED`: physical position is a first-degree anchored projective readout
  of the reciprocal ray.

The conceptual issue is now smaller than before. UDT does not lack a projective structure; it lacks
an operational reason to privilege one coordinate on that structure. That reason might eventually
come from a physical boundary measure, radar/clock protocol, complete action observable, or global
bootstrap functional. None is currently derived.

## Evidence gates and scope

1. **Preregistered:** yes; commit `8beb1c5` before algebra.
2. **Full space or bounded scope:** a symbolic infinite counterfamily over the full bounded interval,
   plus a slope-matched companion; not every conceivable discontinuous or nonmonotone readout.
3. **Independent verification:** separate anchored-coordinate solution and a distinct smooth
   counterfamily, plus direct matrix verification of the two-depth map.
4. **Premises audited:** `PROJECTIVE_JOIN_LEDGER.tsv`, `STATUS_LEDGER.tsv`, source inventory, and
   exercised semantic catch-proofs.

The audit does not select `X_max`, `c`, angular geometry, an action, bootstrap scale, source, carrier,
or mass. Charles retains the physics verdict.

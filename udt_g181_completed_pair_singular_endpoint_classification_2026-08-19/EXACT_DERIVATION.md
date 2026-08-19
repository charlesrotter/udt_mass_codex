# G181 exact derivation — completed-pair singular endpoints

Date: 2026-08-19

## 1. Bounded domain

Let `q>0` approach one endpoint `q=0` of a supplied smooth pair family. The pair metric is regular
and Lorentzian at every interior point and is written in an auxiliary calibrated chart as

\[
h_q=-T(q)^2\bigl(d\tau+\beta(q)dq\bigr)^2+L_q(q)^2dq^2,
\qquad T,L_q>0.
\]

G181 does not assume that the metric, pair immersion, or auxiliary chart extends through `q=0`.
It asks exactly what the accepted G176--G180 construction decides on approach to that endpoint.

## 2. Interior completed coordinate

The determinant and completed density are

\[
\det h_q=-T^2L_q^2,
\qquad
m(q)=\sqrt{-\det h_q}=T L_q>0.
\]

Hence, on the open regular interior,

\[
s(q)=s(q_0)+\int_{q_0}^{q}m(u)\,du
\]

is smooth and strictly monotone. With

\[
B=\frac{\beta}{m},
\qquad dq=\frac{ds}{m},
\]

the completed metric is

\[
\boxed{
h_s=-T^2(d\tau+B,ds)^2+T^{-2}ds^2
}
\]

and therefore

\[
\boxed{\det h_s=-1},
\qquad
\boxed{\Phi=-\log T=-\frac12\log(-h_{00})}.
\]

These identities hold at every interior point. They do not by themselves assert a boundary value.

## 3. Finite versus infinite completed tape

Because `m` is positive,

\[
\boxed{
s(0^+)\text{ is finite}
\iff
\int_0^{q_0}m(q)\,dq<\infty.
}
\]

If the integral diverges, the boundary is at infinite completed ruler coordinate. This is an exact
accessibility classification; it does not identify the endpoint with `X_max`, a wall, a horizon, or
a physical singularity.

## 4. Regular finite completed endpoint

Suppose the completed tape is finite. In the retained calibrated clock chart, the coefficient
matrix of `h_s` has a finite nondegenerate Lorentzian limit exactly when

\[
T\longrightarrow T_0\in(0,\infty),
\qquad
B=\frac{\beta}{m}\longrightarrow B_0\in\mathbb R.
\]

Sufficiency follows immediately from the displayed completed metric. For necessity, a finite
negative limit of `h_{00}=-T^2` forces finite positive `T_0`, and then
`B=h_{0s}/h_{00}` must have a finite limit. The limiting determinant remains `-1`.

Therefore the limit of `m` alone is not an extension criterion:

- `m=q -> 0`, `T=1`, `beta=B_0 m` gives a finite regular completed endpoint;
- `m=q -> 0`, `T=q`, `beta=0` gives `h00 -> 0`, `hss -> infinity`, so the retained completed chart
  has no finite Lorentzian coefficient limit;
- `m=q^(-1/2) -> infinity`, `T=1`, `beta=0` is still integrable and gives a finite regular completed
  endpoint;
- `m=q^(-1)` is not integrable and places the endpoint at infinite completed tape.

## 5. Removable auxiliary stalls and the two-sided warning

Take the primary radial control with `phi=0`, no angular motion, and

\[
r(q)=r_0+q^k,
\qquad k\ge2.
\]

Then

\[
m=kq^{k-1}\longrightarrow0,
\qquad
s=q^k,
\]

and

\[
h_q=-d\tau^2+k^2q^{2k-2}dq^2
\quad\longrightarrow\quad
h_s=-d\tau^2+ds^2.
\]

The zero density is a one-sided auxiliary-parameter stall; the completed coordinate removes it.
It is not an intrinsic singularity of the completed pair.

This does not prove two-sided immersion carry. For

\[
r(q)=r_0+q^2,
\qquad -\epsilon<q<\epsilon,
\]

the monotone completed coordinate is `s=q|q|`, so `r=r0+|s|`. The completed metric can be flat on
both sides while the realized radial map has a cusp at `s=0`. Metric normalization alone cannot
decide whether two incident branches represent one smooth physical realization. That question
remains branch- and immersion-typed.

## 6. Exact power-law census

Let

\[
T=q^a,
\qquad
L_q=q^b,
\qquad
m=q^{a+b}.
\]

Writing `p=a+b`, elementary integration gives

\[
\int_0^{q_0}q^p dq
\begin{cases}
<\infty,&p>-1,\\
=\infty\text{ logarithmically},&p=-1,\\
=\infty\text{ by a power},&p<-1.
\end{cases}
\]

Meanwhile

\[
\Phi=-a\log q
\longrightarrow
\begin{cases}
+\infty,&a>0,\\
0,&a=0,\\
-\infty,&a<0.
\end{cases}
\]

All nine tape/depth cross-classes have exact witnesses in `WITNESS_ATLAS.tsv`. Thus current
identities do not force a unique depth behavior from finite or infinite tape accessibility.

Nonconvergent depth is also permitted. Both

\[
T(q)=2+\sin(\log q),\qquad m(q)=1
\]

and the same `T` with `m=1/q` are regular for every `q>0`; the first has finite tape, the second
infinite tape, and neither has a depth limit. In each case `L_q=m/T>0` constructs the supplied
interior metric exactly.

## 7. Primary-metric first boundary

For the G180 primary time-orthogonal family,

\[
m^2=v^2+e^{-2\phi}r^2b^2.
\]

At `r>0`, both terms are nonnegative and the angular coefficient is positive. Hence

\[
\boxed{m=0\iff v=0\text{ and }b=0}.
\]

A radial turn with `v=0` and `b!=0` is regular. A pure-angular segment is likewise regular. At a
regular center `r=0`, the angular orbit collapses and

\[
m=|v|;
\]

the first zero occurs only when the radial component also vanishes. This sharpens G180's exclusion:
zero radial speed is not the boundary; zero complete spatial tangent is.

## 8. Exact landing and ceiling

```text
COMPLETED_PAIR_ENDPOINT_CLASSIFICATION__REMOVABLE_STALLS_SEPARATED_FROM_INTRINSIC_BOUNDARIES
```

G181 classifies one supplied one-sided endpoint approach. It proves that some apparent
zero-density boundaries are removable auxiliary stalls and gives exact finite/infinite tape and
depth-limit classes. It does not select the supplied family, certify two-sided immersion carry,
cross null/cut/focal/topology changes, derive global completion or `X_max`, or add dynamics or
observational physics.

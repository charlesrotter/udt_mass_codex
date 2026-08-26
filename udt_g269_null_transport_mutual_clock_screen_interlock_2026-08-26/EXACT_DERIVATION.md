# G269 exact derivation — null-transport mutual clock and screen interlock

Date: 2026-08-26

## Primary landing

```text
METRIC_OWNS_A_QUERY_RELATIVE_NULL_TRANSPORT_MUTUAL_CLOCK_SCALAR
__M_PT_IS_BOUNDED_ABOVE_BY_SECH_DELTA
__EQUALITY_IFF_THE_TARGET_CLOCK_IS_IN_THE_TRANSPORTED_NULL_PAIR_PLANE
__NONZERO_SCREEN_MISMATCH_MAKES_THE_INEQUALITY_STRICT
__NO_QUERY_POPULATION_HISTORY_DISTANCE_OR_XMAX_SELECTION
```

This selects preregistered `N2__SCREEN_INTERLOCK`.

## 1. Two constructions on the same supplied null relation

Let a supplied future affine null branch `gamma:A->B` have tangent `k`, endpoint metric-unit
future clocks `U_A,U_B`, and Levi-Civita transport `P_AB`. G220 gives

\[
\omega_A=-g(k_A,U_A)>0,
\qquad
\omega_B=-g(k_B,U_B)>0,
\]

\[
\boxed{r_{AB}=\frac{\omega_A}{\omega_B}},
\qquad
\boxed{\delta_{AB}=-\log r_{AB}}.
\]

This is the directional clock construction.

Independently, transport the source unit clock along the same branch and compare it with the target
unit clock:

\[
\widetilde U_A=P_{AB}U_A,
\]

\[
\boxed{\Gamma_{\rm PT}=-g(\widetilde U_A,U_B)\ge1},
\qquad
\boxed{M_{\rm PT}=\Gamma_{\rm PT}^{-1}}.
\]

`Gamma_PT` is an ordinary bilocal Lorentz factor after the path has fixed the comparison. It is
not obtained by applying a function to `r` or `delta`.

The metric owns this scalar after the branch and endpoint clocks are supplied. Calling its inverse
the physical mutual-clock readout remains a `WORKING_OPERATIONAL_READOUT`, not canon or a claim
that Nature selects every null query.

## 2. The transported null pair plane

Normalize the source null tangent by its source frequency:

\[
K_A=\frac{k_A}{\omega_A},
\qquad
n_A=K_A-U_A.
\]

Because `K_A` is null and `g(K_A,U_A)=-1`,

\[
g(n_A,n_A)=1,
\qquad
g(U_A,n_A)=0.
\]

Metric parallel transport preserves these contractions. Put

\[
\widetilde n_A=P_{AB}n_A.
\]

The transported two-plane is

\[
\mathcal P_{AB}=\operatorname{span}(\widetilde U_A,\widetilde n_A),
\]

and its orthogonal complement is a positive screen. Decompose

\[
\boxed{
U_B=\Gamma_{\rm PT}\widetilde U_A+a\widetilde n_A+W,
}
\]

where

\[
W\perp\mathcal P_{AB},
\qquad
\lVert W\rVert^2=g(W,W)\ge0.
\]

This `W` is an endpoint-clock mismatch relative to the transported null pair plane. It is not the
Jacobi area or a fitted angular modulation.

## 3. Exact interlock theorem

Since `k` is parallel,

\[
P_{AB}K_A=\frac{k_B}{\omega_A}
=\widetilde U_A+\widetilde n_A.
\]

The target frequency contraction is therefore

\[
\frac{\omega_B}{\omega_A}
=-g(P_{AB}K_A,U_B)
=\Gamma_{\rm PT}-a
=\frac1{r_{AB}}.
\]

Thus

\[
a=\Gamma_{\rm PT}-\frac1{r_{AB}}.
\]

Unit normalization of `U_B` gives

\[
\Gamma_{\rm PT}^2-a^2-\lVert W\rVert^2=1.
\]

Eliminating `a` yields

\[
\boxed{
\Gamma_{\rm PT}
=\frac12\left(r_{AB}+r_{AB}^{-1}\right)
+\frac{r_{AB}}2\lVert W\rVert^2.
}
\]

Because

\[
\frac12(r+r^{-1})=\cosh(-\log r)=\cosh\delta,
\]

the exact coefficient-free interlock is

\[
\boxed{
\Gamma_{\rm PT}
=\cosh\delta_{AB}
+\frac{r_{AB}}2\lVert W_{AB}\rVert^2.
}
\]

Therefore

\[
\boxed{
0<M_{\rm PT}\le\operatorname{sech}\delta_{AB}.
}
\]

The screen metric is positive, so equality is necessary and sufficient:

\[
\boxed{
M_{\rm PT}=\operatorname{sech}\delta_{AB}
\quad\Longleftrightarrow\quad
W_{AB}=0.
}
\]

Thus G267's provisional `sech` projection is exactly the transported-planar stratum of the
metric-owned bilocal comparison. It is not the universal full-dimensional result.

## 4. Affine and reversal invariance

A common positive affine rescaling `k->c k` multiplies both endpoint frequencies by `c`, leaves
`r` unchanged, and leaves `K_A=k_A/omega_A` unchanged. Hence the transported plane and `M_PT` do
not depend on affine normalization.

For mathematical reversal along the same path,

\[
P_{BA}=P_{AB}^{-1}.
\]

Metricity gives

\[
\Gamma_{{\rm PT},BA}
=-g(P_{BA}U_B,U_A)
=-g(U_B,P_{AB}U_A)
=\Gamma_{{\rm PT},AB}.
\]

So `M_PT` is reversal-even, while `delta_BA=-delta_AB`. The reverse screen norm need not equal the
forward coordinate value; the theorem gives

\[
\lVert W_{BA}\rVert^2=r_{AB}^2\lVert W_{AB}\rVert^2,
\]

which preserves the same even `Gamma_PT`.

## 5. Planar controls

### Moving flat observers

In `1+1` Minkowski space, let

\[
U_A=(1,0),
\qquad
k=(1,1),
\qquad
U_B=(\cosh\eta,\sinh\eta).
\]

Parallel transport is the identity,

\[
\omega_A=1,
\qquad
\omega_B=e^{-\eta},
\qquad
r=e^\eta,
\qquad
\delta=-\eta.
\]

There is no transverse screen component, and

\[
M_{\rm PT}=\operatorname{sech}\eta=\operatorname{sech}\delta.
\]

### Primary static radial branch

G220 gives, for static observers in the primary reciprocal metric,

\[
r_{AB}=e^{\phi_A-\phi_B},
\qquad
\delta_{AB}=\phi_B-\phi_A.
\]

Radial null transport preserves the time-radial distribution, so `W=0`. Hence

\[
\boxed{
M_{\rm PT}=\operatorname{sech}(\phi_B-\phi_A).
}
\]

This derives the provisional sech form on the central static-radial stratum without fitting or a
post-readout angular envelope.

## 6. Exact nonplanar separator

In flat `1+2` spacetime, embedded in `1+3`, take

\[
U_A=(1,0,0),
\qquad
k=(1,1,0),
\]

and, for any `r>0` and real `w`,

\[
U_B=(\Gamma,a,w),
\]

with

\[
\Gamma=\frac12\left(r+r^{-1}+rw^2\right),
\qquad
a=\Gamma-r^{-1}.
\]

Then exactly

\[
g(U_B,U_B)=-1,
\qquad
-g(k,U_B)=r^{-1},
\]

while

\[
M_{\rm PT}=\frac{2r}{1+r^2+r^2w^2}.
\]

At fixed `r`, varying `w` preserves the directional clock ratio but changes the transport mutual
scalar. For `r=2,w=1`,

\[
\operatorname{sech}\delta=\frac45,
\qquad
M_{\rm PT}=\frac49.
\]

This is the decisive independence witness. The new construction is not another coordinate on the
G268 relation line.

## 7. Exact scope of the advance

G269 supplies the independent metric construction that G268 said would be necessary for a
non-circular comparison. It turns the earlier circle equality into a sharp planarity test:

\[
\Gamma_{\rm PT}-\cosh\delta
=\frac r2\lVert W\rVert^2.
\]

But the theorem does not force every physical relation to be transported-planar. That would be an
additional population/admissibility statement. Nor does `W` equal a sky Jacobi distortion; it is a
specific transported endpoint-clock screen component.

- `DERIVED_CONDITIONAL`: `Gamma_PT` and `M_PT` from a supplied metric, branch, and endpoint clocks.
- `DERIVED_CONDITIONAL`: sharp inequality and equality condition.
- `REGRADES_PROVISIONAL_CANDIDATE`: universal `sech` becomes exact on the planar stratum and an
  upper envelope in the full-dimensional arena.
- `WORKING_INTERPRETATION`: `M_PT` as the physical mutual-clock readout.
- `OPEN`: physical query population, history, distance, `X_max`, observation, source, matter,
  radiative transfer, and canon.

## Evidence

- 34 exact symbolic checks;
- 12,000 implementation-distinct exact-rational cases;
- 143,715 exact-rational assertions;
- 101 distinct transport mutual values at one fixed directional ratio;
- 10/10 mutations injected through one shared validator and caught by their targeted failure;
- no observation, fit, field equation, source, matter model, distance scale, or `X_max` used.

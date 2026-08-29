# G293 exact derivation — history-law architecture constraint funnel

Date: 2026-08-29

## 1. Primary bounded landing

```text
SCALAR_RECIPROCAL_GENERATOR_IS_PARAMETERIZATION_ONLY
__EULER_SECTOR_LEAVES_CONTINUOUS_FLUX_FREE
__PRIMITIVE_STATE_AND_DATA_DEPENDENCE_PARTITION_REMAINS
__UDT_HISTORY_LAW_ARCHITECTURE_NARROWED_NOT_SELECTED
```

The result is a constraint-funnel theorem. It does not derive, adopt, or fit a physical history law.

## 2. Endpoint composition is not homogeneous propagation

The founded reciprocal representation composes supplied depths. An endpoint potential always gives

\[
\delta(a,b)=V(b)-V(a),
\]

and therefore

\[
\delta(a,c)=\delta(a,b)+\delta(b,c),
\qquad
\delta(b,a)=-\delta(a,b).
\]

These identities do not imply that depth depends only on the coordinate difference. For example,

\[
V(s)=s+s^3
\]

obeys both identities, while generically

\[
\delta(a,b)\ne \delta(0,b-a).
\]

Thus the additive homogeneous parameter used below is supplied conditionally. It is not hidden in
F3 endpoint composition.

## 3. Exact scalar homogeneous classification

Supply an additive parameter `s` and a continuous map `gamma` satisfying

\[
\gamma(s+t)=\gamma(s)+\gamma(t).
\]

For every integer `n`, additivity gives `gamma(n)=n gamma(1)`. For rational `m/n`, it gives

\[
\gamma(m/n)=\frac mn\gamma(1).
\]

Continuity and density of the rationals then give

\[
\boxed{\gamma(s)=k s}
\]

for one real constant `k`. The trivial branch `k=0` is valid. Strict increase would add the new
condition `k>0`; unit slope would add the calibration `k=1`.

The reciprocal and projective representations are

\[
D(s)=\operatorname{diag}(e^{-ks},e^{+ks}),
\]

\[
\chi(s)=\tanh(ks),
\]

with

\[
\chi(s+t)=\frac{\chi(s)+\chi(t)}{1+\chi(s)\chi(t)}.
\]

The same result follows from an autonomous scalar generator. Write

\[
X=v(\delta)\,\partial_\delta.
\]

Equivariance under every depth translation requires

\[
v(\delta+a)=v(\delta)
\]

for all `a`, hence `v=k` is constant and

\[
\dot\delta=k,
\qquad
\boxed{\dot\chi=k(1-\chi^2)}.
\]

Flow composition alone is weaker. The nonconstant field `X=delta partial_delta` has the composing
flow `delta(s)=e^s delta(0)` but is not depth-translation equivariant.

## 4. Why this is parameterization rather than physical history

Under a positive rescaling

\[
s'=\alpha s,
\qquad
k'=k/\alpha,
\]

the product is unchanged:

\[
k's'=ks.
\]

Only `ks` is owned by the conditional scalar theorem. If `s` is dimensionful, `k` is a new inverse
scale. If `s` is freely normalized and dimensionless, nonzero `|k|` may be absorbed into it. A future
independent operational attachment could make `k` measurable; current premises do not provide one.

There are two further conditional facts about this scalar lane:

1. A nonzero constant vector field is compatible with pair reversal only when the flow orientation
   is also reversed. Requiring the same vector field at fixed orientation to be odd under
   `delta -> -delta` forces `k=0`.
2. Requiring the quiet identity `delta=0` to be an equilibrium also forces `k=0`.

The second fact must not be overread. UDT's quiet middle need not be a stationary equilibrium. A
signed linear depth can pass through `delta approximately 0` between large negative and positive
regimes, and even functions of depth can then have a natural two-loud-ends/quiet-middle envelope.
What the scalar theorem does not supply is the physical attachment `separation -> s`, the
population of either signed regime, or the simultaneous screen/curvature evolution.

This conclusion does not widen to a complete state. On `(delta,y)`, the vector field

\[
X=y\,\partial_\delta+\partial_y
\]

commutes with every depth translation, yet

\[
y(s)=y_0+s,
\qquad
\delta(s)=\delta_0+y_0s+\frac12s^2.
\]

Additional state can drive nonuniform reciprocal depth and can couple depth to screen/curvature
values. If that richer behavior is required, declaring the state, its physical attachment, and its
generator is precisely the still-missing premise. G293 does not prove that qualitative
loud-quiet-loud scalar behavior itself requires an augmented state.

## 5. Euler sector does not supply continuous propagation

On the unit oriented sphere let

\[
\omega=\sin\theta\,d\theta\wedge d\varphi,
\qquad
P_2(x)=\frac{3x^2-1}{2}.
\]

For any supplied smooth amplitude `a(s)`, define the slice curvature

\[
F_s=[1+a(s)P_2(\cos\theta)]\omega.
\]

Because

\[
\int_{S^2}P_2(\cos\theta)\omega=0,
\]

every slice has

\[
\int_{S^2}F_s=4\pi.
\]

The local density nevertheless changes. At the pole it is `1+a`; at the equator it is
`1-a/2`. A north cap ending at `cos(theta_0)=c` has difference

\[
\Delta\Phi_{\rm cap}=\pi a(s)(c-c^3).
\]

This family uses a supplied axis and is only one same-sector separator.

For a lawful connection family over `S^2 x I`, the slice form alone is incomplete when `a` varies.
The globally pole-regular difference one-form

\[
b=\frac12\cos\theta\sin^2\theta\,d\varphi
\]

satisfies

\[
db=P_2(\cos\theta)\omega.
\]

Starting from a local representative `A_0` of the unit-sphere connection, take

\[
A=A_0+a(s)b.
\]

Its full curvature is

\[
\boxed{
F=F_0+a(s)db+a'(s)\,ds\wedge b.
}
\]

The mixed term makes `dF=0`. Omitting it leaves the nonzero Bianchi defect

\[
a'(s)\,ds\wedge P_2\omega.
\]

This proves abstract same-Euler connection freedom. It does not prove that every `a(s)` is realized
by a complete UDT metric. G292 separately owns an explicit complete-metric family with the same
radial pair block and Euler class but different local flux; that is the metric-realized witness.

The scalar reciprocal theorem contains no equation for `a(s)`. Combining scalar depth with Euler
number therefore still leaves continuous screen data free.

## 6. Inherited strict local branch

G259 already proved the exact conditional implication

```text
four-dimensional Lorentz metric
+ natural symmetric rank-two metric two-jet operator
+ identity divergence freedom
    -> E_ab = a G_ab + b g_ab
+ exact flat quiet vacuum
    -> b=0
+ nonidentity a!=0
    -> zero(E)=zero(G).
```

G293 does not re-prove or adopt those class hypotheses. It regresses the primary formulas

\[
E_0=rf'+f-1,
\qquad
E_1=rf'+\frac{r^2}{2}f'',
\qquad
rE_0'=2E_1,
\]

and the exact quiet branch

\[
f=1+\frac Cr.
\]

The native angular identity remains

\[
A_\parallel+A_\perp=E_1-E_0.
\]

On the nonflat quiet branch both angular modes are nonzero and cancel. No angular sector is removed.

The G259 class is not synonymous with every local metric second-order law. For example the scalar
residual `R[g]=0` lies outside its rank-two identity-divergence-free class. In the primary family,

\[
f=1+\frac Cr+\frac Q{r^2}
\]

has

\[
E_0=-\frac Q{r^2},
\qquad
E_1=+\frac Q{r^2},
\qquad
R=-\frac{2(E_0+E_1)}{r^2}=0,
\]

while it is not Einstein vacuum for `Q != 0`.

The safe conclusion is therefore:

> A non-GR UDT parent law must leave at least one G259 class hypothesis.

It is not yet forced to be higher order, nonlocal, augmented-state, or source-driven.

## 7. Primitive-state and data-dependence lattice

The remaining possibilities are best organized by their primitive state and required continuation
data. They are not disjoint mechanism names.

| Code | Primitive dependence | Minimum new premise |
| --- | --- | --- |
| `M2` | strict G259 metric two-jet rank-two class | adopt all G259 hypotheses; conditionally gives Einstein vacuum zero set |
| `MN` | another local finite metric jet or residual type | specify the exact natural nonidentity operator, order/rank, constraints, data, and well-posedness |
| `A` | a finite local augmented state, such as independent complete relation/screen/source variables | own the state, physical evolution direction, gauge-natural generator, constraints, and initial data |
| `NL` | irreducibly global/nonlocal whole-history or relation-network dependence | own the global domain, path/population, causal support, boundary/asymptotic data, and nonidentity predicate |

A higher-order metric equation can often be rewritten as a first-order augmented system. Eliminating
an augmented field may produce a higher-order or nonlocal metric equation. Thus equation appearance
does not decide physical architecture.

“Einstein plus source” is also not a separate top-level lane:

- an independent local source belongs to `A`;
- a finite-jet metric-functional source belongs to `M2` or `MN`;
- a source with memory or global dependence belongs to `NL`;
- defining `T_ab:=G_ab/kappa` after choosing a metric is an evaluator and selects nothing.

## 8. What a future candidate must accomplish

A candidate completion must, within its declared state/data class:

1. be natural under spacetime, pair, screen, and frame equivalences;
2. act after angular, screen, mixing, and shift enter the complete state;
3. retain exact pair reversal and lawful composition;
4. contain the G257 active-angular GR quiet branch without switched-off terms or fitted windows;
5. reject at least one G286 same-prior/all-join-jet continuation by a preregistered residual;
6. constrain G292's continuous same-sector flux rather than only its Euler label;
7. possess a nonempty regular solution family and a declared continuation-data burden;
8. provide well-posedness or an explicitly weaker global selection notion;
9. expose every new scale, field, source, boundary, and population premise;
10. reduce observationally calibrated freedom to identifiable finite constants before fitting.

G286 is a separator rather than a universal no-go. A local candidate passes if at least one twin
fails its residual. A global candidate passes selectivity only if it treats the completed twin
histories differently. An augmented-state candidate must repeat the twin test with its full state
matched; otherwise hidden state has merely been inserted.

## 9. Exact conclusion ceiling

G293 closes three false shortcuts:

1. endpoint composition is not physical homogeneous propagation;
2. a scalar-only homogeneous generator is only a parameterized constant-depth flow: it can pass
   through a quiet middle, but does not attach that parameter to physical separation or propagate
   screen/curvature state;
3. Euler topology fixes an integral sector but not continuous local flux.

Together with inherited G259, this materially narrows the search. It does not select a history law,
prove the architecture lattice exhaustive, close omitted singular/nonorientable strata, or authorize
observational reverse engineering of a free function.

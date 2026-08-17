# G135 exact derivation — the reciprocal kernel's projective pair coordinate

Date: 2026-08-17

Current grade: `LEAD_PENDING_FRESH_ADVERSARIAL_REVIEW`

## 1. Start only after the complete pair is assembled

For supplied complete coframe and pair-realization data

```text
E=[[B,0],[Q S,Q]],
J=[Y;Z],
```

the controlling evaluator first forms

```text
h=Y^T B^T eta_2 B Y +(S Y+Z)^T Q^T Q(S Y+Z).
```

Nothing in G135 replaces this expression by a radial block or a scalar `mu`. All base, screen,
mixing, and embedding channels enter `h` before the following reduction.

On the regular calibrated Lorentzian pair stratum,

```text
h00<0,
det h<0,
```

there are unique `T>0`, `L>0`, and real `beta` such that

```text
h=-T^2(dy0+beta dy1)^2+L^2(dy1)^2.
```

Explicitly,

```text
T^2=-h00,
beta=h01/h00,
L^2=h11-h01^2/h00,
T L=sqrt(-det h).
```

The reciprocal decomposition is

```text
T=sigma exp(-phi_pair),
L=sigma exp(+phi_pair),
sigma=sqrt(T L),
phi_pair=(1/2)log(L/T).
```

The terminal conditional pair-calibration ratio is

```text
q := c_eff^(pair)/c_E
   = T/L
   = exp(-2 phi_pair).
```

Everything below is therefore a readout of the completed `h`, not an angular correction attached to
a scalar result afterward.

## 2. Sum and contrast reveal a bounded coordinate already inside the kernel

Define the completed clock/ruler density vector

```text
w=(T,L)^T=sigma (exp(-phi_pair),exp(+phi_pair))^T.
```

Pass from the clock/ruler basis to its common/contrast basis:

```text
C=(L+T)/2,
A=(L-T)/2.
```

The projective slope of this vector is

```text
chi=A/C=(L-T)/(L+T).
```

Substitution gives the exact chain

```text
chi=(L-T)/(L+T)
   =(1-q)/(1+q)
   =tanh(phi_pair).
```

Equivalently,

```text
chi=(c_E-c_eff^(pair))/(c_E+c_eff^(pair))
```

inside the conditional pair-`c_eff` scope. This last formula does not promote pair `c_eff` to a
local material signal speed.

The same result appears directly from the reciprocal kernel. Let `p=exp(phi)` and

```text
D=diag(1/p,p),
H=[[1/2,1/2],[-1/2,1/2]].
```

Then

```text
H D H^-1
 =[[ (p+p^-1)/2, (p-p^-1)/2],
   [ (p-p^-1)/2, (p+p^-1)/2]].
```

Acting on the neutral common/contrast ray `(1,0)^T` produces a projective slope

```text
[(p-p^-1)/2]/[(p+p^-1)/2]
 =(p^2-1)/(p^2+1)
 =tanh(phi).
```

Thus `chi` is not guessed because `tanh` looks convenient. It is the contrast/common projective
slope of the founded reciprocal kernel after the complete pair metric has supplied its two positive
densities.

## 3. Exact symmetries and limits

For every finite regular pair,

```text
-1<chi<1.
```

The distinguished rays behave as follows:

```text
T=L                    -> phi_pair=0       -> chi=0,
T/L -> 0               -> phi_pair->+inf   -> chi->+1,
T/L -> +inf            -> phi_pair->-inf   -> chi->-1.
```

Positive common rescaling

```text
(T,L)->(Omega T,Omega L)
```

leaves `chi` unchanged while changing `sigma` and `h`. This is a separation of reciprocal shape
from common scale, not a revival of strong local CSN and not a claim that the metric is scale free.

Abstract channel exchange `T<->L` sends

```text
phi_pair->-phi_pair,
q->1/q,
chi->-chi.
```

This is an exchange of labelled reciprocal channels. It is not a causal Lorentz transformation
that literally swaps a timelike line with a spacelike line.

For a physical nonnegative separation proposal, the corresponding magnitude would be `|chi|`.
G135 does not identify that magnitude with proper length or with physical distance.

## 4. Composition is fractional-linear, not ordinary addition

For a matched carried reciprocal comparison,

```text
phi_12=phi_1+phi_2,
q_12=q_1 q_2.
```

Therefore

```text
chi_12
 =(chi_1+chi_2)/(1+chi_1 chi_2).
```

This operation is associative, has identity zero, and inverse `-chi`. It is the projective display
of the already-derived additive depth law. It is not ordinary addition.

If a dimensional signed coordinate were conditionally defined by

```text
x=X_max chi,
```

its composition would be

```text
x_12=(x_1+x_2)/(1+x_1 x_2/X_max^2).
```

This makes the analogy with rapidity and bounded relative velocity mathematically exact at the
group-chart level. It does not derive the physical identification or the value of `X_max`.

Conversely, if an ordinary signed separation `s` is postulated to add on all of `R`, continuity and

```text
delta(s1+s2)=delta(s1)+delta(s2)
```

force

```text
delta(s)=k s
```

for an inverse-length constant `k`. Such an ordinary additive coordinate has no finite global
endpoint. A finite asymptote therefore belongs naturally to a bounded chart such as `chi`, or to a
partial/non-group distance operation; it cannot simultaneously be an unrestricted ordinarily
additive length coordinate.

## 5. The exact restricted uniqueness theorem

Let a scale-neutral first-degree fractional-linear readout of the positive pair ray be

```text
F(r)=(a r+b)/(c r+d),
r=L/T>0.
```

Demand the three intrinsic ray anchors

```text
F(0)=-1,
F(1)=0,
F(infinity)=+1.
```

After fixing the irrelevant coefficient scale by `d=1`, the equations are

```text
b+d=0,
a+b=0,
a-c=0,
d=1.
```

Their unique solution is

```text
(a,b,c,d)=(1,-1,1,1),
```

so

```text
F(r)=(r-1)/(r+1)=chi.
```

Exchange `r->1/r` then gives `F(1/r)=-F(r)` automatically. Hence `chi` is the unique anchored
first-degree projective coordinate on the completed reciprocal pair ray.

The theorem is exact but its class is load-bearing. The current foundation supplies the dual ray
and its three distinguished rays; it does not explicitly say that operational separation must be a
first-degree projective coordinate.

## 6. Unrestricted smooth uniqueness is false

For

```text
f_epsilon(chi)=chi+epsilon chi(1-chi^2),
-1<epsilon<1/2,
```

every member is a smooth strictly increasing odd bijection of `[-1,1]` fixing `-1,0,+1`.

The slope-matched companion

```text
g_epsilon(chi)=chi+epsilon chi^3(1-chi^2)
```

also has

```text
g_epsilon'(0)=1.
```

Each display inherits an exact associative operation by conjugating additive `phi_pair`. At

```text
epsilon=1/4,
chi_1=1/3,
chi_2=1/5,
```

the discrepancy between marking after native Mobius composition and applying the original Mobius
formula to the re-marked coordinates is exactly

```text
-45/29728 != 0.
```

Thus the original Mobius display law distinguishes the projective chart, but continuity, oddness,
anchors, neutral slope, boundedness, and abstract group consistency do not select it among all
smooth charts.

## 7. Projective position is not metric proper length

Consider

```text
h1=diag(-1,4),
h2=4 h1=diag(-4,16).
```

They have

```text
(T1,L1)=(1,2),
(T2,L2)=(2,4),
q1=q2=1/2,
chi1=chi2=1/3.
```

But on the same unit ruler-coordinate segment their spatial metric lengths are `2` and `4`.
Therefore `phi_pair`, `q`, or `chi` cannot recover common metric scale or ordinary proper length.

This does not refute the UDT interpretation that positional separation may be constituted by
reciprocal dilation rather than equal to a pre-existing path length. It types that interpretation
precisely: adopting it would make projective pair position a distinct operational observable, not a
synonym for the metric length integral.

Observed `c_E` has dimensions length/time. Since `chi` is dimensionless, `c_E` alone cannot produce
the length in `x=X_max chi`. A time, mass/density/curvature datum plus a lawful bridge, or an
independently owned global length is still required. `G_obs` is not load-bearing in this kinematic
audit.

## 8. Information ceiling and the one-spacetime network

Since

```text
phi_pair=atanh(chi),
```

`chi` and `phi_pair` carry exactly the same scalar information on the regular finite stratum.
Consequently, under the G131 shared-domain hypotheses, all labelled `chi` values recover only the
positive conformal class, not the common scale. They do not replace the rank-complete full-pullback
or complete-area network that reconstructs one full metric.

One compatible complete pair network still describes one spacetime. Different pair values are
different relational restrictions/readouts of that same `g`, not separate metrics created by each
observer pair.

## 9. Historical regrade

The July projective audit found the same fractional-linear theorem and the same counterfamilies, but
its language used strong local CSN and preceded the no-shortcut complete-pair evaluator.

G135 changes the provenance:

1. strong local CSN is inactive and unnecessary;
2. common scale `sigma` remains real supplied metric data rather than being quotiented from physics;
3. the projective coordinate is only the reciprocal-shape readout alongside that scale;
4. the full `B,Q,S,Y,Z` orchestra changes `h`, hence `T,L,q,chi`, before terminal readout;
5. no scalar mixing modulus or angular post-processing is used.

The July warning remains valid: physical distance is not selected merely because a canonical
projective chart exists.

## 10. The smallest remaining conceptual joint

The present algebra supports the following sharply bounded statement:

> A supplied regular calibrated complete pair metric owns a canonical anchored projective
> reciprocal coordinate `chi`. If UDT's phrase “positional comparison” is clarified to mean that
> physical normalized signed pair position is this projective coordinate, then
> `x/X_max=chi=tanh(phi_pair)` follows without a fitted profile or appended angular mechanism.

That clause would be a constitutive clarification of the observer-pair observable. It would not be
a new action, force, source, or dynamical mechanism. It is nevertheless not present in the active
premise registry, which explicitly keeps the exact `X_max` approach profile open.

Even after such a clarification, the following remain open:

- the physical pair query/realization and global branch family;
- the numerical/global value and origin of `X_max`;
- how the complete time-live history assigns `h` to every pair;
- singular, cut-locus, and topology-changing continuation;
- action, source, bootstrap, matter, observations, and signalling.

## 11. Exact bounded landing

```text
PROJECTIVE_PAIR_COORDINATE_DERIVED_IN_NATURAL_CLASS__
RECIPROCAL_KERNEL_SUM_CONTRAST_SLOPE_EQUALS_TANH_PHI_PAIR__
FULL_ORCHESTRA_ENTERS_BEFORE_THE_PROJECTIVE_READOUT__
UNRESTRICTED_SMOOTH_POSITION_CHART_UNIQUENESS_FALSE__
PROJECTIVE_POSITION_IS_NOT_PROPER_LENGTH_AND_DOES_NOT_RECOVER_COMMON_SCALE__
PHYSICAL_SEPARATION_IDENTIFICATION_XMAX_SCALE_PAIR_REALIZATION_AND_HISTORY_REMAIN_OPEN
```

No canonization is requested.

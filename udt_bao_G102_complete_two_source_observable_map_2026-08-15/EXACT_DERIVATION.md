# Exact derivation — complete observer-plus-two-source observable map

Date: 2026-08-15

## 1. Result first

The corrected preregistered landing is obtained internally:

```text
COMPLETE_TWO_SOURCE_OBSERVABLE_EVALUATOR_DERIVED
__DIRECTION_IDENTIFICATION_QUERY_OWNED
__ENDPOINT_DEPTH_CARRY_CONDITIONAL
__PHYSICAL_HISTORY_AND_SOURCE_PAIR_MEASURE_OPEN
```

This is a conditional evaluator theorem. No BAO curve, descriptor, feature angle, covariance,
singular vector, ruler, `X_max`, or metric history was read or fitted.

## 2. One observer, two complete pair relations

Let source label `a` denote one supplied regular observer--source pair relation. At the common
observer endpoint, the complete coframe and pair Jacobian give

```text
V_a^O=E_O J_a^O=[v_a0^O,v_a1^O],
h_a^O=(V_a^O)^T eta_4 V_a^O.
```

The upstream identity

```text
E_O=[[B_O,0],[Q_O S_O,Q_O]],
J_a^O=[Y_a^O;Z_a^O]
```

means every complete `B,Q,S,Y,Z` component enters `V_a^O` before the directional readout. Nothing is
appended to a scalar redshift afterward.

Assume only

```text
(h_a^O)00<0,
det(h_a^O)<0.
```

Define

```text
T_a=sqrt(-(h_a^O)00),
u_a=v_a0^O/T_a,
r_a=v_a1^O-((h_a^O)01/(h_a^O)00)v_a0^O,
L_a=sqrt((h_a^O)11-(h_a^O)01^2/(h_a^O)00),
n_a=r_a/L_a.
```

Direct contraction gives

```text
g(u_a,u_a)=-1,
g(u_a,n_a)=0,
g(n_a,n_a)=+1.
```

Thus `n_a` is the normalized positive direction of the supplied pair ruler in the supplied pair
plane. The ordered query—not the bare metric—identifies and orients it as the outward observed
source direction.

The two relations define one observer sky only if

```text
u_1=u_2=u_O.
```

Then the exact observer angle is

```text
cos(theta_12)=g_O(n_1,n_2).
```

This is the missing two-source join. It is not a galaxy--galaxy signal path; it is the angle between
two complete observer--source ruler channels at their common observer.

## 3. Calibration and frame covariance

Under the positive pair-column change

```text
v_0 -> a v_0,
v_1 -> b v_1+c v_0,
a>0, b>0,
```

one obtains exactly

```text
r -> b r,
L^2 -> b^2 L^2,
n -> n.
```

So the observed direction and joined angle do not depend on clock scale, positive ruler scale, or
the pair shift along the clock channel. Negative ruler scaling flips to the antipodal direction;
that is why ordered outward orientation is query data rather than gauge.

A common Lorentz/coframe change preserves every contraction and hence `theta_12`. The exact rational
boost witness in `derive_two_source_map.py` returns zero angle defect.

## 4. Redshift is a different endpoint type

The sky direction is observer-local. The observed redshift belongs to the accumulated depth of the
same full pair relation:

```text
DeltaPhi_a=phi_pair(q_a)-phi_pair(O),
Z_a=1+z_a=exp(DeltaPhi_a).
```

G99 conditionally supplies this middle-regime terminal identification. It does not derive the
physical history or endpoint carry. The observer-local matrix `h_a^O` must not be silently reused as
the accumulated depth. G102 caught and corrected that category error before accepting a result.

Each source therefore contributes the typed output

```text
Psi(a)=(Z_a,n_a)
```

from one complete relation, with the two components evaluated at their proper locations.

## 5. Exact discrete estimator join

For data objects with observed weights `w_i`, shell selector `S(Z_i)`, and angular bin indicator
`I_k(theta_ij)`, define

```text
DD_k=sum_(i<j) w_i w_j S(Z_i)S(Z_j) I_k(theta_ij),
DD_tot=((sum_i w_i)^2-sum_i w_i^2)/2.
```

Define `DR_k,DR_tot` and `RR_k,RR_tot` analogously using the frozen survey random catalog, with

```text
DR_tot=(sum_i w_i)(sum_A w_A^R),
RR_tot=((sum_A w_A^R)^2-sum_A (w_A^R)^2)/2.
```

Then the frozen measurement functional is

```text
dd_k=DD_k/DD_tot,
dr_k=DR_k/DR_tot,
rr_k=RR_k/RR_tot,
w_k=(dd_k-2dr_k+rr_k)/rr_k.
```

The estimator is a borrowed category-A measurement method. It does not add a physical ruler or
source mechanism. A four-data/five-random exact synthetic fixture gives

```text
DD=(8,15,12),
DR=(19,18,13),
RR=(2,4,4),
w=(-58/35,19/70,39/70).
```

An independent Fraction-only implementation reproduces every entry of this synthetic exact fixture.
This is not a survey-scale pipeline replay. The initially mistyped expected vectors were corrected
under a separately banked verifier-repair preregistration before the verifier's first execution.

## 6. Global and branch-safe formulation

Let `Sigma` be a source-label space, `b` label regular relation branches, and

```text
Psi_b:Sigma -> R_+ x S_O^2
```

be the evaluated redshift-and-direction map. Let `lambda_1` and `lambda_2` be source one- and
two-point measures, and let `a_b` contain any physical selection/transfer and branch weighting.
The branch-safe observed measures are pushforwards:

```text
nu_1=sum_b (Psi_b)_*(a_b lambda_1),
nu_2=sum_(b,c) (Psi_b x Psi_c)_*(a_b a_c lambda_2^(b,c)).
```

This statement does not require injectivity and therefore accommodates multiple images, branches,
and critical maps. A local Jacobian-density formula is permitted only on a regular injective chart.

The angular estimator is a bin-and-mask functional of `nu_1,nu_2` and the observed survey
selection. It is not a function of the terminal scalar depth alone.

## 7. Exact identifiability ceiling

If one regular branch `Psi` is invertible onto its image, the source pair measure is unrestricted,
and the target observed pair measure is supported in that image, the target can be reproduced by
pulling it back through `Psi x Psi`. Consequently, on that exact domain an invertible geometric sky
map plus a freely chosen source pair measure is observationally non-identifiable from one angular
curve.

The finite exact witness uses a nontrivial permutation `P`:

```text
C_src=P^T C_obs P,
P C_src P^T=C_obs.
```

Thus two different map/source assignments return the same observed pair measure. This does not say
geometry has no effect. It says the evaluator cannot predict a unique curve until at least one of
the following is owned:

- the physical source pair measure or a cross-query restriction on it;
- the complete history and branch weights;
- noninvertible/critical/global structure producing source-independent constraints;
- a joint law tying source and geometry rather than fitting either freely.

## 8. Where G99 enters

G99 supplies the frozen conditional middle-regime relation between terminal depth and observed
redshift and, separately, a conditional radial chord `r_cal(z)`. The raw angular estimator needs
only `Z` and `n`; it does not use `r_cal`, `X_eff`, or a standard ruler.

`r_cal(z)` can later locate a shell inside a supplied complete history so that its `B,Q,S` response
is evaluated at the proper regime. Because no complete history is selected, G102 does not invent
that dependence or append an orchestra correction to G99.

## 9. Maximum conclusion

The metric now owns the conditional evaluator architecture from two supplied complete pair
relations to the exact observer-coordinate statistic. It does not yet own a predicted BAO curve.
The remaining obstruction is no longer an undefined preferred path: it is the physical complete
history plus source/selection pair measure on the typed two-source relation family.

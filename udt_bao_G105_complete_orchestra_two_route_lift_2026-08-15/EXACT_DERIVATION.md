# Exact derivation — complete-orchestra two-route observer artifact

Date: 2026-08-15

## 1. Bounded landing

```text
COMPLETE_ORCHESTRA_ONE_POINT_OBSERVER_ARTIFACT_CHANNEL_DERIVED_CONDITIONALLY
__FACTORIZED_INTRINSIC_CONNECTED_EXCESS_ZERO
__LOCAL_COMMON_OBSERVER_H_NOT_OWNED
__PHYSICAL_HISTORY_REFERENCE_PROJECTION_AND_GLOBAL_BRANCH_LAW_OPEN
__BOSS_AND_CMB_OUTCOMES_UNREAD
```

This corrects an overly narrow reading of G104. A nonfactorizing `H` is not the only lawful UDT
observer-artifact route. The complete one-source map can produce a physical observed one-point
modulation through its Jacobian. A pair estimator referenced to a survey measure `q` then measures
the autocorrelation of the part of that physical modulation not represented by `q`.

The result is conditional on a supplied complete history, typed observer/source relation family,
source one-point measure, and survey-reference measure. None of those physical choices is selected
here.

## 2. Complete orchestra before the observation map

For source label `a`, the banked complete pair evaluator is

```text
E=[[B,0],[Q S,Q]],
J_a=[Y_a;Zeta_a],
V_a=E J_a,
h_a=V_a^T eta_4 V_a.
```

On the regular common-observer stratum, write the two columns of `V_a` as `v_0,v_1`. The common
observer clock and outward ruler direction are

```text
T=sqrt(-g(v_0,v_0)),
u=v_0/T,
alpha=g(v_0,v_1)/g(v_0,v_0),
r=v_1-alpha v_0,
L=sqrt(g(r,r)),
n=r/L.
```

The accumulated endpoint depth remains a distinct type:

```text
DeltaPhi_a=phi_pair(q_a)-phi_pair(O),
zeta_a=log(1+z_a)=DeltaPhi_a.
```

Thus the one-source observation map is

```text
Psi(a)=(zeta_a,n_a).
```

No angular or mixing correction is appended to `zeta` or `n`. Both are read after the complete
pair relation has been assembled.

## 3. Exact source-label derivative

For a source-label coordinate `a^A`,

```text
D_A V=(D_A E)J+E(D_A J),
D_A h=(D_A V)^T eta_4 V+V^T eta_4(D_A V).
```

On a fixed-observer sky, `D_A E_O=0`, but the common matrix `E_O` still contains `B,Q,S` and acts on
every `D_A J`. For a moving observer/event query the first term remains as well.

The terminal differential is

```text
D_A phi_pair
 =1/4 [tr(h^-1 D_A h)-2(D_A h_00)/h_00].              (1)
```

The accumulated `D_A DeltaPhi` additionally carries the source- and observer-endpoint evaluation
on the same relation family; equation (1) must not be silently replaced by the observer-local
matrix alone.

When the common observer `u` is fixed across the source labels, differentiation of the normalized
ruler gives

```text
D_A n
 =[D_A r-n g(n,D_A r)]/L.                             (2)
```

Equations (1)--(2), together with `D_A V`, are the complete local differential. Every `B,Q,S,Y,Zeta`
channel enters through `V` and its variation before the observation-map Jacobian is formed.

## 4. Covariant geometric Jacobian

Let the source-label sheet carry the supplied proper metric `gamma`. On a three-dimensional source
domain define

```text
M_AB=(D_A DeltaPhi)(D_B DeltaPhi)+g_O(D_A n,D_B n),
J_Psi=sqrt(det(M)/det(gamma)).                         (3)
```

On a fixed-redshift two-surface, retain only the screen term in `M`. Equation (3) is the ratio of
the pulled-back observer-coordinate volume to the source proper volume. It is independent of the
coordinates used on either side.

For a regular finite-to-one branch family and source intensity `rho` per proper source volume, the
observed one-point density is

```text
p(x)=sum_(a in Psi^-1(x)) rho(a)/J_Psi(a).             (4)
```

Equation (4) is the first exact UDT kaleidoscope channel. Even with constant `rho`, a nonconstant
`J_Psi` can give a nonconstant observed `p`. It need not do so: branch sums or a compensating source
density can cancel it. The physical history and source density remain load-bearing.

## 5. Factorized mapping theorem

The null-source working premise is

```text
lambda_2^! = lambda tensor lambda
```

off the diagonal. For any one-source Markov/pushforward operator `K_1`, including a noninjective
map or an independently selected single branch,

```text
nu_1=K_1[lambda],
nu_2=(K_1 tensor K_1)[lambda tensor lambda]
    =nu_1 tensor nu_1.                                 (5)
```

Therefore the intrinsic connected measure relative to the physical one-point intensity is exactly

```text
C_p=nu_2-nu_1 tensor nu_1=0.                           (6)
```

The fact that both directions use the same observer and that an angle bin evaluates
`g_O(n_1,n_2)` does not alter (5). The angle is a function applied to two already-evaluated outputs;
it is not by itself a coupling of their probability measure.

## 6. Why the observer artifact can nevertheless be visible

Let `q` be the normalized one-point reference represented by the survey random catalogue. The
ideal normalized Landy--Szalay numerator for a bin kernel `I_k` is

```text
N_k(q)=integral I_k [nu_2-p tensor q-q tensor p+q tensor q].
```

Using (5),

```text
N_k(q)=integral I_k (p-q) tensor (p-q).                (7)
```

If `q=p`, equation (7) vanishes. If

```text
p=q(1+m),
integral m dq=0,
```

then

```text
N_k(q)=integral I_k(x,y)m(x)m(y)q(dx)q(dy).            (8)
```

Equation (8) is an observer-coordinate pair pattern generated by the autocorrelation of a physical
one-point geometric modulation. It requires no intrinsic source two-point pattern and no
nonfactorizing `H`.

This is the intended observational-artifact route. It is not automatically a survey error. The
same algebra also describes a bad survey-reference model, so ownership matters:

- if `p-q` is produced by the UDT map while `q` correctly represents instrumental selection, the
  term is a physical frame effect;
- if `p-q` is produced by missing mask/completeness/calibration information, it is a survey
  systematic;
- if the random construction absorbs some physical radial or angular modulation, only the
  unabsorbed projection remains in (8).

G105 does not open the survey pipeline or outcome files, so that projection remains `OPEN`.

## 7. Exact complete-orchestra witness

The production witness uses rational nonidentity matrices

```text
B=[[2,1/3],[1/5,3/2]],
Q=[[3/2,1/4],[1/5,4/3]],
S=[[1/4,1/6],[-1/7,1/5]].
```

Its common clock has a nonzero top embedding `Y`, while the ruler circle has a nonzero lower
embedding `Zeta`. The complete clock is timelike:

```text
h_00=-2699027/705600.
```

The exact squared angular speed of the normalized observed direction is

```text
j(0)^2    =6146426711425/8625933756036,
j(pi/2)^2 =2890074927168/2493762097225.
```

They are unequal. Hence a uniform supplied source-circle measure pushes forward to a nonuniform
observer-angle measure. Replacing `B`, `Q`, or `S` independently changes the exact result; the
witness is not produced by bolting one angular correction onto a scalar kernel.

This witness proves existence inside the complete conditional arena. It does not select this
history, source circle, or angular profile as physical.

The discrete measure witness takes

```text
q=(1/3,1/3,1/3),
m=(-1/2,1/4,1/4),
p=q(1+m)=(1/6,5/12,5/12).
```

For one off-diagonal bin kernel, exact evaluation gives

```text
N=1/72,
RR=2/9,
N/RR=1/16.
```

The independent Fraction-only implementation reproduces every rational value.

## 8. The genuinely nonfactorizing route

Write

```text
K_2=K_1 tensor K_1+H.
```

Then

```text
C_p=H[lambda tensor lambda].                          (9)
```

A finite exact witness with fixed one-point marginal is

```text
H=(1/16)[[1,-1],[-1,1]],
p tensor p+H=[[5/16,3/16],[3/16,5/16]].
```

The rows and columns of `H` sum to zero and the total pair measure is nonnegative. This proves the
mathematical type of an irreducible mode; it does not derive a physical `H`.

Independent exactly-one branch marking remains in (5). Retaining several images of the same source,
correlating branch choices, imposing a non-Cartesian global admissible relation family, or averaging
over a physically random common history can produce (9), but no current local complete-pair identity
owns those structures. Existing common-observer and Gram conditions type simultaneous geometry;
for two arbitrary sky directions they do not select a pair law.

## 9. Coefficient disposition

- `a_area`: a conditional geometric channel now exists through `J_Psi`, but no selected basis or
  free amplitude exists. The coefficient remains dormant.
- `a_conn`: dormant; no local irreducible `H` is owned.
- `a_branch`: dormant; no physical correlated branch family is owned.
- `a_regime`: dormant; no complete physical regime history is owned.

When a physical history is supplied, the Jacobian amplitude is determined by that history rather
than automatically becoming a free fit coefficient.

## 10. Maximum justified conclusion

The complete orchestra already supports the user's intended BAO ontology conditionally: an
unpatterned source population can acquire an observer-coordinate one-point modulation, whose
autocorrelation can appear as a pair pattern against a survey-only reference. This route does not
require intrinsic galaxy clustering or an irreducible `H`.

What remains open is whether the physical UDT history produces a nonconstant modulation with the
observed structure, which part survives the actual random-catalogue projection, and whether global
branch geometry adds a separate `H`. No outcome, feature, coefficient, or cosmological scale has
been used.

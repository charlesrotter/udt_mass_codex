# G183 exact derivation — pair degeneracy and multibranch strata

Date: 2026-08-19

## 1. Typed arena

Let `(M,g)` be Lorentzian of index one. For one supplied two-dimensional pair realization, let

```text
V=(v_0,v_1)=EJ,
h=V^T eta V,
h_ij=g(v_i,v_j).
```

The accepted completed-pair scalar kernel uses the supplied clock coordinate and requires

```text
h_00<0, det(h)<0,
T=sqrt(-h_00), m=sqrt(-det(h)), Phi=-log(T).
```

Three different uses of “null” must not be conflated.

## 2. A null curve does not make the pair plane null

In the regular pair metric

```text
h=-d tau^2+d s^2,
```

the curve with tangent `(1,1)` is null, while `det(h)=-1`. Null propagation inside the supplied
Lorentzian plane therefore does not invalidate the pair kernel.

## 3. A null chosen clock is a calibrated-chart failure

In Minkowski coframe take

```text
v_0=(1,1,0,0),  v_1=(0,1,0,0).
```

Then

```text
h=[[0,1],[1,1]], det(h)=-1.
```

The two-plane is nondegenerate Lorentzian even though the chosen clock column is null. Indeed,
`v_0-v_1=(1,0,0,0)` is timelike with norm `-1`.

Thus `h_00=0, det(h)<0` is not an intrinsic plane singularity. It is outside the accepted kernel in
the supplied clock calibration. Replacing the clock direction repairs the chart, but it changes the
calibrated observer query unless that replacement was already part of its rules.

## 4. True rank loss with a timelike clock

Assume `u=v_0` is timelike. Decompose

```text
v_1 = alpha u + w,
alpha = g(u,v_1)/g(u,u),
g(u,w)=0.
```

The orthogonal complement of a timelike vector in an index-one Lorentz space is positive definite.
Therefore `g(w,w)>=0`, with equality exactly when `w=0`. Directly,

```text
det(h)=g(u,u) g(w,w).
```

Since `g(u,u)<0`,

```text
det(h)<0  iff  w!=0  iff  rank(V)=2,
det(h)=0  iff  w=0   iff  v_1 is proportional to u.
```

This is an intrinsic domain failure of the pair pullback. Here `m=sqrt(-det(h))` vanishes and the
completed ruler normalization divides by zero. No scalar continuation can restore the missing
tangent direction.

The timelike-clock hypothesis is essential. Let

```text
k=(1,1,0,0), e=(0,0,1,0).
```

Then `k,e` are independent but their Gram matrix is `[[0,0],[0,1]]`. The ambient tangent map has
rank two while the induced metric has rank one: this is a null-degenerate plane, not map rank loss.
Likewise two independent spatial basis vectors have Gram matrix `diag(1,1)`, a rank-two spacelike
plane with no timelike observer-clock direction. Both lie outside the accepted pair-kernel domain.

The production replay tested this equivalence on 12,000 exact rational timelike Gram families. The
independent replay used a rational Lorentz basis and tested 20,000 further families.

## 5. Focal and caustic rank loss is query-restricted

Consider the flat normal-exponential family of a uniformly accelerated observer,

```text
F(tau,s)=((a^-1+s)sinh(a tau),(a^-1+s)cosh(a tau)).
```

Its tangent columns satisfy

```text
g(F_tau,F_tau)=-(1+a s)^2,
g(F_tau,F_s)=0,
g(F_s,F_s)=1.
```

At `s=-a^-1`, every value of `tau` maps to the same focus and `F_tau=0`. The selected pair
realization loses rank and its kernel genuinely fails there.

The quantifier matters: an ambient exponential map may possess some conjugate direction while the
particular two-dimensional query samples a different, nonsingular variation. Only rank loss of the
actual supplied `dF` breaks this pair germ. “An ambient conjugate point exists” is not by itself a
pair-kernel failure theorem.

## 6. Regular branch crossings do not break the kernel

In flat `1+2` geometry define

```text
F_+(tau,s)=(tau,s,+s(1-s)),
F_-(tau,s)=(tau,s,-s(1-s)),  0<=s<=1.
```

The two branches have the same endpoints and identical induced metrics,

```text
h_+=h_-=-d tau^2 + [1+(1-2s)^2] d s^2,
```

but different spatial endpoint tangents. Both remain rank two. Their completed scalar is `Phi=0`
on each branch. Therefore endpoint equality, scalar equality, and even pair-metric equality do not
select the branch or erase its tangent data.

## 7. Cut and winding multiplicity can remain completely regular

Use the flat product `R x S^1` with circle circumference `2`. Let the source and antipodal endpoint
be separated by the lifted displacements

```text
ell_n=1+2n,  n in Z.
```

For

```text
F_n(tau,u)=(tau, ell_n u mod 2), 0<=u<=1,
```

the induced metric is

```text
h_n=-d tau^2+ell_n^2 d u^2.
```

Every branch is regular. The `n=0` and `n=-1` antipodal branches have the same metric and equal tape
magnitude but opposite lifted directions; other windings have different tape lengths. All have
`Phi=0`.

Thus a cut can be global branch multiplicity rather than local degeneration. The correct output of
the metric evaluator is the branch-indexed family `{Eval(F_n)}` unless a separate query rule proves
uniqueness. The scalar kernel does not erase the winding label. Actual connection holonomy, when
requested, remains a separate path-labelled output and need not be nontrivial in this flat witness.

## 8. Classification theorem

On the stated supplied-query arena:

| Stratum | Local pair plane | Accepted clock chart | Kernel status | Output type |
|---|---|---|---|---|
| null curve inside regular plane | Lorentzian, rank two | regular | valid | same branch scalar plus null curve |
| null chosen clock, `det(h)<0` | Lorentzian, rank two | fails | undefined in that calibration | rechart only by changing/supplying clock |
| null plane, `det(h)=0`, tangent rank two | induced metric rank one | fails intrinsically | undefined | null-degenerate pullback |
| `h00<0, det(h)=0` | tangent rank one | fails intrinsically | undefined | germ rank loss |
| spacelike pair plane | positive definite, rank two | no observer clock | undefined | wrong causal pair type |
| sampled focal/caustic point | rank loss of actual `dF` | fails | undefined at focus | branch endpoint/failure |
| regular cut/crossing | Lorentzian on each branch | regular | valid per branch | branch-indexed family |
| regular winding | Lorentzian on each lift | regular | valid per lift | winding-indexed family; transport separate |

Primary landing:

```text
PAIR_STRATA_SEPARATED__REGULAR_MULTIBRANCH_KERNEL_REMAINS_BRANCH_LABELLED
```

This classifies the already accepted kernel. It neither selects the supplied query/branch nor adds
a path, source, dynamics, global completion, or new scalar.

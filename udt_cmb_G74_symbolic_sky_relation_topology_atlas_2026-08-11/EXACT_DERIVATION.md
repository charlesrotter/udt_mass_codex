# G74 exact derivation — symbolic-scale observer-sky topology and criticality

Date: 2026-08-11

Internal landing pending fresh adversarial review:

`MIXED_GLOBAL_COMPLETION_CLASSES`

This classifies the exact 21-profile G68 control universe under one complete-sky query. It is not a
physical CMB sky, source, profile, endpoint, spectrum, or `X_max` result.

## 1. Correctly typed global relation

At a supplied observer event, let `S_o^2` be the sphere of future null directions. For each regular
first-crossing branch, the metric geodesic flow and the declared comparison sphere supply

```text
f_b:S_o^2 -> S_s^2,
```

where `S_s^2` records the angular point at the first outward `r/R=1` crossing. Endpoint coordinate
time is retained as an additional state but is not part of the angular degree.

The scale `R>0` is symbolic. With `x=r/R` and the registered dimensionless control coefficients
fixed, a common positive rescaling multiplies physical screen areas by a positive factor. It cannot
change a zero, the sign of an oriented Jacobian, or the integer degree. This does not determine a
physical `R`.

Null geodesics are the declared observer-sky query generators. They are not promoted to material
signals in the co-present interpretation.

## 2. Endpoint differential and three distinct singularities

Let the endpoint surface be `sigma(x)=0`, and let `J` be the Jacobi field from varying the initial
sky direction. The affine endpoint also varies. Differentiating `sigma=0` gives

```text
lambda' = -d sigma(J)/d sigma(k),
X = J + k lambda'
  = J - k d sigma(J)/d sigma(k).                            (1)
```

Therefore `d sigma(X)=0`: `X` is the actual endpoint variation tangent to the comparison surface.
After the endpoint angular projection `C`, the sky differential is

```text
df_b = C P_sigma J.                                        (2)
```

On a transverse endpoint (`d sigma(k) != 0`) with regular initial and endpoint screen
calibrations, the outside factors in (2) are invertible. A rank loss is then the metric Jacobi
caustic. This is different from:

- endpoint grazing, where `d sigma(k)=0` and (1) itself fails;
- a singular endpoint chart or screen identification;
- two or more globally distinct regular branches sharing endpoints.

The three cases must not be merged under the word “caustic.”

## 3. Exact global topology constraints

For a smooth connected whole-sky self-map `f:S^2 -> S^2`, every everywhere-regular local
diffeomorphism is proper and therefore a covering. Since the target `S^2` is simply connected, the
cover has one sheet. Hence an everywhere-regular whole-sky map is a degree `+1` or `-1`
diffeomorphism. A nontrivial repeated whole-sky self-image must have critical/branch points or be a
multibranch relation rather than one regular map.

For an axisymmetric representative

```text
(theta,phi) -> (Theta(theta), m phi + psi(theta)),
```

the oriented area Jacobian is

```text
j = m sin(Theta) Theta' / sin(theta),                       (3)
```

and

```text
degree = (m/2)[cos Theta(0)-cos Theta(pi)].                 (4)
```

The twist `psi(theta)` cancels from (3). Thus carry/twist can change orientation transport and
image appearance while leaving topology and the critical set unchanged in this declared class.
That is not a theorem that arbitrary complete angular mixing is topology-neutral.

Exact witnesses reproduce:

- identity degree `+1`;
- orientation reversal degree `-1`;
- degree `m`, where `|m|>1` requires critical points;
- the degree-zero fold `Theta=2 theta`, whose equator is critical and whose two hemispheres have
  opposite parity.

Other source topology, partial skies, and branch-labelled relations remain separate types; regular
multiplicity can occur there without violating the `S^2` self-map theorem.

## 4. Why the center gate is mandatory

The original G68 query used only an outward equatorial ray beginning at `r/R=1/4`. A complete sky
contains inward directions and therefore tests the center. In Cartesian coordinates,

```text
sin^2(theta) dpsi = (-y dx + x dy)/r^2.
```

The mixing term is controlled by `q(r)=h(r)/r^2`:

```text
g_tx=-q(r)y,  g_ty=q(r)x.                                  (5)
```

For `ZERO` and `PERSISTENT`, `q` is constant and the Cartesian metric is smooth. For both
`TAPERED` and `SIGN_CHANGING`, `q` contains a nonzero term linear in `r`. Along the `y` axis,
equation (5) contains `y|y|`; its one-sided second derivatives differ. The supplied metric is
therefore not `C2` at the center.

This produces the exact census:

```text
CENTER_C2_ELIGIBLE                              9
BLOCKED_SUPPLIED_PROFILE_NOT_C2_AT_CENTER      12
```

The twelve blocked controls remain valid for their original outward-ray use. G74 does not smooth,
splice, reflect, or otherwise complete them.

## 5. Exact F01 global theorem

For F01,

```text
ds^2=-A dt^2+dr^2/A+r^2 dOmega^2,  A=1+a r^2.
```

The spatial projections of null geodesics are geodesics of the optical metric

```text
dell_opt^2=dr^2/A^2+r^2 dOmega^2/A
           =dchi^2+S(chi)^2 dOmega^2,
dchi=dr/A,  S=r/sqrt(A).                                   (6)
```

Direct differentiation gives both sectional curvatures equal to `a`:

```text
-S''/S=a,  (1-S'^2)/S^2=a.                                (7)
```

For `a>0`, the optical radius is

```text
chi_R=atan(sqrt(a)R)/sqrt(a) < pi/(2 sqrt(a));              (8)
```

the flat and negative-curvature cases are likewise convex. The registered ball is therefore
strongly geodesically convex: each observer direction has one first exit, and each boundary point
has one in-ball geodesic from the observer. All three F01 control maps are exactly degree-one
diffeomorphisms. This is a control theorem, not physical branch selection.

## 6. Complete numerical census of the eligible controls

The exact Cartesian persistent-family metric is

```text
g_tt=-(1+a r^2),
g_ti=epsilon(-y,x,0),
g_ij=delta_ij-[a/(1+a r^2)]x_i x_j.                         (9)
```

The production calculation evolves the exact Hamiltonian on nested icospheres. Across all
`36` profile/mesh/time rows (`53,352` vertex evaluations and `106,560` oriented face evaluations):

```text
missing endpoint vertices                0
negative oriented faces                  0
near-zero faces                          0
degree estimate on every row             1 within 2.22e-16
minimum finest signed-area ratio          0.5505843446454626
maximum 512-to-1024 endpoint chord drift  4.922697873263042e-6
maximum Hamiltonian residual              9.878675655272673e-11
```

The three F01 rows inherit the exact global theorem. The six persistent-mixing rows are only
`OBSERVED_SAMPLED_REGULAR_NOT_GLOBAL_PROOF`: finite meshes cannot exclude an unsampled critical
set or establish global injectivity.

## 7. Independent metric-connection replay

A separate implementation constructs the Cartesian metric, its derivatives, and the full
Levi-Civita connection directly, then integrates all `9 x 162 = 1,458` subdivision-2 rays with
adaptive `DOP853`. It never calls the production Hamilton equations.

```text
endpoints reached                         1,458 / 1,458
maximum endpoint chord disagreement       1.2166590761244587e-6
maximum direct null residual              4.9960036108132044e-15
maximum independent degree error          0
minimum independent signed-area ratio     0.5505843446454627
```

Its direct one-sided center test gives derivative jumps `0` for persistent mixing,
`0.39999400000233754` for tapered mixing, and `0.3999999999983359` for sign-changing mixing at the
registered witness amplitude.

## 8. Result and authority boundary

The exact 21-profile universe has mixed global-completion classes:

```text
3  F01 controls: exact degree-one whole-sky diffeomorphisms
6  persistent controls: sampled regular degree-one maps, not global proofs
12 tapered/sign-changing controls: blocked at the supplied center, no repair
```

No current eligible control displays a sampled fold, caustic, missing endpoint, parity reversal,
or repeated branch. This does not refute those structures in the complete UDT solution space. It
shows only that the current weak, center-smooth controls do not reveal them and that most of the
historical finite-path profile ensemble was never a complete-sky metric family.

The physical global metric branch, endpoint/profile, scale, source, detector, branch-combination
law, `X_max`, bootstrap closure, action, and native matter source remain `OPEN_NO_OWNER`.

## 9. Next justified gate

Do not insert survey structure yet. First obtain or derive a globally regular complete metric
profile family with the center, angular sector, mixing, and endpoint all defined. Then repeat this
same whole-sky atlas without choosing a branch by desired appearance. Only after its topology and
critical structure are typed should source ensembles enter, including luminous-survey tracers and
separately bracketed unresolved matter.

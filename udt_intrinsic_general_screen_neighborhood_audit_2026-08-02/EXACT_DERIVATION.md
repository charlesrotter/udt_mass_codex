# Exact derivation — intrinsic reciprocal projector in a general-screen neighborhood

## Scope

This is an exact, CPU-only, off-shell configuration-space audit in one chosen stationary complete
`R x S3` arena. The metric contains the founded reciprocal pair, one registered depth profile, and a
positive angular screen with all three symmetric metric modes. The `S3` completion, stationarity,
profiles, and `epsilon=1/10` are existence controls, not selected physics.

The post-review interpretation guards in `PREREGISTRATION_SCOPE_CLARIFICATION.md` are binding. In
particular, the open-neighborhood statement below is relative to the stationary block-screen
subspace retaining `K=partial_t`.

## 1. The screen really has three independent metric modes

Write

```text
g_screen = u^lambda V M,
M = [[r^2, r b],
     [r b, b^2+r^(-2)]].
```

Exact algebra gives

```text
det(M)=1,
det(g_screen)=u^(2 lambda) V^2.
```

At the isotropic parent `(V,r,b)=(1,1,0)`, the three metric tangents are

```text
d_V(VM) = [[1,0],[0,1]],
d_r(VM) = [[2,0],[0,-2]],
d_b(VM) = [[0,1],[1,0]].
```

Their exact rank is three. Thus `V` is the area mode and `r,b` are the two independent shears. The
local screen-frame rotation is `O(2)` gauge and is not a fourth metric amplitude.

The pair block in `(dt,sigma3)` is

```text
[[-1/u, -a/u],
 [-a/u, u-a^2/u]],
```

whose determinant is exactly `-1`. Therefore every registered finite `u`, positive `V`, and
positive `r` gives a nondegenerate Lorentzian four-metric independently of the shear and of `a`.
`V=0` is a genuine degeneration and is never inverted.

## 2. Configuration-level depth/area two-form

The oriented screen-coframe determinant is

```text
D=u^lambda V,
sigma=log(D/D0),
phi=(1/2)log(u).
```

Therefore

```text
dphi wedge dsigma
  = dphi wedge dlog(V)
  = (du wedge dV)/(2 u V).
```

The shear amplitudes cancel from `D`; they affect the complete curvature but not this determinant
identity directly. For the 18 preregistered candidates the exact configuration-level census is

```text
10 ZERO_IDENTICALLY,
 7 NONZERO_SIMPLE_OPEN_DENSE_WITH_ZERO_LOCUS_RETAINED,
 1 UNDEFINED_METRIC_DEGENERATE.
```

`NONZERO_SIMPLE` means a nonzero decomposable two-form. Its antisymmetric-matrix rank is two, not
one. Exact rational coefficients are nonzero at both preregistered points for every independent-area
candidate. Analyticity proves nonidentity and an open dense nonzero set, not global nowhere-vanishing.

At this stage the form is only a registered-configuration object. It becomes contact/metric
intrinsic only after the projector gate below.

## 3. Exact curvature-invariant Killing certificate

For each of the 17 nondegenerate metrics, compute

```text
I1=R,
I2=Ric_ab Ric^ab,
I3=Ric_a^b Ric_b^c Ric_c^a,
J=det[partial_(x,y,z)(I1,I2,I3)].
```

The production route uses an exact rational total-degree-three metric jet, exact formal inverse,
exact Christoffel and Ricci jets, and exact rational determinants. It evaluates both frozen points
for every candidate. All 32 point certificates belonging to the 16 nonhomogeneous metrics have
`J != 0` at both points. C14 has `J=0` at both points and is separately known to be homogeneous,
with a higher-dimensional spatial isometry algebra. C18 is degenerate and skipped.

Where `J != 0`, any Killing field annihilating the three invariants has zero spatial components.
No assumption about time-independent coefficients is made. The remaining possible field is

```text
X=f(t,x1,x2,x3) partial_t.
```

The exact residual Killing system has coefficient determinant

```text
2 g_tt^4 != 0,
```

so every derivative of `f` vanishes and only a constant multiple of `partial_t` remains. The line is
unique on the certified open set; analytic continuation fixes the global line on the connected
registered branch.

## 4. Metric-derived twist line and pair projector

Normalize the unique timelike Killing line to `T`. For nonzero `a`, its twist is globally nonzero
because the projected screen coefficient is proportional to

```text
a kappa u^(-1/2)/D,
```

with `kappa=-2`. The twist therefore supplies a metric-derived spacelike line `S`. Signs of `T` and
`S` disappear from the pair projector and the projected squared norms.

Exact first-Cartan projection gives

```text
Q_T=4 a^2/(u D^2),
Q_S=4 u/D^2,
Q=Q_S-Q_T=4(u-a^2/u)/D^2,
Phi_contact=(1/4)log(Q_S/Q_T)=phi-(1/2)log|a|.
```

The exact passive-Lorentz-frame control preserves the tensor contractions after reconstructing the
projector and rejects naive transformed-slot reuse. Constant rescaling of the unnormalized Killing
generator and independent sign choices leave the projector and squared norms unchanged.

The gate passes for 15 candidates. It does not pass for:

- C14: the homogeneous metric does not have a unique Killing line;
- C15: the Killing line is unique but its twist vanishes, so no ruler line follows;
- C18: the metric is degenerate.

Consequently the raw C14/C15 determinant entries are controls, not intrinsic contact two-forms.

## 5. Joined result

Exactly six candidates have both the intrinsic pair projector and a nonzero decomposable
depth/area form:

```text
C04, C08, C09, C10, C16, C17.
```

The central primary witnesses are C08-C10: all three screen modes are active, `a=1`, and each of the
three registered `lambda` values survives. Thus nonzero depth/area alternation is compatible with
the metric-derived reciprocal projector; the former zero result was a property of the slaved-area
screen, not a general metric no-go.

The controls remain informative:

- C11 (`V=u`) and C13 (constant `u`) retain an intrinsic projector but have zero alternating form;
- C14 loses intrinsic ownership through symmetry enhancement;
- C15 loses the ruler through zero twist;
- C16 has `Q=0` at `u=4` and `Q>0` above it;
- C17 has negative, zero, and positive `Q` strata across the registered `u` range;
- C18 is genuinely degenerate.

None is removed for failing to resemble desired physics.

## 6. Stationary open-neighborhood statement

At each parent `lambda`, the exact parent `J` is nonzero. `J` depends continuously on the metric
through its third jet. Therefore, **relative to the stationary block-screen subspace retaining
`K=partial_t`**, some unquantified `C^3` neighborhood of each parent retains the unique-Killing-line
certificate. The analytic area and shear profiles converge to the parent as their amplitudes tend to
zero, and `du wedge dV0` is exactly nonzero. Hence arbitrarily small independent area and shear
perturbations can coexist with the intrinsic projector and nonzero alternating form.

This does not apply to arbitrary time-dependent perturbations, does not quantify a radius, and does
not exhaust the smooth `GL(2,R)` function space. The explicit `epsilon=1/10` witnesses separately
certify concrete finite perturbations.

## 7. Independent evidence and guard classes

A fresh CPU coordinate/autodiff implementation replayed all 34 point jobs without importing
production functions. It reproduced all 32 nonzero exact determinants with worst relative error
`2.3392144311358414e-11`, the C14 zeros, and independent finite-difference anchors. Exact independent
algebra reproduced the determinant, tangent-rank, contact, alternating, and causal results.

The 30 preregistered failure mutations are typed honestly:

```text
19 exact-output or algebra guards,
 2 evidence-backed semantic guards,
 9 semantic scope guards.
```

The semantic guards prove that forbidden wording/state changes fail closed; they are not advertised
as 30 independent algebraic derivations.

## Maximum conclusion

The complete registered stationary screen can carry, simultaneously, a metric-derived reciprocal
projector, both shear modes, an independently varying angular area, and a nonzero intrinsic
depth/area two-form. This is a verified bounded existence and local-open result.

It does not select a screen profile or branch, supply an equation, make the configuration on shell,
derive a carrier/section, or determine an action, source, boundary, bootstrap value, density,
`X_max`, matter, mass, stability, or phenomenology.

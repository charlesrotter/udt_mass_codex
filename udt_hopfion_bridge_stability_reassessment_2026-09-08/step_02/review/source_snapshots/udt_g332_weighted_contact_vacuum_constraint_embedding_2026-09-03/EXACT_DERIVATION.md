# G332 exact derivation — weighted-contact vacuum-constraint embedding

Date: 2026-09-03
Scope: supplied G331 weighted-contact `S3` spatial metrics inside the active provisional vacuum
constraint arena

## 1. Bounded landing

```text
EXACT_IRREGULAR_WEIGHTED_CONTACT_VACUUM_CONSTRAINT_DATA_EXIST
__INITIAL_CONSTRAINTS_DO_NOT_FORCE_HOPF_ORBIT_RIGIDITY
__EXISTENCE_IS_NOT_A_FULL_K_CENSUS_OR_DYNAMIC_STABILITY
```

Status after fresh adversarial review and accepted repair-only follow-up:
`EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`.

G332 closes the exact boundary left by G331. The weighted-contact spatial metrics were already
smooth geometric configurations. They now receive an explicit smooth extrinsic curvature which
satisfies both active vacuum constraints. This is an initial-data existence theorem, not a
physical-data selector or a theorem about later-time orbit closure.

## 2. Active equation and constraint boundary

Universal Reciprocity/DDR and the two G312 premises are owner-adopted provisionally, not derived or
canonized. In their bounded regular metric-only vacuum arena,

```text
Ric(g_4) = Lambda g_4,                 d Lambda = 0
```

on each connected region. G315 derived the spacelike constraints

```text
R(gamma) + tau^2 - K_ij K^ij = 2 Lambda,
D_j(K^ij - tau gamma^ij) = 0,
tau = tr_gamma K.
```

No action, source, matter model, or new field equation enters G332.

## 3. Unit-Killing constraint lemma

Let `(Sigma,gamma)` be any smooth Riemannian three-manifold carrying a global unit Killing field
`xi`. Let `R` be the scalar curvature. Fix a real constant `C` and define the momentum tensor
with upper indices throughout the divergence calculation:

```text
P^ij = K^ij - tau gamma^ij
     = -C gamma^ij + b xi^i xi^j,
```

where `b` is any smooth scalar invariant along the Killing flow:

```text
xi(b)=0.
```

A Killing field is divergence-free. A unit Killing field is also geodesic because

```text
gamma(nabla_xi xi,Y) = -gamma(nabla_Y xi,xi)
                      = -(1/2)Y[gamma(xi,xi)] = 0.
```

Metric compatibility, constancy of `C`, and these identities give

```text
D_j P^ij
 = xi(b) xi^i + b (nabla_xi xi)^i + b xi^i div(xi)
 = 0.
```

Thus the complete momentum constraint is solved. The derivative of `b` has not been discarded: its
only contraction is exactly `xi(b)`.

The trace relation in three dimensions is

```text
tr(P) = -2 tau = -3C+b.
```

Therefore

```text
tau = (3C-b)/2,
K = ((C-b)/2) gamma + b xi_flat tensor xi_flat.
```

Here the unindexed `K` is the covariant tensor obtained by lowering both indices of the preceding
`K^ij`; correspondingly the vector product `xi^i xi^j` becomes
`xi_flat tensor xi_flat`. No vector/covector identification is being assumed.

The two eigenvalues of `K^i_j` are

```text
k_horizontal = (C-b)/2                 multiplicity 2,
k_vertical   = (C+b)/2                 along xi.
```

It follows directly that

```text
tau^2 - |K|^2 = (3C^2-2Cb-b^2)/2.
```

The Hamiltonian constraint is consequently the pointwise quadratic

```text
b^2 + 2Cb + 4Lambda - 2R - 3C^2 = 0,
```

or

```text
(b+C)^2 = 2(R+2C^2-2Lambda).
```

On the strict real stratum the two exact branches are

```text
b = -C +/- sqrt[2(R+2C^2-2Lambda)].
```

This formula is obtained from the constraint, not fitted to a metric profile.

## 4. Global smooth existence on a compact unit-Killing metric

On compact `Sigma`, `R` has a finite minimum `R_min`. For any fixed finite connected `Lambda`,
choose the free constant `C` so that

```text
C^2 > Lambda - R_min/2.
```

Then

```text
2(R+2C^2-2Lambda) > 0
```

everywhere. Its positive square root is smooth. Since every isometry preserves scalar curvature,
`xi(R)=0`; hence both branches have `xi(b)=0`. The lemma gives a globally smooth symmetric `K`
satisfying both constraints.

This proves existence for every smooth compact three-metric with a global unit Killing field, not
only for the sampled points used by the executables. It does not classify all possible `K` on such
a metric.

If the radicand reaches zero, the algebraic branches meet and a square root can lose smoothness.
That crossing stratum is retained as an open boundary. The strict inequality above avoids it
without a physical cutoff: `C` is free initial-data information, not a selected ruler.

## 5. Application to the complete G331 weighted family

G331 supplied, for every positive pair `(w1,w2)`, the global smooth metric

```text
gamma_w = dx^2/[4x(1-x)F] + [x(1-x)/F] zeta^2 + eta^2,
F = w1*x+w2*(1-x),
xi = w1 partial_phi1+w2 partial_phi2.
```

It directly established

```text
gamma_w(xi,xi)=1,
Lie_xi(gamma_w)=0,
Ric(gamma_w)^sharp xi = 2 xi.
```

Thus `xi` is simultaneously the global unit Killing field needed by Section 3 and the simple
metric-native Ricci eigenline in G331's gap-open near-Berger neighborhood. Because the construction
depends only on `gamma_w`, `R`, `xi`, one constant `C`, one fixed `Lambda`, and a sign, it is smooth
across the angular-coordinate axes where the global G331 metric is smooth.

For unequal weights, `R` is nonconstant. Then on the strict radicand stratum

```text
db = +/- dR/sqrt[2(R+2C^2-2Lambda)],
d tau = -(1/2) db.
```

The resulting `K` is generically nonconstant and non-pure-trace. The construction is therefore not
the homogeneous or pure-trace shortcut excluded by the preregistration. It retains a toric
symmetry because the G331 family itself is toric; it is not a classification of symmetry-free
nearby metrics.

Choose, for example,

```text
w1 = 1+sqrt(2)/n,
w2 = 1-sqrt(2)/n,                       integer n>=2.
```

Both weights are positive and their ratio is irrational. G331 proved that generic `xi` orbits are
then nonclosed and dense on invariant two-tori, with only the two axis orbits closed. Section 4
nevertheless constructs an exact smooth constraint-compatible `K`. Neither the momentum nor
Hamiltonian constraint asks for an orbit period, a circle quotient, or G330's fibre normalization.

Therefore the active constraints do not force Hopf-circle orbit rigidity at the initial-data
level.

## 6. Direct and independent exact evidence

`derive_weighted_constraint_embedding.py` rebuilds the weighted metric, its inverse, first and
second derivatives, Christoffels, Ricci tensor, and scalar curvature using exact rational
arithmetic in the interior chart. It represents the square root by an exact quadratic extension
and checks the trace inversion, direct coordinate momentum divergence, and Hamiltonian residual
for:

- five metric/radial samples, including equal- and unequal-weight controls;
- four fixed values of `Lambda`;
- both signs of `C`; and
- both square-root branches.

All 642 registered checks pass across 80 cases. Nonconstant unequal-weight scalar curvature and the
equal-weight constant-scalar control are checked separately.

`verify_weighted_constraint_embedding_independent.py` imports no production code and reads no
production result. It uses truncated Taylor-series arithmetic, adjugate metric inversion, and a
separate direct coordinate reconstruction. All 65 checks pass across 64 different cases.

`run_catch_proofs.py` catches nine hostile mutations: removal of connection terms, wrong square-root
coefficient, wrong trace inversion, wrong Hamiltonian norm sign, omitted `Lambda`, nonunit
projector, non-invariant `b`, nongeodesic direction, and promoted existence/census wording.

## 7. What the result does and does not say

G332 changes the status of one precise boundary:

```text
G331 weighted metrics: geometric configurations only
        ->
G332 weighted metrics: exact active-constraint initial data for explicit K
```

It does not show that the irregular Ricci flow remains irregular under evolution. It does not prove
linear or nonlinear stability, classify every extrinsic curvature, select a datum or topology,
or provide matter, mass, observation, scale, physical `X_max`, or canon.

The metric, reciprocal kernel, angular cancellation, and active provisional equation are unchanged.

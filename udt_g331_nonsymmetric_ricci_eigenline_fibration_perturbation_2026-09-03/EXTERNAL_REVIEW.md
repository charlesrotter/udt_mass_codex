# External Adversarial Review of Sealed G331 Intake

## Authentication and replay

I authenticated `/intake/REVIEW_SCOPE.json`, `/intake/REVIEW_MANIFEST.tsv`, and
`/intake/REVIEW_MANIFEST.sha256` before using any package content. The manifest seal matched the
manifest bytes, and all 39 listed payloads matched both recorded byte counts and SHA-256 digests,
including the sealed `sources/` subtree.

I then copied only `/intake/package` into a writable ephemeral directory
`/work/g331_review_20260903/package` and ran the four registered commands there:

```bash
python3 -S derive_nonsymmetric_eigenline.py --output DERIVATION_RESULT.json
python3 -S verify_nonsymmetric_eigenline_independent.py --output INDEPENDENT_VERIFICATION.json
python3 -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json
python3 -S verify_package.py --output PACKAGE_VERIFICATION_RESULT.json
```

All four passed. The regenerated JSON outputs in `/work/g331_review_20260903/package` were
byte-identical to the sealed JSON outputs in `/intake/package`.

## Primary finding

I do not find a refuting defect in the bounded G331 claim. The package correctly separates:

1. the `C2`-gap-open persistence of a metric-native Ricci rank-one eigenline near a non-round
   Berger `S3` metric, from
2. the non-openness of the closed Hopf-circle fibration and G330's period-normalized integer in the
   surrounding spatial metric space,

while keeping all active-equation consequences explicitly conditional on independently
constraint-compatible Cauchy data.

## Adversarial check-by-check assessment

### 1. Common-bundle comparison and regularity

This part is correct.

For nearby positive metrics `gamma` and `gamma_0`, the unique positive `gamma_0`-self-adjoint
bundle map `B` defined by `gamma(u,v)=gamma_0(Bu,v)` gives a typed comparison
`Ahat_gamma = B^(1/2) A_gamma B^(-1/2)` on one fixed `gamma_0`-Hilbert bundle. `Ahat_gamma` is
`gamma_0`-self-adjoint and pointwise similar to `A_gamma`, so it has the same spectrum. Since Ricci
depends on the metric through two derivatives, `gamma -> gamma_0` in `C2` implies
`Ahat_gamma -> A_0` uniformly in `C0`. If the operator perturbation norm stays below `Delta_0/2`,
the simple Berger eigenvalue remains separated from the double cluster by Weyl's bound, so the
Riesz projector onto that cluster has constant rank one globally on compact `S3`. The stated
two-derivative loss is also correct: `Ck` metric data give at best `C(k-2)` Ricci/projector
regularity, and smooth metrics recover a smooth line bundle.

### 2. `H1(S3;Z2)=0`

This part is correct and properly bounded.

Vanishing `H1(S3;Z2)` trivializes every real line bundle on `S3`, so once the rank-one Ricci
subbundle exists, a global nonzero section exists and can be unit-normalized. It does not choose a
sign. On connected `S3`, the two global unit representatives differ by the constant map `+-1`.
None of this implies closed leaves, common period, or a circle quotient.

### 3. Weighted contact metric and exact Ricci eigenline

This part survives independent rederivation.

Write `S3={(z1,z2) in C2 : |z1|^2+|z2|^2=1}`, `x=|z1|^2`, `eta_0=x dphi_1 + (1-x) dphi_2`,
`F=w1 x + w2(1-x)`, `eta=eta_0/F`, and
`xi = w1 partial_phi1 + w2 partial_phi2`, the smooth infinitesimal generator of
`(z1,z2) -> (e^{i w1 t} z1, e^{i w2 t} z2)`.

`F>0` for positive weights, so `eta` is globally smooth. Directly,

```text
eta(xi)=1,
d eta = F^{-2} dx ^ (w2 dphi_1 - w1 dphi_2),
i_xi d eta = 0.
```

Thus `xi` is the Reeb field of `eta`.

For the displayed metric, set

```text
e^1 = dx / (2 sqrt(x(1-x)F)),
e^2 = sqrt(x(1-x)/F) zeta,
e^3 = eta,
zeta = (w2 dphi_1 - w1 dphi_2)/F.
```

Then `g_w = (e^1)^2 + (e^2)^2 + (e^3)^2`, so positivity is immediate. The chart singularities at
`x=0,1` are only angular-coordinate singularities; the underlying objects `xi`, `F`, `eta`, and
the contact distribution are global and smooth.

The structure equations are

```text
d e^1 = 0,
d e^2 = kappa e^1 ^ e^2,
d e^3 = 2 e^1 ^ e^2
```

for a smooth scalar `kappa(x)`. Cartan's equations then give

```text
Omega_13 = e^1 ^ e^3,
Omega_23 = e^2 ^ e^3,
```

independently of `kappa`. Hence

```text
Ric(E_3,E_1)=Ric(E_3,E_2)=0,
Ric(E_3,E_3)=2,
```

where `E_3=xi`. So `xi` is an exact Ricci eigenvector with eigenvalue `2` for every positive
`w1,w2`. This is the key G331 geometric witness, and I do not find a defect in it.

### 4. Equal-weight Berger reduction and gap persistence

This part is correct.

If `w1=w2=w`, then `F=w` and

```text
g_(w,w) = H/w + eta_0^2 / w^2,
```

where `H = dx^2/(4x(1-x)) + x(1-x)(dphi_1-dphi_2)^2` is the standard horizontal round metric.
Given Berger radii `(a,c)`, choosing

```text
w = a^2/c^2,
mu = a^4/c^2
```

yields

```text
mu g_(w,w) = a^2 H + c^2 eta_0^2 = gamma_(a,c).
```

Since Ricci endomorphism eigenvalues scale by `1/mu` under constant homothety, the vertical
eigenvalue becomes `2/mu = 2 c^2 / a^4`, exactly matching G330.

At equal weights, the horizontal eigenvalue is `4w-2`, so the unscaled gap is `|2-(4w-2)|=4|1-w|`,
nonzero precisely for the non-round case `a != c`. The weighted family depends smoothly on
`(x,w1,w2)` on compact `S3`, so this nonzero gap remains open for sufficiently nearby unequal
weights.

### 5. Irrational flow and non-openness of circle fibration

This part is correct, and it does refute openness of the circle-fibration property in spatial
metric space.

The weighted Reeb flow is exactly

```text
(z1,z2) -> (e^{i w1 t} z1, e^{i w2 t} z2).
```

Each torus `|z1|^2=x`, `0<x<1`, is invariant. On such a torus, this is the standard linear flow of
slope `w1/w2`. If `w1/w2` is irrational, every torus orbit is nonclosed and dense in that torus.
The two coordinate axes remain exceptional closed circles. Because irrational ratios can be chosen
arbitrarily close to equal weights, arbitrarily close smooth metrics retain the exact Ricci
eigenline while losing the all-circle-fibre property. That is enough to show that Hopf-circle
fibration is not an open property of the nearby spatial metric space.

This does not by itself answer the narrower, still-open question on the constraint manifold. G331
states that limitation correctly.

### 6. Exact conformal bump

This part is correct.

For `g_epsilon = e^{2u} g_0`, `u=epsilon f`, the exact 3D conformal Ricci law is

```text
Ric(g_epsilon)
= Ric(g_0) - Hess(u) + du otimes du - (Delta u + |du|^2) g_0.
```

Choosing a compactly supported smooth bump with `f(p)=0`, `df(p)=0`, `Hess(f)(e_1,e_3)=1`,
`Delta f(p)=2` gives

```text
Ric(g_epsilon)(e_1,e_3) = -epsilon,
R(g_epsilon)(p) = R(g_0) - 8 epsilon.
```

So the old Berger vertical line is not preserved as an eigenline at `p`. The change is genuinely
nonhomogeneous, not a diffeomorphism artifact: Berger scalar curvature is constant, whereas the
bumped scalar curvature equals the Berger constant outside the support and differs at `p`, so it is
nonconstant. No diffeomorphic pullback of a constant-scalar homogeneous Berger metric can do that.

### 7. Period normalization and G330's integer

The package is correct to withhold G330's exact normalization.

G330's quantity depended on a common closed fibre length `ell_fibre` and the normalization
`eta_normalized = (2 pi / ell_fibre) alpha`. In the irrational weighted family, generic leaves have
no period at all, so there is no common `ell_fibre` to insert. One may choose other contact or
framing normalizations, but those are new invariants. They are not the same as G330's
period-normalized object and cannot be used to claim its perturbative survival.

### 8. Constraint boundary and dynamic statement

This is stated correctly and is one of the package's most important limits.

Neither the conformal bump family nor the weighted contact family is shown to lie on the active
vacuum constraint manifold with some extrinsic curvature. Therefore they are only spatial geometric
witnesses/counterfamilies. The local dynamic statement is valid only in the conditional form:
for any independently constraint-compatible smooth datum whose spatial metric lies in the gap-open
neighborhood, smooth local development preserves the rank-one cluster for some nonzero interval
while the gap stays open. G331 correctly drops G330's `U(2)`-symmetry inheritance and does not
promote any broken-symmetry fibration carry.

### 9. Chronology and fallback discipline

This is handled correctly.

The stronger weighted metric family was discovered after the broad candidate outcome had already
been preregistered. The package makes that chronology explicit and also records the right fallback:
if the weighted family failed external rederivation, the package would have to fall back to the
weaker preregistered line-field boundary rather than substitute another post hoc family. Since the
weighted family survives independent review, fallback is unnecessary, but the chronology disclosure
and fallback rule are scientifically appropriate.

### 10. Circularity, shared-code independence, hostile mutations, and overclaim audit

No blocking circularity defect was found.

The two main check scripts do not import each other and do not read each other's outputs. The
independent verifier uses a different exact arithmetic layer and separately reconstructs metric
inverse, Christoffels, Ricci tensor, and Ricci endomorphism. That is genuine code-path separation.
It is not absolute philosophical independence because the same weighted family ansatz is shared, but
that is not a hidden circularity by itself.

The hostile mutations are not uniformly deep. Several are mathematically substantive
gap/metric/projector/conformal/topology/orbit mutations, but a couple are only scope-flag flips
such as promoting constraint compatibility or common fibre period by fiat. Those weaker rows reduce
the value of the mutation suite as a standalone epistemic guard, but they do not overturn the
result because the external review and the exact derivations directly audit those boundaries.

I found no hidden carrier/action imports and no overclaim of occupancy, matter, mass, scale,
`X_max`, stability, or canon. The package repeatedly and correctly marks those as omitted/open.

## Residual risks

The remaining open risk is exactly the one the package says is open: whether the active vacuum
constraint manifold actually contains nearby nonsymmetric data whose spatial Ricci eigenline has the
irregular orbit structure exhibited by the weighted family, or whether the constraints impose an
additional rigidity not seen in spatial metric space alone. G331 does not overclaim this bridge.

## Conclusion

The bounded G331 landing withstands a fresh zero-context adversarial review. The common-bundle
spectral argument is sound, the topology/sign statement is properly limited, the conformal bump
correctly shows that the old Berger direction can tilt under a genuine nonhomogeneous perturbation,
the weighted contact family is a valid exact spatial-metric counterfamily with Ricci eigenvalue `2`
along its weighted Reeb field, irrational nearby weights destroy circle-fibration openness in the
ambient spatial metric space, G330's period normalization is genuinely unavailable there, and the
dynamic statement remains correctly conditional on independently constraint-compatible data.

ACCEPT__G331_BOUNDED_EIGENLINE_FIBRATION_BOUNDARY

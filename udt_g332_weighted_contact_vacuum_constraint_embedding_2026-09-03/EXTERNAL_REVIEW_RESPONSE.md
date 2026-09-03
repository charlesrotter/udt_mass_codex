# External Adversarial Review: G332

## Authentication and replay

I treated `/intake` as sealed read-only evidence and used `/work/g332_intake.VVuNoW` as the only writable replay area.

Authentication results:

- `REVIEW_MANIFEST.sha256` matches `REVIEW_MANIFEST.tsv` exactly:
  `54eb8000e0bbbcab4bec4b6fd8158a63f9163766379b9a2d7538ff095dde95cf`.
- `REVIEW_SCOPE.json` matches the manifest entry exactly:
  `fde699589ea725f0f02ef8d03c9ec67b800eac180754618ec5027989072e076b`.
- All 40 manifest payloads exist, match their listed sizes, and match their listed SHA-256 digests.
- `verify_review_intake.py` passes on the copied intake.

Registered replay results in the writable copy:

- `derive_weighted_constraint_embedding.py`: pass, `642` checks, `80` cases.
- `verify_weighted_constraint_embedding_independent.py`: pass, `65` checks.
- `run_catch_proofs.py`: pass, `9` substantive mutations caught.
- The three regenerated JSON outputs are byte-identical to the sealed outputs.

One registered command does not replay cleanly as shipped:

- `verify_package.py` fails in the sealed intake and in the raw copy with `AssertionError: source_S01_exists`.
- Cause: `SOURCE_MANIFEST.tsv` stores source paths relative to the source subtree root, but `verify_package.py` resolves them against `ROOT.parent` instead of `ROOT.parent / "sources"`.
- After an ephemeral path shim in `/work` only, `verify_package.py` passes with `84` aggregate gates. This is a packaging/replay defect, not a mathematical defect, but it is real and should be repaired.

## Primary findings

### 1. The constrained existence witness is mathematically valid

I do not find a sign error, hidden `db` drop, wrong-branch omission, or existence-to-classification promotion in the core derivation once it is stated with consistent tensor types.

Write the momentum tensor with upper indices for the momentum equation:

\[
P^{ij}=K^{ij}-\tau \gamma^{ij}=-C\gamma^{ij}+b\,\xi^i\xi^j,
\qquad \tau=\operatorname{tr}_\gamma K.
\]

Because `dim Sigma = 3`,

\[
\operatorname{tr}_\gamma P=\tau-3\tau=-2\tau.
\]

Also, since `|\xi|_\gamma=1`,

\[
\operatorname{tr}_\gamma P=-3C+b.
\]

Hence

\[
\tau=\frac{3C-b}{2},
\qquad
K^{ij}=P^{ij}+\tau\gamma^{ij}
=\frac{C-b}{2}\gamma^{ij}+b\,\xi^i\xi^j.
\]

Equivalently in covariant form,

\[
K=\frac{C-b}{2}\gamma+b\,\xi^\flat\otimes\xi^\flat.
\]

This is the correct three-dimensional trace inversion.

### 2. The momentum derivation survives the hostile `db` attack

With `C` constant,

\[
D_jP^{ij}=D_j(b\xi^i\xi^j)
=(D_j b)\xi^j\xi^i+b(D_j\xi^i)\xi^j+b\xi^i D_j\xi^j.
\]

So

\[
D_jP^{ij}=\xi(b)\xi^i+b(\nabla_\xi\xi)^i+b\,\xi^i\operatorname{div}\xi.
\]

Nothing was discarded. The `db` term is present and contracts to `\xi(b)`.

For a Killing field, `div xi = 0`. For a unit Killing field,

\[
g(\nabla_\xi\xi,Y)=-g(\nabla_Y\xi,\xi)
=-\frac12 Y[g(\xi,\xi)]=0,
\]

so `\nabla_\xi\xi=0`.

The remaining point is `\xi(b)=0`. Here

\[
b=-C\pm \sqrt{2(R+2C^2-2\Lambda)},
\]

so `b` is a smooth function of the scalar curvature `R` alone. Scalar curvature is invariant under isometries, hence `\xi(R)=0`, so `\xi(b)=0`.

For the specific weighted metric this is also visible directly: all metric coefficients depend only on `x`, `b=b(x)`, and `\xi=w_1\partial_{\phi_1}+w_2\partial_{\phi_2}` has no `x`-component, so `\xi(b)=0` without any hidden cancellation.

### 3. The Hamiltonian quadratic and both branches are correct

In an orthonormal frame adapted to `\xi`, the eigenvalues of `K^i{}_j` are

\[
k_h=\frac{C-b}{2},\frac{C-b}{2},
\qquad
k_v=\frac{C+b}{2}.
\]

Therefore

\[
\tau=\frac{3C-b}{2},
\qquad
|K|^2=2\left(\frac{C-b}{2}\right)^2+\left(\frac{C+b}{2}\right)^2
=\frac{3C^2-2Cb+3b^2}{4}.
\]

Hence

\[
\tau^2-|K|^2
=\frac{3C^2-2Cb-b^2}{2}.
\]

Substituting into

\[
R+\tau^2-|K|^2=2\Lambda
\]

gives

\[
b^2+2Cb+4\Lambda-2R-3C^2=0.
\]

Equivalently,

\[
(b+C)^2=2(R+2C^2-2\Lambda).
\]

Thus on the strict real stratum,

\[
b=-C\pm \sqrt{2(R+2C^2-2\Lambda)}.
\]

Both square-root branches are genuine algebraic branches. Neither may be discarded.

### 4. One finite global `C` exists for each fixed metric and fixed finite `Lambda`

For a fixed member of the G331 family, `S^3` is compact and `R` is continuous, so `R_min` exists.

If

\[
C^2>\Lambda-\frac{R_{\min}}{2},
\]

then

\[
R+2C^2-2\Lambda > 0
\]

everywhere, so the radicand is strictly positive globally. This gives one finite constant `C` on the whole manifold for one fixed finite connected `Lambda`.

This is a per-metric compactness argument. It is not a claim that one universal `C` works simultaneously for all positive weights, and the package does not need that stronger statement for its stated existence result.

### 5. Smoothness across the `S^3` axes is intact

The coordinate chart `(x,\phi_1,\phi_2)` is singular at `x=0,1`, but the inherited G331 objects are not:

- `\gamma_w` is globally smooth on `S^3`.
- `\xi` is a global smooth unit Killing field.
- `R` is a global smooth scalar.
- With strict radicand positivity, `b(R)` is a smooth scalar on all of `S^3`.

Then

\[
K=\frac{C-b}{2}\gamma+b\,\xi^\flat\otimes\xi^\flat
\]

is a global smooth tensor because it is built from global smooth tensors and scalars. No new axis singularity is introduced by the construction.

### 6. Scope discipline is preserved

The result is an initial-data existence witness only. It does not justify claims about:

- full classification of all smooth symmetric `K`;
- local or global evolution of the irregular Ricci-eigenline flow;
- stability;
- occupancy, matter, mass, observation, scale, `X_max`, or canon.

On this point the package is materially honest.

## Additional adversarial observations

### A. Notation should be tightened

The prose alternates between covariant and contravariant versions of `P` and between `\xi\otimes\xi` and `\xi^\flat\otimes\xi^\flat`. The mathematics is recoverable and the code uses the right typed objects, but the written derivation should state one index convention explicitly at the start of the momentum calculation.

### B. The independence claim is acceptable but not absolute

The independent verifier does not import production code and does not read production results. That satisfies the package's stated independence gate.

Still, both implementations rebuild the same coordinate metric and test the same witness family. So this is legitimate implementation separation, not theorem-level independence from the shared ansatz. The package mostly acknowledges that, and I do not treat it as a refutation.

### C. The hostile mutation suite is useful but not sufficient by itself

The substantive mathematical mutations are meaningful. Two checks are only scope-string guards. That weakens the mutation suite as a standalone quality signal, but not the derivation itself, because the key scope boundaries were separately checked in the analytic review.

## Independent spot checks outside packaged scripts

I also ran separate ad hoc exact-coordinate spot checks, without importing package code, on unsampled cases including axis-adjacent interior points such as `x=1/100` and `x=99/100`. Those checks again gave:

- `|\xi|^2 = 1`,
- momentum residual `0`,
- Hamiltonian residual `0`.

These do not replace the analytic proof, but they are consistent with it.

## Bottom line

The bounded mathematical landing survives hostile review: for each fixed G331 positive-weight metric and each fixed finite connected `Lambda`, one can choose a finite global `C` so that both algebraic branches produce a smooth symmetric extrinsic curvature solving the active provisional vacuum constraints. The construction applies in particular to unequal irrational weights from the G331 irregular-flow subfamily. I do not find a valid refutation of the constraint witness itself.

The sealed replay package does require repairs because one registered verifier is broken in the intake layout and the prose should clean up its tensor typing. Those are repairable packaging/presentation defects, not failures of the bounded existence result.

ACCEPT_WITH_REPAIRS__G332_SCIENTIFIC_LANDING_RETAINED

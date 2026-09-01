# External Review Response — G318

Date: 2026-09-01
Reviewer mode: fresh zero-context adversarial review
Intake inspected: `/intake` only

## Scope compliance

I inspected only the sealed intake, copied it to `/work/g318_review_1` for writable replay, ran the four registered commands there, and did not access any repository, protected package, web resource, or unsealed observation.

## 1. Authentication

- `REVIEW_MANIFEST.sha256` records `REVIEW_MANIFEST.tsv` at SHA-256 `226c20ae969c3f29c5fe9745db36191921cba7ac9030412fdd01e970d6142ee2`, and the actual file matches.
- `REVIEW_SCOPE.json` hashes to the manifest-listed SHA-256 `f31f9bf37b1d2d86fc3919466b2e19af05afabd86e4cc800c14453f28f8d6ef4`.
- All 33 manifest-listed payloads matched both recorded byte count and recorded SHA-256.
- I found no missing payload, mismatched payload, or broken manifest chain.

## 2. Replay in writable copy

Registered commands from `package/REPLAY_COMMANDS.txt`:

```text
python3 derive_nonconstant_psi_family.py
python3 verify_independent.py
python3 run_catch_proofs.py
python3 verify_package.py
```

Replay results in `/work/g318_review_1/package`:

- `derive_nonconstant_psi_family.py`: 14,043 assertions, 4 center witnesses, 16 atlas rows.
- `verify_independent.py`: PASS, 4,440 assertions, 27 Weyl instances.
- `run_catch_proofs.py`: PASS, 48/48 hostile mutations caught.
- `verify_package.py`: PASS_INTERNAL__EXTERNAL_REVIEW_REQUIRED.

Generated-file comparison against sealed artifacts:

- `DERIVATION_RESULT.json`: byte-identical.
- `BRANCH_ATLAS.tsv`: byte-identical.
- `INDEPENDENT_VERIFICATION.json`: byte-identical.
- `CATCH_PROOF_RESULT.json`: byte-identical.
- `PACKAGE_VERIFICATION_RESULT.json`: byte-identical.

I therefore accept that the sealed artifacts are reproducible from the sealed source package.

## 3. Independent derivation of the branch

I rederived the load-bearing formulas from the G315 constraints and G316 conformal bookkeeping.

Seed data in the registered slice:

\[
\bar\gamma_{ij}=\delta_{ij},\qquad \psi=\psi(x)>0,\qquad
\bar A_{TT}^{ij}=\operatorname{diag}(\alpha,-\alpha/2+d,-\alpha/2-d),\qquad
W=w(x)\partial_x.
\]

With `u=w'`, the flat longitudinal operator gives

\[
(\bar LW)^{ij}=\operatorname{diag}(4u/3,-2u/3,-2u/3).
\]

Defining `v=3\alpha/2+2u`, the total conformal tracefree tensor becomes

\[
\bar A_{TT}+\bar LW=\operatorname{diag}(2v/3,-v/3+d,-v/3-d),
\]

with norm

\[
|\bar A_{TT}+\bar LW|^2=\frac23 v^2+2d^2.
\]

Because the seed is flat and everything depends only on `x`, the vector constraint reduces exactly to

\[
\partial_x(2v/3)=\frac23\psi^6\tau'
\quad\Longrightarrow\quad
v'=\psi^6\tau'.
\]

For the constant-ratio separable branch `v=k\psi^6\tau`,

\[
k\psi^6\tau'+6k\psi^5\psi'\tau=\psi^6\tau',
\]

so

\[
(k-1)\tau'+6k\frac{\psi'}{\psi}\tau=0.
\]

Two consequences follow.

- If `k=1`, then `6\psi^5\psi'\tau=0`. On the declared sign-definite nonzero branch, any genuinely nonconstant `psi` has `\psi'\neq 0` somewhere, so the unchanged G317 form is obstructed.
- If `k\neq 1`, integration gives

\[
\tau=C\psi^n,\qquad n=-\frac{6k}{k-1},\qquad k=\frac{n}{n+6},\qquad n\neq -6.
\]

Because `u=(v-3\alpha/2)/2`, periodicity of `w` forces `\langle u\rangle=0`, hence

\[
\alpha=\frac23\langle v\rangle,\qquad w'=\frac12(v-\langle v\rangle).
\]

This part of the landing is correct.

## 4. Physical reconstruction and scalar ODE

From G316,

\[
\gamma_{ij}=\psi^4\delta_{ij},\qquad
A^i{}_j=\psi^{-6}\operatorname{diag}(2v/3,-v/3+d,-v/3-d).
\]

Using `v=k\psi^6\tau` and `q=d\psi^{-6}` gives

\[
K^i{}_j=A^i{}_j+\frac13\tau\delta^i{}_j
=\operatorname{diag}\left(\frac{1+2k}{3}\tau,\frac{1-k}{3}\tau+q,\frac{1-k}{3}\tau-q\right).
\]

Substituting `k=n/(n+6)` yields

\[
K^i{}_j=\operatorname{diag}\left(\frac{n+2}{n+6}\tau,\frac{2}{n+6}\tau+q,\frac{2}{n+6}\tau-q\right),
\qquad q=d\psi^{-6},\qquad \tau=C\psi^n.
\]

That reproduces the claimed physical eigenvalue ratios exactly.

For the momentum constraint, the conformally flat metric `\gamma_{ij}=\psi^4\delta_{ij}` has `H=\psi'/\psi` and nonzero Christoffels

\[
\Gamma^x_{xx}=2H,\quad \Gamma^x_{yy}=\Gamma^x_{zz}=-2H,\quad
\Gamma^y_{yx}=\Gamma^z_{zx}=2H,
\]

plus the symmetric lower-index counterparts. Directly evaluating `D_j(K^{ij}-\gamma^{ij}\tau)=0` gives the only nontrivial component

\[
\left(\frac{n+2}{n+6}-1\right)\tau'
\left(6\frac{n+2}{n+6}-2\right)\frac{\psi'}{\psi}\tau=0,
\]

which vanishes identically after substituting `\tau'=n(\psi'/\psi)\tau`. This direct physical check agrees with the conformal branch and rules out a conformal-only circular pass.

For the Hamiltonian constraint, the spatial scalar curvature is

\[
{}^{(3)}R=-8\psi^{-5}\psi'',
\]

and

\[
K_{ij}K^{ij}
=\left[\left(\frac{n+2}{n+6}\right)^2+2\left(\frac{2}{n+6}\right)^2\right]\tau^2+2q^2.
\]

Hence

\[
{}^{(3)}R+\tau^2-K_{ij}K^{ij}-2\Lambda=0
\]

reduces to

\[
-8\psi''
+\frac{8(n+3)}{(n+6)^2}C^2\psi^{2n+5}
-2d^2\psi^{-7}
-2\Lambda\psi^5=0.
\]

Using the conformal scalar equation with `|\bar A|^2=\frac23v^2+2d^2` gives the same ODE. The production claim of exact conformal/direct agreement is correct.

## 5. Periodic obstruction and the `n=-2` center class

Integrating the scalar ODE over one marked period kills the `\psi''` term.

- For `n<-3`, `n\neq -6`, the coefficient `8(n+3)/(n+6)^2` is strictly negative.
- With `C\neq 0`, `\psi>0`, and `\Lambda\ge 0`, every remaining integral has nonpositive sign, and the `C^2` term is strictly negative.
- Therefore no positive periodic member exists in that power branch.

At `n=-3`, the `C^2` coefficient vanishes, leaving

\[
-2d^2\int\psi^{-7}dx-2\Lambda\int\psi^5dx=0.
\]

If `d` or `\Lambda` is nonzero with `\Lambda\ge 0`, this is impossible. If both vanish, the ODE becomes `\psi''=0`, so periodicity forces `\psi` constant. Thus the claimed `n\le -3` nonnegative-`\Lambda` obstruction is sound within the declared family.

For `n=-2`,

\[
\psi''=\frac{C^2}{16}\psi-\frac{d^2}{4}\psi^{-7}-\frac{\Lambda}{4}\psi^5.
\]

Multiplying by `8\psi'` and integrating gives the first integral

\[
I=-4(\psi')^2+\frac{C^2}{4}\psi^2+\frac{d^2}{3}\psi^{-6}-\frac{\Lambda}{3}\psi^6.
\]

A positive equilibrium `p` satisfies

\[
C^2p^8-4d^2-4\Lambda p^{12}=0.
\]

Linearizing at `p` gives

\[
\eta''+\omega^2\eta=0,\qquad
\omega^2=\frac{C^2}{4}-3d^2p^{-8}.
\]

So if `C^2p^8>12d^2`, then `\omega^2>0`, equivalently the potential has a strict local minimum at `p`. Because the vector field is smooth on `\psi>0`, a sufficiently small neighborhood of `p>0` stays inside `\psi>0`; the standard planar Hamiltonian center theorem then yields smooth finite-period positive nonconstant periodic orbits around `p`. This is a local existence statement only, which matches the package’s bounded wording.

For period alignment, if `\Psi(s)` solves the base `n=-2` ODE with parameters `(C_0,d_0,\Lambda_0)` and period `P`, then

\[
\psi(x)=\Psi(\kappa x),\qquad
(C,d,\Lambda)=(\kappa C_0,\kappa d_0,\kappa^2\Lambda_0)
\]

solves the same-form ODE, now with period `P/\kappa` in `x`. Choosing `\kappa=P/(2\pi)` yields a marked `2\pi` member. This is exact parameter covariance, not hidden physical scale selection, because the parameters scale with the coordinate reparameterization.

## 6. Spatial Ricci and initial Weyl tensors

For `\gamma_{ij}=\psi^4\delta_{ij}`, direct Christoffel reconstruction yields mixed spatial Ricci eigenvalues

\[
{}^{(3)}R^x{}_x=-4\psi^{-5}\psi''+4\psi^{-6}(\psi')^2,
\]

\[
{}^{(3)}R^y{}_y={}^{(3)}R^z{}_z=-2\psi^{-5}\psi''-2\psi^{-6}(\psi')^2.
\]

For Einstein data, the electric Weyl tensor is

\[
E^i{}_j={}^{(3)}R^i{}_j+\tau K^i{}_j-K^i{}_kK^k{}_j-\frac23\Lambda\delta^i{}_j.
\]

On the `n=-2` branch, `K^i{}_j=\operatorname{diag}(0,\tau/2+q,\tau/2-q)` with `\tau=C\psi^{-2}`, `q=d\psi^{-6}`. Substituting the ODE into `E^x{}_x` gives

\[
E^i{}_j=\operatorname{diag}(E_x,-E_x/2,-E_x/2),
\]

\[
E_x=4\psi^{-6}(\psi')^2-\frac{C^2}{4}\psi^{-4}+d^2\psi^{-12}+\frac{\Lambda}{3}
=-I\psi^{-6}+\frac43d^2\psi^{-12}.
\]

That confirms the claimed electric formula and its first-integral identity.

For the magnetic part, a direct covariant-curl calculation shows the antisymmetrized `C` terms cancel, while the `d` terms survive:

\[
\nabla_xK_{zz}-\nabla_zK_{xz}=4d\,\psi^{-3}\psi'.
\]

After the Levi-Civita density and orthonormal conversion factors from `\gamma_{ij}=\psi^4\delta_{ij}` are included, the only independent orthonormal component is

\[
B_{\hat y\hat z}=B_{\hat z\hat y}=-4d\frac{\psi'}{\psi}\psi^{-8}.
\]

Consequences:

- If `d=0`, then `B=0`, but on sufficiently small nonconstant center orbits one has `I>0`, so `E_x=-I\psi^{-6}\neq 0`.
- If `d\neq 0`, any nonconstant periodic orbit has `\psi'\neq 0` somewhere, so `B` is nonzero somewhere.

Thus the registered periodic witness family has nonzero initial Weyl tide, exactly as claimed.

## 7. Adversarial checks and failure search

- I found no bad conformal powers. The exponents `-10`, `-12`, `-7`, `5`, and `6` are the standard three-dimensional conformal weights from G316, and the G318 reductions use them consistently.
- I found no sign error in the obstruction argument, the `n=-2` center linearization, the direct Hamiltonian reduction, or the Weyl formulas.
- I found no hidden promotion of the slice into a general theorem. The package repeatedly confines itself to the positive, sign-definite, constant-ratio, flat marked-`T^3`, diagonal-TT, one-coordinate family and explicitly leaves nonseparable, sign-changing, nonflat, nondiagonal, multidimensional, and global sectors open.
- I found no circular dependence in the executable checks. `verify_independent.py` does not import `derive_nonconstant_psi_family.py` and does not read `DERIVATION_RESULT.json`; it rebuilds Christoffels, Ricci, constraints, and Weyl tensors by separate index loops. All five Python scripts use only standard-library modules.
- The hostile-catch suite presently rejects the load-bearing coefficient, sign, and power mutations I would most worry about. The run record notes two earlier vacuous mutations were repaired before sealing; in the sealed version I did not find a surviving load-bearing mutation that escaped.
- I did not rerun the separate repository regression claim (`214 passed, one known xfail`) because the review scope forbids repository access. I therefore do not use that statement as load-bearing evidence. The scientific landing does not depend on it.

## 8. Scope and provenance judgment

- `SOURCE_SCOPE.tsv` is bounded to nine declared sources and excludes the protected paths called out by the package verifier.
- The landing does not select a data member, history, topology beyond the chosen diagnostic slice, physical scale, source, matter/mass law, observation, population, bootstrap rule, or physical `X_max`.
- The report package itself contains no evidence of metric, kernel, angular-interface, or observational-interface modification; within the sealed-review scope, the “unchanged” claim is adequately supported as a bounded provenance/interface claim rather than a direct repository diff.

## Conclusion

Within its declared positive sign-definite constant-ratio flat marked-`T^3` diagonal-TT one-coordinate family, the sealed G318 package does establish all seven requested points. I found no scientific defect that forces downgrade or repair inside that bounded landing.

G318_ACCEPTED__NONCONSTANT_PSI_BRANCHING_AND_TIDAL_PERIODIC_FAMILY_UPHELD

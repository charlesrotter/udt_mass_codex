# External Review Response

## Authentication and execution record

- I authenticated the sealed intake first by running `python3 -S /intake/package/verify_review_intake.py --root /intake`. It returned `G330 sealed intake authentication PASS: 41 payloads; 43 files`.
- I then copied the intake to `/work/g330_intake` and ran the registered commands only in that writable copy.
- In the copy:
  - `derive_berger_hopf.py` passed with `39` checks.
  - `verify_berger_hopf_independent.py` passed with `40` checks.
  - `run_catch_proofs.py` passed with `8/8` hostile catches.
  - `verify_package.py` failed immediately at `source_exists_S01`.
- The failure is a real packaging defect, not a mathematical one. In [verify_package.py](/work/g330_intake/package/verify_package.py:153) the verifier reads `SOURCE_MANIFEST.tsv` and resolves each manifest row as `REPO / row["path"]`. But [SOURCE_MANIFEST.tsv](/work/g330_intake/package/SOURCE_MANIFEST.tsv:2) lists paths such as `CURRENT_SCIENTIFIC_PREMISES.tsv` and `udt_g289_.../AUDIT_REPORT.md`, while the sealed intake stores those files under `/sources/...`. So the registered aggregate verifier is not self-contained under the copied sealed tree exactly as the review instructions require.

## Findings

1. The bounded scientific landing survives adversarial review, but only conditionally and locally, exactly as bounded in the request. I found no fatal defect in the Berger-Ricci derivation, intrinsic eigenline construction, Hopf identification, normalized absolute helicity, or the nonselector controls.
2. The package has one concrete evidence defect: the registered aggregate verifier does not replay inside the copied sealed intake because `SOURCE_MANIFEST.tsv` omits the `sources/` prefix needed by `verify_package.py`.
3. Two wording repairs are still warranted even though they do not overturn the mathematics:
   - The orbit-period normalization should be stated intrinsically as `eta = (2pi / ell_fibre) alpha`, where `ell_fibre = ∮_fibre alpha`, rather than primarily through the Berger parameter `c`. The present formula is equivalent, but the intrinsic form makes generator independence immediate.
   - The local-persistence section should state more explicitly that it relies on the general imported Einstein-Cauchy existence/uniqueness/isometry-extension theorem, not on a theorem proved by the G321 package for Berger data specifically. The current writeup mostly says this, but the dependence should be maximally explicit.

## Detailed audit

### 1. Berger spatial Ricci spectrum and the G313 witness

Let

\[
\gamma_{a,c}=a^2(\sigma_1^2+\sigma_2^2)+c^2\sigma_3^2,
\qquad
e_1=X_1/a,\ e_2=X_2/a,\ e_3=X_3/c,
\]

with `[X_i,X_j]=2\varepsilon_{ijk}X_k`. Then

\[
[e_1,e_2]=\alpha e_3,\qquad [e_2,e_3]=\beta e_1,\qquad [e_3,e_1]=\beta e_2,
\]

where

\[
\alpha=\frac{2c}{a^2},\qquad \beta=\frac{2}{c}.
\]

Using the Koszul formula for the left-invariant orthonormal frame,

\[
2\langle \nabla_{e_i}e_j,e_k\rangle
=c_{ij}^k-c_{jk}^i+c_{ki}^j,
\]

the nonzero connection coefficients are

\[
\nabla_{e_1}e_2=\frac{\alpha}{2}e_3,\quad
\nabla_{e_2}e_1=-\frac{\alpha}{2}e_3,\quad
\nabla_{e_1}e_3=-\frac{\alpha}{2}e_2,\quad
\nabla_{e_2}e_3=\frac{\alpha-2\beta}{2}e_1,\quad
\nabla_{e_3}e_1=\frac{2\beta-\alpha}{2}e_2,\quad
\nabla_{e_3}e_2=\frac{\alpha-2\beta}{2}e_1.
\]

From these,

\[
\operatorname{Ric}^{(3)}
=\operatorname{diag}\!\left(\alpha\beta-\frac{\alpha^2}{2},
\alpha\beta-\frac{\alpha^2}{2},
\frac{\alpha^2}{2}\right).
\]

Substituting `alpha, beta` yields

\[
\lambda_h=\frac{4}{a^2}-\frac{2c^2}{a^4},
\qquad
\lambda_v=\frac{2c^2}{a^4},
\qquad
{}^{(3)}R=\frac{8}{a^2}-\frac{2c^2}{a^4}.
\]

Hence

\[
\lambda_v-\lambda_h=\frac{4(c^2-a^2)}{a^4},
\]

so the vertical eigenspace is simple exactly for `a!=c`.

At the registered witness `(a,c)=(1,3/2)`,

\[
(\lambda_h,\lambda_h,\lambda_v)=(-1/2,-1/2,9/2),\qquad {}^{(3)}R=7/2,
\]

and with `K=h\gamma`,

\[
{}^{(3)}R+K^2-K_{ij}K^{ij}={} ^{(3)}R+6h^2.
\]

Setting `h^2=5/12` gives `7/2+6(5/12)=6=2\Lambda` at `\Lambda=3`. So the G313 datum is a genuine constraint-compatible nonround Berger witness.

I found no hidden imported structure here.

### 2. Is the simple Ricci eigenspace intrinsic?

Yes, on the nonround stratum only.

For `a!=c`, define

\[
P=\frac{\operatorname{Ric}^{(3)}-\lambda_h I}{\lambda_v-\lambda_h}.
\]

This is a tensorial polynomial in the `(1,1)` Ricci endomorphism, so it is independent of a chosen component frame. Under an orthonormal frame change `O`, the matrix of `P` conjugates as `P \mapsto OPO^T`; under a diffeomorphism it pushes forward naturally with the Ricci endomorphism. Therefore `\operatorname{im}(P)` is an intrinsic unoriented line field on the nonround Berger stratum.

This does not survive the round case. When `a=c`, the eigengap vanishes and `P` is undefined. That is the correct behavior, not a defect: the round metric selects no line.

I do not see a hidden framing assumption in the nonround claim.

### 3. Are the leaves really the Hopf fibration, and is the normalization intrinsic?

Yes.

The vector field `X_3` is a Lie algebra generator of `SU(2) ~= S^3`. Its flow is right multiplication by the one-parameter subgroup `\exp(tX_3)`, which is a closed `U(1)` subgroup with period `2pi` in the bracket normalization `[X_i,X_j]=2\varepsilon_{ijk}X_k`. Thus each orbit is a circle, and the orbit space is the homogeneous quotient `SU(2)/U(1) ~= S^2`. This `S^2` is not imported as a carrier; it appears only after the line field is already determined.

For the unit representative `V = \pm X_3/c`, the metric dual is

\[
\alpha = \gamma(V,\cdot)=\pm c\,\sigma_3.
\]

Each fibre has metric length

\[
\ell_{\mathrm{fibre}}=\oint_{\mathrm{fibre}}\alpha = 2\pi c.
\]

So the intrinsic normalized connection form is

\[
\eta=\frac{2\pi}{\ell_{\mathrm{fibre}}}\alpha=\pm \sigma_3.
\]

This is the same normalization used in the package, just written without privileging the symbol `c`.

With the unit-curvature `S^3` convention,

\[
d\sigma_3=-2\sigma_1\wedge\sigma_2,
\qquad
\int_{S^3}\sigma_1\wedge\sigma_2\wedge\sigma_3=2\pi^2.
\]

Therefore

\[
\frac{1}{4\pi^2}\int_{S^3}\eta\wedge d\eta
=\frac{1}{4\pi^2}\int_{S^3}\sigma_3\wedge(-2\sigma_1\wedge\sigma_2)
=-1
\]

in the frozen orientation, so the absolute value is `1` for every positive nonround Berger pair.

This normalization is intrinsic. It depends only on the metric fibre length of the selected circle action, not on a transported external target or a chosen frame component.

### 4. Reversal, orientation, homothety, and round degeneration

These checks pass.

- Replacing `V` by `-V` sends `eta` to `-eta` and `deta` to `-deta`, so `eta \wedge deta` is unchanged.
- Reversing the spatial orientation changes the sign of the integral, but not its absolute value.
- Under a common homothety `(a,c)\mapsto (sa,sc)`, the eigengap scales like `s^{-2}` while `eta=(2pi/\ell_f)\alpha` is unchanged because both `alpha` and `\ell_f` scale by `s`. So the normalized absolute helicity remains `1`.
- At `a=c`, the integral can still be computed for any separately supplied Hopf field, but the metric no longer selects a unique line. The package respects this boundary correctly.

### 5. Local persistence audit

This part is conditional, but acceptable as stated once the dependence is made explicit.

The argument has two ingredients.

First, the Berger datum `(gamma_{a,c},K=h\gamma_{a,c})` is `U(2)`-invariant. If one assumes the standard imported local Einstein-Cauchy existence/uniqueness theorem in the marked category, then any initial-data isometry extends to an isometry of the local development by the usual uniqueness argument. That is enough to preserve the `U(2)` symmetry locally. In a Gaussian presentation near the initial slice, the induced spatial metrics therefore remain in Berger form

\[
\gamma(t)=a(t)^2(\sigma_1^2+\sigma_2^2)+c(t)^2\sigma_3^2.
\]

Second, because `a(0)!=c(0)` and `a(t),c(t)` are smooth, continuity alone gives an `epsilon>0` such that `a(t)!=c(t)` for `|t|<\epsilon`. So the simple eigenspace persists on a nonzero open interval. No additional field equation or transport law is needed.

What this does not prove:

- any persistence beyond gap closure;
- any nonsymmetric perturbative stability;
- any global conservation law;
- any theorem if the imported local Einstein-Cauchy machinery is rejected.

Within those bounds, I do not find a hidden transport assumption.

### 6. Does this close part of G289/G305/G306 without reviving the old `L2+L4` claim?

Yes, but only a bounded part.

It closes the specific nonround-Berger gap left open by G289 and G306: on this admitted stratum the metric itself selects an intrinsic Hopf line, so one no longer needs a fixed target `S^2`, supplied carrier field, or raw frame component to produce the geometric Hopf object.

It does not revive the historical stability claim. Nothing here variationally perturbs an independent `S^3\to S^2` matter field with the old `L2+L4` functional. The package is correct to refuse that transfer.

It also does not close the round-member-selection problem from G306. The round metric still selects no line.

### 7. Universal history or occupancy selection

The package correctly blocks this overclaim.

The adopted equation admits at least:

- the nonround Berger `S^3` datum discussed here;
- the round positive `S^3` history, where no line is selected;
- other admitted topologies already registered in the intake, including `T^3` controls and the `S^1\times S^2` positive product witness from G313.

So the Hopf line is at most a history discriminator on one admitted branch. It is not a universal selector, occupancy rule, or unique-history theorem.

### 8. Circularity, reused formulas, vacuous tests, and hidden assumptions

My audit result is mixed but acceptable.

- The core mathematics is not circular. The Ricci spectrum, projector, and normalized integral can all be rederived directly from the metric and Lie brackets without using the package outputs.
- The hostile tests are real for the three main scripts.
- The aggregate package verifier is defective as a replay artifact because of the broken source-manifest path resolution described above.
- The period normalization is mathematically fine, but the presentation should make its intrinsic form explicit to eliminate any appearance of parameter dependence.
- The persistence claim is not a machine proof of a new PDE theorem. It is a conditional application of imported local Einstein-Cauchy theory plus a continuity argument. The package should continue to say that plainly.
- I found no hidden import of an `S2` carrier, action, transport law, source, matter model, observation, fit, scale, history selector, population rule, physical `X_max`, or unregistered field equation.

## Referee conclusion

As a bounded mathematical claim, G330 succeeds. On the declared constraint-compatible nonround Berger-`S^3` Cauchy-data stratum, the spatial metric defines an intrinsic simple Ricci eigenline; that line is the Hopf fibration; the period-normalized absolute helicity is `1`; and, conditional on the imported local Einstein development theorem with isometry extension, the line persists on some nonzero local interval while the eigengap stays open.

I am not willing to give the stronger clean acceptance token because the sealed package still contains a registered self-verification defect, and the writeup should make the intrinsic normalization and imported-theorem dependence even more explicit. Those are repairable presentation/evidence issues, not a refutation of the bounded scientific landing.

ACCEPT_WITH_REPAIRS__G330_BOUNDED_SCIENTIFIC_LANDING_RETAINED

# External review response — G349

Date: 2026-09-04  
Role: fresh zero-context adversarial mathematical-relativity, Lorentzian geometric-measure, null-wavefront, caustic, and evidence-integrity review

## Scope and handling

I used the sealed `/intake` tree as the only evidentiary source. I did not access a repository, a protected package, the web, or any external scientific source; I made no download, installation, or network-capable Python call. I did not edit any evidence file or continue the research. After authentication, I copied the complete intake with preserved layout and metadata to `/work/g349_external_review.YOivmm` and ran every executable check from that copy. A separate dependency-free scratch reconstruction was placed at `/work/g349_external_review.YOivmm_scratch/scratch_reconstruction.py`, outside the copied evidence tree.

The question reviewed here is only the conditional finite metric geometry of the supplied endpoint map

\[
F(n)=\gamma_n(\tau(n))
\]

for a supplied smooth Lorentzian metric, source, compact sky patch, regular null-geodesic family, positive smooth cut, and optional orientations and labels. Nothing in this review chooses a spacetime, history, physical ray population, observer population, route, occupancy, matter model, scale, or physical transfer law.

## 1. Authentication and exact file set

Authentication was completed before scientific payloads were read.

- `REVIEW_SCOPE.json` SHA-256 is `86a36ec9ae0c6c31fcb9216a1d7194d2457871be8dd30313e687eeaeab0a5fe3`.
- `REVIEW_MANIFEST.tsv` SHA-256 is `c4fe70fd02e4f3da903e0c525e08a74e5c0e28615a0e92e03977c6ab174db4d0`.
- `REVIEW_MANIFEST.sha256` SHA-256 is `253becb352c06af9bf57b68f0f53b5fcfbc687dde09153bfdff4e5f33fa31aae`.
- The digest declared by `REVIEW_MANIFEST.sha256` exactly equals the independently computed digest of `REVIEW_MANIFEST.tsv`.
- The scope declares 31 payloads. Its ordered file list, the 31 manifest rows, and the payload count agree exactly; there are no duplicates or unsafe absolute/parent paths.
- Every one of the 31 payloads matches both its declared byte count and SHA-256.
- The complete intake contains exactly 33 regular files: the 31 declared payloads plus `REVIEW_MANIFEST.tsv` and `REVIEW_MANIFEST.sha256`. There are no undeclared files, missing files, symlinks, devices, sockets, or other special entries.
- The complete `/work` copy re-passed the manifest and every payload check. `/intake` re-passed after the review, establishing that the sealed evidence remained unchanged.

This establishes exact internal consistency against the supplied checksum chain. It does not establish authorship or chronology against an external trust anchor: the hashes are unkeyed, the manifest hash file is itself unsigned, and repository access was correctly prohibited.

## 2. Preregistration chronology and first hostile failure

The sealed record is internally consistent with the following chronology: commit `84cb5264` contained the outcome-unseen preregistration surfaces and three executable routes; production then reported `44314/44314`, the implementation-distinct route `14314/14314`, and the first hostile execution `20/21`. The sole recorded hostile miss was `call_every_rank_one_a_fold`, whose original implementation depended on a prose phrase. The repair replaced that hook with the explicit cusp test for

\[
(x,y)\mapsto(x,y^3+xy),
\]

and commit `134ecd4a` is recorded as the behavioral repair. The repaired hostile result is `21/21`. The run record separately discloses the first aggregate `13/18` documentary-hook failure and its later `18/18` result.

The exact preregistration and script hashes embedded in the aggregate match the authenticated files. The first failure is therefore recorded, not erased. However, `GIT_PREREGISTRATION_PROOF.txt` is a documentary transcript rather than Git object evidence or a signed remote receipt. Under the mandated repository prohibition I cannot independently prove that the commits were pushed before execution, nor can I rerun the unrepaired first hostile version. “Outcome unseen” is confirmed as the state asserted consistently by the sealed documents, not as externally authenticated temporal provenance.

## 3. Registered replay and executable-evidence audit

From the copied G349 directory I ran exactly:

```text
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -B -S verify_package.py
```

It exited successfully with `18/18`. The nested replays reproduced production `44314/44314`, implementation-distinct `14314/14314`, and hostile `21/21`. An independent wrapper hashed every regular file in the copied intake before and after; all bytes were unchanged and no bytecode appeared. Static AST inspection found only standard-library imports. The scientific scripts contain result-writing branches, but those branches are disabled by `UDT_NO_WRITE=1`; the aggregate only invokes the three local scripts with the active interpreter, `-B -S`, and the no-write environment.

The tolerances are not objectionably loose for the calculations performed. The algebraic tolerance `5e-10` is far above roundoff but all reported algebraic residuals are about `10^-13` or smaller. The finite-difference tolerance `3e-6` is conservative relative to the reported `6.65e-11`; the coarse complex-square quadrature tolerance `0.001` is narrowly met at `7.67e-4` and is accompanied by the registered greater-than-three refinement ratios.

The assertion totals materially overstate evidentiary breadth. Many assertions repeat the same elementary identity. Several hostile guards are literal text lookups or unconditional truths; production includes such checks as `rank_zero_point_retained = True`, and the independent route includes `isolated_crossing_noninjective_equality = True`. The hostile checker catches one-field mutations of its own frozen expectations, not adversarial mathematical countermodels. The aggregate largely authenticates hashes, result JSON, counts, and required phrases. The second numerical route is implementation-distinct, but it shares the same toy maps and mathematical premises and is not premise-independent. None of these are fatal because the theorem must stand analytically, but they are integrity/regression evidence rather than proof.

Most importantly, neither numerical route combines a rank-losing G348 Jacobi map with a nonconstant affine cut. The cut tests use a precaustic Minkowski cone, where the screen differential has full rank; the fold and complex-square tests are separate Euclidean smooth-map controls. That coverage gap is exactly where the mathematical defect below occurs.

## 4. Variable-cut differential and null-longitudinal cancellation

Let `v` be a sky tangent and `J_v` the source-vertex Jacobi field generated by varying the normalized initial direction at fixed affine parameter. Differentiation gives

\[
dF(v)=J_v(\tau)+d\tau(v)k(\tau).
\]

Set `f=g(J_v,k)`. The initial conditions give `f(0)=0` and

\[
f'(0)=g(DJ_v(0),k(0))=0
\]

because differentiating the null initial tangent gives orthogonality. Affine geodesicity, the Jacobi equation, and the curvature symmetries give `f''=0`. Hence `g(J_v,k)=0` along the ray. Since `g(k,k)=0`, for all `v,w`,

\[
g(dF(v),dF(w))=g(J_v,J_w).
\]

Thus `d\tau` contributes no term to the induced Lorentzian Gram matrix or its two-density. This part of G349 is correct. The cut still changes the endpoint and therefore changes the value of the Jacobi map at which the density is evaluated.

Pointwise, the quotient class of `dF(v)` is the quotient class of `J_v`. With source frequency normalized to one, that quotient differential is precisely the G348 source-to-target screen Jacobi map applied to the celestial tangent. Therefore the determinant of the positive quotient Gram form, relative to `d\Omega_u`, is the G348 metric directional two-Jacobian. No target-observer factor enters.

## 5. Required mathematical repair: ordinary rank is not screen rank

The derivation then makes a false inference: it says that every ordinary rank-two plane `dF(T_nU)` is spacelike “by” the Gram cancellation. The cancellation establishes positive semidefiniteness, not positive definiteness.

At a G348 rank-one conjugate direction, choose sky tangents `v,w` so that the quotient Jacobi map has

\[
[J_v]=0,\qquad [J_w]\ne0.
\]

Then `J_v=a k` for some scalar `a`. The smooth positive cut is arbitrary, so prescribe `d\tau(v)\ne-a`. At that point,

\[
dF(v)=(a+d\tau(v))k,
\]

while `dF(w)` has a nonzero screen class. Those two vectors are linearly independent, so the ordinary differential has rank two. Nevertheless their plane contains `k`, is null rather than spacelike, and has Lorentzian Gram determinant zero. The scratch reconstruction checks this explicitly in a Lorentz frame with `k=(1,0,0,1)` and a unit screen vector: ordinary rank is two, the auxiliary Riemannian Gram determinant is positive, and the Lorentzian Gram determinant is zero.

This counterexample is already licensed by the sealed G348 rank-one stratum and G349’s arbitrary smooth cut; it requires no new physical premise. It refutes these statements as written:

- “at every rank-two point the plane is spacelike”;
- `w_g>0` on every ordinary rank-two point;
- the identification of all ordinary rank-two points with the positive G348 screen metric;
- the implied equivalence between the ordinary rank strata of `dF` and the G348 quotient-screen rank strata.

The finite area result is repairable without adopting alternatives B, C, or D, but the repair is mathematically mandatory:

1. Define the screen rank

   \[
   r_s(n)=\operatorname{rank}\bigl(T_nU\xrightarrow{dF}k^\perp\to Q_k\bigr)
   =\operatorname{rank}[J(\tau(n))]
   \]

   separately from the ordinary rank `r_F=rank(dF)`. If `r_s=2`, the endpoint plane is spacelike and `r_F=2`. If `r_s=1`, then `r_F` may be one or two; the latter is a null two-plane. If `r_s=0`, then `r_F<=1`.

2. Define the Lorentzian two-Jacobian everywhere by the nonnegative semidefinite Gram determinant,

   \[
   J_gF=\sqrt{\det(g(dF_i,dF_j))/\det(s_u)},
   \]

   or equivalently by the quotient-screen determinant. It is positive exactly when `r_s=2` and zero when `r_s<2`, including ordinary-rank-two null points. Do not define its zero strata solely by ordinary rank.

3. Replace the assertion `w_g>0` on every ordinary rank-two plane by `w_g>=0` on the non-timelike planes forced by null Gauss orthogonality, with `w_g=0` on null planes and `w_g>0` only on spacelike planes.

4. Retype “critical strata.” The ordinary critical set `r_F<2` has zero auxiliary `H_h^2` image by the usual area formula. The screen-critical set `r_s<2` can include ordinary-rank-two null sheets of positive auxiliary `H_h^2`; those sheets instead have zero Lorentzian two-density because `w_g=0`. The existing proof wrongly uses the first statement as though it covered the second.

5. Add the mixed rank-one-caustic/nonconstant-cut witness above to the scientific and hostile checks. The current precaustic cut test cannot detect this issue.

These repairs preserve the intended nonnegative metric-area conclusion, but the sealed claim cannot accurately be described as needing no mathematical repair.

## 6. Auxiliary-Riemannian reduction and corrected area formula

On a spacelike ordinary-rank-two plane `P`, the stated ratio

\[
w_g(P)=\frac{\sqrt{\det(g|_P)}}{\sqrt{\det(h|_P)}}
\]

is basis independent, and `J_gF=w_gJ_hF`. My scratch calculation varied the positive auxiliary coefficients and recovered the same `J_gF`; the cancellation is genuine. At a null ordinary-rank-two plane the corrected ratio is zero, not positive.

The robust weighted area formula is

\[
\int_U J_gF\,d\Omega_u
=\int_M\sum_{n\in F^{-1}(y),\ r_F(n)=2}
w_g(dF_nT_nU)\,d\mathcal H_h^2(y).
\]

For countably rectifiable coincident sheets, approximate tangent planes agree at `H_h^2`-almost every point of positive overlap; transverse intersections are `H_h^2`-null. Consequently `w_g\,dH_h^2` gives an intrinsic density on spacelike sheet portions, independent of `h`, and vanishes on null portions. Define

\[
N_s(y)=\#\{n:F(n)=y,\ r_s(n)=2\}.
\]

Then the clean intrinsic statement is

\[
\mathcal A_{\rm mult}
=\int_UJ_gF\,d\Omega_u
=\int_{F(U)_{\rm sp}}N_s(y)\,dA_g(y).
\]

Equivalently, one may extend `dA_g` by zero to null rectifiable portions, but that convention must be explicit. Counting all ordinary-rank-two preimages in `N` is harmless only after this zero-weight convention; it obscures the exact G348 rank typing and should not be the primary definition.

## 7. Multiplicity, geometric union, and equality

With the corrected spacelike multiplicity, define

\[
\mathcal A_{\rm union}=\int_{F(U)_{\rm sp}}1\,dA_g.
\]

Then

\[
\mathcal A_{\rm mult}-\mathcal A_{\rm union}
=\int_{F(U)_{\rm sp}}(N_s-1)\,dA_g\ge0,
\]

and equality holds exactly when `N_s=1` for `dA_g`-almost every spacelike regular image point. This is a global preimage statement; the local Jacobian alone cannot recover union area.

The fold witness is correct: absolute sheet area is `2`, union area `1`, and signed integral `0`. The complex-square witness is also correct: the origin is rank zero, absolute sheet area is `2π`, union area `π`, and the signed determinant does not cancel. A transverse isolated meeting of two two-surfaces has zero two-area intersection, so noninjectivity at isolated points is compatible with equality. A coincident positive-area overlap gives genuine multiplicity. These smooth-map examples correctly test the area formula, but—as the package itself says—they do not prove that every polynomial normal form occurs for a null endpoint map.

Ordinary rank-one and rank-zero images have zero target two-area but must remain in the map because they can join sheets and affect topology and limiting multiplicity. Screen-rank-one/ordinary-rank-two null strata must also remain after the repair. The cusp calculation is correct and blocks the false assertion that every rank-one map singularity is a fold.

## 8. Orientation, observers, and labels

Absolute metric sheet density is nonnegative and orientation free. A signed quotient-screen determinant requires compatible supplied source and target screen orientations; it can change sign across a fold and describes an oriented sheet coefficient/current, not geometric union area. It vanishes on screen-critical strata. The package’s fold and complex-square sign distinctions are correct.

Finite source-observer covariance is also correct only for the same intrinsic ray set and endpoint assignment. If the same intrinsic tangent has frequencies related by `D=ω_v/ω_u`, then the G348 directional density and celestial solid angle transform by `D^2` and `D^-2`, respectively, so their product is invariant. When each observer renormalizes its generator to unit frequency, the affine parameter must transform inversely to that tangent rescaling. Explicitly, if `k_v=k_u/D`, then the cut representing the same endpoint is `τ_v=Dτ_u` (including its direction dependence). Holding the same numerical cut instead changes the endpoint map and is not a covariance comparison. Target observer changes only the quotient representative by an isometry.

Each supplied path label may be treated separately, and a declared disjoint-union domain has the mathematical census `N=Σ_ell N_ell`. No metric argument here selects labels or supplies occupancy, probability, or physical weights. Identically overlapping labelled sheets therefore have per-label area one, census two, and geometric union one, without implying equal physical contribution.

## 9. Scope and evidence-integrity conclusion

I found no imported optics, emission, detection, brightness, flux, luminosity, probability, observational-distance, field-equation, matter, mass, stability, scale, `X_max`, or canon premise in the analytic theorem. The result is general conditional Lorentzian geometry, not uniquely diagnostic of UDT. It concerns the image of a supplied endpoint map, not a populated wave, observed image, light bundle, or transfer process.

One documentary widening should be repaired: `CURRENT_RESEARCH_PROGRAM.md` describes the comparison as multiplicity-weighted area versus “physical image-union area.” The proved object is only geometric endpoint image-union area. Without an occupancy or transfer law, “physical” is not licensed and should be removed. The same caution applies to “wavefront” if it is read as an emitted or detected optical front rather than merely the supplied null endpoint map.

Subject to the five mathematical repairs in Section 5 and this documentary scope correction, the central finite conclusion survives: the G348 quotient-screen density integrates to spacelike sheet area with multiplicity; geometric union area additionally requires global preimage identification; isolated crossings, caustic strata, orientations, same-map observer covariance, and path-label census behave as stated. Because the present proof incorrectly identifies ordinary rank two with spacelike screen rank two, an unconditional no-repair acceptance is not warranted.

ACCEPT_WITH_CAVEATS_G349_FINITE_NULL_PATCH_AREA

# External Review Response

## Scope and authentication

I complied with the sealed scope in [REVIEW_SCOPE.json](/intake/REVIEW_SCOPE.json:2): I inspected only `/intake`, mirrored it to `/work/g341_review` before running any checks, and did not browse, download, install packages, or access any external repository.

Authentication passed.

- The detached seal in [REVIEW_MANIFEST.sha256](/intake/REVIEW_MANIFEST.sha256:1) matches the actual SHA-256 of [REVIEW_MANIFEST.tsv](/intake/REVIEW_MANIFEST.tsv:1): `1860832f56889b2ec0246e0dfb535525dc3fd6b6728b6ac63cfc9ba76c67fb53`.
- The scope file hash in [REVIEW_MANIFEST.tsv](/intake/REVIEW_MANIFEST.tsv:2) matches the actual SHA-256 of [REVIEW_SCOPE.json](/intake/REVIEW_SCOPE.json:1): `fab22d4eea96f1080aa8daf9a8dbb37b4f0cc0f91a291a775ab7b0c09fbe0bd4`.
- The manifest declares 30 payload rows plus the scope row; I verified every listed byte count and SHA-256 against the sealed intake, with no mismatches.
- The exact file set is consistent: 32 files total in `/intake` equals 30 payloads plus `REVIEW_SCOPE.json`, `REVIEW_MANIFEST.tsv`, and `REVIEW_MANIFEST.sha256`. The mirrored `/work/g341_review` tree matched that same 32-file set exactly.

## Findings

No findings at high, medium, or low severity overturn the bounded G341 result. I do not see a mathematical, causal-geometric, null-congruence, observer-pair, or evidence-integrity defect that forces rejection or narrowing beyond the limits the package already states.

## Review by question

### 1. Mixed endpoint integrals, derivatives, and determinant

The mixed endpoint formulas in [EXACT_DERIVATION.md](/work/g341_review/g341/EXACT_DERIVATION.md:22) are correct. From

\[
g=-dT^2+C_X^2T^{-2/3}dX^2+C_\perp^2T^{4/3}(dy^2+dz^2)
\]

with conserved spatial covector `(p_X,p_y,p_z)` and `p_\perp=\sqrt{p_y^2+p_z^2}`, the future null condition gives

\[
\omega(T)=\dot T=\frac{|p_X|}{C_X}T^{-2/3}\sqrt{T^2+\lambda^2},\qquad
\lambda=\frac{C_Xp_\perp}{C_\perp|p_X|}>0,
\]

so

\[
\frac{dX}{dT}=\operatorname{sgn}(p_X)\frac{T^{4/3}}{C_X\sqrt{T^2+\lambda^2}},\qquad
\frac{dY}{dT}=\frac{\lambda T^{-2/3}}{C_\perp\sqrt{T^2+\lambda^2}}.
\]

Hence the magnitude formulas (4)-(5) are right, with the signs recovered separately exactly as stated. Differentiating under the integral sign gives the package's signs:

\[
\partial_\lambda Q_X=-\frac{\lambda I}{C_X}<0,\qquad
\partial_\lambda Q_\perp=\frac{I}{C_\perp}>0,
\]

\[
\partial_{T_r}Q_X=\frac{T_r^{4/3}}{C_X\sqrt{T_r^2+\lambda^2}}>0,\qquad
\partial_{T_r}Q_\perp=\frac{\lambda T_r^{-2/3}}{C_\perp\sqrt{T_r^2+\lambda^2}}>0.
\]

The determinant is not merely positive abstractly; it simplifies to

\[
\mathcal D
=\frac{I}{C_XC_\perp}\frac{T_r^{4/3}+\lambda^2T_r^{-2/3}}{\sqrt{T_r^2+\lambda^2}}
=\frac{I\sqrt{T_r^2+\lambda^2}}{C_XC_\perp\,T_r^{2/3}}>0.
\]

I also ran an ad hoc scratch recheck from the metric with my own Simpson quadrature, separate from package code: `bad_cases = 0`, `max_det_formula_error = 1.33e-15`, `max_zero_shift_alpha_error = 4.44e-16`.

### 2. Fixed-`Q_X` monotonicity, properness, and both principal limits

The global inverse argument in [EXACT_DERIVATION.md](/work/g341_review/g341/EXACT_DERIVATION.md:136) is valid for every mixed lift with `q_X>0`. For each finite `\lambda`, `Q_X(T_r,\lambda)` is continuous, strictly increasing in `T_r`, and diverges like `\int T^{1/3}dT`, so there is exactly one `T_r=L(\lambda)`. Because `\partial_\lambda Q_X<0<\partial_{T_r}Q_X`, one gets `L'(\lambda)>0`, and along the fixed-`Q_X` curve

\[
\frac{dQ_\perp}{d\lambda}\Big|_{Q_X}=\frac{\mathcal D}{\partial_{T_r}Q_X}>0.
\]

Properness is also established: for fixed positive `q_X`, finite `L(\lambda)` cannot persist as `\lambda\to\infty` because then `Q_X` would collapse like `O(\lambda^{-1})`. Once `L(\lambda)\to\infty`, the lower bound in (14) forces `Q_\perp\to\infty`. So `\lambda\mapsto Q_\perp(L(\lambda),\lambda)` is continuous, strictly increasing, and onto `[0,\infty)`.

That proves one mixed future null leg per universal-cover lift component with `q_X>0,q_\perp>0`. The package does not silently overuse this argument: it separately takes the principal boundaries from the exact G340 limits, and those limits are regular in Cartesian projective charts via (10)-(11). Restoring the `X` sign and transverse azimuth then covers every nonzero lift, including both principal families.

### 3. No interior conjugate caustic

The no-caustic claim is justified, but only in the bounded form actually written in [EXACT_DERIVATION.md](/work/g341_review/g341/EXACT_DERIVATION.md:131) and [STATUS_LEDGER.tsv](/work/g341_review/g341/STATUS_LEDGER.tsv:19).

On the mixed stratum, the cone map parameterized by `(T_r,\lambda,\phi)` has rank 3 because:

- `\partial_{T_r}` has nonzero `T` component.
- The fixed-`T_r` direction derivative in `(Q_X,Q_\perp)` has nonzero 2x2 determinant `\mathcal D`.
- The azimuth derivative has norm `Q_\perp>0`.

At `\lambda=0` and `\mu=1/\lambda=0`, the apparent singularity is only polar chart collapse; the Cartesian expansions (10) and (11) provide nonzero linear terms, so the rank persists in regular direction charts. Since `dT/ds=\omega>0`, replacing affine parameter by `T_r` is legitimate on each future leg, so this is enough to exclude positive-time interior conjugate points on this one future cone from this one emission event.

The restriction matters. The package keeps it restricted to the exact supplied Taub--Kasner metric, `T>T_e>0`, the universal cover, and this one future null cone. It does not support any generic, perturbed, stability, or all-cones theorem, and it does not claim one.

### 4. Direct Levi-Civita transport, quotient rotation, and G269 mismatch

The screen-transport section in [EXACT_DERIVATION.md](/work/g341_review/g341/EXACT_DERIVATION.md:226) is correct.

With the orthonormal frame

\[
e_0=\partial_T,\quad e_1=a^{-1}\partial_X,\quad e_2=b^{-1}\partial_Y,\quad e_3=b^{-1}\partial_Z,
\]

the only relevant expansion rates are `H_1=-1/(3T)` and `H_\perp=2/(3T)`. Writing

\[
n=ce_1+se_2,\qquad S=-se_1+ce_2,
\]

with

\[
c=\operatorname{sgn}(p_X)\frac{T}{\sqrt{T^2+\lambda^2}},\qquad
s=\frac{\lambda}{\sqrt{T^2+\lambda^2}},
\]

one gets

\[
\nabla_{e_0+n}S=\frac{cs}{T}(e_0+n),\qquad \nabla_{e_0+n}e_3=0.
\]

Then for `\ell=\alpha(e_0+n)` and `\mathcal J' = cs/(T\alpha)`, the exact parallel pair is

\[
E=S-\mathcal J\ell,\qquad Z=e_3.
\]

So the null screen quotient sees zero intrinsic rotation: `E` and the local arrival screen differ only by a null-gauge multiple of `\ell`, while `Z` is parallel outright. But the full transported-source pair plane does not collapse to the target-local pair plane, because the transported source clock decomposes with

\[
W=\alpha_r\mathcal J_r E.
\]

Since the integrand of `\mathcal J` has fixed sign `\operatorname{sgn}(p_X)` on every mixed ray and vanishes only on the principal families, `W\neq0` exactly for mixed rays. That is the correct distinction: trivial null-screen-quotient rotation does not force vanishing G269 mismatch.

### 5. Unique mixed zero-shift direction and G298 regularity

The zero-shift formula in [EXACT_DERIVATION.md](/work/g341_review/g341/EXACT_DERIVATION.md:194) is correct. Writing `R=T_r/T_e>1` and `x=\lambda/T_e`, the condition `r=1` is `\alpha_r=1`, i.e.

\[
R^{-4/3}\frac{R^2+x^2}{1+x^2}=1.
\]

Solving gives

\[
x^2=\frac{R^{4/3}}{R^{2/3}+1},
\]

which is unique because `x^2` is uniquely determined and positive. This direction is genuinely mixed, so `W\neq0` there. Therefore zero ordered frequency depth does not erase the complete endpoint relation.

The G298 plane statements also hold in the bounded sense claimed. The determinants

\[
\det h_T=-r^2(1+A^2)<0,\qquad \det h_L=-r^2<0
\]

show both pair-plane projections remain regular, and their separator is proportional to `-r^2W`, hence nonzero on every mixed ray including the zero-shift one. So the two regular pair planes stay distinct; the package does not silently choose one as the physical kernel input.

### 6. Reversal, physical return, winding, cut/tie, and per-lift typing

The distinctions stay clean.

- Mathematical reversal flips the ordered frequency depth sign while preserving the even `\Gamma`; it rescales the mismatch norm by `r^2`, as stated in (31).
- A later physical return is a separate future leg, not the same mathematical branch run backward.
- Compact quotient multiplicity comes from distinct lattice lifts `q_\ell=\Delta x+\ell`, not from multiple solutions within one fixed lift.
- Cross-lift arrival ties or cuts are quotient-branch phenomena. They are not interior conjugate caustics of a single universal-cover branch.

This is one of the stronger parts of the package: it consistently separates branch multiplicity from per-lift uniqueness and keeps quotient branch structure distinct from caustic structure.

### 7. Replay, implementation independence, hostile controls, and circularity

The registered replay in [COMMANDS.md](/work/g341_review/g341/COMMANDS.md:3) ran successfully in the writable mirror. My no-write runs gave:

- production replay: `8992/8992`;
- independent direct metric/Christoffel replay: `4400/4400`;
- hostile controls: `16/16`;
- aggregate verifier: `20/20`, with unchanged-byte snapshot passing.

The aggregate verifier in [verify_package.py](/work/g341_review/g341/verify_package.py:54) is an integrity gate, not an automated proof engine. It verifies frozen-source hashes, replay success, no-write behavior, hostile-control status, and that the sealed prose contains the expected bounded claims. That is appropriate, but it should not be confused with independent symbolic proof.

The analytic proof work is in [EXACT_DERIVATION.md](/work/g341_review/g341/EXACT_DERIVATION.md:66), and that is where global uniqueness and no-caustic support actually live. The numerical scripts in [derive_nonprincipal_relation.py](/work/g341_review/g341/derive_nonprincipal_relation.py:68) and [verify_nonprincipal_independent.py](/work/g341_review/g341/verify_nonprincipal_independent.py:27) are regression and reconstruction support.

The direct verifier is genuinely implementation-distinct: it reconstructs the metric, null tangent, endpoint map, inverse, Christoffel transport, and RK4 carry without importing production code or production results. But it is not premise-independent. It uses the same supplied metric, same observer setup, same branch definition, and same bounded source scope. That is the right distinction, and I do not treat the second script as an independent physical premise test.

No circularity that would invalidate the bounded result appears here, because the numerics are not the sole support for the global claim and the package explicitly says they are not.

### 8. Silent imports of physics, route, population, scale, `X_max`, or canon

I do not find a silent import of electromagnetic transfer physics, source/detector modeling, physical route selection, observer population, topology selection, occupancy, stability, absolute scale, `X_max`, or canon. The exclusions and open boundaries are stated consistently in [REVIEW_SCOPE.json](/intake/REVIEW_SCOPE.json:4), [STATUS_LEDGER.tsv](/work/g341_review/g341/STATUS_LEDGER.tsv:17), and [AUDIT_REPORT.md](/work/g341_review/g341/AUDIT_REPORT.md:41).

The package stays metric-led. It derives null geodesic timing/frequency/screen transport from the exact metric and explicitly leaves emission, brightness, spectrum, absorption, detection, branch population, and physical protocol questions open.

## Bottom line

As a fresh adversarial review of the sealed intake, I accept the bounded G341 conclusion exactly as bounded. The exact Taub--Kasner metric supports the mixed endpoint formulas and signs, a strictly positive endpoint determinant, one future null solution per nonzero universal-cover lift with both principal limits handled, no positive-time interior conjugate caustic on this exact future null cone, zero null-screen-quotient rotation with nonzero mixed G269 mismatch, one unique mixed zero-shift direction still carrying nonzero mismatch and distinct regular G298 pair planes, and a clean separation among reversal, physical return, lattice winding, cut/tie structure, and per-lift uniqueness.

ACCEPT_G341_BOUNDED_NONPRINCIPAL_NULL_RELATION_AND_SCREEN_CARRY

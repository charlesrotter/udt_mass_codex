# External G344 Review

Scope respected: I inspected the sealed intake at `/intake`, copied it to `/work/g344_intake_copy`, ran only the registered dependency-free checks from the writable copy, and did not edit intake evidence or use network/package access.

## Authentication

- `REVIEW_SCOPE.json`, `REVIEW_MANIFEST.tsv`, and `REVIEW_MANIFEST.sha256` are mutually consistent.
- The detached seal matches the manifest hash exactly: `c12c583fb415d707f372f43073c8ba06f4e4731e241c833778e35e1774d9f1a3`.
- The manifest lists 29 payloads excluding `REVIEW_MANIFEST.tsv` and `REVIEW_MANIFEST.sha256`.
- The actual payload set under `/intake` also contains exactly 29 files.
- Every listed payload matched its recorded byte count and SHA-256 digest.

## Findings By Severity

### High

No high-severity findings.

### Medium

No medium-severity findings.

### Low

No low-severity findings that block the bounded grade.

## Substantive Review

1. `B` invertibility: accepted. In the supplied G343 derivation, each channel has
   `B_j(T1,T0) = const * y_j(T1) y_j(T0) * integral_{T0}^{T1} w_j(u) du`
   with strictly positive prefactor, positive `y_j`, and positive integrand `w_j` on `T>0`. Therefore `sign(B_j)=sign(T1-T0)` and `B_j=0` iff `T1=T0)`. This is an analytic sign argument from the reduction-of-order integral, not a sampling claim. Because the parallel-screen `B` block is diagonal in the supplied chart, `det B = B_parallel B_Z > 0` for every noncoincident positive endpoint pair, in either order, including both principal limits.
2. Type-I generator: accepted. Solving `x1 = A x0 + B p0` gives `p0 = B^-1(x1-Ax0)`. Using the symplectic block identities gives symmetry of `D B^-1` and `B^-1 A` and the identity `C - D B^-1 A = -B^-T`. The displayed quadratic representative therefore yields `p1 = +partial_(x1) S10`, `p0 = -partial_(x0) S10`, and reconstructs the full map with the stated source sign and transposes.
3. Mixed Hessian and density: accepted. For the homogeneous representative, `K10 = -partial_(x1) partial_(x0) S10 = B^-T`, so `det K10 = 1/det B` and `Delta10 = 1/abs(det B) > 0`. Under independent endpoint `O(2)` frame changes, `K` transforms with one index at each endpoint and its determinant acquires the endpoint orientation factors, so the text’s tensor/bidensity typing is correct.
4. Qualification: accepted. The symplectic map fixes all endpoint-position-dependent quadratic coefficients but is blind to an additive `k(T1,T0)`. Exact composition and reversal force `k` to satisfy the cocycle and antisymmetry laws, and on a one-dimensional interval that is exactly an endpoint coboundary `f(T1)-f(T0)`. The `k=0` homogeneous normalization chooses a representative only; it does not change `K` or `Delta`. The proof trail shows this was recorded before accepted reruns at commit `9701e595`.
5. Composition and density sewing: accepted. From block composition, `B20 = A21 B10 + B21 D10`, hence
   `H1 = B21^-1 A21 + D10 B10^-1 = B21^-1 B20 B10^-1`.
   Since `B10`, `B21`, and `B20` are invertible whenever outer endpoints are distinct, stationary elimination gives `S20 = stat_(x1)(S21+S10)` and determinant sewing gives `Delta20 = Delta21 Delta10 / abs(det H1)`. The accepted runs explicitly cover all six endpoint orderings in one common affine gauge.
6. Reversal, affine weights, reference covariance, screen covariance: accepted. In common affine gauge, reversal gives `B01 = -B10^T`, `S01(x0,x1) = -S10(x1,x0)`, and `Delta01 = Delta10`. Common affine rescaling sends `B -> B/a`, hence `S -> a S`, `K -> a K`, and `Delta -> a^2 Delta`. Independent endpoint derivative-unit normalizations are only conformally symplectic unless the scales match, so rejecting them as one bare canonical chart is correct. Reference-event change leaves the underlying G343 blocks invariant, so the generator and density are likewise invariant. Independent endpoint screen rotations/reflections act with the stated endpoint indices and orientation weights.
7. G342 recovery, principal limits, coincidence, compact lifts: accepted. The source-normalized specialization `T*=T0`, `nu=1` recovers the G342 determinant exactly. Both principal limits remain regular away from coincidence: the longitudinal family reduces to the free generator/density, and the transverse family keeps both nonzero `B` entries for `T1 != T0`. Coincidence is the only type-I chart pole because `B=0` only there. Compact lifts are retained as labels and are not summed or selected anywhere in the supplied derivation.
8. Evidence sufficiency: accepted for the bounded grade. I replayed the registered commands in `/work/g344_intake_copy/g344` and got production `13580/13580`, independent `4882/4882`, hostile `14/14`, and aggregate no-write `19/19`, with no byte changes during the package replay. The independent route does not import production or a G343 implementation and instead rebuilds the scalar basis by Simpson quadrature, checks finite endpoint gradients/Hessians, and integrates state plus on-shell action by RK4. Tolerances are consistent with the documented finite-difference and ODE route. I did not find a shared-code false-independence failure.
9. Forbidden promotion: accepted. The intake repeatedly and explicitly rejects promotion of this endpoint generator/bidensity into a spacetime action, quantum amplitude, electromagnetic/light transfer law, flux/luminosity law, observational distance, route/population or occupancy selector, stability theorem, matter/mass law, absolute scale, `X_max`, or canon. I found no silent promotion that contradicts the bounded scope.

## Scratch Check

I also ran a separate one-off reconstruction from the published G343 formulas alone, without importing the package scripts. That scratch check independently reproduced the core identities numerically at expected floating-point scale:

- symplectic reconstruction identity error `~1.4e-14`
- generator-to-momentum reconstruction error `~1.4e-14`
- composition/Hessian/density sewing errors `~1e-11`
- reversal, screen covariance, affine weight, and reference covariance errors `<=1e-12`
- longitudinal and transverse principal formulas matched directly

This does not replace the analytic proof, but it reduces the chance that the package only agrees with itself internally.

## Chronology Judgment

The pre-acceptance qualification did not change the scientific alternatives. It corrected an over-strong uniqueness phrase in the preregistration and exposed a generator gauge freedom that is invisible to the recovered map, mixed Hessian, and determinant bidensity. The accepted reruns were performed after that qualification was banked, and the bounded landing, formulas, tolerances, domain, and maximum conclusion were not broadened.

## Residual Risks

- The compact-lift retention checks inside the executable scripts are mostly documentary rather than computationally substantive: they assert fixed tuple labels rather than exercising a data path that could accidentally sum or select lifts. This is a real testing limitation, but it does not overturn the bounded claim because the supplied mathematics never introduces multi-lift aggregation logic in the first place.
- The aggregate verifier contains several text-token gates. Those are appropriate as packaging guards, but they are not substitutes for the underlying analytic derivation. Here that is acceptable because the analytic derivation and the direct executable replays were both present and consistent.

## Verdict

ACCEPT_G344_BOUNDED_SCREEN_ENDPOINT_GENERATOR_AND_BIDENSITY

# ALP1 mathematical direct review

**Verdict: VERIFIED-WITH-CAVEATS / accept the frozen candidate at its stated
conditional scope.** I found no substantive mathematical defect requiring
repair. This verdict neither adopts AMS/SCN2/SCB2 nor establishes any full-UDT
countermodel, empirical recovery regime or new physical law. It is not a final
attestation of an integrated edition that has not yet been presented.

Reviewer `/root/alp_review_math`, fresh context, inherited model; exact model ID
unavailable. Parent startup/full406 evidence is attributed to the recovery
receipt. Own branch/HEAD/status were checked at
`d8171f965e7759c11c16aecf4dec57d6d641f763`. SOURCE_FIRST and its hash record
preceded exposure to this candidate. I then read the joint candidate, both
researcher candidates, their initial approaches, SCIENCE_FREEZE, B's saved
Fraction output/receipt and its freeze. I did not read/import B's checking
implementation, the campaign notebook, PRIMARY_METHOD_NOTES, or the other
current reviewer's argument/verdict. Prior source verdicts, including FAC1,
were exposed and used at their stated scopes.

The reviewed joint candidate hash is
`b510d53aeef4093cbd727d57f2ca3179b59dd3547c1539a95c756bd05513339f`;
SCIENCE_FREEZE hash is
`9a502898d0aac7f7bb0e6eb7dad3d6477617a5d1c2b20405c462221b44d95092`.
Every listed candidate and baseline binding matched disk before the check.
CHECK_PINS records those versions and the independent check implementation.

## Load-bearing mathematical findings

1. **The two angular problems are correctly separated.** Before candidate
   exposure I derived the opposite fixed-arrow source/receiver mean signs in
   SOURCE_FIRST. Differentiating `Lambda l(n)=f l(m)` and taking its Lorentzian
   norm gives `dn²=f² dm²`; the null terms and cross terms vanish. The area
   factor is consequently `p²`, not `p^-2` in the forward direction. The
   candidate correctly uses the inverse factor for reception-sky normalization.
   Its integral and the continuous zero-boost limit agree with my independent
   hand derivation. The finite-map normalization depends on retaining one
   Lambda. Replacing it by a family of finite experiments is precisely the
   extra hypothesis that the candidate tests rather than assumes.

2. **Composition does not restore a lost measure.** The pushforward identity
   for a matched second-stage log ratio is exact. Replacing its measure by
   uniform measure for all continuous integrands is equivalent to equality of
   the measures; accidental equality for one integrand is correctly preserved.
   The no-Lorentz-invariant-probability statement uses the usual Borel sphere:
   rotation invariance uniquely fixes normalized area, changed by a boost.
   It does not preclude carrying a measure covariantly with its Jacobian.

3. **Weighted quartic and normalization coefficients are correct.** Diagonalize
   symmetric E in a spatial orthonormal frame. The elementary moments
   `<n_i^4>=1/5` and `<n_i² n_j²>=1/15` give
   `<(sum e_i n_i²)²>=[(sum e_i)²+2 sum e_i²]/15`. Trace freedom yields
   `2 E²/15`. Multiplying `1+alpha L² E(n,n)+O(L⁴)` by the prepared clock
   expansion gives exactly the candidate's `-alpha E²/15` shift. This checks
   the sign without importing B's tensor-basis implementation. Uniform
   remainders are available only in the inherited fixed-frame small-L scope.

   Independently expanding `exp(-2d)` gives `1-2d+2d²+O(d³)`. Thus its
   quartic coefficient is

       -(4 E²-3 B²)/180 + E²/15 = (8 E²+3 B²)/180.

   It is strictly positive for nonzero Weyl in every fixed timelike frame.
   Hence SCN2/SCB2 fail in that *regional-vacuum* scope, even when AMS holds.
   The moment inversion is a nonsingular two-by-two linear solve and gives the
   displayed E²/B² and variance formulas. The control substitutions match
   B's saved exact values; they are not independent metric reconstructions.

4. **The flatness corollary has the needed quantifiers.** Exact SCN2 at every
   event for all timelike U and sufficiently small L first kills Ric(U,U).
   A symmetric bilinear form vanishing on the open timelike cone is zero by
   homogeneity/polarization. Because this holds on the region, FAC1's regional
   vacuum hypothesis is then available; its positive-square coefficient kills
   Weyl. This proves vanishing full Riemann tensor and local flatness. One
   event, one frame, merely pointwise vacuum, SCB2, or a distant-only law would
   not permit the same argument. The candidate preserves all these limits.
   Conversely a small convex flat laboratory has parallel free clocks and
   `p_+=p_-=1`, independent of global topology.

5. **The actual reverse sky map is legitimate locally.** Use the sourceward
   direction, so the flat limit is `F_0(n)=n`, and transport the central frame
   along A's geodesic as specified. Rescaled regular shooting extends smoothly
   to L=0. Compact-sphere control gives uniform C1 closeness, making dF
   invertible for small L. A proper local diffeomorphism of S² is a covering;
   the homotopy to identity has degree one, so it has one sheet. This fills in
   the global-on-that-small-sphere step behind the candidate's abbreviated
   diffeomorphism argument. The map does not need a common reception event;
   the supplied central transport identifies the different reception rest
   frames. Its Jacobian integrates to one. Jensen and the Delta identity then
   follow exactly, without assigning Delta a physical cause. No distant map,
   explicit J-curvature expansion or optical flux conservation follows.

6. **The finite/distant family is an actual fixed-history clock control.** I
   checked the coordinate connection, preparation and affine-null requirements.
   An independent analytic check of the ratio uses spatial translation
   symmetry: along an affine null ray the conserved covector is
   `q_i=a² dx_i/dlambda`; nullity gives `dt/dlambda=|q|/a` for the future branch.
   Comoving proper clocks measure `omega=|q|/a`, hence R6 gives
   `p=a(t_R)/a(t_E)`. This separately recovers the ratio obtained by
   differentiating incidence. At t=0 the preparation is exactly spacelike
   geodesic and its transported clock is unchanged because `a'=0`.

   Positivity holds for every `k>-2`, including x=0. In conformal coordinates
   the direct rays are straight; their nonzero transverse separation scales
   by positive a at finite reception, so there is no angular caustic on these
   rays. Any finite t gives a regular finite affine segment. There is no
   finite receiving event at D. The manifold itself remains `R times R³`:
   D bounds the future conformal-time budget for this first-signal query, not
   the spatial chart, proper time, or metric domain. No wall, seam or native
   `X_max` is supplied. Reflection proves reverse equality in this
   special family, not in general.

   I checked the inversion substitution including its x² weight, the local
   series inversion, and the tail: `delta=s/(3 x³)+O(s x^-5)` for fixed k,
   `p~x⁴`. These yield the stated boundary, quartic coefficient and exponent.
   `a''/a` and `(a'/a)²` are continuous on the future and decay as t^-2 for
   each fixed member, proving the claimed bounded unboosted curvature. No
   uniform bound in k or all boosted frames was needed or proved.

## Independent numerical evidence

CHECK_FREEZE was written before launch. A new mpmath implementation directly
integrated `1/a(t)` and solved nearby-emission incidence with separation fixed;
it imports no researcher utility. TPS1 capture ran one CPU worker with one
thread and 2 GiB address-space limit, no GPU and no killing timeout.

- All 37 frozen checks passed; CPU 1.853312957 s, wall 1.903941254 s,
  maximum RSS 34,520 KiB. Capture stdout/stderr hashes were checked afterward.
- For k in `[-1.5,-1,0,1,3]`, direct infinite integrals matched common D=1
  within `1e-35` at 45-digit precision. Nearby-emission derivatives had maximum
  relative discrepancy `5.83e-12`; root residuals met `1e-35`.
- The finer local quartic residual coefficients had maximum absolute error
  `8.50e-7`. Tail-ratio deviations decreased on x=20,40,80; the largest last
  deviation was `9.38e-5`.
- Direct crossing integration gave
  `1.1655711615479214833812079732600786332`, agreeing with the repaired formula.
  The preserved incorrect `pi/4` value differs by
  `0.3801729981504731737655471274402029121` and is explicitly rejected.

These are high-precision floating computations, not exact arithmetic or interval
enclosures. The formulas' proofs remain analytic. The run checks a representative
finite parameter set and cannot establish universal parameter coverage by itself.
No scientific threshold was changed, no failing output discarded, and no check
was rerun merely for packaging. Raw outputs and command/version metadata are
under `checks/finite_01.{stdout,stderr,json}`.

## Defects, survivors and return decision

No substantive defect was found. The earlier research-message crossing error
was already explicitly corrected and preserved before this frozen candidate;
the actual candidate passes an independent calculation. No scientific repair
is requested. The typographic `folds,+multiple` in B's fixed draft is harmless
and need not be edited in historical evidence.

The strongest survivor is narrower than a UDT sign-selection law: angular
normalization cannot automatically justify this prepared sign; an exact proposed
normalization would be exceptionally strong; the two prepared moments infer
conditional curvature norms; and even a common distant boundary and exponent
do not force a local sign in the supplied kinematic class. These conclusions
must survive unchanged in headlines, the central integration and lay brief.

I specifically challenged stopping after these negatives. The campaign did
continue past its first objection: it developed a quantitative trial law,
tested its failure, retained a moment diagnostic, formulated an actual angular
map, and tested a separate finite/distant implication. Possible further work
includes computing J_L's curvature expansion or trying another moment closure,
but neither presently has an identified argument connecting it to the owner's
additional positional requirement. Such work could improve a measurement tool;
it does not presently change this attribution/sign decision. A specified
physically justified finite-domain comparison, or a new explicit conjecture with
a discriminatory use, could reopen the route. This is a justified decision-ready
return under the work order, not exhaustion of all mathematics, literature or
UDT consequences. No automatic successor or mandatory new postulate follows.

## Omissions and acceptance limits

FAC1's general quartic proof and original Kasner/Kerr/plane-wave geometry remain
inherited; this review did not independently reconstruct them. No Kerr ray solve,
all-frame classification, empirical filter test, native field/source/scale
assignment, instrument error model, nonvacuum moment theorem, global sky map,
full optical reciprocity theorem, exhaustive literature search, formal proof,
cross-model review or human specialist review was performed. The new finite
control is explicitly nonvacuum and proves no full-postulate counterexample.
The original fixed candidates and protected/unrelated work remain unchanged.

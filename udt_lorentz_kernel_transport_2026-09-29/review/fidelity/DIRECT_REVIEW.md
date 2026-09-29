# LKT1 direct fidelity and independent-math review

**Verdict: VERIFIED-WITH-CAVEATS for the frozen conditional candidate. No
substantive mathematical or source-fidelity defect found; no scientific repair
requested by this reviewer.** This is a bounded review, not promotion, empirical
validation, native geometry selection, or proof of complete UDT sufficiency or
insufficiency.

Candidate: INITIAL_CANDIDATE.md SHA-256
`600c261ec1662d8a8315034ef362f78563e7c8a193a2ca8fecad2d119ea46d52`.
Reviewer: `/root/lkt_fidelity`, fresh separate context, same inherited model;
exact runtime identifier unavailable. Human/different-model review untested.
Parent startup attribution and original source versions are SOURCE_PINS.json.
SOURCE_FIRST.md, its seal, and the immediate separately sealed numerical
transcription correction predate candidate exposure. No other LKT1 reviewer was
read. DIRECT_CHECK_PLAN.md froze the independent direct-stage scope before the
new code/run; author code/output was read only after that independent run passed.
Parent additionally disclosed one vacuous author check before code exposure.

## Argument and source fidelity

1. **The two forms remain distinct.** The candidate's S exactly sends K to eta,
   conjugates D to the stated signed boost, and simultaneously sends the original
   physical eta to -K. The nonzero D is not an eta isometry in its original
   clock/ruler basis. This faithfully retains the ownership audit §5. It
   establishes a representation equivalence without silently identifying the
   vector spaces/channels of physical transport. Its positive use is preserved;
   it is not presented as an impossibility of any relation to transport.

2. **The existing clock link is recovered at source scope.** Equations(2)-(3)
   match G220 and FSL1 including the orientation repair. Positive frequency,
   future clocks, regular affine-null branch, and the actual intermediate
   direction matter. G176's Phi=-log Z uses the same-correspondence clock leg;
   this is compatibility, not an independent confirmation of G176 or a full
   pair-plane construction. G274 supplies full path-labelled frame composition,
   not projective-vector-only composition. Current W4/W5 remain provisional.

3. **The scalar-homomorphism obstruction has the right quantifier.** The Lie
   brackets span so(1,3), so any smooth real additive character has zero
   derivative; connectedness makes it trivial. The source-first review supplied
   a separate compact-rotation/boost-conjugacy argument. Both leave untouched
   directional cocycles, planar subgroups, path-labelled relations, and
   additional ordinary query data. No full-theory negative inference is made.

4. **The differential bridge uses an actual metric, not only a pointwise germ.**
   The stated Lorentz2 metric, or totally geodesic Lorentz2 surface in the ambient
   metric, supports the required intrinsic connection and ambient identification.
   A generic rank-two pointwise pullback would not. T,L>0, smoothness, x-fixed
   unit clocks, continuous time/spatial frame orientation and a regular connected
   null branch are the relevant restrictions. These are supplied-sector data,
   not derived physical observer/symmetry selection. Large shift is permitted:
   the calculation does not assume that t itself increases along every future
   null branch or that constant-t slices are spacelike. No forbidden division
   by a general null dt/dlambda appears in this sector's transport proof.

5. **Connection, clock sign, and curvature are correct.** Direct coordinate
   Christoffels for h=[[-T²,-T²b],[-T²b,L²-T²b²]], transformed by the inverse
   coframe, give exactly equation(5). Computing the coordinate Ricci scalar from
   derivatives/products of those Christoffels yields equation(9), with the
   stated curvature convention. Direct differentiation of omega=T(k^t+b k^x)
   along affine geodesics independently yields d log omega=-epsilon varpi for
   both null signs. This verifies the clock-depth sign in(7), not merely the
   formal matrix exponential. In SO+(1,1), one fixed generator suffices, and the
   integral/exponential in(6) is exact. Endpoint changes of physical clocks are
   correctly separated from interior frame changes.

6. **The complete record and the extra chart restriction are respected.** G176's
   m=TL is a spatial density for the supplied local record; G180 guarantees its
   one-dimensional interval integration, not a t-preserving spacetime
   coordinate when m_t is nonzero. The Milne control retains m=1+t and has actual
   Z=2 despite local Phi_local=0. It refutes only scalar-only reconstruction in
   its supplied class. Coordinate curvature recomputation confirms flatness.
   Its rest-coordinate clocks are ordinary proper clocks, not intrinsically
   abnormal clocks; no physical positional cosmology is inferred from it.

7. **The negative consequence retains its extra identification.** In the
   diagonal reciprocal chart, Phi_clock=Delta phi-2 integral phi_t dt follows
   for either fixed null orientation. Equality with that *same* presentation
   phi difference on all sufficiently short segments forces phi_t=0. Finite
   cancellation alone does not. Requiring a different endpoint potential is a
   distinct proposition: for example phi=a(t)+b(x) admits psi=-a(t)+b(x) in this
   sector. The candidate does not exclude it. Stationarity then concerns only
   these x-fixed Killing clocks, so the SGE1 two-way exclusion follows without
   becoming a theorem about arbitrary moving clocks, evolving geometry,
   transverse sectors, or a separately isolated positional contribution.

8. **Path and curvature claims stay at their stated level.** On a contractible
   Lorentz2 patch, all-curve frame transport is path independent iff dvarpi=0.
   The real boost group has no nonzero periodic rapidity that could hide a small
   loop. Stokes comparison requires the two paths plus a spanning oriented
   surface in the domain. Global periods remain relevant beyond that patch.
   Scalar frequency endpoint exactness can survive nontrivial full transport;
   it must not be read as a flatness condition. The candidate's statement is
   explicitly about full frame transport for all curves and is sound. Four-
   dimensional transverse transport is outside the one-generator restriction.

## Actual independent evidence and author-check assessment

The source-first run preserved 29 Fraction/SymPy controls. Its initial report's
three illustrative rational values were transcribed incorrectly; the immediately
sealed SOURCE_FIRST_CORRECTION.md points to the actual stdout values
f_total=681/359, wrong-direction total=1843/1077 and Z=359/681. The correction
changes no calculation or argument and precedes candidate exposure.

The direct-stage independent script reconstructs the full general T,L,b
connection and curvature from the coordinate metric, then independently checks
the affine-null frequency contraction. **22 exact checks passed**, exit zero,
empty stderr, **4.173s**, peak child RSS **54,024KiB**. An active-shift example
T=exp(t+x), L=exp(2t-x), b=tx has independently reconstructed R(0,0)=2; this
ensures that a zero-curvature/sign-insensitive witness is not carrying the test.
Other checks cover the Milne arrival map/flatness, reciprocal curvature, and
both forms under the candidate's basis change. The scripts and stdout/stderr/
resource receipts are retained in this directory. Limits were60s/512MiB, CPU
only, with OPENBLAS/OMP/MKL thread environment one.

This implementation was independently written before viewing author code;
it shares Python/SymPy and the ordinary Christoffel mathematical method. This
is not a different CAS, independent underlying simplifier, or machine-checked
formal proof. General formulas were also checked analytically above.

Afterward I read the author's frozen check_bridge.py, stdout and resource
receipt. The recorded30 items include the vacuous assertion `1-1`; exclude that
item from meaningful check totals. The remaining29 are exact algebra/control
items, with overlapping content, and do not constitute29 independent physical
confirmations. Author code was inspected, not rerun by this reviewer. Its
nonzero wrong-form comparisons are discriminating controls; they should not be
advertised as a comprehensive injected-mutation harness. Its limited curvature
control is supplemented by this reviewer's full symbolic T,L,b calculation.
The frozen evidence should remain unchanged, with these counting qualifications.

## Limits and integration conditions

No substantive repair is required for INITIAL_CANDIDATE. Preserve its domain
language and the distinction between the original presentation potential, local
completed scalar, and actual correspondence depth during central integration.
State plainly that another endpoint potential is not excluded by the same-phi
stationarity result. This is an explanatory scope clarification already entailed
by the candidate, not a new scientific theorem/adoption.

No full source package replay, full406 audit, empirical data check, global
caustic/singular analysis, arbitrary-four-dimensional transport calculation,
source/action/carrier test, or native dynamics solve was performed. These omitted
axes are outside this direct review's dependent claims. Parent banking audit
and central/version-binding integration review remain separate required gates.
I have not reviewed future integrated bytes; this verdict cannot be reused as
an attestation to them without that later read/check. Both positive gains and
negative limitations remain conditional and unpromoted.

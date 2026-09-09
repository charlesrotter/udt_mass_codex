# LG2 final adversarial review

Verdict: VERIFIED-WITH-CAVEATS after one focused source-preserving repair.
This verdict covers the effective candidate CANDIDATE.md PLUS REPAIR.md, not
the initial candidate alone. The result remains UNPROMOTED conditional
mathematics. No unresolved load-bearing objection remains in the declared
restricted family. No scientific grade, premise ownership or canon changes.

Reviewer /root/lg2_review, actual fresh separate context, 2026-09-09.
Exact model UNKNOWN; different-model review UNTESTED. Source-first assessment
and its independent algebra preceded exposure to the parent's LG2 proof/code.
The question and proposed mathematical method were known before review.
This was not a fully blind review of the research direction.

## Versions, exposure and repair history

Baseline grok 78c3092b2120a80c8bbabb8024b4448d27c36a00 was independently
verified with status. Parent owned shared sync and full365; this reviewer
inspected the actual failing full365 capture but did not rerun or repair it.
NOT_PASSED at G325 replay_exact:DERIVATION_RESULT.json remains controlling.

SOURCE_FIRST.md was sealed and transmitted at 17:39:48 UTC with SHA256
`bebc4ef9a2af7ac3af14232f40b891ed6691ef08c474bb7eef66df68f9535f36`.
The independent algebra completed at 17:41:09 UTC before the first LG2
candidate read. The initial candidate SHA256 is
`3f21ac35f37bdff8309651d06bb1be5aadce5948bef5ff5d0ec95efe40086537`;
all five original freeze entries independently matched. Then I read the
candidate, author code and actual author stdout/capture. I did not rerun author
code or count its checks as reviewer-independent evidence.

The initial review caught a source-interface defect: raising the source's
covector momentum residual with the varying metric changes its derivative
at the nonlawful interpolation. INITIAL_DIRECT_REVIEW.md preserves the precise
objection, survivor and smallest repair. The author retained the original
candidate and supplied REPAIR.md with SHA256
`b10226648340d45bfbee1e44bae9a50f530826ec3aefe25f8bbde0bb32b3a262`.
REPAIR_SHA256SUMS also pins METHOD_ACCESS.md; both entries matched.

The repaired map is exactly the source's covector J_i=-2M_i, rho=H. P is its
derivative, and the formal adjoint uses the source metric pairing at the fixed
interpolation base, whose metric is I. No independently varying metric-raising
factor remains in C. This closes the identified defect without changing the
equation's zero set, witness data, boundary prescription or conclusion. The
extra derivative of a raised map is independently exhibited by direct_checks.py.
The author's later optional repair diagnostic was not read or replayed and is
not part of the independence claim. No second repair was required or performed.

## Load-bearing mathematical assessment

1. Premises and lawful data. The G310/G312 owner-provisional bounded equation
   and G303/G315 constraints remain explicit. G324 supplies the comparison
   datum, not a selected universe. Agreement of both initial tensors with it
   on an open exterior fixes the connected comparison scalar to Lambda=0.
   The prescribed circle family has trace K=-3a and norm-squared 9a^2, with
   flat gamma, so both the Hamiltonian and three momentum equations vanish
   exactly in the interior. All signs agree with K=-L_n gamma/2.

2. Seed versus solution. The cutoff seed has the displayed nonzero defects
   H=chi(1-chi)|Delta K|^2 and M_i=Delta k_i partial_i chi. Its endpoint
   lawfulness does not make it a solution. For fixed annulus and cutoff those
   errors have smooth support away from both boundaries and tend to zero in
   every required fixed finite weighted norm. Both gamma and K remain free
   in the correction; no CMC, conformal-flatness or one-dimensional reduction
   has been imposed on the annulus PDE.

3. Actual literature interface. I inspected Chrusciel--Delay
   gr-qc/0301073v2, equation (2.1), Proposition 3.3, Theorems 3.6/3.9 and
   5.9, Proposition 5.10, Corollary 5.11, relevant weighted-space definitions
   and boundary scaling, and the section 8.9 uniqueness/symmetry application.
   The compact annulus has smooth boundary components and a positive smooth
   defining function with nonzero derivative at each boundary. Definition 5.3
   is satisfied by taking its smooth reference metric to be I itself. The
   background curvature/second-fundamental-form limits (5.10) hold directly.
   Derivatives are bounded, and required scaling follows from a defining
   function comparable to boundary distance; harmless positive normalization
   of the local scale yields the Appendix B coordinate balls. This is covered
   by the source's equivalent-norm convention, not a changed domain.

4. Fixed kernel and weights. The source inverse is projected off the fixed
   reference kernel, with the nearby fixed-base metric used for orthogonality.
   It does not require that interpolated or corrected data have the same KIDs.
   Here the reference weighted kernel is precisely the four local LG1 fields.
   Interior elliptic regularity makes any weak kernel field smooth; the
   reviewed local classification excludes extra fields. The four smooth
   fields belong to the decaying weighted potential spaces and their compact
   support closures: cutoffs approaching each boundary have vanishing weighted
   error because exponential decay dominates derivative powers. There is no
   scalar-lapse mode. The factor exp(-sigma/d) in the variational potential
   weight is distinguished from growing exp(+sigma/d) output norm labels;
   METHOD_ACCESS.md correctly keeps the source correction and residual factors.

5. Symmetry and EXACT residual removal. The eight coordinate reflections act
   on the four kernel modes by sx, sy, sz, sy*sz. Their common invariant space
   is zero, whereas central inversion alone leaves the fourth mode. The source
   covector constraint operator is natural under all these diffeomorphisms,
   including orientation reversals. The seed, boundary weights, base metric
   inner product and reference subspace are invariant, so the adjoint and
   projection commute with the group. Intersecting the finitely many images
   of the inverse neighborhood makes the uniqueness argument valid in a common
   invariant neighborhood. It gives invariant correction potentials, hence
   invariant corrected data. Their weighted full residual belongs to the
   reference kernel by the projected equation, and is group invariant; hence
   it vanishes. This proves the full nonlinear constraints, not a linearized
   or finite-mode residual. Averaging arbitrary nonlinear solutions is neither
   used nor justified. Only the inverse-slice potential is locally unique.

6. Smooth matching and smallness. Proposition 5.10/Corollary 5.11 provide
   regularity of one small solution and smooth extension of the correction by
   zero. This is not an intersection of unrelated finite-regularity solutions
   with an unproved common parameter radius. Both annulus boundaries receive
   this treatment. Extension patches the prescribed inside and outside tensors
   on the same compact slice. The theorem's smallness plus the relevant
   weighted embeddings controls unweighted C0, so gamma stays positive.
   Choosing the theorem index for a fixed sufficiently high finite norm is
   legitimate. The threshold may depend on all the fixed controls; no
   uniform threshold for shrinking annuli, T0 approaching zero, arbitrary
   C0 perturbations or every Frechet seminorm has been established.

7. Actual smooth development. Smooth compact boundary-free data, positive
   gamma, symmetric smooth K and exact full constraints meet G303/G315's
   explicitly conditional smooth harmonic local-development interface. The
   argument therefore supplies actual local vacuum metrics, conditional on
   that standard PDE method, rather than formal jets or analytic compact bumps.
   Agreement with interior Kasner and exterior Taub patches follows only in
   their justified local domains of dependence and up to the usual geometric
   uniqueness. No common all-time exterior, completeness or stability follows.

8. Geometry versus gauge and dimensional scope. For the exact Kasner interior,
   magnetic Weyl vanishes and the electric eigenvalues are tau*k_i-k_i^2.
   The complex Weyl endomorphism has three distinct eigenvalues for every
   nonzero |u|<1/10 in this candidate, while Taub has a repeated pair everywhere.
   This multiplicity is a spacetime algebraic invariant, not merely an invariant
   of a selected slice. It excludes both a coordinate change and a reslicing
   of Taub. The annulus solve is genuinely on a three-dimensional domain with
   all metric/extrinsic components and all constraints active. Its localized
   departure cannot be an axially periodic slab because it is supported in an
   embedded ball below injectivity scale. Homogeneity of the prescribed interior
   does not make the unrestricted annulus solve one-dimensional. No full
   isometry census, generic absence of symmetry or particle identification
   is being inferred.

## Independent evidence and adverse controls

The pre-exposure script reconstructs the reflection action directly on vector
fields and obtains the zero group-average matrix. It uses a separately chosen
rational Kasner parametrization q near 1, verifies all interior constraints,
forms the Gauss electric tensor, and computes its characteristic-polynomial
discriminant. It also verifies the nonzero defects of the raw cutoff blend.
These are independent algebraic reconstructions of the argument's finite
pieces; the group proof itself uses the same mathematical method identified
in the dispatch. They are not a second proof of the general elliptic theorem.

The post-exposure script computes the candidate family's invariant directly
from traces: D=(tr E^2)^3/2-3(tr E^3)^2. It gives

    D = 6912 a^12 u^2 (u^2-3)^2 (3u^2-1)^6 / (u^2+1)^12.

Every factor is nonzero on 0<|u|<1/10, a>0, which proves the interval claim;
sampled values are controls, not its proof. The same script exhibits the
extra -hJ derivative from variable metric raising.

Three separate intentional red runs preserve actual assertion failures for
central-inversion sufficiency, raw-cutoff sufficiency, and identical raised-map
linearization. They reuse reviewer code and are catch-proof/regression only,
not additional independent implementations. All stdout, stderr, commands,
versions and resource receipts are retained; RUN_RECORD.md gives the details.

## Exact surviving conclusion and omissions

For each fixed supplied T0/background and nested matching domains, every
sufficiently small member of this explicitly prescribed diagonal,
reflection-invariant Kasner family has a smooth exact constraint completion,
with unchanged exterior data on the original compact slice. For the noncentral
members the conditional actual local development differs invariantly from
Taub. This is a restricted sufficient family, not an arbitrary-data criterion,
classification of all completions or proof symmetry is necessary.

Unproved here: the general weighted inverse/regularity and general smooth
hyperbolic theorems themselves; an explicit computable amplitude bound; a
numerical PDE solution or original numerical residual certificate; arbitrary
smooth interior matching; long-time evolution, exterior persistence or stability;
genericity, topology change, mass, source, carrier, action, population or physical
interpretation. No source package/full365 replay, NR1/NR2 proof review, protected
payload access, specialist human review or different-model independence was
performed. Public source bytes are identified in RUN_RECORD.md but kept in a
temporary directory, not committed as a complete external-paper copy.

Disposition: the two-step campaign may return this reviewed conditional,
UNPROMOTED construction for discussion, retaining LG1's limits and this initial
objection/repair history. Full365 remains NOT_PASSED and this review grants no
banking or canon authority.

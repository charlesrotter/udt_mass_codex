# G181 preregistration — completed-pair singular-endpoint classification

Date: 2026-08-19

## Whole question and bounded regime

G180 proves smooth-family descent only where the supplied pair metric is regular and

\[
m(\sigma)=\sqrt{-\det h_\sigma}>0.
\]

G181 asks what the accepted completed-pair construction itself says as one supplied smooth
one-parameter family approaches a single excluded endpoint. The domain is one connected regular
interior interval with one one-sided boundary. This audit classifies endpoint accessibility,
completed-coordinate behavior, scalar-depth limits, removable auxiliary stalls, and the first
primary-metric zero-tangent boundary.

It does not select a physical family, cross a cut/focal/topology-changing branch, derive a global
completion, or use observations.

## Frame and premise ledger

- `pinned-by-THEORY`: on the regular interior, the accepted completed-pair formulas
  `m=sqrt(-det h_sigma)`, `ds=m d sigma`, `det h_s=-1`, and
  `Phi=-1/2 log(-h00_s)` from G176--G180.
- `pinned-by-THEORY`: in the declared primary time-orthogonal spherical family,
  `m^2=v^2+exp(-2 phi) r^2 b^2`.
- `free-and-explored`: every positive smooth interior clock scale `T`, ruler scale `L_sigma`, shift,
  endpoint vanishing/divergence order, and permitted oscillatory limit behavior.
- `free-and-explored`: auxiliary parameterizations and both one-sided orientations.
- `pinned-by-HABIT`: none.
- `OMITTED`: null propagation, non-scalar screen/connection/Jacobi/holonomy transport, multiple
  branches, event/germ selection, ambient global topology, numerical `X_max`, dynamics, action,
  source, matter, bootstrap, radiative transfer, and observations.

The calculation is metric-led. No template endpoint, desired asymptote, fit coefficient, cutoff,
or preferred physical branch is admissible.

## Preregistered claims to test

1. **Interior theorem.** Every positive smooth `m` still gives a smooth strictly monotone completed
   coordinate on the open regular interior.
2. **Endpoint accessibility.** A boundary lies at finite completed ruler coordinate iff `m` is
   integrable there. Otherwise it lies at infinite completed coordinate.
3. **Boundary regularity.** A finite endpoint is a regular completed-pair endpoint only when the
   coefficients of the determinant-minus-one metric in completed coordinate extend to a
   nondegenerate Lorentzian limit. `m -> 0` or `m -> infinity` alone neither proves nor forbids this.
4. **Auxiliary-stall class.** A zero of `m` caused solely by a vanishing auxiliary parameter speed
   may be removable one-sidedly after completed reparameterization. This does not prove that a
   two-sided branch collision, event germ, or immersion extends.
5. **Depth independence.** The tape class depends on the product `m=T L_sigma`, while
   `Phi=-log T`; current identities permit finite, positive-divergent, negative-divergent, and
   nonconvergent depth behavior in both finite- and infinite-tape classes.
6. **Power-law census.** For `T=q^a`, `L_sigma=q^b`, `q -> 0+`, the tape is finite iff
   `a+b>-1`, logarithmically infinite at `a+b=-1`, and power-law infinite below it; depth is
   positive divergent, finite, or negative divergent according as `a>0`, `a=0`, or `a<0`.
7. **Primary zero boundary.** At `r>0`, the primary density vanishes iff the complete spatial
   tangent vanishes (`v=b=0`). A radial turn with `b!=0` is not singular. At a regular center the
   angular term vanishes and the radial component controls the first boundary.

## Exact witness census

The production derivation must contain at least:

- all six power-law tape/depth sign classes (finite/infinite tape crossed with the three monotone
  depth classes), including the logarithmic tape threshold;
- one finite-depth example in each tape class;
- one positive, one negative, and one nonconvergent depth example;
- one one-sided removable auxiliary stall;
- one two-sided cusp/branch-warning control whose metric normalization alone does not prove smooth
  immersion carry;
- primary radial, turning, pure-angular, center, and zero-complete-tangent controls;
- a shifted pair-metric control proving determinant and shift bookkeeping survive on the interior.

## Certification and falsification contract

The landing fails or must be narrowed if any of the following occurs:

- endpoint finiteness is not exactly equivalent to local integrability of `m`;
- `m -> 0` by itself forces either universal extendibility or universal failure;
- current identities couple the tape class uniquely to the depth class;
- the power-law threshold or depth signs differ from the preregistered census;
- primary angular turning produces `m=0` with nonzero complete spatial tangent;
- an alleged independent verification imports production code or reuses production classifications;
- any check filters an allowed class for physical desirability rather than characterizing it.

Certification requires an exact symbolic/analytic derivation, a separate standard-library exact
implementation with at least 20,000 rational exponent cases, mutation catches, frozen source
hashes, the full premise verifier, and a fresh read-only adversarial review before banking a final
scientific verdict.

## Maximum conclusion

At most G181 may classify the one-sided endpoint behavior of the already accepted completed-pair
kernel and identify which apparent zero-density boundaries are removable auxiliary stalls. It may
not claim a physical singularity theorem, select a branch, derive a metric-space distance or
`X_max`, or globalize through null, cut, focal, topology-changing, or observational strata.
